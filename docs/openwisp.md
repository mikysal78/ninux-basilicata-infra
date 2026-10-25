# 3. OpenWISP

Il cuore dell'infrastruttura. Il playbook del repository
[openwisp2](https://github.com/mikysal78/openwisp2) installa in un solo CT:

- **OpenWISP** completo: controller, monitoring, network topology, firmware
  upgrader, RADIUS, IPAM, notifiche;
- le **pagine di login Wi-Fi** (openwisp-wifi-login-pages) per l'hotspot;
- il **controller ZeroTier** della VPN dei nodi;
- il firewall **nftables**, **BIRD/Babel**, la raccolta dei **log dei router**,
  il **proxy LuCI**.

Si appoggia al ruolo ufficiale
[ansible-openwisp2](https://github.com/openwisp/ansible-openwisp2) e lo
completa con le nostre parti.

## Prima di iniziare

- CT del [capitolo 1](proxmox.md), con `/dev/net/tun` esposto.
- Nomi DNS e certificati del [capitolo 2](dns.md) già nel CT
  (`/etc/ssl/acme/ninux-nnxx.it.*` e `/etc/ssl/acme/luci.ninux-nnxx.it.*`).
- Una casella di posta per le mail di OpenWISP (nel nostro caso
  `controller@ninux-nnxx.it`, inviata tramite il nostro server di posta).
- Ansible ≥ 2.13 sul computer da cui lanci il playbook.

## Passi

### 1. Repository, ruoli e secret

```bash
git clone https://github.com/mikysal78/openwisp2.git
cd openwisp2
ansible-galaxy role install -r requirements.yml -p roles/ --force
ansible-galaxy collection install -r requirements.yml -p collections/ --force
cp secrets.example.yml secrets.yml   # fuori da git
```

In `secrets.yml` vanno il secret RADIUS degli hotspot, la password SMTP, la
password di PostgreSQL e la chiave della mesh (`mesh_password`, 32 caratteri
casuali). Poi adatta:

- `hosts`: il **nome dell'host nell'inventario è il dominio di OpenWISP**
  (`openwisp.ninux-nnxx.it`), `ansible_host` è l'IP del CT;
- `playbook.yml`: domini delle pagine Wi-Fi, email, relay SMTP;
- `owlp_organizations/`: la configurazione della pagina Wi-Fi di ogni
  organizzazione (vedi sotto).

### 2. Primo lancio

```bash
ansible-playbook -i hosts playbook.yml
```

I play, nell'ordine:

| Play | Tag | Cosa fa |
|---|---|---|
| 1 | — | OpenWISP, PostgreSQL + PostGIS, pagine Wi-Fi, moduli, cron |
| 2 | `zerotier` | controller ZeroTier self-hosted |
| 3 | `firewall` | nftables, policy *default drop* |
| 4 | `bird` | bird2 con Babel |
| 5 | `router_logs` | rsyslog per syslog e netconsole dei router |
| 6 | `luci_proxy` | virtual host nginx del proxy LuCI |

!!! warning "Prima installazione: freeradius"
    Su un CT nuovo l'handler che riavvia freeradius può partire prima che
    nginx risponda su 443, e freeradius non si avvia. Se succede:
    `systemctl restart nginx && systemctl restart freeradius`, poi rilancia il
    playbook (le parti già fatte non vengono ripetute).

!!! warning "Ripristino da backup"
    Se ricostruisci da un backup del database, **carica i dati prima del primo
    lancio** del playbook: altrimenti lo script iniziale crea l'utente
    `admin/admin` e l'organizzazione di default, che poi vanno in conflitto.

### 3. Primo accesso

Vai su `https://openwisp.ninux-nnxx.it/admin`: l'utente iniziale è
**admin / admin**. Cambia subito la password da
`/admin/password_change/`.

Poi, nell'admin:

1. **Organizzazione**: crea la tua (la nostra è *Basilicata*) e annota lo
   **shared secret** della registrazione automatica (Config settings): va nel
   firmware, [capitolo 5](firmware.md).
2. **RADIUS**: in *Organization RADIUS settings* trovi UUID e token
   dell'organizzazione, che servono alla pagina Wi-Fi.
3. **Credenziali SSH** (*Access credentials*): la chiave con cui OpenWISP entra
   nei router per comandi, aggiornamenti firmware e LuCI. Attiva
   **auto add**, così viene assegnata da sola a ogni nuovo device (la nostra si
   chiama *OpenWISP Default Ssh*).

### 4. VPN ZeroTier

La VPN collega i nodi remoti al server e tra loro, e su di essa gira Babel.
OpenWISP **non fa da gateway**: ogni nodo esce su Internet dalla propria
connessione.

1. Admin → **VPN servers** → Add: backend **ZeroTier**, host `127.0.0.1:9993`,
   AuthToken = contenuto di `/var/lib/zerotier-one/authtoken.secret` sul CT,
   subnet `10.27.255.0/24`. Salvando, OpenWISP crea la rete.
2. Admin → **Templates** → Add: tipo **VPN-client**, la VPN appena creata,
   *automatic tunnel provisioning* attivo.

Dettagli e verifiche: README di openwisp2,
[VPN ZeroTier](https://github.com/mikysal78/openwisp2#4-vpn-zerotier).

### 5. Template dei router

I template sono versionati in
[`openwisp-templates/`](https://github.com/mikysal78/openwisp2/tree/main/openwisp-templates)
e si importano nell'admin (Templates → Add, modalità avanzata `</>`), oppure
dalla shell Django come spiegato nel loro
[README](https://github.com/mikysal78/openwisp2/blob/main/openwisp-templates/README.md).

La nostra configurazione: i template **richiesti** vanno su ogni router, quelli
**default** sui router nuovi (si possono togliere), gli altri si assegnano a
mano.

| Template | Default | Richiesto | Note |
|---|---|---|---|
| Banner | sì | sì | messaggio al login SSH |
| Bird2 Babel (routing) | sì | sì | routing tra i nodi |
| SSH Keys | sì | sì | chiavi di accesso degli amministratori |
| DDNS nsupdate (br-lan / LuCI) | sì | sì | nome del router nella zona `dyn` |
| Mesh 802.11s 2.4GHz | sì | no | cifrata SAE, chiave `mesh_password` |
| VPN ZeroTier (client) | sì | no | generato dall'oggetto VPN |
| ZeroTier Moon (orbit hub) | sì | no | il server come *moon* di ZeroTier |
| NTP Servers | sì | no | fuso Europe/Rome e server INRIM |
| Log remoto (syslog) | sì | no | syslog verso il server |
| Nomi dei nodi (hosts) | sì | no | generato dal cron |
| AP WiFi 2.4GHz / dual band / dual SSID | no | no | gli access point |
| Hotspot uspot 2.4GHz | no | no | captive portal con RADIUS |
| Netconsole, usteer, Uplink LAN su wan | no | no | vedi il [capitolo 6](router.md) |
| Router di confine | no | no | config completa del router x86 di confine |

Nel template della mesh, la variabile `mesh_password` va nei *default values*
del template in OpenWISP: nel repository pubblico c'è solo `{{ mesh_password }}`.
Il template DDNS usa la chiave TSIG della zona `dyn` di ansible-dns.

### 6. Pagina Wi-Fi e hotspot

- Per ogni organizzazione un file YAML in `owlp_organizations/` con slug, UUID
  e token RADIUS, testi, loghi, termini e privacy; poi rilancia il playbook.
  La pagina risponde su `https://wifi.ninux-nnxx.it/<slug>/`.
- **Login con Google**: crea un client OAuth in Google Cloud (tipo
  applicazione web, URI di ritorno
  `https://openwisp.ninux-nnxx.it/accounts/google/login/callback/`) e inserisci
  client ID e secret nell'admin, *Social applications*. Il playbook attiva già
  il provider.
- Sui router l'hotspot è il template **Hotspot uspot**. Il *walled garden*
  deve contenere il sito della pagina Wi-Fi, i domini di Google per il login
  social e i siti che vuoi raggiungibili senza login.
- Il certificato del portale sui router (`wifiauth`) viene aggiornato ogni
  notte dal cron `sync_uspot_cert.py`.

### 7. Topology Babel

Una volta sola: admin → Network Topology → Topologies → Add, label
`Babel NINUX`, parser **NetJSON NetworkGraph**, strategy **RECEIVE**,
expiration time **330**. Il cron `topology_babel_feed.py` la aggiorna ogni 5
minuti con i vicini Babel di tutti i router.

### 8. Utente per Jenkins

Il caricamento automatico del firmware usa il token API di un utente con i
permessi sul firmware upgrader. Il token si ottiene con
`POST /api/v1/users/token/` e va cifrato in `ninux.yml` ([capitolo 5](firmware.md)).

!!! note "Un token per utente"
    OpenWISP dà un solo token per utente: se lo stesso utente lo usa anche
    altrove (per esempio l'app Android), revocarlo li blocca tutti.

## Cron installati dal playbook

| Script | Frequenza | Cosa fa |
|---|---|---|
| `sync_node_hosts.py` | 15 minuti | template «Nomi dei nodi»: IP e MAC → nome del nodo |
| `sync_ipam_hostnames.py` | periodico | nomi dei device nell'IPAM |
| `sync_uspot_cert.py` | ogni notte | certificato del portale sui router con hotspot |
| `topology_babel_feed.py` | 5 minuti | topology «Babel NINUX» |
| rotazione dei log dei router | ogni ora | logrotate con i valori scelti in OpenWISP |

## Controllo

- [ ] L'admin risponde in HTTPS con il certificato giusto.
- [ ] La pagina Wi-Fi risponde su `https://wifi.ninux-nnxx.it/<slug>/`.
- [ ] `systemctl status freeradius` è attivo.
- [ ] Il CT ha fatto il join alla rete ZeroTier (`zerotier-cli listnetworks`).
- [ ] `birdc show babel interfaces` elenca le interfacce attese.
