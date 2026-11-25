---
name: skill-creator
description: Design valid CashCode Skills with concise instructions and progressively loaded scripts, references, templates, and assets.
version: 1
tags: [skill, workflow, authoring]
triggers: [create a skill, update a skill, reusable workflow]
requires:
  tools: [agent_skill_manage]
---

# CashCode Skill Creator Contract

Create broad reusable workflow packages, not one-turn notes.

## Mandatory managed flow

1. Derive a canonical ASCII slug that matches `^[a-z0-9][a-z0-9._-]{0,63}$`.
2. Put the requested localized title in `display_name`; never put Chinese or other unsupported characters in `name`.
3. Prepare the complete `SKILL.md` and optional text support files.
4. Call `agent_skill_manage` with `action=create`, the same canonical `name`, the complete content, and a short reason.
5. When the result has `success=false`, correct the reported validation error and retry the managed tool, or report failure. Never switch to filesystem, shell, or HTTP creation.
6. Report completion only after the result contains `success=true`.

Required package shape:

```text
<slug>/
  SKILL.md
  references/   optional detailed knowledge
  templates/    optional editable starters
  scripts/      optional deterministic helpers
  assets/       optional output resources
```

Rules:

1. Use a lowercase ASCII slug matching the package directory, tool argument, and frontmatter `name`; keep localized titles in the optional `display_name` field.
2. Write a plain string `description` containing both capability and trigger intent.
3. Keep `SKILL.md` concise: trigger conditions, ordered steps, pitfalls, and verification.
4. Move detailed variants into directly linked supporting files.
5. Declare required and optional tools, MCP servers, binaries, and environment variables structurally.
6. Loading a Skill never authorizes executing its scripts.
7. For an explicit chat creation request, call `agent_skill_manage` with `action=create`, the canonical slug, the complete `SKILL.md`, optional text support files, and a short reason.
8. Never create or register a Skill through `write_file`, `edit_file`, `exec`, `curl`, shell commands, or ad hoc HTTP calls.
9. Treat only an `agent_skill_manage` result containing `success=true` as a successful creation. On failure, report its code and detail without claiming the Skill exists.
10. Built-in Skills are read-only. Evolution may modify only agent-created Skills and requires proposal approval.

## CashCode frontmatter rules

- Required: `name` and a non-empty string `description`.
- Optional: `display_name`, `version`, `tags`, `triggers`, `always`, `requires`, and `optional`.
- `display_name` is a trimmed string of at most 80 characters without control characters.
- `version` is a positive integer and `always` is a boolean.
- `tags` and `triggers` are lists of non-empty strings.
- `requires` and `optional` are mappings whose `tools`, `mcp_servers`, `bins`, and `env` values are lists of non-empty strings.
- A non-empty Markdown body must follow the closing frontmatter delimiter.
- Support files are text files under `references/`, `templates/`, `scripts/`, or `assets/`; paths must be package-relative and cannot contain `..`.

Use this shape for a localized title:

```markdown
---
name: renzhi-niuqu
display_name: 认知扭曲
description: 识别常见认知扭曲并在用户要求检查想法时引导生成平衡表述。
version: 1
tags: [反思, 认知]
triggers: [检查想法, 识别认知扭曲]
always: false
requires:
  tools: []
  mcp_servers: []
  bins: []
  env: []
optional:
  tools: []
  mcp_servers: []
  bins: []
  env: []
---

# 工作流程

1. 确认用户希望检查的原始想法。
2. 识别适用的认知扭曲类型并说明证据。
3. 生成更平衡、可验证的替代表述。
4. 检查输出是否遵循用户约束。
```

Validate every package before enabling it. Test scripts explicitly when a Skill introduces them.
