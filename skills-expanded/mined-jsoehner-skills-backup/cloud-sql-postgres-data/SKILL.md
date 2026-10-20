---
name: cloud-sql-postgres-data
description: Use these skills when you need to explore the database structure, discover
  schema objects like views or stored procedures, and execute custom SQL queries to
  interact with your data.
license: Apache-2.0
metadata:
  version: v1
  publisher: google
---

## Usage

All scripts can be executed using Node.js. Replace `<param_name>` and
`<param_value>` with actual values.

**Bash:** `node <skill_dir>/scripts/<script_name>.js '{"<param_name>":
"<param_value>"}'`

**PowerShell:** `node <skill_dir>/scripts/<script_name>.js '{\"<param_name>\":
\"<param_value>\"}'`

Note: The scripts automatically load the environment variables from various .env
files. Do not ask the user to set vars unless skill executions fails due to env
var absence.

## Scripts

### execute_sql

Use this tool to execute a single SQL statement.

#### Parameters

Name | Type   | Description         | Required | Default
:--- | :----- | :------------------ | :------- | :------
sql  | string | The sql to execute. | Yes      |
 

--------------------------------------------------------------------------------

### get_query_plan

Provide information about how MySQL executes a SQL statement. Common use cases
include: 1) analyze query plan to improve its performance, and 2) determine
effectiveness of existing indexes and evalueate new ones.

#### Parameters

Name          | Type   | Description                   | Required | Default
:------------ | :----- | :---------------------------- | :------- | :------
sql_statement | string | The sql statement to explain. | Yes      |
 

--------------------------------------------------------------------------------

### list_active_queries

Lists top N (default 10) ongoing queries from processlist and innodb_trx,
ordered by execution time in descending order. Returns detailed information of
those queries in json format, including process id, query, transaction duration,
transaction wait duration, process time, transaction state, process state,
username with host, transaction rows locked, transaction rows modified, and db
schema.

#### Parameters

| Name              | Type    | Description               | Required | Default |
| :---------------- | :------ | :------------------------ | :------- | :------ |
| min_duration_secs | integer | Optional: Only show       | No       | `0`     |
:                   :         : queries running for at    :          :         :
:                   :         : least this long in        :          :         :
:                   :         : seconds                   :          :         :
| limit             | integer | Optional: The maximum     | No       | `100`   |
:                   :         : number of rows to return. :          :         :
 

--------------------------------------------------------------------------------

### list_tables

Lists detailed schema information (object type, columns, constraints, indexes,
triggers, comment) as JSON for user-created tables (ordinary or partitioned).
Filters by a comma-separated list of names. If names are omitted, lists all
tables in user schemas.

#### Parameters

| Name          | Type   | Description     | Required | Default    |
| :------------ | :----- | :-------------- | :------- | :--------- |
| table_names   | string | Optional: A     | No       | ``         |
:               :        : comma-separated :          :            :
:               :        : list of table   :          :            :
:               :        : names. If       :          :            :
:               :        : empty, details  :          :            :
:               :        : for all tables  :          :            :
:               :        : will be listed. :          :            :
| output_format | string | Optional: Use   | No       | `detailed` |
:               :        : 'simple' for    :          :            :
:               :        : names only or   :          :            :
:               :        : 'detailed' for  :          :            :
:               :        : full info.      :          :            :
 

--------------------------------------------------------------------------------

### list_triggers

Lists all non-internal triggers in a database. Returns trigger name, schema
name, table name, whether its enabled or disabled, timing (e.g BEFORE/AFTER of
the event), the events that cause the trigger to fire such as INSERT, UPDATE, or
DELETE, whether the trigger activates per ROW or per STATEMENT, the handler
function executed by the trigger and full definition.

#### Parameters

| Name         | Type    | Description                  | Required | Default |
| :----------- | :------ | :--------------------------- | :------- | :------ |
| trigger_name | string  | Optional: A specific trigger | No       | ``      |
:              :         : name pattern to search for.  :          :         :
| schema_name  | string  | Optional: A specific schema  | No       | ``      |
:              :         : name pattern to search for.  :          :         :
| table_name   | string  | Optional: A specific table   | No       | ``      |
:              :         : name pattern to search for.  :          :         :
| limit        | integer | Optional: The maximum number | No       | `50`    |
:              :         : of rows to return.           :          :         :
 

--------------------------------------------------------------------------------

### list_views

Lists views in the database from pg_views with a default limit of 50 rows.
Returns schemaname, viewname, ownername and the definition.

#### Parameters

| Name        | Type    | Description                     | Required | Default |
| :---------- | :------ | :------------------------------ | :------- | :------ |
| view_name   | string  | Optional: A specific view name  | No       | ``      |
:             :         : to search for.                  :          :         :
| schema_name | string  | Optional: A specific schema     | No       | ``      |
:             :         : name to search for.             :          :         :
| limit       | integer | Optional: The maximum number of | No       | `50`    |
:             :         : rows to return.                 :          :         :
 

--------------------------------------------------------------------------------

## Anti-Patterns

- NEVER execute raw DML/DDL operations on production database instances without verification.
- NEVER ignore connection limits and connection pool starvation indicators.


