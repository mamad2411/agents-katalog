---
name: flanner-plan
description: >
  Save or update a plan, design, architecture, migration, or RFC document
  through flanner so it is placed in the managed plan directory, given the
  standard YAML header, and versioned. Use when the user asks to write or
  revise any planning markdown that should be tracked, or when you are about
  to create such a document yourself.
---

# Saving a plan through flanner

This repo manages planning docs with flanner. Do not write them with the
Write tool; the plan directory and header are handled by the MCP tools.

1. Confirm intent. If it is ambiguous whether a markdown file is a plan
   (versus a README, changelog, or notes), ask the user before proceeding.
2. Resolve the target with `get_plan_config` and `list_projects`.
3. Create with `create_plan_file_tool(project_id, name, content)`, passing the
   markdown body WITHOUT frontmatter; the header is added for you.
4. Revise an existing plan with `update_plan_file_tool(plan_file_id, content)`,
   which bumps the version and re-hashes the content.

Never hand-write the YAML header, and never place plan files outside the
directory reported by `get_plan_config`.
