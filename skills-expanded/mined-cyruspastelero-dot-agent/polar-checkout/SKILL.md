---
name: polar-checkout
description: Set up Polar.sh subscription checkout on a website, end to end — embedded checkout, signature-verified webhooks, an entitlement record other clients read, a customer portal, and a preflight check that gates the deploy. Use when asked to "add Polar", "set up polar.sh", "sell subscriptions on the site", "add a paid plan / pricing page with real payments", "take payments on the web instead of in-app purchase", or when debugging an existing Polar integration (checkout modal not opening, webhooks not landing, entitlements not updating).
disable-model-invocation: true
---

# Polar checkout, end to end

Born from a session that took a marketing site from zero to charging real cards. Everything
below was paid for once already. The failures that cost the most time were **invisible in the
code**: they lived in dashboard settings, in bundler behaviour that differs between the dev
server and the deployed function, and in a contrast ratio. Do not re-derive them.

## Phase 0 — Ask for the two things only the human has

Do this **first**, before anything else. These two are the only things you cannot discover yourself.

1. **A Polar organization access token.** Sandbox first (`sandbox.polar.sh` → Settings →
   Developers → New token). Tokens are environment-specific: verify which one you were given
   rather than trusting the label, because both start `polar_oat_`:

   ```bash
   curl -sL -o /dev/null -w "prod %{http_code}\n"    https://api.polar.sh/v1/organizations/         -H "Authorization: Bearer $T"
   curl -sL -o /dev/null -w "sandbox %{http_code}\n" https://sandbox-api.polar.sh/v1/organizations/ -H "Authorization: Bearer $T"
   ```

2. **The host that will embed the checkout**, e.g. `example.com`, plus the local dev host
   (`localhost:3000` or whatever the framework uses). You can set these yourself once you have
   a token — `PATCH /v1/organizations/{id}` with `embed_hosts` (see Landmine 1). Ask which
   hosts, don't ask them to go clicking.

Warn them once: a token pasted into a chat lives in the transcript. Sandbox tokens are
low-stakes; a **production** token can read customer records and issue refunds, so it should
be rotated after go-live. Never write either into a tracked file.

**Stack-specific guidance:** for Next.js App Router + Supabase + Vercel, read
[reference/nextjs-supabase-vercel.md](reference/nextjs-supabase-vercel.md) — cookie auth
instead of bearer tokens, the RLS shape, the CSP rule that silently kills the modal, and the
Vercel env-var trap that makes values unverifiable.

If Polar MCP is available (`claude mcp add --transport http "Polar" "https://mcp.polar.sh/mcp/polar-mcp"`,
sandbox at `.../polar-sandbox`), use it for products and webhooks instead of curl. It cannot
create organizations, tokens, or embed hosts.

## Phase 1 — Read the product, then propose the offer

Do not ask "what do you want to sell and for how much?" You can answer most of it from the
repo, and a proposal grounded in the code is both faster to approve and honest. Ask only what
the code cannot tell you.

**Recon, in this order:**

1. **What the product actually does.** Route directories, feature folders, screen names,
   navigation. `src/app/*`, `src/pages/*`, `Features/*`, tab bars. These become the feature
   list.
2. **Existing limits.** This is the most valuable signal and the most often missed. Grep for
   caps, quotas, gates, and trial logic: `limit`, `max`, `free`, `quota`, `remaining`,
   `isPro`, `premium`, `locked`, `paywall`. **What the free tier already restricts is what Pro
   should remove.** If nothing is limited, say so plainly: the product has no free/paid
   boundary yet, and one has to be designed before a subscription means anything.
3. **Identity and schema.** How users authenticate, what the user record looks like, and where
   per-user data lives. That is where the entitlement belongs and how the payer is linked.
4. **Prior monetization signals.** Existing IAP products, StoreKit config, a previous pricing
   page, `.env` keys for other payment providers, App Store metadata. If the app already
   priced itself somewhere, match it rather than inventing a new number.
5. **Voice.** Read the existing marketing copy and README so the plan descriptions sound like
   the product, not like a pricing template.

**Then propose, and make the user confirm before building:**

- **Two plans, monthly and yearly**, unless the recon says otherwise. Yearly at roughly ten
  months of monthly is the common shape; state the discount in words.
- **Check the interval is expressible before you promise it.** Polar supports only
  `day | week | month | year`. "Six months for the price of four" is a **one-time product**
  with an expiry you compute, not a subscription — a different code path and a different
  entitlement shape (Landmine 9). Settle this before writing anything.
- **A feature list where every line is checked against the code.** Cite where each came from.
  Do not write "priority support" or "early access" unless something in the repo actually
  provides them. Inventing perks is the single easiest way to make the page dishonest, and it
  is a promise someone has to keep later.
- **A price with a stated basis** — an existing IAP price, a comparable app, or the cost of the
  paid APIs the product calls. If you are guessing, say you are guessing.
- **The free/paid boundary**, drawn from step 2. Name exactly which limits Pro removes.

Present it as a short table and ask for approval or corrections. Prices live in the code as
display copy and in Polar as the real charge; they drift, which is why the preflight in Phase 6
compares them to the cent.

## Phase 2 — Decide the shape before writing code

Ask, do not assume:

- **Where does the entitlement live?** Whatever the client apps already authenticate against
  (Firestore, Postgres, Supabase). The webhook writes it; clients only read it. One boolean
  (`isActive`) is what they gate on.
- **Is there already a column that answers "is this user paid"?** `subscription_tier`,
  `is_pro`, a `plan` field, a `role` value. There usually is, and it is usually read by admin
  screens you will not think to look at. It must die, not be synced — see Landmine 16, which
  is the most expensive one on the list precisely because nothing errors.
- **How do you comp someone?** A tester, an influencer, a refund make-good. Answer it now:
  a `comp` plan slug in the same entitlement table, never a second mechanism.
- **What happens on a refund?** Not rhetorical — `order.refunded` is absent from every
  webhook subscription anyone copies, and for a one-time product nothing else covers it, so
  the default behaviour is "money back, product stays open" (Landmine 19). Decide the partial
  case too, before you are deciding it about a real customer.
- **How is a payer linked to an account?** Set `externalCustomerId` on the checkout session to
  the app's user ID. The webhook reads it back. Duplicate it into checkout `metadata` as a
  fallback for sessions created before the customer record exists.
- **Embedded or redirect?** Embedded keeps the card form on your page and needs `embedOrigin`
  on the session plus Phase 0's embed hosts. Redirect is simpler and Polar-branded.

## Phase 3 — Build it, avoiding the landmines

Read [reference/landmines.md](reference/landmines.md) **before writing any code**. Each entry
has the symptom, the cause, and the fix. Four only appear in a deployed serverless function
and never on a dev server; three more (16-18) are silent — nothing errors, the money path
stays green, and the product is simply wrong somewhere nobody pointed a test at.

Shape that works:

```
src/lib/plans.ts            plan slugs + display prices (shared, no secrets)
src/lib/entitlement.ts      pure mapping: Polar payload -> entitlement record (unit tested)
src/lib/polar.ts            SDK client + product IDs        (server only)
src/lib/polar-webhook.ts    signature verification          (server only)
src/lib/<db>-admin.ts       admin SDK singleton             (server only)
src/lib/subscription-store.ts  the only writer of entitlements
src/lib/api-auth.ts         bearer ID-token verification
src/pages/api/checkout.ts   POST: verify token -> create session
src/pages/api/portal.ts     POST: verify token -> customer portal URL
src/pages/api/polar/webhook.ts  POST: verify signature -> write entitlement
```

Non-negotiables, each of which prevents a specific class of fraud or corruption:

- **The client never states its own identity.** Resolve the user from a verified ID token on
  every paid route. A user ID in a request body is forgeable.
- **The client never names a product.** It sends a plan slug; the server maps slug → product
  ID from server-only env. Otherwise a tampered request buys any product in the org.
- **Webhooks are order-independent and idempotent.** Deliveries retry and overtake each other.
  Store Polar's `modified_at`, compare it inside a transaction, drop anything staler. Treat
  equal timestamps as fresh so replays are idempotent.
- **Cancelling is not revoking.** Polar keeps a subscription `active` with
  `cancel_at_period_end: true` until the period actually ends. `isActive` covers `active` and
  `trialing` only. Getting this wrong revokes access people have paid for.
- **An unattributable purchase is an alert, not a retry.** No user ID on the subscription →
  log loudly, return 2xx. Retrying cannot fix it.
- **Fail closed.** No webhook secret configured → refuse to process, never "allow for now".
- **Rate limit all three routes.** Checkout and portal by user id — each checkout call creates
  a real session in the merchant's dashboard. The webhook by IP, but *only after* a delivery
  fails verification, so Polar's own retry bursts are never throttled (Landmine 20).
- **Refunds revoke; partial refunds do not.** Date the expiry to the refund, and leave
  subscription-linked orders to the `subscription.*` events (Landmine 19).

Keep the Polar → entitlement mapping in pure functions with no SDK or database imports, and
unit test it. It is the code that decides whether a paying customer gets access.

**If the product already has gates that are stubbed off**, turning them on is the real change,
not the payment. Count who it bites before you flip it:

```sql
select count(*) from user_profiles p
where p.trial_ends_at <= now()
  and exists (select 1 from attempts a where a.user_id = p.user_id
              and a.created_at > now() - interval '30 days');
```

Anyone in that set is mid-session when the wall appears. Offer a grace window, apply it in the
same change as the deploy, and tell them why in the product's own voice.

## Phase 4 — Wire up the dashboards, sandbox first

1. Create two products (monthly, yearly). Prices in **cents**. Tag each with
   `metadata: { plan: "monthly" }` so the preflight can match them back to your code.
2. Register the webhook endpoint, format `raw`, subscribed to **all** `subscription.*` events:
   `created, active, updated, canceled, uncanceled, past_due, revoked`. A missing event means
   an entitlement silently never updates.
3. Add the embed hosts from Phase 0.
4. Security rules on the entitlement record: **owner reads, nobody writes.** The admin SDK
   bypasses rules, so only the webhook can grant access. Deploy the rules; do not just edit
   them locally.
5. Auth provider setup for the web, which is often different from the native app's. Apple in
   particular needs a **Services ID**, not a bundle ID — Landmine 5.

## Phase 5 — Verify with evidence, not screens

A green success page proves nothing. After each test, read the actual records.

| Test | Expected |
|---|---|
| Buy with `4242 4242 4242 4242` | Entitlement written; plan matches the product bought |
| Decline with `4000 0000 0000 0002` | **No** subscription, **no** entitlement anywhere |
| Cancel in the portal | `cancelAtPeriodEnd: true`, `isActive` **still true**, end date visible |
| Re-deliver a webhook from the dashboard | Idempotent; document unchanged |
| POST the API with no auth | 401, nothing created in Polar |
| POST the webhook with a bad signature | 403, nothing written |

**Buy something once, for real.** A synthetic event proves your server; it cannot prove you
guessed Polar's payload shape correctly, and a hand-written fixture will agree with whatever
you assumed (Landmine 7). Sign in as a test user, click through checkout with `4242…`, then
fetch the resulting object over **raw REST** (the SDK camelCases; webhooks are snake_case),
wrap it as `{type, data}`, sign it, and post it to your own endpoint. Read the row back. Pin
that payload as a fixture. Budget an hour; it is the highest-value hour in the whole build.

Then prove the rest **without any purchase** by signing events yourself with
the endpoint's secret and posting them, then reading the record and deleting it. Note Polar signs
with the **base64 of the UTF-8 secret**, not the secret:

```js
const wh = new Webhook(Buffer.from(SECRET, 'utf-8').toString('base64'));
const sig = wh.sign(msgId, timestamp, payload);   // headers: webhook-id / -timestamp / -signature
```

Use a clearly fake user ID and delete the record afterwards.

**Sweep the operator scripts.** Anything under `scripts/` that granted access the old way is
now a tool that prints "DONE" and does nothing — the most dangerous kind of broken, because
whoever runs it believes it worked. Grep for writes to whatever column you just retired, and
either point them at the entitlement table or delete them.

**Mocked unit tests cannot catch schema drift.** A store test that stubs the database client
passes just as happily against a column that does not exist or a check constraint that rejects
your new plan slug. Write a second script that runs the app's exact queries against the real
database on a throwaway user and cleans up after itself — same shape as the webhook verifier.
It is the only thing that proves the migration and the code agree.

Make the webhook verifier cover the *whole* lifecycle, not just the happy purchase: bad
signature, redelivery, an out-of-order stale event, cancel-is-not-revoke, revoke, the one-time
grant, partial refund, full refund, and an unknown product. Every one of those is a rule
somebody will otherwise break during a refactor, and each check reads the stored row rather
than trusting a response body.

**A check that reports on the wrong object is worse than no check**, because it reads as
coverage. Match the webhook endpoint by exact path and require it to be enabled — a prefix
match happily reports on a disabled decoy sitting at `/api/polar/webhook-sandbox-unused`
(Landmine 21).

## Phase 6 — Production

Copy [reference/preflight.mjs](reference/preflight.mjs) into the project as
`scripts/preflight.mjs`, add `"preflight": "node scripts/preflight.mjs"`, and adapt the host and
auth checks. It verifies, against the live dashboards, everything that cannot be seen in code:
the org can actually charge, the embed host is present, each price still matches the code to the
cent, the webhook exists with every event, and the auth domain and providers are configured. It
exits non-zero, so it gates a deploy.

Sequence:

1. Create production products, webhook, and embed hosts — same as Phase 3, new environment.
2. Set every environment variable on the host's **production** scope, `POLAR_SERVER=production`.
3. The seller completes Polar's onboarding checklist in the dashboard (identity, payout
   account, go live). Until then `capabilities.checkout_payments` is `false` and no card can be
   charged. **There is no API for this**; only the human can do it, and an org token cannot even
   read `/v1/accounts/` to see how far they got.

   Poll `GET /v1/organizations/` and read three fields, not one — connecting a payout account
   and submitting the org's details are separate steps, and expect to be told "done" while
   `checkout_payments` is still false (Landmine 12):

   | | meaning |
   |---|---|
   | `payout_account_id` set, `details_submitted_at` null | payout connected, details form never submitted |
   | `status: "created"`, `details_submitted_at` null | **not** under review — it was never sent |
   | `details_submitted_at` set, `status: "created"` | genuinely awaiting Polar's review |
   | `status: "active"`, `checkout_payments: true` | you can charge |

   Report those fields back rather than "it isn't done yet" — it tells them which step to reopen.
4. `npm run preflight` until it is all green. Then deploy.
5. After deploy, verify against the live URL: pages 200, API routes 401 unauthenticated,
   webhook 403 on a bad signature, and one signed synthetic event proving the production
   webhook writes the record. Confirm the plan resolves from the **production** product ID —
   that is what proves the deployment is running production config and not sandbox.
6. Have them buy one real subscription, then revoke it from the dashboard. A refund alone does
   not necessarily end a subscription; revoke is the thing to test.
7. Remind them to rotate the production token.

## Phase 7 — the surfaces that payment just made false

Taking money changes the meaning of copy written when the product was free. This is not
polish; some of it is a consumer-protection problem and it ships in the same change as the
checkout button. Sweep for it deliberately:

```bash
grep -rniE "\bfree\b|no limits|unlimited|at no cost|currently free" src/ --include='*.ts*'
```

Expect to find, and fix:

- **The FAQ**, usually the worst offender — "completely free", "unlimited access to all", "no
  daily limits". Check whether it feeds **FAQ structured data**; if it does, you have been
  telling search engines the same thing.
- **Schema.org offers.** A lone `"price": "0"` in a `SoftwareApplication` block. Build the
  offer list from the same plan catalogue the pricing page uses so the two cannot drift.
- **Terms of service.** Almost always contains "X is currently free to use. We reserve the
  right to introduce paid features" — describing a state that no longer exists, on the page
  people read *before* paying. It needs real prices, who the merchant of record is,
  auto-renewal and cancellation, notice period for price changes, refunds, and failed
  payments. Keep local consumer-law rights intact.
- **Privacy policy.** The payment-processor clause is usually written in the conditional
  ("if paid features are introduced"). Replace it with what is actually shared and what
  comes back.
- **Page metadata and taglines** that lead with "free".

Rewriting a company's legal pages is a bigger call than adding a checkout button. Do it, but
say plainly that you did, and show the before/after — it is their liability, not yours.

## The gap worth naming out loud

Shipping checkout means customers can pay. It does **not** mean they get anything, and it does
not mean they can manage it.

**Entitlement.** Until the client apps read the entitlement and change behaviour, a subscriber
receives the identical product — a refund risk that grows with every visitor sent to the
pricing page. Say this plainly before the pricing page goes public, and offer to build the
gating. (If the gating already exists but is stubbed off, turning it on is the real change:
see Phase 3 for counting who it bites and giving them a grace window.)

**The funnel.** Walk it signed out, from the marketing page to the card form, without typing a
URL. Count the clicks and check what survives each hop — the plan chosen on the pricing page
usually does not survive sign-in, and the failure is silent (Landmine 17). Then buy something
in sandbox and watch the success page: it is racing the webhook (Landmine 18).

**Billing.** Answer these as a signed-in subscriber on a phone, not as the developer with the
URL bar:

1. How do I see what I am paying?
2. How do I get a receipt?
3. How do I cancel?

If any answer is "type /upgrade into the address bar", billing is not shipped — and your own
terms probably promise the customer can cancel from their account. See Landmine 13.
