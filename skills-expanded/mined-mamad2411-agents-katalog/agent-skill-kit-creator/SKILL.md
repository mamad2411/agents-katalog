---
name: agent-skill-kit-creator
description: Scaffold and validate scope-aware agent skills (company, enterprise, org, team, project, application). Use when the user asks to create a new agent skill, generate a SKILL.md file, scaffold a skill directory, or validate that existing skill directories meet SKILL_SPEC.md (frontmatter, naming rules, structure, scope/tier).
tier: org
---

# Agent Skill Creator (Scope-Aware)

Scaffold a new agent skill OR validate an existing one against `SKILL_SPEC.md`. Every skill is scoped to **one** of six tiers — each tier owns a distinct slice of knowledge/context — and the scope is encoded in both the directory-name prefix and the `tier:` frontmatter field.

This skill mirrors the slash commands `/agent-skill-create` and `/agent-skill-validate`. Use it when slash commands are not auto-loaded or when the user invokes the skill explicitly.

## Mode Selection

Pick a mode based on the user's request:

- **create** — user wants to make a new skill ("create a skill", "scaffold a new skill", "new agent skill")
- **validate** — user wants to check existing skills ("validate skill X", "check if this skill meets the spec", "audit skills")

If ambiguous, ask the user which mode before proceeding.

---

## Scope Tiers

Every skill belongs to exactly one scope. The scope determines what kind of knowledge/context the skill encodes, the directory-name prefix, and the `tier:` frontmatter value.

| Scope | Prefix | `tier:` value | Knowledge / context the skill owns |
|-------|--------|---------------|------------------------------------|
| **company** | `company-` | `company` | Company-wide policy, brand, legal/compliance baselines, security floor, code-of-conduct. Applies to every employee and every codebase the company touches. |
| **enterprise** | `enterprise-` | `enterprise` | Multi-org / multi-division standards: shared platforms, cross-BU governance, procurement-approved tooling, enterprise architecture patterns. Sits above org but below company. |
| **org** | `org-` | `org` | Engineering-org or business-unit standards: shared workflows, common tooling choices, on-call/release norms, naming conventions, repo-template policy. |
| **team** | `team-` | `team` | Team-level conventions: tech-stack picks, coding style, review checklist, on-call rotation, sprint cadence. Specific to one squad/team. |
| **project** | `project-` | `project` | Project-specific architecture, build/test pipeline, dependency graph, domain language, milestone plan. Bound to one repo or coordinated set of repos. |
| **application** | `app-` | `application` | Application-runtime concerns: deployed surfaces, integration points, env-config, observability, customer-facing behavior. Bound to one running service or product. |

Note: `application` uses the historical `app-` prefix to stay backwards-compatible with existing skills (e.g. `app-plan-feature-stories`). Do not introduce `application-` as a prefix.

### Scope decision questions

When the user is unsure which scope to pick, ask:

1. **Who is the audience?** Every employee → company. Multiple orgs/BUs → enterprise. One org → org. One team → team. One repo → project. One running service → application.
2. **Where does the knowledge live today?** Legal/policy site → company. Enterprise wiki / architecture council → enterprise. Org handbook → org. Team README → team. Repo docs → project. Runbook / service dashboard → application.
3. **If this knowledge were wrong, who would file the bug?** Picks the owning scope.

---

## Create Mode

### Input

Expected args: `<skill-name>` or `<skill-name> <short description>`.
- If only a name is given, ask for a description before proceeding.
- If empty, ask for a name, scope, and description.

### Step 1: Ask the user which scope to create

**Always ask** which scope the new skill belongs to. Present the six options with their one-line knowledge/context summaries (from the table above) so the user can pick deliberately. If the user names a scope that isn't in the table, push back and offer the closest match — do not invent a seventh tier.

Map the chosen scope to its `<prefix>` and `<tier>` for use in Steps 2–5.

### Step 2: Validate the Skill Name

Check against SKILL_SPEC Section 3.1:

- 1–64 characters
- Lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`) only
- Cannot start or end with a hyphen
- Cannot contain consecutive hyphens (`--`)

**Scope-prefix rule:** the final directory name must begin with the chosen scope's prefix (e.g. `team-onboarding-checklist`, `project-ployglot-release-flow`). If the user-provided name lacks the prefix, prepend it automatically and show the corrected name back to the user for confirmation.

If the name is invalid for any other reason, explain why and suggest a corrected version. Do not proceed until valid.

### Step 3: Determine Skill Location

The skill directory should be created as a sibling of other skill directories under `.agents/skills/`. Confirm the target path with the user:

```
.agents/skills/<prefix><skill-stem>/
```

### Step 4: Gather Skill Details

Ask the user (if not provided):

1. **Description** (required) — what it does and when to trigger it
2. **Knowledge / context payload** — what scope-specific knowledge this skill carries (the answer should reflect the chosen tier — e.g. a `team-` skill should reference team artifacts, not company policy)
3. **Instructions** — step-by-step body content for the agent
4. **Optional directories** — `scripts/`, `references/`, `assets/`
5. **Optional frontmatter** — `license`, `compatibility`, `metadata`, `allowed-tools`

### Step 5: Create the Directory Structure

```
<prefix><skill-stem>/
├── SKILL.md
├── scripts/       # only if requested
├── references/    # only if requested
└── assets/        # only if requested
```

### Step 6: Generate SKILL.md

```markdown
---
name: <prefix><skill-stem>
description: <description>
tier: <tier>
---

# <Skill Title>

<Body: scope-specific knowledge, instructions, examples, edge cases>
```

Include any optional frontmatter the user specified. Keep the body under 500 lines. The body should make the scope explicit — a `tier: team` skill should not silently embed company-wide policy, and a `tier: company` skill should not encode one team's tech stack.

### Step 7: Validate

Run the validator subprocess against the new skill:

```bash
skills-ref validate <full-path> --extra-tiers company,enterprise,application --format human
```

- Exit 0 → all checks passed; proceed to the Output step.
- Exit 1 → one or more errors; do **not** present success. Re-enter Step 4–6 to fix the reported issues, then re-run.
- Exit 2 → warnings only; surface them in the Output's "Validator output" section but proceed.

### Output

```
## Created: <skill-name>

Scope: <tier> (<one-line knowledge/context summary>)
Location: <full-path>

### Structure
<tree output>

### SKILL.md Preview
<first 20 lines>

### Validator output
<verbatim final summary line from `skills-ref validate`, e.g. "PASS: 12/12 checks passed; 0 warnings">

Status: All validation checks passed.
```

---

## Validate Mode

### Input

Expected args: path to a skill directory, OR empty / `.` to scan `.agents/skills/` for all skill directories (any directory containing `SKILL.md`).

### Step 1: Structural Validation

- [ ] Skill directory exists
- [ ] `SKILL.md` file exists inside

### Step 2: Frontmatter Validation

Parse the YAML frontmatter block (between `---` delimiters) and check:

**Required:**
- [ ] `name` exists and is 1–64 characters
- [ ] `name` uses only lowercase alphanumeric (`a-z`, `0-9`) and hyphens (`-`)
- [ ] `name` does not start or end with a hyphen
- [ ] `name` does not contain consecutive hyphens (`--`)
- [ ] `name` exactly matches the parent directory name
- [ ] `description` exists, is non-empty, and is 1–1024 characters
- [ ] `tier` exists and is one of: `company`, `enterprise`, `org`, `team`, `project`, `application`
- [ ] `tier` matches the directory-name prefix per the scope table (`company-` → `company`, `enterprise-` → `enterprise`, `org-` → `org`, `team-` → `team`, `project-` → `project`, `app-` → `application`)

**Optional (if present):**
- [ ] `license` — short string
- [ ] `compatibility` — max 500 characters
- [ ] `metadata` — string-to-string key-value map
- [ ] `allowed-tools` — space-delimited string

### Step 3: Body Content Validation

- [ ] Markdown body exists after the frontmatter
- [ ] Body is under 500 lines (warn if exceeded)
- [ ] File references use relative paths (no absolute paths like `/foo/bar`)
- [ ] Body content is consistent with the declared `tier` (warn if a `tier: team` skill encodes obvious company-wide policy, or vice versa)

### Step 4: Optional Directory Checks

If present, verify non-empty:

- [ ] `scripts/` — executable or recognized script extensions
- [ ] `references/` — `.md` or documentation files
- [ ] `assets/` — resource files

### Output

```
## Validation: <skill-name>

Scope: <tier>
Status: PASS | FAIL | WARN

### Results
- [x] Check that passed
- [ ] Check that failed — reason

### Summary
X/Y checks passed. Z warnings.
```

For multiple skills, append a summary table:

```
| Skill | Scope | Status | Passed | Warnings | Errors |
|-------|-------|--------|--------|----------|--------|
```

## Reference

Full spec: `SKILL_SPEC.md` at the repo root.
Source commands: `.agents/commands/agent-skill-create.md`, `.agents/commands/agent-skill-validate.md`.
