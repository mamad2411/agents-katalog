---
name: workflow-router
description: "Standardize workflow classification and skill selection before execution. Use when a task requires explicit known-vs-unknown workflow judgment, temporary workflow creation, workflow-local skill shortlist construction, or a decision on whether a new skill should be created."
---

# Workflow Router

## Role Boundary

This skill is the canonical routing owner for the agent+skill system.

The agent still owns repo-wide governance and user communication, but reusable routing policy must live here rather than in `AGENTS.md`, `workflow-scoped-execution`, or compatibility shims.

## Use This Skill When

Use this skill when:
- a task needs explicit `known` vs `unknown` workflow judgment,
- the correct workflow is not obvious,
- the agent needs a workflow-local skill shortlist,
- a temporary workflow must be created,
- or there is a question about whether a new skill is justified.

Use this skill as the single source of truth for:
- request-pattern to skill mapping,
- workflow classification,
- skill shortlist construction,
- new-skill creation decision.

## Required Output

Every routing decision should produce:
1. `workflow_status = known | unknown`
2. `workflow_name = <name>`
3. `workflow_family = <direct_specialist | scoped_execution | research_chain | maintenance | utility | temporary>`
4. `workflow_owner_skill = <skill that owns orchestration for this workflow>`
5. `reason = <why this workflow fits or why no known workflow fits>`
6. `allowed_skill_subset = [...]`
7. `next_skill = <selected owner skill or next bounded stage>`
8. `eda_loop_role = owner | delegated_stage | not_used`
9. `new_skill_decision = reuse_existing | create_new_skill | defer`
10. `new_skill_reason = <boundary/specialization judgment>`

The agent must surface the routing result to the user in a short explicit form rather than treating it as internal-only metadata.

## Knowledge And Tool Interaction

1. Read `AGENTS.md`, the skill manifest, and relevant skill docs before making reusable routing decisions.
2. If a task first needs shared KB/tool lookup before routing can be made cleanly, delegate that retrieval step to `eda-context-accessor`.
3. When routing exposes a structural gap, hand off the maintenance action to `eda-infra-maintainer` instead of silently inventing policy inside this skill.

## Design Principle

The system should evolve like this:
- user does not choose skills,
- agent does not micromanage tool internals,
- workflow narrows the search space,
- skills provide bounded expertise,
- and new skills are added only when boundary and professionalism justify them.

For workflow-owner skills specifically:
- keep owner skills stable as control-plane nodes,
- prefer capability growth in lower-layer specialist or utility skills,
- and escalate owner-skill edits only when orchestration semantics or owner/delegate boundaries must change.

## Operational References

1. Load `references/workflow-classification.md` when you need to decide whether the task fits a known workflow or requires a temporary workflow.
2. Load `references/workflow-owner-contract.md` when deciding which skill should own orchestration and whether `workflow-scoped-execution` is owner, delegated stage, or unused.
3. Load `references/request-pattern-routing.md` when the request can be matched by pattern and you need the canonical request-to-workflow-owner mapping plus quick routing examples.
4. Load `references/skill-selection-and-new-skill-decision.md` when choosing the minimal skill subset or deciding whether to reuse, defer, or create a new skill.
5. Load `references/routing-disclosure-format.md` when surfacing the routing decision to the user.
