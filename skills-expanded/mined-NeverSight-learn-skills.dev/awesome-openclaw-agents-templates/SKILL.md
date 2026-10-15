---
name: awesome-openclaw-agents-templates
description: Access and use 200+ production-ready AI agent templates for OpenClaw with SOUL.md configs across 24 categories
triggers:
  - "show me openclaw agent templates"
  - "how do I create a SOUL.md file"
  - "find an agent template for [task]"
  - "what openclaw agents are available"
  - "help me set up an openclaw agent"
  - "configure a productivity agent"
  - "deploy an openclaw agent template"
  - "what's in the awesome-openclaw-agents collection"
---

# Awesome OpenClaw Agents Templates

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill provides access to **205+ production-ready AI agent templates** from the awesome-openclaw-agents repository. Each template is a copy-paste ready `SOUL.md` configuration file that defines an AI agent's personality, skills, and behavior for the OpenClaw ecosystem.

## What This Collection Provides

The awesome-openclaw-agents repository offers:
- **205 agent templates** across 24 categories (Productivity, Development, Marketing, Business, DevOps, Finance, etc.)
- **Copy-paste SOUL.md files** that define agent behavior
- **Pre-configured integrations** with popular tools (Slack, GitHub, Notion, etc.)
- **Quick deployment patterns** using Node.js, Docker, or CrewClaw
- **Real-world use cases** for each agent type

## Installation & Setup

### Quick Start with Any Template

```bash
# Clone the repository
git clone https://github.com/mergisi/awesome-openclaw-agents.git
cd awesome-openclaw-agents/quickstart

# Install dependencies
npm install

# Copy a template (example: Orion project manager)
cp ../agents/productivity/orion/SOUL.md ./SOUL.md

# Run the agent
node bot.js
```

### Using with OpenClaw CLI

```bash
# Register an agent from a SOUL.md file
openclaw agents add --from ./agents/productivity/orion/SOUL.md

# Start the OpenClaw gateway
openclaw gateway start

# List registered agents
openclaw agents list
```

## SOUL.md Configuration Format

Every agent template is a `SOUL.md` file with this structure:

```markdown
# Agent Name

## Core Identity
- Role: [Primary function]
- Tone: [Communication style]
- Goal: [Main objective]

## Capabilities
- [Skill 1]
- [Skill 2]
- [Skill 3]

## Integrations
- Tool: [Service name]
  Config: [Configuration details]

## Behavior Patterns
- When [condition]: [action]
- Trigger: [event] → Response: [behavior]

## Memory
- Track: [what to remember]
- Forget: [what to discard]
```

## Key Agent Categories

### Productivity Agents

```javascript
// Example: Setting up the Orion project manager agent
const fs = require('fs');
const path = require('path');

// Copy Orion template
const orionSOUL = fs.readFileSync(
  path.join(__dirname, 'agents/productivity/orion/SOUL.md'),
  'utf8'
);

// Save to your project
fs.writeFileSync('./SOUL.md', orionSOUL);

// Use cases for Orion:
// - Daily task prioritization
// - Deadline tracking
// - Team alignment
// - Project status updates
```

### Development Agents

```javascript
// Example: Code reviewer (Lens) setup
const lensConfig = {
  agent: 'lens',
  role: 'PR review, security scanning, code quality',
  triggers: ['pr opened', 'pr updated'],
  integrations: {
    github: {
      token: process.env.GITHUB_TOKEN,
      webhooks: ['pull_request']
    }
  }
};

// Load template
const lensSOUL = fs.readFileSync(
  './agents/development/code-reviewer/SOUL.md',
  'utf8'
);

// Configure for your repo
const customSOUL = lensSOUL.replace(
  '{{REPO}}',
  process.env.GITHUB_REPO
);
```

### Marketing Agents

```javascript
// Example: Content writer (Echo) agent
const echoTemplate = `
# Echo - Content Writer Agent

## Core Identity
- Role: Blog post generation, SEO optimization
- Tone: Professional, engaging, clear
- Goal: Create high-quality content that ranks

## Capabilities
- Generate blog posts from topics
- Optimize for target keywords
- Create meta descriptions
- Suggest internal linking

## Integrations
- Tool: OpenAI API
  Config: Model GPT-4, Temperature 0.7
- Tool: Ahrefs
  Config: API Key from process.env.AHREFS_API_KEY
`;

fs.writeFileSync('./SOUL.md', echoTemplate);
```

## Common Agent Patterns

### 1. Scheduled Task Agent

```javascript
// Daily standup collection agent
const standupAgent = {
  schedule: '0 9 * * *', // 9 AM daily
  action: 'collect standup responses',
  integrations: ['slack'],
  
  behavior: `
    Send message to #standup channel:
    "Good morning! Please share:
    - Yesterday's progress
    - Today's plans
    - Blockers"
    
    Collect responses for 30 minutes.
    Generate summary report.
    Post to #management channel.
  `
};
```

### 2. Event-Driven Agent

```javascript
// PR reviewer agent (webhooks)
const prReviewerAgent = {
  trigger: 'github.pull_request.opened',
  
  workflow: [
    'Fetch PR diff',
    'Analyze code changes',
    'Check for security issues',
    'Verify test coverage',
    'Post review comment'
  ],
  
  config: {
    github: {
      webhook_url: process.env.GITHUB_WEBHOOK_URL,
      secret: process.env.GITHUB_WEBHOOK_SECRET
    }
  }
};
```

### 3. Interactive Chat Agent

```javascript
// Customer support agent
const supportAgent = {
  interface: 'telegram',
  memory: 'redis',
  
  behavior: `
    Greet users warmly.
    Understand their issue through questions.
    Search knowledge base for solutions.
    If no solution found, escalate to human.
    Track conversation history.
  `,
  
  integrations: {
    telegram: {
      token: process.env.TELEGRAM_BOT_TOKEN
    },
    redis: {
      url: process.env.REDIS_URL
    },
    zendesk: {
      api_key: process.env.ZENDESK_API_KEY,
      subdomain: process.env.ZENDESK_SUBDOMAIN
    }
  }
};
```

## Running Agents

### Node.js Quickstart Template

```javascript
// bot.js - Basic agent runner
const fs = require('fs');
const { OpenAI } = require('openai');

// Load SOUL.md configuration
const soulConfig = fs.readFileSync('./SOUL.md', 'utf8');

// Initialize OpenAI (or your LLM provider)
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY
});

// Agent runtime
async function runAgent(userInput) {
  const completion = await openai.chat.completions.create({
    model: 'gpt-4',
    messages: [
      {
        role: 'system',
        content: soulConfig // SOUL.md defines behavior
      },
      {
        role: 'user',
        content: userInput
      }
    ]
  });
  
  return completion.choices[0].message.content;
}

// Example usage
runAgent('What tasks are due today?').then(console.log);
```

### Docker Deployment

```dockerfile
# Dockerfile for any agent
FROM node:18-alpine

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY SOUL.md ./
COPY bot.js ./

ENV OPENAI_API_KEY=""
ENV AGENT_PORT=3000

EXPOSE 3000

CMD ["node", "bot.js"]
```

```yaml
# docker-compose.yml
version: '3.8'

services:
  openclaw-agent:
    build: .
    ports:
      - "3000:3000"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
  
  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
```

## Finding the Right Agent Template

### By Category

```bash
# List all productivity agents
ls agents/productivity/

# Output:
# orion/          - Project manager
# metrics/        - Analytics dashboard
# daily-standup/  - Standup collection
# inbox-zero/     - Email triage
# meeting-notes/  - Meeting summaries
```

### By Use Case

```javascript
// Search agents.json programmatically
const agents = require('./agents.json');

function findAgent(useCase) {
  return agents.filter(agent => 
    agent.specialty.toLowerCase().includes(useCase.toLowerCase()) ||
    agent.whenToUse.toLowerCase().includes(useCase.toLowerCase())
  );
}

// Example: Find agents for "email"
const emailAgents = findAgent('email');
// Returns: [{ name: 'Inbox', specialty: 'Email triage...', ... }]
```

## Customizing Templates

### Basic Customization

```markdown
<!-- Original SOUL.md -->
# Orion - Project Manager

## Core Identity
- Role: Task coordination
- Tone: Professional

<!-- Customized version -->
# Orion - Engineering PM

## Core Identity
- Role: Engineering task coordination for team X
- Tone: Technical, direct, async-first
- Context: Remote team across 3 timezones

## Custom Rules
- Tag urgent tasks with 🚨
- Use engineering terminology
- Link to Linear tickets
```

### Adding Integrations

```markdown
## Integrations

- Tool: Slack
  Config:
    Webhook: process.env.SLACK_WEBHOOK_URL
    Channel: #engineering
    Mention: @channel for P0 items

- Tool: Linear
  Config:
    API Key: process.env.LINEAR_API_KEY
    Team ID: process.env.LINEAR_TEAM_ID
    Auto-create tickets: true

- Tool: GitHub
  Config:
    Token: process.env.GITHUB_TOKEN
    Repos: ['org/backend', 'org/frontend']
    Track PRs: true
```

## Configuration Patterns

### Environment Variables Setup

```bash
# .env file for any agent
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...

# Integration tokens
SLACK_TOKEN=xoxb-...
GITHUB_TOKEN=ghp_...
NOTION_TOKEN=secret_...

# Database
REDIS_URL=redis://localhost:6379
POSTGRES_URL=postgresql://user:pass@localhost/db

# Agent-specific
AGENT_NAME=orion
AGENT_TIMEZONE=America/New_York
AGENT_LANGUAGE=en
```

### Multi-Agent Setup

```javascript
// multi-agent.js - Run multiple agents
const agents = [
  { name: 'orion', soul: './agents/productivity/orion/SOUL.md' },
  { name: 'lens', soul: './agents/development/code-reviewer/SOUL.md' },
  { name: 'echo', soul: './agents/marketing/echo/SOUL.md' }
];

agents.forEach(agent => {
  const config = fs.readFileSync(agent.soul, 'utf8');
  
  // Spawn agent process
  const child = spawn('node', ['bot.js'], {
    env: {
      ...process.env,
      AGENT_NAME: agent.name,
      SOUL_CONFIG: config
    }
  });
  
  console.log(`Started ${agent.name} agent`);
});
```

## Troubleshooting

### Agent Not Responding

```javascript
// Debug mode
const DEBUG = process.env.DEBUG === 'true';

async function runAgent(input) {
  if (DEBUG) {
    console.log('Input:', input);
    console.log('SOUL config length:', soulConfig.length);
  }
  
  try {
    const response = await openai.chat.completions.create({...});
    if (DEBUG) console.log('Response:', response);
    return response.choices[0].message.content;
  } catch (error) {
    console.error('Agent error:', error.message);
    return 'Error processing request';
  }
}
```

### Common Issues

1. **Missing environment variables**
   ```bash
   # Check all required vars are set
   node -e "console.log(process.env.OPENAI_API_KEY ? 'OK' : 'MISSING')"
   ```

2. **SOUL.md parsing errors**
   ```javascript
   // Validate SOUL.md format
   const soul = fs.readFileSync('./SOUL.md', 'utf8');
   if (!soul.includes('# ')) {
     throw new Error('Invalid SOUL.md: missing heading');
   }
   ```

3. **Integration failures**
   ```javascript
   // Test integrations independently
   const testSlack = await fetch(process.env.SLACK_WEBHOOK_URL, {
     method: 'POST',
     body: JSON.stringify({ text: 'Test' })
   });
   console.log('Slack test:', testSlack.ok ? 'OK' : 'FAILED');
   ```

## Advanced Usage

### Memory & State Management

```javascript
// redis-memory.js - Persistent agent memory
const Redis = require('ioredis');
const redis = new Redis(process.env.REDIS_URL);

async function rememberContext(agentName, userId, context) {
  const key = `agent:${agentName}:user:${userId}`;
  await redis.set(key, JSON.stringify(context), 'EX', 86400); // 24h
}

async function recallContext(agentName, userId) {
  const key = `agent:${agentName}:user:${userId}`;
  const data = await redis.get(key);
  return data ? JSON.parse(data) : null;
}

// Use in agent
const context = await recallContext('orion', userId);
const response = await runAgent(userInput, context);
await rememberContext('orion', userId, { ...context, lastInput: userInput });
```

### Agent Chaining

```javascript
// Chain multiple agents for complex workflows
async function processCustomerRequest(request) {
  // Step 1: Categorize with support agent
  const category = await runAgent('support', 
    `Categorize this request: ${request}`
  );
  
  // Step 2: Route to specialist
  let specialist;
  if (category.includes('technical')) specialist = 'tech-support';
  else if (category.includes('billing')) specialist = 'billing';
  else specialist = 'general';
  
  // Step 3: Generate response
  const response = await runAgent(specialist, request);
  
  // Step 4: QA check
  const qaResult = await runAgent('qa-agent',
    `Review this response: ${response}`
  );
  
  return qaResult.includes('approved') ? response : 'Escalate to human';
}
```

## Best Practices

1. **Start with a template**, customize incrementally
2. **Use environment variables** for all secrets
3. **Test integrations** separately before combining
4. **Version control** your SOUL.md files
5. **Monitor agent behavior** in production
6. **Set rate limits** for API calls
7. **Implement logging** for debugging
8. **Use Redis/DB** for persistent memory

## Resources

- Repository: https://github.com/mergisi/awesome-openclaw-agents
- Deploy packages: https://crewclaw.com/agents
- Agent JSON index: `agents.json` in repo root
- Troubleshooting: `TROUBLESHOOTING.md` in repo
- Newsletter: Weekly agent templates & tips
