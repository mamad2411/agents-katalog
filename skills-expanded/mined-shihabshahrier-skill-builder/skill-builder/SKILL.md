---
name: skill-builder
description: >
  Build or audit any AI agent skill from a plain-English description.
  Generates SKILL.md, references, hooks, and full marketplace repo scaffold.
  Supports all 32+ agents in the Agent Skills open standard.
license: MIT
user-invocable: true
argument-hint: '"description" [--type workflow|mode|tool|reference|agent] [--repo] [--audit path] [--fix]'
when_to_use: >
  Use when user says build a skill, create a skill, make a skill, generate a skill,
  audit a skill, review a skill, fix a skill, improve a skill, /skill-builder.
allowed-tools:
  - bash
  - read
  - write
  - glob
  - grep
  - web-search
  - web-fetch
  - agent
metadata:
  author: "shihabshahrier"
  category: "developer-tools"
---

# Skill Builder

Turn a plain-English description into a production-ready skill compatible with every
agent that implements the Agent Skills open standard (32+ tools, December 2025).

---

## Invocation

```
/skill-builder "compress images before committing"
/skill-builder "remind the model to always write tests first" --type reference
/skill-builder "scaffold a FastAPI project" --type workflow --repo
/skill-builder "make the model speak formally" --type mode --repo
/skill-builder --audit skills/my-skill/SKILL.md
/skill-builder --audit skills/my-skill/SKILL.md --fix
```

| Arg | Default | Values |
|-----|---------|--------|
| description | required (unless --audit) | plain English, what the skill does |
| --type | auto-detect | workflow, mode, tool, reference, agent |
| --repo | off | also scaffold a full marketplace-ready repo |
| --audit | off | path to existing SKILL.md — audit instead of create |
| --fix | off | with --audit: also output corrected SKILL.md |

---

## Phase 0 — Route

**If `--audit` flag present:** skip to [Phase A — Audit](#phase-a--audit).

**Otherwise:** continue to Phase 1.

---

## Phase 1 — Classify

Load `references/skill-types.md`.

Determine skill type from description:

| Signal | Type |
|--------|------|
| "every time", "always", "mode", "persistently" | **mode** |
| "create", "scaffold", "build", "pipeline", "generate" | **workflow** |
| "compress", "format", "convert", "run X on Y", "transform" | **tool** |
| "remind", "context for", "know about", "rules for" | **reference** |
| "act as", "autonomous", "manage the whole", "firm", "company" | **agent** |

If `--type` provided, skip detection. If ambiguous, ask ONE question:

> "Is this (a) a persistent mode that changes every response, (b) a one-shot action on a specific target, or (c) a multi-step workflow producing artifacts?"

Wait for answer. Never ask more than one question total. Decide the rest.

---

## Phase 2 — Gather Requirements

Load `references/skill-anatomy.md`.

Ask at most 2 more questions total (across all phases). If description already answers, skip:

```
1. Trigger: does the user type /skill-name to invoke, or should it activate automatically?
2. Output: what does it produce — files on disk, changed model behavior, a report, or nothing?
```

Derive:
- `SKILL_NAME` — kebab-case, matches `^[a-z0-9]+(-[a-z0-9]+)*$`, 1–64 chars
- `TRIGGER` — user-invocable (typed) or auto (always-on, requires SessionStart hook)
- `OUTPUTS` — files / behavior change / report / none
- `NEEDS_HOOKS` — true if mode or auto-trigger
- `NEEDS_REFERENCES` — true if skill needs domain knowledge loaded lazily
- `NEEDS_SCRIPTS` — true if skill runs bash/python tools

---

## Phase 3 — Domain Research (if NEEDS_REFERENCES)

Before writing any reference files, research the domain to get verified facts.
Skip this phase if `NEEDS_REFERENCES` is false.

**Step 1 — Identify research targets.** From description, extract tool/library names, APIs, frameworks, flags, method signatures, config schemas.

**Step 2 — WebSearch official docs.** For each target:
```
WebSearch: "{tool-name} official documentation CLI flags"
WebSearch: "{api-name} API reference {relevant-endpoint}"
```
Prioritize: official docs > spec documents > recent release notes.

**Step 3 — Extract and verify.** Only keep: exact flag names + values, method signatures, error codes, version constraints. Never include unverified Stack Overflow answers.

**Step 4 — Build reference stubs.** One file per domain: `references/{domain-slug}.md` with verified flags/methods, error→fix table, input/output examples, TOC if >100 lines.

---

## Phase 4 — Generate SKILL.md

### Frontmatter

```yaml
---
name: {SKILL_NAME}
description: >
  {LINE_1_WHAT_IT_DOES_VERB_OBJECT_MAX_80_CHARS}
  {LINE_2_HOW_INVOKED}
  {LINE_3_KEY_OUTPUT_OR_BEHAVIOR}
license: MIT
user-invocable: {true_OR_false}
argument-hint: '{ARGUMENT_HINT}'
when_to_use: >
  {WHEN_TO_USE}
---
```

Add optional fields only when relevant: `model`, `effort`, `context`, `paths`, `allowed-tools`, `metadata`.
See `references/skill-anatomy.md` for full field reference.

### Body structure by skill type

Load `references/skill-types.md` for full patterns:

- **workflow**: Invocation → Phase 0…N → Report → Token Efficiency → Open-Weight Rules
- **mode**: Activation → Persistence → Rules → Intensity → Auto-Clarity → Boundaries
- **tool**: Trigger → Process (numbered) → Output → Error Handling
- **reference**: Purpose → When to Apply → {Domains} → Never Do
- **agent**: Prime Directive → Mode Detection → Phases → Prohibited → Success Criteria

### Quality rules
- First sentence: action-oriented ("Produce X"), not "This skill..."
- Every section actionable — no vague guidance
- Code templates for any generated code
- Error tables for external tool calls
- Reference loads at the phase that needs them (lazy)
- All `{TEMPLATE_VARIABLES}` substituted — never leave placeholders
- Keep SKILL.md under 5000 tokens

---

## Phase 5 — Generate References (if NEEDS_REFERENCES)

For each domain area identified in Phase 3:

1. Name: `references/{domain-slug}.md`
2. Structure: TOC → headings → tables → code blocks, minimal prose
3. Error→fix tables for external tools
4. Input/output example pairs
5. Add load instruction in SKILL.md: `Load references/{name}.md before {action}.`

Rules: verified facts only, tables over prose, one-level-deep (no chained includes), TOC if >100 lines.

---

## Phase 6 — Generate Hooks (if NEEDS_HOOKS)

Load `references/hook-templates.md` for full templates.

Mode skills only. Generate: `hooks/package.json`, `hooks/activate.js`, `hooks/tracker.js`.
Use `safeWriteFlag` pattern verbatim. ALL filesystem ops must silent-fail.

---

## Phase 7 — Scaffold Repo (if --repo)

Load `references/scaffold-templates.md`, `references/agent-rules.md`, and `references/install-paths.md`.

Generate full repo in `{SKILL_NAME}/` directory. See `references/scaffold-templates.md` for complete file list and content templates.

---

## Phase 8 — Report

```markdown
## Skill Built: {SKILL_NAME}

**Type**: {SKILL_TYPE}
**Hooks**: {yes — SessionStart + UserPromptSubmit | no}
**References**: {list filenames or "none"}
**Repo scaffold**: {yes — {SKILL_NAME}/ | no}

### Files created
{list every file path}

### Install
bash install.sh

### Test
/{SKILL_NAME} {example invocation}
```

---

## Phase A — Audit (only when --audit flag present)

Load `references/skill-anatomy.md`.

**Step 1 — Read target.** Read SKILL.md at `--audit` path. If missing, stop and tell user.

**Step 2 — Extract metadata.** Parse frontmatter: `name`, `description`, `license`, type (infer from body). Estimate token count.

**Step 3 — Run quality checklist.** Check every item in `references/skill-anatomy.md` Quality Checklist. Record each failure:
```
[FAIL] {checklist-item}
  Found:    {what's there}
  Expected: {what should be}
  Fix:      {exact change}
```

Also check: body matches required sections for type, no raw `{VARIABLE}` placeholders, SKILL.md under 5000 tokens, reference files have TOC if >100 lines, domain facts verified not guessed.

**Step 4 — Report.** Output: type detected, size (ok or OVER BUDGET), failures list, warnings list, passed count.

**Step 5 — If --fix.** Output corrected SKILL.md — fix failures only, don't rewrite passing sections. Run Phase 3 first if domain research needed.

---

## Token Efficiency Rules

- Ask 3 questions max total (Phase 1 + Phase 2)
- Load `skill-types.md` once at Phase 1, keep active
- Load `hook-templates.md` only at Phase 6
- Load `scaffold-templates.md`, `agent-rules.md`, `install-paths.md` only at Phase 7
- Run Phase 3 domain research only if NEEDS_REFERENCES
- Generate all files in one pass — no file-by-file back-and-forth

---

## Open-Weight Model Rules

- Substitute ALL `{TEMPLATE_VARIABLES}` — never output raw placeholders
- Every generated SKILL.md self-contained — no dangling `@` includes in skill body
- JSON: valid, no comments, no trailing commas
- YAML: valid, correct indentation, quote special chars
- Hook JS: use safeWriteFlag pattern verbatim
- `name` must match `^[a-z0-9]+(-[a-z0-9]+)*$` — validate before writing
- `description` must be ≤1024 chars — count before writing
