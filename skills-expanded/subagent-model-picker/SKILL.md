---
name: subagent-model-picker
description: "Pick the model for each Claude Code subagent before you spawn it. Given a list of tasks to delegate, assign every task Haiku, Sonnet, Opus or Fable with a one-line cost and quality reason, then pass that model to the Agent tool or write it into the subagent's `model:` frontmatter. Use when a lead agent is about to fan work out to subagents, when someone asks which model their subagents should use, or when a multi-agent run costs too much. Not for deciding whether to delegate, and not for picking the lead's own model."
license: Apache-2.0
metadata:
  version: "0.2.0"
---

# Subagent Model Picker

One job: before any subagent is spawned, give it the cheapest model that will still get its task right the first time, and say why in one line.

Claude Code lets every subagent run on its own model: the Agent tool takes a `model` value (`haiku`, `sonnet`, `opus`, `fable`), and a subagent file in `.claude/agents/` takes `model:` in its frontmatter. Without a choice, every subagent inherits the lead's model, which usually means paying top-tier prices for file inventories and format conversions.

## Step 1. Read each task, answer three questions

For every task you are about to delegate:

1. **Is "done" checkable from the task alone?** A test, an exact expected output, a list to match. Yes means a cheaper model is safe, because a miss is caught.
2. **Does the next step depend on judgment about intermediate results?** Mechanical work (search, list, convert, run and report) needs none. Debugging, design and trade-offs need it.
3. **What does a wrong answer cost?** Cheap to redo, or does it silently ship a bug?

## Step 2. Map to a tier

| Tier | Signals | Model | Typical tasks |
| --- | --- | --- | --- |
| Mechanical | Output checkable, no judgment, cheap to redo | `haiku` | Inventory files or symbols, grep and list, convert a config format, run a command and report its output, rename across files |
| Bounded build | Clear spec or failing test, some interpretation, one area of code | `sonnet` | Fix a bug that has a reproducing test, implement a function against a stated contract, write tests for existing code, summarise with citations |
| Hard build | Edge cases not spelled out, several files, numeric or concurrency subtlety, no test to lean on | `opus` | Tricky algorithms, cross-module refactors, bugs without a reproduction, security-sensitive code |
| Judgment | A recommendation someone must defend, conflicting evidence, final review of others' work | `fable` (or keep it in the lead) | Architecture call, reviewing a risky diff, choosing between designs |

Tie-break rules:

- **Between two tiers, take the higher one.** Routing errors cluster at near ties, and a failed cheap run costs its tokens plus the retry.
- **Cheapen mechanics, never judgment.** A cheaper model never reviews or approves another model's work.
- **No check, no downgrade.** If you cannot verify the result cheaply, do not route it below `sonnet`.

## Step 3. Write the plan, then spawn

Print one line per task before spawning anything:

```
<task> | <tier> | <model> | <why, in one line: what makes it safe or what makes it hard>
```

Example:

```
List functions without docstrings | mechanical | haiku | exact list, checkable with grep, no judgment
Fix parse_date for ISO week dates  | bounded build | sonnet | failing test given, one function
Implement money allocation rounding | hard build | opus | sum invariant and negative edge cases, no tests provided
```

Then pass the model on each spawn (Agent tool `model` parameter) or set it in the subagent file:

```yaml
---
name: inventory-worker
description: Lists and counts things in the repo. Mechanical, checkable output.
model: haiku
---
```

## Step 4. Escalate once, then take it back

If a subagent's result fails its check, rerun that one task one tier up, once. A second failure is a scoping problem: the lead takes the task back instead of escalating again.

## Pin what the aliases mean

`haiku`, `sonnet`, `opus` and `fable` resolve to whatever model your Claude Code version maps them to, which can lag the newest release (Claude Code 2.1.280 mapped `sonnet` to Sonnet 5, not Sonnet 5.5). To get the model you priced, pin each alias once for the session or project:

```bash
export ANTHROPIC_DEFAULT_HAIKU_MODEL=claude-haiku-4-5-20251001
export ANTHROPIC_DEFAULT_SONNET_MODEL=claude-sonnet-5-5
export ANTHROPIC_DEFAULT_OPUS_MODEL=claude-opus-5-5
export ANTHROPIC_DEFAULT_FABLE_MODEL=claude-fable-5-1
```

A subagent file can also take a full model ID in `model:`. After the run, check which IDs actually ran (`modelUsage` in `claude -p --output-format json`).

## Prices to reason with

Per million tokens, Anthropic API list prices as of 2026-10-14. Read current prices before relying on them.

| Model | Alias | Input | Output | Cache read |
| --- | --- | --- | --- | --- |
| Claude Haiku 4.5 | `haiku` | $1 | $5 | $0.10 |
| Claude Sonnet 5.5 | `sonnet` | $2 | $10 | $0.20 |
| Claude Opus 5.5 | `opus` | $4 | $20 | $0.20 |
| Claude Fable 5.1 | `fable` | $10 | $50 | $0.25 |

Compare routes on cost per finished task, not price per token: a cheap model that needs a retry is not cheap.

## Output

The per-task plan lines above, the `model` used on every spawn, and after the run a one-line tally: tasks per model, any escalations.
