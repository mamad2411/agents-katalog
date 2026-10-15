---
name: kmb-eta
description: "Query KMB real-time bus arrival time."
allowed-tools: [Bash]
effort: low
argument-hint: "<路線> <車站名> [總站名] [en|tc]"
---

Run this command and present the output directly as markdown:

```bash
f=.claude/skills/kmb-eta/query.py; [ -f "$f" ] || f=.agents/skills/kmb-eta/query.py; [ -f "$f" ] || f=.agent/skills/kmb-eta/query.py; [ -f "$f" ] || f=skills/kmb-eta/query.py; [ -f "$f" ] && python3 "$f" $ARGUMENTS || echo "ERROR=NO_SCRIPT"
```

Output is pre-formatted. Show it as-is.
