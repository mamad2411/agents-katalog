---
name: db-check
description: Check Supabase database health, security advisors, and RLS policies. Use automatically after creating or modifying database migrations, RLS policies, or schema changes. Also use when working with Supabase tables or when security/performance issues are suspected.
allowed-tools: mcp__supabase__list_projects, mcp__supabase__get_advisors, mcp__supabase__list_tables
---

## Supabase Database Health Check

### Step 1: Identify Project
Use `mcp__supabase__list_projects` to list available projects.
Ask user to confirm if multiple projects are available.

### Step 2: List Tables
Use `mcp__supabase__list_tables` to see current schema.

### Step 3: Check Advisors

Run both security and performance checks:

**Security:**
- Use `mcp__supabase__get_advisors` with type="security"
- Check for:
  - Tables without RLS enabled
  - Missing policies
  - Exposed sensitive columns

**Performance:**
- Use `mcp__supabase__get_advisors` with type="performance"
- Check for:
  - Missing indexes
  - Potential slow queries
  - Large tables without pagination

### Step 4: Report

Display a structured report:
```
## Supabase Report - [Project name]

### Tables (X total)
- profiles (RLS: ✅)
- opportunities (RLS: ✅)
- responses (RLS: ❌ MISSING)

### Security
✅ No issues detected
or
⚠️ 2 issues detected:
  1. [Description + remediation link]
  2. [Description + remediation link]

### Performance
✅ No issues detected
or
⚠️ 1 issue detected:
  1. [Description + remediation link]
```

Include remediation URLs provided by advisors.
