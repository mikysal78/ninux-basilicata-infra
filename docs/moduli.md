# 4. Moduli per OpenWISP

Tre moduli nostri completano OpenWISP. I primi due sono piccole app Django che
estendono la pagina del device; il terzo è l'agente che gira sui router.
Il playbook openwisp2 installa già i primi due: questo capitolo spiega cosa
fanno e cosa controllare.

## openwisp-netconsole

[Repository](https://github.com/mikysal78/openwisp-netconsole) ·
scheda **Netconsole** nella pagina del device.

I router mandano i messaggi del kernel al server con **netconsole** (UDP 6666),
in tempo reale, anche negli ultimi istanti prima di un blocco o di un kernel
panic, quando il syslog non fa più in tempo. rsyslog li salva in
`/opt/router-logs/netconsole-<nome del device>/`, e la scheda li mostra
aggiornati ogni pochi secondi, con i file ruotati da scaricare.

- **Lato server**: Play 5 di openwisp2 (rsyslog, gruppo `router-logs` in sola
  lettura per OpenWISP, script di rotazione).
- **Lato router**: template **Netconsole** (target in configfs, controllo ogni
  5 minuti, nome del device come *userdata*). Serve il firmware NINUX con
  `kmod-netconsole` compilato con `NETCONSOLE_DYNAMIC`.
- **Rotazione dei log**: si regola da OpenWISP, pagina *Monitoring → Rotazione
  dei log dei router* (solo superuser). Default: ogni giorno o oltre 50 MB,
  15 giorni, al massimo 30 file.
- **API** per l'app: `GET /api/v1/netconsole/device/<uuid>/logs/` (da 0.2).

## openwisp-luci

[Repository](https://github.com/mikysal78/openwisp-luci) ·
pulsante **LuCI ↗** nella pagina del device.

Apre l'interfaccia web del router in una nuova scheda passando dal server:
il router deve essere raggiungibile solo dal server, non dal browser.

- Un host per router: `https://<uuid>.luci.ninux-nnxx.it`, così cookie e
  sessioni di un router non arrivano agli altri. Servono il DNS `*.luci` e il
  certificato `luci.ninux-nnxx.it` ([capitolo 2](dns.md)); il Play 6 si ferma
  se il certificato manca.
- Link monouso da 60 secondi, poi un cookie `__Host-` legato a utente, device
  e password; nginx chiede a OpenWISP a ogni richiesta se l'utente può ancora.
- **Accesso automatico** per i superuser: OpenWISP crea via SSH una sessione
  LuCI per l'utente di servizio `admin` del router. Nessuna password sul
  server. Gli altri, e chi vuole entrare come `root`, usano il login di LuCI.
- Router con la gestione sulla `wan`: la regola `Allow-LuCI-OpenWISP` apre la
  443 solo dal server.
- **API** per l'app: `POST /api/v1/luci/device/<uuid>/link/` (da 0.3; usare
  almeno la 0.3.1 per aprirla dall'app).

!!! warning "Cookie di sessione di OpenWISP"
    I sottodomini `*.luci` sono dello stesso dominio di OpenWISP: il cookie di
    sessione di OpenWISP deve chiamarsi `__Host-sessionid`, che i sottodomini
    non possono sovrascrivere. Il playbook lo imposta.

## openwisp-config (fork)

[Repository](https://github.com/mikysal78/openwisp-config) · l'agente che gira
sui router.

È il fork dell'agente ufficiale con le correzioni ai segnali `SIGUSR1/USR2`:
senza, l'agente poteva morire al primo ciclo dopo l'avvio o durante
l'applicazione di una configurazione, lasciando il router fermo su «config
modificata». Il problema è segnalato upstream in
[openwisp-config#283](https://github.com/openwisp/openwisp-config/issues/283).

Il firmware NINUX lo prende dal branch `fix/sigusr-handlers-startup` del fork,
con il feed in `config/build.yml` di ansible-ninux-openwrt:

```
src-git openwisp_config https://github.com/mikysal78/openwisp-config.git;fix/sigusr-handlers-startup
```

Quando la correzione arriverà upstream, si tornerà al pacchetto ufficiale.

## Controllo

- [ ] Nella pagina di un device ci sono le schede/pulsanti **Netconsole** e **LuCI ↗**.
- [ ] Netconsole mostra righe recenti per un router con il template Netconsole.
- [ ] LuCI si apre (da superuser, già autenticata come `admin`).
- [ ] `curl -X OPTIONS https://openwisp.ninux-nnxx.it/api/v1/luci/device/00000000-0000-0000-0000-000000000000/link/`
      risponde 405 (API presente) e non 404.
