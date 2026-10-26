# 6. Routers and network

With OpenWISP and the firmware ready, a new router joins the network almost by
itself. This chapter explains what happens and what to choose by hand.

## A new router

1. **Flash** the NINUX firmware of the right variant (from the Jenkins build or
   the GitHub release of ansible-ninux-openwrt), from the original firmware web
   interface or with `sysupgrade`.
2. On first boot the **openwisp-config** agent contacts
   `https://openwisp.ninux-nnxx.it` with the organization shared secret, and
   the device appears in OpenWISP with the router name.
3. OpenWISP applies the **required** and **default** templates
   ([chapter 3](openwisp.md)): Babel, mesh, ZeroTier VPN, NTP, logs, node
   names.
4. Once the VPN is up the router joins the Babel network and monitoring starts
   collecting data.

Then, on the device page:

- assign the **access point** templates and, where needed, the **hotspot**;
- set the **location** on the map;
- check that the SSH connection works (*Credentials* tab): it is needed for
  commands, upgrades and LuCI.

## Which template for which router

| Case | Template |
|---|---|
| Router with Wi-Fi clients | AP WiFi 2.4GHz, dual band or dual SSID |
| Several APs on the same LAN | also **usteer** (moves clients to the best AP) |
| Public hotspot | **Hotspot uspot 2.4GHz** |
| Connected to the site LAN through the `wan` port | **Uplink LAN su wan** (after Bird2) |
| To keep under observation (hangs, crashes) | **Netconsole** |
| x86 border router | **Router di confine** (full config) |

!!! warning "Uplink LAN su wan only at the site"
    The "Uplink LAN su wan" template opens Babel and SSH on the `wan` zone. Use
    it only on routers connected to our LAN through the `wan` port: on remote
    sites the `wan` is the provider's modem.

## The mesh

- **802.11s** on 2.4 GHz, `mesh_id` `ninux-mesh`, encrypted with **SAE**
  (WPA3): on 802.11s OpenWrt always uses SAE. The key is the `mesh_password`
  variable of the template, the same for all nodes.
- Babel uses the mesh (`br-mesh`) as a radio link: cost from 256 up, growing
  with packet loss. It always costs more than cable (96) and, while the link
  is good, less than the VPN (600): see
  [Architecture](architettura.md#the-router-network).
- Nodes without their own Internet take the default route from their mesh
  neighbours via OSPF.

## Router users and passwords

| User | Purpose | Password |
|---|---|---|
| `root` | the router owner (LuCI, SSH) | public default in the firmware READMEs, set **only if root has none yet**: if you change it, it stays after upgrades |
| `admin` | NINUX service user (UID 0) | reset at every flash, not published; used by the LuCI automatic login |

## Remote nodes

A remote node (a home, an association) reaches the rest of the network only
through the VPN. Before changing its VPN or its OpenWISP configuration, always
prepare an **automatic rollback** (a watchdog that restores the configuration
if the node does not come back): if the VPN goes down, the node stays
unreachable until somebody goes there.

## Checklist

- [ ] The device is in OpenWISP with configuration "applied" and monitoring "ok".
- [ ] `birdc show babel neighbors` on the router shows the expected neighbours.
- [ ] The router appears in the "Babel NINUX" topology.
- [ ] From a client of the router the LANs of the other nodes are reachable.
