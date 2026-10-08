# /create-skill - Create a New Skill

Create a new skill with proper structure, scoped content, and a quality review pass. Adds the skill to the framework's skill table and updates the skill profile.

## Process

### Step 1: Parse Arguments and Validate Name

Parse `$ARGUMENTS`:
- `/create-skill [name]` — interactive mode, delegates to researcher for codebase content
- `/create-skill [name] --from-context` — distill from existing `.context/` knowledge files
- `/create-skill [name] --for-library [lib]` — fetch current docs via Context7 MCP

Validate the name:
- Must be kebab-case (lowercase letters and hyphens only, e.g., `stripe-billing`)
- Must not conflict with any of the 20 existing skills — read `skills/context-system/SKILL.md` skills table to check
- If a conflict exists, stop and tell the user which skill already covers the area

### Step 2: Determine Skill Type

Classify the skill into one of three types:
- **Library/framework skill** — wraps a specific technology (e.g., `stripe-billing`, `celery`)
- **Pattern/convention skill** — captures project-specific conventions (e.g., `error-handling`)
- **MCP integration skill** — wraps an MCP server (always gets SKILL.md + REFERENCE.md two-tier split)

### Step 3: Scope the Skill

Use `mcp__sequential-thinking__sequentialthinking` if available to reason through:

1. **Auto-load trigger**: What file patterns, directory names, or contexts should cause this skill to load? Write this as the `description:` frontmatter field — be specific (e.g., "Stripe billing patterns. Auto-loaded when working with stripe/, billing/, or webhook handler files.")
2. **Content split** (MCP skills only): What belongs in SKILL.md (lean trigger rules) vs REFERENCE.md (full config, catalogs, reference tables)?
3. **Token budget**: Target ~40 lines for SKILL.md, ~80 lines for REFERENCE.md. Estimate chars: 40 lines × ~60 chars = ~2400 chars (~600 tokens).

If sequential thinking is unavailable, reason through these questions inline before proceeding.

### Step 4: Gather Content

**If `--for-library [lib]`**:
1. Resolve the library: `mcp__context7__resolve-library-id` with the library name
2. Fetch focused docs: `mcp__context7__get-library-docs` with topic set to "patterns gotchas configuration"
3. Extract from the fetched docs: key patterns, API conventions, common pitfalls, configuration notes
4. If Context7 is unavailable, fall back to researcher agent (see interactive mode below)

**If `--from-context`**:
1. Read `.context/knowledge/libraries/` — find any file matching the skill topic
2. Read `.context/knowledge/LEARNINGS.md` — extract entries related to the skill topic
3. Read `.context/patterns/CODE_PATTERNS.md` — extract patterns related to the skill topic
4. Distill found entries into skill format: dense bullet points, no prose filler

**Interactive mode (no flag)**:
- Delegate to `researcher` agent to scan the codebase for usage patterns related to the skill topic
- Researcher must: identify 5-10 representative files, extract recurring patterns, note anti-patterns observed, flag any existing `.context/` entries on the topic
- Researcher returns: structured findings (patterns, pitfalls, conventions) ready to be formatted into skill bullets

### Step 5: Draft the Skill

Write `skills/[name]/SKILL.md` following this structure exactly:

```
---
description: [specific auto-load trigger sentence — file patterns, contexts, keywords]
---

# [Skill Title]

## [Section — use concern-based groupings, e.g., "Configuration", "Patterns", "API"]
- Dense bullet-point rules
- Each bullet is actionable, not descriptive prose
- Include the "why" only when non-obvious

## Common Pitfalls
- [Pitfall 1] — [brief consequence]
- [Pitfall 2] — [brief consequence]
```

For MCP integration skills, also write `skills/[name]/REFERENCE.md`:
- SKILL.md: when to use, workflow steps, key tool calls, pointer to REFERENCE.md
- REFERENCE.md: full configuration, complete tool catalog, all parameters

After writing, measure file size:
```
wc -c skills/[name]/SKILL.md
```
Warn if SKILL.md exceeds 2000 chars (~500 tokens). Trim prose or split into REFERENCE.md.

### Step 6: Reviewer Pass

Delegate to `reviewer` agent with this checklist:

1. **Trigger accuracy**: Does the `description:` frontmatter precisely describe when this skill should load? Would it fire on irrelevant files? Would it miss relevant ones?
2. **Content density**: Is every bullet actionable? Remove any sentence that describes what something is rather than what to do.
3. **Duplication check**: Read `skills/context-system/SKILL.md` skills table and spot-check the 2-3 most related existing skills. Flag any content that duplicates an existing skill.
4. **Token budget**: Is SKILL.md under 2000 chars? If over, identify what to trim or move to REFERENCE.md.
5. **Common Pitfalls section**: Is it present? Are pitfalls specific enough to be actionable?

Reviewer returns: APPROVED or a list of specific fixes needed. Apply any fixes before proceeding.

### Step 7: Update Framework References

1. **Skills table** — add an entry to `skills/context-system/SKILL.md`:
   - Read the file first
   - Add a row: `| \`[name]\` | [trigger description, ~5 words] | [one-line purpose] |`
   - Keep alphabetical order within the table

2. **Skill profile** — if `.context/architecture/.skill-profile.json` exists:
   - Read the file
   - Add `"[name]"` to `relevant_skills` array (or `irrelevant_skills` if stack doesn't match)

### Step 8: Report

```
Skill created: skills/[name]/SKILL.md
[If MCP skill]: Reference: skills/[name]/REFERENCE.md

Size: [N] chars (~[N/4] tokens)
Token budget: [WITHIN / OVER — trimmed to N chars]

Auto-load trigger: "[description frontmatter]"
Type: [library / pattern / MCP integration]
Content source: [Context7 / .context/ knowledge / researcher agent]

Framework updated:
- skills/context-system/SKILL.md — skills table
- .context/architecture/.skill-profile.json — [updated / not found]

Reviewer: APPROVED
```

## Rules

- Skill names must be kebab-case — reject anything else before proceeding
- Never create a skill that duplicates an existing skill — check the skills table first
- The `description:` frontmatter field is the auto-load trigger — it must name specific file patterns, directory names, or contexts, not just the topic
- SKILL.md target is ~40 lines, hard warn at 2000 chars (~500 tokens)
- REFERENCE.md target is ~80 lines — use for MCP integration skills and library catalog content
- Always run the reviewer agent before finalizing — do not skip even if content looks clean
- Token measurement via `wc -c` is mandatory — always report chars and estimated tokens
- If Context7 is unavailable for `--for-library`, fall back to researcher agent and note the fallback in the report
- If sequential thinking is unavailable, reason through scoping inline — do not skip scoping
- Do not create skills for topics already covered by the existing 20 skills

## User Input
$ARGUMENTS
