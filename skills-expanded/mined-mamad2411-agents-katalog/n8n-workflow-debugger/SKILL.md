---
name: n8n-workflow-debugger
description: Resolving, scanning, and troubleshooting failed n8n workflows.
---

# n8n Workflow Debugger Skill

Provides strategies for auditing, debugging, and fixing n8n workflow errors.

## When to Use
Use when users report webhook validation issues, duplicate properties failures, or workflow node parameter syntax crashes.

## Debugging Workflow
1.  Run `flowforge validate` to detect duplicate keys or references to deleted nodes.
2.  Run `flowforge lint` to identify unconfigured retry/error strategies.
3.  Check log details. Review conditional branch output indices.
