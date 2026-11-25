---
name: jmcomic
description: Use jmcomic (JMComic-Crawler-Python) to query JMComic metadata (album/photo details, search, rankings, comments) and to download albums or chapters, optionally exporting them to PDF, ZIP, or a long image. All commands return a single JSON object from one stable CLI entry point.
whenToUse: Use when the user supplies a JMComic album/photo id ("车号", JM123, or an 18comic album URL) and wants its metadata, wants to search/browse/rank JMComic works, wants comments, or wants to download/export an album or chapter. Do not use when the user is only asking about the upstream library's source code.
metadata:
  upstream: https://github.com/hect0x7/JMComic-Crawler-Python
  cli: scripts/jmctl.py
---

# JMComic via `jmctl.py`

Drive **JMComic-Crawler-Python** (`jmcomic`) through one wrapper that turns the library
into a stable JSON contract. The same engine (`scripts/jmcore.py`) backs the graphical
builds for Windows / Linux / macOS / Android, so anything done here the user can also do
by clicking.

## The one rule

**Call `scripts/jmctl.py` for everything. Never import `jmcomic` directly.**

The library logs progress to **stdout**, which corrupts machine parsing; `jmctl.py`
reroutes that logging to stderr and writes exactly one JSON object to stdout.

```bash
python <skill-dir>/scripts/jmctl.py <command> [options]
```

Success is `{"status": "ok", ...}`, handled failure is
`{"status": "error", "error": "...", "hint": "..."}` with exit code `1`. Run long
downloads as a background job and read stdout only when it settles — stderr is the live
progress log.

## Step 0 — environment

```bash
python <skill-dir>/scripts/jmctl.py doctor
```

Reports the interpreter, the `jmcomic` version, optional export dependencies, and site
reachability. To install, use **the interpreter `doctor` prints** (several Pythons often
coexist, and installing into the wrong one looks like "installed but still not
importable"):

```bash
"<that path>" -m pip install jmcomic
```

Install only the export extras the task needs:

| Format | Package |
|---|---|
| PDF | `Pillow` |
| ZIP | `pyzipper` (or `py7zr` for 7z) |
| long image | `Pillow` |

A missing dependency makes the download succeed while the export is silently absent, so
always check `exportFiles` in the result.

If `doctor` reports `networkOk: false`, do not retry blindly: switch `--client-impl`
between `api` (default) and `html`, or set a proxy in `option.yml`. Never guess a
replacement domain — the library resolves one itself.

## Commands

### `info` — metadata, no download

```bash
jmctl.py info 438696
jmctl.py info JM438696 https://18comic.vip/album/438696 --pretty
jmctl.py info 438696 --kind photo --image-urls
```

Accepts bare numbers, `JM123`, or URLs. `--kind album` (default) returns `title`,
`authors`, `tags`, `works`, `actors`, `pageCount`, `pubDate`, `updateDate`, `likes`,
`views`, `commentCount`, and `episodes`; `--kind photo` describes one chapter, and
`--image-urls` adds every page URL. An empty `episodes` is normal for a single-chapter
album — the album is then its own chapter and shares its id.

### `search` — find albums

```bash
jmctl.py search "MANA"
jmctl.py search "無修正" --mode tag --page 1
jmctl.py search "原神" --mode work
jmctl.py search "神里绫华" --mode actor
```

`--mode`: `site` (default), `tag`, `work`, `actor`. Filters: `--page`, `--order-by`
(`mr` latest, `mv` views, `mp` pictures, `tf` likes, `tr` score, `md` comments), `--time`
(`a` all, `t` today, `w` week, `m` month), `--category` (`0` all, `doujin`, `single`,
`short`, `another`, `hanman`, `meiman`, `doujin_cosplay`, `3D`, `english_site`),
`--sub-category` (html impl only, e.g. `chinese`, `japanese`, `CG`, `cosplay`, `youth`,
`3d`). `+tag` requires a tag, `-tag` excludes it: `"+全彩 +人妻"`.

Returns `total`, `pageCount`, `page`, and `works[]` of `{id, title, tags}`; feed an `id`
straight into `info` or `download`. When `total` disagrees with `count × pageCount`,
trust `works[]`.

### `rank` — rankings and category browsing

```bash
jmctl.py rank --period day
jmctl.py rank --period week --category doujin
jmctl.py rank --period custom --time m --order-by tf --category hanman
```

`--period` is `day`, `week`, `month`, or `custom` (arbitrary query from `--time` +
`--order-by`). Same result shape as `search`.

### `comments`

```bash
jmctl.py comments --id 438696
jmctl.py comments --forum --page 1
```

Returns `comments[]` with `content`, `nickname`, `likes`, `isSpoiler`, `createdAt`, and
nested `replies[]`. `--forum` reads site-wide comments, each carrying its `albumId`.

### `download` — fetch and optionally export

```bash
jmctl.py download 438696
jmctl.py download 438696 --export pdf
jmctl.py download 438696 123456 --export pdf zip
jmctl.py download 438696 --kind photo
```

`--kind album` (default) downloads every chapter, `--kind photo` one chapter. `--export`
takes `pdf`, `zip`, `png` (long image) and may combine them. Multiple ids download
concurrently and are reported individually — one failure does not abort the rest.

Single id returns `id`, `title`, `savePath`, `durationSec`, `imageCount`, `imageFiles[]`,
plus `exportFiles[]` with `--export`. Multiple ids return
`{total, succeeded, allSucceeded, results[], failed{}}`.

Images are cached on disk, so re-running the same command is cheap and is the correct
response to a partial failure. Incremental "only new chapters" needs the upstream
`find_update` plugin and is out of scope.

### `config` — configuration baseline

```bash
jmctl.py config                       # print the effective default option.yml
jmctl.py config --write ./option.yml  # write a starter file
```

### `doctor`

```bash
jmctl.py doctor
jmctl.py doctor --no-network          # interpreter and deps only
```

## Configuration

Three layers, most specific first: **CLI flags** (`--client-impl`, everything under
`download`) → **`option.yml`** (`--option <path>` or `$JM_OPTION_PATH`) → **jmcomic
defaults**. Generate a baseline with `jmctl.py config --write ./option.yml`, or read
`assets/option.example.yml` (ships with this skill, fully commented). The essentials:

```yaml
client:
  impl: api                  # api (default) | html; html is the only one with --sub-category
  postman:
    meta_data:
      proxies: system        # or null, or "127.0.0.1:7890"
      cookies: {AVS: <value>}  # only for login-gated albums, domain-scoped
download:
  cache: true                # reuse images already on disk
  image: {decode: true, suffix: null}     # decode restores JM's scrambled images
  threading: {image: 30, photo: 16}       # site allows <= 50 images
dir_rule:
  base_dir: ./downloads
  rule: Bd / Aid / Ptitle    # Bd=base_dir, A*=album field, P*=chapter field
```

`dir_rule.rule` composes album (`A`) and chapter (`P`) fields, e.g.
`Bd / Aauthor / (JM{Aid}-{Pindex})-{Pname}`; available fields are visible in
`jmctl.py info <id> --pretty`.

Cookies are domain-scoped: a cookie from one JM domain does nothing on another. Pass
credentials only via `option.yml` or `$JM_OPTION_PATH`, never on the command line, and
never echo them back into the conversation.

Login-gated features (favourites, check-in, favourite export) are deliberately not
wrapped. When needed, use the library's `login` plugin through a custom `option.yml`
instead of extending this CLI.

## Reporting results

- Quote `title`, the JM id, and the absolute `savePath` so the user can open the files.
- `likes` and `views` are site-formatted strings (e.g. `"77K"`), not integers.
- `updateDate: "0"` means unknown.
- For a cover, use `https://18comic.vip/album/<id>/`; do not invent a CDN URL.
- Respect rate limits: keep `threading.image` at or below 50, do not fan out many albums,
  and never loop `download` over a large id list — pass the ids to one invocation.
- If the user would rather click, point them at `python webui/server.py` (serves
  `http://127.0.0.1:<port>/?token=...` and opens the browser) or the packaged desktop /
  Android builds; they are front ends over this same engine.

## Troubleshooting

| Symptom | Cause and fix |
|---|---|
| `jmcomic is not importable` | Install into the interpreter `doctor` prints. |
| `could not parse a JM id` | Non-numeric id; extract the digits from the user's text first. |
| `MissingAlbumPhotoException` | Wrong id, or a login-gated album. Confirm the id before adding cookies. |
| `networkOk: false` | Try the other `--client-impl`, or set a proxy in `option.yml`. |
| Download ok but `exportFiles` empty | The format's dependency is missing, or the id produced no images. |
| `partial download failure` | Re-run the identical command; cached images are reused. Check `failedPhotos`/`failedImages`. |
| JSON parse error from stdout | Something wrote to stdout; confirm `jmctl.py` was invoked, not `jmcomic`/`jmv`. |

## Security and privacy

This skill downloads adult content. Keep it to what the user asked for, do not
auto-download from search results without confirmation, and never write credentials or
cookies into anything reported back.
