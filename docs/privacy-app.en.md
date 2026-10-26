# App privacy policy

**App:** NINUX OpenWISP Manager (`it.ninuxnnxx.openwisp`), source code at
[github.com/mikysal78/openwisp-android](https://github.com/mikysal78/openwisp-android).
**Developer:** NINUX Basilicata · contact
[app@ninux-nnxx.it](mailto:app@ninux-nnxx.it).
**Last updated:** 26 October 2026.

## In short

The app **does not collect data for us**. There is no server of ours, no ads,
no analytics, no tracking and no third-party libraries sending data. The app
talks **only to the OpenWISP server you enter**, over HTTPS.

## What the app handles and where it goes

| Data | Use | Where it stays |
|---|---|---|
| Server address and username | connect to your OpenWISP server | on the phone |
| Password | sent **once** to your server to get the API token | **never stored** |
| API token | authenticate the requests to your server | on the phone, encrypted with an Android Keystore key |
| OpenWISP data (routers, monitoring, Wi-Fi users and sessions, notifications, logs) | show them in the app | read from your server when needed, not stored permanently on the phone |

The data shown belongs to the OpenWISP server you connect to: its processing
is the responsibility of whoever runs that server, under their privacy policy.

## Permissions

| Permission | Why |
|---|---|
| Internet, network state | connect to your OpenWISP server |
| Notifications | show OpenWISP notifications |
| Fingerprint / biometrics | app lock (optional) |
| Boot completed, wake lock | reschedule after a reboot the periodic notification check (every 15 minutes, to your server) |

## LuCI

The LuCI button opens the router web interface in the phone browser, through
your OpenWISP server. From then on the browser privacy policy applies.

## Backup and deletion

- App data is excluded from cloud backups and device-to-device transfers.
- **Sign out** (Settings) removes token and session from the phone.
  Uninstalling the app deletes everything it stored.
- The token stays valid on the server until the OpenWISP administrator revokes
  it: OpenWISP uses one token per user, shared with other tools.

## Children

The app is a network administration tool for OpenWISP users and is not aimed
at children.

## Changes

Changes to this policy are published on this page; the history is in the
[guide repository](https://github.com/mikysal78/ninux-basilicata-infra/commits/main/docs/privacy-app.md).
