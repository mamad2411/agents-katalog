---
name: flutter-monitoring
description: Flutter crash, ANR and startup monitoring as a practice — wire the reporting filter, context keys and symbol upload; run a weekly triage that ranks by users affected and forces a decision per issue; ship an in-app feedback report that carries diagnostics without carrying identity. Usage — /flutter-monitoring <setup|triage|feedback>
argument-hint: "setup | triage | feedback [--owner <name>] [--version <x.y.z>]"
arguments:
  - name: subcommand
    description: "'setup' to wire reporting, symbols and alerts. 'triage' (default) to run the weekly review. 'feedback' to build or audit the in-app report path."
  - name: args
    description: "--owner <name> for this week's triage owner, --version <x.y.z> to scope to one release"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Task
  - Bash(find *)
  - Bash(grep *)
  - Bash(ls *)
  - Bash(cat *)
  - Bash(date *)
  - Bash(git log *)
  - Bash(gh *)
---

# Flutter Monitoring

Parse `$ARGUMENTS[0]` as `setup` | `triage` | `feedback` (default: `triage`).

## Scope — and what this command does not own

This command owns the **practice**: which numbers you watch, what each one hides, how an
issue gets a decision and an owner, what an alert is allowed to fire on, and what a user
report is allowed to carry.

The **code** it wires is owned by the `logging/flutter-observability` layer: the injected
`AppLogger` facade, redaction inside the facade, the crash-context keys, the navigation
breadcrumb observer, the three global error channels, the analytics catalogue and typed
feature flags. Error types and `isReportable` are `api-style/dio`. The release workflow file
is `ci/flutter-release`.

**Never restate or re-derive those rules here.** Load them on demand:

```
Task → stack-dispatcher
  task: "<what this sub-command is about to change>"
  target_files: ["lib/core/observability/*.dart", "lib/core/logging/*.dart", ".github/workflows/release.yml"]
```

Use the rule set it returns. If it returns nothing for observability, say so and stop — do
not invent a facade.

---

## The numbers, and what each one hides

Every sub-command reads from this table. Quote the blind spot whenever you report a number.

| Metric | What it answers | What it hides |
|---|---|---|
| **Crash-free users** | The headline: what share of people had a good day | One user crashing ten times counts once. A tight crash loop for a small group is invisible here |
| **Crash-free sessions** | Repeat crashes and crash loops — the number a loop actually moves | A launch crash looks minor. Users who cannot launch stop opening the app, so they leave the denominator while the healthy majority keeps generating sessions and dilutes it |
| **ANR rate** (Android) | Main thread blocked past the input-dispatch timeout | Everything, if you only look at crash reporting — an ANR is not a crash and never appears there. It comes from Play vitals or a dedicated ANR capture. Play's bad-behaviour line is ~0.47% user-perceived ANR against ~1.09% user-perceived crash |
| **Cold start p90** | The launch users actually feel | The mean hides it entirely. p90 is the floor; watch p95 on the slowest supported device class, not on your desk |
| **Adoption by version** | Whether any of the above is readable yet | Nothing — but it invalidates the rest. Below a few percent adoption every rate is noise |

**The two crash numbers disagree in exactly the informative case.** A crash on launch barely
moves the session number and destroys the user number. When they diverge, the direction of
the divergence *is* the diagnosis — do not average them, do not pick the flattering one.

**Never judge a new version's rate until adoption is meaningful.** The first hours of a
rollout mislead in both directions: early adopters are self-selected (newer devices, better
networks, so rates look good), and a handful of crashes against a tiny denominator produces
a terrifying percentage (so rates look catastrophic). Report the adoption percentage next to
every rate, or do not report the rate.

---

## `/flutter-monitoring setup`

### Step 1 — Find what already exists

```bash
grep -rl "recordError\|FirebaseCrashlytics\|Sentry\|SentryFlutter" lib/ | head -20
grep -rn "setCustomKey\|setUserIdentifier" lib/ | head -20
grep -rn "split-debug-info\|obfuscate\|mapping.txt\|dSYM\|upload.*symbol" .github/ fastlane/ Makefile 2>/dev/null
ls docs/monitoring/ 2>/dev/null
```

Report what is wired and what is missing before changing anything.

### Step 2 — Load the layer rules

Call `stack-dispatcher` as above. The facade, the context keys, the breadcrumb observer and
the three error channels come back from it. Verify each is present; wire the missing ones
**to the layer's shape**, not to a shape invented here.

### Step 3 — The reporting filter — this is the step that decides whether the dashboard survives

**Rule: only errors a human must act on reach crash reporting.** Noise is what kills a
dashboard — not volume, noise. Ten thousand `NetworkError`s from users on trains bury the
one real regression, and after two weeks nobody opens the tool.

| Reach crash reporting | Stay in the UI |
|---|---|
| 5xx from any endpoint | Any expected 4xx — 401 re-auth, 403, 404 on a deleted item, 409 handled as a conflict, 422 validation |
| Connect / send / receive timeouts | Offline and no-connectivity |
| Parse and deserialization failures | User cancellation, back-navigation aborts |
| Unexpected state — an impossible enum branch, a broken invariant | A permission the user declined |
| Platform-channel and secure-storage failures | A retry that then succeeded |

**The decision lives on the error type, never at the catch site.** `isReportable` is defined
in `api-style/dio`; obey it. A `catch` block that decides for itself will disagree with the
next `catch` block, and expected 4xx will be back on the dashboard within a month.

Uncaught → `fatal: true`. Handled and reportable → `fatal: false`. Never `catch (_) {}`.

### Step 4 — Context keys and breadcrumbs

Every report must be triageable **without reproducing it**: flavor, app version, build
number, pseudonymous user id, current route, and the navigation breadcrumb trail. Shapes and
call sites are the observability layer's — verify presence, do not redefine.

Two failure modes to check for specifically:
- A report with no `flavor` means staging noise pages the on-call.
- Route names containing identifiers (`/courses/8f1c…`) make breadcrumbs ungroupable and are
  themselves a data leak. Route names are static patterns.

### Step 5 — Symbol upload is part of the release job, never manual

**Rule: the job that produces the binary uploads the symbols, in the same run.** An
unsymbolicated trace is unreadable, and it cannot be recovered later — the mapping only
exists for that exact build, and once the machine is gone the crash is permanently a hex
dump. A human "remembering" to upload after a release is a process that fails on the release
that matters most.

Per shipped build, produced and uploaded by the release job (workflow file owned by
`ci/flutter-release`):

| Artifact | From | Needed for |
|---|---|---|
| Dart symbol files (`app.*.symbols`) | `--obfuscate --split-debug-info=<dir>` | Any obfuscated build — without it every Dart frame is meaningless |
| Android `mapping.txt` | R8 / Proguard | Java/Kotlin frames |
| Android native debug symbols | the engine `.so` symbols | Engine and plugin native frames |
| iOS dSYMs | the archive — Runner **and** `Flutter.framework` | All iOS frames |

Also archive the symbol directory as a build artifact keyed by `version+build`, retained at
least as long as that version can still be running in the field. Uploading and keeping are
two different guarantees; you want both.

### Step 6 — Alerts fire on rate changes and new signatures, never on counts

**Rule: no alert threshold is an absolute count.** Counts scale with traffic. "More than 50
crashes an hour" fires every time marketing runs a campaign and stays silent through a
weekend outage — and after the third false page, people mute the channel. Once an alert is
muted it is worse than no alert, because everyone believes it is still watching.

Express every threshold as a delta against a comparable baseline, and give each one a
documented first response.

| Alert | Fires on | Compared against | First response |
|---|---|---|---|
| Crash-free users drop | −0.5pp sustained 2h | the same version's 7-day median | Halt the staged rollout, then open triage on the top signature by users |
| Crash-free sessions drop with users flat | −1.0pp sustained 2h | previous version at comparable adoption | Look for a crash loop — one screen retrying. Ship a kill switch before a fix |
| New crash signature in the current release | first occurrence, ≥N distinct users | zero occurrences in any prior version | Owner assesses within one working day; batch same-release signatures into one notification |
| ANR rate rise | +0.2pp | previous version at comparable adoption | Profile the main thread on the top ANR screen; ANRs never show up in crash triage on their own |
| Cold start p90 regression | +20% | previous version, same device class | Bisect the release's bootstrap changes; check work moved into `main()` |

Rules that keep these usable:
- **Gate every alert on adoption.** No rate alert may fire below the adoption floor you set
  in the metrics section. This alone removes most release-day false pages.
- **Batch new-signature alerts during a rollout.** One notification per release window with
  the new signatures listed, not one page per signature — a release always produces several,
  and paging per signature is how you train people to ignore the channel.
- **Every alert names a human first response.** An alert with no documented response is a
  notification, and notifications get muted.

### Step 7 — Write it down

Write `docs/monitoring/MONITORING.md`:

```markdown
# Monitoring
## Metrics and thresholds
<the metrics table, with this app's adoption floor and per-metric targets>
## Alerts
<the alert table — thresholds as deltas, each with its first response>
## What reaches crash reporting
<the filter table>
## Symbols
<where symbol artifacts are archived, and by which job>
## Triage rota
| Week | Owner |   ← a person's name, never "the team"
```

Then report: what was already wired, what you changed, and what still needs a human (vendor
console alert configuration, rota names).

---

## `/flutter-monitoring triage`

Weekly. Takes 30 minutes. Produces decisions, not a reading.

### Step 1 — Name the owner

**Rule: one named person owns triage each week, not "the team".** An issue assigned to a
group is assigned to nobody; issues without an owner survive indefinitely, and the ones that
survive longest are the hard ones that matter. Take `--owner` or ask. Write the name in the
document and in `MONITORING.md`'s rota.

### Step 2 — Close last week's loop first

Open the previous `docs/monitoring/TRIAGE-*.md`. For every item: did the decision happen?
- "Fix now" not shipped → it is now the top item, and say why it slipped.
- "Cannot reproduce" from last week → did the breadcrumbs ship, and did the next occurrence
  carry them? If instrumentation shipped and the crash recurred with no new detail, the
  instrumentation was wrong — that is this week's finding.

### Step 3 — Rank

**Ranked by users affected, descending. Ties and near-ties broken by new-in-this-version.**
A regression you just shipped outranks an equally sized issue that has been there for six
months, because it is fresh in someone's memory and its cause is in a diff you can read.

Two overrides, applied deliberately and noted in the document:
- A crash on a money, auth or data-loss path outranks its user count. Ten users unable to
  pay beats a thousand seeing a cosmetic glitch.
- An issue whose *rate* is climbing outranks a larger flat one.

Check adoption before ranking anything by a rate. Below the floor, rank by absolute users
affected and say the rates are not yet readable.

### Step 4 — Force a decision on every issue

**Rule: no issue leaves triage undecided.** Four outcomes, and only four:

| Decision | Means | Required with it |
|---|---|---|
| **Fix now** | Blocks the release or is actively burning users | Named assignee and a date. Halt the rollout if it is a rollout regression |
| **Fix next release** | Real, not urgent | A tracked issue with the signature, user count and version |
| **Accept** | Not worth fixing | **A written reason and the number accepted.** "Accepted: 3 users on Android 8 with a broken WebView, 0.01%." An acceptance without a reason is just an unfixed bug |
| **Cannot reproduce** | You do not have the data | A note naming **which data is missing**, plus the instrumentation that will supply it |

**"Cannot reproduce" is a logging gap, not a verdict on the crash.** Add the breadcrumbs,
context key or log line that would have answered it, ship them, and bring the issue back to
next week's triage. Do not close it — closing converts a monitoring failure into an
apparently clean dashboard, which is the worst possible outcome. If an issue is
cannot-reproduce three weeks running, the instrumentation is the bug: escalate that, not the
crash.

Breadcrumbs added for this reason go through the observability layer's facade and
observer — a one-off `print` added to chase a crash is banned there and will not survive a
release build anyway.

### Step 5 — Every fix ships with a test that fails without it

A crash that recurs after being marked fixed costs more than the original, because nobody
believes the dashboard any more. The regression test goes at the layer where the crash is
decidable — a unit test on the parser, a widget test on the state that was null. If no test
can express it, say so in the document: an untestable crash usually means the bug is in the
design, and that is worth knowing.

### Step 6 — Write `docs/monitoring/TRIAGE-<YYYY-MM-DD>.md`

```markdown
# Crash triage — <date>
**Owner this week:** <name>
**Versions in the field:** <version> (<adoption>%), <version> (<adoption>%)

## Health
| Metric | Value | vs last week | Readable? |
|---|---|---|---|
| Crash-free users | 99.4% | −0.2pp | yes |
| Crash-free sessions | 99.8% | flat | yes |
| ANR rate | 0.31% | +0.05pp | yes |
| Cold start p90 | 2.4s | +180ms | yes |
| Adoption, newest version | 4% | — | **no — rates below the floor** |

## Issues
| # | Signature | Users | Sessions | New in | Decision | Owner | Due |
|---|---|---|---|---|---|---|---|
| 1 | `_CastError` in CourseMapper | 412 | 903 | 3.4.1 | Fix now | <name> | <date> |
| 2 | ANR in ImageCache.evict | 88 | — | — | Fix next release | <name> | 3.5.0 |
| 3 | `PlatformException(no_activity)` | 3 | 3 | — | Accept — 3 users, Android 8 WebView, 0.01% | — | — |
| 4 | Null check in CheckoutPage | 31 | 44 | 3.4.0 | Cannot reproduce | <name> | next triage |

## Instrumentation shipped for cannot-reproduce
| Issue | Missing data | Added | Ships in |
|---|---|---|---|
| 4 | route + payment step at failure | breadcrumbs on the checkout step machine | 3.4.2 |

## Carried from last week
<what did not happen, and why>
```

Then report the top three items and their owners in the chat, and offer: "Run
`/flutter-monitoring setup` if any alert failed to fire for these."

---

## `/flutter-monitoring feedback`

Build or audit the in-app report path. Two things ship together: the report, and the review
prompt that must never be confused with it.

### Reachable from two places

Settings ("Report a problem"), and **every error state** — the retry screen carries the
report button. A user who has just hit the bug is the one moment they can describe it.

### The diagnostics payload — attached automatically

**Rule: the user writes the description; the app supplies everything else.** A report that
depends on the user knowing their OS version is a report you cannot act on.

| Field | Source | Why triage needs it |
|---|---|---|
| App version + build number | env | "Fixed in 3.4.2" is unanswerable without it |
| Flavor | env | Staging reports must not be treated as production |
| Platform + OS version | device info | Half of all bugs are one OS version |
| Device model + class | device info | The other half are one device |
| Locale | env | Formatting, RTL and text-overflow bugs live here |
| Current route | crash-context key | The screen, without asking |
| Connectivity at the moment of report | connectivity | Distinguishes "broken" from "offline" |
| Redacted log buffer | the `AppLogger` ring buffer | The last N entries, already redacted by the facade |
| **Pseudonymous session reference** | the existing session/user id | Joins this report to your own logs |

Two constraints that are easy to get wrong:

- **The log buffer is the facade's, redacted by the facade.** Do not build a second buffer
  and do not re-implement redaction at the feedback screen — a redaction implementation that
  exists in two places is one implementation and one bug. Cap it by both entry count and
  age, so a long session cannot ship a megabyte of history.
- **The session reference is the pseudonymous id the observability layer already sets**, not
  a new one minted here. A fresh id joins to nothing, which defeats the entire point of
  attaching it.

### What the payload must never contain

Email, name, phone, account handle, raw token or `Authorization` header, full URI with query
string, precise location, or the raw (unredacted) log buffer. If you want to reply to the
user, take a **reply address they type**, and treat it as message content, not as a
diagnostic field.

The pseudonymous reference exists so you never need identity: it joins the report to your
logs without collecting anything identifying, and it is revocable — an email is neither.

### The user sees exactly what is sent, and can remove it

**Rule: the preview is the payload itself, not a description of it.** Render the actual
fields and the actual log lines, scrollable, with a per-item (or at minimum per-section)
remove control, and send only what remains. A summary that says "diagnostic information"
is a consent dialog that has not obtained consent.

Offer a screenshot or screen recording as an **opt-in** attachment — it removes a round trip
and often the whole reproduction. Show the image before sending, because a screenshot can
contain anything that was on screen; the user decides.

### The in-app review prompt is a limited resource

The OS caps how often the prompt can be shown, silently ignores requests past the cap, and
gives you no signal about whether it appeared or what the user did. Spend it deliberately.

| Rule | Because |
|---|---|
| Only after a **success** — an order placed, a course finished, a streak hit | Asking at a neutral moment spends a capped ask on a shrug |
| **Never after an error**, and never on or near a failure screen | You are asking someone annoyed to rate you publicly |
| **Never on launch**, never in the first session, never mid-task | Interruption is what a one-star review is about |
| **Never twice to someone who dismissed it** | Persist the dismissal; if you have accounts, persist it server-side, because local state dies with a reinstall |
| Never a custom dialog that imitates the OS one, and never a reward for a review | Store policy, and it is a dark pattern |
| Rate-limit yourself below the OS cap — at most once per major version, with a long cooldown | The OS quota is shared across your whole app; a wasted ask is gone for months |

The review prompt is not feedback. If someone wants to tell you something, the report path
above is where they should land — never route a complaint into a store review.

---

## Never

- Never judge a release's crash rate before adoption clears the floor.
- Never quote crash-free users without knowing whether sessions agree.
- Never alert on an absolute count.
- Never send an expected 4xx to crash reporting.
- Never upload symbols by hand, and never ship a build whose symbols were not archived.
- Never close a cannot-reproduce issue.
- Never leave an issue owned by "the team".
- Never put an email, a name or a raw token in a diagnostics payload.
- Never show the review prompt after an error.

---

**Related skills — apply together:**
- `logging/flutter-observability` — the facade, redaction, crash context, breadcrumbs, error
  channels, analytics and flags this command depends on. It owns the code; this owns the practice
- `api-style/dio` — defines the error types and `isReportable` that the reporting filter obeys
- `ci/flutter-release` — owns the release workflow where symbol upload lives
- `slo` — the same delta-not-count discipline for server-side error budgets
- `dora` — change failure rate and MTTR are the delivery-side view of these crash numbers
- `debug` — once triage says "fix now", root-cause investigation starts there
