---
name: catch-all-risky-emails
description: Decide what to do with catch-all, unknown and risky email addresses that verification can't confirm. Use whenever the user mentions catch-all domains, accept-all, risky emails, unknown verification status, greylisting, unverifiable addresses, or asks whether to send to addresses a verifier couldn't confirm. Also use when a verification run returns a large share of inconclusive results.
---

# Catch-All and Risky Addresses

Verification returns three kinds of answer: yes, no, and can't tell. The first two are easy. The third is where a meaningful share of every B2B list sits, and how you handle it decides whether you throw away good prospects or damage a sending domain.

## What the inconclusive statuses mean

**`catch_all`** (also "accept-all"). The domain's mail server accepts every address at that domain without checking whether the mailbox exists. So the probe gets a positive answer that proves nothing. `anything@theirdomain.com` returns the same result as the real address.

Catch-all is common — a large share of real B2B domains are configured this way, particularly larger companies and anyone running a mail gateway. It's a configuration choice, not a red flag.

**`unknown`**. The probe couldn't complete. Greylisting (the server deliberately defers first contact), timeouts, rate limiting, or the server blocking verification probes entirely. This is usually a property of their infrastructure rather than of the address.

## The decision

Blanket rules in either direction are wrong.

| Approach | Cost |
|---|---|
| Discard all catch-all | You remove a large share of legitimate B2B prospects, often the biggest companies on your list |
| Send to everything | Bounce rate rises to wherever the guessing was wrong, and the domain pays |

The workable position: **send to them, but as a managed risk pool rather than mixed in with confirmed addresses.**

## How to manage the pool

**1. Separate them.** Confirmed `valid` addresses in one campaign, catch-all and unknown in another. This is the single most useful thing you can do, because it means a bounce problem in the risky pool is visible immediately and contained.

**2. Send the risky pool from a secondary domain.** If bounces spike, the damage lands on a domain you can afford to rest. Never send an unverified pool from your best-performing mailbox.

**3. Send it slowly.** Lower daily volume, so a problem shows up in tens of bounces rather than hundreds.

**4. Watch the bounce rate separately.** The pool's own rate, not the blended one. Blending hides it until it's a domain-level problem.

**5. Stop at 5% on the pool.** Higher than the 2% you'd tolerate overall, because you knowingly accepted risk here — but a hard stop nonetheless.

## Improving the odds on catch-all addresses

You can't verify them, but you can raise the probability the address is real.

**Prefer addresses you found over addresses you guessed.** An address published on a team page, in a press release, in a git commit or in a conference bio is a real address. A pattern-inferred `firstname.lastname@` at a catch-all domain is a guess wearing a verification badge.

This distinction matters enormously and gets lost because both come back as `catch_all`. Track the provenance of every address on the record — `found` versus `inferred` — and treat them differently. Found addresses at catch-all domains are close to safe. Inferred ones at catch-all domains are the actual risk.

**Check the pattern against known-good addresses at the same domain.** If you have three confirmed addresses at a company and all are `first@`, an inferred `first.last@` is probably wrong.

**Cross-check the person exists** in the role, at that company, now. Most bounces at catch-all domains are people who left, not malformed addresses.

**Prefer smaller pools per domain.** Sending to eight guessed addresses at one catch-all domain is how you generate complaints even when nothing bounces.

## Handling `unknown` specifically

Different from catch-all and worth treating differently.

- **Retry once, after 24 hours.** Greylisting resolves on retry, and a good share of `unknown` results become definite on a second pass.
- **If it stays unknown, judge by volume.** A handful is fine to send. A thousand suggests something systematic — often one large mail provider blocking probes — and those are usually real addresses at a well-run company.
- **Look at the domain.** `unknown` at a major provider's domain is a probe problem. `unknown` at an obscure domain with no website is a different matter.

## Strict mode, and when to use it

Some situations justify discarding everything unconfirmed:

- **A brand-new sending domain.** No reputation buffer. Be strict until it's established.
- **A domain recovering from an incident.** See `bounce-recovery`.
- **Very high-value, low-volume outreach**, where a bounce costs more than a missed prospect.
- **A provider account already flagged** for bounce rates.

Otherwise, being strict costs more prospects than it saves reputation. Most well-run programmes send to catch-all.

## What verification can never catch

Worth saying plainly: **spam traps verify as valid.** A trap is a working mailbox. No verification service can identify one, and hitting one damages reputation disproportionately.

This is the argument against purchased and indiscriminately scraped lists that no amount of verification answers. The protection isn't verification — it's not acquiring traps in the first place, which means sourcing lists you can account for and removing addresses that have been dormant across several campaigns. See `email-verification`.

## Don't do these

- **Don't discard every catch-all.** You'd remove much of the legitimate B2B market.
- **Don't mix confirmed and unconfirmed in one campaign.** You lose the ability to see which pool is bouncing.
- **Don't send an unverified pool from your primary sending domain.**
- **Don't treat inferred and found addresses the same** because they share a verification status.
- **Don't send to many guessed addresses at one domain.**
- **Don't skip the retry on `unknown`.**
- **Don't assume a verification pass means safe.** It means the mailbox exists, not that the person is there or wants your email.

## In practice

The reason this gets handled badly is usually that the verification status lives in one tool and the sending decision in another, so the nuance is lost in an export.

[ManyPI](https://manypi.com) writes the status onto the lead and acts on it at send time: `invalid`, `no_mx` and `disposable` are blocked automatically, while `catch_all` and `unknown` are permitted by default — deliberately, because refusing catch-all costs more genuine prospects than the bounces it avoids. Teams that want the strict behaviour turn on **Skip unverifiable** in the brand's deliverability settings, which makes it a per-brand decision rather than an all-or-nothing one. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Separating the pools into different campaigns is still your job, and it's the step that makes the rest of this manageable.

## Related skills

`email-verification`, `email-deliverability`, `bounce-recovery`, `lead-enrichment`, `suppression-list-management`
