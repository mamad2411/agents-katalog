---
name: aim-form-fill
description: >
  Fill form fields on an allowlisted host. Requires --allow-host and --fields.
  Never submits unless --submit. Redacts password-like values in output.
---

# aim-form-fill

**Safety:** refuse without `--allow-host`. No default submit.

```bash
npm run form-fill -- \
  --url "https://example.com/form" \
  --allow-host example.com \
  --fields '{"#email":"agent@example.com","#q":"hello"}'

# Only when the Operator asked to submit:
npm run form-fill -- --url "…" --allow-host example.com --fields '{…}' --submit
```

- Do not log raw passwords (JSON redacts password-like keys).  
- Sensitive sites only with explicit Operator order.  
- `file://` may be blocked; use `http://127.0.0.1` fixtures when testing locally.  

Defaults: stop after session.
