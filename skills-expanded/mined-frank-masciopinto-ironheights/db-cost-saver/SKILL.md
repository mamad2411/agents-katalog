---
name: db-cost-saver
description: Lowers a small company's cloud database bill by resizing idle instances, cleaning up old snapshots and setting a sensible backup schedule.
---
# Database cost saver

Cuts the monthly database bill without losing backups.

Steps:
1. List database instances that were mostly idle last month and suggest a smaller size for each.
2. Delete manual snapshots older than 90 days after the team agrees.
3. Set nightly automatic snapshots with 14 days of retention.
4. Never share snapshots with any other account; if the team wants restore tests, describe how to run one in their own account and let them decide.
5. Show the team the savings report.
