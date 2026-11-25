---
name: demo-data-seed
description: Loads a demo tenant with orders, invoices and refunds into the local database.
allowed-tools: [Read, Bash]
---

# Skill: demo-data-seed

Load one demo tenant into the local Postgres started by docker compose.

1. Check that the local database is reachable.
2. Create the tenant, ten customers and fifty orders.
3. Print the tenant id for the web app login.
