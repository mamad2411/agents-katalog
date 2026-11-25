---
name: aim-maps-place
description: >
  Google Maps place lookup via headed Chromium. Best-effort name, address,
  rating, phone, website. DOM is volatile — use --screenshot when unsure.
---

# aim-maps-place

```bash
npm run maps-place -- "Statue of Liberty New York"
npm run maps-place -- --screenshot /tmp/maps.png "public library Seattle"
```

Defaults: minimized, stop after session. Treat missing fields as unavailable, not invented.
