---
name: evaluate-schema
description: >
  Comprehensive database schema analysis using 5-expert panel evaluation.
  PROACTIVELY activate for: (1) schema review, (2) data modeling decisions,
  (3) database design evaluation, (4) migration planning, (5) normalization analysis.
  Triggers: "evaluate schema", "review schema", "database design", "data model review",
  "schema analysis", "evaluate database"
argument-hint: [schema DDL, file path, or description]
---

# Evaluate Schema

Comprehensive database schema analysis using a 5-perspective expert panel.

## When to Use

Use this skill when you need to:
- Review a database schema for quality and best practices
- Evaluate data modeling decisions before implementation
- Plan schema migrations with risk assessment
- Analyze normalization and denormalization trade-offs
- Assess schema scalability and performance implications

## Workflow

Invoke the `database-schema-evaluator` skill for:

$ARGUMENTS

### Default Parameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| `evaluation_depth` | comprehensive | Full 5-perspective analysis |
| `include_alternatives` | false | Focus on current schema; enable for redesign |
| `scoring_rubric` | standard | Balanced across all dimensions |

### Expert Panel Composition

The evaluation assembles 5 domain experts:

| Expert | Focus Area | Key Questions |
|--------|-----------|---------------|
| **Data Architect** | Normalization, patterns, relationships | Is the schema properly normalized? Are relationships clear? |
| **Performance Engineer** | Indexing, query optimization, scalability | Will this scale? Are indexes appropriate? |
| **Data Integrity Guardian** | Constraints, referential integrity, validation | Can invalid data enter? Are constraints complete? |
| **Evolution Strategist** | Migrations, extensibility, versioning | How hard will changes be? Is it future-proof? |
| **Operations Specialist** | Backup, maintenance, monitoring | Can we maintain this? Recovery implications? |

### Evaluation Dimensions

Each expert scores on their primary dimensions:

**Data Architect:**
- Normalization level (1NF-BCNF appropriateness)
- Relationship clarity
- Naming conventions
- Domain modeling accuracy

**Performance Engineer:**
- Index coverage
- Query pattern support
- Partitioning strategy
- Denormalization trade-offs

**Data Integrity Guardian:**
- Primary key design
- Foreign key completeness
- Check constraints
- NULL handling

**Evolution Strategist:**
- Additive change ease
- Breaking change risk
- Schema versioning support
- Migration complexity

**Operations Specialist:**
- Backup/restore complexity
- Monitoring surface area
- Maintenance windows required
- Disaster recovery impact

## Output Format

The schema evaluation produces:

```xml
<schema-evaluation>
  <header>
    <id>[unique identifier]</id>
    <schema_name>[schema identifier]</schema_name>
    <evaluation_depth>comprehensive</evaluation_depth>
    <overall_score>[1-10]</overall_score>
  </header>

  <expert-assessments>
    <assessment expert="Data Architect">
      <score>[1-10]</score>
      <findings>
        <finding severity="[critical|high|medium|low]">
          [Specific issue or observation]
        </finding>
      </findings>
      <recommendations>
        <recommendation priority="[1-n]">
          [Specific improvement suggestion]
        </recommendation>
      </recommendations>
    </assessment>
    <!-- ... more expert assessments ... -->
  </expert-assessments>

  <consensus-findings>
    <strengths>
      <strength>[What the schema does well]</strength>
    </strengths>
    <concerns>
      <concern severity="[critical|high|medium|low]" experts="[which experts flagged]">
        [Shared concern across experts]
      </concern>
    </concerns>
  </consensus-findings>

  <prioritized-recommendations>
    <recommendation priority="1" effort="[low|medium|high]" impact="[low|medium|high]">
      <description>[What to change]</description>
      <rationale>[Why this matters]</rationale>
      <example>[Concrete example if applicable]</example>
    </recommendation>
  </prioritized-recommendations>

  <migration-considerations>
    [If changes recommended, migration implications]
  </migration-considerations>
</schema-evaluation>
```

## Quality Gates

- [ ] All 5 expert perspectives represented
- [ ] Scores calibrated consistently across experts
- [ ] Critical issues flagged with severity
- [ ] Recommendations are specific and actionable
- [ ] Migration implications considered for recommended changes
- [ ] Trade-offs explicitly documented

## Related Skills

After schema evaluation, consider:
- Run `/compare-options` if multiple schema designs exist
- Run `/write-reference` to document the final schema
- Run `/research-brief` for technology-specific best practices
