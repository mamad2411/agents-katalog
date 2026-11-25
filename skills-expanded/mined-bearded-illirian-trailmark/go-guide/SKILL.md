---
name: go-guide
description: |
  Adds a new conceptual guide to a project's knowledge folder. Runs in
  three modes: interactive (user-invoked), from-task (auto-invoked from
  ship-first after a fast-track completes), from-epic (from epic closure).

  Storage: local `.md` file under `project-knowledge/guides/{topic}/`,
  registered via git commit + push. No database, no admin panel — the
  file itself is the artifact, discoverable via file tree or search.

  Flow: project selection → topic selection → title → text → .md creation
  → git push.

  Use when: "/go-guide", "add guide", "new guide", "save concept",
  or auto-invoked at the end of ship-first when work produced a
  reusable concept worth documenting.
---

# /go-guide — Add a Conceptual Guide

Captures a durable concept — architectural decision, workflow rule,
domain vocabulary — into the project's knowledge folder so future
readers (including the same person in three months) can rediscover it
without digging through commits.

---

## Step 0 — Choose invocation mode

Three modes cover three lifecycles:

| Mode | Trigger | Behavior |
|---|---|---|
| **interactive** | User types `/go-guide` | Full flow, asks project + topic + title + text |
| **from-task** | `Skill('go-guide', mode='from-task', task_slug=…)` | ship-first hook after fast-track close; suggests title/text from task context, user edits |
| **from-epic** | `Skill('go-guide', mode='from-epic', epic_slug=…)` | Epic closure hook; same as from-task but scoped to whole epic |

---

## Step 1 — Select project

Read `aihub/projects.yml`. Show numbered menu of projects. Wait for user
choice or partial-name match.

**Save to session context:**

- `{project_id}` = chosen project id (slug)
- `{project_path}` = project's local path
- `{knowledge_root}` = `{project_path}/project-knowledge/guides/`

If `{project_path}` doesn't have `project-knowledge/` folder — create it:

```bash
mkdir -p "{project_path}/project-knowledge/guides/"
```

---

## Step 2 — Select topic

A **topic** is a stable folder grouping guides by subject (e.g.
`architecture`, `workflows`, `terminology`, `decisions`). Ask the user
which topic; offer existing topics first:

```bash
ls "{knowledge_root}" 2>/dev/null
```

Show numbered menu + `0. New topic`. If user picks new — ask for slug
(lowercase, hyphens). Create the folder:

```bash
mkdir -p "{knowledge_root}/{topic_slug}/"
```

---

## Step 3 — Compose title

For **interactive** mode — ask user for one-line title.

For **from-task** / **from-epic** mode — propose a title derived from
task/epic slug + brief. Show proposal, wait for user edit or approval.

Convert to filename slug:

```
"Why we chose SQLite over Postgres" → "why-sqlite-over-postgres.md"
```

---

## Step 4 — Compose text

**interactive** — ask user for content. Accept multiline paste.

**from-task** / **from-epic** — propose content derived from the source
material:

- Task's `task.md` intent + key decisions from `decision-*.md` files
- Report highlights ("What was notable" sections)
- Any `note-*.md` capturing the essence

Show the proposal for user edit before saving. Never save auto-generated
content without user approval.

---

## Step 5 — Write file

```bash
FILE="{knowledge_root}/{topic_slug}/{title_slug}.md"

cat > "$FILE" <<EOF
# {title}

**Date:** {date}
**Topic:** {topic_slug}
**Source:** {task_slug or epic_slug or "interactive"}

{text}
EOF
```

Print the resolved path to the user for confirmation.

---

## Step 6 — Register via git

```bash
cd "{project_path}"
git add "project-knowledge/guides/{topic_slug}/{title_slug}.md"
git commit -m "guide: add {title} ({topic_slug})"
git push origin main  # or the project's default branch
```

If push fails (auth, network, protected branch) — report the error but
leave the file in place. User can push manually later; the guide isn't
lost.

---

## Step 7 — Confirm

Print a one-line summary to the user:

```
✅ Guide saved: project-knowledge/guides/{topic_slug}/{title_slug}.md
   Committed: {short_sha}
```

For **from-task** / **from-epic** mode — return to caller (ship-first)
with `{success: true, path: "…"}`.

---

## Discovery

Consumers find guides through three paths:

1. **File tree** — `project-knowledge/guides/{topic}/` grouped by subject
2. **Search** — grep across the folder for keywords
3. **Cross-reference** — task reports and decision docs cite guide paths

No database or admin panel required. The file tree is the index.

---

## Rules

- One guide = one concept. Long docs → split.
- Title should read as a claim or question, not a category label
- Topic folders are stable — don't renumber, don't rename lightly
- Guides are additive: new decisions supersede old ones via new files,
  don't edit old guides to reflect new state
- Never save auto-generated content without user approval, even in
  from-task mode

---

## Anti-patterns

### ❌ Editing old guides instead of adding new

The guide `why-sqlite.md` reflected a 2024 decision. In 2026 the
project moves to Postgres. The agent edits the old file to "update"
it — the historical context vanishes.

**Rule:** old guides stay as-is. New decisions create new guides.
Optionally cross-link: new guide adds "supersedes: `why-sqlite.md`"
line at top.

### ❌ Saving without user preview in from-task mode

ship-first invoked `go-guide` from-task; agent auto-generated content
from task artifacts and pushed without showing the user. Result:
malformed guide committed to git history.

**Rule:** always show proposal + wait for approval in from-task /
from-epic mode. User can edit or reject.

### ❌ Missing git push step

Guide file created but never committed. Next agent invocation
overwrites it thinking it's uncommitted junk.

**Rule:** Step 6 is mandatory in all three modes. If push fails —
report it, don't retry silently, but leave the file.

### ❌ Guide as an open todo

Agent uses go-guide to save "what still needs doing" — a running
todo list. The knowledge folder fills up with never-actioned items
that decay into noise. Future readers can't tell durable concepts
from stale plans.

**Rule:** guides are durable concepts (why we chose X, how the domain
works, what a term means). Open work items belong in `tasks/`, not
`project-knowledge/guides/`. If it starts with a verb and has no
answer yet, it's a task, not a guide.

---

## Related skills

- **ship-first** — invokes go-guide in from-task mode after a
  fast-track closes; the guide captures the durable concept from
  the just-completed work
- **plan-first** — precedes execution; a guide often derives from
  a plan-first decision worth preserving beyond the current task
- **decision-first** — decisions and guides are siblings: decisions
  record *why* a choice was made in context; guides record *what*
  the resulting concept is, standalone

---

## Step 99 — Log invocation

Before exiting, log this skill invocation to routing.db:

```bash
sqlite3 {routing_db} \
  "INSERT INTO skill_invocations (task_id, block_num, skill_name, invoked_at)
   VALUES ('{slug}', '{N}', 'go-guide', datetime('now'))" 2>/dev/null || true
```

If `{slug}` / `{N}` are unknown the row is written with empty values; `|| true` keeps a logging failure from aborting the skill.
