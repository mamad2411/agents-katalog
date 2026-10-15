---
name: hermes-agent-control-room
description: Control Room template for managing Hermes agents from one VPS agent to specialist teams and orchestrated workflows
triggers:
  - set up a hermes agent control room
  - create an agent control room for my vps
  - organize my hermes agents with a control room
  - bootstrap hermes agent infrastructure
  - set up orchestrator and specialist agents
  - create a multi-agent hermes system
  - manage multiple hermes agents on my server
  - design an agent control plane
---

# Hermes Agent Control Room

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

Hermes Agent Control Room is a governance and documentation framework for running Hermes agents as a managed system instead of disconnected bots. It provides:

- **Control plane structure** for documenting agents, runbooks, secrets, and backups
- **Architecture levels** from one agent → specialists → orchestrator → automated team
- **Task bus pattern** for orchestrator-to-specialist delegation
- **Bundled skills** for VPS setup, agent management, security audits, and backups
- **Templates** for agent inventory, Docker configs, env maps, runbooks, and backup plans

The core principle: **set up the Control Room first, then plug agents into it.**

## Architecture Levels

### Level 1: Control Room + One Agent
Single Hermes agent with documented setup, runbooks, and secret management.

### Level 2: Direct Specialist Agents
Multiple role-specific agents (`hermes-seo`, `hermes-dev`, `hermes-cmo`) that you talk to directly.

### Level 3: Orchestrator + Specialists
Add `hermes-orchestrator` as a front door that routes tasks to specialists via the task bus.

### Level 4: Automated Agent Team
Recurring workflows, audits, and automated task routing after manual workflows work.

## Installation

### Option A: Clone to Existing VPS

```bash
ssh root@YOUR_SERVER
git clone https://github.com/shannhk/hermes-agent-control-room.git /root/agent-control-room
cd /root/agent-control-room
cat docs/starter-guide.md
```

### Option B: Bootstrap New Hetzner VPS

Use the bundled `create-vps` and `setup-control-room` skills:

```bash
# Agent workflow:
# 1. create-vps → creates Hetzner VPS, SSH key, SSH alias
# 2. setup-control-room → installs Node, Claude Code, Codex, Docker, Hermes, clones repo
# 3. SSH in and complete auth
```

The `setup-control-room` skill will:
- Install base packages (git, curl, build-essential)
- Install Node.js via nvm
- Install Claude Code, Codex CLI, Hermes Agent
- Clone this repo to `/root/agent-control-room`
- Link bundled skills to `~/.claude/skills`

After bootstrap, complete interactive auth:

```bash
ssh <alias>
claude /login
codex
hermes
```

## Folder Structure

```text
agent-control-room/
  README.md                      # This file
  agents/                        # Per-agent folders
    hermes-life/
      inventory.md               # Agent metadata
      docker.md                  # Container notes
      env-map.md                 # Secret map (no raw values)
      runbook.md                 # Start/stop/debug procedures
      backup.md                  # Backup plan
  docs/
    architecture.md              # System design
    levels.md                    # Growth stages
    naming.md                    # Agent naming conventions
    security.md                  # Security model
    task-bus.md                  # Task routing spec
    orchestrator.md              # Orchestrator design
    starter-guide.md             # First steps
  shared/
    api-keys-sop.md              # Secret management SOP
    commands.md                  # Common commands
    security.md                  # Security checklist
  templates/
    agent/                       # Agent doc templates
    docker/                      # Docker compose templates
    task-bus/                    # Task bus templates
  skills/                        # Bundled agent skills
  examples/                      # Example setups per level
```

## Registering Your First Agent

```bash
cd /root/agent-control-room
mkdir -p agents/hermes-life
cp templates/agent/*.md agents/hermes-life/
```

Fill in the templates:

**agents/hermes-life/inventory.md**
```markdown
# hermes-life Agent Inventory

**Agent Name:** hermes-life  
**Role:** Personal assistant  
**Port:** 3000  
**Status:** Active  
**Created:** 2026-05-15  
**Owner:** Your Name

## Purpose
Personal Hermes agent for daily tasks, research, and file management.

## Tools
- Terminal
- File system
- Web research
- Email (via API)

## Secrets Required
- ANTHROPIC_API_KEY
- GMAIL_API_KEY (optional)
```

**agents/hermes-life/env-map.md**
```markdown
# hermes-life Environment Map

**DO NOT COMMIT RAW SECRETS**

## Required Secrets

| Name | Provider | Scope | Location | Rotated |
|------|----------|-------|----------|---------|
| ANTHROPIC_API_KEY | Anthropic | Full API | /srv/hermes-life/data/.env | 2026-05-10 |
| GMAIL_API_KEY | Google | Gmail read/send | /srv/hermes-life/data/.env | Never |

## Storage Location
`/srv/hermes-life/data/.env`

## Backup Location
Encrypted backup in `/root/backups/hermes-life-env.gpg`
```

**agents/hermes-life/runbook.md**
```markdown
# hermes-life Runbook

## Start Agent
```bash
cd /srv/hermes-life
docker-compose up -d
```

## Stop Agent
```bash
docker-compose down
```

## View Logs
```bash
docker-compose logs -f
```

## Restart After Config Change
```bash
docker-compose restart
```

## Emergency Recovery
1. Check logs: `docker-compose logs --tail=100`
2. Verify .env exists: `ls -la /srv/hermes-life/data/.env`
3. Restore from backup if needed: `gpg -d /root/backups/hermes-life-env.gpg > /srv/hermes-life/data/.env`
4. Restart: `docker-compose restart`
```

## Runtime Split

Keep control plane separate from runtime state:

```text
/root/agent-control-room/
  Control plane: docs, templates, runbooks, registry
  No raw secrets

/srv/<agent-name>/data/
  Runtime: .env, memory, skills, sessions, crons, logs
  Raw secrets live here
```

## Adding Direct Specialist Agents (Level 2)

```bash
# Create specialist agent folders
cd /root/agent-control-room
mkdir -p agents/{hermes-seo,hermes-dev,hermes-cmo,hermes-ops}

# Copy templates
for agent in hermes-seo hermes-dev hermes-cmo hermes-ops; do
  cp templates/agent/*.md agents/$agent/
done
```

Document each specialist's:
- **Role**: What it does (SEO audits, code changes, marketing, ops)
- **Tools**: Specific tool access (Ahrefs API, GitHub, Mailchimp, Docker socket)
- **Secrets**: Scoped credentials (not full system access)
- **Port**: Unique port per agent (3001, 3002, 3003, etc.)

## Adding an Orchestrator (Level 3)

### Create Orchestrator Agent

```bash
mkdir -p agents/hermes-orchestrator
cp templates/agent/*.md agents/hermes-orchestrator/
```

**agents/hermes-orchestrator/inventory.md**
```markdown
# hermes-orchestrator Agent Inventory

**Agent Name:** hermes-orchestrator  
**Role:** Front door / task router  
**Port:** 3100  
**Status:** Active

## Purpose
Routes user requests to specialist agents via the task bus.
Synthesizes results from multiple specialists.

## Tools
- File system (task bus access)
- No direct access to specialist credentials
- Read/write to `/srv/agent-bus/{inbox,working,outbox,archive}`

## Does NOT Have
- Database credentials
- API keys for specialist services
- SSH keys to other systems

## Delegation Model
1. Receives user request
2. Writes task to `/srv/agent-bus/inbox/<specialist>/`
3. Specialist picks up task, works on it, writes result to `/srv/agent-bus/outbox/`
4. Orchestrator reads result, synthesizes, responds to user
```

### Set Up Task Bus

```bash
# Create task bus directories
mkdir -p /srv/agent-bus/{inbox,working,outbox,archive}
mkdir -p /srv/agent-bus/inbox/{seo,dev,cmo,ops}

# Copy task bus config
cp agent-control-room/templates/task-bus/agents.yaml /srv/agent-bus/
```

**Task Bus Workflow**

```text
1. User → Orchestrator: "Audit SEO for example.com"

2. Orchestrator → Task Bus:
   /srv/agent-bus/inbox/seo/task-001.md
   ---
   Task: SEO audit for example.com
   Requested: 2026-05-17T10:00:00Z
   Requestor: User via hermes-orchestrator
   ---

3. hermes-seo → Picks Up Task:
   Moves task-001.md to /srv/agent-bus/working/seo/

4. hermes-seo → Works:
   Runs Ahrefs audit, generates report

5. hermes-seo → Completes:
   /srv/agent-bus/outbox/seo/result-001.md
   Moves task to /srv/agent-bus/archive/seo/

6. Orchestrator → Reads Result:
   Synthesizes and responds to user
```

## Task Bus Example

**Task Template** (`/srv/agent-bus/inbox/dev/task-002.md`):

```markdown
---
task_id: task-002
specialist: dev
created: 2026-05-17T14:30:00Z
requestor: hermes-orchestrator
priority: normal
---

# Task: Add Contact Form to Website

## Requirements
- Add contact form to /contact page
- Fields: name, email, message
- POST to /api/contact endpoint
- Basic validation

## Context
User requested contact form for their business site.

## Expected Deliverables
- Updated HTML/CSS
- Form validation script
- Deployed to staging
```

**Result Template** (`/srv/agent-bus/outbox/dev/result-002.md`):

```markdown
---
task_id: task-002
specialist: dev
completed: 2026-05-17T15:45:00Z
status: success
---

# Result: Contact Form Added

## What Was Done
- Created /contact.html with form fields
- Added client-side validation in contact.js
- Configured backend endpoint at /api/contact
- Deployed to staging: https://staging.example.com/contact

## Files Changed
- /public/contact.html (new)
- /public/js/contact.js (new)
- /api/contact.js (new)

## Testing
- Tested form submission
- Verified email delivery
- Checked validation for all fields

## Next Steps
User can review at staging URL. Ready for production deploy on approval.
```

## Docker Compose for Orchestrator

**templates/docker/docker-compose.orchestrator.yml**:

```yaml
version: '3.8'

services:
  hermes-orchestrator:
    image: hermes-agent:latest
    container_name: hermes-orchestrator
    restart: unless-stopped
    ports:
      - "3100:3000"
    volumes:
      - /srv/hermes-orchestrator/data:/app/data
      - /srv/agent-bus:/srv/agent-bus
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - AGENT_ROLE=orchestrator
      - TASK_BUS_PATH=/srv/agent-bus
    networks:
      - agent-net

networks:
  agent-net:
    driver: bridge
```

## Security Best Practices

### Secret Storage

```bash
# Store secrets in per-agent .env files
/srv/hermes-life/data/.env
/srv/hermes-seo/data/.env
/srv/hermes-dev/data/.env

# Backup encrypted
gpg -c /srv/hermes-life/data/.env -o /root/backups/hermes-life-env.gpg

# Never commit to git
echo "*.env" >> /root/agent-control-room/.gitignore
```

### Agent Credential Scope

```text
❌ BAD: Orchestrator has all API keys
✅ GOOD: Each specialist has only its scoped keys

hermes-seo:
  - AHREFS_API_KEY
  - GOOGLE_SEARCH_CONSOLE_KEY

hermes-dev:
  - GITHUB_TOKEN
  - DEPLOY_KEY

hermes-orchestrator:
  - ANTHROPIC_API_KEY (for LLM)
  - NO access to specialist service APIs
```

### Port Security

```bash
# Check exposed ports
ss -tulpn | grep LISTEN

# Use firewall for non-orchestrator agents
ufw allow 3100/tcp  # orchestrator only
ufw deny 3001/tcp   # hermes-seo (internal only)
ufw deny 3002/tcp   # hermes-dev (internal only)
```

## Bundled Skills

The repo includes agent skills for VPS and control room management:

| Skill | Purpose |
|-------|---------|
| `create-vps` | Create Hetzner VPS, SSH key, SSH alias |
| `setup-control-room` | Bootstrap VPS with Node, Docker, Hermes, Control Room |
| `agent-control-room` | Manage Control Room docs and agent folders |
| `agent-task-router` | Route tasks from orchestrator to specialists |
| `agent-registry-manager` | Maintain agent registry |
| `agent-backup-manager` | Design and audit per-agent backups |
| `agent-security-auditor` | Check ports, dashboards, SSH, Docker, secrets |
| `agent-team-cron-planner` | Plan recurring multi-agent workflows |

After running `setup-control-room`, skills are linked to `~/.claude/skills/`.

## Common Commands

### Manage Control Room

```bash
# Update Control Room repo
cd /root/agent-control-room
git pull

# Register new agent
mkdir -p agents/hermes-newagent
cp templates/agent/*.md agents/hermes-newagent/

# List all agents
ls agents/

# View agent inventory
cat agents/hermes-seo/inventory.md
```

### Manage Agents

```bash
# Start agent
cd /srv/hermes-seo
docker-compose up -d

# View logs
docker-compose logs -f

# Restart agent
docker-compose restart

# Stop agent
docker-compose down
```

### Task Bus Operations

```bash
# Create task for specialist
cat > /srv/agent-bus/inbox/seo/task-003.md <<EOF
---
task_id: task-003
specialist: seo
created: $(date -Iseconds)
requestor: manual
---
# Task: Run SEO audit for newsite.com
EOF

# Check task status
ls /srv/agent-bus/working/seo/
ls /srv/agent-bus/outbox/seo/

# Archive completed tasks
mv /srv/agent-bus/outbox/seo/* /srv/agent-bus/archive/seo/
```

## Troubleshooting

### Agent Won't Start

```bash
# Check Docker logs
docker-compose logs --tail=50

# Verify .env exists
ls -la /srv/<agent-name>/data/.env

# Check port conflicts
ss -tulpn | grep <port>

# Restart Docker
systemctl restart docker
docker-compose up -d
```

### Orchestrator Can't Find Specialists

```bash
# Verify task bus directories exist
ls -la /srv/agent-bus/inbox/

# Check permissions
chmod -R 755 /srv/agent-bus

# Verify agents.yaml
cat /srv/agent-bus/agents.yaml
```

### Secret Not Found

```bash
# Check .env file
cat /srv/<agent-name>/data/.env | grep API_KEY

# Restore from backup
gpg -d /root/backups/<agent-name>-env.gpg > /srv/<agent-name>/data/.env

# Restart agent
cd /srv/<agent-name>
docker-compose restart
```

### Task Not Being Picked Up

```bash
# Check task format
cat /srv/agent-bus/inbox/<specialist>/task-*.md

# Verify specialist is running
docker ps | grep hermes-<specialist>

# Check specialist logs
cd /srv/hermes-<specialist>
docker-compose logs --tail=100
```

## Recommended First Milestone

Do not build a full team immediately. Start with:

1. Control Room exists on VPS: `/root/agent-control-room`
2. One agent documented: `agents/hermes-life/`
3. No raw secrets in repo
4. Can restart/debug agent using runbook

Then expand to Level 2 (direct specialists), Level 3 (orchestrator), Level 4 (automation).

## Environment Variables

Reference environment variables in agent configs:

```yaml
# docker-compose.yml
environment:
  - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
  - GITHUB_TOKEN=${GITHUB_TOKEN}
  - DATABASE_URL=${DATABASE_URL}
```

Store actual values in `/srv/<agent-name>/data/.env`:

```bash
ANTHROPIC_API_KEY=sk-ant-...
GITHUB_TOKEN=ghp_...
DATABASE_URL=postgresql://...
```

## Access Paths

You have multiple ways to interact with agents:

**Control Path**: Edit Control Room docs directly
```bash
vim /root/agent-control-room/agents/hermes-seo/runbook.md
```

**Direct Path**: Talk directly to specialist agents
```bash
curl http://localhost:3001  # hermes-seo
curl http://localhost:3002  # hermes-dev
```

**Orchestrated Path**: Use orchestrator as front door
```bash
curl http://localhost:3100 -d "Audit SEO for example.com"
# Orchestrator → Task Bus → Specialist → Result → Orchestrator → You
```

## Resources

- **GitHub**: https://github.com/shannhk/hermes-agent-control-room
- **License**: MIT
- **Topics**: agent-control-room, ai-agents, hermes-agent, multi-agent, vps
