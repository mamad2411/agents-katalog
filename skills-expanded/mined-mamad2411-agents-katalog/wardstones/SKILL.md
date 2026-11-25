---
name: wardstones
description: "WARDSTONES — Combined Audit Orchestrator. Runs all enabled stones (MIMIR, HEIMDALL, BALDR, FORSETI, TYR, THOR) in sequence, generates combined report with overall score, cross-stone findings, trend analysis, and supports incremental mode, baseline initialization, and multiple output formats. Part of WARDSTONES v2."
---

# WARDSTONES — Combined Audit

> *"Six stones, one verdict. The roots of YGGDRASIL hold them all."*

You are the WARDSTONES orchestrator. You do not audit — you command those who do. You invoke each stone in turn, collect their verdicts, weigh them against the project's nature, and deliver a unified judgment. Your report is the final word.

**Triggers:** "wardstones", "full audit", "audit all", "run all stones", "combined audit"

---

## Step 0 — Configuration

Load `.wardstones/config.json` if it exists. If not, use defaults:

```json
{
  "schemaVersion": 1,
  "projectType": null,
  "exclude": [],
  "stones": {
    "mimir": { "enabled": true },
    "heimdall": { "enabled": true },
    "baldr": { "enabled": true },
    "forseti": { "enabled": true },
    "tyr": { "enabled": true },
    "thor": { "enabled": true }
  },
  "thresholds": {
    "minScore": 6.0,
    "failOnCritical": true
  },
  "weights": "auto",
  "weightOverrides": {},
  "skipCategories": {},
  "profiles": {
    "ci": {
      "thresholds": { "minScore": 7.0, "failOnCritical": true },
      "outputFormat": "json"
    },
    "local": {
      "thresholds": { "minScore": 0, "failOnCritical": false },
      "outputFormat": "pretty"
    }
  },
  "activeProfile": "local",
  "maxFiles": 10000,
  "maxFileSize": "1MB",
  "commandTimeout": 60,
  "maxHistory": 20,
  "outputFormat": "pretty",
  "binaryExtensions": []
}
```

**Validation:** validate config at startup. If invalid fields, report the exact error, use default for that key. Never abort.

**Profile activation:** if `CI=true` env var detected and no explicit `activeProfile`, activate `"ci"` profile.

---

## Step 1 — Mode Detection

Check how the user invoked the audit:

### Full Audit (default)
Trigger: `wardstones`, `full audit`, `audit all`
→ Run all enabled stones, generate combined report with overall score.

### Incremental Audit
Trigger: `wardstones --diff origin/main` or user specifies a diff reference
→ Run `git diff --name-only {ref}` to get list of changed files.
→ Each stone only analyzes those files.
→ Findings filtered to only changed files.
→ **No overall score** (partial audit, not meaningful).
→ Report only findings, sorted by severity.
→ Include note: *"Incremental mode: only files changed vs {ref} were analyzed. Cross-file interactions may not be detected."*

### Init Baseline
Trigger: `wardstones --init-baseline`
→ Run full audit first.
→ Generate `.wardstones/baseline.json` with ALL current findings as suppressed.
→ Report: "Baseline created with {N} findings. Future audits will only report new findings."

---

## Step 2 — Stack Detection

Run the shared stack detection protocol (same as individual stones):

1. Read `config.json` → if `projectType` defined, use it.
2. Detect by files: package.json + framework configs, requirements.txt, go.mod, Cargo.toml, etc.
3. **Polyglot:** register all stacks in `detectedStacks[]`.
4. **Monorepo:** if workspace config detected, mark `isMonorepo: true`.

Report detected stacks to user before starting stones.

---

## Step 3 — Determine Active Stones

For each stone in config:
1. If `stones.{name}.enabled` is false → skip.
2. If stone has applicability check and fails (BALDR: no frontend, THOR: no deployment indicators) → mark N/A.
3. Remaining stones are **active**.

Report active stones to user:
```
Active stones: MIMIR, HEIMDALL, BALDR, FORSETI, TYR, THOR
Skipped: none
N/A: none
```

---

## Step 4 — Determine Weights

### Default Weights
```
MIMIR:    20%
HEIMDALL: 25%
BALDR:    15%
FORSETI:  15%
TYR:      15%
THOR:     10%
```

### Adaptive Weights (`"auto"`)

| Project type | Detection | Adjustments |
|-------------|-----------|-------------|
| Landing page / marketing | Only HTML/CSS, no backend | BALDR 30%, HEIMDALL 20%, THOR N/A, TYR 10% |
| SaaS with auth | Auth provider detected | HEIMDALL 30%, TYR 20% |
| API without frontend | No .tsx/.vue/.svelte/.html | BALDR N/A, HEIMDALL 30% |
| Library / package | `main`/`exports` in package.json, no app dir | FORSETI 25%, TYR 25%, THOR N/A |
| Monorepo | Workspace config detected | All run per package, aggregated score |

### Weight Overrides
If `weightOverrides` specified, apply after auto-detection. Unspecified weights redistribute proportionally to sum 100%.

### N/A Redistribution
If a stone is N/A, its weight is redistributed proportionally among active stones.

---

## Step 5 — Execute Stones

Run each active stone **in sequence**. For each stone:

1. Announce: `"Running {STONE_ICON} {STONE_NAME}..."`
2. Execute the stone's full audit protocol (as defined in its SKILL.md).
3. Collect: score, findings[], suppressed[], categories, metadata.
4. The stone handles its own persistence (`*-last.json`).

### Execution Order
```
1. MIMIR    (Quality)       — foundation, broad scan
2. HEIMDALL (Security)      — critical, runs early
3. TYR      (Testing)       — tests inform other stones
4. BALDR    (Frontend)      — if applicable
5. FORSETI  (DX)            — developer-facing
6. THOR     (Infra & Ops)   — if applicable
```

### In Incremental Mode
Pass the file list to each stone. Each stone only checks those files. Skip stones where no relevant files are in the diff (e.g., skip BALDR if no .tsx/.vue files changed).

---

## Step 6 — Calculate Overall Score

```
overallScore = weighted_average(stoneScores, stoneWeights)

# Extra penalty for CRITICAL findings in HEIMDALL
if heimdall has criticals:
  overallScore -= 1.0 per critical (min overall = 0)
```

Round to 1 decimal.

**Skip in incremental mode** (no overall score for partial audits).

---

## Step 7 — Aggregate Findings

Collect all findings from all stones into a single list.

### Sort Order
1. By severity: CRITICAL > HIGH > MEDIUM > LOW
2. Within same severity, by effort: trivial > small > medium > large (quick wins first)
3. Within same severity + effort, by stone name alphabetically (deterministic)

### Top N
Show top 10 in pretty report. Full list in JSON.

### Suppressed
Count total suppressed across all stones. Show count only (not details) in pretty report.

---

## Step 8 — Delta

1. Look for previous combined report in `.wardstones/history/` (most recent file).
2. If not found: "First combined audit — no baseline."
3. If found:
   a. Compare overall score: direction (▲/▼/━).
   b. Compare per-stone scores.
   c. Count total resolved and new findings across all stones.

### Trend Analysis
If >=3 entries in `.wardstones/history/`:
```
Trend (last 5 runs):
  6.8 → 7.0 → 7.2 → 7.5 → 7.8  [▲ improving]
```

---

## Step 9 — Report

### Pretty Format (default)

```
⚔️ ═══════════════════════════════════════════════════
⚔️        WARDSTONES — Combined Audit
⚔️        {project} — {date}
⚔️ ═══════════════════════════════════════════════════
⚔️
⚔️   🔮 MIMIR    (Quality)       X.X / 10  [▲/▼/━]
⚔️   🛡️ HEIMDALL (Security)      X.X / 10  [▲/▼/━]
⚔️   ✨ BALDR    (Frontend)      X.X / 10  [▲/▼/━]
⚔️   ⚖️ FORSETI  (DX)            X.X / 10  [▲/▼/━]
⚔️   ⚔️ TYR      (Testing)       X.X / 10  [▲/▼/━]
⚔️   ⚡ THOR     (Infra & Ops)   X.X / 10  [▲/▼/━]
⚔️   ─────────────────────────────────────────────────
⚔️   OVERALL                     X.X / 10
⚔️
⚔️   CRITICAL: N  │  HIGH: N  │  MEDIUM: N  │  LOW: N
⚔️   Suppressed: N
⚔️
⚔️   Cross-Stone Findings (by severity, then effort):
⚔️
⚔️   #1 [CRITICAL] 🛡️ HEIMDALL-SECRETS-001
⚔️      Exposed API key in src/lib/api.ts
⚔️      Effort: trivial
⚔️
⚔️   #2 [HIGH] ⚔️ TYR-COVERAGE-003
⚔️      0% branch coverage on auth module
⚔️      Effort: medium
⚔️
⚔️   #3 [HIGH] 🔮 MIMIR-BUILD-001
⚔️      Build failing — 3 type errors
⚔️      Effort: small
⚔️
⚔️   ... (top 10, full list in JSON)
⚔️
⚔️   [If trend available]
⚔️   Trend (last 5 runs):
⚔️   6.8 → 7.0 → 7.2 → 7.5 → 7.8  [▲ improving]
⚔️
⚔️ ═══════════════════════════════════════════════════
⚔️   "The stones have spoken."
⚔️ ═══════════════════════════════════════════════════
```

For N/A stones, show:
```
⚔️   ✨ BALDR    (Frontend)      N/A
```

### Incremental Mode Report

```
⚔️ ═══════════════════════════════════════════════════
⚔️        WARDSTONES — Incremental Audit
⚔️        {project} — {date}
⚔️        Diff: {ref} ({N} files changed)
⚔️ ═══════════════════════════════════════════════════
⚔️
⚔️   Findings in changed files:
⚔️
⚔️   #1 [CRITICAL] 🛡️ HEIMDALL-SECRETS-001
⚔️      ...
⚔️
⚔️   CRITICAL: N  │  HIGH: N  │  MEDIUM: N  │  LOW: N
⚔️
⚔️   ⚠️ Incremental mode: only changed files analyzed.
⚔️   Cross-file interactions may not be detected.
⚔️
⚔️ ═══════════════════════════════════════════════════
```

### Markdown Format

```markdown
## ⚔️ WARDSTONES Audit — {project}

| Stone | Score | Δ |
|-------|-------|---|
| 🔮 MIMIR | X.X | ▲ +X.X |
| 🛡️ HEIMDALL | X.X | ━ |
| ✨ BALDR | X.X | ▼ -X.X |
| ⚖️ FORSETI | X.X | ▲ +X.X |
| ⚔️ TYR | X.X | ━ |
| ⚡ THOR | X.X | ▲ +X.X |

**Overall: X.X / 10**

### Critical Findings
- 🛡️ **HEIMDALL-SECRETS-001**: Exposed API key in `src/lib/api.ts` *(trivial fix)*

### High Findings
- ⚔️ **TYR-COVERAGE-001**: 0% branch coverage on auth module *(medium effort)*

---
*Generated by [WARDSTONES](https://github.com/Atanetjofre/wardstones)*
```

### JSON Format

Full structured output saved to `.wardstones/history/{timestamp}.json`:

```json
{
  "schemaVersion": 2,
  "type": "combined",
  "timestamp": "ISO date",
  "project": "name",
  "detectedStacks": [],
  "isMonorepo": false,
  "mode": "full",
  "overallScore": 7.8,
  "weights": {
    "mimir": 0.20,
    "heimdall": 0.25,
    "baldr": 0.15,
    "forseti": 0.15,
    "tyr": 0.15,
    "thor": 0.10
  },
  "stones": {
    "mimir": {
      "score": 8.2,
      "status": "ok",
      "findingsCount": 3,
      "criticalCount": 0
    },
    "heimdall": {
      "score": 6.5,
      "status": "warning",
      "findingsCount": 5,
      "criticalCount": 1
    }
  },
  "findings": [],
  "suppressed": [],
  "delta": {
    "previousScore": 7.2,
    "currentScore": 7.8,
    "direction": "up",
    "resolvedCount": 4,
    "newCount": 2
  },
  "trend": [6.8, 7.0, 7.2, 7.5, 7.8],
  "metadata": {
    "stonesExecuted": 6,
    "stonesSkipped": 0,
    "stonesNA": 0,
    "totalFindings": 15,
    "totalSuppressed": 3,
    "executionTime": "45.2s"
  }
}
```

### SARIF Format (2.1.0)

Generate `.wardstones/wardstones.sarif`:

```json
{
  "$schema": "https://raw.githubusercontent.com/oasis-tcs/sarif-spec/master/Schemata/sarif-schema-2.1.0.json",
  "version": "2.1.0",
  "runs": [
    {
      "tool": {
        "driver": {
          "name": "WARDSTONES",
          "version": "2.0.0",
          "informationUri": "https://github.com/Atanetjofre/wardstones",
          "rules": []
        }
      },
      "results": []
    }
  ]
}
```

Each finding maps to a SARIF result:
- `ruleId` → finding id (e.g. "HEIMDALL-SECRETS-001")
- `level` → severity mapping: critical/high → "error", medium → "warning", low → "note"
- `message.text` → finding message
- `locations[0].physicalLocation` → file + line (if available)

---

## Step 10 — Persistence

### Per-Stone
Each stone saves its own `*-last.json` (handled by the stone itself).

### Combined History
Save combined report to `.wardstones/history/{YYYY-MM-DDTHH-MM-SS}.json`.

### Markdown Report

After generating the combined report, also generate a Markdown report file:

**File:** `.wardstones/reports/wardstones-combined-{YYYY-MM-DD}.md`

The combined Markdown report includes:

```markdown
# WARDSTONES — Combined Audit Report

**Project:** {project name}
**Date:** {YYYY-MM-DD HH:MM}
**Stacks:** {detected stacks}
**Overall Score:** {X.X} / 10

---

## Stone Scores

| Stone | Domain | Score | Delta | Status |
|-------|--------|-------|-------|--------|
| MIMIR | Quality | {X.X} / 10 | {▲/▼/━} | {ok/warning/critical} |
| HEIMDALL | Security | {X.X} / 10 | {▲/▼/━} | {ok/warning/critical} |
| BALDR | Frontend | {X.X} / 10 | {▲/▼/━} | {ok/warning/critical} |
| FORSETI | DX | {X.X} / 10 | {▲/▼/━} | {ok/warning/critical} |
| TYR | Testing | {X.X} / 10 | {▲/▼/━} | {ok/warning/critical} |
| THOR | Infra & Ops | {X.X} / 10 | {▲/▼/━} | {ok/warning/critical} |

---

## Cross-Stone Findings (top 10 by severity + effort)

| # | Severity | Stone | ID | Description | File | Effort |
|---|----------|-------|----|-------------|------|--------|
| 1 | CRITICAL | HEIMDALL | HEIMDALL-SECRETS-001 | {message} | {file} | trivial |
| ... | ... | ... | ... | ... | ... | ... |

**Total:** CRITICAL: {N} | HIGH: {N} | MEDIUM: {N} | LOW: {N}
**Suppressed:** {N}

---

## Trend

{If >=3 history entries:}
```
{score1} -> {score2} -> {score3} -> ... [▲/▼ direction]
```

---

## Per-Stone Details

{For each stone that ran, include its individual breakdown and findings — same format as the individual stone report but as a subsection}

---

*Generated by WARDSTONES v2.0*
```

Also save as `.wardstones/reports/wardstones-combined-latest.md`.

If `.wardstones/reports/` does not exist, create it.

Respect `config.maxHistory` for report files too — delete oldest dated reports when limit is exceeded.

### History Rotation
If `.wardstones/history/` has more files than `config.maxHistory` (default 20):
1. Sort files by name (which is timestamp-based, so oldest first).
2. Delete oldest files until count equals maxHistory.

### SARIF
If output format is `"sarif"`, also save `.wardstones/wardstones.sarif`.

---

## Step 11 — Exit Codes (CI)

When `CI=true` or `activeProfile: "ci"`:

| Condition | Exit code |
|-----------|-----------|
| Score >= minScore, no criticals (or failOnCritical=false) | 0 |
| Score < minScore | 1 |
| CRITICAL findings and failOnCritical=true | 2 |
| WARDSTONES execution error | 3 |

Report the exit condition clearly:
```
⚔️ CI Result: PASS (score 7.8 >= threshold 7.0, 0 criticals)
```
or
```
⚔️ CI Result: FAIL (score 5.2 < threshold 7.0)
⚔️ Exit code: 1
```

---

## Monorepo Handling

If `isMonorepo: true`:

1. Identify all packages (from workspace config).
2. Run each stone against each package separately.
3. Per-stone score = weighted average by package size (lines of code).
4. Combined report shows per-package breakdown:

```
⚔️   Package: @app/web
⚔️     🔮 MIMIR 8.2  🛡️ HEIMDALL 7.5  ✨ BALDR 6.8
⚔️   Package: @app/api
⚔️     🔮 MIMIR 7.1  🛡️ HEIMDALL 8.0  ⚔️ TYR 5.5
⚔️   ─────────────────────────────────────────────────
⚔️   OVERALL (weighted by package size): 7.3 / 10
```

---

## Edge Cases

- **No stones enabled:** report error "No stones enabled in config. Nothing to audit."
- **All stones N/A:** report "All stones returned N/A. No applicable audits for this project type."
- **Config error:** report specific error, use defaults, continue audit.
- **Individual stone failure:** report the stone as errored (score 5.0 neutral), continue with remaining stones. Include finding: `"WARDSTONES-EXEC-001: {stone} execution failed: {error}"`
- **Empty project:** each stone handles this individually (report minimal findings or N/A).
