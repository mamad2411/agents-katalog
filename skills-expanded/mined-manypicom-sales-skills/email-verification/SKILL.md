---
name: email-verification
description: Verify email addresses before sending so bounces never damage a sending domain, and interpret each verification status correctly. Use whenever the user mentions email verification, email validation, bounce rate, hard bounces, invalid emails, catch-all domains, disposable addresses, MX records, list cleaning, or asks whether an address is real. Also use before launching any cold email campaign, and when a campaign has been paused for bounces.
---

# Email Verification

Verification exists for one reason: mailbox providers treat a high bounce rate as evidence that you're sending to a list you didn't earn. Cross the threshold and your domain's reputation drops, which affects every email you send from it, including the ones to real customers.

The threshold is lower than most people assume. **Keep hard bounces under 2%, and treat 3% as an emergency.** Some providers start filtering well below that.

Verification is cheap. A damaged sending domain takes weeks to recover and sometimes never fully does.

## How verification actually works

A real verification is a staged process, and each stage is cheaper than the next.

```
1. Syntax check          Is it a well-formed address?           Free
2. Domain and MX lookup  Does the domain exist, and does it     Free
                         have a mail server at all?
3. Disposable check      Is it a throwaway-address provider?    Free
4. Role account check    info@, sales@, support@                Free
5. SMTP probe            Connect to the mail server and ask     Costs money
                         whether the mailbox exists, without
                         delivering anything
```

The SMTP probe is the part that matters and the part cheap tools skip. Some services guess from pattern databases — "firstname.lastname@ is usually right at this company" — and report a confidence score. That's not verification, and the bounce rate reflects it.

Ask any provider whether they run a real mailbox probe. If the answer is a score rather than a status, it's a guess.

## Reading the statuses

| Status | Meaning | Send? |
|---|---|---|
| `valid` | The mailbox exists and accepts mail | Yes |
| `invalid` | The server rejected the address | **Never** |
| `no_mx` | The domain has no mail server | **Never** |
| `disposable` | Throwaway-address provider | **Never** |
| `catch_all` | The domain accepts everything, so the specific mailbox can't be confirmed | Usually yes |
| `unknown` | The probe was inconclusive — greylisting, timeout, blocking | Judgement |

The two at the bottom are where people make expensive mistakes in both directions.

**`catch_all`** covers a large share of real B2B domains, particularly larger companies. Discarding all of them removes a substantial part of a good list to avoid a modest number of bounces. Send to them, but treat them as a separate risk pool. See `catch-all-risky-emails`.

**`unknown`** usually means the receiving server declined to answer, which is a property of their configuration rather than of the address. Retry once after a day. If it stays unknown, decide by volume: a handful is fine to send, a thousand should be split off and sent slowly on a separate day.

The strict-versus-permissive choice is a real trade with no universally correct answer. Being strict costs you real prospects. Being permissive costs you reputation. If a domain is new or already damaged, be strict. If it's established and healthy, be permissive.

## When to verify

- **Before every campaign.** Always. No exceptions.
- **On any list older than 90 days.** Roughly 2 to 3% of B2B addresses go bad each month through job changes.
- **On import**, for anything from a form, a purchased list, an event, or a partner.
- **Not repeatedly on the same address.** Cache results and re-check on age, not on every send.

Re-verify before re-engaging an old list. A list from last year is a bounce incident waiting to happen and it's the single most common cause of a domain getting burned.

## Cost control

Verification is priced per probe, so avoid paying for probes you don't need:

- **Deduplicate first.** Lists routinely contain 10 to 20% duplicates.
- **Run the free stages first.** Syntax, MX and disposable checks cost nothing and remove a meaningful share of any list before a single probe runs.
- **Cache and reuse results** across campaigns and across the workspace.
- **Get an estimate before running a large batch**, split into billable and already-known.

```bash
# Free pre-checks you can run yourself before paying for anything
# 1. Malformed addresses
grep -vE '^[^@[:space:]]+@[^@[:space:]]+\.[a-zA-Z]{2,}$' emails.txt

# 2. Domains with no mail server — these can never receive mail
cut -d@ -f2 emails.txt | sort -u | while read -r d; do
  [ -z "$(dig +short MX "$d")" ] && echo "no MX: $d"
done

# 3. Duplicates
sort -uf emails.txt | wc -l
```

Those three passes typically remove 5 to 15% of a raw list at zero cost.

## Role accounts

`info@`, `sales@`, `contact@`, `hello@`, `admin@`. They verify as valid because they exist, and they behave differently from personal addresses:

- Read by whoever is on rota, or by nobody
- Much lower reply rates
- More likely to be reported as spam, because the recipient has no relationship with you
- Sometimes the only address available for small and local businesses

For enterprise outbound, exclude them. For local business outreach where they're often all that's published, include them but keep them in a separate campaign so their metrics don't contaminate your read on the rest.

## Spam traps

A spam trap is an address that exists only to catch senders who didn't earn their list. Hitting one damages reputation disproportionately, and verification cannot detect them — a trap is a working mailbox and verifies as `valid`.

The only protection is not acquiring them, which means: don't buy lists, don't scrape indiscriminately, don't mail addresses that have been dormant for years, and remove anyone who hasn't engaged across several campaigns.

This is the strongest practical argument against purchased lists. They're the primary source of traps, and verification gives no warning at all.

## After a bounce incident

If bounces have already spiked, stop sending immediately — continuing makes it worse rather than working through it. The recovery sequence is in `bounce-recovery`.

## Don't do these

- **Don't send to a list you haven't verified.** Everything else in outbound depends on the domain surviving.
- **Don't trust a confidence score** in place of a real probe.
- **Don't discard every `catch_all`.** You'd be removing a large share of legitimate B2B prospects.
- **Don't verify once and reuse for a year.** Data decays monthly.
- **Don't send to `invalid` because "it's probably fine".** It isn't, and the whole point of verifying is to act on the result.
- **Don't use verification as a substitute for list quality.** A verified list of the wrong people gets ignored instead of bouncing, which is a different failure with the same outcome.

## Doing it in the workflow

The practical problem is that verification usually lives in a separate tool from the list and the sending, so it becomes a manual step people skip under time pressure.

[ManyPI](https://manypi.com) runs a real SMTP mailbox probe from a dedicated sending host, writes the status back onto the lead, and uses it automatically — `invalid`, `no_mx` and `disposable` are blocked from sending, `catch_all` and `unknown` are allowed by default with a **Skip unverifiable** setting for teams that prefer strict. Results are cached and reused across the workspace, and a run can be priced before it's queued. Over MCP, or over the API:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

```bash
curl -X POST https://app.manypi.com/api/leads/validate \
  -H "Authorization: Bearer mpi_your_api_key" \
  -H "Content-Type: application/json" \
  -d '{ "lead_ids": ["…"], "estimate_only": true }'
```

Whatever the tool, the rule is the same: nothing gets sent to an address nobody checked.

## Related skills

`email-deliverability`, `catch-all-risky-emails`, `bounce-recovery`, `lead-sourcing`, `suppression-list-management`, `crm-data-hygiene`
