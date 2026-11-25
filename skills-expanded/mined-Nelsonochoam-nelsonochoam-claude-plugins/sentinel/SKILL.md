---
name: sentinel
description: QA artifact generator — point it at a PR or give it freeform instructions. Navigates the UI using agent-browser, captures screenshots at each step, and stitches a GIF. Flags: --debug (annotated overlays), --folder <name> (custom artifact folder).
argument-hint: '<pr-number | instructions> [--debug] [--folder <name>]'
---

User's request: $ARGUMENTS

# sentinel — UI artifact generator

You generate visual QA artifacts: a set of screenshots and a GIF that shows the feature working in the browser. You operate in two modes depending on what the user provides.

## Step 0: Parse arguments

Extract from `$ARGUMENTS`:
- `debug` — optional flag, present if `--debug` appears in args
- `folder` — optional custom artifact folder name, value after `--folder` (e.g. `--folder abc` → `folder="abc"`)
- Everything else is either a **PR number** or **freeform instructions**

**Determine mode:**

- If the remaining argument is a bare integer (e.g. `22254`) → **PR mode**
- If the remaining argument is absent or non-numeric free text (e.g. "toggle dark mode 3 times…") → **Manual mode**
- If nothing is provided at all → ask:

  **PR number or freeform instructions?**

  Reply with a PR number (e.g. `22254`) to capture a pull request, or describe what you want navigated (e.g. "go to settings and toggle dark mode").

Store `screenshot_flag` based on `debug`:
- `debug` present → `screenshot_flag="--annotate"` (numbered red boxes, useful for inspecting what sentinel saw and clicked)
- `debug` absent → `screenshot_flag=""` (clean screenshots)

Use `screenshot_flag` on every `agent-browser screenshot` call throughout the run:

```bash
agent-browser screenshot $screenshot_flag "$ARTIFACT_DIR/step-001.png"
```

## Step 1: Preflight checks

Run these in parallel:

```bash
which agent-browser 2>/dev/null || echo "MISSING"
which magick 2>/dev/null || echo "MISSING_IMAGEMAGICK"
```

If `agent-browser` is missing, tell the user:

> `agent-browser` is not installed. Run `npm install -g agent-browser@0.26.0 && agent-browser install` then retry.

Exit.

If imagemagick is missing, warn but continue — GIF generation will be skipped:

> ImageMagick not found. Will deliver screenshots only (no GIF). Install with `brew install imagemagick@7.1.2-21` to enable GIF output.

## Step 2: Build navigation plan

### PR mode

```bash
gh pr view <pr_number> --json title,body,headRefName,files --jq '{title: .title, body: .body, branch: .headRefName, files: [.files[].path]}'
```

Classify the PR:

- **UI change** — files under `src/pages/` or `src/client/` → continue
- **Backend-only** — only `src/server/`, test files, or config → ask:

  **This looks like a backend-only PR. Is there a UI surface you'd like to capture anyway?**

  Reply with a URL path or `skip` to exit.

Score confidence and clarify when needed:

**High confidence** — PR body has explicit test steps ("Test plan", "How to test", numbered steps). State plan in one line and proceed:

> Test plan from PR: [summary]. Starting now.

**Medium confidence** — feature described but no navigation path. Present the inferred plan:

> Based on the PR I'm planning to: [one-sentence summary].
>
> **Does that sound right, or would you like to adjust the path?**

Reply `yes` or describe a correction.

**Low confidence** — sparse or missing PR body. Ask directly:

> The PR doesn't have enough detail. A few quick answers:
>
> **1. Where should I start?**
>
> **2. What should I do once I'm there?**
>
> **3. Anything special needed to see this?** (feature flag, account type, test data)

### Manual mode

The user has already provided the instructions in `$ARGUMENTS`. Extract:
- What to navigate to
- What actions to perform
- Any special conditions mentioned (e.g. "3 times", "in dark mode", specific UI elements)

Confirm the plan in one line and proceed without gating:

> Instructions: [one-sentence restatement of what you'll do]. Starting now.

If the instructions are ambiguous about where to start (no URL or app section mentioned), ask one focused question:

**Where should I start?** (e.g. `localhost:3000/settings`, "the dashboard", "wherever dark mode is")

## Step 3: Confirm dev server

Ask:

**What URL is the dev server running on?**

Reply `localhost:3000` or paste the full URL. Reply `skip` if there's no UI to test.

Normalize: strip trailing slash, prepend `http://` if no scheme. Store as `base_url`.

## Step 4: Load config

This step loads all user and project configuration. It runs entirely before the browser opens.

### 4a. Determine project key

```bash
PROJECT_KEY=$(basename "$(git rev-parse --show-toplevel 2>/dev/null)" 2>/dev/null || echo "default")
CONFIG_FILE=$HOME/.sentinel/config.json
NAV_FILE=$HOME/.sentinel/nav.json
mkdir -p "$HOME/.sentinel"
```

### 4b. Load or initialise global config

```bash
cat "$CONFIG_FILE" 2>/dev/null || echo "{}"
```

If the file is absent or empty, this is a **brand-new user**. Create it with defaults and proceed to the first-run setup in 4c:

```json
{
  "artifacts_dir": "~/sentinel-artifacts",
  "projects": {}
}
```

From the loaded config extract:
- `artifacts_dir` — global default artifact storage path (fallback: `~/sentinel-artifacts`)
- `project_config` — `config.projects[PROJECT_KEY]` (may be absent)

### 4c. First-run setup (when project has no config entry)

If `project_config` is absent for this `PROJECT_KEY`, ask the user:

> **First-time setup for `[PROJECT_KEY]`** — answers are saved to `~/.sentinel/config.json` and won't be asked again.
>
> 1. **Auth command** — What command prints your session cookie to stdout? You can give the full command (`yarn workspace @acme/playwright cookie`) or a short hint (`playwright cookie`, `auth token`). Enter `none` to log in manually.
>
> 2. **Cookie name** — What is the session cookie key? (the name in `Cookie: <name>=<value>`, e.g. `sessionToken`, `authToken`)
>
> 3. **Fallback profiles** — If the auth command fails, are there alternative environment profiles to retry with? Enter them comma-separated (e.g. `dev, staging, prod`) or leave blank.

If this is also a **brand-new user** (no config file existed at all), additionally ask:

> **Where should sentinel save screenshots and GIFs?**
>
> Press Enter to use the default (`~/sentinel-artifacts`) or enter a custom path (e.g. `/tmp/sentinel`, `~/Desktop/sentinel-artifacts`).

#### Resolving the auth command

After collecting the answers, check whether the auth command answer looks like a **hint** or a **full command**:

- **Full command** — starts with a known executable prefix (`yarn`, `npm`, `npx`, `node`, `./`, `/`, `bash`, `sh`, `pnpm`, `bun`) → save as-is, skip discovery.
- **Hint** — anything else (e.g. `playwright cookie`, `auth token`, `get-cookie`) → run discovery below.

**Discovery — find matching scripts:**

```bash
# Collect all package.json files up to 3 levels deep
find . -maxdepth 3 -name "package.json" ! -path "*/node_modules/*" | sort
```

For each found `package.json`, read its `scripts` block. Extract every entry whose **key or value** contains any keyword from the hint (case-insensitive, partial match). Collect results as `{workspace, script_name, full_command}` where:
- `workspace` = the `name` field from that `package.json` (or the relative directory if `name` is absent)
- `full_command` = the resolved invocation, e.g. `yarn workspace <name> <script_name>` for workspace packages, or `npm run <script_name>` for the root

Also search for shell scripts:

```bash
find . -maxdepth 4 ! -path "*/node_modules/*" \( -name "*.sh" -o -name "*.bash" \) | xargs grep -li "<keyword>" 2>/dev/null
```

**Present the results:**

- **One match** → confirm with the user:

  > Found `<full_command>`. Use this as the auth command?

  Reply `yes` to accept or paste a different command.

- **Multiple matches** → list them numbered and ask:

  > Found several scripts matching your hint. Which one prints the session cookie?
  >
  > 1. `yarn workspace @acme/playwright cookie` _(apps/playwright)_
  > 2. `npm run auth:token` _(root)_
  > 3. `./scripts/get-cookie.sh`

  Reply with the number or paste a custom command.

- **No matches** → tell the user and ask for the full command:

  > Couldn't find a script matching `<hint>`. Please paste the full command that prints your session cookie to stdout (or `none` for manual login).

Save all answers into `~/.sentinel/config.json` under `projects[PROJECT_KEY]` (and update `artifacts_dir` if the user provided a custom path):

```bash
node -e "
  const fs = require('fs');
  const file = process.env.CONFIG_FILE;
  const key = process.env.PROJECT_KEY;
  const entry = JSON.parse(process.env.PROJECT_ENTRY);
  const artifactsDir = process.env.ARTIFACTS_DIR_OVERRIDE || null;
  const all = JSON.parse(fs.readFileSync(file, 'utf8').trim() || '{}');
  all.projects = all.projects || {};
  all.projects[key] = entry;
  if (artifactsDir) all.artifacts_dir = artifactsDir;
  fs.writeFileSync(file, JSON.stringify(all, null, 2));
  console.log('Config saved.');
"
```

### 4d. Prepare artifact directory

```bash
ARTIFACTS_DIR=$(node -e "
  const cfg = JSON.parse(require('fs').readFileSync(process.env.CONFIG_FILE, 'utf8'));
  const proj = cfg.projects[process.env.PROJECT_KEY] || {};
  console.log(proj.artifacts_dir || cfg.artifacts_dir || '~/sentinel-artifacts');
" | sed "s|~|$HOME|g")
```

Determine `ARTIFACT_DIR`:
- If `--folder <name>` was provided → `$ARTIFACTS_DIR/<name>`
- PR mode, no `--folder` → `$ARTIFACTS_DIR/<pr_number>`
- Manual mode, no `--folder` → derive a short slug from the instructions (e.g. "toggle dark mode 3 times" → `dark-mode-toggle`) and use `$ARTIFACTS_DIR/<slug>`

```bash
mkdir -p "$ARTIFACT_DIR"
echo "$ARTIFACT_DIR"
```

### 4e. Load nav hints

```bash
# Migrate from old location transparently
if [[ ! -f "$NAV_FILE" && -f "$HOME/sentinel-artifacts/_nav.json" ]]; then
  cp "$HOME/sentinel-artifacts/_nav.json" "$NAV_FILE"
fi

cat "$NAV_FILE" 2>/dev/null || echo "{}"
```

The nav file is a JSON object keyed by project: `{ "my-repo": { "Settings": "/settings", "Dashboard": "/dashboard" }, ... }`.

Extract the entry for `$PROJECT_KEY` as `nav_map` (a flat label→path object). If the key is absent, `nav_map` starts as `{}`.

## Step 5: Authenticate

Load auth settings from `project_config`:
- `auth_cmd` — command to run, or `"none"` for manual login
- `cookie_name` — session cookie key
- `fallback_envs` — array of fallback profiles (may be empty)

### When `auth_cmd` is set (not `"none"`):

```bash
session_cookie=$(eval "$auth_cmd" 2>/dev/null)
```

If `session_cookie` is empty and `fallback_envs` is non-empty, ask the user:

> **Auth command returned nothing. Which fallback profile should I try?**

List the `fallback_envs`. On selection, let the user guide how to pass the profile to the auth command (append as argument, set an env var, etc.), then retry.

If all attempts fail, fall back to manual login.

### When `auth_cmd` is `"none"` or all attempts fail — manual login:

```bash
agent-browser open
agent-browser set viewport 1440 900
agent-browser open <base_url>
```

Tell the user:

> **Please log in manually in the browser, then reply `ready`.**

Wait for `ready`. Then:

```bash
agent-browser state save sentinel-auth
```

Inform the user: saved auth state as `sentinel-auth` for future runs.

### Inject cookie and open app:

```bash
agent-browser open
agent-browser set viewport 1440 900
agent-browser set headers "{\"Cookie\":\"${cookie_name}=${session_cookie}\"}"
agent-browser open <base_url>
agent-browser wait --load networkidle
```

Then immediately extract the sidebar nav map and merge it into `nav_map`:

```bash
agent-browser eval "JSON.stringify(
  [...document.querySelectorAll('nav a[href]')].map(a => ({
    label: a.textContent.trim(),
    href: a.getAttribute('href')
  })).filter(x => x.label && x.href)
)"
```

Parse the result. For each `{label, href}` entry, add `label → href` to `nav_map` (sidebar wins over stale file). Persist the updated map back:

```bash
node -e "
  const fs = require('fs');
  const file = process.env.NAV_FILE;
  const key = process.env.PROJECT_KEY;
  const updated = JSON.parse(process.env.UPDATED_MAP);
  const all = JSON.parse(fs.readFileSync(file, 'utf8').trim() || '{}');
  all[key] = { ...(all[key] || {}), ...updated };
  fs.writeFileSync(file, JSON.stringify(all, null, 2));
"
```

## Step 6: Navigate and capture

Core loop — for each meaningful step:

1. `agent-browser snapshot` to read the accessibility tree
2. Decide the next action from the navigation plan
3. Execute the action
4. Screenshot after the state change lands

Screenshot naming: `step-001.png`, `step-002.png`, … zero-padded to 3 digits.

```bash
# Snapshot (navigation only — not saved)
agent-browser snapshot

# Navigate — resolve section name via nav_map first, then sidebar links, never guess
agent-browser open <base_url><nav_map["Section Name"]>

# Interact
agent-browser click @e5
agent-browser find role button click --name "Submit"

# Screenshot
agent-browser screenshot $screenshot_flag "$ARTIFACT_DIR/step-001.png"

# Wait for async state then screenshot
agent-browser wait --load networkidle
agent-browser screenshot $screenshot_flag "$ARTIFACT_DIR/step-00N.png"
```

**Navigation strategy:**
- Follow the plan from Step 2 faithfully — in manual mode, honour the exact instructions (e.g. "3 times" means exactly 3)
- **Always resolve section names through `nav_map` before navigating** — never construct a URL by guessing from a label
- If a label is missing from `nav_map`, read it from a sidebar link via `agent-browser eval "document.querySelector('nav a[text*=\"Label\"]')?.href"` before navigating
- Screenshot after every meaningful state change: page load, menu open, toggle, modal, result rendered
- Aim for 4–10 screenshots — enough to tell the story
- If you hit an unexpected state (error, redirect to login, feature not visible), stop and report — do not fabricate a happy path
- When the menu closes after an action and you need it again, re-open it with the same button before the next action

After the last screenshot:

```bash
agent-browser close
```

## Step 7: Stitch GIF

```bash
magick -delay 150 -loop 0 $(ls "$ARTIFACT_DIR"/step-*.png | sort) "$ARTIFACT_DIR/walkthrough.gif"
```

If the GIF exceeds 10 MB, reduce quality:

```bash
magick -delay 150 -loop 0 -resize 1280x -colors 128 $(ls "$ARTIFACT_DIR"/step-*.png | sort) "$ARTIFACT_DIR/walkthrough.gif"
```

```bash
du -sh "$ARTIFACT_DIR/walkthrough.gif" "$ARTIFACT_DIR"/step-*.png
```

## Step 8: Summary

```
════════════════════════════════════════
✓ sentinel complete

Artifacts: <ARTIFACT_DIR>/
  <N> screenshots: step-001.png … step-00N.png
  GIF: walkthrough.gif (<size>)
════════════════════════════════════════
```
