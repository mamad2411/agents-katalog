---
name: skip-skill-discovery-on-skill-expansion
description: "Bypass skill discovery when expanded SKILL.md or generated prompt content is being reprocessed for attachments, so non-user text does not trigger recursive discovery work."
metadata:
  author: ychampion
---

# SKILL: Skip Skill Discovery on Skill Expansion
**Domain:** command-surfaces  
**Trigger:** Apply when generated or expanded skill text must pass through the attachment pipeline for parsing, but it is not fresh user intent and must not trigger discovery queries.
**Source Pattern:** Distilled from reviewed command-surface and listing-control patterns.

## Core Method
Separate "text being inspected" from "text expressing user intent." When a pipeline reuses the attachment extractor on expanded SKILL.md content or other generated prompts, pass an explicit skip flag so the discovery subsystem stays off while the rest of the attachment logic still runs. This preserves useful secondary parsing such as `@`-mentions without paying for recursive or misleading skill-discovery calls on machine-generated text. The guard should live exactly where discovery would otherwise be attached so the expensive path is impossible to trigger accidentally.

## Key Rules
- Run skill discovery only for genuine user-authored input, not for expanded skill files, generated prompts, or other agent-produced text.
- Use an explicit option or context flag to disable only the discovery branch, leaving the rest of the attachment pipeline active.
- Keep the gate adjacent to the discovery attachment construction so future refactors cannot bypass it unintentionally.
- Treat large injected documents as especially high risk; one missing gate can turn a single skill invocation into repeated expensive discovery calls.

## Example Application
If a slash command loads a 100 KB skill specification and then reuses the normal attachment extractor to resolve `@`-mentions inside it, pass `skipSkillDiscovery: true`. The extractor still parses mentions, but it does not launch another round of skill-discovery queries against the generated document body.

## Anti-Patterns (What NOT to do)
- Do not run discovery on expanded SKILL.md content or other generated prompts; that mistakes system-produced text for user demand.
- Do not disable the entire attachment pipeline just to suppress discovery; you still want legitimate parsing such as file mentions and other lightweight attachments.
