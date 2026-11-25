---
name: cc-wiki
description: Distill the user's `~/.claude` history into a Quartz knowledge base. Runs preprocess.py, dispatches parallel project-digest agents, then parallel cross-cutting synthesis agents (people / companies / projects / concepts / workflows / tools / playbooks), writes the spine, installs Quartz, and starts the dev server. Single command, no flags required.
argument-hint: "[output-dir, default ./my-kb]"
allowed-tools: Read Write Edit Bash Glob Grep Task TaskCreate TaskUpdate
model: claude-opus-4-7
---

# cc-wiki — Claude history → Quartz knowledge base

When the user runs `/cc-wiki [dir]`, build a complete Quartz vault from their
`~/.claude/` history. Five phases. The first and last are mechanical; the
middle three dispatch parallel subagents. End-of-run prints the localhost URL.

Default output dir: `./my-kb`. If the user passes `[dir]`, use that. If the
directory already exists and is non-empty, ask once before overwriting.

If the user has copied another account's Claude data to a custom location,
they can mention it inline (e.g. `/cc-wiki --source ~/backup-claude`) — pass
the same `--source <path>` to preprocess.py in Phase 1. Otherwise default to
`~/.claude`.

`<SKILL_DIR>` resolution: `~/.claude/skills/cc-wiki/` (installed by install.sh).
Templates and scripts live under `<SKILL_DIR>/templates/` and
`<SKILL_DIR>/scripts/`.

## Phase 0 — Scaffold

```
Bash(mkdir -p <dir>)
Bash(cp -R <SKILL_DIR>/templates/quartz/. <dir>/)
Bash(cp -R <SKILL_DIR>/templates/spine-defaults/. <dir>/)
```

The Quartz template includes `quartz/`, `quartz.config.ts`, `quartz.layout.ts`,
`package.json`, `tsconfig.json`, `vercel.json`, `kb.py`, and a starter
`internal/` skeleton. The spine defaults are empty stubs for `index.md`,
`methodology.md`, `arc.md`, `glossary.md`, `open-questions.md`,
`disambiguation.md` — Phase 4 fills them.

## Phase 1 — Pre-process

```
Bash(python3 <SKILL_DIR>/scripts/preprocess.py --out <dir>/internal [--source <path>])
```

Reads `~/.claude/history.jsonl` + `~/.claude/projects/**/*.jsonl` (or
`<path>/history.jsonl` + `<path>/projects/**/*.jsonl` if `--source` is set). Writes:

- `<dir>/internal/prompts/{project_slug}.md` — chronological prompt log per project (chunked by month when > 400 prompts)
- `<dir>/internal/sessions/{slug}/{session_id}.md` — per-session digest
- `<dir>/internal/subagents/{slug}/{session_uuid}/agent-*.md` — subagent transcripts
- `<dir>/internal/project-overview.{md,json}` — authoritative project → corpus mapping (agents use this)
- `<dir>/internal/session-inventory.{md,json}` — counts and date ranges

If no sessions are found, stop and report: `No sessions in ~/.claude/projects/. Nothing to build.`

If the user has fewer than ~50 prompts total, warn that the output will be thin
but proceed (some signal is better than none).

## Phase 2 — Project digests (parallel agents)

Read `<dir>/internal/project-overview.json` to get the list of projects with
prompt counts. Group them:

- **Big projects** (>200 prompts): one dedicated agent each
- **Medium** (50-200): one agent each
- **Small** (<50): bundle 3-5 into a single "cluster" agent

For typical users you'll dispatch **5-12 agents in parallel** in a single
message. Each agent gets the project-digest prompt template
(`<SKILL_DIR>/templates/prompts/digest-project.md`) with project-specific
substitutions: project path, slug, prompt file paths, session/subagent dir
paths, and total prompt count.

The template instructs the agent to:
1. Read all assigned prompt files chronologically (not skim)
2. Sample 5-15 session/subagent transcripts for depth
3. Write `<dir>/internal/project-digests/{slug}.md` with fixed schema
   (TL;DR → strands → people → companies → tools → concepts → workflow obs →
   cross-project connections → notable verbatim prompts → open threads)

The template requires verbatim quotes (no paraphrasing) and `[[wikilinks]]`
for every person/company/concept mentioned.

Wait for all agents to finish before Phase 3.

## Phase 3 — Cross-cutting synthesis (parallel agents)

Dispatch six agents in parallel, one per axis. Each reads ALL project digests
from Phase 2 and writes its assigned output dir. Templates under
`<SKILL_DIR>/templates/prompts/synthesize-{axis}.md`:

| Axis | Output dir | Template |
|---|---|---|
| People | `<dir>/people/` | `synthesize-people.md` |
| Companies | `<dir>/companies/` | `synthesize-companies.md` |
| Projects | `<dir>/projects/` | `synthesize-projects.md` |
| Concepts | `<dir>/concepts/` | `synthesize-concepts.md` |
| Workflows | `<dir>/workflows/` | `synthesize-workflows.md` |
| Tools & Playbooks | `<dir>/tools/` + `<dir>/playbooks/` | `synthesize-tools-playbooks.md` |

Each output dir gets its own `index.md` plus one page per entry.

Wait for all six to finish before Phase 4.

## Phase 4 — Spine (you do this directly)

Write six files with full context of what Phases 2 and 3 produced:

- `<dir>/index.md` — landing
- `<dir>/methodology.md` — how this KB was built (cite the pipeline)
- `<dir>/arc.md` — chronological narrative of the user's six months (or however long)
- `<dir>/glossary.md` — distilled vocabulary, grouped by category
- `<dir>/open-questions.md` — unresolved threads, including stated-vs-observed tensions
- `<dir>/disambiguation.md` — name collisions flagged by Phase 3

Use `<SKILL_DIR>/templates/spine-defaults/*.md` as starting structure but
fill them with the specific evidence from the run. The arc should be a
single-read narrative — past tense, dated milestones.

## Phase 5 — Build and serve

```
Bash(cd <dir> && npm install --silent)
Bash(cd <dir> && python3 kb.py build)             # generate .index.json
Bash(cd <dir> && npm run dev)                     # background
```

`npm run dev` starts the Quartz server at `http://localhost:8080`. Run in
background and surface the URL.

Final message to the user:

```
Built {N} pages from {M} prompts. Open http://localhost:8080.

Spine: index, arc, glossary, methodology, open-questions, disambiguation
Content: {p_count} projects, {ppl_count} people, {co_count} companies,
         {c_count} concepts, {w_count} workflows, {t_count} tools, {pb_count} playbooks

⚠️ This vault names real people and unredacted strategy. Don't deploy public without a redact pass.
```

## Hard rules

- **One command, no flags.** If the user passes `[dir]`, use it. Otherwise default `./my-kb`. No other arguments.
- **Phases 2 and 3 dispatch in parallel via the Task tool in a single message.** Don't fan out sequentially — costs 5-10× more wall time.
- **Verbatim quotes only.** Every person / decision / pivot in the synthesis must trace back to a quoted prompt from the digest. Forbidden to paraphrase load-bearing claims.
- **`[[wikilinks]]` everywhere.** Pre-resolve to lowercase-kebab slugs. Aliases go in frontmatter.
- **Don't touch `~/.claude/`.** Read-only. Pre-processor never writes back.
- **No network calls except LLM API.** The preprocessor is stdlib; Quartz is local-build.
- **If `npm install` fails**: report the error, suggest `nvm use 22`, and stop. Don't try to repair.
- **If a Phase 2 or Phase 3 agent fails**: continue with the others, then report which axes have gaps. The KB is still useful with one axis missing.
- **Don't write inside `<SKILL_DIR>/`.** Treat it as read-only at runtime; everything goes under `<dir>`.

## Failure modes

- **Empty history**: `No sessions found in ~/.claude/projects/.` Stop.
- **Single tiny project (<50 prompts)**: build succeeds but warn output will be thin.
- **`history.jsonl` missing** (older Claude Code installs): fall back to session JSONL alone; the corpus is still usable, just missing the project-tagged prompt spine.
- **Agent returns malformed digest**: re-dispatch that one agent only with `Retry with stricter adherence to the digest schema.` Don't retry more than once.
- **YAML frontmatter error in synthesized page**: the page-template forbids unquoted titles with colons / quotes. Phase 3 templates emphasize this.

## What this skill does NOT do

- Doesn't pick which projects matter — every project gets analyzed.
- Doesn't push to GitHub or deploy to Vercel.
- Doesn't redact for public use.
- Doesn't run behavioral analysis on the sessions (no session-quality metrics, no model-regression detection).
- Doesn't update across runs — re-running re-builds from scratch. (Future: incremental refresh.)
