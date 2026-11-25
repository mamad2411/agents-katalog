---
name: awesome-openclaw-usecases-discovery
description: Discover and implement real-world OpenClaw use cases from a curated community collection covering productivity, automation, content creation, and infrastructure.
triggers:
  - "show me openclaw use cases"
  - "what can I do with openclaw"
  - "openclaw automation ideas"
  - "how are people using openclaw"
  - "openclaw productivity workflows"
  - "give me openclaw project examples"
  - "openclaw use case for social media"
  - "best openclaw automation patterns"
---

# awesome-openclaw-usecases-discovery

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill enables AI agents to discover, recommend, and help implement real-world use cases from the awesome-openclaw-usecases repository — a community-curated collection of 42+ production-tested OpenClaw automations across social media, creative workflows, DevOps, productivity, research, and finance.

## What It Covers

The awesome-openclaw-usecases repository organizes battle-tested OpenClaw implementations into categories:

- **Social Media**: Reddit/YouTube digests, X automation, multi-source news aggregation
- **Creative & Building**: Autonomous task generation, content pipelines, game dev automation
- **Infrastructure & DevOps**: n8n orchestration, self-healing servers
- **Productivity**: Project management, multi-channel customer service, CRM, health tracking
- **Research & Learning**: Knowledge bases, paper readers, semantic search
- **Finance & Trading**: Prediction market automation

Each use case includes detailed implementation guides, skill requirements, and real-world patterns.

## Installation

This is a reference repository, not a package. Access it via:

```bash
# Clone the repository
git clone https://github.com/hesamsheikh/awesome-openclaw-usecases.git
cd awesome-openclaw-usecases

# Browse use cases
ls usecases/
```

Or view online at: https://github.com/hesamsheikh/awesome-openclaw-usecases

## Repository Structure

```
awesome-openclaw-usecases/
├── usecases/
│   ├── daily-reddit-digest.md
│   ├── youtube-content-pipeline.md
│   ├── n8n-workflow-orchestration.md
│   ├── autonomous-project-management.md
│   ├── semantic-memory-search.md
│   └── ... (42+ use cases)
├── CONTRIBUTING.md
└── README.md
```

Each use case follows a standard format:
- **Overview**: What it does and why
- **Skills Required**: OpenClaw plugins/skills needed
- **Implementation**: Step-by-step setup
- **Configuration**: Environment variables, API keys
- **Examples**: Real prompts and outputs
- **Tips & Troubleshooting**: Common issues

## Key Use Case Categories

### Social Media Automation

```markdown
# Daily Reddit Digest
Summarize curated subreddits based on preferences
Skills: reddit-skill, summarization

# X/Twitter Automation
Post, reply, like, DM, search via TweetClaw plugin
Skills: tweetclaw-plugin, scheduling

# Multi-Source Tech News
Aggregate from 109+ sources (RSS, X, GitHub, web)
Skills: rss-reader, web-search, content-scoring
```

### Creative Workflows

```markdown
# Goal-Driven Autonomous Tasks
Brain dump → auto-generate tasks → build mini-apps overnight
Skills: task-generation, autonomous-execution, git-integration

# YouTube Content Pipeline
Automate idea scouting, research, tracking
Skills: youtube-api, notion-integration, scheduling

# Multi-Agent Content Factory
Research + writing + thumbnail agents in Discord
Skills: multi-agent, discord-integration, image-generation
```

### Infrastructure & DevOps

```markdown
# n8n Workflow Orchestration
Delegate API calls to n8n via webhooks (agent never touches creds)
Skills: webhook-trigger, n8n-integration

# Self-Healing Home Server
Always-on infra agent with SSH, cron, self-healing
Skills: ssh-access, cron-management, monitoring
```

### Productivity

```markdown
# Autonomous Project Management
Multi-agent coordination using STATE.yaml pattern
Skills: state-management, multi-agent, file-system

# Multi-Channel Customer Service
Unified inbox: WhatsApp, Instagram, Email, Google Reviews
Skills: whatsapp-api, instagram-api, email-integration

# Personal CRM
Auto-discover contacts from email/calendar + NL queries
Skills: email-parsing, calendar-integration, database
```

### Research & Learning

```markdown
# Personal Knowledge Base (RAG)
Drop URLs/tweets/articles → searchable knowledge base
Skills: rag, vector-search, content-extraction

# arXiv Paper Reader
Fetch, analyze, compare papers conversationally
Skills: arxiv-api, pdf-parsing, summarization

# Semantic Memory Search
Vector-powered search over markdown memory files
Skills: embeddings, hybrid-retrieval, file-watching
```

## Common Implementation Patterns

### Pattern 1: Scheduled Digest

```yaml
# Daily Reddit Digest implementation
schedule: "0 8 * * *"  # Every day at 8 AM
skills:
  - reddit-skill
  - summarization
  - notification

workflow:
  1. Fetch top posts from configured subreddits
  2. Filter by upvotes/engagement threshold
  3. Summarize using LLM
  4. Format digest
  5. Send via Telegram/Email/Discord
```

### Pattern 2: Multi-Agent Coordination

```yaml
# Content Factory pattern
agents:
  - name: researcher
    channel: "#research"
    skills: [web-search, note-taking]
  
  - name: writer
    channel: "#writing"
    skills: [content-generation, editing]
  
  - name: designer
    channel: "#design"
    skills: [image-generation, thumbnail-creation]

coordination:
  type: state-file  # STATE.yaml
  handoff: automatic
```

### Pattern 3: Webhook Orchestration

```javascript
// n8n Workflow Orchestration pattern
// Agent sends request to n8n webhook
const triggerN8nWorkflow = async (workflowName, payload) => {
  const webhookUrl = process.env.N8N_WEBHOOK_BASE + workflowName;
  
  const response = await fetch(webhookUrl, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  });
  
  return response.json();
};

// Agent never touches API credentials
// All integrations managed visually in n8n
```

### Pattern 4: RAG Knowledge Base

```python
# Personal Knowledge Base pattern
from openclaw_skills import rag_skill

# Add content to knowledge base
rag_skill.add_document(
    content=article_text,
    metadata={
        "source": "https://example.com/article",
        "date": "2026-05-16",
        "tags": ["ai", "research"]
    }
)

# Query conversationally
results = rag_skill.search(
    query="What did I save about RAG implementations?",
    top_k=5
)
```

### Pattern 5: State Management (Multi-Agent)

```yaml
# STATE.yaml pattern for autonomous coordination
project: youtube-content-pipeline
state: research

completed:
  - idea-scouting
  - keyword-research

current_task:
  agent: researcher
  action: competitor-analysis
  started_at: 2026-05-16T10:30:00Z

next_tasks:
  - script-outline (writer)
  - thumbnail-concepts (designer)

context:
  channel: tech-tutorials
  target_keywords: ["AI agents", "automation"]
  deadline: 2026-05-20
```

## Accessing Use Case Details

```bash
# Read a specific use case
cat usecases/daily-reddit-digest.md

# Search for keywords
grep -r "telegram" usecases/

# List all use cases by category
grep "^|" README.md | grep -A 1 "Social Media"
```

## Configuration Examples

### Environment Variables (Common Across Use Cases)

```bash
# Social Media
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
TWITTER_API_KEY=your_twitter_key
YOUTUBE_API_KEY=your_youtube_key

# Communication
TELEGRAM_BOT_TOKEN=your_telegram_token
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token

# Infrastructure
N8N_WEBHOOK_BASE=https://n8n.yourdomain.com/webhook/
SSH_PRIVATE_KEY_PATH=/path/to/ssh/key

# AI/LLM
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key

# Databases
POSTGRES_URL=postgresql://user:pass@localhost/db
VECTOR_DB_URL=http://localhost:6333  # Qdrant/Weaviate/etc
```

### Skill Requirements Mapping

```markdown
# Example: Daily Reddit Digest
Required Skills:
- reddit-skill (community or custom)
- summarization (built-in LLM)
- notification (telegram/discord/email)

Installation:
openclaw install reddit-skill
openclaw install notification-skill

# Example: Autonomous Project Management
Required Skills:
- state-management (file-system based)
- multi-agent (orchestration)
- git-integration (commits, PRs)

Installation:
openclaw install state-management-skill
openclaw install git-skill
```

## Real-World Implementation Example

```python
# Implementing "Custom Morning Brief" use case
# usecases/custom-morning-brief.md

import os
from datetime import datetime
from openclaw_skills import calendar, todoist, news_api, llm, notification

async def generate_morning_brief():
    """
    Aggregate daily briefing from multiple sources
    """
    # Fetch calendar events
    events = await calendar.get_today_events()
    
    # Fetch tasks
    tasks = await todoist.get_today_tasks()
    
    # Fetch news
    news = await news_api.get_top_headlines(
        topics=["AI", "technology", "startups"]
    )
    
    # Generate briefing
    briefing = await llm.generate({
        "prompt": f"""
        Create a concise morning briefing:
        
        Calendar: {events}
        Tasks: {tasks}
        News: {news}
        
        Include:
        - Today's schedule highlights
        - Top 3 priority tasks
        - 2-3 relevant news items
        - AI-recommended actions
        
        Keep it under 300 words, friendly tone.
        """
    })
    
    # Send via SMS/Telegram
    await notification.send(
        channel="sms",
        recipient=os.getenv("PHONE_NUMBER"),
        message=briefing
    )
    
    return briefing

# Schedule: Every day at 7 AM
# openclaw schedule add "0 7 * * *" generate_morning_brief
```

## Discovering Use Cases via Natural Language

When a user asks "show me openclaw use cases for X", reference this mapping:

```python
# Intent → Use Case Category mapping
category_mapping = {
    "social media": ["daily-reddit-digest", "x-twitter-automation", "multi-source-tech-news"],
    "content creation": ["youtube-content-pipeline", "content-factory", "podcast-production"],
    "productivity": ["custom-morning-brief", "todoist-task-manager", "personal-crm"],
    "automation": ["n8n-workflow-orchestration", "self-healing-home-server"],
    "research": ["knowledge-base-rag", "arxiv-paper-reader", "semantic-memory-search"],
    "devops": ["n8n-workflow-orchestration", "self-healing-home-server"],
    "customer service": ["multi-channel-customer-service"],
    "health": ["health-symptom-tracker"],
    "finance": ["polymarket-autopilot", "earnings-tracker"]
}

# Example agent response
def recommend_use_case(user_intent):
    """
    User: "I want to automate my morning routine"
    Agent: Recommends custom-morning-brief, family-calendar-household-assistant
    """
    pass
```

## Troubleshooting Common Issues

### Issue: Use Case References Missing Skills

```bash
# Check if skill exists in OpenClaw ecosystem
openclaw search reddit-skill

# If not found, check use case documentation for custom skill link
# Many use cases link to community GitHub repos
```

### Issue: API Rate Limits

```python
# Most use cases should implement rate limiting
import time
from functools import wraps

def rate_limit(calls_per_minute=10):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait_time = min_interval - elapsed
            if wait_time > 0:
                time.sleep(wait_time)
            result = await func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
```

### Issue: Security Concerns

```markdown
⚠️ SECURITY WARNING from repository README:

> OpenClaw skills and third-party dependencies may have critical 
> security vulnerabilities. Many use cases link to community-built 
> skills that have NOT been audited.

Best Practices:
1. Review all skill source code before installation
2. Use environment variables for credentials (never hardcode)
3. Limit agent permissions (no sudo, restricted file access)
4. Audit third-party skills regularly
5. Use webhook patterns (n8n) to isolate credentials
```

### Issue: Multi-Agent Coordination Failures

```yaml
# Use STATE.yaml pattern from autonomous-project-management
# Each agent checks state file before acting

state_file: STATE.yaml
lock_file: STATE.lock

read_state:
  1. Acquire lock
  2. Read STATE.yaml
  3. Check current_task.agent == self.name
  4. Release lock

write_state:
  1. Acquire lock
  2. Update STATE.yaml
  3. Commit changes
  4. Release lock
  5. Notify next agent (optional)
```

## Contributing New Use Cases

```markdown
# From CONTRIBUTING.md

Requirements:
1. Must be production-tested (at least 1 day)
2. Include real implementation details
3. List all required skills/dependencies
4. Provide configuration examples
5. No crypto-related use cases

Template:
usecases/your-use-case.md

---
# Use Case Title

## Overview
What it does and why

## Skills Required
- skill-name-1
- skill-name-2

## Implementation
Step-by-step setup

## Configuration
Environment variables, API keys

## Example Prompts
Real user interactions

## Tips & Troubleshooting
Common issues
---
```

## Integration with Other Tools

```bash
# n8n Workflow Orchestration
# Use case: usecases/n8n-workflow-orchestration.md
# Benefit: Agent never touches credentials

# AIONui Desktop Cowork
# Use case: usecases/aionui-cowork-desktop.md
# Benefit: Multi-agent unified UI

# DenchClaw Local CRM
# Use case: usecases/local-crm-framework.md
npx denchclaw
# Benefit: Fully local CRM with browser automation
```

## Quick Reference: Top 10 Use Cases by Popularity

Based on repository structure (ordered by category appearance):

1. **Daily Reddit Digest** - Automated subreddit summaries
2. **YouTube Content Pipeline** - End-to-end video production automation
3. **n8n Workflow Orchestration** - Credential-free API delegation
4. **Autonomous Project Management** - STATE.yaml multi-agent coordination
5. **Multi-Channel Customer Service** - Unified AI inbox
6. **Custom Morning Brief** - Personalized daily briefing via SMS
7. **Personal Knowledge Base (RAG)** - Conversational document search
8. **Self-Healing Home Server** - Always-on infrastructure agent
9. **X/Twitter Automation** - Full social media automation via TweetClaw
10. **arXiv Paper Reader** - Conversational research paper analysis

## Links & Resources

- Repository: https://github.com/hesamsheikh/awesome-openclaw-usecases
- OpenClaw: https://github.com/openclaw/openclaw
- Discord: https://discord.gg/vtJykN3t
- Author: [@Hesamation](https://x.com/Hesamation)

## Agent Usage Recommendations

When helping users implement use cases:

1. **Ask about their goals first** - Match use case to actual need
2. **Check skill availability** - Verify required skills exist or link to custom implementations
3. **Warn about security** - Reference repository security disclaimer
4. **Provide real examples** - Use code from this skill, not placeholders
5. **Suggest combinations** - Many use cases work well together (e.g., morning brief + personal CRM)
6. **Start simple** - Recommend single-agent use cases before multi-agent orchestration
