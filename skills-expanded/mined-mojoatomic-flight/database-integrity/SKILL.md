---
name: database-integrity
description: "Database safety — migrations, schema changes, irreversible operations. Use when writing SQL, migrations, or modifying database schema."
user-invocable: false
---

# Database Perception Risk

Database operations are irreversible. Confabulation here causes
data loss. Your model of the schema is especially prone to
reconstruction from training patterns because SQL schemas follow
strong conventions — which means your priors are strong, which
means the distortion risk is high.

Read existing schema before writing migrations.
Verify table names, column names, types, and relationships
against actual schema files. Never drop or alter without
reading current state first.
