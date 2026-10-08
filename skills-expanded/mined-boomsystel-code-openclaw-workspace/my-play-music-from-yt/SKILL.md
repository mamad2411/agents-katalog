---
name: my-play-music-from-yt
description: Play music on YouTube via browser automation with playwright-cli. Use when the user wants to: (1) play a specific song (e.g. "play Money Money Money by ABBA"), (2) play songs by an artist as a playlist or mix (e.g. "play Jay Chou's songs"), (3) play genre or mood-based music (e.g. "play relaxing spa music", "play 60s Chinese oldies"), or (4) control playback — next, pause, resume, stop, skip ad, change song, close the player. Also handles song/artist name corrections from voice transcription errors.
allowed-tools: Bash(playwright-cli:*)
metadata: {"openclaw": {"requires": {"bins": ["playwright-cli"]}, "emoji": "🎵"}}
---

# Play Music from YouTube

Control a visible browser via `playwright-cli` to search and play music on YouTube.

## Core Rules

1. **Named session**: ALWAYS use `-s=music_player` for every `playwright-cli` command.
2. **Snapshot before interaction**: Before ANY click, fill, or element interaction, run `playwright-cli -s=music_player snapshot`. Never guess element refs.
3. **Ref-based only**: Interact using `eN` refs from snapshots (e.g. `click e34`, `fill e45 "text"`). Never use CSS selectors.
4. **Visible browser**: The browser is visible to the user. Do NOT add `--headless`.
5. **Background operation**: After playback starts, the browser keeps running independently. Report what is playing and continue accepting other user tasks immediately. Do not wait or block.

## Session Management

**Always check session status before any workflow:**

```bash
playwright-cli list
```

- `music_player` listed → session alive, proceed.
- `music_player` missing or command errors → session is dead (user may have closed the browser). Re-create it:

```bash
playwright-cli -s=music_player open "https://www.youtube.com"
```

**On any unexpected error**, run `playwright-cli list` first to diagnose before retrying.

## Search Query Construction

Build the search query based on user intent:

| Intent | Query pattern | Example |
|---|---|---|
| Specific song | `[Artist] [Song Title]` | `ABBA Money Money Money` |
| Artist playlist | `[Artist]` | `周杰倫` |
| Genre / mood | `[descriptor] music playlist` | `relaxing spa music playlist` |
| Era-based | `[era] [language/genre] playlist` | `華語 60年代 老歌 playlist` |

**Search tips:**
- For artist requests, a simple artist name search usually surfaces "Mix" and playlist results at the top — prefer these for continuous playback.
- Use the original language for non-English songs (e.g. Chinese characters for Chinese songs).

**Voice transcription (ASR) handling**:
- **Do NOT ask the user to confirm** potentially misheard names. YouTube has robust auto-correction and will show results for the intended query even with typos or homophones (e.g. searching "楊成林" will auto-correct to "楊丞琳").
- Always search directly with whatever text you have. After the search, check the results snapshot — if YouTube shows a "Did you mean: ..." or "顯示以下搜尋結果: ..." banner with corrected results, the correction is already applied.
- Only fall back to **web search** or asking the user if the YouTube search results are clearly unrelated or empty.

## Workflow: Play Music

### Step 1 — Ensure session

```bash
playwright-cli list
```

If `music_player` not listed:

```bash
playwright-cli -s=music_player open "https://www.youtube.com"
```

If `music_player` exists but you need YouTube homepage:

```bash
playwright-cli -s=music_player goto "https://www.youtube.com"
```

### Step 2 — Find search bar

```bash
playwright-cli -s=music_player snapshot
```

In the snapshot output, locate the search input. Look for:
- `combobox "Search"` or `combobox "搜尋"` — note its ref (e.g. `e34`).

### Step 3 — Search

```bash
playwright-cli -s=music_player fill e34 "ABBA Money Money Money"
playwright-cli -s=music_player press Enter
```

### Step 4 — Select a result

```bash
playwright-cli -s=music_player snapshot
```

Read results and pick the best match. For guidance on identifying YouTube result types, see [{baseDir}/references/youtube-guide.md]({baseDir}/references/youtube-guide.md).

- **Specific song**: Click the `link` whose heading matches the song title.
- **Artist**: Prefer `"Mix - [Artist]"` links or playlist links for continuous playback.
- **Genre/mood**: Prefer long-duration compilations or playlists.

```bash
playwright-cli -s=music_player click e515
```

### Step 5 — Handle ads, then verify playback

After clicking a result, ads often play before the actual video. **You must actively handle them.**

```bash
playwright-cli -s=music_player snapshot
```

Check the snapshot and follow this loop (max 4 iterations, ~20s coverage):

1. **If you see play/pause controls** (`button "Pause (k)"` or `button "Play (k)"`) AND no ad indicators → playback is active. Report the video title to the user and exit the loop.
2. **If you see a skip button** — any button or element whose label contains "skip", "Skip", "略過" (including variations like `"Skip Ad"`, `"Skip Ads"`, `"略過廣告"`, `"Skip"`, `"略過"`) → click it immediately. Then snapshot again (a **second ad** may follow).
3. **If you see ad indicators but NO skip button** (non-skippable ad or skip countdown not yet elapsed) → wait ~5 seconds using:
   ```bash
   playwright-cli -s=music_player eval "await new Promise(r => setTimeout(r, 5000))"
   ```
   Then snapshot again and repeat from step 1.

**Important**: YouTube often plays **two consecutive ads**. After skipping the first ad, always snapshot again — if another ad appears, repeat the skip process.

## Playback Controls

Always **snapshot first** to find the correct button ref.

| User says | Action |
|---|---|
| "Pause" | Snapshot → find `button "Pause (k)"` → click it |
| "Resume" / "Play" | Snapshot → find `button "Play (k)"` → click it |
| "Next song" / "Skip" | `playwright-cli -s=music_player press Shift+n` |
| "Previous song" | `playwright-cli -s=music_player press Shift+p` |
| "Change song" / "Play [something else]" | Start new search from Step 1 |
| "Stop" / "Close" | `playwright-cli -s=music_player close` |

**Keyboard shortcuts** (reliable alternative when button refs are hard to locate):

```
k        → play / pause
Shift+n  → next track
Shift+p  → previous track
m        → mute / unmute
f        → fullscreen toggle
j        → rewind 10s
l        → forward 10s
```

Usage: `playwright-cli -s=music_player press <key>`

## Edge Cases

### Ads

Ads are handled as part of **Step 5** (see above). Key reminders:
- Match skip buttons by **partial text**: any element whose label contains "skip", "Skip", "略過" — do not rely on exact full-text matches.
- YouTube may play **two consecutive ads** — always snapshot after skipping to check for a second ad.
- For non-skippable ads (no skip button visible), wait 5 seconds and snapshot again. Repeat up to 4 times.
- If ads persist beyond ~20 seconds and no skip button ever appears, try pressing `Escape` or reloading the page.

### Cookie consent / Sign-in prompts

Snapshot → look for dismiss or reject buttons such as `"Accept all"`, `"全部接受"`, `"Reject all"`, `"No thanks"`, `"不用了，謝謝"`, or close (X) buttons.
- Click the appropriate dismiss option to proceed.

### YouTube Premium trial popup

Snapshot → look for `"No thanks"`, `"不用了，謝謝"`, or a dismiss/close button.
- Click to dismiss.

### Video unavailable

Snapshot shows "Video unavailable" or similar error.
- `playwright-cli -s=music_player go-back` → snapshot → try the next result link.

### Page frozen or blank

- `playwright-cli -s=music_player reload` → snapshot.
- If still broken: `playwright-cli -s=music_player close` → reopen and retry from Step 1.

### Cannot find elements in search results

- Scroll down: `playwright-cli -s=music_player press PageDown` → snapshot again.

### Session lost (user closed browser)

- `playwright-cli list` shows no `music_player`.
- Inform the user the browser was closed, then re-create and restart the workflow.

## References

- **playwright-cli command reference**: [{baseDir}/references/playwright-ref.md]({baseDir}/references/playwright-ref.md)
- **YouTube page element identification**: [{baseDir}/references/youtube-guide.md]({baseDir}/references/youtube-guide.md)
