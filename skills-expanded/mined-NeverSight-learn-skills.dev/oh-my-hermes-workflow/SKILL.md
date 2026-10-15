---
name: oh-my-hermes-workflow
description: Install and configure Oh My Hermes workflow layer for building, shipping, and operating apps with Hermes Agent
triggers:
  - "install oh my hermes"
  - "set up hermes workflow layer"
  - "configure hermes cto loop"
  - "bootstrap hermes skills"
  - "set up autonomous deployment workflow"
  - "install hermes agent skills"
  - "configure hermes for production"
  - "set up hermes monitoring"
---

# oh-my-hermes-workflow

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Oh My Hermes is an opinionated workflow layer for building, shipping, and operating apps with Hermes Agent. It provides 23+ curated skills that enable Hermes to autonomously handle the complete software lifecycle — from requirements clarification to production deployment and monitoring.

## What Oh My Hermes Does

- **Full Project Lifecycle**: Takes projects from idea to production with autonomous workflows
- **Autonomous CTO Loop**: Hourly issue triage, implementation, security review, and deployment approval flow
- **Multi-Agent Orchestration**: PM, Dev, QA, Security, and Ops agents working together via Kanban
- **Persistent Memory**: Hermes remembers project context, requirements, and decisions across sessions
- **Integration Layer**: Connects Hermes with Claude Code, Codex, Vercel, Supabase, GitHub, Sentry

## Installation

### Prerequisites

1. **Install Hermes Agent first**: Follow [Hermes quickstart](https://hermes-agent.nousresearch.com/docs/getting-started/quickstart)
2. **Configure messaging**: Set up Telegram, Slack, Discord, or WhatsApp gateway
3. **Verify Hermes is running**: Test by messaging your Hermes bot

### Install Oh My Hermes

```bash
# One-line install
curl -fsSL https://raw.githubusercontent.com/salomondiei08/oh-my-hermes/main/install.sh | bash

# Or clone and install manually
git clone https://github.com/salomondiei08/oh-my-hermes /tmp/oh-my-hermes
bash /tmp/oh-my-hermes/install.sh
```

### Bootstrap a Project

```bash
# Navigate to your project directory
cd /path/to/your/project

# Run bootstrap script
bash /tmp/oh-my-hermes/scripts/bootstrap.sh

# Verify installation
bash /tmp/oh-my-hermes/scripts/verify.sh
```

### Message-Based Setup (Recommended)

Once installed, message your Hermes bot:

```
set up the CTO loop
```

Hermes will guide you through:
- GitHub repository configuration
- Fine-grained token creation
- Production URL setup
- Webhook configuration
- Monitoring setup

## Key Skills

Oh My Hermes provides 23+ skills loaded into `~/.hermes/skills/`:

### Onboarding & Planning

**onboarding**
```bash
# Trigger in Hermes chat
"walk me through setting up oh my hermes"
```
Guides full setup in chat — no terminal required.

**clarify-requirements**
```bash
# Trigger in Hermes chat
"start a new app"
"clarify requirements for this project"
```
Asks 7 structured questions, saves answers to Hermes memory.

**product-brief**
```bash
# Trigger after clarify-requirements
"generate the product brief"
```
Creates `PRODUCT_BRIEF.md` from requirements.

**design-handoff**
```bash
# Trigger in Hermes chat
"convert my design to implementation spec"
```
Transforms design notes into technical specifications.

### Implementation

**choose-engine**
```bash
# Trigger in Hermes chat
"implement this feature"
```
Routes tasks to Hermes, Claude Code, or Codex based on complexity.

**implement-with-claude-code**
```bash
# Invoked by choose-engine for complex multi-file tasks
# Scaffolds Claude Code with:
# - Full project context
# - Scope constraints
# - Security guardrails
```

**implement-with-codex**
```bash
# Invoked by choose-engine for single-file fixes
# Quick targeted edits
```

### Deployment

**deploy-to-vercel**
```bash
# Trigger in Hermes chat
"deploy to vercel"
"ship this to production"
```

Example workflow:
1. Pre-deploy checks (secrets scan, build validation)
2. Deploys to Vercel
3. Captures preview/production URL
4. Runs health checks
5. Notifies via configured channel

**connect-supabase**
```bash
# Trigger in Hermes chat
"connect supabase"
"set up database"
```

Handles:
- Database linking
- Migration pushing
- Environment variable configuration in Vercel
- Connection validation

### Monitoring

**setup-monitoring**
```bash
# Trigger in Hermes chat
"set up monitoring"
```

Configures:
- Sentry error tracking
- Uptime Kuma health checks
- Alert webhooks

**health-check**
```bash
# Runs automatically every 15 minutes
# Manual trigger:
"run health check"
```

Validates:
- `/api/health` endpoint response
- Supabase connectivity
- Vercel deployment status
- Response times

### GitHub Integration

**manage-github-issues**
```bash
# Trigger in Hermes chat
"triage github issues"
"create issue for bug in login"
"close issue #42"
```

**create-github-pr**
```bash
# Automatic during implementation workflow
# Includes:
# - Secret scan before PR creation
# - Conventional commit messages
# - Linked issue references
```

**auto-issue-triage**
```bash
# Runs hourly via cron
# Scores issues by:
# - User impact
# - Business priority
# - Technical debt
# Picks top priority and starts implementation
```

**review-github-pr**
```bash
# Automatic when PR is ready
# Provides:
# - Diff analysis
# - Security checks
# - Plain-English summary
# - Preview URL validation
```

**security-review**
```bash
# Runs on every PR
# Weekly supply chain audit
"run security review on PR #12"
```

Checks:
- Secret scanning (no API keys, tokens)
- OWASP top 10 vulnerabilities
- CVE audit of dependencies
- Supply chain security (weekly)

## Configuration

### Environment Variables

Create `.hermes/config.env`:

```bash
# GitHub Integration
GITHUB_OWNER=your-username
GITHUB_REPO=your-repo
GITHUB_TOKEN=${GITHUB_TOKEN}  # Fine-grained token with repo access

# Deployment
VERCEL_TOKEN=${VERCEL_TOKEN}  # Vercel API token
VERCEL_PROJECT_ID=${VERCEL_PROJECT_ID}
VERCEL_ORG_ID=${VERCEL_ORG_ID}

# Database
SUPABASE_URL=${SUPABASE_URL}
SUPABASE_ANON_KEY=${SUPABASE_ANON_KEY}
SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}

# Monitoring
SENTRY_DSN=${SENTRY_DSN}
UPTIME_KUMA_URL=${UPTIME_KUMA_URL}
UPTIME_KUMA_TOKEN=${UPTIME_KUMA_TOKEN}

# Notifications
SLACK_WEBHOOK_URL=${SLACK_WEBHOOK_URL}
TELEGRAM_BOT_TOKEN=${TELEGRAM_BOT_TOKEN}
TELEGRAM_CHAT_ID=${TELEGRAM_CHAT_ID}

# Production
PRODUCTION_URL=https://yourapp.com
```

### Hermes Memory Configuration

Oh My Hermes stores project context in Hermes memory at:
```
~/.hermes/memory/
  ├── requirements.json      # From clarify-requirements
  ├── product-brief.md       # Generated brief
  ├── kanban-state.json      # Current task status
  └── deployment-log.json    # Deployment history
```

### Kanban Configuration

The autonomous loop uses a simple Kanban:

```
Backlog → In Progress → Review → Done
```

Stored in `~/.hermes/memory/kanban-state.json`:

```json
{
  "backlog": [
    {"id": "issue-42", "priority": 8, "title": "Fix login redirect"}
  ],
  "in_progress": [
    {"id": "issue-39", "assigned": "dev-agent", "started": "2026-05-16T10:00:00Z"}
  ],
  "review": [
    {"id": "pr-12", "reviewer": "security-agent", "checks": ["secret-scan", "owasp"]}
  ],
  "done": [
    {"id": "issue-38", "completed": "2026-05-15T14:30:00Z", "deployed": true}
  ]
}
```

## Real-World Workflows

### Start a New App from Scratch

Message your Hermes bot:

```
Start a new app called TaskFlow — a Kanban board for small teams
```

Hermes will:
1. Load `clarify-requirements` skill
2. Ask 7 questions about your app
3. Generate `PRODUCT_BRIEF.md`
4. Run `choose-engine` to decide implementation approach
5. Implement the app
6. Deploy to Vercel
7. Set up monitoring

### Implement a Feature

Message your Hermes bot:

```
Add Google OAuth login to the app
```

Hermes workflow:
1. Creates GitHub issue
2. Dev Agent implements
3. Security Agent scans for secrets
4. QA Agent validates build and preview
5. Sends you approval message:

```
PR #15 — Add Google OAuth login

What changed: Users can now sign in with Google.
Added /api/auth/google endpoint and callback handler.

Build: passing | Preview: healthy (200ms) | No secrets found
Preview: https://taskflow-oauth.vercel.app

Reply YES to ship. Reply NO and tell me why.
```

6. You reply `YES`
7. Merges, deploys, health-checks, confirms

### Manual Deployment

```bash
# From your project directory
cd /path/to/your/project

# Message Hermes:
"deploy to vercel"

# Or run skill directly (if configured)
hermes run deploy-to-vercel
```

### Security Audit

```bash
# Message Hermes:
"run security review on main branch"

# Hermes will:
# - Scan for hardcoded secrets
# - Check dependencies for CVEs
# - Run OWASP checks
# - Generate report
```

### Health Check

```bash
# Message Hermes:
"check if production is healthy"

# Hermes validates:
# - Production URL responds
# - Database is connected
# - API endpoints work
# - Response times are acceptable
```

## Autonomous CTO Loop

Once configured, this runs every hour automatically:

```
┌─────────────────────────────────────────┐
│  GitHub Issue Opened (#42)              │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  PM Agent (auto-issue-triage)           │
│  - Scores issue: priority 8/10          │
│  - Moves to Backlog                     │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  Dev Agent (implement)                  │
│  - Moves to In Progress                 │
│  - Writes code                          │
│  - Creates PR #12                       │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  Security Agent (security-review)       │
│  - Secret scan: PASS                    │
│  - OWASP check: PASS                    │
│  - CVE scan: PASS                       │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  QA Agent (review-github-pr)            │
│  - Build: passing                       │
│  - Health check: 180ms                  │
│  - Plain-English summary written        │
│  - Moves to Review                      │
└───────────┬─────────────────────────────┘
            │
            ▼
┌─────────────────────────────────────────┐
│  Notification Sent (YOU on Telegram)    │
│  "PR #12 ready. Reply YES to ship."     │
└───────────┬─────────────────────────────┘
            │
     ┌──────┴──────┐
     │             │
     ▼             ▼
  ┌─────┐      ┌──────┐
  │ YES │      │  NO  │
  └──┬──┘      └───┬──┘
     │             │
     │             ▼
     │      ┌────────────────┐
     │      │ Dev Agent      │
     │      │ iterates on    │
     │      │ your feedback  │
     │      └────────────────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  Ops Agent                              │
│  - Merges PR                            │
│  - Deploys to production                │
│  - Runs health check                    │
│  - Confirms live URL                    │
│  - Moves to Done                        │
└─────────────────────────────────────────┘
```

## Common Patterns

### Goal-Oriented Sessions

Use `/goal` command to keep Hermes focused:

```
/goal Build a working MVP of TaskFlow with Google OAuth, deploy to Vercel, and set up monitoring — all within the next 2 hours
```

Hermes will:
- Break down the goal into sub-tasks
- Execute each step autonomously
- Check in with you at key decision points
- Persist progress across interruptions

### Custom Skill Creation

Create project-specific skills:

```bash
# Message Hermes:
"create a new skill for automated database backups"

# Hermes will:
# - Use create-skill meta-skill
# - Generate skill template
# - Save to ~/.hermes/skills/db-backup.md
# - Make it available for invocation
```

Skill structure:

```markdown
---
name: db-backup
description: Automated Supabase database backup to S3
triggers:
  - "backup the database"
  - "create db backup"
---

# db-backup

## What it does
Creates timestamped backup of Supabase database and uploads to S3.

## Prerequisites
- Supabase CLI installed
- AWS credentials configured
- S3 bucket created

## Steps
1. Export database: `supabase db dump -f backup.sql`
2. Compress: `gzip backup.sql`
3. Upload: `aws s3 cp backup.sql.gz s3://my-backups/$(date +%Y%m%d-%H%M%S).sql.gz`
4. Verify upload
5. Clean up local files
6. Notify completion

## Configuration
- S3_BUCKET=${S3_BUCKET}
- SUPABASE_PROJECT_REF=${SUPABASE_PROJECT_REF}
```

### Scheduled Tasks

Configure cron jobs in `~/.hermes/cron.d/`:

```bash
# Hourly issue triage
0 * * * * hermes run auto-issue-triage

# Daily deployment report
0 9 * * * hermes run daily-report

# Weekly security audit
0 2 * * 0 hermes run security-review --full-audit

# Every 15 minutes health check
*/15 * * * * hermes run health-check
```

### Integration with Claude Code

When a task requires deep multi-file editing:

```bash
# Message Hermes:
"refactor the authentication system to use sessions instead of JWT"

# Hermes workflow:
# 1. choose-engine analyzes complexity
# 2. Determines Claude Code is needed
# 3. Scaffolds Claude Code session with:
#    - Full project context
#    - Relevant files identified
#    - Scope constraints
#    - Security requirements
# 4. Claude Code performs refactor
# 5. Hermes reviews changes
# 6. Creates PR for your approval
```

## Troubleshooting

### Hermes Not Loading Skills

```bash
# Verify skills directory
ls -la ~/.hermes/skills/

# Re-run installer
bash /tmp/oh-my-hermes/install.sh

# Check Hermes logs
tail -f ~/.hermes/logs/hermes.log
```

### GitHub Integration Failing

```bash
# Verify token has correct permissions
# Required: repo (full), workflow, admin:repo_hook

# Test token manually
curl -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}

# Reconfigure in Hermes chat:
"reconfigure github integration"
```

### Deployment Issues

```bash
# Verify Vercel token
vercel whoami

# Check environment variables are set
hermes run verify-env

# View deployment logs
vercel logs ${VERCEL_PROJECT_ID}

# Manual health check
curl https://your-production-url.vercel.app/api/health
```

### Monitoring Not Working

```bash
# Verify Sentry DSN
echo ${SENTRY_DSN}

# Test Uptime Kuma connection
curl ${UPTIME_KUMA_URL}/api/status

# Reconfigure monitoring
"set up monitoring again"
```

### Autonomous Loop Not Running

```bash
# Check cron jobs are configured
crontab -l | grep hermes

# Verify Hermes daemon is running
ps aux | grep hermes

# Restart Hermes
systemctl restart hermes  # if using systemd
# or
hermes restart

# Check kanban state
cat ~/.hermes/memory/kanban-state.json
```

## Advanced Configuration

### Custom Agent Behavior

Modify agent behavior in `~/.hermes/config/agents.yaml`:

```yaml
agents:
  pm:
    issue_scoring:
      user_impact_weight: 0.4
      business_priority_weight: 0.3
      technical_debt_weight: 0.3
    auto_triage_frequency: "0 * * * *"  # Hourly
  
  dev:
    max_parallel_tasks: 2
    preferred_engine: "claude-code"  # or "codex" or "hermes"
    
  security:
    require_all_checks: true
    fail_on_secrets: true
    weekly_audit_day: "sunday"
    
  qa:
    health_check_timeout: 5000  # ms
    required_response_time: 1000  # ms
    
  ops:
    auto_merge_on_approval: true
    deployment_health_check_retries: 3
```

### Notification Templates

Customize notification format in `~/.hermes/config/notifications.yaml`:

```yaml
templates:
  pr_ready:
    title: "PR #{pr_number} — {pr_title}"
    body: |
      What changed: {summary}
      
      Build: {build_status} | Preview: {health_status} ({response_time}ms)
      Security: {security_status}
      Preview: {preview_url}
      
      Reply YES to ship. Reply NO and tell me why.
    
  deployment_success:
    title: "✅ Deployed to production"
    body: |
      {project_name} v{version}
      URL: {production_url}
      Health: {health_status}
      Deploy time: {deploy_time}s
```

## Best Practices

1. **Start with onboarding**: Message `"set up oh my hermes"` — let the bot guide you
2. **Use /goal for focus**: Keep long sessions on track with explicit goals
3. **Review security scans**: Always check security-review output before merging
4. **Monitor health checks**: Configure alerts for failed health checks
5. **Backup Hermes memory**: `~/.hermes/memory/` contains valuable project context
6. **Version control skills**: Commit custom skills to your repo in `.hermes/skills/`
7. **Test in preview**: Always validate preview URLs before approving production deploys
8. **Keep tokens secure**: Never commit tokens — use `.env` files and `.gitignore`

## Integration Reference

### Vercel

```bash
# Deploy
vercel deploy --prod

# Get deployment URL
vercel ls ${PROJECT_NAME} --json | jq -r '.[0].url'

# Set environment variable
vercel env add SUPABASE_URL production
```

### Supabase

```bash
# Push migrations
supabase db push

# Get connection string
supabase db connection-string

# Run query
supabase db query "SELECT * FROM users LIMIT 1"
```

### GitHub API

```bash
# Create issue
curl -X POST \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/issues \
  -d '{"title": "Bug in login", "body": "Description", "labels": ["bug"]}'

# Create PR
curl -X POST \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Content-Type: application/json" \
  https://api.github.com/repos/${GITHUB_OWNER}/${GITHUB_REPO}/pulls \
  -d '{"title": "Fix login", "head": "fix-login", "base": "main", "body": "Fixes #42"}'
```

### Sentry

```bash
# Initialize
sentry-cli init

# Upload source maps
sentry-cli releases files ${VERSION} upload-sourcemaps ./dist
```

This skill enables AI coding agents to guide developers through installing, configuring, and using Oh My Hermes to build autonomous software development workflows with Hermes Agent.
