---
name: fable-app-mapping
description: Recon app-mapping substage — traffic and JS comprehension
version: 8.0.0
---

# App Mapping

Read `Workflow/reconnaissance/APP_MAPPING.md`.

```bash
bin/fable-util app-map --target https://HOST --campaign campaigns/T
bin/fable-util js-harvest --campaign campaigns/T
```

Output: `api_inventory.json`, `js_bundle_index.json`, update `fingerprint.json` target_class.
