---
name: fabble
description: The prompt-engineering family — author, migrate, enhance, and gate prompts for Claude models. Use when the user wants to (1) write or create a prompt, plan, or task spec from a goal ("write a prompt for X", "turn this into something Fable 5 can run"), (2) upgrade or port an existing prompt to Fable 5 ("upgrade this prompt for Fable 5", "this was tuned for sonnet/opus", "fablize this"), (3) improve an existing prompt that stays on Sonnet or Opus ("make this prompt better without switching models", "fabelike this"), (4) review, audit, score, or gate a prompt before an expensive run ("is this ready for Fable 5?", "audit this prompt"), (5) elevate an ask into a well-specified goal (/until), or (6) enable the /until slash command ("/fabble install", "set up the fabble command"). Every job routes to a references/ playbook.
license: MIT
---

# fabble

One family, five jobs, one subject: getting the most out of a Claude model through the prompt. Each job has a playbook under `.claude/skills/fabble/references/` — route, read the matching playbook fully, then work from it. Never work from memory of a playbook; if it or a behavior file it names is missing, stop and tell the user.

Shared doctrine: prompt quality splits into the **contract** — intent stated, full spec up front, boundaries fenced, claims traced to evidence, done defined countably — and the model's **capability** — what it does unprompted. The contract is model-agnostic and always belongs. Fable 5 needs little beyond it; Sonnet/Opus need the contract plus compensating scaffolding; over-prescribing Fable 5 degrades it.

The doctrine applies reflexively: these playbooks are themselves prompts, executed by whichever model runs this skill. On a Sonnet/Opus executor the compensations fabelike prescribes bind YOU — walk every delivery gate item one by one against the actual text, trace every add, cut, and verdict to its named reason, and never claim a gate or probe ran without having run it. Optimistic completion claims about your own gates are the same defect the gates exist to catch.

## Routing

Two questions pick the playbook: what does the user HAVE, and what should the RESULT run on?

| Have | Result | Playbook |
|---|---|---|
| Goal + raw information, no prompt yet | Execution-ready prompt (Fable 5 default; Opus/Sonnet on request) | `references/promptify.md` |
| Existing prompt | Runs on Fable 5 | `references/fablize.md` |
| Existing prompt | Stays on Sonnet/Opus, raised to its ceiling | `references/fabelike.md` |
| Fable-shaped task, user staying on Sonnet/Opus | Goal re-authored + ordered run sequence | `references/promptify.md` with the Opus/Sonnet deltas — the `/until opus|sonnet <intent>` path |
| Finished prompt | Verdict before an expensive run | `references/audit.md` |

If the ask doesn't say which: a pasted prompt-shaped block means they HAVE a prompt; loose goals and facts mean create. Target model defaults to Fable 5 unless the user names another.

## Shared behavior files

Playbooks draw on three files in the same `references/` directory — single source of truth, never duplicated into playbooks:

- `fable5-behavior.md` — Fable 5 defaults, failure modes → steering snippets, classifier hazards.
- `opus-behavior.md` — deltas when the runtime is Sonnet/Opus.
- `gate.md` — the seven audit probes and scoring rubric.

## Commands

- `/until [opus|sonnet] <ask>` — elevates an ask into a goal via `references/promptify.md`. (Distinct from Claude Code's built-in `/goal`, which loops the current session until a condition holds.)
- `/fabble install [global]` — one-time enable of `/until`: copies the bundled `commands/until.md` into the matching commands directory. Procedure, scope rules, and output contract: `references/install.md`.
