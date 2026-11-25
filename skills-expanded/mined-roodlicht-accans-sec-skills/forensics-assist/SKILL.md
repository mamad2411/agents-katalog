---
name: forensics-assist
description: Digital-forensics assistant for IR context — memory analysis via Volatility 3, disk-imaging hygiene (write-blocker, hash validation), timeline reconstruction via plaso/log2timeline, file-system artifacts per OS. Audit-grade evidence; courtroom-grade chain of custody requires additional specialized forensics work.
---

# Forensics Assist

> **Audit-grade vs. forensics-grade**: this skill supports incident-response-grade investigation with evidence that can later be supplemented for legal proceedings, but it is not on its own a fully chain-of-custody-certified forensics output. Specialized forensic teams (an internal forensics cell or an external partner such as Fox-IT or Northwave) handle the courtroom-grade work where required. The skill structures hash validation, write-blocker discipline, and timeline reconstruction so the output is usable for IR plus any follow-up forensics.

## When to use

An incident often calls for forensic investigation in parallel with IR action. This skill provides the practical lens for the blue-team side: what you capture, how you analyse it, and what you hand off to IR or specialized forensics.

Triggers on:

- A question like "memory analysis on this dump", "disk-image hygiene check", "build a timeline from this event log + filesystem", "what is known from MFT", "Volatility plugin choice".
- A handoff from `ir-runbook` (forensics step inside the response), `malware-triage` (memory-extracted binary), `log-triage` (host investigation after an anomaly).
- A suspect host snapshot where you must determine "what happened, how far did it go, how long has it been there".
- Periodic training or post-incident review where a sample investigation is repeated.

### When NOT (handoff)

- Courtroom-grade forensics → specialized team. This skill is operational-grade.
- Reverse engineering a sample in detail → `malware-triage`.
- IR coordination itself → `ir-runbook`.
- Detection-rule building from findings → `detection-engineer`.
- IOC extraction and sharing → `ioc-hunter`.
- Cloud forensics specifically (AWS snapshots, Azure disk export, M365 eDiscovery): partly in scope (interpreting artifacts), provider-specific workflows coordinated with the cloud team.
- E-Discovery for litigation → legal team plus specialized tooling (Relativity, Nuix).

## Approach

Six phases. Phase 1 (acquisition discipline) is where evidence value is preserved; phase 4 (timeline) is where forensic work becomes a story.

### 1. Acquisition: hygiene and chain

Foundation. A corrupted-acquisition disk makes later analysis untrustworthy.

- **Write blocker** for disk acquisition: hardware blocker (Tableau, Wiebetech, CRU) or software write blocker if hardware is not available. Goal: do not modify the source disk.
- **Hash validation**: compute the source hash before and after imaging via FTK Imager / dd / Guymager. If the hashes match, the image is bit-identical to the source at that moment.
- **Image formats**: raw `.dd`, EnCase `.E01` (compressed + metadata), AFF4. For IR context, typically `.dd` or `.E01`.
- **Memory acquisition** before power-off where possible: WinPMEM (Windows), AVML (Linux), osxpmem (macOS). Memory holds process info, network state, decrypted data — destroyed at shutdown.
- **Live-response data** as an alternative to a full image where full is impossible: KAPE (Kroll Artifact Parser/Extractor) for targeted artifact collection, Velociraptor for live collection across an endpoint fleet.
- **Chain-of-custody record**: who collected, when, how transferred, who had access. Sufficient for audit-grade; for evidentiary-grade more discipline is needed (signed, witness present, dual control).

Output of phase 1: hash-confirmed image plus collection log. Only then begin analysis.

### 2. Memory analysis with Volatility 3

Volatility 3 is the open-source standard.

```bash
# Profile auto-detect
vol -f mem.raw windows.info

# Process listing and any hidden processes
vol -f mem.raw windows.pslist
vol -f mem.raw windows.psscan      # carved processes (can show hidden)
vol -f mem.raw windows.pstree

# Network connections at the time of capture
vol -f mem.raw windows.netscan

# Process-injection detection
vol -f mem.raw windows.malfind

# Loaded DLLs / suspicious imports
vol -f mem.raw windows.dlllist --pid <PID>

# Command-line forensics
vol -f mem.raw windows.cmdline
```

Plugin categories to walk through by default:

- **Process state**: pslist, pstree, psscan (carved), psxview (cross-source), malfind (process injection).
- **Network**: netscan, netstat (kernel state).
- **DLL/handle**: dlllist, handles, modules.
- **Registry from memory**: windows.registry.printkey, hashdump.
- **Filesystem**: filescan, dumpfiles.
- **Userland**: cmdline, getsids, sessions.

For Linux: `linux.pslist`, `linux.netstat`, `linux.bash` (bash history from memory), `linux.malfind`. For macOS: `mac.pslist`, `mac.netstat`, etc.

Memory evidence is volatile — once dumped, it is a snapshot. Document the capture time carefully.

### 3. Disk analysis and filesystem artifacts

Artifacts differ per OS. Top sources to consult by default:

**Windows**:

- **MFT** (Master File Table) — record of all file creates/changes. `MFTECmd` (Eric Zimmerman tools) parses to timeline-friendly output.
- **USN journal** — change log of NTFS, faster to age out.
- **Event logs** (`%SystemRoot%\System32\winevt\Logs\*.evtx`): Security, System, Application, plus the PowerShell log, Sysmon log, RDP log.
- **Registry hives**: SOFTWARE, SYSTEM, SAM, NTUSER.DAT, USRCLASS.DAT. RegRipper for parsing.
- **Prefetch** (`%SystemRoot%\Prefetch\*.pf`): execution history. PECmd for parsing.
- **Shimcache / AmCache**: app-execution evidence.
- **LNK files** in Recent: file-access history.
- **Browser history**: per-browser SQLite databases.
- **ShellBags** (registry): folder-navigation evidence.
- **SRUM** (System Resource Usage Monitor): per-process resource usage with timestamps.

**Linux**:

- **bash_history** + zsh_history.
- **/var/log/auth.log**, syslog, journald (`journalctl`).
- **inotify events** where configured.
- **systemd journal** for unit execution.
- **crontab + at-jobs** for persistence.
- **last/wtmp** for login history.

**macOS**:

- **Unified logs** (`log show --predicate ...`).
- **plist files** for LaunchAgents/LaunchDaemons.
- **FSEvents** for filesystem changes.
- **Quarantine database** for downloaded-files tracking.

Tool packages: KAPE targets per OS, Eric Zimmerman tools (MFTECmd, RECmd, EvtxECmd, AmcacheParser, etc.), Plaso/log2timeline for a unified timeline.

### 4. Timeline reconstruction

A timeline turns forensic work into story. plaso/log2timeline aggregates artifacts into one timeline.

```bash
# Plaso parses image to .plaso storage
log2timeline.py --storage-file mfx.plaso /evidence/disk.E01

# Timeline output as CSV
psort.py -o l2tcsv -w timeline.csv mfx.plaso

# Filter on time window and source
psort.py -o dynamic -w timeline-filtered.csv mfx.plaso "date > '2026-04-20 09:00:00'"
```

Discipline:

- **Time-zone discipline**: all artifacts to one time zone (UTC default in Plaso). Per-source clocks may drift — document.
- **Pivot points**: a known-suspect event (a specific process execution, a log anomaly) as anchor. Work N minutes before and after.
- **Multi-source**: filesystem + registry + event logs + browser data together tell the story. A single-source timeline lacks context.
- **Visualization**: Timesketch (open-source, by Google), or CSV in Excel/Tableau for smaller datasets.
- **Anti-forensics aware**: timestomping (T1070.006), log clearing (T1070.001) — if the artifact timeline is inconsistent, possibly tampered. Document.

### 5. Reporting and handoff

Output fits in the `ir-runbook` incident log or as an appendix to a `pentest-reporter`-style finding. Structure:

- **Acquisition context**: source, method, hash confirmation, time of capture.
- **Top findings** prioritized by IR impact: persistence, lateral-movement evidence, data-exfil evidence, malware presence.
- **Timeline** around pivot events.
- **Open questions** for specialized forensics if courtroom-grade is needed.
- **Recommendations** for cleanup and re-image-or-restore strategy.

### 6. Verification-loop

Layer 1: scope (all expected artifacts checked for the OS, no single-source tunnel vision?), assumptions (capture time zone documented, pre/post hashes match?), gaps (anti-forensics possibilities considered?). Layer 2: tool names against current versions (Volatility 2 vs 3, Plaso syntax changes), filesystem-artifact names correct (Windows evolution between 10/11; macOS artifacts between Catalina/Ventura/Sonoma), no invented registry paths.

## Output

```
Forensics findings — <host / case-ID>
Acquisition:
  Type:               <full-disk image / memory-only / live-response>
  Tool:               <Tableau / WinPMEM / KAPE / etc>
  Capture time:       <UTC + local + TZ>
  Hash pre/post:      <verified | mismatch>
  Storage:            <encrypted vault path + chain-of-custody ref>

Memory analysis (if dump):
  Profile:            <auto-detected version>
  Process tree:       <summary of suspect branches>
  Network state:      <connections at capture>
  Process injection:  <malfind hits + PIDs>
  Hidden processes:   <psxview discrepancies>

Disk/filesystem (per platform):
  MFT/USN highlights:    <suspect file creates/changes>
  Event-log highlights:  <Security/PowerShell/Sysmon anomalies>
  Registry highlights:   <persistence keys, recent-doc traces>
  Execution evidence:    <Prefetch / Shimcache / AmCache / SRUM>
  Browser history:       <suspect URLs>

Timeline (around pivot events):
  T-30m → T+30m chronological overview

Anti-forensics signal:
  <if timestomping / log clear / journal truncation detected>

Findings prioritized:
  Persistence:        <mechanism + location>
  Lateral movement:   <evidence of connection / credential use>
  Data exfil:         <evidence of outbound volume / staged archives>
  Malware:            <hash + handoff to malware-triage>

Open questions for specialist forensics:
  - <which questions require courtroom-grade work>

Handoffs:
  ir-runbook:         <findings → response action>
  malware-triage:     <if sample/memory-extracted binary>
  ioc-hunter:         <extracted IOCs>
  detection-engineer: <patterns for future detection>

Verification-loop: ...
```

## References

- **Volatility 3** — [https://github.com/volatilityfoundation/volatility3](https://github.com/volatilityfoundation/volatility3). Memory-analysis framework.
- **Plaso / log2timeline** — [https://plaso.readthedocs.io/](https://plaso.readthedocs.io/). Timeline reconstruction.
- **Timesketch** — [https://timesketch.org/](https://timesketch.org/). Collaborative timeline analysis.
- **Eric Zimmerman tools** — [https://ericzimmerman.github.io/](https://ericzimmerman.github.io/). MFTECmd, RECmd, EvtxECmd, AmcacheParser, PECmd. Free, quality standard for Windows forensics.
- **KAPE** — [https://www.kroll.com/en/services/cyber-risk/incident-response-litigation-support/kroll-artifact-parser-extractor-kape](https://www.kroll.com/en/services/cyber-risk/incident-response-litigation-support/kroll-artifact-parser-extractor-kape). Live-response artifact collection.
- **Velociraptor** — [https://docs.velociraptor.app/](https://docs.velociraptor.app/). Endpoint-fleet collection and hunting.
- **SANS DFIR posters** — [https://www.sans.org/posters/](https://www.sans.org/posters/). Per-OS artifact-overview posters.
- **NIST SP 800-86** — [https://csrc.nist.gov/pubs/sp/800/86/final](https://csrc.nist.gov/pubs/sp/800/86/final). Guide to Integrating Forensic Techniques into Incident Response.
- **MITRE ATT&CK — Defense Evasion (anti-forensics)** — [https://attack.mitre.org/tactics/TA0005/](https://attack.mitre.org/tactics/TA0005/). T1070-class.
- **NCSC-NL forensic-readiness guideline** — [https://www.ncsc.nl/](https://www.ncsc.nl/). NL context.

## Categories

- blue
