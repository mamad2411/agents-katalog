---
name: context-hygiene
description: Use when context is growing large or the agent forgets earlier instructions, when deciding clear vs compact, when processing documents/logs >50k tokens, when monitoring token cost or limiting subagent fan-out, when choosing a reasoning effort level, or when reducing token/compute/MCP costs. Covers lost-in-the-middle, context folding (RLM), cost guards, and difficulty-matched effort.
triggers: [user, model]
---

# Context Hygiene

Context window = input + output tokens the model sees at once. Every system
prompt, rules file, MCP tool definition, message, and tool result counts
against a hard provider-set limit. Output quality degrades past ~100k active
tokens ("dumb zone") regardless of total window — lost-in-the-middle means
middle detail has weak impact (arXiv:2307.03172). Bigger window ≠ better
retrieval.

**Default stance:** with SWE-2 (262K) most sessions fit — use context
directly. Apply the techniques below only when actually needed.

## Clear vs Compact

| Action | What it does | When |
|---|---|---|
| `clear` | Wipes history | **Default.** Task done or unrelated to prior chat. |
| `compact` | Summarizes history | Same task continues; losing thread would hurt. Lossy — preserves intent, not facts. |

Compaction leaves "sediment" — treat it as escape hatch, not hygiene default.
If dense access to early detail is needed, fold (below) instead.

## Prune vs Fold vs Compact vs Summarize

| Action | Mechanism | When |
|---|---|---|
| Prune | Per-item keep/truncate/drop via `extensions/laya-compactor` (laya `compact-item-v1`, suggestion/abstain only) | Tool noise fills the window; facts must survive verbatim. |
| Fold | Offload artifacts to files; peek/grep/sub-query | Dense access to early detail needed; >50k-token artifacts. |
| Compact | `compact` summary | Escape hatch when pruning cannot reach target size. |
| Summarize | Manual tl;dr | Almost never inside a session; for handoffs write a doc instead. |

Pruning decision policy lives here: pin system + first message + last user
task + newest `preserve_recent` messages; abstain means keep (fail-safe);
drop applies pair-wise so no `tool_result` is orphaned; survivors stay
byte-identical. Escalate to `compact` summary only when pruning cannot
reach `compact_to`.

**Smart Window params** (adaptive effective window, not fixed recency):

| Param | Value | Basis |
|---|---|---|
| `compact_at` | 0.70 x window (SWE-2 262k -> ~183k) | headroom for next tool batch |
| `compact_to` | 0.40 x window (~105k) | hysteresis, avoids thrash |
| `preserve_recent` | 6 messages + first message | upstream port default |
| `keep_threshold` | 0.5, calibrate on real transcripts | laya confidence is entropy-based |
| `truncate_head` | 300 chars | upstream port default |
| `max_state` | ~25k est. tokens | fits laya context |
| `reduction_floor` | <0.25 -> abort, keep original | avoids pointless churn |

`assist` mode requires `activation_errors` empty plus a calibrated
threshold; run shadow first, measure, then promote.

## Lean Context Rules

1. Clear chats between unrelated tasks.
2. Keep rules files small — they load into *every* conversation. Modularize
   into skills; see `writing-skills`.
3. Be paranoid about MCP servers — each injects every tool definition into
   the system prompt. Audit with `mcp-governance` before adding; keep <10-15
   tools/server.
4. Don't paste huge documents — write to file, then `read` offset/limit or
   `grep`.
5. Prefer subagents for parallel exploration — each has its own window; only
   synthesis returns (50-100x savings).
6. Watch the budget — `context-budget.py` (SessionStart hook).
7. Guard against overflow — unbounded loops are a cost and correctness risk.

## Context Folding (RLM-style, for >50k-token artifacts)

Adapted from Recursive Language Models (arXiv:2512.24601): treat context as a
variable in an environment — peek, grep, partition, sub-query — instead of
reading it all.

Workflow: **offload** to file → **peek** (read offset/limit) → **grep** to
locate → **partition** (`split -l 500`) → **sub-query** chunks with
`researcher` subagents → **verify returns** (Rule 12 spot-checks) →
**synthesize**.

**Depth rule (critical):** depth=1 only. Subagents must NOT spawn subagents —
depth=2 causes overthinking, 95x slower (arXiv:2603.02615).

Don't fold preemptively, don't dump whole files into context, don't use for
simple retrieval (grep is cheaper).

## Cost Guard

| Limit | Action |
|---|---|
| 1-3 subagents | Default max; >3 requires explicit user approval (enforced by `validate-tool-args.py`). |
| Loops/retries | Bound every loop; each iteration multiplies cost. |
| Token maxing | Detect effort disproportionate to task difficulty. |

## Cost Optimization Protocol

1. Measure current cost (tokens/request, model tier, cache hit rate).
2. Audit context usage (`mcp-governance` for MCP tool-definition cost).
3. Right-size effort (see below); paid models only when explicitly approved.
4. Add caching; shorten prompts; prefer file snippets over full reads.
5. Re-measure; report tokens/cost before and after with commands used.

## Code-formatting minification — scoped caution

Stripping non-semantic whitespace cuts **input** tokens ~24.5% (arXiv:2508.13666,
ICSE'26 — Java 33.7% avg; tool: Deblank). Verified but **narrow**: measured on
FIM completion only. Do NOT minify code in agentic/editing flows —

- SWE-bench agents: input −42% but resolution 50%→38% (arXiv:2606.01326).
- Whitespace-preserving rewrites flip predictions up to 60% (TokDrift,
  arXiv:2510.14972).
- Python: indentation is syntax → ~6.5% gain; minified files break
  edit-matching, linters, and review.
- Output stays formatted regardless (−2.9%); "emit unformatted" prompting
  broke Gemini 67%→11% and is model-fragile.

Valid as a per-project rule only when ALL hold: model reads but never edits
the code (analysis/completion/RAG input); brace-delimited language (not
Python/YAML); a formatter restores output (Deblank pattern — prettier/CI
round-trip, disk unchanged); payload is one-shot, not an editing session.

## Effort Calibration

Effort is scarce — match to task difficulty. Maps to `data/bundle-models.json`:

| Level | model_uid | When |
|---|---|---|
| Medium | `swe-2-medium` | Simple tasks, spot fixes, isolated scripts, mechanical refactors. Single test/build verifies. |
| High | `swe-2-high` | Multi-file tasks with clear dependencies. **Default.** |
| Max | `swe-2-max` | Open-ended, long-horizon, architecture, novel debugging, or failure at lower effort. |

Rules:
1. **Improve the spec before raising effort** — information quality
   substitutes for reasoning budget (arXiv:2608.01347).
2. **Start minimal, expand on failure** (E3: Estimate, Execute, Expand —
   arXiv:2607.13034; 85% cost cut at equal success on simple edits).
3. **Never start at Max** for a task untried at Medium. But don't starve hard
   tasks — higher effort lifted first-try success 28%→89% on a hard build
   (arXiv:2607.02436).
4. **Prompt wording allocates work** — "multiple approaches" multiplies
   reasoning 2.4-7.4× with no success gain; "max certainty" creates
   verification loops 18× median cost. State WHAT + acceptance criteria.
