---
name: second-brain
description: Set up and operate a file-based second brain — a knowledge vault that every Claude Code session reads on start and writes back to before it ends, so context compounds across sessions instead of evaporating. Use "second-brain setup" to bootstrap a new vault (folder structure, brain CLAUDE.md, note templates, optional session-log hook), and follow the OPERATE rules in every session once a vault exists. Built for Obsidian-flavored markdown but works with any plain-markdown folder.
---

# Second Brain — the vault every session reads and feeds

A session's context dies when the session ends. A vault of plain markdown files does not. This skill sets up and operates that vault: one folder tree that holds the registry of everything you work on, the conventions for writing it down, and the accumulated lessons that make every future session smarter than the last one.

The machinery is three habits enforced by files:
1. **Boot from the brain.** Every session starts by reading the vault's own CLAUDE.md — the registry, the rules, the pointers to deeper indexes.
2. **Write back before ending.** Substantive sessions end with a session log, updated notes, and new learnings. No mental notes; files or it didn't happen.
3. **Garden continuously.** A recurring pass (see the `vault-gardener` skill) removes entropy so recall stays precise as the vault grows.

## Mode 1: SETUP — bootstrap a new vault

Trigger: "second-brain setup" or any request to create a knowledge vault. Ask only for two things if not evident: where the vault should live (`{VAULT}`, e.g. `~/Documents/brain` — pick a synced folder if the user works across machines) and the user's main work contexts (businesses, clients, or domains — these become the registry rows and `#ctx/*` tags).

1. **Create the structure:**

```text
{VAULT}/
├── Projects/          One folder per active project; each gets a Title Case index note
├── Areas/             Ongoing responsibilities with no end date
├── Resources/         Reference material, guides, imported docs
├── Inbox/             Quick capture; the gardener files it later
├── Session-Logs/      One subfolder per project slug
├── Archive/           Completed/inactive items from anywhere above
├── Templates/         Note templates
└── System/
    ├── learnings/     One lesson per file (see extract-approach)
    ├── standards/     Pass/fail quality bars per deliverable type
    └── dashboards/    Optional overview notes
```

Projects/Areas/Resources/Archive is Tiago Forte's PARA method; Session-Logs and System are our additions — the session memory and the self-improvement machinery respectively.

2. **Write the brain's CLAUDE.md** at `{VAULT}/CLAUDE.md` from [references/brain-claude-md-template.md](references/brain-claude-md-template.md), filled in with the user's contexts. This file is the boot sector: registry table, conventions, tag taxonomy, and a pointer to the learnings index. Keep it under ~200 lines — it loads into every session, so every line costs tokens forever. The learnings index itself lives in `System/learnings/Learnings Index.md`, searched on demand, never inline here (an inline index grows without bound; ours hit 60KB before we moved it).

3. **Copy the note templates** from [references/](references/) into `{VAULT}/Templates/`: session log and project note. Adjust frontmatter fields to taste, but keep `type`, `project`, `tags`, `date` — the gardener audits against them.

4. **Wire the boot instruction** into the user's global `~/.claude/CLAUDE.md`:

```markdown
## Second brain (always)
My knowledge vault is at {VAULT}. At the start of every session: read
{VAULT}/CLAUDE.md (registry, conventions, learnings rules), identify which
project/context the task belongs to, and read that project's index note.
After every substantive session, write back before ending: a session log to
Session-Logs/{project-slug}/YYYY-MM-DD-HH_MM-topic.md, updates to any note
whose facts changed, and new learnings per the vault rules. Never mix
contexts across projects.
```

5. **Optional but recommended — install the write-back nudge hook** from [references/session-log-nudge.sh](references/session-log-nudge.sh) as a Claude Code Stop hook. It fires when a session ends without a recent session log and asks the model to write one (or explicitly decide the session was trivial). Discipline that depends on remembering fails; hooks don't forget. Show the user the script and where it goes (`settings.json` Stop hook) rather than installing it silently.

6. **Seed, don't backfill.** Create index notes for the 2-3 most active projects now; let the rest accrete through real sessions. An empty-but-correct structure beats a week of imported clutter the gardener has to untangle.

## Mode 2: OPERATE — the per-session ritual

**Session start (before the first substantive action):**
1. Read `{VAULT}/CLAUDE.md`.
2. Identify which registry context the task belongs to; read that project's index note.
3. Check `Session-Logs/{project-slug}/` for recent logs, and search `System/learnings/Learnings Index.md` for known pitfalls relevant to the task.

**Session end (before finishing, unless the interaction was trivial):**
1. Session log to `Session-Logs/{project-slug}/YYYY-MM-DD-HH_MM-topic.md`: what was done, decisions with rationale, open items, gotchas.
2. Update any index note, dashboard, or reference note whose facts changed. Link related notes with `[[wikilinks]]`.
3. New lessons → one file each in `System/learnings/` + one index line in `System/learnings/Learnings Index.md` — never in the brain's CLAUDE.md (the extract-approach skill covers what qualifies and the format). Log mistakes the moment they happen, not at session end.
4. Unsorted knowledge with no clear home → `Inbox/`.

**Standing rules:**
- The vault holds **knowledge only** (markdown). Code lives in repos; binaries (spreadsheets, PDFs) live in a documents folder and get *linked*, never copied in. The registry table maps knowledge ↔ code path ↔ context.
- **Never mix contexts.** Notes belong to one project/business; cross-cutting notes carry every context tag they genuinely touch.
- Folder index notes are **Title Case matching the subject** (`Acme Ops.md`), never `index.md`/`overview.md` — generic names make graphs and search unreadable.
- Tags are namespaced so trends are visible: `#ctx/<context>` (owning domain), `#theme/<topic>` (cross-cutting, controlled vocabulary), `#status/<active|done|archived>`. In YAML frontmatter, write tags hashless.
- Decisions get logged **with rationale** — a decision without its why is a fact you'll re-litigate.

## Why this compounds

Each mechanism feeds another: session logs keep index notes true; learnings prune every future model's search tree; standards sharpen the review-panel's rubric; the gardener keeps all of it findable. The loops are documented in [docs/second-brain.md](../../docs/second-brain.md) — read it once when adopting, and point skeptics at it when they ask why the setup pays rent.
