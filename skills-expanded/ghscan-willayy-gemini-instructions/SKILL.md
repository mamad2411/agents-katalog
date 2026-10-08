---
name: relational-database-instructions
description: Checklist to run when making changes, additions to a relational database or creating a new relational database.
---

# Relational Database Instructions

This is a checklist to run when making changes, additions to a relational database or creating a new relational database.

## Model distinct entities
Group attributes by the real-world concept they belong to. Attributes belong in the same table if:
- They describe the same core entity.
- They can be uniquely identified with the same primary key.
- They are created and modified together.

## Map Cardinality to Keys
Separate data into different tables based on how entities relate to one another:
- One-to-One (1:1): Keep them in the same table by default.
- One-to-Many (1:N): Put the foreign key on the "many" side.
- Many-to-Many (N:M): Create an intermediate junction table containing foreign keys to both parent tables.

## Apply the 3NF Dependency Rule
Check every column against the primary key. In a normalized table:
- Every column holds a single, atomic value.
- Every column depends directly on the entire primary key, depending on just some parts of a composite key does not count.
- No non-key column depends on another non-key column.

## Constraint naming convention

| Type | Format |
| --- | --- |
| Primary Key | `pk_<table>` |
| Foreign Key | `fk_<source_table>_<target_table>` |
| Unique | `uq_<table>_<column>` |
| Check | `chk_<table>_<purpose>` |
| Default | `df_<table>_<column>` |

## Constraints
- Default to NOT NULL. Allow NULL only when an empty value has a distinct, intentional meaning.
- Explicitly Define Delete Behavior. Never leave foreign key deletion behavior to engine defaults.
- Keep CHECK Constraints Independent. A CHECK constraint must only evaluate the data inside the current row. Never attempt to reference other tables or volatile values.

## When to use a Constraint versus Trigger
- Always use a constraint by default; use a trigger only when a constraint cannot express the rule.

## CRUD only
- The database should only serve CRUD operations, all business logic should be kept application side and not in the DB.
