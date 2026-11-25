---
name: capture
description: "Brain dump and quick capture tools for Obsidian vaults. Stream-of-consciousness dumps, one-liner captures, and rapid-fire note creation. Use when the user wants to quickly get thoughts out of their head and into their vault."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: cognitive-toolkit
---

# Capture Pack — "I have thoughts everywhere"

Tools for getting thoughts out of your head and into your vault quickly, with structure added automatically.

## Commands

### /dump — Stream-of-consciousness brain dump

When the user invokes `/dump`, do the following:

1. Ask the user to brain dump — tell them to write freely without worrying about structure. They can use stream-of-consciousness, bullet points, fragments, whatever comes naturally.
2. Once they provide their dump, analyze it and:
   - Identify the core topic or theme
   - Extract any actionable items as tasks
   - Identify related concepts that could be wikilinks
   - Suggest relevant tags based on existing vault tags (`obs tags all --json`)
3. Create a well-structured note:
   - Generate a clear, descriptive title from the content
   - Add appropriate frontmatter (tags, date, type: dump)
   - Rewrite the content with structure (headings, paragraphs) while preserving the original voice and meaning
   - Convert related concepts to `[[wikilinks]]` where matching notes exist (`obs search path`)
   - Add any tasks as checkbox items
4. Save it: `obs files create "Inbox/<title>.md" --content "<structured content>"`
5. Show the user the before/after transformation

### /capture — One-liner quick capture

When the user invokes `/capture <thought>`:

1. Take the thought as-is
2. Check existing vault tags for relevant ones: `obs tags all --json`
3. Create a timestamped note in the inbox:
   ```
   obs files create "Inbox/YYYY-MM-DD-<slug>.md" --content "<frontmatter + thought>"
   ```
   Frontmatter should include: date, tags (auto-detected), type: capture
4. Check if the thought relates to existing notes: `obs search content "<key phrases>" --json`
5. If related notes found, mention them to the user and suggest adding wikilinks

### /quick — Rapid-fire capture session

When the user invokes `/quick`:

1. Tell the user: "Rapid-fire mode. Give me one thought at a time. Type 'done' when finished."
2. For each thought:
   - Create a minimal note in Inbox with auto-generated title, date tag, and type: capture
   - Use `obs files create` to save immediately
   - Confirm with a one-line summary and move on
3. When done, show a summary:
   - How many thoughts captured
   - List of created files
   - Any themes detected across the batch
   - Suggest which captures might be worth expanding (use `/expand` from the clarify pack)

## Tips

- Always check if an Inbox folder exists first. If not, create notes in the vault root.
- Use `obs search path "Inbox"` to verify the inbox location.
- Keep captures lightweight — the point is speed, not perfection.
- Auto-detect tags by comparing against `obs tags all` output, not by guessing.
