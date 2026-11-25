---
name: backlog-management
description: Manage the feature backlog from docs/features/ and Git issues. Prioritizes features, tracks readiness, identifies specs missing details, and surfaces what needs human input. Used by the multi-agent-project-manager agent.
origin: AI Dev Kit
---

# Backlog Management

Manage the feature backlog from `docs/features/` and Git issues. Prioritize, track readiness, identify missing details, and surface what needs human input.

## When to Use

- The multi-agent-project-manager agent scans for new work in its 60-second cycle
- A user wants to see what features are in the backlog
- A feature spec is incomplete and needs human input before a workflow can start
- Reprioritization is needed due to changing business needs

## Backlog Sources

### Source 1: Feature Specs (`docs/features/`)

```bash
# Scan for all feature specs
find docs/features -name "spec.md" -type f
```

Each spec in `docs/features/<name>/spec.md` should have:

```yaml
---
name: <feature-name>
version: 1.0.0
status: proposed | approved | in_progress | done | rejected
created: YYYY-MM-DD
author: <name>
priority: 1-10
---
```

### Source 2: Git Issues

```bash
gh issue list --state open --label "feature" --json number,title,labels
```

## Backlog States

```
new → ready → approved → in_progress → done
         ↓
      needs_human_input
```

| State | Meaning |
|---|---|
| `new` | Spec/issue exists but has not been reviewed |
| `ready` | Spec has all required fields, acceptance criteria defined |
| `approved` | Human has reviewed and approved the spec for implementation |
| `in_progress` | Multi-agent workflow is running |
| `done` | Merged to main |
| `needs_human_input` | Spec is missing critical details — cannot proceed without human |

## Spec Completeness Check

Before a feature enters the `ready` state, validate it has all required information:

```yaml
required_fields:
  - name: "Feature name is present"
  - name: "Problem statement is clear"
  - name: "Proposed solution exists"
  - name: "Acceptance criteria are defined (at least 2)"
  - name: "Affected surfaces are identified"
  - name: "Dependencies are listed (or 'none')"
  - name: "Risk level is assessed"

optional_but_recommended:
  - name: "User stories with acceptance criteria"
  - name: "Technical constraints documented"
  - name: "Success metrics defined"
  - name: "Timeline/deadline specified"
```

### Missing Details Detection

```python
def check_spec_completeness(spec_path):
    spec = parse_frontmatter(spec_path)
    content = read_markdown_body(spec_path)

    missing = []

    if not spec.get("name"):
        missing.append("Feature name missing")
    if "problem" not in content.lower() and "why" not in content.lower():
        missing.append("Problem statement unclear — why is this needed?")
    if "acceptance" not in content.lower() and "criteria" not in content.lower():
        missing.append("Acceptance criteria not defined")
    if "scope" not in content.lower() and "affected" not in content.lower():
        missing.append("Affected surfaces not identified")

    return {
        "complete": len(missing) == 0,
        "missing": missing,
        "action": "ready" if len(missing) == 0 else "needs_human_input"
    }
```

## Priority Scoring

```yaml
priority_scoring:
  business_impact:
    revenue_affecting: 10
    user_facing: 7
    internal_tooling: 4
    tech_debt: 3
  urgency:
    security_fix: 10
    production_bug: 9
    deadline_driven: 8
    scheduled: 5
    backlog: 2
  dependencies:
    no_blockers: 10
    blocked_by_1: 7
    blocked_by_2_plus: 3
  complexity:
    trivial_auto_approve: 10
    small_1_surface: 8
    medium_2_3_surfaces: 5
    large_4_plus_surfaces: 3
    massive_full_stack: 1

  final_score = weighted_average(business_impact, urgency, dependencies, 1/complexity)
```

## Backlog Operations

### Add to Backlog

```bash
# Create a new feature spec
mkdir -p docs/features/<feature-name>
cat > docs/features/<feature-name>/spec.md << 'EOF'
---
name: <feature-name>
version: 1.0.0
status: proposed
created: $(date +%Y-%m-%d)
author: <name>
---

# Feature: <Title>

## Problem
<What problem does this solve?>

## Proposed Solution
<How will it be solved?>

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2

## Affected Surfaces
- List files/directories that will change

## Dependencies
- List dependencies or "none"

## Risk Level
low/medium/high
EOF
```

### Move Between States

```bash
# Update status in spec frontmatter
python3 -c "
import frontmatter
post = frontmatter.load('docs/features/<name>/spec.md')
post['status'] = 'approved'  # or 'in_progress', 'done', 'rejected'
with open('docs/features/<name>/spec.md', 'w') as f:
    f.write(frontmatter.dumps(post))
"
```

### Report Backlog

```
BACKLOG REPORT:

  Ready for work (approved, waiting for agents):
    1. <feature-name>     Priority: 8/10  Est. agents: 3

  Needs human input:
    1. <feature-name>     Missing: Acceptance criteria, OAuth provider decision
    2. <feature-name>     Missing: Affected surfaces not identified

  New (not yet reviewed):
    1. <feature-name>     Created: 2026-04-12

  In progress:
    1. <feature-name>     Wave: executing (5 agents active)
```

## Integration with Multi-Agent Project Manager

The PM agent calls this skill during its 60-second cycle:

```
Step 1 of PM loop: SCAN FOR NEW WORK
  → Call backlog-management skill
  → Scan docs/features/ for new/updated specs
  → Check completeness of each spec
  → Score priority
  → Move complete specs to "ready" queue
  → Flag incomplete specs as "needs_human_input"
  → Update backlog report
```
