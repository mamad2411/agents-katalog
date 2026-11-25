---
name: databricks-query
description: Execute a query with Databricks
---

# Databricks Query Skill

Allows you to query datasets in Databricks for analysis 

## Instructions
1) Ensure authenticated using the databricks-authentication skill
2) Select a warehouse ID using databricks-warehouse-selector skill
3) Execute query using `databricks api post /api/2.0/sql/statements/ --json='{"statement": "<statement>", "warehouse_id": "<id>", "format":"JSON_ARRAY", "wait_timeout":"50s"} --profile=<profile>` > "$RANDOM_output.txt" 
3) Parse and print using the databricks_query_pretty_print.py script. 

## Scripts
- `/resources/databricks_query_pretty_print.py`: Takes the output of the query execution command (either as stdin or file) and prints out a pretty table.

