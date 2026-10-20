---
name: autopsy-case-basics
description: >
  Autopsy digital forensics case workflow for owned DFIR labs and authorized
  investigations: creating cases, adding disk/image data sources, ingest modules,
  keyword/hash sets, timelines, tagging, and reporting. Use when triaging disk
  images in Autopsy/Sleuth Kit — not for unauthorized access to systems or data
  outside legal/organizational authority.
---

# Autopsy Case Basics

## Scope And Authorization

- **In scope:** Disk images, memory captures, and logical files you are legally authorized to examine (owned labs, warrants, corporate IR with authority).
- **Out of scope:** Imaging or analyzing systems/data without authorization; privacy-invasive use outside mandate.
- Maintain chain of custody: hash evidence, work on copies, log access.
- Redact PII in reports when sharing beyond the investigation team.
- Pair tooling notes with org IR process; use `code-quality-standards` only if scripting plugins.

## When To Use

- Opening a new Autopsy case for a disk image (E01, raw/dd, VMDK, etc.).
- Running ingest modules (hash lookup, keyword search, recent activity, EXIF, …).
- Building timelines, tagging artifacts, and exporting reports.
- Teaching DFIR lab workflows with public datasets.
- Coordinating multi-examiner cases with central repository (if licensed/used).

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Live network traffic PCAP | `traffic-analysis-pcap` / NetworkProtocolAnalysisSkill |
| Malware reverse engineering | `binary-re/*` skills |
| Cloud log IR only | cloud forensics skills |
| Legal process / warrants | counsel / IR leadership — not this skill |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| Concept | Guidance |
| --- | --- |
| Case | Container for evidence, databases, reports |
| Data source | Image/logical/local disk added once; verify hash |
| Ingest | Background analysis modules; enable only needed |
| Notable files / tags | Examiner conclusions must be evidence-backed |
| Timeline | Combined events; filter noise |
| Report | Portable HTML/Excel/etc. for stakeholders |

## Evidence Handling Rules

| Rule | Practice |
| --- | --- |
| Work copies | Never analyze the only original without write-blocker policy |
| Hashing | MD5/SHA-256 of image at acquisition and when adding |
| Notes | Examiner log: who/when/what action |
| Isolation | Analysis workstation network policy per org IR |

## Workflow

### 1. Confirm scope and success criteria

1. Record legal basis, case ID, custodian, systems in scope, retention policy.
2. Success: image hashes verified; ingest complete without corruption; key artifacts tagged with paths/timestamps; report delivered.
3. Identify tools version (Autopsy x.y) for reproducibility.

### 2. Create case and add data source

1. **File → New Case**: case name, number, base directory on large fast disk.
2. Optional: single-user vs multi-user (Solr/PostgreSQL) per org setup.
3. **Add Data Source**: choose image type; point to E01/raw; verify hash matches acquisition sheet.
4. Time zone settings: set consistent zone for timeline interpretation.

```bash
# Host-side hash verification before add (example)
sha256sum evidence.dd
# or for E01 use ewfacquire/ewfverify ecosystem as available
```

### 3. Baseline / acquisition metadata

1. Store acquisition form: tool, version, examiner, date, hash, source serial.
2. Photograph or note write-blocker model when physical disks used.
3. Keep originals read-only; Autopsy case DB is derivative.

### 4. Configure ingest modules

| Module | Use when |
| --- | --- |
| Hash lookup | NSRL / custom malware hash sets |
| Keyword search | Terms from investigation plan |
| Recent activity | Web, USB, installed programs cues |
| EXIF parser | Image provenance |
| Email parser | PST/MBOX present |
| Encryption detection | BitLocker/possible crypto containers |
| Interesting files | Extension/path heuristics |

1. Start with a focused module set on large images to save time; re-run selective ingest later.
2. Add hash sets and keyword lists from approved investigation sources only.
3. Monitor ingest progress; free disk space for temp/solr indexes.

### 5. Analyze with evidence discipline

1. **Views**: Directory tree, views by type (images, documents, executables).
2. **Keyword hits**: open hit → verify context; tag true positives.
3. **Timeline**: filter by date range around incident; export relevant spans.
4. **Accounts / Web**: correlate logons and browser artifacts carefully (timezone!).
5. Tag schema example: `suspicious`, `exfil-candidate`, `malware-path`, `benign-known`.
6. Do not assert intent without supporting artifacts; separate fact vs hypothesis in notes.

### 6. Verify and report

1. Re-check image hash if case moved between disks.
2. Cross-verify critical files with independent tools (`istat`, `fls`, `icap`/Sleuth Kit CLI) when results drive major decisions.
3. Generate Autopsy report; include hashes, case ID, examiner, tool versions.
4. Peer review tags for high-impact findings.

```bash
# Example independent listing (Sleuth Kit)
fls -r -m / evidence.dd | head
```

### 7. Hand off and retention

1. Archive case folder per retention; encrypt if policy requires.
2. Deliver report + exhibit file exports with path and hash of each exhibit.
3. Document negative findings (what was searched and not found) when relevant.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Authority | Written scope/case number | “Curious” imaging of random machines |
| Evidence | Hashed copies + logs | Working on original RW mounted |
| Analysis | Tagged paths + timestamps | Screenshots only, no artifact path |
| Keywords | Investigation-driven lists | unbounded phishing of personal data out of scope |
| Reports | Tool versions + hashes | Unverifiable claims |
| Scope creep | Re-authorize expansion | Silent expansion to personal files |

## Output Checklist

- [ ] Legal/org authorization and case ID recorded
- [ ] Image hash verified on add
- [ ] Case storage path and Autopsy version noted
- [ ] Ingest modules justified and completed
- [ ] Keyword/hash sets documented
- [ ] Timeline window analyzed; artifacts tagged with paths
- [ ] Independent verification for critical exhibits
- [ ] Report with hashes and examiner notes delivered
- [ ] Retention/custody handoff done

## Rules

- Authorization and privacy first; Autopsy does not create legal authority.
- Always hash and work from forensic images/copies per policy.
- Separate facts (artifact + path + time) from hypotheses.
- Redact sensitive data in external reports as required.
- Focus on Autopsy case workflow; deep malware RE and network forensics use other skills.
