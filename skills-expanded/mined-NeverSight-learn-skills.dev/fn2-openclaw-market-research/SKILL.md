---
name: fn2-openclaw-market-research
description: Use FN2's grounded market research API and schedulable research agents for stocks, earnings, filings, and economic data inside OpenClaw
triggers:
  - "research this stock's recent performance"
  - "what happened with earnings for this company"
  - "set up a daily market brief agent"
  - "get economic data and analysis"
  - "analyze recent SEC filings"
  - "create a scheduled research agent"
  - "what did the CEO say on the earnings call"
  - "why did this stock move today"
---

# FN2 OpenClaw Market Research Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill enables grounded market and stock research using the FN2 API within OpenClaw. Get sourced answers about stocks, earnings, filings, economic data, and set up schedulable research agents that run on your behalf.

## What FN2 Does

FN2 provides AI-powered financial research that cites live market data, earnings transcripts, SEC filings, and economic reports. Unlike generic LLMs, FN2 grounds its answers in real-time financial sources.

**Key capabilities:**
- Research stocks, sectors, and markets with cited sources
- Query earnings transcripts and SEC filings
- Analyze economic data and macro trends
- Create scheduled research agents (daily briefs, weekly recaps, earnings monitors)
- Access grounded chat models for financial Q&A

## Installation

**From ClawHub:**

```bash
openclaw skills install @fn2/fn2
```

**Manual installation:**

```bash
git clone https://github.com/fn2ai/fn2-openclaw-skill.git
mkdir -p ~/.openclaw/workspace/skills/fn2
cp -r fn2-openclaw-skill/{SKILL.md,scripts,references} ~/.openclaw/workspace/skills/fn2/
chmod +x ~/.openclaw/workspace/skills/fn2/scripts/fn2
```

## Authentication

Get your API key from [fn2.ai/api-keys](https://fn2.ai/api-keys?ref=openclaw) (requires free account). Grant `chat`, `agents`, and `models` scopes.

Export the key:

```bash
export FN2_API_KEY=fn2_your_actual_key_here
```

The skill reads this environment variable. Never hardcode keys in code.

## CLI Reference

The skill bundles a zero-dependency Python CLI at `~/.openclaw/workspace/skills/fn2/scripts/fn2`.

### Research Command

Ask grounded research questions:

```bash
fn2 research "How did NVDA perform this quarter and what drove the results?"
fn2 research "What's the current inflation outlook based on recent CPI data?"
fn2 research "Summarize Apple's latest 10-K key risks"
```

**With JSON output:**

```bash
fn2 research "Tesla delivery numbers vs consensus" --json
```

**Using stdin (for programmatic queries):**

```bash
echo "Compare mega-cap tech earnings this season" | fn2 research -
```

### Agents Commands

Create scheduled research agents that run automatically:

```bash
# Daily market brief at 8am ET on weekdays
fn2 agents create \
  --name "Morning Brief" \
  --prompt "Market overnight moves, key economic data, stocks to watch" \
  --every weekdays \
  --timezone America/New_York

# Weekly sector rotation analysis
fn2 agents create \
  --name "Sector Review" \
  --prompt "Which sectors outperformed this week and why? Include rotation flows." \
  --every weekly \
  --timezone America/New_York

# Custom cron schedule (daily at 6:30am)
fn2 agents create \
  --name "Pre-Market" \
  --prompt "Futures, overnight news, earnings releases today" \
  --cron "30 6 * * *" \
  --timezone America/New_York
```

**List agents:**

```bash
fn2 agents list
fn2 agents list --json  # machine-readable
```

**Get agent details and recent runs:**

```bash
fn2 agents get <agent-id>
fn2 agents get <agent-id> --json
```

**Delete an agent:**

```bash
fn2 agents delete <agent-id>
```

### Models Command

List available FN2 chat models:

```bash
fn2 models
fn2 models --json
```

Use these model IDs when calling the chat API directly.

### Common Options

- `--json`: Output JSON instead of formatted text
- `--help`: Show command help
- `--version`: Show CLI version

## Direct API Usage

The CLI wraps the FN2 REST API. You can also call endpoints directly.

### Research Endpoint

```python
import os
import json
import urllib.request

api_key = os.environ["FN2_API_KEY"]
question = "What drove the market selloff yesterday?"

req = urllib.request.Request(
    "https://api.fn2.ai/v1/research",
    data=json.dumps({"question": question}).encode(),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    method="POST"
)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    print(result["answer"])
    print("\nSources:", result.get("sources", []))
```

### Create Agent Endpoint

```python
import os
import json
import urllib.request

api_key = os.environ["FN2_API_KEY"]

agent_config = {
    "name": "Earnings Monitor",
    "prompt": "Track AAPL, MSFT, GOOGL earnings releases and key metrics",
    "schedule": {
        "type": "cron",
        "cron": "0 17 * * *",  # 5pm daily
        "timezone": "America/New_York"
    }
}

req = urllib.request.Request(
    "https://api.fn2.ai/v1/agents",
    data=json.dumps(agent_config).encode(),
    headers={
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    },
    method="POST"
)

with urllib.request.urlopen(req) as resp:
    agent = json.loads(resp.read())
    print(f"Created agent {agent['id']}: {agent['name']}")
```

### List Agents Endpoint

```python
import os
import json
import urllib.request

api_key = os.environ["FN2_API_KEY"]

req = urllib.request.Request(
    "https://api.fn2.ai/v1/agents",
    headers={"Authorization": f"Bearer {api_key}"},
    method="GET"
)

with urllib.request.urlopen(req) as resp:
    agents = json.loads(resp.read())
    for agent in agents["agents"]:
        print(f"{agent['id']}: {agent['name']} - {agent['schedule']}")
```

## Configuration

**Environment Variables:**

- `FN2_API_KEY` (required): Your FN2 API key
- `FN2_BASE_URL` (optional): Override API base URL (default: `https://api.fn2.ai/v1`)

**Schedule Types:**

Agents support flexible scheduling:

- `weekdays`: Monday-Friday (specify time with `--timezone`)
- `weekly`: Once per week
- `cron`: Custom cron expression (e.g., `"0 9 * * 1-5"` for weekdays at 9am)

**Timezones:**

Use IANA timezone names (`America/New_York`, `Europe/London`, `Asia/Tokyo`, etc.). Defaults to `UTC` if not specified.

## Common Patterns

### Stock Research Workflow

```bash
# Get quick overview
fn2 research "NVDA stock performance this month"

# Deep dive on earnings
fn2 research "Analyze NVDA's latest earnings call: revenue breakdown, guidance, management tone"

# Compare to peers
fn2 research "How does NVDA's revenue growth compare to AMD and Intel this quarter?"
```

### Economic Analysis

```bash
# Macro snapshot
fn2 research "Current inflation trends and Fed expectations"

# Sector impact
fn2 research "How will rising rates affect REITs and utilities?"

# Data deep-dive
fn2 research "Break down the latest jobs report: headline vs real numbers"
```

### Scheduled Research Agents

```bash
# Morning routine agent
fn2 agents create \
  --name "Market Open Prep" \
  --prompt "Pre-market: futures, overnight international markets, key earnings today, economic calendar" \
  --every weekdays \
  --timezone America/New_York

# Weekly portfolio review
fn2 agents create \
  --name "Portfolio Check" \
  --prompt "Review: AAPL, MSFT, GOOGL, AMZN - weekly performance, news, upcoming catalysts" \
  --every weekly \
  --timezone America/New_York

# Earnings season monitor
fn2 agents create \
  --name "Tech Earnings Watch" \
  --prompt "Track mega-cap tech earnings: beats/misses, guidance changes, analyst reactions" \
  --cron "0 16 * * *" \
  --timezone America/New_York
```

### Integration with OpenClaw

When a user asks about markets/stocks, invoke the skill:

```python
# In your OpenClaw agent logic
import subprocess
import json

def get_market_research(query):
    """Get grounded market research via FN2 skill."""
    result = subprocess.run(
        ["fn2", "research", query, "--json"],
        capture_output=True,
        text=True,
        check=True
    )
    data = json.loads(result.stdout)
    return {
        "answer": data["answer"],
        "sources": data.get("sources", [])
    }

# Example usage
research = get_market_research("Why did tech stocks drop today?")
print(research["answer"])
for source in research["sources"]:
    print(f"- {source}")
```

## Troubleshooting

### Missing API Key

**Error:** `FN2_API_KEY environment variable not set`

**Solution:** Export your API key:

```bash
export FN2_API_KEY=fn2_your_key_here
```

Add to `~/.bashrc` or `~/.zshrc` to persist across sessions.

### Permission Denied

**Error:** `Permission denied: fn2`

**Solution:** Make the CLI executable:

```bash
chmod +x ~/.openclaw/workspace/skills/fn2/scripts/fn2
```

### API Rate Limits

**Error:** `429 Too Many Requests`

**Solution:** FN2 free tier has rate limits. Wait a moment and retry, or upgrade your plan at [fn2.ai/pricing](https://fn2.ai/pricing).

### Invalid Schedule

**Error:** `Invalid cron expression`

**Solution:** Use valid cron syntax (`minute hour day month weekday`):

```bash
# Valid examples
--cron "0 9 * * *"        # 9am daily
--cron "0 9 * * 1-5"      # 9am weekdays
--cron "0 17 * * 5"       # 5pm Fridays
```

Or use preset schedules:

```bash
--every weekdays
--every weekly
```

### Empty or Irrelevant Answers

**Issue:** Response doesn't match your query

**Solution:** Be specific in your research questions:

❌ "Tell me about the market"
✅ "What drove the S&P 500 move in the last session? Break down sector performance."

❌ "Apple stock"
✅ "How has AAPL performed vs the Nasdaq over the past month, and what were the key drivers?"

### Agent Not Running

**Issue:** Scheduled agent isn't producing results

**Solution:** 

1. Verify agent is created: `fn2 agents list`
2. Check recent runs: `fn2 agents get <agent-id>`
3. Confirm timezone is correct
4. Ensure prompt is specific enough to generate useful research

## Advanced Usage

### Batch Research Queries

```bash
# Create a file with questions
cat > research_questions.txt <<EOF
What's the current state of AI chip demand?
How are cloud infrastructure stocks positioned?
What's the outlook for cybersecurity spending?
EOF

# Run batch queries
while IFS= read -r question; do
    echo "=== $question ==="
    fn2 research "$question"
    echo
done < research_questions.txt
```

### JSON Parsing in Scripts

```python
#!/usr/bin/env python3
import subprocess
import json

def research_with_sources(query):
    result = subprocess.run(
        ["fn2", "research", query, "--json"],
        capture_output=True,
        text=True,
        check=True
    )
    data = json.loads(result.stdout)
    
    print(f"Answer: {data['answer']}\n")
    if "sources" in data:
        print("Sources:")
        for src in data["sources"]:
            print(f"  - {src.get('title', 'Unknown')}: {src.get('url', '')}")

research_with_sources("What's driving semiconductor stocks this week?")
```

### Agent Result Webhooks

When creating agents via API, add a webhook URL to receive results:

```python
import os
import json
import urllib.request

agent_config = {
    "name": "Daily Brief",
    "prompt": "Market summary: overnight, key data, stocks to watch",
    "schedule": {"type": "weekdays", "timezone": "America/New_York"},
    "webhook_url": "https://your-server.com/webhook/fn2-agent-results"
}

req = urllib.request.Request(
    "https://api.fn2.ai/v1/agents",
    data=json.dumps(agent_config).encode(),
    headers={
        "Authorization": f"Bearer {os.environ['FN2_API_KEY']}",
        "Content-Type": "application/json"
    },
    method="POST"
)

with urllib.request.urlopen(req) as resp:
    agent = json.loads(resp.read())
    print(f"Agent {agent['id']} will POST results to webhook")
```

## Resources

- **API Documentation:** [fn2.ai/docs/api](https://fn2.ai/docs/api)
- **API Keys:** [fn2.ai/api-keys](https://fn2.ai/api-keys)
- **GitHub Repo:** [github.com/fn2ai/fn2-openclaw-skill](https://github.com/fn2ai/fn2-openclaw-skill)
- **Full CLI Reference:** See `references/api.md` in the skill directory

## License

MIT © FN2. Not affiliated with OpenClaw or ClawHub.
