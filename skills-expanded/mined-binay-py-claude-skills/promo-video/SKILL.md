---
name: promo-video
description: Make promo videos of the user's own website, web app or extension — the real page recorded smoothly inside a phone (9:16 for Reels, Shorts, TikTok) and a browser window (16:9 for Fiverr gig videos, Reddit, YouTube), with a hook over the product in the first frame, bold chunked captions, cursor and tap effects, rehooks, a CTA that loops back to frame 0, optional music and edge-tts voiceover — then checked against a short-form video playbook. Use for "make a promo video of my site/app", "product demo video", "Reel/Short for my website", "Fiverr gig video", "turn my landing page into a video".
---

# promo-video

`scripts/promo.mjs` is zero-dependency Node 22+ and needs **ffmpeg**. It records with its own headless Chrome / Edge / Chromium and a throwaway profile (`BROWSER=` to choose), so the user's browser and logins are never touched. Voiceover is optional and needs Python with `edge-tts`.

```
node promo.mjs quick https://example.com --hook "Book a table in 10 seconds" --cta "Order today"   # reads the page, writes storyboard.json, renders
node promo.mjs render storyboard.json                       # after editing the storyboard
node promo.mjs render storyboard.json --preview             # half-size key frames only, no video (seconds, not minutes)
node promo.mjs plan storyboard.json                         # validate + timeline, no browser
node promo.mjs check promo                                  # rule check of rendered videos, no frames to look at
```
Options: `--out promo` · `--formats 16x9,9x16` · `--music song.mp3` · `--platform shorts|reels|tiktok|x|fiverr|reddit|linkedin` · `--seconds 30` (quick) · `--brand "#bg1,#bg2,#accent"` · `--hook`, `--title`, `--tagline`, `--cta` (quick) · `--no-cache` · `--fresh` (re-record) · `--keep-frames`.

Output in `--out`: `promo-9x16.mp4` (1080×1920) and `promo-16x9.mp4` (1920×1080), both 30 fps H.264 High with AAC; `poster-*.jpg` (frame 0, which is designed as the cover); `contact.png` (one small sheet, ≤ 12 tiles: frame 0, rehooks, scenes, CTA, last frame); `promo-*.json` (timeline + text boxes, read by `check`); `storyboard.json` in quick mode; `.cache/` (see below).

## Cheap workflow (keep tokens low)
1. `quick <url> --preview` → read the printed rule lines and open only `preview.png`. Fix the hook/captions in `storyboard.json`.
2. `render storyboard.json` → read the compact summary (durations, failed rules, paths). Look at `contact.png` once; never extract or open individual frames unless a rule points at a specific problem.
3. Caption, hook, CTA, color or music edits re-render without re-recording: recordings are cached in `<out>/.cache` by a hash of what the browser does (URL, actions, timing, viewport). Only changed pages are recorded again; unused cache entries are pruned after each render. `--no-cache` skips it.
4. `check <out>` re-verifies videos any time (ffprobe, freezedetect, loudnorm measurement) without viewing frames.

## What every video gets (from `references/video-playbook.md`, section 11)
- **Frame 0 = hook + product**: the hook (3–7 words, `hook` or the first scene's caption) is on screen from t = 0 for the whole first scene (≥ 1.5 s) over the real page. No logo card first; the brand (logo + title + tagline) appears in the same band after the hook.
- **Captions**: 1–3 word chunks (≤ 16 chars), 72–96 px, weight 900, 7 px dark stroke; word-synced and highlighted when there is a voiceover, else spread over the scene.
- **Safe zones**: in 9:16 all text stays inside x 65–890, y 250–1440 (clear of the Reels/Shorts/TikTok buttons and captions); the phone sits left of center for the same reason. 16:9 uses the full width.
- **Motion**: slow push-in/pull-out per scene, a cut or text change at least every 3 s, punch-in + impact sound at 40% and 70% (on a scene cut when one is near), whoosh on cuts, click sound on clicks.
- **CTA**: one CTA (text + URL pill) in the last ≤ 3 s, the video ends with it, and it cross-fades back to the opening frame so the end loops into frame 0.
- **Audio**: music trimmed/looped, faded, ducked 20 dB under the voice (300 ms release), two-pass loudnorm to −14 LUFS (true peak ≤ −1.5 dBTP before AAC); a silent track if there is no audio at all.
- **Encode**: libx264 High, yuv420p, CRF 18, GOP 0.5 s, maxrate 12M (6M for Fiverr), +faststart, AAC 48 kHz.
- **Platforms**: length caps Shorts/Reels/X 45 s, TikTok 60 s, Fiverr 75 s and 50 MB. `platform: "fiverr"` drops the URL (Fiverr bans contact info), skips TTS (Fiverr asks for a human voice) and renders 16:9 only.

`check` prints one line per failed/warned rule and a compact list of passing rule numbers. Fix failures before calling a video done; WARN is advice.

## Storyboard
```json
{
  "title": "Binay Websites",
  "hook": "Your business online in days",
  "tagline": "Websites for clinics, salons and cafés in Nepal",
  "platform": "reels",
  "brand": { "bg": ["#121a2b", "#1f2d4a"], "accent": "#f2a71b", "logo": "logo.png", "font": "Bricolage Grotesque" },
  "music": "music/track.mp3",
  "voice": { "name": "en-US-AndrewMultilingualNeural", "rate": "+5%" },
  "outro": { "cta": "Get your site this week", "url": "binaywebsites.pages.dev", "seconds": 2.5, "voiceover": "Link in bio." },
  "formats": ["9x16", "16x9"],
  "hide": ["#chat-widget"],
  "scenes": [
    { "url": "https://binaywebsites.pages.dev/", "seconds": 3, "voiceover": "Want customers to find you online?" },
    { "caption": "Live demos for every niche", "actions": [{ "scroll": "text=Pick your business", "ms": 1300 }] },
    { "caption": "Tap to see a real demo", "actions": [{ "click": "a[href*=dental]", "ms": 1400 }, { "wait": 800 }] },
    { "caption": "Booking built in", "actions": [{ "zoom": ".booking", "scale": 1.7, "ms": 2400 }] }
  ]
}
```
A full example is `examples/storyboard.json`. Rules: `title` and `scenes[0].url` are required. A scene without `url` continues on the same page (scroll position, opened menus and typed text carry over). `seconds` is optional (lead-in 0.6 s + actions + 1 s hold, stretched to fit its voiceover). `formats` on a scene limits it to one format (selectors often differ between desktop and phone). `colorScheme: "dark"` records the site's dark theme (default light, not the OS theme). `sfx: false` turns sound effects off. `hide` adds CSS selectors to hide (common cookie banners and chat bubbles are hidden already). Unknown keys are errors, so typos are caught.

Actions run one after another: `{"scroll": "#id" | "text=Heading" | "top" | "bottom" | 600, "ms"}` (a number scrolls by that many px), `{"click": sel, "ms"}`, `{"hover": sel, "ms"}` (desktop only), `{"type": sel, "text", "ms"}`, `{"wait": ms}`, `{"zoom": sel, "scale": 1.6, "ms"}`. `text=Our work` matches the element whose text is exactly that (headings first, then buttons/links), else one that contains it. Pointer actions scroll their target into view while the cursor glides there; on the phone a tap indicator replaces the cursor. Zooms are re-rendered at the zoom scale, so text stays sharp.

## Voiceover (optional)
Add `voiceover` text to scenes and `outro`. If Python can `import edge_tts` (`pip install edge-tts`, or set `PROMO_PYTHON` to a venv's python), each sentence is one edge-tts call (sentences over 12 words are split), with word timings for word-synced captions, 380 ms between sentences and 600 ms before the CTA line. Default voice: `en-US-AndrewMultilingualNeural`, or `ne-NP-SagarNeural` when the text is Nepali. Microsoft rejects custom SSML, so pacing comes from those gaps and `voice.rate` (default +0%, about 160 wpm). Without edge-tts the render still works and prints a note; the voiceover text then becomes the captions. Say "you" early (rule 5), 150–170 wpm (rule 14). TTS clips are cached in `.cache` too.

## How it works
- **Recording**: each frame the page's clock (`requestAnimationFrame`, timers, `Date.now`, CSS/Web Animations, same-origin iframes) advances exactly 1/30 s, so scrolling is eased and smooth and page animations never stutter however slow a screenshot is. Desktop 1440×900; phone 390×844 at 3× with a mobile user agent and touch. Network requests and images in view are awaited before each shot (lazy images, fonts). Frames where nothing changed reuse the previous shot. Analytics beacons (Google, Meta, Cloudflare, Clarity…) are blocked so renders don't count as visits.
- **Compositing**: each output frame is an HTML stage drawn by the same headless browser — brand gradient, browser window with the real URL or a phone with a status bar in the page's theme color, captions, cursor, ripples — so Devanagari and emoji render with real fonts (Nirmala UI / Mangal / Noto Sans Devanagari, plus the site's Google font when it has one). Frames are piped as JPEG into ffmpeg.
- **Browser lifecycle**: closed with `Browser.close` on every exit path (a detached watchdog covers a killed Node), and stale profiles are swept, because a force-killed headless browser on Windows leaves blank entries in Alt+Tab.

## Safety
- Read-only by default: quick mode only scrolls and opens the site's own nav links by URL (never login/admin/cart/delete links). It never clicks, types or submits.
- Storyboard `click` and `type` actions really happen in the throwaway browser. **Don't click buttons that submit forms, send messages, buy or post** unless that is intended; typing never presses Enter. Prefer a staging URL for flows that change data.
- Logged-in pages can't be recorded (the profile is empty); use a public demo page.

## Limits
- Timing (4-core laptop, measured while other work was running): 19 s in both formats ≈ 3.5 min, 23 s with voiceover ≈ 6.5 min; recording ~0.3 s and compositing ~0.2 s per changing frame. `--preview` takes 20–50 s. A re-render after caption edits skips recording (compositing still runs).
- Videos (`<video>`) and cross-origin iframes (YouTube embeds, maps) play in real time, not on the page clock, so they look sped up; WebGL works but is slow.
- Sites that block headless browsers or need a login show whatever they serve to a fresh visitor.
- Music licensing is the user's job: YouTube Audio Library tracks are safe; avoid claimed songs in Shorts over 60 s.
