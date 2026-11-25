---
name: gauntlet
version: 1.0.0
description: |
  The Gauntlet Loop. Forge the bar FIRST, then build against it under adversarial
  critique until every piece either beats the bar or provably stops improving.
  Sealed BAR.md (sha256-verified, never edited in flight), independent builder and
  critic subagents with fresh context, critics inspecting the REAL artifact (rendered
  pixels, running code, test output) and never a builder's summary, per-round LEDGER.md
  with convergence detection, and a tend pass that makes separately improved parts one
  coherent thing. Runs end to end with no mid-run questions and no status pings: Eddie
  sees the finished artifact and a report, nothing else. Use when: "gauntlet",
  "run the gauntlet", "beat the bar", "forge the bar", "adversarial build loop",
  "build until it wins", "make this best-in-class".
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
  - Agent
  - Workflow
  - Skill
slug: gauntlet
category: operations
complexity: complex
author: "id8Labs"
triggers:
  - "gauntlet"
  - "run the gauntlet"
  - "beat the bar"
tags:
  - orchestration
  - quality
  - adversarial
---

# Gauntlet Loop


## Core Workflows

### Workflow 1: Primary Action
1. Analyze the input and context
2. Validate prerequisites are met
3. Execute the core operation
4. Verify the output meets expectations
5. Report results

An agentic harness protocol, not a chat pattern. You forge a concrete standard of
winning BEFORE building anything, then run builders and blind critics against it until
every piece clears the bar or provably converges.

The core discipline: **the bar comes first and never moves.** A bar written after the
build is a rationalization of what you happened to produce. A bar edited mid-run is the
same thing with extra steps.

## Arguments

`$ARGUMENTS` is the GOAL: one line, the destination, not the route.

Flags:

- `--bar <path>` -- use an existing artifact as the bar instead of forging one
- `--pieces N` -- override the decomposition count (default: your call, 3 to 5)
- `--max-rounds N` -- rounds per piece before forced stop (default 3)
- `--workdir <path>` -- where BAR.md / LEDGER.md live (default `.gauntlet/<goal-slug>/`)
- `--resume` -- continue an existing run from its LEDGER
- `--no-workflow` -- use direct Agent fan-out instead of the Workflow engine
- `--dry-run` -- print the forged bar and the decomposition, build nothing

## Step 0: Refuse to start blind (HARD STOP)

If `$ARGUMENTS` is empty, is still the template placeholder
(`<one line. the destination, not the route.>`), or names no inspectable destination,
**halt before FORK**. Say so in one line and ask for the goal. Do not guess a target,
do not offer a menu of candidate projects, do not build a partial run "to show shape."

Everything downstream is forged from the goal. A sealed bar built against a guessed
destination is worse than no run: the loop cannot correct it, because the loop is
forbidden from editing the bar.

This is the only question you may ask. After it is answered, run to completion.

## Step 1: FORK -- forge the bar

Before building anything, produce the bar: a concrete, inspectable artifact that
represents winning. Not a description of winning. Something that can be opened, run,
measured, or looked at.

Acceptable bars, in order of preference:

1. A real competitor's shipped output (page, deck, binary, dataset, screenshot)
2. A reference implementation you can execute
3. A test suite that passes on the reference and fails on nothing else
4. A hard numeric target with a stated measurement method (p95 latency, token cost,
   error rate, word count, frame time)
5. A rendered visual reference for blind A/B comparison

Write `BAR.md` to the workdir using `BAR-TEMPLATE.md` in this skill directory. It must
contain, at minimum: what winning looks like, how a critic verifies it (the exact
command, URL, or comparison), and the pass threshold per criterion.

**Seal it.** After writing:

```bash
shasum -a 256 "$WORKDIR/BAR.md" | awk '{print $1}' > "$WORKDIR/.bar.seal"
chmod 444 "$WORKDIR/BAR.md"
```

Seal rules, enforced by you and not by trust:

- Re-verify the sha256 against `.bar.seal` at the start of every wave. Mismatch is a
  HALT, not a warning. Report it to Eddie with the diff.
- No builder, critic, or tend agent may soften, reinterpret, expand, or edit the bar.
  Agent prompts say this explicitly and pass BAR.md as a read-only path.
- If a critic argues the bar itself is wrong or unreachable, **stop the run and surface
  it.** Do not adjust the bar in flight. A wrong bar is Eddie's call, not yours.

## Step 2: SPLIT

Decompose the goal into the smallest pieces that can be built AND judged independently.
Default 3 to 5 pieces. Each piece needs:

- a one-line contract (what it must do)
- the specific BAR.md criteria it is judged against
- the concrete artifact path a critic will inspect

You decide the decomposition. Do not report it for approval. Write it into the LEDGER
header so it is inspectable after the fact.

## Step 3: FAN

Per piece, per round: **one builder subagent, one critic subagent, fresh context each.**

Builder prompt gets: the piece contract, the artifact path, the read-only BAR.md path,
and the single named gap from the previous round (round 1: none). Nothing else. No prior
builder transcripts.

Critic prompt gets: the artifact path, the read-only BAR.md path, and the piece
contract. **Never the builder's reasoning, history, or self-report.** The critic must
not be told what the builder claims it did.

## Step 4: STRIKE

Critics inspect the real artifact, never a summary:

- Visual work: render it and look. Screenshot via `browse`, `claude-in-chrome`, or
  `omni-vu`. Where the bar is a visual reference, do a blind A/B: present both images
  unlabeled and pick the winner before revealing which is ours.
- Code: run it. Execute the test suite, hit the endpoint, measure the number.
- Prose: read the rendered output, apply the bar's rubric verbatim.

Critic returns exactly: `verdict` (BEATS_BAR | TIES | LOSES), `score` 0-10, `evidence`
(the command output, screenshot path, or measurement that grounds the verdict), and
**one** `gap` -- the single largest remaining distance to the bar. Not a list. One.

A verdict without evidence is void. Re-run the critic.

If ours loses, the named gap becomes the next round's builder input.

## Step 5: TRACE

Append every round to `LEDGER.md` (see `LEDGER-TEMPLATE.md`): piece, round, verdict,
score, gap named, delta since last round, evidence path.

Convergence rule: when a piece's improvement is flat across **three consecutive rounds**
(score delta below 0.5 each round, or the critic names the same gap three times), stop
that loop and mark the piece `converged`. Converged is an honest outcome, not a failure.
Record why it stalled.

Also stop a piece at `--max-rounds` and mark it `capped`. Never silently truncate: a
capped piece is reported as capped in the final report.

## Step 6: TEND

After each wave (all pieces advanced one round), spawn **one fresh agent** to inspect
the complete artifact end to end and smooth it into a single coherent thing.

Its mandate is resolving conflicts between separately improved parts: duplicated logic,
clashing visual language, contradictory copy, seams where two builders met. It is
explicitly **not** a redesign, and it may not lower a piece that already beats the bar.
Log its diff as a TEND row in the ledger.

## Step 7: GATE

- **G1 (yours):** every piece either beats the bar or is marked converged/capped. You
  verify this yourself against the ledger. Do not present a run that has not cleared G1.
- **G2 (Eddie's):** he sees the finished artifact and a report. Only that.

## Run discipline

- **No questions mid-run.** The only permitted question is Step 0.
- **No status updates.** Deliver a report, not a progress note.
- Maintain `progress.html` in the workdir, regenerated each wave, for optional viewing
  only. It is never a request for input. Follow the id8Labs design language, no emojis.
- The final report leads BLUF: did it beat the bar, where it converged short, what the
  single remaining gap is per unconverged piece, and the path to the artifact.

## Halt conditions (surface, never improvise)

Stop the run and report when:

1. The bar seal fails, or an agent proposes editing the bar.
2. The bar is proven wrong or unreachable.
3. The same piece fails twice on the same gap with the same approach. Escalate one model
   tier per the Model Cascade, then take it yourself. Two failures is a signal, not a
   reason for a third identical attempt.
4. Work drifts outside the goal line. The goal is the scope.
5. Anything lands in Eddie's lane: titles that become identity, public positioning,
   named relationships, money, or shipping.

**Never auto-commit or push.** The human gate on shipping always stays.

## Execution engine

Default to the `Workflow` tool. This skill is explicit opt-in for multi-agent
orchestration, so calling Workflow from here is authorized.

Shape: `pipeline()` over pieces, so a fast piece reaches its critic while a slow piece is
still building. Barrier only at TEND, which genuinely needs the whole artifact.

```
phase('Fork') -> forge + seal bar (main loop, not delegated)
phase('Wave N'):
  pipeline(pieces,
    piece  => agent(builderPrompt(piece, lastGap), {phase: 'Build'}),
    (_, p) => agent(criticPrompt(p), {phase: 'Strike', schema: VERDICT}))
  agent(tendPrompt, {phase: 'Tend'})   // barrier, one per wave
```

With `--no-workflow`, run the same shape with parallel `Agent` calls in a single message
per stage.

**Cost:** worst case is roughly `pieces x rounds x 2 + rounds` agents. At the defaults
(4 pieces, 3 rounds) that is about 27 agents. If you exceed 5 pieces or 5 rounds, say
the projected agent count in the final report. Honor the session's workflow-size
guideline; if the run needs more, note the cap you applied rather than blowing past it.

## What this is NOT

Not `/polish` (code quality), not `/verify` or `/qa` (correctness), not `/assay` (is it
worth existing). Those ask *is it right?* The gauntlet asks *is it better than the thing
we agreed was winning?* It is the only loop here that requires an external standard to
exist before the first line of work.
