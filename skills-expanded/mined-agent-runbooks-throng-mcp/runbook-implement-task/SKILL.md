---
name: runbook-implement-task
description: One coding task end to end in a repository. A coder, the project's checks, two independent reviews by different models, triage, fix rounds with verification, a polish pass, with subagents through throng-mcp. Takes a task brief; a project profile sets the rest. Leaves the changes uncommitted.
---

# Implement task

Leaves one task implemented in a repository, uncommitted, with the checks green and every review finding triage marked to fix either fixed with evidence or listed for the human. Commit, PR and CI happen outside.

`flow.py` runs two steps itself, preflight and checks, as code steps. Every other step runs as a thronglet, so the session needs the [throng-mcp](https://github.com/agent-runbooks/throng-mcp) MCP server: `run_thronglet`, `wait_thronglet`, `send_message`, `cancel_thronglet`. If your session has a skill for throng-mcp, load it before `start`. How the Execution rules below map onto throng-mcp:

- throng-mcp does not wake a session up, so the second branch of Waiting applies, and this is how its foreground launch is done: `run_thronglet` with `background: true` for every step `flow.py` lists together, in one turn, with `timeout_s` left at its default, then, in the same turn, a `wait_thronglet` call of its own for each, `timeout_s` 86400, called again when it returns the session's state instead of a result. Record each result with its `reply` command as its call returns. What the `flow.py` commands of one turn print, launches and corrections alike, goes out together once that turn's waits have returned, followed by a wait for each.
- `run_thronglet` takes `agent` from the line of the message the executor's description names, `cwd` from the `repo` line, `prompt` the message, `description` the step's address, and `schema` the JSON object in the `reply schema` file, which you read for it. The step's message is the result's `structured` value, or its `text`.
- A correction, and a brief change, go to the step's session through `send_message`. A correction takes `background: true` and the same `schema` as the launch, and is collected with `wait_thronglet` like a launch. If `send_message` refuses the session, your tool cannot send it a message: run the command `flow.py` printed for that case.
- `run_thronglet` or `wait_thronglet` returns an error in place of a result, such as an agent that cannot run here or a crashed process: the step has ended with no reply and nothing to correct. This is not a running step whose executor is gone, so `interrupted` does not apply; that is for a thronglet launched in an earlier session. If the thronglet may still run, as after an error from `wait_thronglet`, stop it with `cancel_thronglet`. Run `flow.py <run> log '<the step's address>: <the error, in one line>'`, the only record of the cause, then the step's `reply` command with `{}`, then at once the command that `reply` prints for a subagent that cannot be sent a message; do not send the correction it prints. What this last command prints joins the rest of the turn's output, as the first item says.
- You launch every thronglet yourself, so no executor relays another agent's reply.

## Inputs

- `brief`: the task brief as text: the task alone, as the human states it. The request to run this runbook and the inputs named in it, such as the checks, go to `start`, not into the brief; a ticket key goes to both. The orchestrator saves it to `<run>/brief.md` and passes `"brief": "brief.md"` to `start`
- `repo`: absolute path of the repository with the task's branch checked out, the directory this session started in unless the human names another
- `profile`: the project's profile, `<repo>/.agent-runbooks/implement-task.md`. The orchestrator reads it before `start` for the inputs below, copies it to `<run>/profile.md` right after `start`, an empty file when the repository has none, and passes `"profile": "profile.md"`. Reading it is part of starting. Three of its sections go to `start` as inputs: the line `command: <shell command>` of its Checks section as `checks`, the line `status: <shell command>` of its VCS section as `statusCommand`, and its Executors section, lines `- <executor>: <agent>`, as inputs under those names. A section without its line gives no input. The rest of it is for the executors. [`README.md`](README.md) next to this file describes the sections
- `checks`: the shell command that checks the project, run from `repo`; exit code 0 means the checks pass. E.g. `python3 -m unittest` or `pnpm check`. Prefer a command that runs every check and fails if any failed, so that the one fix attempt sees every failure: `a && b` stops at the first. The human's words, else the profile's Checks section. Ask the human when neither gives one
- `statusCommand`: the shell command that lists the uncommitted files, run from `repo`, one per line and nothing when the tree is clean. Default `git status --porcelain -- .`; the profile's VCS section replaces it for another VCS
- `task`: a ticket key or short id, used as given in the run directory's name. Optional
- `scope`: a directory the changes stay in, relative to `repo`, such as `packages/grid` in a monorepo. Optional, empty means the whole repository
- `maxFixRounds`: positive integer, default 2. One round is one pass of fix and verify
- `top`, `strong`, `second`: the agent of each executor as throng-mcp names it, `<harness>/<model>[:<effort>]`. The defaults are in the Models table of `README.md`, the profile's Executors section replaces them for the project, the human's words replace both for one run
- `run-id`: given only to resume an interrupted run
- Smoke input, in a repository with green checks and a profile whose Checks section has a `command:` line: brief "Add a file `SMOKE.md` with the single line `smoke`", no other input. The expected path is the shortest one: the checks pass and the reviewers find nothing. The human deletes `SMOKE.md` after. Without a profile: the same brief in any small repository with green checks, the checks command given with the brief. A second smoke input reaches a human step: the same repository with an untracked file `notes.txt` left in it, and the answer `stop` at ask-dirty

`start` takes `brief`, `repo`, `profile`, and every other input above that the human's words or the profile give; the inputs nobody gave are left out, so their defaults apply. Save `brief.md` and `profile.md` into the run directory right after `start`, before launching what it prints.

Before a run the human makes sure the checks are green on the branch. The runbook does not fix what was red already.

## Run directory

`<the directory this session started in>/.agent-runbooks/runs/<YYYYMMDD>-<slug>/`. Slug: `task` when it is given, else three or four words from the brief in kebab-case, for example `add-version-constant`. Any such words do: the slug only names the directory. Give the run directory to `flow.py` as an absolute path, since the executors work with `cwd` the repository.

## Execution rules

You are the orchestrator of this run. Orchestrating takes a session that can launch subagents and learn when they finish. If yours cannot, stop and say so. During the run you do only these things:

- run `python3 <skill>/flow.py …` as written below
- save the input files the Inputs section names into the run directory `start` created
- launch steps as subagents, with the message `flow.py` prints, and with the reply schema where your tool takes one
- send an executor the correction `flow.py` prints for its reply
- read a step's output file only to quote it to the human
- ask the human, and report the end of the run
- show the human the run's status, as the Status group below says
- change the brief as the Brief changes section says

Nothing else. No command beyond these, no reading of `flow.py`, `state.json`, `progress.md` or the prompt files, no editing of anything in the run directory beyond `brief.md` as the Brief changes section says. `<skill>` is the directory this `SKILL.md` was loaded from.

Starting

- The run directory is `.agent-runbooks/runs/<YYYYMMDD>-<slug>` under the directory your session started in, with today's local date. Run `python3 <skill>/flow.py <run> start '<the inputs you were given, as one JSON object>'` first, with every input the Inputs section saves to a file given as that file name: it creates the directory, or refuses because it exists, in which case add `-2`, `-3` to the name and start again. Then save the input files the Inputs section names into the directory it created.
- Resume: `python3 <skill>/flow.py <run>`.

flow.py

- It keeps the state of the run and prints what to do: which steps to launch, with which executor and what message, whom to wait for, what to ask the human, or that the run has ended. Do all of what it prints, then wait. Every command it asks you to run next is printed in full.
- A `flow.py` command may run long, because it runs the runbook's code steps itself. Run it with the largest timeout your tool accepts, and wait for it as for a step. If your tool moves it to the background and tells you when it exits, wait for that. If your tool killed it, run `python3 <skill>/flow.py <run>` and do what it prints. Never start a second `flow.py` for a call that is running.
- `flow.py` names a code step running in another `flow.py` command. It is not a subagent: wait for that command, and never run `interrupted` for it.
- An executor is a named way to launch a step: a new subagent through your own subagent tool, with the model and settings its description gives, or through another tool when the description names one.
- A step's message arrives: take the last JSON object in it and run the `reply` command printed for that step with that JSON. No JSON object in the message: pass `{}`. Any JSON argument, for `start`, `reply` or `answer`, with a single quote (`'`) in it goes through stdin: put `-` in place of the JSON and pass the JSON on stdin, in a POSIX shell with a quoted heredoc. One argument of a command at most.
- The human answers a question: map the answer to one of the choices `flow.py` listed, ask again if none fits, and run the `answer` command printed with that choice and the human's words verbatim. A free-text question takes the words alone. When `flow.py` lists fields with the question, the command takes a JSON object in place of the choice: the choice and the fields the human gave. A field they did not give is left out, never guessed. `flow.py` keeps the words and writes them where the steps that follow read them.
- A reply did not pass the check: `flow.py` prints a correction. Send it to the subagent that ran the step, as a follow-up message in its session, not as a new launch, and wait for its answer the way you wait for a step. Its answer goes to the same `reply` command. If your tool cannot send a message to a subagent that has finished, run the command `flow.py` printed for that case instead. An executor that only relays another agent's reply passes the correction on to that agent, in its session, and returns its answer verbatim.
- A running step's executor is gone, because the session is new or the tool reports it dead: `flow.py <run> interrupted <call>`, with the address `flow.py` printed for that launch, such as `main/review#2`, in single quotes, since `#` and `[` mean things to a shell. Executors you launched in this conversation are not gone: wait for them.
- You departed from these rules, or did something `flow.py` does not know about: `flow.py <run> log '<one line>'`.

Launching

- Launch every step `flow.py` lists, with the executor it names, and send exactly the text between `--- message ---` and `--- end of message ---`. Add nothing, apart from lines your harness or your own rules require in every subagent prompt. An executor that only relays another agent's reply gets one more line: "Return the agent's final message verbatim."
- Steps `flow.py` lists together are launched together, in one turn.
- The message names a `reply schema` file. If your subagent tool can hold a subagent's final message to a JSON schema, give it this one: the path, or the file's content when the tool takes only that. Otherwise leave the file to the executor.

Waiting

- Waiting costs zero turns. Pick the branch that matches your harness.
  - You can launch a subagent in the background and get woken up when it finishes, and ending your turn does not end your session: launch the ready steps that way and end your turn. On a wake-up, record the reply, do what `flow.py` prints, end your turn.
  - Otherwise, which includes running nested in another agent where the end of your turn is the end of your run: launch the ready steps in the foreground, in parallel if your harness allows several calls at once, otherwise one after another. Set every timeout or yield parameter your tool accepts to 24 hours or its maximum. If a call returns while the step still runs, call the wait again and do nothing else.
- Either way the step's completion is the only event. No polling, no sleeping, no reading ahead, no status messages while it runs. An hour-long step is a normal working state.

Status

- By default, show no status during the run: the final state comes with `end`.
- Before you ask the human a question, run `flow.py <run> status --tail 10` and show its output as it is, in a code block, above the question.
- If the human asks to see the progress after every step, run `flow.py <run> status --tail 10` after every `flow.py` command that launches or ends a step (`start`, `reply`, `answer`, `interrupted`, `relaunch`), and show its output as it is, in a code block, with no commentary. Never while waiting for a step.
- If the human asks for the status: `flow.py <run> status`, its output in a code block.

Human steps and side effects

- `flow.py` tells you when to ask the human and what. Ask, then wait for the answer the way you wait for a step. A failed or interrupted step with side effects is relaunched only after the human says yes: `flow.py <run> relaunch <call>`, with the address the question names.
- `flow.py` tells you to withdraw a question: tell the human no answer to it is needed, and do not run its `answer` command.

Brief changes

- The human changes the task while implement is running or has not launched yet: edit `<run>/brief.md` in place, so it reads as if written that way from the start, then `flow.py <run> log 'brief changed: <one line>'`; that line is the trace of what changed. If implement is running, `send_message` its thronglet with `steer: true`, saying that the brief at that path changed, the one line, and that it must re-read the brief and continue. Then wait for the step as before.
- After implement has reported, the run goes on with the brief it had. Tell the human that the change is a second run on the same tree once this one ends: its brief describes the delta and names the first run's directory, and the human answers preflight's ask-dirty with `continue`.

Ending

- When `flow.py` prints `end`, report what it says to the human: the status, the run directory, the file to read. Then show the table it prints under that as it is, as markdown and not in a code block. The run is over and these rules no longer bind you.

## Steps

Declared in `flow.py` next to this file: inputs, executors, steps with their prompts, what each reads and writes, and the flow that calls them. `flow.py` drives the run and prints, for every launch, the executor's model and tool. This section is a pointer, not a copy.

## End of run

- `ready`: both reviewers found nothing, so triage was skipped, or triage marked nothing to fix, or every finding to fix is resolved with evidence; the checks are green and the polish pass is done. The human reads the polish file `flow.py` names, then the last `verify.md` if there is one, else `triage.md` if there is one. Step outputs in the run directory carry the order of their launch as a prefix, `NN-`, so the last `verify.md` is the highest-numbered `*-verify.md`. Findings not worth fixing are under "Rejected" in `triage.md` with reason "not worth it". Then commit, PR, CI.
- `needs_attention`: findings to fix remain unresolved or the checks still fail. `verify.md` says which, or `polish.md` if the polish pass left them red. The human decides.
- `failed`: a step failed or was blocked, the checks stayed red after one fix attempt or the coder found no fix within the brief, or the human stopped at ask-dirty. The file `flow.py` names at the end says why.

Report the status, the run directory and the file `flow.py` names, with the part of this section's line for that status that applies.
