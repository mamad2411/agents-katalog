---
name: evolution-engine
description: >-
  Evidence-driven change cycle for any AI agent setup - prompts, CLAUDE.md/AGENTS.md rules, hooks,
  skills, subagent definitions, loop or cron configs. Runs observe (read the evidence the repo already
  has - logs, transcripts, test/CI results, run receipts, git history) -> propose (cited evidence,
  numeric baseline, hypothesis, pre-registered gate criteria, one variable) -> human gate -> enact ->
  measure over N runs -> verdict (pending / improved / no_change / reverted). Keeps an append-only
  ledger in .evolution/ with a stdlib Python helper that refuses proposals lacking numbers, sources or
  thresholds and blocks verdicts when the goalposts moved or N is too small. Use when the user says
  "evolve my agent setup", "should we change this prompt/rule/hook", "evolution review", "is this
  change working", "tune my CLAUDE.md", "harness improvement", "loop evolution", "measure whether
  that fix helped", or when an agent keeps failing the same way and someone wants to tweak its
  instructions.
---

# Evolution Engine

A disciplined way to change an agent setup: every change starts from evidence, is approved by a
human, is measured against criteria written down before it shipped, and is kept only if it earned
its place.

```
observe -> propose -> human gate -> enact -> measure (N runs) -> verdict
                                                                  |- improved  : keep
                                                                  |- no_change : roll back (default)
                                                                  '- reverted  : regression, roll back
```

**What counts as a target**: anything that shapes agent behaviour and can be edited - a system or
task prompt, a rule file (CLAUDE.md, AGENTS.md, cursor rules), a hook or guard script, a skill, a
subagent definition, a multi-step pipeline, a scheduled loop's config, a tool allow-list, a model or
budget setting.

## The principle (binding)

**No evolution without evidence. No evidence without a source.**

"I think this prompt would be clearer" is not a proposal. "In the last 8 runs the reviewer flagged
14 issues, 9 of which the human dismissed (64% false positive) - source: review comments on runs
41-48" is a proposal.

Four disciplines follow from it and are not negotiable:

1. **Cited evidence** - every data point names where it came from.
2. **One variable at a time** - one proposal changes one thing, and a target has at most one change
   under measurement. Two simultaneous changes make every verdict unattributable.
3. **Pre-registered success criteria** - baseline, gate criteria and N are written *before*
   enactment and frozen at enactment. Criteria edited after the fact are how self-deception works.
4. **Revert on no improvement** - a change that did not measurably help is rolled back by default.
   Every kept change adds surface area; it has to pay rent.

And one more: **the human gates every enactment**. The engine proposes; it never evolves itself
autonomously.

## Setup (first use in a repo)

The helper lives at `scripts/evo.py` inside this skill folder (Python 3, stdlib only). Run it from
the repo root with the path to wherever this skill is installed, e.g.:

```bash
python .claude/skills/evolution-engine/scripts/evo.py init
```

This creates `.evolution/` (ledger, proposals, reviews). The format is documented in
`references/ledger-format.md`. Commit `.evolution/` to version control: the ledger and proposals are
the audit trail of what was tried, and git history is the backstop if a proposal file is edited or
deleted by accident. Do not gitignore it.

If Python is unavailable, keep the same files by hand following `references/ledger-format.md` and
apply every gate below yourself - the rules are the point, the script only makes them hard to skip.

## Phase 1 - Observe

Goal: find out what is actually happening, with numbers, before forming an opinion.

1. **Name the target and its job.** Name the target by its repo path (`CLAUDE.md`,
   `hooks/review.sh`, `.claude/skills/deploy`) so every proposal on it uses the same name. What is it
   supposed to achieve? One sentence. That sentence decides which parameters matter.
2. **Inventory the evidence the repo already has.** Do not invent a logging system first. Look for:
   git history (reverts, "fix" commits, churn on the target file), test and CI results, run logs or
   receipts, hook/guard logs, issue/PR review threads, and agent transcripts if the tool keeps them
   (Claude Code, for example, stores session transcripts as JSONL under `~/.claude/projects/`).
   Details per source: `references/evidence-sources.md`.
3. **Check the ledger** (`evo.py status --target X`): what was already tried on this target, and what
   happened? Never re-propose a reverted change without new evidence that explains why it failed.
4. **Assess the parameters** in `references/parameters.md` (cost, gate friction, human override rate,
   handoff quality, test integrity, faked-completeness, output quality, delegation, context pressure,
   check precision) - as many as the data supports. State N for each. If N is small, say so plainly;
   never inflate confidence.
5. **If the evidence does not exist**, the right proposal is often *start recording it* (e.g. a
   one-line receipt per run), not a behaviour change. A change you cannot measure cannot get a verdict.

## Phase 2 - Propose

Scaffold and fill a proposal:

```bash
python .claude/skills/evolution-engine/scripts/evo.py new --target hooks/review.sh --title "Cap reviewer retries at 2"
```

A proposal (`references/ledger-format.md` has the full template) must contain:

| Part | What it must hold |
|------|-------------------|
| `variable` | The ONE thing that changes |
| `parameters_cited` | Keys from `references/parameters.md`, or `custom:<name>` defined in Evidence |
| `## Evidence` | Bullets, each with a number and a checkable `source:` (path, run id, commit, PR #, date) |
| `## Baseline` | Current value of each cited parameter, with N and the window |
| `## Hypothesis` | The mechanism: why this edit should move that number - and how you confirmed the diagnosis |
| `## Gate Criteria` | `- improved:` / `- no_change:` / `- reverted:` lines, each with a threshold number |
| `min_n` | Runs to measure before a verdict (floor 3; use 5+ for frequently-run or noisy targets) |
| `## Change` | Exact files and edit |
| `## Rollback` | How to undo it |

Then log it: `evo.py propose <file>`. The helper **refuses** a proposal that cites no parameter or an
unknown one, has an evidence bullet without a number or without a checkable source, a baseline
without numbers, a gate line without a threshold, `min_n < 3`, or a `variable` listing several things
- and logs the refusal as `incomplete`, so refusals leave a trace too. These are structural checks:
they stop "source: my gut" and "better / same / worse", but only a reader can tell whether a cited
source really says what the bullet claims. Read the evidence before approving.

Before proposing, run the proposal-quality checks in `references/measurement.md` (confirm the root
cause directly; back-test the gate criteria against the history you already have; make sure the
metric can actually go red).

## Phase 3 - Human gate

Present the proposal to the human: the evidence, the one-line change, the gate criteria, the
rollback. Use the environment's ask-the-user tool if one exists; otherwise ask in chat and **stop** -
do not enact in the same turn you proposed unless the human has explicitly said yes to this proposal.

- Approved -> Phase 4.
- Rejected -> `evo.py reject EVO-007 --by <name> --reason "..."`. Never enacted, still recorded.
- Changes requested -> edit the proposal, run `evo.py propose` on it again (a new `proposed` event
  supersedes the old text), and show the human the new version.

`propose` records a hash of the whole proposal file. `enact` refuses if the file changed since then, so
what gets enacted is exactly what the human approved.

## Phase 4 - Enact

1. Apply exactly the change in `## Change`. Nothing else rides along - no drive-by cleanups in the
   same edit, they are a second variable.
2. If the repo uses git, make it one commit and put the sha in `--ref`, so rollback is one revert.
3. Record it: `evo.py enact EVO-007 --approved-by <name> --ref <sha>`.

Enactment copies the Baseline, Gate Criteria and `min_n` text into the ledger. From then on the
ledger's copy is what the verdict is judged against. The helper refuses to enact while another change
on the same target (compared case- and punctuation-insensitively) is still `pending`.

## Phase 5 - Measure

After each run of the target, record the cited parameters:

```bash
python .claude/skills/evolution-engine/scripts/evo.py measure EVO-007 --run 2026-10-02-a --metric retries=1 --metric cost_usd=0.42
```

Each run id counts once. The helper warns if a metric name appears nowhere in the frozen baseline,
criteria or cited parameters. Measure what the gate criteria name, in the same way the baseline was
measured - a different measuring method is a different variable. Note confounders (model upgrade,
different task mix, other config changes) with `--note`; see `references/measurement.md`.

## Phase 6 - Verdict

When `min_n` runs are in, compare against the frozen gate criteria and close it:

```bash
python .claude/skills/evolution-engine/scripts/evo.py verdict EVO-007 improved --reason "retries 3.1 -> 1.2 avg over 5 runs, cost flat"
```

| Verdict | Meaning | Action |
|---------|---------|--------|
| `pending` | Enacted, still measuring | Keep measuring; no claims yet |
| `improved` | `improved:` criteria met | Keep the change |
| `no_change` | Criteria not met, no regression | **Roll back** by default. `--keep` only with a stated reason (e.g. the change is a pure simplification) |
| `reverted` | Regression per `reverted:` criteria | Roll back immediately; allowed at any N |

The helper does not do the arithmetic. You compare the recorded numbers against the frozen criteria
and quote them in `--reason`. What the helper does enforce:
- `improved` / `no_change` are refused below `min_n`.
- They are also refused if the proposal file no longer matches the frozen criteria, or is missing.
  When that happens it prints the frozen text so you can restore it. The procedure is under
  "Restoring a lost or edited proposal" in `references/ledger-format.md`.
- `reverted` is **always** allowed: at any N, and even if the file was edited or lost. Rolling back is
  never blocked. The verdict is then recorded with `criteria_changed: true`.

When a verdict requires rollback, do it in the same session, then record it with
`evo.py rollback EVO-007 --ref <revert sha>`, or pass `--rollback-ref` to `verdict` if it is already
done. `status` flags `[ROLLBACK DUE]` until then.

## Evolution reviews

A review is a periodic snapshot across targets, written to `.evolution/reviews/review-NNN.md`
(template in `references/ledger-format.md`). Each review: states N and confidence per target; reports
every assessable parameter; separates improved / not improved / not yet measurable; lists pending
evolutions and how many runs each still needs; lists new proposals the data suggests. Changes that
were shipped without going through the cycle are logged retroactively (proposal with the evidence
that existed at the time, then `enact`) so they get measured like everything else.

## Guard rails

- Never propose without at least one cited parameter backed by sourced data.
- Never assert a verdict below the pre-registered N. Never change the criteria after enactment -
  if they were wrong, revert and re-propose.
- Never run two changes on the same target at once; never bundle two edits into one proposal.
- State N and limitations plainly. "3 runs, directionally better, low confidence" is a fine sentence.
- When a component keeps missing its metric after hand-tweaks (say, 3 runs in a row), stop editing it
  in place - set up a proper experiment with rollback rather than a fourth tweak.
- Prose is not enforcement. If the evidence shows an instruction was already being ignored, adding
  more instruction text is a weak hypothesis; consider a deterministic check (hook, test, script).
- Log everything to the ledger, including refused and rejected proposals. The ledger is append-only:
  correct mistakes with a new event, never by rewriting history.
- The engine never edits its own gates (this skill, the helper, the ledger format) as part of an
  evolution it is running.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| "The agent seemed better today" | Anecdote, N=1, no baseline |
| Fixing the symptom named in a plan without checking the diagnosis | A wrong diagnosis ships a harmful "fix" that looks like progress |
| Rewriting the whole prompt at once | Many variables; no verdict can say which part helped |
| Setting criteria after seeing the numbers | Criteria will always be met |
| A metric that has never been seen to fail | It may be unable to detect the problem at all |
| Keeping every no_change "just in case" | Instructions accrete until nothing is followed |
| Measuring only where it is convenient | The failure lands elsewhere and the check certifies it |

## References

- `references/parameters.md` - the ten parameters, how to compute each, custom parameters
- `references/evidence-sources.md` - where evidence lives in an ordinary repo and how to extract it
- `references/measurement.md` - proposal-quality checks, small-N honesty, confounders, worked example
- `references/ledger-format.md` - ledger events, proposal template, review template
