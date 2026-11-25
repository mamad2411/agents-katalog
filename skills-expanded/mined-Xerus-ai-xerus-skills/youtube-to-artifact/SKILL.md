---
name: youtube-to-artifact
description: "Turns a YouTube video into a deep, self-contained HTML analysis page by reading BOTH channels: the timestamped transcript (what was said) and extracted frames (what was shown - slides, code, UI, diagrams). Extracts named frameworks, decision principles, step-by-step techniques, anti-patterns, recommendations and linked resources, recreates on-screen diagrams as SVG, links every point back to its timestamp, and verifies every pull quote against the transcript before delivering. Bundled stdlib-only scripts feature-detect yt-dlp, youtube-transcript-api and ffmpeg and degrade cleanly (transcript-only or frames-only) when one is missing. Use when the user shares a YouTube URL and says 'analyze this video', 'summarize this video', 'extract the frameworks from this talk', 'make notes from this tutorial', 'turn this video into a page/artifact', 'what are the key takeaways', or wants knowledge extracted from a YouTube video."
---

# YouTube to Artifact

Watch a video the way a careful human note-taker would, listening AND looking, then publish what it
teaches as one offline-safe HTML page where every claim links back to the second it came from.

The value is in three disciplines, not in the HTML:
1. **Two channels, fused.** Transcript-only summaries miss everything that was shown but not said:
   menu paths, code on screen, the numbers on a chart, the diagram the whole talk hangs on.
2. **Structured extraction.** Frameworks, principles, techniques and anti-patterns, not a retelling.
3. **Verified honesty.** Quotes are verbatim and machine-checked; inferences are labelled; degraded
   runs say so.

## Files in this skill

| Path | What |
|---|---|
| `scripts/extract.py` | metadata + timestamped transcript + frames into a work dir; prints a manifest |
| `scripts/check_artifact.py` | pre-delivery gate: self-containment, timestamps, quote fidelity |
| `references/extraction.md` | frame strategy, reading order, channel fusion, troubleshooting |
| `references/artifact-structure.md` | the sections, depth levels, honesty rules |
| `references/design.md` | how the page should look and behave, with a starting stylesheet |

Script paths are relative to this skill's folder. Both scripts are Python 3 standard library only;
the external tools they call are optional and detected at run time.

---

## Workflow

### 1. Agree the brief (one round of questions, then work)

Ask these together (use a structured-question tool if the environment has one):

- **Goal**: comprehensive summary · frameworks and techniques · technical deep-dive (code, tools,
  architecture) · decision intelligence (recommendations, debates, trade-offs)
- **Depth**: brief · detailed (recommended) · exhaustive
- **Save to**: default `artifacts/<video-title-slug>.html` in the current repo or working directory

If nobody is there to answer (a headless or scheduled run), use *frameworks and techniques*,
*detailed*, and the default path, and state those defaults in the final report.

For a video over 60 minutes, also agree the scope (all of it, or specific chapters/time ranges)
before extracting. That is the only other question worth asking; everything else is reported, not asked.

### 2. Extract

```bash
python scripts/extract.py "<URL>" --out "<temp work dir>" [--frames auto|scene|none|N] [--start S --end S]
```

- `--frames scene` for screen recordings, UI demos and slide talks; `auto` otherwise.
- Read the printed manifest. Its `degraded` list is what you will tell the user.
- Exit code 2 (no transcript AND no frames): stop, report which tools are missing or what failed
  (see `references/extraction.md` section 5). Never analyse a video from its title and description.

### 3. Read: transcript first, then frames

Follow `references/extraction.md` sections 3-4: build a timestamped topic outline from the transcript,
mark the "look here" moments, then read frames in batches of 8-10 in order. Fuse each key moment as
SAID / SHOWN / MEANS, and flag visual-only information. If an important moment fell between frames,
re-extract that range at a small interval.

Only describe on-screen content you actually saw in a frame. If you did not extract frames, the
artifact says the visuals were not analysed.

### 4. Extract the knowledge

Tailor the emphasis to the agreed goal, but always look for:

- **Frameworks**: named or clearly structured mental models. Name, origin, when to use, steps, the
  example used, timestamp.
- **Principles**: decision rules. The rule, when it applies, the reasoning, stated exceptions.
- **Techniques**: step-by-step methods. Prerequisites, steps, pitfalls, what success looks like.
- **Anti-patterns**: what to avoid. The pattern, why it fails, what to do instead, how to detect it.
- **Recommendations and debates**: explicit endorsements, disagreements with conventional wisdom,
  trade-offs.
- **Voice**: recurring phrases, reasoning style, where the speaker is emphatic vs hedged.

A section with nothing real in it is omitted, not padded. An hour-long interview may have no
techniques; say nothing rather than invent one.

### 5. Research the resources

Collect every link in the description (`metadata.json`) plus tools, repos, papers and products that
were mentioned or shown. For each, find: what it is, how it relates to the video's argument, current
status (for repos: stars, language, last update, as of today), anything important the video left out.

- If the environment can run sub-agents in parallel, give each resource its own agent and wait for all
  of them before building. Otherwise research them one after another.
- If web access is unavailable, list the resources anyway, marked "not fetched".
- Keep it proportionate: roughly the 10 most relevant resources. Research informs the Resources and
  Debates sections; it never gets blended into what the speaker said.
- When the video makes a contestable claim central to its argument, one search for supporting or
  opposing evidence is worth it; attribute what you find.

### 6. Recreate the diagrams

Where the speaker shows a diagram, flowchart, architecture or chart that carries the argument,
recreate it as inline SVG (or HTML/CSS) from the frames: accurate labels, plus annotations the speaker
said aloud but were not drawn. Caption each with its timestamp. Embed an actual frame only when a
recreation would lose information (see `references/design.md`, "Embedded frame").

### 7. Build the page

Write ONE self-contained HTML file: sections per `references/artifact-structure.md`, look and
behaviour per `references/design.md`. If a design-taste or frontend-design skill is installed, apply
it too; the offline and honesty rules in this skill take precedence where they conflict.

Save to the agreed path, creating the folder if needed. If that file already exists, ask before
overwriting (or write `<slug>-2.html`). Slug: lowercase title, non-alphanumerics to `-`, trimmed to
about 60 characters.

### 8. Verify (gate: do not deliver until this passes)

```bash
python scripts/check_artifact.py "<artifact.html>" --work "<work dir>"
```

It fails on: any external script, stylesheet, font or image (`src`, `srcset`, CSS `url()`, SVG
`<image href>`), not exactly one `<h1>`, no link to the source video, timestamps past the video's
end, and any `<blockquote>` whose words are not in the transcript as whole words (quotes under three
words are refused as unverifiable).
Fix every FAIL; for a quote failure, correct it to the transcript's words or move it out of the
blockquote as a labelled paraphrase. Then do the self-review in `references/design.md` section 8.

### 9. Deliver and clean up

Delete the work directory (the video file is already gone; frames can be tens of MB) unless the user
asked to keep the frames. Report in this shape:

```
Saved: artifacts/<slug>.html  (<size>, <N> sections)
Covers: <one or two sentences on what the page captures>
Method: transcript (<source>) + <N> frames (<mode>) | transcript only | frames only
Degraded: <each item from the manifest's degraded list, or "nothing">
Checker: PASS (<n> quotes verified, <n> timestamped links)
```

---

## Terminal states

Every run ends in exactly one, named in the report:

| State | When |
|---|---|
| **done** | transcript and frames both used, checker passes |
| **done, degraded** | one channel missing (no captions, or no frames), or research unfetched; checker passes; the page and the report both say what is missing |
| **blocked** | invalid URL, private/removed video, or neither channel available; nothing written; report the cause and the fix |
| **scoped out** | a long video where the user chose to stop or narrow the scope before extraction |

## Rules that come from getting this wrong

- **No title-only analyses.** If extraction failed, the answer is "blocked", not a plausible summary.
- **No unseen visuals.** Never write "as shown on screen" about something you did not see in a frame.
- **No paraphrase in a blockquote.** The checker will catch it; do not route around the checker by
  dropping the `--work` flag.
- **Timestamps are the audit trail.** A point without a timestamp is a point the reader cannot check;
  every topic section, quote, framework and technique carries one.
- **Do not read 300 frames.** For long videos, the transcript tells you where to look; extract
  narrowly and read in batches.
- **Research is labelled.** What a linked paper says is not what the speaker said.
- **Report degradation twice**: on the page (header line) and in the final message.
- **Ask before installing or upgrading tools**, and before using browser cookies.

## Dependencies

| Need | Required? | Notes |
|---|---|---|
| Python 3.8+ | yes | runs both scripts |
| `yt-dlp` | strongly recommended | metadata, captions fallback, video for frames; keep it updated, YouTube changes often |
| `ffmpeg`, `ffprobe` | for frames | without them the analysis is transcript-only |
| `youtube-transcript-api` | optional | first transcript source; the yt-dlp path covers for it |
| web access / sub-agents | optional | resource research; without it resources are listed "not fetched" |
