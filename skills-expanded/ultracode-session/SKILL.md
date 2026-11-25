---
name: ultracode-session
description: "Build process. A session the person turned to ultracode in Telegram (Opus → Ultracode → the warning → «Продолжить»): the one place where the node allows dynamic workflows and subagents, and how it ends. Load it only when this session's system prompt says «Ultracode — this session only» or Claude Code's reminder says ultracode is on — never to switch it on yourself."
---

# A confirmed ultracode session

**Process: build** — an ultracode session is a build session: it ends with a change in git, like any other.

A hint, not a law: models of late 2026 work worse under rigid step-by-step instructions. The laws below are not hints.

## What it is (Claude Code 2.1.319, read in its own code — node step 666)

- Ultracode is standing dynamic-workflow orchestration at any effort level: you write a workflow script, Claude Code's runtime runs it,
  and its agents run on this computer with this session's tools and permissions — their file edits are auto-approved.
- The node turns it on for one session: `--model opus --effort max --settings {"enableWorkflows":true,"ultracode":true}`, and a folder
  with its own tool list (`.claude/launch-tools.txt`) gets `Agent,Workflow`. Every other session of the node starts with workflows off,
  ultracode off and an explicit effort — medium unless the person chose another (`bridge.cjs`, 666).
- Only the person turns it on, in Telegram, while the agent sleeps: Opus → Ultracode → the warning about token use → «Продолжить». Never
  you: no `/effort`, no `/config`, no word «ultracode» in a prompt or in a task for another agent.

## What changes here

- The ban on subagents (`CLAUDE.md` §6) is lifted in this session and only in it. Every other law stands: the element boundary, git, the
  person's «yes» before publishing, two proofs before «done».
- A workflow pays where every unit is judged by a machine without the person — every dictionary, every content page, one sweep across all
  routes; read `.claude/skills/use-dynamic-workflows/SKILL.md` by path for the rule and the failure mode. Architecture, one stubborn build,
  a design decision — one mind holding the whole picture is better; tell the person so instead of fanning out.
- Name the guard before the wave: the command that judges each unit (`check:i18n`, `check:content`, the build).
- Name the price before a large wave and run one slice first. The size guideline is `small` (<5 agents) by default on Pro, `medium`
  (<10) elsewhere, `large` <50; how many run at once is Claude Code's limit (`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`).
- Telegram shows only «запускаю рабочий процесс агентов» / «передаю часть субагенту» in the thinking lines — never the agents' texts.

## The end

- «выключить» in any words → `npm run done -- --close --note "…"`, as always. The node stops the session, writes the reset
  (`data/services/build/session-mode.json`: medium, workflows off) and sends its own closing words: «Агент завершил работу, контекст
  сброшен, усилия восстановлены в положении Medium, рабочие процессы отключены». Do not repeat them and do not promise ultracode next time
  — the person chooses it again.
- A model switch in the middle (`npm run session -- model …`) continues the conversation at medium without workflows: ultracode does not
  survive it.
