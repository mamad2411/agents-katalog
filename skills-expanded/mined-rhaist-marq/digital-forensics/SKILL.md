---
name: digital-forensics
description: Covers DFIR across host, memory, network, mobile and cloud, including order of volatility, sound acquisition and chain of custody, and the current open-source stack (Volatility 3, Plaso, tshark and others). Use when the user asks to acquire or analyze a disk image, memory dump, PCAP, phone or cloud logs, build a timeline, or preserve evidence for legal use.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Digital forensics (DFIR)

Reconstruct what happened from artifacts, defensibly. Two rules dominate
everything: **preserve before you analyze**, and **work the copy, never the
original**. Forensics usually runs inside an incident (`load_skill
incident-response`); a found binary goes to `load_skill malware-triage` /
`malware-static`.

## Golden rules

- Acquire in **order of volatility** (RFC 3227): CPU/registers/cache → RAM →
  network state (ARP, routes, sockets) → running procs/open files → disk →
  logs/archives → physical/topology. The volatile end evaporates on power-off, so
  grab it first. Powering off or "just looking" mutates the source.
- Hash on acquisition (sha256), again after imaging; matching hashes prove the
  copy is faithful. Write-block all originals.
- **Chain of custody**: who/what/when/where for every access and transfer, signed.
  A gap makes evidence inadmissible. Keep originals offline + read-only; analyze a
  verified working copy.

## Host / disk forensics

- Image: `dd`/`dcfldd`/`ewfacquire` (E01 w/ embedded hash) or FTK Imager.
- Analyze with **The Sleuth Kit + Autopsy** (TSK 4.15.0, Autopsy 4.23.x, 2026;
  verify https://www.sleuthkit.org/). Filesystem timeline, deleted-file
  recovery, carving.
- Build a **super-timeline** with Plaso/log2timeline (`psort`): correlates FS,
  registry, EVTX, browser, prefetch into one chronology.
- Windows artifacts that answer "what ran / when / who": Prefetch, Amcache/
  Shimcache, SRUM, $MFT/$UsnJrnl, registry (Run keys, Services, UserAssist,
  ShellBags), EVTX (4624/4688/7045/Sysmon), scheduled tasks, browser history.
  Tooling: Eric Zimmerman tools (KAPE for collection + parsing), RegRipper, Velociraptor for fleet-wide hunting/collection.
- Linux/macOS: bash/zsh history, auth/syslog/journald, cron/systemd timers,
  ~/.ssh, FSEvents/Unified Logs (macOS).

## Memory forensics

- Acquire RAM _before_ disk: WinPMEM/DumpIt (Win), AVML/LiME (Linux), `osxpmem`
  (macOS). A page file + hibernation file complement it.
- Analyze with **Volatility 3** (v2.28.2, Sep 2026; the v2.26 parity release
  deprecated + archived Vol2 in May 2025; verify
  https://github.com/volatilityfoundation/volatility3). Symbol tables auto-resolve
  most modern OSes. High-value plugins: `pslist`/`pstree`/`psscan` (hidden procs),
  `malfind` (injected code), `cmdline`, `netscan`, `dlllist`/`ldrmodules`,
  `handles`, `svcscan`, `hashdump`. Memory catches what disk can't: injected/
  fileless malware, decrypted strings, live network state, keys.

## Network forensics

- Sources: full PCAP (Wireshark/`tshark`), Zeek logs (conn/dns/http/ssl/files),
  Suricata alerts, NetFlow. DNS + TLS SNI/JA3 reveal C2 and exfil even when payload
  is encrypted.
- Pivot extracted indicators (IPs, domains, JA3, certs) with `load_skill
ioc-pivoting`. Carve transferred files with Zeek `files.log` / NetworkMiner.

## Mobile forensics

- Logical vs file-system vs physical acquisition: modern iOS/Android encryption
  usually limits you to logical/advanced-logical (full-FS needs exploit or vendor
  tooling). Tools: ALEAPP/iLEAPP (artifact parsers), MVT (Mobile Verification
  Toolkit: spyware/IOC checks), commercial Cellebrite/GrayKey/Oxygen.
- Targets: app DBs (SQLite), call/SMS, location, cloud-sync, keychain, notifications.

## Cloud forensics (different game)

- No disk to seize: evidence is API logs + snapshots. You depend on what logging
  was enabled _before_ the incident (enable CloudTrail/Azure Activity/GCP Audit +
  data events _now_, in prep).
- Acquire: control-plane audit logs, EBS/disk snapshots, serial console, IAM/role/
  key activity, object-store access logs. Beware ephemeral compute: snapshot
  before the instance is terminated.
- Full cloud/identity-plane IR playbook (revocation order, federation/app abuse,
  log retention): `load_skill cloud-incident-response`.
- Watch identity abuse: new keys, role assumption, federation/OAuth grants,
  CloudTrail tampering. Map to ATT&CK Cloud matrix.

## Anti-patterns

- Booting/poweroff the evidence machine, or running tools on the original.
- Skipping RAM because "disk has everything"; fileless attacks live in memory.
- No hashing / no custody log: that turns good evidence into a story you can't prove.
- Trusting a single artifact: corroborate across at least two independent sources.

## marq tie-in

This box is not a full forensic suite; stage evidence copies under `/work` (file
tools are sandboxed to `/work` + `/tmp`), then run YARA (IOC sweeps), capa (binary
capabilities) and rabin2/strings on captured samples in your own isolated
analysis sandbox (copy only). `report_finding` each artifact-backed conclusion with its source +
hash; `render_report` for the forensic timeline.
