---
name: organize-agency
description: >
  Full-service file organization for donjon.agency (or any directory the user points at).
  Use this skill whenever the user mentions organizing files, cleaning up a directory,
  auditing what's in a folder, creating a file index, mapping project files, archiving
  old work, or running graphify on their agency. Trigger on phrases like: "organize my
  files", "clean up the agency folder", "what's in this directory", "archive old stuff",
  "map my projects", "run graphify on this", or any time the user points at a folder and
  wants it tidied up, understood, or restructured. This skill does it all in one pass:
  audit → reorganize → archive → graphify → index. Always use it when files and folders
  are involved — don't just manually move things without consulting this skill first.
---

# Organize Agency Files

You are performing a full audit, reorganization, archival, and knowledge-graph pass on one or more directories.

## Phase 0 — Confirm targets

If the user hasn't specified a directory, ask: "Which director(ies) should I organize? (Default: `/Users/clay/Desktop/donjon.agency`)"

Accept multiple paths. Process each one in sequence.

## Phase 1 — Audit (read before moving anything)

Keep the **agency-standard taxonomy** in mind as you audit — annotate each misplaced file with where it *would* go under that structure. This makes Phase 2's proposal faster and ensures your audit labels are immediately actionable.

**Taxonomy reminder:**
- Named-client files → `clients/<client-name>/deliverables/` or `clients/<client-name>/working/`
- Internal agency projects → `projects/<project-name>/`
- Images, diagrams, brand files → `assets/`
- Internal docs, playbooks, guides → `docs/`
- Agent configs, skills, automation → `agents/`
- Old/sent/superseded files → `archive/<year>/`

For each target directory:

1. Run `find <dir> -maxdepth 3 -not -path '*/\.*' | sort` to get a flat file list.
2. Note:
   - Files sitting **directly at the root** of the target (not in subdirs) — these are almost always misplaced; annotate where each would go under the taxonomy above
   - Files with "final", "v2", "FINAL", "copy", "backup" in the name — likely deliverables or duplicates
   - Files **not modified in 90+ days** — archive candidates (use `find <dir> -not -newer <date90daysago>` or `stat`; if macOS timestamp propagation means nothing is >90 days old, fall back to content signals: "final" names, sent deliverables, completed report series)
   - Recognized deliverable types at the root: `.pdf`, `.zip`, `.docx`, `.pptx`, `.html` (if they look sent/complete)
3. Print a short summary: counts by type, how many are misplaced, how many are archive candidates.

**Don't move anything yet.**

## Phase 2 — Propose structure

Reorganize into this **agency-standard taxonomy**:

```
<target>/
├── clients/
│   └── <client-name>/
│       ├── deliverables/   ← final PDFs, ZIPs, decks sent to client
│       └── working/        ← WIP docs, drafts, briefs
├── projects/               ← internal agency projects (not client-specific)
├── assets/                 ← images, fonts, brand files, templates
├── docs/                   ← agency docs, playbooks, internal guides
├── agents/                 ← agent configs, skill files, automation
├── archive/
│   └── <year>/             ← 90-day-old or already-sent files, sorted by year
└── INDEX.md                ← auto-generated map (you'll create this in Phase 4)
```

**Key judgment calls:**
- If a file's client is obvious from its name or neighboring context, put it under `clients/<client-name>/`.
- If uncertain, default to `projects/` and note the ambiguity in the INDEX.
- Existing `ARCHIVE` or `(ARCHIVE)` folders → fold their contents into `archive/<year>/`.
- Agent-related files (`.json` configs, skill markdown, automation scripts) → `agents/`.
- Images and brand assets → `assets/`.

Present the proposed moves as a clear **before → after list** grouped by destination folder. Ask: "Does this look right? I'll wait for your go-ahead before moving anything."

## Phase 3 — Execute moves (only after approval)

Once the user approves (or adjusts the plan):

1. Create any new directories needed.
2. Move files using `mv` — do NOT copy then delete.
3. For conflicts (two files with the same name going to the same place): keep both, append `-2` to the incoming file, and flag it in the output.
4. After all moves, run `find <target> -maxdepth 3 -not -path '*/\.*' | sort` again and confirm the directory looks right.

## Phase 4 — Generate INDEX.md

Write or overwrite `<target>/INDEX.md` with this structure:

```markdown
# Agency File Index
_Last updated: <date>_

## Directory Overview
<one-sentence description of what this directory is for>

## Structure
<tree view, 2-3 levels deep, with a one-line annotation per folder>

## Clients
| Client | Folder | Notes |
|--------|--------|-------|
| ...    | ...    | ...   |

## Projects
<brief bullet list of active projects found>

## Archive
<what was archived this pass and why>

## Generated by
organize-agency skill + graphify
```

## Phase 5 — Run Graphify

After the directory is reorganized and the index is written, run graphify to produce a knowledge graph.

### Check if graphify is available

```bash
which graphify || python -m graphify --version 2>/dev/null || echo "not found"
```

If graphify is **not installed**, tell the user:
> "Graphify isn't installed. You can get it from https://github.com/safishamsi/graphify — once installed, re-run this skill and I'll build the knowledge graph."
Then skip to Done.

If graphify **is installed**, run:

```bash
graphify <target> --output <target>/graphify-output/ --format html
```

(Adjust flags to match the actual graphify CLI — check `graphify --help` first if uncertain about flags.)

Report the output path so the user can open the HTML file.

## Done

Summarize what happened:
- Files moved: N
- Files archived: N
- INDEX.md: created/updated
- Graphify output: `<path>` (or "not installed")

Then ask: "Want me to do another directory, or is there anything you'd like to adjust?"
