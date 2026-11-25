---
name: backfill-gates
description: "Runs security review retroactively on work that shipped before the gate existed."
---

# /sulis:backfill-gates

Retroactive security gate for WPs that shipped before the Step 11
per-batch flow was wired up.

## When to invoke

Two situations:

1. **Post-rollout gap recovery** — a batch of WPs shipped via
   `wpx-train run` BEFORE `v0.20.0` (the Step 11 per-batch fix).
   Those WPs got no security review. You want to catch up
   retroactively. (This is the slice-1 + slice-2 case that
   prompted v0.20.x.)

2. **Periodic codebase-wide assessment** — even with Step 11 active,
   per-WP review can miss cross-WP issues (cumulative attack
   chains, supply-chain drift over time). A quarterly or
   release-candidate full sweep catches what per-WP review can't.

## What it does (the loop, in plain English)

Each iteration:

1. Invoke `/sulis:codebase-assess` — a whole-codebase scan
   across 25 primitives in 5 categories (Security, Data Protection,
   Code Quality, Supply Chain, Infrastructure).
2. Parse the resulting findings.
3. For each finding, check the findings register (signature-hash
   dedup): if it's NEW, register it + auto-draft a remediation
   work package; if it's a duplicate of something already known,
   skip it.
4. Stop here. Print a summary. The founder reviews the drafted
   WPs, promotes them from `auto-draft` to `pending`, fires
   `wpx-train run` to ship them.
5. Once the train ships, re-invoke `/sulis:backfill-gates`
   to start the next iteration — assesses again, finds fewer new
   findings, drafts fewer remediation WPs.
6. Loop terminates when an iteration finds zero NEW findings — the
   codebase is now clean from codebase-assess's perspective.

This is the "loop-until-clean" semantic the founder requested. The
loop is DISTRIBUTED across train cycles, not tight within one
session — because each finding's remediation needs to be SHIPPED
(via a train) before re-assessing makes sense.

## Inputs

| Argument | Required? | Description |
|---|---|---|
| `--project <slug>` | Yes | Project name (e.g., `agent-applications`). Used for `.security/{project}/` output. |
| `--repo <org/repo>` | Yes | Git repository (e.g., `sulis-ai/platform`). Used by codebase-assess for the clone. |
| `--deployed-url <url>` | No | Staging or production URL. If provided, codebase-assess includes DAST cycle. |
| `--max-remediation <N>` | No | Hard cap on remediation WPs drafted per iteration. Default `10`. Override when you know the codebase has many findings and you want a bigger batch. |

## How to invoke

```
/sulis:backfill-gates --project <slug> --repo <org/repo> [--deployed-url <url>] [--max-remediation 10]
```

The skill is a procedure document — the calling session executes
the steps below. You (the calling session) own the loop; the skill
walks you through one iteration.

## Procedure (one iteration)

### Step 1: Resolve tool paths

```bash
# v0.10.1+ — resolve the wpx-* tool paths up front
WPX_DIR=$(ls -td ~/.claude/plugins/cache/sulis-ai-agents/sulis/*/scripts/ | head -1)
test -d "$WPX_DIR" || { echo "FATAL: wpx-* tools not found"; exit 1; }
```

### Step 2: Run codebase-assess

Invoke the security assessor — this is a top-level skill call
that produces `.security/<project>/viability-report-<TIMESTAMP>.md`.

```
/sulis:codebase-assess <project> <repo> [<deployed-url>]
```

Capture the report path:

```bash
REPORT=$(ls -td .security/<project>/viability-report-*.md | head -1)
test -f "$REPORT" || { echo "FATAL: assess produced no report"; exit 1; }
```

### Step 3: Parse the report

The viability report has these relevant sections:

- `## Critical Findings` — CRITICAL severity items (must be addressed
  ASAP; auto-draft as `harden` primitive WPs)
- `## Attack Chains` — cross-primitive findings (also CRITICAL or
  CONCERN class)
- `## Category Detail` — per-category findings (Security, Data
  Protection, etc.) — these include CONCERN and ADVISORY severity

For each finding identified in those sections, extract:

- **Severity**: CRITICAL / CONCERN / ADVISORY
- **Summary**: one-line description
- **File / location**: where the issue lives (file path + line, OR
  primitive-level for codebase-wide issues like "no rate limiting on
  any auth endpoint")
- **Evidence**: the quoted text or tool output from the report
- **Suggested fix**: the recommendation paragraph
- **Primitive**: the SEC-NN identifier from the assessment, OR map
  to a Sulis change primitive: `Secure` / `Harden` / `Instrument` /
  `Gate`

### Step 4: Register + dedup + auto-draft (the main loop)

For each finding, in this iteration's batch:

```bash
REMEDIATION_COUNT=0
MAX_REMEDIATION=10  # from --max-remediation
DRAFTED=()
SKIPPED=()

for FINDING in <parsed findings list>; do
  if [ "$REMEDIATION_COUNT" -ge "$MAX_REMEDIATION" ]; then
    echo "Reached --max-remediation $MAX_REMEDIATION; stopping."
    break
  fi

  # 1. Register the finding (signature-hash dedup automatic)
  REGISTER=$("$WPX_DIR/wpx-findings" register \
    --project <project> \
    --wp <backfill-marker-or-source-WP> \
    --severity "$FINDING_SEVERITY" \
    --summary "$FINDING_SUMMARY" \
    --file "$FINDING_FILE" \
    --evidence-json @/tmp/finding-$N.json \
    --suggested-fix "$FINDING_SUGGESTED_FIX" \
    --primitive "$FINDING_PRIMITIVE")

  IS_DUPLICATE=$(jq -r '.data.is_duplicate' <<< "$REGISTER")
  SF_ID=$(jq -r '.data.sf_id' <<< "$REGISTER")

  if [ "$IS_DUPLICATE" = "true" ]; then
    # Already known; this iteration's loop won't draft a duplicate WP
    SKIPPED+=("$SF_ID")
    continue
  fi

  # 2. Auto-draft the remediation WP (new finding)
  AUTO_WP_ID=$(jq -r '.data.auto_wp_id' <<< "$REGISTER")

  "$WPX_DIR/wpx-findings" auto-draft-wp \
    --project <project> \
    --source-finding "$SF_ID" \
    --source-wp "backfill-$(date -u +%Y-%m-%dT%H%M%SZ)" \
    --auto-wp-id "$AUTO_WP_ID" \
    --primitive "$FINDING_CHANGE_PRIMITIVE" \
    --severity "$FINDING_SEVERITY"

  # 3. Register in INDEX (status: auto-draft; founder promotes)
  "$WPX_DIR/wpx-index" add-wp \
    --wp "$AUTO_WP_ID" --project <project> --from-wp-file

  DRAFTED+=("$AUTO_WP_ID")
  REMEDIATION_COUNT=$((REMEDIATION_COUNT + 1))
done
```

### Step 5: Write the iteration summary report

Write a summary at `.security/<project>/backfill-<TIMESTAMP>/SUMMARY.md`:

```markdown
# Backfill Iteration Summary

**Date**: <ISO timestamp>
**Project**: <project>
**Repo**: <repo>
**Source report**: <REPORT path from Step 2>
**Iteration cap**: <MAX_REMEDIATION>

## Outcome

- **Findings parsed**: <N>
- **NEW findings (drafted as remediation WPs)**: <K>
- **DUPLICATES (already in register)**: <D>
- **Critical findings (require founder review)**: <C>

## Drafted remediation WPs (this iteration)

- WP-AUTO-NNN — <one-line summary> (<SEVERITY>)
- ...

## Skipped duplicates (already addressed by prior backfill)

- SF-NNN — already in register
- ...

## Termination check

- [ ] If K == 0: **loop complete**. The codebase is clean from
      codebase-assess's perspective. No further iterations needed.
- [ ] If K > 0 AND K < MAX_REMEDIATION: **founder action needed**.
      Promote the K WP-AUTO-* drafts to `pending`; fire
      `wpx-train run`; re-invoke this skill after the train ships.
- [ ] If K == MAX_REMEDIATION: **cap reached**. The codebase has
      more findings than this iteration's cap. Promote + ship +
      re-invoke; the next iteration will see fewer findings (the
      shipped ones are no longer present); continue iterating.

## Next step

(One of the three above, in plain English for the founder.)
```

### Step 6: Emit the plain-English summary to the founder

```
Backfill iteration complete for project <project>.

Codebase-assess scanned <N> primitives over 25 checks.
- <C> CRITICAL findings (founder review needed; auto-drafted as
  Harden remediation WPs)
- <X> CONCERN findings (auto-drafted as Secure/Gate WPs)
- <Y> ADVISORY findings (auto-drafted as Instrument WPs)
- <D> findings were duplicates of previously-registered ones
  (signature-hash dedup; no new WPs created for these)

Total NEW remediation WPs drafted this iteration: <K>

To continue the loop:
  1. Review the drafted WPs in `.architecture/<project>/work-packages/`
     (they have status `auto-draft`)
  2. Promote ready ones to `pending`:
       wpx-index flip-status --wp WP-AUTO-NNN --to pending --expected auto-draft
  3. Fire the train to ship them:
       wpx-train run --project <project> --deploy-workflow <workflow>
  4. After the train completes (Step 11 reviews each remediation WP
     individually per v0.20.0), re-invoke this skill to start the
     next iteration:
       /sulis:backfill-gates --project <project> --repo <repo>

The loop terminates when an iteration produces ZERO new findings.

Summary report: .security/<project>/backfill-<TIMESTAMP>/SUMMARY.md
```

## Why this is a skill, not a wpx-* CLI tool

The orchestration involves multiple top-level skill invocations
(`/sulis:codebase-assess`, parsing free-form markdown,
agent judgement about how to map findings to change primitives).
That's the calling session's job — the skill IS the procedure.

The CLI tools (`wpx-findings`, `wpx-index`) handle the
state-changing operations (register, auto-draft, index-add). They
provide signature-hash dedup so iterations converge.

## Anti-patterns

- **Auto-promoting drafted WPs without founder review.** The skill
  writes WPs at status `auto-draft`. Founder promotion to `pending`
  is mandatory before train ships them. Backfill drafts can be
  noisy (the assess might flag patterns that don't apply); founder
  judgement filters.
- **Skipping the iteration boundary.** Don't run codebase-assess +
  promote + train + re-assess in one session loop. Each iteration's
  remediation needs to actually SHIP to main before the next assess
  can see the fix.
- **Ignoring CRITICAL findings.** CRITICAL must be addressed before
  any other work proceeds. If the founder defers a CRITICAL because
  "it's slice-3's problem", at minimum capture the deferral in
  `.security/<project>/deferred-critical-<SF-ID>.md` with the
  rationale + scheduled date.

## Related

- `plugins/sulis/skills/run-all/SKILL.md` — Step 11
  per-batch dispatch (forward gate; this skill is the retrofit)
- `plugins/sulis/skills/codebase-assess/SKILL.md` — the
  scan invocation this skill orchestrates
- `plugins/sulis/scripts/wpx-findings` — signature-hash
  dedup + auto-draft mechanics
- `plugins/sulis/skills/backfill-gates/recipes/post-rollout.md`
  — step-by-step recipe for the slice-2 12-WP case
- `plugins/sulis-execution/sdk/docs/recipes/backfill-security-review.md`
  — operator-facing recipe (same content, SDK-style)
