---
name: routeros-mobile-networking
description: Mobile networking on MikroTik RouterOS 7. Covers LTE and 5G interfaces and modems (Direct-IP, MBIM, serial mode), APN profiles, authentication and IP types, default route distance and NAT for LTE uplinks, multi-APN and passthrough, band and operator locking, dual SIM slot switching and failover scripts, eSIM and MikroTik Connectivity, SMS and USSD, GPS, BG77 AT commands, LTE logging and troubleshooting. Use when bringing up or debugging a cellular WAN link, choosing APN settings, switching SIM slots, sending SMS, or reading signal and modem status.
---

# RouterOS mobile networking

A cellular modem appears as `/interface/lte` (LTE, 5G NR, MBIM; built-in or USB or mPCIe modems) and its network parameters live in an **APN
profile** (`/interface/lte/apn`). Direct-IP and MBIM modems are supported in v7 and the MBIM driver loads automatically; test an unrecognised modem on
v7 before asking for support on v6. The SXT LTE (RBSXTLTE3-7) needs the optional `lte` package. To use a PPP interface instead (lower
throughput), set `/interface/lte/settings/set mode=serial` and reboot (this property was `ignore-direct-modem` in v6).

## Bring up an LTE uplink

```ros
/interface/lte/apn/add name=profile1 apn=internet.example authentication=chap user=USER password="REPLACE-ME" ip-type=ipv4
/interface/lte/set [find] apn-profile=profile1
/interface/lte/print                                # flag R = running
/interface/lte/monitor lte1 once                    # status, operator, band, rssi, rsrp, rsrq, sinr, cell id, imei/iccid
/ip/firewall/nat/add chain=srcnat out-interface=lte1 action=masquerade
```

- APN profile: `add-default-route` and `default-route-distance` (default 2, so wired uplinks win over LTE, which is what you want for failover),
  `ip-type` (`auto`, `ipv4`, `ipv4-ipv6`, `ipv6`), `authentication` (`none`, `pap`, `chap`), `ipv6-interface` for prefix advertisement.
- `allow-roaming` (default no) is needed when abroad; some modems refuse an IP session with it off. `network-mode` forces the radio
  technology: for 5G NSA select both `lte` and `5g`, `5g` alone means standalone only. `band`, `nr-band` and `operator` (MCC plus MNC) lock the
  network; `pin` holds the SIM PIN and is sensitive.
- Multi-APN, passthrough (give the public address to a downstream router through `passthrough-interface`, optional MAC and subnet selection) and
  tips such as cell lock and finding location from cell information are in the LTE guide. Huawei modems cannot lock bands with `band=`; the guide shows
  the AT-command route with `at-chat` and `modem-init`.
- The firewall and masquerade rules must name the real interface (`lte1`), or use an interface list that includes it (`routeros-ethernet`).
- mPCIe modems in RB9xx boards have board-specific notes in the troubleshooting part of the guide.

## Dual SIM

Boards with switchable SIM slots (LtAP, LtAP mini, SXT R, ATL 5G) switch slots with `/interface/lte/settings/set sim-slot=down` (v7; slot names
`up`/`down`, or `a`/`b`, `sim`/`esim` depending on the model). On v6 use `/system/routerboard/modem/set sim-slot=`. The dual SIM guide has two script
examples: switch to the roaming SIM when the home network is lost or roaming is detected, and switch when the connection is down. Treat them as
starting points: they need testing for your carriers, and the scheduler and script syntax is in `routeros-scripting`.

## eSIM and MikroTik Connectivity

MikroTik Connectivity is a built-in eSIM service: register the device serial in your MikroTik account, buy a plan, and check in RouterOS that the
interface uses the `esim` slot and the right profile (`/interface/lte/esim`). Profiles are preloaded, so no internet is needed to activate;
activation takes minutes to a few hours.

## SMS and USSD

```ros
/tool/sms/send lte1 phone-number="+10000000000" message="status ok"
/tool/sms/inbox/print
```

The modem is a serial port (`/port/print`) or the LTE interface. Messages use GSM 7 encoding (no UCS2), 160 characters at most and
`^{}\[]~` count double; `status-report-request` defaults to yes. USSD works through AT commands and only in 3G or GSM network modes, not LTE-only
(the guide shows the debug log). Use SMS actions carefully in scripts: they can cost money and message content is not authenticated.

## GPS

`/system/gps` (package `gps`) reads NMEA from a built-in receiver or a serial or USB port: `enabled`, `port`, `coordinate-format` (`dd`, `dms`, `ddmm`),
`set-system-time`, init strings, `gps-antenna-select`. Examples of tracking with HTTP POST or MQTT and ThingsBoard are in the GPS section.

## Troubleshooting

1. `/system/logging/add topics=lte` then `/log/print`. `+CME ERROR: 10` means SIM not inserted (search the CME code for others).
2. Interface not running: wrong APN or authentication, SIM locked (PIN), roaming off, wrong SIM slot, antenna, band lock too narrow.
3. Connected but no internet: no NAT for `lte1`, firewall, default route missing or LTE distance higher than another default route, DNS.
4. BG77 modems (cellular IoT): AT commands for troubleshooting and WWAN/GNSS priority automation are in `bg77-modem-at-commands.md`.
5. Knowledge-base articles: LtAP "SIM not inserted", LTE USB modem, Chateau LTE12 APN problem (`references/help/`).

## Where to look

| Need | Open |
| --- | --- |
| LTE/5G client, APN profiles, multi-APN, passthrough, tips, troubleshooting | `references/guides/mobile-networking/lte-5g.md` |
| SIM switching scripts | `references/guides/mobile-networking/dual-sim-application.md` |
| eSIM | `references/guides/mobile-networking/mikrotik-connectivity.md` |
| SMS and USSD | `references/guides/mobile-networking/sms.md` |
| GPS and tracking examples | `references/guides/mobile-networking/gps.md` and `gps/` |
| PPP over serial modems | `references/guides/mobile-networking/ppp.md` |
| Properties | `references/cli/interface/lte/`, `references/cli/system/gps.md`, `references/cli/tool/sms/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-firewall` (NAT), `routeros-routing` (failover, distances), `routeros-high-availability`, `routeros-hardware` (LTE
models, SIM slots, antennas), `routeros-iot` (MQTT for GPS data), `routeros-scripting`.
