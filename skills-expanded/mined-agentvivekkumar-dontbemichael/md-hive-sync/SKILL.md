---
name: md-hive-sync
version: 1.0.0
description: |
  Don't Be Michael hive sync: runs the start-of-task hive protocol steps:
  checks inbox/ for new messages, and reminds you how to add notes worth
  keeping to your memory inbox before ending.
  Use when asked to "sync with the hive", "check my inbox", "hive status",
  or "hive sync".
  Proactively suggest at the start of a new task if you haven't checked your
  hive inbox in this conversation. (dontbemichael)
allowed-tools:
  - Read
  - Bash
---

## Hive Sync

Run the mandatory hive start-of-task steps:

1. **Memory** — your memory index was given to you at the start of this session. Procedure files it names are under `$AGENT_DIR/memory/`.

2. **Check inbox** — list and read all files in `$AGENT_DIR/inbox/` that are NOT in `inbox/.done/`. For each message:
   - Act on the message.
   - Move the handled file into `$AGENT_DIR/inbox/.done/` with `mv`.

3. **Report** — summarize any new inbox messages. Note any tasks assigned to you or information relevant to the current session.

4. **End-of-task reminder** — when you finish a task, add at most three short notes to `$AGENT_DIR/memory/inbox.md`, only for things you'd otherwise work out again: a researched fact with its source and date, steps that worked for a task you'll repeat, or an owner correction with the reason. End each note with "Why:" and what showed it (a source and date, a card or message id, a file), or leave it off when nothing did. Often there's nothing worth saving. Never write session logs or status updates there; the app tidies notes into your index.

Run `echo $AGENT_DIR` if the variable is not set to locate your agent directory under the hive root.
