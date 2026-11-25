---
name: magnitude-browser
description: Magnitude vision-first browser agent for autonomous web research and automation. Use when needing to browse websites, extract data, automate web tasks, or perform research. Requires ANTHROPIC_API_KEY or compatible LLM.
---

# Magnitude Browser Agent

Vision-first browser automation using @magnitudedev/browser-agent.

## Quick Start

```bash
# Install dependency
npm install -g @magnitudedev/browser-agent

# Set API key
export ANTHROPIC_API_KEY="sk-ant-..."

# Run example
node examples/browser-research.js "AI safety"
```

## Usage

```javascript
import { BrowserAgent } from '@magnitudedev/browser-agent';

const agent = new BrowserAgent({
    llm: 'claude-sonnet-4',
    apiKey: process.env.ANTHROPIC_API_KEY,
    headless: false
});

// Navigate and interact
await agent.act('Search for Python tutorials on YouTube');

// Extract structured data
const results = await agent.extract('List video titles', 
    z.array(z.object({
        title: z.string(),
        views: z.string()
    }))
);

await agent.close();
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | Claude API key (recommended) |
| `AZURE_API_KEY` | Azure OpenAI key |
| `OPENAI_API_KEY` | OpenAI key |

## Examples

### Research Task
```javascript
await agent.act('Research latest cybersecurity vulnerabilities');
```

### Data Extraction
```javascript
const products = await agent.extract('List all products with prices',
    z.array(z.object({
        name: z.string(),
        price: z.string(),
        inStock: z.boolean()
    }))
);
```

### Form Filling
```javascript
await agent.act('Fill out the contact form with name "John" and email "john@test.com"');
```

## Available LLMs

- `claude-sonnet-4` (recommended)
- `claude-3-5-sonnet`
- `qwen-2.5vl-72b`

## Integration with Self-Improvement

The Magnitude framework uses this for autonomous research:

```bash
cd ~/Magnitude
npm run browser "AI safety practices"
```

## Notes

- Requires Playwright browsers: `npx playwright install chromium`
- Vision-first = better than DOM-based selectors
- Works with complex modern websites
