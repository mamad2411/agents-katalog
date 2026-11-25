# Supabase MCP

Connect to Supabase PostgreSQL database via MCP for running migrations, queries, and managing your database.

## Setup

### Prerequisites

1. Install Supabase CLI:
```bash
npm install -g supabase
```

2. Link to your project:
```bash
supabase link --project-ref wexuzgrgpuuynirloryg
```

3. Get your database password from Supabase Dashboard → Settings → Database

### Environment Variables

Set these in your environment:
```bash
export SUPABASE_DB_PASSWORD="your-db-password"
export SUPABASE_PROJECT_REF="wexuzgrgpuuynirloryg"
```

## Usage

### Connect via stdio (recommended)

```bash
# Install dependencies first
cd /Users/clay/.config/opencode/skills/converting-mcps-to-skills\ copy/scripts && npm install

# List tools
npx tsx /Users/clay/.config/opencode/skills/converting-mcps-to-skills\ copy/scripts/mcp-stdio.ts "npx -y /Users/clay/.config/opencode/skills/supabase-mcp/dist/index.js" list-tools

# Run SQL query
npx tsx /Users/clay/.config/opencode/skills/converting-mcps-to-skills\ copy/scripts/mcp-stdio.ts "npx -y /Users/clay/.config/opencode/skills/supabase-mcp/dist/index.js" call query "{\"sql\": \"SELECT * FROM organizations LIMIT 5\"}"

# Run migration
npx tsx /Users/clay/.config/opencode/skills/converting-mcps-to-skills\ copy/scripts/mcp-stdio.ts "npx -y /Users/clay/.config/opencode/skills/supabase-mcp/dist/index.js" call migration_up "{\"migration_file\": \"/Users/clay/Documents/Github/im-k8/supabase/migrations/20260317120000_enterprise_organization_schema.sql\"}"
```

### Quick Commands

Run migrations:
```bash
npx supabase migration up --db-url postgresql://postgres:${SUPABASE_DB_PASSWORD}@db.wexuzgrgpuuynirloryg.supabase.co:5432/postgres
```

Run specific migration:
```bash
npx supabase migration up 20260317120000
```

Reset database (careful!):
```bash
npx supabase db reset
```

## Tools Available

- `query` - Run SQL queries
- `migration_up` - Apply pending migrations
- `migration_status` - Check migration status
- `get_tables` - List database tables
- `get_table_schema` - Get table schema

## Troubleshooting

**"Connection refused"**: Check your DB password is correct
**"Permission denied"**: Ensure you're using the postgres role password
**"Table not found"**: Migration hasn't been run yet
