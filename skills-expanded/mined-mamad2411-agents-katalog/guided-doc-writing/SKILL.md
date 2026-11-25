---
name: guided-doc-writing
description: Write or revise learner-facing documents, Markdown pages, policies, guides, and explanatory materials so readers can grasp the main points in seconds. Use when drafting course docs, student-facing notices, instructions, overviews, or any prose that needs clear visual hierarchy, concrete examples, explicit reasons, and selective emphasis.
---

# Guided doc writing

Use this skill when the document itself must teach the reader
quickly, without relying on a separate chat explanation.

The canonical source of this skill is the GitHub repository
`metyatech/skill-guided-doc-writing`. To update this skill, edit
that repository and re-install. The agent MUST NOT treat installed
copies in agent skill directories as the primary place to edit.

## Core outcome

The agent MUST design the page so the reader can tell at a glance:

1. What matters most.
2. What they should do or remember.
3. Why that point exists.
4. Which examples define acceptable and unacceptable behavior.

## Default workflow

### 1. Define the scan-first takeaway

The agent MUST state the page's core message in one sentence
before drafting:

- The main conclusion.
- The reader action.
- The misunderstanding to prevent.

The agent MUST place that takeaway near the top. A reader who only
scans for 3 seconds MUST still catch the page's main point.

### 2. Build visible hierarchy

The agent MUST use headings intentionally:

- Use H1 through H3 as needed.
- Keep one section to one theme.
- Order content as important first, supporting detail later.
- Use bullets whenever the content is naturally list-shaped.
- Split dense paragraphs aggressively.

If a paragraph grows past 2-3 lines, the agent MUST break it.

### 3. Turn abstract rules into felt understanding

Whenever the page asks the reader to change behavior, the agent
MUST include all three:

- The abstract rule.
- A concrete example.
- The reason.

The agent MUST NOT stop at "do this" or "do not do this" when the
likely reader reaction is "why?"

If the renderer supports callouts or admonitions, the agent SHOULD
use titled callouts to separate reader jobs such as:

- `Conclusion First`
- `OK Example`
- `NG Example`
- `Why?`
- `Checkpoint`

The agent MUST use only the titles that help the page. The agent
MUST NOT add boxes that repeat the heading without adding meaning.

### 4. Apply selective emphasis

The agent MUST use emphasis as a second hierarchy layer, not
decoration:

- Each section SHOULD have at least one emphasized focal point.
- Each paragraph SHOULD have 1-2 emphasized phrases in most cases.
- Use bold for conclusions, keywords, rules, and required actions.
- Use italics for nuance, caution, or secondary importance.
- Use underline only for likely misunderstandings or high-risk
  cautions when the format supports it.

If the format does not support underline well, the agent MUST
replace it with a warning sentence or a warning-style callout.

### 5. Preserve contrast

The agent MUST NOT emphasize everything:

- Leave supporting explanation plain.
- The agent MUST NOT bold whole sentences unless the entire
  sentence is the key takeaway.
- If everything looks loud, the hierarchy has failed.

### 6. Run the final scan test

Before finishing, the agent MUST verify:

1. The reader can understand the page by reading headings and
   bold text only.
2. Each section has a visible focal point.
3. Every important abstract point has enough example or reason
   support.
4. No paragraphs are still dense enough to slow scanning.
5. Emphasis is selective rather than saturated.

## Reference

For a compact checklist, callout patterns, and rewrite examples,
read `references/visual-hierarchy-and-emphasis.md`.
