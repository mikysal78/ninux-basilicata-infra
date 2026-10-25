# 1. Proxmox

All services run on a **Proxmox VE** host, each one in its own LXC container
or VM. This way every service is rebuilt on its own, backed up separately, and
a problem in one does not touch the others.

## Host network

The host is connected to the site management LAN (`10.27.22.0/24`), behind
the border router. Containers that must be reachable from the Internet
(OpenWISP, mail, websites) also have an interface on the public /29.

| Bridge | Network | Used by |
|---|---|---|
| `vmbr0` | management LAN `10.27.22.0/24` | all CTs and VMs |
| `vmbr1` | public /29 `194.28.98.56/29` | exposed services (e.g. OpenWISP on `.61`) |

!!! note
    The bridge names are the most common ones: adapt them to yours. What
    matters is that every exposed CT has one interface on the management LAN
    and one on the public network.

## Containers and VMs

| Service | Type | System | Indicative resources | Notes |
|---|---|---|---|---|
| OpenWISP | unprivileged CT | Debian 13 | 4 cores, 4–8 GB RAM, 40 GB | access to `/dev/net/tun` for ZeroTier |
| Jenkins (firmware) | CT | Debian 13 | 12 cores, 24 GB RAM, 200 GB | `nesting=1` for the build tmpfs |
| DNS hidden primary | VM | Debian 13 | 2 vCPU, 2 GB RAM, 40 GB | created by the ansible-dns playbook |
| Monitoring | CT | Debian 13 | 2 cores, 2 GB RAM | Prometheus, Alertmanager, Grafana |
| Proxmox Backup Server | VM or separate host | PBS | depends on data | backups of CTs and VMs |

### OpenWISP CT

ZeroTier needs `/dev/net/tun`, which must be exposed by hand in an
*unprivileged* CT. In `/etc/pve/lxc/<ID>.conf`:

```
lxc.cgroup2.devices.allow: c 10:200 rwm
lxc.mount.entry: /dev/net/tun dev/net/tun none bind,create=file
```

Then `pct restart <ID>`. The playbook does the rest (chapter 3).

### Jenkins CT

The OpenWrt build uses a tmpfs to go faster: the container needs *nesting*.
In `/etc/pve/lxc/<ID>.conf`:

```
features: nesting=1
```

CPU, RAM and disk requirements and the installation are in the
[Firmware and Jenkins](firmware.md) chapter.

### DNS VM

The ansible-dns playbook creates it through the Proxmox API: Debian Trixie
*genericcloud* template, clone with cloud-init, initial snapshot. You need a
Proxmox API token and the *snippets* storage enabled: see the ansible-dns
README, section
[Proxmox — VM provisioning](https://github.com/mikysal78/ansible-dns#proxmox--vm-provisioning).

## Useful tools

- [vmbuilder](https://github.com/mikysal78/vmbuilder): creates Proxmox VMs from
  cloud images in a few minutes.
- [pve-io-guard](https://github.com/mikysal78/pve-io-guard): alerts (also on
  Telegram) when a VM saturates the disk, and can throttle it by itself.

## Backups

Every CT and VM goes into **Proxmox Backup Server** backups, scheduled daily.
Besides full backups, keep outside the host:

- the secret files that are not in git (openwisp2 `secrets.yml`, the
  ansible-dns and ansible-ninux-openwrt vaults, `~/.vault_pass`);
- the **Android app signing key** (chapter 7): if it is lost, app updates can
  no longer be installed over the existing app.

## Checklist

- [ ] The CTs start and are reachable over SSH from the management LAN.
- [ ] The OpenWISP CT sees `/dev/net/tun` (`ls -l /dev/net/tun`).
- [ ] The Jenkins CT has `nesting=1` (`pct config <ID> | grep features`).
- [ ] PBS backups run and can be restored.
