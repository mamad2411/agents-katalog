# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A local web viewer for FLEX paging traffic. An SDR app demodulates an NFM paging
channel into a virtual audio device (BlackHole on macOS); `decode.sh` pipes that
through `sox` → `multimon-ng -a FLEX` → a log file; `viewer.py` tails the log
and serves a single-page web UI at `http://127.0.0.1:8732/` over SSE.

The whole stack is intentionally tiny: one Python file (stdlib only, no
dependencies, no virtualenv), two shell scripts, no build step. There are no
tests.

## Run / develop

```bash
./start.sh                              # decoder + viewer together
./decode.sh & python3 viewer.py         # run them separately
DEVICE="BlackHole 16ch" ./start.sh      # override CoreAudio input device
LOG_PATH="/tmp/flex.log" ./start.sh     # override log path
```

There's no lint config and no test suite. Changes to the UI are tested by
opening `http://127.0.0.1:8732/` and watching live traffic (or replaying a
saved log by pointing `LOG_PATH` at it before starting the viewer — the viewer
primes from history on startup, then tails for new lines).

## Architecture

### Single-file Python server (`viewer.py`)

- **`tail_log()`** runs on a daemon thread, seeks to EOF, and reads new lines.
  Records can span multiple lines (continuation lines have no `FLEX` header),
  so it buffers until either the next `HEADER_RE` match or a 2-second idle
  flush.
- **`parse_record()`** handles two `multimon-ng` log formats:
  - `PIPE_RE` — the current pipe-delimited format
  - `LEGACY_RE` — the older space-delimited bracketed format
  Both must continue to parse — don't remove `LEGACY_RE` without checking real
  logs.
- **`/stream`** is an SSE endpoint. On connect, it pushes a single
  `event: history` with the full ring buffer (`HISTORY_SIZE = 500`),
  then streams each new page as a default `message` event. The HTTP handler
  is `ThreadingHTTPServer`, one thread per subscriber; broadcast fan-out is a
  per-subscriber `queue.Queue(maxsize=SSE_QUEUE_MAX)` guarded by `_state_lock`.
  A subscriber whose queue fills (client `SSE_QUEUE_MAX` pages behind / wedged)
  is dropped from fan-out so one stalled client can't grow memory without bound;
  its `EventSource` reconnects and re-primes from history.
- **`render_html()`** returns the entire UI (CSS + JS) inline. There is no
  static file serving — `/` returns HTML, `/stream` returns SSE, and
  `/labels` serves (GET) and updates (POST) the capcode-label store, and
  `POST /clear` (loopback-only, same guard as `POST /labels`) truncates the log in
  place, empties `_history`, and sends an SSE `event: cleared` — labels untouched,
  and `tail_log()` rewinds when it sees the file shrink; everything
  else 404s. Every GET enforces a Host allowlist (`_allowed_get_hosts`: loopback
  + the detected LAN IP + any `$ALLOWED_HOSTS`) to block DNS-rebinding reads of
  the feed/labels — a rebound attacker domain sends its own name as `Host` and
  gets 403. DOMPurify is loaded from jsDelivr, pinned with an SRI `integrity`
  hash (recompute it if you bump the version, or the browser will block it).

Config lives as constants at the top of `viewer.py` (`LOG_PATH`, `PORT`,
`HISTORY_SIZE`, `MAX_BODY`, `SSE_QUEUE_MAX`). `LOG_PATH` is overridable via env
in the shell scripts; `ALLOWED_HOSTS` (comma-separated extra GET hosts) is read
from env in `main()`.

### Frontend (inline JS in `viewer.py`)

The non-obvious behavior is concentrated in three places:

1. **Multi-fragment stitching** (`shouldStitch`, `findStitchTarget`). FLEX
   caps a page at ~248 chars, so long messages arrive as 2–3 consecutive
   pages to the same capcode. The viewer merges them in two contexts:
   - **Live** (`addPage`): scans up to 30 recent pages (other capcodes can
     interleave) and stitches if same proto+capcode+ALN, within 5 OTA frames
     (`frameDistance` handles cycle 14 → 0 wraparound), and the prior fragment
     doesn't already end in terminal punctuation (`looksComplete`).
   - **History prime** (`history` event handler): re-runs the same stitch
     logic over the oldest-first history array before reversing to display.
   Both paths must stay in sync — if you change stitching rules, change both.

2. **Type bucketing** (`bucket`). The four UI chips are ALN/NUM/TON/TEST, but:
   - `TEST` is not a FLEX type — it's any body matching `THIS IS A TEST
     PERIODIC PAGE` (carrier test pages). These render dimmed.
   - ALN pages whose body is purely digits/whitespace/hyphens get rebucketed
     as NUM, so the NUM chip hides callback numbers and beeper codes whether
     the decoder labeled them ALN or NUM.

3. **Body formatting** (`structureBody`). Pages packed with `Label:value`
   pairs separated by spaces (no newlines) get a newline inserted before each
   label. The regex deliberately:
   - Treats 2-char labels strictly (must end at the colon — no multi-word
     extension), so "PM Time…" can't be captured as a label
   - Allows 3+ char labels with up to 20 chars of multi-word body
   - Excludes underscores from the first character class so underscore-joined
     identifiers don't get swallowed
   - Refuses a `/` right after the colon to skip URLs (`HTTP://...`)
   Only lines with **2+** label hits get rewritten — a single `Label:` per
   line is left alone. After structuring, `\n` → `<br>` and the result goes
   through DOMPurify with a tight allowlist (`b i u em strong br font`,
   attr `color` only — `style` is intentionally excluded so OTA bodies can't
   smuggle CSS beacons). DOMPurify is the only path that writes HTML into
   the DOM — keep it that way.

State that persists: `enabledTypes` in `localStorage` under
`flexViewer.enabledTypes`.

### Capcode labels and callback hints

- **Labels** are a `capcode → name` map. They live server-side in
  `labels.json` (atomic writes), are served by `GET /labels`, and updated by
  `POST /labels` ({"capcode","label"}; empty label deletes).
  `POST /labels` also accepts a bulk form `{"capcodes": [...], "label": "X"}` (one
  atomic write, capped at `MAX_BULK`) used by group-tagging.
  The client holds a
  `labels` object, fetched once via `loadLabels()`, and re-renders all pages on
  change. Keys use the same leading-zero-stripped capcode form as the feed. The
  POST handler is loopback-only (Host/Origin guard — stricter than GET's host
  allowlist, so LAN-share clients stay view-only), validates capcode (digits,
  ≤10) and label (≤64, `<`/`>` stripped), and caps total labels.
- **Callback hints** are computed server-side: `phone_hints()` runs `PHONE_RE`
  over the body and maps NPA-NXX → town via `_npa_nxx`, attached as `rec["hints"]`
  in `parse_record` (covers history + live). The table is loaded once by
  `load_npa_nxx()` in `main()` (read-only, no lock); a missing
  `data/npa-nxx-on.json` silently disables hints. Regenerate the dataset with
  `python3 build_npa_nxx.py` (pulls CNAC per-NPA CSVs); `--check` runs offline
  self-tests. Labels and hints render via the `el()` helper (textContent only),
  never through DOMPurify.

### Group-tagging

A "group broadcast" is one message sent to many pagers at once (e.g. a trauma
team activation). `findGroup(page)` (client) finds the distinct capcodes that
received an **identical body within `GROUP_TIME_WINDOW` seconds** (keyed on the
`ts` field — broadcasts spread across FLEX home frames, so wall-clock proximity,
not frame distance, is the grouping axis; TEST pages excluded; `≥ GROUP_MIN_SIZE`
distinct capcodes to count). When you edit a label on a page that's part of a
group, the editor shows a default-checked "also tag N others" checkbox; checked +
Enter bulk-tags the whole broadcast (overwrite) via the bulk `POST /labels`.

## Things to know before changing parser regexes

- The `ts` field in the JSON record is **time-only** (`HH:MM:SS`); the date
  is split into `date`. The UI only shows `ts`. If you add date display,
  update both the prime and live paths.
- `capcode` has leading zeros stripped (`"0001234567"` → `"1234567"`).
  The click-to-filter compares as substring on the displayed form.
- `MAX_BODY` truncation appends an ellipsis character (`…`, not `...`).

## Privacy / publishing

Real FLEX traffic on commercial channels routinely contains PHI (hospital
pages with patient names, MRNs), dispatch traffic, and industrial alarms.
Never paste real decoded page bodies into commit messages, issues, PRs, or
test fixtures. Use the synthetic examples already in the README if you need
illustrative data.
