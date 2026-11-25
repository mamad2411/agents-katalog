---
name: paperclip-setup-infraforge-specialist
description: Routes Paperclip terminal setup, local development environment bootstrap, and Supabase connection configuration to the Paperclip Setup Specialist.
company: infraforge-ai
---

# Paperclip Setup Specialist

## Overview
This skill routes all Paperclip setup and installation operations to the Paperclip Setup Specialist agent. This agent handles the workflow from cloning the repository and installing dependencies, through configuring the Supabase connection, to verifying the server is running and agents are populated.

## Routing Criteria

Route to this skill when:
- Setting up Paperclip in a terminal for the first time
- Configuring local development environment (clone, install, run)
- Connecting Paperclip to Supabase (setting DATABASE_URL, SUPABASE_URL, keys)
- Running Drizzle schema generation and database push
- Verifying server health and agent population
- Troubleshooting startup or connection issues
- Configuring environment variables for local or production use

## Capabilities

### Terminal Setup & Bootstrap
- **Repository Cloning**: Clone paperclip-render from GitHub
- **Dependency Installation**: Run `pnpm install` with proper Node.js version
- **Dev Server Startup**: Run `pnpm dev` and verify server starts on port 3100
- **Health Check**: Verify `/api/health` and `/api/companies` endpoints respond

### Supabase Connection
- **Environment Configuration**: Set `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, `SUPABASE_ANON_KEY` from `.env.example`
- **Database URL**: Configure `DATABASE_URL` for production or leave unset for local PGlite
- **Schema Sync**: Run `pnpm db:generate` and `pnpm db:push` to sync Drizzle schema
- **Connection Verification**: Confirm Supabase connection is working

### Troubleshooting
- **Startup Issues**: Diagnose port conflicts, missing dependencies, Node version mismatches
- **Database Issues**: Diagnose connection failures, schema mismatch, migration errors
- **Agent Population**: Verify agents are populated in the database after setup

## Related Skills

- `nimbus-infraforge-supabase-specialist` - Supabase database operations (coordinate for advanced DB work)
- `environment-variable-access` - Environment variable management
- `configuration-file-parsing` - Configuration file handling
- `hermes-communication-setup` - Hermes agent communication setup
- `secure-api-key-management` - API key security
- `infrastructure-monitoring-setup` - Infrastructure monitoring

## Setup Workflow

### Step 1: Clone & Install
```bash
git clone https://github.com/Construct-AI-primary/paperclip-render.git
cd paperclip-render
pnpm install
```

### Step 2: Configure Environment
```bash
# For local dev (PGlite) - leave DATABASE_URL unset
cp .env.example .env
# Edit .env with actual Supabase credentials
```

### Step 3: Start Server
```bash
pnpm dev
# Server starts on http://localhost:3100
```

### Step 4: Verify
```bash
curl http://localhost:3100/api/health
curl http://localhost:3100/api/companies
```

### Step 5: Database Schema (if using Supabase)
```bash
pnpm db:generate
pnpm db:push
```

## Success Metrics

- **Setup Success**: ≥95% successful first-time setups
- **Connection Success**: 100% successful Supabase connection verification
- **Time to Running**: <10 minutes from clone to running server

---

*This skill routes to the Paperclip Setup Specialist for comprehensive setup and configuration of the Paperclip ecosystem.*
