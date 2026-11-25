---
name: super-code-category-pointer
description: "Pointer to a library of 16 specialized Super Code skills. Use when working on super-code-related tasks."
risk: none
---

# Super Code Capability Library 🎯

This is a **pointer skill**. The 16 specialized Super Code skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **bash** — Language-specific super-code guidelines for bash.
- **c** — Language-specific super-code guidelines for c.
- **cpp** — Language-specific super-code guidelines for cpp.
- **csharp** — Language-specific super-code guidelines for csharp.
- **dart** — Language-specific super-code guidelines for dart.
- **elixir** — Language-specific super-code guidelines for elixir.
- **go** — Language-specific super-code guidelines for go.
- **java** — Language-specific super-code guidelines for java.
- **kotlin** — Language-specific super-code guidelines for kotlin.
- **php** — Language-specific super-code guidelines for php.
- **python** — Language-specific super-code guidelines for python.
- **ruby** — Language-specific super-code guidelines for ruby.
- **rust** — Language-specific super-code guidelines for rust.
- **scala** — Language-specific super-code guidelines for scala.
- **swift** — Language-specific super-code guidelines for swift.
- **typescript** — Language-specific super-code guidelines for typescript.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/super-code/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/super-code`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
