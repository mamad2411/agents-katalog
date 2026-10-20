---
name: validate-scan
description: >
  Independent validation agent that reviews all findings from escalate-scan with
  fresh context. Each finding is assessed by a bias-free reviewer that receives
  ONLY the finding + evidence (no original scan context) and independently
  determines whether the evidence actually proves the claimed vulnerability.
  Applies self-reflection (argues why each finding might be a false positive)
  and drops or downgrades findings that don't survive scrutiny. This breaks
  the "I found it so it must be real" confirmation bias that scan agents have.
  For Critical and High findings, runs THREE independent reviewers with
  different priors (skeptical / engineering / operations) and requires
  ≥2-of-3 consensus before CONFIRM is allowed — Anthropic's
  Firefox-collaboration multi-reviewer rule, slightly relaxed for recall.
  Inspired by Anthropic's Mythos secondary validation agent methodology.
  Use when the user invokes "validate-scan", "validate findings",
  "secondary validation", "independent review", "3-reviewer consensus",
  or "bias-free review".
---

# Validate Scan — Independent Finding Validation Agent

## Purpose

Act as an **independent, bias-free reviewer** of all findings from escalate-scan.
You have NOT seen the original scan. You receive ONLY the findings report and must
independently determine whether each finding's evidence actually proves the claim.

This skill implements two key techniques from Anthropic's Mythos methodology:
1. **Secondary validation agent** — a separate reviewer with fresh context
2. **Self-reflection loop** — explicitly arguing why each finding might be wrong

**Core principle**: If you can construct a plausible argument that a finding is a
false positive, AND the evidence doesn't definitively refute that argument, the
finding should be downgraded or dropped.

## Scan Progress Checklist

```
Validation Progress:
- [ ] Step 0:   Load escalated findings report
- [ ] Step 0b:  Reviewer-pool setup (Critical/High → 3 reviewers; Medium/Low → 1)
- [ ] Step 1:   Independent evidence review (per finding, per reviewer)
- [ ] Step 2:   Self-reflection challenge (argue false positive)
- [ ] Step 3:   Live re-probe of contested findings
- [ ] Step 4:   Verdict assignment (confirm / downgrade / drop)
- [ ] Step 4b:  Consensus rule (≥2-of-3 to CONFIRM Critical/High)
- [ ] Step 5:   Output validated findings report
```

---

## Step 0 — Load Findings

1. Read the escalated findings report (passed via `--report` argument)
2. Extract all findings with `reportable: true`
3. Also load findings with `reportable: false` — these will be checked for
   incorrect rejections (false negatives)
4. **Do NOT read** any other scan artifacts (raw URLs, recon output, agent logs).
   You must assess findings based ONLY on the evidence provided in each finding.
   This isolation is intentional — it prevents confirmation bias.

Print: "Loaded N reportable + M rejected findings for independent validation"

---

## Step 0b — Reviewer-Pool Setup

For Critical and High findings, this skill runs **three independent
reviewers** in parallel and requires ≥2-of-3 to vote CONFIRM before
the final verdict can be CONFIRM. This is Anthropic's Firefox-collaboration
multi-reviewer rule (the strictest version is unanimity; we relax to
≥2-of-3 to balance recall against precision).

Findings outside Critical/High keep the existing single-reviewer flow —
the cost of an erroneous CONFIRM on a Low finding is small, and tripling
the review cost for every finding is wasteful.

### 0b-1 — Partition findings

```
H = findings with severity ∈ {Critical, High}
L = findings with severity ∈ {Medium, Low, Info}
```

### 0b-2 — Reviewer roster (for set H)

For each finding in H, dispatch THREE Agent invocations in a single
message (parallel). Each receives ONLY the finding object (per Step 0's
isolation rule) and one of the following priors:

| Reviewer | Prior                                                                        | CONFIRM bar                                                          |
|----------|------------------------------------------------------------------------------|----------------------------------------------------------------------|
| **A — skeptical**     | "treat every claim as suspect; assume false-positive until proven otherwise" | "the evidence definitively proves exploitation right now"             |
| **B — engineering**   | "could a working POC be written from this evidence today, no manual fill-in?" | "yes, with high confidence"                                          |
| **C — operations**    | "as the asset owner, would I lose sleep over this if it were left unfixed?"  | "yes, this represents real risk to production"                        |

Each reviewer runs Steps 1-3 INDEPENDENTLY using their prior — they do
not see each other's output. Each emits a Step 4 verdict (CONFIRM,
DOWNGRADE, or DROP) and a 1-2 sentence rationale.

### 0b-3 — Single-reviewer path (set L)

For each finding in L, run the existing Steps 1-4 flow once with the
default reviewer prompt. Skip Step 4b for these findings — `consensus_count`
is recorded as `null`.

### 0b-4 — Budget guardrail

If `|H| > 30`, print a warning and ask the user to confirm. Three
reviewers per finding × 30 findings = 90 Agent dispatches; the user
should know this is what the skill is about to do.

A user who wants single-reviewer behaviour for everything (e.g., for
quick re-runs) can set `SINGLE_REVIEWER=1` in the environment to skip
this step entirely. The Step 4b consensus rule then becomes a no-op.

---

## Step 1 — Independent Evidence Review

For each reportable finding, perform an **isolated assessment**. Evaluate ONLY
what is present in the finding object:

### 1a — Evidence Completeness Check

For each finding, verify these fields exist and are meaningful:

| Field | Required | Check |
|-------|----------|-------|
| `affected_url` | Yes | Must be a real URL, not a pattern or placeholder |
| `evidence` | Yes | Must contain specific data (not "vulnerability found") |
| `verification_output` | Yes | Must contain actual HTTP response data |
| `evidence_type` | Yes | Must be `exploitation`, `code_analysis`, or `inferred` |
| `verified` | Yes | Must match evidence_type rules |
| `verification_note` | If verified:false | Must explain why |

**Missing or empty `verification_output`** → flag as `evidence_incomplete`.
A finding with no response data is unverifiable.

### 1b — Evidence-Claim Alignment

Does the evidence actually prove what the title claims?

- **XSS finding**: Does `verification_output` show the canary/payload reflected
  in an executable HTML context? Or just reflected in a JSON response / comment?
- **SQLi finding**: Does it show actual SQL error or timing difference? Or just
  a different response length that could be normal variation?
- **SSRF finding**: Was an OOB callback actually received? Or just assumed?
- **Rate limit finding**: Were 3+ rapid requests sent with no 429? Or was only
  1 request tested?
- **Header finding**: Is the missing header actually security-relevant for this
  specific endpoint type?
- **Secret finding**: Is the matched string actually a live secret? Or a test
  key, example, or documentation value?
- **CORS finding**: Does it show `Access-Control-Allow-Credentials: true` with
  reflected origin? Or just `Access-Control-Allow-Origin: *` (often acceptable)?

Assign: `evidence_alignment: "strong" | "weak" | "mismatch"`

### 1c — Severity Calibration

Is the assigned severity proportional to the actual demonstrated impact?

- A reflected XSS requiring user interaction should not be Critical
- A missing optional header should not be Medium
- An info disclosure of non-sensitive public data should not be High
- An IDOR that only shows the user's own data should not be High

Flag any finding where severity seems inflated: `severity_check: "appropriate" | "inflated"`

---

## Step 2 — Self-Reflection Challenge

For EVERY finding that passed Step 1, apply the self-reflection loop.

**For each finding, explicitly answer these 3 questions:**

### Q1 — "Why might this be a false positive?"

Construct the strongest argument you can for why this finding is NOT real:
- Could the "vulnerability" be normal application behavior?
- Could the reflected content be safely encoded/escaped in context?
- Could the error message be a generic handler, not a real SQL error?
- Could the "secret" be a public/test/example value?
- Could the "missing" header be irrelevant for this endpoint?
- Could an auth barrier exist that the scan missed?

Write this argument in `false_positive_argument`.

### Q2 — "Does the evidence definitively refute my false-positive argument?"

Look at the actual `verification_output` and `evidence`:
- Is there concrete proof that defeats the false-positive argument?
- Or is the evidence ambiguous / could be interpreted either way?

Write this in `evidence_rebuttal`.

### Q3 — "If I showed only this evidence to a senior pentester, would they accept it?"

Apply the "senior pentester test":
- Would a senior pentester look at this `verification_output` and say "yes, this is real"?
- Or would they say "this needs more investigation" or "this is noise"?

Assign: `senior_pentester_verdict: "accept" | "investigate_more" | "reject"`

---

## Step 3 — Live Re-Probe of Contested Findings

For findings where Step 2 produced ambiguous results (`investigate_more`),
perform a **single independent verification request**:

```bash
curl -sk --max-time 10 -o /dev/null -w "%{http_code}" "$affected_url"
```

Then a targeted probe based on vuln class:

- **XSS**: `curl -sk --max-time 10 "$poc_url" | grep -c "$canary_or_payload"`
- **SQLi**: Compare baseline vs payload response lengths
- **CORS**: `curl -sI -H "Origin: https://evil.attacker.com" "$url"`
- **Headers**: `curl -sI "$url"` and check specific header
- **Secrets**: `curl -sk "$url" | grep "$pattern"`
- **Rate limit**: 3 rapid requests, check for 429

**Maximum 2 requests per finding. No exceptions.**

Check response for auth barriers:
```
grep -iE "password|pin.*code|enter.*pin|login.*required|sign.*in|
  <input.*type=.password|WWW-Authenticate|oauth.*redirect" response
```
Auth barrier detected → `verdict: "drop"`, reason: "auth barrier — not exploitable unauthenticated"

---

## Step 4 — Verdict Assignment

Based on Steps 1-3, assign a verdict to each finding:

### Verdict: CONFIRM
Requirements (ALL must be true):
- `evidence_alignment: "strong"`
- `severity_check: "appropriate"`
- `senior_pentester_verdict: "accept"`
- No auth barrier detected
- `evidence_type: "exploitation"` with actual HTTP proof

Action: Keep finding as-is. Set `validation_status: "confirmed"`.

### Verdict: DOWNGRADE
Conditions (ANY):
- `severity_check: "inflated"` — reduce severity one level
- `evidence_alignment: "weak"` but finding is likely real — add caveat
- `senior_pentester_verdict: "investigate_more"` after re-probe — cap at Medium
- `evidence_type: "code_analysis"` — cap at Medium, note requires manual testing

Action: Reduce severity and/or add qualification. Set `validation_status: "downgraded"`.
Add `downgrade_reason` explaining what changed.

### Verdict: DROP
Conditions (ANY):
- `evidence_alignment: "mismatch"` — evidence doesn't match claim
- `senior_pentester_verdict: "reject"`
- Auth barrier detected on re-probe
- `verification_output` is empty/missing and re-probe fails
- False-positive argument is convincing AND evidence doesn't refute it
- Finding references URLs/endpoints that were never actually observed in scan data

Action: Mark `reportable: false`. Set `validation_status: "dropped"`.
Add `drop_reason` explaining why.

### Verdict Recovery — False Negative Check

For findings that escalate-scan marked `reportable: false`:
- If the rejection reason seems incorrect based on the evidence, flag it
- Example: finding rejected as "theoretical_only" but `verification_output`
  contains actual exploitable response
- Set `validation_status: "recovered"`, `reportable: true`

---

## Step 4b — Consensus Rule (Critical/High only)

For findings in set H from Step 0b-1, merge the three reviewer verdicts
using this table. Set L findings (single reviewer) skip this step
entirely — their Step 4 verdict is final, and `consensus_count` is `null`.

| Reviewer A | Reviewer B | Reviewer C | Final verdict             |
|------------|------------|------------|---------------------------|
| CONFIRM    | CONFIRM    | CONFIRM    | CONFIRM (unanimous)       |
| CONFIRM    | CONFIRM    | DOWNGRADE  | CONFIRM                   |
| CONFIRM    | CONFIRM    | DROP       | CONFIRM with caveat       |
| CONFIRM    | DOWNGRADE  | DOWNGRADE  | DOWNGRADE                 |
| any        | DROP       | DROP       | DROP                      |
| 1× CONFIRM<br>1× DOWNGRADE<br>1× DROP | — | — | DOWNGRADE (no consensus) |

**CONFIRM with caveat** keeps the finding at its severity but adds:

```json
"consensus_caveat": "1 reviewer voted DROP — see validation.rationales[]"
```

This surfaces the dissent in the Step 5 report so the asset owner
sees the disagreement explicitly.

### Per-finding metadata

For every finding in H, record under `validation:`:

```json
"validation": {
  "reviewer_a": { "verdict": "CONFIRM", "rationale": "..." },
  "reviewer_b": { "verdict": "CONFIRM", "rationale": "..." },
  "reviewer_c": { "verdict": "DOWNGRADE", "rationale": "..." },
  "consensus_count": 2,
  "final_verdict": "CONFIRM",
  "consensus_caveat": null
}
```

For findings in L:

```json
"validation": {
  "reviewer_solo": { "verdict": "CONFIRM", "rationale": "..." },
  "consensus_count": null,
  "final_verdict": "CONFIRM"
}
```

### Severity downgrades from non-consensus

When the consensus rule produces DOWNGRADE for a Critical or High
finding, also downgrade the severity by one level (Critical → High,
High → Medium). This makes the consensus disagreement visible in the
severity column without forcing the reader to inspect the
`validation:` block.

---

## Step 5 — Output Validated Report

Generate `reports/report_validated_<YYYYMMDD_HHMMSS>.json` + `.md`.

### JSON structure

```json
{
  "scan_type": "validated",
  "target": "<target>",
  "timestamp": "YYYYMMDD_HHMMSS",
  "source_report": "report_escalated_*.json",
  "validation_stats": {
    "total_reviewed": 0,
    "confirmed": 0,
    "downgraded": 0,
    "dropped": 0,
    "recovered": 0,
    "false_positive_rate": "N%"
  },
  "findings": [
    {
      "id": "VAL-001",
      "original_id": "ESC-001",
      "title": "...",
      "severity": "High",
      "original_severity": "Critical",
      "affected_url": "...",
      "evidence": "...",
      "verified": true,
      "evidence_type": "exploitation",
      "validation_status": "confirmed | downgraded | dropped | recovered",
      "validation_detail": {
        "evidence_alignment": "strong | weak | mismatch",
        "severity_check": "appropriate | inflated",
        "false_positive_argument": "...",
        "evidence_rebuttal": "...",
        "senior_pentester_verdict": "accept | investigate_more | reject",
        "downgrade_reason": null,
        "drop_reason": null
      },
      "cvss_score": 7.5,
      "cvss_vector": "CVSS:3.1/...",
      "business_impact": { "..." },
      "primitive_type": "read|write|auth|access",
      "reportable": true
    }
  ],
  "dropped_findings": [
    {
      "original_id": "ESC-003",
      "title": "...",
      "drop_reason": "...",
      "false_positive_argument": "..."
    }
  ]
}
```

### Markdown summary

Include:
- Validation summary table (confirmed / downgraded / dropped / recovered)
- For each confirmed finding: ID, title, severity, evidence alignment
- For each downgraded finding: what changed and why
- Dropped findings appendix with reasons
- Recovered findings with explanation

### Handoff

Print:
```
=== validate-scan complete ===
  Reviewed:    N findings
  Confirmed:   N (unchanged)
  Downgraded:  N (severity reduced)
  Dropped:     N (false positives removed)
  Recovered:   N (false negatives restored)
  FP rate:     N% of escalated findings were false positives
  Report:      reports/report_validated_<timestamp>.json

  Next step: run chain-scan --report reports/report_validated_<timestamp>.json
======
```

---

## Safety Rules (Non-negotiable)

- **Maximum 2 HTTP requests per finding** during re-probe (Step 3)
- **No new attack payloads** — only re-send the original POC URL or baseline
- **No requests outside target scope**
- **Isolation is mandatory** — do NOT read raw scan logs, recon output, or
  agent artifacts. Assess findings purely on their evidence fields.
- All re-probe output saved to `assets/validate_<finding_id>_<timestamp>.txt`
