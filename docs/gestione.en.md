# Operations

## Updates

| Component | How |
|---|---|
| OpenWISP | run the openwisp2 playbook again: pip packages are `state: latest`, with minimum versions pinned for security advisories |
| Our modules | raise the version in the openwisp2 `playbook.yml` (git tag of the release) and run it again |
| Ansible roles | `ansible-galaxy role install -r requirements.yml -p roles/ --force` |
| Router firmware | new Jenkins build, then upgrade from OpenWISP (never the border router, see [chapter 5](firmware.md)) |
| DNS | ansible-dns playbook; BIND as in its README |
| App | release from a tag, see [chapter 7](app.md) |
| Voucher program | release from a tag, see [chapter 8](voucher.md) |

OpenWISP security advisories arrive by email and on
[GitHub Security Advisories](https://github.com/openwisp). On the server,
`pip-audit` in the OpenWISP virtualenv (`/opt/openwisp2/env`) lists the
dependencies with known vulnerabilities.

## Backups

- **Proxmox Backup Server**: all CTs and VMs, daily.
- **OpenWISP database** (PostgreSQL): included in the CT backup; before a major
  upgrade a `pg_dump` is also a good idea.
- **Outside the host**: the secrets that are not in git (`secrets.yml`, vaults,
  `.vault_pass`), the app signing key, the Jenkins API token.

## Security

- Secrets are never in the repositories: `secrets.yml`, Ansible vaults and the
  real DNS zones are in `.gitignore`.
- The OpenWISP server has a *default drop* firewall: SSH only from the
  management network, RADIUS only from the VPN and the LAN, router logs only
  from the NINUX network.
- Our repositories have CI, CodeQL where it applies, Dependabot, protection of
  `main` and of the tags, private vulnerability reporting (see the
  `SECURITY.md` of each one).

## Problems we have already met

| Symptom | Cause and fix |
|---|---|
| freeradius does not start on the first deploy | nginx does not answer yet: restart nginx and freeradius, run the playbook again |
| Router stuck on "configuration modified" | the openwisp-config agent died during the apply: use the fork ([chapter 4](moduli.md)); on the router send `kill -USR2` to the main process |
| Router looping on "checksum mismatch" | race between close changes in OpenWISP: save the device config again |
| ZeroTier offline after a reboot of the border router | the clock starts in 2100 (RTC): restart ZeroTier after NTP |
| The hotspot portal does not open | `wifiauth` certificate expired or incomplete walled garden: check the `sync_uspot_cert.py` cron job and the template |
| LuCI opened from the app says "session missing" | openwisp-luci older than 0.3.1 |
| Firmware upload rejected (HTTP 400) | image `type` unknown to OpenWISP, or category name over 64 characters |
| Removing a template brings back old settings on the router | openwisp-config restores the copy in `/etc/openwisp/stored/`: clean it first |

## Contributing

The guide is in the
[ninux-basilicata-infra](https://github.com/mikysal78/ninux-basilicata-infra)
repository: every page has an edit button at the top. Fixes to the single
components go to their own repositories.
