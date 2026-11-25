---
name: dreamfab-news
description: >
  Make news with Dreamfab's news line (`news/`): a short daily vertical brief, or a 3-6 minute 16:9 in-depth report.
  The daily brief: English sources first, every
  number checked against a second source, a script with numbers spelled out, an AI anchor who opens and closes on
  camera (lip-sync of her two parts only), cards for the numbers, subtitles, the show's theme, a cover and SEO copy that
  open on the same hook. Files only: nothing is uploaded or published.
  Use when the user wants a daily news brief / 新聞 / 每日美股 / 盤前快報 / 一分鐘新聞 / AI 主播 / 深度報導 / 深度研究, or mentions
  dreamfab-news, 造夢廠 新聞, 聞.
---

# Dreamfab · news (聞・新聞)

One folder per show (`projects/<show>/`, settings in `series.py`), one folder per day (`YYYY-MM-DD/`). Everything runs
through `news/make.py`; read `ROOT/docs/en/news/OVERVIEW.md` before the first day of a new show.

## 0. Locate the toolkit

1. `ROOT` = `$DREAMFAB_HOME`, else `~/.dreamfab`. If this skill's base directory is `<repo>/skills/dreamfab-news` and
   `<repo>/news/make.py` exists, you may use `<repo>` instead.
2. If `ROOT/news` is missing, install with `DREAMFAB_LINES=news` (and `DREAMFAB_AGENTS=none`):
   - macOS / Linux / Git Bash:
     `curl -fsSL https://raw.githubusercontent.com/autoip/dreamfab/main/install.sh | DREAMFAB_LINES=news DREAMFAB_AGENTS=none bash`
   - Windows PowerShell:
     `$env:DREAMFAB_LINES='news'; $env:DREAMFAB_AGENTS='none'; irm https://raw.githubusercontent.com/autoip/dreamfab/main/install.ps1 | iex`
3. `PY` = `ROOT/.venv/bin/python` (Windows: `ROOT/.venv/Scripts/python.exe`). `ffmpeg` with libass, and Edge or Chrome
   for the cards (`DREAMFAB_BROWSER`). `AUTOIP_API_KEY` is set by the user; never read keys from elsewhere, write them
   into files or echo them.

## Hard rules

- **Upload only to the show's channel, as the show says.** `upload` goes to `series.py`'s `CHANNEL` with its own login
  and at its `PRIVACY`. With no channel it is files only. Never pick a privacy, a channel or a schedule the user did not
  set. An unattended daily run works under the approvals written in its instructions: no questions, a log at the end.
- **Credits are charged on submit and there is no cancel.** Before the first job of a day (and before any extra
  re-read) give the price now and off-peak (03:00-09:00 Taiwan time, half; `submit … --off-peak`) and wait for a yes,
  unless the user has approved a standing daily run. One job at a time.
- **English sources first, then two sources for every number.** CNBC's live blog, AP, Reuters, MarketWatch, company
  releases and SEC 8-Ks, official data (ISM, BLS, the Fed). Chinese-language media only for local numbers (for Taiwan:
  the TAIEX futures night session, the index). When two sources disagree, check a quote page's historical close. Never
  invent a number, a reason or a quote.
- **News, not advice: the legal lines are checked twice per episode.** Read `ROOT/docs/en/news/COMPLIANCE.md` and run
  its checklist once when the research is written (before the script is shown) and once more before the render; a
  script that fails is rewritten, not published. In short: no buy, sell, price target, support or resistance, timing
  or bullish/bearish verdict of our own (valuation only as a quote with its source); every number from two sources
  and no rumour written as fact; allegations kept apart from verdicts, with the company's answer; nothing
  undisclosed; nothing paid for by viewers. The end card and the description always list the sources and say the
  anchor and voice are AI-generated, that the channel is not a securities investment consulting business, and that
  the content is compiled news and public information, not investment advice.
- **No logos, no real people's pictures.** Companies appear as names and numbers. The anchor is a made-up person
  (text-to-image portrait, her voice from an image-to-video line); never clone a real person's face or voice.

## Every day

1. `PY ROOT/news/make.py new projects/<show> YYYY-MM-DD`: `day.py` is copied from the day before (date changed);
   `script.md` has the fixed first and last lines.
2. Research (send the searches together; it takes about a minute) and write `script.md`, one line per sentence:
   `spoken｜subtitle｜picture`.
   - About 11 lines and 280 characters make a minute.
   - Spoken: numbers as words; company and index names in English (Dow Jones, Oracle, Apple…); local companies in the
     local language; avoid words with two readings (in Chinese, 重啟 → 恢復).
   - Subtitle: digits, local names.
   - Picture: `anchor` for the first and last line, card ids in between.
3. `day.py`:
   - `SOURCES` and `CARDS`, built with `row()`, `bar()` and `box()`; red up and green down for Taiwan.
   - `COVER`: two hook lines (the biggest number, then a question) plus one line of the next stories.
   - `COVER_HERO` (optional): the day's biggest story as one picture for the cover, in English prose: no text, logos,
     real people or flags, the subject in the middle, the top third dark for the hook. `hero` → `submit hero` makes it
     (one v4 picture, 20 credits); without it the cover shows the anchor.
   - `SEO`: titles A/B/C that open on the same hook, a lead, tags.
4. `cards`, `cover`, `seo` (no credits). Run the `COMPLIANCE.md` checklist on the script and the SEO copy. Show the
   cards and the cover before spending anything.
5. `voice` → `submit voice` → `check`. Listen to every spot `check` lists. English names are often written otherwise
   by the recogniser, so do not re-read on the transcript alone.
6. `anchor` → `submit lipsync` (only her opening and her closing lines, the call to subscribe included) → `render`.
   Before `render`, look at her chest in a few frames of `clips/anchor.mp4`: the lip-sync service sometimes burns in a
   line of made-up captions and still reports success. Then `desub` → `submit desub` (video restore clears the line;
   30 credits per 8 s) rather than another lip-sync, which mostly comes back with them too.
7. A line read wrong: `redo DAY FIRST LAST` → `submit redo` → `splice DAY FIRST LAST`. The lip-sync is kept when her
   lines did not change. If only a word of the new take is wrong, mix old and new by hand at the pauses.
8. `upload` when the show has a channel (then report the link).
9. Report:
   - the files: `out/<NAME>_<YYYYMMDD>.mp4`, `.zh-TW.srt`, `_cover.jpg`, `_SEO.txt`
   - the length and the credits spent
   - the spots to listen to
   - the minutes per step (`timing.tsv`)

## Every day, unattended

Only when the user asks for a standing daily run, and after they agree to its time, its daily credits and its privacy:
`DAILY = dict(at=, days=, latest=)` in `series.py`, then `PY ROOT/news/make.py schedule projects/<show> --dry-run`
(show it), `schedule`, and `daily projects/<show> --test`. Each day the scheduler runs `news/make.py daily`, and
Claude Code works through `ROOT/news/daily_prompt.md` (or the show's own `DAILY` `prompt`): no questions, every job
off-peak, a misread word swapped in `SAY` and re-read once (never a second round), a log at the end. Skipped when it
starts after `latest`. Read the show's `daily_log.md` when the user asks how it went.

## In-depth reports (深度報導)

A 16:9 report of 3-6 minutes on one story, on the same channel with the same anchor. Read the last section of
`ROOT/docs/en/news/OVERVIEW.md` first. In short:

1. Research from primary sources (SEC filings, company releases, earnings calls), checked against English media: two
   sources for every number, and nothing that sources disagree on. Write the script and its sources
   (`文案_v1.md`), run the `COMPLIANCE.md` checklist on it (bull and bear cases quoted with their sources, signals to
   watch instead of a verdict, disputes as "who alleged what, how the company answered, where it stands"), and show
   them before any credits are spent.
2. Build it on the explainer line (`explain/`): `script.md` (numbers as words, `SAY` for misread words such as
   `("光纖", "光仙")`), `project.py` with `IMAGES` (v4, no text or logos), `SHOTS`, `FACTS` (source cards), `TITLE`, `MUSIC`.
3. The anchor: cut only the opening and closing parts of the narration for lip-sync (31 s at most each, 0.6 s of
   silence at the end); lay them out 16:9 (title left, anchor right) as `CLIPS`; hold a still for the `GAPS` lead at
   the start of the opening one.
4. Data cards as HTML (16:9), a 16:9 cover (tag, date, hook, the anchor's face), SEO with chapter times.
5. `news/make.py upload` with the show's `series.py` (`CHANNEL`, `YT_TOKEN`, `PRIVACY`, private suggested) and the
   episode's `day.py` (`FILE`).
   A vertical trailer under 60 s goes with it (the Shorts feed brings the views): `SHORTS` in `project.py` (clips of
   the narration as written; the anchor's parts from their first line; `layout="band"`; events and numbers only),
   `explain/render.py EPISODE --shorts`, the SEO file's 「Shorts 標題」「Shorts 說明欄」, then `upload EPISODE --shorts`
   and the related video set to the long report in Studio.
6. Report the link, the length, the credits and the spots to listen to.
