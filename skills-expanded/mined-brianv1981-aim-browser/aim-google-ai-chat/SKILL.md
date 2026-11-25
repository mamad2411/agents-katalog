---
name: aim-google-ai-chat
description: >
  Multi-turn Google AI Mode via headed Chromium. Initial query uses udm=50;
  --follow-up / --turns for more turns. Prefer aim-google-ai for single-shot.
---

# aim-google-ai-chat

```bash
npm run google-ai-chat -- "name three primary colors" --follow-up "which is brightest"
npm run google-ai-chat -- --turns /tmp/turns.json "initial query"
```

Chat input DOM is unstable — use `--screenshot` when results look wrong.  
Defaults: minimized, stop after session. Single-shot → **aim-google-ai**.
