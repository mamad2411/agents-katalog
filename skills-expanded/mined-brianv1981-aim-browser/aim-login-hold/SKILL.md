---
name: aim-login-hold
description: >
  Open a URL and wait for Operator human login or CAPTCHA. Continues when
  --ready-file is created or URL matches --until-url-includes. Never captures
  passwords. Window visible by default for this skill.
---

# aim-login-hold

```bash
# Operator logs in, then: touch /tmp/aim-login-ready
npm run login-hold -- \
  --url "https://example.com/login" \
  --ready-file /tmp/aim-login-ready \
  --max-wait-ms 300000

npm run login-hold -- --url "…" --until-url-includes "/dashboard"
```

- Agents must not type Operator passwords or log credentials.  
- Profile cookies may persist under `CDP_PROFILE_DIR` — treat as a vault.  
- Stop after session still applies (session stays on disk profile).
