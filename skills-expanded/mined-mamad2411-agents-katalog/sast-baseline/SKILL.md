---
name: sast-baseline
description: Manage SAST scan baselines with full lifecycle operations (create, update, show, suppress, diff, stats, audit, cleanup, import). Use to suppress accepted risks and focus on new issues.
when_to_use: Use when the user asks to manage SAST baselines, suppress findings, accept known risks, review suppression lists, audit baseline changes, or compare findings over time.
argument-hint: "[create|update|show|suppress|unsuppress|diff|stats|audit|cleanup|import] [options]"
allowed-tools:
  - Read
  - Glob
  - "Bash(python3 .claude/skills/sast-scan/tools/baseline_manager.py *)"
  - "Bash(python3 .claude/skills/sast-scan/tools/triage_findings.py *)"
---

# SAST Baseline Management (Full Lifecycle)

Manage the baseline of known SAST findings with comprehensive lifecycle operations:

- Suppress accepted risks and false positives
- Track suppression changes with audit trail
- Compare findings over time
- Bulk import from triage results
- Auto-cleanup expired suppressions

## Input

User arguments:

```text
$ARGUMENTS
```

## Commands

### create
Generate a new baseline from the latest scan results:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py create
```

### show
Display the current baseline summary:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py show
```

### update
Refresh the baseline with the latest findings:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py update
```

### suppress
Add a suppression for a specific finding fingerprint:
- Requires `--fingerprint` and `--reason`
- Optional `--expires-at` for temporary suppressions
- Optional `--owner` to record who approved

```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py suppress \
  --fingerprint fp-abc123 --reason "False positive: framework CSRF protection" --owner security-team
```

### unsuppress
Remove a suppression by fingerprint:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py unsuppress --fingerprint fp-abc123
```

### diff
Compare current baseline against latest findings to see what changed:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py diff
```

Output includes:
- New fingerprints added (new findings)
- Fingerprints removed (resolved findings)
- Suppressions added/removed

### stats
Show baseline analytics:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py stats
```

Returns:
- Total fingerprints tracked
- Total suppressions (active, expired, permanent)
- Created/updated timestamps

### audit
Show suppression change history:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py audit --limit 50
```

Returns the most recent audit trail entries, including:
- Action (add/update/remove/cleanup_expired/import)
- Fingerprint affected
- Detail (reason or change description)
- Owner who made the change
- Timestamp

### cleanup
Remove expired suppressions:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py cleanup
```

Removes all suppressions where `expires_at` is in the past.

### import
Bulk import suppressions from a JSON file:
```bash
python3 .claude/skills/sast-scan/tools/baseline_manager.py import --import-file triage-results.json
```

Import file format:
```json
[
  {"fingerprint": "fp-1", "reason": "False positive", "expires_at": null},
  {"fingerprint": "fp-2", "reason": "Accepted risk", "expires_at": "2026-12-31"}
]
```

Skips fingerprints that already have suppressions.

## Workflow

1. **After first scan**: Create a baseline
   ```bash
   python3 .claude/skills/sast-scan/tools/baseline_manager.py create
   ```

2. **Review findings**: Run `/sast-triage` to categorize findings

3. **Suppress FPs**: Suppress confirmed false positives
   ```bash
   python3 .claude/skills/sast-scan/tools/baseline_manager.py suppress --fingerprint fp-1 --reason "Framework CSRF protection"
   ```

4. **On subsequent scans**: Update baseline and diff
   ```bash
   python3 .claude/skills/sast-scan/tools/baseline_manager.py update
   python3 .claude/skills/sast-scan/tools/baseline_manager.py diff
   ```

5. **Periodic review**: Check stats and cleanup
   ```bash
   python3 .claude/skills/sast-scan/tools/baseline_manager.py stats
   python3 .claude/skills/sast-scan/tools/baseline_manager.py cleanup
   python3 .claude/skills/sast-scan/tools/baseline_manager.py audit
   ```

## Suppression policy

Suppressions should include:
- **reason**: Why the finding is accepted (false positive, accepted risk, mitigated elsewhere)
- **owner**: Who approved the suppression
- **expires_at**: When to re-review (mandatory for accepted risks, optional for false positives)
- **confidence**: From triage (if available)

## Guidelines

- Never suppress findings without a documented reason.
- Prefer fixing over suppressing.
- Review suppressions quarterly (use `stats` to see expired ones).
- Temporary suppressions must have an expiry date.
- False positive suppressions should include evidence of why it's a FP.
- Use `audit` to track who changed what and when.

## Integration with other skills

- **Input from**: `/sast-triage` (confirmed FPs to suppress), `/sast-scan` (findings to baseline)
- **Output to**: `/sast-scan` (suppressed findings filtered from future reports)
- **Workflow**: scan → triage → baseline → fix → verify
