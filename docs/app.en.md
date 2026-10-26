# 7. Android app

[openwisp-android](https://github.com/mikysal78/openwisp-android) manages
OpenWISP from the phone through the REST API: nothing to install on the
server, except the two modules for LuCI and netconsole.

## What it does

- router list with monitoring status, search and filters;
- router page with information, Wi-Fi interfaces, charts;
- actions with confirmation: reboot, commands, firmware upgrade, **LuCI** and
  **netconsole**;
- hotspot users and sessions (RADIUS), with block and unblock;
- OpenWISP notifications every 15 minutes, without external push services;
- lock with the phone fingerprint or PIN.

The app shows only what the server has: if monitoring, firmware upgrader,
RADIUS, openwisp-luci or openwisp-netconsole are missing, the related parts do
not appear.

## Installation

Download the APK from the
[releases](https://github.com/mikysal78/openwisp-android/releases) and open it
on the phone (Android 8.0 or later). Releases are always signed with the same
key; the certificate fingerprint and the SHA256 checksums are in the notes of
every release.

On first start enter the server (`openwisp.ninux-nnxx.it`), your user and
password: the password is only used to get the API token and is never stored.

## Server side

| Feature | Needs |
|---|---|
| List, charts, actions, firmware, notifications, RADIUS | nothing: standard OpenWISP API |
| **LuCI** button | openwisp-luci ≥ 0.3.1 with `api_urls` under `api/v1/` |
| **Netconsole** button | openwisp-netconsole ≥ 0.2 with `api_urls` under `api/v1/` |

The openwisp2 playbook already includes both APIs.

Privacy policy: [App privacy policy](privacy-app.md).

## Become a tester

The app is coming to Google Play too. To register as a tester write to
[app@ninux-nnxx.it](mailto:app@ninux-nnxx.it?subject=openwisp-android%20tester)
with the Google account you use on the phone.

## Releases

Releases are built by GitHub Actions when a `v*` tag is pushed: tests, APK and
AAB signed with the key in the `release` environment, certificate check,
SHA256 and build provenance attestation. The procedure is in the app README,
section [Publishing a release](https://github.com/mikysal78/openwisp-android#publishing-a-release).

!!! danger "The signing key"
    Keep the signing key in a safe backup. If it is lost, updates can no longer
    be installed over the existing app, neither from GitHub nor from Google
    Play.
