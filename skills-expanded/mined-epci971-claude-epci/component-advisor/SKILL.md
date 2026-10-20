---
name: component-advisor
description: >-
  Passive detection of EPCI component creation opportunities. Identifies
  repetitive patterns that could become skills, commands or subagents.
  Use when: workflow analysis, recurring pattern detection.
  Not for: active component creation (use /epci:create).
---

# Component Advisor

## Overview

Passive skill that detects opportunities for new EPCI component creation
based on usage pattern analysis.

**Reference Documents:**
- [Detection Patterns](references/detection-patterns.md) — Scoring criteria and thresholds
- [Suggestion Examples](references/suggestion-examples.md) — Real-world suggestion templates

## Automatic Detection

### New Skill Indicators

| Signal | Score | Example |
|--------|-------|---------|
| Pattern repeated 3+ times | +3 | Same validation in multiple commands |
| Technical domain not covered | +2 | New unsupported stack |
| Documentation frequently consulted | +2 | Repeated searches on same topic |
| Copy-paste of guidelines | +1 | Same conventions applied |

**Suggestion threshold:** Score ≥ 4

### New Command Indicators

| Signal | Score | Example |
|--------|-------|---------|
| Repeated action sequence | +3 | Same recurring manual workflow |
| Frequent skill combination | +2 | Always the same skills together |
| Documented but not automated process | +2 | Guide followed manually |
| Explicit user request | +3 | "I'd like a command for..." |

**Suggestion threshold:** Score ≥ 4

### New Subagent Indicators

| Signal | Score | Example |
|--------|-------|---------|
| Repeated specialized validation | +3 | Specific security check |
| Recurring manual review | +2 | Same checklist applied |
| Narrow domain expertise | +2 | Specialized knowledge required |
| Standardized report format | +1 | Same report structure |

**Suggestion threshold:** Score ≥ 4

## Suggestion Format

When a threshold is reached:

```markdown
💡 **COMPONENT OPPORTUNITY DETECTED**

### Suggested Type: [Skill | Command | Subagent]

**Identified pattern:**
[Description of detected pattern]

**Occurrences:**
- [Occurrence 1]
- [Occurrence 2]
- [Occurrence 3]

**Estimated benefits:**
- [Benefit 1]
- [Benefit 2]

**Proposal:**
```
/epci:create [type] [suggested-name]
```

**Confidence score:** [X/10]

---
*Automatic suggestion - Ignore if not relevant*
```

## Monitored Patterns

### For Skills

| Pattern | Potential Domain |
|---------|------------------|
| Repeated searches on a tech | New stack skill |
| Manually applied conventions | Conventions skill |
| Often cited best practices | Patterns skill |
| Frequently used external tools | Integration skill |

### For Commands

| Pattern | Potential Command |
|---------|-------------------|
| Repeated tool sequence | Composite command |
| Manual multi-step workflow | Automation command |
| Process with breakpoints | Structured command |
| Action + validation + report | Workflow command |

### For Subagents

| Pattern | Potential Subagent |
|---------|-------------------|
| Recurring validation | Validator agent |
| Specialized analysis | Analyzer agent |
| Review with checklist | Reviewer agent |
| Formatted generation | Generator agent |

## Configuration

### Enable/Disable

The component-advisor is passive by default.
It observes and suggests without interrupting workflow.

### Customizable Thresholds

```yaml
component_advisor:
  skill_threshold: 4
  command_threshold: 4
  subagent_threshold: 4
  suggestion_frequency: "on_pattern_detected"  # or "end_of_session"
```

## Detection Examples

### Example 1: New Skill Detected

```
💡 COMPONENT OPPORTUNITY: Skill

Pattern: Kubernetes documentation consulted 5 times
         Same deployment structure applied 3 times

Suggestion: /epci:create skill kubernetes-patterns

Benefits:
- Auto-detection of K8s projects
- Standardized patterns
- Reduced search time
```

### Example 2: New Command Detected

```
💡 COMPONENT OPPORTUNITY: Command

Pattern: Repeated sequence
         1. Lint → 2. Test → 3. Build → 4. Deploy

Suggestion: /epci:create command ci-pipeline

Benefits:
- Process automation
- Consistency across projects
- Time savings
```

### Example 3: New Subagent Detected

```
💡 COMPONENT OPPORTUNITY: Subagent

Pattern: Accessibility checklist applied 4 times
         Same report format generated

Suggestion: /epci:create agent a11y-auditor

Benefits:
- Automatic audit
- Standardized report
- No missed criteria
```

## Metrics

| Metric | Description |
|--------|-------------|
| Patterns detected | Number of patterns identified |
| Suggestions issued | Number of suggestions proposed |
| Suggestions accepted | Components actually created |
| Adoption rate | % suggestions → components |

## Limitations

- Detection based on current session
- No memory between sessions (unless context provided)
- Suggestions are indicative, not prescriptive
- Requires repeated patterns to detect
