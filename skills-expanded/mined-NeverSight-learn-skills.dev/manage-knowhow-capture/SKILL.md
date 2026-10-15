---
name: manage-knowhow-capture
description: Capture reusable knowledge as templates, recipes, or tips
argument-hint: "[type] [description] [--lang lang] [--source url] [--tag tag1,tag2]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep, AskUserQuestion
---

<purpose>
Capture reusable knowledge into `.workflow/knowhow/`. Nine content types: `session` (full session recovery), `template` (code/config pattern), `recipe` (step-by-step guide), `reference` (external doc summary), `decision` (ADR), `tip` (quick note), `asset` (API contract, data model, etc.), `blueprint` (architecture design with code paths), `document` (general long-form). Auto-detects type or asks user.
</purpose>

<context>
$ARGUMENTS — type token followed by description and optional flags.

```bash
$manage-knowhow-capture
$manage-knowhow-capture "compact"
$manage-knowhow-capture "template React form pattern --lang typescript"
$manage-knowhow-capture "tip Always check state.json before phase operations --tag workflow,state"
$manage-knowhow-capture "recipe Deploy to production --tag deploy,ops"
$manage-knowhow-capture "reference Stripe API --source https://docs.stripe.com/api"
$manage-knowhow-capture "decision Use PostgreSQL over MongoDB --status accepted"
```

**Types**: `compact` | `template` | `recipe` | `reference` | `decision` | `tip` | `asset` | `blueprint` | `document`

**Flags**:
- `--lang <lang>` — Language for templates (typescript, python, bash, yaml, ...)
- `--source <url>` — Source URL for references
- `--tag tag1,tag2` — Categorization tags
- `--title <title>` — Explicit title
- `--asset-type <type>` — Asset subtype (api-contract, data-model, prompt, config, ...)
- `--code-paths <paths>` — Related source paths for asset/blueprint (comma-separated)
- `--category <cat>` — Spec category for agent discovery (coding, arch, test, debug, review, learning)
</context>

<execution>

### Step 1: Validate

Verify `.workflow/` exists (E001). Create `.workflow/knowhow/` if missing.

### Step 2: Detect Type

Parse first token as type. If absent or ambiguous, ask user via AskUserQuestion.

| Token | Type |
|-------|------|
| `compact`, `session`, `压缩` | session |
| `template`, `tpl`, `模板` | template |
| `recipe`, `rcp`, `配方`, `步骤` | recipe |
| `reference`, `ref`, `参考` | reference |
| `decision`, `dcs`, `决策` | decision |
| `tip`, `note`, `记录` | tip |
| `asset`, `ast`, `资产`, `契约` | asset |
| `blueprint`, `blp`, `蓝图` | blueprint |
| `document`, `doc`, `文档` | document |

### Step 3: Capture Content by Type

**session** (KNW-{YYYYMMDD}-{HHMM}.md):
Extract from conversation: objective, key decisions, modified files (absolute paths), execution plan (verbatim), pending work, notes. Sections: Session ID, Project Root, Objective, Execution Plan, Working Files, Reference Files, Last Action, Decisions, Constraints, Dependencies, Changes Made, Pending, Notes.

**template** (TPL-{YYYYMMDD}-{HHMM}.md):
Prompt for or extract: language (`--lang`), usage context, code content, parameters, dependencies. Sections: Usage, Parameters, Dependencies, Code (fenced block).

**recipe** (RCP-{YYYYMMDD}-{HHMM}.md):
Prompt for or extract: goal, prerequisites, numbered steps, expected outcome, common pitfalls, related entries. Sections: Goal, Prerequisites, Steps, Expected Outcome, Common Pitfalls, Related.

**reference** (REF-{YYYYMMDD}-{HHMM}.md):
Source from `--source` flag (offer WebFetch if URL). Extract: key points, applicable scenarios, quick examples. Sections: Source, Key Points, Applicable Scenarios, Quick Examples.

**decision** (DCS-{YYYYMMDD}-{HHMM}.md):
Prompt for or extract: context, decision, alternatives (at least 2), rationale, consequences. Sections: Context, Decision, Alternatives Considered (table), Rationale, Consequences, Related.

**tip** (TIP-{YYYYMMDD}-{HHMM}.md):
Content from remaining arguments. Auto-detect context from recent conversation files. Sections: Content, Context, Tags, Timestamp.

**asset** (AST-{YYYYMMDD}-{HHMM}.md):
Prompt for or extract: asset subtype (`--asset-type`), related code paths (`--code-paths`), category (`--category`). Sections: Overview, Structure (tables/schemas), Usage, Related Code Paths. Common asset subtypes: `api-contract`, `data-model`, `prompt`, `config`, `ui-prototype`.

**blueprint** (BLP-{YYYYMMDD}-{HHMM}.md):
Prompt for or extract: system scope, code paths (`--code-paths`), category (`--category`). Sections: Overview, Components, Interactions, Code Paths, Constraints, Trade-offs.

**document** (DOC-{YYYYMMDD}-{HHMM}.md):
General long-form fallback. No specific structure enforced.

### Step 4: Write File

Write to `.workflow/knowhow/{PREFIX}-{YYYYMMDD}-{HHMM}.md` with YAML frontmatter:

```yaml
---
title: {auto or --title}
type: {type}
category: {type}
created: {ISO timestamp}
tags: [{tags}]
```
Plus type-specific: `lang` (template), `source` (reference), `status` (decision), `assetType` + `codePaths` (asset), `codePaths` (blueprint). `category` written when `--category` provided.

### Step 5: Confirm

Display: type, ID, file path, and type-specific summary.
</execution>

<error_codes>
| Code | Severity | Description |
|------|----------|-------------|
| E001 | error | `.workflow/` not initialized — run `Skill({ skill: "maestro-init" })` first |
| E002 | error | Template: no code provided after prompt |
| E003 | error | Recipe: no steps provided after prompt |
| W001 | warning | No active workflow session — compact captures conversation only |
| W002 | warning | No explicit plan found — using inferred plan |
| W003 | warning | `--source` URL could not be fetched — proceeding with manual entry |
</error_codes>

<success_criteria>
- [ ] `.workflow/` existence validated; `.workflow/knowhow/` created if missing
- [ ] Type detected or prompted (all 6 types)
- [ ] Type-specific content collected (code for template, steps for recipe, etc.)
- [ ] YAML frontmatter with type-specific fields written
- [ ] Markdown file written with correct prefix and structured sections
- [ ] Confirmation displayed with ID, type, category, and file path
</success_criteria>
