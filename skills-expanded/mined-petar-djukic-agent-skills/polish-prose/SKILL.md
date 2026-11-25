<!-- Copyright (c) 2026 Petar Djukic. All rights reserved. SPDX-License-Identifier: MIT -->
---
name: polish-prose
description: >-
  Improve, polish, tighten, or make better any prose a person reads end
  to end — an essay, post, paper section, README, or book chapter. The
  default for any request to improve a whole piece of writing ("can you
  improve this", "make this better", "polish this", "this is meh", "it
  reads flat", "clean this up"), ahead of the single-stage skills it
  runs. One multi-agent Workflow, the review loop: reverse-outline, a
  length pre-check, a critic panel answering the caller's focus brief by
  name, critic-apply, cold review, ross read, voice-critic, re-reading
  until a panel read of the final text changes nothing. The humanize
  chain runs first only when the caller passes humanize: true. Line and paragraph work; restructuring a piece
  is a separate refine pass. Invoking this skill is the opt-in to the
  Workflow run. Triggers: improve this, polish this, make it better,
  tighten this, it's meh, it reads flat, clean up this draft, rewrite
  this, full rewrite, humanize and review, run the whole pipeline.
argument-hint: '<file.md> [--humanize] [--max-rounds N] [--panel-only] [--roster name] [--focus-file path] [--venue name] [--pangram]'
---

# Polish Prose (critics, until stable)

**Polish is the critics** (GH-483). The run is the review loop: the
panel reads, critic-apply makes one narrow change per flagged passage,
and cold review reverts any change the original does not entail. The
humanize chain is not part of a polish unless the caller asks for it
with `humanize: true`. The chain rewrites every paragraph, and on
authored prose that is where the damage came from: two runs on a
journal paper drifted claim-carrying sentences ("how the LAM looks and
acts" became "the LAM's appearance and operation"; "level 4" became
"level 4 and above"), and protected terms and an inflation lexicon
(GH-477) did not stop the next run, because the drift lands in ordinary
words no list names. The round-1 panel caught that drift both times.
Opt in only for AI-drafted text that has not yet been through the chain.

The pipeline used to live only as prose in the caller's workflow
command, executed by hand one stage at a time. Prose rules get skipped:
on the article that prompted this skill, the panel read a draft on
2026-10-21, two later cycles added prose, and nothing re-read it — the
author found the result flat on his own read. This skill moves the
order, the parallel critics, and the re-read into a Workflow script,
where a skipped step is impossible rather than unlikely.

**It owns order and the loop, nothing else.** Every stage is one agent
that reads the owning skill's SKILL.md and follows it. No stage command,
model name, or threshold is restated here or in the script; when a
stage changes, its own skill changes and this pipeline picks it up. The
one model choice that is the pipeline's own is which tier each stage
*agent* runs on (GH-487): six measured runs averaged ~84k tokens per
agent with ~58k of it boot context, so the judgment-light stages run on
smaller models while the persona critics and the Iceberg legs keep the
session model. That choice never touches an owning skill's internal
transport (critic-apply's `CRITIC_APPLY_MODEL`, voice-critic's judge).

**Polish, not refine.** This pass works on lines and paragraphs: cuts,
splits, diction, the announcing clause, the paragraph that restates the
lede. It will report that a piece wants splitting in two or a section
reordered, but it does not do that work; structure is a refine pass
(match-outline, reverse-outline's cut list) the caller runs first.

## Launch

Run the bundled script with the Workflow tool, from the repository that
holds the file:

```
Workflow({
  scriptPath: "<this skill's directory>/workflow.js",
  args: { article: "<path/to/file.md>" }
})
```

In a repository that composes skills under `.github/skills/`, the
script path is `.github/skills/polish-prose/workflow.js`. When the run
returns, read the report's `word_diff` — the article's word-diff against
the baseline — before anything else, and relay it first: name the
largest meaning-bearing changes the diff shows, then the roster used,
rounds, what each round applied, the last panel read's convergent
findings and focus answers, which optional stages were skipped and why,
and the residue still open. Metrics never stand in for the diff: a
caller who has not read the diff has not reviewed the run (GH-477, where
two runs shipped meaning drift on the report's numbers). The report is
the record; nothing is written to a sheet.

| arg | default | meaning |
|---|---|---|
| `article` (or `file`) | required | the markdown file to polish |
| `skills_dir` | `skills` | where the owning skills live |
| `roster` | by form | a critic-panel roster name or a list of persona names |
| `humanize` | false | `true` runs the humanize chain once before the review loop; only for AI-drafted text that has not been through it |
| `skip_humanize` | true | kept for older callers; it is the default, and it wins over `humanize` |
| `max_rounds` | 3 | review rounds before the read-only final pass |
| `min_edits_for_next_round` | 3 | a round whose net applied edits (after cold-review reverts) fall below this ends the loop: it already read the near-final text, and the separate final read is skipped (GH-487) |
| `panel_only` | false | a verdict without the loop: preflight, the critics, one converge; no commits, and the run returns the sheet path and per-critic verdicts. Runs on any branch, main included, because it changes nothing (GH-487) |
| `stage_models` | by stage | per-stage overrides of the stage agent's model tier, `{stage: model}`; an empty value means the session model. Stages: `preflight`, `humanize`, `step6`, `outline`, `critic`, `converge`, `apply`, `cold`, `iceberg`, `iceberg_apply`, `ross`, `voice`, `final_prep`, `record` (GH-487) |
| `focus_file` | discovered | path to the caller's `critic-focus.md` |
| `form` | inferred | the file's form; selects its constitution and voice-critic caps |
| `venue` | inferred | passed to humanize's venue mode when the chain runs; preflight picks the `writing-voice/venues/` profile that fits the form (a paper section is `academic`) when the caller names none |
| `pangram` | false | `true` opts this run into Pangram uploads. Off by default, whatever the standing consent says: every stage then runs with `PANGRAM_CONSENT=off` and `--no-pangram`, and scores read "not measured" (GH-437) |
| `validate_only` | false | preflight only: reports roster, focus file and skipped stages, changes nothing |

Run `validate_only` first in a repository the skill has not run in.

## Any prose, not just articles

| what preflight finds | what changes |
|---|---|
| a book chapter | the `book` roster (verdict critics) instead of `article` |
| `docs/constitutions/*.yaml`, an SRD, a form constitution | every critic judges against those rules first (critic-panel's "The draft's own rules") |
| no `writing-voice/` corpus | with `humanize: true`, humanize is skipped: match-voice needs the exemplars |
| no voice constitution | voice-critic is skipped: it refuses without one |
| a form voice-critic has no profile for (paper section, README, chapter), or no judge ready (no Cohere key and `gemma4:12b` not pulled) | voice-critic is skipped once, named in the skip list; `voice_critic.py --preflight` decides it and every round reuses its form and model |
| no YAML front matter | no generation note; the report is the record. No stage may add front matter: reverse-outline's thesis proposal goes in its commit body, and Record removes any block a stage added |

Every skip is named in the report, never silent.

## The stages

| phase | stage | owning skill | commits |
|---|---|---|---|
| Preflight | branch check, skill paths, focus file, form, roster, the draft's rules, protected spans, baseline commit | — | baseline commit only |
| Humanize (only with `humanize: true`) | the chain, once, one commit per stage | humanize | one per stage |
| | filter-tells Step 6, the independent evaluator, in a fresh context that never saw the rewrites; its findings seed round 1's residue (GH-443); after the rounds, the same evaluator runs once more on the shipping text, since critic-apply and the Iceberg pass write prose the chain never scanned — with humanize off it is the run's only filter-tells coverage — and its findings land in the residue (GH-493) | filter-tells | `filter-tells step 6`, empty, with the verdict |
| Review, each round | annotate or audit, rank | reverse-outline | `reverse-outline` (markers, or empty with the audit) |
| | length pre-check | the focus file's command | — (in the reverse-outline commit's body) |
| | the roster in parallel, fresh contexts, focus brief answered by name | critic-panel Mode A | — (critics write sidecar reports) |
| | merge, then rule-based application, one agent: the merge is a script run and rides with the apply (GH-487) | critic-panel `converge.py` + critic-apply | `panel`, empty, with the convergent passages and focus answers; then `critic-apply … candidate`, the attempt itself |
| | fresh-context entailment, reverts only | cold-review | `cold-review … critic-apply: <verdict>`: empty, reverts, or the baseline restored |
| | CoT warrant tails removed by deletion only, two fresh legs carrying the focus brief, the draft's rules, and the panel's keep answers; keep-listed cuts reported, not applied (GH-416) | critic-panel `iceberg` roster + critic-apply | `iceberg … candidate` |
| | fresh-context entailment on the Iceberg candidate, reverts only | cold-review | `cold-review … iceberg: <verdict>` |
| | cross-family comprehension read; closes the round by measuring its net prose diff (GH-487) | critic-panel Mode C | `ross` (fixes in rounds 1–2, empty with the findings after) |
| | voice audit | voice-critic | `voice-critic`, empty, with the verdicts |
| Final read | read-only panel on the shipping text, when the round cap stopped the loop | critic-panel Mode A | `panel … final read`, empty |
| Record | rst-marker strip (reverse-outline `strip`), generation-note entry when there is front matter, sidecar sweep, the word-diff for the report | — | yes |

Every stage that runs ends in a commit (GH-434). A stage that leaves the
text alone commits empty, with what it found in the body, so `git log` on
the branch reads as the run's record. An attempted change is committed
before cold review judges it, and the verdict is a commit of its own, so a
rejected attempt stays readable with `git show`. The round's "did the prose
change" test measures the net diff from the round's first commit, so an
attempt that cold review undid does not count as change.

The persona critics and the Iceberg legs run on the session model; the
ross read adds two Ollama models from different families, and only its
cross-family convergence gets fixed. Every other stage agent runs on a
smaller tier by default (GH-487) — mechanical stages (preflight,
converge, record, the final-read prep, the ross agent's own
orchestration) on the smallest, the judgment-light middle (critic-apply,
cold review, reverse-outline, voice-critic, filter-tells Step 6) one
up — overridable per stage with `stage_models`.

## The stopping rule

A panel read binds only the text it read (critic-panel Mode A). Each
round reads the current text; if the round changed the prose (markers
excluded), the next round re-reads it, carrying this round's unapplied
convergent targets and paragraph moves as residue the critics must
check by name: the open items join the focus list as numbered items
(R1, R2, ...), and the merge returns one consensus answer per item,
marked "unanswered" when no critic took it up (GH-457). Shown apart from
the focus list, they were answered in round 1 and dropped after. Every edit cold review reverted, or every applied target
of a candidate it rejected, joins a closed list the panel and the
Iceberg legs are told not to re-propose, for the rest of the run
(GH-438): without it, one run proposed, applied and reverted the same
three edits in all three rounds. The list is also enforced: each rejected
change goes to critic-apply as data (`--closed`), which declines the same
kind of change on the same passage however the panel rewords it (GH-467). The loop ends when a round changes nothing: that round
was a read of the final text. It also ends when a round's net applied
edits (after cold-review reverts) fall below `min_edits_for_next_round`
(GH-487): a round costs the same whether or not it finds anything, so a
round that landed almost nothing was already the read of the near-final
text, and the separate final read is skipped — the report says which
rule stopped the loop (`stop_reason`). At the round cap, one read-only
panel pass runs on the final text, so the report always describes what
ships.

The ross read fixes cross-family convergent findings in round 1,
repairs regressions in round 2, then only reads (the batch cap). One
exception holds in every round: an edit the same round applied that the
cross-family read flags as a convergent regression is reverted verbatim
to the round-start wording, so the min-edits stop cannot ship an edit
the read refuted; the revert joins the closed list and counts against
the round's net edits (GH-491). Whatever it
leaves unfixed, it hands on: every cross-family convergent finding still
marked NOT FIXED joins the next round's residue, so the panel answers for
it by name, and the run's final residue, so the report names it even
after the batch cap (GH-439).
When the caller opts in, humanize runs once: re-running the chain on gated prose degraded it in
measurement (0.621 to 0.579 human, 2026-08-22), and the caller decides
any further cycle from the seed-reach report.

## Definitions are yours

No stage writes a definition (GH-469). When a critic or the ross read
flags a term used before it is defined, critic-apply declines the fix as
`declined-author-definition` instead of asking a model to invent a
meaning: one run expanded LAM as "Lean Agent Model". The term stays in
the residue, and the report lists these items as `author_definitions`,
the definitions only the author can write.

## The focus brief

Generic persona briefs miss what the author already knows to look for;
briefed with his standing complaints, the panel converged in one pass on
classes a generic read had surfaced none of. The list belongs to the
caller. Put a `critic-focus.md` at or above the file — the skill walks
up from the file to find the nearest — naming each check as one item,
plus one deterministic pre-check command with `{article}` as the
placeholder. Absent, the panel gives its free read and the report says
so.

## Contracts it inherits

- **Worktree branches only.** Preflight refuses on `main`; every stage
  commits, empty when it changed nothing.
- **No hand-written prose.** Agents analyse and choose; text changes
  only through the rewrite transport, mechanical deletions, and
  verbatim reverts.
- **Protected spans hold.** Constitution-required spans, locked spans,
  numbers, citations and quotations pass through every stage untouched.
- **Sidecars die in the step that consumed them**, and the Record stage
  sweeps anything left (critic-panel's Artifact hygiene).

## Position

It is the caller's whole review pipeline in one call: what a
workflow command runs after a draft exists, and what "improve this"
means for any finished piece of prose. The caller still owns structure,
publication decisions, and the author's read; this skill hands the
author a stable text and an honest residue list.
