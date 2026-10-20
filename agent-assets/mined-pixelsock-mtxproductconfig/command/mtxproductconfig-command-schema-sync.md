---
name: schema-sync
description: Synchronize Supabase schema and regenerate TypeScript types
---

Execute the schema synchronization workflow for the dynamic configurator by running the schema workflow scripts.

This command will:
1. Introspect the current Supabase schema
2. Generate updated TypeScript types
3. Validate queries against the new schema
4. Update type definitions throughout the codebase

Perfect for:
- After database schema changes
- When new tables or columns are added
- Before major development sessions
- When type mismatches are detected

Usage: `/schema-sync [operation]`
       `/schema-sync` (full sync)
       `/schema-sync watch` (watch mode)
       `/schema-sync validate` (validation only)