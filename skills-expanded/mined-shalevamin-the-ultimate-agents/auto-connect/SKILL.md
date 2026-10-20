---
name: auto-connect
description: Automatically detect installed apps, running services, and logged-in accounts — then connect to them without asking the user. Use when starting a new task to understand what tools are available, when the user mentions an app, or when you need to figure out how to accomplish something without manual user steps.
allowed-tools: Bash
user-invocable: false
---

# Auto-Connect — Detect and Use Everything Available

Scan the user's environment and automatically connect to all available tools, apps, and services.

## RUN THIS FIRST (at session start)

```bash
# Load environment
ENV_FILE="$(find ~ -name '.env' -path '*/tua-agent/*' 2>/dev/null | head -1)"
[ -f "$ENV_FILE" ] && source "$ENV_FILE" 2>/dev/null || true

echo "=== TUA AGENT — ENVIRONMENT SCAN ==="
echo ""

# ── INSTALLED APPS ──
echo "📱 INSTALLED APPS:"
apps=("Google Chrome" "Safari" "Firefox" "Microsoft Word" "Microsoft Excel" "Microsoft PowerPoint" "Slack" "Visual Studio Code" "Notion" "Figma" "Xcode" "Discord" "Zoom" "Spotify" "1Password" "Obsidian" "Linear" "Things 3" "Bear" "Mailmate" "Airmail" "Spark" "Finder")
for app in "${apps[@]}"; do
    if [ -d "/Applications/$app.app" ] || [ -d "$HOME/Applications/$app.app" ]; then
        echo "  ✅ $app"
    fi
done

# ── RUNNING PROCESSES ──
echo ""
echo "🔄 RUNNING:"
pgrep -x "Google Chrome" >/dev/null && echo "  ✅ Chrome (active — accounts likely logged in)"
pgrep -x "Safari" >/dev/null && echo "  ✅ Safari (active)"
pgrep -x "Slack" >/dev/null && echo "  ✅ Slack (active — can send messages)"
pgrep -x "Discord" >/dev/null && echo "  ✅ Discord (active)"
pgrep -x "Zoom" >/dev/null && echo "  ✅ Zoom (active)"
pgrep -x "Spotify" >/dev/null && echo "  ✅ Spotify (active — can control playback)"
pgrep -x "Code" >/dev/null && echo "  ✅ VS Code (active)"

# ── CLI TOOLS ──
echo ""
echo "🛠️  CLI TOOLS:"
command -v node &>/dev/null && echo "  ✅ Node.js $(node --version)"
command -v python3 &>/dev/null && echo "  ✅ Python $(python3 --version 2>&1 | cut -d' ' -f2)"
command -v git &>/dev/null && echo "  ✅ Git $(git --version | cut -d' ' -f3)"
command -v docker &>/dev/null && echo "  ✅ Docker $(docker --version 2>&1 | cut -d' ' -f3)"
command -v brew &>/dev/null && echo "  ✅ Homebrew"
command -v npm &>/dev/null && echo "  ✅ npm $(npm --version)"
command -v pip3 &>/dev/null && echo "  ✅ pip3"
command -v uv &>/dev/null && echo "  ✅ uv (fast Python)"
command -v gh &>/dev/null && echo "  ✅ GitHub CLI"
command -v aws &>/dev/null && echo "  ✅ AWS CLI"
command -v gcloud &>/dev/null && echo "  ✅ Google Cloud CLI"

# ── PYTHON PACKAGES ──
echo ""
echo "🐍 PYTHON PACKAGES:"
python3 -c "import browser_use" 2>/dev/null && echo "  ✅ browser-use (AI browser automation)"
python3 -c "import playwright" 2>/dev/null && echo "  ✅ playwright (browser control)"
python3 -c "import pyautogui" 2>/dev/null && echo "  ✅ pyautogui (GUI automation)"
python3 -c "import anthropic" 2>/dev/null && echo "  ✅ anthropic SDK"
python3 -c "import openai" 2>/dev/null && echo "  ✅ openai SDK"
python3 -c "import langchain_anthropic" 2>/dev/null && echo "  ✅ langchain-anthropic"
python3 -c "import pandas" 2>/dev/null && echo "  ✅ pandas (data analysis)"
python3 -c "import PIL" 2>/dev/null && echo "  ✅ Pillow (image processing)"
python3 -c "import requests" 2>/dev/null && echo "  ✅ requests (HTTP)"

# ── BROWSER TABS ──
echo ""
echo "🌐 CHROME TABS (active sites you're likely logged into):"
osascript 2>/dev/null << 'AS'
tell application "Google Chrome"
    if it is running then
        set allURLs to {}
        repeat with w in windows
            repeat with t in tabs of w
                set end of allURLs to URL of t
            end repeat
        end repeat
        repeat with u in allURLs
            -- Show logged-in platforms
            if u contains "google.com" or u contains "docs.google.com" then
                log "  ✅ Google (Docs/Sheets/Slides available)"
            end if
            if u contains "notion.so" then
                log "  ✅ Notion (open)"
            end if
            if u contains "github.com" then
                log "  ✅ GitHub (logged in)"
            end if
            if u contains "linear.app" then
                log "  ✅ Linear (open)"
            end if
            if u contains "figma.com" then
                log "  ✅ Figma (open)"
            end if
            if u contains "slack.com" then
                log "  ✅ Slack web (open)"
            end if
        end repeat
    end if
end tell
AS

# ── API KEYS ──
echo ""
echo "🔑 API KEYS:"
[ -n "$ANTHROPIC_API_KEY" ] && echo "  ✅ Anthropic API key (configured)" || echo "  ❌ ANTHROPIC_API_KEY not set — run setup.sh"
[ -n "$OPENAI_API_KEY" ] && echo "  ✅ OpenAI API key"
[ -n "$GOOGLE_API_KEY" ] && echo "  ✅ Google API key"

# ── GIT CONFIG ──
echo ""
echo "📋 GIT:"
git config --global user.name 2>/dev/null && echo "  ✅ Git user: $(git config --global user.name)"
git config --global user.email 2>/dev/null && echo "  ✅ Git email: $(git config --global user.email)"

echo ""
echo "=== SCAN COMPLETE ==="
echo "Tua Agent is now connected to all available tools."
```

## AUTO-INSTALL MISSING TOOLS

If a tool is needed but not installed:

```bash
# Install browser automation
pip3 install --user browser-use playwright langchain-anthropic 2>/dev/null
python3 -m playwright install chromium 2>/dev/null

# Install GUI automation
pip3 install --user pyautogui pillow 2>/dev/null

# Install GitHub CLI
brew install gh 2>/dev/null

# Install Node packages
npm install -g @anthropic-ai/claude-code 2>/dev/null || npx @anthropic-ai/claude-code --help 2>/dev/null
```

## CONNECT TO APPS WITHOUT USER ACTION

### Microsoft Word (if installed)
```bash
# Create new Word document
osascript << 'AS'
tell application "Microsoft Word"
    activate
    set newDoc to make new document
    set content of text object of newDoc to "DOCUMENT_CONTENT"
    save newDoc in (POSIX file "/tmp/tua-document.docx")
end tell
AS
```

### Google Docs (via Chrome — user already logged in)
```bash
osascript -e 'tell application "Google Chrome" to open location "https://docs.google.com/document/create"'
sleep 3
# Then use keyboard to paste content
osascript << 'AS'
tell application "System Events"
    keystroke "DOCUMENT_CONTENT"
end tell
AS
```

### Slack (if running)
```bash
# Send message to a Slack channel
osascript << 'AS'
tell application "Slack"
    activate
end tell
AS
# Then use keyboard shortcut to open channel
```

### Spotify (control playback)
```bash
osascript -e 'tell application "Spotify" to play track "spotify:track:TRACK_ID"'
osascript -e 'tell application "Spotify" to pause'
osascript -e 'tell application "Spotify" to next track'
```

### Calendar (add event)
```bash
osascript << 'AS'
tell application "Calendar"
    tell calendar "Work"
        make new event with properties {summary:"EVENT_TITLE", start date:date "EVENT_DATE", end date:date "EVENT_END"}
    end tell
end tell
AS
```

## RESULT FORMAT

After scanning, output a capabilities summary:
```
🤖 TUA AGENT — READY

Available tools:
• Browser: Chrome (logged in as USER@gmail.com)
• Documents: Google Docs ✓, Word ✓
• Communication: Slack ✓
• Code: VS Code ✓, Python ✓, Node ✓
• AI: Anthropic ✓ (single API key)

What would you like to build?
```
