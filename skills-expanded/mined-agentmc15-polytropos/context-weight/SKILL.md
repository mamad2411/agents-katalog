---
name: context-weight
description: Reach for this when your context is huge, you're near 700K, cache reads are high, or you're asking should I compact — it explains what this skill can and cannot do, ranks prevent/prune/measure in priority order, and gives the checkpoint move before you compact.
allowed-tools: Bash, Read
---

# Context weight

## What this skill cannot do

This skill cannot remove anything from your context window. Skills and agents are text loaded
INTO the window — read-only instructions the model follows — they have no mechanism to mutate the
message array a call submits. Only the harness can do that: `/compact`, auto-compaction, and, for
API callers, context editing (`clear_tool_uses_20250919`, `clear_thinking_20251015`). This skill's
job is to tell you *when* to act and *what* to act on; the harness is the thing that actually acts.
If you install this skill expecting your context to start shrinking on its own, nothing will
happen — that expectation is the single most likely misreading of this whole kit, and everything
below only works once it's corrected.

That limit applies to this kit's own tooling too: measuring context has mass.
`bin/context_weight.py` itself is tens of thousands of estimated tokens
(`wc -c bin/context_weight.py`, chars/4 — the number drifts as the engine grows). That doesn't
defeat the point, because of the **on-demand** vs **resident** distinction: the engine and its
tests are read only when you or a subagent runs them, costing nothing the rest of the time. Only
this SKILL.md's frontmatter `description` is **resident** — loaded on every call whether you use
it or not — which is why its wording (here and above) has to earn that keep with a trigger a
reader would actually type, not a feature summary.

## The three levers, in priority order

There are exactly three things you can do about context weight, and they are not
interchangeable — using them in the wrong order sends you to the lossy one first.

1. **PREVENT — free and lossless.** Delegate bulk reads to subagents that return conclusions
   instead of raw dumps, cap tool output before it enters the main window, defer loading a
   file/tool until it's actually needed, favor progressive disclosure over dumping everything
   up front. None of this mass ever enters the window, so there is nothing to lose later.
2. **PRUNE — cheap but lossy.** Compaction and, for API callers, context editing. This is the
   only lever of the three that can cost accuracy: it discards detail, and a summary is not the
   original. Use it, but pay it in full awareness of that cost (see the checkpoint move below).
3. **MEASURE — free.** Knowing when to act and what to act on — `session`, `overview`, `audit`,
   `watch`. Measurement doesn't change anything by itself; it's what tells you whether lever 1 or
   lever 2 is the right move right now.

**Why prevention wins:** a file never read costs nothing and loses nothing, but a file that's read
and later compacted costs three things — the read, the write (carried turn over turn until
compaction), and the fidelity (a compacted summary is lossy by construction). Prevention avoids
all three; pruning only ever stops the second, after the first is already paid.

**Why you can't just "pull the relevant context" once the window is full:** every API call
resubmits the whole message array — there's no selective re-read of a window already filled, no
way to retroactively un-submit what turned out not to matter. The retrieval-shaped answer exists
only *prospectively*, before the read happens: a subagent does the wide read off in its own
context and returns only the conclusion.

For a wide read whose question is *repo structure* rather than a specific file's contents,
reach for `/polytropos:graphify` first — a knowledge-graph query answers "what is this / who
calls it" in hundreds of bytes instead of the tens of thousands a raw exploratory read submits.

## How to run it

Use the `${CLAUDE_PLUGIN_ROOT}` env var Claude Code sets for plugin-executed content; if it is
unset, fall back to resolving `../../bin/context_weight.py` relative to this SKILL.md to an
absolute path:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/bin/context_weight.py" session      # this session's per-call weight, growth curve, ranked contributors
python3 "${CLAUDE_PLUGIN_ROOT}/bin/context_weight.py" overview     # cross-session working-set table, one section per harness
python3 "${CLAUDE_PLUGIN_ROOT}/bin/context_weight.py" audit        # resident-surface audit vs a token budget — tokens only, no dollars
python3 "${CLAUDE_PLUGIN_ROOT}/bin/context_weight.py" watch        # live: current % of window, and what's prunable vs load-bearing right now (Claude only)
python3 "${CLAUDE_PLUGIN_ROOT}/bin/context_weight.py" constraints --kit KIT  # is this kit's GUARDRAILS.md still resident right now (Claude only)
python3 "${CLAUDE_PLUGIN_ROOT}/bin/context_weight.py" demo         # synthetic smoke across all six cards — no real data touched
```

All six take `--json` for machine-readable output. `session`, `overview`, and `constraints` take
`--harness claude|codex|copilot` (default `claude`); each harness is reported at its own honest
fidelity, never at Claude's. `watch` has no `--harness` flag and is Claude-only by design (see the
Codex/Copilot note at the end of the checkpoint section below); passing `codex` or `copilot`
as its positional argument prints an honest refusal line and exits 0 rather than fabricating a
number those harnesses' logs can't support. `constraints --kit KIT` answers whether
that kit's `GUARDRAILS.md` is still resident in the reconstructed window — the check `execute`'s
phase-start fence re-read exists to force; on `codex`/`copilot` it prints their existing
fidelity-limit line instead.

Read `references/columns.md` when you must explain or defend a number in a `session` /
`overview` card — the weight / est. / measured / inferred / session-average glossary.

Read `references/practices.md` when the user asks "so what do I actually change" — the five
habits, each tied to the metric and the command that measures it.

## Checkpoint before compacting

PRUNE is the only lever that costs accuracy, so protect against that cost before you pull it:
**write decisions, constraints, and open questions to a file — `NOTES.md`, `tasks/todo.md` —
before compaction runs**, not after. A summary written after the fact can only summarize what
survived; a note written before it runs is an anchor the summary cannot lose, and the full detail
stays re-readable on demand even once the transcript it came from is folded away. This repo
already does exactly this at the kit level — every `.claude/kits/<slug>/NOTES.md` is "write it
down before the context that produced it goes away," applied to a session instead of a kit.

Not everything in the window is equally safe to lose, and `watch` reports the split rather than
leaving it to guesswork:

- **Safe to drop:** tool results already acted on and summarized, a superseded file read (read
  v1 → edited → read v2 — only v2 still matters), thinking from a completed step, verbose output
  whose conclusion is already recorded elsewhere.
- **Dangerous to drop:** the original task statement, decisions and their rationale, anything
  that would have to be re-derived from scratch if lost, unresolved error evidence, and early
  constraints that still bind late (e.g. "never push to main").

Auto-compaction is a timer, not a policy — it can't tell these two classes apart, which is why
the checkpoint file matters: it's how the dangerous-to-drop class survives a lossy step that
can't distinguish it from the safe-to-drop class on its own. Command:
`python3 bin/context_weight.py watch` — its `recommendation` line turns to
`checkpoint decisions to disk, then compact` once the current call passes ~60% of the window,
with the safe/dangerous breakdown printed alongside it, each item labeled `est.`.

**Codex and Copilot:** `watch` is Claude-only — Codex has no per-call provenance and Copilot has
no growth curve (D3), so neither can support a live threshold; `watch codex`/`watch copilot`
print an honest refusal instead. There is no substitute live check for those two harnesses —
use `session`/`overview` after the fact (their own honest
fidelity, per the table above) and apply the same levers and checkpoint habit manually, on a
schedule, instead of on a threshold.

## Honesty rules this tool holds, and this skill repeats

- Every estimated figure is labeled `est.`; it is a rank and a magnitude, never an exact token
  count, and it is never priced.
- Copilot never gets a growth curve — its logs carry no per-turn input/cache split, so `session`
  prints the verbatim line naming that instead of approximating one.
- Codex never gets content attribution — its usage containers carry token counts only, no
  content provenance, so `session` prints a labeled byte-share by record type and the verbatim
  line naming why, instead of a fabricated tool ranking.
- Dollar figures everywhere in this tool are API-equivalent estimates, not a bill — they price
  measured usage tokens (never estimated ones) through that harness's own pricing file, and each
  harness's dollars stay inside its own section. There is no cross-harness dollar total anywhere
  in this tool's output.
