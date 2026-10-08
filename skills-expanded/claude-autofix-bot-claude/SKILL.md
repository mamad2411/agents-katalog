# Claude Context Document - Claude AutoFix Bot

> **Purpose:** This file provides comprehensive context for LLM agents (Claude, GPT, etc.) working on this codebase. Read this FIRST before making any changes.

---

## Project Overview

**Name:** Claude AutoFix Bot
**Type:** Production-ready AI-powered development automation system
**Status:** MVP complete with Claude Code CLI, deployable on Railway
**Repository:** https://github.com/MattKilmer/claude-autofix-bot
**Deployment Platform:** Railway (requires persistent server for Claude CLI)

### What This System Does

This is an **automated code fixing pipeline** that:

1. **Monitors** a Slack channel for bug reports/feature requests (natural language)
2. **Processes Images** - Analyzes attached screenshots for visual context (requires `files:read` scope)
3. **Analyzes** your codebase using Claude Code CLI (full agentic capabilities)
4. **Generates** code fixes using agentic tools (Read, Edit, Bash, Glob, Grep)
5. **Creates** a new Git branch with semantic naming (`fix/`, `feat/`, etc.)
6. **Commits** changes with descriptive messages
7. **Pushes** to GitHub and creates a Pull Request
8. **Reports** back to Slack with PR link + cost stats
9. **Supports Follow-ups** - Reply in thread to continue working on same branch/PR

### Key Innovation

Unlike GitHub Copilot or Cursor (IDE-based), this works in **Slack** where teams communicate. Non-technical PMs/designers can request fixes, and the system handles the entire workflow end-to-end.

---

## Architecture

### High-Level Flow

```
Slack Message (user reports bug)
    |
Slack Events API Webhook (verified with signature)
    |
Express Server on Railway (instant 200 OK acknowledgment)
    |
Async Job Queue (in-memory, with retry logic)
    |
Issue Processor (main orchestration - see src/handlers/issue-processor.ts)
    |
+-------------+--------------+------------+--------------+
|             |              |            |              |
Clone/Pull    Claude Agent   Create       Push + Create
Repository    (AI Analysis)  Git Branch   Pull Request
|             |              |            |              |
+-------------+--------------+------------+--------------+
                             |
                    Post Results to Slack
```

### Technology Stack

- **Runtime:** Node.js 20+ with TypeScript (strict mode)
- **Hosting:** Railway (Express server) - requires persistent server for Claude CLI
- **AI:** Claude Code CLI (`claude`) - Full agentic capabilities via shell out
- **Git:** simple-git library + GitHub REST API (Octokit)
- **Slack:** @slack/web-api + Events API
- **Validation:** Zod for runtime type checking
- **Build:** TypeScript compiler (tsc)

### Why Railway (not Vercel)?

The Claude Code CLI requires a persistent server environment with filesystem access. Vercel's serverless functions don't have these capabilities. Railway provides:
- Git CLI pre-installed
- Claude Code CLI installed globally
- Persistent filesystem for repo cloning
- No function timeout limits
- Background job processing

### Claude Code CLI Capabilities

The Claude Code CLI gives Claude full agentic capabilities for fixing code:
- **Read** - Read file contents, explore codebase
- **Edit** - Make surgical edits (not full file replacement)
- **Bash** - Run commands (`npm run build`, `npm test`, etc.)
- **Glob** - Find files by pattern
- **Grep** - Search file contents
- **Write** - Create new files
- **MCP Servers** - Access external tools (GitHub, databases, etc.)

### Design Patterns

- **Event-Driven:** Slack webhook triggers async pipeline
- **Queue-Based:** Jobs processed sequentially with retry logic
- **Fail-Safe:** Comprehensive error handling at every step
- **Stateless:** No database required (MVP), all state in git/Slack
- **Observable:** Structured JSON logging + real-time Slack updates

---

## Codebase Structure

### Critical Files (Touch these with care!)

| File | Purpose | Key Points |
|------|---------|------------|
| `src/handlers/issue-processor.ts` | **Main orchestration** | Handles entire pipeline including follow-ups. This is the heart of the system. |
| `src/services/claude/cli.ts` | **Claude Code CLI integration** | Shells out to Claude CLI with --print and --output-format json flags. |
| `src/services/claude/safety.ts` | **Safety filters** | Blocks dangerous commands, protects sensitive files. |
| `src/services/git/automation.ts` | **Git operations** | Clone, branch, commit, push. Handles authentication + follow-up branch checkout. |
| `src/services/git/github-api.ts` | **PR creation** | Uses Octokit to create PRs with formatted descriptions. |
| `src/utils/thread-tracking.ts` | **Thread context storage** | Stores branch/PR info for thread follow-ups (in-memory). |
| `src/config/index.ts` | **Configuration** | Validates all env vars with Zod. Fails fast if misconfigured. |
| `src/server.ts` | **Express server** | Webhook endpoint, signature verification, job queuing. |

### Directory Map

```
claude-autofix-bot/
├── src/
│   ├── server.ts                 # Express server (Railway entry point)
│   │
│   ├── config/
│   │   └── index.ts              # Environment variable loading + validation
│   │
│   ├── types/
│   │   └── index.ts              # All TypeScript interfaces & Zod schemas
│   │
│   ├── services/                 # External service integrations
│   │   ├── slack/
│   │   │   └── client.ts         # Slack Web API wrapper
│   │   ├── claude/
│   │   │   ├── cli.ts            # Claude Code CLI integration (PRIMARY)
│   │   │   └── safety.ts         # Safety filters for bash commands
│   │   ├── git/
│   │   │   ├── automation.ts     # Git operations (clone, branch, commit, push, checkout)
│   │   │   └── github-api.ts     # GitHub REST API (PR creation, labels)
│   │   └── deployment/
│   │       └── vercel.ts         # Vercel deployment tracking (optional)
│   │
│   ├── handlers/
│   │   └── issue-processor.ts   # MAIN ORCHESTRATION - handles new requests + follow-ups
│   │
│   └── utils/
│       ├── logger.ts             # Structured logging (JSON in prod, colored in dev)
│       ├── queue.ts              # In-memory job queue with retry logic
│       └── thread-tracking.ts    # Thread context storage for follow-ups
│
├── api/                          # Vercel serverless functions (legacy, not used)
│   ├── slack-events.ts           # Slack Events API webhook
│   └── health.ts                 # Health check
│
├── README.md                     # Project overview
├── QUICKSTART.md                 # Setup guide for new users
│
└── Configuration files
    ├── package.json              # Dependencies + scripts
    ├── tsconfig.json             # TypeScript configuration
    ├── railway.json              # Railway deployment settings
    └── .env.example              # Environment variable template
```

---

## Environment Variables

### Required

| Variable | Description | Where to Get | Example |
|----------|-------------|--------------|---------|
| `SLACK_BOT_TOKEN` | Bot OAuth token (requires scopes: `chat:write`, `chat:write.public`, `reactions:write`, `channels:history`, `channels:read`, `files:read`) | Slack App → OAuth & Permissions | `xoxb-123...` |
| `SLACK_SIGNING_SECRET` | Webhook verification | Slack App → Basic Information | `abc123...` |
| `SLACK_CHANNEL_ID` | Channel to monitor | Right-click channel → Copy ID | `C01234567` |
| `ANTHROPIC_API_KEY` | Claude API key | console.anthropic.com | `sk-ant-...` |
| `GITHUB_TOKEN` | Personal access token | github.com/settings/tokens | `ghp_...` |
| `GITHUB_USERNAME` | GitHub username | Your profile | `your-username` |
| `TARGET_REPO_URL` | Repo to fix | GitHub repo URL | `https://github.com/your-org/your-repo.git` |
| `BASE_BRANCH` | Main branch name | Usually `main` or `master` | `main` |

### Optional (for Vercel deployment tracking)

| Variable | Description | Default Behavior |
|----------|-------------|------------------|
| `VERCEL_TOKEN` | Vercel API token | Uses GitHub integration instead |
| `VERCEL_PROJECT_ID` | Vercel project ID | Skips deployment tracking |
| `VERCEL_ORG_ID` | Vercel org/team ID | Relies on auto-deploy |

### Configuration Rules

- **Validation:** All variables validated with Zod at startup
- **Fail-Fast:** Missing required vars = immediate error with helpful message
- **Security:** Never commit `.env.local` (in .gitignore)
- **Development:** Use `.env.local` (loaded by dotenv)
- **Production:** Set in Railway dashboard → Variables

---

## Data Flow & State Management

### Job Lifecycle

1. **Slack Message Received**
   - User posts: `"Fix the navigation bug on mobile"`
   - Webhook triggered: `POST /api/slack-events`

2. **Signature Verification**
   - Validates `x-slack-signature` header
   - Prevents replay attacks (timestamp check)
   - Returns 401 if invalid

3. **Job Creation**
   ```typescript
   IssueJob {
     id: slack_timestamp,
     text: "Fix the navigation bug...",
     channel: "C01234567",
     threadTs: "1234567890.123456",
     userId: "U01234567",
     timestamp: new Date(),
     retryCount: 0,
     images: [{ url, filename, mimetype }],  // Optional: attached screenshots
     isFollowUp: false,
     threadContext: undefined,  // Set on follow-ups
   }
   ```

4. **Async Processing**
   - Job added to in-memory queue
   - Immediate 200 OK returned to Slack (within 3 seconds!)
   - Processing happens in background

5. **Orchestration Pipeline**
   - See `src/handlers/issue-processor.ts` for complete flow
   - Each step updates Slack message in real-time
   - Errors are caught and reported gracefully

6. **Final Result**
   ```typescript
   JobResult {
     status: 'completed',
     branchName: 'fix/navigation-bug-mobile',
     prUrl: 'https://github.com/...',
   }
   ```

### State Storage

- **No database** - Stateless design
- **Git as source of truth** - All changes in version control
- **Slack as UI** - Messages show current state
- **Queue in memory** - Jobs lost on restart (acceptable for MVP)

---

## Claude Integration Details

### Claude Code CLI Architecture

The system uses the **Claude Code CLI** (`claude`) via shell execution. This gives Claude full agentic capabilities including MCP servers, native skills, and the ability to run tests.

### How It Works

1. **CLI Invocation**
   ```typescript
   const result = await execFile('claude', [
     '--print',                    // Non-interactive mode
     '--output-format', 'json',    // JSON output for parsing
     '--max-turns', '100',         // Allow multi-step tasks
     '--dangerously-skip-permissions', // Accept all edits
     issueDescription              // The prompt
   ], {
     cwd: repoPath,
     env: { ...process.env, ANTHROPIC_API_KEY: config.claude.apiKey },
     timeout: 600000,              // 10 minute timeout
   });
   ```

2. **JSON Output Parsing**
   ```json
   {
     "type": "result",
     "subtype": "success",
     "total_cost_usd": 0.15,
     "duration_ms": 45000,
     "num_turns": 12,
     "result": "I've fixed the navigation bug...",
     "session_id": "abc123-def456"
   }
   ```

3. **Workflow**
   - **EXPLORE:** Read project files, use Glob/Grep to find relevant code
   - **INVESTIGATE:** Read files, trace code paths
   - **FIX:** Use Edit tool for surgical changes
   - **VERIFY:** Run build/test commands
   - **ITERATE:** If tests fail, debug and retry

### Thread Follow-up Support

When a user replies in a completed thread:
1. **Context retrieval** - Get branch name, PR URL, original request from `thread-tracking.ts`
2. **Branch checkout** - Use `gitAutomationService.checkoutExistingBranch()` instead of creating new
3. **Enhanced prompt** - Include original request and files changed in Claude prompt
4. **Same PR** - Commits go to existing branch, updating the same PR

### Customizing the System Prompt

The system prompt in `cli.ts` can be customized for your specific codebase:
- Add your project's architecture overview
- Specify package managers and build commands
- Include code conventions and patterns
- Add paths to key files Claude should be aware of

---

## Security Considerations

### Current Security Measures

1. **Slack Signature Verification**
   - Prevents unauthorized webhook calls
   - Uses timing-safe comparison
   - Checks timestamp to prevent replay attacks

2. **GitHub Token Handling**
   - Token injected into git URLs for authentication
   - Removed from logs and error messages

3. **Environment Variable Protection**
   - All secrets in environment variables
   - Never committed to git (.env.local in .gitignore)
   - Validated at startup with helpful error messages

4. **Safety Filters**
   - Dangerous bash commands can be blocked
   - Sensitive files can be protected
   - Customize rules in `src/services/claude/safety.ts`

---

## Deployment Guide

### Local Development

```bash
# 1. Install dependencies
npm install

# 2. Create .env.local from template
cp .env.example .env.local
# Edit .env.local with your credentials

# 3. Start dev server
npm run dev
# Server runs on http://localhost:3000

# 4. Expose webhook (in another terminal)
ngrok http 3000
# Copy HTTPS URL (e.g., https://abc123.ngrok.io)

# 5. Configure Slack Event Subscriptions
# Set Request URL to: https://abc123.ngrok.io/api/slack-events
```

### Production Deployment (Railway)

```bash
# Option 1: Railway CLI
npm install -g @railway/cli
railway login
railway init
railway up

# Option 2: GitHub Integration (Recommended)
# 1. Go to railway.app/new
# 2. Import GitHub repo
# 3. Railway auto-detects Node.js and uses railway.json config
# 4. Add environment variables in Railway dashboard
# 5. Deploy (auto-deploys on every push to main)
```

### Post-Deployment Checklist

- [ ] Update Slack Event Subscriptions URL to Railway URL
- [ ] Test health endpoint: `curl https://your-app.up.railway.app/api/health`
- [ ] Send test message in Slack
- [ ] Verify PR created successfully
- [ ] Check Railway logs for errors

---

## Common Issues & Solutions

### Issue: "Invalid Slack signature"

**Causes:**
- Wrong `SLACK_SIGNING_SECRET`
- Request timestamp too old (>5 minutes)
- ngrok tunnel expired (local dev)

**Solutions:**
1. Verify signing secret from Slack app settings
2. Restart ngrok and update Slack webhook URL
3. Check system clock is synchronized

### Issue: "Claude API error"

**Causes:**
- Invalid `ANTHROPIC_API_KEY`
- API rate limits exceeded
- Network timeout

**Solutions:**
1. Verify API key at console.anthropic.com
2. Check API usage/limits in dashboard
3. Increase timeout in Claude service

### Issue: "Git push failed"

**Causes:**
- Invalid `GITHUB_TOKEN`
- Insufficient permissions (needs `repo` scope)
- Token expired

**Solutions:**
1. Generate new token at github.com/settings/tokens
2. Ensure `repo` and `workflow` scopes are selected
3. Verify `TARGET_REPO_URL` is correct

---

## Git Workflow

### Branch Naming Convention

Automatically determined from issue text:

| Keywords | Branch Prefix | Example |
|----------|---------------|---------|
| bug, fix, error | `fix/` | `fix/navigation-menu-mobile` |
| feature, add, implement | `feat/` | `feat/dark-mode-toggle` |
| refactor, improve, optimize | `refactor/` | `refactor/authentication-async` |
| (default) | `chore/` | `chore/update-dependencies` |

### Commit Message Format

```
Auto-fix: [first 50 chars of issue]

[Claude's solution description]

Files changed:
- src/components/Nav.tsx
- src/styles/nav.css

---
Generated by Claude AutoFix Bot
Co-authored-by: Claude <noreply@anthropic.com>
```

### Pull Request Format

**Title:** `[emoji] [type]: [description]`

**Body:**
```markdown
## Automated Fix by Claude

### Analysis
[Claude's analysis of the issue]

### Solution Applied
[Description of the fix]

### Files Changed (N)
- `path/to/file1.ts`
- `path/to/file2.css`

### Testing
- [ ] Verify fix works as expected
- [ ] Check for any regressions
- [ ] Review code changes for quality

---
This PR was automatically generated by Claude AutoFix Bot
Co-authored-by: Claude <noreply@anthropic.com>
```

**Labels:** Automatically adds `automated` and `claude-fix`

---

## AI Agent Guidelines

### When Making Changes

**DO:**
- Read this file first
- Understand the full pipeline before modifying
- Test changes locally before committing
- Update documentation if you change behavior
- Follow existing code style and patterns
- Add TypeScript types for new code
- Handle errors gracefully
- Log important events

**DON'T:**
- Remove error handling without replacement
- Change API contracts without updating callers
- Commit secrets or credentials
- Break the build (run `npm run build` first)
- Skip signature verification on webhooks
- Return non-200 status to Slack webhook within 3s

### Code Review Checklist

Before committing changes, verify:

1. **Type Safety**
   ```bash
   npm run type-check  # Should pass with no errors
   ```

2. **Build**
   ```bash
   npm run build  # Should complete successfully
   ```

3. **Lint**
   ```bash
   npm run lint  # Should pass (or fix issues)
   ```

---

## Critical Constraints

### Hard Requirements

1. **Slack Webhook Must Respond in <3 Seconds**
   - Slack retries if no response
   - Use async queue for long-running tasks
   - Return 200 OK immediately

2. **Git Authentication**
   - Token must have `repo` scope
   - Use HTTPS URLs with embedded token
   - Never log or expose tokens

3. **Branch Naming Rules**
   - No spaces (use hyphens)
   - Lowercase only
   - Max 50 characters
   - Semantic prefix (fix/, feat/, etc.)

### Performance Targets

- **Webhook Response:** <500ms (actual: ~100ms)
- **Total Pipeline:** <5 minutes (typical: 2-3 minutes)
- **Claude API Call:** <30 seconds (depends on complexity)
- **Git Operations:** <20 seconds (clone + commit + push)
- **PR Creation:** <5 seconds (GitHub API)

---

## FAQ for AI Agents

**Q: Where should I start if asked to add a new feature?**
A: 1) Understand the feature, 2) Review `issue-processor.ts` to see where it fits, 3) Create a new service if needed, 4) Update types, 5) Test locally, 6) Update docs.

**Q: How do I test my changes?**
A: Run `npm run build && npm run type-check`, then `npm run dev` + ngrok, post a test message in Slack.

**Q: The build is failing. What should I check?**
A: 1) TypeScript errors (`npm run type-check`), 2) Missing imports, 3) Zod schema validation.

**Q: Can I change the Claude prompt?**
A: Yes! The prompt is in `src/services/claude/cli.ts` → `buildSystemPrompt()`. Customize it for your specific codebase.

**Q: How do thread follow-ups work?**
A: When a job completes, the bot stores context (branch, PR URL, files changed) in memory. If someone replies in the thread, the bot checks out the existing branch and continues work there, pushing to the same PR.

**Q: Can this work with private repositories?**
A: Yes! The `GITHUB_TOKEN` authenticates with private repos. Just ensure the token has access.

---

**Last Updated:** 2025-12-12
**Maintained By:** Matt Kilmer
**Contact:** https://github.com/MattKilmer/claude-autofix-bot/issues

---

*This document is living documentation. Update it whenever you make significant changes to the codebase.*
