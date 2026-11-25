---
name: create-constitution
description: Create or update a CONSTITUTION.md file in the specs/ folder by scanning the project. The constitution captures project-wide context that all other nano-spec skills rely on, like tech stack, sanity check commands, coding conventions, key files, and hard rules. Use when the user wants to set up nano-spec for a new project, initialize the constitution, or keep it up to date. Trigger when the user says things like "create the constitution", "set up the project constitution", "initialize nano-spec", or "update the constitution".
---

# Constitution Creator

This skill creates `specs/CONSTITUTION.md` — a short, factual document that every other nano-spec skill reads before doing its job. It captures what an agent cannot derive from reading the code: what the project is, which sanity checks to run, which conventions to follow, and which rules must never be broken.

The output is saved at `specs/CONSTITUTION.md`.

---

## Step 0: Check for an existing constitution

Look for `specs/CONSTITUTION.md`.

- If it doesn't exist, proceed to Step 1.
- If it already exists, ask the user:
  > "A constitution already exists at `specs/CONSTITUTION.md`. Do you want to recreate it from scratch, or update specific sections?"

  - If recreating: proceed to Step 1.
  - If updating: read the existing file, go to Step 2, and focus exploration only on the sections the user wants updated.

---

## Step 1: Explore the codebase (read-only)

Scan the project to gather the information needed to fill each section of the template. Use subagents via the Agent tool to explore independent areas in parallel if available.

For each section, here is what to look for:

**Project**
- Read the README if one exists.
- Identify what the project does and who it's for from file structure and entry points.

**Tech Stack**
- Read `package.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, or equivalent to identify languages, frameworks, and key dependencies.

**Sanity Checks**
- Look for scripts in `package.json`, `Makefile`, `pyproject.toml`, or similar.
- Look for config files that indicate available tools: `tsconfig.json`, `.eslintrc*`, `eslint.config.*`, `.biome.json`, `pytest.ini`, `go.sum`, etc.
- Identify the actual commands to run (type check, lint, build, test) and their correct invocation.

**Conventions**
- Read 2–3 existing source files to identify naming patterns, file structure, import style, and any non-obvious idioms.
- Only note things that deviate from common defaults or that an agent could easily get wrong.

**Key Files**
- Identify entry points, main config files, and modules that are central to the architecture.

**Rules**
- Look for a `CLAUDE.md` or project-level instructions file. Extract hard constraints from it if present.
- Note anything from exploration that suggests a firm rule (e.g., a migration pattern that must always be followed, a file that must never be edited directly).

---

## Step 2: Ask the user

After exploration, always ask the user a set of questions — even for things you think you already know. The goal is to validate your findings and surface knowledge that isn't visible in the code.

Send all questions in a single message, grouped by section. Present what you found first, then ask the user to confirm, correct, or expand. Use this format:

> **Here's what I found — please confirm, correct, or add anything missing:**
>
> **Project**
> I understand this project is [your summary]. Is that accurate? Anything important to add about the audience or purpose?
>
> **Tech Stack**
> I found: [list]. Is this complete? Any key libraries or tools I should know about that aren't obvious from the config files?
>
> **Sanity Checks**
> I found these commands: [list with invocations]. Are these the right ones to run after every implementation? Is there a canonical order? Any that should be skipped in certain situations?
>
> **Conventions**
> I noticed: [list of observed patterns]. Are these intentional rules, or just the way things happened to be written? Any naming conventions, structural rules, or patterns I should always follow that aren't obvious from reading the code?
>
> **Key Files**
> I identified these as central: [list]. Are there other files an agent must know about to navigate this codebase safely (e.g., files that must never be touched, generated files, critical config)?
>
> **Rules**
> [If you found rules in CLAUDE.md or elsewhere, list them.] Are there any hard constraints I should add — things agents must never do, or must always do in this project? Think about past mistakes or things that have gone wrong.

Wait for the user's answers before writing the constitution. Do not skip this step even if you feel confident about your findings — the user's input is what makes the constitution trustworthy.

---

## Step 3: Create the constitution

1. Read `assets/CONSTITUTION-TEMPLATE.md` from this skill's directory.

2. Create the `specs/` directory if it doesn't already exist.

3. Write the template contents to `specs/CONSTITUTION.md`, preserving the structure exactly.

4. Fill in each section with what you learned. Be concise — the constitution should take under 2 minutes to read. If a section has nothing meaningful to say, remove it entirely.

5. Before saving, do a self-review:
   - Remove the instruction comment block at the top.
   - Remove any sections that ended up empty.
   - Verify every sanity check command is real and correct — don't invent commands.
   - Check that conventions and rules are specific, not generic advice.

---

## Step 4: Tell the user

> The constitution has been created at `specs/CONSTITUTION.md`.
>
> Please review it — especially the Sanity Checks and Rules sections. Edit anything that's wrong or missing before we proceed.
>
> All nano-spec skills will now read this file automatically.

Then stop and wait. Do not proceed until the user confirms or edits the constitution.
