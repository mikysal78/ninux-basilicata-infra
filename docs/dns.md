# 2. DNS e certificati

Il DNS viene prima di OpenWISP perché fornisce i nomi (`openwisp`, `wifi`,
`*.luci`…) e soprattutto i **certificati wildcard** che OpenWISP usa per HTTPS.
Tutto è nel repository [ansible-dns](https://github.com/mikysal78/ansible-dns).

## Come è fatto

- **Hidden primary** in LAN (VM su Proxmox): BIND con le zone, non esposto a
  Internet.
- **Due secondari pubblici** su VPS: rispondono alle query, ricevono le zone
  dal primary dentro un tunnel **WireGuard** (AXFR/IXFR firmati con TSIG).
- **DNSSEC** con firma automatica (Ed25519), chiavi ruotate da BIND.
- **acme.sh** sul primary emette i certificati wildcard con la sfida DNS-01 e li
  copia nei container che li usano.
- **DDNS**: i router con IP variabile aggiornano il proprio nome nella zona
  `dyn` con `nsupdate`.
- **Monitoring**: Prometheus, Alertmanager e Grafana in un CT dedicato.

## Passi

Il README di ansible-dns spiega ogni passo nel dettaglio: qui l'ordine e i
punti che riguardano la nostra infrastruttura.

1. **Controller Ansible**: clona il repository e installa le dipendenze
   ([Prerequisiti](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#prerequisiti)).
2. **VM primary su Proxmox**: template Debian Trixie e VM
   ([Proxmox — Provisioning VM](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#proxmox--provisioning-vm)).
3. **VPS secondari**: ordina le VM e apri il firewall del provider
   ([OVH — VM secondarie](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#ovh--vm-secondarie)).
4. **Chiavi TSIG e vault** con i secret
   ([Setup iniziale](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#setup-iniziale)).
5. **Zone in YAML** (`zones/*.yml`, fuori da git) e deploy completo
   ([Deploy DNS](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#deploy-dns)).
6. **DNSSEC**: dopo il primo deploy pubblica i record DS presso il registrar
   ([DNSSEC](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#dnssec)).

## Record che servono a OpenWISP

Nella zona `ninux-nnxx.it` (`zones/ninux-nnxx.it.yml`); gli `aliases` di un
record A diventano CNAME verso quel nome:

```yaml
zone:
  name: "ninux-nnxx.it"
  a:
    - name: "openwisp"
      ip: "194.28.98.61"
      ipv6: "2a07:7e81:3f1c::18"
      aliases:
        - "wifi"       # pagine di login dell'hotspot
        - "zerotier"   # controller ZeroTier
        - "*.luci"     # proxy LuCI: <uuid>.luci.ninux-nnxx.it
    - name: "gw"
      ip: "194.28.98.57"   # router di confine
  cname:
    - name: "docs"
      target: "mikysal78.github.io."   # questa guida (GitHub Pages)
```

!!! note
    Il formato esatto delle zone è nel README di ansible-dns
    ([Formato zone YAML](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#formato-zone-yaml)).
    Gli indirizzi sono i nostri: sostituiscili con i tuoi.

Per modifiche piccole a una zona con DDNS attivo (come `ninux-nnxx.it`), il
playbook non riscrive la zona: si aggiorna lo YAML per tenerne traccia e si
applica la modifica con `nsupdate` sul primary.

## Certificati

OpenWISP ha bisogno di due certificati, emessi dal primary e copiati nel CT di
OpenWISP in `/etc/ssl/acme/`:

| Certificato | Nomi | Usato da |
|---|---|---|
| `ninux-nnxx.it` | `ninux-nnxx.it`, `*.ninux-nnxx.it` | admin di OpenWISP, pagine Wi-Fi |
| `luci.ninux-nnxx.it` | `luci.ninux-nnxx.it`, `*.luci.ninux-nnxx.it` | proxy LuCI (un host per router) |

Si configurano in `acme_domains` (`inventory/group_vars/all/main.yml` di
ansible-dns), con il CT di OpenWISP tra i destinatari
([Certificati ACME](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#certificati-acme)):

```yaml
acme_deploy_ssh_port: 2400
acme_domains:
  - domain: "ninux-nnxx.it"
    keylength: "ec-256"
    deploy:
      - host: "10.27.22.18"          # CT OpenWISP
        reload_cmd: "systemctl reload nginx"
  - domain: "luci.ninux-nnxx.it"     # copre anche *.luci.ninux-nnxx.it
    keylength: "ec-256"
    deploy:
      - host: "10.27.22.18"
        reload_cmd: "systemctl reload nginx"
```
Il rinnovo è automatico, ogni notte; il reload parte solo quando il
certificato cambia davvero.

!!! warning "Il certificato wildcard non copre i sottodomini di secondo livello"
    `*.ninux-nnxx.it` non vale per `<uuid>.luci.ninux-nnxx.it`: per questo il
    proxy LuCI ha un certificato suo, con `*.luci.ninux-nnxx.it`.

## Controllo

- [ ] `dig +dnssec openwisp.ninux-nnxx.it @ns1.<tuo-dominio>` risponde con le firme.
- [ ] I secondari hanno lo stesso serial del primary.
- [ ] Nel CT di OpenWISP ci sono i due certificati in `/etc/ssl/acme/`.
- [ ] `openssl x509 -in /etc/ssl/acme/ninux-nnxx.it.fullchain.pem -noout -text | grep DNS`
      mostra `*.ninux-nnxx.it`.
