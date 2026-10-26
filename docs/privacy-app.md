# Informativa privacy dell'app

**App:** NINUX OpenWISP Manager (`it.ninuxnnxx.openwisp`), codice sorgente su
[github.com/mikysal78/openwisp-android](https://github.com/mikysal78/openwisp-android).
**Sviluppatore:** NINUX Basilicata · contatto
[app@ninux-nnxx.it](mailto:app@ninux-nnxx.it).
**Ultimo aggiornamento:** 26 ottobre 2026.

## In breve

L'app **non raccoglie dati per noi**. Non c'è un nostro server, non ci sono
pubblicità, statistiche, tracciamento né librerie di terze parti che inviano
dati. L'app parla **solo con il server OpenWISP che inserisci tu**, in HTTPS.

## Cosa tratta l'app e dove va

| Dato | Uso | Dove resta |
|---|---|---|
| Indirizzo del server e nome utente | collegarsi al tuo server OpenWISP | sul telefono |
| Password | inviata **una sola volta** al tuo server per ottenere il token delle API | **non viene salvata** |
| Token delle API | autenticare le richieste al tuo server | sul telefono, cifrato con una chiave del Keystore di Android |
| Dati di OpenWISP (router, monitoring, utenti e sessioni Wi-Fi, notifiche, log) | mostrarli nell'app | letti dal tuo server al momento, non salvati in modo permanente sul telefono |

I dati mostrati appartengono al server OpenWISP a cui ti colleghi: il loro
trattamento è responsabilità di chi gestisce quel server, secondo la sua
informativa.

## Permessi

| Permesso | Perché |
|---|---|
| Internet, stato della rete | collegarsi al tuo server OpenWISP |
| Notifiche | mostrare le notifiche di OpenWISP |
| Impronta / biometria | blocco dell'app (facoltativo) |
| Avvio del dispositivo, wake lock | riprogrammare dopo un riavvio il controllo periodico delle notifiche (ogni 15 minuti, verso il tuo server) |

## LuCI

Il pulsante LuCI apre l'interfaccia web del router nel browser del telefono,
tramite il tuo server OpenWISP. Da quel momento vale l'informativa del browser.

## Backup e cancellazione

- I dati dell'app sono esclusi dal backup su cloud e dal trasferimento tra
  telefoni.
- **Esci** (Impostazioni) toglie token e sessione dal telefono. Disinstallando
  l'app si cancella tutto ciò che aveva salvato.
- Il token resta valido sul server finché l'amministratore di OpenWISP non lo
  revoca: OpenWISP usa un solo token per utente, condiviso con altri strumenti.

## Minori

L'app è uno strumento di amministrazione di rete per utenti di OpenWISP e non
è rivolta ai minori.

## Modifiche

Le modifiche a questa informativa sono pubblicate su questa pagina; la
cronologia è nel [repository della guida](https://github.com/mikysal78/ninux-basilicata-infra/commits/main/docs/privacy-app.md).
