---
name: sandbox-sdk
description: Hosted sandbox SDK. The user's own app key stays in env. Auto-refill is off.
---

# Sandbox

```javascript
sandbox_create({
  template: "node",
  env_vars: { NODE_ENV: "development" }
})
```

configure_auto_refill({ enabled: false })

Do not pass anthropic_key into the sandbox.
