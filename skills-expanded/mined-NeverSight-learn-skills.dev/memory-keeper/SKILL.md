---
name: memory-keeper
description: |
  Save and load durable knowledge — project facts, conversation context, or user requirements/preferences — in a per-project memory store under `~/.agents/memories/`.
  TRIGGER (save) when: the user invokes this skill to persist something; says "save this to memory", "remember this", "记一下", "保存记忆", "记住这个", "把这个存到记忆里"; states a durable preference, decision, or constraint worth carrying across sessions; or asks to summarize the project / context for later.
  TRIGGER (load) when: the user invokes this skill to recall; says "load project memory", "read my memories", "what do you remember", "读取该项目记忆", "加载记忆", "回忆一下这个项目"; or starts work on a project and wants prior context restored.
  DO NOT TRIGGER when: the fact only matters to the current turn, is already recorded in the repo (code, README, git history), or the user is just asking a question without wanting anything persisted or recalled.
---

# Memory Keeper

A per-project memory store that survives across sessions and agents. Two modes:

- **Save** — distill what matters into one fact per file. See [Saving memories](#saving-memories).
- **Load** — restore prior context for the current project. See [Loading memories](#loading-memories).

Both modes resolve the same per-project directory the same way — see [Storage layout](#storage-layout).

## When to use

**Save** when:
- The user explicitly asks to remember / save something ("保存记忆", "remember this", "记住").
- A durable fact surfaces that future sessions would benefit from: a user preference, a project goal or constraint, a non-obvious decision, or a pointer to an external resource.
- The user asks to summarize the project or current context for later reuse.

**Load** when:
- The user invokes the skill to recall, or says "读取该项目记忆", "加载记忆", "read my memories", "what do you remember about this project".
- You are starting work on a project and want any previously-saved context, preferences, or decisions restored before acting.

Do **not** save: things only relevant to this turn, facts already captured in the repo (code structure, past fixes, git history, CLAUDE.md/AGENTS.md), or secrets/credentials.

## Storage layout

All memories live under `~/.agents/memories/`, partitioned by the **project root path** so each project has its own namespace:

```
~/.agents/memories/
└── <encoded-project-path>/
    ├── index.md              # index of every memory in this project (always present)
    ├── <topic>-<detail>.md   # one fact per file, semantic kebab-case name
    └── ...
```

### Encoding the project path (Claude Code projects format)

The subdirectory name is the **absolute project root path** with every non-alphanumeric character replaced by `-`. This matches how Claude Code names its `~/.claude/projects/` directories.

```bash
PROJECT_ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
ENCODED="$(printf '%s' "$PROJECT_ROOT" | sed 's/[^a-zA-Z0-9]/-/g')"
MEM_DIR="$HOME/.agents/memories/$ENCODED"
```

Example: `/Users/alice/Documents/github_workspace/agent-skills` → `-Users-alice-Documents-github-workspace-agent-skills`.

If there is no project context at all (no git root and the cwd is not meaningful), ask the user which project this memory belongs to rather than guessing.

Saving is a **two-step, confirm-before-write** flow: first present a report of exactly what would be saved, then write only after the user approves. Never write memory files before confirmation — this avoids persisting inaccurate content that has to be reworked later.

### Step 1 — Draft a report (no writes yet)

1. **Resolve the memory directory** — compute `MEM_DIR` with the snippet above. Do **not** create it or write anything yet.
2. **Distill the fact** — reduce the content to the durable essence (1–2 short paragraphs). One file = one coherent fact. If the user dumped several unrelated facts, plan several files.
3. **Check for duplicates** — read `index.md` and existing files in `MEM_DIR` (read-only). If a memory already covers this topic, plan to **update that file in place** rather than create a near-duplicate; note any memory that is now wrong and should be deleted.
4. **Present the save report and ask for confirmation** — show the user, for each memory to be written:
   - the target absolute path and whether it is **new** or an **update** (and any deletion);
   - the proposed semantic filename;
   - the `type` (user / feedback / project / reference);
   - the **full distilled content** that would be written (verbatim, including frontmatter);
   - the exact `index.md` line that would be added or changed.

   Then explicitly ask the user to confirm or correct it. **Do not proceed without explicit approval.** If the user requests changes, revise the report and re-confirm. Treat silence or an ambiguous reply as "not approved".

### Step 2 — Write (only after approval)

5. **Create the directory and index** — `mkdir -p "$MEM_DIR"`; if `index.md` is absent, create it from the [index template](#indexmd-template) before adding the first memory.
6. **Write the memory file(s)** — exactly as approved. Name each `<topic>-<detail>.md` in semantic kebab-case (e.g. `build-pnpm-commands.md`, `user-prefers-terse-replies.md`, `auth-jwt-decision.md`), using the [memory file template](#memory-file-template). Avoid generic names like `note-1.md`.
7. **Update the index** — add or update the one-line pointer in `index.md`: `` - [`<file>`](<file>) — <one-line hook> `` under the matching type heading.
8. **Confirm** — report the saved absolute path(s) back to the user.

## Memory file template

Each memory file is self-contained with light YAML frontmatter:

```markdown
---
title: <human-readable title>
type: user | feedback | project | reference
created: <YYYY-MM-DD>
tags: [<optional>, <kebab-tags>]
---

<The fact, stated plainly. For `feedback` and `project` memories, follow with:>

**Why:** <the reason / motivation this matters>
**How to apply:** <what to do differently because of it>

<Link related memories with [[other-file-slug]] (the filename without .md).>
```

Memory types:

- **user** — who the user is: role, expertise, standing preferences.
- **feedback** — guidance on how the agent should work (corrections or confirmed approaches); always include **Why** and **How to apply**.
- **project** — ongoing goals, constraints, or decisions not derivable from the code or git history; convert relative dates ("next week") to absolute dates.
- **reference** — pointers to external resources (URLs, tickets, dashboards).

## index.md template

```markdown
# Project memory index

> Memories for `<PROJECT_ROOT>`. One file per fact; this index is the table of contents.

## User
- [`user-prefers-terse-replies.md`](user-prefers-terse-replies.md) — wants concise, markdown answers

## Feedback
- [`feedback-branch-before-commit.md`](feedback-branch-before-commit.md) — always branch off main before committing

## Project
- [`project-q3-migration-goal.md`](project-q3-migration-goal.md) — migrate auth to OAuth2 by 2026-09-30

## Reference
- [`reference-design-doc.md`](reference-design-doc.md) — link to the architecture RFC
```

Keep the index to one line per memory — never put memory bodies in `index.md`. When a file is updated or deleted, update its index line to match (or remove it).

## Loading memories

When the user asks to load / read the project's memory (or you are restoring context before starting work):

1. **Resolve the memory directory** — compute `MEM_DIR` exactly as in [Storage layout](#storage-layout) (`git rev-parse --show-toplevel` → encode → `~/.agents/memories/<encoded>/`).
2. **Check existence** — if `MEM_DIR` or its `index.md` does not exist, tell the user there are no saved memories for this project yet (and offer to start saving). Do not invent memories.
3. **Read the index first** — open `index.md` to get the table of contents and the one-line hook for every memory. This is the cheap overview.
4. **Decide what to open**:
   - On a broad request ("load all project memory", "回忆一下这个项目") read every memory file so nothing is missed.
   - On a scoped request ("what do you remember about auth?") read only the files whose hooks/`tags` match, to stay context-efficient.
5. **Apply, don't just dump** — fold the loaded facts into how you proceed: honor `user`/`feedback` preferences, respect `project` constraints, and follow `reference` pointers. Resolve `[[other-file-slug]]` links by opening the referenced memory when relevant.
6. **Verify before acting** — a memory reflects what was true when written. If it names a file, flag, function, or date, confirm that still holds in the current repo before relying on it; flag anything that looks stale to the user.
7. **Summarize** — give the user a short briefing of what was loaded (grouped by type), not a raw paste of every file.
