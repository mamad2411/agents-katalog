---
name: act
description: "Turn thinking into doing with Obsidian vaults. Get focused next actions, make decisions using your own notes, or promote buried ideas into standalone notes. Use when the user has ideas but needs help prioritizing, deciding, or organizing for action."
license: MIT
metadata:
  author: markfive-proto
  version: "0.1.0"
  pack: cognitive-toolkit
---

# Act Pack — "I have 100 ideas and no plan"

Tools for turning vault knowledge into decisions and actions.

## Commands

### /next — What should I focus on right now?

When the user invokes `/next`:

1. Gather current state:
   - `obs tasks pending --json` — open tasks across vault
   - `obs daily open --json` — today's daily note (if exists)
   - `obs files list --since 3d --sort modified --json` — recently active files
2. Analyze:
   - Group pending tasks by file/project
   - Check which tasks are in recently active files (high momentum)
   - Look for tasks with deadlines in frontmatter (due dates)
   - Check for tasks tagged with priority markers
3. Recommend top 3 actions:
   ```
   ## What to focus on now

   ### 1. [Task or action]
   From: [[source note]]
   Why now: [Has momentum / deadline approaching / blocking other work]

   ### 2. [Task or action]
   From: [[source note]]
   Why now: [reason]

   ### 3. [Task or action]
   From: [[source note]]
   Why now: [reason]

   ## Also on your plate
   - [Other pending items, grouped by area]

   ## Stale tasks (consider archiving)
   - [Tasks in files not modified for 2+ weeks]
   ```
4. Offer to update the daily note with the focused plan

### /decide — Gather evidence for a decision

When the user invokes `/decide <question>`:

1. Parse the decision question
2. Search the vault for relevant context:
   - `obs search content "<key terms>" --json`
   - `obs search content "<alternative terms>" --json`
   - Check for notes explicitly about this topic
3. Read relevant notes and extract:
   - Arguments for and against
   - Past experiences or lessons learned
   - Related decisions already made
   - Values or principles expressed
4. Present the decision framework:
   ```
   ## Decision: <question>

   ### What your notes say

   #### For
   - [Evidence from [[note]]]
   - [Evidence from [[note]]]

   #### Against
   - [Concern from [[note]]]
   - [Concern from [[note]]]

   ### Related past decisions
   - [Previous decision from [[note]] and its outcome]

   ### Your values on this
   - [Principles or values expressed in relevant notes]

   ### What's missing
   - [Information you'd need that isn't in the vault]

   ### Bottom line
   [Based on your own notes, the evidence leans toward X because...]
   ```
5. Emphasize: this is the user's own thinking reflected back, not new advice

### /graduate — Promote buried ideas to standalone notes

When the user invokes `/graduate`:

1. Scan daily notes and journal entries for buried ideas:
   - `obs files list --folder "Daily" --sort modified --json` (or detect daily note folder)
   - `obs files list --since 2w --sort modified --json`
2. Read recent daily/journal notes and look for:
   - Ideas that deserve their own note (substantial paragraphs not about daily logistics)
   - Recurring themes across multiple days
   - Questions or hypotheses that were written once and never followed up
   - Links to notes that don't exist yet (broken links as idea signals)
3. Also check: `obs links broken --json` — broken links are ideas waiting to be born
4. Present candidates:
   ```
   ## Ideas ready to graduate

   ### 1. "[Idea title]"
   Source: [[daily note]] (date)
   Original text: "[excerpt]"
   Why graduate: [Substantial thought / recurring theme / has connections]
   Suggested location: [folder/filename.md]

   ### 2. ...

   ## Broken links worth creating
   - [[missing-note]] — referenced by N notes
   - [[another-missing]] — referenced by M notes
   ```
5. For each idea the user wants to graduate:
   - Create the new note with content expanded from the original excerpt
   - Add wikilinks back to the source
   - Add a wikilink from the source daily note to the new note
   - Set frontmatter: type, tags, graduated-from

## Tips

- /next should be opinionated. Don't just list everything — recommend a focus.
- /decide must only use the user's own notes as evidence. Don't inject outside opinions.
- /graduate is about recognizing when an idea has outgrown its container (daily note, journal entry).
- Check for daily note folder config: the folder might be "Daily", "Journal", "Daily Notes", etc.
