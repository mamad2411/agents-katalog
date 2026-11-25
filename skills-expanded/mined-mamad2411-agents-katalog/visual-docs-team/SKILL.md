---
name: visual-docs-team
description: Generate a fully working React + Vite app that explains a codebase's workflows, data types, and architecture through interactive visuals — click-to-step animated walkthroughs with auto-play, sequence diagrams, animated packet tracers, message inspectors that toggle between named-field view and raw JSON, and collapsible code peeks with file:line citations. Splits the repo into 4–6 domain clusters and dispatches one content agent per cluster to write the pages in parallel. The skill bundles its own reference pages (under references/examples/) so it works in any repo. Use this skill whenever the user asks for interactive docs, animated explainers, an "agent team" for docs, one page per domain, wants to visualize a system's request flow or wire protocol, or any visual documentation site. Requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1 in .claude/settings.json.
---

# Visual docs team

A multi-phase workflow that turns a codebase into an interactive
docs site using parallel agents. One agent per domain cluster, all
running concurrently, all writing into disjoint files in the same
scaffold. The skill is repo-independent — drop it into any
`.claude/skills/` directory and it works.

## When to use

Trigger this skill when the user asks for documentation that goes
beyond plain markdown — animated explainers, interactive
walkthroughs, wire-format inspectors, or visual diagrams.

**What you'll produce** is a running React + Vite + Tailwind app.
Not markdown. Not static HTML. Not a generator. The user opens it
in a browser and clicks through it.

**Three explainer categories**, each backed by named components:

- **Workflows** → `Stepper` driving `PacketTracer` or
  `SequenceLane` (step-by-step animations: request flow,
  handshakes, lifecycle transitions, state machines).
- **Data types & wire formats** → `MessageInspector` (Fields ↔ JSON
  toggle), `CodePeek` (collapsible struct/SQL snippets with
  file:line citations), `Card` grids for schema columns.
- **Architecture & reference** → `ComponentNode`-based static
  diagrams, error matrices, API endpoint tables, vocabulary grids,
  custom SVG state diagrams.

Signal phrases that trigger this skill: "make beautiful docs",
"interactive docs", "agent team", "one page per domain",
"animate how my service handles requests", "explainer site for
my wire protocol", "visualize the architecture".

For a single markdown page or a one-off ASCII diagram, this is
overkill — recommend something lighter.

## Reference implementation

The skill bundles four working reference pages under
`<skill-dir>/references/examples/`, each demonstrating a distinct
structural pattern. **Content agents read the closest analog before
writing their cluster's page.** The pages contain real domain terms
(a Go orchestration project's wire protocol) — agents are told to
**ignore the content and mirror the structure**.

| Output cluster wants to explain… | Bundled reference |
| --- | --- |
| An end-to-end workflow / request flow | `examples/workflow-walkthrough.tsx` |
| A handshake or message lifecycle | `examples/sequence-handshake.tsx` |
| A data model / schema / state machine | `examples/data-model.tsx` |
| A landing page | `examples/landing.tsx` |

See `references/examples/README.md` for what to extract from each
file. The same patterns apply whether the host project is a Go
service, a Python web app, or a Rust CLI — only the prose and the
cluster names change.

## Phase 0 — Preflight: verify agent teams is enabled

Run the preflight script first. The skill dispatches multiple
background agents that run concurrently, which requires the
experimental agent-teams runtime.

```bash
bash <skill-dir>/scripts/check_agent_teams.sh
```

Exit 0 → continue. Exit 1 → STOP and show the user the JSON to add
(the script prints it on stderr). Do not try to work around a missing
flag — without it, parallel dispatch falls back to sequential and the
workflow loses most of its value.

If the user is on a fresh machine, prefer adding the env to the
project-local `.claude/settings.json` rather than the user-global one
— this keeps the flag scoped to projects that want it.

## Phase 1 — Clarify scope

Before any code touches disk, ask the user up to four short questions
using `AskUserQuestion`. These four are the same ones the original
workflow asked — they shape the entire downstream pipeline, so don't
skip them.

1. **Output format.** Recommend "Interactive docs site (Vite app)" by
   default. The scaffold this skill ships is Vite — alternative formats
   require abandoning the bundled assets.
2. **Topic clusters.** Multi-select. Pre-fill with the clusters you
   inferred from the repo survey (Phase 2). Let the user add or drop.
3. **Interactivity.** Animated walkthroughs vs. static diagrams. The
   bundled components support both; animated is the default.
4. **Audience.** Layered (both) / new-contributor / reviewer. Layered
   is the recommended default — each page leads with friendly prose
   then drills into struct-level detail.

If the user has already specified any of these in their initial
prompt, skip those questions.

## Phase 2 — Survey the repo and propose domain clusters

Read the project's orientation files before proposing anything:

- `AGENTS.md` / `CLAUDE.md` (these are usually symlinks to one another)
- `CONTEXT.md` if it exists
- `README.md`
- The module-map section of any of the above

Then run a quick survey:

```bash
ls -la <repo-root>
find <repo-root> -maxdepth 3 -type d -name 'internal' -o -name 'pkg' -o -name 'src' -o -name 'lib' | head -20
```

Identify 4–6 domain clusters. A good cluster has:
- a clear scope with no overlap with siblings
- maps to 1–2 doc pages
- corresponds to a coherent subsystem (not a random grab-bag)

Map each cluster to one of the four accent colors. The accents are
fixed by the scaffold's CSS: `arch` (green), `tunnel` (blue),
`shell` (amber), `auth` (violet). If you have more than four clusters,
let related clusters share an accent — adjacent topics on the same
color reads as grouped in the sidebar.

Present the cluster list back to the user (in Phase 1's question #2)
and confirm before proceeding.

## Phase 3 — Research pass

Dispatch ONE research agent with `subagent_type: Explore`. Its only
job is to produce a single markdown fact-sheet that all downstream
content agents will cite from. This avoids each content agent
re-grepping the same files and improves accuracy.

See `references/research-prompt.md` for the full prompt template. Fill
in the cluster-specific bullets (which files to read, which structs
and constants matter).

Save the result to `/tmp/<project-slug>-factsheet.md`. The path is
the contract between this phase and Phase 5.

Wait for the research agent to complete before continuing.

## Phase 4 — Audit existing UI stack, then scaffold

If the project has an existing frontend (e.g., `server/web`,
`frontend/`, `ui/`), read its `package.json` and primary CSS to
identify the design language — fonts, color palette, component
library. The docs site should feel like a sibling, not a stranger.

Then run the scaffold script:

```bash
bash <skill-dir>/scripts/scaffold_site.sh [base_dir]
```

`base_dir` defaults to `docs`. The script always creates a
**timestamped** target so every generation is a non-destructive
snapshot of the docs at a point in time:

    <base_dir>/site-YYYYMMDDTHHMMSSZ/

The timestamp is UTC ISO-8601 compact (e.g.
`docs/site-20260518T095612Z/`). Capture the printed `scaffold ready
at:` path — that's the directory the rest of the workflow operates
in. Pass it as `<docs-site-path>` to every subsequent command.

What the script does:
- Creates `<base_dir>/site-<UTC_TS>/` (will not clobber)
- Copies `assets/scaffold/` into it
- Writes `metadata.json` capturing the documented repo's git state
  (commit, short hash, branch, dirty status, remote URL, describe,
  HEAD message + author + committed_at)
- Runs `npm install`
- Rebuilds `<base_dir>/index.html` — the wrapper index that lists
  every previous run so the user can browse generations side by side
- Leaves the scaffold ready for project-specific customization

What the script does NOT do (you do these next):
- Write `src/lib/topics.ts` from the chosen clusters
- Write `src/App.tsx` with the cluster routes
- Write `src/pages/Home.tsx` (landing page)
- Write stub `src/pages/<Cluster>.tsx` files for every cluster
- Update `metadata.json` with the cluster list (do this in Phase 6,
  after the team finishes)

Templates for all four are in `references/templates.md`. Use them
verbatim, substituting cluster data. The bundled
`references/examples/landing.tsx` is a working reference for the
landing page structure.

**Smoke-test the empty scaffold build before dispatching content
agents:**

```bash
cd <docs-site-path>
npm run build 2>&1 | tail -25
```

Build must pass with stubs. If it fails at this stage, finding the
problem now (one orchestrator context) is far cheaper than finding it
inside four parallel agents.

## Phase 5 — Dispatch content agents in parallel

This is the heart of the workflow. One `general-purpose` agent per
cluster, all dispatched in **a single turn** with multiple Agent tool
calls so they run concurrently. Set `run_in_background: true` on each
— the orchestrator will get completion notifications instead of
polling.

See `references/content-agent-prompt.md` for the full prompt template.
Each agent receives:
- The cluster label, accent, and file list (their disjoint write
  targets)
- The fact-sheet path with their cluster section
- The path to `CONTRIBUTING.md` in the scaffold (the component API
  contract — also available at `references/components.md` in this
  skill)
- The expected page structure (PageHeader → Overview → Walkthrough →
  Wire → Reference)
- An instruction to run `npm run build` and fix any TS errors before
  returning

**File ownership rules** (these are why parallelism is safe):
- Each cluster owns one or two `src/pages/*.tsx` files
- Each cluster optionally owns `src/data/<cluster>.ts` for diagram
  data
- No agent touches shared components, the App, the topics file, or
  another cluster's pages

While the agents work, do not touch any files in `src/pages/` or
`src/data/`. You can write the README, polish unrelated files, or
just wait for notifications.

## Phase 6 — Integrate and verify

When all content agents have returned:

1. Run the combined build:
   ```bash
   cd <docs-site-path>
   npm run build 2>&1 | tail -30
   ```
   Each agent's individual build check doesn't catch type errors that
   only surface when all pages compile together. This is the
   integration test.

2. Update `<docs-site>/metadata.json` with the cluster list and any
   decisions from Phase 1. Use `Edit` or `Write` to merge keys — the
   file already has `generated_at`, `generator`, and `source`; add:
   ```json
   {
     "clusters": [
       { "key": "arch", "label": "Architecture", "accent": "arch" },
       { "key": "tunnel", "label": "Tunnel & wire protocol", "accent": "tunnel" }
     ],
     "format": "vite-react",
     "audience": "layered"
   }
   ```
   The `write_metadata.py` helper preserves these keys across re-runs,
   so the list is durable even if you later refresh the git state
   after a new commit.

3. Refresh the wrapper index so the new run's cluster chips show up:
   ```bash
   python3 <skill-dir>/scripts/rebuild_index.py <base_dir>
   ```
   The wrapper lives at `<base_dir>/index.html`. Each card on it
   shows date, branch, commit, dirty status, the HEAD commit message,
   the cluster chips, and direct links into that run's built bundle.

4. Host the wrapper and open it. This is the user-facing payoff —
   they shouldn't have to figure out the right `npm run preview`
   incantation or remember the dist/ path:
   ```bash
   python3 <skill-dir>/scripts/serve.py <base_dir>
   ```
   What this does:
   - Starts `python3 -m http.server` on port 4173 (or +1/+2 if busy)
     bound to 127.0.0.1, with `--directory <base_dir>`, fully
     detached so it survives this turn ending.
   - Writes `<base_dir>/.visual-docs-team.{pid,port,log}` so re-runs
     replace the previous server cleanly.
   - Opens the URL:
     - **Inside VS Code** (or a fork like Cursor — detected via
       `TERM_PROGRAM=vscode`, `VSCODE_PID`, or `VSCODE_IPC_HOOK`):
       prints the Cmd+Shift+P → "Simple Browser: Show" recipe with
       the URL pre-formatted for copy-paste. VS Code's CLI does not
       expose `simpleBrowser.show`, so a manual one-liner is the
       most reliable cross-version path.
     - **Outside VS Code:** opens the system default browser via
       Python's `webbrowser` module.
   - Pass `--external` to force the system browser even inside VS
     Code; pass `--no-open` to start the server silently.

   To stop the server later:
   ```bash
   bash <skill-dir>/scripts/stop_server.sh <base_dir>
   ```

5. Report to the user:
   - The live URL (`http://localhost:<port>/`) — the wrapper is open
     in front of them, this is just so they can re-find it
   - The timestamped target path (`docs/site-<TS>/`) and what commit
     it was generated from (read from `metadata.json`)
   - How to stop the server when they're done
     (`bash <skill-dir>/scripts/stop_server.sh <base>`)
   - File inventory (`find <docs-site>/src -name '*.tsx' -o -name '*.ts' | xargs wc -l`)
   - Combined gzipped size from the build output
   - How to run dev with hot reload
     (`cd <docs-site> && npm run dev`)

## Orchestration anti-patterns

These are the failure modes the original workflow hit and recovered
from — avoid them.

### Tailing agent transcripts

The agent's JSONL output file is enormous and will blow your context
window. The completion notification already contains the summary, the
token count, and the duration. Trust it.

### Writing pages while agents run

If the orchestrator writes a page file at the same time as a content
agent, last-write-wins. Always finish your scaffold writes before
dispatching. Once dispatched, only touch files outside `src/pages/`
and `src/data/`.

### Skipping the empty-build smoke test

It's tempting to dispatch agents immediately after scaffolding. Don't.
A typo in `src/lib/topics.ts` or `src/App.tsx` will fail every single
agent's build verification, and you'll spend an hour debugging four
parallel transcripts to find one mistake the orchestrator made. The
30-second `npm run build` after writing stubs catches every such bug
upfront.

### Reusing fact-sheet across very different projects

The fact-sheet is project-specific. If the user runs the skill again
on a different codebase, generate a new fact-sheet with a new slug
(`/tmp/<project-slug>-factsheet.md`).

### Hand-editing the timestamp out of the path

Don't. The timestamp is the provenance — every generation is a
snapshot tied to a specific commit. If the user wants a stable URL
like `<base>/latest/`, recommend a symlink:

```bash
ln -sfn site-<TS> docs/latest
```

Renaming the directory breaks the link between the docs and the
`source.commit` recorded in `metadata.json`.

### Inventing new accent colors

The four accents (`arch`, `tunnel`, `shell`, `auth`) are baked into
the CSS at multiple places. Adding a fifth accent means updating
`src/index.css`, `src/lib/topics.ts`'s `accentClasses` helper, and the
`Badge`/`Callout` variant maps. If you have more than four clusters,
group them and share accents — don't add new ones at the orchestrator
layer.

## Files in this skill

| Path | Purpose |
| --- | --- |
| `scripts/check_agent_teams.sh` | Phase 0 preflight |
| `scripts/scaffold_site.sh` | Phase 4 scaffold copy + install (creates `<base>/site-<TS>/`) |
| `scripts/write_metadata.py` | Phase 4 metadata.json writer (idempotent, preserves user keys) |
| `scripts/rebuild_index.py` | Phase 4/6 — rebuilds `<base>/index.html`, the wrapper listing every run |
| `scripts/serve.py` | Phase 6 — hosts `<base>/` over HTTP and opens it (VS Code Simple Browser when available, else system browser) |
| `scripts/stop_server.sh` | Stops a server started by `serve.py` |
| `assets/scaffold/` | Vite app shell + shared components + CONTRIBUTING.md |
| `references/research-prompt.md` | Phase 3 — research agent prompt template |
| `references/content-agent-prompt.md` | Phase 5 — content agent prompt template |
| `references/components.md` | Component API contract (mirrors CONTRIBUTING.md) |
| `references/templates.md` | topics.ts / App.tsx / page stub templates |

## Quick mental model

```
Preflight ─▶ Clarify ─▶ Survey ─▶ Research ─▶ Scaffold + stubs ─▶ Dispatch ─▶ Integrate ─▶ Serve
   (1)        (4 Qs)   (clusters) (1 agent)   (orchestrator)     (N agents)   (1 build)    (open)
                                                                 parallel
```

Each arrow is a phase boundary you should not cross until the previous
phase verifies cleanly. The pattern is: do the work that's hard to
parallelize sequentially, then explode into a parallel team for the
content, then converge back for the integration verify.
