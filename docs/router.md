# 6. Router e rete

Con OpenWISP e il firmware pronti, un router nuovo si mette in rete quasi da
solo. Questo capitolo spiega cosa succede e cosa scegliere a mano.

## Un router nuovo

1. **Flash** del firmware NINUX della variante giusta (dalla build di
   Jenkins o dalla release GitHub di ansible-ninux-openwrt), dall'interfaccia
   del firmware originale o con `sysupgrade`.
2. Al primo avvio l'agente **openwisp-config** contatta
   `https://openwisp.ninux-nnxx.it` con lo shared secret dell'organizzazione e
   il device compare in OpenWISP, con il nome del router.
3. OpenWISP gli applica i template **richiesti** e **default**
   ([capitolo 3](openwisp.md)): Babel, mesh, VPN ZeroTier, NTP, log, nomi dei
   nodi.
4. Con la VPN attiva il router entra nella rete Babel e il monitoring inizia a
   raccogliere i dati.

Poi, nella pagina del device:

- assegna i template degli **access point** e, dove serve, l'**hotspot**;
- imposta la **posizione** sulla mappa;
- controlla che la connessione SSH risulti funzionante (scheda *Credentials*):
  serve per comandi, aggiornamenti e LuCI.

## Quale template per quale router

| Caso | Template |
|---|---|
| Router con client Wi-Fi | AP WiFi 2.4GHz, dual band o dual SSID |
| Più AP sulla stessa LAN | in più **usteer** (sposta i client sull'AP migliore) |
| Hotspot pubblico | **Hotspot uspot 2.4GHz** |
| Collegato alla LAN della sede dalla porta `wan` | **Uplink LAN su wan** (dopo Bird2) |
| Da tenere sotto osservazione (blocchi, crash) | **Netconsole** |
| Router di confine x86 | **Router di confine** (config completa) |

!!! warning "Uplink LAN su wan solo in sede"
    Il template «Uplink LAN su wan» apre Babel e SSH sulla zona `wan`. Va solo
    sui router collegati alla nostra LAN dalla porta `wan`: nei siti remoti la
    `wan` è il modem del provider.

## La mesh

- **802.11s** sulla 2.4 GHz, `mesh_id` `ninux-mesh`, cifrata con **SAE**
  (WPA3): su 802.11s OpenWrt usa sempre SAE. La chiave è la variabile
  `mesh_password` del template, uguale per tutti i nodi.
- Babel usa la mesh (`br-mesh`) come collegamento radio: costo più alto del
  cavo, più basso della VPN.
- I nodi senza Internet propria prendono la default route dai vicini della
  mesh con OSPF.

## Utenti e password dei router

| Utente | A cosa serve | Password |
|---|---|---|
| `root` | il proprietario del router (LuCI, SSH) | default pubblica nei README del firmware, impostata **solo se root non ne ha già una**: se la cambi resta anche dopo gli aggiornamenti |
| `admin` | utente di servizio NINUX (UID 0) | reimpostata a ogni flash, non pubblicata; usata dall'accesso automatico di LuCI |

## Nodi remoti

Un nodo remoto (una casa, un'associazione) raggiunge il resto della rete solo
attraverso la VPN. Prima di cambiare la sua VPN o la configurazione di
OpenWISP, prepara sempre un **ritorno automatico** (watchdog che ripristina la
configurazione se il nodo non torna raggiungibile): se la VPN cade, il nodo
resta irraggiungibile finché qualcuno non va sul posto.

## Controllo

- [ ] Il device è in OpenWISP con configurazione «applicata» e monitoring «ok».
- [ ] `birdc show babel neighbors` sul router mostra i vicini attesi.
- [ ] Il router compare nella topology «Babel NINUX».
- [ ] Da un client del router si raggiungono le LAN degli altri nodi.
