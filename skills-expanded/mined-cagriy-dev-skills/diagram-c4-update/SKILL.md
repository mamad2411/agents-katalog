---
name: diagram-c4-update
description: Generate or refresh an interactive C4 architecture diagram for the current project — a single self-contained HTML page the reader drills down through, system context to containers to components. Use when the user wants an architecture diagram, a C4 model, a system/container/component diagram, or a visual map of how the project is put together. Runs in any repo — a conventional software project, a plugin or agent-asset repo, or a repo that is only architecture documents — classifying the repo first and grounding the model in whatever evidence it actually has. Writes exactly two files, diagram/c4-model.json (the reconciled source of truth, Structurizr-workspace compatible) and diagram/c4.html (rendered wholesale from templates/c4-diagram.html by token substitution — the template owns all presentation; this skill authors data only). Accepts an optional mode: fresh re-derives everything, render re-renders the model on disk without re-deriving it. Read-only towards everything except those two files; never commits or pushes. Step 0 confirms with the user before doing any work when invoked proactively; the confirmation is skipped when the user explicitly typed /diagram-c4-update.
user-invocable: true
disable-model-invocation: false
argument-hint: "[fresh|render]"
allowed-tools: Read, Write, Grep, Glob, Bash(git *), Bash(ls *), Bash(find *), Bash(mkdir *), Bash(test *), Bash(date *), Bash(jq *), Bash(mv *), Bash(basename *), Bash(pwd), Bash(wc *)
---

# diagram-c4-update — Interactive C4 architecture diagram

You are running the `diagram-c4-update` skill. Your job is to build a **C4 model of the current project** and render it as one self-contained, interactive HTML page the reader can drill down through: system context → containers → components. The page is produced by substituting per-run **data** into the plugin template `templates/c4-diagram.html`, which owns all presentation, interaction and geometry; this skill never authors the page from scratch and never hand-tunes the engine in the output.

**This skill runs in any repo.** Unlike its sibling `/diagram-update`, which refuses outside the dev-skills plugin repo, this one is portable by design: a conventional software project, a plugin or agent-asset repo, or a repo that is nothing but architecture documents. Step 2 classifies the repo and that classification decides *what to read* — nothing else.

**The model is not purely re-derivable, and that is the other thing that separates this skill from `/diagram-update`.** Where the system boundary sits, whether a unit is a container or a component, and whether several services are one system or many are judgement calls, not facts on disk (`docs/c4-model.md` §2.2–§2.4, §10.1). So `diagram/c4.html` is regenerated wholesale every run — it holds no state — while `diagram/c4-model.json` is **reconciled**: recorded decisions and hand-tuned coordinates survive, and nothing is ever silently deleted.

This skill has twelve steps (Steps 0–11). Execute them in order.

## Step 0 — Confirm before proceeding (when invoked proactively)

Check the most recent user message for the literal tag `<command-name>/diagram-c4-update</command-name>` (or, equivalently, a leading `/diagram-c4-update` typed by the user). If present, skip this step and continue with Step 1.

Otherwise (proactive invocation from natural-language intent), ask once via `AskUserQuestion`:

- **Question**: "Build an interactive C4 architecture diagram for this project? Writes `diagram/c4-model.json` and `diagram/c4.html`."
- **Options**: "Yes, build it" / "No, skip".

On anything other than an explicit yes, stop without touching the filesystem. This gate is separate from the Step 6 clarification round and is never merged with it.

## Step 1 — Resolve root, mode, template and any existing model

- `git rev-parse --show-toplevel` → `project_root`. If it fails, use `pwd` and say in one line that the run is not repo-scoped — a folder of architecture documents need not be a git work tree. **Never refuse on repo identity.**
- `repo_name` = `basename "<project_root>"`. `generated_at` = `date -u +"%Y-%m-%d %H:%M UTC"`.
- Parse `$ARGUMENTS`: empty → `reconcile` (default); `fresh` → set any existing model aside and re-derive everything; `render` → skip Steps 2–7 and re-render the model already on disk. Any other token stops the skill with one line: `diagram-c4-update: refused — unknown argument '<token>'; expected 'fresh', 'render', or nothing.` Never guess at a best-effort reading.
- `template_file` = `templates/c4-diagram.html` inside this plugin. Verify it exists and contains all seven tokens listed in Step 8. If it is missing or has drifted, stop with one line: `diagram-c4-update: refused — templates/c4-diagram.html is missing or has drifted from this skill's contract.` Do not fall back to authoring the page by hand.
- `test -f "<project_root>/diagram/c4-model.json"`. If present, read and parse it as `prior_model`. In `fresh` mode, `mv` it to `diagram/c4-model.<UTC>.json` first and treat the run as cold. If it exists but does not parse, `mv` it to `diagram/c4-model.json.broken-<UTC>`, continue cold, and report it — never attempt to reconcile against a broken file.
- Also `test -f "<project_root>/diagram/index.html"` — its presence decides `{{C4_WORKFLOW_LINK}}` in Step 8.

## Step 2 — Classify the repository

Evaluate in this order; **first match wins**. Plugin signals are tested before manifests deliberately — an agent-asset repo often carries a `pyproject.toml` for its own test harness and would otherwise misclassify as software.

- **Prior formal model** (a modifier, not a class): any of `workspace.dsl`, `workspace.json`, `**/*.c4`, `**/*.likec4`, a `*.puml` containing `C4_Context`/`C4_Container`/`C4_Component`, or a markdown fence opening `C4Context`/`C4Container`/`C4Component`. Read it first in every class and treat its elements and relationships as authoritative, deriving only what it omits.
- **Plugin / agent-asset**: `.claude-plugin/plugin.json`; two or more `skills/*/SKILL.md`; `hooks/hooks.json`; `commands/*.md` with `agents/*.md`; a root `.mcp.json` defining servers; or `AGENTS.md` / `.cursor/rules/` / `.github/copilot-instructions.md` with no application entrypoint.
- **Software**: any application dependency manifest (`package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, `pom.xml`, `build.gradle*`, `*.csproj`, `Gemfile`, `composer.json`, `mix.exs`, `pubspec.yaml`, `Package.swift`, `CMakeLists.txt`) **or** any deploy descriptor (`Dockerfile*`, `docker-compose*.y*ml`, `Procfile`, `*.tf`, `serverless.y*ml`, a YAML with `kind: Deployment|StatefulSet|CronJob|Service`, `Chart.yaml`, `fly.toml`, `vercel.json`, `app.yaml`).
- **Documents**: markdown/adoc/rst dominate the tracked files and the only manifest is a docs-site one (`mkdocs.yml`, `docusaurus.config.*`, `_config.yml`, `book.toml`, `docs/conf.py`). Corroborated by `docs/adr/**`, `adr/**`, `*arc42*`, `docs/architecture/**`, `rfcs/**`.
- **Fallback**: software, noted as "no manifests found; grounded from source layout only".

Record the class and the exact paths that decided it — both go in the Step 10 report.

## Step 3 — Ground: harvest the evidence

Read the universal set in every class — `README*`, `ARCHITECTURE*`, `CLAUDE.md` / `AGENTS.md`, `CODEOWNERS`, `CONTRIBUTING*` — plus the class-specific set:

- **Software** — deploy descriptors first, because they name the deployable units directly (compose services, k8s workloads, Terraform `aws_lambda_function` / `aws_ecs_service` / `google_cloud_run_service`, `serverless.yml` functions, Procfile process types). Then per-service manifests, for technology strings taken from *actual* dependency names. Then entrypoints (`main.*`, `cmd/*/main.go`, `manage.py`, `server.*`, `index.*`). Data stores from compose images, migration directories, ORM config and IaC bucket/table/queue resources. External systems from third-party SDK dependencies, outbound base URLs, OAuth providers and webhook receivers. People from auth roles, route guards, admin surfaces, CLI entrypoints and the README's stated audience. `CODEOWNERS` specifically answers the ownership heuristic behind the container-vs-system call.
- **Plugin / agent-asset** — the manifest, every `skills/*/SKILL.md`, `hooks/hooks.json` and each script it references, `commands/`, `agents/`, `.mcp.json`, `templates/`, `scripts/`. The mapping that matters, because the C4 literature is silent on this repo shape: the plugin as installed is the **software system**; the agent runtime, the target project repo, the git forge and each MCP server are **external systems**; the things the harness runs or stores as separate units are **containers** — the skill-definition set, each hook script, the template set, each artefact store the plugin writes; individual skills are **components** inside the skill-definition container. The worked deployability call to apply: *a skill is not separately deployable — it is loaded into the agent's context — so it is a component; a hook script is executed as its own process, so it is a container.*
- **Documents** — prior formal model, then ADRs, then arc42 / RFC / design docs, then the README. Extract elements from prose: proper nouns in headings, service tables, "X calls Y" sentences, ADR titles. Note diagram image files by path but never infer their content from a filename.

**Attach an evidence pointer to every candidate** — `path:line`, `doc:<path>#<heading>` or `manifest:<path>#<key>`. Anything you cannot cite is not a candidate. This skill never invents architecture: an under-evidenced element is reported in Step 11 as *not modelled*, not guessed onto the diagram.

## Step 4 — Derive the candidate model

Apply the abstraction rules in `docs/c4-model.md` §2 — the mapping is a judgement, not a transcription:

- **Deployability decides container vs component.** A unit with its own start command, process, workload, function or cron entry is a **container**; anything living inside another unit's process is a **component**. A shared library is a component wherever it is used, never a container.
- Docker containers, pods, VMs and load balancers are **deployment nodes** — excluded entirely from these views (§2.3, §10.3).
- A single-page app and the server that delivers it are **two containers** (§10.3).
- Serverless functions are containers, not systems (§10.1).
- **External systems are modelled at the boundary only** — never their internals (§11).
- Queues and topics: with four or fewer, model each as its own container (explicit); beyond that, omit them and name them in the relationship labels (implicit). Either is legitimate — §10.2 — but be consistent within a diagram and record which you chose.

Every element gets a name, an explicit type tag, and a one-line responsibility description. Every **container and component** gets a `technology` string derived from a manifest — never guessed; if it cannot be evidenced, say so in the description rather than inventing a framework. Every relationship gets a direction, an intent label and — where it crosses a process boundary — a protocol.

Record each self-decided judgement in the model's `c4.decisions[]` with a one-sentence rationale citing the governing section.

## Step 5 — Reconcile with any existing model

Skip in `fresh` mode. Otherwise merge the candidate into `prior_model` under these ownership rules:

| Field | Behaviour on re-run |
|---|---|
| Element / relationship existence | Re-derived. New ones are added. Ones no longer evidenced are **retired** to `model.retired[]` with the date and their last evidence pointer — never deleted. A retired element that reappears is restored with its old cell. |
| `name`, `description`, `technology`, relationship labels | Re-derived **unless the user hand-edited them**. Every run stamps what it would have written into `properties["c4.generated.<field>"]`; a field whose on-disk value differs from that stamp is treated as hand-edited and left alone. |
| `col` / `row` | **Preserved** for every surviving element whose semantic band (Step 7) is still correct. Re-placed only on a band change or a collision; every re-placement is counted as a *moved* in the report. |
| `x` / `y` / `dimensions` | Always re-derived from `col`/`row`. Cells are the source of truth; px is derived. |
| `c4.decisions[]` | **Sticky.** A recorded answer is never re-asked while the evidence that grounded it still holds. It re-opens only when that evidence changed. |
| `c4.evidence` | Always re-derived — a stale pointer is a bug, not user content. |

## Step 6 — Close the judgement calls (exactly one bounded round)

Ask **one** `AskUserQuestion` call with **at most four questions**, drawn only from this closed catalogue and only where the trigger fires and Step 5 has not already answered it. Put the recommendation first in every question.

| Question | Fires when | Fallback if unanswered |
|---|---|---|
| **System boundary** — one system or several? | Always on a cold run and in documents repos; otherwise only when more than one boundary is plausible | One system, on the §2.2 ownership + deployment-alignment heuristic |
| **Service ownership** — one team's implementation detail, or separate systems? | Two or more independently deployable services, and the boundary question did not already settle it | `CODEOWNERS`: a single or absent owner → one system; distinct owners per service → separate systems (§10.1) |
| **Component detail** — which containers get a component view, and at what granularity? | Always on a cold run where at least one container has three or more identifiable units. See below — this question needs real work before you can ask it | The middle option (§5.1 maintenance cost, §13 "only where it earns its keep") |
| **Queues and topics** — explicit containers or relationship labels? | A broker, queue or topic is detected | Four or fewer → explicit; more → implicit (§10.2) |

There is never a second round. On a headless run, a non-answer, or "you decide", apply each fallback and record it as a skill decision with its rationale — an unanswered question is a recorded decision, never a stall and never a re-ask. If an answer raises a new question, record it in the Step 10 report rather than asking it.

### The component-detail question, in detail

On a cold run this is the question the reader will feel most, and it is the one you cannot answer for them: the same codebase is legitimately one component per package or one per module, and which reads better depends on what they want the diagram *for*. So do the analysis first, then offer the real choices.

**Derive the options from structural levels the project actually has** — never from levels you invent. Walk the candidate container's contents and identify the nesting levels that exist (top-level packages, then modules, then classes; or route groups, then handlers; or skill directories, then individual skill files), and count the units at each. Then offer two or three of those levels as options, **each naming the real unit and its resulting element count**, plus an opt-out:

- *"One component per `<unit>` — `<N>` components"* (recommended, marked)
- *"One per `<coarser unit>` — `<M>` components"*
- *"One per `<finer unit>` — `<K>` components"*
- *"No component view — context and container only"*

Recommend the level that lands nearest **8–20 elements** in the finished view, because that is what stays readable; break the tie toward the coarser level, which rots more slowly (§5.1).

Two rules keep this honest, and they are the reason this is a granularity question rather than a "how many boxes" question:

- **Every option must be a level that exists in the project.** "One per functional group" is only on the menu if those groups are real — a directory, a package, a manifest section. If a grouping exists only in your head, it is not an option; it is a boundary rectangle round the real components (Step 7).
- **Coarser never means fewer real things shown.** Choosing a coarse level means the components *are* the coarse units and their contents are simply not drawn — it never means collapsing several real peers into one invented box. That is the §2.6 / §11 anti-pattern and no answer to this question authorises it.

Record the chosen level, the rejected levels and their counts in `c4.decisions[]`, so a later run can re-offer the same menu without redoing the analysis.

Everything else you decide yourself: the container/component call, people and actors, technology strings, relationship labels, which views exist beyond the mandated two, and which candidates are elided for want of evidence.

## Step 7 — Place the model on the grid

Always produce a **system context view** and a **container view**; add a component view per container chosen in Step 6, and a system landscape view only if the boundary question yielded more than one system.

**The container view has to earn its place as the middle of the zoom.** Once Step 6 has fixed the component granularity, the three views should read as a progression — one system, then a handful of runtime units, then their insides — and not as a cliff where a 3-box container view drops into a 24-box component view. Containers are facts, so you never invent one to smooth the curve. What you do instead, in this order:

1. **Let each drillable container preview its own contents.** A container is a single box at this level, so the preview goes in its *description*: end it with what the next level down holds — "…19 skills in 9 functional groups". The reader sees the shape of the zoom before committing to the click, and the ⤢ affordance tells them the click exists.
2. **Group the containers themselves** into boundary rectangles wherever the project has real groupings — the microservices-as-container-groups case in §10.1 is exactly this. Structure without extra boxes.
3. **State the progression in the view description** — "1 system → 5 containers → 19 components in 9 groups". Three numbers cost nothing and make the zoom legible.
4. **Split the component view when the jump is still more than roughly four-fold**, using the coarser structural level from Step 6's menu as the split: one component view per coarse unit, each showing its finer units. Only do this where that second level genuinely exists; otherwise keep one view and say in its description that it is dense on purpose.
5. If none of that applies because the project really is one container holding everything, say so in the container view's description rather than padding it.

Elements are placed on integer `(col, row)` cells. The template owns the geometry — **box 220×140 in a 300×260 cell**, margin 90 — so a 80px column gutter and a 120px row gutter separate every pair of boxes. Derive `x = 90 + col × 300` and `y = 90 + row × 260`, and the view `dimensions` from the largest cell used. Never author pixels by hand.

**Placement is a semantic band, not a free integer.** This is what makes an authored layout better than an algorithmic one: the convention carries meaning that a graph-layout library is blind to. Assign each element a `band` from the table below, then **collapse the bands a view does not use** into consecutive `row` values — a context view using only bands 0, 1, 3 and 6 renders as rows 0–3, so the page carries no dead vertical space while the top-to-bottom ordering the band encodes survives. Store both: `band` is the decision, `row` is the geometry, and `y` derives from `row`.

| band | Meaning | Context view | Container view | Component view |
|---|---|---|---|---|
| 0 | actors | People | People | People |
| 1 | upstream | External systems that initiate | + inbound containers | Containers that call in |
| 2 | edge | — | SPA, mobile, desktop, CLI, web server | Inbound adapters — controllers, handlers |
| 3 | app | **The system in scope** | API and application containers | Domain services, business logic |
| 4 | worker | — | Workers, batch jobs, schedulers | Outbound adapters — facades, gateways |
| 5 | stores | — | Databases, blob stores, queues-as-containers | Data stores the components touch |
| 6 | downstream | External systems the system calls | Same | Same |

Columns carry no semantics, only ordering: all members of one boundary occupy a **contiguous** column range (this is what makes the boundary box derivable), the in-scope system is centred in a context view, and otherwise place each element near the mean column of what it connects to, busiest toward the middle, ties broken alphabetically so the layout is deterministic.

Boundaries are **membership, not geometry**: set `boundary: "<parent element id>"` on a view element and the template computes the rectangle. Never author a boundary's coordinates.

Where a container holds many **peer** components with no adapter layering — a catalogue rather than a stack — bands express *invocation distance from the user* instead: entry points first, then the primary workflow, then secondary workflows, then helpers, then the stores they write to. Say so in the view description when you do this.

Groups of components are **boundaries, not elements**. Set `boundary: "<group name>"` on each member and the template draws a labelled rectangle round them; the group itself is never a box. Collapsing a group into one component instead is the mistake `docs/c4-model.md` §2.6 and §11 name — an organisational grouping masquerading as an abstraction level.

Then check, before going further: no two elements in a view share a cell · every element's `row` is its `band`'s rank among the bands that view uses · a boundary's cell rectangle contains no non-member · **20 elements per view is a soft target, not a licence to coarsen the model.** Past it you have exactly three honest moves, and all three are visible to the reader: split the view, drop the least significant elements and *name every one you dropped* in the Step 10 report, or keep them all and record in the view description why this view legitimately needs more. What you may never do is invent a coarser component so the count fits — that hides real units behind a label and smuggles in a fifth abstraction level.

## Step 8 — Write the model, then render

Write `<project_root>/diagram/c4-model.json` (`mkdir -p diagram` first) in the Structurizr-workspace-compatible schema — standard `{id, x, y}` on view elements, with `col`, `row`, `boundary`, `c4.evidence` and `c4.decisions[]` as additive keys. Keep it readable by `structurizr local`; do not "tidy" it into a bespoke shape.

Then `Read` the template in full, verify all seven tokens are present, substitute, and `Write` the result wholesale to `<project_root>/diagram/c4.html`.

| Token | Value |
|---|---|
| `{{C4_SYSTEM_NAME}}` | Name of the software system in scope. **Appears twice in the template** — replace both. |
| `{{C4_REPO_NAME}}` | `repo_name` from Step 1. |
| `{{GENERATED_AT}}` | The UTC stamp from Step 1. |
| `{{C4_WORKSPACE}}` | The whole workspace as a JS object literal — the same object you just wrote to `c4-model.json` (the file is pretty-printed, the embedded copy need not be), so page and model cannot drift. |
| `{{C4_DEFAULT_VIEW}}` | Quoted key of the view opened on load — the landscape view if present, else the system context view. |
| `{{C4_DECISIONS}}` | JS array of `{ q, choice, by: "user"\|"skill", why }` from Steps 4–6. |
| `{{C4_WORKFLOW_LINK}}` | `<a class="vchip" href="index.html">&#8592; workflow diagram</a>` when `diagram/index.html` exists, otherwise the empty string. |

## Step 9 — Verify the output

Check the written artefacts, not your intent. On any failure, fix the model and re-run Steps 7–9; never ship a failing artefact.

- **Referential** — every `sourceId`/`destinationId` resolves; every view element and relationship id exists in the model; no duplicate ids; component views contain only components of their own container plus legal supporting elements.
- **Notation** (`docs/c4-model.md` §8–§9) — every element has a name, an explicit type and a real description; every container and component has a non-empty `technology`, and no person or software system has one; every relationship is **unidirectional** with an intent label that matches its direction and a protocol where it crosses a process boundary; no relationship label is a bare `"Uses"`, `"Calls"` or `"Depends on"`; every view has a title; the rendered page shows a **legend** covering every shape, colour and line style it actually uses; no acronym is left unexpanded; the context view carries no technology anywhere.
- **Grid** — cells unique per view; rows match their bands; `x`/`y` equal the pitch formula exactly; boundaries contain no non-members.
- **Completeness** — every unit the Step 2 classification mapping names as a container or component is either an element in some view or listed by name in the report's *not modelled* line. Silence is a bug: an elision the reader cannot see reads as a complete picture. Check this by counting the real units on disk (skill files, services, hook scripts) against the elements in the model.
- **Render** — no token remains literal (grep the seven anchored names, not bare `{{`); no `http://` or `https://` anywhere in the output; every drill-down target resolves; exactly two files written this run.

## Step 10 — Report

Emit this block:

```
diagram-c4-update: diagram/c4.html regenerated — <class> repo, <S> systems, <C> containers, <K> components, <V> views, <R> relationships
model: diagram/c4-model.json (<mode>) — +<a> added, ~<m> moved, -<r> retired
decisions: <u> answered by you, <s> taken by the skill
not modelled (insufficient evidence): <list or "none">
Open diagram/c4.html in a browser. To nudge layout, edit col/row in the model and re-run: /diagram-c4-update render
```

If the run added or retired anything, add one sentence pointing at the Decisions panel in the page. Then stop — the artefacts stay as working-tree changes (see Constraints).

## Modification points — four owners

- **Project reality** → re-derived every run. Never hand-edit the model to fix a fact; fix the signal in the project, or the classification.
- **Judgement** → `c4.decisions[]` in the model file. Hand-edits survive re-runs.
- **Layout** → `col`/`row` in the model file, then `/diagram-c4-update render`. Never pixels.
- **Presentation, interaction and geometry** → `templates/c4-diagram.html`, edited outside a run, in lockstep with Step 8's token table. A token or grid constant renamed on only one side fails Step 1's contract check and `tests/test_static.py::TestC4DiagramContract` — that is the tripwire working, not an error to route around.

## Constraints (non-negotiable)

- **Runs in any repo.** No plugin-identity gate, no manifest-name check, no refusal by project type. Outside a git work tree it uses `pwd` and says so. Never copy `/diagram-update`'s repo gate into this skill.
- **Read-only except two files** — `diagram/c4-model.json` and `diagram/c4.html`. Never modifies source, config, manifests, `features/` or `bugs/`. The only other writes are the set-aside `mv`s, which move rather than destroy.
- **Never commit or push.** Leave both artefacts as working-tree changes.
- **The template is the single source of presentation**, including the grid geometry. This skill authors data only. Hand edits to the generated page are lost on the next run.
- **HTML wholesale, model reconciled.** Never patch the page; never blind-overwrite the model. Nothing is deleted from the model — unevidenced elements are retired.
- **Exactly one clarification round, ever** — one `AskUserQuestion`, at most four questions from the closed catalogue, never a follow-up, never re-asking a recorded decision.
- **Never invent architecture.** Every element and relationship cites evidence. Under-evidenced candidates are reported as not modelled.
- **Four levels only.** No code-level views, no deployment or dynamic views, no fifth abstraction level, no "subcomponents" (`docs/c4-model.md` §2.6, §11).
- **No dependencies, no network.** Never shell out to Java, Node, Docker, `structurizr`, `npx` or `likec4`; never fetch anything. The output is one self-contained HTML file plus one JSON file, working offline over `file://`.
- This skill does **not** call `lessons-capture` — like `/diagram-update` and `/bug-submit`, it is a rendering skill and the reflection overhead isn't worth it.
