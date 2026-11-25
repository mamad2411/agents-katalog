---
name: mc-manage-skills
description: Save, edit, list, or delete a Claude Code skill in this workspace. Use when the user wants to turn a workflow into a reusable skill ("skill 化して", "save this as a skill"), modify or remove one, or list what's registered. Writes one markdown file per skill at `data/skills/<slug>/SKILL.md`; a workspace-side hook mirrors it into `.claude/skills/<slug>/SKILL.md` so Claude Code picks it up.
---

# Skill manager

A bundled MulmoClaude preset skill (`mc-` prefix = launcher-managed; do not edit
this file in the workspace, it is overwritten on every server boot).

Help the user manage **project-scope** Claude Code skills. The skill *body*
that Claude Code reads lives at `.claude/skills/<slug>/SKILL.md`, but agents
**must not write there directly** — Claude Code's permission system treats
`.claude/` as a self-modification surface and the host GUI cannot answer the
resulting prompt, so the write hangs.

Instead, **edit the staging file** at `data/skills/<slug>/SKILL.md`. A PostToolUse
hook mirrors every Write / Edit / `rm` on those staging files into
`.claude/skills/<slug>/SKILL.md` (or removes the entire dir on delete) and
then asks the server to re-register skills — no restart needed. The user
never sees the staging vs. canonical split; they just say "skill 化して".

The user-scope folder `~/.claude/skills/` is read-only territory managed
outside MulmoClaude — don't touch those.

End with a one-line confirmation ("Saved as foo-skill." / "Removed foo-skill.")
so the user can verify without scrolling.

## Collections (a skill + a `schema.json`)

If the user wants a small **data app** — a list/table they can view and edit
(a swimming log, a recipe box, a client database) — that's a **collection
skill**: a skill dir that also ships a `schema.json` (and optional
`templates/*.md`). Author all of them under the same staging dir
(`data/skills/<slug>/SKILL.md` + `data/skills/<slug>/schema.json` +
`data/skills/<slug>/templates/*.md`); the same bridge hook mirrors those three
file kinds into `.claude/skills/<slug>/` and the collection appears at
`/collections/<slug>`. **Read `config/helps/collection-skills.md` first** — it
is the authority on the schema DSL (field types, relations, derived fields,
actions). Don't hand-roll a schema from memory.

## Workflow 1: save a new skill

**Triggers**: "skill 化して", "save this as a skill", "make this reusable",
"そのまま skill に".

**Step 1 — distil.** If the user is asking you to skill-ify the current
conversation, read the chat transcript first. The transcript lives at
`conversations/chat/<session-id>.jsonl`; if you don't know the session id, list the
directory and pick the most-recent one. Reduce the conversation into a
focused markdown body in **second person** ("First, do X. Then, do Y.") that
captures the reusable workflow — not the one-off details that won't generalise.

**Step 2 — pick a kebab-case slug.** Lowercase ASCII letters / digits, single
hyphens between segments, no leading / trailing / consecutive hyphens, 1-64
characters. Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$`. If the user proposed a name,
use it as-is (validate the same way).

If `data/skills/<slug>/SKILL.md` already exists, ask before overwriting.

**Step 3 — Write `data/skills/<slug>/SKILL.md`** (NOT `.claude/skills/...` — the
bridge hook handles that copy):

```markdown
---
name: <slug>
description: One-line summary that frames *when* the skill should run.
schedule: daily 09:00      # optional — auto-runs on schedule
roleId: general            # optional — role to use for scheduled runs
---

# <Skill name>

Body in markdown, second person. Focused on the reusable workflow.
```

**Description rules** (the discovery layer reads this — make it count):

- Lead with an action verb + noun ("Save / list / delete a recipe", "Schedule
  a recurring task"). Vague descriptions like "Helps with X" don't trigger.
- Include a few **trigger phrases** the user might say, in their language.
- Cap around 1-2 sentences. Long descriptions get truncated when the listing
  is sent to Claude.

**Optional fields**:

- `schedule` — `daily HH:MM` (UTC) or `interval Ns` / `Nm` / `Nh`. The
  scheduler auto-runs the skill at that cadence.
- `roleId` — role to use for scheduled runs (defaults to `general`).

The bridge hook mirrors `data/skills/<slug>/SKILL.md` → `.claude/skills/<slug>/SKILL.md`
and fires `POST /api/config/refresh`, so a new `schedule:` activates without a
server restart.

## Workflow 2: recall / browse

**Triggers**: "what skills do I have?", "保存した skill みせて", "list my
skills".

List the staging directory:

```bash
ls data/skills/
```

Read each `data/skills/<slug>/SKILL.md`'s frontmatter and present the names + one-line
descriptions in chat. Don't dump raw markdown unless the user asks for a
specific skill's details.

## Workflow 3: update

**Triggers**: "〇〇 の skill を更新して", "change the description of foo",
"add a schedule to foo-skill".

Read `data/skills/<slug>/SKILL.md`, apply the change with Edit (preserve every other
field unless the user explicitly asked to change it), and confirm. The bridge
hook re-mirrors the file and triggers a refresh.

## Workflow 4: delete

**Triggers**: "remove the foo skill", "foo-skill いらない".

Only when the user explicitly asks. **Re-validate the slug against
`^[a-z0-9]+(-[a-z0-9]+)*$` before running the command** — if it fails, refuse
and ask the user to confirm by name. When valid, use exactly this form
(the bridge hook only mirrors deletes that match this shape; bulk `rm -rf` of
the parent dir or paths with wildcards are intentionally NOT mirrored so a
typo can't wipe every skill):

```bash
rm -rf data/skills/<slug>/
```

The hook then removes `.claude/skills/<slug>/` to match. Confirm afterward.

## Tone

Friendly, practical. Don't lecture about staging files, paths, or hooks —
those exist behind the scenes and the user should never need to know. Just
save and confirm. If a request needs several decisions (e.g. "save as foo
and schedule it daily"), do them in one go, don't ping-pong.
