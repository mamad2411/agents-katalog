---
name: project-notes
description: Create, read and maintain the private per-project knowledge base in `personal_docs/` (README index, active work items, runbook, gotchas, decisions, architecture, learnings). Use when starting non-trivial work in a folder, when resuming unfinished work, when you learn something non-obvious worth keeping, when asked to "write this down", "take notes" or "remember this for the project", or before ending a substantial session.
---

# project-notes

`personal_docs/` is a private, git-ignored folder in each project. It is the shared memory for every agent that works there (Claude Code, Codex, Gemini, Cursor): plain markdown, same rules for all. Its job is to make the next session start informed and resume unfinished work without rediscovering anything.

Helper: `scripts/notes.py brief | init | check` (stdlib Python). With the dot-agent installer, Claude Code runs `brief` at session start, so the README and active work are already in context when one exists.

## Layout

```
personal_docs/
├── README.md         always read · ≤60 lines · what it is, current focus, "read when" map
├── work/             one file per unfinished task: goal · plan checklist · state · next
├── runbook.md        ┐
├── gotchas.md        │ stable knowledge, opened only when the task needs it
├── decisions.md      │ (the README "read when" table says when)
├── architecture.md   │ created on first entry, never as empty templates
├── learnings.md      ┘
├── docs/             longer reference: specs, research, API notes
└── archive/          finished work items and rolled-up old entries
```

Templates are in `templates/`.

## Principles

1. **Progressive disclosure.** Only `README.md` is read every session. Everything else is opened on a trigger ("before you debug → gotchas.md"). This keeps the per-session cost at about 60 lines.
2. **Lazy creation.** `init` creates only `README.md` and `work/`. A topic file appears when it gets its first real entry. Empty skeletons teach agents to ignore the folder.
3. **Resume, don't recap.** Unfinished work lives in `work/<task>.md` with a `**Next:**` line. Any agent can pick it up cold.
4. **Every fact has a source and a date.** Entries carry `**Source:**` (path:line or commit) and `**Verified:** YYYY-MM-DD`. Old entries get re-checked before anyone relies on them, and `check` flags those older than 90 days.
5. **Budgets.** README ≤60 lines, topic files ≤250 lines. Over budget means roll up: merge duplicates, move the detail to `docs/`, move dead entries to `archive/`.

## Where it lives

- The nearest `personal_docs/` from the working directory upward, stopping at the git root. If there's no repo, the working folder.
- Monorepo: one at the root. Add `packages/<x>/personal_docs/` only when a package has its own runbook and gotchas, and link it from the root README.
- It must be git-ignored through the **global** excludes file, never the repo's `.gitignore` (that would reveal it to the team). `init` and `check` both verify this.

## Session start

1. Run `notes.py brief` (skip it if its output is already in context from the hook).
2. Nothing there and the task is non-trivial (more than a quick question or one-line fix)? Run `notes.py init`. Fill README's what / stack / focus from what you can verify (manifests, scripts, CI, the repo README). Write `<unknown>` rather than guess. Tell the user in one line.
3. Resuming? Open the matching `work/` file and start from its **Next** line.
4. Treat notes as likely right, not certainly right. Verify a fact against the code before acting on it, and fix it if it's stale.

## While working: write back when it earns a line

Write only what the next agent couldn't get cheaply from the code or git history.

| You learned | Goes in |
|---|---|
| A trap that cost time: misleading error, wrong env, flaky step | `gotchas.md` |
| A choice between options, and why | `decisions.md` |
| How to run, test, deploy or release; an env var **name** and where its value lives | `runbook.md` |
| A structural fact: a service, a data flow, a key file | `architecture.md` |
| A pattern or preference for working in this project | `learnings.md` |
| A project-wide "never do this" | README **Never do here** |

To create a topic file, copy its template, then add the entry. Use absolute dates, newest first. Edit or delete wrong entries rather than stacking contradictions.

## Multi-session work: `work/`

- Start a `work/<short-task-name>.md` from `templates/work/_template.md` when a task won't finish this session, or when the user asks to plan something.
- Keep the **Plan** checklist and the **Next** line current as you go, not only at the end.
- Done: set Status to done, add a final Log line, move the file to `archive/`, and move any lasting lessons into the topic files.

## End of a substantial session

1. Update the `work/` file (State, Next, Log) or archive it.
2. Update the README's **Current focus** and **Updated** date.
3. Run `notes.py check`. Fix what it flags: stale entries, dead paths, budget overruns, anything that looks like a secret.

## Never

- Secrets, tokens, customer data or personal data. Store env var **names** only, with where the value lives.
- Copied code or restated git log. Link the path or commit instead.
- Committing it. If a note would help the whole team, suggest moving it into the repo's docs. The user decides.

## Relation to other memory

- **Agent memory** (Claude auto-memory, Codex memories): who the user is and how they work, across projects.
- **`personal_docs/`:** facts about this project, visible to every agent.
- **Repo docs** (`README`, the committed `AGENTS.md`/`CLAUDE.md`): team-facing. Content gets promoted there only when the user says so.
