---
name: agent-sleep
description: >-
  Sleep-cycle memory management for coding agents. Use when consolidating a
  finished session into memory, running daily memory hygiene or drift checks,
  prestudying a repo before the next session, reconciling accumulated memory,
  rebuilding memory from source, or installing the wake/sleep triggers on a
  new machine or platform. Modes are offline by design — never run
  consolidation inline during an interactive session.
---

# agent-sleep

A memory architecture for coding agents, built around one split: sessions
work, offline phases remember. The agent that does the task should not be the
agent doing memory bookkeeping in the same breath.

Six modes, each with a trigger:

| Mode | Trigger | What runs |
| --- | --- | --- |
| consolidate | session end (off-peak) | extract → verify vs raw source → promote |
| check | daily, scripts only | TTL expiry, pointer re-validation, founding tests |
| reconcile | N new memories, or a contradiction flag | dedupe, prune, scoped rewrites |
| prestudy | idle (off-peak) | re-derive repo state into warm-start memory |
| rebuild | re-grounding costs more than maintaining | regenerate memory from source |
| rollback | drift alarm, or any bad write | restore last-known-good from git |

## The invariants

These exist because specific, measured failure modes were documented
(see README for the evidence). Breaking one is a bug even if nothing
visibly breaks today.

1. **Never summarize a summary.** Extraction reads the raw transcript and the
   repo. Existing memory is never an input to consolidation.
2. **Never write the charter.** `AGENTS.md` (or platform equivalent) and skill
   cores are re-loaded fresh each session and live outside every write path
   this skill offers. If a mode seems to need charter edits, stop and report.
3. **Admit less.** A candidate memory enters only if it passed verification
   against a source and carries a scope. When in doubt, drop it.
4. **Every write is a git commit.** One writer at a time, one commit per
   promotion, via `scripts/snapshot.sh`. No exceptions, no batch rewrites
   outside reconcile.
5. **Check daily, rewrite on trigger.** Mechanical checks are cheap and
   frequent; semantic rewrites are rare and batched. Each rewrite is a
   compression event — spend them.

## Memory file format

Every memory is one file with frontmatter (see `templates/memory-file.md`):

```yaml
name: short-kebab-slug
description: one line, used for recall decisions
metadata:
  type: user | feedback | project | reference
  scope: when this applies — and when it does not
  source: /path/or/URL/or session:<id>
  verify: optional command that must exit 0
  ttl_days: 30
  last_validated: 2026-10-28
```

An index file (`MEMORY.md`) lists one line per memory and nothing else.
The index routes recall; the files carry the facts.

## Running the modes

Scripts are plain bash; the only dependencies are git, curl, and a POSIX
shell. Model-driven steps use the prompt templates in `templates/prompts/`
with the strongest model available — consolidation quality is the whole game.

    scripts/snapshot.sh <memory-dir> [message]     # commit memory state
    scripts/rollback.sh <memory-dir> [N]           # restore N commits back
    scripts/verify-memory.sh <memory-dir>          # re-validate every entry
    scripts/prune-ttl.sh <memory-dir> [--apply]    # list/move expired entries
    scripts/run-fixtures.sh <fixtures-dir>         # founding tests, exit 1 on drift
    scripts/install-triggers.sh                    # platform wiring

Platform-specific trigger wiring (hooks, idle queues, cron) lives in
`adapters/` — one file per platform, starting with ZCode, Claude Code,
OpenCode, and a generic cron adapter that covers the rest.

## What this is not

It is not parametric learning. Everything lives in token space — files a
harness reads. That ceiling is real (weight-space consolidation outperforms
it in the literature), and the payoff is that memory survives every model
swap underneath.
