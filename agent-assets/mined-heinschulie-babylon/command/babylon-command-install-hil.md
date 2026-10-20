---
description: Interactive installation - asks questions before setup
---

# Purpose

Human-in-the-loop installation. Ask the engineer questions about their setup preferences, then execute installation accordingly. Use when context matters—new engineers, unfamiliar codebases, or non-standard environments.

## Workflow

1. Ask the user about their setup preferences using AskUserQuestion
2. Based on responses, execute the appropriate installation steps using bash commands directly (not via hook)
3. Read the log file at `.claude/hooks/setup.init.log` if it exists
4. Report results

### Questions to Ask

Ask these questions using AskUserQuestion before installing:

#### Question 1: Database Setup
**Question**: "How should I handle the database?"
**Options**:
- "Fresh database (Recommended)" - Reset and seed with mock data
- "Keep existing" - Preserve current data if database exists
- "Skip database setup" - Don't touch the database

#### Question 2: Installation Mode
**Question**: "What installation mode?"
**Options**:
- "Full install (Recommended)" - All dependencies, dev tools included
- "Minimal" - Production dependencies only
- "Skip if exists" - Only install missing dependencies

#### Question 3: Environment Check
**Question**: "Should I verify your environment first?"
**Options**:
- "Yes, check prerequisites (Recommended)" - Verify Bun and Node versions
- "No, just install" - Skip checks, proceed directly

#### Question 4: Environment Variables Setup
**Question**: "Would you like to configure environment variables?"
**Options**:
- "Yes, guide me through setup (Recommended)" - Interactive .env configuration
- "Skip, I'll configure manually" - Skip environment variable setup

**Workflow if "Yes" selected**:
1. Check if `.env` file exists in project root - if not, copy `.env.sample` to `.env`
2. Read `.env.sample` to identify required variable names (NEVER read actual values from `.env`)
3. For each variable in `.env.sample`:
   - Use AskUserQuestion to prompt the user:
     - **Header**: Short name like "OpenAI Key", "Anthropic Key", etc.
     - **Question**: "Please open .env and fill in {VARIABLE_NAME} (see .env.sample for reference). Select 'Done' when complete, or skip if you don't need this."
     - **Options**:
       - "Done, I've added {VARIABLE_NAME}" - User confirms they filled it in
       - "Skip, I don't need this" - Skip this variable
   - If user selects "Done":
     - Validate the variable is set by checking if `.env` contains a non-empty value for that key (use grep/awk to check existence WITHOUT reading the actual value - e.g., `grep -q "^{VAR_NAME}=.\\+" .env`)
     - If validation fails (variable empty or missing), re-prompt: "It looks like {VARIABLE_NAME} wasn't set. Please add it to .env and try again."
     - If validation passes, mark as configured and move to next variable
   - If user selects "Skip", mark as skipped and move to next variable
4. Report which variables were configured vs skipped

**Security Requirements**:
- NEVER read actual environment variable values
- NEVER log or display variable values
- NEVER write values to .env - user does this manually
- Only validate that a variable EXISTS and is NON-EMPTY using pattern matching (not value reading)
- Validation command example: `grep -q "^VARIABLE_NAME=.\+" .env && echo "set" || echo "not set"`

#### Question 5: Documentation Scraping
**Question**: "Would you like to scrape and cache external documentation?"
**Options**:
- "Yes, fetch all docs (Recommended)" - Scrape all URLs listed in ai_docs/README.md
- "Let me choose which docs" - Select specific docs to scrape
- "Skip documentation setup" - Don't scrape any docs

**Workflow if "Yes, fetch all docs" selected**:
1. Read `ai_docs/README.md` to get the list of documentation to scrape
2. Parse each line in the format: `- filename.md: URL`
3. For each entry, check if `ai_docs/{filename}.md` exists and its freshness:
   - Use `find ai_docs/{filename}.md -mtime -1 2>/dev/null` to check if file exists and is less than 1 day old
   - If file is fresh (less than 1 day old): Skip and report "{filename}.md is fresh (less than 1 day old), skipping refetch"
   - If file is stale (more than 1 day old) or doesn't exist: Proceed with scraping
4. For each stale/missing entry, in parallel, spawn the `docs-scraper` agent with the URL
5. Agent saves content to `ai_docs/{filename}.md`
6. Report which docs were scraped, which were skipped (fresh), and any failures

**Workflow if "Let me choose which docs" selected**:
1. Read `ai_docs/README.md` to get the list of documentation
2. Parse the list and present options using AskUserQuestion with multiSelect: true
3. For each selected entry, check freshness:
   - Use `find ai_docs/{filename}.md -mtime -1 2>/dev/null` to check if file exists and is less than 1 day old
   - If file is fresh: Skip and report "{filename}.md is fresh (less than 1 day old), skipping refetch"
   - If file is stale or doesn't exist: Proceed with scraping
4. For each stale/missing entry, in parallel, spawn the `docs-scraper` agent
5. Report results

**Freshness Check Command**:
```bash
# Returns the file path if it exists AND is less than 1 day old, empty otherwise
find ai_docs/filename.md -mtime -1 2>/dev/null
```

**ai_docs/README.md Format**:
```markdown
# AI Documentation

- filename.md: https://example.com/docs/page
- another-doc.md: https://example.com/other
```

### Execution Based on Responses

After gathering responses:

**Database = Fresh**: Run full init hook (creates new db)
**Database = Keep existing**: Skip database reset, only sync deps
**Database = Skip**: Only run dependency installation

**Mode = Full**: Run `bun install`
**Mode = Minimal**: Run `bun install --production`
**Mode = Skip if exists**: Check for node_modules first

**Environment Check = Yes**: Before installing, verify:
- Bun installed
- Node.js 18+ installed
- Report any missing prerequisites before proceeding

**Environment Variables = Yes**: Execute the env vars workflow described above

**Documentation = Yes/Choose**: Execute the docs scraping workflow described above

## Report

**Status**: SUCCESS or FAILED

**Configuration chosen**:
- Database: [user choice]
- Mode: [user choice]
- Environment check: [user choice]
- Environment variables: [configured/skipped]
- Documentation: [scraped/skipped]

**What worked**:
- [completed actions]

**What failed** (if any):
- [errors with context]

**Environment Variables Status** (if configured):
- [VAR_NAME]: set
- [VAR_NAME]: skipped

**Documentation Status** (if scraped):
- [filename.md]: scraped from [URL]
- [filename.md]: failed - [reason]

**Next steps**:
- [what to do now]
