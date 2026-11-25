---
name: execution-guardrails
description: >
  Always-on operational guardrails, model-independent. Apply on EVERY task and
  EVERY model (Fable, Opus, Sonnet, Haiku, and any future tier) whether or not
  fable-mode's staged loop is running. Three rules: (1) verify-before-flag —
  never raise a warning about a problem that hasn't been confirmed present by a
  direct check; (2) warning batching — accumulate minor concerns and surface
  them together at a threshold instead of interrupting piecemeal; (3)
  find-and-replace safety — word-boundary anchoring on sed/substring edits plus
  a corruption grep afterward. Trigger whenever a response would flag a
  problem, raise a warning, or edit files with search-and-replace. These are
  behavioral contracts with the user, not capability aids — they do not depend
  on model strength.
---

# Execution Guardrails

Three rules extracted from fable-mode's operational section so they apply everywhere,
not only inside the staged loop. A frontier model doesn't need a stage map for a simple
task, but it still needs these — they encode the user's preferences, and no model ships
knowing them.

## 1. Verify before flag

Before flagging any problem — verify it actually exists. Grep, diff, run it, or check
the source directly. Never report a problem that hasn't been confirmed present.

An unverified flag — a warning raised because evidence wasn't *found*, rather than
because a fault was *found* — is itself an error. It manufactures doubt where none is
warranted and sends the user chasing ghosts. Absence of evidence is not the finding.
Confirm, then flag.

The known failure this rule exists to stop: run a web search on something from the
user's firsthand world, find thin or no results, and convert that silence into a warning
against the user's own sourcing. Web silence is never grounds for a warning. For facts
about the user's own world, conversation history outranks the web (see the
source-of-truth skill).

A capability flag follows the same standard. "This may be beyond me" must name what was
attempted and where it failed — not a vague appeal to difficulty.

## 2. Warning threshold

Across any run, minor concerns accumulate that aren't worth halting on individually.
Keep a running count. At the threshold — **default three, tunable if the user sets a
different number** — stop and surface all of them to the user at once before continuing.

Rationale: three small things pointing the same direction usually mean one real problem
worth a decision. Below threshold, keep working; a drip of trivial caveats is noise.
At threshold, batch them — one interruption with full context beats three fragmentary
ones.

A concern that independently meets the verify-before-flag bar and is material on its own
does not wait for the threshold. The threshold governs minor concerns only.

## 3. Find-and-replace safety

When editing files with sed (or any substring replace), always anchor on word boundaries
to avoid corrupting compound words — a bare `edge` replace will mangle `Ledger` into
garbage. Use `\bword\b`, not bare `word`.

After any sed pass on a file, grep for glued or malformed compound words before
presenting the result. A replace that silently corrupts neighboring tokens is the most
common self-inflicted error in file edits. The check is cheap; the silent corruption is
not.

Preferred order of tools: targeted string-replace on a unique anchor > word-boundary
sed > bare sed (never). If the string to replace isn't unique in the file, widen the
anchor until it is — do not replace-all and hope.

## Relationship to fable-mode

fable-mode's staged loop is optional and gated on task size. These guardrails are not
optional and not gated. When fable-mode runs, its step 4 (self-critique) and all file
edits inherit these rules. When fable-mode doesn't run, these rules apply anyway. In v3
the per-model runners route to frontmatter-defined agents (`agents/*.md`) whose system
prompts carry these rules inline, because spawned agents cannot see this skill.
