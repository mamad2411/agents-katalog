---
name: database-changes
description: Rules for any change to the database schema, migrations, row-level security or auth. Use before editing anything in supabase/ or prisma/.
paths: supabase/**, prisma/**
---

Before any database change:

1. Explain the change in plain English and what could break.
2. Show me the migration before running it. Wait for my OK.
3. Never turn off row-level security, and never drop a table or column without asking twice.
4. After the change, tell me how to check that existing data is still there.
