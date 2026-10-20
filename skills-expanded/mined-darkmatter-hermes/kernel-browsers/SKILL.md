---
name: kernel-browsers
description: >-
  Use when Cooper wants OnKernel / `kernel` cloud browsers (browser automation,
  Playwright, profiles, live-view HITL), AA.com booking in a remote browser, or
  "generate a URL when stuck" on a Kernel session — instead of Studio cua or Camofox.
version: 2.2.1
metadata:
  hermes:
    tags: [kernel, onkernel, browser, playwright, cloud, booking, profiles, hitl]
    category: devops
    related_skills: [studio-cua-drive, agent-browser, camofox, bluebubbles-studio, vapi-phone-ops]
---

# Kernel browsers (OnKernel CLI)

## When
- Cloud browser VM for booking/scraping **without** occupying Studio/Pro Chrome
- Real **DOM Playwright** (Angular/Material ladders) beats AX
- Durable site state via **profiles** (cookies/login)
- User must take over → **live view URL** (HITL)
- User pastes Kernel CLI docs or says “use Kernel”

## Auth (non-interactive)
CLI: `/opt/homebrew/bin/kernel` (~0.20+). API: `https://api.onkernel.com`

```bash
export KERNEL_API_KEY=<REDACTED>
kernel auth status   # Authentication method: API Key
```

- **Himitsu only** — never bare biometric `op` prompts for this.
- `kernel login` (OAuth browser) only if Cooper explicitly allows.
- Do not thrash `browsers create` while unauthenticated.

## Session lifecycle
```bash
kernel browsers create --stealth -t 900 \
  --viewport 1440x900@25 \
  --start-url 'https://www.aa.com/booking/find-flights' \
  --name aa-book-test -o json
# JSON includes: session_id, browser_live_view_url, cdp_ws_url

kernel browsers playwright execute <session_id|name> --timeout 120 -o json < script.ts
kernel browsers computer …          # OS-level click/type/screenshot fallback
kernel browsers delete <id-or-name>
```

## Viewport: go BIG before driving a form (Cooper preference)
Small viewports force scroll-hunting and overshoot. **Max the viewport first** — more page per screenshot = far fewer round trips.

```bash
kernel browsers update <id-or-name> --viewport 2560x1440@10 --force
```

- Presets: **2560x1440@10** (max, use this), 1920x1200@25, 1920x1080@25, 1440x900@25, 1280x800@60, 1200x800@60, 1024x768@60
- `--force` is required when a **live view / recording is active**, else the resize is refused
- Resize works on a **running** session — no need to recreate; live URL stays the same
- Cooper explicitly asked for this ("make it even bigger, you will have an easier time that way"). Default to 2560x1440 for any booking/checkout drive.
- **Resize FIRST, before the first screenshot of a form.** The Aug-3 run wasted ~8 scroll/screenshot round trips ping-ponging between the flight rows and the footer at 1440x900; after the bump to 2560x1440 the date carousel, fare columns and 3 flight rows were all readable in **one** capture and every subsequent click landed first try. If you catch yourself scroll-hunting for a control, stop and resize instead of scrolling again.

## Computer-use drive cadence (VALIDATED — completed AA passenger + payment)
Order Cooper wants: **computer use first, Playwright only as fallback.**

```bash
kernel browsers computer screenshot <id> --to /tmp/s1.png     # then vision_analyze for coords
kernel browsers computer click-mouse <id> --x 1449 --y 665
kernel browsers computer type       <id> --text "Telavaya"    # NOTE: `type`, flag --text
kernel browsers computer scroll     <id> --x 1280 --y 700 --delta-y 400
kernel browsers computer press-key  <id> --key ctrl+a
```

Loop: **screenshot → one `vmap.py` sweep → act by control type → re-sweep to verify.** Batch only mapped text/email/tel inputs; never batch blind clicks or `<select>` commits.

### ⭐ THE DRIVE LOOP: one `vmap.py` sweep per screen, then act
**Do not ask vision for one element at a time.** Take a screenshot, map the WHOLE
screen in a single call with `scripts/vmap.py`, then drive off that map.

```bash
set -a; source ~/.hermes/.env; set +a          # OPENROUTER_API_KEY lives here, not himitsu
SKILL=~/.hermes/skills/devops/kernel-browsers
kernel browsers computer screenshot "$SID" --to /tmp/s.png
python3 $SKILL/scripts/vmap.py /tmp/s.png --plan
```

Returns every interactive element with **ref, type, label, x, y, value, state** —
works on forms, **fare ladders, date carousels, modals, cookie banners**, not just forms:

```
 ref  type      label                          x     y  value/state
  e9  tab       date_mon_aug_3               1283   663  $836
 e24  select    flight_1_main                1267   901  $836
 e25  button    flight_1_main_extra          1443   914  Not available
 e20  button    select_main                  1161  1187  $946
 e11  select    state_province               1262   699  Select state  [disabled]
```

Why this is the win:
1. **~1 vision call per screen** instead of one per field — the real latency fix.
2. **`value` doubles as verification** — re-run the sweep after acting and read back
   `first_name=Telavaya`, `state_province=CALIFORNIA`. No separate check step.
3. **`type` tells you how to drive it** (`--plan` groups it for you):
   - `text/email/tel` → **batchable**, chain in one `computer batch`
   - `select` → **one at a time**: click → type-to-jump → Enter → verify
   - `button/link/tab/row` → single click
4. **`state` catches ordering constraints** — e.g. `state_province [disabled]` until
   country is set. That exact dependency broke earlier runs.

### `computer batch` — nested payload shape (easy to get wrong)
Each action needs a **nested object keyed by its own type**:
```bash
kernel browsers computer batch "$SID" --actions '{"actions":[
{"type":"click_mouse","click_mouse":{"x":870,"y":480}},
{"type":"type_text","type_text":{"text":"Telavaya"}},
{"type":"click_mouse","click_mouse":{"x":1654,"y":480}},
{"type":"type_text","type_text":{"text":"Reynolds"}}
]}'
```
Flat `{"type":"click_mouse","x":870,"y":480}` → `ERROR: click_mouse field is required`.

**Batch limitation (measured):** batching `press_key Return` to commit a `<select>`
**silently fails** — the sweep showed all six dropdowns still empty after a batched run.
Text inputs batch fine; **selects must be discrete `click-mouse` / `type` / `press-key`
calls**. Verify with a sweep before trusting either.

### ⚠️ Ask vision for `box_2d`, NEVER raw pixel coords
Asking Gemini for `[x,y]` pixels fails **bimodally** — ~2px perfect or ~178px wrong, because
on bad runs it measures Y against the page content area and drops the ~391px Chrome
toolbar (`1440/1.373 ≈ 1049`). X is always fine; **only Y breaks**. One row off = typing
into the wrong field.

**Always request Gemini's native convention — normalized 0–1000, `[ymin,xmin,ymax,xmax]` (y first):**
```
Detect the form input controls in this <page>.
Report these items: first_name, last_name, dob_month, gender, state_province
Output ONLY a JSON array, Gemini box_2d convention, normalized 0-1000:
[{"label":"first_name","box_2d":[ymin,xmin,ymax,xmax]}, ...]
```
```python
x = ((xmin+xmax)/2)/1000 * real_w
y = ((ymin+ymax)/2)/1000 * real_h
```
Measured: raw pixels **3/10 clean** → box_2d **10/10 clean**, and it makes cheap models
work too (`gemini-3.1-flash-lite` 9/9 @ 2.7s / $0.0007). There is **no image-dimension
metadata** in the API response, and asking the model to self-report its frame returns a
bogus constant `1920x1080` — don't bother. Full detail: **`references/vision-coordinates-box2d.md`**.

Configured aux model: **`google/gemini-3.6-flash`**.

**Use the packaged helper — don't re-derive this every session:**
```bash
set -a; source ~/.hermes/.env; set +a     # OPENROUTER_API_KEY lives HERE, not himitsu
python3 ~/.hermes/skills/devops/kernel-browsers/scripts/vcoord.py shot.png \
  first_name_input last_name_input save_button
# first_name_input	870 479
# last_name_input	1656 479
kernel browsers computer click-mouse "$SID" --x 870 --y 479
```
`scripts/vcoord.py` does the box_2d request + rescale for you and prints
`label<TAB>x y`. Validated end-to-end on a full AA search→passenger→contact drive:
every coordinate it returned landed first try, including an exact match to the
known-good hand-verified values (870,479 / 1656,479 / 760,581 / 1262,581).

### `vcoord.py` vs `vision_analyze` — pick by question type
| Need | Tool | Why |
|---|---|---|
| **Click targets / pixel coords** | **`scripts/vcoord.py`** | Forces box_2d JSON + deterministic rescale. 10/10 clean. |
| **Page state, errors, "did it save?"** | **`vision_analyze`** | Prose is the right shape for judgment. |

`vision_analyze` returns **narrative text with no coordinate contract** and does no
box_2d rescale — parsing coords out of its prose is exactly the fragility that caused
the 178px Y-bug. Never use it to decide where to click.

### Don't touch `agent.image_input_mode` to "speed up vision"
Tried this session and **reverted to `auto`** — it is the wrong lever:
- `auto` (**correct, leave it**) — vision-capable main model sees real pixels; aux Flash is fallback
- `text` — degrades **Cooper's own attached images** to lossy prose, and makes
  `vision_analyze` return an `{"success":true,"analysis":"…"}` blob. Worse for both jobs.
- Changing `auxiliary.vision.model` alone does **not** reroute the drive loop: with a
  native-vision main model `vision_analyze` stays native by design
  (`tools/vision_tools.py`: `if decide_n(...) != "native"`). Cooper caught this —
  *"it also just used the built in vision model, i thought we disabled this?"*
- Config edits do not require a restart, but they also don't fix the coordinate path.
  **The fix is calling `vcoord.py` explicitly**, not global config.

### Speed: the bottleneck is ROUND TRIPS, not any one tool
Measured on a live 2560x1440 session (2026-07-31):

| Op | Wall time |
|---|---|
| `computer screenshot` (full 2560x1440, ~130KB PNG) | **0.9–1.6s** |
| `computer type` | **~0.7s** |
| `computer click-mouse` | **~4s** ← slowest Kernel call |
| `vision_analyze` on a full-frame PNG | **~5–15s** ← dominant cost |

A naive `screenshot → vision → click → screenshot → vision …` loop is **~15–25s per field**.
The AA passenger+payment drive was ~30 interactions ⇒ most of the elapsed time was
vision re-reads of a 3.7-megapixel image, **not** Kernel and **not** the network.

**Cooper asked "is it the vision model that is slow?" — root cause turned out to be the
PROMPT FORMAT, not the model.** Raw-pixel prompts made every model unreliable and forced
reliance on the slowest one. Switching to **`box_2d` normalized 0–1000** (see above) made
3.6-flash 10/10 clean at 5.1s, and even flash-lite perfect at 2.7s/$0.0007.
Historical benchmark of raw-pixel prompting across 12 models:
**`references/vision-model-benchmark.md`** (superseded by box_2d, kept for the negative result).
Bigger viewport buys accuracy and costs latency; don't undo it — reduce vision **calls**.

> **SUPERSEDED — read `references/vision-coordinates-box2d.md` first.** The table below
> measured *raw-pixel* prompting, where the only usable option looked like main-model
> native vision. With **box_2d** prompting (`scripts/vcoord.py`) that conclusion no longer
> holds: `gemini-3.6-flash` is 10/10 clean at ~5s, and even `gemini-3.1-flash-lite` is
> 9/9 at 2.7s/$0.0007. Kept for the negative result and the routing note.

#### Which vision model is actually running (CHECK FIRST)
`auxiliary.vision.model` in `~/.hermes/config.yaml` is often **not** what runs. With
`system.image_input_mode: auto` and a main model that has native vision (e.g.
`anthropic/claude-opus-5`), Hermes attaches the PNG **straight into the main model's
context** and `vision_analyze` replies *"Image loaded into your context."* — the aux model
never fires. Don't tune aux config before confirming which path is live.

Benchmarked on one real AA screenshot:

| Model | Time | Reasoning tok | Cost | Coords |
|---|---|---|---|---|
| main model native (Opus 5) | ~5–15s | n/a | premium | **best**, landed first try |
| `google/gemini-3.5-flash` | **10.6s** | **1,489** | **$0.0194** | **wrong scale** ❌ |
| `google/gemini-2.5-flash` | **2.8s** | 0 | **$0.0008** | roughly right, not exact |

`gemini-3.5-flash` **cannot disable reasoning** (`HTTP 400: "Reasoning is mandatory for
this endpoint and cannot be disabled"` — both `reasoning.enabled:false` and
`reasoning.max_tokens:0` are rejected), so it burns ~1.5k reasoning tokens to find a
button: ~4x slower, ~24x pricier, and it returns **downscaled** coords that would make
clicks miss. **Avoid it for coordinate work.** Use `gemini-2.5-flash` for cheap checks
("what page am I on", is the error banner up?) and keep **main-model native vision for
coordinate-critical clicking** — a missed Pay-now click costs far more than 10 seconds.

Re-measure instead of guessing: `scripts/bench-vision-model.py <shot.png> [models…]`.
`OPENROUTER_API_KEY` lives in `~/.hermes/.env` (**not** himitsu, not exported into the
agent shell) — `set -a; source ~/.hermes/.env; set +a` first.
Full write-up: `references/vision-model-latency.md`

#### Four fixes (all CLI, all cheap)
1. **`computer batch`** — many actions in ONE round trip:
   ```bash
   kernel browsers computer batch <id> --actions '{"actions":[
     {"type":"click_mouse","x":869,"y":479},
     {"type":"type_text","text":"Telavaya"}
   ]}'
   ```
   Would collapse a name/card block from 4–8 calls into one.
   **UNVALIDATED — read off `--help`, never exercised on a real form.** Confirm exact
   action `type` names with `kernel browsers computer batch --help` and try it on a
   throwaway field before trusting it mid-checkout.
2. **Region screenshots** — `--x --y --width --height` crops to just the form:
   ```bash
   kernel browsers computer screenshot <id> --x 650 --y 400 --width 900 --height 700 --to /tmp/form.png
   ```
   Far fewer pixels ⇒ materially faster vision, and coords still map to page space
   (add the region origin back when clicking).
3. **Don't vision every step.** Vision once to map a stable form, then batch 3–4
   fills blind, then **one** verify screenshot. Only re-vision after navigation,
   a modal, or an unexpected result.
4. **Reuse known-stable coords.** Once a `<select>` list is open, the option rows are
   predictable — click without a fresh vision pass.

Keep full-frame 2560x1440 for **recon / after navigation**; use crops + batch for **filling**.

### Native `<select>` dropdowns — type to jump, don't scroll
AA DOB year/state/country lists are long; wheel-scrolling overshoots badly (1926↔2026 ping-pong).
**Click the select to open, then `computer type --text "1991"`** — the option highlights instantly. Then click it.
Same for `California`, `United States`.

### Clearing a field before retype
`click-mouse` → `press-key --key ctrl+a` → `press-key --key Delete` → `type`. Used to fix the Expiration field after AA flagged "Enter a valid date."

### Card data shape (Amex, from himitsu SA vault `cm`)
- 1P `expiry` is stored **`203105`** (YYYYMM) → AA wants **`05/31`**
- Amex CVV is **4 digits**; the field label is `CVV` and sits right of Expiration
- Card number typed raw with no spaces; AA shows the AMEX badge when accepted

## Replays — start recording BEFORE the run, not after
Kernel can record a real video of a session, but **only from the moment you start it**.
There is no retroactive capture. Cooper asked *"i missed it, can you get me a replay"*
after a long drive and `replays list` returned `[]` — the run was unrecoverable.

```bash
SID=$(cat /tmp/sess_sid.txt)
kernel browsers replays start "$SID" -o json     # → replay_id + replay_view_url
# … drive the session …
kernel browsers replays stop "$SID" <replay-id>
kernel browsers replays list "$SID" -o json
kernel browsers replays download "$SID" <replay-id> --to /tmp/run.mp4
```

**Rule: on any drive Cooper may want to review — bookings, checkouts, demos, "run a
simulation" — call `replays start` immediately after `browsers create`, before the first
screenshot.** It is cheap insurance; an unrecorded run cannot be reconstructed.

Stitching screenshots into an mp4 with ffmpeg is a **poor substitute** (no cursor, no
timing, no intermediate frames) — Cooper rejected it outright: *"this doesnt work we need
to start over"*. Don't offer it as an equivalent; if the run wasn't recorded, say so
plainly and re-run with recording on.

Note: `--force` is required on `browsers update --viewport` while a replay/live view is
active (already noted in the viewport section).


```bash
kernel profiles create --name aa-cooper-test -o json
kernel browsers create --name job --profile-name aa-cooper-test --save-changes \
  --stealth -t 600 --start-url 'https://www.aa.com/' -o json
# … automate / human in live view …
kernel browsers delete job          # REQUIRED to persist — not context/page.close()

# later — state should reload
kernel browsers create --name job2 --profile-name aa-cooper-test --stealth -t 300 \
  --start-url 'https://www.aa.com/' -o json
```

**Validated:**
- Cookie + `localStorage` on `.aa.com` survived delete → recreate (`aa-cooper-test`).
- **Gmail profile `cooper-email`:** Cooper live-view login → delete → recreate still on `mail.google.com` inbox (accounts seen: `me@cm.xyz` u/0, `cooper@darkmatter.io` u/1). Check SID/__Secure-1PSID + inbox title before claiming login.

Notes:
- `--save-changes` on create if writes should flush on end. If get JSON omits a save flag, still delete after successful human login and re-open profile to verify cookies.
- Empty `profiles list` ⇒ create first. `--profile-id` **xor** `--profile-name`.
- Browser pools: profile is **read-only** (`save_changes` ignored).

## HITL / “stuck → give me a URL”
**Always put the live (or hosted) URL in the user-facing reply immediately** — never only in tool logs / after a long poll.

| Source | Command / field |
|---|---|
| Create JSON | `browser_live_view_url` |
| Anytime | `kernel browsers view <id-or-name>` → plain URL (`-o json` → `liveViewUrl`) |
| Full detail | `kernel browsers get … -o json` |
| Managed Auth | `hosted_url` from `auth connections login` |

Also: Playwright `page.url()`; AA cart `sid` expires — don’t reuse dead trip-summary links. Live GET is often **302 + jwt** — share URL, don’t curl for UX.

**Preferred Gmail HITL:** live browser on profile + Cooper drives Google login (same control UX as booking). **Hosted Managed Auth is secondary** for Google (see below).

**HITL loop:** URL → pause → Cooper acts → resume Playwright on same session → optional `browsers delete` to save profile.

No separate Kernel `ask_human` tool — HITL = live view (**or** hosted login) + pause.

## Managed Auth + 1Password (site logins on a profile)
Docs: https://www.kernel.sh/docs/auth/overview — **website** sessions, not API-key auth to Kernel.

### Google / Gmail preference order
| Path | Result / use |
|---|---|
| **Live browser** + `--profile-name cooper-email --save-changes` | **Primary** — Cooper controls browser; cookies persist after delete |
| Hosted UI (`auth connections login` → `hosted_url`) | **Unreliable** — fell `stuck_in_loop` / “page not advancing”; OK to offer as alternate, not sole path |
| Passkeys | Managed Auth **unsupported** (`unsupported_auth_method`) |

Live Gmail setup that worked:
```bash
kernel browsers create --name cooper-gmail-hitl --profile-name cooper-email \
  --save-changes --stealth -t 900 \
  --start-url 'https://accounts.google.com/ServiceLogin?service=mail&continue=https://mail.google.com/mail/' \
  -o json
# Immediately reply with browser_live_view_url / browsers view …
# After Cooper done: verify mail.google.com + cookies → browsers delete → recreate to prove profile
```

### 1Password provider (himitsu SA — no GUI)
```bash
export KERNEL_API_KEY=<REDACTED>
export OP_SA_TOKEN=<REDACTED>
kernel credential-providers create --provider-type onepassword \
  --name cooper-1p --token "$OP_SA_TOKEN" -o json
unset OP_SA_TOKEN
kernel credential-providers test cooper-1p -o json   # vaults SA can see
```
Provider `cooper-1p` saw vaults **cm / cooper / dev**. **`list-items` had no Google/Gmail login** — auto domain match cannot fill Gmail until a Login item with google/gmail URLs exists in an SA-readable vault. Until then: **live-view seed only**.

When item exists:
```bash
kernel auth connections create --profile-name cooper-email --domain gmail.com \
  --login-url 'https://accounts.google.com/ServiceLogin?service=mail&continue=https://mail.google.com/mail/' \
  --allowed-domain google.com --allowed-domain accounts.google.com \
  --credential-provider cooper-1p --credential-auto -o json
```
Avoid interactive `connections delete` prompts that hang agents (confirm flags / expect y prompt).

Hosted login / connection lifecycle detail: `references/managed-auth.md` · Gmail+1P notes: `references/gmail-profile-and-1p.md`
## Prefer agent-browser plain-text snapshots (not giant Playwright blobs)
Ad-hoc `playwright execute` megascripts are brittle on AA (shadow DOM, cookie banners). When you need **simple agent-oriented UI text** (a11y tree + refs, no HTML), route through **agent-browser** — native Kernel provider or CDP connect.

Official docs: https://www.kernel.sh/docs/integrations/agent-browser · Hermes plugin: https://www.kernel.sh/docs/integrations/hermes-agent

### Option A — native provider (simplest)
```bash
export KERNEL_API_KEY=<REDACTED>
# optional: KERNEL_STEALTH=true KERNEL_TIMEOUT_SECONDS=900 KERNEL_PROFILE_NAME=cooper-email
agent-browser -p kernel open 'https://www.aa.com/booking/find-flights'
agent-browser snapshot -i          # interactive-only a11y refs @e1 @e2 …
agent-browser snapshot --compact --depth 8
agent-browser fill @e3 'LAX'
agent-browser click @e12
agent-browser close                # ends local attach; provider may still need kernel browsers delete
```

### Option B — existing Kernel session via CDP
```bash
CDATA=$(kernel browsers get aa-telavaya-ticket -o json)
CDP=$(echo "$CDATA" | python3 -c 'import sys,json;print(json.load(sys.stdin)["cdp_ws_url"])')
LIVE=$(echo "$CDATA" | python3 -c 'import sys,json;print(json.load(sys.stdin)["browser_live_view_url"])')
echo "HITL $LIVE"
agent-browser connect "$CDP"
agent-browser snapshot -i
# drive with @refs; re-snapshot after each nav
```

### Option C — Hermes browser tools on Kernel
```bash
hermes plugins install kernel/hermes-browser-plugin --enable
hermes config set browser.cloud_provider kernel
hermes config set browser.inactivity_timeout 600   # match plugin ~10m browser timeout
# KERNEL_API_KEY in profile .env (hermes config env-path); himitsu → writekey there if needed
hermes tools post-setup agent_browser
```
Desktop: Capabilities → Browser Automation → **Kernel**. Verify with `browser_navigate` + `browser_snapshot` to example.com and check Kernel dashboard (not just success).

### Snapshot hygiene (what “good” looks like)
- Output is **plain text a11y tree** with `@eN` refs — no HTML dump
- Prefer `snapshot -i` (interactive) or `--compact`; re-snap after every navigation
- Act only on current refs; never reuse stale `@eN` across pages
- Still send **live view URL** when stuck or asking Cooper to take over
- Kernel still recommends computer-use / playwright-execute for high bot-sensitivity; CDP/`agent-browser` is fine when the **readable recon** payoff matters more than bot surface
- Detail: `references/agent-browser-plain-text.md`

### CDP blank-tab trap
`agent-browser connect $CDP` often lands on **`about:blank`** while Kernel Playwright still has AA open. Always `tab list` + open/`bringToFront` passenger-ui **before** declaring the form dead. Re-snapshot after every nav; parse refs from **indented** lines (skip `option "` rows).

### Anti-pattern
Do **not** keep authoring 100+ line one-shot Playwright delete/fill/pay scripts in `playwright execute` when a snapshot→ref loop would work. Use short Playwright only for known stable ids or shadow-root helpers after a snapshot-driven map. Never fill AA passenger by “Nth large input” — **last name can swallow email**; key on `aria-label`.

### "Stop writing scripts" — heed it immediately
Cooper said **"please only use the cli, dont write scripts"** and later **"keep going, but stop writing scripts."** When that lands:
- Switch to `kernel browsers computer …` subcommands + screenshots. Nothing else.
- If Playwright is genuinely needed, pipe a **one-line** stdin snippet (`printf '%s\n' 'return {url: page.url()};' | kernel browsers playwright execute <id> --timeout 20 -o json`) — never a generated `/tmp/*.js` file per step.
- Repeatedly regenerating `/tmp/k_*.js` after being told to stop is the exact behavior that burned this session. Heredoc/`write_file` script churn also invites encoding corruption (stray non-ASCII sneaking into generated JS/Python, causing `SyntaxError: invalid character`) — another reason the CLI path is safer.

**It took three corrections in one session** — "please only use the cli, dont write scripts",
then "please use computer use first, then playwright as fallback", then "keep going, but stop
writing scripts." Treat the first one as binding for the rest of the session. The pure-CLI
computer-use run that followed booked the ticket cleanly with zero script files, so this is
not a handicap — it is the faster path. Default to it on any AA/checkout drive without
waiting to be told.

### When a helper tool breaks, fix the root cause — don't downgrade
Cooper: **"if vision tool fails, dont just go to a workaround that wont work as well, lets try to fix it."**
Vision died with `'DaemonThreadPoolExecutor' object has no attribute '_initializer'` → real Python 3.14 API change, not a broken feature. Diagnose and patch (see `references/python314-daemon-pool-vision.md`), then resume with the good tool. Falling back to pixel-guessing without vision made the drive materially worse.

### User preference: recon vs drive
Cooper wants **observations** agent-browser-shaped (plain a11y text + `@eN`, no HTML). That does **not** mean agent-browser fill is preferred for AA passenger/payment:
- **Recon:** `snapshot -i` / compact a11y (or AX text on Studio) — good
- **AA passenger form / pay:** **computer use + vision screenshots** (or careful aria shadow fill). Agent-browser `@fill` mis-mapped phone→loyalty and skipped State/CA
- Always surface **live URL immediately** when stuck; when cart is Ready (e.g. `$945.50` + Enter new passenger), prefer handing the link over ROI-chasing DOM spaghetti
- **Loyalty must stay blank** unless Cooper asks; **email `telvaya@icloud.com`** (not pelavaya); **State = California**
- **Phone for Telavaya passenger = `+1 206-954-2027`**, never Cooper’s `310-989-7067`. Debasor was texting 206 for ticket digits / warm-transfer; Cooper called out “that’s MY phone” when 310 was stuffed into pay payload
- **CLI over script files:** when Cooper says only use CLI / don’t write scripts — use `kernel browsers computer *`, short `playwright execute` **stdin one-liners**, `browsers view`. No thrashing long generated `/tmp/k_*.js` per step
- Live-view freeze on one field (phone): fill **that field only** via one small evaluate / computer type; don’t restart whole passenger wizard

Detail: `references/aa-passenger-form.md` · **validated computer-use drive (big viewport, select type-to-jump, full Aug-3 sequence): `references/aa-passenger-computer-use.md`** · phone/identity: `references/aa-telavaya-identity.md`

## Playwright execute rules (keep for known-stable ids)
Kernel injects **`page`**, **`context`**, **`browser`**. **Do not redeclare** (`Identifier 'page' has already been declared`).

1. Prefer **stable DOM ids** (`#matOriginAirport`, `#matDestinationAirport`, `#trip-type`, `#matDepartureDatePicker`).
2. AA **swap** button steals `getByLabel(/To/)` — use destination **id**.
3. Trip type defaults Round trip; `#trip-type` → **One way** before date.
4. Date may be `h:0/w:0` — set via JS `value` + `input`/`change`/`blur` if click times out.
5. Fare ladder: open Main teaser → **`Select One way Main fare for $946`** (not Basic $836). Prefer `querySelectorAll('button')` + `includes` over fragile hasText.
6. Stay in Main / Continue as guest OK; **never Purchase/Pay now** without Cooper gate.
7. Split long work — execute can abort on timeout; check `success` + `result.url` before fail.
8. **Success may be early** with hard URL/total evidence; **failure only after** full execute JSON (same discipline as Vapi logs).

## AA smoke (validated 2026-07-31)
One-way LAX→LHR Aug 2 → **AA 6935** Main · trip-summary **Total ~$945.50**.
Passenger/checkout is a separate unreliable stage — see `references/aa-passenger-form.md`.

### Full booking completed 2026-07-31 (Aug 3 LAX→LHR)
Whole funnel driven **computer-use-only at 2560x1440**, no generated script files:
search → date tile → Main $946 → Stay in Main → Continue as guest → passenger →
contact → Review and pay → decline Allianz → Amex → **Pay now** → SafeKey code → confirm.
Result: AA **OYVTLE** / BA **CEP4TZ**, ticket **0012364615262**, status **Ticketed**, $945.50.
Checkout + 3DS + confirmation detail: **`references/aa-checkout-3ds-confirmation.md`**

Also: `references/aa-kernel-booking.md` · Managed Auth: `references/managed-auth.md` · Gmail+1P: `references/gmail-profile-and-1p.md` · plain-text driver: `references/agent-browser-plain-text.md` · session notes: `references/aa-session-2026-07-30-notes.md` · **coordinate helper: `scripts/vcoord.py` + `references/vision-coordinates-box2d.md`** · vision latency/benchmark (superseded, negative result): `references/vision-model-latency.md` · `references/vision-model-benchmark.md` · `scripts/bench-vision-model.py`

## Contrast
| Path | Best for |
|---|---|
| **Kernel** | Ephemeral DOM automation, profiles, live-view HITL, no Studio seat |
| **Studio cua** (`studio-cua-drive`) | Logged-in **local** Studio Chrome via SSH+cua |
| **Camofox** | Stealth headless on NixOS |

## Pitfalls
| Issue | Fix |
|---|---|
| Auth required | `himitsu read kernel-api-key` |
| `page` already declared | Don’t rebind injected globals |
| Label matches swap | `#matDestinationAirport` |
| Date invisible | One way first; JS value fallback |
| Execute timeout | Split steps; exact button text |
| AA `sid` session-timeout | Re-search; use **Kernel live URL** for HITL not dead AA links |
| Gmail Hosted UI `stuck_in_loop` | Prefer **live view** + profile save; Hosted UI unreliable on Google |
| Google passkeys | Managed Auth unsupported — live view / password+TOTP |
| 1P SA has no Google item | Add Login with google/gmail URL in cm/cooper/dev **or** live-view seed only |
| Spoken `001…` ticket | Prove on aa.com — STT wrong (`0012342708964` rejected) |
| Failure mid-run | Full execute JSON + URL before declaring fail |
| 1Password GUI / bare `op` | Never — himitsu `read` / `exec op-service-account/token` only |
| BB ticket ask default 310 | When Cooper says **206**, Studio BB → **+12069542027** |
| CDP lands on about:blank | `tab list`; open/bringToFront real AA URL; re-snap before fail |
| Passenger Save still “required” with filled values | aria-label fill only; never index-map inputs; see `references/aa-passenger-form.md` |
| Giant fill+pay Playwright blob | Snapshot→@ref loop; short shadow helper only |
| Hosted URL buried in poll | Surface `hosted_url` / live URL in the **first** user-facing line after create/login |
| BB ticket ask default 310 | When Cooper says **206**, Studio BB → **+12069542027** |
| Cooper passenger phone = 310 | Wrong — Telavaya contact phone is **206-954-2027** (handoff/text number) |
| Long `/tmp` drive scripts | CLI only if Cooper asked; stdin one-liners |
| `computer click-mouse` SUCCESS but still on same URL | Click missed or sticky footer; verify `page.url()`; try `page.mouse.click(x,y)` or blue-bbox center; AA **ERRCODE858** after Continue means cart bounced to choose-flights (“system having trouble”) — re-select fare, don’t claim paid |
| 1P Google missing in SA list | Vault **cm** (`bvakxbnetm2hwbctrdhka3x3oq`); after Cooper adds Login, path `cm/Google`; ask before interactive `op` |
| Cooper asks for a replay and none exists | `replays start` must run **before** the drive; there is no retroactive capture. Start it right after `browsers create` on any reviewable run. ffmpeg-stitched screenshots are **not** an acceptable substitute — re-run with recording on |
| Coord helper "not working" / `OPENROUTER_API_KEY` unset | `set -a; source ~/.hermes/.env; set +a` then `python3 scripts/vcoord.py shot.png <labels…>` |
| Autocomplete field looks filled but reverts | AA airport inputs need the **suggestion row clicked**, not just typed text. Type → screenshot → `vcoord.py` the suggestion → click it. Typing LAX/LHR and moving on silently leaves From empty |
| Trip-type dropdown click seems to do nothing | It toggles open/closed. Click once, screenshot, `vcoord.py` the **option row** inside the open list, then click that — don't assume the first click selected anything |
| Clicks land ~178px too high / one row off | Vision asked for **raw pixels** — Y measured against page area, dropping Chrome toolbar (1.373×). Use **`scripts/vcoord.py`** (box_2d + rescale). `references/vision-coordinates-box2d.md` |
| Per-element vision lookups feel slow | Wrong loop. **One `scripts/vmap.py` sweep per screen** → drive off the map. ~10x fewer vision calls, and the `value` column verifies for free |
| `computer batch` → "click_mouse field is required" | Payload is **nested**: `{"type":"click_mouse","click_mouse":{"x":..,"y":..}}`, not flat |
| Batched select + Return leaves dropdown empty | Selects don't commit inside a batch. Use discrete `click-mouse`/`type`/`press-key`, then re-sweep to confirm. Text inputs batch fine |
| Save rejects form though fields "look" filled | Sweep `--plan` and read `state` — e.g. `state_province [disabled]` until country set. Respect that ordering |
| Vision slow → tempted to swap model | Fix the **prompt** first (box_2d), not the model. With box_2d even flash-lite is 9/9 @2.7s. Then reduce vision **calls** (batch + region crops). `references/vision-model-benchmark.md` |
| Vision `DaemonThreadPoolExecutor._initializer` | Py3.14 pool bug — see `references/python314-daemon-pool-vision.md` + overlay; not “vision broken forever” |
| `computer type-text` → "Unknown flag: --text" | Subcommand is **`type`**, not `type-text`: `kernel browsers computer type <id> --text "…"`. Check `computer --help` before inventing names |
| Long `<select>` (DOB year, state, country) | Don't wheel-scroll — click to open, then `computer type --text "1991"` to jump, then click the highlighted row |
| Amex Pay now → "Follow payment instructions" modal | Normal **SafeKey 3DS**, not a decline. Push first, then a code to **Cooper's** 310/`m*****@cm.xyz`. Ask him for the code; nothing is charged until it passes — see `references/aa-checkout-3ds-confirmation.md` |
| "On request" green banner on confirm page | OAL/BA-metal normal — booking is still Ticketed. Report as caveat, never as failure |
| Drive feels slow, blame the vision model | Measure first: Kernel ops are 0.7–4s; the cost is **re-visioning a full 2560x1440 frame every field** (~15–25s/field x ~30 fields). Fix with region crops, fewer vision passes, terse coord-only prompts — not by shrinking the viewport. `references/vision-model-latency.md` |
| Tuning `auxiliary.vision.model` with no effect | With `image_input_mode: auto` + a native-vision main model, Hermes bypasses the aux model entirely (`vision_analyze` says *"Image loaded into your context"*). Confirm which path is live before editing config |
| `google/gemini-3.5-flash` for coords | **Don't.** Reasoning is mandatory (HTTP 400 if disabled) → 10.6s, 1,489 reasoning tok, $0.019, and **downscaled** coords that miss. Use `gemini-2.5-flash` (2.8s / $0.0008) for cheap checks, main-model native for click accuracy |
| `OPENROUTER_API_KEY` unset in agent shell | It's in `~/.hermes/.env`, not himitsu: `set -a; source ~/.hermes/.env; set +a`. That file may emit a harmless `Chrome.app/...: No such file or directory` line |
| Booked the wrong date | Confirm the **date pill + header date** in a screenshot before selecting a fare. This session built an entire Aug-2 cart, filled passenger, and only then got "date is wrong, use aug 3" — re-verify the date at trip-summary too, since re-picking the tile reloads the whole ladder |

## Verify
- `kernel auth status` → API Key
- `browsers list` / named session
- `browsers view` returns https live URL
- Profile reload keeps markers if `--save-changes` was used
- Booking: choose-flights or trip-summary; **no pay** unless authorized

## Related
- **studio-cua-drive** — Mac Studio path
- **vapi-phone-ops** — calls; failure only after full call log
- **bluebubbles-studio** — ask for missing ticket # via Studio BB (206 when that’s the ask)
