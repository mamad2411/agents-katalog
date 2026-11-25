---
name: collect-github
description: Fetch GitHub repos created in the last 7 days with stars>50 in AI/ML topics; insert new ones into the items DB.
user-invocable: false
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["AI_NEWS_DB", "GITHUB_TOKEN"]
      os: ["linux", "darwin"]
---

Run `python3 -m core.skills.collect_github`. Uses a read-only PAT (`public_repo` scope only). Output: `{collected, new}`.
