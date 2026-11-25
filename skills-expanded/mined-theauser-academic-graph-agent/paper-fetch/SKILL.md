---
name: paper-fetch
description: Fetch paper metadata from lightweight academic sources like arXiv and save normalized paper JSON records.
metadata:
  {
    "openclaw":
      {
        "emoji": "📥",
        "requires": { "bins": ["python3"] }
      },
  }
---

# paper-fetch

Use this skill when the user wants to search papers by topic, keyword, or free-text query.

Workflow
- Run `python3 /root/openclaw-dev/workspace/scripts/fetch_papers.py "<query>" --max-results <N>`
- Read the JSON output
- Use returned `saved_to` paths as inputs for later reflection

Notes
- This MVP uses arXiv first for stability and low dependency overhead.
- Outputs are saved under `/root/openclaw-dev/workspace/data/papers/`.
