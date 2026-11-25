---
name: author-rules
description: Use `author-rules` to write `AGENTS.md` files.
---

# AGENTS.md Authoring

Use this skill only for `AGENTS.md` files.

## Valid locations

* Project root `AGENTS.md`: common rules applicable to whole repo.
* Subdirectory `AGENTS.md`: specialized rules for that folder and child folders only.
* Use one file per scope when rules apply only there.

## AGENTS.md Layout Template

```markdown
# [TITLE]

[PURPOSE]

[COMMON RULES]

[USER CONTENT]

[CONDITIONAL RULES]
```

Replace placeholders in Root Layout Template as follow:
* Replace [TITLE] with scope of instructions (e.g. Project name for root AGENTS.md like "Autocode Plugin" or Package purpose for sub AGENTS.md like "Business Services")
* Replace [PURPOSE] with purpose of repo directory (max 20 words)
* Replace [COMMON RULES] with common or critical rules like forbidden actions/limiting scope
  - Group related rules with H2 headers
  - When rules contradict: Add conditions when to apply which rule (move rules to [CONDITIONAL RULES] section)
  - Must be < 30 words per rule
* Replace [USER CONTENT] with H2 title and user-provided content only if explicitly requested
  - Prefer concise bullets unless user specified format
  - Omit entire [USER CONTENT] section by default  
* Replace [CONDITIONAL RULES] rules that apply conditionally:
  - Group related conditions with H2 headers
  - Numbered list to indicate priority of conditions
  - Format "If [some condition], then: [rule]"

## Rules

* ALWAYS speak and write Caveman English
* No repetitions
* Only use emojis to highlight important aspects to LLM, like attention, warning, checklists, correct vs wrong
* ALWAYS keep md < 100 lines by:
  1. Cleaning up redundant content (try first)
  2. Removing excessive examples
  3. Summarize trivial info
  4. Merge basic instructions (last resort)
* Use this skill layout/format as example `AGENTS.md`.
