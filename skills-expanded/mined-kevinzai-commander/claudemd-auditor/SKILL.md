---
name: claudemd-auditor
description: "Audit your CLAUDE.md against the actual codebase — find stale instructions, missing context, and optimization opportunities. Use when 'audit claude md', 'check claude md', 'is my claude md accurate', 'optimize instructions'."
allowed-tools:
  - Read
  - Bash
  - Glob
  - Grep
  - Edit
  - AskUserQuestion
---

# CLAUDE.md Auditor

Compares your CLAUDE.md instructions against the real state of the codebase and suggests concrete improvements.

## What It Checks

### 1. Stale References
- File paths mentioned in CLAUDE.md that no longer exist
- Commands referenced that aren't in package.json scripts
- Dependencies mentioned that aren't in package.json
- Tool/framework references that don't match installed versions

### 2. Missing Context
- Key directories not documented (src/, lib/, tests/)
- Package.json scripts not mentioned
- Environment variables used in code but not documented
- MCP servers configured but not referenced
- Git hooks or CI workflows not mentioned

### 3. Cache Optimization
- Is static content first, dynamic last? (cache-friendly ordering)
- Are frequently-referenced paths at the top?
- Is the file under 500 lines? (diminishing returns above this)
- Are there duplicate instructions that waste tokens?

### 4. Token Efficiency
- Verbose instructions that could be condensed
- Commented-out or TODO sections wasting context
- Redundant path listings that could use glob patterns
- Long example blocks that could be shortened

## Process

### Step 1: Read CLAUDE.md
Read the project's CLAUDE.md file completely.

### Step 2: Scan Codebase
Use Glob and Bash to check:
```bash
# Files that exist
ls -la package.json tsconfig.json .env* Dockerfile docker-compose.yml
# Package scripts
node -e "console.log(Object.keys(require('./package.json').scripts || {}).join(', '))"
# Key directories
ls -d src/ lib/ tests/ app/ pages/ components/ 2>/dev/null
# Installed deps
node -e "var p=require('./package.json'); console.log(Object.keys({...p.dependencies,...p.devDependencies}).join(', '))"
```

### Step 3: Cross-Reference
For each instruction in CLAUDE.md:
- Does the referenced file/path exist?
- Does the referenced command work?
- Is the information current?

### Step 4: Report
Present findings via AskUserQuestion:

```
CLAUDE.md Audit Results:
━━━━━━━━━━━━━━━━━━━━━━

File: CLAUDE.md (342 lines)

Stale References: 3
  X "src/utils/auth.ts" — file doesn't exist (was it renamed?)
  X "npm run deploy" — no deploy script in package.json
  X "Uses Prisma" — prisma not in dependencies

Missing Context: 4
  ! tests/ directory not documented (14 test files)
  ! .github/workflows/ not mentioned (CI exists)
  ! Environment: NEXT_PUBLIC_API_URL used but not documented
  ! MCP server "context7" configured but not referenced

Cache Optimization: 2
  > Move "Coding Standards" section above "API Reference" (more frequently needed)
  > Remove 45 lines of commented-out old instructions

Token Savings Estimate: ~2,100 tokens/session

Apply fixes?
> Yes, fix all automatically
  Show me each fix first
  Export report only
```
