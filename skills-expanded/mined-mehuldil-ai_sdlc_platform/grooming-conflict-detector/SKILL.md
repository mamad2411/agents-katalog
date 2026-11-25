---
name: grooming-conflict-detector
description: Detect resource conflicts, skill gaps, and schedule blockers
model: sonnet-4-6
token_budget: {input: 3000, output: 1500}
---

# Grooming Conflict Detector Skill

Identify conflicts in resource availability, skill gaps, and scheduling issues.

## Conflict Categories

- **Resource Conflict**: Team member needed for multiple stories
- **Skill Gap**: Required expertise not available
- **Schedule Conflict**: Deadline vs capacity issue
- **Dependency Block**: External blocker preventing progress
- **Team Capacity**: Insufficient team size for scope

## Analysis

- Check team member availability
- Verify skill requirements covered
- Validate timeline feasibility
- Identify blocking dependencies
- Assess capacity vs workload

## Triggers

Use this skill when:
- Grooming story assignments
- Planning sprint commitments
- Checking feasibility before approval
- Identifying schedule risks

## Inputs

- Story requirements and AC
- Team member availability
- Required skills/expertise
- Timeline constraints

## Outputs

- Conflict report
- Suggested resolutions
- Risk assessment
- Recommended adjustments

## Quality

- Accurate availability data
- Skill matching complete
- Realistic timeline assessment
- Clear mitigation suggestions
