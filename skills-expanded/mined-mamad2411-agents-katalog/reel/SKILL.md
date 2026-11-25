---
name: reel
description: Analyze an Instagram Reel into an action report — deep mode (-h, default) does yt-dlp download, Whisper transcription, frame extraction, comments, and web research; fast mode (-l) does a Firecrawl + Playwright visual read only. Use when you want to know what a reel is about and whether it is worth acting on.
---

# Instagram Reel Intelligence Skill

Analyze a single Instagram Reel from every available signal and produce a direct, opinionated action report.

**Arguments:** `[reel-url] [-l | -h]`
- `-h` or no flag → **High mode** (deep analysis). Run the **HIGH MODE** section below.
- `-l` → **Low mode** (fast analysis). Run the **LOW MODE** section below.

Only single-post URLs are supported. `/reel/` and `/p/` are both valid; profile pages (`/@`, `/channel/`, `/c/`) are not — if given one, stop and say:
> "This skill is for single reels only. Please provide a direct reel URL (e.g. instagram.com/reel/XXXXX/)."

**Prerequisites:** `yt-dlp`, `ffmpeg` (frames), `faster-whisper` (audio transcription), plus Firecrawl, Tavily, and Playwright MCP tools if available. Each step degrades gracefully when a tool is missing.

**Output location:** reports are saved under `research/reels/` in your working directory (change the path to suit your setup). Scratch files live in `research/reels/.tmp/` and are deleted at the end.

---

# HIGH MODE (-h, default)

Full multi-signal analysis. Downloads the reel via yt-dlp, transcribes spoken audio with Whisper, extracts frames with ffmpeg, fetches comments, and captures a Playwright visual.

## Phase 1: Check & Update yt-dlp

```bash
command -v yt-dlp
```

**If not found**, install:
- **Windows (winget)**: `winget install yt-dlp.yt-dlp`
- **Windows (pip fallback)**: `pip install yt-dlp`
- **macOS**: `brew install yt-dlp`
- **Linux**: `pip3 install yt-dlp`

```bash
yt-dlp -U
```

## Phase 2: Detect Channel/Profile URLs

Check URL for `/@`, `/channel/`, `/c/`. If it is a profile page, stop with the single-reel message above. `/reel/` and `/p/` are allowed.

## Phase 3: yt-dlp Download (Primary Source)

**Step 0 — Pin the working directory.** All `reel_session.*` / `reel_frame_*.jpg` scratch files are written here and globbed/cleaned up from here in later phases, so every phase must share one known CWD. Run this first and stay here:

```bash
mkdir -p "research/reels/.tmp"
cd "research/reels/.tmp"
```

**Authentication: a `cookies.txt` file, not the live browser.** Do NOT use `--cookies-from-browser chrome` — since Chrome 127 (mid-2024) Windows Chrome encrypts cookies with app-bound encryption that no external process can decrypt, and Chrome locks its cookie DB while running. The reliable path is an exported `cookies.txt`, which works with the browser open and needs no DB access. To create one: in a browser logged into Instagram, use the "Get cookies.txt LOCALLY" extension to export instagram.com cookies to `~/.claude/secrets/instagram_cookies.txt`.

**Run as a single bash block** — it uses the cookie file if present, else goes cookieless, and reports which path it took:

```bash
COOKIES_FILE="$HOME/.claude/secrets/instagram_cookies.txt"
if [ -s "$COOKIES_FILE" ]; then
    echo "[reel] using cookies.txt (authenticated)"
    yt-dlp \
      --cookies "$COOKIES_FILE" \
      --write-comments \
      --write-info-json \
      --output "reel_session" \
      "REEL_URL"
else
    echo "[reel] no cookies file — running cookieless (comments limited, no private reels)"
    yt-dlp \
      --write-comments \
      --write-info-json \
      --output "reel_session" \
      "REEL_URL"
fi
```

`--cookies` passes an Instagram session to yt-dlp, bypassing login walls and unlocking real comment data + like counts. `--write-comments` reads comments into the info JSON — it does not post anything. It is present in **both** branches, so cookieless still attempts whatever comment data Instagram returns unauthenticated.

**After the run, react to what happened — tell the user at most once, don't block:**
- **No cookies file existed** (cookieless branch ran): say once → *"No Instagram cookies file found, so comments are limited and private reels are inaccessible. To fix permanently (works with the browser open): export instagram.com cookies once with the 'Get cookies.txt LOCALLY' extension to `~/.claude/secrets/instagram_cookies.txt`."*
- **Cookies file existed but yt-dlp errored with a login/auth wall** (`login required`, `rate-limit`, `Restricted Video`, or an empty/zero-comment result on a clearly popular reel): cookies are likely **stale**. Say once → *"Your Instagram cookies look stale — re-export them; Instagram wants a fresh session."*
- **Success:** no message needed.

**If yt-dlp fails entirely** (private reel, geo-blocked, unavailable): note it and continue — Phase 8 (Playwright) becomes the primary source.

Check for success: **Glob** for `reel_session*.info.json`. If found, Phase 3 succeeded.

## Phase 4: Parse Metadata + Comments

Only run if `reel_session*.info.json` exists. Run as a **single bash block**:

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
PYTHONUTF8=1 $PYTHON -c "
import json, glob, sys, html

files = glob.glob('reel_session*.info.json')
if not files:
    print('ERROR: info JSON not found')
    sys.exit(1)

with open(files[0], encoding='utf-8') as f:
    info = json.load(f)

print('Title: ' + str(info.get('title', 'Unknown')))
print('Uploader: ' + str(info.get('uploader', 'Unknown')))
print('Duration: ' + str(info.get('duration_string', 'Unknown')))
print('Duration_secs: ' + str(info.get('duration', 30)))
print('Like_count: ' + str(info.get('like_count', 'Unknown')))
print('View_count: ' + str(info.get('view_count', 'Unknown')))

print()
print('=== DESCRIPTION ===')
desc = (info.get('description') or '').strip()
if desc:
    print(html.unescape(desc[:1000]))
    if len(desc) > 1000:
        print('...[truncated]')
else:
    print('[No description]')

comments = info.get('comments') or []
print()

# Engagement-bait detection: many creators run a 'comment WORD for the link' DM funnel,
# which floods comments with one repeated trigger word. That is a marketing mechanic,
# not organic sentiment — flag it so the report doesn't misread it as community reaction.
from collections import Counter
texts = [html.unescape((c.get('text') or '').strip()) for c in comments]
short = [t.lower() for t in texts if t and len(t.split()) <= 3]
if short:
    top_text, top_n = Counter(short).most_common(1)[0]
    if len(comments) >= 8 and top_n / len(comments) >= 0.35:
        pct = round(100 * top_n / len(comments))
        print('=== ENGAGEMENT-BAIT FLAG ===')
        print(f'~{pct}% of captured comments are the repeated trigger \"{top_text}\" — this is a '
              f'\"comment X for the link\" DM-funnel mechanic, NOT organic sentiment. Treat with skepticism.')
        print()

# Without auth, IG returns comment text but every like_count is 0, so a
# 'top comments' sort is meaningless. Detect that and label honestly.
have_likes = any((c.get('like_count') or 0) > 0 for c in comments)
print('=== COMMENTS ===' if have_likes else '=== COMMENTS (unranked — like counts unavailable without login) ===')
if comments:
    sorted_c = sorted(comments, key=lambda c: c.get('like_count', 0) or 0, reverse=True)[:20]
    for c in sorted_c:
        author = c.get('author', 'Unknown')
        text = html.unescape((c.get('text') or '').strip())
        likes = c.get('like_count', 0) or 0
        if not text:
            continue
        if have_likes:
            print('[' + str(likes) + ' likes] ' + author + ': ' + text[:300])
        else:
            print(author + ': ' + text[:300])
else:
    print('[Not available via yt-dlp — Playwright DOM snapshot will attempt to capture visible comments]')
" > reel_session_meta.txt
```

Read `reel_session_meta.txt` with the **Read tool**. If it contains `ERROR: info JSON not found`, Phase 3 failed — skip Phases 5 and 6.

## Phase 5: Extract Frames

Only run if `reel_session*.info.json` exists. Run as a **single bash block**:

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
VIDEOFILE=$(ls reel_session.* 2>/dev/null | grep -Ev '\.(json|txt|jpg|webp|png)$' | head -1)

if [ -z "$VIDEOFILE" ]; then
    echo "No video file found — skipping frame extraction" > reel_session_frames.txt
    exit 0
fi

DURATION=$(PYTHONUTF8=1 $PYTHON -c "
import json, glob
files = glob.glob('reel_session*.info.json')
if files:
    d = json.load(open(files[0], encoding='utf-8')).get('duration', 30)
    print(int(d) if d else 30)
else:
    print(30)
")

if command -v ffmpeg &>/dev/null; then
    for PCT in 0 25 50 75; do
        TS=$(( DURATION * PCT / 100 ))
        ffmpeg -ss "$TS" -i "$VIDEOFILE" -frames:v 1 -q:v 2 "reel_frame_${PCT}.jpg" -y 2>/dev/null
    done
    echo "Frames extracted at 0% 25% 50% 75%" > reel_session_frames.txt
else
    echo "ffmpeg not available — install ffmpeg to enable frame extraction" > reel_session_frames.txt
fi
```

## Phase 6: Whisper Transcription

Only run if a video file exists (Phase 3 succeeded). Uses `faster-whisper` — runs on GPU (CUDA) when available and falls back to CPU automatically.

**Step 1 — Install check (do this BEFORE running the transcription block).** Run `PYTHONUTF8=1 $PYTHON -c "import faster_whisper"`. If it succeeds, go to Step 2. If it fails, ask the user:
> "faster-whisper is not installed — the first install pulls the package (and, for GPU use, the CUDA runtime). Proceed?"

If confirmed, install: `$PYTHON -m pip install --user faster-whisper`. For NVIDIA GPU acceleration, also install `nvidia-cublas-cu12 nvidia-cudnn-cu12==9.*`. If declined, skip Phase 6 entirely and note "Audio transcription declined" in the report.

**Step 2 — Transcribe.** Run as a **single bash block**:

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
VIDEOFILE=$(ls reel_session.* 2>/dev/null | grep -Ev '\.(json|txt|jpg|webp|png)$' | head -1)
if [ -z "$VIDEOFILE" ]; then
    echo "No video file — Whisper skipped" > reel_session_transcript.txt
    exit 0
fi
if ! PYTHONUTF8=1 $PYTHON -c "import faster_whisper" 2>/dev/null; then
    echo "faster-whisper not installed — run: $PYTHON -m pip install --user faster-whisper" > reel_session_transcript.txt
    exit 0
fi
PYTHONUTF8=1 $PYTHON -c "
import sys
from faster_whisper import WhisperModel
audio, out = sys.argv[1], sys.argv[2]
try:
    model = WhisperModel('small', device='cuda', compute_type='float16')
except Exception:
    model = WhisperModel('small', device='cpu', compute_type='int8')
segments, info = model.transcribe(audio, vad_filter=True)
with open(out, 'w', encoding='utf-8') as f:
    for seg in segments:
        t = seg.text.strip()
        if t:
            f.write(t + '\n')
" "$VIDEOFILE" reel_session_transcript.txt || echo "Transcription failed" > reel_session_transcript.txt
```

Read `reel_session_transcript.txt` with the **Read tool**.

**If the transcript is empty or whitespace-only**, that is correct behavior for a silent or music-only reel — Whisper detected no speech. Do not treat it as an error. Carry `[Silent reel — background music only, no speech detected]` into the report's Raw Captures → Spoken transcript section.

## Phase 7: Firecrawl Scrape — SKIP for Instagram

Firecrawl categorically blocks Instagram (`We do not support this site`) — a policy block, not a transient error. **Skip this phase entirely and do not spend a tool call on it.** The caption/links/account it would have provided are recovered from the yt-dlp description (Phase 4) and the Playwright DOM snapshot (Phase 8).

(If this skill is ever pointed at a non-Instagram host, or Firecrawl later adds Instagram support, re-enable a Firecrawl scrape with `formats: ["markdown","links"]`, `onlyMainContent: false`, extracting caption / hashtags / mentioned links / account name.)

## Phase 8: Playwright Visual Capture — ALWAYS RUN

**This phase is mandatory on every high-mode analysis.** Do NOT skip it because yt-dlp already returned comments. The screenshot and DOM caption captured here are independent signals (they confirm what the frames show and catch on-screen text the frames missed). The only reason to skip is if Playwright is unavailable.

1. **Navigate** to the reel URL with `browser_navigate`.
2. **Wait for page load** with `browser_wait_for` — selector `video`, timeout 3000ms. Prevents a blank screenshot on Instagram's JS-heavy load.
3. **Check for overlays** with `browser_snapshot`. If a cookie consent dialog or modal is present ("Allow all cookies", "Accept", "Decline optional cookies"), dismiss it with `browser_click`. This snapshot also yields the caption / engagement counts — keep it.
4. **Screenshot** with `browser_take_screenshot`. The image is returned inline — analyze it in Phase 9.
5. **Close browser** with `browser_close` — but only after Phase 8b, if you run it. Keep the page open if you will run 8b.

If a login wall is shown: extract whatever text is visible (preview frame, account name, captions) and note it.

## Phase 8b: Comment Recovery via Playwright — OPTIONAL

**Run only when the yt-dlp comments from Phase 4 are absent or weak** — no comments, or only the engagement-bait flood, or comments with no like counts when you want real community reaction. If Phase 4 already gave solid ranked comments, skip 8b. Skipping 8b does **not** skip the screenshot — that already happened in Phase 8.

Keep the browser from Phase 8 open. Instagram lazy-loads comments, so the Step 3 snapshot has caption + counts but zero comment text. To capture them:
1. In the Step 3 snapshot, find the comment button (labeled like "Comment" with the count). `browser_click` it.
2. `browser_wait_for` ~2s for the panel to render.
3. Take a **scoped** snapshot to avoid the ~1,200-line full-feed dump: `browser_snapshot` with `target` set to the comment dialog/list container ref (or pass `depth: 8` to cap tree size). Instagram auto-loads unrelated reels below the target; scoping keeps the snapshot to the active reel.
4. To pull more than the first few comments, scroll the panel (`browser_press_key` PageDown, or `browser_evaluate` to scroll the container), then snapshot again. One extra scroll is usually enough.

Extract comment text from these scoped snapshots. **Caveat:** if the panel renders to canvas rather than accessible DOM, note "comments visible in screenshot but not extractable from DOM" and move on. Then close the browser.

## Phase 9: Analyze Frames

**Glob** for `reel_frame_*.jpg`. If frames exist, **Read** each in order: `reel_frame_0.jpg` (opening), `25`, `50`, `75` (near end). Also analyze the Playwright screenshot from Phase 8.

For each frame, extract: all visible text overlays (on-screen captions, subtitles, titles); any tool/product/website names shown; any URLs or handles; the visual subject; any UI, code, or before/after being shown.

If no frames exist (ffmpeg unavailable), the Playwright screenshot is the only visual.

## Phase 10: Web Research

From Phases 4–9, compile every tool, product, website, or concept identified. For each significant one (skip generic words), use **WebSearch** (or Tavily/Firecrawl search if available):
- What it is / what it does
- Pricing or access model (free / paid / open-source)
- Relevance to the reader's workflow and developer productivity

Limit to 1 search per item.

## Phase 11: Synthesize → Action Report

Combine all signals: transcript, comments, caption, visual frames, web research. Be direct and opinionated. Write for a technical reader who values speed and signal over completeness — judge relevance against their actual tools and workflow.

```
## What this is about
[1 sentence — the reel's topic and the specific angle or claim being made]

## The core idea
[2–4 sentences — what's being shown or recommended, and why it's framed as interesting. Draw from the transcript if available — spoken words are usually more specific than captions.]

## What was identified
- **Tool / Product / Concept**: [name] — [what it is, one line]
- [repeat for each significant item]
- **Source account**: [Instagram handle if known]

## What people are saying
[Only include if comments were found. Summarize sentiment — is the community validating the claim, calling it out, sharing results? Include 1–2 direct quotes if useful. If no comments, omit this section.]

## Why this is interesting
[Honest take: what makes this genuinely good or novel. Be specific — don't hedge.]

## Relevance to your workflow
[Does this apply to your tools and workflow? Be direct about fit or lack of fit.]

## Verdict
**[DO IT / BACKLOG / SKIP]**
[1–3 sentences explaining why. If DO IT: the first concrete step.]

## Watch out for
[Caveats, limitations, assumptions the reel glosses over. If nothing significant, say "None."]
```

## Phase 12: Save to Disk

Generate the filename as a **single bash block**:

```bash
PYTHON=$(command -v python3 2>/dev/null || command -v python 2>/dev/null)
TODAY=$(date +%Y-%m-%d)
SLUG=$(PYTHONUTF8=1 $PYTHON -c "
import re, json, glob
files = glob.glob('reel_session*.info.json')
info = json.load(open(files[0], encoding='utf-8')) if files else {}
title = info.get('title') or ''
slug = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')[:60]
# Instagram has no real title — yt-dlp fills it with 'Video by <uploader>',
# which makes a useless, colliding slug. Fall back to the reel id instead.
if not slug or re.match(r'^(video|reel)-by-', slug):
    rid = info.get('id') or info.get('display_id') or ''
    slug = re.sub(r'[^a-z0-9]+', '-', str(rid).lower()).strip('-')[:60] or 'reel'
print(slug)
")
echo "${TODAY}_${SLUG}.md" > reel_session_filename.txt
cat reel_session_filename.txt
```

If you can produce a more memorable slug from the report's main tool/topic or the first ~6 words of the caption, override it. If info JSON never existed (yt-dlp failed entirely), build the slug from the main tool/topic in the report.

Read the filename, then **Write** the report to the parent reports folder (you are inside `research/reels/.tmp`, so write to `../[filename]`):

```markdown
---
source: instagram-reel
url: [REEL_URL]
date: TODAY
account: [account name if known]
verdict: [DO IT / BACKLOG / SKIP]
mode: high
---

# [Main topic / tool name]

**URL:** [REEL_URL] | **Account:** [handle] | **Date analyzed:** TODAY

## What this is about
[from Phase 11]

## The core idea
[from Phase 11]

## What was identified
[from Phase 11]

## What people are saying
[from Phase 11 — omit if no comments were found]

## Why this is interesting
[from Phase 11]

## Relevance to your workflow
[from Phase 11]

## Verdict
[from Phase 11]

## Watch out for
[from Phase 11]

---

## Raw Captures

### Caption / DOM text
[raw text from Playwright DOM snapshot]

### Spoken transcript
[Whisper output — omit if transcription was skipped]

### Comments
[raw comment data from yt-dlp or Playwright DOM — omit if none found]

### Visual notes
[frame-by-frame observations: 0%, 25%, 50%, 75%]
```

Tell the user the save path (`research/reels/[filename]`).

## Phase 13: Cleanup

```bash
rm -f reel_session.* reel_frame_*.jpg \
  reel_session_transcript.txt reel_session_meta.txt \
  reel_session_frames.txt reel_session_filename.txt
```

The saved `.md` file is kept permanently.

## High-Mode Edge Cases

| Situation | How to handle |
|---|---|
| yt-dlp fails entirely | Skip Phases 4–6. Playwright (Phase 8) becomes the only source. Note in report. |
| No cookies.txt file | yt-dlp runs cookieless. Comments limited, no private reels. Tell user once how to set up `~/.claude/secrets/instagram_cookies.txt`. |
| Cookies present but auth-walled | Cookies are stale — tell user once to re-export. Proceed with whatever data came back. |
| Comments are engagement-bait | ENGAGEMENT-BAIT FLAG fired in Phase 4 — report it as a DM-funnel mechanic, not sentiment. Optionally run Phase 8b. |
| No comments anywhere | Omit "What people are saying". |
| ffmpeg not available | Skip frame extraction. Playwright screenshot is the only visual. |
| Whisper declined | Skip transcription. Note "Audio transcription declined". |
| Login wall on Instagram | Playwright extracts whatever is visible. Note in report. |
| Purely visual reel, no speech | Whisper produces little — fine, visual frames carry it. |
| Non-English reel | Whisper `small` supports many languages. Note detected language. |
| `/p/` URL | Treat same as `/reel/` — allow and proceed. |

---

# LOW MODE (-l)

Fast analysis. Firecrawl for caption, Playwright for visual capture, web research on identified tools. No download, no audio transcription, no frame extraction. Use when you want a quick read without waiting for yt-dlp or Whisper.

## Phase 1: Detect Channel/Profile URLs

Check URL for `/@`, `/channel/`, `/c/`. If it is a profile page, stop with the single-reel message. `/reel/` and `/p/` are allowed.

## Phase 2: Scrape Page Text (Firecrawl)

Use a Firecrawl scrape on the reel URL with `formats: ["markdown", "links"]`, `onlyMainContent: false`. Extract: **Caption**, **Hashtags**, **Mentioned links**, **Account name**.

If Firecrawl returns an error or empty content (Instagram login wall), note silently and continue — Phase 3 compensates.

## Phase 3: Visual Capture (Playwright)

1. **Navigate** with `browser_navigate`.
2. **Wait** with `browser_wait_for` — selector `video`, timeout 3000ms.
3. **Check overlays** with `browser_snapshot`; dismiss any cookie/consent modal with `browser_click`.
4. **DOM snapshot** with `browser_snapshot` (or reuse Step 3). Captures accessible DOM text — often caption + top comment text even without login.
5. **Screenshot** with `browser_take_screenshot` (returned inline — analyze in Phase 4).
6. **Close browser** with `browser_close`.

If a login wall is shown, extract whatever text is visible and note it.

## Phase 4: Read the Screenshot

Analyze the inline screenshot. **Fallback:** if it is blank, mostly dark, or a loading state, use any available vision-capable LLM/MCP with the DOM text and caption to infer what the reel is about.

Look for: text overlays (captions, titles, subtitles); tool/product/website names; URLs or handles; the visual subject; any before/after, code snippet, or UI shown.

## Phase 5: Web Research

From Phases 2–4, compile every tool, product, website, or concept. For each significant one, use **WebSearch** (or Tavily/Firecrawl search): what it is, pricing/access model, relevance to the reader's workflow. Limit to 1 search per item. Do not spiral.

## Phase 6: Synthesize → Action Report

Combine Phases 2–5. Be direct and opinionated; write for a technical reader who values speed and signal over completeness.

```
## What this is about
[1 sentence]

## The core idea
[2–4 sentences]

## What was identified
- **Tool / Product / Concept**: [name] — [one line]
- [repeat]
- **Source account**: [handle if known]

## Why this is interesting
[Specific, no hedging]

## Relevance to your workflow
[Direct about fit or lack of fit]

## Verdict
**[DO IT / BACKLOG / SKIP]**
[1–3 sentences. If DO IT: first concrete step.]

## Watch out for
[Caveats. If nothing, say "None."]
```

## Phase 7: Save to Disk

```bash
mkdir -p "research/reels"
```

Generate a slug from the main topic/tool (lowercase, hyphens, max 6 words). Use today's date: `YYYY-MM-DD_slug.md`. **Write** to `research/reels/YYYY-MM-DD_slug.md`:

```markdown
---
source: instagram-reel
url: [REEL_URL]
date: YYYY-MM-DD
account: [account name if known]
verdict: [DO IT / BACKLOG / SKIP]
mode: low
---

# [Main topic / tool name]

**URL:** [REEL_URL] | **Account:** [handle] | **Date analyzed:** YYYY-MM-DD

## What this is about
[from Phase 6]

## The core idea
[from Phase 6]

## What was identified
[from Phase 6]

## Why this is interesting
[from Phase 6]

## Relevance to your workflow
[from Phase 6]

## Verdict
[from Phase 6]

## Watch out for
[from Phase 6]

---

## Raw Captures

### Caption / DOM text
[raw text from Firecrawl / Playwright DOM snapshot]

### Visual notes
[what the screenshot showed — text overlays, UI, etc.]
```

Tell the user the save path. No temp files to clean — screenshot data is inline.

## Low-Mode Edge Cases

| Situation | How to handle |
|---|---|
| Login wall on Instagram | Use whatever is visible + caption from Firecrawl if it worked. Note in report. |
| Purely visual, no text | Describe what's shown; research the visual subject with WebSearch. |
| No tool/product — just an idea | Skip Phase 5 search. Focus on the concept and its applicability. |
| Non-English reel | Use available content; note language; translate key terms if needed. |
| Firecrawl returns login wall HTML | Ignore it. Playwright screenshot is primary. |
| Screenshot blank or loading | Use DOM snapshot text; vision-LLM fallback if needed. |
