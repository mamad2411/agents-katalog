---
name: production-agent-architecture
description: Design production-ready AI agents using a loop-based architecture with explicit tools, context, memory, permissions, observability, evaluation, and rollout planning.
---
# Production Agent Architecture

## When To Use This Skill
Use this skill when the task is to:
- design a new AI agent
- turn a chatbot idea into a real agent system
- hand off an agent build to developers or another AI coding agent
- adapt coding-agent architecture patterns to another domain

## Core Rule
Do not design the system as a one-shot chatbot unless the user explicitly asks for that.

Default to a loop-based runtime with:
1. controller loop
2. context builder
3. tool registry
4. tool executor
5. session state
6. permissions and approvals
7. observability
8. evaluation
9. reliability rules
10. rollout phases

## Design Workflow
1. define the user goal and success condition
2. define the controller loop
3. define 2 to 5 domain tools
4. define context inputs
5. define session state
6. define permissions and approval rules
7. define observability minimums
8. define evaluation plan
9. define reliability and retry rules
10. define rollout phases

## Required Output
Always produce all of the following:

```markdown
# Agent Build Spec

## Domain
## User goal
## Success condition
## Core workflow
## Controller loop
## Context inputs
## Tools
## Session state
## Permissions and approvals
## Stop conditions
## Observability
## Evaluation
## Reliability and failure handling
## Rollout phases
## Future extensions
```

After the spec, also produce:
- controller loop pseudocode
- tool contract table with input, output, side effects, timeout, and permission level
- session state schema
- approval matrix
- failure and retry strategy
- minimum logs and metrics

## Guardrails
- separate tool schemas from executors
- treat permissions as runtime policy, not prompt text
- make approval flows explicit
- do not pretend a vague idea is production-ready
- explain the design plainly if the user is learning
