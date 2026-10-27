# NINUX Basilicata: the infrastructure, step by step

This guide explains how to **rebuild from scratch** the infrastructure of the
NINUX Basilicata community network: from the Proxmox host to the routers in
people's homes, through DNS, OpenWISP, the OpenWrt firmware build and the
Android app that manages everything from the phone.

It is our *disaster recovery* plan, and a starting point for other communities
that want the same infrastructure. Every component lives in a public
repository with its own detailed README: here you find the order in which to
put them together, how they connect and why they are made this way.

!!! tip "How to use this guide"
    Follow the **Rebuild** chapters in order: each one assumes the previous
    ones are done. Where a step is already well explained in the README of its
    repository, the guide links to it instead of repeating it.

## Repositories

| Repository | What it does | Chapter |
|---|---|---|
| [ansible-dns](https://github.com/mikysal78/ansible-dns) | Authoritative DNS (BIND hidden primary, secondaries, DNSSEC), ACME certificates, router DDNS, monitoring | [DNS and certificates](dns.md) |
| [openwisp2](https://github.com/mikysal78/openwisp2) | Full OpenWISP server: controller, monitoring, RADIUS, topology, firmware upgrader, Wi-Fi pages, ZeroTier VPN, Babel, router logs, LuCI proxy | [OpenWISP](openwisp.md) |
| [openwisp-netconsole](https://github.com/mikysal78/openwisp-netconsole) | "Netconsole" tab on the device page and log rotation | [Modules](moduli.md) |
| [openwisp-luci](https://github.com/mikysal78/openwisp-luci) | "LuCI" button on the device page, with an authenticated proxy | [Modules](moduli.md) |
| [openwisp-config](https://github.com/mikysal78/openwisp-config) | Fork of the OpenWISP agent of the routers, with our fixes | [Modules](moduli.md) |
| [ansible-ninux-openwrt](https://github.com/mikysal78/ansible-ninux-openwrt) | NINUX OpenWrt firmware build with Ansible and Jenkins, upload to the firmware upgrader | [Firmware and Jenkins](firmware.md) |
| [openwisp-android](https://github.com/mikysal78/openwisp-android) | Android app to manage OpenWISP | [Android app](app.md) |
| [openwisp-voucher](https://github.com/mikysal78/openwisp-voucher) | Desktop program that creates and prints time-limited Wi-Fi accounts for the captive portal | [Time-limited Wi-Fi access](voucher.md) |

## Rebuild order

- [ ] **Proxmox**: host, network, containers and VMs ([chapter 1](proxmox.md))
- [ ] **DNS**: zones, DNSSEC, wildcard certificates delivered to the containers ([chapter 2](dns.md))
- [ ] **OpenWISP**: openwisp2 playbook, organization, VPN, templates ([chapter 3](openwisp.md))
- [ ] **Modules**: netconsole and LuCI inside OpenWISP ([chapter 4](moduli.md))
- [ ] **Firmware**: Jenkins, first build, images in the firmware upgrader ([chapter 5](firmware.md))
- [ ] **Routers**: flashing, automatic registration, templates, mesh ([chapter 6](router.md))
- [ ] **App**: installation and login ([chapter 7](app.md))
- [ ] **Vouchers**: RADIUS group for guests and the time-limited access program ([chapter 8](voucher.md))

The [Operations](gestione.md) page collects updates, backups, security and
problems we have already met.

## What is not in this guide

Passwords, tokens, keys and secrets are **not** here nor in the repositories:
commands use placeholders such as `CHANGEME`, and each repository explains
where the real values go (`secrets.yml`, vaults, `ninux.yml` encrypted with
ansible-vault, all outside git).

!!! info "Contact"
    Questions about the guide or the app: [app@ninux-nnxx.it](mailto:app@ninux-nnxx.it).
    Fixes and improvements are welcome as
    [issues or pull requests](https://github.com/mikysal78/ninux-basilicata-infra).
