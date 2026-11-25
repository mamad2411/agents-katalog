---
name: log-reader
description: Reads the recent history of the repository and answers questions about it. Use when the user asks who changed a file, when a line was introduced, or what the last release contained.
version: 1.0.0
allowed-tools: Read, Bash
---

# Log reader

1. Run `scripts/history.py <path>` for the file the user named.
2. Answer from what it printed, quoting the commit you relied on.
