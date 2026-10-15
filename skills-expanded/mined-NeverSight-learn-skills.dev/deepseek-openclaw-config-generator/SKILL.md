---
name: deepseek-openclaw-config-generator
description: Build and configure DeepSeek model integrations with OpenClaw agent framework using this local-first web app.
triggers:
  - how do I connect DeepSeek to OpenClaw
  - generate OpenClaw config for DeepSeek
  - set up DeepSeek model with OpenClaw
  - create DeepSeek OpenClaw onboarding command
  - configure DeepSeek API for OpenClaw agent
  - which DeepSeek model should I use with OpenClaw
  - show me DeepSeek OpenClaw configuration
  - help with DeepSeek OpenClaw integration
---

# DeepSeek OpenClaw Config Generator

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

DeepSeek OpenClaw is a local-first web application for generating OpenClaw configuration assets tailored to DeepSeek models. It provides a UI for selecting models, generating onboarding commands, and creating redacted config snippets without sending API keys to any backend.

## What It Does

- **Model Catalog**: Browse DeepSeek models with recommended use cases for OpenClaw workflows
- **Command Generator**: Create copy-ready OpenClaw onboarding commands
- **Config Preview**: Generate redacted OpenClaw configuration snippets
- **Security-First**: All processing happens client-side; secrets never leave the browser
- **OpenClaw Integration**: Streamlines the setup of DeepSeek as an OpenClaw provider

## Installation

### Local Development

```bash
# Clone the repository
git clone https://github.com/LawmakerTreasure/deepseek-openclaw.git
cd deepseek-openclaw

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

### Production Deployment

```bash
# Build static assets
npm run build

# Deploy dist/ folder to your hosting provider
# (GitHub Pages, Netlify, Vercel, etc.)
```

## DeepSeek Models for OpenClaw

The app includes these model references:

| Model ID | Best For |
|----------|----------|
| `deepseek/deepseek-v4-flash` | Fast, everyday automation and lightweight tasks |
| `deepseek/deepseek-v4-pro` | Complex coding, planning, and reasoning workflows |
| `deepseek/deepseek-chat` | General conversational interfaces |
| `deepseek/deepseek-reasoner` | Deep reasoning and multi-step problem solving |

Always verify model availability against current DeepSeek and OpenClaw documentation.

## Configuration

### Environment Variables

Create a `.env` file for local configuration (never commit this file):

```bash
# DeepSeek API key (optional for local dev)
DEEPSEEK_API_KEY=your_key_here
```

In production, use environment variable references:

```bash
export DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}"
```

### OpenClaw Onboarding Command

The app generates commands like:

```bash
openclaw onboard \
  --provider deepseek \
  --model deepseek/deepseek-v4-flash \
  --env DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}"
```

### OpenClaw Config Snippet

Generated configuration follows OpenClaw's JSON structure:

```json
{
  "env": {
    "DEEPSEEK_API_KEY": "${DEEPSEEK_API_KEY}"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-v4-flash"
      }
    }
  }
}
```

## Code Examples

### React Component Structure (TypeScript)

The main configuration generator component:

```typescript
import { useState } from 'react';
import { DeepSeekModel, OpenClawConfig } from './types';
import { generateOpenClawCommand, generateConfigSnippet } from './openclaw';
import { deepSeekModels } from './models';

function ConfigGenerator() {
  const [apiKey, setApiKey] = useState('');
  const [selectedModel, setSelectedModel] = useState<DeepSeekModel>('deepseek/deepseek-v4-flash');
  const [verbose, setVerbose] = useState(false);

  const command = generateOpenClawCommand({
    apiKey,
    model: selectedModel,
    verbose,
  });

  const config = generateConfigSnippet({
    apiKey,
    model: selectedModel,
  });

  return (
    <div className="generator">
      <input
        type="password"
        placeholder="DeepSeek API Key"
        value={apiKey}
        onChange={(e) => setApiKey(e.target.value)}
      />
      <select
        value={selectedModel}
        onChange={(e) => setSelectedModel(e.target.value as DeepSeekModel)}
      >
        {deepSeekModels.map((model) => (
          <option key={model.id} value={model.id}>
            {model.name}
          </option>
        ))}
      </select>
      <label>
        <input
          type="checkbox"
          checked={verbose}
          onChange={(e) => setVerbose(e.target.checked)}
        />
        Verbose mode
      </label>
      <pre>{command}</pre>
      <pre>{config}</pre>
    </div>
  );
}
```

### Model Data Structure

```typescript
// src/models.ts
export interface ModelInfo {
  id: string;
  name: string;
  description: string;
  useCase: string;
}

export const deepSeekModels: ModelInfo[] = [
  {
    id: 'deepseek/deepseek-v4-flash',
    name: 'DeepSeek V4 Flash',
    description: 'Fast and efficient for everyday tasks',
    useCase: 'Default choice for automation and quick responses',
  },
  {
    id: 'deepseek/deepseek-v4-pro',
    name: 'DeepSeek V4 Pro',
    description: 'Advanced reasoning for complex coding',
    useCase: 'Multi-file refactoring, architecture planning',
  },
  {
    id: 'deepseek/deepseek-chat',
    name: 'DeepSeek Chat',
    description: 'General conversational model',
    useCase: 'Customer support, casual interactions',
  },
  {
    id: 'deepseek/deepseek-reasoner',
    name: 'DeepSeek Reasoner',
    description: 'Deep reasoning and problem solving',
    useCase: 'Research, debugging, logical analysis',
  },
];
```

### Command Generation Logic

```typescript
// src/openclaw.ts
export interface CommandOptions {
  apiKey: string;
  model: string;
  verbose?: boolean;
}

export function generateOpenClawCommand(options: CommandOptions): string {
  const { apiKey, model, verbose } = options;
  const keyValue = apiKey ? apiKey : '${DEEPSEEK_API_KEY}';
  const verboseFlag = verbose ? ' \\\n  --verbose' : '';

  return `openclaw onboard \\
  --provider deepseek \\
  --model ${model} \\
  --env DEEPSEEK_API_KEY="${keyValue}"${verboseFlag}`;
}

export function generateConfigSnippet(options: CommandOptions): string {
  const { apiKey, model } = options;
  const redactedKey = apiKey ? 'sk-***redacted***' : '${DEEPSEEK_API_KEY}';

  const config = {
    env: {
      DEEPSEEK_API_KEY: redactedKey,
    },
    agents: {
      defaults: {
        model: {
          primary: model,
        },
      },
    },
  };

  return JSON.stringify(config, null, 2);
}
```

### Type Definitions

```typescript
// src/types.ts
export type DeepSeekModel =
  | 'deepseek/deepseek-v4-flash'
  | 'deepseek/deepseek-v4-pro'
  | 'deepseek/deepseek-chat'
  | 'deepseek/deepseek-reasoner';

export interface OpenClawConfig {
  env: {
    DEEPSEEK_API_KEY: string;
  };
  agents: {
    defaults: {
      model: {
        primary: DeepSeekModel;
      };
    };
  };
}
```

## Common Patterns

### Pattern 1: Quick Setup for Simple Automation

```bash
# Use V4 Flash for fast, lightweight agent tasks
openclaw onboard \
  --provider deepseek \
  --model deepseek/deepseek-v4-flash \
  --env DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}"
```

### Pattern 2: Complex Coding Tasks

```bash
# Use V4 Pro for multi-file refactoring and architecture work
openclaw onboard \
  --provider deepseek \
  --model deepseek/deepseek-v4-pro \
  --env DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}" \
  --verbose
```

### Pattern 3: Reasoning-Heavy Workflows

```bash
# Use DeepSeek Reasoner for debugging and analysis
openclaw onboard \
  --provider deepseek \
  --model deepseek/deepseek-reasoner \
  --env DEEPSEEK_API_KEY="${DEEPSEEK_API_KEY}"
```

### Pattern 4: Multiple Model Configuration

```json
{
  "env": {
    "DEEPSEEK_API_KEY": "${DEEPSEEK_API_KEY}"
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "deepseek/deepseek-v4-flash",
        "fallback": "deepseek/deepseek-chat"
      }
    },
    "research": {
      "model": {
        "primary": "deepseek/deepseek-reasoner"
      }
    },
    "coding": {
      "model": {
        "primary": "deepseek/deepseek-v4-pro"
      }
    }
  }
}
```

## Security Best Practices

### Never Commit Secrets

```bash
# Always use environment variables
export DEEPSEEK_API_KEY="your-actual-key"

# Or use a .env file (add to .gitignore)
echo "DEEPSEEK_API_KEY=your-actual-key" >> .env
echo ".env" >> .gitignore
```

### Redaction in UI

```typescript
function redactApiKey(key: string): string {
  if (!key) return '${DEEPSEEK_API_KEY}';
  return 'sk-***redacted***';
}
```

### OpenClaw Channel Security

```json
{
  "channels": {
    "slack": {
      "allowlist": ["@specific-user"],
      "mentionRequired": true
    }
  }
}
```

## Troubleshooting

### Issue: "Model not found"

**Solution**: Verify the model ID against current DeepSeek documentation. Model names may change between versions.

```bash
# Check available models via DeepSeek API
curl https://api.deepseek.com/v1/models \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}"
```

### Issue: "API key invalid"

**Solution**: Ensure your key is correctly set and has the necessary permissions.

```bash
# Test API key
curl https://api.deepseek.com/v1/chat/completions \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -H "Content-Type: application/json" \
  -d '{"model":"deepseek-chat","messages":[{"role":"user","content":"test"}]}'
```

### Issue: Build fails with TypeScript errors

**Solution**: Ensure all dependencies are installed and TypeScript config is correct.

```bash
# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install

# Check TypeScript version
npx tsc --version

# Run type check
npx tsc --noEmit
```

### Issue: OpenClaw command doesn't work

**Solution**: Verify OpenClaw installation and provider support.

```bash
# Check OpenClaw version
openclaw --version

# List available providers
openclaw providers list

# Verify DeepSeek provider is installed
openclaw providers info deepseek
```

## References

- **OpenClaw Documentation**: https://docs.openclaw.ai/
- **OpenClaw DeepSeek Provider**: https://docs.openclaw.ai/providers/deepseek
- **DeepSeek API Documentation**: https://api-docs.deepseek.com/
- **DeepSeek OpenClaw Integration**: https://api-docs.deepseek.com/quick_start/agent_integrations/openclaw

## Project Structure

```
deepseek-openclaw/
├── src/
│   ├── App.tsx              # Main application component
│   ├── main.tsx             # React entry point
│   ├── models.ts            # DeepSeek model definitions
│   ├── openclaw.ts          # Command and config generators
│   ├── types.ts             # TypeScript type definitions
│   └── styles.css           # Global styles
├── .env.example             # Environment variable template
├── vite.config.ts           # Vite build configuration
├── tsconfig.json            # TypeScript configuration
└── package.json             # Dependencies and scripts
```
