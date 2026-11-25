---
name: entry
description: Author a kind as data (an entry in content/kinds) for the Soul Actions tranche and prove it with one command, `pnpm entry prove <family>` — write the entry and its cases, prove, look at the sheets, revise up to three times, attach the verdict and sheets to the pull request. Use when asked to write, add or fix an entry, a kind, a thing's forms or a form's cases, or when a Soul Actions task says "an entry".
---

# entry — write a kind, prove it, look at it, attach

One way in, the same for every lane. An entry is a kind written as data for Engine v2: what it is, the state it
keeps, where it can be held, stood at or sat in, and what can be done with it. The format is
[docs/soul-actions/entry-format.md](../../../docs/soul-actions/entry-format.md); what a form needs and does is
[packages/form-rules/README.md](../../../packages/form-rules/README.md). Read both once. Copy from the examples:
[the kettle](../../../content/kinds/kitchen/kettle.json), [a bench](../../../content/kinds/seating/bench.json),
[a lecture](../../../content/kinds/gathering/lecture.json), and their cases in `packages/form-rules/cases/`.

## The loop

1. **Write** the entry and its cases (below).
2. **Prove**: `pnpm entry prove <family>` (or `node tools/entry/prove.mjs <family|folder|file>`).
3. **Look** at the sheets the verdict names (`gates.look.kinds[].sheet`). Judge them against the bar: it reads as
   the thing in each state, natural if comical. Today no entry can carry a shape, so there is no sheet yet (below).
4. **Revise** and prove again, up to three times. Still failing after three: hand back with the last verdict.
5. **Attach** the verdict and the sheets to the pull request (`tools/proof/upload.mjs`). Never commit a sheet.

## 1. Write

**The entry**: `content/kinds/<family>/<name>.json`, `"format": "souls-entry/1"`, `"kind": "<namespace>:<name>"`.
The rules that catch most first drafts:

- Whole numbers only, in stated units: `_mm`, `_mdeg`, `_us`. No `1.5`, no `1.0`, nothing in ticks.
- Every state field has `n` (a stable number), `type`, `default` and `audience` (`public` unless it is private).
- Words go by reference: every phrase lives in `text` and is named by its key. A `card` names one text of at most
  80 characters saying what it is and what can be done, in facts, never a mood ("quiet", "cosy").
- No word of today's engine in any name you choose (`server`, `tick`, `eden`, `json`, ...), no time of day.
- A relation (who sits, who holds, who signed up) is a link or a parent, never an id in a field.
- Each form: `who`, `starts`, `needs`, `steps`, `effects`; every argument it `takes` is used; a `create` spends
  something; every form can be reached from the defaults. A field that no form sets to some value it declares is
  taken as set from outside (the kettle's water), so a need on it is not a dead end.

**The cases**, one file per kind in `packages/form-rules/cases/<name>.json` (`"format": "souls-form-cases/1"`)
and its outcomes in `packages/form-rules/cases/effects/` (`"format": "souls-effect-cases/1"`). The cases gate
asks, for every form of every kind in the family:

- a rule case where every need is met (`"expect": {"verdict": "yes"}`);
- for each need, by its index, a rule case where it is unmet (`"expect": {"verdict": "no", "need": <i>, "reason": ...}`);
- the form done in an effect case, with what it changes (`"expect": {"verdict": "yes", "changes": [...], "events": [...]}`).

A rule case is `{name, act: {this, form, args}, state: {actor, nodes, moves}, asker: {sees}, expect}`; an effect
case is `{name, state, do: [{act, receipt, expect}], after}`, each act with its own `receipt`. `expect` holds only
the keys you want compared (`verdict`, `reason`, `need`, `detail`, `fix`, `read`, `changes`, `events`, `timers`);
copy the shape of `detail` for each reason from the examples' cases.

Write the expectation from what the form should do, before you run it. **Never edit a case to make it pass**:
cases are data the new engine will run unchanged. If a case is wrong, say why in the pull request.

Working in a scratch folder under `.local/` (nothing published yet, or a broken copy): `node tools/entry/prove.mjs
<folder> --cases <dir>` reads rule cases from `<dir>` and effect cases from `<dir>/effects`. A kind in the folder stands in
for a published kind of the same name.

## 2. Prove

```sh
pnpm entry prove kitchen                       # a family: a folder of content/kinds
node tools/entry/prove.mjs path/to/folder      # a folder or one file
```

It prints one JSON verdict and exits 0 when no gate failed, 1 when one did, 2 on a bad argument.

| Gate | What it runs | Fails when |
|---|---|---|
| `check` | `tools/entry/check.mjs`: the format and the check gate's rules | any finding; each is `{rule, form, field, path, reason, fix}` |
| `cases` | every rule and effect case on the family's kinds, through `@souls/form-rules` | a case's verdict differs, or a form lacks a case above |
| `look` | `tools/entry/look.mjs`: one sheet per kind, a frame per declared state | the picture could not be drawn |
| `run`, `body-look`, `find` | nothing yet | never; they wait for a runner (Engine v2) |

Read `failed` first: it names the gates that failed. `ran` lists the gates that ran, `waits` those that could not
run yet. When `check` fails, `cases` and `look` are skipped: fix the check findings first, each carries its `fix`.

**The run gate on a world.** `pnpm entry run <family> --world <url> [--god <creator folder>]` (`tools/entry/run.mjs`)
plays the same cases on a running local world, from outside: the creator's god CLI sets each scene, the Soul in
`SOULS_HOME` sends the act and reads the receipt. A row passes, fails or is skipped with its cause (a form the world
does not offer, one started by a timer, a start that needs a take); a skip is never a pass.
Then each form a Soul starts is disturbed: the Soul leaves as each step begins and mid-step, a creator removes the
thing, the world restarts (a world under a launcher). Each passes when the form ends with a named reason, the Soul is
free and holds what it held, and the thing, as it stands, can be used again.

**The find gate.** `pnpm entry find <family> --world <url> --kind <name> --form <form> --goal "<goal>"`
(`tools/entry/find.mjs`) runs a real model on the playtest seat, told only the goal, against a thing placed beside a
fresh Soul. It reports whether the form finished and the seat's reads, acts and refusals, with the card and without
(`--arms`). It spends model time: run it only when the task is to measure finding, two repeats.

**The look gate and shapes.** It draws `looks.shape`. Until SA-D3 (#2855) settles how an entry carries a shape,
the format cannot hold one, so a kind with no shape shows `"waits": "a shape: ..."` instead of a sheet. That is
not a failure; say so in the pull request.

## 3 to 5. Look, revise, attach

In the pull request, under Acceptance or Proof: the command, the verdict line (or `ok`, `failed`, `ran`, `waits`
from it), and each sheet as an image link. Run `node tools/proof/publication.mjs` on anything you post.
