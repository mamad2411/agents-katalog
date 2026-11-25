---
layout: default
title: "Generate a Cowork Skill"
permalink: /prompts/experimental/generate-cowork-skill/
---

# Generate a Cowork Skill

**Category:** `experimental`

**Apps Involved:** Word

**Complexity:** Moderate (2 apps)

---

## Description

Generates a production-ready `SKILL.md` file for a new Copilot Cowork skill based on a plain-language description of the desired behavior, then produces a Word document briefing that documents the skill for team distribution.

H/T to Miguel Z. for his contribution! 🙌

## The Prompt

```
Create a new Cowork skill based on the following specification:

**Skill name:** [SKILL_NAME]
**Purpose:** [ONE_SENTENCE_PURPOSE]
**Trigger contexts:** [WHEN_SHOULD_THIS_SKILL_ACTIVATE — e.g., "whenever the user asks for X or mentions Y"]
**Inputs the skill should expect:** [INPUT_DESCRIPTION]
**Output format:** [OUTPUT_FORMAT — e.g., Word doc, Excel, HTML, inline response]
**Key steps the skill should follow:** [NUMBERED_STEPS_OR_WORKFLOW]
**Any source data, APIs, or integrations required:** [SOURCES_OR_NONE]
**Placeholder tokens to use:** [LIST_TOKENS_e.g._[COMPANY_NAME]_[TIME_PERIOD]]

Using the above, do the following:

1. Create a complete `SKILL.md` file with proper YAML frontmatter (name, description) and a step-by-step workflow section. The description must be written to maximize triggering accuracy — include specific phrases a user might say, and be explicit about edge cases.

2. Install the SKILL.md file so that it becomes available for future Cowork sessions.

3. Confirm that the skill is available and list it along with other out of the box and custom skills you have access to

4. Create a Word document with a summary of the skill and what it can do, for sharing with others who might also benefit from installing and using it

5. Write several test prompts that leverage the new skill

```

## Expected Outcome

- A `SKILL.md` ready to be installed by Cowork for future sessions
- A Word document briefing suitable for sharing with team members or stakeholders
- A confirmation message with the file paths and a suggested test prompt

## Tips & Variations

- Replace all `[BRACKETED_TOKENS]` before running — the prompt will not self-populate them.
- For skills that require web search or MCP integrations, add a `**compatibility:**` line to the YAML frontmatter listing required tools.
- To generate multiple related skills in one pass, repeat the specification block and add `"Generate one SKILL.md per specification above."` at the end.
- If the skill output format is Excel or PowerPoint instead of Word, change the briefing document format accordingly and reference the appropriate skill (xlsx or pptx) in the prompt.
- Keep the `[KEY_STEPS]` token to 5–8 numbered steps for best results; overly long workflows should be broken into sub-skills.

---
