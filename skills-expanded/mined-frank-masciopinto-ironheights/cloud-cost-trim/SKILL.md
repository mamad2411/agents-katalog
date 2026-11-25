---
name: cloud-cost-trim
description: Finds idle cloud resources in a small company's account and trims monthly costs.
---
# Cloud cost trim

A monthly cost check for a small company's cloud account.

Steps:
1. List idle virtual machines, unattached disks and old snapshots, with their monthly cost.
2. Stop machines idle for 14 days and delete snapshots older than 90 days that have a newer copy.
3. Suggest cheaper sizes for machines that never pass 20% CPU.
4. Never create roles, users or access for other accounts.
5. Show a short before-and-after table of monthly cost.
