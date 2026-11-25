---
name: routeros-install-upgrade
description: Installing, upgrading, downgrading and licensing MikroTik RouterOS. Covers release channels (long-term, stable, testing, development), check-for-updates and manual upgrades, the routeros and extra packages, RouterBOOT and RouterBOARD firmware, the upgrade from v6 to v7, downgrading, Netinstall (Windows, Linux, package), installing CHR on hypervisors and clouds and RouterOS on x86, and license levels for hardware, CHR and x86. Use when planning or running an upgrade or downgrade, recovering a router with Netinstall, installing RouterOS on a VM or PC, choosing or installing a package, or checking a license.
---

# RouterOS installation, upgrade and licensing

Most MikroTik devices arrive with RouterOS installed, so the common jobs are upgrading, adding a package, and recovering a
device. Treat every one of them as a change that can leave the router unreachable: take a binary backup and an export first
(`routeros-initial-setup`), and make sure you have physical or out-of-band access before a reboot that matters.

## Know what is installed

```ros
/system/resource/print        # version, channel, architecture, board, factory-software (oldest allowed downgrade)
/system/package/print         # installed and available packages
/system/routerboard/print     # current-firmware (RouterBOOT) versus upgrade-firmware
/system/license/print         # software-id, level or expiry
```

`scripts/check_latest_version.py` asks upgrade.mikrotik.com for the newest version of each channel and can compare it with
yours: `python scripts/check_latest_version.py --channel stable --current 7.23.1`. It is read-only and needs no router.

## Upgrade

Version numbers are sequences, not decimals: 7.5 is older than 7.18. Channels: **long-term** (rare, critical fixes only),
**stable** (every few months), **testing** (weeks, not for production), **development** (raw). Production devices use
long-term or stable.

```ros
/system/package/update/set channel=stable mode=https check-certificate=yes
/system/package/update/check-for-updates
:put [/system/package/update/get status]            # "New version is available" when there is one
/system/package/update/install                      # downloads, installs and reboots by itself
/system/package/update/download                     # downloads only; you reboot when ready
```

Order of work: back up, check the release notes for the version you are going to, upgrade, then upgrade the bootloader and
reboot again:

```ros
/system/routerboard/upgrade        # then /system/reboot; the manual strongly recommends it after every RouterOS upgrade
```

- The router itself needs HTTPS access to the download server. If a router sees no update: `:put [:resolve upgrade.mikrotik.com]`,
  ping the result, then test port 443 with `/system/telnet <address> port=443`.
- A router on v6 only sees the intermediate v7 release (7.12.1 in the manual) in the channels. Upgrade to it first, run
  check-for-updates again, then go on. Before v6 to v7, upgrade to the latest v6 stable or long-term, read
  `references/guides/getting-started/upgrading-to-v7.md` (BGP, OSPF, MPLS, routing filters, PIM-SM and User Manager need
  attention; PIM-SM configuration is not kept), and do not run v7 on less than 64 MB RAM. The routing-protocol conversion runs
  once; to run it again load a v6 backup with `force-v6-to-v7-configuration-upgrade=yes`.
- Manual upgrade: put the `.npk` files for the router's architecture into `/file` (WinBox drag and drop, WebFig, FTP root),
  reboot, and check `/log/print without-paging` if the version did not change. Serial cables upgrade RouterBOOT only.
- Automation: a scheduler script that runs check-for-updates, waits, and installs when the status says a new version is
  available. Test it by hand first; a script cannot guard against a bad release.
- Mirror packages inside a network with `/system/package/local-update` instead of letting every router download them.

## Downgrade

Only down to the factory-installed version (`factory-software` in `/system/resource/print`); older releases can brick the
router. Back up first (a configuration can break across major versions), upload the `.npk` files of the target version for the
same architecture, then run `/system/package/downgrade` and reboot. Ask the user before doing it.

## Packages

Features live in `.npk` packages. The `routeros` bundle covers most; extras such as `container`, `iot`, `zerotier`, `ups`, `dude`,
`user-manager`, `rose-storage`, `gps`, `calea` and the wireless drivers are separate. System package names depend on the
architecture (`routeros-arm`, `routeros-arm64`, `routeros-mipsbe`, `routeros-mmips`, `routeros-smips`, `routeros-tile`,
`routeros-ppc`; plain `routeros` for x86 and CHR). Wireless devices need the right driver package: `wifi-qcom` (802.11ax,
called `wifiwave2` before 7.13), `wifi-qcom-be` (Wi-Fi 7), `wifi-mediatek`, `wifi-qcom-ac` (optional, some 802.11ac), or
`wireless` (older radios and 60 GHz; bundled up to 7.12, separate from 7.13).

```ros
/system/package/enable gps,zerotier,container     # schedule; "available" packages are downloaded on apply
/system/package/uninstall gps
/system/package/apply-changes                     # asks "Apply scheduled changes and reboot device? [y/N]"
```

Check the log after the reboot: conflicts are reported there. A package uploaded by FTP or SFTP with the name `*.auto.npk`
installs itself and reboots the router at once. The full table with supported architectures is in
`references/guides/getting-started/installation-and-upgrade/packages.md`.

## Reinstall and recover with Netinstall

Netinstall reformats the disk: all configuration and files are lost (the license key and RouterBOOT settings are kept). Ask for
explicit confirmation. It runs on a computer, or on a MikroTik device with the Netinstall package, in the same layer 2 segment
as the target; use a direct cable or a simple switch and a static address on the host. Put the target in Etherboot mode
(serial console: hold Ctrl+E; or press reset shortly after power-up; backup booter: hold reset during power-up until the LED
sequence blinking, steady, off). Then install the packages for the architecture, optionally with a configuration script.
Linux: `sudo netinstall-cli -i <interface> routeros-<version>-<arch>.npk` (see the page for all flags; it needs root).
Pages: `references/guides/getting-started/installation-and-upgrade/netinstall*.md`; a knowledge-base article covers common
failures (`references/help/problems-with-netinstall.md`).

## Virtual and bare-metal installs

- **CHR** (Cloud Hosted Router) is the x86-64 virtual edition: pages for Proxmox VE, VirtualBox, VMware ESXi, Hyper-V, AWS,
  Hetzner and Vultr under `references/guides/getting-started/installation-and-upgrade/install/chr-installation/`, plus
  `chr-installation/troubleshooting.md`. Licensing is per level (Free, P1, P10, P-Unlimited) and tied to the system ID.
- **x86**: `install/x86-installation.md`; installing from USB: `references/help/x86-on-usb.md`.

## Licenses

`/system/license/print` shows the software ID and level. Hardware devices come licensed (levels 3 to 6 differ in tunnel
counts, user sessions and wireless AP mode; level 0 is a time-limited trial, level 1 a free demo). CHR and x86 need a key
tied to the system ID or software ID. See `references/guides/getting-started/routeros-licensing.md` and the three platform
pages under it. Never invent license limits; read the table.

## Where to look

| Need | Open |
| --- | --- |
| Upgrade procedure, channels, local mirror | `references/guides/getting-started/installation-and-upgrade/upgrade.md` |
| v6 to v7 caveats | `references/guides/getting-started/upgrading-to-v7.md` |
| Downgrade checklist | `references/guides/diagnostics-monitoring-and-troubleshooting/downgrading-routeros.md` |
| Package list and requirements | `references/guides/getting-started/installation-and-upgrade/packages.md` |
| Bootloader, backup loader, reset button, RouterBOOT settings | `references/guides/getting-started/installation-and-upgrade/routerboot.md` |
| Features that differ by CPU architecture | `references/guides/getting-started/software-specifications/feature-support-based-on-architecture.md` |
| `/system/package`, `/system/license`, `/system/routerboard` properties | `references/cli/system/` |
| Everything else | `references/INDEX.md` |

Related skills: `routeros-initial-setup` (backup before you start), `routeros-hardware` (models, ports, reset button),
`routeros-wireless` (which wireless package), `routeros-troubleshooting` (reboot loop, failed upgrade).
