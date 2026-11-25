---
name: collect-hn
description: Pull AI-tagged Hacker News stories from the last 24h via Algolia.
user-invocable: false
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["AI_NEWS_DB"]
      os: ["linux", "darwin"]
---
Run `python3 -m core.skills.collect_hn`. Output: `{collected, new}`.
