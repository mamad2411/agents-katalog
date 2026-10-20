---
name: agent-plugin-design
description: Design agent personas, workflows, tool permissions, and handoff patterns before implementation to ensure clear scope and secure execution.
---

# Agent Design

## Specialization

Define an agent's operational contract before authoring code: persona, capabilities, tool whitelist, workflow logic, and multi-agent handoff transitions. This skill ensures security, clarity, and deterministic behavior.

## Supporting Activities

- Draft agent persona (role, expertise, constraints).
- Document primary use cases and non-goals.
- Define tool whitelist (deny-by-default approach).
- Design workflow logic and decision points.
- Map handoff transitions to other agents or termination.
- Record security boundary assumptions.
- Pressure-test assumptions against common pitfalls.

## Workflow

1. **Define agent persona** (2-3 sentences):
   - Role: What is the agent's primary responsibility?
   - Expertise: What does it specialize in?
   - Scope: What is explicitly out of scope?
   - Example: "Code reviewer agent: reads and analyzes code changes, identifies bugs and security issues, provides actionable feedback. Out of scope: implementation, test writing, deployment decisions."

2. **List primary use cases** (3-5):
   - Scenario: "User submits a Git diff for code review."
   - Expected outcome: "Agent produces a severity-ranked finding set with remediation guidance."
   - User provides context: "Should the agent ask clarifying questions or immediately review?"

3. **Whitelist required tools** (deny-by-default):
   - Built-in tools: `search`, `read`, `edit`, `web/fetch`, `execute`
   - Rationale: Why is each tool needed?
   - Example (Code Reviewer): `search` (find related code), `read` (examine files), `web` (reference APIs), but NOT `edit` (read-only mandate).

4. **Document workflow logic**:
   - Decision tree: "If [input characteristic], then [agent action]."
   - Multi-turn behavior: "After first response, does the agent ask follow-up questions or terminate?"
   - Error handling: "What happens if a tool fails (retry, escalate, fallback)?"
   - Depth limits: "How many tools calls maximum? How many turns before forced termination?"

5. **Design handoff transitions** (if multi-agent):
   - From this agent: When does it hand off? To which agents? With what context?
   - To this agent: When does it receive handoffs? What is the expected input? How is it validated?
   - Example: "Code reviewer → hands off to implementation agent with: findings + remediation steps + code sample."

6. **Identify security boundaries**:
   - What information should never be logged or cached?
   - What URLs or domains are trusted for web requests? (Deny-by-default for SSRF prevention)
   - What filesystem paths are accessible? (Whitelist approach)
   - What commands can be auto-approved vs. require user confirmation?

7. **Pressure-test assumptions** (Critical Thinking):
   - Can the tool whitelist be tighter? (Remove read-only tools if not essential)
   - Are there hidden dependencies on tools not listed?
   - Does the persona conflict with the tool set? (e.g., "implementation specialist" with only read-only tools)
   - What happens if the user asks the agent to do something out of scope?
   - Are there single points of failure (e.g., all logic depends on one web API)?

8. **Document design artifact**:
   - Persona statement.
   - Tool whitelist with justification.
   - Workflow pseudocode or decision tree.
   - Handoff routes (if applicable).
   - Security boundaries.
   - Known limitations and explicit non-goals.
   - Acceptance criteria for "agent behaves as designed."

## Inputs

- Agent name and domain (e.g., "Test Runner" for testing domain).
- Motivation: Why is this agent needed? What problem does it solve?
- Constraints: Budget (API rate limits, context limits), platform (VS Code only, or Copilot CLI + VS Code).
- Existing agents: Are there related agents to hand off to?
- Tool availability: Which MCP servers or extension tools are available?

## Required Outputs

- Design document (markdown) with all sections listed in workflow step 8.
- Tool whitelist (explicit list of tool names + justification).
- Workflow decision tree (pseudocode or flowchart).
- Handoff map (if multi-agent): source agent → target agents → transition conditions.
- Security assumptions document (SSRF domains, filesystem paths, auto-approve rules).
- Acceptance criteria (3-5 testable statements like "Agent does not edit files" or "Agent terminates after 5 turns").

## Done Criteria

- Persona is concise (2-3 sentences) and clearly scoped.
- Tool whitelist uses deny-by-default (every tool listed is justified).
- Workflow logic is deterministic (no vague "tries to" statements; use explicit decision rules).
- Handoff routes are bidirectional (source agent knows destination; destination knows expected input format).
- Security boundaries are explicit (no assumptions like "assume the web API is safe").
- Design is peer-reviewable (a colleague can understand the agent's behavior without reading code).
- Acceptance criteria are testable (not vague like "agent works well"; e.g., "agent does not call edit tool" or "agent terminates after max 10 tool calls").

## Validation Checklist

- [ ] Persona statement is 2-3 sentences and clearly differentiates from other agents.
- [ ] Tool whitelist includes only tools required for primary use cases.
- [ ] Each tool has a 1-line justification (not "might be useful").
- [ ] Workflow logic avoids vague terms like "intelligently" or "tries to."
- [ ] Decision tree includes both happy-path and error cases.
- [ ] Handoff routes name the target agent and describe transition input format.
- [ ] Security boundaries are explicit: SSRF domains, file paths, auto-approve commands.
- [ ] Depth limits are quantified: max tool calls, max turns, timeout in seconds.
- [ ] Acceptance criteria are testable and written as imperative statements ("Agent does X").
- [ ] Design has been pressure-tested: hidden assumptions surfaced and resolved.

## References

- [VS Code Custom Agents Documentation](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [Agent Tools Reference](https://code.visualstudio.com/docs/copilot/agents/agent-tools)
- [MCP Servers Overview](https://code.visualstudio.com/docs/copilot/customization/mcp-servers)
- [Security Considerations for Agents](https://code.visualstudio.com/docs/copilot/security)

## Trigger Conditions

Invoke this skill when any of the following is true:

- A new agent is being designed before implementation begins.
- An existing agent needs its capabilities redefined or constraints tightened.
- Tool whitelist or workflow logic must be documented for security review.
- A multi-agent handoff pattern needs to be designed (agent A → agent B).
- Design assumptions need pressure-testing before code commit.

