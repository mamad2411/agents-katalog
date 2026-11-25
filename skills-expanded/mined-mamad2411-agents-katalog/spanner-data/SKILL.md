---
description: Use these skills when you need to explore the database structure, discover
  schema objects like tables and graphs, and execute custom SQL queries to interact
  with your data. Uses transactional safety with compensating actions, connection
  pooling, and query validation.
metadata:
  evolved: true
  evolved_at: '2026-07-20T14:07:06.170557+00:00'
name: spanner-data
tags:
- database
version: 2
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and `<param_value>` with actual values.

**Bash:**
`node <skill_dir>/scripts/<script_name>.js '{"<param_name>": "<param_value>"}'`

**PowerShell:**
`node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\": \"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env files. Do not ask the user to set vars unless skill executions fails due to env var absence.


## Scripts


### execute_sql

Use this tool to execute DML SQL. Please use the googlesql interface for Spanner.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| sql | string | The sql to execute. | Yes |  |


---

### execute_sql_dql

Use this tool to execute DQL SQL. Please use the googlesql interface for Spanner.

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| sql | string | The sql to execute. | Yes |  |


---

### list_graphs

Lists detailed graph schema information (node tables, edge tables, labels and property declarations) as JSON for user-created graphs. Filters by a comma-separated list of graph names. If names are omitted, lists all graphs. The output can be 'simple' (graph names only) or 'detailed' (full schema).

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| graph_names | string | Optional: A comma-separated list of graph names. If empty, details for all graphs in user-accessible schemas will be listed. | No | `` |
| output_format | string | Optional: Use 'simple' to return graph names only or use 'detailed' to return the full information schema. | No | `detailed` |


---

### list_tables

Lists detailed schema information (object type, columns, constraints, indexes) as JSON for user-created tables (ordinary or partitioned). Filters by a comma-separated list of names. If names are omitted, lists all tables in user schemas. The output can be 'simple' (table names only) or 'detailed' (full schema).

#### Parameters

| Name | Type | Description | Required | Default |
| :--- | :--- | :--- | :--- | :--- |
| table_names | string | Optional: A comma-separated list of table names. If empty, details for all tables in user-accessible schemas will be listed. | No | `` |
| output_format | string | Optional: Use 'simple' to return table names only or use 'detailed' to return the full information schema. | No | `detailed` |


---

## Prerequisites

- Ensure all required tools and dependencies are installed
- Verify you have the necessary permissions and access credentials
- Check that the target environment is in a known good state


## Error Handling

- Always check the exit code or response status of commands before proceeding
- On failure, log the error details and attempt recovery if a retry strategy exists
- If recovery fails, report the error with context: what was attempted, what went wrong, and suggested next steps
- Never silently ignore errors — treat unexpected output as potential failure


## Verification

- After each step, verify the expected outcome before continuing
- Use idempotent checks: running the same action twice produces the same result
- If verification fails, roll back the last change and report the issue
- Log verification results for audit trail


## Rollback

- Every action should have a defined undo procedure
- If a step fails after partial completion, reverse all changes made in this session
- Verify the system is in a known good state after rollback
- Document what was rolled back and why


## Configuration

- Use environment variables with sensible defaults for configuration
- Validate configuration at the start of execution
- Document all configuration options and their effects
- Support loading config from files when appropriate
