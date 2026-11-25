---
name: vault-save
description: Capture insights, solutions, or learnings from the current Claude Code conversation into a formatted Obsidian note with wikilinks. Use when the user wants to save something discovered during a conversation — a technique, a solution, a workflow decision, or a key insight.
---

# Vault Save

Save conversation insights to the vault. Extracts the key discovery from the current session and creates or appends to a vault note.

## Workflow

1. **Identify what to capture.** Accept user guidance:
   - "Save this conversation" → summarize the full session's key insight
   - "Save the part about X" → extract that specific topic
   - "Save this solution" → extract the specific fix/answer
   - Freeform: user pastes or describes what they want saved

2. **Extract the core content** from the conversation:
   - **Context:** What problem or question prompted this?
   - **Key insight:** The main discovery, in 1-3 sentences
   - **Details:** Commands, code, configs, or steps that were key
   - **What to avoid:** Mistakes or dead-ends encountered along the way (if relevant)

3. **Search for a related existing vault folder:**
   ```bash
   obsidian search query="<topic keywords>" limit=8
   ```
   If a directly relevant project folder exists (e.g., the conversation is about a technique covered in an existing folder), offer to append to it instead of creating a new note.

4. **Decide filing strategy:**
   - **Append to existing folder:** If a closely related folder exists and the insight is a small addition
     ```bash
     obsidian append path="<folder>/README.md" content="\n## Insight — <title>\n<content>\n"
     ```
   - **Create a new standalone note:** For novel insights or anything not clearly belonging to one project
     ```bash
     obsidian create name="<Descriptive Title>" content="..." silent
     ```
     Or use the `Write` tool for longer content.

5. **Compose the note:**

   ```markdown
   ---
   description: <one-line summary of the insight>
   title: <Descriptive Title>
   date: YYYY-MM-DD
   source: conversation
   ---

   # <Title>

   ## Context
   What prompted this investigation or conversation.

   ## Key Insight
   The main discovery, stated clearly.

   ## Details
   Expanded explanation, code blocks, commands, or steps.

   ```bash
   # Commands or code here
   ```

   ## Related
   - [[related_folder/README]]
   - [[another_folder/gemini3_summary]]
   ```

6. **Cross-reference in today's daily note:**
   ```bash
   obsidian daily:append content="### HH:MM — Saved: <Title>\n<one-line summary>.\nNote: [[<Title>]]\n"
   ```

7. **Report** where the note was saved (path or note name) and what was captured.

## Tips

- For naming standalone notes: use descriptive action phrases like `Obsidian CLI Multiline Content Workaround.md`, `Agent Team Dispatch Pattern.md`
- If the conversation covered multiple distinct insights, save them as separate notes rather than one large dump
- The `## Context` section is the most important for future reference — without it, isolated insights lose their meaning
- If the user says "save everything", be selective: capture the 1-3 most reusable/novel insights, not a full transcript
