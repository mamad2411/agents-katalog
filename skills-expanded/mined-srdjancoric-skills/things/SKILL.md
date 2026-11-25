---
name: things
description: File a bug, improvement or research item into Things 3 (Work area) with a plain-English Claude Doc linked in its notes. Use only when the user invokes /things with an argument describing the item.
disable-model-invocation: true
argument-hint: <what the bug / improvement / research is about>
---

# Things

File one item: a Claude Doc that explains it, and a Things to-do that links to the doc.

**Input:** the argument (what the item is about) plus what this conversation already found.
Do not investigate further: no code reading, searching or fetching. If something is not known
from the conversation, write it in the doc as an open question.

## 1. Pick the project

All three projects are in the Things area **Work**:

| Project | Use when the item is |
| --- | --- |
| Bugs | something broken or behaving wrongly |
| Improvements | something working that should work better |
| Research | a question to answer, options to compare, or a decision to make |

If the argument fits more than one, ask the user once which project, then continue.

## 2. Create the Claude Doc

Use the Claude Docs connector and follow its own instructions for creating and filling a doc.

- **Title:** the same as the to-do title (step 3).
- **Language:** plain English. Short sentences. Explain any technical term the first time it
  appears, in one short phrase.
- **Sections, by project:**
  - Bugs: *What happens* · *Why it matters* · *Where* (files, lines, versions) · *Fix*
  - Improvements: *The problem* · *What to change* · *Where* · *How to check it worked*
  - Research: *The question* · *Options* (a table) · *Recommendation*
- End with *Sources*: the repo, branch, commit and any external versions (e.g. a Langfuse prompt
  version) the findings are based on.
- Quote exact sentences or code when the finding depends on wording.
- Keep the doc's URL for step 3.

## 3. Create the Things to-do

**Title:** starts with a verb, one line, at most about 70 characters.

**Notes**, in this order:

```
<1–2 sentence summary in plain English>

Doc: <Claude Doc URL>

Source: <repo> @ <branch> (<short commit>)
Added: <today's date, YYYY-MM-DD>
```

Add a deadline, a schedule date or tags only if the user asked for one.

**Create it** with `mcp__things__add_todo` (`title`, `notes`, `list_title` = the project).

**Verify it landed.** The MCP can report success while Things ignores the request. Check with
AppleScript:

```bash
osascript -e 'tell application "Things3" to return (count of (to dos of project "<Project>" whose name is "<Title>"))'
```

- `1` → done.
- `0` → create it with AppleScript instead. Write the notes to a file in the scratchpad first,
  so quotes and line breaks survive:

  ```bash
  osascript -e 'set n to read POSIX file "<notes file>" as «class utf8»
  tell application "Things3"
  set t to make new to do with properties {name:"<Title>", notes:n}
  set project of t to project "<Project>"
  end tell'
  ```

  Then run the check again. Also check the Inbox for a stray copy with the same title, and
  delete it if there is one.
- Still `0` → stop and tell the user. Give them the title, the notes and the doc link, so
  nothing is lost.

## 4. Report

Two lines to the user: the to-do title with its project, and the doc link.
