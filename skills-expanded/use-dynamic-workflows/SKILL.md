---
name: use-dynamic-workflows
description: >
  Waves of agents instead of one — what a dynamic workflow is, what it may be pointed at, and what it costs. On the node it runs
  only in a session the person confirmed as ultracode in Telegram (skill ultracode-session, which sends you here by path). Read it
  there before the first wave, or when the owner asks how workflows work. The thing you cannot see from inside a session: the agents
  a workflow spawns run on THIS machine with THIS session's permissions, and they edit files auto-approved — so the only thing
  standing between a fan-out and a large, tidy, expensive wrong answer is a command that judges each unit without you.
---

# use-dynamic-workflows

> Informational, not binding. **Know a better way for the case in front of you — do it your way and
> say so.** You are trusted with the creative work on this project.

**Off in every session of the node, and that is the correct state for most work.** The law in `CLAUDE.md` §6 forbids subagents; the
one door out is a session the person confirmed as ultracode in Telegram (Opus → Ultracode → the warning → «Продолжить», node step 666,
skill `ultracode-session`). Nobody opens that door from inside a session — not you, not a task, not the size of a job.

---

## 1. What it is — and what it is not

**Not "many agents at once".** That is a fan-out, and a fan-out is what people build by hand when they
are guessing.

A dynamic workflow is **a script that the model writes and a runtime executes**. The script holds the
loop, the branching and the intermediate results: the first wave runs, its results decide what the
second wave is — verification, summary, another fan-out — and only the final answer reaches the
conversation.

Ultracode (Claude Code 2.1.319) is the standing form of it: «standing dynamic-workflow orchestration at any effort level» — a
substantive task becomes a workflow by default. It needs dynamic workflows (`enableWorkflows`, OFF by default on Pro) and a model with
the `xhigh` effort. The node starts it with flags, for one session: `--model opus --effort max --settings
{"enableWorkflows":true,"ultracode":true}`; every other session gets `enableWorkflows: false, ultracode: false`.

## 2. 🔒 Where it runs — read this before promising anything

**Nothing is created on the production server and no virtual machine is started anywhere.** The runtime
executes the *script* in an isolated environment with no filesystem or shell of its own; the script only
coordinates. The agents it spawns run **inside the existing session, on the machine that session runs
on**, with the same permission mode, the same tool allowlist and the same sandboxing as any other call.

So the honest answer to "what will it touch?" is: **exactly what this session can already touch, only by
many agents at once instead of one.** If the session can reach the server, so can they.

- **Subagents always run in `acceptEdits`**, whatever the session's mode is: file edits are
  auto-approved. Shell, web and MCP calls outside the allowlist still prompt.
- **There is no mid-run input.** Only a permission prompt pauses a run. Sign-off between stages means
  each stage is its own workflow.

## 3. 🔒 The guard rule — the whole skill in one line

> **A workflow is justified only where each unit's result is judged by a machine, without the owner.**

Yes: translations, content sweeps, mechanical migrations — `check:i18n` counts languages and keys,
`check:content` refuses a bad link, `check:encoding` finds a broken character in any language.
No: architecture, the client/server boundary, debugging a build. There, proving an answer costs more
than producing it, and more agents produce more work to review, not less.

**Name the guard before the wave.** Cannot say which command judges the output — then it is not a
workflow, it is a fan-out with a hope attached. In an ultracode session this rule still stands: say to the person «this one is better
done by one mind» when it is.

## 4. 🔒 The failure mode: not a wrong answer, a plausible one at scale

**An agent that dies mid-write leaves a file that does not compile.** It already happened here: five
agents were translating one dictionary each, the session hit its limit, two died while writing and left
placeholder markers (`__UK_BLOCK__`) inside an object literal. The file looked finished. It could never
have built, and nobody noticed until a real build ran — a dictionary check validates dictionaries, not
the code that uses them.

Multiply that by a fan-out and you have the real risk. This is why §3 is a rule and not advice.

## 5. Cost — the test is the owner's own last week

What stops a run is not availability but the limit hit halfway through.

- an ordinary single-agent session already reaches the limit before the work is done → a workflow will
  not fit;
- ordinary sessions finish comfortably → a workflow is affordable.

**Stopping mid-run costs more than it looks.** On resume, cached results stop at the first agent that had
not finished, and every agent that started after it runs again — including the ones that completed. A run
does not survive leaving the CLI. Hence: **many small agents preserve far more progress than a few long
ones.**

What the product gives instead of a promise: `/workflows` shows each agent's tokens live and can stop the run; a «Large workflow»
warning is advisory and pauses nothing; the size guideline aims the planner — `small` <5 agents (the default on Pro), `medium` <10 (the
default elsewhere), `large` <50; how many run at once is Claude Code's own limit (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`). **Price a
big job by running one slice first** — one directory, not the repository. Plan numbers change; the last-week test does not.

## 6. 🔒 One door, opened by the person

**The person's choice in Telegram** — Opus → Ultracode → the warning «Ultracode запускает рабочие процессы с множеством субагентов …
Это может привести к экстремально высоким расходам токенов» → «Продолжить». The warning is the price said aloud; the press is the
person's judgement about cost, which no panel and no agent can make for them. «Выбрать другую модель» closes the door again.

## 7. Once it is on

- **The owner approves the plan before it runs.** The prompt lists the planned phases, `View raw script`
  shows the script. That is the last cheap moment to notice the wrong direction.
- **The session stays free while it runs**, but cannot steer mid-run (§2).
- **Save what worked** — in `/workflows`, `s` saves the run's script as a command. A review that runs on
  every branch then repeats the same orchestration; that, not the size of one run, is where a workflow
  repays its setup.

## 8. When it switches back off

At «выключить»: the node stops the session, the next one starts at medium with workflows off, and the person hears it in the node's
closing words. A model switch in the middle of the conversation also ends it. Ultracode is never carried into another session.
