# 8. Accessi Wi-Fi a tempo

[openwisp-voucher](https://github.com/mikysal78/openwisp-voucher) è un
programma per computer (Linux e Windows) che crea **accessi Wi-Fi a tempo**
per il captive portal e li stampa come **biglietti o etichette**, come negli
hotel: «Mario ha accesso per 3 giorni, poi l'utente si spegne da solo». Usa
le API REST di OpenWISP: sul server non si installa niente.

## Cosa fa

- **ospite con nome** (nome utente, email, password generata) oppure **serie
  di voucher** (`ospite1`, `ospite2`, …) con password generate dal server;
- **durata in giorni**: la data stampata è l'ultimo giorno valido, OpenWISP
  disattiva l'utente alle 00:01 del giorno dopo; si può anche disattivare
  subito;
- stampa su **foglio A4** (10 biglietti), **scontrino** 58/80 mm o
  **etichetta** di misura libera, con logo, sito, email, telefono, nome della
  rete e QR code; oppure PDF o testo da copiare;
- elenco degli accessi creati, con ristampa e stato letto dal server;
- il **superuser** sceglie l'organizzazione, l'**operatore** vede solo la sua.

## Installazione

Scarica l'eseguibile dalle
[release](https://github.com/mikysal78/openwisp-voucher/releases):
`openwisp-voucher-<versione>-windows.exe` per Windows,
`openwisp-voucher-<versione>-linux-x86_64.tar.gz` per Linux. Non si installa:
si avvia e basta. Su Windows l'eseguibile per ora non è firmato e SmartScreen
chiede conferma («Ulteriori informazioni» → «Esegui comunque»); la richiesta
di firma gratuita alla SignPath Foundation è in corso.

In **Impostazioni**: «Accedi…» con il server (`openwisp.ninux-nnxx.it`) e il
tuo utente, poi organizzazione, gruppo RADIUS, logo e dati della struttura.
La password serve solo a ottenere il token, che va nel portachiavi del
sistema.

## Lato server

| Cosa | Dove |
|---|---|
| API dei batch di openwisp-radius e task `deactivate_expired_users` | già nel playbook openwisp2 |
| Gruppo RADIUS per gli ospiti | admin → RADIUS → Gruppi; per Basilicata `basilicata-24H` (24 ore e 3 GB al giorno) |
| Pagina di login che accetta il **nome utente** | `login_form.input_fields.username.type: "text"` nel YAML dell'organizzazione (vedi [capitolo 3](openwisp.md)) |
| Utenti operatori (reception) | staff, gestori dell'organizzazione, permessi elencati nel [README](https://github.com/mikysal78/openwisp-voucher/blob/main/README.it.md#utenti-operatori) |

!!! warning "Email degli ospiti"
    OpenWISP vuole un'email diversa per ogni utente. Con un'email già usata
    openwisp-radius 1.3 risponde con un errore 500 generico: il programma la
    controlla prima e lo dice chiaramente.

## Release

Le release le compila GitHub Actions al push di un tag `v*`: test, eseguibili
per Windows e Linux con PyInstaller, SHA256 e attestazione di provenienza. La
procedura è nel README del programma, sezione
[Sviluppo](https://github.com/mikysal78/openwisp-voucher/blob/main/README.it.md#sviluppo).
