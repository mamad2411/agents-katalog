Recall knowledge from the graph memory about: $ARGUMENTS

Steps:
1. Run `node .claude/graph-memory/engine.cjs recall "$ARGUMENTS" 2 5` to get matching nodes with context
2. If results found, summarize the relevant knowledge and connected concepts
3. If no results, say "No graph memory found for this topic"
4. Show node types, strengths, and relationship paths
