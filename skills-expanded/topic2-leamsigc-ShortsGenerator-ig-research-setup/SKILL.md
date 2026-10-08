---
name: ig-research-setup
version: 1.0.0
description: |
  Setup state for social research tool. Checks prerequisites, creates directory
  structure, creates config.json, installs deps, sets up Chrome for scraping.
  Call this before any other research state.

allowed-tools:
  - Bash
  - Read
  - Write
  - Question
---

# Social Research — Setup State

Run this first. It checks prerequisites, creates the project, and sets up Chrome.

## Steps

### 1. Check prerequisites

Check each of these. Ask user for permission before installing anything missing.

- **Homebrew** (Mac only): `brew --version`
- **Node.js** (v18+): `node --version`
- **Python 3**: `python3 --version`
- **ffmpeg**: `ffmpeg -version`
- **yt-dlp**: `yt-dlp --version` or `pip3 list 2>/dev/null | grep yt-dlp`
- **openai-whisper**: `pip3 list 2>/dev/null | grep whisper`

Install commands:
- Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
- Node (Mac): `brew install node`
- ffmpeg (Mac): `brew install ffmpeg` | (Windows): `winget install ffmpeg`
- yt-dlp: `pip3 install yt-dlp`
- whisper: `pip3 install openai-whisper`

### 2. Create project directory

```bash
SESSION=$(date +%Y-%m-%d_%H%M%S)
mkdir -p .ig-research/projects/<project-name>/$SESSION
mkdir -p .ig-research/projects/<project-name>  # legacy root for back-compat
```

### 3. Create config.json

Ask the user:
1. "What's your niche? (e.g., fitness coaching, real estate, personal branding)"
2. "What platform? (instagram, facebook, linkedin, x, youtube)"
3. "What are 1-3 hashtags/keywords?"
4. "Any competitor accounts to analyze?"
5. "How many posts per keyword?"

Create `.ig-research/projects/<project-name>/config.json`:

```json
{
  "name": "Project Name",
  "niche": "Niche description",
  "platform": "instagram",
  "searchTerms": ["keyword1", "keyword2"],
  "competitors": ["https://www.instagram.com/handle/"],
  "browserPort": 9222,
  "maxPostsPerSearch": 50,
  "maxCompetitorPosts": 10
}
```

### 4. Install Node dependencies

```bash
npm install --prefix "$CLAUDE_SKILL_ROOT/scripts"  # ~/.claude/skills/ig-research/scripts
# fallback: npm install --prefix ./skills/ig-research/scripts
```

### 5. Set up Chrome

Tell the user:

> "Close Chrome completely (Cmd+Q on Mac, not just closing the window), then reopen it with:"
>
> Mac: `/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222`
>
> "Once Chrome opens, go to instagram.com and log in. Then come back and tell me when you're ready."

Wait for user confirmation before finishing.
