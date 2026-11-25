---
name: tidy-folder
description: Propose how to tidy a messy folder (Downloads, Desktop) - group files, flag duplicates and old installers - and only move files after the user approves the plan.
---

# Tidy a folder

1. List the folder with `glob`/`read_file` (names, sizes, dates via a read-only command if allowed).
2. Propose a plan as a table: file group -> destination, plus duplicates and stale installers to remove.
3. **Stop and ask.** Move or delete nothing until the user approves the plan. Never delete without an explicit yes for that item.
4. After approval, apply it step by step and report what moved; on any error stop and say which file.
