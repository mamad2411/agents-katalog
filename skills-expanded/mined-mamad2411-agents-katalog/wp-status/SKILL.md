---
name: wp-status
description: "Shows what's done, in-flight, blocked, and pending for a change."
---

# /sulis:status

Read-only view of the Work Package INDEX state. **This skill runs
inline in the invoking session — it does NOT spawn the executor or
orchestrator.** No `Agent()` call required; the skill itself reads
the INDEX and renders.

## Usage

```
/sulis:status
```

No arguments. Reads `.architecture/{project}/work-packages/INDEX.md`
and produces a plain-English summary.

## How to render

Parse the INDEX file (Markdown table). For each WP, classify by
status. Render as:

```
Work Package status:

✓ Done: N
  WP-NNN, WP-MMM, ...

⏳ In flight: N
  WP-NNN — <title> (<lifecycle step or branch reference>)

▣ Queued for train: N        ← v0.11.0+ (step-7-complete status)
  WP-NNN — <title>

⚠ Blocked: N
  WP-NNN — <plain-English summary from BLOCKER-WP-NNN.md
            ## Plain-English summary section>

▢ Pending: N
  WP-NNN, WP-MMM, ...

▶ Next ready: WP-NNN — <title>

Train state:                   ← v0.11.0+
  N eligible WPs ready. Trigger: <ready_size|waiting|not_ready>.
  Last train run: <path or "none yet">.
```

For the **Queued for train** + **Train state** sections, invoke the
MCP tool `mcp__sulis-execution-mcp__train_status` with `project: <slug>`
and `repo: <org/repo>`. The result is a typed `TrainStatusResult` —
read `eligible_count`, `eligible_wps`, and `trigger_state` directly.

> **Fallback (no MCP):** if the sulis-execution-mcp server isn't
> available in this session (e.g. the plugin isn't installed; running
> against a bare checkout), fall back to
> `"$WPX_DIR/wpx-train" status --project <slug> --repo <org/repo>` and
> parse the JSON. Same result shape; just unwrap from the
> `{"ok": true, "data": {...}}` envelope.

### Change context (CW-04, v0.12.0+)

When run from inside a change worktree, prepend a "Change" section
to the status output. Detect via `git branch --show-current`; if it
starts with `change/`, invoke the MCP tool
`mcp__sulis-execution-mcp__change_status` with `slug: <slug>` and
`primitive: <primitive>`.

> **Fallback (no MCP):** `"$WPX_DIR/sulis-change" status --slug <slug>
> --primitive <primitive>` produces the same shape.

Then render:

```
Change: change/{primitive}-{slug}
  Started: <ISO timestamp>
  Branch SHA: <sha> (ahead of base by N, behind by M)
  Worktree: <path>
```

Then continue with the Work Package status table — those are the WPs
inside this change. (Or if not in a change worktree, just show the WP
status directly — the original behaviour.)

The plain-English summaries for blocked WPs come from each
`BLOCKER-WP-NNN.md`'s `## Plain-English summary` section — that's
the AAF-compliant text the concierge would surface to the founder.

## What it shows

```
Work Package status:

✓ Done: 7
  WP-001, WP-002, WP-003, WP-004, WP-005, WP-006, WP-007

⏳ In flight: 1
  WP-008 — cancel-subscription flow (branch pushed; CI green; awaiting merge)

⚠ Blocked: 1
  WP-009 — staging cluster at capacity (BLOCKER-WP-009.md)

▢ Pending: 4
  WP-010, WP-011, WP-012, WP-013

▶ Next ready: WP-010 — webhook idempotency keys
```

For each blocked WP, shows the plain-English summary from the
BLOCKER record's `## Plain-English summary` section so the founder
or concierge can read the status without opening files.

## What it doesn't do

- It doesn't dispatch executors. Use `/sulis:run-wp` or
  `/sulis:run-all` for execution.
- It doesn't modify INDEX or any other file. Pure read.
- It doesn't follow dependsOn — it just shows declared status.

## When to use

- After a `run-all` session, to see where things landed.
- Before a `run-all` session, to confirm the starting state.
- When debugging — the INDEX is the source of truth, but `status`
  is the readable view.
- To resume after a break — see what's blocked and what's next
  ready.

## See also

- `agents/orchestrator.md` (ships v0.4) — uses similar logic
  internally to pick the next ready WP.
- The INDEX file itself at `.architecture/{project}/work-packages/INDEX.md`.
