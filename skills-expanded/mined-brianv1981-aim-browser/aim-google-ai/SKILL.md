---
name: aim-google-ai
description: >
  Google Search AI Mode (udm=50) via headed Chromium. Returns answer text and
  sources as markdown + JSON. Use for AI Mode answers, not classic blue links.
---

# aim-google-ai

1. Ensures headed daemon is up (minimized by default)  
2. Opens `https://www.google.com/search?q=…&udm=50`  
3. Waits for the AI answer  
4. Prints **markdown** + `---JSON---`  

Classic SERP / blue links → **aim-google-web**. Workspace APIs → **aim-google** (separate package).

## Run (from aim-browser repo root)

```bash
npm run google-ai -- "your query here"

node aim-google-ai.skill/scripts/run.js "what is example.com used for"
node aim-google-ai.skill/scripts/run.js --query "weather Seattle WA" --timeout-ms 90000
node aim-google-ai.skill/scripts/run.js --visible "..."           # watch mode
node aim-google-ai.skill/scripts/run.js --no-start --keep-open "..."  # reuse daemon
```

## Output

- Markdown: answer + sources  
- After `---JSON---`: structured payload for agents  
- Optional: `--screenshot /tmp/google-ai.png`

## Agent rules

- Run live — never invent search results.  
- DOM shifts often; empty extract → `--screenshot` or fall back to aim-browser.  
- **Minimized** + **stop after session** by default; `--keep-open` / `--visible` only when needed.  
- Respect Operator policy and rate limits.
