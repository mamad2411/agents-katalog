---
name: create-agent
description: Create effective project-level agent definitions in `.agents/agents/` with clear responsibilities, practical constraints, and concise prompts. Use when the user asks to create, refine, or standardize custom agents.
---
<!-- Generated from .agents/ by scripts/sync-ai-workspace.mjs. Do not edit directly. -->


# Create Agent

Define agents that are clear, focused, and reusable for this repository.

## Goals

- Create agents that are easy for Claude to delegate to.
- Keep definitions concise and specific.
- Encode realistic behavior (deliver outcomes without overpromising).
- Ensure project scope so agents are shareable in git.

## Location and Format

1. Store each agent in `.agents/agents/<agent-name>.md`.
2. Use YAML frontmatter plus a short markdown prompt body.
3. Keep names lowercase with hyphens.
4. Keep the whole file concise (prefer practical rules over long prose).

## Required Frontmatter

Include at minimum:

```markdown
---
name: <agent-name>
description: <what it does + when to use it>
tools: <comma-separated tools or omit to inherit>
model: inherit
permissionMode: default
---
```

Guidance:
- `description` should include both **WHAT** and **WHEN** (trigger terms).
- Start with `model: inherit` unless there is a clear reason to change it.
- Restrict tools where useful; do not grant broad access by default.

## Agent Design Checklist

For each agent, define:

1. **Role boundary**: what this agent owns and what it explicitly does not own.
2. **Success definition**: what “good output” looks like.
3. **Workflow**: short ordered steps the agent follows.
4. **Escalation rules**: when to ask the human vs proceed independently.
5. **Communication style**: concise, outcome-focused reporting.
6. **Anti-patterns**: behaviors to avoid.

## Writing Rules

- Prefer short bullets and action verbs.
- Use specific operational language (e.g., "produce acceptance criteria", "surface risks early").
- Avoid vague instructions like "be helpful" without execution details.
- Avoid duplicate rules across sections.
- Keep terminology consistent across agents.

## Reusable Template

```markdown
---
name: <agent-name>
description: <specific role>. Use when <trigger scenarios>.
tools: <tools>
model: inherit
permissionMode: default
---

You are a <role> for this repository.

You own:
- <responsibility 1>
- <responsibility 2>

You do not own:
- <non-goal 1>

Workflow:
1. <step 1>
2. <step 2>
3. <step 3>

Escalate only when:
- <high-impact decision>
- <irreversible change>
- <permission-gated action>

Communication:
- <concise update style>

Avoid:
- <anti-pattern 1>
- <anti-pattern 2>
```

## Integration-Heavy Agent Guidance

When creating agents that own work against third-party vendors, regulators, or upstream APIs:

- Anchor instructions to integration delivery outcomes.
- Emphasize dependency mapping and third-party constraints.
- Require early risk surfacing (vendor/API/schema/change windows).
- Prefer unblock-first behavior across team roles.
- Keep responsibilities distinct (PM orchestrates, analyst clarifies, implementer builds).

## Sync to Claude Code

After creating or modifying the agent file, run:

```bash
just ai-sync
```

This generates the Claude Code mirror in `.claude/agents/`. Without this step, Claude Code won't discover the new agent.

**Always run `just ai-sync`** — do not skip it or leave it for the user.

## Validation Before Finalizing

- File exists in `.agents/agents/`.
- Name/description are specific and discoverable.
- Prompt is concise and actionable.
- Role boundaries and escalation rules are explicit.
- No overdelivery or noisy-reporting behavior is encouraged.
- Ran `just ai-sync`.
