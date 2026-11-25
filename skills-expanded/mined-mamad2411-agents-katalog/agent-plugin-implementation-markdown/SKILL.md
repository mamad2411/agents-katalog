---
name: agent-plugin-implementation-markdown
description: Author custom agents in Markdown format (.agent.md) for simple workflows that use built-in or existing tools without custom code.
---

# Agent Implementation: Markdown

## Specialization

Implement a VS Code custom agent as a single `.agent.md` file when the agent does not require custom TypeScript code. Use Markdown frontmatter for metadata and body for detailed instructions.

## Supporting Activities

- Apply `.agent.md` YAML frontmatter syntax (name, description, tools, model, user-invocable).
- Write clear, concise agent instructions (2-4 paragraphs).
- Define handoff transitions to other agents (optional).
- Apply tool picker configuration (optional; control which tools are visible).
- Reference external resources or templates for specialized workflows.
- Validate syntax and test in VS Code Chat interface.

## Workflow

1. **Create `.agent.md` file** in the plugin `agents/` directory:
   - Naming: `agent-name.agent.md` (kebab-case, matches agent name).
   - Location: `my-plugin/agents/my-agent.agent.md`.

2. **Author YAML frontmatter** (required fields):
   ```yaml
   ---
   name: my-agent
   description: Brief description (max 1024 characters)
   tools: ['search', 'read', 'web']  # Array of tool names (deny-by-default)
   model: 'GPT-5.2 (copilot)'         # Optional; defaults to system default
   user-invocable: true               # Optional; defaults to true
   ---
   ```

3. **Add optional frontmatter fields**:
   - `agents: ['*']` — Allow any agent as subagent (or list specific agents: `['implementation', 'reviewer']`).
   - `handoffs` — Define transitions to other agents (see step 5 below).
   - `temperature`, `max-tokens` — Model behavior tuning (optional; rare).

4. **Write agent instructions** (markdown body):
   - **Opening paragraph**: Summarize the agent's role and primary responsibility (1-2 sentences).
   - **Scope boundary**: Explicitly state what is in scope and what is NOT (prevent hallucination).
   - **Step-by-step guidance**: If the agent should follow a specific process, outline numbered steps with decision points.
   - **Examples**: Provide 1-2 concrete examples of good behavior or expected output format.
   - **Error handling**: Describe how the agent should behave if tools fail or input is invalid.
   - **Constraints**: List explicit limits (e.g., "do not edit files exceeding 10KB" or "do not make more than 5 tool calls").
   - Length: 200-500 words typically sufficient; avoid excessive verbosity.

5. **Define handoff transitions** (optional; multi-agent workflows):
   ```yaml
   ---
   name: planner
   handoffs:
     - label: Start Implementation
       agent: implementation
       prompt: "Now implement the plan produced above."
       send: false  # true = auto-send; false = user confirms before handing off
       model: 'GPT-5.2 (copilot)'
   ---
   ```

6. **Example structure**:
   ```markdown
   ---
   name: code-reviewer
   description: Analyzes code changes and produces severity-ranked findings
   tools: ['search', 'read', 'web', 'grep']
   agents: ['implementation', 'security-reviewer']
   user-invocable: true
   ---

   # Code Review Agent

   You are a code review specialist. Your role is to analyze code changes submitted by the user and produce actionable findings with severity rankings.

   ## What You Do

   - Read and understand the code change (via file path or diff).
   - Identify bugs, design issues, performance problems, and security vulnerabilities.
   - Produce a structured finding set: each finding includes severity (critical/major/minor), description, remediation steps, and code examples.
   - Suggest related code that might be affected (use search to find it).
   - If findings are security-critical, hand off to the security-reviewer agent for deeper analysis.

   ## What You Don't Do

   - Do not implement fixes yourself.
   - Do not modify the user's code.
   - Do not make assumptions about build environment or dependencies; ask the user if unclear.

   ## Your Process

   1. Ask the user for the code change (file path, diff, or description).
   2. Read the files using the read tool.
   3. Search for related code and usage patterns using search tool.
   4. Analyze for bugs, performance issues, and security concerns.
   5. Produce findings in this format:
      ```
      **Severity**: [Critical|Major|Minor]
      **Type**: [Bug|Performance|Design|Security]
      **Description**: [What is the issue?]
      **Remediation**: [How to fix it]
      **Example**: [Code example showing the fix]
      ```
   6. If findings are security-critical, hand off to security-reviewer agent.

   ## Constraints

   - Do not approve code; only identify issues.
   - Keep findings concise (1-2 paragraphs per finding).
   - If the codebase is too large to analyze quickly, ask the user to provide a diff or file list.
   - Maximum 10 findings per review (prioritize by severity).
   ```

7. **Validate in VS Code**:
   - Place `.agent.md` file in `my-plugin/agents/`.
   - Run `Chat: Install Plugin From Source` and enter the plugin directory.
   - Open Chat and verify the agent appears in the agent selector.
   - Test: Send a message to the agent and verify it behaves as documented.

8. **Test edge cases**:
   - User provides invalid input: Does the agent ask for clarification or error gracefully?
   - User asks agent to do out-of-scope work: Does the agent decline and explain why?
   - Tool fails (e.g., file not found): Does the agent recover and suggest next steps?
   - Large context: Does the agent truncate history or ask user to refocus?

## Inputs

- Agent name, description, and intended role (from design step).
- Tool whitelist (from agent-plugin-design skill).
- Workflow logic and decision tree (from agent-plugin-design skill).
- Handoff routes, if multi-agent (from agent-plugin-design skill).
- Target plugin directory path.

## Required Outputs

- Valid `.agent.md` file with YAML frontmatter and markdown body.
- Tool whitelist is explicit and matches design whitelist.
- Instructions are clear, concise, and include examples.
- Handoff transitions are defined with target agent names and prompts.
- Validated in VS Code Chat (loads without errors).
- Test evidence: agent behaves as documented in edge cases.

## Done Criteria

- `.agent.md` file is in `agents/` directory with kebab-case name matching frontmatter `name` field.
- YAML frontmatter is valid (no syntax errors).
- `name` field uses lowercase kebab-case only (no slashes or namespace prefixes).
- `tools` field is an array of valid tool names (no typos).
- Instructions are 200-500 words and include scope boundary, examples, and constraints.
- Handoff transitions (if present) name valid target agents.
- Agent loads in VS Code without errors.
- Agent behaves as documented: accepts valid input, rejects out-of-scope requests, handles tool failures gracefully.

## Validation Checklist

- [ ] `.agent.md` filename uses kebab-case and matches `name` field in frontmatter.
- [ ] YAML frontmatter has valid syntax (colons after keys, quoted strings with special chars).
- [ ] `tools` array lists only available tools (search, read, edit, web, execute, etc.).
- [ ] `description` is max 1024 characters and concise.
- [ ] Instructions clearly state what the agent does (scope).
- [ ] Instructions clearly state what the agent does NOT do (non-scope).
- [ ] At least one example is provided showing expected agent behavior.
- [ ] Constraints are explicit and quantified (e.g., "max 10 findings per review").
- [ ] Handoff transitions (if present) name valid agents from the plugin.
- [ ] Agent tested in VS Code: loads, accepts input, produces expected output.

## References

- [VS Code Custom Agents Documentation](https://code.visualstudio.com/docs/copilot/customization/custom-agents)
- [.agent.md Format Specification](https://code.visualstudio.com/docs/copilot/customization/custom-agents#_agent-markdown-format)
- [Agent Tools Reference](https://code.visualstudio.com/docs/copilot/agents/agent-tools)
- [Handoff Patterns](https://code.visualstudio.com/docs/copilot/agents/agents-window#_agent-handoffs)

## Trigger Conditions

Invoke this skill when any of the following is true:

- A simple custom agent needs to be implemented in Markdown (no TypeScript code required).
- An agent uses only built-in or existing MCP tools (no custom tool implementation).
- An agent design has been finalized and is ready for implementation.
- An agent needs to be tested or deployed quickly without extension infrastructure.
