---
name: codex-harness
description: "Design or update a specialized Codex harness: define role-specific agents, generate an orchestrator skill and AGENTS.md, and connect work to the shared to-spec/to-issues tracker contract. Use for requests to build a Codex harness, create a Codex agent team, or change an existing harness's roles, workflow, or project policy."
---

# Codex Harness Meta-Skill

Generate a project-specific harness using native Codex subagents, shared work records, and verifiable outputs. The main Orchestrator delegates and aggregates; no separate agent-team runtime or local execution-state engine is required.

## Phase 0: Inspect and scope

Read existing project instructions, agent definitions, skills, and the current request. Preserve user edits and decisions already supplied. Do not treat the presence of an old execution workspace as a reason to resume or reset it.

For an existing harness, use `references/expansion-matrix.md`. For request examples, use `references/usage-examples.md`. Only generate or modify the components needed for the request.

## Phase 1: Work and audience policy

Apply `references/project-policy.md`:
- Natural-language requests are valid inputs. For actionable work, ask existing issue / new issue / no issue only if the user has not already chosen.
- Share `.scratch/.tracker` with `to-spec` and `to-issues`; do not introduce another tracker configuration.
- One issue represents a work unit with completion criteria, not an agent invocation or retry.
- Read the selected issue/spec and actual project artifacts before executing or resuming work.
- Update progress and evidence at meaningful milestones. Close an issue only on user request.
- Reuse the existing explanation profile, or ask for domain-specific familiarity with suggested choices and free text before writing AGENTS.md.

The publication skills and their shared tracker contract are external dependencies. Missing dependencies must be reported; they do not prevent explicitly issue-free work.

## Phase 2: Roles and coordination

Choose the smallest sufficient set of roles from `references/schemas/models.md`. Do not generate a State Manager. Single focused work may run directly; delegate only when the work benefits from a separate role.

Use `references/agent-design-patterns.md` to choose sequential, parallel, review-loop, specialist, supervisor, hierarchical, or handoff coordination. Only the main Orchestrator spawns subagents. Team leads propose decomposition; they do not spawn workers.

Assign each worker a bounded objective, relevant context, allowed scope, dependencies, expected output, and verification. For parallel edits, use non-overlapping file ownership or isolated worktrees and define who integrates the results.

Select the least permissions needed. Read-only analysis may use `read-only`; editing and test execution may require `workspace-write`. Do not grant full access just because the role is Operator. Existing environment and project approval rules still apply.

## Phase 3: Agent definitions

Generate `.codex/agents/{name}.toml` from `references/schemas/agent-worker.template.toml`.

Set `name`, `description`, `developer_instructions`, `model`, `model_reasoning_effort`, and `sandbox_mode`. Use the explicit role mapping in `references/schemas/models.md`, with `medium` effort for all roles unless the user overrides it. Validate availability in the target environment; do not silently replace a model. A skill cannot change the active main session's model.

Workers report results directly to the main Orchestrator: outcome, changed artifacts, verification, blockers, and suggested next action. They do not write a second task database or independently publish progress.

## Phase 4: Orchestrator skill

Render `references/schemas/agent-orchestrator.template.md` to `.codex/skills/{orchestrator}/SKILL.md`.

Copy this exact runtime bundle into the generated skill:
- `references/project-policy.md`
- `references/orchestrator-procedures.md`
- `references/schemas/models.md`

The generated skill must be self-contained apart from the explicitly documented external publication skills. Do not copy the entire meta-skill or create runtime schemas, state scripts, or mandatory workflow files.

Describe the project's completion criteria and role roster in the generated skill. A task-specific plan belongs in the selected issue/spec or conversation; temporary notes under `_workspace/<task>/` are optional.

## Phase 5: AGENTS.md integration

Merge, rather than overwrite, the project's instructions:

```markdown
## Harness: {name}

- Entry: use the {orchestrator} skill at .codex/skills/{orchestrator}/SKILL.md.
- The main Orchestrator coordinates the selected native Codex subagents.
- Agents: {generated agent paths and responsibilities}.
- Role model policy: .codex/skills/{orchestrator}/references/schemas/models.md.
- Work and documents: share .scratch/.tracker with to-spec and to-issues.
- Reuse an explicit existing/new/no-issue choice; otherwise ask before selecting one.
- Record progress, verification, blockers, and next actions on the selected work record.
- Resume by reading that record and checking actual artifacts and tests.
- Close an issue only on user request.

## Explanation Profile

- Audience: {user-supplied domains and familiarity}.
- For familiar domains, focus on evidence and tradeoffs.
- For unfamiliar domains, explain necessary terms with concrete examples.
- An explicit request such as ELI5 takes precedence for that task.
- Explanation style never reduces code quality, verification, or disclosure of material risks.
```

Resolve all placeholders. Preserve an existing profile unless the user asks to change it.

Do not initialize mandatory local task, checkpoint, or findings files. Keep optional scratch artifacts out of version control; keep shared local tracker documents trackable under the publication contract.

## Phase 6: Validation

Use `references/skill-testing-guide.md`.

- Agent TOML parses and role models/efforts match the selected policy.
- Generated skill metadata and all three bundled reference paths resolve.
- Normal, resume, reviewer-rejection, no-issue, and publication-failure scenarios are checked.
- No worker independently creates tickets or changes the issue's completion state.
- No runtime state script, local task database, or State Manager is required.
- AGENTS.md contains the selected audience profile and no unresolved placeholders.
- Preserve existing work during migration; do not delete old user artifacts automatically.
- Distinguish static checks, mocked publication, live execution, and untested dependencies in the final report.

## References

- `references/project-policy.md` — work selection, tracker/documents, progress, resume, explanation profile
- `references/orchestrator-procedures.md` — generated runtime procedure
- `references/orchestrator-template.md` — generation guidance and exact bundle
- `references/schemas/models.md` — role model assignments
- `references/schemas/agent-worker.template.toml` — agent template
- `references/schemas/agent-orchestrator.template.md` — generated skill template
- `references/agent-design-patterns.md` — coordination patterns
- `references/skill-testing-guide.md` — verification scenarios
- `references/skill-writing-guide.md` — authoring guidance
- `references/qa-agent-guide.md` — independent result verification
- `references/expansion-matrix.md` — migration and scoped changes
- `references/team-examples.md` — example role combinations
