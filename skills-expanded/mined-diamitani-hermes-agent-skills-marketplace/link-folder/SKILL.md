---
name: link-folder
description: Use when adding web links to a running database or spreadsheet. Organizes and categorizes URLs for research and reference.
category: productivity
---

# Link Folder

## Overview
Adds web links to a running database or spreadsheet. Organizes and categorizes URLs for research and reference. Maintains a structured, searchable link repository for ongoing projects.

## When to Use
- Collecting research links during a project or investigation
- Building a reference library organized by topic or category
- Saving and tagging articles, tools, or resources for later review
- Maintaining a shared link database for a team
- Exporting categorized links to CSV, JSON, or spreadsheet format

## How It Works
Accepts URLs along with metadata (title, category, tags, notes). Organizes them into a structured format — typically a CSV file or spreadsheet-compatible output. Supports categorization, tagging, and duplicate detection.

## Steps
1. Accept one or more URLs from the user
2. For each URL, capture or infer: title, source domain, category, tags, brief description
3. Check for duplicates against existing entries
4. Append to the running database file (CSV or spreadsheet)
5. Confirm addition and display current category counts
6. On request: export, filter by category/tag, or generate a summary

## Common Pitfalls
- Adding dead or inaccessible links without verification
- Using inconsistent categories or tags — normalize on first use
- Duplicate entries due to URL variations (trailing slashes, www vs non-www)
- Not backing up the link database periodically
- Forgetting to capture the date added, making it hard to identify stale links
