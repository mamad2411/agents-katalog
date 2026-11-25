---
name: botkits-youtube-niche-report
description: >-
  Use this to study what wins in a YouTube niche before planning videos. It
  pulls the top videos and Shorts of 20 to 30 similar channels with yt-dlp
  (read-only), screens out everything off-niche with a language model,
  breaks the rest down by topic, format, hook, structure and title shape,
  scores each video against its own channel's median, and builds one
  self-contained, filterable HTML report with a ranked leaderboard, idea
  teardowns and a "make these next" batch. Also use it to compare your own
  channel with the leaders, or to re-check a niche a few weeks later.
---

# YouTube Niche Report

Raw view counts mislead. A big channel's ordinary upload beats a small
channel's breakout every time. This skill measures every video against its
own channel instead: views divided by that channel's median for the same
tab (videos or Shorts). 1.0× is an ordinary upload; 3× and up is a hit. Then
it groups the hits by what they have in common, so you can see which topics,
openings, structures and titles win in this niche right now, not in general.

The output is a single HTML file that works offline: summary tables with a
scope switch (established channels, recent uploads, small channels), the
"most replayed" curve per structure, frame sheets of the strongest openings,
idea teardowns with thumbnails, a sortable leaderboard of every screened-in
video, and a screening table that shows what was dropped and why.

## When to use

- Before starting a channel or a series, to find the gaps worth filling.
- Before planning the next batch of videos, to pick topics, hooks and titles
  with evidence.
- When your own uploads stall and you want to see how the niche's leaders
  open, title and structure theirs.
- A few weeks after a first report, to see whether the niche moved.

Skip it for a single competitor (just read their channel) or for a niche
with fewer than about five active channels (the medians will be noise).

## Requirements

- A machine that can reach YouTube. Some cloud sandboxes block it; run the
  pull on a laptop or a server if `yt-dlp "ytsearch1:test"` fails.
- Python 3.9+, [yt-dlp](https://github.com/yt-dlp/yt-dlp) (recent; YouTube
  changes often), `curl`, `ffmpeg` (for the hook frame sheets) and Pillow
  (for the report). Optional: `youtube-transcript-api` as a caption fallback.
- A language model for the screening step: the agent running this skill, or
  any model CLI that can read a prompt file and print JSON.
- Disk: a few hundred MB for thumbnails and 60 s opening clips.

## Inputs to ask for

Ask for these first. If the user can't answer one, use the default and say so.

1. **The niche in one sentence**, specific enough to screen with. "Home espresso
   for beginners" works; "coffee" doesn't.
2. **Seed channels**: 5 to 20 handles or URLs the user sees as the leaders
   or direct peers. Searches will add up to 12 more.
3. **Search queries**: 10 to 20 phrases a viewer would type to find this
   niche. Mix topic words with format words ("tutorial", "review",
   "short film", "vlog").
4. **The keep rule**: what is in, and what is out. Write it as one paragraph
   with examples of both.
5. **Topic clusters**: 4 to 7 groups the user would plan around, each with a
   one-line description, plus `other`.
6. **Structures and hook types** to tag. Start from the examples in
   `config.example.json` and adapt them to the niche.
7. **Their own channel** (optional), to compare against the niche.
8. **What "recent" means**: a start date for the current wave (a trend, a
   season, a breakout video), or leave it empty for the last 90 days.
9. **What the answer should be**: for example "the next seven videos", "ten
   Short ideas", or "which of our three formats to double down on".

## Procedure

Make a work folder for this report (one per niche and date, for example
`niche-espresso-2026-11-13/`) and copy `config.example.json` into it as
`config.json`. That file is an example only: a made-up home espresso niche
that shows the format. Replace every value with the user's inputs. All scripts take `--dir <work folder>`
and are resumable: rerun a step and it skips what is already done.

### 1. Pull (30 to 60 minutes)

```sh
python3 scripts/pull.py --dir <work> --discover-only   # searches + channel list, a few minutes
python3 scripts/pull.py --dir <work>                   # the rest, 30 to 60 minutes
```

It runs the searches, picks channels (seeds, your own, then up to
`max_discovered` channels that came up in at least `discover_min_hits`
searches with a video over `discover_min_views`), lists every video on each
channel for the medians, fetches full metadata for each channel's top 50
videos and top 50 Shorts plus its newest `recent_per_tab` (20) of each, so a
channel that has gone quiet or a new one that is growing both show up, the
first 60 s of captions for the top 20 of each,
and 320 px thumbnails. The first run stops after the channel list. Open
`channels.json`, delete discovered channels that are obviously off-niche,
then run without `--discover-only`: it reuses the edited list, so the
later steps don't waste time on them.

Rate limits: the script backs off on HTTP 429. If YouTube keeps refusing,
lower `workers` to 2 and try again later. Don't add cookies from a signed-in
account; this is public data.

### 2. Screen and tag

```sh
python3 scripts/tag.py --dir <work> export
```

This writes `tag-batches/prompt-<name>.md` (about 120 videos each) and
`schema.json`. Answer each prompt with JSON `{"rows": [...]}` in
`tag-batches/answer-<name>.json` (same `<name>`), then:

```sh
python3 scripts/tag.py --dir <work> import
```

Or let a model CLI answer every batch:

```sh
python3 scripts/tag.py --dir <work> run --cmd "<your model cli> ... {prompt} ... {schema}"
```

Spot-check 20 rows of `tags.jsonl` by hand: open the video, compare. If the
keep rule lets in more than one wrong video in ten, tighten `keep_rule`,
delete `tags.jsonl` and tag again. Screening is the step that decides
whether the report is about the niche or about YouTube in general.

### 3. Read the openings frame by frame

```sh
python3 scripts/hookframes.py --dir <work>
```

It picks the kept videos that beat their channel most (up to 60, at most 6
per channel, about 20 of them Shorts), downloads only their first 60 s at
480p, and writes a 3×3 frame sheet for each to `thumbs/hook-<id>.jpg`.
With `own_channel` set it adds that channel's newest `hook_sheets_own` (12)
uploads, so you can put your openings beside the winners'. `--ids a,b,c`
builds sheets for exactly those videos and adds them to the picks.
Look at each sheet and write one line per video to `hook-frames.jsonl`
(fields in [references/method.md](references/method.md)): the text on
screen at each frame, the first visual, cuts in the first 15 s, and when the
main subject first appears. The first on-screen line then becomes that
video's hook text in the report. This is slow and worth it: titles and
captions miss most of what an opening does.

### 4. Analyse

```sh
python3 -I scripts/analyze.py --dir <work>
```

It writes `data.json` and prints every table: per cluster, format, hook,
structure, title shape, voice, era and channel size, with count, median
views, median × channel and hits (3×+), for all screened videos and for
established channels' recent uploads. It also writes a row per channel
(subscribers, uploads per week, median views per upload week by week).
Add `--prev <older work folder>` (repeatable) when the same niche was
pulled before: the page then shows how the same videos and subscriber
counts moved between pulls. Set `pulled_at` in each folder's config.json
if the folder name has no date. Read the tables against
[references/method.md](references/method.md) before writing anything.

### 5. Write the findings and ideas

Write `insights.json` ([references/insights-schema.md](references/insights-schema.md)):

- A lede that answers the user's question in two sentences.
- Three or four findings per table, each with the number that backs it and
  one example video. Lead with "established, recent" and say when the
  all-time picture disagrees.
- Ideas: take the top hits that fit the user's channel, tear each one down
  (why it worked, in one paragraph), and convert it: your version, three
  title options (lead first), two thumbnail concepts, one opening line.
- The answer: the batch the user asked for, ordered by strength of
  evidence, each with why and which idea it comes from.
- Caveats: small groups, recent videos that haven't peaked, anything the
  pull missed.
- When the question is a diagnosis ("why did my channel stall"), use the
  free `sections` for the verdict, a shown / inferred / could-not-read
  split and a side-by-side score, and `channels` and `compare` for the
  text around those two tables.

Also write a short `FINDINGS.md` next to it with the same conclusions in
plain text, so the result can live in a repo and be read without a browser.

### 6. Build the page

```sh
python3 -I scripts/build_report.py --dir <work> --out report.html
```

`--out` defaults to `report.html` in the work folder. Open it and check it
at phone width. An idea whose source has no thumbnail on disk (Shorts
often don't) gets the first frame of its hook sheet. It embeds everything, so it
can be shared as one file or published as a web page.

## Reading the numbers

- **Trust × channel over views.** Views say which channel is big; ×
  channel says what worked for that channel.
- **Read n.** A row with n under 5 is an anecdote. Say so, or merge it.
- **Small pulls inflate × channel.** The median comes from the whole
  catalogue, but only the top `top_per_tab` videos per channel are scored,
  so a test run with `top_per_tab: 4` shows 50× to 100× everywhere. Compare
  groups with each other, not with 1.0×, unless you pulled the default 50.
- **Recent beats all-time for planning.** All-time tables are dominated by
  a few evergreen hits from years ago. Use them to spot durable topics, and
  the recent established scope to pick what to make now.
- **Small channels show what doesn't work.** A format that only the small
  channels use, at a median near zero, is a copy pattern. Don't follow it.
- **A pattern needs a hit and a repeat.** One 10M video is luck; five
  videos at 3× with the same opening is a pattern.

## Safety and fair use

- Read-only. The scripts never sign in, comment, like or subscribe.
- Thumbnails, captions and opening clips belong to their creators. Keep
  them for analysis, don't republish them, and delete `.hooks/` and
  `.subs/` when the report is done.
- Study what works; don't copy titles, scripts or thumbnails one to one.
  The ideas step converts a pattern into the user's own version.
- Don't commit the user's private analytics into a public repo. The report
  only uses public numbers; keep it that way unless the user asks.

## Checklist

- [ ] The niche, keep rule and clusters are written down in `config.json`
- [ ] `channels.json` reviewed; off-niche discovered channels dropped
- [ ] 20 tags spot-checked; fewer than one wrong keep in ten
- [ ] Hook sheets read and `hook-frames.jsonl` written
- [ ] Every finding names its number, its n and one example
- [ ] The answer is the batch the user asked for, ordered by evidence
- [ ] `report.html` checked at desktop and phone width
- [ ] Clips and caption files deleted after the report

## Files

- [config.example.json](config.example.json): every setting, filled in for a made-up example niche (home espresso); replace it all
- [scripts/pull.py](scripts/pull.py), [scripts/tag.py](scripts/tag.py),
  [scripts/hookframes.py](scripts/hookframes.py),
  [scripts/analyze.py](scripts/analyze.py),
  [scripts/build_report.py](scripts/build_report.py),
  [scripts/template.html](scripts/template.html)
- [references/method.md](references/method.md): the metrics, scopes, file formats and frame-reading fields
- [references/insights-schema.md](references/insights-schema.md): the shape of `insights.json`
