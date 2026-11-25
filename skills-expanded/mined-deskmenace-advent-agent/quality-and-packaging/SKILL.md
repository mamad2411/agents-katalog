---
name: quality-and-packaging
description: Before every submission. The gift@2 manifest (emotion, interaction, tier, collection, share frame, downloads, print, credits) and its embedded-HTML form, the capture hook and data-advent-private, per-form checklists, running advent-agent check, every gate problem code and its fix, the offline rule (vendored libraries only), credits and allowed licences, secret hygiene, size limits, honest incomplete lists, progress phases.
license: MIT
---

# Quality and Packaging

The quality gate is a friend with a checklist. Pass it on the first try by checking the same things yourself. The gate checks the package; it cannot check delight. That part is still yours: the three criteria in `gift-director` (emotional effect, delightful interaction, shareability).

## Progress phases

Report where you are, never what you are making, with one of four phases: `thinking`, `making`, `testing`, `wrapping`. Run `advent-agent progress <phase>`. If the shell is blocked, write the phase word into `.progress` in your door's folder (`./doors/NN/.progress`).

## The manifest (schema `advent-agent/gift@2`)

Form A (folder or zip): `gift.json` next to the files. Form B (single HTML): the same JSON inside `<script type="application/advent-gift+json">` in the `<head>`. Full field table and a complete example: `references/manifest.md`. Schema file: `schema/gift.schema.json`.

Required: `schema` (`advent-agent/gift@2`), `day` (1–24, must match the door), `title` (≤ 160), `note` (≤ 8000), `emotion`, `interaction`, `share.still`. Strongly expected: `ideaId` (or `null` for your own invention), `family`, `form`, `tierUsed`, `entry` (folder gifts), `share.caption`, `credits` whenever you adapted anything. Optional: `collection`, `share.loop`, `share.privateText`, `downloads`, `print`, `realWorld`, `song`, `artifacts`, `incomplete`, `continuity`.

```html
<script type="application/advent-gift+json">
{ "schema": "advent-agent/gift@2", "day": 7, "title": "Your Very Own Jelly Persimmon",
  "ideaId": "jelly-fruit", "family": "tactile-toys", "emotion": "cute", "interaction": ["squeeze", "stretch"],
  "form": "interactive-html", "tierUsed": "S",
  "note": "You said persimmons taste like autumn pretending to be summer. This one wobbles like it agrees.",
  "share": { "still": { "capture": "still" }, "caption": "My AI Secret Santa made me a jelly persimmon", "privateText": [] },
  "credits": [] }
</script>
```

`gift@1` manifests are still accepted, but every new gift uses `gift@2`.

Paths are relative, forward slashes, no `..`, no leading `/`, and must exist in the package. URLs are https without credentials.

## The share frame and the capture hook

Every gift declares `share.still`: either a `share.png` (1080×1350) in the package, or `{ "capture": "still" }` plus a capture hook in the page. Gifts whose magic is motion add `share.loop`: `{ "capture": "loop", "durationMs": 6000 }` (3000–10000) or a `share.webm` you recorded with the kit recorder.

```js
window.adventCapture = {
  async prepare(kind) {            // "still" (1080×1350) or "loop" (1080×1920)
    document.documentElement.classList.add('is-capturing');   // hide buttons, hints, cursors
    openCard();                    // the most showable state: opened, shaken, bloomed, high score…
    if (kind === 'loop') startTheShowyAnimation();            // the calendar records durationMs from here
    await new Promise((r) => setTimeout(r, 400));             // let transitions settle
  }
};
```

Rules: `prepare` is idempotent, never needs a click, never plays sound, finishes within 5 seconds, and works under reduced motion (show the final state). The personal detail is visible. The bottom-right 160×48 px stays clear for the share mark. No logo, watermark, link or hashtag of your own. A kit helper lives in `workshop/kit/capture/` when present; use it or write the hook by hand as above.

**Private text.** Put `data-advent-private` on any element with a name, a place or anything the person might not want to post. List short strings in `share.privateText` too. The privacy preview offers to blur them. Sensitive matters (health, money, relationships in difficulty) never appear in the share frame at all.

## Offline, always

No `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource`, `sendBeacon`, and no remote `src` or `href` on scripts, stylesheets, images, fonts, media or frames. No CDN, no web fonts, no analytics. Libraries come only from `workshop/kit/vendor/` (three.js, matter.js, canvas-confetti), inlined or copied into the package, and credited. Links the person clicks (`<a href>` to a print service or a vendor) are fine. The gate reports `network_request`.

## Credits

Any third-party code, art, font or sound you adapted goes into `credits[]` as `{ what, source, license, url }`. Allowed licences: MIT, BSD, ISC, Apache-2.0, CC0, Unlicense, CC BY (art and sound), OFL (fonts), public domain. Anything else (GPL, NC, ND, no licence) is inspiration only: rewrite the technique yourself and credit nothing. Kit blocks are ours (MIT); credit vendored libraries when you inline them. The gate reports `credit_license`.

## Checklists

**Every gift**
- One clear `emotion`, a discoverable first `interaction` (under 3 seconds) and one surprise deeper in.
- A share frame you have actually pictured; the capture hook puts the page in that state.
- Opens with no console errors and no network (see above).
- Works with keyboard only and with touch only; visible focus; text ≥ 16 px; contrast ≥ 4.5:1.
- `prefers-reduced-motion` respected; no autoplay audio; mute wherever there is sound; restart wherever there is a game; no flashing.
- Fits 360 px wide and 1280 px wide. The single HTML works when opened from disk on its own.
- No file paths, keys, tokens; nothing from the person's folders copied verbatim; nothing from their avoid list.
- None of the purchase words in any text you write, not even in a negation ("nothing was …"). Say what you did instead ("I found", "I picked out").
- `note` is warm, specific, two to four sentences, says why you made this; no stock phrases, no process talk.
- `incomplete` lists everything that does not work. Empty only if everything works.
- `day` equals the brief's day. `tierUsed` is the tier you actually built in.
- Collections: `collection { set, index, size }` with `index` ≤ 3; the third item completes the set.

**Interactive HTML**: reset works without reload; pause exists where there is motion; state survives a resize; under ~5 MB (hard limit 8 MB per HTML).
**Images**: real PNG/JPEG/SVG/WebP that decode; `alt` on each; wallpapers at exact sizes, listed in `downloads`.
**Audio/video**: decodes; a player with controls; captions or a transcript for spoken words.
**Documents / text**: first line `# Title` for text gifts; print CSS for printables; PDF opens. Still give it one thing to touch.
**Song**: karaoke player (lyrics highlighted in time with `score.json`), mute, `song.score` valid, `song.wav` decodes, `song.renderSheet` present and naming no provider.
**Printables**: print-ready files at real sizes with bleed in `downloads`; when research is allowed, 2–3 real print services in `print` with price, currency, `checkedAt` and `shipsTo`.
**Real-world**: every item has `name`, `vendor`, https `url`, `checkedAt` today, price + currency; ceiling respected. `whatsLeft` is optional; say what's left in your note if useful.

## Run the gate

```
advent-agent check ./doors/NN/gift --day N
```

Output is a list of `{ code, severity, path?, message }`. Errors block submission; warnings do not but deserve a look. Fix, re-run, repeat until clean. Then:

```
advent-agent submit ./doors/NN/gift --day N
```

Problem codes and fixes: `references/gate-errors.md`. If the brief lists `previousProblems`, fix those first.

## Secret hygiene

The gate scans every text file for API keys (`sk-…`, `AKIA…`, `ghp_…`, `xox…`, `AIza…`), private keys, bearer headers, `KEY=value` env lines, home paths (`/Users/…`, `/home/…`, `C:\Users\…`), node_modules, and the calendar's own token. Any hit is `secret_<kind>` and blocks the gift. Before packaging, grep your files for `sk-`, `/Users/`, `/home/`, `@` and `token`. Do not include logs, `.env`, `.git`, `node_modules`, editor files, or your own notes.

## Limits

200 files, 200 MB total, 8 MB per HTML file; keep single-file gifts under ~5 MB and media under 2 MB (images) / 10 MB (video) for a fast reveal. No symlinks, no absolute paths, no `..`.

## Honest incompleteness

`incomplete: ["Level 3 is not built", "No sound on Safari (untested)"]`. Plain sentences, each a fact. Never "minor polish remaining".

## Hand-over

Nobody sees your output, and the calendar shows only your note. Do not describe the gift anywhere else.
