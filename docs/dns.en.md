# 2. DNS and certificates

DNS comes before OpenWISP because it provides the names (`openwisp`, `wifi`,
`*.luci`…) and above all the **wildcard certificates** that OpenWISP uses for
HTTPS. Everything is in the [ansible-dns](https://github.com/mikysal78/ansible-dns)
repository.

## How it is made

- **Hidden primary** in the LAN (VM on Proxmox): BIND with the zones, not
  exposed to the Internet.
- **Two public secondaries** on VPS: they answer queries and receive the zones
  from the primary inside a **WireGuard** tunnel (TSIG-signed AXFR/IXFR).
- **DNSSEC** with automatic signing (Ed25519), keys rotated by BIND.
- **acme.sh** on the primary issues the wildcard certificates with the DNS-01
  challenge and copies them to the containers that use them.
- **DDNS**: routers with a changing IP update their own name in the `dyn`
  zone with `nsupdate`.
- **Monitoring**: Prometheus, Alertmanager and Grafana in a dedicated CT.

## Steps

The ansible-dns README explains every step in detail: here are the order and
the points that concern our infrastructure.

1. **Ansible controller**: clone the repository and install the dependencies
   ([Prerequisites](https://github.com/mikysal78/ansible-dns#prerequisites)).
2. **Primary VM on Proxmox**: Debian Trixie template and VM
   ([Proxmox — VM provisioning](https://github.com/mikysal78/ansible-dns#proxmox--vm-provisioning)).
3. **Secondary VPS**: order the VMs and open the provider firewall
   ([OVH — secondary VMs](https://github.com/mikysal78/ansible-dns#ovh--secondary-vms)).
4. **TSIG keys and vault** with the secrets
   ([Initial setup](https://github.com/mikysal78/ansible-dns#initial-setup)).
5. **YAML zones** (`zones/*.yml`, outside git) and full deploy
   ([DNS deployment](https://github.com/mikysal78/ansible-dns#dns-deployment)).
6. **DNSSEC**: after the first deploy, publish the DS records at the registrar
   ([DNSSEC](https://github.com/mikysal78/ansible-dns#dnssec)).

## Records needed by OpenWISP

In the `ninux-nnxx.it` zone (`zones/ninux-nnxx.it.yml`); the `aliases` of an A
record become CNAMEs to that name:

```yaml
zone:
  name: "ninux-nnxx.it"
  a:
    - name: "openwisp"
      ip: "194.28.98.61"
      ipv6: "2a07:7e81:3f1c::18"
      aliases:
        - "wifi"       # hotspot login pages
        - "zerotier"   # ZeroTier controller
        - "*.luci"     # LuCI proxy: <uuid>.luci.ninux-nnxx.it
    - name: "gw"
      ip: "194.28.98.57"   # border router
```

!!! note
    The exact zone format is in the ansible-dns README. The addresses are
    ours: replace them with yours.

For small changes to a zone with DDNS enabled (such as `ninux-nnxx.it`), the
playbook does not rewrite the zone: update the YAML to keep track of it and
apply the change with `nsupdate` on the primary.

## Certificates

OpenWISP needs two certificates, issued by the primary and copied to the
OpenWISP CT in `/etc/ssl/acme/`:

| Certificate | Names | Used by |
|---|---|---|
| `ninux-nnxx.it` | `ninux-nnxx.it`, `*.ninux-nnxx.it` | OpenWISP admin, Wi-Fi pages |
| `luci.ninux-nnxx.it` | `luci.ninux-nnxx.it`, `*.luci.ninux-nnxx.it` | LuCI proxy (one host per router) |

They are configured in `acme_domains` (`inventory/group_vars/all/main.yml` of
ansible-dns), with the OpenWISP CT among the targets:

```yaml
acme_deploy_ssh_port: 2400
acme_domains:
  - domain: "ninux-nnxx.it"
    keylength: "ec-256"
    deploy:
      - host: "10.27.22.18"          # OpenWISP CT
        reload_cmd: "systemctl reload nginx"
  - domain: "luci.ninux-nnxx.it"     # also covers *.luci.ninux-nnxx.it
    keylength: "ec-256"
    deploy:
      - host: "10.27.22.18"
        reload_cmd: "systemctl reload nginx"
```

Renewal is automatic, every night; the reload runs only when the certificate
actually changes.

!!! warning "The wildcard certificate does not cover second-level subdomains"
    `*.ninux-nnxx.it` is not valid for `<uuid>.luci.ninux-nnxx.it`: that is why
    the LuCI proxy has its own certificate, with `*.luci.ninux-nnxx.it`.

## Checklist

- [ ] `dig +dnssec openwisp.ninux-nnxx.it @ns1.<your-domain>` answers with signatures.
- [ ] The secondaries have the same serial as the primary.
- [ ] The two certificates are in `/etc/ssl/acme/` on the OpenWISP CT.
- [ ] `openssl x509 -in /etc/ssl/acme/ninux-nnxx.it.fullchain.pem -noout -text | grep DNS`
      shows `*.ninux-nnxx.it`.
