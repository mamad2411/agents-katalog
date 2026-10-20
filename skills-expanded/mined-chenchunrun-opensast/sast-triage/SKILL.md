---
name: sast-triage
description: Triage SAST findings with three-phase workflow (auto-bucket → LLM validate → recommend). Use after running /sast-scan when findings need review.
when_to_use: Use when the user asks to triage SAST results, review findings, identify false positives, prioritize security issues, or bulk-triage scan results.
argument-hint: "[--findings path] [--focus critical|high|medium|low|all] [--output markdown|json] [--bulk]"
allowed-tools:
  - Read
  - Grep
  - Glob
  - "Bash(python3 .claude/skills/sast-scan/tools/triage_findings.py *)"
  - "Bash(python3 .claude/skills/sast-scan/tools/baseline_manager.py *)"
---

# SAST Finding Triage (Three-Phase Workflow)

Triage SAST scan results through a three-phase process:

1. **Phase A — Auto-Bucket** — categorize findings by severity, suppression status, and triage metadata
2. **Phase B — LLM Validate** — validate each finding as TP/FP with confidence scoring and code context
3. **Phase C — Recommend** — generate fix priorities, suppressions for confirmed FPs, and export to baseline

## Required input files

Before triage, confirm these exist:

| File | Required | Purpose |
|------|----------|---------|
| `.claude/sast/results/findings.json` | Yes (or `llm-findings.json`) | Findings to triage |
| `.claude/sast/results/summary.json` | Recommended | Scan context / severity counts |
| `.claude/sast/baseline.json` | Optional | Existing suppressions |

Check session progress:

```bash
python3 .claude/skills/sast-scan/tools/session_status.py --results .claude/sast/results
```

## Input

User arguments:

```text
$ARGUMENTS
```

## Workflow

### Step 1: Phase A — Auto-Bucket

Run the structured triage helper:

```bash
python3 .claude/skills/sast-scan/tools/triage_findings.py --findings .claude/sast/results/findings.json --focus all --output markdown
```

Or use bulk mode for the full pipeline:

```bash
python3 .claude/skills/sast-scan/tools/triage_findings.py --findings .claude/sast/results/findings.json --bulk --repo-root .
```

Read findings from `.claude/sast/results/findings.json` (or `.claude/sast/results/llm-findings.json`).

Auto-bucket findings into:
- **Priority**: critical/high issues that should block or be fixed first
- **Important**: medium/low issues that are still actionable
- **Needs Review**: not clearly false, but needs manual validation
- **False Positive / Suppressed**: can be suppressed with evidence
- **Informational**: low-value context

### Step 2: Phase B — LLM Validate

For each finding in Priority and Important buckets, use Claude to validate:

Use the `--bulk` flag to generate validation targets with code context. For each target:

1. **Assess false positive likelihood**:
   - Is the input actually user-controlled? Is there a sanitizer?
   - Is the code path reachable from an external entry point?
   - Is the finding in test code, generated code, or dead code?
   - Does the framework provide built-in protection?

2. **Score confidence** (0.0-1.0):
   - 0.9+ : Definitely true positive, high exploitability
   - 0.7-0.9: Likely true positive, needs verification
   - 0.3-0.7: Uncertain, needs manual review
   - 0.0-0.3: Likely false positive

3. **Assign verdict**: TP or FP with rationale

4. **Apply verdicts** using `apply_triage_verdicts()` to update findings with triage metadata.

### Step 3: Phase C — Recommend

For true positives, produce:

1. **Priority fix list** ordered by:
   - Severity (critical → low)
   - Exploitability (remote > local > requires auth)
   - Business impact (data breach > service disruption > information leak)

2. **Estimated effort** for each fix:
   - Low: One-line change, configuration update
   - Medium: Function-level change, middleware addition
   - High: Architecture change, multi-file refactor

3. **For confirmed false positives**, generate suppression entries:

```json
{
  "fingerprint": "...",
  "reason": "Explanation of why this is a false positive",
  "owner": "triage-analyst",
  "confidence": 0.85,
  "expires_at": "2026-12-31"
}
```

4. **Export to baseline** (optional):

```bash
# Auto-suppress FPs with confidence >= 0.7
python3 .claude/skills/sast-scan/tools/triage_findings.py --findings .claude/sast/results/findings.json --export-baseline .claude/sast/baseline.json
```

## Output format

```markdown
# SAST Triage Report

## Summary
- Focus: all
- Total findings: X
- Priority: X
- Important: X
- Needs review: X
- False positive / suppressed: X
- Informational: X

## Priority Fix List
1. [CRITICAL] Title — File:Line — (confidence: 0.95)
2. [HIGH] Title — File:Line — (confidence: 0.80)
...

## Needs Review
1. Title — File:Line — Rationale for uncertainty

## False Positive / Suppressed
1. Title — File:Line — Reason — (confidence: 0.90)

## Recommended Suppressions
| Fingerprint | Reason | Confidence |
|-------------|--------|------------|
| fp-abc123... | Framework provides CSRF protection | 0.85 |
```

## Triage criteria

When evaluating false positives, consider:
- Is the source actually user-controlled? (request params, file uploads, API input)
- Is there a sanitizer or validator between source and sink?
- Is the code path reachable from an external entry point?
- Is the finding in test code or dead code?
- Does the framework provide built-in protection?
- Is the severity appropriate for the actual exploitability?

## Integration with other skills

- **Input from**: `/sast-scan` findings (both rule-based and LLM-generated)
- **Output to**: `/sast-baseline` (suppressions), `/sast-fix` (prioritized findings)
- **Workflow**: scan → triage → fix → verify

## Next Skill (required at end of triage response)

```markdown
## Next steps
1. **Suppress FPs:** `/sast-baseline suppress --fingerprint <fp> --reason "..."` or `--export-baseline` from triage
2. **Fix TPs:** `/sast-fix <fingerprint> --test`
3. **Re-scan:** `/sast-scan --changed-only --profile quick`
```
