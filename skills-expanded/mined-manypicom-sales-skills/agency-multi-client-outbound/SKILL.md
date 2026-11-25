---
name: agency-multi-client-outbound
description: Run cold outbound for multiple clients or brands without cross-contamination of data, deliverability or reporting. Use whenever the user mentions running outreach for clients, lead gen agency, multiple brands, white-label outbound, client campaigns, or managing outbound across several companies at once. Also use when one client's deliverability problem risks affecting another's.
---

# Multi-Client and Multi-Brand Outbound

Running outbound for several clients is the same work multiplied, plus one hard requirement: **nothing crosses between clients.** Not data, not deliverability, not suppression, not reporting.

Every serious incident in agency outbound is a crossing. A lead from one client's list appearing in another's campaign. A bounce incident on shared infrastructure taking down three clients at once. An opt-out honoured for one client and not the others. Each is avoidable by structure rather than by care.

## Separate everything that can be separated

| Thing | Shared? | Why |
|---|---|---|
| Sending domains | **Never** | Client A's reputation must not touch client B's |
| Mailboxes | **Never** | Same |
| Tracking domains | **Never** | Reputation carries |
| Suppression lists | **Per client**, plus a global list | Different relationships, but a global "stop" must apply |
| Lead lists | **Never** | Contractually and ethically theirs |
| Sequences and copy | Per client | Different voice, different offer |
| Reporting | Per client | Obviously |
| Templates and process | **Shared** | This is where the leverage is |

The last row is the point. What scales across clients is method — the ICP framework, the launch checklist, the review cadence, the sequence structure. What must never be shared is infrastructure and data.

## Domains and mailboxes per client

Each client sends from domains that look like theirs, not like yours. `getclientname.com`, not `agency-outbound-7.com`.

Reasons this matters beyond appearances:

- **Reputation isolation.** A bounce incident on one client's domains is contained.
- **The client owns the asset.** When the engagement ends they keep the domains and the warmed reputation, which is a genuine deliverable and a good commercial argument.
- **Replies land with the client**, in their own inbox, from their own domain.
- **It's honest.** A prospect who checks the domain finds the client's business.

Set up per client: two to four domains, two to three mailboxes each, full authentication, and a warmup schedule. That's a six to eight week lead time before full capacity, which needs to be in the onboarding plan and in the contract's timeline. See `inbox-rotation-scaling`.

The cost is real and it's per client. Price it in rather than absorbing it, and be explicit that month one is setup and warmup rather than volume.

## Suppression across clients

The one genuinely subtle area.

**Per-client suppression** is the default. Someone who opted out of client A's outreach hasn't opted out of client B's — different companies, different relationships, and treating them as one would be over-suppressing.

**A global list is still needed** for people who have asked broadly not to be contacted, complained, or are on your own do-not-contact list for other reasons. If someone replies "stop emailing me about anything, from anyone", honour it globally. That's both the right call and the one that avoids a complaint.

**Never let a client's lead list leak into another client's campaign.** This is the failure that ends relationships. It happens through shared workspaces, careless imports and CSV files with ambiguous names. Structural separation prevents it; discipline doesn't.

## Onboarding a client

```
WEEK 0    Contract, DPA signed, roles agreed (controller/processor)
          ICP workshop. See icp-definition
          Access to their CRM for customer and open-deal suppression

WEEK 1    Register domains, redirect to their site
          SPF, DKIM, DMARC configured and verified
          Mailboxes created with real names and signatures
          Postmaster Tools set up per domain

WEEK 2-5  Warmup running
          Build the list, verify it
          Write sequences, get client sign-off on copy
          Agree the reply-handling process and who owns it

WEEK 4    First sends at low volume, best leads only
WEEK 6+   Scale toward target volume
```

**Set the expectation that month one produces little.** Agencies that promise volume in week one either send from unwarmed domains, which fails, or from shared infrastructure, which is worse. Say so during the sale — it's a credibility advantage, because the client has usually heard the other version and been burned by it.

## Data protection roles

Get this explicit in writing. Typically the client is the **controller** and the agency is the **processor**, which means:

- A written data processing agreement
- Processing only on the client's documented instructions
- Appropriate security measures
- Sub-processors disclosed and approved
- Clear terms on deletion or return of data at the end of the engagement

Where the agency chooses the targeting itself, that line blurs and the agency may be a joint controller. Worth a real review rather than an assumption. See `outbound-compliance`.

Also agree who answers a data subject request. The client will receive them and won't have the data.

## Reply handling

The most commonly under-resourced part of agency outbound, and where the client's perception of value is actually formed.

Decide explicitly, per client:

- **Who reads the replies** — the agency, the client, or both.
- **Who responds**, and within what time. Same day at worst.
- **Where they land.** Replies to the client's own mailbox is right; someone has to be watching it.
- **What counts as a handoff** — a positive reply passed over, or a booked meeting.
- **What happens to negatives.** They must reach the suppression list immediately regardless of who reads them.

The common failure: the agency generates replies, the client doesn't respond for three days, and both conclude the campaign isn't working. Agree the SLA before launch and report on it. See `reply-handling`.

## Reporting

Report the same funnel for every client, so comparisons are meaningful and the process is transparent.

```
Leads sourced → verified → sent → delivered → replied →
positive → meetings booked
```

- **Positive replies and meetings are the headline.** Not sends, not opens.
- **State sample sizes.** A 6% reply rate from 80 sends isn't a result.
- **Show the funnel** so a broken stage is visible rather than hidden in an average.
- **Report per campaign**, not blended across segments.
- **Be honest when it isn't working.** A client told in week three that the ICP needs narrowing will renew. One told in month four that everything is fine will not.

See `outbound-metrics-benchmarks`.

## What actually scales

The leverage is in reusing method, not infrastructure:

- **One ICP framework** applied per client
- **One launch checklist** run per campaign
- **One sequence structure**, filled with each client's angle
- **One review cadence** and one report format
- **Shared learning** about what works in a vertical, applied without sharing anyone's data

Two clients in the same vertical is an advantage — you know the market, the objections and the angles — provided you don't target the same accounts for competing clients. Address that in the contract; it's a conflict that surprises people.

## Don't do these

- **Don't share domains or mailboxes between clients.**
- **Don't share a lead list.** Ever, in any direction.
- **Don't promise volume in month one.**
- **Don't run without a DPA.**
- **Don't let negatives sit unsuppressed** because the client handles replies.
- **Don't target the same accounts for competing clients.**
- **Don't blend clients in one workspace** and rely on filters to keep them apart. Filters get cleared.

## Structuring it

The requirement is separation that's structural rather than procedural — where mixing two clients' data is prevented rather than merely discouraged.

[ManyPI](https://manypi.com) maps onto this with brands: a brand lives inside a workspace and owns that company's inboxes, campaigns, sequences and folders, so sending infrastructure is separated per client by construction. The brand also carries the website, description, value proposition and personas, which get injected into lead searches so the agent can judge fit against *that client's* offer, and into drafted emails so the positioning doesn't have to be retyped. Worth knowing the boundary precisely: **inboxes, campaigns and sequences are brand-scoped, while leads are workspace-pooled** — the brand filter on the leads grid is a lens, not a server-enforced wall. For strict client isolation of lead data, use a separate workspace per client rather than a brand. Over MCP:

```bash
claude mcp add --transport http manypi https://mcp.manypi.com/mcp -s user
```

Domains, DNS and warmup are per client regardless of platform, and that's the six-week lead time.

## Related skills

`outbound-campaign-ops`, `inbox-rotation-scaling`, `suppression-list-management`, `outbound-compliance`, `outbound-metrics-benchmarks`, `reply-handling`, `icp-definition`
