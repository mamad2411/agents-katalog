---
name: email-automation
description: >-
  Build a non-disruptive automation section inside an app's admin panel: lifecycle reminders (welcome,
  abandoned cart, post-purchase, upsell, win-back) across **email, push notifications, WhatsApp, and
  SMS**, with proven funnel timing, personal copy, a free WYSIWYG editor, conversion stats, and
  admin-only tables. Reuses the app's existing email/notification/SMS/WhatsApp providers, or lets the
  admin add API keys. Ships paused. Use for email automation, drip/lifecycle email, abandoned-cart
  recovery, push/WhatsApp/SMS reminders, or an "Email Automation" admin menu. Triggers: "email
  automation", "drip campaign", "abandoned cart emails", "reminder emails", "lifecycle emails", "welcome
  sequence", "win-back emails", "upsell emails", "push notifications", "whatsapp reminders", "sms
  reminders", "notification automation", "cross-sell sequence", "product recommendation email",
  "similar product", "like/dislike feedback".
---

# Email Automation — Admin Section Builder

Build a **world-class email automation system inside the user's existing admin panel**. It watches
user behaviour, enrols people in the right lifecycle sequence, and sends **personal, one-at-a-time
reminder emails** through the app's own configured email connection — underpinned by proven funnel
timing, not blasts.

**Goal:** increase user return, purchase, and retention — without spamming anyone and without breaking
anything that already works.

> **Read this first:** this skill is *non-disruptive by design*. It **studies the app before touching
> it**, adds **only new tables/routes** (never rewrites existing flows), **reuses the app's email
> connection**, and ships **paused**. Nothing sends until an admin explicitly turns it on.

---

**Fast path:** `references/quickstart.md` (one page). **Depth:** the references below.

> **Design standard (mandatory):** every admin page, **every table/list**, and **every email** is a
> product surface. Before shipping any of them, load the **`ui-ux-20-laws`** skill (if available) and
> run its **Audit → Implement → Trace** protocol. Use the app's design tokens for style, and these
> references for the surface rules:
> - `references/admin-design-laws.md` — the admin page and its data tables.
> - `references/email-design-laws.md` — the email canvas, hierarchy, CTA, contrast, mobile, dark mode.
>
> If the skill is not available, apply the same laws inline. Never ship a page, table, or email
> without its pre-ship checklist and a short `Trace:` block.

## The workflow

```
0. Discover ─▶ 1. Design ─▶ 2. Build ─▶ 3. Wire events ─▶ 4. Admin UI ─▶ 5. Verify ─▶ 6. Hand off
   study the     data model    new tables/    triggers →       dashboard +     dry-run +     paused +
   app + admin   + sequences   worker/cron    enrolments       tables + stats  preview       "turn on?"
```

### 0. Discover (mandatory, before any code)
Study the app thoroughly and produce a short **integration plan**. See `references/discovery.md`.
- Detect the stack, framework, ORM/DB, auth, sessions, the **admin panel** (or note its absence).
- Find the existing **email connection** (SMTP/provider SDK) — reuse it; never add a second one.
- Map **products**, **cart/checkout**, **orders**, **users**, and the events needed.
- **Understand the platform's purpose and business model** (e-commerce, SaaS, fintech, booking, …), its
  activation event, and its critical account steps — then **propose extra reminder sequences** that fit
  (email verification, profile completion, onboarding, KYC, trial/billing, booking, renewal…).
- If there is **no admin panel**, ask the user whether to create a minimal one.

### 1. Design
- Define the **data model** (`examples/data-model.md`): sequences, steps, enrolments, scheduled
  emails, sent log, settings, suppressions.
- Choose the **sequence set** and timings (`references/sequences.md`).
- **Run the UI/UX audit now**, not after coding: the admin page (`admin-design-laws.md`), every table
  it exposes, and every email template (`email-design-laws.md`). Record the decisions that will become
  the final `Trace:` block.

### 2. Build (additive only)
- Add new tables/collections, a scheduler job, and the send worker. **Do not modify existing tables.**
- Add a **feature flag / master pause switch** (default OFF) and a global kill switch.

### 3. Wire events
- Hook the app's existing events (registration, login, cart add, checkout start, purchase, inactivity)
  into enrolment — **without changing their behaviour** (observe, don't intercept).

### 4. Admin UI
- Build the page under the **`ui-ux-20-laws` skill** (if available): apply its Audit → Implement → Trace
  protocol, design tokens, and the per-surface map in `references/admin-design-laws.md`.
- Design **every table** with the table rules in `admin-design-laws.md`: aligned columns, right-aligned
  numbers, 44px row actions, pagination, responsive column hiding, empty/loading/error states,
  keyboard sort, and status shown with text + colour (never colour alone).
- Use **one icon family** consistently (reuse the app's Lucide/Heroicons/Material set; else Lucide) —
  nav, tabs, actions, status and channels. Icons speed scanning but never replace labels on primary or
  destructive actions; icon-only controls get `aria-label` + tooltip + a 44px target. Full map and a
  ready sprite: `references/iconography.md` + `examples/icons.svg`.
- **Gate it before you style it:** admin role required at the **route** (proxy/middleware), in the
  **page**, and in **every server action**; render **404** for everyone else; `noindex` the section;
  audit denials. Fail closed when no admin exists. (Rule 14.)
- Add a top-level **"Email Automation"** menu with tabs: **Sequences (with stats) · Users & recipients ·
  Settings**. See `references/admin-ui.md`.
- Design **every email** with `email-design-laws.md`: one idea, one 44px CTA, 600px single column,
  16px body, one accent, ≥4.5:1 contrast, alt text, dark mode, plain-text twin.
- Add **admin-only** **Leads / Paid** tables at the bottom of product and checkout pages.

### 5. Verify
- Dry-run mode, a **preview/test-send** tool, idempotency checks, and a stop-condition audit.

### 6. Hand off
- The system ships **paused**. Notify the admin, show a one-click "Turn on" (or let the agent help),
  and document rollback.

---

## The sequence catalog (proven funnel timing)

Full detail, copy intent, and stop conditions: `references/sequences.md`. Summary:

| # | Sequence | Trigger | Timing (default) | Stops when |
|---|----------|---------|------------------|------------|
| 1 | **Welcome / activate** | Registration | 0h welcome → 24h value → 72h social proof | Login / purchase |
| 2 | **Registered, never logged in** | Registered + no login | 1h → 24h → 72h | Login |
| 3 | **Logged in, no purchase/use** | Logged in, inactive | 1h nudge → 24h → 5d | Purchase / activation |
| 4 | **Abandoned cart / checkout / product** | Cart or checkout or product view, no purchase | **1h reminder (no discount) → 24h social proof/objection → 48–72h urgency + discount** | Purchase |
| 5 | **Post-purchase review** | Purchase (product type aware) | Next day "how's it going?" → 2 weeks "experience + upsell" | Review / unsubscribe |
| 6 | **Upsell / cross-sell** | Purchase, other products exist | After value moment (3–7 days) | Purchase of promoted item |
| 7 | **Win-back / re-engagement** | Inactive 30 / 60 / 90 days | Neutral → value → final "we'll stop" | Activity / unsubscribe |
| 8 | **Replenishment** | Consumable product | ~Day 45–60 | Repurchase |
| 9 | **Payday re-engage** | Product lead pending ≥ 7 days | 27th → last day → 2nd (calendar) | Purchase / per-product opt-out |
| 10 | **Intelligent cross-sell** | Initial sequence ends, no purchase | **7d cooldown → 7 / 10 / 14** with Like/Dislike | Like / Dislike / purchase / unsubscribe |

**Payday is a *nurture* sequence** — per product, runs alongside the promotional sequence, and shares the
one-marketing-email-per-day cap, so it never clashes with the cart reminders. On purchase the lead moves
from **Leads → Paid** and enters the paid-product sequences.

**Discounts:** upsells may carry a discount; abandoned carts carry **urgency + discount**. Default
**0%** — when 0, the email must **not mention a discount at all**. A **min-cart guard** skips the
incentive on very low-value carts. (`references/sequences.md`.)

**Precedence:** a user is in at most one promotional sequence — purchase > cart > browse > welcome >
no-login > inactive > win-back. Extra sequences: browse-abandon, back-in-stock, price-drop, dunning,
referral. See `references/sequences.md`.

**Plus platform-derived sequences** discovered from the app's purpose — e.g. **email verification,
profile completion, onboarding setup, KYC, billing/trial ending, booking reminders, renewals**. Only add
the ones the platform can detect and act on (`references/sequences.md`).

**Intelligent cross-sell** (sequence 10) upgrades the dead-end where the initial sequence finishes with no
purchase: after a **7-day cooldown** it picks the **next most similar product**, extracts its features,
uses the platform's **exact product noun** (`course` / `car` / `destination` / `property`), and enrols the
user in a **hand-typed 3-email sequence** with signed **Like / Dislike** links. Full spec:
`references/cross-sell.md`; runnable core + tests: `examples/cross-sell.mjs`.

---

## Non-negotiable rules

1. **Study before building.** Never modify existing auth, cart, checkout, order, or user flows. Add
   new tables/routes only.
2. **Reuse the existing email connection.** No second SMTP/provider setup. No mass/bulk sending —
   emails are **per-user and event-driven**.
3. **Ships paused.** Master switch OFF; admin is notified to turn it on (agent can offer to help).
4. **No spam.** Frequency caps (default ≤1 marketing email/user/24h, ≤4/week), quiet hours, and a
   **global suppression list** (unsubscribed, bounced, complained). Respect interest + consent.
5. **Stop conditions always win.** Re-check the goal (purchase/login/activation) **before every send**
   so buyers don't get cart reminders.
6. **Personal, one-to-one copy.** "From" one real person (`Name from Brand`), personally worded,
   references the actual product, one clear CTA, and a **"contact admin" link in every email**.
7. **Deliverability + legal.** SPF/DKIM/DMARC, branded sending domain, HTML + plain-text, unsubscribe
   + physical address, no spam trigger words. See `references/sending-and-compliance.md`.
8. **Everything auditable.** Every send is logged (who, which sequence/step, when, why) and every
   scheduled email is visible in the admin.
9. **Beauty + seamlessness — on every surface.** Build the admin page, its tables, **and the emails**
   under the **`ui-ux-20-laws` skill** (if available): apply its laws, tokens, and Audit → Implement →
   Trace protocol (`references/admin-design-laws.md`, `references/email-design-laws.md`). Match the
   app's design tokens so it looks native; clear hierarchy, 44px targets, accessible contrast, one
   primary action, one CTA per email. **Detect the app's icon source first**, then use one consistent
   family (app set → Lucide) for nav, tabs, actions, status and channels — see
   `references/iconography.md` §1a. The pre-ship checklists and
   the `Trace:` block are part of the deliverable, not optional polish.
10. **Template editor: reuse before adding.** If the app already has a WYSIWYG editor, **reuse it**
    (configured for email). Otherwise add a **free, self-hosted** one (TinyMCE Community / Quill /
    TipTap / Summernote / GrapesJS). Output must be **email-safe** (inline CSS, tables, ~600px, no JS),
    sanitized, with merge tokens, a conditional-discount block, and a plain-text twin. See
    `references/wysiwyg.md`.
11. **Transactional ≠ marketing; one active marketing sequence.** Tag each sequence `kind`
    (`marketing` | `transactional`); marketing respects consent/suppress/holdout, while transactional
    (verification/KYC/billing) bypasses them. Enforce **≤1 active marketing sequence per user**, plus
    consent, holdout, exclusions, quiet hours in the user's timezone, retry caps and max deferrals —
    implemented and tested in `examples/worker.mjs` + `worker.test.mjs`.
12. **Multi-channel with per-channel consent.** Email is the baseline; **push / WhatsApp / SMS require
    explicit opt-in** and per-channel suppression. **Reuse the app's existing providers**; only add
    credentials when none exists (Settings → Channels). Prefer push → email → WhatsApp → SMS with
    fallback, and never send on two channels the same day. See `references/channels.md`.
13. **Scoped unsubscribe + payday re-engagement.** A user can opt out of **one sequence for one product**
    (not all email) — respect it at send time (`sequence-optout`). Unsubscribe tokens carry a required
    `scope`, `exp` and single-use `jti`; never infer a scope from a missing field. The **payday** sequence
    is a per-product *nurture* that runs on calendar dates (27th → last day → 2nd) **after** the cart
    sequence ends, anchored **sequentially** in the user's **local** time, and moves the lead
    **Leads → Paid** on purchase via an idempotent `handlePurchase`. A date that cannot be met is marked
    **`missed`**, never sent late. See `references/sequences.md`.
14. **Admin-only means admin permission, not "logged in".** The Email Automation page, its sequences,
    recipients, sent log, statistics, test-send, exports, and the Leads/Paid tables must require the
    app's **admin role or permission** — never merely an authenticated session. Enforce it in **three**
    places: a **route-level gate** (proxy/middleware), an **authorization check inside the page**, and
    inside **every server action** (including the master switch and sequence toggles). Return **404**
    to non-admins so the surface's existence is not confirmed, mark admin routes `noindex`, audit both
    allowed and denied attempts, and **fail closed**: if no admin is configured, the surface is closed.
    There is **no** "any signed-in user" or "development mode" bypass. See
    `references/admin-ui.md` §Access control and `references/non-disruption.md` §9.
15. **Intelligent cross-sell is toggle-gated and noun-aware.** Map the host's Product model + a
    singular/plural **product noun** (`course`, `car`, `destination`, `property`, `product`) to
    `ProductSimilarityMatcher`, and keep it editable in Settings. Cross-sell **ships active**
    (`cross_sell_automation_enabled = true`); the admin pauses it with the Settings toggle, and every
    cross-sell job, listener and worker checks that toggle before enrolling or dispatching. The
    "initial sequence completed → enrol" listener is observe-only (`try/catch`) and **idempotent**
    (replay returns `duplicate`, never double-enrols). Like/Dislike are **signed, single-use**
    endpoints (no login required) — Like redirects to checkout, Dislike blacklists the product and
    re-enrols the next one after 24–48h. See `references/cross-sell.md` and
    `references/non-disruption.md` §10.

---

## Non-disruption contract (enforced)

"Non-disruptive" is **verified**, not assumed. Full checklist: `references/non-disruption.md`. Minimum:

- **Back up** the DB before migrating; migrations are **additive + reversible** (no altering existing
  tables).
- **Hooks are observe-only and wrapped in `try/catch`** — a failing observer never breaks
  registration/login/checkout/payment.
- **Ships paused** with a **global kill switch**; reuse the existing mail connection.
- **Cross-sell ships active with an admin pause toggle** and its enrolment is **idempotent** (event replay
  returns `duplicate`), so it never double-sends; the observe-only listener never breaks existing flows.
  (`references/non-disruption.md` §10.)
- **Smoke test** all five core flows after install; run a **rollback drill** (disable → drop tables →
  confirm untouched).

## Admin surface (what the admin gets)

- **Access control (hard requirement).** Everything below is admin-only in the strict sense: a stored
  admin role or explicit allowlist, checked at the route, in the page, and in every action. A normal
  account and an anonymous visitor both get **404**. This section contains PII (email + phone) and a
  send button; "logged in" is not a permission.
- **Calm, uncluttered layout** — ≤3 tabs, one primary action per view, details in a drawer, secondary/
  destructive actions in an overflow (`⋯`) menu, advanced settings collapsed, and a **checklist** that
  stays quiet when everything is fine.
- **Sending readiness checklist**, not a wall of warnings: verify the provider and sender through the
  provider API (`references/provider-api.md`), then show ✓ rows for what is done and a plain-language
  action only for what fails. When everything passes, collapse it to a green
  **"Everything is ready — nothing for you to do."** See `references/health-checks.md`.
- **Email Automation** menu (top-level), with tabs:
  - **Sequences** — opens with the performance block (KPIs, **emails sent per day**, **sales from
    email per day**, and the **provider plan/quota** card), then the list. Each sequence has
    **Start / Pause / Delete** (confirmed + soft-deleted, tucked into `⋯`), delays, discounts, stop
    conditions, a **WYSIWYG editor (reuse the app's existing one if present)**, and **add / reorder /
    delete steps**.
  - **Users & recipients** — search a user by email; expand their **sequence of emails** with the down
    caret; **cancel a specific email** or **exclude the user completely**; plus the full sent log
    **paginated by 100** with *when* and *why*.
  - **Settings** — sender (from-name/from-email/reply-to/physical address), master pause, caps,
    quiet hours, attribution window, and a **Channels** panel (email · push · WhatsApp · SMS):
    detect/reuse the app's provider or add API keys, test-send, enable/disable.
  - **Statistics are not a tab** — they live at the top of Sequences so the admin sees performance and
    the list in one place.
- **Admin-only tables** at the bottom of **product** and **checkout** pages:
  - Tabs **Leads** (pending) / **Paid** — clearly marked *"Admin only"*. A purchase moves the user from
    **Leads → Paid** and into the paid-product sequences.
  - Columns: email (→ user panel), registration/login/abandon/purchase datetimes, would-have-paid
    amount, phone (→ `tel:` call), and a caret revealing the sequence status (**active** /
    **exited-unsubscribed** / **exited-purchased**).
  - Disable-able from Email Automation → Settings, with instructions under the table title + link.

Full UI spec: `references/admin-ui.md`.

---

## When NOT to use

- **No lawful consent basis** for marketing email (offer a consent flow first).
- **Very small user bases** where automation noise outweighs value — send manually.
- **Products where email isn't the channel** (SMS/push-first) — adapt the engine, don't force email.
- **Regulated contexts** (health/finance) needing stricter review — get sign-off on copy + data flows.
- **High-assurance transactional needs** — never route receipts/security email through this system.

## Deliverables the agent produces

1. `references/discovery.md` → an **integration plan** for the specific app, including a **proposed
   sequence shortlist** derived from the platform's purpose.
2. New tables/migrations + the scheduler + send worker (additive).
3. The event hooks (observe-only).
4. The admin "Email Automation" page with **three tabs**, a performance block at the top of Sequences
   (KPIs, emails/day, sales/day, provider plan/quota), including a **free WYSIWYG editor**,
   **add / reorder / delete steps**, a **user search + per-email cancel / exclude**, and **health
   warnings** (paused, cron not running, no mail transport).
5. The admin-only **Leads / Paid** tables, designed with the table laws.
6. Email templates that pass `email-design-laws.md` (single column, one CTA, contrast, dark mode,
   plain-text twin).
7. A preview/test-send tool + dry-run + rollback notes.
8. The **UI/UX traces and pre-ship checklists** for the page, its tables, and the email set.
9. A short **hand-off doc**: what was added, how to turn it on, how to pause, how to roll back.
10. **Admin access control**: route gate + page check + per-action check, 404 for non-admins,
    `noindex`, denial auditing, and a documented way to appoint the first admin. A screenshot of the
    surface rendering 404 for a normal account is part of the proof, not optional.
11. **Intelligent cross-sell** (when the platform has a similar-product catalog): the
    `ProductSimilarityMatcher` service, the signed Like/Dislike endpoints, the 3 hand-typed email
    templates, the admin toggle + product-noun settings, and the tested state machine
    (`examples/cross-sell.mjs` + `cross-sell.test.mjs`).
12. **User-profile email sequences** — an admin-only **active / previous / pending** sequence list on the
    user profile (or attached at the bottom when there is no menu) with **stop one**, **add to a
    sequence** (product search by id/title), and **stop all** buttons; plus a user-facing **"Stop
    promotional emails"** button that stops all sequences and blocks re-enrolment. See
    `references/user-profile.md`.

---

## References

- `references/discovery.md` — study the app, find the admin, choose an integration path.
- `references/non-disruption.md` — the enforced non-disruption contract (backup, reversible migrations,
  hook isolation, smoke test, rollback drill).
- `references/triggers.md` — exact detection rules for every trigger (cart-abandon, inactivity, etc.).
- `references/sequences.md` — the full sequence catalog, precedence, timing, copy intent, stop conditions.
- `references/email-copy.md` — personal "from one person" copy standards, subject lines, templates.
- `references/sending-and-compliance.md` — scheduler, idempotency, caps, deliverability pre-flight.
- `references/compliance.md` — consent, signed unsubscribe, preference center, bounce/complaint webhooks.
- `references/admin-ui.md` — the dashboard, users tab (search/cancel/exclude), log (100/page), stats,
  admin-only tables, WYSIWYG, add/edit steps.
- `references/iconography.md` — one icon family, sizes/stroke/colour, accessibility, the full page icon
  map, and the do/don't; `examples/icons.svg` is a ready Lucide-style sprite.
- `references/admin-design-laws.md` — the admin page and tables mapped to the 20 UI/UX laws
  (Audit → Trace → checklist).
- `references/email-design-laws.md` — the 20 laws applied to the email canvas, hierarchy, CTA,
  contrast, mobile, dark mode, and in-email tables (Trace → checklist).
- `references/health-checks.md` — the humanized readiness checklist, when to warn, and exact copy.
- `references/provider-api.md` — verify account/sender, read plan, quota and reset via the provider
  API; cache and degrade to "unknown" instead of warning when unreachable.
- `references/channels.md` — multi-channel (email · push · WhatsApp · SMS), detection, consent, limits.
- `references/opt-in-prompts.md` — when and how to ask users to enable push/SMS/WhatsApp.
- `references/wysiwyg.md` — reuse an existing editor, else add one; email-safe pipeline.
- `references/cross-sell.md` — intelligent multi-product cross-sell: matching engine, signed Like/Dislike
  routes, migrations + Eloquent relationships, admin toggle, 7-day cooldown state machine.
- `references/user-profile.md` — the per-user **active / previous / pending** sequence surface with
  admin stop-one / add / stop-all and the user's "Stop promotional emails" self-service opt-out.
- `references/quickstart.md` — the one-page path.
- `examples/render.mjs` + `render.test.mjs` — Mustache email renderer + 0%-discount test.
- Run the tests with `npm install && npm test` (worker + renderer + cross-sell).
- `references/reference-implementation.md` — the engine in pseudocode + SQL (locking, reaper, attribution).
- `examples/worker.mjs` + `examples/worker.test.mjs` — executable, tested scheduler/worker core.
- `examples/cross-sell.mjs` + `examples/cross-sell.test.mjs` — `ProductSimilarityMatcher` +
  `CrossSellEngine` + signed feedback tokens (22 tests).
- `examples/cross-sell-templates.md` — the 3 hand-typed cross-sell emails (Like/Dislike links).
- `examples/data-model.md` — DB schema.
- `examples/sequence-config.json` — a concrete, editable sequence config.
- `examples/email-templates.md` — sample rendered emails.
