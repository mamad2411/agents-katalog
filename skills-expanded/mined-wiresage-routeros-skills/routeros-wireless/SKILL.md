---
name: routeros-wireless
description: Wireless on MikroTik RouterOS 7. Covers choosing between the wifi (wifi-qcom, wifi-qcom-be, wifi-mediatek, wifi-qcom-ac) and legacy wireless drivers, access point, station, repeater and outdoor CPE setups, security profiles (WPA2, WPA3, OWE, WPS), configuration profiles and networks, channels, country and regulatory limits, access lists and RADIUS MAC authentication, scanning and spectral tools, CAPsMAN for both driver families, VLANs on wireless, Nv2, mesh, 60 GHz W60G links, and wireless debug logging. Use when configuring or troubleshooting Wi-Fi on a MikroTik device, managing several access points centrally, building a point-to-point link, or when clients cannot connect or roam.
---

# RouterOS wireless

Pick the driver first: it decides the whole command tree (`routeros-fundamentals` has the short version).

| Device family | Menu | Driver package |
| --- | --- | --- |
| Wi-Fi 6 and 7 (802.11ax and be) | `/interface/wifi` | `wifi-qcom`, `wifi-qcom-be`, `wifi-mediatek` (`wifi-qcom` was `wifiwave2` before 7.13) |
| Wi-Fi 5 (802.11ac), ARM | `/interface/wifi` or `/interface/wireless` | `wifi-qcom-ac` or `wireless` (your choice; legacy features Nstreme and Nv2 need `wireless`) |
| 802.11 a/b/g/n, MIPS | `/interface/wireless` | `wireless` |
| 60 GHz | `/interface/w60g` (or `/interface/wifi`) | `wireless` |

`/system/package/print` and `/interface/print` show which one is installed. Never paste v6-style `wireless` commands onto a `wifi`
device or the reverse. CAPsMAN has two generations too: WiFi CAPsMAN (`/interface/wifi/capsman`) for the new drivers and the older
`/caps-man` for the legacy ones; each manages only its own kind of CAP. Regulatory limits depend on `country`: set the real one.

## wifi: the quick setup

```ros
/interface/wifi/security/add name=sec-home authentication-types=wpa2-psk,wpa3-psk passphrase="REPLACE-8-TO-63-CHARACTERS" wps=disable
/interface/wifi/configuration/add name=cfg-home ssid=MyNetwork country=Latvia security=sec-home
/interface/wifi/set wifi1 configuration=cfg-home configuration.mode=ap disabled=no
/interface/wifi/set wifi2 configuration=cfg-home configuration.mode=ap disabled=no
/interface/bridge/port/add bridge=bridge1 interface=wifi1
/interface/bridge/port/add bridge=bridge1 interface=wifi2
/interface/wifi/registration-table/print
```

- The same settings can be written directly on the interface (`configuration.ssid=`, `security.passphrase=`) or in profiles
  (`/interface/wifi/security`, `channel`, `configuration`, `datapath`, `aaa`, `interworking`). Priority: interface value, profile on
  the interface, configuration profile, profile inside the configuration profile. `/interface/wifi/print detail` shows the effective values,
  `print detail config` only the ones set directly.
- `/interface/wifi/network` bundles SSID, security, datapath and radio settings and provisions them to all radios that match its labels.
- Guest SSID: a second interface with `master-interface=wifi2` and its own `configuration.ssid`.
- Open network with encryption: OWE transition mode needs two interfaces (hidden OWE SSID plus visible open SSID); 802.11r does not work over OWE.
- **Every wireless interface that serves the LAN must be a bridge port**, or clients get no DHCP and no connectivity.
- `/interface/wifi/radio/reg-info country=Latvia` shows allowed ranges, EIRP (transmit power plus antenna gain), indoor and DFS flags.
  The `Superchannel` country profile removes software limits; use it only where the law allows.
- Access list (`/interface/wifi/access-list`): first match wins, no implicit reject; filter by MAC, SSID regexp, signal range, time and days;
  `action=accept|reject|query-radius`; per-client `passphrase`. Rejecting too often makes clients avoid the AP.
- Tools: `/interface/wifi/scan`, `frequency-scan`, `sniffer`, `spectral-scan`, `registration-table` (with `deauth`).

Task guides: standalone AP (bridge, no DHCP server, same SSID on several APs gives client-driven roaming only), repeater, outdoor CPE to
AP links, Interworking (802.11u): `references/guides/wireless/wifi/`.

## CAPsMAN (wifi)

```ros
# controller
/interface/wifi/configuration/add name=cfg5 country=Latvia ssid=CAPsMAN_5 security=sec-home
/interface/wifi/provisioning/add action=create-dynamic-enabled master-configuration=cfg5 supported-bands=5ghz-ax
/interface/wifi/capsman/set enabled=yes ca-certificate=auto
# each access point
/interface/wifi/cap/set enabled=yes
/interface/wifi/set wifi1,wifi2 configuration.manager=capsman-or-local
```

CAPs find the controller by layer 2 discovery, DHCP option 138, or DNS `_capsman._tcp.<domain>`; any device with the wifi package can be a CAP
(licence level 4 or higher) and CAPsMAN runs on any device. Radios are identified by radio MAC. Provisioning creates an interface once; later
edits to a configuration profile are pushed to existing interfaces. Forwarding is on the CAP (`traffic-processing=on-cap`) or, from 7.21beta2,
on the controller. CAPsMAN gives the CAPs 802.11r/k/v roaming that standalone APs cannot. The guide has VLAN and OWE examples. On hAP ax
devices acting as CAP enable RSTP on the bridge.

## Legacy wireless (`/interface/wireless`)

```ros
/interface/wireless/security-profiles/add name=sec-home mode=dynamic-keys authentication-types=wpa2-psk wpa2-pre-shared-key="REPLACE-ME"
/interface/wireless/set wlan1 mode=ap-bridge ssid=MyNetwork band=2ghz-b/g/n frequency-mode=regulatory-domain country=latvia security-profile=sec-home disabled=no
```

Modes: `ap-bridge`, `bridge`, `station`, `station-wds`, `station-bridge`, `station-pseudobridge` and others (see `user-guides/wireless-station-modes.md`).
Only one station-bridge style choice fits a given topology; read that guide before choosing. Nv2 (TDMA, for point-to-multipoint) and
Nstreme are MikroTik protocols that need MikroTik on both ends. HWMP+ mesh, interworking profiles, spectral scan and VLANs on wireless
(`vlans-on-wireless.md`) have their own pages.

## Troubleshooting

1. Interface `disabled`, not in the bridge, wrong country (no supported channels), or channel list without allowed frequencies.
2. Clients connect and drop: check `security`, `authentication-types` (WPA3-only devices versus old clients), access list rules, signal range, DFS.
3. Log first: enable debug logging and watch the connect and disconnect messages:
   `/system/logging/add topics=wireless,debug action=memory` then `/log/print where topics~"wireless"`. Station-mode messages say
   `lost connection`, `failed to connect` and `established connection`; `MIC failure` means TKIP attack or key problems.
4. Slow or unstable: busy channel (`frequency-scan`), 40/80/160 MHz widths in a crowded band, too much transmit power, 2.4 GHz overlap.
5. After a driver switch (`wireless` to `wifi-qcom-ac`) the configuration is not converted; the manual's "Replacing 'wireless' package"
   section lists what is lost.

## 60 GHz (W60G)

Wireless Wire kits come as pre-configured pairs. Otherwise one side is a `bridge`/`ap-bridge` (frequency chosen there, with `auto`) and the other
`station-bridge`; the link has AES encryption with a `password`. Examples for PtP, PtMP and failover (CLI and GUI) and a distance guide are in
`references/guides/wireless/w60g/`.

## Where to look

| Need | Open |
| --- | --- |
| Which section is for my device, packages, frequency bands | `references/guides/wireless.md` |
| wifi properties, profiles, network, access list, scans, WPS, property reference | `references/guides/wireless/wifi.md` |
| WiFi CAPsMAN | `references/guides/wireless/wifi/capsman.md` |
| Wi-Fi 5 driver choice | `references/guides/wireless/wifi-ac.md` |
| Legacy interface properties | `references/guides/wireless/abgn/wireless-interface.md` |
| Legacy CAPsMAN, mesh, Nv2, spectral scan, troubleshooting | `references/guides/wireless/abgn/` |
| 60 GHz | `references/guides/wireless/w60g.md` |
| Properties | `references/cli/interface/wifi/`, `references/cli/interface/wireless/`, `references/cli/caps-man/` |
| Package missing or interface gone after update (knowledge base) | `references/help/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-bridging-switching` (VLANs on wireless, bridge ports), `routeros-users-aaa` (RADIUS, 802.1X, WPA-EAP),
`routeros-install-upgrade` (packages), `routeros-hotspot`, `routeros-user-manager`, `routeros-initial-setup`.
