---
name: pavlo-agent-skill-creator
version: "1.1.0"
description: >
  Create and edit SKILL.md files for AI coding agent skills.
  Use when adding a new skill or improving an existing one.
metadata:
  author: Pavlo Glushko
  applies_to:
    - "**/.agents/skills/**/SKILL.md"
  triggers:
    - create skill
    - new skill
    - add skill
    - edit skill
    - update skill
    - improve skill
    - audit skill
  capabilities:
    - create new SKILL.md files with correct structure and metadata
    - edit and improve existing SKILL.md files
    - audit skills for completeness and consistency with conventions
---

# Skill: Agent Skill Creator

Create or edit `SKILL.md` files for AI coding agent skills in this repository.

## File Location & Naming

- Every skill lives in its own directory: `.agents/skills/<skill-name>/SKILL.md`
- Skill directory names follow the pattern `pavlo-<kebab-case-topic>` (e.g., `pavlo-jira-ticket-writer`).
- Ask for the skill name if the user did not specify one.

## Examples Directory

Skills that produce output files (tickets, plans, PRs, etc.) should include
an `examples/` subdirectory with real-world reference files:

```
.github/skills/<skill-name>/
├── SKILL.md
└── examples/
    └── <real_example_file>.md
```

- Place **copies** of real project files that demonstrate the skill's expected output.
- The `SKILL.md` must reference the examples explicitly
  (e.g., "See `examples/M2_PR3_plan.md` for a real-world reference.").
- Examples are **snapshots** — they do not need to stay in sync with the original files in `docs/`.
- Agents should read the examples before generating output to match style and structure.

---

## SKILL.md Structure

Every `SKILL.md` **must** follow this exact structure and section order.

### 1. YAML Metadata Block

A fenced YAML code block at the very top of the file — no content before it:

```
---
name: <skill-directory-name>
version: "1.0.0"
description: >
  <one or couple sentence description of what the skill does and when to use it.>
  Use when …
metadata:
  author: Pavlo Glushko
  applies_to:
    - "<glob pattern for files this skill produces or edits>"
  triggers:
    - <phrase that should activate this skill>
    - ...
  capabilities:
    - <specific thing the skill can do>
    - ...
---
```

Field rules:
- `name` — must exactly match the directory name.
- `version` — top-level document version; start at `"1.0.0"`, increment minor for content additions, patch for corrections.
- `description` — one or two sentences; include a "Use when …" clause so agents can decide whether to invoke it.
- `metadata.applies_to` — glob(s) for the output or target files (e.g., `"docs/ticket_*.md"`, `"**/.agents/skills/**/SKILL.md"`).
- `metadata.triggers` — lower-case phrases a user might say to invoke this skill. Include synonyms.
- `metadata.capabilities` — concrete actions the skill can perform, not aspirational qualities.

### 2. Title

```markdown
# Skill: <Human-Readable Skill Name>
```

One sentence immediately after the heading describing what the skill does (no heading needed for this sentence).

### 3. File Location & Naming *(if the skill produces output files)*

Explain where output files are created and the naming convention. Include concrete examples.

### 4. Body Sections

The remaining content is skill-specific. Structure it so an agent can follow it as a precise procedure. Common patterns used by existing skills:

- **Structure definition** — when the skill produces a document, define every required section with its exact heading, content rules, and ordering (see `pavlo-jira-ticket-writer`).
- **Rules / conventions** — when the skill enforces a coding or formatting standard, list rules grouped by category with explicit do/don't examples (see `pavlo-markdown-editor`).
- **Workflow** — a numbered step-by-step procedure the agent follows when executing the skill.
- **Writing guidelines** — tone, specificity level, privacy constraints, and anything else that cannot be inferred from the structure definition alone.

---

## Workflow

### Creating a new skill

1. Determine the skill name: `pavlo-<topic>` in kebab-case.
2. Create the file at `.agents/skills/<skill-name>/SKILL.md`.
3. Write the YAML front matter block first (between `---` delimiters).
4. Add the `# Skill: …` title and one-sentence description.
5. Add a File Location & Naming section if the skill produces output files.
6. Write the body: structure definitions, rules, workflow, guidelines — whatever the skill needs to work without further clarification.
7. Keep instructions agent-actionable: avoid vague advice; write steps an agent can execute directly.
8. Add a row for the new skill to the skills table in `.github/copilot-instructions.md` — columns: **Skill** (display name), **File** (path to `SKILL.md`), **Description** (exact text from the `description` metadata field, collapsed to one line).


### Editing an existing skill

1. Read the existing `SKILL.md` in full before making any changes.
2. Identify gaps: missing sections, outdated content, or conventions that changed in the codebase.
3. Apply **surgical updates** — do not rewrite sections that are still accurate.
4. Increment `version` in the metadata block (minor bump for additions, patch for corrections).
5. If the `description` field changed, update the corresponding row in the skills table in `.github/copilot-instructions.md` to match exactly.
6. Summarise what was added, modified, or removed so the user is aware of the changes.

---

## Writing Guidelines

- **Be prescriptive, not descriptive.** Write "use X" not "X is commonly used".
- **Include examples.** Abstract rules are hard to follow; concrete examples eliminate ambiguity.
- **Reference real files.** When a convention is grounded in an existing file, cite it by path.
- **One source of truth.** If a convention is already in `AGENTS.md` or `copilot-instructions.md`, reference it rather than duplicating it.
- **Privacy.** Do not expose personal workflow rules from `copilot-instructions.md` in skill output visible to others.
