---
name: "java-sdk-doc-generator"
description: "Generates AI-agent-friendly Markdown SDK docs from Java source comments. MANDATORY: When invoked, MUST follow the execution steps below in order."
---

# SDK Doc Generator


EXECUTION FLOW (MUST follow strictly):
1. Read analyze.md → determine scope and detect git changes
2. Read produce.md → learn output format rules
3. Read template.md → learn Markdown template structure
4. Generate docs following template.md format exactly
5. Output to docs/agent-rules/ directory structure
6. Update README.md index

Invoke when user asks to generate/update SDK docs, Java API docs, or mentions 'generate SDK documentation'.