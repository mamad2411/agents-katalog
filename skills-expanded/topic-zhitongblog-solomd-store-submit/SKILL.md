---
name: store-submit
version: 1.0.0
description: |
  Publish a SoloMD release to the stores that have no usable submission API —
  Google Play Console and Microsoft Partner Center — by driving them through
  the local Unzoo Browser REST API. Covers upload, release notes, track and
  country selection, and submitting for review, plus the traps that have cost
  whole sessions before. Use when asked to "submit to Play", "上架 Play",
  "update the Microsoft Store", "提交商店", "发到应用商店", or when a release
  has shipped on GitHub and the store channels are still owed.
  Apple is NOT here: the App Store has a real API — see scripts/submit-for-review.sh.
triggers:
  - submit to play store
  - 提交 play
  - 上架 google play
  - update microsoft store
  - 提交微软商店
  - submit to store
  - 商店提交
allowed-tools:
  - Bash
  - Read
  - Write
---

# Store submission over the Unzoo browser

Google Play and Microsoft Partner Center are the two channels with no usable
API for this account, so releasing to them means driving a real browser. This
skill is the accumulated way to do that without losing an afternoon.

**Apple does not belong here.** iOS and macOS submit over the App Store Connect
API with no browser at all:

```bash
./scripts/submit-for-review.sh --platform ios   --version X.Y.Z \
    --notes-dir app-store/release-notes/X.Y.Z --dry-run
```

Reach for the browser on Apple only if that script has failed for a reason you
have actually diagnosed.

## Preflight

```bash
S=.claude/skills/store-submit
$S/unzoo.sh status          # {"browser_connected":true,...}
$S/unzoo.sh up              # starts the browser if it is down
$S/unzoo.sh tabs            # find the console tab that is already signed in
```

If the daemon is down, start it from a Bash call with `run_in_background: true`
— `nohup … &` is not enough, it dies with the tool's shell:

```
"/Applications/Unzoo Browser.app/Contents/MacOS/unzoo-service" --daemon
```

`browser_connected: false` while the daemon is up means every navigate and
evaluate will return HTTP 500; `unzoo.sh up` opens the browser and waits.

## The six rules

These are not style preferences. Each one has already cost a session.

**1. Pin the tab. Always.** Without `tab_id` the API acts on whatever tab the
user is looking at — their mail, their bank. Resolve one and export it:

```bash
export UNZOO_TAB=$($S/unzoo.sh find-tab play.google.com/console)
```

If a read comes back nonsensical, check `unzoo.sh url` before you debug the
page. It has been the user's Cloudflare dashboard.

**2. A coordinate click goes to the ACTIVE tab, not to `tab_id`.** The endpoint
accepts the id and ignores it. Clicking a background tab produces no click
event, no error, and a page that looks like it ignored you. `unzoo.sh click`
and `click-el` activate first for this reason — if you call `/api/v1/click`
directly, activate yourself.

**3. Read pages with `text`, never with screenshots.** A screenshot does not
follow scroll, so `full_page` silently omits exactly the banner you are looking
for. Use a screenshot only to locate something you must click by coordinate.

**4. Use the console's own session, in the user's own profile.** The signed-in
Google and Microsoft sessions live in the default profile. Prefer `find-tab`
over `new`. Do not touch cookies: setting one without `SameSite=None` has
signed the main profile out.

**5. Never claim a submission you have not read back.** Both consoles render
optimistically and will lie in both directions. Partner Center showed "Update
in certification" seconds after the click, then "Update in draft" in a
screenshot taken moments later, with a session-expired dialog in the DOM
throughout — and the submission had in fact gone through. **Navigate away and
back before reading a status**, and look for a structural change (the Submit
button gone, a Cancel button appeared), not just a word.

**6. A file input that reads back empty was probably filled.** Angular and
React uploaders take the FileList and clear the input in the same tick, so a
successful `set_input_files` leaves `files.length === 0`. Confirm on the page.
Retrying on the count uploads twice.

## Which store

- **Google Play** → `play.md`. AAB upload, release notes, countries, review.
- **Microsoft Store** → `msstore.md`. MSIX packaging, Partner Center, certification.

## unzoo.sh

```
status | up | tabs | find-tab <url-substring> | new <url> | activate
nav <url> | url | wait-load | wait-for <sel> [s] | exists <sel>
text | html | eval <js> | box <sel> | click <x> <y> | click-el <sel>
upload <input-sel> <file> | shot [path]
```

`-t <id>` overrides `UNZOO_TAB` for one call. Full API surface, if you need
something not wrapped here:

```bash
curl -s --noproxy '*' http://127.0.0.1:9399/api/v1/openapi.json
```

Note the `--noproxy '*'`: the local proxy mangles loopback calls, and it is
also why store uploads through the browser stall — see
`reference_release_upload_watchdog` in memory.

## ★ `text` lies when the window is not on screen

`unzoo.sh text` and any `innerText` read need layout, and Chrome skips layout
for a browser window that is not actually being painted. The Play Console page
then reads as ~550 characters of loading splash **while it is fully rendered** —
a screenshot shows the real content. This is silent: no error, just a short
string that looks like "still loading".

Anything unattended (a watcher, a poll loop, a cron) must read
`unzoo.sh dom-text`, which returns `document.body.textContent` and does not
depend on layout. Two caveats that come with it:

- `textContent` includes hidden and collapsed elements, so match on markers you
  expect to *appear*; do not conclude something is gone because a string is
  absent from a freshly loaded page.
- Loading-splash text stays in `textContent` permanently, so judge "page ready"
  by length plus a content anchor, never by the absence of the splash string.

When a read disagrees with what you think is on screen, take a screenshot —
that forces a paint and settles it.

## ★ `eval` used to share one scope, and a collision looked like `null`

Every `unzoo.sh eval` landed in the *same* top-level context, so the second
`const b = ...` in a session threw "Identifier 'b' has already been declared" —
and that throw came back as a plain `null` result, indistinguishable from "the
selector matched nothing". It sent this session chasing imaginary DOM changes
more than once, and it is visible in the page console as a stray SyntaxError
that has nothing to do with the page.

`eval` now wraps every expression in its own arrow scope, so redeclaration is
impossible. Three input shapes are handled: a bare expression, several
statements where you write your own `return`, and several statements where you
do not (the last one is returned for you). A `;` inside a string literal is the
one case that misfires — and it fails as a visible syntax error, not silence.
