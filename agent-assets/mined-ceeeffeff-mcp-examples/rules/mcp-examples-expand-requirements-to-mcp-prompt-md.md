---
description: Use this rule when converting high-level requirements into detailed
  MCP prompts. The rule provides guidance on structuring prompts for the Agent,
  including best practices for using fastmcp and mcp.prompt() decorators.
alwaysApply: false
---

When generating MCP prompts from concise requirements, expand them into structured instructions that:
1. **Define the task clearly** with specific objectives (e.g., "Generate a deployment summary for team communication")
2. **Specify required tools** the Agent will need to use to achieve the objective (e.g., "Use the get_workflow_status tool")
3. **Include step-by-step workflows** for the Agent to follow (e.g., "Retrieve statuses → Transform → Format")
4. **Add example inputs/outputs** for clarity (e.g., "Example format: '🚀 New deployment...'")
5. **Format prompts using mcp.prompt()** with proper documentation through decorator arguments
6. **Emphasize transformation logic** (e.g., "Convert technical statuses to friendly icons/text")
7. **Include structural formatting guidance** (e.g., "Use markdown headers, bullet points, emoji")
8. **Specify tone and style requirements** (e.g., "Maintain team communication tone with emojis")
9. **Decouple planning from execution** - The prompt should describe the plan, not execute it (e.g. the only thing the prompt function should do is return a prompt)
10. **Mandatory structure elements** - Include headers, bullet points, and emoji for clarity
11. **Prioritize clarity over complexity** - Use simple language and avoid technical jargon
12. **Show, don't tell** - Demonstrate expected output through examples rather than abstract descriptions
13. **Use consistent formatting** - Apply markdown headers, bullet points, and emoji for visual hierarchy
14. **Focus on user needs** - Frame instructions around the user's goals rather than technical implementation
15. **Make it actionable** - Provide clear, step-by-step guidance that can be directly followed