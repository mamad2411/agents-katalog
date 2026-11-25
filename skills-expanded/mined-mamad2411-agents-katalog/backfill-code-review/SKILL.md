---
name: backfill-code-review
description: "Runs code review retroactively on work that shipped without it."
---

# /sulis:backfill-code-review

Retroactive code-review for WPs that shipped before the Step 6.5
bundle-path verification landed (`v0.20.1`). Those WPs may have
self-attested ("inline review; 0 findings") without actually
invoking `/sulis:code-review` — no bundle file on disk; no audit
trail; no remediation WPs for findings that may have been missed.

## When to invoke

1. **Post-rollout gap recovery** — the slice-2 audit (2026-05-22)
   found 9 of 12 WPs had no `/code-review` bundle. Inline
   self-attestation. This skill catches them up.
2. **Periodic codebase-wide audit** — even with Step 6.5 enforced
   forward, sometimes WPs from outside the executor flow land
   (hotfixes, direct PRs). A periodic code-review backfill
   catches them.

## What it does (the loop, in plain English)

Each iteration:

1. Scan `.architecture/<project>/train-runs/*.yaml` for shipped
   WPs (entries with `merge_sha_on_dev` set).
2. Cross-reference against `.architecture/<project>/code-reviews/`
   — which WPs have NO `PR-feat-wp-NNN-*` bundle?
3. For each missing WP:
   - Read the squash-merge SHA from the train state YAML.
   - Compute the parent SHA: `git rev-parse <merge_sha>^`.
   - Invoke `/sulis:code-review <parent>..<merge_sha> <project>`.
4. For each finding in each newly-produced bundle:
   - `wpx-findings register` (signature-hash dedup).
   - If new: `wpx-findings auto-draft-wp` + `wpx-index add-wp`.
5. Stop at `--max-remediation` cap (default 10).
6. Print a summary. Founder reviews drafted WPs, promotes to
   `pending`, ships via `wpx-train run`. Re-invoke this skill
   to continue the loop.
7. Loop terminates when an iteration produces zero NEW findings.

The loop is **DISTRIBUTED** — each iteration's remediation WPs ship
via `wpx-train` before the next iteration can see the effect (the
fixes themselves change the codebase shape).

## Inputs

| Argument | Required? | Description |
|---|---|---|
| `--project <slug>` | Yes | Project name (e.g., `agent-applications`) |
| `--repo <org/repo>` | Yes | Git repository (e.g., `sulis-ai/platform`) for context |
| `--wps WP-A,WP-B,...` | No | Explicit list of WPs to backfill; bypasses the auto-scan. Use for ad-hoc backfill of a known WP set. |
| `--max-remediation <N>` | No | Hard cap on remediation WPs drafted per iteration. Default `10`. |
| `--since-sha <sha>` | No | Limit scan to WPs merged after `<sha>` on main. Default: all. |

## How to invoke

```
/sulis:backfill-code-review --project <slug> --repo <org/repo>
```

The skill is a procedure document — the calling session executes
the steps below.

## Procedure (one iteration)

### Step 1: Resolve tool paths

```bash
WPX_DIR=$(ls -td ~/.claude/plugins/cache/sulis-ai-agents/sulis/*/scripts/ | head -1)
test -d "$WPX_DIR" || { echo "FATAL: wpx-* tools not found"; exit 1; }
```

### Step 2: Identify WPs missing bundles

```bash
# All shipped WPs with merge SHAs (from train state YAMLs)
SHIPPED_WPS=$(
  for f in .architecture/<project>/train-runs/train-*.yaml; do
    # Extract bundle entries with merge_sha_on_dev set
    python3 -c "
import yaml, sys
state = yaml.safe_load(open('$f'))
for entry in state.get('bundle', []):
    if entry.get('merge_sha_on_dev'):
        print(f\"{entry['wp']}|{entry['merge_sha_on_dev']}|{entry.get('branch', '')}\")"
  done | sort -u
)

# WPs with existing code-review bundles
WITH_BUNDLES=$(
  ls -d .architecture/<project>/code-reviews/PR-feat-wp-*-*/ 2>/dev/null \
    | sed -E 's|.*/PR-(feat-wp-[^-]+-[^/]+)-[^/]+/$|\1|' \
    | sort -u
)

# WPs missing bundles = SHIPPED minus WITH_BUNDLES
echo "$SHIPPED_WPS" | while IFS='|' read -r wp merge_sha branch; do
  # Heuristic: match wp_id to branch suffix
  if ! echo "$WITH_BUNDLES" | grep -qi "${wp,,}"; then
    echo "MISSING: $wp ($branch @ ${merge_sha:0:8})"
  fi
done
```

If `--wps WP-A,WP-B,...` was passed, override the discovery and use
the explicit list instead.

### Step 3: Run /code-review per missing WP (with iteration cap)

```bash
REMEDIATION_COUNT=0
MAX_REMEDIATION=10  # from --max-remediation
DRAFTED=()
PROCESSED=()
SKIPPED_BY_CAP=()

for WP_ENTRY in <missing WPs from Step 2>; do
  WP_ID=$(echo "$WP_ENTRY" | cut -d'|' -f1)
  MERGE_SHA=$(echo "$WP_ENTRY" | cut -d'|' -f2)
  BRANCH=$(echo "$WP_ENTRY" | cut -d'|' -f3)

  # Skip if cap reached (we'll continue running /code-review but
  # not drafting more remediation WPs)
  if [ "$REMEDIATION_COUNT" -ge "$MAX_REMEDIATION" ]; then
    SKIPPED_BY_CAP+=("$WP_ID")
    continue
  fi

  # Compute parent SHA (the commit before the squash-merge)
  PARENT_SHA=$(git rev-parse "${MERGE_SHA}^" 2>/dev/null)
  if [ -z "$PARENT_SHA" ]; then
    echo "WARN: $WP_ID — can't resolve parent of $MERGE_SHA; skipping"
    continue
  fi

  # Invoke /sulis:code-review against the historical range
  # The skill resolves the commit range locally; no checkout needed.
  # Output lands at .architecture/<project>/code-reviews/PR-<rangeID>-<TS>/
  /code-review "${PARENT_SHA}..${MERGE_SHA}" <project>

  PROCESSED+=("$WP_ID")

  # Find the bundle that was just written (most recent)
  BUNDLE_DIR=$(ls -td .architecture/<project>/code-reviews/PR-*-*/ 2>/dev/null | head -1)
  if [ -z "$BUNDLE_DIR" ] || [ ! -f "$BUNDLE_DIR/signals.json" ]; then
    echo "WARN: $WP_ID — /code-review didn't produce signals.json; skipping"
    continue
  fi

  # Step 4 — register findings + auto-draft
  # (logic below)
done
```

### Step 4: Register findings + auto-draft remediation WPs

For each bundle produced in Step 3, parse `signals.json` for findings.
Findings in /sulis:code-review's PH-06 signal table have severity
(high / medium / low — roughly equivalent to CRITICAL / CONCERN /
ADVISORY).

For each finding:

```bash
# 1. Register the finding (signature-hash dedup automatic)
REGISTER=$("$WPX_DIR/wpx-findings" register \
  --project <project> \
  --wp "$WP_ID" \
  --severity "<finding_severity>" \
  --summary "<one-line>" \
  --file "<file_path>" \
  --evidence-json @/tmp/finding-N.json \
  --suggested-fix "<recommendation>" \
  --primitive "<CR-NN code>")

IS_DUPLICATE=$(jq -r '.data.is_duplicate' <<< "$REGISTER")
SF_ID=$(jq -r '.data.sf_id' <<< "$REGISTER")

if [ "$IS_DUPLICATE" = "true" ]; then
  SKIPPED+=("$SF_ID")
  continue
fi

# 2. Auto-draft (new finding)
AUTO_WP_ID=$(jq -r '.data.auto_wp_id' <<< "$REGISTER")

"$WPX_DIR/wpx-findings" auto-draft-wp \
  --project <project> \
  --source-finding "$SF_ID" \
  --source-wp "$WP_ID" \
  --auto-wp-id "$AUTO_WP_ID" \
  --primitive "Refactor" \
  --severity "<finding_severity>"

# 3. Register in INDEX (status: auto-draft)
"$WPX_DIR/wpx-index" add-wp \
  --wp "$AUTO_WP_ID" --project <project> --from-wp-file

DRAFTED+=("$AUTO_WP_ID")
REMEDIATION_COUNT=$((REMEDIATION_COUNT + 1))
```

Note: the `--primitive Refactor` mapping is a default for code-review
findings (CR-NN are quality / design / performance issues, mapped to
the Refactor change primitive). Adjust per finding if a different
primitive fits (e.g., CR-10 N+1 detection → `Harden`).

### Step 5: Write the iteration summary

Write to `.architecture/<project>/backfill-code-review-<TIMESTAMP>/SUMMARY.md`:

```markdown
# Backfill Code-Review Iteration Summary

**Date**: <ISO timestamp>
**Project**: <project>
**Repo**: <repo>
**Iteration cap**: <MAX_REMEDIATION>

## Outcome

- **WPs scanned (missing bundles)**: <N>
- **WPs processed (bundle created)**: <count of PROCESSED>
- **WPs skipped (cap reached)**: <count of SKIPPED_BY_CAP>
- **Findings parsed**: <total>
- **NEW findings (drafted as remediation WPs)**: <count of DRAFTED>
- **DUPLICATES (already in register)**: <count of SKIPPED>

## Bundles created this iteration

- WP-NNN — `.architecture/<project>/code-reviews/PR-<range>-<TS>/`
- ...

## Drafted remediation WPs

- WP-AUTO-NNN — <one-line> (<severity>; source: WP-NNN)
- ...

## Skipped by cap (process in next iteration)

- WP-XXX, WP-YYY, ...

## Termination check

- [ ] If DRAFTED is empty AND SKIPPED_BY_CAP is empty:
      **loop complete**. No new findings; no WPs queued for
      next iteration. The backfill is done.
- [ ] If DRAFTED is non-empty: **founder action needed**.
      Promote the drafted WPs to `pending`; fire `wpx-train run`;
      re-invoke this skill after the train ships.
- [ ] If SKIPPED_BY_CAP is non-empty: **continue in next iteration**.
      Even if no drafts this round, the next iteration processes
      the skipped WPs.

## Next step

(One of the three above, in plain English for the founder.)
```

### Step 6: Plain-English summary to the founder

```
Backfill code-review iteration complete for project <project>.

Scanned <N> WPs without bundles.
- <P> bundles produced this iteration
- <S> WPs skipped (cap reached at <MAX_REMEDIATION>)

Findings:
- <K_new> NEW (drafted as Refactor remediation WPs)
- <K_dup> DUPLICATES of previously-registered findings
- <K_critical> CRITICAL (require founder review; auto-drafted as
  Harden remediation WPs)

To continue the loop:
  1. Review the drafted WPs in `.architecture/<project>/work-packages/`
  2. Promote ready ones to `pending`:
       wpx-index flip-status --wp WP-AUTO-NNN --to pending --expected auto-draft
  3. Ship via train:
       wpx-train run --project <project> --deploy-workflow <workflow>
  4. After the train completes, re-invoke this skill to continue:
       /sulis:backfill-code-review --project <project> --repo <repo>

The loop terminates when an iteration produces ZERO new findings
AND zero SKIPPED_BY_CAP.

Summary report: .architecture/<project>/backfill-code-review-<TIMESTAMP>/SUMMARY.md
```

## Why this is a skill, not a wpx-* CLI tool

Same reasoning as `backfill-gates`: orchestration involves multiple
top-level skill invocations (`/sulis:code-review`), parsing free-form
markdown + JSON, agent judgement about how to map findings to change
primitives. That's the calling session's job; the CLI tools handle
the state-changing operations.

## Anti-patterns

- **Auto-promoting drafted WPs without founder review.** Drafts can
  be noisy — /code-review can flag CR-10 patterns that don't apply
  in context. Founder filters.
- **Skipping the iteration boundary.** Don't run /code-review →
  promote → ship → re-scan in one session. Each iteration's
  remediation needs to actually SHIP before the next /code-review
  sees the fix.
- **Treating CR-10 N+1 as low priority.** /code-review's CR-10
  performance checks catch real production issues. Prioritise
  these in promotion ordering.

## Related

- `plugins/sulis/skills/backfill-gates/SKILL.md` — sibling
  skill for security backfill (uses `/sulis:codebase-assess`)
- `plugins/sulis/skills/code-review/SKILL.md` — the skill this
  orchestrates
- `plugins/sulis/agents/executor.md` — Step 6.5 (the
  forward gate this skill complements)
- `plugins/sulis/skills/backfill-code-review/recipes/post-rollout.md`
  — step-by-step recipe for the slice-2 9-WP case
- `plugins/sulis-execution/sdk/docs/recipes/backfill-code-review.md`
  — operator-facing recipe
