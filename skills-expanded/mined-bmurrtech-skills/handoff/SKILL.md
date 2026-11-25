---
name: handoff
description: >
  Handoff: write a portable session brief for a fresh agent (OS temp by
  default; keep → .scratch/handoffs/). Hybrid content + kind overlays; post-write
  glance for human check. Use when switching sessions, forking ADR/PRD/idea work
  out of a muddy chat, or when the user asks for a handoff.
disable-model-invocation: true
---

# handoff

Write one markdown file so a fresh agent can continue **without this chat**.
Full detail lives in the file. The reply is a short **at-a-glance** only.

Read [references/handoff-base.md](references/handoff-base.md) when drafting.
Read [references/kind-legend.md](references/kind-legend.md) to match a kind.
When a kind matches, read that overlay under `references/kinds/` and apply its
deltas — do not copy the base into the kind file.

## Boundaries

- Do **not** write a default (temp) handoff into the repo (`docs/`, `pm/`,
  `skills/`, or `.scratch/`).
- Do **not** write a **keep** handoff anywhere except `.scratch/handoffs/`.
- Do **not** invent kind slugs or use a `generic` kind — closed set only.
- Do **not** paste full specs, plans, ADRs, issues, commits, or diffs — **path /
  URL refs**. Put short acceptance, constraints, verdict, and ADR candidacy
  **inline** (hybrid).
- Do **not** use “see this chat/transcript” as the carrier of a fact — write the
  fact into the file or omit it.
- Do **not** paste the full handoff into chat — glance only.
- Do **not** include secrets, tokens, passwords, or PII.
- Do **not** author ADR or PRD bodies here — point at **`create-adr`** / **`create-prd`**.
- Do **not** overwrite an existing handoff on correct/reprompt — write a **new**
  timestamped file.

## Workflow

### 1. Classify destination

**keep** when the invoke prompt says *keep*, *save this file*, or clear persist
intent. Otherwise temp.

| Signal | Destination |
|--------|-------------|
| Absent (default) | `{tmpdir}/{filename}` |
| **keep** | `.scratch/handoffs/{filename}` (create dirs if missing) |

If destination ambiguous → ask once; default remains temp.

**Filename:** `{kind}-{slug}-{yyyyMMdd-HHmmss}.md` when a legend kind matches;
else `{slug}-{yyyyMMdd-HHmmss}.md`. Infer a short kebab `slug` from aim.

**Done when:** destination path + filename chosen.

### 2. Resolve aim

1. If the user passed an invoke arg → treat it as next-session aim.
2. Else infer aim from the conversation.
3. If ≥2 plausible next aims and no arg → **ask once** before write (one beat).
   If aim is clear (arg or single thread) → do not ask.

**Done when:** one aim is selected (or user answered the ask).

### 3. Match kind

Using [kind-legend.md](references/kind-legend.md): attach at most one closed
kind. No match → base only (title/slug filename, no invented kind).

**Done when:** kind is a legend slug or none.

### 4. Draft from base + overlay

Fill [handoff-base.md](references/handoff-base.md). Omit empty sections (note
N/A only when useful). If a kind matched, apply `references/kinds/{kind}.md`
deltas. In the handoff **body** and glance, label the kind as **Display (slug)**
from the legend (e.g. `code-review (cd-rvw)`) — never slug-only. Filenames still
use the slug prefix. Suggested skills: **next workflow first**; housekeeping last.

Repo-state claims must include a **re-verify** cue (`git status` / equivalent).

If the write is **blocked** (e.g. plan mode): say so, name the path that will be
used, and write automatically on the next unrestricted turn **without** waiting
for a second `/handoff`.

**Done when:** draft covers base (and kind deltas when applicable).

### 5. Write + glance

Write the file. Then report **only** this at-a-glance (≤ ~5 lines):

1. **Path** (absolute) + `temp` | `keep`
2. **Intent** (one line) + **kind** as Display (slug) or `none`
3. **Next action** (skill/command)
4. **Check:** 2–4 bullets the user should verify
5. **Correct?** Reprompt to rewrite if wrong → new timestamped file

**Done when:** file exists at that path and the glance was reported.
