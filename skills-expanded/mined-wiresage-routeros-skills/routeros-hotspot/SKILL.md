---
name: routeros-hotspot
description: HotSpot captive portal on MikroTik RouterOS 7. Covers the setup wizard and the pieces it creates (address pool, DHCP server, masquerade, server profile, HotSpot server, users), login methods (HTTP PAP and CHAP, HTTPS, cookie, MAC, MAC cookie, trial), server and user profiles with rate limits and session limits, local users and RADIUS authentication and accounting, IP bindings (bypass, block, one-to-one NAT), walled garden for HTTP and other protocols, login page customisation, RFC 7710 captive portal API, device mode and PCC caveats. Use when building guest Wi-Fi or a paid-access network with a login page, bypassing devices, limiting guest bandwidth or time, or customising the portal pages.
---

# RouterOS HotSpot

HotSpot makes IPv4 clients log in before they get internet. It depends on firewall NAT and a built-in web proxy, so it is **IPv4 only**, it
works only with the default routing table (PCC and multi-table designs do not work, see below), and it can be blocked by **device mode**:
check `/system/device-mode/print` for `hotspot: yes` first (`routeros-system-utilities`).

## Setup

`/ip/hotspot/setup` is an interactive wizard. It asks for the interface, the gateway address with prefix (default 10.5.50.1/24), whether to
masquerade, the address pool, an optional certificate for HTTPS login, an SMTP server for redirecting port 25, DNS servers, the portal DNS name (a
full domain name) and the first local user. It creates the pool, a DHCP server, a masquerade rule, a profile and the HotSpot server.

```ros
/ip/hotspot/setup                         # answer the prompts; then verify:
/ip/hotspot/print
/ip/pool/print
/ip/dhcp-server/print
/ip/firewall/nat/print
```

The same result by hand (values mirror the wizard output in the manual):

```ros
/ip/address/add address=10.5.50.1/24 interface=ether3
/ip/pool/add name=hs-pool-3 ranges=10.5.50.2-10.5.50.254
/ip/dhcp-server/add name=dhcp1 interface=ether3 address-pool=hs-pool-3 lease-time=1h
/ip/firewall/nat/add chain=srcnat action=masquerade src-address=10.5.50.0/24
/ip/hotspot/profile/add name=hsprof1 hotspot-address=10.5.50.1 dns-name=hotspot.example.com login-by=http-chap,cookie
/ip/hotspot/add name=hotspot1 interface=ether3 address-pool=hs-pool-3 profile=hsprof1 idle-timeout=5m
/ip/hotspot/user/add name=guest password="REPLACE-ME" profile=default
```

- One HotSpot server per interface (Ethernet, wireless, VLAN or bridge). On a bridge, set the **bridge** as the HotSpot interface, never a
  port, and keep public interfaces out of the bridge. Wireless interfaces must be bridge ports (`routeros-wireless`).
- The server's `address-pool` hands out valid addresses to clients with wrong network settings (universal client). `addresses-per-mac`
  (default 2) limits addresses per MAC. `idle-timeout` (default 5m) applies to unauthenticated hosts, `login-timeout` removes hosts that never log in.
- Create the DHCP server and network as in `routeros-dhcp`; HotSpot can also tell DHCP clients they are behind a captive portal (RFC 7710).

## Login methods (`login-by` in the server profile)

`http-chap`, `http-pap`, `https`, `cookie` (only together with another HTTP method), `mac`, `mac-cookie`, `trial`. Default: `http-chap, cookie`.

- **https** needs `ssl-certificate` (`routeros-certificates`); `https-redirect=yes` (default) redirects https:// requests of unauthenticated users to the
  login page, which causes browser certificate errors; `no` simply rejects them.
- **mac** logs in by MAC address: create a user whose `name` is the client MAC; set `mac-auth-password` in the profile when the RADIUS server
  needs one. **mac-cookie** needs `add-mac-cookie=yes` in the user profile and remembers the credentials per MAC for `mac-cookie-timeout`;
  it logs in only when exactly one host has that MAC.
- **trial** gives free time: `trial-uptime=30m/1d` (first value usable, second the wait before the next trial) and `trial-user-profile`.
- `use-radius=yes` authenticates against RADIUS (`/radius`, see `routeros-users-aaa` and `routeros-user-manager`); `radius-accounting=yes`
  (default), `radius-interim-update`, `radius-mac-format`, `nas-port-type`, and `radius-default-domain` with `split-user-domain` for domains.

## Profiles, users, bypass

```ros
/ip/hotspot/user/profile/add name=guests rate-limit=1M/5M shared-users=1 session-timeout=1h idle-timeout=10m address-list=hs-guests
/ip/hotspot/user/add name=ticket1 password="REPLACE-ME" profile=guests limit-uptime=2h limit-bytes-total=500M
/ip/hotspot/ip-binding/add mac-address=AA:BB:CC:DD:EE:FF type=bypassed comment="printer"
/ip/hotspot/active/print
/ip/hotspot/active/remove [find user=ticket1]
```

- `rate-limit` (`rx/tx`, from the router's view: rx is the client's upload) creates a dynamic simple queue per logged-in user
  (`routeros-queues`). `shared-users` limits simultaneous logins of one name. `on-login` and `on-logout` run scripts with `$user`.
  `incoming-filter`, `outgoing-filter`, `incoming-packet-mark` and `outgoing-packet-mark` hook users into the firewall (a jump rule to the
  `hotspot` chain is required for the filters); `address-list` marks users for queue trees.
- User limits: `limit-uptime`, `limit-bytes-in|out|total`, `mac-address` (restrict to one MAC), `server` (restrict to one HotSpot server), `address` (one-to-one NAT).
- `/ip/hotspot/ip-binding` `type=regular` is one-to-one NAT, `bypassed` skips login (printers, cameras, own devices), `blocked` drops the host.
- `/ip/hotspot/host` shows all hosts (unauthenticated included), `/ip/hotspot/active` the logged-in ones, `/ip/hotspot/cookie` the cookies.

## Walled garden

`/ip/hotspot/walled-garden` lists HTTP and HTTPS hosts reachable before login (`action=allow`) or forced through login (`deny`); fields: `dst-host`,
`dst-port`, `path`, `method`, `src-address`, `server`. Wildcards `*` and `?` match the whole string (`example` does not match `example.com`);
a leading `:` makes the value a regular expression. `/ip/hotspot/walled-garden/ip` handles other protocols and addresses (`action=accept|drop|reject`, `protocol`,
`dst-address`, `dst-address-list`, `dst-host`), for example DNS, NTP, SSH or a payment provider. An unauthenticated client cannot reach anything
the garden does not list.

## Customisation

Pages are HTML files in the `html-directory` of the profile (default `hotspot`, on the router's file system). Copy the default files out, edit, and upload
to a new directory named in `html-directory-override`; an empty or missing path falls back to the defaults. Main pages: `login.html`, `alogin.html`,
`status.html`, `logout.html`, `error.html`, `redirect.html`, plus `rlogin.html`, `flogin.html`, `radvert.html` and others for finer control. Variables use
`$(name)` syntax. The login form can pass `username`, `password`, `dst`, `popup` and `radius<id>` attributes. `api.json` implements the RFC 7710
captive portal API (`captive`, `user-portal-url`, `seconds-remaining`, `bytes-remaining`, `can-extend-session`). Page-by-page behavior and the full
variable list are in `references/guides/authentication-authorization-accounting/hotspot-captive-portal/hotspot-customisation.md`.

## Pitfalls

- PCC or any multi-table setup breaks HotSpot (it uses only the default routing table). With multiple uplinks make HotSpot-bound traffic use the local
  table first with a routing rule or `/routing/settings`, as the end of the main guide describes.
- Debug with `/system/logging/add topics=hotspot,debug` (`routeros-diagnostics-monitoring`); look at `/ip/hotspot/host` to see where a client is stuck.
- `password` and `otp-secret` of HotSpot users and `mac-auth-password` are sensitive parameters: treat backups and `show-sensitive` exports as secrets.

## Where to look

| Need | Open |
| --- | --- |
| Wizard, all server, profile, user, walled garden, binding, cookie properties | `references/guides/authentication-authorization-accounting/hotspot-captive-portal.md` |
| Page files, variables, serving logic, advertising | `.../hotspot-captive-portal/hotspot-customisation.md` |
| Properties | `references/cli/ip/hotspot/` (server, profile, user, user/profile, active, host, ip-binding, cookie, walled-garden) |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-user-manager` (RADIUS and billing), `routeros-users-aaa` (RADIUS client), `routeros-dhcp`, `routeros-firewall` (NAT, filter chains),
`routeros-queues`, `routeros-wireless`, `routeros-certificates`, `routeros-high-availability` (PCC).
