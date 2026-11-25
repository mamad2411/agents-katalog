---
name: mini-sdd-context
description: 'Create or update the project context document that captures product vision, architecture, and tech stack in a single file. Use when bootstrapping a new project with mini-SDD, onboarding AI agents to an existing codebase, or updating project context after completing a feature. Do not use for writing feature specs or implementing code.'
disable-model-invocation: true
---

Create or update the project context document at `./{ARTIFACT_MAIN_FOLDER}/context.md`.

This file is the single source of truth read by every other mini-SDD skill. It merges product vision, architecture overview, and tech stack into one concise document.

---

## Hook execution

Check `./{ARTIFACT_MAIN_FOLDER}/mini-sdd.config.yml` for `hooks.context.pre` and `hooks.context.post` entries. Run pre-hooks before the Entry point; run post-hooks after the full workflow completes. See [references/hooks.md](./references/hooks.md) for the full execution rules.

---

## Entry point

1. Check whether `./{ARTIFACT_MAIN_FOLDER}/context.md` already exists.
   - **If it exists** → read it, show a summary to the user, and ask:
     > "The project context already exists. Do you want to **update** it or **start fresh** (overwrite)?"
     - **Update** → proceed to **Step 2 — Update flow**
     - **Start fresh** → proceed to **Step 1 — Creation flow**
   - **If it does not exist** → proceed to **Step 1 — Creation flow**

---

## Step 1 — Creation flow

### 1a. Codebase reconnaissance

Inspect the project to gather as much context as possible before asking questions.

**Read and parse** (skip missing files silently):
- `README.md` at project root
- `package.json` / `Cargo.toml` / `pyproject.toml` / `go.mod` / build manifests
- `AGENTS.md`, `CONTRIBUTING.md`, `docs/`
- CI/CD config (`.github/workflows/`, `Dockerfile`, `docker-compose.yml`)
- Source structure (`src/`, `app/`, `lib/`, `server/`, `api/`)

**Derive**:
- Project type (web app, API, CLI, library, monorepo, etc.)
- Tech stack (languages, frameworks, databases, test runners, build tools)
- Entry points
- UI presence (yes/no, which framework)
- Test setup

Present a short summary:

```
📋 Reconnaissance

Project: <name>
Type: <type>
Stack: <languages>, <frameworks>, <database>
UI: <yes — framework / no>
Tests: <yes — runner / no>
```

Ask: _"Does this look correct? Anything to add or fix?"_

### 1b. Targeted questions

Ask the following in a **single numbered message** so the user can answer all at once:

1. **What does this project do?** — One or two sentences describing the product/tool and who it's for.
2. **Key features** — List the main capabilities or modules.
3. **Architecture style** — Monolith, microservices, serverless, CLI, etc.
4. **Non-functional requirements** — Performance targets, security constraints, compliance needs (if any).
5. **Current status** — What's already built vs. what's planned?

Skip any question already answered by the reconnaissance.

### 1c. Generate context.md

Read the template from `assets/context.template.md` and fill it in using the gathered information.

- Write the file to `./{ARTIFACT_MAIN_FOLDER}/context.md`
- Set `Last updated` to today's date (`YYYY-MM-DD`)
- Confirm to the user:
  > "✅ Created `./{ARTIFACT_MAIN_FOLDER}/context.md`. You can review and edit it manually anytime."

---

## Step 2 — Update flow

Use this flow when the context file already exists and the user chose to update it.

1. Read the current `./{ARTIFACT_MAIN_FOLDER}/context.md`.
2. Ask the user:
   > "What changed? For example: new feature completed, tech stack change, architecture update, status change."
3. Based on the answer, update only the relevant sections of `context.md`.
4. Update the `Last updated` date to today (`YYYY-MM-DD`).
5. Show a diff summary of what changed.
6. Confirm:
   > "✅ Updated `./{ARTIFACT_MAIN_FOLDER}/context.md`."

---

## Output rules

{SKILL_ASSETS_NOTICE}
- Keep the document **concise** — aim for a single page that an AI agent can quickly consume.
- Use the structure from the template; do not invent new sections.
- Write in plain English, no marketing language.
- If the user provides vague answers, ask one follow-up, then proceed with best effort and note assumptions.

## Error handling

- **File not writable / path missing**: Create parent directories as needed before writing `context.md`.
- **User provides no answers**: Proceed with information gathered from reconnaissance and mark unknown fields as `<!-- unknown — update manually -->`.
- **Codebase reconnaissance finds nothing**: Skip the summary step and go directly to targeted questions.
- **Conflicting information**: Surface the conflict to the user and ask for clarification before writing.
