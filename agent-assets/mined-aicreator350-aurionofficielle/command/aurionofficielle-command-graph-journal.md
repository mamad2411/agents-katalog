Write a journal entry to the graph memory for today's session.

Content: $ARGUMENTS

Steps:
1. Run `node .claude/graph-memory/engine.cjs journal "$ARGUMENTS" "session,manual"`
2. Show confirmation with the journal entry details
3. Run `node .claude/graph-memory/engine.cjs stats` to show updated graph size
