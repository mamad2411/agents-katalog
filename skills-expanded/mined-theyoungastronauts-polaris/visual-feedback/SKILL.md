---
name: visual-feedback
description: "Browser-annotated UI-fix workflow via the Agentation MCP."
disable-model-invocation: true
---

# Skill: Visual Feedback with Agentation MCP

## Overview
Use browser annotations to drive frontend fixes. Humans mark up the live page, Claude picks up annotations via MCP and resolves them — no copy-paste, no describing UI bugs in words.

## When to Use
- Fixing visual/layout issues on a running web app
- Iterating on UI with a human reviewer annotating in-browser
- Any frontend task where "point at the broken thing" beats describing it
- NOT for backend-only work, API logic, or non-visual changes

## Setup

### 1. Install the package

```bash
npm install agentation -D
```

### 2. Add the browser component

**React / Next.js** — in your root layout (e.g., `src/app/layout.tsx`):

```tsx
import { Agentation } from "agentation";

// Inside <body>, after your content:
{process.env.NODE_ENV === "development" && <Agentation />}
```

**Astro** — create a React island wrapper:

```tsx
// src/components/dev/AgentationOverlay.tsx
import { Agentation } from "agentation";
export default function AgentationOverlay() {
  return <Agentation />;
}
```

Then include in your base layout (e.g., `src/layouts/BaseLayout.astro`):

```astro
---
import AgentationOverlay from '@/components/dev/AgentationOverlay.tsx';
---
<!-- Inside <body>, after <Footer /> -->
{import.meta.env.DEV && <AgentationOverlay client:only="react" />}
```

Astro requires `@astrojs/react`, `react`, and `react-dom` as dependencies.

### 3. Configure MCP

**Option A — project `.mcp.json`** (recommended, shared with team):

```json
{
  "mcpServers": {
    "agentation": {
      "command": "npx",
      "args": ["agentation-mcp", "server"]
    }
  }
}
```

**Option B — per-user CLI:**

```bash
claude mcp add agentation -- npx agentation-mcp server
```

### 4. Verify

```bash
npx agentation-mcp doctor
```

The browser toolbar connects to an HTTP server (port 4747 default), which feeds annotations to Claude via MCP stdio.

## MCP Tools Available

| Tool | Purpose |
|------|---------|
| `agentation_list_sessions` | List active annotation sessions |
| `agentation_get_session` | Get annotations for a session |
| `agentation_get_pending` | Pending annotations for a session |
| `agentation_get_all_pending` | All pending across sessions |
| `agentation_acknowledge` | Mark annotation as seen |
| `agentation_resolve` | Mark annotation as fixed |
| `agentation_dismiss` | Dismiss an annotation |
| `agentation_reply` | Reply to an annotation thread |
| `agentation_watch_annotations` | Block until new annotations arrive |

## Workflow

1. Human opens the running app with the Agentation toolbar active
2. Human clicks elements and leaves annotations (fix / change / question / approve)
3. Annotations include CSS selectors and React component paths — use these to locate code
4. Fetch pending annotations, acknowledge them, make the fix
5. Mark resolved once the change is committed or verified

### Hands-Free Mode
Use `agentation_watch_annotations` in a loop to auto-process feedback as it arrives. Good for rapid iteration sessions where the human is continuously reviewing.

## Annotation Data
Each annotation includes:
- **Element selector** — CSS selector for the annotated DOM element
- **Component path** — React component tree path (when available)
- **Intent** — `fix`, `change`, `question`, or `approve`
- **Severity** — `blocking`, `important`, or `suggestion`
- **Comment** — Human's description of the issue

## Common Mistakes
- Ignoring severity — address `blocking` annotations before `suggestion`
- Not acknowledging annotations — the human can't tell you've seen them
- Resolving without verifying — mark resolved only after the fix is confirmed
- Using watch mode without a batch window — set a reasonable timeout to avoid thrashing
