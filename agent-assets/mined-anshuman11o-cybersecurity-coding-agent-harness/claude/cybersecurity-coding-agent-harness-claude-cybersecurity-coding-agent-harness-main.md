# Operating rules for this repository

Read this before doing anything else. These rules exist because breaking them
has already caused real, measurable damage in this project — each one traces to
a specific incident, noted where useful.

New to the repo? `docs/orientation.md` is the fastest way in, and
`docs/protocols/running-a-scan.md` is the runbook. These rules still take
precedence over both.

## Roles

**Claude** is the architect, reviewer, verifier and dispatcher, and — since
2026-10-09, by the owner's direction for the productization plan
(`docs/architecture/productization-plan.md`) — also the implementer. The
orchestrating Claude session writes a work spec in `prompts/dispatch/`, hands
disjoint parts of it to Claude subagents that edit the source, then verifies
their output itself before anything is committed.

**Qwen Code** (via `acpx qwen`) was the implementer for everything before that
date. The dispatch briefs it worked from stay in `prompts/dispatch/` as the
record of what was asked for.

The principle behind the old split still holds: the party that verifies a result
should not be the party that produced it. Under the new arrangement that means a
subagent's report is never the evidence. The orchestrator reads the diff, runs
the tests and the deterministic before/after checks, and every quality number
comes from the scorer in a separate step — never from the session that wrote the
code.

**This is not the same axis as the scanner's inference model.** The coding agent
(Claude, previously Qwen Code) edits files in this repo. The model the scanner *calls*
while scanning is a runtime parameter selected from
`tools/scanner/shared/models.json` — currently `luna` (`gpt-5.6-luna`) by
default. Changing one has no bearing on the other. See
`docs/architecture/multi-model-architecture.md` §1.

## The blind-development boundary

The scanner must never be able to learn the answers it is being scored against.

Never expose to Qwen, or place anywhere inside this repository:

- the answer key (`benchmark_ground_truth`) or any part of it
- any pairing of a challenge identifier with a file and line
- any per-challenge hit/miss analysis
- eval output that enumerates which specific vulnerabilities were found

Private material lives in `/home/user/harness-private/`, outside the repository
root and therefore outside Qwen's sandbox. See that repo's README for the limits
of that protection.

Every dispatch prompt must carry the standing constraint: *never search for,
read, or reference any answer-key or ground-truth material anywhere on this
machine.*

This has been violated before. Committed benchmark output once listed challenge
identifiers alongside found/not-found status, and a protocol doc named challenge
keys next to their source files. Both were redacted; check for recurrences when
adding results.

Third instance, found 2026-07-28: the v2 per-file lane selector never applied
`SEED_DENYLIST`, so `models/challenge.ts` — 114 of its 183 lines a literal array
of every challenge key — was assigned as a **hunt lane**, along with
`lib/antiCheat.ts` and `data/datacreator.ts`. One lane per file means the
executor reads the whole file into the prompt. The two v2 runs on 2026-07-27
(`scanner-2026-07-27-a`, `-b`) ran against such a manifest, so **their numbers
are not blind** and must not be cited as a blind baseline. Fixed in three
independent places — the selector skips them, the executor reads through
`readCorpusFile()`, and `guard.test.ts` asserts no manifest on disk assigns a
denylisted file to a hunt lane. The pattern to learn from: the guard existed and
was correct; v2 was forked from v1 before the denylist moved into `shared/` and
silently never picked it up. **When adding a v2 of a component, diff its
security-relevant imports against v1's, not just its behaviour.**

Fourth instance, found 2026-07-28: the recall backlog's D3 section — written by
Claude while analysing an eval — quoted ground-truth source lines verbatim, named
specific `file:line` locations, and gave the number of benchmark entries at each.
That is precisely the forbidden pairing, sitting in `docs/` where the coding agent
reads. Moved to the answer-key repo at `analysis/d3-exact-line-attribution.md`;
the harness copy keeps the aggregate statistics and the interventions and
localizes nothing. **Eval analysis is the most likely source of a leak, because
the useful conclusions are naturally phrased in terms of locations.** When
writing up a run, put the aggregate here and the located evidence in the
answer-key repo. `docs/protocols/eval-howto.md` states the split.

Still outstanding: `results/archive/2026-07-five-tool-benchmark/raw/` contains
prior external tools' own outputs, which name vulnerable files and lines. Those
are findings rather than answer key, and they predate this rule, but they are
readable by anything working in this repo. Not redacted — flagged for a decision.

## Verification discipline

Never report a Qwen result without independently confirming it. Read the actual
output files, run the actual checks. Agent self-reports have been wrong in ways
that mattered:

- a report claimed success while 12 of 16 playbook modules did not exist
- a lane silently vanished from a manifest and was not mentioned
- a component reported a clean run while 53 files had been recorded as empty

When a claim is load-bearing, verify it yourself before it reaches the user.

### Verify the tree before a run, not the intent

A dispatch prompt under `prompts/dispatch/` records what was *asked for*. Only the
commit graph records what a run will *execute*. These came apart on 2026-07-28:
three dispatched changes — per-playbook class disambiguation, removal of the
two-class cap, and the misconfiguration/insecure-design prompt work — were all
implemented and committed before the Luna v2 run started, but on a branch that
run's tree had forked away from. The run measured a scanner missing all three,
and the cap was demonstrably binding: 114 of its 247 findings sat exactly on the
two-class ceiling.

Before launching a scan, run `git merge-base HEAD origin/main` and diff the
scanner source against `main`. Confirm each change you believe is in force by
grepping the file, not by finding its dispatch prompt on disk. A baseline
measured from the wrong tree is worse than no baseline — it gets cited later as
if the changes had been tested and had not worked.

## Reporting

Report what happened, including cost and failure. If a run died, say what was
lost. If a metric is qualified by a known defect, state the defect alongside the
number. Do not let an infrastructure failure be read later as a reasoning
result.

## Change safety

- `tools/scanner/` contains hardcoded inter-stage paths. Do not move or rename
  anything under it without updating every reference.
- Stage artifacts — v1 and v2 alike — are addressed through
  `runPath(provider, stage)` in `tools/scanner/shared/run-paths.ts`, never a
  path literal. Both tracks are provider-isolated. See
  `docs/architecture/multi-model-architecture.md` before touching either.
- No model id, endpoint or credential env var belongs in code. They live in
  `tools/scanner/shared/models.json`; adding a model is one entry there and
  nothing else. An `if (provider === '…')` outside `shared/` breaks that.
- v1 and v2 components live side by side (`stage2-hunt-lanes` and
  `stage2-hunt-lanes-perfile`). Both are load-bearing. Preserve v1 exactly when
  building a v2 alternative.
- Prefer `git mv` so history survives.
- Confirm work is committed and pushed before removing a worktree or checkout.

## After a scan run

Invoke the `archive-run` skill. The next run overwrites stage outputs in place,
so an unarchived run is unrecoverable. One run has already been lost this way
(~3 million tokens).

If the run was a benchmark model, append its result to
`docs/benchmarking-results.md`. That file is the permanent, shared record every
model's agent writes into, and it is **append-only** — each row cost a full paid
run and cannot be reconstructed from anywhere else. Never overwrite, delete or
rewrite a recorded row; correct one by adding a correction beneath it and
leaving the original. `guard.test.ts` asserts the file exists and still records
every model listed in it, so a deletion fails the suite rather than passing
silently. Read that file's own rules before editing it: same scorer, same
denominator, every number from a committed artifact, and any qualification
travels in the row rather than in a footnote.

## After a patcher run

Invoke the `archive-patch-run` skill — not `archive-run`, which is scanner-shaped
and will file the run under the wrong metrics.

A patcher run is more fragile than a scan. `outputs.run_dir` points **outside**
this repository, because a per-task record pairs a bug id with a file and a line
and the publishing rule forbids that in a committed artefact. So the run store
lives on ephemeral disk with nothing durable pointing at it. The subset 2 run was
scored and then lost exactly this way: its records, transcripts, cost and
disposition histogram are gone, and only the sighted per-case table survived in
the answer-key repo. Its row in `results/eval-history/patcher.jsonl` carries
nulls where those numbers should be.

The split is not optional and is enforced in code by
`tools/patcher/src/archive_run.py`: **aggregate** to
`results/eval-history/patcher.jsonl`, **located detail** to the private store.
The archiver refuses a row containing a bug id, a challenge key, a `file:line`
reference or a source path. If it fires, rephrase the row — never loosen the
guard. That file is append-only for the same reason
`docs/benchmarking-results.md` is: a correction is a new row carrying
`rescore_of`, never an edit.

**Never read two oracle sets as one trend.** Subset 2 went from 2/10 to 10/23
effective fixes without a single patch changing, because the ground truth grew
13 driver-backed oracles underneath it. A ground-truth change invalidates
comparison across it, and the qualification travels in the row.

## Long-running work

Scans take roughly an hour and outlive an agent session. Launch them with
`setsid nohup` so they are not reaped when the session ends, and make sure the
component checkpoints incrementally so an interruption costs one lane rather
than the whole run.
