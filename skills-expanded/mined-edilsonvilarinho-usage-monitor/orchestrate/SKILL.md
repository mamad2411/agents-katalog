---
name: orchestrate
description: Runs a request through a cheap-first multi-agent workflow. The main session plans and validates, subagents on haiku execute, failures go back to the same agent, and only 3 rejections escalate to sonnet. Starts a live visual office portal showing agents, tasks and messages (skippable with --no-portal), and gates visual work behind prototypes. Use when the user asks to orchestrate, delegate to agents, or use the office portal.
argument-hint: "[--no-portal] [--design-system <path>] [--prototypes N] <request>"
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/portal/start.mjs *), Bash(node ${CLAUDE_SKILL_DIR}/portal/emit.mjs *), Bash(node ${CLAUDE_SKILL_DIR}/setup/agentes.mjs *)
---

# Orchestrate

Request: $ARGUMENTS

Agents:
!`node ${CLAUDE_SKILL_DIR}/setup/agentes.mjs verificar || true`

## Mode: with or without portal

- **With portal (default).** Your first action, before anything else, is to run
  `node ${CLAUDE_SKILL_DIR}/portal/start.mjs --sessao ${CLAUDE_SESSION_ID}`. The first line of your reply is the
  URL it prints, so the user can follow progress from the start; the plan comes after. If it prints an error, fix
  the portal before delegating: with the portal on, it is not optional.
- **Without portal (`--no-portal` in the request).** Never run `start.mjs`: no server, no browser, no URL. The flow
  is identical (sections 0 to 7, same rules, same limits). Everything that goes through `emit.mjs` still runs,
  because it is the log that counts rejections and enforces the escalation limits. Only the visual layer is gone.

Every `emit.mjs` call below carries `--sessao ${CLAUDE_SESSION_ID}`, which works in both modes.

The portal lives in `portal/web/` and shows one desk per agent, a task board and a communication log on a single
screen. It reads the session transcripts on its own; what only you know (tasks, messages, verdicts) goes in through
`emit.mjs`. Subcommands and flags of `emit.mjs` are in Portuguese by design (see `references/portal-contract.md`).

You are the orchestrator. With the portal on, you appear in it as agent `am`.

## 0. First run: configure the agents for this project

If the `Agents:` block above says `PENDENTE`, the project has no agents configured yet. Do this after the portal URL
line (right at the start, in `--no-portal` mode) and before planning; if it says `CONFIGURADO`, skip to section 1.

1. Show the user the detected stack and commands from the block (they come from manifests only; commands marked
   `convenção` are the ecosystem default, not verified in this project).
2. Ask which option they want, with `AskUserQuestion`:
   - **Install for this project (recommended)**: `node ${CLAUDE_SKILL_DIR}/setup/agentes.mjs instalar` writes the
     five agents to `<project>/.claude/agents/` from the templates in `agents/`, each with a `Project context`
     section (stack, commands, rule files). It never overwrites an existing agent.
   - **Use the generic agents**: `node ${CLAUDE_SKILL_DIR}/setup/agentes.mjs dispensar` records the choice and stops
     asking.
3. After installing, read each generated agent and fix what the manifests could not tell: conventions, forbidden
   paths, the real test command if the detected one is a `convenção`. Take the rules from the project's `CLAUDE.md`
   or `AGENTS.md` if present; do not invent any.
4. If the new agents are not available to delegate to, tell the user to restart the session (or reload with
   `/agents`) and run the same request again.

## 1. Interpret the request

- `--no-portal`: skip the portal (see Mode above). Strip it from the request before planning.
- `--design-system <path>`: local file or folder with the project's design system (tokens, components, rules). Strip it
  from the request. Used by section 6 and by any visual task. A value that is not a local path (a URL, a Figma
  link) is not supported: tell the user and ask for a local path. If the path does not exist, stop and ask.
- `--prototypes N`: number of prototypes per visual deliverable. Without the option, N = 4.
- Work is **visual** when it involves a screen, front end, video, image or any artefact the user judges by looking
  at it. Visual work always goes through the prototype gate (section 6).
- A request with more than one visual deliverable produces N prototypes for each.

## 2. Plan

Break the request into tasks with a new ID (check the project's task plan first, if there is one; IDs never
repeat), an owner, exclusive paths and a verifiable acceptance criterion, preferably a command that exits 0: the
agent iterates alone until it passes, without spending an orchestrator turn. Record each task in the plan and in
the portal:

```bash
node ${CLAUDE_SKILL_DIR}/portal/emit.mjs tarefa --sessao ${CLAUDE_SESSION_ID} --id PE1 --titulo "Floor plan" --dono prototype-dev --estado fila
```

Shared specification goes in a briefing file, never in the prompt. N agents read the same file.

## 3. Route: haiku first

Every subagent runs on haiku with high effort. Set that in the agent's frontmatter and delegate without `model` or
`effort`. Ready-made agent templates are in `agents/` of this skill; section 0 installs them per project.

| Work | Agent |
|---|---|
| Sweeps, locating code, gathering facts | `explorer` |
| Tests, typecheck, build, smoke, CI | `test-runner` |
| Back-end code | `backend-dev` |
| Front-end code | `frontend-dev` |
| Prototype, tooling, video, audio | `prototype-dev` |
| Planning, judging, integrating, shared contracts, dependencies, commits | you |

The portal draws these five names with their own desk. Any other subagent type works and is drawn as a generic
desk (`outro`).

Sonnet only enters by escalation (section 5). Never pass `model: "sonnet"` in advance, nor because a task looks
hard. Haiku costs 5x more above 100K prompt tokens: a large task becomes several small tasks, not one long agent.

Edit directly only a pinpoint tweak to one known file. A long command that needs no judgement (a render, for
example) runs in the background in your own session: it costs no agent tokens.

## 4. Delegate without inflating context

Split only when it pays off: evaluate the demand before opening agents. A small or sequential task goes to one
agent. Parallelism needs several truly independent tasks, never a target number of agents: every return costs one
orchestrator turn with the whole context.

A delegation prompt has at most 12 lines, in this format:

```text
Task <ID>. Briefing: <path>, section <n>.
Edit only: <paths>.
Acceptance: <command that exits 0, or verifiable criteria>.
Return: the agent's standard format.
```

Forbidden in the prompt: conversation summary, another agent's return, file contents the agent can read, the
reason behind the request. Point to a path, do not paste text.

- At most 4 simultaneous agents. Agents always in the background when there is other work to do.
- Parallel code tasks go in `isolation: "worktree"`. Exception: artefacts in exclusive folders with no shared
  test suite may use the same checkout, because no agent runs or reads another's work.
- Speak in the portal at each handoff:

```bash
node ${CLAUDE_SKILL_DIR}/portal/emit.mjs fala --sessao ${CLAUDE_SESSION_ID} --de am --para prototype-dev --tarefa PE1 --texto "Floor plan is yours."
node ${CLAUDE_SKILL_DIR}/portal/emit.mjs tarefa --sessao ${CLAUDE_SESSION_ID} --id PE1 --estado andamento
```

## 5. Validate and send back

No delivery is accepted on the agent's own report. Check every criterion with your own evidence: diff, execution,
screenshot or a frame extracted from the video.

```bash
node ${CLAUDE_SKILL_DIR}/portal/emit.mjs veredito --sessao ${CLAUDE_SESSION_ID} --tarefa PE1 --resultado aprovada --texto "Criteria checked."
```

Rejected: `--resultado devolvida`. The command prints the count and the action; follow the printed action, never
memory. Only delivery defects reject: a `BLOQUEADA` return and a usage-limit interruption do not count. Never fix
it in the agent's place.

- **`devolver ao mesmo agente`** (return to the same agent): `SendMessage` to the same agent, which keeps its
  context. The first line is `<ID> devolvida: <defect>`, because the portal classifies by it. The message carries
  only the failed criterion, the evidence and the expected result. Never resend the briefing. Verdict and
  `SendMessage` go out in the same turn: each orchestrator turn resends the whole session context.
- **`escalar para sonnet high`** (3rd rejection on haiku): run `emit.mjs escalada` and open a new agent of the same
  type with `model: "sonnet"` and `effort: "high"`, because `SendMessage` cannot change the model. No `isolation`:
  the work continues in the path where haiku stopped, which the prompt points to with the open defect. Never paste
  haiku's history.
- **`parar e reportar ao dono do produto`** (3rd rejection on sonnet): stop and report to the user what failed.

```bash
node ${CLAUDE_SKILL_DIR}/portal/emit.mjs escalada --sessao ${CLAUDE_SESSION_ID} --tarefa PE1
```

`emit.mjs escalada` refuses a task below the limit. Limits live in `LIMITE_REPROVACOES` in `portal/emit.mjs`.

## 6. Prototype gate (visual work)

1. Generate N prototypes in `prototipos/<deliverable>/`, one agent per prototype, with genuinely different directions.
2. Publish the gallery in the portal (`/prototipos/<deliverable>/`) and validate each one in a real browser. With
   `--no-portal`, open the `prototipos/<deliverable>/index.html` files directly in the browser and give the user those
   paths.
3. Stop and ask the user to choose. No final version before the choice.

### Design system

The design system is the one at `--design-system <path>`; without the option, look for one in the project only if
the work is visual, and use it if found. Never read it yourself: the `explorer` does it, to keep the whole system
out of your context.

1. Before planning any visual task, delegate to `explorer` with the standard prompt format. Task: locate, in
   `<path>`, the tokens (colors, type, spacing), the components with their props and usage rules, and any written
   guidelines. Return `file:line` pointers, at most 20 lines. `explorer` is read-only and cannot write files.
2. Write the return to a briefing file (for example `prototipos/design-system.md`): pointers plus the few values
   that decide the work. Shared specification goes in a briefing, never in the prompt.
3. Every visual task points to that briefing and names the design-system files the agent must read. Prototypes use
   the existing tokens and components only.
4. A new token, component or rule: list what is missing and ask permission first.

If the explorer finds nothing usable at `<path>`, stop and tell the user; do not invent a design system.

## 7. Wrap up

One activity, one commit, in Conventional Commits. Update the status in the project's task plan if there is one.
In the final report, state what was verified, what was not, the per-agent token cost shown in the portal (with `--no-portal`: say the cost was not measured), and how
many rejections and escalations each task had.
