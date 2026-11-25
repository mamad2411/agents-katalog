---
name: sfx-sources
description: Find and download free sound effects (音效/拟音/SFX) from Mixkit, Kenney, Freesound, Pixabay. Use for any request to find or add sound effects.
allowed-tools: Bash(python3 */sfx-sources/scripts/*)
---
Order: Mixkit (general, wav) → Pixabay (huge catalog, mp3) → Kenney (UI/game packs) → Freesound (rare foley, mp3).

```
S=${CLAUDE_SKILL_DIR}/scripts/sfx.py
python3 $S mixkit <tag>                    # one English word
python3 $S kenney [pack]                   # no pack: list packs
python3 $S freesound "<q>"                 # all CC; non-CC0 needs credit
python3 $S pixabay "<q>"                   # English query; ranked by ♥likes; Pixabay license, no credit
python3 $S get <dir> <key>...              # parallel download
```
`--urls` on a search adds preview links for the user to audition.

- Freesound caps ~80 KB/s per connection: put all keys in one `get`.
- Pixabay is behind Cloudflare; the script auto-uses a curl_cffi venv in ~/.cache/sfx-sources/venv (built on first call). Results come ranked by likes (♥, ↓ = downloads) across `--pages` (default 3 × 20) relevance pages: prefer the highest-♥ clip that fits the cue, and say the ♥ count when proposing it. If it starts returning 403, Cloudflare tightened — fall back to WebFetch on the search page for titles.
