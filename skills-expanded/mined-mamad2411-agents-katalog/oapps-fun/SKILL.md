---
name: oapps-fun
description: >-
  Build an app destined for oapps.fun (an oApp): the zero-secrets discipline,
  why every capability must be steward-owned ("if Bounded can't do it, you
  can't do it"), how to call out unsupported capabilities honestly, the
  x402 relay fallback for services Bounded doesn't natively provide, and the
  lifecycle: private bounded.page development, completed Open publication at
  the exact workload app-id host, and explicit Commence for the oApps slug,
  listing, token, and Gauntlet. Use
  whenever a user says the app will launch on oapps.fun, become an oApp,
  be community-owned / token-governed, or "outlive its creator". Part of the
  Bounded skill family; the mechanics live in bounded-backend / bounded-onchain.
---

# Building for oapps.fun (oApps)

An **oApp** is an app that outlives its creator: it launches on
[oapps.fun](https://oapps.fun), gets a token, a build fund, and a community
that governs it. Bounded is the steward that operates it. The full standard is
at [oapps.org](https://oapps.org); the operational story is at
[oapps.fun/under-the-hood](https://oapps.fun/under-the-hood).

Everything in this skill follows from one design goal:

> **The creator must not be able to rug the app.** Not "promises not to" —
> structurally can't.

As steward, Bounded's job is to remove every dependency a person could hold
over the app. If any capability rides on a credential, account, or server that
a human controls, that human can kill or hostage the app no matter what the
token says. So for oApps:

- **Everything must be Bounded-owned.** Hosting, data, auth, payments,
  wallets, onchain access, AI — all provided by the runtime, billed to the
  app's own buckets, governed by its proven policy.
- **Zero secrets.** The app carries no API keys, no vendor accounts, no
  credentials in anyone's drawer. Most apps simply never need one.
- **If Bounded can't do it, you can't do it.** This is the rule, and it is a
  feature: a smaller app nobody can kill beats a bigger app with a kill switch.

## The lifecycle: local → Bounded → Open → Commence

An oApp passes through four states.
Keep its direct app address separate from its stable venue page and its later oApps slug.

**1. Local.** You build in a normal repo.
Nothing is deployed or public.

**2. Bounded (development).** Promote the creator app with `bounded init`, `bounded verify`, `bounded deploy`, and `bounded site deploy dist`.
At creation the app claims a slug derived from its name plus a random suffix, such as `myapp-x7k2.bounded.page`.
That is a development address, not an oapps.fun address.
There is no oapps.fun URL until Commence.

While building, keep the creator site **private** (`sitePrivate`, set through the dashboard or API).
The platform serves a sign-in gate to everyone else, and `bounded site preview` mints short-lived view links when you need to show someone.
Do not flip it public yourself.
Open publishes a separate governed workload only after the full opening completes.

**3. Open (public, awaiting Commence).** Completed Open creates the venue-owned root and workload, then makes the exact workload site and source public at `https://<workloadAppId>.bounded.page`.
It also publishes the stable venue page at `/l/<rootAppId>`.
The app is real and usable, but it has no oApps slug, venue listing, token, or running Gauntlet yet.
The creator app remains a disconnected development sandbox.

**4. Commenced.** An explicit Commence action claims `<slug>.oapps.fun`, writes the venue listing, creates the token sale, and starts the Gauntlet.
Commence does not create the app or make its source public because Open already did both.
The direct workload app-id host remains public, and `/l/<rootAppId>` remains the canonical venue page before and after Commence.
Choose the requested slug before Commence because its pointer becomes governance-controlled once Commence completes.

### Community code contributions while exact patches are closed

Do not tell a contributor that `bounded propose` submitted code or created a voteable proposal.
The venue cannot yet carry the exact reviewed diff through approval, build application, and promotion, so code-patch submission remains fail-closed.

The only supported code-draft mode is local inspection:

```bash
bounded propose --title "Show the streak counter" --slug <oapp-slug> --dry-run
```

That command reads the local Git tree, prints the exact diff and deterministic `draftHash`, and never opens a venue session or writes a proposal.
The hash is local comparison evidence, not an onchain content commitment or proposal id.
Use the oApp's Ideas tab to submit the intended outcome as a normal idea holders can vote on today.
`bounded proposals <slug>` is only the read-only viewer for proposal history and backlog.

**Boundaries come first, not last.** Write `policy.json` boundaries early,
while you build, not as a launch chore. They are the single most important
trust artifact reviewers and buyers will read alongside your source. An app
whose money and state rules are proven invariants graduates cleanly. An app
with ad-hoc checks in function code reads as a rug risk.

The launch gate (`publish-oapp`) REFUSES an app that does not satisfy ALL of the
following, so these are requirements and not advice.

| What | Required value | Refusal if wrong |
|---|---|---|
| `boundaries` | present at all | `no_boundaries` |
| `boundaries.posture` | `"closed"` - nothing changes except what you open | `posture_not_closed` |
| `boundaries.binding` | `"all"` - applies to everyone including you | `binding_not_all` |
| `boundaries.egress` | declared (an empty `allow` IS a declaration) | `egress_missing` |
| `boundaries.policy` | a `"mode": "locked"` freeze covering `openApps` (NOT over `boundaries` - see below) | `policy_freeze_missing_openapps` |
| `openApps.activity` | `"public"` - every prompt and change on the record | `activity_not_public` |
| a deployed policy | the app must have one to launch | `no_deployed_policy` |
| accepted terms | current version, accepted | `terms_not_accepted`, `terms_version_unsupported` |

Do NOT choose `boundaries.amend` or add a freeze over the `boundaries` section on
your creator app.
Neither is a launch requirement, and both are DERIVED by the platform on the
launched clone: graduation sets `amend: "none"` and seals `boundaries` there
(`lockGraduatedPolicy`), replacing any freeze you tried to pre-declare.
Sealing `boundaries` on your own creator app is what used to wedge a launch (see
the next section), so leave it to the platform.

Launching is ONE-WAY. A second `publish-oapp` on an app that already launched
answers `409 already_launched` and carries the launched app's id as `appId` -
that id is the venue-owned clone, which is the thing your users are using. It is
never an error to retry a launch you are unsure landed: the ritual is idempotent
and converges on the same clone.

`boundaries.egress` is REQUIRED, not optional. On the functions lane the egress
gateway is always constructed and fails closed if it cannot be built, but the host
allow-list only BINDS when the app declared one - without a declaration,
destinations are unrestricted. For an ordinary Bounded app that default is right:
you should not have to enumerate every host to ship. For an oApp it is wrong,
because the entire promise is that the app can only do what it publicly declared,
and an undeclared egress surface is the one hole through which a governed build
could later reach anywhere. An empty `allow` array is a real declaration and the
honest one for an app that talks to nothing.

### What shape the app can take, and what visitors get

oApps are framework-independent: Open does not require Vite, React, a `package.json`, or any particular layout.
What it requires is honesty between three artifacts: the synced source, the deployed frontend (if any), and the policy.
There are two shapes, and both are first-class openings.
They differ in what a visitor sees first at `https://<workloadAppId>.bounded.page` and, after Commence, at `<slug>.oapps.fun`:

**An app with a web frontend.** Deploy the exact static files users should see with `bounded site deploy dist --with-source`.
The platform serves those bytes as-is forever, and governed edits keep the human source and the deployed `dist/` in sync.
For anything beyond hand-written HTML, build with a real bundler.
**Vite is the recommended default**, and a real bundler is effectively required when the frontend uses `@bounded-sh/client` because CDN imports break it at runtime; see **bounded-frontend**.
Plain static HTML with no JavaScript is equally valid: what you deploy is what visitors use.

**An app with no web frontend** can be a CLI, an agent, or a pure backend.
It is still a real oApp: the backend runs and the boundaries hold.
Its home page becomes the public repo view.
Visitors landing on the direct workload app-id host, or the oApps slug after Commence, see the app's source browser with files, history, `Download .zip`, and `bounded clone`, plus a link to the stable `/l/<rootAppId>` venue page for history, reports, and governance.
They read and take the project rather than using it in the browser.
Say this plainly before Open so nobody expects a web app to appear.

Either way, the synced source must be the real, complete project.
If the deployed frontend is compiled output, the source that compiles into it rides along in the same tree.
Never add a framework, a bundler, or an unused `init()` call merely to change shape because Open does not ask for them.

**The dist must be reproducible.** A deployed frontend classifies at Open,
and an unclassifiable one refuses (`dist_not_reproducible`):

- **static** — every file you deploy is byte-identical to a file in your source
  tree. Only inert assets (images, fonts, media) are exempt from the match;
  anything served as code or markup — `.js`, `.html`, `.css`, `.svg`, `.wasm` —
  must be in your source verbatim, whatever its encoding. Hand-written pages
  deployed as-is land here automatically.
- **built** — your source declares how the frontend is produced: a `"build"`
  object in `bounded.json` (`{"command": "npm run build", "output": "dist"}`)
  or a `package.json` `build` script. **Open builds your source itself in an
  isolated network-less sandbox and serves THAT output from the governed
  workload.** The bytes you uploaded are not what the public workload gets -
  your own source is. Your build must succeed and produce
  `<output>/index.html`.
  This is deliberate: if the launched site were your upload while only your
  source was checked, the two could say different things, which is exactly the
  hole the standard exists to close. Your creator development address keeps
  serving your uploads as always; only the opened workload is rebuilt.
- A dist that matches nothing in source and has no working declared build is
  dead weight the community could never maintain, so it cannot Open. Fix it
  by declaring a real build, or by deploying your source files directly.

Because the rehearsal sandbox has no network, a build that fetches things at
build time (remote configs, API calls in build scripts) will fail there —
vendor those inputs into the tree instead.

What the ritual still refuses:

| What | Required | Refusal |
|---|---|---|
| synced source | `--with-source` / `sourcePush: true` | `source_not_synced` |
| every app-id literal names THIS app | yes (repeats of your own id are fine) | `app_id_literal_foreign` |
| text-only tree (binaries cannot ride the source lane) | yes | `source_not_text` |
| if the source `init()`s the Bounded client, the DEPLOYED site embeds that literal id | yes — rebuild + redeploy if stale | `clone_app_id_not_rewritten` |
| a recorded site deployment must actually be found at Open | platform-checked | `clone_site_missing_expected` |

The refusal body carries the specific `rejections`, so read them rather than
guessing.

### The `gov-frozen` freeze covers `openApps` only - never `boundaries`

The launch preset writes a single `mode: "locked"` freeze (`gov-frozen`) over
`openApps` - the token and prompt settings - and nothing else.
It deliberately does NOT freeze the `boundaries` section on your creator app,
because a freeze over `boundaries` would lock its own escape hatch: if any later
step of the ritual failed, you could no longer edit `boundaries` to fix it and
the app would be permanently unlaunchable.

The permanence you want lands on the launched CLONE, not on you.
When graduation runs, the platform seals `boundaries` and sets `amend: "none"`
on the venue-owned clone (`lockGraduatedPolicy`), and replaces any governance
lock you tried to pre-declare with the canonical one.
So the rules become genuinely unchangeable on the public app, while your creator
app's `boundaries` stay editable.

That is why a refused or partly-completed launch is always recoverable: read the
`rejections` the gate returned, fix the named row in your creator app's policy,
re-deploy, and launch again.
Launch is idempotent and converges on the same clone, so retrying a launch you
are unsure landed is never an error.
Do not add a `boundaries` freeze or an `amend` choice to "help" - it is not
required and only reintroduces the self-sealing wedge.

A related trap if you script it: read the app's current policy from
`/app/:id/details` (`GET /app/:id` is not a route and 404s), and remember a
Bounded policy is FLAT - collections are top-level keys, there is no
`collections` wrapper.
Swallowing that 404 and merging onto `null` replaces the app's whole policy with
the preset alone.

A caution worth internalizing: an AI-generated app does NOT produce a boundaries
block unless the build prompt asks for one. If you are commissioning an app that
is meant to launch, put the four fields above plus the egress allow-list in the
prompt, or the app will build cleanly and then be refused at the gate.

## What Open publishes (read before you let go)

Completed Open is the publication boundary and is separate from Commence.
Spell these implications out before starting Open:

1. **Your workload site and source become public.** Anyone can use the site at `https://<workloadAppId>.bounded.page`, read its source at `https://<workloadAppId>.bounded.page/__bounded/source`, and download the whole tree as `source.zip`.
2. **Your boundaries are published.** The governed workload's `policy.json` appears at `/__bounded/boundaries` on that same exact app-id host.
   The rules are part of the public safety story and the first thing a careful participant should read.
3. **Open creates a venue-owned root and workload copy.** The workload receives the source, site, and policy under its own app id.
   It accepts no creator-driven interactive deploy after Open; governed builds are the only update lane.
   Your original creator app remains your disconnected sandbox, and editing it no longer changes the public workload.
4. **The canonical venue page is stable.** `/l/<rootAppId>` exists when Open completes and remains the same page before and after Commence.
   People can inspect and participate in the public app while it is `awaiting_commence`.
5. **Commence is a later, explicit boundary.** It claims the requested oApps slug, writes the venue listing, creates the token sale, and starts the Gauntlet.
   It does not clone or publish the app again.
   The fee model is fixed as part of that token launch. The sale is a 24h continuous clearing auction of 65% of supply: each bid pays 3% admission plus a 0.9% gauntlet fee, win or lose, and escrows the rest. At settlement the raise pays out of escrow in a fixed waterfall: 2% creator, 1% OpenApps, a tiered gauntlet draw, a fuel tank, locked liquidity, and the remainder to the app reserve. Pool trading fees are 1% flat, claimed split 50 app reserve / 20 creator / 20 app fuel / 10 OpenApps.
   The venue may waive the gauntlet fee for select launches (operator-funded gauntlet): set once, before any demand lands, after which bids escrow and refund 100% and the graduation gauntlet draw is zero.

Source sync is load-bearing because completed Open publishes the synchronized tree rather than an unsynchronized checkout.
No synced source means Open cannot complete.
Source rides the deploy; there is no separate register or sync machinery.
Enable it once in `bounded.json`:

```json
{ "sourcePush": true }
```

With that set, every `bounded site deploy` (and `bounded deploy`) also pushes
the project source tree to the app's cloud source repository and prints
`source synced: <sha>`. One-off control: `--with-source` / `--no-source` on
the deploy commands. An oApps-bound app must deploy with source ON, and the
source that ships must be the tree that produced the deployed site.

## The capability ladder

For EVERY capability the user asks for, resolve it in this order and never
skip to a workaround:

1. **Native first.** Does the runtime provide it? `ctx.ai` (LLMs, images,
   video — no keys), `ctx.services` (Bounded-managed third-party APIs; list
   them with `bounded services`), direct crypto and provider payment rails,
   onchain (Solana collections, embedded wallets, DEX/token plugins),
   data/auth/realtime/files/functions. Route to **bounded-backend**,
   **bounded-frontend**, **bounded-onchain** for the mechanics.
2. **x402 relay second.** No native integration, but the counterparty prices
   itself with [x402](https://www.x402.org) (HTTP 402 payment-required,
   machine-to-machine)? Bounded can pay that API per-call **on the app's
   behalf** — see the next section.
3. **Call it out.** Neither exists? Say so, plainly, BEFORE building around
   it. Do not quietly wire a dependency that a person controls.

### What "calling it out" looks like

When a requested capability fails the ladder, tell the user:

- **What** can't be done and **which** dependency it would require
  (e.g. "live shipping rates need a carrier API we don't provide natively and
  that doesn't support x402").
- **Why** the rule exists: as steward, Bounded must ensure no individual —
  including you, the creator — holds a lever that can rug the app once the
  community owns it. A key in your name is exactly such a lever.
- **The nearest compliant alternative** (a native service, an x402-priced
  competitor, a reduced feature, or a manual/off-app step).

Then build the compliant version. Never "temporarily" add a user-held secret
to an oApp — the whole point of launch is that the frozen rules and the
runtime are the only trust surface.

### What counts as a forbidden dependency

- API keys or tokens the creator obtained from a vendor (even via
  `bounded secret set` — secrets are fine for private apps, not for oApps
  whose pitch is that no person is a dependency).
- External databases, servers, cron boxes, webhooks, or oracles the creator
  (or any individual) operates.
- Vendor accounts billed to a person (Stripe keys, RPC providers, mail
  providers, etc.) — the Bounded-managed equivalents exist for a reason.
- "Deploy hooks" or admin backdoors reachable only by the creator.

Credential-free public endpoints are not a rug vector, but they still need to
be declared egress and they are an availability risk — prefer native services,
and mention the risk when you use one.

## The x402 relay (the escape hatch that keeps the rule honest)

"If Bounded can't do it, you can't do it" stings less as Bounded's surface
approaches "everything". The x402 relay is how gaps get covered without
reintroducing personal keys:

- Bounded operates **one admin-funded relay wallet on Solana** (primary rail).
  When a third-party API supports x402, the steward pays it per-call from that
  wallet on the app's behalf. The app itself still holds nothing.
- **Metering:** each relayed call debits the app's **service bucket** exactly
  like measured AI spend, **plus a small surcharge that covers the payment
  transaction fee** (the send-tx costs real lamports; the app's budget carries
  it, not the platform). Price relayed features accordingly.
- **Fail-closed:** app bucket empty → that app's relay calls stop. Relay
  wallet empty → all relay calls stop until admins top up (balance alerts +
  an admin-console panel watch it). Nothing overdrafts; apps freeze, they
  don't die.
- **Trust surface unchanged:** the relay is steward infrastructure — the same
  single trusted (and replaceable) party as the rest of the runtime. No third
  party gets a key to the app.

### Using the relay from a function

The relay is a standard services tool. From any hosted function:

```ts
const res = await ctx.services.invoke("X402_FETCH", {
  url: "https://api.vendor.com/v1/thing", // https only; auth headers are rejected — that's the point
  method: "GET",                           // or POST + body (≤64KB)
  maxUsd: 0.25,                            // refuse to pay more than this per call (platform hard-cap applies)
});
// res.paid === "verification_pending" means the provider response arrived,
// but finalized settlement still belongs to the recovery lane;
// res.chargedMicroUsd = price × 1.05 markup + the flat tx-fee surcharge.
// Unsupported or unsafe payment terms return a stable public error without
// reflecting the provider's raw demand.
```

Semantics to design around: the endpoint is probed unpaid first (non-402
responses pass through for a flat routing fee); a 402 quoting Solana USDC —
either the standard x402 `X-PAYMENT` dialect or Bounded's own intake dialect —
is authorized from the relay wallet and retried with proof; anything else is a
call-out. A failure before signing, submission, or provider disclosure may
return the reserved app charge immediately. After a transaction is submitted
or a signed authorization is disclosed, Bounded never guesses that payment did
not happen and never automatically refunds from an HTTP result.
The exact operation remains held until independent finalized chain evidence
proves settlement, an exact failed transaction, or complete absence after the
signed blockhash is invalid on both recovery RPCs.
Provider receipts and transaction hints are accelerators only, never settlement
truth. Retry or reconcile the same operation after an ambiguous response; do
not create a replacement call or payment.
Discovery: `ctx.services.search("x402")` / `describe("X402_FETCH")`. The tool
is environment-gated. When disabled, treat the feature as ladder-step-3 and flag it as
"unblocks when the x402 relay is enabled".

When designing: if a needed service advertises x402 support, note it as
"relay-eligible" in your plan and budget its per-call price + surcharge into
the app's running costs.

## Rehearse before you open (`bounded oapp rehearse`)

An Open App's data starts from ZERO — none of your test data survives the
opening. `bounded oapp rehearse` lets you (and the user) experience exactly
that before committing: it creates an **ephemeral, budget-sealed rehearsal**
of the app — a fresh platform-managed copy whose data starts empty, with the
app's deployed policy mirrored on — deploys your local functions and site onto
it, runs the bootstrap you declared, and prints its address.

```
bounded oapp rehearse              # create (or converge on the live one)
bounded oapp rehearse --status     # address, expiry, spend vs sealed budget
bounded oapp rehearse --fresh      # tear down, rebirth from zero
bounded oapp rehearse --down       # tear down now
```

Declare the bootstrap in bounded.json — it MUST be idempotent, because a
rehearsal (like a real opening) starts from nothing and reruns converge:

```json
{ "rehearsal": { "bootstrap": "node scripts/bootstrap.mjs" } }
```

The script runs on your machine with `BOUNDED_APP_ID` pointing at the
rehearsal app (`BOUNDED_REHEARSAL=1` is set). Facts to rely on: the budget is
a sealed slice of the owner's credits (default $0.25, max $5 — caps cannot be
widened after birth); the rehearsal expires on its own (default 2h, max 24h)
and the platform deletes it; it can never launch as an oApp; rerunning is
cheap and expected. Backend-only apps rehearse fine — with no built dist
there is simply no site deploy.

## Practical checklist before Open and Commence

- The app uses the human owner's normal Bounded web account (`bounded init` opens login when needed; confirm with `bounded whoami`).
  Open is owner-only and needs an email-backed account.
  If this is an intentionally legacy key-owned app, use the advanced deploy account-recovery reference before Open rather than inventing a new owner.
- Boundaries were written early and cover the app's money and state rules as
  proven invariants, not ad-hoc checks. They are the trust artifact buyers
  read alongside your source.
- `policy.json` contains **no** rule, function, or egress that depends on a
  user-held credential; `bounded verify` passes.
- Functions use `ctx.ai` / `ctx.services` / `ctx.bounded` only — no fetches to
  key-authenticated endpoints.
- Every external egress is declared and either credential-free, native, or
  relay-eligible.
- Keep the creator site private (`sitePrivate`) while you build.
  Do not flip it public yourself.
  Completed Open publishes the separate governed workload at the exact workload app-id host.
- Make source ride the deploy with `sourcePush: true` in `bounded.json` or `--with-source` on the last deploy.
  After Open, verify the synchronized tree at `https://<workloadAppId>.bounded.page/__bounded/source`.
- The slug is the name the token should live at (`<slug>.oapps.fun`), so rename it before Commence if it is wrong.
  Open already created the venue-owned root and workload; Commence claims the requested slug for that opening.
- Save `/l/<rootAppId>` as the canonical venue page.
  Do not replace it with a slug-derived venue route after Commence.
- The synced tree is the real, complete project and every `init({ appId })`
  literal names this app (see "What shape the app can take").
  If the app has a frontend, the deployed site was built from THIS tree.
  A stale dist that no longer embeds the app id refuses at Open (`clone_app_id_not_rewritten`).
- If the app has NO web frontend, the user knows its home page will be the
  public repo view at the direct workload host, not a web app.
- Running costs (AI spend, service calls, relayed calls + surcharge) are
  sane against the app's expected build-fund inflow — out of budget means
  frozen, and you should be able to say at what usage level that happens.
- Anything you had to rule out is in your handoff to the user, with the
  reasoning, not silently dropped.
