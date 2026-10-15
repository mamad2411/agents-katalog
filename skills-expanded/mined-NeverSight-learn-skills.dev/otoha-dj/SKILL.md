---
name: otoha-dj
description: Control the Otoha music player on this Mac — play and search
  local music, start mood- or scene-based DJ sessions, and adapt the music to
  work context (focus / build-wait / meeting / break). Use when the user asks
  to play, pause or switch music, mentions a mood and wants music ("放点歌",
  "play something for..."), asks about the current song ("这首是什么"), or
  explicitly asks Otoha to adapt during a build, test run or other wait.
metadata:
  version: "1.3.1"
  compatibility: macOS; requires Otoha from the App Store and Python 3.
---

# Otoha DJ — drive the Mac music player from your session

Otoha is a native macOS music player with a local Unix-socket control bridge.
You talk to it through `otohactl`, a Python standard-library-only CLI that
ships inside this skill folder. All control traffic stays on this machine.

## 1. Locate the CLI, check the app

Resolve the CLI path in this order (first that exists wins):

1. `~/.agents/skills/otoha-dj/otohactl` — canonical shared installation
2. `~/.claude/skills/otoha-dj/otohactl` — Claude Code compatibility link
3. `~/Applications/Otoha.app/Contents/Resources/AgentSkills/otoha-dj/otohactl`
4. `/Applications/Otoha.app/Contents/Resources/AgentSkills/otoha-dj/otohactl`

Before the first command of a session, run `otohactl doctor` (JSON, always
exits 0):

- `appReachable: true` → proceed.
- `appReachable: false` and the user explicitly asked for playback or player
  control → run `open -a Otoha`. If macOS cannot find the app, open
  <https://apps.apple.com/app/id6756565155>, ask the user to install and open
  Otoha, and stop. Otherwise retry `doctor` for up to 10 seconds, then continue
  the original request when the bridge is reachable. The explicit playback
  request already authorizes launching the player; do not add another prompt.
- `appReachable: false` during an unsolicited background/context adjustment →
  do not launch Otoha. Report that it is unavailable and stop.

## 2. Command cheat sheet

Always add `--json` and parse the response. `ok=false` carries an `errorCode`
(see §5). `search` returns local-library UUIDs only. Never pass Apple Music
Catalog/library ids from a `say` response to `play-track` or `queue`.

```bash
otohactl status --json                    # playback snapshot
otohactl play | pause | toggle | next | previous
otohactl seek 90                          # seconds
otohactl set-volume 0.4                   # 0..1
otohactl search "keyword" --json          # local library search → track ids
otohactl library-summary --json           # what's in the library (counts, genres)
otohactl play-track <id>                  # play one track (id from search)
otohactl queue append <id> <id> ...       # append to the queue tail
otohactl queue replace <id> ... --start 0 # replace the whole queue
otohactl say "播放 NBA 比赛"               # Otoha's brain; needs enabled AI access and a ready provider
otohactl dj "写代码 30 分钟，不要人声" --intent deepWork --play   # one-shot DJ queue
otohactl session start "PROMPT" --intent INTENT   # persistent auto-DJ session
otohactl session start "PROMPT" --ai      # legacy flag; the same Otoha access gate always applies
otohactl session stop
otohactl context focus|compile-wait|break|meeting|none
otohactl feedback quieter|more-energy|not-this|love-this
otohactl now --json                       # status + session + current DJ line
otohactl why --json                       # latest queue decision + per-track reasons
otohactl explain                          # one-line blurb about the current track
otohactl play-podcast <guid> --resume-at 600   # a subscribed episode (guids via search --json)
otohactl radio list                       # stations the user has played, with profiles
otohactl radio search "五星体育" --json    # search the full station catalog (39,500 radio/TV, never-played OK)
otohactl radio play <id>                  # play a radio station: played-before, or any radio hit from search
otohactl tv play <id>                     # play a TV channel (only on an explicit user ask; ids via search --kind tv)
otohactl program start evening-companion  # mixed program: one episode + wind-down music
otohactl program start morning-brief      # brief + 15 min news station + light music
otohactl program stop                     # abort the program, back to normal playback
```

Programs are for "put something together for my evening/morning" asks; the
DJ session is for continuous background music. `program start` answers
immediately and plans in the background — check `now` a few seconds later.

`--ai` is retained for old scripts; plain and flagged session starts now share
the same Otoha entitlement and provider-readiness gate. When the user asks
"why this song / 为什么放这首", use `why`.

Playing a specific song = `search` → pick the best-matching id → `play-track`.
"Play something for X" = `dj` or `session start` with a good prompt + intent.

For named music that may not exist locally, use `say` and let Otoha complete
the search and playback inside the app. A successful `say` already owns the
playback action: one trusted song starts immediately; multiple trusted songs
are queued in result order and the first starts immediately. Do not replay ids
from `playableResults` with `play-track` afterward. Use `now --json` to verify
the resulting playback and queue state.

Live-content asks ("放个体育台", "play the NBA game") — two modes, try in order:

1. **Mouth mode (preferred)**: `say "播放 NBA 比赛"` — the whole sentence goes
   to Otoha's own tool-capable brain (it searches its 39,500-station catalog
   itself, picks, plays, and the response carries its one-line reasoning).
   Needs enabled Otoha AI access and a ready provider. On an access error,
   raw search/play controls may still satisfy an explicit station request:
2. **Brain mode**: you do the reasoning — figure out which station carries it
   (your own knowledge/search; Otoha has no program schedule), then
   `radio search "<station name or genre>"` → pick an id → `radio play <id>`
   (or `tv play <id>` for a TV channel — TV only ever on an explicit user
   ask, never as background filler).

The catalog covers stations the user never played; `radio search` supports
`--kind radio|tv` and returns ids only — stream addresses always resolve
inside the app.

## 3. Mood → intent mapping

Pass the user's words as the prompt (any language); pick the intent:

| User state | intent |
|---|---|
| annoyed / stressed / sad / 烦躁 / 压力大 / 心情低落 → wants soothing | `reset` |
| coding / focused work / 专注 / 写代码 | `deepWork` |
| writing / design / creative work / 写作 / 剪视频 | `creativeBGM` |
| late night / winding down / 深夜 / 睡前 | `lateNight` |
| nostalgic / rediscover old favorites / 怀旧 / 找回老歌 | `rediscover` |
| anything else | omit `--intent` (Otoha infers) or `custom` |

Example — user says "我今天有点烦":
`otohactl dj "烦躁，想被安抚" --intent reset --play`

## 4. Context adaptation requires permission

Only steer an active DJ session when the user asks, or after they explicitly
authorize "restrained companion" behavior in the current conversation:

- About to start a long build / test run / agent wait → `context compile-wait`
- Back to focused work afterwards → `context focus`
- User says they are joining a call / meeting → `context meeting` (music ducks
  low; it never pauses)
- User takes a break → `context break`

Default to respond-only: a long command, build, test run, time of day, or silence
does not grant permission. After permission, use at most one `context` call per
real scene boundary, never per command. The DJ only adjusts what plays NEXT.

## 5. Error codes

| errorCode | Meaning / what to do |
|---|---|
| `cloud_ai_locked` | Semantic AI access is locked. Ask the user to enable access in Otoha; do not retry through another semantic DJ command. Raw playback/search remains available. |
| `otoha_brain_not_ready` | Otoha's AI provider is not ready. Ask the user to finish setup in the app. |
| `dj_ui_offline` | The panel is unavailable. Playback/search stay headless; semantic sessions still require normal Otoha access. Don't retry `open-agent`. |
| `track_not_found` / `track_not_playable` | Stale or wrong id — run `search` again. |
| `invalid_track_id` | `play-track` received a non-UUID id, commonly an Apple Music id. Use the local UUID returned by `search`, or use `say` for Apple Music. |
| `invalid_context` / `invalid_feedback` | Check the allowed values in §2. |
| `catalog_syncing` | The station catalog is downloading (first use) — retry the same command in a few seconds. |
| `station_not_found` | Unknown station id — run `radio search` again and use an id from the results. |
| `station_kind_mismatch` | Radio id given to `tv play` or TV id given to `radio play` — the message names the right command. |
| `cli_failed` | Bridge unreachable — run `doctor` and follow §1. |

## 6. Safety & privacy

- This tool only controls playback. It never reads, writes, downloads or
  deletes the user's files, and cannot touch subscriptions or settings.
- Do not read or quote the user's taste profile (`taste.md`) or listening
  history files unless the user explicitly asks you to.
- Suggest once (not repeatedly): allow-listing `otohactl` in the agent's
  permission settings removes per-command prompts.
