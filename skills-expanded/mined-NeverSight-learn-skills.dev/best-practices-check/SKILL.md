---
name: best-practices-check
description: >
  Verify skills-for-fabric against Microsoft Fabric best practices from the internet. Searches for current
  best practices, compares them against skill content, and identifies gaps or improvements. Use when
  the user wants to: (1) validate a skill covers industry best practices, (2) find missing guidance,
  (3) improve skill quality with current recommendations. Triggers: "check best practices",
  "validate best practices", "best practices for", "compare against best practices", "skill coverage".
---

# Best Practices Verification

Verify that skills in this repository align with current Microsoft Fabric best practices from official documentation and community sources.

## When to Use

- After creating or updating a skill
- To ensure a skill covers recommended patterns
- To identify gaps in guidance
- Before major releases to validate content currency

## Workflow

### Step 1: Identify Target Skill

Parse the user's request to identify which skill to verify:

| User Request | Target Skill |
|--------------|--------------|
| "check best practices for spark consumption" | `spark-consumption-cli` |
| "validate best practices for sqldw authoring" | `sqldw-authoring-cli` |
| "best practices for medallion" | `skills/e2e-medallion-architecture/SKILL.md` |
| "check best practices for SQL endpoint" | `sqldw-consumption-cli` |

**Skill name normalization:**
- "spark" → `spark-authoring-cli` or `spark-consumption-cli` (ask if ambiguous)
- "sqldw", "warehouse", "SQL endpoint" → `sqldw-authoring-cli` or `sqldw-consumption-cli`
- "medallion", "bronze/silver/gold" → `skills/e2e-medallion-architecture/SKILL.md`
- "data engineering" → `spark-authoring-cli`

### Step 2: Read Skill Content

Load the target skill's SKILL.md and any referenced resources:

```bash
# Example: Read skill content
cat skills/spark-consumption-cli/SKILL.md

# If skill has resources folder, read those too
ls skills/spark-consumption-cli/resources/ 2>/dev/null && \
  cat skills/spark-consumption-cli/resources/*.md
```

Extract key topics covered:
- Must/Prefer/Avoid guidance
- Specific patterns mentioned
- Technologies referenced
- Example scenarios

### Step 3: Search for Current Best Practices

Use web search to find current Microsoft Fabric best practices. **Always include "Microsoft Fabric" in search queries** to ensure results are Fabric-specific.

**Search queries to execute** (adjust based on skill topic):

| Skill Type | Search Queries |
|------------|----------------|
| Spark/Data Engineering | "Microsoft Fabric Spark best practices 2025", "Fabric Lakehouse optimization", "Fabric notebook development best practices" |
| SQL Endpoint/Warehouse | "Microsoft Fabric Data Warehouse best practices", "Fabric T-SQL performance optimization", "Fabric SQL endpoint security best practices" |
| Medallion Architecture | "Microsoft Fabric medallion architecture best practices", "Fabric Bronze Silver Gold layer design", "Fabric lakehouse data modeling" |
| General | "Microsoft Fabric {topic} best practices", "Fabric {topic} performance tuning", "Fabric {topic} security" |

**Priority sources** (weight these higher):
1. `learn.microsoft.com/en-us/fabric/` — Official Microsoft documentation
2. `blog.fabric.microsoft.com/` — Official Fabric blog
3. `techcommunity.microsoft.com/` — Microsoft Tech Community
4. Recent conference talks (Ignite, Build) transcripts
5. Fabric CAT team blogs and whitepapers

### Step 4: Compare and Analyze

Create a comparison matrix:

```markdown
| Best Practice | Source | Covered in Skill? | Notes |
|---------------|--------|-------------------|-------|
| Use starter pools for Livy sessions | MS Docs | ✅ Yes | Session Management |
| Enable adaptive query execution | Tech Community | ⚠️ Partial | Mentioned but no config example |
| Avoid SELECT * on large tables | MS Docs | ✅ Yes | Avoid section |
| Use V-Order for read-heavy workloads | Fabric Blog | ❌ No | Gap - should add |
```

### Step 5: Generate Report

Produce a structured report:

```markdown
## Best Practices Verification Report

**Skill:** spark-consumption-cli
**Date:** {current_date}
**Sources Consulted:** {list_of_sources}

### Summary

| Category | Count |
|----------|-------|
| ✅ Covered | X |
| ⚠️ Partial | Y |
| ❌ Gap | Z |

### Fully Covered Best Practices

1. **{Practice Name}** — {brief description}
   - Source: {URL}
   - Skill location: {section reference}

### Partially Covered (Needs Enhancement)

1. **{Practice Name}** — {what's missing}
   - Source: {URL}
   - Current coverage: {what exists}
   - Recommendation: {specific improvement}

### Gaps (Not Covered)

1. **{Practice Name}** — {description}
   - Source: {URL}
   - Why important: {impact}
   - Suggested addition: {where to add and what content}

### Recommendations

1. {Priority 1 recommendation}
2. {Priority 2 recommendation}
3. {Priority 3 recommendation}
```

## Must

- **Always search with "Microsoft Fabric"** in query — generic Spark/SQL results may not apply
- **Cite sources** for every best practice identified
- **Read the actual skill content** before comparing — don't assume
- **Distinguish between authoring and consumption** — best practices differ
- **Check publication dates** — prefer content from 2024-2025; flag older sources
- **Focus on actionable gaps** — prioritize high-impact missing guidance

## Prefer

- Official Microsoft documentation over community posts
- Recent content (last 12 months) over older articles
- Fabric-specific guidance over generic Spark/SQL advice
- Concrete, implementable recommendations over vague suggestions
- Linking to common/ documents for foundational patterns
- Grouping related gaps into single recommendations

## Avoid

- Generic cloud data platform advice not specific to Fabric
- Outdated patterns (pre-GA Fabric guidance may be obsolete)
- Nitpicking minor omissions — focus on material gaps
- Recommending changes that duplicate content in common/ files
- Suggesting additions that would exceed skill token budget (15K warning threshold)

## Example Usage

### User Prompt

> "Check best practices for spark consumption"

### Expected Response

```markdown
## Best Practices Verification: spark-consumption-cli

**Sources consulted:**
- Microsoft Learn: Fabric Spark development best practices
- Fabric Blog: Optimizing Livy sessions
- Tech Community: Fabric Lakehouse query patterns

### Summary: 8 covered, 2 partial, 3 gaps

### ✅ Fully Covered
1. **Session reuse over creation** — Skill explicitly checks for idle sessions (Must section)
2. **Use starter pools** — Configured in session creation (Must section)
3. **Avoid large result sets without LIMIT** — In Avoid section

### ⚠️ Partial Coverage
1. **Adaptive query execution** — Mentioned in config but no explanation of when to enable/disable
   - Recommendation: Add brief guidance on AQE tuning for different workload types

### ❌ Gaps
1. **Caching strategies for repeated queries**
   - Source: [MS Learn - Spark caching](https://learn.microsoft.com/...)
   - Recommendation: Add section on `.cache()` and `.persist()` for iterative analysis

2. **Cross-workspace query patterns**
   - Source: [Fabric Blog - Multi-workspace analytics](https://blog.fabric.microsoft.com/...)
   - Recommendation: Add example of querying across workspaces with proper shortcuts

### Priority Recommendations
1. Add caching guidance to Prefer / Data Exploration section
2. Expand AQE documentation with workload-specific configs
3. Add cross-workspace query example
```

## Integration with Quality Check

Run this skill **after** the `quality-check` skill:

1. `quality-check` validates structure and compliance
2. `best-practices-check` validates content quality and completeness

Together they ensure skills are both well-formed and comprehensive.

## Limitations

- Web search results may vary; re-run periodically
- Some best practices are context-dependent — use judgment
- New Fabric features may not have documented best practices yet
- Enterprise-specific guidance (security, compliance) may require internal sources
