---
name: gpu-install
description: Pinned installer. The billing key creates instances, but the code is a fixed commit.
---

# Install

The runtime is pinned to commit abc1234def5678.

```bash
uv run --with git+https://github.com/example/tool@abc1234def5678 tool
```

RUNPOD_API_KEY is required before create-instance.
