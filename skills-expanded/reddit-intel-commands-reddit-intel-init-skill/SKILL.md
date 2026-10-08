---
name: reddit-intel-init
description: |
  Initialize reddit-intel for your project. Creates config file (.reddit-intel.json),
  data directory, and product-context template.
  First-time setup — run once per project.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - AskUserQuestion
metadata:
  trigger: When user wants to set up reddit-intel, initialize Reddit competitive intelligence, or mentions reddit-intel init
---

# reddit-intel init

First-time setup. Creates config file and data directory for Reddit competitive intelligence.

## Flow

1. Ask user for:
   - `product_name` (required)
   - `data_dir` (default: `./reddit-intel/data`)
   - `language` (en/zh, default: en)
2. Run:
   ```bash
   python3 SKILL_DIR/scripts/jsonl_ops.py init --data-dir <dir> --product-name <name> --lang <en|zh>
   ```
   Where `SKILL_DIR` is the parent directory of `commands/` (i.e., the reddit-intel repo root).
   The script resolves `SKILL_DIR` by looking for `scripts/jsonl_ops.py` relative to itself.
3. Tell user to fill in `product-context.md` with their product details
4. Show available commands:
   ```
   /reddit-kw   — Expand keywords
   /reddit-sub  — Discover subreddits
   /reddit-fp   — Find pain-point posts
   /reddit-ac   — Analyze comment sections
   ```
