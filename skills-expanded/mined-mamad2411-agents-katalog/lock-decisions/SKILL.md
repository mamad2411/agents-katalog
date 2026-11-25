---
name: lock-decisions
description: "Per-finding lock/defer/grill prompt for decision-shaped clusters. Walks the captain through a finite list of decision-shaped findings (typically from triage-feedback), restates each, and routes per the captain's choice — locking via /create-decision, deferring (no file), or invoking /grill-me and returning to the same prompt."
tools: Read, Edit, Write, Glob, Grep
---

Finding-driven decision capture. You receive a finite list of decision-shaped
findings — usually from `triage-feedback`'s `lock-decisions` route, sometimes
hand-supplied by the captain. For each finding you restate the claim, ask the
captain how to resolve it via a three-path prompt, and act on the answer. You
do not generate candidate resolutions yourself.

This skill is **not** open-ended like `grill-me`. The input list bounds the
work: when the list is exhausted, you summarize and exit.

## Inputs

- `findings` — ordered list of decision-shaped clusters. Each entry has:
  - `clusterId` (e.g., `C3`)
  - `topic` (short label)
  - `claim` (verbatim member text from the rNN- file)
  - `citation` (`rNN-{focus}.md:{location}`)
  - Optional: `surfacedBy` (reviewer set), `severity`
- The artifact path the findings refer to (used only to read context if asked
  during the captain's deliberation — never to invent alternatives).

An empty `findings` list is valid input — exit cleanly with an empty summary.

## Process

Execute per finding, in order. Do not batch the prompts.

1. **Restate.** Quote the claim verbatim and name the citation. One short
   paragraph — no editorial summary, no rephrasing of the captain's options.
   Format:

   > **{clusterId} — {topic}** (cited at `{citation}`)
   >
   > {claim}

2. **Ask.** Single three-path prompt via `AskUserQuestion`:
   - `Lock answer now` — captain has a resolution ready
   - `Defer for later` — capture nothing; revisit in a future round
   - `Grill me on this` — invoke `/grill-me` to surface the decision tree

3. **Act on the answer.**

   **Lock**: Ask the captain (free-form follow-up) for the decision body —
   the actual resolution they want recorded. Then invoke `/create-decision`
   with the body **and the rNN- citation appended verbatim** so provenance
   is preserved. Record the resulting file path for the summary.

   **Defer**: Record the deferral. Write nothing. Move on.

   **Grill**: Invoke `/grill-me` with the finding's topic + claim + citation
   as starting context. When `/grill-me` returns, **return to step 2 for the
   same finding** — the captain may now be ready to lock OR may still want
   to defer. Both are valid grill outcomes; do not assume grill always
   resolves into a lock.

4. **Loop** to the next finding.

5. **Summarize.** When the list is exhausted, emit a brief markdown summary
   (see schema below).

## Hard rules

- **Never auto-generate candidate resolutions.** Surfacing alternatives is
  `grill-me`'s job. If the captain wants options, the answer is `grill`,
  not "let me list options for you".
- **Always restate the finding before asking.** The captain should not have
  to re-read the rNN- file to recall what they're deciding.
- **Always include the rNN- citation in the create-decision body.** The
  decision file must carry its provenance forward.
- **Defer-after-grill is a first-class outcome.** Grill exiting does not
  imply the captain is ready to lock. Re-prompt; honor whichever path they
  pick.
- **Empty list → empty summary, clean exit.** No prompts, no apologies.
- **One finding at a time.** Do not concatenate prompts across findings or
  batch decisions in a single create-decision invocation.

## Output schema

Conversational markdown returned to the calling skill (or the captain
directly when invoked ad-hoc):

```markdown
# Lock-decisions summary

| Cluster | Topic | Outcome | Artifact |
|---------|-------|---------|----------|
| {C1} | {topic} | locked | `<scope>/decisions/dNN-{slug}.md` |
| {C2} | {topic} | deferred | — |
| {C3} | {topic} | grilled-then-locked | `<scope>/decisions/dNN-{slug}.md` |
| {C4} | {topic} | grilled-then-deferred | — |

**Totals**: {N locked} locked, {N deferred} deferred, {N grilled-then-locked}
grilled-then-locked, {N grilled-then-deferred} grilled-then-deferred.
```

Outcome values are exactly one of: `locked`, `deferred`, `grilled-then-locked`,
`grilled-then-deferred`. Use the artifact column only for `locked` /
`grilled-then-locked` rows — em-dash for the others.

For an empty input list:

```markdown
# Lock-decisions summary

No decision-shaped findings to process.
```
