---
name: hoo-task-board
description: Use to view or mirror the work queue - "task board", "show the queue", /organic-os:task-board. Mirrors to Notion when that connector exists; local queue.md is the source of truth.
---

# Task board

1. Rebuild queue (`core.contracts.rebuild_queue`) and show pending items,
   in-flight items (approved/drafted/partially-applied - the last with its
   human-follow-up note, mirrored from the queue's PARTIAL rows), and
   recently completed (published/measured, last 14 days).
2. Before anything leaves the repo, scan what is about to be mirrored:
   `core.redact.scan(text)` over each item's title, target, and body, then
   `core.redact.summarize(findings)`. This is ADVISORY - it reports, it does
   not block, and a mirror never stops because of it. Include the summary
   line verbatim in the run report when it is non-empty, and read a high-tier
   finding for what it is: the value is already in the brain repo and about
   to be in Notion too, so rotate the credential rather than assume the scan
   caught it in time. If the scan itself fails, mirror anyway and say the
   scan did not run.
3. If the Notion connector is available and site-profile connectors.notion is
   "available": upsert a page per item into the "organic-os board" database
   (create it on first run: properties Status, Kind, Target, Created, ItemId).
   One-way mirror: repo -> Notion. Approvals never flow back through Notion.
4. Without Notion: print the board and stop. No degradation warnings needed;
   the local board IS the product.
