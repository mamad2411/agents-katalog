---
name: authoring-godot-prompter-skills
description: Use when writing or editing a SKILL.md, a skill's references/*.md, or an agent definition in this repo — required frontmatter, section ordering, the GDScript-then-C# example convention, and C# parity exemptions.
---

# Authoring GodotPrompter skills and agents

File format templates for this repo. See the root `CLAUDE.md` for the conventions
and size budget that govern the content itself.

## SKILL.md format

Every skill must start with YAML frontmatter:

```yaml
---
name: skill-name
description: Use when [trigger] — [brief scope]
---
```

Followed by:
1. Title and intro
2. Related skills line: `> **Related skills:** **skill-a** for X, **skill-b** for Y.`
3. Numbered sections with patterns and examples
4. GDScript first, then C# equivalent (use `gdscript` and `csharp` language tags)
5. Implementation checklist at the end

## C# parity

The validator also checks C# parity inside `references/*.md` (`csharp-parity-*-reference`), so Pattern X moves stay enforced. Files that section **by language** (`## C#`, `## Dash (C#)`, `### … — C#`) are checked file-level instead of per-section; a heading that merely mentions C# in prose is not a partition.

When a section genuinely cannot have a C# counterpart, mark that section — never the whole skill:

```markdown
<!-- csharp-parity: n/a — C# is statically typed; there is no untyped alternative to contrast -->
```

It works in both `SKILL.md` and `references/*.md`. The reason is **mandatory**; omitting it is an error (checked on every marker, not only on sections missing C#), because an exemption that cannot say why is indistinguishable from an example nobody wrote. A reason may contain `<` and `>`, and a marker inside a fenced block is ignored, so a file can document the marker without exempting itself.

Do **not** reach for the two blunter tools instead: adding the skill to `GDSCRIPT_ONLY_BY_DESIGN` exempts every section in it, and renaming a heading to `"… (GDScript)"` trips the language-partition check and silently downgrades the *entire file* to a file-level check. Both hide real gaps in neighbouring sections.

A fenced ```gdscript block containing only comments is not a code example — it is prose in a fence, and it will be flagged as an unpaired GDScript block. Write it as prose or a bullet list.

## Agent format

Agent definitions in `agents/<name>.md` use YAML frontmatter:

```yaml
---
name: agent-name
description: |
  When to use, with <example> blocks.
model: inherit
---
```

## Before you finish

Run `node scripts/validate-skills.mjs` — it enforces frontmatter, cross-references,
and the 16 KB size budget.
