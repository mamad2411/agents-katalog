---
name: n8n-workflow-engineer
description: Engineering and generating robust n8n workflow JSON schemas from instructions.
---

# n8n Workflow Engineer Skill

This skill guides the creation and validation of n8n workflow schemas.

## When to Use
Use this skill when the user requests generating workflows, mapping out connections, and validating JSON exports.

## SOP / Workflow Steps
1.  **Analyze description:** Extract trigger conditions, processing elements, external services, and outputs.
2.  **Generate Scaffold:** Call `flowforge new "<description>"` to obtain a valid structural draft.
3.  **Validate Structure:** Run `flowforge validate` to assert connection routes and parameters.
4.  **Audit Quality:** Execute `flowforge score` to identify areas of improvement and security concerns.

## Constraints
*   Do not hardcode sensitive user API keys or endpoints. Always use credentials placeholders.
*   Validate all target node connections.
