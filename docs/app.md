# 7. App Android

[openwisp-android](https://github.com/mikysal78/openwisp-android) gestisce
OpenWISP dal telefono tramite le API REST: niente da installare sul server,
salvo i due moduli per LuCI e netconsole.

## Cosa fa

- elenco dei router con lo stato del monitoring, ricerca e filtri;
- pagina del router con informazioni, interfacce Wi-Fi, grafici;
- azioni con conferma: riavvio, comandi, aggiornamento del firmware,
  **LuCI** e **netconsole**;
- utenti e sessioni dell'hotspot (RADIUS), con blocco e sblocco;
- notifiche di OpenWISP ogni 15 minuti, senza servizi push esterni;
- blocco con impronta o PIN del telefono.

L'app mostra solo quello che il server ha: se mancano monitoring, firmware
upgrader, RADIUS, openwisp-luci o openwisp-netconsole, le parti relative non
compaiono.

## Installazione

Scarica l'APK dalle
[release](https://github.com/mikysal78/openwisp-android/releases) e aprilo sul
telefono (Android 8.0 o successivo). Le release sono firmate sempre con la
stessa chiave; l'impronta del certificato e gli SHA256 sono nelle note di
ogni release.

All'avvio inserisci il server (`openwisp.ninux-nnxx.it`), il tuo utente e la
password: la password serve solo a ottenere il token delle API e non viene
salvata.

## Lato server

| Funzione | Serve |
|---|---|
| Elenco, grafici, azioni, firmware, notifiche, RADIUS | niente: API standard di OpenWISP |
| Pulsante **LuCI** | openwisp-luci ≥ 0.3.1 con `api_urls` sotto `api/v1/` |
| Pulsante **Netconsole** | openwisp-netconsole ≥ 0.2 con `api_urls` sotto `api/v1/` |

Il playbook openwisp2 include già entrambe le API.

## Diventa tester

L'app arriverà anche su Google Play. Per registrarti come tester scrivi a
[app@ninux-nnxx.it](mailto:app@ninux-nnxx.it?subject=openwisp-android%20tester)
indicando l'account Google che usi sul telefono.

## Release

Le release le compila GitHub Actions al push di un tag `v*`: test, APK e AAB
firmati con la chiave nell'environment `release`, controllo del certificato,
SHA256 e attestazione di provenienza. La procedura è nel README dell'app,
sezione [Pubblicare una release](https://github.com/mikysal78/openwisp-android/blob/main/README.it.md#pubblicare-una-release).

!!! danger "La chiave di firma"
    La chiave di firma va conservata in un backup sicuro. Se si perde, gli
    aggiornamenti non si installano più sopra l'app esistente, né da GitHub
    né da Google Play.
