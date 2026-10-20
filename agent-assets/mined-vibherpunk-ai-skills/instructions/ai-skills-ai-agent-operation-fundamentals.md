# Copilot Instructions: Ai Agent Operation Fundamentals
Description: Master the five core components of modern AI agent systems: agents.md configuration, agent skills, MCP for tool integration, A2A for agent coordination, and subagent management.

# AI Agent Operation Skill

## Overview
This skill enables you to operate effectively within modern AI agent ecosystems by mastering five core components: [Project Configuration](references/core_concepts.md), [Skill Development](references/practical_guide.md), tool integration, inter-agent communication, and workload distribution.

## Step-by-Step Workflow
1. **Initialize Project Context**
   - Check for agents.md in current directory and parent directories
   - Merge configurations with closer files overriding distant ones
   - Example command to locate configs:
     ```bash
     find . -name "agents.md" -o -name "Claude.md"
     ```

2. **Load Relevant Skills**
   - Match user request against skill.md descriptions
   - Only load skills where request matches invocation conditions
   - Sample matching logic:
     ```python
     def should_invoke(skill, request):
         return any(trigger in request.lower() 
                  for trigger in skill.triggers)
     ```

3. **Connect to External Resources**
   - Establish MCP connections to required tools
   - Authenticate using platform credentials
   - Standard connection template:
     ```yaml
     mcp_connections:
       notion:
         server: "mcp.notion.com:8080"
         auth_token: "${NOTION_TOKEN}"
     ```

4. **Coordinate with Other Agents**
   - Query A2A discovery service for needed capabilities
   - Exchange data using standardized agent cards
   - Example delegation:
     ```python
     finance_agent = a2a_discovery.find("contract_approval")
     finance_agent.submit(contract_data)
     ```

5. **Manage Subagents**
   - Spawn subagents for parallelizable work
   - Pass required context explicitly
   - Collect and aggregate results
   - Subagent launch template:
     ```python
     results = []
     for chunk in split_workload(tasks, n=20):
         subagent = spawn_agent(context=chunk)
         results.append(subagent.result)
     ```

## Best Practices
- **Configuration**: Keep agents.md files focused and override sparingly ([details](references/common_pitfalls.md))
- **Skills**: Design small, purpose-specific skills that load minimal context
- **MCP**: Use connection pooling for frequent tool interactions
- **A2A**: Publish detailed, accurate agent cards
- **Subagents**: Implement proper cleanup handlers

## Validation Steps
1. Verify agents.md parsing with:
   ```bash
   agent validate-config
   ```
2. Test skill matching with sample requests
3. Confirm MCP connections with:
   ```bash
   mcp-ping notion
   ```
4. Validate A2A discovery with test queries
5. Stress test subagent spawning with parallel workloads

For comprehensive implementation examples, see our [Practical Guide](references/practical_guide.md). To avoid common mistakes, review [Common Pitfalls](references/common_pitfalls.md).

## Reference Guides

### Common Pitfalls

# Common Pitfalls in Agent Operations

## Configuration Errors
1. **Overriding Chaos**: Having too many nested agents.md files can create unpredictable behavior when rules conflict. Best practice is to limit overrides to 2-3 levels maximum.

2. **Skill Bloat**: Creating overly broad skills that load unnecessary context. Example: A "document processing" skill that loads both PDF and PowerPoint logic when only one is needed.

## Protocol Missteps
3. **MCP Authentication Gaps**: Forgetting to include credential rotation in MCP configurations can lead to service disruptions when tokens expire.

4. **A2A Discovery Failures**: Agents failing to find each other because:
   - Agent cards aren't properly published
   - Network permissions block discovery requests
   - Card descriptions are too vague for proper matching

## Subagent Problems
5. **Context Leakage**: Assuming subagents inherit all parent context automatically. In reality, you must explicitly pass required context to each subagent.

6. **Orphaned Subagents**: Subagents that don't properly terminate after completing tasks, consuming resources. Always implement:
   - Timeout mechanisms
   - Completion confirmation protocols
   - Resource cleanup routines

## Cross-Platform Issues
7. **File Name Variations**: Some platforms use different names for agents.md (e.g., Claude.md). Always check documentation for the specific agent platform you're using.

8. **Protocol Version Mismatch**: When different agents or tools use incompatible versions of MCP or A2A. Standardize on:
   - MCP v1.2+
   - A2A v2.0+
   Across all components.

### Core Concepts

# Core Concepts of AI Agent Operation

Modern AI agents operate through five fundamental components that enable autonomous task execution:

1. **agents.md**: A markdown configuration file that defines project-specific rules and commands for the agent. This acts as a README specifically for AI agents, containing instructions like test commands to run before commits or code style guidelines. Multiple agents.md files can exist in nested directories, with closer files overriding parent configurations.

2. **Agent Skills**: Modular task capabilities stored in folders containing a skill.md file and supporting resources. Each skill has metadata describing when it should be invoked (e.g., "when user wants to create PowerPoint slides"). Skills remain dormant until needed, preserving context window space.

3. **Model Context Protocol (MCP)**: A standardized interface for connecting agents to external tools and data sources. MCP servers wrap APIs (like Notion or Stripe) into a uniform interface that any MCP-compatible agent can use, eliminating the need for custom connectors per tool.

4. **Agent-to-Agent (A2A)**: A communication protocol where agents publish 'agent cards' describing their capabilities. This enables seamless delegation between specialized agents (e.g., a procurement agent handing contracts to a finance agent for approval).

5. **Subagents**: Child agents spawned by a main agent to handle parallelizable work or tasks requiring separate context windows. Each subagent operates independently and returns results to the parent, enabling scalable processing of large workloads.

These components work together to create flexible, powerful agent systems capable of complex workflows while maintaining clean context management and standardized interfaces.

### Practical Guide

# Practical Guide to Implementing Agent Systems

## Setting Up agents.md
1. Create an agents.md file at your project root
2. Include these essential sections:
   - **Setup Commands**: Installation and environment preparation
   - **Test Procedures**: Commands to validate work (e.g., `npm test`)
   - **Style Guidelines**: Code formatting rules
   - **Workflow Rules**: PR title formats, commit message conventions

Example agents.md structure:
```markdown
# Project X Agent Configuration

## Setup
Run: `npm install && pip install -r requirements.txt`

## Testing
Always execute before committing:
`pytest ./tests && npm run lint`

## Style Guide
- Use 4-space indentation
- Follow PEP8 for Python
- Prefix React components with 'X'
```

## Developing Agent Skills
1. Create a skill folder with:
   - skill.md (metadata and invocation conditions)
   - Required scripts/resources
2. In skill.md, specify:
   - Description of when to use the skill
   - Required parameters
   - Expected outputs

Example skill.md:
```markdown
# PowerPoint Creation Skill

Invoke when user requests:
- "create presentation"
- "make slides about X"

## Parameters
- topic: string
- slide_count: integer

## Output
.pptx file in /output
```

## MCP Integration
1. Identify target APIs/tools
2. Deploy MCP servers as wrappers
3. Configure agent to connect via:
   - Standard MCP port (default 8080)
   - Authentication tokens

## A2A Implementation
1. Publish agent cards describing:
   - Capabilities
   - Input/output formats
   - Availability
2. Set up discovery service for agents to find each other

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[5 AI Agent Terms You Need to Know](https://www.youtube.com/watch?v=k5jYwyhDMxA)** by IBM Technology