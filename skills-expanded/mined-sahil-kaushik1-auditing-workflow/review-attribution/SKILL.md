---
name: review-attribution
description: >
  When a known vulnerability is missed, attribute the failure to the correct pipeline
  component. Prevents global prompt dumping by ensuring changes are local and measured.
---

# Review Attribution Skill

## Purpose

When the system misses a known vulnerability, determine WHERE in the pipeline the failure
occurred. This prevents the anti-pattern of adding global rules for every miss.

## When to Use

- After benchmarking against a known-vulnerability dataset
- When a client reports a bug the system missed
- During Evolution Manager analysis

## The 8 Failure Categories

Trace through the pipeline in order. Stop at the FIRST failure point.

### 1. Task-Design Failure
**Question**: Did any task target this root cause?
**Check**: Search `specs/tasks/` for a task whose invariant or failure predicate
relates to the missed vulnerability.
**If NO** → The Threat Modeler failed to create the right task.
**Fix**: Improve decomposition-to-task compilation patterns.

### 2. Missing Failure Predicate
**Question**: Did the relevant task define the specific failure condition?
**Check**: Read the task's `Failure Predicate` field.
**If vague or wrong** → The task was poorly defined.
**Fix**: Improve task-compilation skill templates.

### 3. Missing Witness Requirement
**Question**: Did the task require concrete evidence of this type?
**Check**: Read the task's `Required Witness` field.
**If too generic** → The reasoner had no concrete target.
**Fix**: Improve witness specification patterns.

### 4. Context Failure
**Question**: Was the relevant code/state provided to the reasoner?
**Check**: Read `specs/context/TASK-{N}-context.md`.
**If relevant contract/function was excluded** → Context Builder failed.
**Fix**: Improve context extraction rules.

### 5. Reasoning Failure
**Question**: Task + context were correct, but the model didn't find it?
**Check**: Read `specs/reasoning/TASK-{N}-reasoning.md`.
**If the analysis went in the wrong direction** → Model limitation.
**Fix**: Improve drift anchors, add more specific constraints to task.

### 6. Verification Failure
**Question**: Was the issue found by the reasoner but not verified?
**Check**: Read `specs/verification/TASK-{N}-verification.md`.
**If PoC was incorrect or incomplete** → Verifier failed.
**Fix**: Improve foundry-harness skill or verification protocol.

### 7. Artifact Failure
**Question**: Was the issue found + verified but not in structured output?
**Check**: Search `findings/` for the issue.
**If absent** → Report Compiler lost it.
**Fix**: Improve report compilation pipeline.

### 8. Reporting Failure
**Question**: Was it in findings but lost/filtered in the final report?
**Check**: Read `findings/EXECUTIVE-SUMMARY.md`.
**If missing** → Executive summary generation filtered it out.
**Fix**: Improve reporting templates.

## Output

Save attribution to: `specs/evolution/ATTRIBUTION-{finding-id}.md`

```markdown
# Attribution: {Finding ID}

## Missed Vulnerability
[Description of what was missed]

## Failure Category
[1-8, with name]

## Root Cause of Miss
[Specific explanation of why the pipeline component failed]

## Proposed Fix
[Local change to the specific component]

## Affected Component
[Exact file path of the component to modify]
```

## Rules

- Only fix the FIRST failure point (don't fix downstream symptoms)
- Only promote a fix to global config if it works across 3+ projects
- Document the fix as an experiment, measure before inheriting
