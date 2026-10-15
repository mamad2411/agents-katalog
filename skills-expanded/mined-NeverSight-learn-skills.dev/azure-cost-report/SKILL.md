---
name: azure-cost-report
description: Create a markdown report of costs for the current month in production azure
---

## Context

- Use Azure `az` cli to get data on the current production environment
- The production environment is in a subscription with production in its name\
- We use azure built in alerts to manage all monitoring
- The report should only focus on the current month

## Your task

i want you to do a report on the cost of our azure cloud environment for the current month. I would like a breakdown of our most expensive items. Along with any delta from the last month or significant changes. I will let you decide what other data should be in a cloud cost report

Output the report to a markdown file.
