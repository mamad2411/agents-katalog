---
name: chat-to-obsidian
description: |
  Convert conversation content into a structured deep technical article and save it to the Obsidian vault.
  Use when the user wants to save conversation content or chat history as an Obsidian note.
  Triggers: "save conversation as article", "save to obsidian", "turn this into a note", "/chat-to-obsidian"
allowed-tools:
  - Glob
  - Grep
  - Read
  - Write
  - Bash(open *)
  - Bash(ls *)
  - AskUserQuestion
---

# Chat to Obsidian

Convert conversation content into a deep, well-structured technical article and save it to the Obsidian vault.

## Workflow

### Step 1: Environment Detection & Content Analysis

**1a. Detect vault root** — follow [../../_shared/common-steps.md](../../_shared/common-steps.md) "Vault Detection" section.

**1b. Analyze conversation content:**

1. Identify the core topic(s) and key knowledge points discussed
2. Extract code examples, diagrams, comparisons, and insights
3. Determine the article's scope — what to include, what to skip

**1c. Determine target directory** — follow the **Directory Mapping Rules** in [../../_shared/common-steps.md](../../_shared/common-steps.md). Use the article's primary topic to match.

**1d. Search for bidirectional links** — follow the **Bidirectional Link Search** in [../../_shared/common-steps.md](../../_shared/common-steps.md).

### Step 2: Write the Article

Follow the template in [references/article-template.md](references/article-template.md) strictly.

Key principles:
- **Not a conversation transcript** — restructure, reorganize, and deepen the content
- **Scene-driven opening** — start with a concrete engineering problem, not abstract definitions
- **Numbered sections** (1, 2, 3...) with `---` separators
- **Rich code examples** with inline comments explaining key points
- **ASCII diagrams and tables** for visualizing complex concepts
- **`> **Key takeaway**` blockquotes** after key sections
- **Bold key terms** with `**bold**`
- **Depth over breadth** — go deep on each point rather than skimming many
- Include `[[wikilink]]` connections identified in Step 1d
- YAML frontmatter: title, date (today), tags (3-8), summary, source ("Claude conversation")

### Step 3: Save and Confirm

**3a. Save** — follow the **Save and Open in Obsidian** section in [../../_shared/common-steps.md](../../_shared/common-steps.md).

**3b. Update index.md** — follow the **Index Update** section in [../../_shared/common-steps.md](../../_shared/common-steps.md). Use the article's title, summary (condensed to under 80 chars), and top 2 tags.

**3c. Report to user:**
- Article title and brief summary
- File path where saved
- Target directory and why it was chosen
- Tag list
- Related notes linked (list the `[[wikilink]]` connections made)
