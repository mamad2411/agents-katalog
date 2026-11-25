---
name: architecture
description: Use this skill when the user wants "architecture" work but the scope is ambiguous and you want auto-classification — as the architecture entry-point router that classifies the request as feature design, existing-system analysis, or migration/evolution and then dispatches to `/architecture-design`, `/architecture-analyze`, or `/architecture-evolve`. For a known scope, invoke the specialized command directly instead.
context: fork
argument-hint: "<feature PRD, analysis request, or migration brief>"
---

# /architecture — Scope Router

Thin dispatcher. The bulk of architecture work lives in three specialized skills with focused scopes:

| Skill | Scope | Routes to |
|---|---|---|
| `/architecture-design` | Feature-level design from a PRD | `Agent(solution-architect)` (default), `Agent(cloud-architect)` (`--cloud`), `Agent(devops-architect)` (`--cicd`) |
| `/architecture-analyze` | Document existing system; gap analysis; tech-debt register | `Agent(system-architect)` (default), `Agent(cloud-architect)` (`--cloud`), `Agent(devops-architect)` (`--cicd`) |
| `/architecture-evolve` | Migration / redesign / cross-tech evolution | `Agent(solution-architect)` + `Agent(system-architect)` |

## When to use

- Scope is unclear and you want auto-classification
- Quick entry point when you do not remember the specialized command name

For known scope, prefer the specialized command directly — it avoids the dispatch round-trip.

## Behavior

1. Read the user's input.
2. Classify scope via these triggers:

| Trigger phrase | Classified as |
|---|---|
| "PRD", "feature", "design", "new capability", "endpoint", "API" | Feature design |
| "analyze", "document architecture", "audit", "tech debt", "what do we have" | Analysis |
| "migrate", "redesign", "from X to Y", "replace", "evolve", "modernize" | Evolution |
| "cloud", "GCP", "Azure", "AWS", "landing zone", "networking", "VPC" | + `--cloud` flag |
| "CI/CD", "pipeline", "deployment", "GitHub", "platform engineering" | + `--cicd` flag |

3. Announce the classification and dispatch:

```
Classified as: <feature design | analysis | evolution> [+ <flag>]
Dispatching to: /architecture-<design | analyze | evolve> [<flag>]
```

4. If the input contains conflicting signals (e.g. both "PRD for new feature" and "migrate from old system") — present the candidate classifications to the user and ask. Do not pick silently.

5. If the input is too sparse to classify — ask the user one clarifying question (scope: design / analyze / evolve?) before dispatching.

## Why this exists

The previous monolithic `/architecture` skill bundled all three scopes inline and crowded the 12K skill-body limit. Splitting into three focused workflows (per the agentskills.io single-responsibility recommendation) keeps each scope readable, lets each declare scope-specific NFRs and quality gates, and avoids step duplication for users who already know their scope.

## Integration

- **Dispatches to**: `/architecture-design`, `/architecture-analyze`, `/architecture-evolve`
- **Templates**: shared at `${CLAUDE_PLUGIN_ROOT}/skills/architecture/assets/` (adr-template, c4-mermaid-template, nfr-template, gap-analysis-template, tech-debt-register-template) — referenced by all three specialized skills
