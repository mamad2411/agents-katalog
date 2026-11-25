---
name: mulmoterminal-notify
description: Decide which moments MulmoTerminal beeps or pushes for, and what each one plays — `soundKinds`, `sounds` and `pushKinds` in `~/.mulmoterminal/config.json`, plus a per-project `sound` / `sounds` in `<project>/.mulmoterminal.json` so one repo can have its own chime. Six moments exist (a turn finished, the agent is waiting on you, a Run command succeeded or failed, a session exited, a PR's CI went red) but only two beep by default; the rest are opt-in. The per-project ones are also set in Settings → Directory settings → Change here. Use when the user says notifications are too noisy or too quiet, wants a sound only when an agent is waiting, wants a different sound per project or per event, wants to know when CI fails or a command finishes, or asks why their phone isn't getting notified.
---

# Which moments notify you, and how

Running several agents at once is what turns notifications into noise, so the defaults are
deliberately narrow: **only `finished` and `waiting` beep**, and the other four are opt-in.

Ask what they actually want to be interrupted for before changing anything. "Turn on all six" is
almost never the right answer.

## The six moments

| Kind | Fires when | Beeps by default |
|---|---|---|
| `finished` | The turn ended; output is waiting to be reviewed | **yes** |
| `waiting` | The agent is blocked on input — a permission prompt or a question | **yes** |
| `command-done` | A Run cell's command exited 0 | no |
| `command-failed` | A Run cell's command exited non-zero | no |
| `session-exited` | A session's PTY ended | no |
| `pr-ci-failed` | A directory's PR phase became CI-failing | no |

Two of these have caveats worth saying out loud:

- **`session-exited` fires when you close a cell yourself.** Closing goes through the same path, so
  someone who enables it will hear it on every deliberate close and think it is misfiring.
- **`pr-ci-failed` is only seen while the roster is on screen.** The phase poll doesn't run
  otherwise, so a failure that lands while the user is in another view is never noticed. It is not
  a background CI watcher; don't offer it as one.

## Sound — global

Settings has a UI for this (**Notification sounds**), so use this skill when the user wants
something the UI makes tedious — a different sound per moment, or per project.

```json
{
  "soundKinds": ["finished", "waiting", "command-failed"],
  "sounds": { "waiting": "preset:coin", "command-failed": "preset:gong" },
  "soundFile": "/Users/you/sounds/done.mp3"
}
```

- **`soundKinds`** — which moments beep. Omit to keep `["finished", "waiting"]`; `[]` for silence.
  Listing a kind here is what makes it audible at all — a `sounds` entry for a kind that isn't in
  `soundKinds` plays nothing.
- **`sounds`** — per-kind sound. A `preset:<id>` or an **absolute** path. A kind with no entry falls
  back to `soundFile`, and then to the built-in chime.
- **`soundFile`** — the fallback for every kind. Absolute path.

Presets: `preset:chime` · `preset:coin` · `preset:cheep` · `preset:door` · `preset:gong` ·
`preset:magic` · `preset:meow`.

The preset audio is **fetched once** from GitHub into `~/.mulmoterminal/sounds/` and served locally
afterwards, so it keeps working offline — but the **first** play of a preset needs the network. If
the user is offline and a new preset is silent, that is why; it isn't a config error.

Partial `POST /api/config` merge — write only the keys you are changing, and send each of them
**complete**. `sounds` is an object, but it is replaced whole exactly as `soundKinds` is: posting
`{"sounds": {"waiting": "preset:coin"}}` deletes every other kind's sound, with no warning and a
successful response. Read the current `sounds` from `GET /api/config`, add your entry to that map,
and send the merged map back.

## Sound — per project

`<project>/.mulmoterminal.json`. Settings → Directory settings → **Change here** sets one directory's
`sound` and per-kind `sounds` (a preset or a file in the directory); this skill is for setting it up
across projects, or explaining what a moment plays: one repo that beeps differently so you know
which one called you.

```json
{ "sound": "./sounds/done.wav", "sounds": { "waiting": "preset:coin", "command-failed": "./sounds/bad.wav" } }
```

- **`sound`** — this directory's fallback for every kind.
- **`sounds`** — per-kind.
- Both accept **either** a `preset:<id>` **or** a relative file path. (Before 8.0.0 `sound` took a
  file path only and silently dropped a preset; a file written for that version still works.)
- **A file path here must be RELATIVE to the project.** Absolute paths and `../` escapes are
  **rejected**, and the resolved path is canonicalised so a symlink pointing outside the project is
  rejected too — a project you open must not be able to make the player read arbitrary files. This
  is the opposite rule from the global file, where paths must be **absolute**; pasting an absolute
  path into the project file is the most common mistake, and it fails silently.
- **The file must exist**, or the entry resolves to nothing. If it is gitignored, say that a
  colleague cloning the project gets silence, not an error.
- A per-kind sound still only plays if that kind is in the **global** `soundKinds`. A project cannot
  switch a moment on for itself.

Writing the file with your Write/Edit tool is itself the live-reload signal — there is no filesystem
watcher. It applies immediately.

## Web Push — `pushKinds`

Push reaches a phone, so it can only carry what the **server** observes:

```json
{ "pushEnabled": true, "pushKinds": ["finished", "waiting"] }
```

- **Only `finished` and `waiting` can push.** The other four are seen in the browser, not on the
  server, so they cannot be delivered to a phone — if the user asks for a push on CI failure or a
  command exiting, say plainly that it isn't available rather than writing a key that does nothing.
- `pushEnabled` is the master switch, off by default. Settings has a toggle for it and for the
  kinds; the subscription itself is set up there, so **send the user to Settings to enable push**
  rather than writing `pushEnabled: true` into the file — a flag with no subscription behind it
  delivers nothing.

## After writing

- **Per-project sound**: live.
- **Global**: read by the page — **reload the tab**. A hand-edit while the server is running also
  needs a restart.
- Settings' sound rows have a **play button per kind**. That is the check: it plays exactly what
  that moment will play, including a per-kind override.

## "The config is right and it still doesn't beep"

Browsers refuse to play audio until the page has been clicked or typed in, and that permission is
per page load — so a tab that was reloaded and then left alone is silent no matter what the config
says. It is not a config error and there is nothing to write.

- The toolbar's sound button shows it: **amber with a paused bell** means blocked, blue means
  playing. Any click or keypress anywhere on the page clears it.
- Nothing raised while blocked is lost. One beep plays when the page unblocks, and every session
  whose notification went unheard keeps an **amber ring on its status dot** until you look at it.
- The same ring appears for a session that was ALREADY waiting when the tab loaded: the page has
  no way to announce something that happened before it existed.
