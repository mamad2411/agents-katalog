---
name: make-media
description: >-
  Generate images and short video for a site or product when code is not enough: atmosphere, places,
  materials, textures, source images to dither or turn into ASCII, an ambient hero loop, a consistent
  illustration set, OG and social images. Two routes: the paid Gemini API (Nano Banana 2.1 images,
  Gemini Omni Flash video) under a hard monthly spend cap, or the user's own logged-in Gemini app or
  Flow driven in their browser. Includes post-processing: crop, WebP/AVIF, ordered dithering, ASCII art,
  web video with a poster. Never for people presented as real, the product's UI, or proof.
---

# make-media

Generated media is for what does not exist yet and cannot be drawn better in code. Decide that first
(the `taste` skill, "Pictures"): text, UI, diagrams, charts, icons, logos, pixel art, ASCII, dithering
effects and wireframes are better in code; real product screenshots beat any generated product shot.

**Never generate** customers, team photos, testimonials, the product's UI, or "real-world" footage
presented as real. Generated places, materials and atmosphere are fine. **List every generated asset in
the build report** (file, route, model, prompt, cost, where it is used).

## Choose the route

| | Route A: Gemini API (default) | Route B: the user's browser |
| --- | --- | --- |
| What | `scripts/gemini.mjs` or Google's `gemini-api` CLI; files land on disk | Gemini app or Flow, logged in as the user, driven with gstack `/browse` |
| Paid by | A Google Cloud billing account (Google AI Pro and Ultra plans include a monthly Cloud credit) | The Gemini or Google AI plan's included quota (Flow credits) |
| Use when | A key is set up (below). Repeatable, scriptable, logged | No API key yet, or a Flow-only feature (Flow editing) |
| Reliability | High | Fragile: the UI changes; every download must be checked by eye |

## Route A: the Gemini API

**Models and prices** (AI Studio pricing, checked 2026-11-07; the script's price table must match):

| Model id | What | Price |
| --- | --- | --- |
| `gemini-nano-banana-2.1` (default image) | Nano Banana 2.1, sizes 512 / 1K / 2K / 4K | $0.034 at 1K, $0.050 at 2K, $0.113 at 4K; Batch API half |
| `gemini-3-pro-image` | Nano Banana Pro: hard compositions, legible text in the image | $0.134 at 1K/2K, $0.24 at 4K |
| `gemini-omni-1.2-flash` (default video) | 3-15 s with native audio, 16:9 or 9:16, 360p / 720p / 1080p / 4k (the last two upscaled); can edit video | about $0.023/s at 360p, $0.07/s at 720p, $0.104/s at 1080p, $0.209/s at 4k |

Gone, do not use: Imagen (shut down in the Gemini API) and the Veo 3.1 preview models (shut down there
on 2026-10-22). Veo 3.1 GA lives on Vertex AI (about $0.40/s at 1080p with audio); use it only if the
user asks for 4K cinematic video. `$40` buys about 1,190 images at 1K, or about 57 ten-second clips at
720p. Draft at 1K / 720p; render finals at 2K / 1080p. The free tier refuses the image and video models
(`429 ... limit: 0`): a key on a billing account is required.

**The cap.** `scripts/gemini.mjs` keeps a ledger (`~/.make-media/ledger.jsonl`) and refuses any call
whose estimate would take the calendar month past `MAKE_MEDIA_CAP_USD` (default 40; set it to the user's
monthly budget). Raising it needs the user's yes **for that project**: ask, and only after the answer
pass `--cap <usd>`. Check the month with `node <make-media>/scripts/gemini.mjs spend`. Google's budget
alert on the billing account (setup step 2) is the real backstop; the ledger only knows about calls made
through the script.

**Setup (the user, once, about 15 minutes):**
1. Have a Google Cloud billing account. With a Google AI Pro or Ultra plan, activate the Google
   Developer Program benefits and link the plan's monthly Cloud credit to it (a prepaid billing account
   may be required; credits expire a year after grant).
2. In AI Studio, create an API key in a project on that billing account. Set a budget alert at the cap.
3. Store the key where Claude can use it without seeing it: a secrets mod if one is installed (for
   example a vault that substitutes `{{vault:GEMINI_API_KEY}}`), else a `GEMINI_API_KEY` user
   environment variable. **Never ask for a key in chat.**

**Unverified on a paid key.** The script's request path, cap, ledger and error handling have been tested
only against the free tier's refusal (`429 ... limit: 0`); no paid call has produced a file yet. Treat the
first real call as the check: look at the file, and compare the ledger with the billing page. Use only
`GEMINI_API_KEY`, never another Google key that happens to be set, and don't spend on a test the user
didn't ask for.

**Commands** (run from the project root; `<make-media>` is where this skill is installed, and the
`GEMINI_API_KEY="{{vault:...}}"` prefix applies only with a vault mod):

```bash
# image: default model, 1K square; --aspect 16:9|4:5|1:1|9:16|4:1 ..., --size 512|1K|2K|4K
GEMINI_API_KEY="{{vault:GEMINI_API_KEY}}" node <make-media>/scripts/gemini.mjs image \
  "<prompt>" --aspect 16:9 --size 2K --out assets/generated/hero-sea.jpg

# video: default model, 720p, 8 s, 16:9; --resolution 360p|720p|1080p|4k, --duration 3s..15s, --aspect 9:16
GEMINI_API_KEY="{{vault:GEMINI_API_KEY}}" node <make-media>/scripts/gemini.mjs video \
  "<prompt>" --duration 8s --out assets/generated/hero-loop.mp4

# check the request and the estimate without spending
node <make-media>/scripts/gemini.mjs image "<prompt>" --out x.jpg --dry-run
```

Without the vault mod, drop the `GEMINI_API_KEY=...` prefix (the variable is read from the
environment). The script prints the written path; exit 3 means the cap refused the call, 2 a usage or
key problem, 1 an API error (the message says which).

**Editing or reference images** (keeping a look across a set, restyling a photo): use Google's official
`gemini-api` CLI, which takes `-i <image>`. Install a pinned release from
`github.com/google-gemini/gemini-api-cli/releases` (it is a beta; the install one-liner is
`iwr -useb https://raw.githubusercontent.com/google-gemini/gemini-api-cli/main/scripts/install.ps1 | iex`
on Windows, `curl -fsSL .../install.sh | bash` on Linux). It reads `GEMINI_API_KEY` too:
`gemini-api image "<prompt>" -i ref.jpg --out assets/generated/`. Size and aspect go in
`--body '{"response_format":{"type":"image","aspect_ratio":"16:9","image_size":"2K"}}'` (see
`gemini-api image --schema`). Its calls bypass the ledger: add up the cost yourself and stay under the cap.

## Route B: the user's browser

Only when the user has said Claude may generate in the Gemini app (`gemini.google.com`) or Flow
(`labs.google/flow`) with their logged-in account. Google's terms on automated use of the consumer apps
are the user's call.

- **Drive the browser the user prefers.** With gstack installed: its `/browse` skill, bringing the user's
  login in with `/setup-browser-cookies` (imports their Chrome cookies into the headless browser), or
  `/open-gstack-browser` for a visible window they can watch. Otherwise any browser automation the user
  has set up; computer use is the fallback when a page will not drive.
- One generation at a time: open the app, choose image or video, paste the prompt, wait, download, then
  move the file into `assets/generated/` with a name that says what it is.
- **Open every downloaded file and look at it** before using it; the UI may have given you the wrong
  variant, a watermark or a low-resolution preview.
- Record it in the report as Route B with the prompt; cost is the included quota.

## Prompting for site media

Write the prompt like an art director's brief: the subject from the page's idea; the light and time;
the palette in the page's own colours (name them: "deep cobalt #1f3fbf and pale lavender"); the
composition with room where text will sit ("empty sky in the upper third"); the lens or medium;
and what to leave out ("no text, no logos, no people, no watermark"). For **source images that code will
dither or turn into ASCII**, ask for strong silhouettes, simple shapes and a full tonal range from near
black to near white. For a **set**, fix one style sentence and reuse it verbatim in every prompt (or
use the CLI with a reference image). Make two or three drafts at 1K, pick one, then render the final.

## Post-process, then place

Every recipe below has been run (ffmpeg 9 with libwebp, libaom-av1, libx264, libvpx-vp9, palette dither):
`references/post-process.md`. In short:

- **Crop and compress** to WebP (and AVIF where the stack serves it), at the largest size the layout
  shows, two widths for `srcset`. A 1600 px hero should be well under 200 KB.
- **Dither** (the technical mode) with a fixed two-colour palette taken from the page's ink and ground,
  in ffmpeg for a static picture or at runtime in a canvas so it stays themeable.
- **ASCII**: `node <make-media>/scripts/ascii.mjs <image> --cols 96 --invert --out art.txt`,
  set in a `<pre>` with an `aria-label`.
- **Video**: H.264 MP4 (plus WebM), muted, a poster frame, under about 2 MB for an ambient loop; it pauses
  under `prefers-reduced-motion`.

Where files go: raw outputs in `assets/generated/` (the ledger keeps the prompt for each), processed
files wherever the stack serves static assets (`public/`, `static/`, `src/assets/`). Then verify the page
with the `taste` skill: screenshots at 1440, 768 and 375.
