# NINUX Basilicata: l'infrastruttura, passo passo

Questa guida spiega come **ricostruire da zero** l'infrastruttura della rete
comunitaria NINUX Basilicata: dall'host Proxmox fino ai router nelle case,
passando per il DNS, OpenWISP, la compilazione del firmware OpenWrt e l'app
Android per gestire tutto dal telefono.

Serve a noi per il *disaster recovery* e a chi vuole replicare la stessa
infrastruttura in un'altra comunità. Ogni componente sta in un repository
pubblico, con il suo README dettagliato: qui trovi l'ordine in cui metterli
insieme, come si collegano e perché sono fatti così.

!!! tip "Come usare la guida"
    Segui i capitoli di **Ricostruzione** nell'ordine: ognuno presuppone che i
    precedenti siano fatti. Dove un passo è già spiegato bene nel README del
    suo repository, la guida ci rimanda invece di ripeterlo.

## I repository

| Repository | Cosa fa | Capitolo |
|---|---|---|
| [ansible-dns](https://github.com/mikysal78/ansible-dns) | DNS autoritativo (BIND hidden primary, secondari, DNSSEC), certificati ACME, DDNS dei router, monitoring | [DNS e certificati](dns.md) |
| [openwisp2](https://github.com/mikysal78/openwisp2) | Server OpenWISP completo: controller, monitoring, RADIUS, topology, firmware upgrader, pagine Wi-Fi, VPN ZeroTier, Babel, log dei router, proxy LuCI | [OpenWISP](openwisp.md) |
| [openwisp-netconsole](https://github.com/mikysal78/openwisp-netconsole) | Scheda «Netconsole» nella pagina del device e rotazione dei log | [Moduli](moduli.md) |
| [openwisp-luci](https://github.com/mikysal78/openwisp-luci) | Pulsante «LuCI» nella pagina del device, con proxy autenticato | [Moduli](moduli.md) |
| [openwisp-config](https://github.com/mikysal78/openwisp-config) | Fork dell'agente OpenWISP dei router, con le nostre correzioni | [Moduli](moduli.md) |
| [ansible-ninux-openwrt](https://github.com/mikysal78/ansible-ninux-openwrt) | Compilazione del firmware OpenWrt NINUX con Ansible e Jenkins, caricamento nel firmware upgrader | [Firmware e Jenkins](firmware.md) |
| [openwisp-android](https://github.com/mikysal78/openwisp-android) | App Android per gestire OpenWISP | [App Android](app.md) |
| [openwisp-voucher](https://github.com/mikysal78/openwisp-voucher) | Programma per computer che crea e stampa accessi Wi-Fi a tempo per il captive portal | [Accessi Wi-Fi a tempo](voucher.md) |

## Ordine di ricostruzione

- [ ] **Proxmox**: host, rete, container e VM ([capitolo 1](proxmox.md))
- [ ] **DNS**: zone, DNSSEC, certificati wildcard distribuiti ai container ([capitolo 2](dns.md))
- [ ] **OpenWISP**: playbook openwisp2, organizzazione, VPN, template ([capitolo 3](openwisp.md))
- [ ] **Moduli**: netconsole e LuCI dentro OpenWISP ([capitolo 4](moduli.md))
- [ ] **Firmware**: Jenkins, prima build, immagini nel firmware upgrader ([capitolo 5](firmware.md))
- [ ] **Router**: flash, registrazione automatica, template, mesh ([capitolo 6](router.md))
- [ ] **App**: installazione e accesso ([capitolo 7](app.md))
- [ ] **Voucher**: gruppo RADIUS per gli ospiti e programma degli accessi a tempo ([capitolo 8](voucher.md))

Poi la pagina [Gestione](gestione.md) raccoglie aggiornamenti, backup,
sicurezza e problemi già incontrati.

## Cosa non c'è in questa guida

Password, token, chiavi e secret **non** stanno qui né nei repository: nei
comandi trovi segnaposto come `CHANGEME`, e ogni repository spiega dove vanno i
valori veri (file `secrets.yml`, `vault`, `ninux.yml` cifrato con
ansible-vault, tutti fuori da git).

!!! info "Contatti"
    Per domande sulla guida o sull'app: [app@ninux-nnxx.it](mailto:app@ninux-nnxx.it).
    Correzioni e miglioramenti sono benvenuti come
    [issue o pull request](https://github.com/mikysal78/ninux-basilicata-infra).
