---
name: rpi-workflow
description: Run the research/plan/implement example against a live Copilot agent, answer the questions it asks, open the portal, and read what it built
---

# Run the research/plan/implement example

Drives the `examples/rpi-workflow` workflow end to end: start the run, watch the
research agent ask the user what they actually want, answer it, and carry the
run through planning and implementation until a tic-tac-toe game exists in
`workspace/`.

This spends the user's AI credits. Never start, advance, or answer without the
user having asked for it in this conversation.

## Prerequisites

Check these before doing anything else. Report a failure and stop rather than
working around it.

| Requirement | Check | If missing |
| --- | --- | --- |
| Copilot login | `copilot --version` runs, and the user says they have logged in | Tell the user to run `copilot login`. Never run it for them |
| Built senawa | `test -f apps/senawa/dist/main.js` (from repo root) | Run `pnpm build` from the repo root |
| Valid workflow | `make check` | Read the diagnostics and fix `.senawa/`, do not start the run |
| Node 22 | `node --version` | Stop; the workflow targets Node 22 |

There is no offline way to prove the login works. A missing or expired one
surfaces at the first agent dispatch, in `.senawa-state/senawa/service.log`.

Run every command from the example directory unless stated otherwise:

```bash
cd examples/rpi-workflow
```

## The mental model

Three things are separate and it matters:

* The **workflow** in `.senawa/` is authored text. Compiling it costs nothing.
* The **run** is durable state under `.senawa-state/`. `senawa start` creates it
  and exits.
* The **service** is the supervisor process that actually runs agents.
  `senawa service start` starts it.

`make run` does all three in the right order. Everything after that is a loop of
*look at what the run needs, give it that, advance*.

## Quick start

```bash
make check                  # compiles the workflow, costs nothing
make run                    # writes the request, creates the run, starts the service
```

`make run` prints the run and repository ids. Capture them; every later command
needs both:

```
run: run_3ecb3d1cd61810fecd9457a230b49009
repository: repository_rpi-workflow
```

Export them so the rest of the session is short:

```bash
export RUN=run_3ecb3d1cd61810fecd9457a230b49009
export REPO=repository_rpi-workflow
```

## The driving loop

Repeat until the run says every phase is done.

### 1. Ask what the run needs

```bash
make status REPO=$REPO RUN=$RUN
```

Read `waiting on you`. The listed needs are in the order they arose, and
`make answer` answers the first one.

### 2. Give it what it needs

| What status shows | What to do |
| --- | --- |
| `question: ...` | Put the question to the user, then `make answer REPO=$REPO RUN=$RUN TEXT="their answer"` |
| `approval: ...` | Put it to the user, then `make approve REPO=$REPO RUN=$RUN` |
| `escalation: Budget allowance ...` | The phase ran out of attempts. See Troubleshooting |
| `waiting on you: 0` | Nothing is needed; go to step 3 |

Never invent an answer to a question meant for a person. The whole point of this
example is that the run stops for a human decision. Put the agent's question to
the user verbatim, wait, and pass their words through unchanged.

### 3. Advance

```bash
make advance REPO=$REPO RUN=$RUN
```

One call takes as many steps as it can and stops when it needs an agent or a
person. What it prints:

| Output | Meaning |
| --- | --- |
| `dispatched <phase> as dispatch_...` | An agent is now working. Wait, then check status |
| `waiting for the agent working on <phase>` | The agent is mid-turn. Wait, then check status |
| `closed <phase>` | That phase passed its gate and is done |
| `fanned <phase> out over N items` | The plan became N members, each with its own agent |
| `<phase> did not pass: ...` | A gate refused it. Read the reasons |
| `every phase is done` | Finished |

### 4. Wait for the agent

A live agent turn takes roughly a minute. Sleep about 75 seconds before checking
status again. Do not poll in a tight loop; each check is cheap but each agent
turn is not.

## Launching the portal

```bash
make portal
```

This prints a single-use URL. Tell the user to open it themselves and hand them
the URL; do not open it for them.

Facts the user needs to know about that URL:

* It works once and expires in 60 seconds. Run `make portal` again for another.
* It grants a read-write session for up to eight hours.
* A second tab is read-only, because only one session may act at a time.
* The port is chosen at random each time the service starts.

What the user can do there that the command line cannot:

* **Agents** view: who is working, on what, and on which model.
* **Questions** view: answer a specific question rather than the oldest one.
* **Allowances**: grant a phase more attempts when it escalates.
* Steer or override an agent from a dialog rather than by typing a command.

If `make portal` fails, the service is not running. Run `make service`.

## Reading what was built

```bash
make game                                    # lists the files the agents wrote
node scripts/check.mjs                       # the same check the gate runs
make agents REPO=$REPO RUN=$RUN              # the dispatches and their contexts
```

There is no make target for the published outputs. `senawa` is not on the path;
the Makefile runs the build in this repository, so call it the same way:

```bash
SENAWA="node ../../apps/senawa/dist/main.js"
XDG_STATE_HOME=$PWD/.senawa-state $SENAWA artifact list $REPO $RUN
```

Everything the agents wrote is under `workspace/`. They cannot write anywhere
else.

## What the workflow does

```
research ── asks the user what they actually want, records the answers
    │        no gate: its schema is what constrains it
   plan ── turns the request and the research into three to five tasks
    │        reads `request` from the run's input and `research` from upstream
implement ── one agent per planned task, each gated on `node scripts/check.mjs`
             onFailure: continue, so one failing member does not stop the rest
```

The research schema requires a non-empty `decisions` array, so the phase cannot
close without the agent having recorded what it asked and what it was told.

## How a question actually flows

Understanding this prevents most confusion:

1. The agent calls senawa rather than writing the question into its reply.
2. The question becomes durable and the run stops. Nothing else is dispatched.
3. Someone answers, in the portal or with `make answer`. The answer is bound to
   the exact question.
4. `make advance` dispatches the phase **again**, carrying the question and the
   answer in the person's own words.
5. The agent reads them and carries on.

The answer arrives on a new attempt, because the turn that asked must not be able
to hand work in afterwards. **Each question therefore spends an attempt**, which
is why this workflow authors `attempts: 8` rather than the default three.

## Stopping and cleaning up

```bash
make stop     # drains and stops the service, keeps the run
make clean    # stops, then deletes .senawa-state/, workspace/, and request.json
```

`make clean` never touches `.senawa/`. Starting over always means `make clean`
followed by `make run`, because a run id is derived and a second `start` against
existing state is refused.

## Troubleshooting

| Symptom | Cause | Fix |
| --- | --- | --- |
| `Run instantiation was refused` | A run already exists in this state | `make clean` then `make run` |
| `Supervisor socket already has a live singleton lock` | A previous service is still up | `make stop`, then retry |
| `Supervisor did not become ready` | Cold start is slow, or it refused | `tail .senawa-state/senawa/service.log` |
| `Operational command failed` with no detail | Message withheld because it may name a path | Re-run with `SENAWA_DEBUG=1` |
| `escalation: Budget allowance requested` | The phase used every attempt | Grant it in the portal, or `make clean` and raise `attempts` in `.senawa/workflow.yaml` |
| `FOREIGN KEY constraint failed` on advance | senawa was rebuilt mid-run, so the compiled workflow no longer matches | `make clean` then `make run` |
| `mapped phase input does not satisfy schema` | A phase's declared input names a property no source provides | Fix the schema in `.senawa/schemas/`, then `make clean` |
| Agent asks how to use senawa | It should ask senawa, not a person | Answer briefly and let it continue; it costs an attempt |
| Nothing happens after `make answer` | The service has not been told | `make advance`, which wakes it |

## Rules for the agent running this skill

1. Confirm before spending. `make run`, `make advance`, and `make answer` all
   cost credits. `make check`, `make status`, `make agents`, and `make game` do
   not.
2. Never answer a worker's question on the user's behalf. Relay it and wait.
3. Never run `copilot login`; ask the user to.
4. Never open the portal URL; hand it over.
5. Report the run and repository ids once and reuse them; do not re-derive them.
6. When a gate refuses, read the reasons before doing anything. The agent gets
   them on its next attempt, so usually the right action is to advance again.
7. Do not edit `workspace/`. It is the agents' output and editing it makes the
   gate readings meaningless.

## Making this skill discoverable

VS Code loads skills from `.github/skills/` at the workspace root. This one lives
with the example so it travels with it. To use it from the repository root:

```bash
mkdir -p .github/skills
ln -s ../../examples/rpi-workflow/.github/skills/rpi-workflow .github/skills/rpi-workflow
```

## Reference

* [The example README](../../../README.md) covers the same ground for a person
  rather than an agent.
* `make help` lists every target with a one-line description.
