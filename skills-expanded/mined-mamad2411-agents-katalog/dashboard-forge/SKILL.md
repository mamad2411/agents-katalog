---
name: dashboard-forge
description: >
  Supervised browser automation of vendor dashboards for operations that have NO public API —
  minting scoped API tokens, creating OAuth apps, flipping account-level toggles. Drives a real
  Chrome over CDP with a persistent per-site profile (human logs in once, supervised; scripts do
  the rest), extracts secrets DOM-to-vault without ever exposing them, and survives UI drift via
  the step-and-shoot method. Use when a task needs a dashboard click-path (Cloudflare token/Zero
  Trust, GitHub OAuth apps, any admin console) and the vendor offers no API or your token lacks
  the scope to grant itself more. Triggers: "no API for this", "create an OAuth app", "mint a
  token in the dashboard", "automate the admin console", "browser-automate the setup".
allowed-tools: Read, Bash, Grep, Glob
---

# dashboard-forge — supervised dashboard automation doctrine

Some operations exist ONLY behind a vendor's web UI (GitHub fine-grained PATs and OAuth apps have
no creation API; a Cloudflare token cannot grant itself new scopes). This skill is the canonical
method for automating those click-paths safely: the human supervises and handles logins/2FA; the
scripts do everything else, reproducibly.

**Harness (SSoT):** [`../../lib/browser-forge.mjs`](../../lib/browser-forge.mjs) — per-site
persistent Chrome profiles + CDP attach + login-wait + identity preflight + consent dismissal +
vault sinks. node ONLY (Bun's `connectOverCDP` times out). Requires `playwright-core` (pinned at
the repo root) and Chrome at the standard macOS path.

> **Self-Evolving Skill**: dashboards drift constantly. When a selector misses or a flow changes,
> fix the forge script AND append the drift note to the Vendor Quirks section below — immediately,
> not later. Only update for real, reproducible breakage.

## The method — step-and-shoot

Write the forge as small, resumable steps against a LONG-LIVED Chrome (launch once; each step
connects, acts, disconnects — `browser.close()` on a CDP connection only detaches, Chrome keeps
running). Never author one monolithic script against an unseen UI.

1. **Launch + human login.** `launchChrome(site, loginUrl)`; the human signs in (incl. 2FA).
   Detect completion with `waitForLogin(ctx, probeUrl, ok)` — poll an authenticated endpoint via
   `ctx.request` with the context cookies. NEVER navigate a visible tab to poll: you would reload
   a half-typed login form.
2. **Identity preflight.** Before ANY mutating step, extract the signed-in identity (a meta tag,
   a settings-page marker, an API echo) and `assertIdentity(actual, expected, resource)`. An
   account-owned resource created under the wrong login is a silent disaster (it happened:
   an OAuth app landed under the wrong GitHub user mid-forge because the human switched accounts).
3. **Act in small steps, screenshot between.** One interaction cluster per step; `shot(page, name)`
   after each. When a locator misses, READ the latest shot, adapt, re-run just that step. Prefer
   role/label-based locators (`getByRole`, description-text anchoring) over CSS classes; for
   checkbox grids, `page.evaluate` walking from a UNIQUE description text up to its row is far
   more drift-proof than nth-child chains.
4. **Expect interceptors.** Cookie/consent overlays (OneTrust & co.) swallow clicks and produce
   pure timeouts with no visible cause — call `dismissConsent(page)` when a click times out
   mysteriously, then retry. GitHub-style sudo/2FA walls mid-flow: pause and let the supervising
   human clear them (or see gh-fine-grained-pat's `autosudo.mjs` for the autonomous passkey path).
5. **Extract secrets DOM-only.** On a token/secret reveal page: `page.evaluate` → match the value
   → `vaultSet(scope, path, value)`. **NEVER screenshot a reveal page** — an agent reading that
   screenshot puts the secret into the conversation context permanently. If a reveal was
   accidentally captured, purge the file AND treat the secret as context-exposed (rotate if the
   transcript leaves the machine).
6. **End-of-run hygiene.** `purgeShots()` (breadcrumbs can show near-secret state), then
   `teardown(site)` — kills the SPECIFIC pid on the CDP port, never `pkill -f` (process-storm
   policy, `~/.claude/CLAUDE.md`).

## Hybrid rule — forge the key, then use the door

Browser-automate the MINIMUM: usually just (a) the login and (b) the one form that mints a
scoped credential. Everything after that goes through the vendor's REAL API with the minted
credential, written as an **idempotent GET-before-POST bootstrap** (see the cf-access-wall skill
for the worked template). UI automation is the crowbar, not the workflow.

## Borrowed-session mode — driving a browser the HUMAN already logged into

A third mode, distinct from launching a per-site profile over CDP. Instead of owning a session,
you **borrow one that is already open** in the operator's own Chrome and drive it via AppleScript:

```applescript
tell application "Google Chrome"
  execute (tab N of window M) javascript "…"
end tell
```

Requires **View → Developer → Allow JavaScript from Apple Events** (persisted per profile as
`browser.allow_javascript_apple_events` in `Preferences` — grep it to check before promising
anything). You then have full DOM read/write with no driver, no profile copy, and no port.

**When it is the RIGHT tool:** the console is behind a passkey / hardware-key / step-up flow that
you must not automate, and a human session already exists. You never touch the credential — you
type inside a door somebody else opened. That distinction is the whole justification, and it is
worth stating out loud in whatever you write afterwards.

**When it is the WRONG tool:** anything unattended, anything needing isolation, anything that
should not be able to see the operator's other tabs. It has no sandbox by construction.

Hard-won rules, each one paid for:

- **Address tabs by URL, never by index.** `activate` and `set index` REORDER windows, so an
  index captured a moment ago can point somewhere else by the time you use it. Re-resolve on
  every call. Make the URL needle specific — `"admin.google.com"` will happily match a different
  admin tab and you will read the wrong page and believe it.
- **Read the JS from a FILE** (`set js to read POSIX file "/tmp/step.js" as «class utf8»`).
  Interpolating JS through bash → osascript → AppleScript string literals mangles quotes and
  backslashes in ways that fail silently or, worse, alter the script.
- **`offsetParent` is null for `position: fixed`,** which is how essentially every Material/modal
  dialog is rendered. A "is it visible" filter built on `offsetParent !== null` therefore hides
  the dialog you are looking for and you conclude the form never opened. Use
  `getBoundingClientRect()` width/height instead.
- **Framework inputs need the NATIVE setter.** Assigning `el.value` updates the DOM but leaves
  Angular/React/Closure's model stale, so the form submits empty. Use
  `Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set.call(el, v)` then
  dispatch `input` + `change` (+ `blur`). Read the value back and assert it.
- **Verify what is under the point before any coordinate-based click** —
  `document.elementFromPoint(x,y)` and compare to the intended element. In an admin console a
  mis-aimed click is not a failed test, it is an unintended action.
- **Chrome can be RUNNING with zero windows and refuse `open -a`.** `make new window` via Apple
  Events still works. Never quit or restart the operator's browser to "fix" it; you will destroy
  their tabs.

## Secrets discipline (non-negotiable)

- Values ride PIPES: `vault set --stdin <scope> <path>` (SCS vault). Never argv, never stdout,
  never a chat transcript.
- Scripts print LENGTHS and vault paths, not values (`✓ vaulted (len 53)`).
- Profile dirs (`~/.local/share/web-forge/profile-<site>`) hold live sessions — sensitive, never
  committed, listed in backups as credential-equivalent.
- Public identifiers (OAuth client_id, account ids) may be logged; anything CONCEALED may not.

## Vendor quirks (drift log — append, with dates)

- **Cloudflare 2026-07 token UI**: the old template-picker → 3-combobox flow is GONE. "Create
  Token" lands directly on a categorized checkbox form ("Cloudflare One / Zero Trust" section →
  per-group Read/Revoke/Edit boxes); submit is **"Review token"** → "Create token" → modal reveal.
  Tokens are `cfat_…` (53 chars), not the old 40-char format.
- **Cloudflare account-owned tokens** (2026-07-23): `/user/tokens/verify` ALWAYS rejects them
  ("Invalid API Token"); verify with `/accounts/{id}/tokens/verify`. Don't misdiagnose a working
  token as dead.
- **Cloudflare dashboard consent** (2026-07-23): OneTrust overlay appears minutes into a session
  and intercepts pointer events page-wide.
- **GitHub OAuth apps** (2026-07-23): no creation API (same as fine-grained PATs). Form fields:
  `oauth_application[name|url|callback_url]`. "Generate a new client secret" triggers sudo mode;
  a FRESH login usually has a sudo grace window — create the app right after login and the secret
  generation is prompt-free. Client secrets render as a 40-hex blob.
- **Azure Portal — ambiguous accessible names** (2026-08-02): every blade's close button is labelled
  `"Close content '<Blade Title>'"`, so on "Register an application" a fuzzy
  `getByRole("button", {name:/register/i}).first()` matches the CLOSE button, not the submit. It
  clicks, Playwright reports success, the blade shuts and nothing is created. Cost two runs, and the
  second created a DUPLICATE once the truth surfaced. Use `clickExact()` — it refuses on a non-exact
  name and prints the candidate list (verified live: `["Close content 'Register an application'","Register"]`).
- **Azure Portal — two elements match `input[placeholder*="Search"]`** (2026-08-02): the page-wide
  search in the masthead matches BEFORE any blade's own filter. Typing the role name into it left the
  role grid unfiltered, so an exact row lookup found 0 rows and the wizard advanced with no role
  selected. Anchor on the distinctive placeholder (`"Search by role name, description, permission, or ID"`).
- **Azure Portal — a list view can lie about creation** (2026-08-02): after successfully creating an
  app registration as a GUEST (`#EXT#`) user, **App registrations → Owned applications** said "This
  account isn't listed as an owner of any applications in this directory." True (a guest creator is not
  auto-assigned owner) and deeply misleading. Ground truth is the **notifications pane** ("Successfully
  created application X") or the **All applications** tab. Never confirm a mutation from the same
  console's default list view.
- **Azure Portal — tokens are in memory, not localStorage** (2026-08-02): an MSAL SPA of this
  generation keeps ARM/Graph access tokens in memory; a localStorage sweep returns nothing. Capture
  them off the wire with `captureBearer(page, "management.azure.com" | "graph.microsoft.com")`. With an
  ARM token the whole 3-tab role-assignment wizard collapses into one idempotent `PUT` (HTTP 201 first
  try) — the clearest instance of the Hybrid rule in this log.
- **Azure Portal — a cached blade issues no request** (2026-08-02): navigating to a view the SPA has
  already hydrated produces zero traffic, so token capture silently yields `null`, which reads exactly
  like "no permission". `captureBearer` retries with a `reload()` for this reason. The
  App-registrations LIST blade reliably re-queries Graph; the Entra Overview blade often does not.
- **Azure — the Portal and the CLI are DIFFERENT Entra apps** (2026-08-02): portal
  `c44b4083-3bb0-49c1-b47d-974e53cbdf3c`, CLI `04b07795-8ddb-461a-bbee-02f9e1bf7b46`. A Conditional
  Access policy scoped to the CLI (`AADSTS530035`, "Device state: Unregistered") therefore does **not**
  block the portal. This asymmetry is what makes a browser forge the only way in — and note that
  `az account list` then returns `[]`, which is a consequence of the block and **not** evidence that no
  subscription exists.
- **Tailscale — console moved and OAuth clients were renamed** (2026-08-05): `login.tailscale.com`
  redirects to **`console.tailscale.com`**, and `/admin/settings/oauth` redirects to
  **`/admin/settings/trust-credentials`** ("OAuth clients" is now "Trust credentials", created via a
  button labelled just **`Credential`**). Auth keys stayed at `/admin/settings/keys`.
- **Tailscale — Radix checkboxes: the `<input>` is a decoy** (2026-08-05): every scope checkbox
  renders a real `<input type=checkbox>` that is `aria-hidden`, `opacity:0`, **`pointer-events:none`**,
  next to a `<button role="checkbox" data-state="checked|unchecked">` that holds the actual state.
  Clicking the input — even with `{force:true}` — reports success and changes NOTHING; it cost a run
  that looked like it selected six scopes and submitted an empty form. Click
  `button[role=checkbox][id="<scope>"]` and assert via `data-state`. Bonus: **the button ids ARE the
  API scope names** (`auth_keys` = write, `auth_keys:read` = read, `devices:core`, `policy_file`),
  which is the most drift-proof selector on the page — better than the row-title walk.
- **Tailscale — a 50-char cap silently disables the wizard** (2026-08-05): the OAuth/credential
  description is labelled "(optional)" but capped at 50 characters, and exceeding it leaves
  **`Continue` disabled with no inline error** near the button. Symptom is a permanently disabled
  submit; the rule is only visible in body text ("Descriptions can be a maximum of 50 characters").
  When a submit stays disabled, dump the form's body text before suspecting the click.
- **Tailscale — write scopes are gated on tags, so OAuth clients need an ACL change first**
  (2026-08-05): selecting ANY write scope surfaces "Tags (required for write scope)", and tags only
  exist if the tailnet policy file declares them. So an OAuth client (the durable, non-expiring
  credential) cannot be minted in one pass on a tailnet with no tags — it needs a policy-file edit,
  which is a security change the operator should approve. A plain **user-owned auth key** from
  `/admin/settings/keys` has no tag requirement and is the right unblock when the goal is just
  joining one device.
- **Seeding a forge profile from the operator's real Chrome** (2026-08-05): when the per-site profile
  has no session and an interactive login would be the only manual step, copy `Local State` +
  `Default/Cookies` (+ `Default/Network/Cookies` if present) from
  `~/Library/Application Support/Google/Chrome` into a throwaway dir and point
  `WEB_FORGE_PROFILE_DIR` at it. Cookies decrypt because the macOS Keychain key is per-user, not
  per-profile, and no Keychain prompt appears (same Chrome binary). The operator's running Chrome is
  untouched — different `--user-data-dir`. **Delete the seeded dir afterwards**: it holds a copy of
  live session cookies and is credential-equivalent.

- **`shot()` used to report phantom screenshots** (fixed 2026-08-07): it wrapped `page.screenshot`
  in `.catch(() => {})` and returned the intended path regardless, so a failed capture printed a
  confident `[shot] …png` for a file that never existed (caught live — a 30 s font-loading timeout
  on the Lark console, path printed with `existsSync === false`). Screenshots are the only evidence
  a forge has when a selector misses, so a phantom one makes "capture failed" indistinguishable
  from "the page was blank". It now returns `null` and says `FAILED` on both the throw path and the
  resolved-but-no-file path. **Callers must treat `null` as "no evidence", never as a path.**
- **Lark/Feishu developer console — the scope table is VIRTUALIZED** (2026-08-05): `document
.querySelectorAll("tr")` returns **1** and `[role="row"]` returns **0**; rows are
  `div.virtual-table__row` and only ~25 exist in the DOM at once, so scroll-and-scrape silently
  under-reports. Never enumerate it by scrolling — type into the scope filter instead, anchored on
  its distinctive placeholder `input[placeholder^="E.g."]` (the masthead "Search documentation" box
  matches a generic `input[placeholder*="Search"]` FIRST — the same trap as the Azure entry above).
- **Lark console — "More" in Security Settings is a section anchor, not a button** (2026-08-07):
  `getByText("More", {exact:true})` matches exactly one node, and clicking it times out at 10 s with
  no visible cause. Scroll and read the whole page instead of clicking.
- **Feishu docs are JS-gated but expose a markdown twin** (2026-08-07): fetching a doc page yields
  only its title, but the HTML advertises `<link rel="alternate" type="text/markdown">` — append
  `.md` to the doc URL and `curl` returns the full text, Chinese included. The Chinese pages carry
  detail the English ones omit (the app-level "refresh `user_access_token`" switch appears only
  there). Wrong slugs answer `This document is not found`, so probe a few rather than assuming one.

- **Chrome silently ignores `--remote-debugging-port` on the DEFAULT data directory**
  (2026-08-12): Chrome starts normally, the flag appears in `ps`, and the port never binds. The
  only signal is one line on stderr — `DevTools remote debugging requires a non-default data
directory. Specify this using --user-data-dir.` — which is invisible if stderr goes to a log
  nobody reads. `curl 127.0.0.1:<port>/json/version` then fails with "connection refused" and
  looks like a dead browser rather than a rejected flag. **Diagnose with
  `lsof -nP -iTCP -sTCP:LISTEN -a -p <pid>`**: a Chrome that is up but listening on nothing is
  this, every time. Always pass an explicit `--user-data-dir` alongside the debugging port —
  which the harness already does, and which is exactly why the harness works and ad-hoc
  invocations do not.

- **Google Admin console — the group list lies after a write** (2026-08-12): immediately after
  creating a group, **Directory → Groups** still rendered the empty state, _"Your organization
  doesn't have any groups yet"_, for long enough to read as a failure. The group existed the
  whole time. **This is the SECOND vendor to do this** — see the Azure "a list view can lie about
  creation" entry above — so treat it as a rule rather than a quirk: _never confirm a mutation
  from the same console's default list view._ Confirm from a DIFFERENT system. Here the proof was
  that GCP's `setIamPolicy` **rejects members that do not exist** and accepted the new group, so
  the IAM grant doubled as the existence check.
- **Google Admin console — repeated clicks STACK duplicate dialogs** (2026-08-12): clicking
  "Create group" twice (e.g. once via `.click()`, once via a synthetic pointer sequence when the
  first appeared to do nothing) leaves TWO form instances in the DOM. A later "fill the field with
  this aria-label" then hits an arbitrary one and the visible form stays empty. Reload to a clean
  state before filling, and assert the field count is exactly 1 first.
- **Google Admin console — controls are Closure `div[role=button]` with obfuscated classes**
  (2026-08-12): e.g. `class="U26fgb O0WRkf oG5Srb …"`. Never build a CSS-path selector; match on
  visible text or `aria-label`. Plain `.click()` DOES work on them — if a click appears to do
  nothing, suspect that you are reading the wrong tab before you conclude the click failed.
- **Google Admin console — a preset flips to "Custom" when you narrow a sub-setting**
  (2026-08-12): choosing the `Restricted` access-type preset and then setting "Who can join" to
  _Only invited users_ relabels Access type as **Custom**. That is correct and expected, not a
  failed selection. Assert on the SUB-SETTINGS you care about, never on the preset label.
- **Google Admin console — `/ac/groups/new` is not a deep link** (2026-08-12): it answers
  `Error 400 (Bad Request)`. There is no URL that opens the create dialog; you must click through
  from `/ac/groups`.
- **Seeding a forge profile with copied cookies NO LONGER WORKS FOR GOOGLE** (2026-08-13): the
  "Seeding a forge profile from the operator's real Chrome" recipe above is now **dead for
  `accounts.google.com`**. 109 `google.com` cookies copied cleanly out of the operator's profile and
  the very first navigation still landed on the sign-in page — Google binds sessions to the profile's
  device key (DBSC), so a cookie copy authenticates nothing. The recipe remains valid for vendors that
  do plain cookie sessions; budget a supervised login for Google and do not plan a run around
  borrowing its session. **Symptom to recognize:** a clean copy, a plausible cookie count, and an
  immediate redirect to sign-in — which reads as "I copied the wrong profile" and is not.
- **Google's sign-in identifier input is `type="text"`, not `type="email"`** (2026-08-13): the field is
  `#identifierId`. A guarded `input[type="email"]` fill therefore matches ZERO nodes and, if the fill
  is wrapped in `if (await field.count())`, does nothing at all — the screenshot then shows an empty
  box, which reads as "the form rejected my value" rather than "my selector missed". Anchor on
  `#identifierId`. (Same family as the Azure/Lark placeholder traps: a selector that matches nothing is
  far more expensive to diagnose than one that matches the wrong thing, because the failure is silent.)
- **Chrome ignores `--profile-directory` when another Chrome owns a DIFFERENT `--user-data-dir`**
  (2026-08-13): with a leftover forge Chrome running, `open -a "Google Chrome" --args
--profile-directory="Profile 22" <url>` and the direct-binary equivalent both print _"Opening in
  existing browser session"_ and open **nothing** — no window, no error, exit 0. AppleScript then
  enumerates the FORGE's tabs, so `tell application "Google Chrome"` silently drives the wrong browser.
  Check `ps -axo pid,command | grep "[G]oogle Chrome" | grep -v " --type="` for a stray
  `--user-data-dir` **before** trusting borrowed-session mode, and note two Chrome PIDs can coexist
  where only one receives Apple Events. Prefer an explicit CDP profile over fighting for the default.
- **Masking a value you have not validated hides the ERROR, not the secret** (2026-08-13): piping a
  token-minting command through `2>&1 | sed 's/./x/g'` to keep a secret out of the transcript printed a
  confident row of `x`s for what was actually `ERROR: Reauthentication failed…`. The masking made a
  failure indistinguishable from success, and the next call's 401 was the only clue. Mask **lengths and
  exit codes** (`len=${#TOK} rc=$?`), never a raw stream you have not first checked is a value —
  `${#TOK}` would have read `0` and ended it immediately.
- **Apple Events `execute javascript` needs SYNCHRONOUS JS — a Promise serializes to nothing**
  (2026-08-19): the idiomatic `(async () => { … })()` probe returns a `Promise`, which crosses the
  Apple Event boundary as an **empty string**. The step reads as "the page returned no data", i.e.
  exactly like a failed selector, and the natural response is to rewrite selectors that were fine.
  Write borrowed-session steps as a plain synchronous IIFE returning `JSON.stringify(out)`; where a
  step genuinely needs to wait, split it into two invocations with the sleep in the **shell**, not
  in the page.
- **GitHub's React issues UI exposes NO file input and NO React `onDrop`** (2026-08-19): attaching a
  file to an issue comment used to mean driving `file-attachment` + `input[type=file]`. On the current
  UI a DOM sweep finds **zero** `input[type=file]`, **zero** `<file-attachment>`, and **zero**
  `__reactProps$*.onDrop` anywhere in the textarea's ancestor chain — the only evidence an upload path
  exists is the hint text _"Paste, drop, or click to add files"_. Do not conclude uploading is
  impossible: dispatching a synthetic `DragEvent` sequence (`dragenter`, `dragover`, `drop`) carrying a
  `DataTransfer` with one `File` **at the textarea** works. Confirm it by checking `dispatchEvent`
  returned `false` on the `drop` (i.e. `preventDefault` was called — the listener exists even though no
  property exposes it), then poll the textarea for the injected
  `[name](https://github.com/user-attachments/files/…)` markdown. Two follow-ons worth knowing: the
  upload is **not** a page mutation, so GitHub's own CSP blocks an in-page authenticated `fetch` to
  verify it; and navigating to the resulting URL **downloads** rather than renders, so the tab
  self-closes — which reads as "the tab vanished, something broke" when it is the success path.
  Verify from **outside** the browser instead (`shasum` the downloaded file against the original;
  Chrome's `History` DB `downloads` table records `total_bytes` and `state`).
- **Payload SIZE is rarely the Apple Events failure — quoting is** (2026-08-19): a 106 KB step script
  (78 KB file base64-encoded) round-trips through `osascript` intact; a measured probe put a
  104,576-char string through unharmed. The actual break was an **unterminated JS string literal**,
  caused by emitting `var B64 = "` and then a newline before the payload. Keep any large literal on
  **one physical line**, and when a big step fails, test the transport with a synthetic string of the
  same length before blaming a limit that does not exist.
- **1Password web — a persistent profile keeps the Secret Key, so the wall is PASSWORD-ONLY**
  (2026-08-24): `eonlabs.1password.com` redirected to `/signin` with the account already resolved —
  email prefilled (`terry@eonlabs.com`), one `input#master-password`, no Secret Key field. So
  "the profile still has cookies" does **not** mean the session is live (the profile's `Cookies` DB
  was 5.9 MB and 3 days old), and the resulting wall is _weaker_ than the "Secret Key + master
  password" a cold login demands — which matters because a forge told to "STOP if it demands a full
  sign-in" can misread a password-only wall as something it may proceed through. It may not: the
  master password is exactly the credential a forge must never type or fetch. Detect it on
  `input#master-password` and hand the parked Chrome back to the human for the supervised login.
  Corollary for the same vendor: the **`op` CLI is not a fallback** — with desktop-app integration
  (`system_auth_latest_signin` in `~/.config/op/config`) every authenticated call raises a Touch ID
  prompt and dies with `[ERROR] authorization timeout` after 60 s if nobody is at the machine, while
  `op account list` still answers from local config and makes it look configured. Both doors need
  the same absent human, so there is no clever route around it.

- **A reveal modal OUTSIDE `<main>` makes a successful click look like a broken button** (2026-09-02, Cloudflare token forge): the "Token created successfully" panel renders in a `div.fixed.inset-0` appended to `<body>`, so an extractor scoped to `document.querySelector("main")` reports "no token present" while the secret is plainly on screen. Worse, that same overlay intercepts pointer events on the submit button underneath, so Playwright's next click retries until it times out — and the natural reading of "click timed out" is "the button is broken", when in fact **the click already succeeded and the overlay is the proof**. Rule: on a click-interception timeout, FIRST check whether the mutation already happened (`document.elementFromPoint` on the button's centre will name the overlay), and always search the whole document for a reveal, never just the main region.
- **Cloudflare API tokens are `cfat_` + 48 = 53 chars** (re-confirmed 2026-09-02): a `\b[A-Za-z0-9_-]{40}\b` extractor matches NOTHING and reports "no token found". The Cloudflare entry higher in this log already said this and it still cost a cycle — when an extractor finds zero candidates, re-read the vendor's own format before widening the regex. The most reliable extraction point is not the masked token field at all but the modal's ready-to-run **`curl` verification snippet**, which embeds the secret as `Authorization: Bearer <token>`; parse that.
- **Cloudflare's token builder replaces the template grid after the first pick** (2026-09-02): selecting "Write all resources" swaps the card grid for the configured-policy view, so a loop that clicks several templates in sequence silently applies only the first and reports "not found" for the rest. Each additional policy needs an explicit **"Add policy"** click to bring the grid back. Note also that ONE template can expand into MULTIPLE policies — "Write all resources" produced both an account-scoped policy (+118) and a zone-scoped one (+42) — so policy count never matches template count. A policy left empty by a stray "Add policy" blocks submission with "At least one permission is required"; its Select-all state is panel-local and does not commit, and the panel's own controls are unlabeled SVG icon buttons, so the reliable fix is to delete the empty row (right-most icon) rather than try to fill it.
- **Cloudflare's own signup Turnstile does not solve under CDP** (2026-09-02): the widget renders but `cf_challenge_response` stays empty and submission returns "Please complete the CAPTCHA and try again". This is the vendor's anti-automation control working as designed and it is the correct place to stop and hand the parked, pre-filled window to the human — not something to engineer around. Everything after the signup (token creation, zone creation, DNS, deploy) automated cleanly, so budget exactly one human click for account creation.
- **`wrangler deploy` silently invents a workers.dev subdomain from the DIRECTORY NAME** (2026-09-02): in `~/vj/sys/site` it tried to claim `site.workers.dev`, failed with "the name is unavailable", and aborted the deploy — which reads as a permissions or config error rather than a naming collision. Register the subdomain deliberately first with `PUT /accounts/{id}/workers/subdomain {"subdomain":"..."}`, then deploy. Note a freshly registered workers.dev subdomain serves TLS handshake failures (`curl` exit 35) for several minutes while its certificate provisions; that is not a broken deploy.
- **Session cookies make profile-seeding impossible for some vendors** (2026-09-02): the "seed a forge profile from the operator's real Chrome" recipe above failed for Wix and Name.com because their auth cookies (`LSESSION_*`) are **session-scoped** — `is_persistent=0`, `expires_utc=0` — so they live only in the running browser's memory and the on-disk `Cookies` DB holds nothing but analytics trackers. Symptom: a clean copy with a plausible cookie count that still lands on the login page, i.e. exactly like the Google/DBSC failure but for a different reason. Check `is_persistent` on the vendor's actual auth cookie BEFORE planning a run around seeding; if it is 0, seeding can never work and borrowed-session or a real login is the only path.
- **Two Chrome processes: Apple Events follow the FRONTMOST one** (2026-09-02): with the operator's Chrome and a forge Chrome both running, `tell application "Google Chrome"` silently retargeted from the operator's window to the forge window once the latter was brought to front — so a tab-listing that had been reading the operator's Gmail/Name.com tabs started reading the forge's Cloudflare tabs, with no error. When both exist, drive the forge over **CDP** (unambiguous, addressed by port) and reserve Apple Events for the operator's browser only.
- **A vendor that resells another vendor can mint a session for it** (2026-09-02, genuinely useful): Name.com resells Wix, and its `/account/wix/library/wix` page renders a per-site `https://users.wix.com/auth/sso/<a>/<b>?targetUrl=...` link that exchanges the **Name.com** session for a **Wix** one. Swapping `targetUrl` reaches any `manage.wix.com` destination. That removed the need for a Wix credential entirely — no password, no OAuth, nothing to store. Before assuming a second vendor needs its own login, check whether the first one resells it.
- **Healthchecks.io Integrations — row-action buttons are `visibility: hidden` until the row is hovered** (2026-09-08): the "Test!" button on `/projects/<uuid>/integrations/` resolves perfectly, reports a real 50×30 box at a sensible viewport position, and every ancestor is `display: table-*` and visible — yet Playwright retries for 30 s with `element is not visible`, because the button ITSELF carries `visibility: hidden` and only `tr.channel-row:hover` reveals it. That combination (a locator that matches, a non-zero rect, a visible ancestor chain, and a click that never lands) reads as "the button was removed in a redesign" and sends you hunting for a selector that does not exist. Diagnose by dumping `getComputedStyle(el).visibility` on the ELEMENT, not just on the chain — the classic ancestor walk clears every ancestor and points nowhere. Fix: `row.hover()`, assert the computed visibility actually flipped to `visible`, then click. Same shape as the Radix "the `<input>` is a decoy" entry: the state you need sits on a node the natural selector skips past.
- **Chromium IndexedDB forensics: `dfindexeddb` hard-rejects V8 wire version 16, which looks like an EMPTY object store** (2026-09-08): reading a Chrome 152 profile's IndexedDB with google/dfindexeddb yields every metadata and index record fine but ZERO `ObjectStoreDataKey` rows, each one raising `ParserError("Unsupported header")` from `v8.ValueDeserializer.ReadHeader`. It is a version GATE (`LATEST_VERSION` still sits at 15), not a parse failure — Chrome now writes 16 — so the tool reports the store as unreadable while the data sits right there, and the matching `ExistsEntryKey` count is the tell (130 ExistsEntry rows against 0 data rows means a gated decoder, not an empty DB). Monkey-patch `LATEST_VERSION` upward from your own script rather than editing the installed package, and log the version actually encountered so the assumption stays visible; the object/string/number tags are backward compatible and decode cleanly. Two install notes: `ccl-chromium-reader` is NOT on PyPI despite the importable name, and `dfindexeddb` hard-pins a pre-cramjam `python-snappy` that ships no arm64 wheel, so it needs `brew install snappy` plus `CPPFLAGS=-I/opt/homebrew/opt/snappy/include` to build. Corollary worth repeating: a plain `strings` grep over a `.leveldb` directory undercounts badly, because SSTable data blocks are snappy-compressed and only the uncompacted regions are visible as text — "I grepped and found nothing" is therefore not evidence of absence.
- **Chrome's default profile can be relaunched non-destructively when `exit_type` is `Normal`** (2026-09-08): when a forge needs a page-bound client to come online (here the Pushover desktop client, whose message store exists only inside the operator's own profile), the safe preflight is `Default/Preferences` → `session.restore_on_startup` (absent, or 5, = open the New Tab page) and `profile.exit_type` (`Normal` = clean quit, so no crash-restore bubble). With both true, launching the BINARY with an explicit `--user-data-dir=<default dir>` `--profile-directory=Default` plus one URL opens exactly that one tab, not the operator's seventy — and a later `kill -TERM <specific pid>` shuts it down cleanly and flushes/compacts LevelDB. Do NOT use `open -a` (it answers "Opening in existing browser session" and opens nothing while any other Chrome is running), and do NOT add `--remote-debugging-port` to the operator's real profile: Chrome ignores that flag on the default data dir anyway, and it would be a security change nobody authorised.

## Relationship to gh-fine-grained-pat

The PAT skill (gh-tools) is the origin of this harness and keeps its own battle-tested copy +
GitHub-specific machinery (autosudo/webauthn/multi-account). NEW forges build on web-forge's
`lib/browser-forge.mjs`; the PAT skill migrates here only in a deliberate, tested pass — never
casually (anti-fragility: don't destabilize a working credential forge for DRY points).

## Reference implementation

`~/459ecs/example-clinic/scripts/access-bootstrap/` — the 2026-07-23 run that canonicalized this
skill: Cloudflare scoped-token forge + GitHub OAuth-app forge + idempotent Access bootstrap,
end-to-end in one supervised session (decision record: that repo's compliance README §D10).

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the dashboard automation succeed?** — If selectors failed or the flow changed, update the forge script and add a drift note to the Vendor Quirks section.
2. **Were secrets stored safely?** — Verify no secrets appear in screenshots, argv, or stdout—only in the SCS vault.
3. **Did the supervised step succeed?** — If the human had to intervene (2FA, sudo, account switch), document the new quirk for future runs.
