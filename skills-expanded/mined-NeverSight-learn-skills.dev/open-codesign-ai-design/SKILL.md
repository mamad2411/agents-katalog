---
name: open-codesign-ai-design
description: Use Open CoDesign to generate prototypes, slides, and PDFs from prompts with Claude, GPT, Gemini, or local models
triggers:
  - create a design prototype with Open CoDesign
  - generate slides using Open CoDesign
  - set up Open CoDesign with my API key
  - export a design to HTML or PDF
  - configure multi-model support in Open CoDesign
  - use Open CoDesign locally with Ollama
  - integrate Open CoDesign into my design workflow
  - troubleshoot Open CoDesign provider settings
---

# Open CoDesign AI Design Skill

> Skill by [ara.so](https://ara.so) — Design Skills collection.

Open CoDesign is an MIT-licensed, local-first desktop application that transforms prompts into polished prototypes, slide decks, and marketing assets. It's the open-source alternative to Claude Design, v0, Lovable, and Bolt.new — letting you bring your own API key (BYOK) for Claude, GPT, Gemini, DeepSeek, Ollama, or any OpenAI-compatible endpoint.

**Key capabilities:**
- Prompt → prototype/slides/PDF generation
- Multi-model support (20+ providers)
- Desktop-native Electron app (macOS 12+, Windows 10+, Linux)
- Local-first with workspace-backed sessions
- Version history and iteration tracking
- Comment mode for targeted edits
- AI-generated tweaks panels (color pickers, sliders)
- Export to HTML, PDF, PPTX, ZIP, Markdown

## Installation

### Package Managers (Recommended)

**macOS:**
```bash
brew install --cask opencoworkai/tap/open-codesign
```

**Windows (Scoop):**
```bash
scoop bucket add opencoworkai https://github.com/OpenCoworkAI/scoop-bucket
scoop install opencoworkai/open-codesign
```

**Windows (winget - pending approval):**
```bash
winget install OpenCoworkAI.OpenCoDesign
```

### Direct Downloads

Download from [GitHub Releases](https://github.com/OpenCoworkAI/open-codesign/releases/latest):

- **macOS (Apple Silicon):** `open-codesign-*-arm64.dmg`
- **macOS (Intel):** `open-codesign-*-x64.dmg`
- **Windows (x64):** `open-codesign-*-x64-setup.exe`
- **Windows (ARM64):** `open-codesign-*-arm64-setup.exe`
- **Linux (AppImage):** `open-codesign-*-x64.AppImage`
- **Linux (Debian/Ubuntu):** `open-codesign-*-x64.deb`
- **Linux (Fedora/RHEL):** `open-codesign-*-x64.rpm`

### macOS Security Workaround

Installers are not yet notarized. On macOS Sequoia 15+:

```bash
xattr -cr "/Applications/Open CoDesign.app"
```

Then launch normally. On Windows, click "More info" → "Run anyway" when SmartScreen appears.

## Configuration

### First Launch Setup

Open CoDesign opens Settings automatically on first run. Choose one of three provider paths:

#### 1. ChatGPT Subscription (No API Key)

For ChatGPT Plus/Pro/Team subscribers using Codex models:

1. Click **"Sign in with ChatGPT"**
2. Authenticate via browser
3. Select Codex models from the dropdown

#### 2. API Key Provider

Set up any supported provider with an API key:

```typescript
// Supported providers in TypeScript config format
interface ProviderConfig {
  type: 'anthropic' | 'openai' | 'google' | 'openrouter' | 
        'deepseek' | 'kimi' | 'glm' | 'siliconflow' | 
        'openai-compatible';
  apiKey: string;
  baseURL?: string; // For OpenAI-compatible endpoints
  model?: string;
}
```

**Environment variable pattern:**
```bash
# Anthropic
export ANTHROPIC_API_KEY=sk-ant-...

# OpenAI
export OPENAI_API_KEY=sk-...

# Google Gemini
export GOOGLE_API_KEY=...

# OpenRouter
export OPENROUTER_API_KEY=...

# DeepSeek
export DEEPSEEK_API_KEY=...
```

**In-app configuration:**
1. Open Settings (gear icon or `Cmd+,` / `Ctrl+,`)
2. Navigate to **Providers** tab
3. Click **Add Provider**
4. Select provider type
5. Paste API key from environment variable
6. (Optional) Set base URL for custom endpoints
7. Click **Save**

#### 3. Local/Keyless (Ollama)

For local models without API keys:

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model (e.g., llama3.1)
ollama pull llama3.1

# Ollama runs on http://localhost:11434 by default
```

In Open CoDesign:
1. Settings → Providers → Add Provider
2. Select **OpenAI-compatible**
3. Base URL: `http://localhost:11434/v1`
4. Leave API key empty
5. Model name: `llama3.1` (or your pulled model)

### One-Click Import

Import existing configurations:

- **Claude Code config:** Settings → Import → Browse to `~/.claude/config.json`
- **Codex API config:** Settings → Import → CLIProxyAPI auto-detect

## Core Workflows

### Generate a Design from Scratch

**Basic prompt pattern:**
```typescript
// The agent interprets natural language prompts
const prompt = `
Create a landing page for a SaaS product called "TaskFlow" 
with a hero section, feature cards, pricing table, and footer. 
Use a blue and white color scheme.
`;
```

**In the app:**
1. Open Open CoDesign
2. Click **New Design** (or `Cmd+N` / `Ctrl+N`)
3. Enter prompt in left panel
4. Select model from dropdown (e.g., `claude-3-5-sonnet-20241022`)
5. Click **Generate** or press `Enter`
6. Watch agent panel for live progress (todos, tool calls)

**Expected output:** Full HTML artifact with CSS, interactive elements, hover states

### Iterate with Comment Mode

**Target specific regions without rewriting entire prompt:**

```typescript
// Comment mode workflow
1. Click "Comment" button in toolbar (or `C` key)
2. Click element in preview pane
3. Drop pin with feedback: "Make this heading larger and bold"
4. Agent rewrites only that region
```

**Use cases:**
- Adjust typography: "Increase line height in this paragraph"
- Refine colors: "Make this button background darker"
- Add elements: "Insert a contact form below this section"

### Use AI-Generated Tweaks

The model emits a tweaks panel with adjustable parameters:

```typescript
// Example tweaks JSON structure (auto-generated)
{
  "primaryColor": { type: "color", value: "#3B82F6" },
  "headingSize": { type: "range", value: 32, min: 16, max: 64 },
  "spacing": { type: "range", value: 16, min: 8, max: 48 }
}
```

**In the app:**
1. Generate a design
2. Open **Tweaks** panel (right sidebar)
3. Adjust sliders, color pickers, or dropdowns
4. Preview updates live
5. Click **Apply** to commit changes

### Export Artifacts

**Export formats:**
- **HTML:** Single-file with embedded CSS/JS
- **PDF:** Print-ready document
- **PPTX:** PowerPoint presentation
- **ZIP:** Multi-file project archive
- **Markdown:** Source code with annotations

```typescript
// Programmatic export pattern (desktop app API)
// Available in Electron main process

import { exportArtifact } from './export';

await exportArtifact({
  sessionId: 'abc123',
  format: 'html', // 'pdf' | 'pptx' | 'zip' | 'markdown'
  outputPath: './exports/my-design.html'
});
```

**In the app:**
1. Open a completed design
2. Click **Export** button (top-right)
3. Select format
4. Choose save location
5. Optionally include version history

### Work with Design Systems

Use `DESIGN.md` files to enforce consistent styling:

```markdown
<!-- DESIGN.md in your workspace -->
# TaskFlow Design System

## Colors
- Primary: #3B82F6
- Secondary: #10B981
- Neutral: #6B7280

## Typography
- Heading: Inter, 32px, bold
- Body: Inter, 16px, regular

## Spacing
- Base unit: 8px
- Section padding: 64px vertical

## Components
- Button: 12px padding, 4px border-radius, primary background
```

**How to use:**
1. Create `DESIGN.md` in workspace directory (Settings → Workspace → Set Path)
2. In prompt, reference: "Follow the design system in DESIGN.md"
3. Agent reads file via permissioned local tools

### Version History

All iterations are saved locally:

```typescript
// Session directory structure
~/.open-codesign/sessions/
  abc123/
    design-v1.html
    design-v2.html
    design-v3.html
    metadata.json
    chat-history.json
```

**In the app:**
1. Open **Your Designs** hub (`Cmd+Shift+D` / `Ctrl+Shift+D`)
2. Select a design
3. Click **Versions** in right sidebar
4. Preview past iterations
5. Restore or fork from any version

## Multi-Model Configuration

### Switch Models Mid-Session

```typescript
// Model selection pattern
1. Start design with claude-3-5-sonnet-20241022
2. Click model dropdown in top bar
3. Switch to gpt-4o for next iteration
4. Conversation context carries over
```

**Recommended models by use case:**
- **Prototypes:** `claude-3-5-sonnet-20241022` (best design sense)
- **Slides:** `gpt-4o` (structured layouts)
- **Code-heavy:** `deepseek-chat` (technical accuracy)
- **Local/offline:** `llama3.1` via Ollama (privacy)

### Configure Multiple Providers

```typescript
// Example: Use Claude for design, GPT for copy, Ollama for experiments

// In Settings → Providers, add:
[
  {
    name: "Anthropic",
    type: "anthropic",
    apiKey: process.env.ANTHROPIC_API_KEY,
    models: ["claude-3-5-sonnet-20241022"]
  },
  {
    name: "OpenAI",
    type: "openai",
    apiKey: process.env.OPENAI_API_KEY,
    models: ["gpt-4o", "gpt-4o-mini"]
  },
  {
    name: "Ollama Local",
    type: "openai-compatible",
    baseURL: "http://localhost:11434/v1",
    models: ["llama3.1", "codellama"]
  }
]
```

## TypeScript Integration Patterns

### Extend with Custom Tools

Open CoDesign uses permissioned local tools in workspace mode:

```typescript
// Example custom tool definition
// Place in workspace/.open-codesign/tools/

import { Tool } from '@open-codesign/types';

export const fetchDataTool: Tool = {
  name: 'fetch_marketing_data',
  description: 'Fetch product metrics from local JSON file',
  parameters: {
    type: 'object',
    properties: {
      filePath: { type: 'string' }
    },
    required: ['filePath']
  },
  handler: async ({ filePath }) => {
    // Permission check happens in main process
    const data = await fs.readFile(filePath, 'utf-8');
    return JSON.parse(data);
  }
};
```

### React Component Generation

Prompts targeting React components:

```typescript
const reactPrompt = `
Create a reusable TaskCard component in React + TypeScript.
Props: title (string), description (string), status (enum: pending | done).
Use Tailwind CSS for styling.
`;

// Expected output structure
/*
interface TaskCardProps {
  title: string;
  description: string;
  status: 'pending' | 'done';
}

export const TaskCard: React.FC<TaskCardProps> = ({ 
  title, 
  description, 
  status 
}) => {
  return (
    <div className="p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-bold">{title}</h3>
      <p className="text-gray-600">{description}</p>
      <span className={status === 'done' ? 'text-green-500' : 'text-yellow-500'}>
        {status}
      </span>
    </div>
  );
};
*/
```

## Common Patterns

### Prompt Engineering for Designs

**Effective prompt structure:**
```typescript
const goodPrompt = `
[Type]: Landing page
[Purpose]: SaaS product launch
[Sections]: Hero with CTA, 3 feature cards, pricing table, footer
[Style]: Modern, minimal, blue/white palette
[Technical]: Responsive, mobile-first, use CSS Grid
[Extras]: Include hover effects on cards
`;

// ❌ Avoid vague prompts:
const badPrompt = "Make a nice website";
```

**Iteration tips:**
- Start broad, refine with comments
- Reference existing designs: "Like Stripe's homepage but for education"
- Specify frameworks: "Use Tailwind utilities, avoid custom CSS"

### Slide Deck Generation

```typescript
const slideDeckPrompt = `
Create a 5-slide pitch deck for TaskFlow:
1. Title slide with logo placeholder
2. Problem statement with bullet points
3. Solution overview with 3 features
4. Market opportunity (include a bar chart placeholder)
5. Call to action with contact info

Use a professional blue gradient background.
Export as PPTX.
`;
```

### PDF Report Generation

```typescript
const pdfPrompt = `
Generate a quarterly business review report:
- Cover page with Q1 2026 title
- Executive summary (1 page)
- Key metrics table (revenue, users, churn)
- 3 charts: line graph (revenue), pie chart (user segments), bar chart (MRR)
- Conclusion with 3 action items

Use corporate colors: #1E40AF (blue), #064E3B (green).
Export as PDF with page numbers.
`;
```

### Local-First Workflow

```typescript
// Set workspace to enable file-backed sessions
// Settings → Workspace → Set Path: ~/projects/my-designs

// Now designs auto-save to:
~/projects/my-designs/.open-codesign/
  sessions/
  cache/
  exports/

// Commit to git:
cd ~/projects/my-designs
git add .open-codesign/sessions/
git commit -m "Save design iterations"
```

## Troubleshooting

### Provider Connection Issues

**Symptom:** "Failed to connect to provider" error

**Solutions:**
```typescript
// 1. Verify API key format
// Anthropic: sk-ant-api03-...
// OpenAI: sk-proj-... or sk-...
// Check for trailing spaces/newlines

// 2. Test connectivity
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{"model":"claude-3-5-sonnet-20241022","max_tokens":10,"messages":[{"role":"user","content":"Hi"}]}'

// 3. Check firewall/proxy settings
// Open CoDesign respects HTTP_PROXY and HTTPS_PROXY env vars

// 4. Enable diagnostics
// Settings → Advanced → Enable Provider Diagnostics
// Check logs in Help → Open Logs Folder
```

### Gemini Model Not Found

**Symptom:** Error with `gemini-*` models

**Fix:** Prefix with `models/`:
```typescript
// ❌ Incorrect
model: "gemini-1.5-pro"

// ✅ Correct
model: "models/gemini-1.5-pro"
```

### OpenAI-Compatible Relay Issues

**Symptom:** "Instructions required" error with third-party relays

**Cause:** Some relays incorrectly enforce system messages

**Workaround:**
```typescript
// Settings → Providers → [Your Relay] → Advanced
{
  "forceSystemMessage": true,
  "defaultInstructions": "You are a helpful assistant."
}
```

### macOS Sequoia Gatekeeper Block

**Symptom:** Cannot open app, "Open Anyway" fails

```bash
# Remove quarantine attribute
xattr -cr "/Applications/Open CoDesign.app"

# Verify removal
xattr -l "/Applications/Open CoDesign.app"
# Should show no com.apple.quarantine
```

### Electron IPC Errors

**Symptom:** "IPC handler not found" in console

**Solution:**
```bash
# Clear cache and restart
# macOS/Linux:
rm -rf ~/.open-codesign/cache

# Windows:
rmdir /s %APPDATA%\open-codesign\cache

# Restart app
```

### Export Failures

**Symptom:** PDF/PPTX export hangs or produces empty file

**Debug steps:**
```typescript
// 1. Check disk space (exports need temp space)
df -h  # macOS/Linux
wmic logicaldisk get size,freespace,caption  # Windows

// 2. Verify Chromium renderer (for PDF)
// Help → Open DevTools → Console
// Look for Chromium print errors

// 3. Try HTML export first (always works)
// Then convert HTML → PDF externally if needed

// 4. Check export logs
// macOS: ~/Library/Logs/open-codesign/export.log
// Windows: %APPDATA%\open-codesign\logs\export.log
// Linux: ~/.config/open-codesign/logs/export.log
```

### ChatGPT Subscription Sign-In Fails

**Symptom:** OAuth redirect loop or "Session expired"

**Fix:**
```typescript
// 1. Clear OAuth cache
// Settings → Advanced → Clear OAuth Cache

// 2. Ensure browser cookies for chat.openai.com are enabled

// 3. Try incognito/private window for OAuth flow

// 4. Verify subscription is active at https://chat.openai.com
```

## Advanced Configuration

### Custom Model Definitions

Add unsupported models via config file:

```typescript
// ~/.open-codesign/config.json
{
  "customModels": [
    {
      "id": "my-custom-model",
      "provider": "openai-compatible",
      "baseURL": "https://my-llm-api.com/v1",
      "apiKey": "ENV:MY_LLM_KEY",
      "contextWindow": 128000,
      "maxOutput": 4096
    }
  ]
}
```

### Workspace Permissions

Control what the agent can access:

```typescript
// workspace/.open-codesign/permissions.json
{
  "allowedPaths": [
    "./design-system",
    "./assets",
    "./data"
  ],
  "deniedPaths": [
    "./secrets",
    "./.env"
  ],
  "allowNetworkAccess": false,
  "allowedTools": [
    "read_file",
    "search_files",
    "list_directory"
  ]
}
```

### Keyboard Shortcuts

- **New Design:** `Cmd+N` / `Ctrl+N`
- **Save:** `Cmd+S` / `Ctrl+S` (auto-saves enabled by default)
- **Export:** `Cmd+E` / `Ctrl+E`
- **Comment Mode:** `C`
- **Tweaks Panel:** `T`
- **Your Designs Hub:** `Cmd+Shift+D` / `Ctrl+Shift+D`
- **Settings:** `Cmd+,` / `Ctrl+,`
- **DevTools:** `Cmd+Opt+I` / `Ctrl+Shift+I`

## Security Best Practices

1. **Never commit API keys:** Use environment variables
   ```bash
   # .env (add to .gitignore)
   ANTHROPIC_API_KEY=sk-ant-...
   OPENAI_API_KEY=sk-...
   ```

2. **Verify downloads:** Check `SHA256SUMS.txt` from releases
   ```bash
   shasum -a 256 -c SHA256SUMS.txt
   ```

3. **Workspace isolation:** Keep sensitive files outside workspace paths

4. **Review tool calls:** Agent panel shows every file access

5. **Update regularly:** Security patches ship with minor versions

## Resources

- **Documentation:** https://opencoworkai.github.io/open-codesign/
- **GitHub:** https://github.com/OpenCoworkAI/open-codesign
- **Releases:** https://github.com/OpenCoworkAI/open-codesign/releases
- **Discussions:** https://github.com/OpenCoworkAI/open-codesign/discussions
- **Issues:** https://github.com/OpenCoworkAI/open-codesign/issues
- **Contributing:** https://github.com/OpenCoworkAI/open-codesign/blob/main/CONTRIBUTING.md
- **Security:** https://github.com/OpenCoworkAI/open-codesign/blob/main/SECURITY.md
