---
name: agent-autonomy
description: Operating mode rules for custom agents that can run either under a team lead or independently. Use when an agent must decide whether to follow team artifacts or work directly from the user request.
user-invocable: false
---

# Agent Autonomy

Custom agents must be able to operate in two modes: coordinated by a team lead, or directly invoked by the user. The lead is an orchestrator for large team workflows, not a required dependency for every agent.

## Mode Detection

Use **Team Mode** when the prompt includes a team lead, feature name, project root, plan path, sub-branch, worktree, or `agents/{feature-name}/` artifact paths.

Use **Standalone Mode** when the user invokes the agent directly without team workflow context.

If the mode is unclear, infer from the prompt and proceed. Ask only when the difference changes the work product or could cause destructive git/file operations.

## Team Mode

- Follow the team workflow, artifact paths, branch rules, and escalation paths provided by the lead.
- Treat the provided plan/report/track files as coordination artifacts.
- Message the lead for requirement ambiguity, cross-role dependencies, or decisions that need team arbitration.
- Keep reports and track files concise; do not paste full logs, full diffs, or large screenshots into artifacts.

## Standalone Mode

- Work directly from the user's request and the current workspace.
- When the user asks for independent work across multiple projects or repositories, run one standalone subagent per project when practical, and keep the main session responsible for coordination and acceptance.
- Discover the project structure, conventions, commands, and relevant files yourself.
- Do not require `agents/{feature-name}/plan.md`, team artifacts, a sub-branch, or a worktree.
- Use the current branch unless the user explicitly asks for a branch/worktree.
- Ask the user only for blocking product or requirement ambiguity.
- Produce the role's deliverable directly: plan, implementation, tests, review findings, or QA report.
- Verify your own work within the role's scope.
- If no separate QA agent is present, implementation agents should add or update focused tests for production-risk behavior they changed.
- If no architecture plan is provided, create a brief internal implementation plan before editing, then proceed.
- If no report path is provided, summarize findings/results directly to the user.

## Escalation Without A Lead

When standalone, escalate to the user instead of a lead for:

- Ambiguous requirements that change behavior or architecture.
- Risky database migrations, public API changes, or security-sensitive choices.
- Destructive git/file operations.
- Conflicts between requested behavior and existing project conventions.

Make your own judgment for local implementation details, naming, file organization, and small deviations that follow project conventions.