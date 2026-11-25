---
name: collect-reddit
description: Pull top-of-day posts from r/MachineLearning and r/LocalLLaMA via public JSON.
user-invocable: false
disable-model-invocation: true
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["AI_NEWS_DB"]
      os: ["linux", "darwin"]
---
Run `python3 -m core.skills.collect_reddit`. Output: `{collected, new}`.
