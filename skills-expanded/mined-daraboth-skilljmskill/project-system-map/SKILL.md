---
name: project-system-map
description: Build an architecture and project document for any codebase (web server, mobile app, desktop app, monorepo) as one interactive, bilingual (Korean and English) HTML page with AWS architecture-icon diagrams, a click panel on every box and step, What / How / Why cards, a sidebar of tabs, a generated database schema tab, Save as Markdown, and a single offline HTML file. Use it whenever someone asks to document a system's architecture, containers, cloud layout, runtime flows, data model, HTTP API, screens or role processes "so a developer can understand everything", wants onboarding docs or a system map, or asks to update such a document, even if they do not name this skill. Works in Claude Code and Codex.
---

# Skill: System map document

> **Purpose**: Turn a codebase into a document a new developer can read top to bottom and trust: every claim cited to a pushed commit, every diagram box explained, in Korean and English.

## When to Use
- "Document the architecture / the whole project / every flow" for a repo: a web server, an API, a mobile app, a desktop app, a library, a monorepo
- "Draw it like AWS architecture diagrams", "explain it so a new developer understands everything", onboarding docs
- A data model or database document, an API reference generated from the code, role or user-journey flows
- Updating an existing system map after the code moved on

A worked example lives in `examples/demo/`: sources for every file the build reads (it documents this kit itself, with `rev: 'WORKTREE'`). Copy its shapes, never its content. `examples/demo-output.html` is what those sources build. `examples/sample-output.html` is a finished document for a real, larger project (addresses replaced with placeholders): open both in a browser to see the target structure and style before you start.

---

## What you deliver
1. A claude.ai artifact: `index.html` (sidebar of tabs, notes) plus `diagrams/<name>-map-<lang>.html` (one page per diagram and language, loaded in iframes).
2. A single offline file with every diagram embedded (`build-single.mjs`). Give the user its path.
3. A "Save as Markdown" pair in the header (This tab / Whole document), from `md-export.js`, which `build-page.mjs` inlines. It saves in the language on screen; each diagram becomes a list of its boxes with their explanations and code links. On claude.ai it saves through the `downloads` capability, so publish with `capabilities: {downloads: true}`; opened from disk it falls back to a plain browser download.

## House rules (do not skip)
1. **Architecture and project doc, not a user manual.** Screens appear only as "screen calls which API".
2. **Bilingual everywhere.** Every sentence as `<span class="ko">…</span><span class="en">…</span>` or a ko/en pair. Korean in 해요체 with easy words. No em dashes, no emoji, no AI filler words.
3. **AWS icon style for every diagram**: white canvas, official AWS icons, rounded soft groups, a legend panel on the right with icon, title and one line, a title plus subtitle. The renderer does this; do not hand-draw.
4. **Every clickable box and step has a plain explanation**, never only a file link. `find-empty.mjs` must print "every item has an explanation".
5. **Cite `path:line` at a pushed commit.** Unpushed commits make every GitHub link 404. `check-cites.mjs` must report 0 problems.
6. **No "open decisions / risks / TODO" tab.** Findings go to the project's owner (a `findings-<date>.md` beside the work folder, each item with path:line) to triage and file. The document states how things are.
7. **Under every diagram**, a What / How / Why card row (`www-data.mjs`).
8. **Role flows draw every branch**: decision diamonds, end circles, plus an "Every branch" table on the tab.
9. **Header shows only** created and last-updated dates (plus a counts row). No repo/branch/commit chips.
10. **Never invent infrastructure** (CIDRs, AZs, regions). Draw what the code proves; mark the rest "assumed, confirm with infra".
11. Notes use the full width; boxes sit in two columns on wide screens.
12. **A Database schema tab is required**: every collection, every field (type, rules, meaning), every index and why, generated from the schema files, never copied by hand. How: `references/schema-tab.md`.

---

## Claude Code or Codex
The scripts are plain Node (20+) and git; both agents run them the same way. Only the helpers differ:
| step | Claude Code | Codex |
|---|---|---|
| Research (step 3) | `Agent` tool, `subagent_type: researcher`, all prompts in one message | run each prompt yourself, one after another, and save each result to a notes file before the next |
| Browser check (step 7) | Playwright MCP (`browser_run_code_unsafe` with `page.route`) | Playwright MCP if configured; otherwise `npx playwright screenshot` against a local `python -m http.server` in `out/`, or skip and say so |
| Publish (step 8) | the `Artifact` tool, if this session has it; otherwise as Codex | no artifact: deliver `out/` (index.html + diagrams/) and the single offline file, and give both paths |
| Findings for the owner (rule 6) | `findings-<date>.md` beside the work folder, and tell the user | write them to `findings-<date>.md` beside the work folder and tell the user where it is |
| Language of replies | follow the user's style rules | same |

Never claim a check you could not run in your agent (for example "visually checked" without a browser).

---

## Workflow

### 1. Pin the commit (5 min)
```bash
git -C <repo> fetch origin
git -C <repo> log -1 --format='%H %ad' origin/<branch>   # document THIS sha
git -C <repo> rev-list --count <old-sha>..origin/<branch> # when updating: how far it moved
```
Put the full sha in `map-config.mjs` (`rev`). Read code only with `git show <rev>:<path>` and `git grep <pattern> <rev>`; other agents may be working in the tree.

### 2. Plan the tabs
Start from the tab menu in `references/page-writing.md` (Overview, Building blocks, Deployment, Runtime flows, Data, Interfaces, Roles, Project) and the set for the project type below. Drop what the system lacks; add a tab per major subsystem. Order the sidebar the way a new developer should read it.

| project type | tabs that usually earn their place |
|---|---|
| web server / API | overview, containers or processes, cloud and network, release and deploy, one tab per key request flow (sign-in, the main write path, background jobs), data and statuses, database schema, HTTP API, roles, working on the code |
| mobile app | overview, app structure (modules, state, navigation), screens and navigation map, sign-in and session, offline storage and sync, push notifications, the backend it calls (API tab or a link), local database schema, release to the stores (build, signing, versions, feature flags), roles or user journeys, working on the code |
| desktop app | overview, processes (main, renderer, helpers) and IPC, windows and screens, local storage, auto-update and signing, the backend it calls, release, working on the code |
| library / SDK | overview, public API surface, internal modules, data formats it reads or writes, versioning and release, how products use it, working on the code |
| monorepo | overview, one building-blocks tab per app, shared packages, release and deploy per app, then the flows that cross apps |

### 3. Research in parallel
If your agent can run helpers in parallel, give each topic its own helper, plus one fact-checker if a document already exists; otherwise run the prompts yourself one after another. Prompts: `references/research-prompts.md`. Every agent reads only at `<rev>`, never prints secrets, and returns `path:line` facts plus a SEQUENCE or FLOW list ready for a diagram.

**Save each report to a notes file as it arrives.** Long sessions compact; reports in chat get lost.

### 4. Set up the work folder
```bash
mkdir work && cd work
cp <skill>/scripts/*.mjs <skill>/scripts/md-export.js .   # lib.mjs is shared by every script
mkdir pages && cp <skill>/scripts/page.css pages/
# AWS icons (aws-icons 3.3.0, MIT, official AWS set). Untrusted download: own folder, read SVGs only.
mkdir dl-aws-icons && curl -sSL -o dl-aws-icons/aws-icons.tgz https://registry.npmjs.org/aws-icons/-/aws-icons-3.3.0.tgz
tar -xzf dl-aws-icons/aws-icons.tgz -C dl-aws-icons
```
Copy `examples/demo/*.mjs` and edit them. Look at `examples/demo/` and `examples/demo/pages/` for every other file's shape.

### 5. Write the diagrams
- `map-data.mjs`: one entry per diagram. Three kinds: `free` (architecture, authored coordinates), `lanes` (role flows, auto layout), `sequence` (runtime flows, auto layout). Schema: `references/diagram-data.md`.
- `details.mjs`: shared explanations referenced by `info: 'set.key'`.
- `map-explain.mjs`: fills anything `find-empty.mjs` lists.

### 6. Write the tab pages
`pages/<tab id>.html`, one per tab: lead, figure, notes. Rules and building blocks: `references/page-writing.md`. Big tables (routes, tools) are generated by a small script that follows the pattern of `gen-schema.mjs` (see "Generated tables" in `references/page-writing.md`).

### 7. Build and verify
```bash
node gen-schema.mjs --sql "<migrations glob>"   # or --prisma / --json; pages/schema.generated.html
node check-cites.mjs     # 0 problems
node find-empty.mjs      # every item has an explanation
node build-maps.mjs      # out/diagrams/*
node add-www.mjs         # What / How / Why rows
node build-page.mjs      # out/index.html
node check-tags.mjs      # all balanced
node build-single.mjs    # out/<singleFileName>
```
Then look at every diagram in a real browser (Playwright: `page.route()` plus `route.fulfill({ path })`, because `file://` is blocked). Screenshot each one. Fix overlapping labels with `at` / `anchor` / `side` / `offset`. Check both languages, dark mode, and a 390 px phone width.

### 8. Publish
If your agent can publish to claude.ai (the Artifact tool), publish `out/index.html` with `root` set to `out`, a `files` map of every `diagrams/*.html`, and `capabilities: {downloads: true}` for the Markdown buttons. Otherwise hand over the single offline HTML file and the `out/` folder, and give both paths. Map old files to `null` to delete them. Same file path every time keeps the URL. Give the single-file path too.

### 9. Report
State what changed, what you verified (and how), and what you did not (for example "did not open the published link"). Name the commit the document describes.

---

## Top gotchas (full list: `references/gotchas.md`)
- **The documented commit must be pushed**, and check `origin` again before you publish: teammates push during the day.
- **Fact-check claims about what code does at runtime.** One "deploy invalidates CloudFront" turned out to be a no-op binding.
- **Shell heredocs in this harness eat backslashes**; the Write tool turned a ` ` escape into the raw character. Build escapes with `String.fromCharCode(92)`.
- **`'…'.replace(a, b)` turns `$$` in `b` into `$`.** Use `split(a).join(b)` for code that contains `$`.
- A claude.ai artifact page is a fragment with no charset; open it locally only through the single-file build.

---

## Files in this skill
| file | job |
|---|---|
| `scripts/lib.mjs` | shared helpers: loading the sources, text, citations, git reads, explanation lookup |
| `scripts/check-cites.mjs` | every `path:line` exists at `rev`, and `rev` is pushed |
| `scripts/find-empty.mjs` | every clickable item and every What / How / Why has both languages |
| `scripts/build-maps.mjs` | renders `free`, `sequence` and `lanes` diagrams to `out/diagrams/` |
| `scripts/add-www.mjs` | puts the What / How / Why row under each figure in `pages/*.html` |
| `scripts/build-page.mjs` | assembles `out/index.html` (header, sidebar, tabs, links, scripts) |
| `scripts/check-tags.mjs` | balanced tags in the output and the pages |
| `scripts/build-single.mjs` | one offline HTML file with every diagram embedded |
| `scripts/gen-schema.mjs` | the Database schema tab from SQL migrations, Prisma, or an adapter's JSON |
| `scripts/md-export.js` | Save as Markdown (inlined by `build-page.mjs`) |
| `scripts/page.css` | the page style, light and dark |
| `references/*.md` | diagram data, page writing, research prompts, schema tab, gotchas |
