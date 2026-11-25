---
name: aim-screenshot-url
description: >
  Open a URL in headed Chromium and save a PNG. Use for proof artifacts.
  Minimized by default; stops after session.
---

# aim-screenshot-url

```bash
npm run screenshot-url -- "https://example.com"
npm run screenshot-url -- --out /tmp/proof.png --url "https://example.com"
npm run screenshot-url -- --full-page "https://example.com"
```

Report the absolute `screenshot` path from JSON. Do not describe visuals without the PNG (or pair with page-fetch).
