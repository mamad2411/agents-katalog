---
name: opsec-reporting
description: |
  This skill should be used when the user mentions "generate report", "opsec report",
  "engagement report", "pentest report", "red team report", "purple team report",
  "security assessment", "hardening report", "compliance report", "audit report",
  "findings report", "evidence handling", "chain of custody", "redaction", "redact",
  "report delivery", "secure delivery", "debrief", "debrief prep", "post-engagement",
  "artifact inventory", "secure destruction", "evidence capture", "screenshot capture",
  "metadata removal", "report encryption", "encrypted report", "GPG report",
  "compliance reporting", "PCI-DSS report", "SOC2 report", "HIPAA report",
  "CVSS scoring", "DREAD scoring", "severity classification", "finding severity",
  "operational timeline", "timeline documentation", "operation log", "activity log",
  "cleanup report", "trace elimination report", "VPS audit report", "dead drop",
  "secure channel", "report template", "executive summary", or discusses generating
  documentation about operational security posture, engagement results, or red team activities.
  Use this skill even when the user just says "write up the results" or "document what we did"
  in an engagement context.
version: 2.0.0
---

# Opsec Reporting

End-to-end operational reporting for red team engagements — from evidence capture through secure delivery and post-engagement destruction. Every report produced through this skill is designed to protect both the operator and the client by enforcing metadata hygiene, redaction discipline, and secure handling throughout the report lifecycle.

## Why This Matters

Reports are the most dangerous artifact an operator produces. They contain target details, exploitation paths, credentials, and internal architecture — all in a single document. A report leaked, intercepted, or left unencrypted on disk is an operational compromise. This skill treats reports as sensitive material from creation to destruction.

## Report Lifecycle

```
Evidence Capture → Classification → Drafting → Redaction → Encryption → Delivery → Destruction
```

Every phase is documented. Every phase has opsec controls. Skip nothing.

## Report Types

| Report Type | When to Use | Template | Reference |
|-------------|-------------|----------|-----------|
| Engagement Summary | End of any engagement | Executive + technical sections | `references/report-templates.md` |
| Hardening Assessment | After system hardening audit | Coverage map + findings matrix | `references/report-templates.md` |
| Trace Elimination | After cleanup operations | Artifact inventory + verification | `references/report-templates.md` |
| VPS Security Audit | After VPS provisioning/audit | Provisioning checklist + exposure map | `references/report-templates.md` |
| Purple Team Exercise | Joint red/blue engagement | Attack timeline + detection gaps | `references/report-templates.md` |
| Compliance Assessment | PCI-DSS, SOC2, HIPAA mapping | Control mapping + gap analysis | `references/compliance-reporting.md` |
| Debrief Package | Pre-presentation preparation | Slide-ready findings + demo notes | `references/debrief-and-delivery.md` |
| Incident Timeline | Documenting operational chronology | Timestamped event sequence | `references/report-templates.md` |

## Data Collection

Before writing any report, gather all available data from trenton's data layer:

```bash
# Operational data
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" summary
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" coverage
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" list

# Identity rotation history
node "${CLAUDE_PLUGIN_ROOT}/scripts/identity-tracker.js" summary
node "${CLAUDE_PLUGIN_ROOT}/scripts/identity-tracker.js" list

# Current opsec profile
node "${CLAUDE_PLUGIN_ROOT}/scripts/opsec-profile.js" show

# Session state and metrics
node "${CLAUDE_PLUGIN_ROOT}/scripts/session-state.js" show
```

## Evidence Handling

Read `references/evidence-handling.md` for full evidence handling procedures, including:

- Screenshot capture with automatic metadata stripping
- Chain of custody documentation
- Evidence hashing (SHA256) for integrity verification
- Secure evidence storage with encryption at rest
- Evidence correlation and cross-referencing

All evidence must be hashed on capture and logged to the ops tracker:

```bash
# Log evidence capture
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" add \
  --category "reporting" --action "evidence-capture" \
  --detail "Screenshot of <target>:<port> — SHA256:<hash>"
```

## Redaction

Read `references/redaction-methodology.md` for redaction rules by opsec profile. Key principles:

- **Always redact**: Real credentials, API keys, tokens, session cookies
- **Profile-dependent**: IP addresses, hostnames, domain names, employee names
- **Never redact**: Finding descriptions, severity ratings, remediation steps

Redaction markers use consistent format: `[REDACTED-<TYPE>-<SEQ>]` (e.g., `[REDACTED-IP-001]`, `[REDACTED-CRED-003]`). A redaction key mapping markers to real values is stored separately, encrypted, and delivered only to authorized recipients.

## Severity Classification

Findings use dual classification — CVSS 3.1 base score for technical precision, DREAD for business context:

| Severity | CVSS Range | DREAD Range | Report Color |
|----------|-----------|-------------|--------------|
| Critical | 9.0 - 10.0 | 40 - 50 | Red |
| High | 7.0 - 8.9 | 30 - 39 | Orange |
| Medium | 4.0 - 6.9 | 20 - 29 | Yellow |
| Low | 0.1 - 3.9 | 10 - 19 | Blue |
| Informational | 0.0 | 0 - 9 | Gray |

See `references/compliance-reporting.md` for CVSS vector string construction and DREAD scoring methodology.

## Opsec Profile Integration

Report handling adapts to the active opsec profile:

| Aspect | `loud` | `normal` | `stealth` | `paranoid` |
|--------|--------|----------|-----------|------------|
| Report format | Markdown on disk | Markdown on disk | Encrypted Markdown | Memory-only, encrypted export |
| Evidence storage | Plain files | Plain files | GPG-encrypted archive | RAM disk, encrypted export |
| Metadata stripping | None | Basic (exiftool) | Full (mat2 + exiftool) | Full + filename sanitization |
| Delivery method | Email/upload | Encrypted email | Encrypted dead drop | Air-gapped transfer |
| Retention | Indefinite | 90 days | 30 days | Destroy after delivery confirmation |
| Redaction level | Minimal | Standard | Aggressive | Maximum (all identifiers) |

Check the current profile before generating any report:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/opsec-profile.js" get
```

## Report Output

Reports are written to the project directory under `reports/`:

```
reports/
├── engagement-summary-<target>-<YYYYMMDD>.md
├── hardening-<target>-<YYYYMMDD>.md
├── trace-elimination-<target>-<YYYYMMDD>.md
├── vps-audit-<target>-<YYYYMMDD>.md
├── purple-team-<target>-<YYYYMMDD>.md
├── compliance-<framework>-<target>-<YYYYMMDD>.md
├── debrief-<target>-<YYYYMMDD>.md
├── evidence/
│   ├── screenshots/           # Metadata-stripped screenshots
│   ├── captures/              # Network captures, command outputs
│   └── hashes.jsonl           # SHA256 hashes of all evidence files
├── redaction-key-<YYYYMMDD>.gpg  # Encrypted redaction mapping
└── delivery-receipt-<YYYYMMDD>.md # Delivery confirmation log
```

## Report Encryption

For `stealth` and `paranoid` profiles, encrypt reports before writing to disk:

```bash
# GPG symmetric encryption (recipient doesn't need your key)
gpg --symmetric --cipher-algo AES256 --armor \
  -o reports/engagement-summary-target-20260320.md.gpg \
  reports/engagement-summary-target-20260320.md

# Then securely delete the plaintext
shred -vfz -n 3 reports/engagement-summary-target-20260320.md
```

## Secure Delivery

Read `references/debrief-and-delivery.md` for delivery procedures per profile. Quick reference:

| Method | Profile | How |
|--------|---------|-----|
| Direct email | `loud` / `normal` | Attach report, CC stakeholders |
| Encrypted email | `normal` / `stealth` | GPG-encrypted attachment, key exchanged out-of-band |
| Secure file share | `stealth` | Time-limited link (OnionShare, Magic Wormhole, Tresorit) |
| Dead drop | `paranoid` | Pre-arranged location, one-time retrieval, auto-expiry |
| Air-gapped transfer | `paranoid` | USB via secure facility, no network involved |

## Post-Engagement Destruction

After delivery confirmation, destroy local copies according to profile:

```bash
# Secure deletion of report files
shred -vfz -n 3 reports/*.md reports/*.gpg
shred -vfz -n 3 reports/evidence/screenshots/*
shred -vfz -n 3 reports/evidence/captures/*
shred -vfz -n 3 reports/redaction-key-*.gpg

# Wipe free space on the partition (paranoid only)
sfill -v /path/to/reports/

# Log the destruction
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" add \
  --category "reporting" --action "artifact-destruction" \
  --detail "All reports and evidence securely destroyed post-delivery"
```

## Logging

All reporting operations MUST be logged:

```bash
node "${CLAUDE_PLUGIN_ROOT}/scripts/ops-tracker.js" add \
  --category "reporting" --action "<action>" \
  --detail "<detail>"
```

Actions: `evidence-capture`, `report-draft`, `redaction-pass`, `encryption`, `delivery`, `delivery-confirmed`, `artifact-destruction`, `debrief-prep`

## Cross-Skill References

- **Evidence metadata stripping** — see `anti-forensics` skill (`references/metadata-stripping.md`)
- **Secure file deletion** — see `anti-forensics` skill (`references/secure-deletion.md`)
- **VPS audit checks** — see `vps-security` skill
- **System hardening baselines** — see `system-hardening` skill
- **Network anonymity for delivery** — see `network-anonymity` skill

## Reference Files

| File | When to Read |
|------|-------------|
| `references/report-templates.md` | When generating any report — contains all templates |
| `references/evidence-handling.md` | When capturing, storing, or managing evidence and chain of custody |
| `references/redaction-methodology.md` | When redacting sensitive data from reports |
| `references/compliance-reporting.md` | When mapping findings to PCI-DSS, SOC2, HIPAA, or scoring with CVSS/DREAD |
| `references/debrief-and-delivery.md` | When preparing debriefs, delivering reports, or destroying post-engagement artifacts |
