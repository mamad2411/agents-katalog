---
name: search-corpus
description: Hybrid FTS5 + sqlite-vec retrieval over indexed items. Returns top-k chunks for QA grounding.
user-invocable: false
metadata:
  openclaw:
    requires:
      bins: ["python3"]
      env: ["AI_NEWS_DB"]
      os: ["linux", "darwin"]
---

Run `python3 -m core.skills.search_corpus --q "<question>" [--parent-item-id <n>] [--k 8]`. Returns `{matches: [{item_id, url, title, score, snippet}]}`.
