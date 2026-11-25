---
name: tracking-plan-scan
description: "Analytics detector: event vs tracking-plan drift, name and property drift, conversions fired early, duplicate fires."
kind: skill
pack: product
allowed-tools: [Read, Grep, Glob, Bash]
---

# Skill: tracking-plan-scan

## Premise

Product decisions are made on funnels, and a funnel is only as true as its events. Common breakages:

- An event is renamed in code but not in the plan, so the dashboard silently loses it.
- `Signup Completed` and `signup_completed` split one count in two.
- A property sent as `"42"` where the plan says number is dropped by the pipeline.
- `PackagePurchased` fires when the checkout URL is created, before anyone pays, so the ad platform is told about purchases that never happened.
- An impression fires twice, because its effect depends on a callback rebuilt every render.

None of these fails a build or a test that mocks the sink. All of them reach the decisions made on the data.

**Every finding cites both ends:** the call site `<file:line>`, and the plan line it disagrees with (or the plan's silence, or the `/define-success` file that declares the metric). It also gives the firing context the script read, the oracle that failed or the test that would settle it, and the fix. A script row is a candidate, never a finding by itself. "Tracking is consistent" is never printed without the class-coverage block (§ Output).

**Detect statically, prove by execution.** `scripts/event-inventory.py` builds the inventory: every call site, the project's wrapper resolved, names normalised, properties and the firing point read. It joins that against the plan. The proofs are a plan-diff exit code and a fake sink in a unit test: a failed write emits 0 outcome events and a confirmed write emits exactly 1 (`proof-oracles.md` § Product, V413–V417). A candidate with no harness is **Unconfirmed**, carrying the test that would settle it ([`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 2, gate 6).

## The rule

A candidate is a finding when all four hold:

1. **It ships and fires for users.** The call is in production source, reachable from a mounted route or a server handler. Debug events behind a dev flag fail here.
2. **There is an oracle for the claim.** §1, §2 and §4 need a plan: a codegen plan, a vendor export, a typed union, a plan document, or a `/define-success` metric. Without one, they print `N/A (no plan — no oracle)`, and the run gives one Hardening inventory row ([`precedents/product.md`](../../../../snippets/precedents/product.md) § 16). §3, §5, §6 and §7 need no plan.
3. **No delivery leg or design choice explains it.** A server leg that delivers the outcome (§ 11), two events that are distinct by design (§ 12), an intent event named as one (§ 14), and a per-open impression (§ 15) all fail here. So do auto-tracked and lifecycle events (§ 10).
4. **The oracle fires, or would.** Typical oracles: the plan diff exits 2, a typed channel fails `tsc`, or a fake sink counts the wrong number of events.

## Boundaries

- **PII in event properties, and tracking before consent** → security (`data-exposure-scan`, `@data-privacy-reviewer`), when the security pack is installed. This skill lists the property names it saw, in `--inventory`, and never grades them. Raw identifiers hashed before the vendor call are not a leak (§ 13). Without security, list the rows tagged `privacy (owner pack security not installed)`.
- **One flow's funnel drop-off and onboarding completion** → business `/suggest-metrics --funnel`, when installed. It consumes the AN rows here for its "missing instrumentation" line. Without business, the AN rows stand alone.
- **Whether a launch metric returns data** (NO-DATA vs STALE at runtime) → `launch-readiness` (this pack), through its query lane. §2 here is the static half: the event has no call site at all.
- **Flag evaluations reported as events** (exposure events) → devops `progressive-delivery`, when installed. Without devops, exposure events are skipped here and named in the ledger.
- **Observability metrics and logs** (`counter.inc()`, structured log events) are not product analytics → observability `metric-hygiene-scan`, when installed. Without observability, they are out of scope here, never graded as events.

## Adapt to the codebase — the lanes

Read the SDKs **and their versions** from the manifests (grep 0a), and print the lanes in the header. The script's ledger names every lane that produced a site.

| Lane | Call shapes the script reads | Plan source it trusts | Typed-channel control |
|---|---|---|---|
| **Segment / RudderStack** | `analytics.track('X', {…})`, `rudderanalytics.track`, Node object form `analytics.track({ userId, event: 'X' })`, Python `analytics.track(uid, 'X', {…})`, Ruby `Analytics.track(event:)`, Go `analytics.Track{Event:}` | Protocols / tracking-plan export (JSON); Typewriter output (shape unverified) | Typewriter codegen |
| **Amplitude** | `amplitude.track`, `logEvent`, Python `BaseEvent(event_type=)`; Ampli `ampli.packagePurchased(…)` | `ampli.json` + generated `ampli/index.*` event classes (`event_type`) | Ampli codegen; `ampli status` exits non-zero with untracked events |
| **Mixpanel / PostHog / Heap / Umami / Plausible / Statsig** | `mixpanel.track`, `posthog.capture` (+ object form), `heap.track`, `umami.track`, `plausible('X')`, `Statsig.logEvent` | a plan document or a typed union. PostHog has no repo-side schema | a typed union on the wrapper |
| **GA4 / GTM / Meta** | `gtag('event', 'x')`, `dataLayer.push({ event: 'x' })` (`gtm.*` bootstrap skipped), `fbq('track' \| 'trackCustom', 'X')` | a plan document | — |
| **Firebase / native** | `logEvent(analytics, 'x')`, `FirebaseAnalytics.instance.logEvent(name:)`, Kotlin / Swift `logEvent("x")` | a plan document | — |
| **Snowplow** | `trackSelfDescribingEvent({ event: { schema: 'iglu:…' } })`: the schema path is the name | Iglu schemas in the repo (`**/jsonschema/**`) | Snowtype (unverified) |
| **Avo** | `Avo.packagePurchased(…)` | `avo.json` + generated `Avo.*` functions | Avo codegen; `avo status` fails on uncalled functions |
| **The project's wrapper** | `trackEvent('X', {…})` and any name in `--wrapper=`. The script finds a wrapper by itself when a function forwards its own parameter as the event name to an SDK call | the wrapper's parameter type, when it is a union or an enum | the same type |

**Vendor CLIs run only when already installed, offline, and with telemetry off.** They never log in.

- `ampli status`: the CLI (1.36.6) bundles an Amplitude client and an error reporter, so treat it as phoning home. `AMPLI_SENTRY=disabled` was seen in its source. Never pass `-u`, which uploads status.
- `avo status`: the CLI (3.7.0) runs an install-tracking postinstall. Use only a pre-installed binary, and never `npm i` into the audited repo.

A CLI that needs a login is `NOT-RUN (auth)`, and the class falls back to the script; it is never PASS. Sources: the research catalog's tools table, 2026-10-19.

## The inventory script

`scripts/event-inventory.py`, beside this file (installed as `.claude/skills/tracking-plan-scan/scripts/event-inventory.py`). It uses the Python 3.8 standard library only. It reads files and never writes into the scanned repo. Run it from the repo root:

```bash
python3 -I .claude/skills/tracking-plan-scan/scripts/event-inventory.py . --wrapper=<names from 0c> [--plan=<file>] [--success=ai/product/success] --max=40
python3 -I .claude/skills/tracking-plan-scan/scripts/event-inventory.py --self-test        # 26 checks; exit 3 on a failure
```

**What it reads.**

- **Call sites.** Every lane above, plus the wrappers: the ones it discovers and the ones named in `--wrapper=`. A generic wrapper name (`track`, `log`) counts only when its first argument looks like an event name.
- **Plans.** Each `--plan` file. Otherwise it discovers the plan: `tracking-plan*` / `analytics-events*` (JSON, a YAML subset, TS unions, Markdown tables and bullets), Ampli and Avo codegen, Iglu schemas, and the wrapper's typed union.
- **Success files.** It reads `ai/product/success/*.md` § Instrumentation for metric events.

**How it compares names.** Names are normalised by word (case, separators, tense: `Signup Completed` = `signup_completed` = `SignUpComplete`).

**Context per site.** Each site gets one of:

- `on-intent`, a JSX `onClick` or `onSubmit`;
- `on-success`, `.then` or `onSuccess`;
- `on-failure`, `catch` or `onError`;
- `effect(deps=[…])`;
- `after-await(<callee>)` or `before-await`;
- `top-level`.

Each site also gets a side (`client` / `server`) and whether a dedupe id travels with it.

**Rows:**

- **AN1:** `unplanned`, or `no-plan` (one Hardening row).
- **AN2:** `never-fired`, with `metric=yes` when a success file declares the event.
- **AN3:** `spelling` (a cluster) and `convention` (outside the dominant style once there are 5 or more names).
- **AN4:** `keys-differ`, `type-conflict`, `required-missing`, `unplanned-property`, `type-mismatch`.
- **AN5:** every outcome-named event with its context.
- **AN6:** `multi-site`, `effect-deps` / `effect-no-deps`, `two-legs` (`event_id=yes|no`).
- **AN7:** `untyped-wrapper`, `bypasses-codegen`, `bypasses-wrapper`.
- **UNRESOLVED:** names built at runtime (§ 17).

`--inventory` adds SITE, PLAN and WRAPPER rows. Exit codes: 0 means no plan-backed drift; 2 means an AN1-unplanned, AN2, AN3-spelling or AN4 row backed by a plan or success file (the V413 shape: 2 before the fix, 0 after); 1 means usage; 3 means the self-test failed. AN5, AN6, AN7 and the no-plan and convention rows are read lists and never set the exit code.

**Measured** (2026-10-19). The 23 fixture roots have no analytics call (0 sites each; `mobile-defects` declares `firebase-analytics` in Gradle and never calls it). On a real NestJS + React monorepo (read-only, 7,618 files, 21 s):

- The script found the wrapper itself: `trackEvent` in the tracking provider. It forwards one event to the Meta pixel, the GTM data layer and a server Conversions-API leg, with one shared event id, and its name is typed `string`.
- It resolved 15 call sites and 14 names, with 0 unresolved. The prototype grep counted 13 names, because it missed one wrapped call.
- No plan exists, so AN1 is one Hardening `no-plan` row, and §2 and §4 print N/A.
- AN7 gives `untyped-wrapper` (15 call sites).
- AN5 gives two rows. `CompleteRegistration` follows `await register.mutateAsync`, which is the outcome. `PackagePurchased`, carrying `value`, follows `await purchase.mutateAsync`, which only creates the payment URL. That second row is the measured candidate in § 14, unverified there.
- AN6 is quiet. `OnboardingDialogShown` runs in an effect on `[open, trackEvent]`, and the wrapper is kept stable by a ref after a recorded double count (§ 15).
- The GTM bootstrap `dataLayer.push({ event: 'gtm.js' })` was first counted as an event and a `bypasses-wrapper` row. It is now skipped as an auto event (§ 10).

On `benchmarks/fixtures/launch-gaps` (2026-10-19: wrapper found, plan of 14 events, 4 success events, 16 sites, 0 unresolved, exit 2), all 15 AN seeds print: AN1 2, AN2 3 (one `metric=yes`), AN3 2 clusters (each printed at its first spelling; the `convention` rows land on the drifted lines), AN4 2, AN5 2, AN6 2, AN7 2. The `Order Placed` decoy prints as AN5 `on-success` and the read clears it. One false row: AN4 `required-missing` on a posthog-node object call, because the object lane does not read its `properties: { … }`; two AN7 `bypasses-wrapper` rows sit on server legs, which cannot use the React wrapper.

## Pre-flight greps

Run as **one** script from the repo root. Every `rg` names its path. An `rg` exit 2 is `blocked (rg exit 2)`, never zero hits. Grep 0 is context for the script: 0c names the wrappers for `--wrapper=`, and 0b names the plan for `--plan=`.

```bash
ROOTS=(.)
X=(-g '!**/node_modules/**' -g '!**/vendor/**' -g '!**/{dist,build,out,.next,.nuxt,.output,.svelte-kit,.turbo,coverage,.venv,venv,__pycache__,generated,__generated__}/**' -g '!**/*.min.*' -g '!**/{docs,ai,.claude,.git,scripts}/**')
T=(-g '!**/{test,tests,__tests__,spec,specs,e2e,fixtures,__fixtures__,mocks,__mocks__,testdata,stories}/**' -g '!**/*.{spec,test,e2e-spec,stories,test-data}.*' -g '!**/{test_*,*_test,conftest}.*')
C=(-g '*.{ts,tsx,js,jsx,mjs,cjs,vue,svelte,py,rb,go,dart,kt,swift,java}')
NC='^[^:]+:\d+:\s*(?://|\*|/\*|#|<!--)'
g() { out=$("$@" 2>&1); ec=$?; [ $ec -eq 2 ] && { echo "blocked (rg exit 2): $out" | head -3; return; }; printf '%s\n' "$out" | rg -v --pcre2 "$NC" | head -40; }
# 0a. Analytics SDKs in the manifests (the lanes to expect).
g rg -n --no-heading --pcre2 -g '**/{package.json,requirements*.txt,pyproject.toml,Gemfile,go.mod,pubspec.yaml,build.gradle*,Podfile}' -g '!**/node_modules/**' '"(?:@segment/analytics-[\w-]+|analytics-node|@rudderstack/[\w-]+|rudder-sdk-js|@amplitude/[\w-]+|mixpanel(?:-browser)?|posthog-(?:js|node)|@heap/[\w-]+|@snowplow/[\w-]+|@statsig/[\w-]+|statsig-[\w-]+|firebase|@react-native-firebase/analytics|react-ga4|@vercel/analytics|plausible-tracker|@ampli/[\w-]+)"\s*:|^\s*(?:segment-analytics-python|analytics-python|posthog|mixpanel|amplitude-analytics)\b|^\s*gem\s+["\x27](?:analytics-ruby|mixpanel-ruby|posthog-ruby)|firebase_analytics:|mixpanel_flutter:|segment_analytics:|firebase-analytics|segmentio/analytics-go|posthog/posthog-go' "${ROOTS[@]}"
# 0b. Plan and codegen files (narrowed: `**/events*` matches domain-event specs, § 16).
g rg --files -g '**/{tracking-plan,tracking_plan,trackingPlan,analytics-events}*.{json,yml,yaml,ts,md}' -g '**/ampli.json' -g '**/avo.json' -g '**/.avo/**' -g '**/iglu/**/jsonschema/**' -g '**/ampli/index.*' -g '!**/node_modules/**' "${ROOTS[@]}"
# 0c. Wrapper definitions and typed signatures (the names for --wrapper=; the script also discovers forwarding wrappers).
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" "${T[@]}" '\b(?:const|let|var|function|def|fun|func)\s+(?:track|trackEvent|trackAnalytics|trackConversion|logEvent|logAnalyticsEvent|captureEvent|sendEvent|sendAnalyticsEvent|recordEvent|track_event|log_event)\b|\b(?:track|trackEvent|logEvent|captureEvent)\s*:\s*\(\s*\w+\s*\??\s*:\s*\w+' "${ROOTS[@]}"
# 0d. Direct SDK and pixel calls (cross-check of the script's lanes; a call outside the wrapper is §7 bypasses-wrapper).
g rg -n --no-heading --pcre2 "${C[@]}" "${X[@]}" "${T[@]}" '\b(?:analytics|posthog|mixpanel|amplitude|rudderanalytics|heap|umami|statsig|Analytics)\s*\.\s*(?:track|capture|logEvent|event)\s*\(|\bgtag\s*\(\s*["\x27]event|\bfbq\s*\(\s*["\x27]track|\bdataLayer\.push\s*\(|\blogEvent\s*\(' "${ROOTS[@]}"
# 0e. Launch-metric declarations the script joins as §2 even with no plan.
g rg -n --no-heading --pcre2 -g 'ai/product/success/*.md' '^#+\s*(?:Instrumentation|Events|Tracking)\b' "${ROOTS[@]}"
```

**Measured** (2026-10-19). Across the 23 fixture roots: 0 exit-2 runs. 0a found 1 line (`mobile-defects` Gradle Firebase), and 0b–0e found 0. On the real monorepo:

- 0a found 0 lines. The pixels load as scripts, not packages.
- 0b found 0. The first, wider plan glob (`**/events*`) had matched a domain-event consumer spec.
- 0c went from 45 lines (`track\w*` matched shipment-tracking code) to 2 once the name list was closed: the wrapper, and a carrier adapter's local `let track` (read and dismissed). The context type's signature spans two lines, so the one-line signature form misses it; the script reads it.
- 0d found 3: the pixel call and the data-layer push inside the wrapper, plus the GTM bootstrap.

## The 3,000-hit path

1. **Fix the inventory first.** Pass every wrapper 0c found. If `unresolved` is more than 10 % of the sites, read the dynamic names (a name map, a constant object) and add their values as a plan or a `--wrapper`. Never triage rows from a half-resolved inventory.
2. **Group.** One AN3 row is a cluster. Group AN4 rows by event. Group AN1 and AN2 by feature (the call site's directory, the plan's section). A wrapper with `name: string` is one AN7 finding, however many sites it has.
3. **Rank.** Rank first the declared launch metrics (`metric=yes`), revenue conversions sent to an ad platform with a `value` (AN5), and events on signup, checkout and onboarding. Rank renamed events last: a dashboard may still read the old name.
4. **Read the top 30 groups.** For AN5, read both the call and the awaited write.
5. **Prefer the runtime bulk oracle at scale.** One fake-sink harness around the wrapper, run through the existing component and e2e suites, records every event with its trigger. Count per test, then compare with the plan (V415, V416).
6. **Ledger the rest** as `Live, unreviewed (k groups / n rows)`, never `checked`.

## Scans for

| § | Class | Research id | Default severity |
|---|---|---|---|
| 1 | Event fired in code, absent from the plan; or no plan at all | PR-AN-1 | medium; Hardening for the no-plan row |
| 2 | Planned event never fired, including a `/define-success` metric's event | PR-AN-2 | high for a declared launch metric; medium otherwise |
| 3 | Name drift: one event, several spellings; the convention broken | PR-AN-3 | medium; low for convention-only |
| 4 | Property drift: key sets or literal types differ per site; a required property missing | PR-AN-4 | medium; high when a launch metric's breakdown property is missing |
| 5 | An outcome event fired before the outcome (on intent, before the confirming response) or on the failure path too | PR-AN-5 | high for a revenue conversion sent to an ad platform with a value; medium otherwise |
| 6 | Duplicate firing: an effect on unstable deps, an impression in render, client + server legs with no shared id | PR-AN-6 | medium |
| 7 | Untyped event channel; direct SDK calls bypassing the codegen or the wrapper | PR-AN-7 | Hardening |

### 1. Unplanned event, or no plan

**Class** PR-AN-1 · **Severity** medium; the no-plan row is Hardening.

```
BAD:   trackEvent('PurchaseFailed', { reason })          // the plan has no PurchaseFailed
       (no plan in the repo: 14 names live only in code)
GOOD:  the event is in the plan with its properties, or it is removed
```

**Read the code:**

- Is it a debug or dev-only event behind a flag?
- Is the plan filtered by source? An event planned for the iOS source is not planned for web (§ 10).
- Is it a near-spelling of a planned event? Then it is §3.

**Finding when** the plan exists and lacks the event. With no plan, report the one inventory row and its names.

**Proof:** `event-inventory.py --plan=<plan>` exits 2 listing it, and 0 after the plan or code is fixed (V413).

### 2. Planned event never fired

**Class** PR-AN-2 · **Severity** high for a declared launch metric (`metric=yes`); medium otherwise.

```
BAD:   ai/product/success/referrals.md § Instrumentation: `Referral Sent` — no call site anywhere
GOOD:  the event fires at the outcome, or the success file names the event that does
```

**Read the code:**

- Is it fired outside the repo: a server job, a reverse-ETL, a tag-manager trigger configured in the vendor UI? Ask, and cite the answer.
- Is it fired under a different spelling? Then it is §3.

**Finding when** neither the repo nor a cited outside source fires it. The finding opens on the plan line that declares the event (`<plan file>:<line>`) — there is no call site to cite. `metric=yes` rows feed `launch-readiness` PRR-AN-2.

**Proof:** the plan diff exits 2 for it (V413). At runtime, the query returns NO-DATA (V423, `launch-readiness`).

### 3. Name drift

**Class** PR-AN-3 · **Severity** medium; low for a convention-only row.

```
BAD:   'Signup Completed' (web) · 'signup_completed' (mobile) · 'SignUpComplete' (plan)
GOOD:  one spelling everywhere, or the plan declares the variants distinct
```

**Read the code:** Are these one trigger with the same properties under two spellings, or two events by design (`StoreConnected` vs `StoreConnectedFromOnboarding`, § 12)? Is a legacy name frozen for dashboard continuity, and declared as such?

**Finding when** one trigger is counted under two names.

**Proof:** after normalisation, each cluster holds one spelling (V414).

### 4. Property drift

**Class** PR-AN-4 · **Severity** medium; high when a launch metric loses its breakdown property.

```
BAD:   trackEvent('StoreConnected', { store_type: 'manual', count: 2 })
       trackEvent('StoreConnected', { store_type: 'shopify', count: '2' })    // number vs string; plan has no `count`
GOOD:  every site sends the plan's keys with the plan's types
```

**Read the code:** Is the property optional by design? Is a spread (`...data`) supplying the missing key? The script skips spread sites for the required check. Does the pipeline coerce types?

**Finding when** a required key is missing, or a literal type contradicts the plan or another site.

**Proof:** a typed channel fails `tsc` on the bad site, or the plan diff exits 2 (V413, V417).

### 5. Outcome fired before the outcome

**Class** PR-AN-5 · **Severity** high for a revenue conversion sent to an ad platform with a value; medium otherwise.

```
BAD:   const r = await purchase.mutateAsync(id);     // creates a checkout URL; nobody has paid
       trackEvent('PackagePurchased', { value, currency });  assign(r.paymentUrl);
       <button onClick={() => trackEvent('Signup Completed')}>          // fires on the click, before the server answers
GOOD:  the purchase event fires on the payment-confirmed callback or the webhook (server leg), and
       'Checkout Started' fires on the click
```

**Read the code:**

- What did the awaited call (`after-await(<callee>)`) actually write: the outcome, or an intent such as a checkout session?
- Does a server leg fire the confirmed outcome with the same name and id (§ 11)?
- Is the name an intent name (`…Started`, `…Clicked`, § 14)?
- Is it in both the `then` and the `catch`?

**Finding when** an outcome name fires on intent, before the confirming response, or on failure, and no leg records the confirmed outcome instead.

**Proof:** a fake-sink test: a failed write emits 0 events, and a confirmed write emits exactly 1 (V415).

### 6. Duplicate firing

**Class** PR-AN-6 · **Severity** medium.

```
BAD:   useEffect(() => { trackEvent('DialogShown') }, [onClose])   // onClose is rebuilt every render
       client pixel + server Conversions API both send 'Purchase' with no shared event_id
GOOD:  deps hold only the trigger (`[open]`), the wrapper is stable (useCallback + ref), both legs share one event id
```

**Read the code:** Is `trackEvent` stable (a `useCallback` with `[]`, a ref)? Is the impression meant per open (§ 15)? For `two-legs`, does the vendor dedupe by `event_id` (Meta) or `insert_id` (Amplitude), and does the id travel on both legs?

**Finding when** one trigger produces more events than the plan specifies.

**Proof:** a fake-sink count under StrictMode, re-render and re-open (V416).

### 7. Untyped event channel

**Class** PR-AN-7 · **Severity** Hardening; medium when §3 or §4 drift the type would have stopped.

```
BAD:   trackEvent: (eventName: string, data?: Record<string, unknown>) => void
GOOD:  trackEvent<E extends EventName>(name: E, data: EventProps[E])   — or the generated Ampli / Avo functions
```

A wrapper typed `string` turns every typo into a new event, and every property into `unknown`. A direct SDK call beside a codegen plan bypasses the plan's types.

**Finding when** the channel accepts any string. It is Hardening by default, and medium when §3 or §4 found drift that the type would have stopped.

**Proof:** a misspelt name fails `tsc` or the codegen check (V417).

## Proof

The oracles, failing first and green after the fix, are in [`proof-oracles.md`](../../../../snippets/proof-oracles.md) § Product: V413 (plan diff), V414 (name cluster), V415 (outcome firing), V416 (firing count), V417 (typed event channel).

A static fact with both ends cited needs no runtime oracle: a planned name with no call site, or a required key absent from a literal object. §5 and §6 always need the fake sink, because the firing point is behaviour.

The fix's regression set covers every variant (`/product-fix`):

- an SDK call, a wrapper call, a codegen call and a server-side call;
- case, separator and tense drift;
- a missing key, an extra key and a literal type;
- `onClick`, before the `await`, and in both `then` and `catch`;
- an effect on an unstable callback, StrictMode, and two legs with no id.

## Output

```
tracking-plan-scan — lanes: wrapper trackEvent (web/src/tracking/AnalyticsProvider.tsx:60, name: string, event id on all legs),
posthog 2 direct calls; plan: ai/product/tracking-plan.yaml (31 events); success: 2 files (5 metric events)

Findings: 2 · Unconfirmed: 1

1. web/src/features/wallet/use-wallet.ts:43                                            [report-with-fix]   high
   §5 purchase fired before payment — trackEvent('PackagePurchased', { value, currency }) after
   `await purchase.mutateAsync` (creates the checkout URL; the payment lands later via billing/webhook.ts:88, which
   fires nothing). The pixel and the Conversions API receive a purchase with a value for every checkout start.
   Proof: fake sink — payment abandoned after checkout → 1 PackagePurchased (fails; expected 0).
   Fix: fire 'Checkout Started' here; fire 'PackagePurchased' from the payment-confirmed webhook with the order's event id.
2. ai/product/success/referrals.md  `Referral Sent`                                     [report-with-fix]   high
   §2 launch metric never fired — no call site in web/ or api/; the plan lists it (tracking-plan.yaml:44).
   Proof: event-inventory.py --plan=ai/product/tracking-plan.yaml exits 2 (AN2 never-fired, metric=yes).
   Fix: fire it in api/src/referrals/send-referral.use-case.ts after the commit.
3. web/src/onboarding/Dialog.tsx:4                                                      [report-flagged]    medium
   §6 impression on an unstable dependency — useEffect(…, [onClose]). Unproven link: whether the parent rebuilds
   onClose per render. Settling test: render under StrictMode, re-render twice, expect 1 DialogShown per open.

Verification: 17 candidates → 2 findings · 1 unconfirmed · 3 hardening (untyped wrapper, 2 convention) · 11 refuted
(4 intent names, 3 server-leg confirmed outcomes, 2 per-open impressions, 2 distinct-by-design names)

Class coverage:
  §1  unplanned / no plan     checked (script: 29 names vs 31 planned → 0 unplanned)
  §2  never fired             checked (3 rows → 1 finding; 2 fired by a server job, cited)
  §3  name drift              checked (1 cluster → refuted: distinct by design)
  §4  property drift          checked (4 rows → 0 findings; 4 behind a spread)
  §5  outcome before outcome  checked (6 outcome sites → 1 finding)
  §6  duplicate firing        checked (2 rows → 1 unconfirmed)
  §7  untyped channel         checked (1 Hardening: trackEvent name: string)
```

`[report-with-fix]`: both ends are read, the oracle failed, and the fix is local. `[report-flagged]`: one link is unproven (an awaited write's meaning, a parent's render behaviour, an outside leg), and the row names it and the settling test.

The coverage block lists **all seven** classes on every run:

- `checked (k rows → m findings)` when the script ran with the lanes present;
- `N/A (no plan — no oracle)` for §1, §2 (the plan half) and §4 without a plan, and `N/A (no analytics calls)` when 0a and 0d are empty;
- `blocked (<reason>)` when the script or a grep failed;
- `NOT-RUN (auth)` for a vendor CLI lane that needs a login.

## False positives / precedents

The verifier reads [`precedents/product.md`](../../../../snippets/precedents/product.md) § 10–17 and § 36–38 and [`refute-before-report.md`](../../../../snippets/refute-before-report.md) § 4. The ones this skill meets most:

- **Auto-tracked and non-track calls** (§ 10). Page and screen views, autocapture, `identify`, the GTM `gtm.js` bootstrap.
- **A second delivery leg** (§ 11). A client pixel absent when signed in, while the server leg delivers.
- **Similar names, distinct events** (§ 12).
- **Hashing before the vendor** (§ 13). Security's class either way.
- **Intent events fire on intent** (§ 14).
- **Per-open impressions repeat** (§ 15).
- **No plan, no plan-diff** (§ 16).
- **A name built at runtime is unresolved** (§ 17).

## When to run

- On a diff that adds or changes an analytics call, the wrapper, the plan, a success file's § Instrumentation, or the write an outcome event follows.
- On every whole-repo `/audit-requirements --repo`, reporting all seven classes. `launch-readiness` reads §2 (`metric=yes`) for PRR-AN-2 and §5 for PRR-AN-5.
- When a dashboard number moves without a product change, or before an ad-platform conversion is switched on.

## Halt conditions

- Do not report a high row as confirmed until a verifier other than the run that found it has passed it through [`refute-before-report.md`](../../../../snippets/refute-before-report.md) with [`precedents/product.md`](../../../../snippets/precedents/product.md). Under `/audit-requirements --repo`, that happens in its verification phase. Run standalone, apply the protocol as a separate second pass, tag those rows `self-verified`, and list the rest as Unconfirmed, Hardening, Pre-existing or Refuted. Never drop them.
- Halt on any row without both ends: the site, and the plan line, the success file, or the plan's silence.
- Do not grade §1, §2 or §4 against an invented plan. With no plan, they are N/A, and the inventory is the deliverable.
- Do not report a dynamic name as a mismatch (§ 17), or an intent name as §5 (§ 14).
- Do not run a vendor CLI that logs in, uploads (`ampli status -u`) or installs into the repo. A tool that did not run is `NOT-RUN`, never PASS.
- Do not edit the tracking plan without the plan owner's yes. A plan change alters what dashboards count.
- Do not write into the scanned repo. The script writes nothing.
- Do not re-derive a class another skill owns (§ Boundaries). Cross-link it.

## Related

- `/audit-requirements --repo` (this pack) dispatches this skill and folds its coverage block into the class ledger. `/product-fix` closes the findings failing-first. `/define-success` (this pack) names the metric events §2 joins.
- `launch-readiness` (this pack) consumes §2 and §5 for PRR-AN-2 and PRR-AN-5. `feature-surface-scan` and `entitlement-consistency-scan` (this pack) are the other product joins.
- Business `/suggest-metrics --funnel` (when installed) consumes the AN rows per flow. Security `data-exposure-scan` and `@data-privacy-reviewer` (when installed) own PII and consent.
