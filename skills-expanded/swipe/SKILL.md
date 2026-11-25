---
name: swipe
description: Turn a pile of digital cleanup into a Tinder-style swipe deck on your phone. Point it at a folder (or your unread texts) and it serves a card deck to your phone over local WiFi. Swipe each card left or right, and the chosen action runs in one reversible batch at the end. Files swipe to Trash (recoverable, never deleted outright), texts swipe to skip or reply (replies are staged, never auto-sent). Cards show a real preview whenever possible, not just a filename, so you are never swiping blind. Built for the kind of task paralysis where 300 screenshots in a folder is easier to ignore than to face. Trigger on "/swipe", "let me swipe through my desktop", "swipe to clean out <folder>", "swipe my screenshots", "swipe my downloads", "swipe my unread texts", "give me a deck to clean out X".
---

# swipe

A swipe-to-triage deck for digital cleanup. You point it at a source, it serves a card deck to your phone over your local WiFi, you swipe through the whole pile in one sitting, and the actions run as one reversible batch when you are done.

## Why this exists

A folder with 300 screenshots is a wall. Cleaning it the normal way means 300 separate decisions, each with its own friction (open it, look at it, decide, find the next one), and that friction is exactly what task paralysis feeds on. So the folder just sits there, growing.

This collapses every decision into one flick of a thumb. One card, one swipe, next card. The deck shows up on your phone, so you can do it on the couch instead of staring at a file manager. Each swipe is its own tiny hit of done, and the momentum carries you through the pile that you would otherwise never start. Nothing is destructive in the moment: files go to the Trash (recoverable), text replies are staged for you to send later. The payoff is fast and visible, and you can undo.

Design rules that make it work, do not break them:
- **Push, not pull.** It loads the whole pile and hands it to you. It never makes you come back to fetch more.
- **No guilt, no streaks, no counters that shame you.** Just the deck and a running position.
- **Reversible.** Trash, not delete. Staged replies, not sent messages.
- **One uninterrupted session.** See below.
- **Never make someone swipe blind.** Every card should tell you enough to actually decide. See Previews below.

## The engine is source-agnostic

The server and deck do not know or care what they are showing. They render whatever a **manifest** describes. A "source" is just an adapter script that emits that manifest. v1 ships two adapters (Files and iMessage); adding a new source (Gmail, Photos, a download queue, anything) is one new adapter that emits the same schema. That is what "point it at anything" means here.

### Manifest schema (the contract)

```json
{
  "source": "files",
  "title": "Downloads cleanup",
  "left":  { "label": "Trash", "kind": "trash" },
  "right": { "label": "Keep",  "kind": "keep"  },
  "reply": false,
  "items": [
    {
      "id": "0",
      "type": "image | file | text",
      "label": "headline (file/image card)",
      "sub": "subline, e.g. size and date, or a timestamp",
      "path": "/abs/path  (files: needed for thumbnail + action)",
      "thumb": true,
      "preview": "inline text preview shown on the card (files or text)",
      "sender": "headline for a text card",
      "handle": "who to reply to (text)",
      "row": 123
    }
  ]
}
```

- `left` / `right` set the two swipe actions and their on-screen labels. `kind` is a free-form tag your executor reads.
- `reply: true` makes each text card show a reply box.
- `type` controls the card: `image` and `file` both render an image thumbnail from `path` when `thumb` is true; `text` renders `sender` + `preview`.
- `id` must be a unique string. Decisions come back keyed by `id`.

### Previews: never swipe blind

A card with nothing but a filename is a coin flip, not a decision. The Files adapter tries hard to give every card something real to look at:

- **Images** get a real thumbnail (resized via `sips`).
- **PDFs, videos (`.mov`/`.mp4`/...), Office docs (`.pptx`/`.docx`/`.key`/...), and `.svg`** get a real thumbnail too, rendered on macOS by QuickLook (`qlmanage -t`) - first page of a PDF, poster frame of a video, first slide of a deck. SVGs are served directly since a browser can already render them.
- **Text-like files** (`.txt`, `.md`, `.json`, `.py`, `.jsx`, source code, etc.) get an inline text snippet instead of a thumbnail.
- **`.zip` archives** get a contents listing (file names inside) instead of nothing.
- Anything else falls back to a plain file icon - that is the one case where the adapter genuinely has nothing better to show.

If you write a new adapter, try to give every item a `thumb` or a `preview`. An icon-only card is a last resort, not the default.

## Flow

1. **Intake.** Ask two things as a short multiple choice, not open-ended:
   - **Source:** a folder (offer Desktop, Downloads, screenshots, or a custom path) or unread texts.
   - **Screenshots** is a special folder source. Screenshots save to the path in `defaults read com.apple.screencapture location` (defaults to `~/Desktop`). Point the Files adapter at that folder, then filter the manifest items to screenshot-named files only (case-insensitive regex `screenshot|screen shot|cleanshot|screen recording`) and renumber their ids `0..n` before serving. Keep each item's real `path` so trashing still works.
   The action pair is implied by the source (files: Keep vs Trash; texts: Reply vs Skip), so do not ask a separate question about it.
   **Always load the FULL pile in one deck. Never cap it or drip-feed.** The entire point is one uninterrupted swipe session; making someone come back to load "the next batch" kills the momentum that got them started. Only chunk if a set is genuinely huge (hundreds and up) and a single page would choke the phone, and if so, say so out loud. Default sort is oldest-first; do not ask unless they want largest-first.

2. **Preflight.**
   - **Network:** the deck is served to the phone over the local network, so the phone just needs to be on the same WiFi as the computer. The server auto-detects the LAN IP (`ipconfig getifaddr en0`, falling back to `en1`, `en2`). If you are on a VPN, do not hand the phone a VPN-only address; pass `--host <lan-ip>` explicitly or run on the computer's own browser with `--host 127.0.0.1`. Re-check the LAN IP if the phone can't connect - it can change mid-session (network switch, VPN toggle).
   - **iMessage source only:** reads `~/Library/Messages/chat.db`, which needs Full Disk Access for the terminal. If the adapter errors on permission, surface that.

3. **Gather items.** Run the adapter, writing the manifest into the run dir. Use a high `--cap` (e.g. 1000) as a sanity ceiling only, never as a drip limit:
   - Files: `python3 <skill>/adapters/files.py "<folder>" --cap 1000 --sort oldest > <skill>/.run/manifest.json`
   - Screenshots: gather as Files against the screenshot folder, then filter and renumber as in Intake.
   - Texts: `python3 <skill>/adapters/imessage.py --cap 1000 > <skill>/.run/manifest.json`
   If the manifest has zero items, say there is nothing to swipe and stop.

4. **Start the server** in the background:
   `python3 <skill>/server.py <skill>/.run/manifest.json &`
   It writes `<skill>/.run/server-info.json` with the `url`. Pass `--host <lan-ip>` if auto-detection picked the wrong interface.

5. **Hand off to the phone.** Open the QR page on the computer so it can be scanned:
   `open "<url>qr"` (the url ends in `/`, so this opens `.../qr`).
   Also print the plain `url` as a typeable fallback. Tell them: scan, swipe the deck, hit Done, then come back and say "done." The phone only needs to be on the same WiFi.

6. **Wait.** Stop and let them swipe. They will say "done" (or "stop") in chat.

7. **Read decisions** from `<skill>/.run/decisions.json`. Sanity check: the number of decisions should be at most the number of manifest items. If it is wildly off (e.g. zero), say so and ask before acting.

8. **Execute the batch** by source. The reversible parts run without an approval gate; the irreversible part (sending texts) always waits:
   - **Files:** collect every manifest item whose decision `dir == "left"`, map `id -> path`, and pipe the path list to the trash executor:
     `echo '<json array of paths>' | python3 <skill>/trash_files.py`
     Report the returned `trashed` count and any `failed`.
   - **Texts:** for every decision with `dir == "right"`:
     - If `reply` is non-null, that is the reply text for that `handle`.
     - If `reply` is null, draft a reply in the user's voice and pull context as needed.
     Collect all `(handle, reply)` pairs. **Do not send.** Present them as a numbered list of staged replies and wait. Only on an explicit "send it" do you send each (e.g. via the local iMessage send path). `dir == "left"` texts are skipped, no action.

9. **Report** one plain line, e.g. "41 trashed, 12 kept. 5 replies queued (3 yours, 2 I drafted), say 'send it' to send them." Then **shut down the server** (kill the background process) and **wipe the run dir**: `rm -rf <skill>/.run/*`. This is required. `.run/` can hold message bodies and must never persist.

## Hard rules

- Files go to Trash via the file manager (Put Back preserved), never `rm`.
- Texts are never auto-sent. Replies (typed or drafted) are staged; sending waits for "send it."
- Always wipe `<skill>/.run/` at the end of a run. Message bodies must not persist anywhere.
- No em dashes in any output.

## Platform notes

Thumbnails (`sips` for images, `qlmanage` for PDFs/video/Office docs), Trash (Finder via `osascript`), and the iMessage source (`chat.db`) are macOS-specific. The server and deck themselves are plain Python and a single HTML file, so a new adapter plus a new executor could target another OS without touching the engine.

## Adding sources later

A new source is one adapter emitting the manifest schema above, plus one executor for its swipe-left action. Sketches:
- **Gmail:** list = unread threads; card = sender + subject + snippet; left = archive, right = keep.
- **Photos:** deferred. Library deletion via automation is unreliable.

## Credits

The phone handoff QR code is generated by the bundled `vendor/qrcode.js`, a third-party library by [davidshimjs](https://github.com/davidshimjs/qrcodejs), Copyright (c) 2012, MIT licensed. Its full license text is bundled at `vendor/LICENSE-qrcodejs.txt`. Everything else is original.
