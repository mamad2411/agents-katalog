---
name: digest-writer
description: Writes a weekly digest of what changed in the repository. Use when the user asks what happened this week, wants a changelog draft, or has to report progress on Friday.
version: 1.1.0
allowed-tools: Read, Bash(git *)
---

# Digest writer

1. Run `git log --since="1 week ago" --oneline` and read the result.
2. Run `scripts/summarise.py` on it to group the commits by area and attach the
   title of every issue a commit mentions.
3. Write `digest.md` with one section per area.
