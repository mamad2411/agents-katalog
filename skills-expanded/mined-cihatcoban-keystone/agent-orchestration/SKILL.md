---
name: agent-orchestration
description: Coordinates several agents on one task - splitting work, parallel subagents, fresh-context verification, loop specs and stop conditions. Triggers - use subagents, run this in parallel, split this across agents, agent keeps retrying, design an agent loop, run this unattended, verify with a fresh agent.
---

# Agent Orchestration

One agent is the default. More agents pay off for **independent** parts, a
**broad search** whose details nobody needs to keep, and **verification by an
agent that has not seen the work**. Elsewhere coordination costs more than it
saves: every subagent starts cold and re-derives what the parent knew.

## When to split

| Situation | Split? | Shape |
|---|---|---|
| Independent changes in separate areas (three services, five docs) | Yes | One agent per area, in parallel |
| A wide search: "where is X used", "which modules do Y" | Yes | A subagent returns the conclusion, not its reads |
| Review, adversarial check, security audit of finished work | Yes | A fresh agent with the diff and the spec only |
| One feature across tightly coupled files | No | One agent, sequential slices (`incremental-delivery`) |
| Debugging an unexplained failure | No | One agent holding the whole picture (`debugging-and-root-cause`) |
| The task is small | No | Coordination overhead exceeds the work |

The test: can two agents work without reading each other's output? If not,
it is one task.

## Splitting work

1. **Contracts first.** Fix any shared interface (types, schema, API) before
   fanning out (`api-and-contract-design`); agents negotiating one through code
   produce two.
2. **One owner per file, one worktree per writer.** Assign files or
   directories, never overlap. Each writing agent gets its own git worktree
   and branch, so a failed part is discarded without touching the rest; the
   parent merges.
3. **Self-contained briefs.** Each brief carries the goal, the files it owns,
   the contract it must honor, the constraints (`CONSTRAINTS.md`), and what to
   return. A subagent cannot ask the parent's context what was meant.
4. **A defined return shape.** Ask for a summary, the files changed, the
   commands run with their result, and open questions — not a narrative.
5. **Model per role.** A cheaper model for searches and mechanical edits; the
   strongest for design, debugging and review.

## Verification by fresh context

An agent grading its own work finds what it expected to find. Keystone's
reviewers exist for this:

| Check | Agent |
|---|---|
| Is this plan or conclusion wrong? | `adversarial-reviewer` |
| Is this change ready to merge? | `code-reviewer` |
| Does it hide failures? | `silent-failure-hunter` |
| Is it secure? | `security-auditor` |
| Are the tests meaningful? | `test-engineer` |

Give the reviewer the spec, the diff and the bar — not the author's reasoning,
which would anchor it. The parent acts on findings; the reviewer does not fix.

## Loops: write the spec before the first iteration

Fix-until-green, generate-then-critique, a nightly run: each is a loop, and a
loop without a written spec runs until the budget runs out. Fill this in first:

| Field | Must be | Bad example |
|---|---|---|
| Goal | One sentence, the end state | "improve the code" |
| Done signal | A check that runs **outside** the working agent and exits pass/fail | "the agent says it is done" |
| Progress metric | A number that must move each iteration: failing tests, open findings, rubric score | lines changed |
| Budget | Max iterations, wall time and tokens — all three | "until it works" |
| State file | Where progress is written after every iteration, so a restart resumes instead of repeating | the conversation |
| Escalation | Who is told, with what, when the loop stops without the done signal | silent exit |
| Kill switch | How a person stops it mid-run without corrupting state | killing the process |

## Loop shapes

| Shape | Use when | Done signal | Typical stop |
|---|---|---|---|
| Fix-until-green | A known check is red | The check passes | Same failure twice |
| Plan–execute–verify | A multi-step task with a plan | Every plan step has passing evidence | A step fails verification twice |
| Generator–evaluator | Quality is judged, not computed (docs, designs, prompts) | Rubric score ≥ the bar set **before** generating | Score flat for 2 rounds; 3–5 rounds max |
| Fan-out / fan-in | Independent parts | Every part returned and the merged result passes `/verify` | One part fails twice → report it, merge the rest |
| Panel | One artifact, several reviewer lenses | Each lens returned findings or "nothing found, checked X" | Lenses disagree → a human, never a vote |
| Unattended / scheduled | Recurring work nobody watches | The run's report is written | Budget hit, irreversible step reached, or kill switch |

Per-shape structure, the state-file format, and a review checklist for an
existing loop: `references/agent-loop-patterns.md`.

## Stop conditions

Loops are the expensive failure: an agent retrying the same fix, or two agents
handing a task back and forth. Set the limits before starting:

- **Same failure twice → change approach.** A third identical attempt is not
  persistence; escalate with what was tried.
- **No measurable progress in N iterations → stop.** Progress means a check
  turned green, a test count rose, a finding closed — not more text. Default N
  is 2.
- **Oscillation → stop.** State A, then B, then A again (a fix reverted by the
  next fix) means two constraints conflict; a third pass will not resolve it.
  Compare each iteration's state against all earlier ones, not only the last.
- **Budget.** Ceilings on iterations, wall time and tokens per agent; hitting
  any one ends the run with a report, never a silent continuation.
- **Irreversible step → stop and ask**, even unattended (`CLAUDE.md` §1.3). A
  loop that can reach a destructive action without a pause is mis-specified.
- **Disagreement between agents → a human.** Do not let a third agent break the
  tie by majority.

The worker must not be able to edit its done signal. A generator that can
change the rubric, or a fixer that can edit the test it is fixing, reaches
"done" by moving the target; `CLAUDE.md` §4 applies to every iteration.

`build-error-resolver` applies these limits to red builds and reports what
remains instead of disabling a check.

## Merging results

The parent integrates, and owns the outcome:

1. Read every return; contradictions between them are findings.
2. Run `/verify` on the combined result — parts that passed alone can fail
   together.
3. Report which agent did what, what was verified, and what was not.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Two agents changed the same file | Ownership not assigned | Partition by path before starting |
| Subagent solved a different problem | Brief relied on the parent's context | Self-contained brief with goal and constraints |
| Results look fine, combined build fails | Integration never verified | `/verify` after merging, every time |
| Cost far above estimate | Agents re-reading the same files, retry loops | Shared conclusions in files; stop conditions |
| Reviewer approves everything | It saw the author's reasoning | Give it only spec, diff and bar |
| Loop reaches "done" fast after a test or rubric changed | The worker moved the target | Done signal outside the worker's write access; diff scan each iteration |
| Fix, revert, same fix again | Two constraints conflict | Oscillation stop; escalate both constraints |
| Restarted run redoes finished work | Progress lived only in the conversation | State file written after every iteration; resume reads it first |
| Unattended run burned the budget overnight | No ceiling on one of iterations, time or tokens | All three ceilings in the loop spec |

## Exit checklist

- [ ] Split only for independent parts, broad searches, or fresh-context review
- [ ] Interfaces fixed before fan-out; each file has exactly one owner
- [ ] Every brief self-contained, with a defined return shape
- [ ] Every loop has a written spec: done signal outside the worker, progress
      metric, three-part budget, state file, escalation, kill switch
- [ ] Stop conditions and budget set before starting; oscillation checked
      against all earlier states
- [ ] Work verified by an agent that did not produce it
- [ ] Combined result passed `/verify`; who did what is reported
