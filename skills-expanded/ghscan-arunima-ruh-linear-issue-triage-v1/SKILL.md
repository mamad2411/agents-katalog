---
name: result-query
version: 1.0.0
description: "Read stored records from the agent result tables for inspection and follow-up questions."
user-invocable: true
metadata:
  openclaw:
    requires:
      bins: [bash, python3]
      env: [PG_CONNECTION_STRING, ORG_ID, AGENT_ID]
---

# Result Query

## I/O Contract

- **Input:** Query intent from the user (table name + optional filters)
- **Output:** JSON rows from the selected result table
- **DB Read:** `scripts/data_writer.py query` command

## Execute

```bash
python3 scripts/data_writer.py query --table <table_name> --limit 50
```
