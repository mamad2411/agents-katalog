---
name: html-to-video
description: Record an HTML page, local .html file or URL as an MP4 (H.264) or WebM (VP9) video with frame-exact timing (virtual clock), optional muxed audio and a JPG poster. Use for product or game trailers, animated demo clips, screencasts of a local dev server, changelog or social videos, and turning CSS/JS animations into a video or GIF.
---

Needs ffmpeg on PATH and the Playwright Chromium build that matches the plugin's pinned Playwright (`npx playwright@<version> install chromium`; installing the plugin does not download a browser). Run `node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" doctor` first: it checks both and prints the exact install command. A bare `npx playwright install chromium` uses the project's own or the latest Playwright and can install a Chromium the plugin cannot use.

## Run

```bash
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" video http://localhost:5173/trailer.html dist/trailer.mp4 10 --width 1920 --height 1080
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" video demo/page.html dist/demo.webm --fps 60 --poster
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" video demo/page.html dist/trailer.mp4 12 --audio score.wav
node "${CLAUDE_PLUGIN_ROOT}/bin/atelier" video --help
```

JS API, for an audio track generated in code (`audioSource`). This one writes a short 880 Hz beep at the start of every second; replace the sample loop with your own track:

```bash
node --input-type=module -e "const { pathToFileURL } = await import('node:url'); const m = await import(pathToFileURL(process.argv[1]).href);
const { writeFileSync } = await import('node:fs');
const seconds = 12;
// 48 kHz 16-bit mono PCM on the video timeline: sample i plays at i / 48000 s, frame N at N / fps s.
const writeWav = (wavPath) => {
  const n = Math.round(48000 * seconds), b = Buffer.alloc(44 + 2 * n);
  b.write('RIFF', 0); b.writeUInt32LE(36 + 2 * n, 4); b.write('WAVEfmt ', 8);
  b.writeUInt32LE(16, 16); b.writeUInt16LE(1, 20); b.writeUInt16LE(1, 22);
  b.writeUInt32LE(48000, 24); b.writeUInt32LE(96000, 28); b.writeUInt16LE(2, 32); b.writeUInt16LE(16, 34);
  b.write('data', 36); b.writeUInt32LE(2 * n, 40);
  for (let i = 0; i < n; i++) if (i % 48000 < 4800) b.writeInt16LE(Math.round(8000 * Math.sin((2 * Math.PI * 880 * i) / 48000)), 44 + 2 * i);
  writeFileSync(wavPath, b);
};
const out = await m.recordHtml({ url: 'demo/page.html', outPath: 'dist/trailer.mp4', duration: seconds, fps: 60, poster: true, audioSource: writeWav });
console.log('Video written to: ' + out);" "${CLAUDE_SKILL_DIR}/index.mjs"
```

## Options

API name first, then the CLI form.
- `url` (1st argument): http(s), `file://` or `data:` URL, or a path to a local HTML file (relative to the working directory). `localhost:5173/x` without a scheme is rejected; write `http://localhost:5173/x`.
- `outPath` (2nd argument): `.mp4` (libx264 `-preset medium -crf 20 -pix_fmt yuv420p`, `+faststart`) or `.webm` (libvpx-vp9 2 Mbit/s). Any other extension, or none, gets `format` (default MP4).
- `duration` (`[seconds]` or `-d, --duration`): seconds of page time, default 5. Frames = round(duration x fps), at least 1.
- `fps` (`--fps`): default 30, max 240.
- `width`, `height` (`--width`, `--height`): default 1280x720, integers 1 to 8192. MP4 needs even sizes, so an odd value is rounded up by 1 px and the page is laid out at that size (the CLI prints a note). WebM keeps odd sizes.
- `format` (`-f, --format`): `mp4` or `webm`. Must agree with a `.mp4`/`.webm` extension; a mismatch is an error.
- `poster` (`--poster`): also write `<name>-poster.jpg` (the first frame) next to the video.
- `audioSource(wavPath)` (`--audio <file>`): see Audio below.
- `timeoutMs` (`--timeout <ms>`): how long to wait for navigation and the page's `load` event. Default 30000.
- `allowHttpError` (`--allow-http-error`): record a page that answers HTTP 4xx or 5xx instead of failing. Without it such a page is a runtime error, so a mistyped dev-server URL does not turn into a clip of the error page.
- `browser` (API only): a launched Playwright Chromium to reuse across calls. It is not closed; each call opens and closes its own context.
- `signal` (API only): an `AbortSignal`. Aborting stops the capture or ffmpeg step, removes the temp files and rejects with the abort reason. The CLI does this on the first Ctrl+C.

## Output

- The video at `outPath` (parent directories are created) and, with `poster`, `<name>-poster.jpg` beside it. `recordHtml` resolves with `outPath`; the CLI prints `Video written to: <path>` and `Poster written to: <path>`.
- Frames, the intermediate video and the WAV live in a temp directory that is removed on success and on every failure. The finished files are moved into place last, so a failed run never leaves a truncated video at `outPath` or overwrites an earlier one.

## Exit codes

- `0`: video written.
- `2`: usage error (message and usage on stderr) or runtime failure (one `atelier: ...` line, plus a `Fix:` line when ffmpeg or Chromium is missing). Runtime failures include a page that answers HTTP 4xx or 5xx (`<url> answered HTTP 404 Not Found; ...`), a URL that cannot be opened (`could not open <url>: ...`) and a page that misses its `load` event within the timeout.

## Notes

### Timing

Capture runs on a virtual clock: frame N shows the page exactly N / fps seconds after the first frame, however long each screenshot takes. The video is `duration` long and animations play at their authored speed.
- The first frame is taken after the `load` event and `document.fonts.ready`. Page timers are frozen during load, so page time 0 is the first frame.
- Between frames the clock advances 1000 / fps ms in equal sub-steps of at most 1/60 s (2 per frame at 30 fps, 1 at 60 fps and above); the last sub-step lands on the frame time.
- JS time (`Date`, `performance.now`, `setTimeout`, `setInterval`) runs on Playwright's fake clock, run forward to each sub-step.
- `requestAnimationFrame` callbacks run once per sub-step, so at least 60 times per page second, with the sub-step time as their timestamp. The last run before each frame gets that frame's exact time, so canvas, GSAP or three.js motion lines up with CSS animations.
- CSS animations, CSS transitions and Web Animations are frozen when created and stepped at every sub-step, honoring `playbackRate` and page seeks. An animation the page pauses stays paused where it was. SVG SMIL is seeked with `setCurrentTime`.
- A CSS animation, transition or Web Animation that starts between sub-steps (from a timer or an event) begins at the next sub-step, so it can trail JS-timed content by up to 17 ms, as on a 60 Hz display. One started inside a `requestAnimationFrame` callback begins at that callback's time.
- Not on the virtual clock: `<video>` and `<audio>` playback, Web Workers, scroll-driven animations, CSS animations inside cross-origin iframes, and `document.timeline.currentTime`. Content fetched after `load` appears at whichever frame is being captured when it arrives.
- ffmpeg is resolved on PATH (never through a shell) before Chromium launches, so a missing ffmpeg fails immediately.

### Audio

Output is silent unless `audioSource` or `--audio` is given. `audioSource` receives an absolute path in the temp directory and must write a WAV there (48 kHz 16-bit PCM recommended). A missing file, or one of 44 bytes or less (header only), throws `audioSource wrote an empty or missing file: <path>`. `--audio` copies an existing file (WAV recommended; any format ffmpeg reads). The video stream is copied; audio is encoded to AAC 192k (MP4) or Opus 160k (WebM) and the output ends with the shorter stream.

Do not record Web Audio in headless Chromium (`MediaRecorder`): it drifts 10 to 50 ms per minute against the video, and some Chromium versions silently record zeros. Synthesize the track in Node on the same timeline (frame N = N / fps seconds) and pass it in.

### Trailers and GIFs

- Record at the delivery frame rate (60 for store pages and YouTube), then check the file:
  ```bash
  ffprobe -v error -select_streams v:0 -count_frames -show_entries stream=width,height,r_frame_rate,nb_read_frames -of json dist/trailer.mp4
  ```
  Expect the exact size, `r_frame_rate` = fps/1 and `nb_read_frames` = round(duration x fps).
- Show real UI rather than bullet lists, use concrete numbers, prefer percussive audio over ambient pads, and keep outros under about 0.8 s.
- GIF (two-pass palette):
  ```bash
  ffmpeg -i dist/demo.mp4 -vf "fps=15,scale=640:-1:flags=lanczos,palettegen" palette.png
  ffmpeg -i dist/demo.mp4 -i palette.png -filter_complex "fps=15,scale=640:-1:flags=lanczos[x];[x][1:v]paletteuse" dist/demo.gif
  ```

Also exported: `runCli(argv, { stdout, stderr })` (returns the exit code) and `findOnPath`, re-exported from the shared preflight helper for v0.2 callers.
