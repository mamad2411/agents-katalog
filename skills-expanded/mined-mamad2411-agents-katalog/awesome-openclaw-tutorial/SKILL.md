---
name: awesome-openclaw-tutorial
description: OpenClaw AI工作助手完整中文教程 - 安装配置、Skills扩展、自动化工作流和实战案例
triggers:
  - how do I install and configure OpenClaw
  - show me OpenClaw skills and automation examples
  - help me set up OpenClaw with custom models
  - how to use OpenClaw for file management and knowledge base
  - OpenClaw integration with Feishu Slack or WeChat
  - troubleshoot OpenClaw gateway or API connection issues
  - OpenClaw Task Flow and webhooks configuration
  - create OpenClaw workflows for productivity automation
---

# awesome-openclaw-tutorial

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Complete Chinese tutorial for OpenClaw - an AI-powered work assistant. Covers installation, configuration, Skills ecosystem, automation workflows, API integration, and practical use cases for solo entrepreneurs and teams.

## What is OpenClaw?

OpenClaw is an AI assistant framework that runs locally or in cloud, providing:
- File management, knowledge base, and scheduling automation
- 1800+ Skills for extending capabilities
- Multi-platform integration (Feishu, Slack, WeChat, DingTalk, QQ)
- Task automation with cron, Task Flow, and webhooks
- Media generation (images, video, audio, TTS) via `openclaw infer`
- Active Memory and Memory Wiki for context retention

**Current stable version**: v2026.4.14  
**Recommended runtime**: Node 24 (minimum Node 22.16+)

## Quick Installation

### Method 1: One-Click Deployment (Recommended for Beginners)

**Feishu Miaoda** (Free, 1M tokens/day):
```bash
# Visit https://awesome.tryopenclaw.asia/
# Click "Feishu Miaoda" deployment
# Complete in 1 minute, no server needed
```

**Baota Panel** (Free plugin, visual management):
```bash
# Install Baota Panel first
# Add "OpenClaw" plugin from marketplace
# One-click install and configure
```

### Method 2: Standard Installation

```bash
# Install via npm (Node 22.16+ required)
npm install -g openclaw

# Or via yarn
yarn global add openclaw

# Initialize and onboard
openclaw onboard

# Start gateway
openclaw gateway start
```

### Method 3: Docker

```bash
# Pull latest image
docker pull openclaw/openclaw:latest

# Run with environment variables
docker run -d \
  -e OPENCLAW_TZ=Asia/Shanghai \
  -e OPENCLAW_API_KEY=$OPENCLAW_API_KEY \
  -p 3000:3000 \
  -v ~/.openclaw:/root/.openclaw \
  openclaw/openclaw:latest

# Check status
docker ps
```

## Configuration

### Model Authentication (2026.4+ Standard)

```bash
# Login to model providers (replaces old local-* skills)
openclaw models auth login --provider anthropic
openclaw models auth login --provider openai
openclaw models auth login --provider gemini

# List authenticated providers
openclaw models auth list

# Set default model
openclaw config set model.default "claude-3-5-sonnet-20241022"

# Enable fast mode (cheaper, faster for OpenAI/Anthropic)
# User says: /fast
```

### Gateway Authentication (Required since v2026.3.7)

```bash
# Set authentication mode (token or password)
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "${OPENCLAW_GATEWAY_TOKEN}"

# Restart gateway
openclaw gateway restart
```

### Tools Profile (Fix "AI can't do anything" issue)

```bash
# Set to 'full' for complete toolset including command execution
openclaw config set tools.profile full

# Profile options:
# - messaging: only chat and session management
# - default: standard tools (no command exec)
# - coding: programming tools
# - full: complete toolset (RECOMMENDED)
# - all: everything enabled

openclaw gateway restart
```

### Active Memory and Memory Wiki (2026.4+ Mainline)

```bash
# Enable Active Memory (retrieves context before replies)
openclaw config set memory.active.enabled true

# Enable Dreaming (background memory consolidation)
openclaw config set memory.dreaming.enabled true

# Enable Memory Wiki (structured knowledge claims)
openclaw config set memory.wiki.enabled true

# Configure memory retention
openclaw config set memory.retention.days 90
```

## Key Commands

### Core CLI

```bash
# Check version
openclaw --version

# Show current config
openclaw config list

# Set config value
openclaw config set <key> <value>

# Gateway control
openclaw gateway start
openclaw gateway stop
openclaw gateway restart
openclaw gateway status

# Model inference (unified interface)
openclaw infer text "Explain quantum computing"
openclaw infer image "A red panda in space" --model dall-e-3
openclaw infer video "Ocean waves" --provider runway
openclaw infer audio "Calm piano music" --provider suno
openclaw infer tts "Hello world" --voice nova
openclaw infer web "https://example.com"
openclaw infer embedding "Document text to embed"

# Skills management (DEPRECATED in 2026.4+, use models auth instead)
# clawhub search <query>
# clawhub info <skill-name>
# clawhub install <skill-name>
```

### Task Automation

```bash
# Create cron task (scheduled)
openclaw tasks create \
  --name "daily-summary" \
  --schedule "0 18 * * *" \
  --command "Generate daily summary and send to Feishu"

# Create Task Flow (persistent workflow)
openclaw tasks flow create \
  --name "content-pipeline" \
  --trigger webhook \
  --steps "research,write,review,publish"

# List tasks
openclaw tasks list

# Create webhook endpoint
openclaw webhooks create \
  --name "github-pr-review" \
  --url "/webhooks/github" \
  --action "Review PR and comment"

# List webhooks
openclaw webhooks list
```

## Real Code Examples

### Example 1: File Management Automation (Shell)

```bash
#!/bin/bash
# Auto-organize downloads folder

# User prompt to OpenClaw:
# "Organize my Downloads folder: move images to Images/, 
#  PDFs to Documents/, and delete files older than 30 days"

# OpenClaw executes internally via file management tools
# No manual scripting needed - AI handles the logic

# For custom automation, use Task Flow:
openclaw tasks flow create \
  --name "organize-downloads" \
  --schedule "0 2 * * *" \
  --steps "scan_downloads,categorize_files,move_files,cleanup_old"
```

### Example 2: Knowledge Base Integration (JavaScript/Node)

```javascript
// Add document to knowledge base
const { OpenClawClient } = require('openclaw-sdk');

const client = new OpenClawClient({
  apiKey: process.env.OPENCLAW_API_KEY,
  baseUrl: 'http://localhost:3000'
});

async function addToKnowledgeBase(filePath, metadata) {
  try {
    const result = await client.knowledge.add({
      file: filePath,
      metadata: {
        tags: metadata.tags,
        source: metadata.source,
        category: metadata.category
      },
      activeMemory: true, // Enable Active Memory indexing
      memoryWiki: true    // Add to Memory Wiki
    });
    
    console.log('Document added:', result.id);
    return result;
  } catch (error) {
    console.error('Failed to add document:', error.message);
    throw error;
  }
}

// Query knowledge base
async function searchKnowledge(query) {
  const results = await client.knowledge.search({
    query: query,
    limit: 10,
    useActiveMemory: true, // Include Active Memory context
    useMemoryWiki: true    // Include Memory Wiki claims
  });
  
  return results;
}

// Example usage
addToKnowledgeBase('./report.pdf', {
  tags: ['quarterly', 'finance'],
  source: 'internal',
  category: 'reports'
});

searchKnowledge('Q4 revenue analysis').then(results => {
  console.log('Found:', results.length, 'documents');
});
```

### Example 3: Feishu Bot Integration (JavaScript)

```javascript
// Feishu bot webhook handler
const express = require('express');
const app = express();

app.post('/feishu/webhook', async (req, res) => {
  const event = req.body;
  
  if (event.type === 'message') {
    const userMessage = event.message.content;
    
    // Send to OpenClaw for processing
    const response = await fetch('http://localhost:3000/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.OPENCLAW_API_KEY}`
      },
      body: JSON.stringify({
        message: userMessage,
        sessionId: event.message.chat_id,
        platform: 'feishu',
        useActiveMemory: true // Retrieve relevant context
      })
    });
    
    const result = await response.json();
    
    // Send response back to Feishu
    await sendFeishuMessage(event.message.chat_id, result.reply);
  }
  
  res.json({ success: true });
});

app.listen(3000);
```

### Example 4: Media Generation Workflow (Shell)

```bash
#!/bin/bash
# Generate content pipeline: text -> image -> video

# Step 1: Generate article
ARTICLE=$(openclaw infer text "Write a 500-word article about sustainable energy" \
  --model gpt-4-turbo)

# Step 2: Generate cover image
openclaw infer image "Sustainable energy concept art, vibrant, professional" \
  --model dall-e-3 \
  --size 1792x1024 \
  --output cover.png

# Step 3: Generate promotional video
openclaw infer video "Solar panels in a green field, golden hour" \
  --provider runway \
  --duration 5 \
  --output promo.mp4

# Step 4: Generate background music
openclaw infer audio "Uplifting corporate background music" \
  --provider suno \
  --duration 30 \
  --output bgm.mp3

# Step 5: Combine and publish
echo "Content pipeline complete!"
ls -lh cover.png promo.mp4 bgm.mp3
```

### Example 5: Task Flow with Webhooks (YAML)

```yaml
# ~/.openclaw/flows/content-approval.yaml
name: content-approval-flow
trigger:
  type: webhook
  path: /webhooks/content-submit
  
steps:
  - name: review-content
    action: infer
    input: "Review the submitted content for quality and compliance"
    model: claude-3-5-sonnet-20241022
    
  - name: check-approval
    action: conditional
    condition: "review.score > 8"
    
  - name: publish
    action: webhook
    url: https://cms.example.com/publish
    method: POST
    headers:
      Authorization: "Bearer ${CMS_API_KEY}"
    body:
      content: "{{ steps.review.content }}"
      status: approved
      
  - name: notify
    action: send-message
    platform: feishu
    channel: "${FEISHU_CHANNEL_ID}"
    message: "Content published: {{ steps.publish.url }}"
```

Load flow:
```bash
openclaw tasks flow load ~/.openclaw/flows/content-approval.yaml
openclaw tasks flow start content-approval-flow
```

## Common Patterns

### Pattern 1: Daily Automation Routine

```bash
# Create morning briefing task
openclaw tasks create \
  --name "morning-briefing" \
  --schedule "0 8 * * *" \
  --command "Generate morning briefing: check emails, calendar, news, weather. Send to Feishu."

# Create evening summary task
openclaw tasks create \
  --name "evening-summary" \
  --schedule "0 18 * * *" \
  --command "Summarize today's work: meetings attended, tasks completed, files created. Archive to knowledge base."
```

### Pattern 2: Multi-Platform Sync

```javascript
// Sync message across platforms
async function syncMessage(message, platforms) {
  const results = await Promise.all(
    platforms.map(platform => 
      client.messaging.send({
        platform: platform,
        channelId: process.env[`${platform.toUpperCase()}_CHANNEL_ID`],
        message: message,
        useActiveMemory: true
      })
    )
  );
  
  return results;
}

// Usage
syncMessage('Deployment complete for v2.0', ['feishu', 'slack', 'wechat']);
```

### Pattern 3: Knowledge Base -> Memory Wiki Pipeline

```bash
# User uploads document
openclaw knowledge add ./research-paper.pdf \
  --tags "AI,research" \
  --auto-extract-claims

# OpenClaw automatically:
# 1. Extracts text content
# 2. Creates Memory Wiki claims with evidence
# 3. Indexes for Active Memory retrieval
# 4. Checks for contradictions with existing claims

# Query across knowledge base and memory
openclaw infer text "What are the latest findings on transformer models?" \
  --use-active-memory \
  --use-memory-wiki
```

## Troubleshooting

### Gateway Won't Start (2026.3.7+)

**Symptom**: `Error: gateway.auth.mode must be set`

**Fix**:
```bash
openclaw config set gateway.auth.mode token
openclaw config set gateway.auth.token "$(openssl rand -hex 32)"
openclaw gateway restart
```

### AI Only Chats, Can't Execute Commands (2026.3.2+)

**Symptom**: OpenClaw responds to questions but won't manage files or run commands

**Fix**:
```bash
# Check current profile
openclaw config get tools.profile

# Set to 'full' for complete toolset
openclaw config set tools.profile full
openclaw gateway restart
```

### Model Authentication Errors

**Symptom**: `Model provider not authenticated`

**Fix**:
```bash
# Re-authenticate (2026.4+ method)
openclaw models auth login --provider openai
openclaw models auth login --provider anthropic

# Verify
openclaw models auth list

# Set default
openclaw config set model.default "claude-3-5-sonnet-20241022"
```

### High API Costs

**Solutions**:
```bash
# 1. Enable fast mode for OpenAI/Anthropic (cheaper)
openclaw config set model.fast_mode true

# 2. Use local models with Ollama
openclaw models auth login --provider ollama
openclaw config set model.default "llama3:70b"

# 3. Set token limits
openclaw config set model.max_tokens 4000

# 4. Use Chinese domestic models (95% cost savings)
openclaw models auth login --provider deepseek
openclaw config set model.default "deepseek-chat"
```

### Active Memory Not Working

**Symptom**: AI doesn't recall previous context

**Fix**:
```bash
# Enable Active Memory
openclaw config set memory.active.enabled true
openclaw config set memory.dreaming.enabled true

# Force memory refresh
openclaw memory rebuild

# Check memory stats
openclaw memory stats

# Restart gateway
openclaw gateway restart
```

### Task Flow Execution Failures

**Symptom**: Workflows stuck or fail silently

**Debug**:
```bash
# Check task logs
openclaw tasks logs <task-name>

# Validate flow definition
openclaw tasks flow validate ~/.openclaw/flows/my-flow.yaml

# Test individual steps
openclaw tasks flow test my-flow --step review-content

# Enable debug mode
openclaw config set debug.tasks true
openclaw gateway restart
```

### ComfyUI Integration Issues

**Symptom**: `infer image` fails with ComfyUI backend

**Fix**:
```bash
# Install ComfyUI skill (if using pre-2026.4 setup)
# Note: In 2026.4+, use built-in infer command instead

# Verify ComfyUI is running
curl http://localhost:8188/system_stats

# Set ComfyUI endpoint
openclaw config set comfyui.endpoint "http://localhost:8188"

# Test connection
openclaw infer image "test" --provider comfyui
```

### Windows Specific Issues

**Symptom**: Black console window pops up on gateway restart

**Fix**: Upgrade to v2026.3.13+ which fixes this issue

```powershell
# Update OpenClaw
npm update -g openclaw

# Verify version
openclaw --version  # Should be >= v2026.3.13
```

## Configuration Reference

Key config paths in `~/.openclaw/config.json`:

```json
{
  "model": {
    "default": "claude-3-5-sonnet-20241022",
    "fast_mode": true,
    "max_tokens": 4000
  },
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "${OPENCLAW_GATEWAY_TOKEN}"
    },
    "port": 3000
  },
  "tools": {
    "profile": "full"
  },
  "memory": {
    "active": {
      "enabled": true
    },
    "dreaming": {
      "enabled": true,
      "schedule": "0 3 * * *"
    },
    "wiki": {
      "enabled": true
    },
    "retention": {
      "days": 90
    }
  },
  "platforms": {
    "feishu": {
      "app_id": "${FEISHU_APP_ID}",
      "app_secret": "${FEISHU_APP_SECRET}"
    },
    "slack": {
      "bot_token": "${SLACK_BOT_TOKEN}"
    }
  }
}
```

## Resources

- **Official Tutorial**: https://awesome.tryopenclaw.asia/
- **GitHub Repo**: https://github.com/xianyu110/awesome-openclaw-tutorial
- **Skills Marketplace**: Search via `openclaw models auth` (2026.4+) or legacy `clawhub search`
- **Quick Start Guide**: [Chapter 3 - Quick Start](docs/01-basics/03-quick-start.md)
- **API Integration**: [Chapter 10 - API & External Capabilities](docs/03-advanced/10-api-integration.md)
- **Task Flow Guide**: [Chapter 13 - Advanced Automation](docs/04-practical-cases/13-advanced-automation.md)

**Important**: This tutorial tracks v2026.4.14 stable. Some legacy content (old skill names, deprecated commands) remains for reference. Always verify against current `openclaw --version` and official docs.
