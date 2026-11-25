---
name: enrich-fetch
description: SSRF-guarded fetch of an item's primary URL to fill missing raw_body. Internal use only — not callable by the model directly.
user-invocable: false
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["AI_NEWS_DB"]
      os: ["linux", "darwin"]
---

Run `python3 -m core.skills.enrich_fetch --item-id <n>`. Refuses any URL whose host is not on the allowlist or that resolves to a private IP.
