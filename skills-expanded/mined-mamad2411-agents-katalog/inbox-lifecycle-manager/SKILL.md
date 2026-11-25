---
name: inbox-lifecycle-manager
description: The weekly keep/cancel/promote/buy loop for a cold email sending fleet. Decides which domains are burned and should be cancelled, which warmed reserves to promote into campaigns, which capacity to demote, and how many new domains to buy — using measured reply, bounce, age and send-volume floors instead of gut feel. Use when asked "which inboxes should I cancel", "what should I replace this week", "my fleet costs too much", "I'm under my send goal", or as the Friday hygiene routine.
---

# Inbox Lifecycle Manager

**Diagnosis tells you a domain is sick. This skill decides whether it dies.**

Every cold email fleet leaks money in two directions at once: you keep paying for burned domains
that will never reply again, and you run under your send goal because nobody promoted the warmed
reserves sitting idle. This is the weekly loop that fixes both, with an approval gate in the
middle so nothing gets cancelled on a hunch.

**Read-only by default.** The plan step writes nothing, anywhere. Only the apply step, run after
an explicit human "yes", changes a tag, a campaign, or a provider subscription.

## When to use

- The weekly hygiene routine (Friday morning is the natural slot — see `/cold-email-weekly-rhythm`)
- "Which inboxes should I cancel?" / "What's burned?" / "Clean up my domains"
- "I'm under my daily send goal" / "How many domains do I need to buy?"
- "My inbox bill is too high" — the spend section prices every domain against what it earns
- After `/email-deliverability-audit` or `/deliverability-incident-response` hands you a
  `SENDER_BURNED` verdict and you need to act on it

**Not this skill:** *why* a domain is bad (`/email-deliverability-audit`), fixing DNS
(`/zapmail-domain-setup-public`), an acute incident (`/deliverability-incident-response`),
warmup settings and signatures (`/smartlead-inbox-manager`).

---

## The status model

Four statuses, and they apply to a **whole domain**, never to one inbox inside it.

| Status | Meaning | Warmup | In campaigns |
|---|---|---|---|
| **Warmup** | Newly provisioned, under 14 days of warmup | ON | no |
| **Insurance** | Warmed, healthy, idle — the reserve pool | ON | no |
| **Active** | Sending in live campaigns | OFF or minimal | yes |
| **Cancel** | Condemned; stop sending, cancel the subscription | OFF | no |

⛔ **Never split a domain's inboxes across statuses.** Mailbox providers judge reputation at the
domain level. Half a domain "Active" and half "Cancel" means you are still sending from a domain
you have declared burned, and the healthy half inherits the reputation of the dead half. Every
decision below is computed per domain and applied to every inbox on it.

⛔ **Warmup domains are untouchable.** Not counted as capacity, not promotable, not demotable,
not cancellable. If your tool has no `Warmup` tag, the domain's age is your only protection —
see the age guard below, and keep a list of domains provisioned in the last 30 days.

In Smartlead these statuses are tags. See `/smartlead-inbox-manager` for the tagging mechanics.

---

## Sample-size floors — the rule that is broken most often

A domain is only judged once there is enough data to judge it. Below the floor the answer is
**"we don't know yet"**, and that is a legitimate output, not a failure.

| Judgment | Floor | Why |
|---|---|---|
| Reply rate | **200 sends** in the window | At a 1% line, 200 sends is ~2 expected replies. Below 200, a 0% reply rate cannot distinguish a burned domain from an unlucky week. |
| Bounce rate | **50 sends** | Below that, one dead address reads as 2% and two read as 4% — straight through a 3% threshold. |
| Bounce *composition* | **30 classified bounces for that domain** | A domain with no sampled bounces has a 0% sender-originated share by construction, which looks identical to a rotten list. |
| Domain age | **30 days** | A domain that has not finished ramping has not earned a verdict. |
| Placement test | 100-300 senders per test | Smaller samples swing double digits run to run. |

⛔ **Unresolvable age counts as young.** If you cannot date a domain, it is `TOO_YOUNG` and it is
not cancelled. Fail closed: you can always cancel it next week.

---

## The decision ladder

Run top to bottom per domain, over a **7-day window** (fall back to 14 days if 7 days is under the
200-send floor). The first gate that matches wins.

```
G0. Status is Warmup, or any inbox on the domain is in Warmup?
      -> EXCLUDED. Not judged. Stop.

G1. Domain age < 30 days, or age unknown?
      -> TOO_YOUNG. Never a cancel candidate at any reply rate. Stop.

G2. sent < 200 in the window?
      -> INSUFFICIENT_DATA. Do not judge the reply rate. Re-check next week. Stop.

G3. sent >= 50 AND bounce_rate > 3%?
      -> BOUNCE_FORK. This is not a cancel decision yet — a high bounce rate is usually the
         LIST, not the domain. Hand to /email-deliverability-audit to classify the bounce
         codes before you condemn anything. A domain is only cancelled out of this fork when
         the bounces are majority sender-originated AND the DNS auth is already clean.
         (>20% of classified bounces in the blocklist codes 5.7.606-5.7.614, or DSN text
          naming a blocklist, means burned regardless of the bounce rate.)

G4. reply_rate >= 1.0%?
      -> KEEP. Healthy enough to stay Active. Stop.

G5. reply_rate < 1.0% (or 0 replies on >= 150 sends), age >= 30d, bounce not the story?
      -> CANCEL CANDIDATE. The domain has had a fair sample and did not reply. It is burned.
         Then one of three:
           still at/above goal without it  -> CANCEL, no swap needed
           an Insurance domain can replace it -> CANCEL + PROMOTE the oldest eligible reserve
           neither                          -> KEEP_BELOW_THRESHOLD: buy first, cancel next week.
         Cancelling into a shortfall trades a bad reply rate for no sends at all.
```

### The numbers, and where they come from

| Threshold | Value | Note |
|---|---|---|
| Cancel line (reply) | **< 1.0%** over 7d at ≥200 sends | The line below which a domain stops earning its subscription. |
| Zero-reply cancel | **0 replies at ≥150 sends** | A 0% rate is decisive earlier than a low-but-nonzero one. |
| Healthy | **≥ 1.0%** | Keep. |
| Genuinely good | **≥ 1.5%** | Full marks. Do not cancel anything near this. |
| Bounce fork / autopause | **> 3%** at ≥50 sends | Same number your sending tool should use for `bounce_autopause_threshold`. |
| Blocklist share | **> 20%** of classified bounces | Burned regardless of bounce rate. |
| Minimum age | **30 days** | Hard floor, no exceptions. |
| Placement | **≥85% inbox = healthy**, 70-84% degraded, **<70% fails** | From a real seed placement test, not a guess. |
| Warmup reputation | **< 98% = pull the inbox** | If the tool reports it live. |

> **One number, everywhere in this repo: 1%.** A domain that cannot reply at 1% after a fair
> sample is not earning its subscription. The same 1% that flags a domain in
> `/email-deliverability-audit` is the line that cancels it here — the difference between "flag"
> and "cancel" is not a second threshold, it is the **floors**: 200 sends and 30 days of age.
> Below those, 1% means nothing and nothing gets cancelled.

### Warmup-off is "held", not "healthy"

An inbox with warmup switched off reports no reputation, so you cannot evaluate it at all. Treat
it as **HELD**: excluded from capacity, not attached to campaigns, reported for a human. Do not
silently turn warmup back on to make the number appear — that rewrites the very signal you are
measuring. A shortfall caused by holds is a finding to report, never a reason to release the holds.

---

## Capacity and the buy plan

Cancelling without replacing is how you wake up at half your send goal.

```
goal            = your daily send target (emails/day)
inbox capacity  = 30/day per Google inbox, 30/day per Outlook inbox, ~15/day per SMTP inbox
domain capacity = 30 x (actual inbox count on that domain)     <- never a flat per-domain number
active capacity = sum of domain capacity over Active domains
insurance target = 50% of goal, held warm in reserve
```

⛔ **Count capacity per inbox, never per domain.** "150/day per domain" is the single most common
capacity error — it assumes 5 inboxes on every domain and silently over-reports a 2-inbox domain
by 90/day. Multiply the real inbox count.

Then:

1. **Promote** from Insurance until `active capacity >= goal` — **oldest domain first**. Age is
   trust; spend the oldest reserve, keep the newest warming.
2. **Demote** Active → Insurance when active capacity is **≥ 1.25x goal**. Paying to send more
   than you planned is still paying.
3. **Buy** when `goal + 50% insurance` exceeds what you have after promotion:

```
capacity_short   = (goal * 1.5) - (active + insurance capacity, post-promotion)
inboxes_to_buy   = ceil(capacity_short / 30)
domains_to_buy   = ceil(inboxes_to_buy / inboxes_per_domain)     # 2 per domain
```

Express the ask to a human in **emails/day of capacity**, not in domain count — "we are 900/day
short" is a decision; "we need 10 domains" is an implementation detail they cannot sanity-check.

Buy new domains with `/zapmail-domain-setup-public`, then warm them via `/smartlead-inbox-manager`.
New domains are not capacity for **at least 14 days of warmup plus the 30-day judging age** — plan
the buy a month before you need the sends.

---

## Spend math — is this domain worth its subscription?

| Item | Typical |
|---|---|
| Inbox subscription | $2.00-$2.60 / inbox / month |
| Domain registration | ~$10-12 / year (cap what you will pay; cheap TLDs are fine for sending) |
| A 2-inbox domain | ~$4-5 / month, ~60 sends/day, ~1,800 sends/month |

At 1% reply that is ~18 replies/month from a $5 domain. At 0.2% it is ~4. The cancel line is not
an aesthetic judgment — it is the point where the subscription stops paying for itself.

**Already dead, do not pay to cancel carefully:** a domain whose warmup is off *and* whose SMTP
connection fails is not sending anything. Cancel the subscription and move on; it needs no swap-in.

---

## The weekly loop

### Step 1 — Pull fresh data (read-only)

```bash
npx tsx scripts/plan-lifecycle.ts --goal=2000 --out=./lifecycle-$(date +%F)
# multi-client / agency account: omit --goal and you get verdicts only
npx tsx scripts/plan-lifecycle.ts --out=./lifecycle-$(date +%F)
```

**One goal, one sending program.** The capacity, promote/demote and buy math assume the whole
account is one program with one daily target. On an agency account with sub-clients that math is
meaningless (and the inbox list cannot be attributed to clients), so omit `--goal`: the verdict
ladder still runs per domain and is the useful half there. Measured on a 402-client, 39,829-inbox
account the full pull took about two hours, with roughly one 429 per metrics page.

**Untagged inboxes.** When an inbox carries no status tag the planner infers one: sent in the
window means `active`; idle with warmup on means `insurance`; idle with warmup off is treated as
`active` so the judge can call it dead or data-starved. Tags always win. Tag your fleet; the
inference is a fallback, not a convention.

⛔ **Always pull live.** Any cached or mirrored "last 7 days" column in your own database goes
stale silently and you will never notice — the plan just quietly starts condemning healthy
domains. The API window is the only truth.

The script pulls per-domain sent/replied/bounced for 7d and 14d, joins every inbox (age, tags,
warmup state, reputation, SMTP health), applies the ladder above, and writes:

- `plan.csv` — one row per domain, with verdict and every number that forced it
- `actions.csv` — only the rows where something should change
- a printed summary

It calls no write endpoint. You can run it on someone else's account without risk.

**Large accounts (5k+ inboxes).** The inbox inventory is the slow part: 100 per page, and
Smartlead's rate limit is account-wide, so any other job on the same key eats your budget.
Measured on a ~20k-inbox account: the pull was refused for 8+ minutes straight while
`Retry-After` kept saying 60s. The script checkpoints every page to `<out>/inboxes.jsonl`;
if the run dies, **re-run the same command and it resumes** from the last complete page.
Budget 20-40 minutes for the first pull on an account that size, run it when other sync jobs
are idle, and pass `--fresh` when you deliberately want a new inventory. The metrics pull is
checkpointed the same way (`metrics-7d.jsonl`, `metrics-14d.jsonl`) and runs per sub-client
when the account has them, which is roughly 50x faster than one account-wide pull.

### Step 2 — Report

Summarize for the human:

- Totals: cancels / demotes / promotes / buys
- Capacity vs goal, **per client or per program**, flagging anything under 90% coverage
- `KEEP_BELOW_THRESHOLD` rows — below the line but with no reserve to swap in (this is the "buy
  first" list)
- Watch list: zero-reply domains with 100-199 sends, which will cross the floor next week
- Anything with no goal set or no insurance pool at all

### Step 3 — HUMAN APPROVAL GATE

Ask plainly: *"Does this plan look right? Should I apply it?"* Wait for an explicit yes. Never
apply on a maybe.

Ask the second question too, separately: **"Tags only, or also cancel the subscriptions at the
provider?"** These are different blast radii. Tag changes are reversible in seconds; a provider
cancellation may not be reversible at all once the billing period lapses.

Ask the third question: **"Any domain provisioned recently that should be held back from
promotion?"** If your tool has no Warmup status, this question is the only thing standing between
a two-week-old domain and a live campaign.

### Step 4 — Snapshot, then apply

⛔ **Snapshot before you apply.** Write the current tag/status of every domain the plan touches to
a dated file first. Nothing in the apply path records prior state, and without a snapshot there is
no clean undo.

```bash
npx tsx scripts/plan-lifecycle.ts --goal=2000 --out=./lifecycle-$(date +%F) --snapshot
# review, get the yes, then:
npx tsx scripts/apply-lifecycle.ts --actions=./lifecycle-$(date +%F)/actions.csv --apply
```

Without `--apply` the apply script is a dry run: it prints exactly what it would change and exits.
Run the dry run every single time and read the counts before you trust them.

The apply script changes **tags only**. Two follow-ups belong to `/smartlead-inbox-manager` and
are not optional: every domain you just tagged `cancel` gets **warmup switched off**
(`set-warmup.ts --mode=disable --domain=...`), and every domain promoted to `active` gets its
warmup turned down to your sending ramp. A cancelled domain still warming is still spending.

Provider cancellations are **not** in this script on purpose. Do them deliberately, in batches you
can see, after the tag changes have settled. See the cancellation rules below.

### Step 5 — Verify (mandatory before reporting success)

A `200 OK` is not proof. Read the state back.

1. Re-fetch ~10 mutated domains and confirm the tag actually changed.
2. Re-run the capacity query and report coverage vs goal. Anything under 90% is an open item.
3. If you cancelled at a provider, read the subscription state back from the provider. Never
   report a cancel batch as successful off the cancel response alone.

### Step 6 — Rollback, if you regret it

Reversibility has a clock. Tag changes are instant to undo from the snapshot. A scheduled provider
removal is usually reversible **only while it is still scheduled** — once the period lapses the
domain and its reputation are gone. Decide fast, and check the provider's revert path exists
*before* you fire the cancel, not after.

---

## Cancellation rules (the part that costs real money)

1. ⛔ **Never cancel a domain under 30 days old**, at any reply rate.
2. ⛔ **Never cancel on a partial sample.** Under 200 sends the verdict is "unknown".
3. ⛔ **Never bulk-cancel by pattern match.** Cancel an explicit, enumerated list of domain IDs you
   have read back. A partial-match cancel on a provider API has taken out an order of magnitude
   more domains than intended; the blast radius of a wrong filter here is your whole fleet.
4. ⛔ **Never blind-retry a provider cancel.** If the response is ambiguous, read the subscription
   state back before retrying. Retrying a cancel that succeeded has cancelled neighbouring
   subscriptions on real provider APIs.
5. ⛔ **Never un-cancel a domain that is replying well** just to hit a spend target, and never
   cancel one just because a domain is idle — idle is what Insurance is for.
6. **Cancel in whole domains.** Partial-domain cancellation leaves you sending from a domain you
   have condemned.
7. **Batch small, verify each batch.** Ten domains, read back, then the next ten. A cancel run is
   not the place to discover your filter was wrong.
8. **Keep the domain registration** if the domain is worth re-warming later; cancel only the inbox
   subscription. Registration is ~$1/month, an inbox is ~$2.50 each.

---

## Failure modes

- **Stale mirrored metrics.** Any `*_7d` column you maintain yourself drifts silently. Pull live.
- **Flat per-domain capacity.** See the capacity section — multiply real inbox counts.
- **`min()` over a domain's statuses.** If a domain has mixed inbox statuses, aggregate by
  *restrictiveness* (Warmup > Cancel > Insurance > Active). Alphabetical `min()` returns "Active"
  and lets a mostly-warming domain be judged and cancelled.
- **Judging bounces per client instead of per domain.** A client-level bounce split tells you
  nothing about which domain to cancel. Attribute bounces to the sending domain first.
- **Old campaign history polluting the window.** Bounce/reply rosters often return a campaign's
  *entire* history with no date parameter. Filter client-side on the sent date, or bounces from a
  completed campaign six months ago will drive this week's cancel list.
- **Page size over 100.** Most Smartlead endpoints silently return zero rows above `limit=100`,
  which reads as "no data" instead of an error. The domain-wise analytics endpoint *accepts*
  larger pages, but an account-wide page of 1000 on a 14k-domain account never returns
  (Cloudflare 524 after ~2 minutes: the origin cannot finish it). Scope to one client, or page at 100.
- **Judging a domain that is not Active.** If an Insurance or Cancel domain shows sends, that is an
  infrastructure bug to report, not a deliverability verdict.

---

## What to do next

- **Cancels approved and applied:** buy replacements now, not when you feel the shortfall —
  `/zapmail-domain-setup-public`, then warm for 14 days via `/smartlead-inbox-manager`.
- **Plan shows no cancels and you are at goal:** nothing to do. Re-run next week.
- **Plan is mostly `INSUFFICIENT_DATA`:** your fleet is bigger than your send volume. Consolidate
  onto fewer domains before you buy more.
- **A domain is bad but you don't know why:** `/email-deliverability-audit` before you cancel it —
  a fixable DNS problem looks exactly like a burned domain in the reply rate.

## Related skills

- `/email-deliverability-audit` — *why* a domain is failing (auth, placement, bounce codes)
- `/deliverability-incident-response` — acute triage when something breaks today
- `/smartlead-inbox-manager` — tags, warmup, signatures; the mechanics this skill plans
- `/zapmail-domain-setup-public` — buying and provisioning the replacements
- `/cold-email-weekly-rhythm` — where this loop sits in the week
- `/deliverability-test-public` — reply/bounce comparison by inbox type

## Scripts

- `scripts/plan-lifecycle.ts` — read-only planner: pulls live metrics, applies the ladder, writes `plan.csv` + `actions.csv`
- `scripts/apply-lifecycle.ts` — dry-run by default; applies tag changes from `actions.csv` on `--apply`

## References

- `references/decision-ladder.md` — the full gate-by-gate tree, verdict table, and what each verdict hands off to
- `references/cancellation-safety.md` — provider cancellation procedure, batching, readback, rollback windows
