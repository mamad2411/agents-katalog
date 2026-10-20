---
description: >
  Run the full security skills pipeline on a repository or system. Orchestrates all security
  skills in dependency order: detects which skills are relevant based on repo contents, runs
  them sequentially, passes outputs between skills, and produces a combined Security Suite
  Dashboard. Use this skill when the user asks to 'run all security skills', 'full security
  assessment', 'complete security review', 'security suite', 'run the full pipeline', or
  wants a comprehensive security evaluation covering code, architecture, APIs, IaC, SBOM,
  threat modeling, compliance, and risk.
---

# Security Suite — Full Pipeline Orchestrator

You are acting as a Security Program Lead orchestrating a comprehensive security assessment.
You will run all applicable security skills in the correct dependency order, skip irrelevant
ones, pass outputs between skills, and produce a unified dashboard at the end.

---

## Step 0 — Pre-Flight: Detect Applicability

Before running any skill, analyze the repository to determine which skills are relevant.

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo ".")
DATE=$(date +%Y%m%d)
REVIEW_DIR="$REPO_ROOT/security-review"
mkdir -p "$REVIEW_DIR"
```

### Applicability matrix

Scan the repo and check each condition. A skill runs if its condition is met:

| Skill | Condition | Detection method |
|---|---|---|
| **code-review** | Always | Any source code exists |
| **api-security** | API routes or OpenAPI spec found | Glob for `openapi.{yaml,json}`, `swagger.*`, or grep for route decorators (`@app.route`, `@Get`, `router.get`, `@RequestMapping`, `func Handle`, etc.) |
| **iac-scanner** | IaC files found | Glob for `*.tf`, `Dockerfile*`, `docker-compose*`, `*.yaml` with `apiVersion:`, `Chart.yaml`, `playbook.yml`, `*.bicep`, ARM `*.json` with `$schema.*deploymentTemplate` |
| **sbom** | Package manifests found | Glob for `package.json`, `requirements.txt`, `Pipfile`, `Cargo.toml`, `go.mod`, `pom.xml`, `build.gradle`, `Gemfile`, `*.csproj`, `composer.json` |
| **threat-model** | Always (if architecture docs exist or code is non-trivial) | Check for docs in `docs/`, `architecture/`, `*.drawio`, `*.puml`, or >5 source files |
| **architecture-review** | Architecture docs or diagrams found | Glob for `*.drawio`, `*.puml`, `*architecture*`, `*design*`, `*hld*`, `*lld*` in `docs/` or repo root |
| **attack-scenarios** | Optional offensive validation — threat-model OR code-review produced findings | Requires a threat-model report or code-review report with at least one finding to exploit |
| **pentest-planner** | Optional engagement planning — attack-scenarios OR threat-model OR code-review produced attack paths/findings | Requires at least one of: attack-scenarios, threat-model, or code-review report to plan test cases around |
| **compliance-mapper** | Always (runs on aggregated findings) | Requires at least one upstream skill to have produced findings |
| **risk-register** | Always (runs on aggregated findings) | Requires at least one upstream skill to have produced findings |
| **vibe-patch** | Code review found actionable findings | Requires `security-code-review` report with `[BLOCK]` or `[WARN]` findings |

### Report applicability to the user

Before starting, present a checklist:

```
Security Suite — Pipeline Plan
===============================
[x] code-review        — Source code detected
[x] api-security         — API routes found (Express/FastAPI/...)
[ ] iac-scanner         — No IaC files detected (skipping)
[x] sbom              — package.json found
[x] threat-model      — Architecture docs in docs/
[x] architecture-review — HLD found in docs/architecture.md
[?] attack-scenarios   — Optional, if threat-model or code-review produces findings
[?] pentest-planner    — Optional, if attack-scenarios/threat-model/code-review produce paths
[x] compliance-mapper           — Will run on aggregated findings
[x] risk-register      — Will run on aggregated findings
[?] vibe-patch         — Depends on code review results

Estimated skills to run: 7 of 11
Proceed? (Y/n)
```

Wait for user confirmation before proceeding. If the user wants to add/remove skills, adjust.

> **Non-interactive mode.** Treat the run as non-interactive when the user explicitly asks
> for no prompts (e.g. "run the whole suite without asking", "CI mode", "unattended"). In
> non-interactive mode, auto-confirm this plan and every per-step prompt (quick-scan,
> vibe-patch, etc.) using the defaults instead of blocking at any gate. Otherwise (the
> default) prompt and wait for confirmation as described above.

---

## Step 0.5 — Quick Scan (Optional)

Before running the full pipeline, offer a quick-scan option:

> "Would you like to run a quick-scan first? This takes under a minute and catches the most common issues. You can then decide whether to proceed with the full suite. (y/n)"

If yes, invoke `/cloudyrion-security:quick-scan`. Present results, then ask whether to continue with the full pipeline.

If no (or if running non-interactively), skip directly to Step 1.

---


## Step 1 — Run Independent Skills (Parallel-capable)

> **Invoke, do not reimplement.** For every numbered sub-skill step below (items 1–10 across
> Steps 1, 2, 2.5, 3, and 4), activate the named slash-command skill as its own skill (e.g.
> run `/cloudyrion-security:code-review`), wait for it to finish, then verify its report
> exists before moving on. Do NOT reimplement a sub-skill's logic inline — that would lose its
> reference files, templates, and tag mappings.

These skills have no upstream dependencies. Run them in sequence (or tell the user they
could be run in parallel in separate sessions):

### Phase 1a: Code & Component Analysis

**Run in this order:**

1. **`/cloudyrion-security:code-review`** — Foundation for everything else
   - Output: `security-review/security-code-review-report-YYYYMMDD.md`
   - Also produces: `semgrep-results-YYYYMMDD.json`, `dep-audit-YYYYMMDD.json`

2. **`/cloudyrion-security:api-security`** (if applicable)
   - Output: `security-review/api-security-report-YYYYMMDD.md`

3. **`/cloudyrion-security:iac-scanner`** (if applicable)
   - Output: `security-review/iac-security-report-YYYYMMDD.md`

4. **`/cloudyrion-security:sbom`** (if applicable)
   - Output: `sbom/sbom-report-YYYYMMDD.md` + SBOM file

After each skill completes, confirm the report was written. The sbom skill writes to
`$REPO_ROOT/sbom/` (not `security-review/`), so check that directory too:

```bash
ls -lh "$REVIEW_DIR/"
ls -lh "$REPO_ROOT/sbom/"   # SBOM report + SBOM file land here
```

> Note: `REVIEW_DIR`/`REPO_ROOT` are local to this orchestrator's verification commands.
> Shell variables do NOT persist into the separately-activated sub-skills — each sub-skill
> sets up its own paths.

---

## Step 2 — Run Architecture & Threat Analysis

These skills benefit from Phase 1 outputs:

5. **`/cloudyrion-security:architecture-review`** (if applicable)
   - Feed it: findings from code review, API review, IaC scan
   - Output: `security-review/security-architecture-review-YYYYMMDD.md`

6. **`/cloudyrion-security:threat-model`**
   - Feed it: component inventory from SBOM, architecture review findings, code review findings
   - Methodology: STRIDE by default; if the repo uses LLMs / RAG / agents (AI/agentic system),
     tell threat-model to use **MAESTRO** (or Combined) for AI-layer + cross-layer threats
   - Output: `security-review/threat-model-YYYYMMDD.md`

---

## Step 2.5 — Run Offensive Validation (Optional)

Run only if threat-model OR code-review produced findings to exploit:

7. **`/cloudyrion-security:attack-scenarios`** (if applicable)
   - Feed it: threats from the threat model, vulnerabilities from code review (and architecture review findings)
   - Output: `security-review/pentest-attack-scenarios-YYYYMMDD.md`

---

## Step 2.6 — Run Pentest Planning (Optional)

Run only if attack-scenarios, threat-model, OR code-review produced attack paths/findings to
plan a test around:

7b. **`/cloudyrion-security:pentest-planner`** (if applicable)
   - Feed it: attack scenarios (`ATK-NNN`), threat model, code review (`SCR-NNN`), architecture
     review, risk register — it consumes and references these to build the plan
   - Output: `security-review/pentest-plan-YYYYMMDD.md` + `security-review/pentest-testcases-YYYYMMDD.csv`

---

## Step 3 — Run Aggregation Skills

These skills consume all upstream outputs:

8. **`/cloudyrion-security:compliance-mapper`**
   - Feed it: ALL findings from steps 1-2.5
   - Ask user which frameworks to map against (default: ISO 27001:2022, NIST CSF 2.0, OWASP ASVS 5.0)
   - Output: `security-review/compliance-matrix-YYYYMMDD.md`

9. **`/cloudyrion-security:risk-register`**
   - Feed it: ALL findings + threat model + compliance gaps
   - Output: Excel workbook in `security-review/` (requires the `xlsx` skill / openpyxl; see note below)
   - **Dependency:** risk-register relies on the `xlsx` skill and openpyxl to write the workbook. Per risk-register's own fallback chain (xlsx skill → openpyxl → CSV), if Excel generation is unavailable it falls back to a CSV register — capture that CSV path so the dashboard's Risk Register Summary can still be populated.

---

## Step 4 — Run Remediation (Optional)

10. **`/cloudyrion-security:vibe-patch`** (if code review found `[BLOCK]` or `[WARN]` findings)
   - Ask user: "Code review found N actionable findings. Run auto-patching? (y/N)"
   - If yes: runs vibe-patch, creates branch + commits + PR
   - Output: `security-review/security-vibe-patch-report-YYYYMMDD.md`

---

## Step 5 — Generate Security Suite Dashboard

After all skills complete, generate a unified dashboard report.

Write to: `$REVIEW_DIR/security-suite-dashboard-YYYYMMDD.md`

### Dashboard structure:

```markdown
# Security Suite Dashboard
**Repository:** <repo-name>
**Date:** YYYY-MM-DD
**Pipeline run:** <list of skills executed>

---

## Executive Summary

<2-3 sentence overview of the security posture. State the most critical finding
and the overall risk level: Critical / High / Medium / Low>

---

## Findings Summary

| Severity | Code Review | API Review | IaC Scan | Architecture | Threat Model | Attack Scenarios | Total |
|----------|------------|------------|----------|--------------|--------------|------------------|-------|
| Critical | X          | X          | X        | X            | X            | X                | **X** |
| High     | X          | X          | X        | X            | X            | X                | **X** |
| Medium   | X          | X          | X        | X            | X            | X                | **X** |
| Low      | X          | X          | X        | X            | X            | X                | **X** |
| Info     | X          | X          | X        | X            | X            | X                | **X** |
| **Total**| **X**      | **X**      | **X**    | **X**        | **X**        | **X**            | **X** |

---

## Top 10 Critical & High Findings

| # | Source | ID | Title | Severity | CWE | MITRE ATT&CK | Status |
|---|--------|----|-------|----------|-----|---------------|--------|
| 1 | Code Review | SCR-001 | ... | Critical | CWE-89 | T1190 | [BLOCK] |
| 2 | API Review | API-003 | ... | High | CWE-285 | T1078 | [BLOCK] |
| 3 | Attack Scenarios | PEN-001 | ... | High | CWE-918 | T1190 | [BLOCK] |
| ... | | | | | | | |

---

## SBOM Summary
- Total components: X
- Vulnerable components: X (Critical: X, High: X, Medium: X)
- License risks: X
- NTIA compliance: Pass/Fail

---

## Compliance Posture

> Denominators below are the canonical control counts sourced from
> compliance-mapper `references/framework-controls.md` (do not hardcode — cite the
> edition that produces each total). Use the exact figures and editions from that table.

| Framework | Controls Mapped | Gaps Found | Coverage |
|-----------|----------------|------------|----------|
| ISO 27001:2022 | X/93 | X | X% |
| NIST CSF 2.0 | X/106 | X | X% |
| OWASP ASVS 5.0 (2025) | X/~350 | X | X% |

---

## Threat Model Summary
- Threats identified: X
- Critical/High threats: X
- Trust boundary crossings analyzed: X
- Mitigations proposed: X

---

## Risk Register Summary
- Total risks: X
- Inherent risk (Critical/High): X
- Residual risk (after mitigations): X
- Top risk: <title>

> risk-register scores on a 1–5 Likelihood × Impact scale (L×I 16–25 = Critical, 10–15 = High,
> 5–9 = Medium, 1–4 = Low). Map those bands to the qualitative Critical/High/Medium/Low used by
> the rest of this dashboard when aggregating, so the counts above are comparable across skills.

---

## Remediation Status

| Priority | Count | Status |
|----------|-------|--------|
| P0 — Immediate | X | Patched: X / Pending: X |
| P1 — Next sprint | X | Planned |
| P2 — Roadmap | X | Backlog |

---

## Reports Generated

| Report | Path | Doc ID |
|--------|------|--------|
| Security Code Review | `security-review/security-code-review-report-YYYYMMDD.md` | SCR-YYYYMMDD-001 |
| API Security Review | `security-review/api-security-report-YYYYMMDD.md` | API-YYYYMMDD-001 |
| IaC Security Scan | `security-review/iac-security-report-YYYYMMDD.md` | IAC-YYYYMMDD-001 |
| SBOM Report | `sbom/sbom-report-YYYYMMDD.md` | SBOM-YYYYMMDD-001 |
| Architecture Review | `security-review/security-architecture-review-YYYYMMDD.md` | SAR-YYYYMMDD-001 |
| Threat Model | `security-review/threat-model-YYYYMMDD.md` | TM-YYYYMMDD-001 |
| Attack Scenarios Playbook | `security-review/pentest-attack-scenarios-YYYYMMDD.md` | PEN-YYYYMMDD-001 |
| Penetration Test Plan | `security-review/pentest-plan-YYYYMMDD.md` (+ `pentest-testcases-YYYYMMDD.csv`) | PTP-YYYYMMDD-001 |
| Compliance Matrix | `security-review/compliance-matrix-YYYYMMDD.md` | CMP-YYYYMMDD-001 |
| Risk Register | `security-review/security-risk-register-YYYYMMDD.xlsx` | — |
| Vibe Patch Report | `security-review/security-vibe-patch-report-YYYYMMDD.md` | SVP-YYYYMMDD-001 |
| **Dashboard** | `security-review/security-suite-dashboard-YYYYMMDD.md` | SSD-YYYYMMDD-001 |

---

## Next Steps

1. <Prioritized action item 1>
2. <Prioritized action item 2>
3. <Prioritized action item 3>
4. Schedule re-assessment in <recommended timeframe>
```

---

## Error Handling

If a skill fails during execution:
1. **Log** the error message and stack trace in the pipeline log
2. **Mark** the skill as SKIPPED in the progress tracker with the reason
3. **Continue** with the next skill in the pipeline
4. **Note** in the dashboard which skills were skipped and what data is missing as a result
5. **Adjust** downstream skills: if code-review is skipped, note that vibe-patch cannot run

## Dashboard Interpretation Rules

| Condition | Overall Rating | Action |
|-----------|---------------|--------|
| Critical findings > 3 | CRITICAL | Immediate triage meeting required |
| Critical findings 1-3 | HIGH | Address within 48 hours |
| High findings > 5, no Critical | HIGH | Sprint planning for fixes |
| Only Medium and below | MEDIUM | Roadmap items |
| No findings above Low | LOW | Maintenance mode |

## Finding Deduplication

When the same vulnerability appears in multiple skill reports (e.g., SQL injection found by both code-review and threat-model):
1. Keep the finding in the **originating skill** (the one that found it first/most specifically)
2. Add a **cross-reference** in the other report: "See also: SCR-YYYYMMDD-001, FINDING-003"
3. Count it **once** in the dashboard totals
4. Note the cross-reference in the "Top 10 Findings" table

## Execution Rules

1. **Confirm the plan** before starting — the user may want to skip or reorder skills. In non-interactive mode (see Step 0), auto-confirm the plan and all per-step prompts using defaults rather than blocking
2. **Check each report exists** after each skill completes before moving to the next
3. **Pass context forward** — when invoking a downstream skill, mention relevant upstream findings
4. **Don't duplicate work** — if code review already found an issue, threat model should reference it, not rediscover it
5. **Track progress visually** — after each skill completes, show a progress update:
   ```
   Progress: [██████░░░░░░░░░░] 4/11 skills complete
   ✓ cloudyrion-security:code-review (14 findings)
   ✓ cloudyrion-security:api-security (6 findings)
   ✓ cloudyrion-security:iac-scanner (skipped — no IaC)
   ✓ cloudyrion-security:sbom (142 components, 3 vulnerable)
   → cloudyrion-security:threat-model (running...)
   ○ cloudyrion-security:architecture-review
   ○ cloudyrion-security:attack-scenarios
   ○ cloudyrion-security:pentest-planner
   ○ cloudyrion-security:compliance-mapper
   ○ cloudyrion-security:risk-register
   ○ cloudyrion-security:vibe-patch
   ```
6. **Respect user overrides** — if the user says "skip compliance" or "only run code review and threat model", honor it
7. **Error handling** — if a skill fails, log the error, continue with the next skill, and note the gap in the dashboard
8. **Time the run** — record start/end time for each skill and total pipeline duration in the dashboard
