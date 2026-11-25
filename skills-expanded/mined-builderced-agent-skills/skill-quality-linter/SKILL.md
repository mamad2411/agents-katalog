---
name: skill-quality-linter
description: Validate SKILL.md structure, frontmatter completeness, token budget, freshness, naming conventions, and cross-platform portability before publishing.
version: "1.0.0"
last-updated: "2026-04-22"
model_tested: "claude-sonnet-4-6"
category: security
platforms: [claude-code, codex, gemini-cli, cursor, copilot, windsurf, cline]
language: en
geo_relevance: [global]
priority: medium
dependencies:
  mcp: []
  skills: [skill-security-audit]
  apis: []
  data: []
update_sources:
  - url: "https://code.claude.com/docs/en/skills"
    check_frequency: "quarterly"
    last_checked: "2026-04-22"
license: MIT
---

# Skill Quality Linter

## When to Use

- Before publishing a new skill to a registry
- Reviewing a skill PR
- Auditing existing skill quality
- Setting up CI for a skill repository

## Lint Checks

### 1. Frontmatter (Required Fields)

| Field | Required | Format |
|-------|----------|--------|
| name | YES | kebab-case, matches directory name |
| description | YES | 1 line, max 250 chars, starts with verb |
| version | YES | Semver (X.Y.Z) |
| last-updated | YES | YYYY-MM-DD, not in future |
| platforms | YES | Array of known platform names |
| license | YES | Valid SPDX identifier |
| dependencies | RECOMMENDED | Object with mcp, skills, apis, data |
| update_sources | RECOMMENDED | Array with url + check_frequency |
| language | RECOMMENDED | ISO 639-1 (en, fr, etc.) |
| geo_relevance | RECOMMENDED | Array (global, fr, eu, africa, etc.) |
| category | RECOMMENDED | Matches parent directory name |
| priority | OPTIONAL | critical, high, medium, low |

### 2. Structure

| Check | Rule |
|-------|------|
| Starts with `---` | Valid YAML frontmatter |
| Has `# Title` | H1 heading after frontmatter |
| Has `## When to Use` | Trigger conditions documented |
| Has `## What This Skill Does NOT Do` | Limitations section present |
| No H1 other than title | Single H1 only |
| Sections use H2 (`##`) | Consistent hierarchy |

### 3. Size Budget

| Metric | Limit | Rationale |
|--------|-------|-----------|
| SKILL.md lines | < 800 | ETH Zurich: more = worse perf |
| SKILL.md tokens | < 2500 | Context window budget |
| SKILL.md + references/ | < 3000 tokens | Total load budget |
| references/ file count | < 5 | Keep focused |

### 4. Portability

| Check | Rule |
|-------|------|
| No tool-specific syntax | No `Read`, `Write`, `Bash`, `Edit` references |
| No platform-specific imports | No `import`, `require`, `from` in instructions |
| Natural language instructions | Steps readable by any agent |
| Graceful degradation | "If terminal available... otherwise..." pattern |

### 5. Freshness

| Age | Status |
|-----|--------|
| < 60 days | PASS |
| 60-90 days | WARN — review needed |
| > 90 days | FAIL — must update before use |

### 6. Naming

| Check | Rule |
|-------|------|
| Directory name | kebab-case, no uppercase |
| name field | Matches directory exactly |
| description | Starts with action verb (Guide, Build, Detect, Generate...) |
| No emoji in name/description | Plain text only |

## Output Format

```
LINT: {skill-name}
Status: PASS | WARN | FAIL

[PASS] Frontmatter: all required fields present
[PASS] Structure: all sections present
[WARN] Size: 2800 tokens (approaching 3000 limit)
[PASS] Portability: no platform-specific syntax
[PASS] Freshness: 5 days old
[PASS] Naming: matches conventions

Verdict: PASS (1 warning)
```

## What This Skill Does NOT Do

- Does not check factual accuracy of content
- Does not validate referenced URLs (use separate check)
- Does not scan for security issues (see `skill-security-audit`)
- Does not auto-fix issues (reports only)
