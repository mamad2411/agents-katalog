---
name: skill-creator
description: Meta-skill that guides agents to create reusable skills from completed tasks — frontmatter schema (including YAML quoting rules), body structure, quality checklist, and the propose_skill workflow.
source: manual
version: 1.0.1
triggers:
  - "create skill"
  - "new skill"
  - "propose skill"
  - "skill generation"
  - "reusable skill"
---

## Goal

Create high-quality, reusable SKILL.md files capturing patterns, procedures, and best practices discovered during task execution.

## When to create a skill

- **Repeated patterns**: you applied the same multi-step procedure that could be reused for future similar tasks.
- **Domain-specific knowledge**: tools, conventions, or workflows specific to a domain.
- **Novel combinations**: techniques combined in a way not covered by existing skills.
- **Tool-heavy tasks**: ≥5 tool calls with a coherent workflow.

## Frontmatter (required)

```yaml
---
name: snake-case-name
description: "Clear, specific description of what this skill covers (≥20 chars)"
source: auto-generated
version: "1.0.0"
triggers:
  - "keyword1"
  - "keyword2"
generated_by: coder
generated_from_task: "Original task description"
---
```

Field rules: `name` snake-case, starts lowercase (`[a-z][a-z0-9_-]*`), unique across all skills. `description` ≥20 chars, specific enough to distinguish from similar skills. `triggers` ≥1 entry — keywords/phrases that should match during auto-discovery. `source` always `"auto-generated"` for skills created via this meta-skill.

### Frontmatter YAML safety (avoid the "mapping values are not allowed here" warning)

The validator parses frontmatter as strict YAML first; a failure is only recovered by a tolerant fallback and produces a warning. Write values so strict parsing succeeds:

- **Quote any value containing a colon.** `description: Audit bugs: root cause analysis` fails (the second colon is read as a nested mapping). Write `description: "Audit bugs: root cause analysis"`. This is the single most common cause — descriptions phrased as "X: does Y".
- Also quote values containing `#`, leading/trailing spaces, `: ` inside lists, or a leading `[`/`{` (they get parsed as flow collections). `#` unquoted starts a comment and silently truncates the value.
- Keep `version` quoted (`version: "1.0.0"`) so it stays a string and is not read as a number.
- Quote every `triggers` entry (`- "retry loop"`). Multi-word triggers unquoted are fragile.
- Lists must be block-style on their own lines (as in the template), not inline with commas, and no tabs — indentation must be spaces.
- If the tool still reports a YAML warning, re-read your own frontmatter for an unquoted special character before assuming the body was at fault; the line/column in the message points at the offending value.

## Body structure (≥100 chars)

```markdown
## Goal
One sentence: what this skill enables.

## Procedure
### Step 1 — First Action
Concrete, actionable instructions.
### Step 2 — Second Action
Include code examples, commands, or config snippets.

## Tips
- Domain-specific best practices
- Common pitfalls to avoid
```

Prefer an **anti-patterns table** (`| Pattern | Why it fails |`) at the end for procedural skills: it is the part agents actually re-check mid-task.

## Quality checklist

- [ ] Name and coverage is unique (check existing skills via `scan_skills`)
- [ ] Name contains the exact info necessary to pick up on its role and use case at a quick glance
- [ ] Description is specific (not generic like "coding" or "debugging")
- [ ] Frontmatter parses as strict YAML (values with `:` / `#` are quoted)
- [ ] Triggers cover how the skill will be matched in practice
- [ ] Body has concrete, actionable steps (not vague advice)
- [ ] Total file size ≤ 15 KB
- [ ] Reusable — applies to a class of tasks, not just one

## Using propose_skill

```
propose_skill(params={
    "name": "<snake_case skill name — required, becomes the registered name>",
    "skill_content": "<full SKILL.md with frontmatter and body>",
    "justification": "<why this skill is needed>"
})
```

The `name` argument is authoritative: if the frontmatter carries a different name it is patched to match. A NEW name is written to a pending location, validated (frontmatter, required fields, uniqueness), and — if valid — promoted to `agents/global/skills/`. An EXISTING name is an **update**: the version is bumped (never downgraded), the new content goes to `agents/global/candidates/<name>/SKILL.md`, and it becomes the **live-serving candidate** immediately. It is later promoted (copied over production) or discarded by the rating-based decision gate once it has enough ratings; the production file is not modified until then. To update, call `scan_skills` with `preview="<name>"` first and submit the full current file plus your changes — never rewrite an existing skill from memory.

Rating-only mode: `propose_skill(name=..., rating=0-10)` with **no** `skill_content` records a rating without touching the file and requires no approval. Use it at the end of a run for skills you actually applied; do not rate skills that were merely loaded.

## Agent-specific guidance

- **Coder:** coding patterns, testing strategies, debugging workflows, build-tool usage, code-review checklists, refactoring patterns.
- **Researcher:** search strategies, source evaluation, fact-checking, citation handling, evidence synthesis, claim verification against primary sources.
- **Reviewer:** code-review checklists, consistency checks, edge-case identification, security review patterns.
- **Writer:** content structures, tone adaptation, editing workflows, style-guide enforcement.
