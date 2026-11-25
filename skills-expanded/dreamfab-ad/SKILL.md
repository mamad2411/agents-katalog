---
name: dreamfab-ad
description: >
  Make ads for a physical product, a service or a brand with Dreamfab's ad line (`ad/`): a brief, one market version
  per language each in its own look (documentary, variety show, keynote, cinematic), a cloned narrator per language,
  bilingual subtitles, the user's existing footage, product shots, website screenshots and designed cards, then a
  main cut plus 30 s and 15 s cuts in 16:9, 9:16 and 1:1, delivered as files with a delivery list.
  Use when the user wants an ad / 廣告 / 宣傳片 / 產品介紹 / 品牌片 / 多國語言版本 / 30 秒短版, or mentions dreamfab-ad,
  造夢廠 廣告, 廣.
---

# Dreamfab · ad (廣・廣告)

One campaign folder, one sub-folder per market version (`<lang>_<pack>`), one `project.py` each. The ad line renders
with the explain line's `explain/render.py` and `explain/narration.py`, plus its own tools in `ad/`. You write the brief
with the user, the scripts and the prompts, run the scripts, and show every result before money is spent on the next
step.

## 0. Locate the toolkit

1. `ROOT` = `$DREAMFAB_HOME`, else `~/.dreamfab`. If this skill's base directory is `<repo>/skills/dreamfab-ad` and
   `<repo>/ad/new.py` exists, you may use `<repo>` instead.
2. If `ROOT/ad` is missing, install (pass `DREAMFAB_AGENTS=none`; skills are already installed):
   - macOS / Linux / Git Bash:
     `curl -fsSL https://raw.githubusercontent.com/autoip/dreamfab/main/install.sh | DREAMFAB_AGENTS=none bash`
   - Windows PowerShell:
     `$env:DREAMFAB_AGENTS='none'; irm https://raw.githubusercontent.com/autoip/dreamfab/main/install.ps1 | iex`
3. `PY` = `ROOT/.venv/bin/python` (Windows: `ROOT/.venv/Scripts/python.exe`).
4. `ffmpeg -filters` must list `subtitles` (libass); Edge or Chrome must be installed for cards and screenshots
   (`DREAMFAB_BROWSER` to name one). `AUTOIP_API_KEY` must be set by the user; never read keys from elsewhere, write
   them into files or echo them.

## Hard rules

- **Credits are charged on submit and there is no cancel.** Before every batch give the job count and the price now
  and off-peak (03:00-09:00 Taiwan time, half; `aip_runner.py --off-peak`), and wait for a yes. Jobs one at a time
  unless the user's workflow switches say otherwise (`PY ROOT/dreamfab/workflow.py show <folder>`).
- **A new look for every market.** Never copy one language's version into the next: offer two or three style packs as
  sample frames (`ad/styles.py`, drawn locally, no credits) and let the user pick per language.
- **Every claim traces to the brief.** Numbers, "free", who made the music (if the user made it with Suno, the ad must
  not say it came from AutoIP), what the product does. No real people, brands, logos or trademarks the user does not
  own; product shots are of the user's product or a clearly invented one.
- **Deliver files, do not upload**, unless the user asks; uploads are private.
- Narrators: text-to-video of a new person saying one line in the wanted language and manner, never a drama
  character's voice, never ask the user to record. Voice v3 (`voxcpm2`) reads the script's language.
- Projects live in the user's `projects/`, never in `ROOT`; keep media, fonts and keys out of git.

## Workflow

Details: `ROOT/docs/en/ad/OVERVIEW.md` (中文：`ROOT/docs/zh-TW/ad/OVERVIEW.md`); the renderer's fields:
`ROOT/docs/en/explain/OVERVIEW.md`. Example: `ROOT/examples/ad/demo/`.

1. **Start**: `PY ROOT/ad/new.py projects/<brand>/<campaign> --kind product|service|brand --langs ja:documentary,ko:variety`
   → fill `brief.md` with the user (audience, three points, proof, call to action, lengths, what not to say).
2. **Looks**: per market, a sample frame in two or three packs → user picks → `STYLE` and its fields.
3. **Scripts**: `script.md` per language, `> 中文` under each line (one line = one subtitle, one row); a hook in the
   first three seconds; user approves every language.
4. **Narrators**: text-to-video per language (`/videos/text-to-video`, 480p, 8 s) → cut 5-15 s → `VOICE`;
   `PY ROOT/explain/narration.py P jobs` → `aip_runner.py` → `narration.py P check`; list the words to listen to.
5. **Pictures**: `CLIPS` from the user's footage; product shots (text-to-image v4 prompts are MOSS-Image prose, see
   the explain skill) and image-to-video; `PY ROOT/ad/capture.py URL images/site_<lang>.png --lang <lang> --hide-corner`;
   `CARDS` → `PY ROOT/ad/cards.py P`; review sheet → user.
6. **Music: Suno by default** (it has no API for ordinary users): fill each version's `suno.md` (title, Style of
   Music from the pack rewritten for this ad, Exclude styles, length; Instrumental for a bed, lyrics only for a sung
   jingle in the market's language) and give it to the user to paste into Suno; the downloaded file goes in `music/`
   and `MUSIC`. All automatic instead: AutoIP `/voice/song` (measure the length that comes back). The ad never says
   Suno music came from AutoIP. No `CH_MUSIC` = straight through; loop the middle on the beat if short.
7. **Render**: `SHOTS`, `CUTS` (30 s 16:9, 15 s 9:16 and 1:1 by default) → `PY ROOT/explain/render.py P --until <words>`
   for a new look → `PY ROOT/ad/render.py projects/<brand>/<campaign>` (every version and cut, then `delivery.md`).
   Check frames: subtitles clear of the picture, cards not cut off in the vertical and square cuts.
8. **Deliver**: tick the brief's checklist, give the delivery list and the preview addresses
   (`PY ROOT/dreamfab/library.py serve projects`; the front page shows the 廣 line).
