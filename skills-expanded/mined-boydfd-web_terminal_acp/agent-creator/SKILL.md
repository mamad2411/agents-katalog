---
name: agent-creator
description: Create or refine Web Terminal ACP agent profiles, AGENT.md prompts, companion skills, tool/MCP/hook recommendations, guardrails, and validation plans.
---

# Agent Creator

Use this skill when creating, modifying, evaluating, or productizing a Web Terminal ACP agent profile or reusable agent-client behavior.

## Workflow

1. Frame the agent intent: name, purpose, target users, default agent-client, repeated workflows, expected inputs/outputs, stopping conditions, and explicit non-goals.
2. Choose the capability shape:
   - Use a profile when the main need is reusable role, boundaries, and default config.
   - Add a skill when the workflow has reusable procedure, templates, references, or scripts.
   - Use an MCP/tool when structured external action or deterministic execution is required.
   - Use a hook only for automatic event-triggered behavior.
   - Use documentation only when no reusable runtime behavior is needed.
3. Draft an agent design contract before implementation when decisions are ambiguous or risky:
   - profile id, display name, description, and default agent-client
   - `AGENT.md` responsibilities, boundaries, escalation rules, and output contract
   - enabled skills and any new skill directories
   - tool, MCP, hook, or plugin changes
   - permission and safety guardrails
   - validation prompts and automated tests
4. Write instructions:
   - Keep `AGENT.md` concise and action-oriented.
   - Put reusable methods in `SKILL.md`.
   - Put long domain material in skill references.
   - Put fragile repeated steps in scripts.
   - Avoid duplicate or conflicting instructions across profile and skill.
5. Verify:
   - Run a prompt dry run against the main workflow.
   - For repository changes, follow local project instructions, keep multi-agent-client skill copies aligned, and run focused tests for listing, config, and materialization.

## Output Contract

Return these sections unless the user requested a narrower artifact:

- Recommendation: profile, skill, tool/MCP, hook, plugin, or documentation.
- Agent Profile: id, name, description, default agent-client.
- Instructions: concise `AGENT.md` draft or diff.
- Skills: existing skills to enable and new skills to create.
- Capability Diff: new abilities, explicit limits, required confirmations, and disabled/high-risk capabilities.
- Validation: realistic prompts, tests, and expected results.
- Risks: unresolved product, permission, security, or maintenance risks.

## Quality Bar

- The agent has one clear job family, not every possible job.
- The prompt says when to ask, when to act, when to stop, and what evidence to report.
- The skill is discoverable from its frontmatter description.
- High-risk tools are opt-in and documented.
- The design can be validated with concrete prompts or tests.
