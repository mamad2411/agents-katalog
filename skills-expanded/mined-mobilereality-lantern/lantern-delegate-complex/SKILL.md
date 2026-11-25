---
name: lantern-delegate-complex
description: Hand one heavy task to a background delegate on Opus or Fable instead of Sonnet, in its own git worktree, with the same Lantern flow as lantern-delegate, but only after the user chose that model for that task. Sonnet is always the default; when you judge a task heavy (Sonnet unlikely to manage it, unclear blast radius, hard design or debugging) you ask the user one question with Sonnet (Recommended, cheaper), Opus and Fable (most capable, dearest) and dispatch as they answer. Use for "zleć to mocniejszemu modelowi", "delegate this to Opus", "delegate this to Fable", "lantern-delegate-complex", "this is too hard for the Sonnet delegate"; never for mechanical work and never on your own pick. An Opus or Fable delegate does the whole run itself, the map and the pull request record included, because the map's model policy accepts both. Not self-contained: it states only what differs and sends the orchestrator to lantern-delegate's SKILL.md and the delegate to its protocol.md for the rest.
user-invocable: true
---

# Delegate (Lantern), heavy tasks

Read `lantern-delegate`'s `SKILL.md` in full first and follow it for everything this file does not
change: the preflight gate (`$D/scripts/preflight.mjs`), PR delivery, scoping, the brief template, the
map status, the diff reading, the map gate, the PR handover with its real cost, the linters and the
clean-up. `$D` is `lantern-delegate`'s folder, `$S` is `lantern-sync`'s, `$L` is `lantern-setup`'s. The delegate follows
`lantern-delegate`'s `protocol.md`, including its "Opus and Fable delegates" section. Nothing is copied here: a
script, the protocol or the brief template changes once, in `lantern-delegate`, for both.

## Sonnet is the default; the user picks anything dearer

Many delegates run at once and every run spends quota, so Sonnet is the norm and stays the norm. **You never
pick Opus or Fable yourself**, and no stored preference, earlier answer or habit selects a dearer model for
you: every Opus or Fable delegate exists because the user answered a question about that very task.

When you judge a task **heavy**, return to the user with **one question for that task** before dispatching
it: `AskUserQuestion` in the Claude orchestrator, a plain question otherwise, with three options in this order:

1. **Sonnet (Recommended, cheaper)**: the usual `lantern-delegate` ladder, `sonnet-high` for a hard one.
2. **Opus**: `lantern-delegate-complex-opus-<level>`.
3. **Fable (most capable, dearest)**: `lantern-delegate-complex-fable-<level>`.

Dispatch as the user answers. A split of several tasks asks one question per heavy task and dispatches the
others at once, on Sonnet. Never offer the choice for a task you do not judge heavy, and never ask twice.

A task is **heavy** when Sonnet at `sonnet-high` is unlikely to manage it, for example:

- the hard part is deciding *what* to do: a design with real trade-offs, an architecture or contract change
  that other code leans on;
- the blast radius is unclear and finding it is the job: a bug nobody can reproduce, behaviour that spans
  many modules, a refactor with no obvious edge;
- it needs judgement no `Verify` command can check, so a weaker model's mistake would pass unnoticed.

It is **not** heavy because it is long, mechanical or fully specified, nor because it is risky but easy (a
migration with a clear shape needs a stronger `Verify` and a narrower `Should not`, as in `lantern-delegate`).
Torn between heavy and not: it is not, and Sonnet takes it.

## Who does what

| | agent type | model | does |
|---|---|---|---|
| delegate | `lantern-delegate-complex-opus-medium`, `-high`, `-xhigh` | Opus (`claude-opus-5-5`) | everything of `protocol.md`: the code, the green loop, the Lantern re-mapping, the PR record with its flow, the push, the pull request |
| delegate | `lantern-delegate-complex-fable-medium`, `-high`, `-xhigh` | Fable (`claude-fable-5-1`) | the same |
| reviewer | `reviewer` for an Opus delegate | Opus | the review (`VERDICT:` lines), read-only |
| reviewer | `reviewer-complex` for a Fable delegate | Fable | the same |

The delegate does the whole run, including the Lantern work (`sync.mjs finish`, the re-mapping, features and
areas, the PR record with reasons, order and flow, `sync.mjs verify`), because the heavy delegate already
holds the context and the map's model policy accepts it (`$L/scripts/model.mjs floor`: Sonnet, Opus
and Fable of any version; Sonnet 5.5, Opus 5.5 and Fable 5.1 or newer are recommended and a lower version
only warns; Haiku is refused). Nothing is handed to a third agent. The
`--model` of `finish` is the delegate's own exact id (`claude-opus-5-5`, `claude-fable-5-1`), never an alias.
A Sonnet delegate still spawns only its reviewer; so does an Opus or Fable one.

## The ladder

`medium → high → xhigh` for each model, entered at the lowest that fits, with the same rules as
`lantern-delegate`'s ladder: torn between two, take the lower; `xhigh` is never a first dispatch, only the
escalation after `high`; no effort change mid-session. The Agent tool has no effort parameter, so effort is
set only by the agent type. Dispatch:

```
Agent(
  description:       "<3-5 words>",
  subagent_type:     "lantern-delegate-complex-fable-high",
  model:             "fable",
  isolation:         "worktree",
  run_in_background: true,
  prompt:            "<the brief>"
)
```

`model` matches the type or is left out; never `sonnet` on these types, never `opus` on a Fable one or `fable`
on an Opus one (`lint-reviewer.mjs` flags it as `delegate-type-on-wrong-model`).

## What changes in the workflow

- **Agent types.** The gate does not check them. Before dispatch the session must offer the type you are
  about to use (`lantern-delegate-complex-opus-<level>` or `-fable-<level>`) and its reviewer (`reviewer` or
  `reviewer-complex`); the bundle installs all of them (`pnpm run install-skills -- <project>`, or opening the
  project in Lantern). Missing one: run the installer, retry the dispatch once, and if it is still rejected
  tell the user. There is no Sonnet fallback for these types, and `reviewer-complex` has none either.
- **The brief** is `lantern-delegate`'s template with these changes: the `Protocol` line says "Load
  `lantern-delegate` and read only its `protocol.md`, including its Opus and Fable delegates section"; the
  `Lantern` block and the `Should not` bullets stay as they are, since the delegate re-maps itself.
- **Review check** (step 8 of `lantern-delegate`). The verdict is the matching reviewer's; a reviewer whose
  result never arrives is replaced by a fresh one of the same type that you spawn yourself, and the same "no
  fallback" rule holds.
- **The map gate** is the same command, run in the delegate's worktree after it reports. `RED`: resume the
  delegate with the exact output. Never fix the map yourself.
- **Linters at handover.** The same four runs of `lantern-delegate`; `lint-reviewer.mjs` is the one that
  knows this skill: a review by a type other than the matching reviewer, a reviewer spawned with a `model` and
  a delegate type that ran on another model family are each a non-zero count (`review-not-by-reviewer`,
  `model-override-on-spawn`, `delegate-type-on-wrong-model`). `check-skill-use.mjs --role reviewer` runs on
  the `reviewer-complex` transcript too.
- **Stalls.** A stalled loop is diagnosed as in `lantern-delegate`. There is no stronger model than Fable at
  `xhigh`: past it, change the approach or tell the user.

## The closing message

The same, with the model column showing `opus` or `fable` for the delegate row and the reviewer row of the
same model. The reviewer row is grouped under its delegate (`build-report.mjs` finds it through
`parentAgentId`): grouping, not containment, so sum every row.

| Agent | Model | Effort | Calls | Cache-read | Cache-write+input |
|---|---|---|---|---|---|
| cart store · delegate | fable | high | 61 | 910220 | 52100 |
| └ reviewer-complex ×2 | fable | medium | 48 | 690410 | 41230 |
| promo codes · delegate | opus | high | 40 | 520300 | 30100 |
| └ reviewer ×1 | opus | medium | 22 | 340220 | 19080 |
| **total** | | | **171** | **2461150** | **142510** |

The `map:` lines are the delegate's own count, taken from its Report. The PR body's cost block has the same
kinds of row (`protocol.md` says how the delegate fills them).

## Hard rules

All of `lantern-delegate`'s apply. In addition:

- Never dispatch through `lantern-delegate-complex-<model>-<level>` without the user's answer to that task's
  own question; Sonnet is the default and the recommended option, and nothing stored overrides it.
- Dispatch only through the type of the model the user chose, never a Sonnet type with `model: "fable"` or
  `"opus"`, and never an Opus or Fable type for work `sonnet-high` could do.
- Reviewer is `reviewer-complex` for a Fable delegate and `reviewer` for every other.
