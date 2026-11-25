---
name: demo-video
description: 로컬 웹앱의 기능 시연(데모) 영상을 Cap 같은 녹화 앱 없이 자동 제작한다 — Playwright 헤드리스로 실제 서비스를 조작·녹화하면서 하단 자막바·기능 라벨·부드러운 가짜 커서·줌을 코드로 굽고, LLM 대기 구간은 ffmpeg로 배속 압축해 완성 mp4를 만든다. Auto-produce a feature-demo video of a local web app WITHOUT a screen recorder like Cap — drive and record the real service headlessly with Playwright, bake in a bottom subtitle bar, feature label, smooth fake cursor and zoom, then speed-compress LLM/loading waits with ffmpeg into a finished mp4. 사용자가 시연영상, 데모영상, 기능시연, cap 영상, 화면 녹화 영상, 홍보용 데모, demo video, product walkthrough, screen recording of a localhost app을 요청하면 — 명시적으로 영상이라 말하지 않아도(이 기능 돌아가는 걸 보여줄 만한 걸 만들어달라는 식이어도) 반드시 이 스킬을 사용한다. 모션그래픽 티저가 아니라 실제 화면 조작 데모가 이 스킬의 영역이다.
---

# Demo Video Automation (Playwright + ffmpeg)

Record the real product screen as if a human were operating it, to make a demo video.
Proven: a 10-scene product feature demo (scenes 0–9 + a ~6.5 min montage), same pipeline the user approved.

Three core ideas — understand these and the rest is application:
1. **Inject the overlay directly on `document.documentElement` (html).** Zoom applies a transform to `body`, so subtitle/cursor as children of `html` are unaffected by the zoom.
2. **A fake cursor** (SVG + CSS transition) stages the mouse — the real mouse is invisible headless, and the transition does the cursor-smoothing that Cap would.
3. **LLM/loading waits use `waitForFunction`, not a fixed sleep**, recording the elapsed `waitMs` — only that window is speed-compressed 6–9x by ffmpeg (measured: 28s dead-air → 3s).

## Workflow (order is fixed — each step has a reason)

### 1) Script first, shoot after approval
Make a per-scene table and get user approval: **[URL/enter | action | input value | zoom point | speed-up window | subtitle (one value-prop sentence) | bottom-left label]**. Shooting without a script means long re-shoot loops. For file-upload scenes, **request the local file** in this step (a chat-attached image cannot be used by `setInputFiles` — measured).

### 2) Environment check
- Target server alive: `curl -s -m 5 -o /dev/null -w "%{http_code}" <URL>` — **never kill a server the user started.**
- In scratch: `npm i playwright-core` (uses system Chrome — no browser download; auto-detected on macOS/Linux/Windows, override with `CHROME_PATH`), and confirm `ffmpeg` exists.

### 3) One PoC scene → approval → roll out
Do not make every scene at once. Build **just the most representative scene** first, show the user, and after the tone (subtitle style · cursor speed · zoom ratio) is approved, roll out the rest. Users give second-level feedback ("text overlaps around 0:02"), so you just precisely fix that sleep/coordinate.

### 4) Scene capture
Copy `scripts/cap_scene.template.js` per scene and replace **only the SEQUENCE block** (overlay/helpers stay). Three+ scenes → consolidate into one `gen.js` that takes a scene number as an arg (sequences as an array of functions). Each run emits `{ waitMs, webm }` JSON on stdout.

### 5) Post-process + QA (per scene)
See `scripts/postprocess.sh`. Order: speed-up wait window → mp4 → **montage (3x3 tile) eyeball check** → confirm length. Do not skip the montage — subtitle overlap / zoom misalignment don't show in numeric metrics, only in frames.

### 6) Montage
Concat scene mp4s via `list.txt` (`-c copy`) → pull 4–6 frames at chosen points for a final spot-check → user real-playback confirmation is the completion condition.

## Output spec + direction standards

- 1920×1080 · 30fps · 25–45s per scene · 6–7 min montage (for 9–10 scenes)
- Scene structure: enter subtitle (2.5s) → key operation (deliberate cursor, 0.8s pause before click) → wait (speed-up) → result emphasis (zoom 1.35 + subtitle swap) → 0.7s after subtitle off
- Subtitle bar: bottom-center, translucent navy (`rgba(15,18,28,.85)`) + white text 30px — one value sentence. Bottom-left: blue label `N. feature name`
- Typing is `page.type(sel, text, {delay:55})` — the value that looks like real usage
- Clips `<project>/clips/N_name.mp4`, montage `<project>/final/name_montage.mp4`

## Pitfalls (all hit in production — full list in references/playbook.md)

- `await ctx.close()` **before** `browser.close()` — otherwise the webm is never flushed.
- `goto` with `waitUntil:'networkidle'` — otherwise you film mid initial-render.
- Speed-up on wait windows is mandatory. 30s of un-sped LLM wait is when the viewer leaves.
- Completion is judged not by automated metrics but by a triple check: montage eyeball + montage spot frames + user real playback.

For full detail (complete overlay CSS, 5 ffmpeg recipes, storyboard template, QA conventions, cross-platform notes): read **references/playbook.md**.
