Learn something new and store it in the graph memory.

Input format: topic | insight | source | confidence
Example: $ARGUMENTS

Steps:
1. Parse the input — split by | if provided, otherwise use $ARGUMENTS as the insight with "conversation" as source
2. Run `node .claude/graph-memory/engine.cjs learn "<topic>" "<insight>" "<source>" <confidence>`
3. Check if there are related topics to link: run `node .claude/graph-memory/engine.cjs search "<topic>" 3`
4. If related nodes found, link them: `node .claude/graph-memory/engine.cjs link "<topic>" "<related>" "related"`
5. Confirm what was stored and any new links created
