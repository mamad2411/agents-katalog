---
name: qa
description: Run the lifecycle's functional test — the prescribed strategy catalogue. Reads the repository profile and the run record, computes the required strategies from file patterns, lets one advisory judgment widen that set and never narrow it, runs each strategy's driver to passed, failed, or blocked, appends one evidence envelope each to the run record, counts the verdict, publishes the per-strategy statuses, and routes. It never fixes anything. Triggers on "qa", "functional test", "does the shipped thing work", "run the strategies", or the release step's hand-off after a non-production deployment.
---

# QA — the functional test

`/qa` answers **"Does the shipped thing actually work?"** It runs after the release step has
merged the change and deployed it to the non-production destination, and it decides whether what
was shipped works. It reports, it verdicts, and it routes. It does **NOT** fix.

It is the only step in the chain with no prescribed method — which is exactly why its method is
prescribed here, as data, rather than improvised per run.

## What replaced what

This skill used to classify a change into nine risk classes, improvise the checks for each, ask a
language model for a severity per finding, and turn those counts into a number. Every part of that
is gone. In its place:

| Then | Now |
|---|---|
| Nine risk classes, checks improvised per class | Ten prescribed strategies, declared as data in `saga/references/qa-catalogue.yaml` |
| The checks a run performed were whatever it thought of | The strategies come from the repository's profile, matched by file pattern, by code |
| A check that could not run was a "graceful no-op" | A check that cannot run is `blocked`, and a required `blocked` stops the run |
| A model assigned a severity per finding | Nothing assigns a severity; there is no severity |
| A number was computed from those severities | The verdict is counted from three result values |
| `ship` / `ship-with-deferred` / `no-ship` | `pass` / `pass-with-proof-debt` / `fail` |
| Advisory: it never blocked the router | Authoritative: a failure re-enters the build loop |

The verdict words changed because the decision changed. This step runs **after** the deployment,
so it no longer decides whether to ship; it decides whether the shipped thing works.

## Position in the lifecycle

```
build loop  →  code review  →  merge turn  →  release + non-production deploy  →  /qa  →  close
                    ▲                                                              │
                    └──────────────── fail re-enters the build loop ───────────────┘
                                      a required block stops for the operator
```

The Functional Tester is a herdr session created from the roles library. Its prompt names one
command and one issue. It makes **no selection decisions of its own**: the selection is computed.

**This skill is what the board's `Verify` stage holds (W8, SDLC R69/R71).** A card enters `Verify`
only after the change is merged plus a succeeded non-production deployment. For work with no
deployable software, the same merge precondition still applies — the no-deployable route relaxes
the **deployment** requirement, never the **merge** requirement — so the card enters `Verify` only
after the change is merged **and** the delivered artifact exists in its real form and consumption
context (`Deploying to non-production` is applicable-only and never set for it). There is no
pre-merge entry route: PR-ready never moves a card to `Verify`; the single authority for the
condition is the `verify_entry` block of `config/sdlc-schema.json` in `infiquetra-sdlc`. When a
card is in `Verify`, the activity it holds is this functional test.

**Any verify-class role this step runs is sandboxed.** The Functional Tester runs as a roster
session in its own worktree, so it can run a command without its working tree reaching the primary
checkout. `/qa` reads running behaviour and never writes code, and the isolation is what makes that
a property rather than a promise. Where the step must spawn a subagent instead of a pane, it runs
read-only and in a disposable worktree for the same reason.

## Core principles

1. **Reports, never repairs.** `/qa` does **NOT** fix bugs, does **NOT** edit code, does
   **NOT** commit, does **NOT** push, does **NOT** open, update, or merge a PR, does **NOT**
   deploy, and does **NOT** file SDLC issues. Every repair belongs to the build loop. Never
   `git add` anything under `.claude/saga/` — the run record is git-ignored on purpose.
2. **Prescribed, not improvised.** The strategies, their tools, their evidence fields, their proof
   boundaries and their thresholds are catalogue rows. A new strategy is a row plus a driver, not
   a rewrite of this document.
3. **Three results, and there is no fourth.** `passed`, `failed`, `blocked`. A strategy the
   boundary excludes is recorded in the selection as out-of-boundary, never as a result. A silent
   skip has nowhere to hide.
4. **Nothing is scored.** No severity is assigned by anything, and no number is derived from
   counting severities. The verdict is arithmetic over three values.
5. **The judgment may only widen.** The required set is computed first, from the profile's file
   patterns. The advisory typed judgment may add a strategy the patterns under-selected; it may
   never remove one, and it never computes the verdict.
6. **Evidence is declared before it is gathered.** Each strategy's catalogue row names the fields
   its envelope must carry, and every envelope validates against the envelope schema.
7. **Explicit invocation.** `/qa` runs when the chain reaches it or when the operator asks for it
   by name. It is never launched implicitly from inside another skill's phase.

## The one command

Everything below is done by one runnable command. Read its output; do not reproduce its logic by
hand.

```bash
# Print what would run and why, with one reason per entry. Runs no driver.
uv run python plugins/saga/scripts/qa_strategies.py select --issue <N>

# The whole procedure: select, preflight, dispatch, count, record.
uv run python plugins/saga/scripts/qa_strategies.py run --issue <N>

# The same runner at the build loop's narrower boundary (issue 1027's scenario smoke).
uv run python plugins/saga/scripts/qa_strategies.py run --issue <N> --boundary branch-preview

# Recompute the verdict from what the record already holds, changing nothing.
uv run python plugins/saga/scripts/qa_strategies.py verdict --issue <N>
```

Exit codes, which are the routing decision in numeric form:

| Code | Meaning | Where the run goes |
|---|---|---|
| 0 | `pass` or `pass-with-proof-debt` | close |
| 1 | an internal error | the operator |
| 2 | a refusal: no profile, a profile that proves nothing, or a preflight refusal | the operator |
| 3 | an unknown run-record version | the operator |
| 4 | `fail` | the build loop |
| 5 | a required strategy is `blocked` | the operator |

4 and 5 are separate because they route to different places. A failure is something the build loop
can repair. A block is an environment, a credential or a permission, and no build loop repairs one.

## The procedure, step by step

1. **The release step records the deployment** in the run record: the destination, the base URL,
   the deployed revision and the version marker. `/qa` reads that identity; it never invents one.
2. **Code computes the required strategies** from the profile's file patterns against the change's
   file list, then filters by the proof boundary this run can reach.
3. **The advisory judgment is asked, and its answer is unioned with the floor.** Its absence, its
   timeout and its error all degrade to the declared set. No run fails because it was unavailable.
4. **Code preflights** the environments, the secret handles, the estimated duration and the
   estimated cost. Over the profile's ceiling, or missing a credential, the **whole** selection is
   refused. The affordable subset is never run on its own and reported as a partial pass.
5. **Each selected strategy's driver runs** and appends exactly one evidence envelope. Secrets are
   redacted inside the driver, before the envelope exists.
6. **Code counts the verdict and writes it** to the run record under the top-level `qa` key.
7. **Publish one comment** carrying the selection, the per-strategy statuses and the artifact
   pointers, so the operator can see which checks ran and which did not:

   ```bash
   uv run python plugins/saga/scripts/qa_strategies.py run --issue <N> > /tmp/qa-<N>.md
   gh issue comment <N> --repo <owner/repo> --body-file /tmp/qa-<N>.md
   ```

8. **Route by the exit code**, per the table above.

## The status card

The operator-facing card for this surface is rendered by the single emitter,
`saga/scripts/status_card.py`, through its `project_qa` projection — never hand-drawn here. It
reads the frontmatter and the results table of the comment the runner prints, and renders five
rows: Selection · Preflight · Evidence · Proof debt · Verdict.

Two of those rows are the reason the card is worth having. **Evidence** follows the per-strategy
results rather than the verdict word, so a run whose strategies could not run never renders as a
finished one. **Proof debt** stays visible on a passing run, because a debt that rendered as done
would be a hidden skip in a new place.

## The catalogue

Ten strategies. Their situations, tools, evidence fields, boundaries and thresholds live in
`references/qa-catalogue-reference.md`, and the data itself in
`saga/references/qa-catalogue.yaml`.

| Strategy | The situation that selects it |
|---|---|
| `api-workflow` | a change to a deployed HTTP surface, handler, route, or authorization rule |
| `contract-check` | a change to an OpenAPI document, event schema, generated client, or pinned contract |
| `app-ui` | a change to application widget or screen behaviour |
| `hosted-surface` | a change touching a non-application hosted page |
| `cli-smoke` | a change to a command-line entry point, console script, or plugin script |
| `deploy-boundary` | any change that reaches a deployed environment |
| `data-check` | a change to a schema, migration, write path, or idempotency key |
| `infrastructure-read-back` | a change to infrastructure roles, cluster or network configuration |
| `installed-surface` | a change to a Claude plugin's skills, commands, agents, or metadata |
| `manual-runbook` | automation is unavailable, unsafe, or needs operator-held credentials |

Five ship with drivers in the first release: `cli-smoke`, `contract-check`, `deploy-boundary`,
`installed-surface`, and `api-workflow` by delegation to the executor the profile declares. The
other five are declared and ship no driver; selecting one yields `blocked` carrying the reason the
catalogue row states and the condition that reopens it. That is deliberate and it is honest: an
unexercised driver is the "graceful no-op" this redesign exists to remove, wearing a new name.

## The repository profile

Each repository declares its own strategies in the optional `qa` block of the tracked
`.saga-profile.json` at its root. `references/qa-evidence-and-verdict.md` carries the field list;
`saga/references/qa-profile.schema.json` is the shape.

Two refusals, both deliberate:

- **A repository with no `qa` block is `blocked`,** naming the file and the missing key. It is
  never an empty selection that reports a pass.
- **A profile whose strategies are all optional is `blocked`.** Such a profile would let a run
  report a pass having proved nothing, which is the failure this design exists to remove.

The Planner writes a new scenario into the profile at plan time. `/qa` never writes its own
scenarios: a functional test that authored its own scenarios would be grading its own homework.

## The verdict

| Verdict | When |
|---|---|
| `pass` | every required strategy returned `passed` |
| `pass-with-proof-debt` | every required strategy returned `passed`, and at least one optional strategy returned `blocked`; the debt, its reason and its revisit condition are recorded |
| `fail` | anything else |

## Where the judgment helps, and where it would mislead

One advisory judgment ships: strategy widening. Its act band is a declared number in the catalogue
file, not a literal in code and not a value an implementer chose — the evaluation harness sets the
operating band from recorded real uses. Every call is logged with its probability and any override.

The judgment must never: compare timestamps or freshness windows; count findings, failures or
coverage; decide whether a threshold is met; screen driver output for adversarial content; or read
live external state. Each of those is a documented weakness of the model, and each of those jobs
belongs to code here.

Three further judgments — target variant, scenario ranking, failure triage — ship only after the
evaluation harness has recorded agreement for the widening judgment at the chosen band.

## What this skill does not do

`/qa` does **NOT** fix bugs, does **NOT** edit code, does **NOT** commit, does **NOT** push, does
**NOT** open, update, or merge a PR, does **NOT** deploy, does **NOT** file SDLC issues, and does
**NOT** set readiness labels. It reports, verdicts, and routes — then stops.

Outbound routing is the chain's. The next step is the one the section below names, read from the
run record; issue 1030 removed the `/loop` router and its dispatch table, so there is no separate
map to consult.

## The step this continues into

On a `pass`, the run advances to close and this step continues into `/retro`, which turns the
finished work into durable journal knowledge. That is a step this skill takes, not a suggestion it
hands over: the chain runs automatically once admission has answered its questions, and a step that
stopped to ask which command comes next would be the hand-written coordinator the chain replaced.

On a `fail` the continuation is the build loop, and on a required `blocked` it is the operator.
Those three are the whole set, and the exit code says which one applies.

## References

- `references/qa-catalogue-reference.md` — the ten strategies with their situation, tool, proof
  boundary, required evidence and threshold.
- `references/qa-evidence-and-verdict.md` — the evidence envelope, the repository profile's field
  list, the verdict arithmetic and the routing table.
- `saga/references/qa-catalogue.yaml`, `saga/references/qa-profile.schema.json`,
  `saga/references/qa-envelope.schema.json` — the data and the two shapes.
- `saga/references/run-record.md` — where the evidence and the verdict are written.
