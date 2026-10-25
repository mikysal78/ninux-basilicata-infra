# 1. Proxmox

Tutti i servizi girano su un host **Proxmox VE**, ognuno nel proprio container
LXC o nella propria VM. Così ogni servizio si ricostruisce da solo, si fa il
backup per conto suo e un problema in uno non tocca gli altri.

## Rete dell'host

L'host è collegato alla LAN di gestione della sede (`10.27.22.0/24`), dietro
il router di confine. I container che devono essere raggiungibili da Internet
(OpenWISP, mail, siti) hanno anche un'interfaccia sulla /29 pubblica.

| Bridge | Rete | Chi lo usa |
|---|---|---|
| `vmbr0` | LAN di gestione `10.27.22.0/24` | tutti i CT e le VM |
| `vmbr1` | /29 pubblica `194.28.98.56/29` | i servizi esposti (es. OpenWISP su `.61`) |

!!! note
    I nomi dei bridge sono quelli più comuni: adattali ai tuoi. Conta solo che
    ogni CT esposto abbia un'interfaccia sulla LAN di gestione e una su quella
    pubblica.

## Container e VM

| Servizio | Tipo | Sistema | Risorse indicative | Note |
|---|---|---|---|---|
| OpenWISP | CT unprivileged | Debian 13 | 4 core, 4–8 GB RAM, 40 GB | accesso a `/dev/net/tun` per ZeroTier |
| Jenkins (firmware) | CT | Debian 13 | 12 core, 24 GB RAM, 200 GB | `nesting=1` per il tmpfs della build |
| DNS hidden primary | VM | Debian 13 | 2 vCPU, 2 GB RAM, 40 GB | creata dal playbook di ansible-dns |
| Monitoring | CT | Debian 13 | 2 core, 2 GB RAM | Prometheus, Alertmanager, Grafana |
| Proxmox Backup Server | VM o host separato | PBS | in base ai dati | backup di CT e VM |

### CT di OpenWISP

ZeroTier ha bisogno di `/dev/net/tun`, che in un CT *unprivileged* va esposto a
mano. In `/etc/pve/lxc/<ID>.conf`:

```
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net/tun dev/net/tun none bind,create=file
```

Poi `pct restart <ID>`. Il resto lo fa il playbook (capitolo 3).

### CT di Jenkins

La build di OpenWrt usa un tmpfs per andare più veloce: il container deve avere
il *nesting* attivo. In `/etc/pve/lxc/<ID>.conf`:

```
features: nesting=1
```

I requisiti di CPU, RAM e disco e l'installazione sono nel capitolo
[Firmware e Jenkins](firmware.md).

### VM del DNS

La crea il playbook di ansible-dns tramite l'API di Proxmox: template Debian
Trixie *genericcloud*, clone con cloud-init, snapshot iniziale. Servono un
token API di Proxmox e lo storage *snippets* attivo: vedi il README di
ansible-dns, sezione
[Proxmox — Provisioning VM](https://github.com/mikysal78/ansible-dns/blob/main/README.it.md#proxmox--provisioning-vm).

## Strumenti utili

- [vmbuilder](https://github.com/mikysal78/vmbuilder): crea VM Proxmox da
  immagini cloud in pochi minuti.
- [pve-io-guard](https://github.com/mikysal78/pve-io-guard): avvisa (anche su
  Telegram) quando una VM satura il disco e può rallentarla da solo.

## Backup

Ogni CT e VM va nei backup di **Proxmox Backup Server**, con una pianificazione
giornaliera. Oltre ai backup interi, conviene tenere fuori dall'host:

- i file di secret non versionati (`secrets.yml` di openwisp2, i vault di
  ansible-dns e di ansible-ninux-openwrt, `~/.vault_pass`);
- la **chiave di firma dell'app Android** (capitolo 7): se si perde, gli
  aggiornamenti dell'app non si installano più sopra quella esistente.

## Controllo

- [ ] I CT si avviano e si raggiungono via SSH dalla LAN di gestione.
- [ ] Il CT di OpenWISP vede `/dev/net/tun` (`ls -l /dev/net/tun`).
- [ ] Il CT di Jenkins ha `nesting=1` (`pct config <ID> | grep features`).
- [ ] I backup su PBS partono e si possono ripristinare.
