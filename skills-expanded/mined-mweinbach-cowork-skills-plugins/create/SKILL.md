---
name: create-skill
description: "Use when the user asks to create, author, scaffold, write, or improve a skill — a SKILL.md package that gives an agent specialized, on-demand instructions plus optional bundled resources. Triggers on: 'create a skill', 'new skill', 'write a skill', 'author a skill', 'add a skill', 'scaffold a skill', 'make a SKILL.md', 'improve this skill', 'fix my skill description'."
metadata:
  triggers: "create skill, new skill, author skill, write skill, scaffold skill, make a skill, SKILL.md, improve skill, edit skill, skill description"
---

# Create a skill

A skill is a directory containing a `SKILL.md` (YAML frontmatter + a markdown body) and, optionally,
bundled resources (references, scripts, assets). When a skill is invoked, its body is injected
verbatim as authoritative instructions — write the body for an agent to execute, not for a human
to read.

Skills are discovered in three locations, highest priority first; a name in an earlier location
shadows the same name in a later one:

1. **Project** — `<project>/.cowork/skills/`
2. **User** — `~/.cowork/skills/`
3. **Built-in** — shipped with the app (read-only)

## Frontmatter: the complete field set

Exactly these keys are recognized. `name` and `description` are required; the rest are optional.
Any other key is ignored. Full constraints and limits are in `references/schema.md`.

| Key | Required | Purpose |
|-----|----------|---------|
| `name` | yes | kebab-case identifier; **must equal the directory name** |
| `description` | yes | what the skill does + when to use it; this is what an agent reads to decide whether to invoke it |
| `license` | no | free-form license identifier |
| `compatibility` | no | free-form environment note (≤500 chars) |
| `metadata` | no | a string→string map (e.g. `author`, and `triggers` for discovery) |
| `allowed-tools` | no | informational tool list |

## Process

Follow these steps in order; skip one only with a clear reason.

### 1. Understand the skill with concrete examples
Pin down what the skill does and **what a user would say to trigger it** before writing anything.
If unclear, ask one or two focused questions: "What tasks should this cover?", "Give two example
requests that should invoke it." A skill earns its place by carrying procedural or domain knowledge
that is non-obvious to a capable agent — not by restating common sense.

### 2. Choose the scope, then the name

**Decide scope first** — where the skill is installed determines who can use it:

- **Global (user)** — `~/.cowork/skills/`: available in every session.
- **Project** — `<project>/.cowork/skills/`: available only when working in that project, and
  checked in so it travels with the repo. A project skill shadows a global skill of the same name.

Apply this rule:

- **In a chat (no project in context): always install the skill as global** (`~/.cowork/skills/`).
  Skills created from a chat are global — do not write a project skill from a chat.
- **When working in a project: ask the user whether this should be a project skill or a global
  one** — do not assume. Choose **project** when the skill is specific to that codebase and should
  be shared with collaborators; choose **global** for a personal or general-purpose skill wanted
  everywhere.

Then choose a **kebab-case** name matching `^[a-z0-9]+(?:-[a-z0-9]+)*$` (≤64 chars) — the directory
name **must equal** the frontmatter `name`, or the skill is dropped — and create the skill at
`<chosen-skills-dir>/<name>/`.

### 3. Write the frontmatter
Keep it minimal — `name` and `description` are usually all you need. Invest in `description`: it is
what an agent reads to decide whether to invoke the skill, so make it concrete and pack it with the
phrases a user would actually type (see `references/authoring.md`). To aid discovery via
`@`-mentions, add `metadata.triggers` — a comma-separated string or a YAML array of short aliases.
Consult `references/schema.md` for each field's exact rules before adding it.

### 4. Write a lean, imperative body
Write in **imperative/infinitive form** ("Stage related changes", not "You should stage…"). Lead
with the core procedure. Target under ~2,000 words and push detail into `references/`. Use `##`
headings, short numbered steps, and real, copy-pasteable commands. Reference the actual tool names
available in the environment rather than generic placeholders.

### 5. Bundle resources only when they earn it
A skill directory can hold subdirectories alongside `SKILL.md`:

- **`references/`** — documents loaded on demand: schemas, API docs, policies, deep guides, edge
  cases. Keeps the body lean. For a large reference (>~10k words), add grep patterns in the body so
  the agent can find sections.
- **`scripts/`** — runnable code for deterministic or repeated tasks (validators, parsers,
  generators). Keep them dependency-free where practical so they run wherever the skill lands.
- **`assets/`** — files used *in the output*, not read into context: templates, boilerplate
  projects, images, fonts, sample documents the agent copies or fills in.
- **`agents/openai.yaml`** — optional UI metadata (`display_name`, `short_description`,
  `default_prompt`, and small/large icons).

Reference every resource you add from the body so the agent knows it exists.
`references/authoring.md` explains the progressive-disclosure rationale and when each applies.

### 6. Validate — required before declaring done
Run the bundled validator against the new skill directory and fix every reported error:

```bash
bun ~/.cowork/skills/create-skill/scripts/validate-skill.ts <path-to-new-skill-dir>
```

(Adjust the script path if this skill is installed in a project or built-in tier.) It applies the
same rules the loader applies — frontmatter parsing, the `name` regex, `name == directory`, length
limits, and string-only `metadata` values. A clean PASS means the skill will be discovered and
loaded. Then confirm discovery: the skill should appear in the skill list and resolve on an
`@<name>` mention.

### 7. If publishing through a marketplace, refresh source hashes
Marketplace catalogs may carry `sourceHash: "sha256:<64 hex chars>"` beside standalone skill
entries. This is not skill frontmatter and does not belong in `SKILL.md`; it belongs in
`.agents/plugins/marketplace.json`.

When editing a standalone skill in the `cowork-skills-plugins` marketplace repo:

1. Do not publish installer provenance or desktop noise in the source root. Remove tracked
   `.cowork-skill.json`, `.cowork-plugin/install.json`, `.codex-plugin/install.json`, and
   `.DS_Store` files before hashing.
2. Run the marketplace helper from the repo root:

   ```bash
   node scripts/update-source-hashes.mjs
   node scripts/update-source-hashes.mjs --check
   ```

3. Commit the skill change and the resulting `.agents/plugins/marketplace.json` hash update
   together. Do not hand-edit `sourceHash`; let the script compute it.

## Editing an existing skill

To improve or fix a skill, edit its files in place and re-validate:

1. **Locate it.** Find the directory under `<project>/.cowork/skills/`, `~/.cowork/skills/`, or the
   built-in skills directory. When the same name exists in more than one tier, the higher-priority
   tier is in effect (project > user > built-in). Built-in skills are read-only — to change one,
   copy its directory into `~/.cowork/skills/` (or the project tier) under the **same name**; that
   copy shadows the built-in.
2. **Read what's there first.** Open `SKILL.md` and any `references/`, `scripts/`, and `assets/`,
   so edits build on the current content instead of duplicating or contradicting it.
3. **Make the change.** The highest-impact edits (detailed in `references/authoring.md`):
   - Sharpen `description` / `metadata.triggers` so the skill fires at the right time.
   - Tighten the body, or split a section that has grown long into `references/`.
   - Add a `scripts/` helper or an `assets/` template for a task the skill keeps redoing by hand.
4. **Keep the invariants.** `name` must still equal the directory name and match the kebab-case
   regex; `description` ≤1024 chars; every `metadata` value a string. **Renaming a skill means
   renaming both the directory and the frontmatter `name`** (and updating `triggers` and anything
   that references it). Leave `.cowork-skill.json` in place for a live installed copy, but do not
   commit it to a marketplace source package.
5. **Re-validate.** Run `scripts/validate-skill.ts` against the directory for a clean PASS, then
   re-invoke the skill to confirm the new behavior.
6. **Refresh marketplace hashes when applicable.** If the skill is listed in
   `.agents/plugins/marketplace.json`, run `node scripts/update-source-hashes.mjs` and then
   `node scripts/update-source-hashes.mjs --check` from the marketplace repo root.

## Quick frontmatter reference

Minimal (almost always sufficient):

```yaml
---
name: my-skill
description: "Use when ... . Triggers on: 'phrase one', 'phrase two'."
---
```

## Resources
- **`references/schema.md`** — the full skill format: every field, its constraints, frontmatter
  parsing rules, triggers, the `agents/` interface, and how the body is used.
- **`references/authoring.md`** — methodology: progressive disclosure, writing trigger-rich
  descriptions, imperative style, when to add references/scripts/assets, common mistakes.
- **`references/templates.md`** — copy-ready minimal and full `SKILL.md` plus directory layouts.
- **`scripts/validate-skill.ts`** — the validator from step 6.

To author a skill *inside a plugin* (under a plugin's `skills/` directory), follow this same skill
for each `SKILL.md`, then use the `create-plugin` skill for the surrounding manifest.
