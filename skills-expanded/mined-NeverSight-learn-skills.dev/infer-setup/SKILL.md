---
name: infer-setup
description: Use when setting up Infer analytics in a new project, integrating the SDK, or configuring the MCP server. Triggers on "set up analytics", "add tracking", "integrate infer", "install infer", or when a project has no analytics and the user wants to add it.
allowed-tools:
  - AskUserQuestion
---

# Infer Setup — The Wizard

## Update Check (non-blocking)

Run this at the start. Checks for newer Infer versions using a 6-hour cache:

```bash
_INFER_CACHE=~/.infer/last-update-check.json
_NEEDS_CHECK="yes"
if [ -f "$_INFER_CACHE" ]; then
  _CACHE_AGE=$(( $(date +%s) - $(stat -f '%m' "$_INFER_CACHE" 2>/dev/null || stat -c '%Y' "$_INFER_CACHE" 2>/dev/null || echo 0) ))
  [ "$_CACHE_AGE" -lt 21600 ] && _NEEDS_CHECK="no"
fi
if [ "$_NEEDS_CHECK" = "yes" ]; then
  _SDK_LATEST=$(npm view @inferevents/sdk version 2>/dev/null || echo "unknown")
  _MCP_LATEST=$(npm view @inferevents/mcp version 2>/dev/null || echo "unknown")
  _SDK_INSTALLED=$(npm ls @inferevents/sdk --json 2>/dev/null | grep '"version"' | head -1 | sed 's/[^0-9.]//g' || echo "none")
  mkdir -p ~/.infer
  echo "{\"checked\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"sdk_latest\":\"$_SDK_LATEST\",\"mcp_latest\":\"$_MCP_LATEST\",\"sdk_installed\":\"$_SDK_INSTALLED\"}" > "$_INFER_CACHE"
  echo "INFER_SDK_INSTALLED=$_SDK_INSTALLED INFER_SDK_LATEST=$_SDK_LATEST INFER_MCP_LATEST=$_MCP_LATEST"
else
  cat "$_INFER_CACHE"
  echo "INFER_CHECK=cached"
fi
```

If installed SDK version differs from latest, append at the END of your response:
`Infer update available — run /infer-upgrade to get the latest.`
Do NOT block the wizard. Continue normally.

This is the full setup wizard. It detects your current state and walks you through
everything step by step, asking before each change.

## How Infer Works

- **Write key** (`pk_write_...`): Public. Embedded in app JS. Can ONLY send events.
- **Read key** (`pk_read_...`): Secret. In `~/.infer/config.json`. Used by this MCP server to query data.
- **SDK** (`@inferevents/sdk`): Installed in the user's app. Tracks events.
- **MCP server** (`@inferevents/mcp`): Separate package. Connects to Claude Code as an MCP server. Queries the API.
- **Skills** (`@inferevents/skills`): This package. Teaches agents how to use Infer.

## Setup Flow

The wizard follows this order:

```
1. Account setup (signup or login)
2. Project setup (create or select project, fetch keys)
3. SDK install + integrate into project code
4. Tracking plan (read codebase, suggest and add events)
5. Configure MCP + restart Claude Code
```

MCP is last because it needs a restart. By doing it last, the restart serves
double duty: connects MCP AND marks the end of setup. When the user comes back,
everything is ready — SDK installed, events instrumented, MCP connected.

## Entry Points

There are two ways users arrive here:

### Entry A: User says "set up Infer" or invokes /infer-setup
Start from Step 1 below.

### Entry B: User pasted a setup prompt from infer.events/signup
The prompt contains credentials inline. Extract them and skip to Step 3.
Look for: `projectId`, `writeKey`, `readKey`, `endpoint` in the pasted text.

## The Wizard

### Step 1: Account setup

Read `~/.infer/config.json`. Four possible states:

**State A: Config exists with projects**
The user already has an Infer account. Check if the current directory already has
Infer configured (check `package.json` for `@inferevents/sdk` in dependencies).

If SDK is already installed:
→ Say: "This project already has Infer configured (project: [active project name])."
→ Ask: "Want to keep this config, switch to a different project, or create a new one?"
  A) Keep current config → Jump to Step 3 (detect project)
  B) Switch project → List projects from config, let user pick, then Step 3
  C) Create new project → Go to Step 2

If SDK is NOT installed:
→ Say: "Found your Infer account ([N] projects). Let's set up this codebase."
→ Ask: "Use an existing project or create a new one?"
  A) Use existing → Let user pick, then jump to Step 3
  B) Create new → Go to Step 2

**State B: Config exists but empty/invalid**
→ Say: "Found Infer config but it's invalid. Let's reconnect."
→ Go to Step 1c (signup).

**State C: Config exists with session but no projects (new signup)**
The user just signed up. The config has `{"endpoint":"...","session":"abc123"}`
but no projects yet.
→ Say: "Found your Infer session. Let me fetch your project."
→ Go to Step 1b (fetch keys).

**State D: No config file**
→ Say: "No Infer account found. Let's get you set up."
→ Go to Step 1c (signup).

### Step 1b: Fetch project keys via session

If the config has a `session` field but no project keys, fetch them from the API.

1. Call `GET /v1/auth/me?session=SESSION` to get the user's project list
2. If user has one project:
   - Call `GET /v1/auth/project-keys?session=SESSION&project_id=PROJECT_ID`
   - Save the returned write_key and read_key to `~/.infer/config.json`
   - Write `.infer.json` to project root: `{"project": "<project-slug>"}`
   - Add `.infer.json` to `.gitignore`
   - Jump to Step 3 (detect project)
3. If user has multiple projects:
   - Ask which project to use for this codebase
   - Fetch keys for the chosen project
   - Save to config as active project
   - Write `.infer.json` to project root with chosen project
   - Add `.infer.json` to `.gitignore`
4. If user has no projects:
   - Go to Step 2 (create new project)

This step is the magic: the user never sees or handles API keys. The session
token authenticates, the API returns the keys, and they're saved automatically.
The `.infer.json` file in the project root pins this directory to the correct
project so the MCP server auto-selects it regardless of the global activeProject.

### Step 1c: Signup

→ Ask: "Do you have an Infer account?"
  A) Yes → Open https://infer.events/signup, sign in, paste the setup command here.
  B) No → Open https://infer.events/signup, create an account, paste the setup command.

When they paste it, the config is saved to `~/.infer/config.json` with a session
token. Proceed to Step 1b.

### Step 2: Create new project

This runs entirely in the CLI. No website redirect needed.

Ask: "What should we call this project?" (suggest: the current directory name)

Then call the `create_project` MCP tool with the project name. This:
1. Reads the saved session token from `~/.infer/config.json`
2. Calls the Infer API to create a new project
3. Generates write + read API keys
4. Saves the new project to `~/.infer/config.json` as the active project

If the tool returns "No session found": the user needs to sign in first.
Say: "You need to sign in once. Opening infer.events/signup..."
After they complete signup and paste the setup command, extract the session token
and retry the project creation.

After project creation succeeds:
→ Write `.infer.json` to the project root: `{"project": "<project-slug>"}`
  This pins this directory to the project so the MCP server auto-selects it.
→ Add `.infer.json` to the project's `.gitignore` (it contains no secrets,
  but it's machine-specific like .env.local).
→ Say: "Project '[name]' created! Config saved. This directory is now linked to it."
→ Jump to Step 3 (detect project).

### Step 3: Detect project and install SDK

Read `package.json` in the current working directory.

**Framework detection:**

| Signal | Framework | Entry point |
|--------|-----------|-------------|
| `"next"` in deps + `src/app/` exists | Next.js App Router | `src/app/layout.tsx` |
| `"next"` in deps + `src/pages/` exists | Next.js Pages Router | `src/pages/_app.tsx` |
| `"react-scripts"` in deps | Create React App | `src/index.tsx` |
| `"vite"` in devDeps + `"react"` in deps | Vite + React | `src/main.tsx` |
| `"expo"` in deps | Expo / React Native | `App.tsx` or `app/_layout.tsx` |
| `"nuxt"` in deps | Nuxt.js | `app.vue` or `plugins/` |
| `"@sveltejs/kit"` in devDeps | SvelteKit | `src/routes/+layout.svelte` |
| None detected | Unknown | Ask user |

Tell the user what you detected:
"Detected **[framework]** project. Entry point: `[path]`."

If `@inferevents/sdk` is already in dependencies:
"SDK already installed. Checking integration..."
→ Skip to Step 4.

Otherwise, ask: "Install @inferevents/sdk? (This adds the tracking library to your project)"

If yes:
```bash
npm install @inferevents/sdk@latest
```

### Step 4: Integrate SDK

Ask: "Add tracking to [detected entry point]? I'll create the analytics module and
wire it into your app. I'll ask before changing each file."

**Then create files based on detected framework:**

#### Next.js App Router

**Gate 1:** "Create `src/lib/analytics.ts`?"
```typescript
import { init, track, identify, page, reset } from "@inferevents/sdk";

export function initAnalytics() {
  if (typeof window === "undefined") return;
  init({
    projectId: "[WRITE_KEY]",
    endpoint: "[ENDPOINT]",
    autoTrack: true,
    debug: process.env.NODE_ENV === "development",
  });
}

export { track, identify, page, reset };
```

**Gate 2:** "Create `src/components/analytics-provider.tsx`?"
```typescript
"use client";
import { useEffect } from "react";
import { initAnalytics } from "@/lib/analytics";

export function AnalyticsProvider() {
  useEffect(() => { initAnalytics(); }, []);
  return null;
}
```

**Gate 3:** "Add `<AnalyticsProvider />` to `src/app/layout.tsx`?"
- Import the component
- Add inside `<body>` tag

#### Next.js Pages Router

**Gate 1:** Create `src/lib/analytics.ts` (same as above)
**Gate 2:** Add to `src/pages/_app.tsx`:
```typescript
import { useEffect } from "react";
import { initAnalytics } from "@/lib/analytics";

// Inside the component:
useEffect(() => { initAnalytics(); }, []);
```

#### Vite / CRA / Plain React

**Gate 1:** Create `src/lib/analytics.ts` (same as above)
**Gate 2:** Add to `src/main.tsx`:
```typescript
import { initAnalytics } from "./lib/analytics";
initAnalytics();
```

### Step 4b: Check for Content Security Policy

After integrating the SDK, check if the project has a CSP that would block
requests to `api.infer.events`. Search for Content-Security-Policy in:
- `next.config.ts` / `next.config.js` (Next.js headers)
- `middleware.ts` (Next.js middleware)
- `<meta http-equiv="Content-Security-Policy">` in HTML
- `.htaccess`, `nginx.conf`, `vercel.json` headers

If a CSP with `connect-src` is found and does NOT include `api.infer.events`:
→ Say: "Your site has a Content Security Policy. I need to add api.infer.events
   to connect-src so the SDK can send events."
→ Add `https://api.infer.events` to the existing `connect-src` directive.
→ Ask before making the change.

If no CSP is found, skip this step silently.

### Step 5: Build tracking plan

Say: "Now let's set up your tracking plan. I'll read your codebase and suggest
which user actions to track beyond the auto-tracked page views and clicks."

Follow the tracking plan process completely. It will:
1. Deep dive into the codebase to understand the product
2. Map the user journey (entry → activation → core action → engagement)
3. Propose specific events at specific file:line locations
4. Present a table for approval
5. Implement only the approved events

This is the most valuable step — it's doing the PM's job of deciding what to measure,
based on the actual code, not guessing.

### Step 6: Configure MCP server

Now that the SDK and tracking plan are set up, add the MCP server config.

Check if `.mcp.json` already exists in the project root or if the user's
Claude Code settings already have an `infer` MCP server configured.

If NOT configured:
Ask: "I need to add the Infer MCP server to your project config. This lets
your agent query your analytics data. OK?"

Add to `.mcp.json` in the project root:
```json
{
  "mcpServers": {
    "infer": {
      "command": "npx",
      "args": ["--yes", "@inferevents/mcp@latest"]
    }
  }
}
```

If `.mcp.json` already exists, merge the `infer` entry into it.

### Step 7: Restart and verify

This is the final step. Present a summary of everything that was set up:

```
Setup complete:
- ~/.infer/config.json — account credentials
- .infer.json — links this directory to your project
- .mcp.json — Infer MCP server for querying analytics
- src/lib/analytics.ts — SDK initialized with your project key
- src/components/analytics-provider.tsx — client component that boots the SDK
- src/app/layout.tsx — provider wired into root layout
- [N] custom events added via tracking plan

To start using Infer:
1. Restart Claude Code (so the MCP server connects)
2. Open your app in the browser (npm run dev)
3. Navigate around — auto-tracking and custom events will fire
```

Then you MUST call the `AskUserQuestion` tool:

> Restart Claude Code to connect the MCP server. After restart, you can ask
> your agent anything about your analytics data.
>
> 💡 Tip: After restarting, try asking "Give me a quick pulse on the app" to see your first insights.

Options:
- A) I'll restart now — Come back and ask me anything about your data
- B) See my first insights — Run a quick health check on whatever data is flowing (requires restart first)
- C) Set up daily monitoring — Schedule automatic checks so you catch issues early
- D) Just explore — I'll ask questions about my data as I go

## From the Website: Install Flow

When a user signs up on the website, the signup page shows two steps:

**Step 1: Install skills**
```
npx skills add infer-events/skills
```

**Step 2: Paste into Claude Code**
```
Save this config to ~/.infer/config.json:
{"apiKey":"[READ_KEY]","endpoint":"[ENDPOINT]","projectId":"[PROJECT_ID]"}.
Then run /infer-setup to configure everything.
```

The setup wizard handles the rest: account check, SDK install, framework
detection, tracking integration, MCP config, and restart instructions.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| "No events found" after setup | Write key wrong or app not running | Check write key in analytics.ts, check browser console |
| 401 from API | Invalid or wrong key type | Write key for SDK, read key for MCP |
| SDK not initializing | SSR calling init() | Check `typeof window !== "undefined"` guard |
| MCP server can't connect | Wrong endpoint or read key | Check ~/.infer/config.json |
| "Failed to reconnect" after upgrade | .mcp.json has pinned version (@inferevents/mcp@0.1.6) | Change args to `["@inferevents/mcp"]` (no version), then /mcp restart |
| Auto-track not firing | autoTrack not set | Set `autoTrack: true` in init() |
| Console: "Refused to connect" / CSP error | Content Security Policy blocks api.infer.events | Add `https://api.infer.events` to `connect-src` in your CSP header |
| SDK retries then stops after 5 attempts | CSP or network blocking the endpoint | Check console for the CSP help message, add domain to connect-src |
