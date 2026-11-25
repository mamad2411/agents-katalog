---
name: aim-web-diff
description: >
  Snapshot page main text twice (interval) or compare to a baseline JSON.
  Exit 0 = unchanged, 2 = changed, 1 = error. Headed CDP; stop after session.
---

# aim-web-diff

```bash
# Baseline
npm run web-diff -- --url "https://example.com" --save-baseline /tmp/ex-base.json

# Compare later
npm run web-diff -- --url "https://example.com" --baseline /tmp/ex-base.json
echo $?   # 0 same, 2 changed

# Two captures in one run
npm run web-diff -- --url "https://example.com" --interval-ms 5000
```
