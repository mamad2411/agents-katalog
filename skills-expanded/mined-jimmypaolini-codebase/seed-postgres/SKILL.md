---
name: seed-postgres
description: "Use this skill to dump and restore local PostgreSQL databases, schemas, and tables (collections) using Nx targets and pg_dump/pg_restore. Use when asked to backup, dump, export, restore, import, or copy local database data."
user-invocable: true
---

# PostgreSQL Data Management

## When to Use

Use this skill when you need to:

- Backup or export the entire local PostgreSQL database.
- Dump specific databases, schemas, or tables (often referred to as collections).
- Restore or import data into the local PostgreSQL instance.

## Prerequisites

- The PostgreSQL container must be running. Use `nx run codebase:postgres-container:up` to start it.
- `pg_dump` and `pg_restore` (version 18) must be installed locally. If you see version mismatch errors, ensure the client tools are installed via Homebrew (`brew install postgresql@18`) or apt.

## Procedure

Dumps and restores are managed securely via Nx targets, which pull credentials directly from the `.env` file and output to the `data/` folder at the workspace root.

Choose the appropriate command based on the required scope:

### Dumps (Backup/Export)

Files are exported using the custom format (`-Fc`) and saved as `.dump` files in the `data/` folder.

1. **Complete Database Cluster:**

   ```bash
   nx run codebase:postgres-data:dump-complete

   ```

2. **Dictionary Tables Only:**

   ```bash
   nx run codebase:postgres-data:dump-dictionary

   ```

3. **Literature Tables Only:**

   ```bash
   nx run codebase:postgres-data:dump-literature

   ```

4. **Specific Database:**

   ```bash
   nx run codebase:postgres-data:dump-database --database=<database_name>

   ```

5. **Specific Schema:**

   ```bash
   nx run codebase:postgres-data:dump-schema --schema=<schema_name>

   ```

6. **Specific Table (Single Collection):**

   ```bash
   nx run codebase:postgres-data:dump-table --table=<table_name>

   ```

7. **Custom Flags (Multiple Tables):**

   ```bash
   nx run codebase:postgres-data:dump-custom --flags="-t table1 -t table2" --name="my_dump"

   ```

### Restores (Import)

Restores are destructive by default. They use the clean flag (`-c`) to drop existing objects before restoring, and run in a single transaction (`-1`).

1. **Complete Database Cluster:**

   ```bash
   nx run codebase:postgres-data:restore-complete

   ```

2. **Dictionary Tables Only:**

   ```bash
   nx run codebase:postgres-data:restore-dictionary

   ```

3. **Literature Tables Only:**

   ```bash
   nx run codebase:postgres-data:restore-literature

   ```

4. **Specific Database:**

   ```bash
   nx run codebase:postgres-data:restore-database --database=<database_name>

   ```

5. **Specific Schema:**

   ```bash
   nx run codebase:postgres-data:restore-schema --schema=<schema_name>

   ```

6. **Specific Table (Single Collection):**

   ```bash
   nx run codebase:postgres-data:restore-table --table=<table_name>

   ```

7. **Custom Flags (Multiple Tables):**

   ```bash
   nx run codebase:postgres-data:restore-custom --flags="-t table1 -t table2" --name="my_dump"

   ```

## Notes

- "Collections" in the context of this codebase typically map to PostgreSQL **tables**. Use the `table` commands when collections are requested.
- Dumps created using these targets are saved to the `data/` folder, which is intentionally gitignored to prevent accidental commits of local database structures or sensitive data.
