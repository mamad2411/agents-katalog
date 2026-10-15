---
name: price-change
description: "Change InboxMate pricing, features, or campaign coupons across all touchpoints (website, app, docs, terms, Stripe, demo page). Guides through the full process with audit, approval, and coordinated push."
---

# InboxMate Price & Feature Change Pipeline

> **Announce to the user at the very start:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> InboxMate Price Change Pipeline started.
> First I'll audit all current pricing sources, then walk you through the change.
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## PHASE 0 — Classify the Change

**Ask the user before doing anything else:**

1. **What type of change is this?**
   - **A) General price change** — base monthly/yearly prices are changing
   - **B) Campaign coupon change** — only the demo-offer discount percentages/amounts are changing (Stripe coupons)
   - **C) Feature change** — which features are included in which tier (may also involve price changes)

2. **Which tiers are affected?** (Starter / Pro / Business / All)

Wait for the user's answer before proceeding.

---

## PHASE 1 — Audit Current State

> **Announce:** `[1/5] Auditing current pricing across all sources...`

Read ALL of the following files and extract current pricing data into a summary table. **Do not skip any source.** This is the single source of truth audit.

### Sources to read:

| Source | File | What to extract |
|--------|------|-----------------|
| **Stripe config** | `/Users/martinpammesberger/Documents/psquared/agenthub/server/utils/subscriptionUtils.ts` | Monthly price IDs, yearly price IDs, tier limits (maxUsers, maxAgents, maxChats, etc.), feature flags, coupon references |
| **Stripe live** | Use Stripe MCP `list_prices` for each product | Actual live prices, verify they match config |
| **App pricing modal** | `/Users/martinpammesberger/Documents/psquared/agenthub/app/components/InboxMatePricingModal.vue` | Displayed monthly/yearly prices, demo prices, discount labels, feature lists per tier, highlight features |
| **Stripe checkout** | `/Users/martinpammesberger/Documents/psquared/agenthub/server/services/subscription/StripeService.ts` | Coupon logic (search for `DEMO_COUPONS`), which env vars are used |
| **Website landing** | `/Users/martinpammesberger/Documents/psquared/psquared-websites/apps/inboxmate/index.html` | Displayed prices (`data-price-monthly`, `data-price-annual`), feature lists per tier card, savings notes |
| **Website i18n** | `/Users/martinpammesberger/Documents/psquared/psquared-websites/apps/inboxmate/i18n.js` | Price strings in EN and DE, FAQ price references |
| **Demo page** | `/Users/martinpammesberger/Documents/psquared/psquared-websites/apps/demo-inboxmate/index.html` | Demo offer prices per tier, crossed-out prices, discount labels |
| **Terms (AGB)** | `/Users/martinpammesberger/Documents/psquared/psquared-websites/apps/inboxmate/agb.html` | Section 4 pricing, annual discount description, promotional clause |
| **Help center** | `/Users/martinpammesberger/Documents/psquared/inboxmate-docs/user-guide/workspace/usage-and-billing.mdx` | Pricing table (monthly, annual, limits, features) |
| **Comparison pages** | `/Users/martinpammesberger/Documents/psquared/psquared-websites/apps/inboxmate/vs-intercom.html` and `vs-chatbase.html` | Any hardcoded price references |
| **Insight articles** | `/Users/martinpammesberger/Documents/psquared/psquared-websites/apps/inboxmate/insights/*.html` | Any hardcoded price references |
| **Env example** | `/Users/martinpammesberger/Documents/psquared/agenthub/.env.example` | Coupon env var names |

### Output format (always use this):

```
┌─────────────────────────────────────────────────────────┐
│                 CURRENT PRICING AUDIT                    │
├──────────────────┬──────────┬──────────┬────────────────┤
│                  │ Starter  │ Pro      │ Business       │
├──────────────────┼──────────┼──────────┼────────────────┤
│ Monthly          │ €__/mo   │ €__/mo   │ €__/mo         │
│ Yearly (std)     │ €__/mo   │ €__/mo   │ €__/mo         │
│ Demo 1st year    │ €__/mo   │ €__/mo   │ €__/mo         │
│ Yearly discount  │ __%      │ __%      │ __%            │
│ Demo discount    │ —        │ __%      │ __%            │
├──────────────────┼──────────┼──────────┼────────────────┤
│ Stripe monthly   │ price_.. │ price_.. │ price_..       │
│ Stripe yearly    │ price_.. │ price_.. │ price_..       │
│ Demo coupon      │ —        │ coupon.. │ coupon..       │
├──────────────────┼──────────┼──────────┼────────────────┤
│ Max users        │ __       │ __       │ __             │
│ Max agents       │ __       │ __       │ __             │
│ Max chats/mo     │ __       │ __       │ __             │
│ Tool calls/mo    │ __       │ __       │ __             │
│ [other limits]   │ ...      │ ...      │ ...            │
├──────────────────┼──────────┼──────────┼────────────────┤
│ Key features     │ list     │ list     │ list           │
└──────────────────┴──────────┴──────────┴────────────────┘
```

**Flag any inconsistencies** between sources (e.g., website shows €X but Stripe has €Y). These must be resolved before proceeding.

---

## PHASE 2 — Plan the Changes

> **Announce:** `[2/5] Planning changes...`

Based on the user's request and the audit:

### For price changes (Type A):
- Calculate new yearly prices: `monthly × 10 / 12` (round to nearest euro)
- Calculate new Stripe yearly amounts: `displayed_monthly × 12` (in cents)
- Show a diff table: old vs new for each source

### For campaign coupon changes (Type B):
- Calculate coupon amounts: `standard_yearly - demo_yearly` (in cents)
- Determine coupon type (fixed amount, duration: once)
- Show which Stripe coupons need creating/updating

### For feature changes (Type C):
- Show which features move between tiers
- **Generate a constraints report** listing files in the agenthub repo where feature enforcement happens:

  | Feature | Config location | UI gating location | Notes |
  |---------|----------------|-------------------|-------|
  | `removeBranding` | `subscriptionUtils.ts` → `INBOXMATE_TIERS[tier].features.removeBranding` | Check components that read this flag | |
  | `humanHandover` | `subscriptionUtils.ts` → `INBOXMATE_TIERS[tier].features.humanHandover` | ... | |
  | `tools` | `subscriptionUtils.ts` → `INBOXMATE_TIERS[tier].features.tools` | ... | |
  | etc. | | | |

  Search for these patterns to find UI gating:
  ```
  grep -r "humanHandover\|removeBranding\|tools\|apiAccess\|whitelabel\|contacts\|gdprMode\|scheduledTasks\|triageEnabled\|emailAutoReply\|ticketManagement\|slackEnabled\|whatsappEnabled\|mcpEnabled" app/ server/
  ```

  Report which files need changes and what the change would be. **Do not make these changes yet** — present the report for approval.

### Output format (always use this):

```
┌─────────────────────────────────────────────────────────┐
│                    PROPOSED CHANGES                       │
├──────────────────┬──────────────────┬────────────────────┤
│ Source           │ Current          │ New                │
├──────────────────┼──────────────────┼────────────────────┤
│ [file/location]  │ [old value]      │ [new value]        │
│ ...              │ ...              │ ...                │
└──────────────────┴──────────────────┴────────────────────┘
```

**Wait for user approval before proceeding.**

---

## PHASE 3 — Execute Changes

> **Announce:** `[3/5] Applying changes across all sources...`

**Only proceed after explicit user approval.**

Apply changes in this order:

### 3a. Stripe (if prices or coupons change)
1. Create new Stripe prices via MCP (`create_price`) — yearly prices are `interval: year`
2. Create new coupons via MCP (`create_coupon`) — use `amount_off` in cents, `currency: eur`, `duration: once`
3. Note: MCP connects to PROD Stripe only. Flag DEV Stripe as manual TODO.
4. **Record all new price IDs and coupon IDs** — you need these for the next steps.

### 3b. Backend config
- `agenthub/server/utils/subscriptionUtils.ts` — update price IDs, tier limits, feature flags
- `agenthub/server/services/subscription/StripeService.ts` — update coupon env var names if changed
- `agenthub/.env.example` — update coupon env var documentation

### 3c. App frontend
- `agenthub/app/components/InboxMatePricingModal.vue` — update prices, features, discount labels, highlight features

### 3d. Website
- `psquared-websites/apps/inboxmate/index.html` — pricing cards (data-price attributes, feature lists, savings notes)
- `psquared-websites/apps/inboxmate/i18n.js` — EN and DE price strings, FAQ references
- `psquared-websites/apps/demo-inboxmate/index.html` — demo offer prices
- `psquared-websites/apps/inboxmate/agb.html` — Section 4 pricing, promotional clause
- `psquared-websites/apps/inboxmate/vs-intercom.html` — price references
- `psquared-websites/apps/inboxmate/vs-chatbase.html` — price references
- `psquared-websites/apps/inboxmate/insights/intercom-alternatives.html` — price references
- `psquared-websites/apps/inboxmate/insights/chatbase-alternatives.html` — price references

### 3e. Help center
- `inboxmate-docs/user-guide/workspace/usage-and-billing.mdx` — pricing table

### 3f. Feature constraints (if Type C)
- Apply the approved changes from the constraints report (Phase 2)

**Do NOT commit or push yet.**

---

## PHASE 4 — Verify

> **Announce:** `[4/5] Verifying all changes...`

1. **Grep for old prices** across all three repos to catch stragglers:
   ```
   grep -r "€OLD_PRICE" psquared-websites/apps/inboxmate/ agenthub/app/ agenthub/server/ inboxmate-docs/
   ```

2. **Show a final diff summary** across all repos:
   ```
   cd psquared-websites && git diff --stat
   cd agenthub && git diff --stat
   cd inboxmate-docs && git diff --stat
   ```

3. **Present the verification report** to the user.

**Wait for final approval before pushing.**

---

## PHASE 5 — Commit & Push

> **Announce:** `[5/5] Committing and pushing all changes...`

**Only after explicit "push it" or equivalent approval.**

Push all repos at once:

```bash
# 1. psquared-websites
cd /Users/martinpammesberger/Documents/psquared/psquared-websites
git add [changed files]
git commit -m "feat: [description of price/feature change]"
git push origin main

# 2. agenthub
cd /Users/martinpammesberger/Documents/psquared/agenthub
git add [changed files]
git commit -m "feat: [description of price/feature change]"
git push origin main

# 3. inboxmate-docs (auto-deploys via Mintlify)
cd /Users/martinpammesberger/Documents/psquared/inboxmate-docs
git add [changed files]
git commit -m "feat: [description of price/feature change]"
git push origin main
```

> **Announce:**
> ```
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> All changes pushed to main across 3 repos.
>
> Deployment checklist:
> □ Set env vars on agenthub deployment (if new coupons)
> □ Create DEV Stripe prices manually (MCP is prod-only)
> □ Verify inboxmate.psquared.dev after Dokploy deploy
> □ Verify docs.inboxmate.psquared.dev (Mintlify auto-deploy)
> □ Verify app.psquared.dev pricing modal
> ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
> ```

---

## Reference: Repo Locations

| Repo | Path | Branch | Auto-deploy |
|------|------|--------|-------------|
| agenthub | `/Users/martinpammesberger/Documents/psquared/agenthub` | main | No (manual) |
| psquared-websites | `/Users/martinpammesberger/Documents/psquared/psquared-websites` | main | Dokploy |
| inboxmate-docs | `/Users/martinpammesberger/Documents/psquared/inboxmate-docs` | main | Mintlify (auto) |

## Reference: Stripe Accounts

| Environment | Account | Access |
|-------------|---------|--------|
| Production | `acct_1PeH7A2MM5yLq2OK` (psquared GmbH) | Via Stripe MCP |
| Development | `acct_*Ro4DnEindd*` | Manual (Stripe dashboard) |

## Reference: Env Vars for Coupons

Set on agenthub deployment:
```
NUXT_STRIPE_INBOXMATE_DEMO_COUPON_PRO=<coupon_id>
NUXT_STRIPE_INBOXMATE_DEMO_COUPON_BUSINESS=<coupon_id>
```
