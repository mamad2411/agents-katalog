---
name: gemini-extension-sync
description: Provides the ability and instructions to refresh and synchronize the offline Gemini CLI documentation by running the up-to-date python update script locally.
---

# Sync Official Documentation

Whenever a user explicitly asks you to "sync the documents", "update the docs", or refresh the local documentation knowledge base for this Gemini plugin repository, you should automatically trigger the Python update script located in the root of the project via your shell command tool.

```bash
python3 scripts/update_docs.py
```

## How It Works

The script securely runs `git clone --depth 1` against the official GitHub repository (`google-gemini/gemini-cli`), extracts strictly the `docs/` folder, overwrites the local `docs/` directory matching the latest remote commit, and aggressively deletes temporary files. It requires virtually 0 configuration and completely circumvents GitHub API throttle mechanisms.
