---
name: sql-server
description: "Operate and tune Microsoft SQL Server: execution plans, indexing strategy, isolation levels, tempdb contention, backup/restore and migration safety."
type: procedural
category: databases
domain: databases
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - sql server slow query
  - mssql execution plan
  - tempdb contention
  - sql server index strategy
  - sql server backup strategy
aliases:
  - mssql
keywords:
  - sql-server
  - mssql
  - t-sql
  - execution-plan
  - indexing
  - tempdb
source: custom
enabled: true
---

# Microsoft SQL Server

## Purpose

Operate and tune Microsoft SQL Server: execution plans, indexing strategy, isolation levels, tempdb contention, backup/restore and migration safety.

## When to Use

- A query or stored procedure is slow and you need the actual plan, waits and reads.
- You are designing indexes, partition schemes or statistics maintenance for a T-SQL workload.
- A schema migration or backup/restore needs a rollback plan that provably works.

## When NOT to Use

- The engine is PostgreSQL, MySQL or SQLite; use the engine-specific skill instead.
- The problem is at the application layer (N+1 loops, chatty ORM) rather than in the statement.
- You need cross-cloud managed-service decisions only, with no T-SQL involved.

## Capabilities

- Read and interpret actual execution plans, wait stats and SET STATISTICS IO output.
- Design covering, filtered and columnstore indexes with write-cost accounting.
- Choose isolation levels and row-versioning options without introducing deadlock storms.
- Plan backup, restore and online-index operations with measured downtime.

## Inputs

- The failing statement or procedure, its parameters, and the target row counts.
- SQL Server version and edition (Express lacks online index and partition features).
- Baseline metrics: duration, logical reads, CPU time, and the waits observed.

## Workflow

1. Capture the baseline with `SET STATISTICS IO, TIME ON` and Query Store before changing anything.
2. Read the actual plan for scans, key lookups, spills and cardinality misestimates; note the costliest operator.
3. Fix the highest-cost operator first: index, rewrite, statistics update or parameterization change.
4. Re-measure against the same baseline; a faster plan with more logical reads is not a win.
5. Roll the change forward through a tested restore or migration script the team can reverse.

## Tools

- sqlcmd / Azure Data Studio / SSMS
- Query Store and DMVs (`sys.dm_exec_query_stats`)
- git for versioned migrations

## Examples

- `SET STATISTICS IO, TIME ON; EXEC dbo.ReportSales @From='2026-01-01';`
- `SELECT TOP 5 * FROM sys.dm_exec_query_stats ORDER BY total_worker_time DESC;`
- `ALTER INDEX ALL ON dbo.Orders REBUILD WITH (ONLINE = ON, MAXDOP = 4);`

## Safety

- Never run a destructive migration or restore without a verified backup and a tested rollback.
- `ONLINE = ON` and partitioning are Enterprise features; confirm the edition before promising uptime.
- Take schema locks into account: a rebuild can block writes for the duration of the operation.

## Source

All-Skills canonical library (`skills/databases/sql-server`). First-party skill, maintained in this repository.

## Notes

- Query Store is the cheapest long-term regression detector; enable it before tuning.
- Capturing the plan is not the same as proving the fix: keep both the before and after numbers.
- Pairs with: `databases/schema-evolution`, `performance-optimization`.
