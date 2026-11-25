---
name: sdd-init
description: 'Set up SDD on an existing project — inspects the codebase, interviews the user, and generates prd.md, architecture.md, ux.md (if a UI exists), and sdd-tracker.yml. Use when adopting SDD on legacy code or an existing codebase that has no SDD artifacts yet. Do not use for new (greenfield) projects or for updating SDD documents that already exist.'
---

Bootstrap the SDD workflow on a **brownfield** project — existing code, no SDD documents yet.

This skill reverse-engineers the shared project documents from the existing codebase and a targeted conversation with the user, then writes them to the standard SDD locations so the full SDD workflow can proceed normally.

This covers:
- Creating `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md` — what the product does and why
- Creating `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` — how the system is built today
- Creating `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md` + HTML prototype — **only** if a UI layer is detected
- Initializing `{ARTIFACT_MAIN_FOLDER}/sdd-tracker.yml`

---

## Entry point

**Before doing anything else**, check whether shared SDD documents already exist:

1. Try to read `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md`.
2. If it **exists**, stop and inform the user:
   > "SDD shared documents already exist for this project. `/sdd-init` is intended for first-time setup.
   > To update existing docs use `/sdd-prd`, `/sdd-arch`, or `/sdd-ux` directly.
   > To re-initialize from scratch, delete the `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/` folder first and run `/sdd-init` again."

   Do **not** proceed past this point if the PRD already exists.

3. If no shared docs exist, continue with **Step 1** below.

---

## Steps

### Step 1 — Codebase reconnaissance

Systematically inspect the project to extract as much context as possible before asking the user anything.

**Structural inventory** — read and parse:
- `README.md` (or `README.*`) at project root — primary source of intent
- `package.json` / `Cargo.toml` / `pyproject.toml` / `go.mod` / build manifests — tech stack, scripts, dependencies, version
- Lock files — to verify actual installed dependency versions
- `AGENTS.md`, `CONTRIBUTING.md`, `docs/` — any existing documentation
- CI/CD config (`.github/workflows/`, `Dockerfile`, `docker-compose.yml`, `.gitlab-ci.yml`) — deployment context
- `src/`, `app/`, `lib/`, `server/`, `api/` — source structure

**Codebase analysis** — derive:
- **Project type**: web app, API, CLI, mobile, library, monorepo, etc.
- **Tech stack**: language(s), frameworks, databases, ORMs, auth libraries, test runners, build tools
- **Entry points**: main scripts, API routers, page routes, CLI commands
- **API surface** (if applicable): list top-level routes or endpoints found in source
- **UI presence**: does source contain frontend code, templates, or components? If yes, note the framework (React, Vue, HTML templates, etc.)
- **Test coverage signals**: are tests present? What framework?
- **Dependency health signals**: notably outdated or security-sensitive packages
- **Scale / deployment hints**: multi-service? cloud platform? containerized?

Build a **Reconnaissance Report** and present it to the user as a structured summary:

```
🔍 Reconnaissance complete

Project: <name>
Type: <web app | API | CLI | library | monorepo | ...>
Stack: <language>, <framework>, <database>
Entry: <main entry points>
UI: <yes — React / no>
Tests: <yes — Vitest / no>
Deployment: <Docker, AWS, Vercel, unknown>

Files read: <count>
Key observations:
  - ...
  - ...
```

Ask: _"Does this match your understanding of the project?"_ Wait for user confirmation before proceeding.

---

### Step 2 — Targeted gap-filling interview

Ask **only** the questions whose answers cannot be inferred from the code. Present them as a numbered list in a single message so the user can answer all at once.

Standard questions (always ask):

1. **Product vision** — What problem does this tool/product solve, and for whom? _(The README rarely captures the full "why".)_
2. **Current users** — Who uses it today? Are they internal (team), external (customers), or both?
3. **What's working well** — Which parts of the product are you most confident in and want to keep stable?
4. **Known pain points** — What areas of the product need the most improvement or are most fragile?
5. **Near-term roadmap** — Any features or changes already planned that aren't in the code yet?

Conditional questions (ask only if the answer isn't in the code):

- If **no README or minimal README**: _"Can you describe in 2–3 sentences what this project does?"_
- If **UI detected**: _"Is UX documentation needed? Should I also generate a UX design doc and a prototype?"_
- If **monorepo detected**: _"Which package(s) should the SDD docs focus on? All of them, or a specific one?"_
- If **no tests found**: _"Is the lack of tests a known gap, or is testing handled differently (manual, external QA)?"_

After the user responds, confirm:
> "Got it. I have everything I need. Proceeding with document generation — PRD → Architecture → UX (if applicable). I'll report back when done."

Do **not** ask any more questions after this confirmation.

---

### Step 3 — Run the pipeline

Use the **TodoWrite tool** to track pipeline progress through the phases below.

> **Execution rules (same as `sdd-propose`):**
> - Phases 1 and 2 MUST each be dispatched via `runSubagent`.
> - Phase 3 (UX) runs via `runSubagent` only if UI was detected and user confirmed UX doc is needed.
> - Each subagent prompt must be completely self-contained: include all findings, context, rules, and expected output format.
> - Run phases sequentially — each phase may supply context to the next.

---

#### Phase 1 — Generate PRD

Launch a **subagent** (via `runSubagent`) with a prompt that:

- Instructs it to read `sdd-team/agents/sdd-pm.agent.md` and adopt the PM agent persona
- Provides the Reconnaissance Report and gap-filling answers as input
- Instructs it to use `assets/prd.md` as the document structure
- States: **brownfield context** — document what the product _already does_; use placeholders only for genuinely unknown info. Set `Context: brownfield` in the Executive Summary.
- Instructs it to write to `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md` and set `Last updated` to today
- Asks for a one-paragraph summary of what was written

Use the returned summary as context for Phase 2.

---

#### Phase 2 — Generate Architecture doc

Launch a **subagent** (via `runSubagent`) with a prompt that:

- Instructs it to read `sdd-team/agents/sdd-architect.agent.md` and adopt the Architect agent persona
- Provides the Reconnaissance Report and Phase 1 summary as input
- Instructs it to use `assets/architecture.md` as the document structure
- States: **brownfield context** — document decisions already made in the codebase. Fill every row from what is actually in use; use "unknown / not documented" only if genuinely unclear after reading the source. Focus on: tech stack, database/ORM, auth approach, API style, and any conventions found in linting or docs.
- Instructs it to write to `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md` and set `Last updated` to today
- Asks for a one-paragraph summary of what was written

---

#### Phase 3 — Generate UX doc (conditional)

**Run this phase only if:**
- A UI layer was detected in Step 1, **AND**
- The user confirmed in Step 2 that a UX doc is needed

Launch a **subagent** (via `runSubagent`) with a prompt that:

- Instructs it to read `sdd-team/agents/sdd-ux.agent.md` and adopt the UX Designer agent persona
- Provides the Reconnaissance Report, PRD summary (Phase 1), and architecture summary (Phase 2) as input
- Instructs it to use `assets/ux.md` and `assets/prototype-template.html` as document structure
- States: **brownfield context** — document the design patterns, components, and flows that _already exist_. The prototype reflects the current UI, not a redesign.
- Instructs it to write `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md` and `{ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prototype-[project-name].html`, and set `Last updated` to today

If this phase is skipped, note it in the completion summary.

---

### Step 4 — Initialize tracker

Follow the **`sdd-tracker` skill** to initialize `{ARTIFACT_MAIN_FOLDER}/sdd-tracker.yml`:

- Create the tracker file from the template.
- Set `project.name` from the project's package.json / folder name.
- Set `project.created` and `project.lastUpdate` = today.
- Mark only the shared artifacts that were actually written:
  - `shared.prd` — always (created in Phase 1)
  - `shared.architecture` — always (created in Phase 2)
  - `shared.ux.ux` and `shared.ux.prototype` — only if Phase 3 ran
- Add a changelog entry for each artifact: `{ date: <today>, note: "Initialized from brownfield codebase inspection" }`

---

### Step 5 — Completion report

Show a structured summary:

```
✅ SDD initialized for brownfield project

Documents created:
  ✅ {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prd.md
  ✅ {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/architecture.md
  [✅ | ⏭️ skipped] {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/ux.md
  [✅ | ⏭️ skipped] {ARTIFACT_MAIN_FOLDER}/{SHARED_SUBFOLDER}/prototype-<name>.html
  ✅ {ARTIFACT_MAIN_FOLDER}/sdd-tracker.yml

What to do next:
  → Review the generated docs and correct anything that doesn't match reality.
  → Use /sdd-prd, /sdd-arch, or /sdd-ux to refine any document interactively.
  → When ready, use /sdd-propose <change-name> to start your first change.
```

---

## Guardrails

{SKILL_ASSETS_NOTICE}
- **Never overwrite existing shared docs**
- **Code is the ground truth** — prefer what's in the source over what's in any README if they conflict; flag the discrepancy.
- **No aspirational content** — do not fill sections with ideal/future decisions. Use "unknown / not documented" for gaps.
- **Single interview round** — ask all gap-filling questions at once in Step 2. Do not ask follow-up questions between phases.
- **Subagents are autonomous** — each subagent prompt must be self-contained. Do not rely on shared state between subagents.
- **UX phase is gated** — never generate a UX doc if no UI was detected, even if the user requests it in Step 2.
- **Validate outputs** — after each phase, verify the output file exists before proceeding to the next phase.
