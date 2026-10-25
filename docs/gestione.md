# Gestione

## Aggiornamenti

| Componente | Come |
|---|---|
| OpenWISP | rilancia il playbook openwisp2: i pacchetti pip sono `state: latest`, con versioni minime fissate per gli avvisi di sicurezza |
| Moduli nostri | alza la versione in `playbook.yml` di openwisp2 (tag git della release) e rilancia |
| Ruoli Ansible | `ansible-galaxy role install -r requirements.yml -p roles/ --force` |
| Firmware dei router | nuova build Jenkins, poi aggiornamento da OpenWISP (mai il router di confine, vedi [capitolo 5](firmware.md)) |
| DNS | playbook di ansible-dns; BIND come da README |
| App | release dal tag, vedi [capitolo 7](app.md) |

Gli avvisi di sicurezza di OpenWISP arrivano per email e su
[GitHub Security Advisories](https://github.com/openwisp). Sul server,
`pip-audit` nel virtualenv di OpenWISP (`/opt/openwisp2/env`) elenca le
dipendenze con vulnerabilità note.

## Backup

- **Proxmox Backup Server**: tutti i CT e le VM, ogni giorno.
- **Database di OpenWISP** (PostgreSQL): incluso nel backup del CT; prima di
  un aggiornamento importante conviene anche un `pg_dump`.
- **Fuori dall'host**: i secret non versionati (`secrets.yml`, vault,
  `.vault_pass`), la chiave di firma dell'app, il token API di Jenkins.

## Sicurezza

- I secret non stanno mai nei repository: `secrets.yml`, vault di Ansible e
  zone DNS reali sono in `.gitignore`.
- Il server OpenWISP ha un firewall *default drop*: SSH solo dalla rete di
  gestione, RADIUS solo dalla VPN e dalla LAN, i log dei router solo dalla rete
  NINUX.
- I nostri repository hanno CI, CodeQL dove serve, Dependabot, protezione di
  `main` e dei tag, segnalazione privata delle vulnerabilità (vedi il
  `SECURITY.md` di ciascuno).

## Problemi già incontrati

| Sintomo | Causa e rimedio |
|---|---|
| freeradius non parte al primo deploy | nginx non risponde ancora: riavvia nginx e freeradius, rilancia il playbook |
| Router fermo su «configurazione modificata» | l'agente openwisp-config è morto durante l'apply: usa il fork ([capitolo 4](moduli.md)); sul router `kill -USR2` al processo principale |
| Router in loop «checksum mismatch» | corsa tra modifiche ravvicinate in OpenWISP: risalvare la config del device |
| ZeroTier offline dopo un riavvio del router di confine | l'orologio parte nel 2100 (RTC): riavviare ZeroTier dopo l'NTP |
| Il portale dell'hotspot non si apre | certificato `wifiauth` scaduto o walled garden incompleto: controlla il cron `sync_uspot_cert.py` e il template |
| LuCI aperta dall'app dice «sessione assente» | openwisp-luci precedente alla 0.3.1 |
| Upload del firmware rifiutato (HTTP 400) | `type` dell'immagine sconosciuto a OpenWISP o nome categoria oltre 64 caratteri |
| Togliendo un template il router riprende vecchie impostazioni | openwisp-config ripristina la copia in `/etc/openwisp/stored/`: ripulirla prima |

## Contribuire

La guida è nel repository
[ninux-basilicata-infra](https://github.com/mikysal78/ninux-basilicata-infra):
ogni pagina ha il pulsante di modifica in alto. Le correzioni dei singoli
componenti vanno nei loro repository.
