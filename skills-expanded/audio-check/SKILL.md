---
name: audio-check
description: "Checks, repairs, or sets up a browser game's audio: its sound settings and whether sound actually plays under each browser's conditions. Use when a game is silent, or goes silent, on a phone, in Safari, inside an iframe or an in-app browser while it plays elsewhere; when sound works for the builder but not for players; when music does not start, loops with a gap, or keeps playing in a hidden tab; when volume, mute, or sound settings are missing, ignored on some device, or forgotten between sessions; when the user asks to add sound or music to a game; or when a pre-release audio pass is requested. Reports observed versus inferred findings and applies fixes only on confirmation."
---

# Audio Check

Audio fails without an error: the page renders, the loop runs, and the player hears nothing.
Check what the player's browser will do under the player's conditions — first gesture, ringer
switch, embed, hidden tab — not what the code intends.

## 1. Read the audio stack

Identify, with `file:line` evidence:

- **Playback paths** — Web Audio (an `AudioContext` feeding decoded buffers or synthesized
  nodes — oscillators, noise — through gain nodes), media elements (`<audio>`, `new Audio()`),
  an engine or library sound manager, or several at once. Every path is audited; a setting that
  reaches only one of them is a finding.
- **Role of sound** — decoration, feedback, or gameplay-critical (rhythm timing, a cue with no
  visual). It sets what a silent row costs in section 4.
- **The four sites** — where audio is loaded or decoded, where the context is created and
  unlocked, where playback starts, where volume and mute are applied. Every finding names one.
- **Settings** — master, music, and effect volume, mute, their defaults, where they persist, and
  the control that reaches each.
- **Delivery** — a standalone page, an `<iframe>` on another origin, an installed web app, or an
  in-app browser. Ask when the source does not say and the answer changes the work.

None of it present — no audio API, no engine sound call, no audio file, no sound setting — means
the game has no audio: say so in one line and stop. Adding sound is section 6 and happens only
when asked. Audio that exists but is never wired (a file loaded and never played, a mute button
that changes nothing) is a defect and goes in the table.

## 2. Check the settings

- Every control reaches every path: mute silences music and effects on both stacks, and volume
  applies through a gain node per path. `HTMLMediaElement.volume` is ignored on iOS, so a media
  element's volume needs a gain node or the mute path.
- Settings survive a reload: read on start, written on change, defaults stated in one place. A
  control that exists only in a development tool, or a value that persists only there, does not
  count: the player's mute and volume live in the game's own UI and its own store.
- Music waits for the first qualifying gesture and starts with the game; nothing plays on load.
- A gameplay-critical event signalled only by sound — a hit, a warning, a timer — gets a visual
  counterpart. Players on mute, on silent, or without hearing still play.

## 3. Reproduce the browser conditions

Walk every row of [browser-audio-conditions.md](references/browser-audio-conditions.md); each
states how to observe the condition, what a healthy game does, and the fix. The reported symptom
says where to start, not where to stop: "silent on my friend's iPhone" is the ringer switch
*and* activation *and* the file format *and* the embed. Run the game:

- in a fresh profile or a private window — the builder's own profile carries an autoplay
  allowance a new visitor lacks;
- on a real phone, with the ringer switch both ways, and once through a screen lock and back;
- inside the embed it ships in, not only the bare page;
- through a tab switch and a return.

Emulation proves only what it emulates. If the game cannot run, inspect the source, run the
reference's probe where a console exists, and run its contract check, which fixes what the code
does under a stubbed context — which events unlock, what `play()` does while the clock is
stopped, what persists. Policies stay inferred and are labelled so.

## 4. Report

One row per defect, including every check in section 2 that failed:

| Defect | Trigger condition | Site and evidence | Status | Severity | Fix |
|---|---|---|---|---|---|
| Context never unlocks on touch | Chrome on Android, first tap; `resume()` runs from `touchstart` | unlock — `game.js:41`; `ctx.state` stays `suspended` | observed | silent | unlock on `pointerup`, `touchend`, `click`, or `keydown` |

The site is one of the four from section 1. Severity is **silent** (no sound reaches the player
under the condition), **degraded** (a sound missing, wrong, or at the wrong level), or
**polish**; a silent row blocks play only where section 1 found sound gameplay-critical, and
says so. An inferred finding stays a suspicion until reproduced. When the builder reports "works
for me, not for them", rule out two things before code: the builder's own profile allowance,
and the phone's ringer switch.

## 5. Apply on confirmation, then verify

- Apply only what the builder requested or approved, at the sites you named. Keep the engine's
  sound API; one context per page; no new audio library by default.
- Policy stays with the builder and is stated as a row with your proposed default: whether sound
  plays through the iOS silent switch, whether music continues in a hidden tab, whether the game
  opens muted.
- One check per fix, the smallest thing that fails if the logic breaks: `ctx.state === 'running'`
  logged after the first tap in a fresh profile; the `play()` promise resolving; Safari selecting
  the MP3 source; a setting reading back after a reload; the contract check run against the
  game's script. Observed in a browser, the fix is **verified**; on the contract check alone it
  is **contract-verified**, its policy still inferred; without a check it is **unverified**,
  never done.

## 6. Set up sound when asked

Only on an explicit request — "add sound", "add music", "add a mute button". Build the
foundation in the reference's setup pattern: one context created and resumed on the first
qualifying gesture; a master gain with one gain per group; mute and volume persisted, with a
mute control the player can reach; music that starts after the unlock and pauses when the page
is hidden; formats the target browsers decode; named slots (`play('jump')`) that the builder
fills. Which sounds to use is the builder's decision: a synthesized placeholder is labelled as
one, and no asset is invented or fetched.

## Constraints

- Audio only. Input feel, the layout of a settings screen, and a rhythm game's offset
  calibration are other passes; name them as follow-ups.
- Preserve the game's mix and sound design; what a sound is, and how loud, is the builder's call.
- Observe state — `ctx.state`, the `play()` rejection name, `navigator.userActivation` — instead
  of sniffing user agents. A policy name changes; a state does not.
