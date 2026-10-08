# Suno Music Skill - AI Music Generation via Browser Automation

Generate full songs (vocals + instrumentals) using Suno.com via Playwright browser automation.

## First-Time Setup

```bash
# 1. Log in to Suno visibly (one-time)
python3 ~/.claude/skills/suno-skill/suno_skill.py login

# This opens a visible browser. Log in with your Google/Discord/Apple account.
# Once logged in, close the browser — session is saved.

# 2. Verify it works
python3 ~/.claude/skills/suno-skill/suno_skill.py create "upbeat indie rock song about coding at 3am"
```

## Commands

### Login (one-time, visible browser)
```bash
python3 ~/.claude/skills/suno-skill/suno_skill.py login
```

### Create a Song
```bash
python3 ~/.claude/skills/suno-skill/suno_skill.py create "PROMPT" [--style "STYLE"] [--instrumental] [--output DIR]
```

**Arguments:**
- `PROMPT` - Song description or lyrics
- `--style` - Musical style tag (e.g., "kawaii metal", "lo-fi hip hop", "80s synthwave")
- `--instrumental` - Generate instrumental only (no vocals)
- `--output` - Directory to save downloaded audio (default: ./output)
- `--wait` - Max seconds to wait for generation (default: 120)

### Download a Song by URL
```bash
python3 ~/.claude/skills/suno-skill/suno_skill.py download "https://suno.com/song/SONG_ID" [--output DIR]
```

### List Recent Creations
```bash
python3 ~/.claude/skills/suno-skill/suno_skill.py list [--limit 10]
```

## Examples

```bash
# Generate a kawaii metal track
python3 ~/.claude/skills/suno-skill/suno_skill.py create \
  "aggressive kawaii metal song about fighting robots in Tokyo" \
  --style "kawaii metal, japanese, heavy guitar"

# Generate an instrumental lo-fi beat
python3 ~/.claude/skills/suno-skill/suno_skill.py create \
  "chill lo-fi study beat with rain sounds and soft piano" \
  --instrumental --style "lo-fi hip hop, chill, ambient"

# Generate with full lyrics
python3 ~/.claude/skills/suno-skill/suno_skill.py create \
  "[Verse 1]\nWaking up at 3am\nScreen light in my eyes again\n[Chorus]\nWe're building something new tonight" \
  --style "indie rock, upbeat"
```

## Output

Returns JSON:
```json
{
  "success": true,
  "songs": [
    {
      "title": "Robot Wars in Tokyo",
      "url": "https://suno.com/song/abc123",
      "audio_url": "https://cdn.suno.com/...",
      "file": "./output/robot_wars_in_tokyo.mp3",
      "duration": "3:24",
      "style": "kawaii metal"
    }
  ]
}
```

## Notes

- Suno generates 2 variations per prompt. Both are downloaded.
- Free tier: 10 generations/day (50 songs/month). Pro: 500/month ($10/mo). Premier: 2000/month ($30/mo).
- Songs are saved with sanitized filenames.
- Session persists across runs — only need to login once.
- **ToS consideration:** Browser automation is not officially supported by Suno. Use at your own discretion.

## Requirements

- Python 3.9+
- `pip install playwright`
- `playwright install chromium`
