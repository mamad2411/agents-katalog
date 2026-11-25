---
name: microsoft-appsource-playbook
description: >-
  Takes a B2B SaaS onto Microsoft Marketplace (formerly AppSource and Azure Marketplace) and the
  Teams store as a publisher - transactable SaaS offer, choices locked at publish, Teams and
  Microsoft 365 app validation, Publisher Attestation, Teams-linked SaaS, private offers, co-sell
  and Azure IP co-sell (MACC) eligibility. Use whenever a vendor mentions AppSource, Microsoft
  Marketplace, the Teams store, a Partner Center offer, Microsoft co-sell, MACC eligibility,
  Frontier Accelerate or ISV Success. Do NOT use for listing copy or rank (use
  samber/developer-platform-skills@integration-listing-optimization), running your own
  marketplace (use samber/developer-platform-skills@app-marketplace-review), Teams bot code,
  Windows Store apps, services co-sell, or spending MACC as a buyer.
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# Microsoft AppSource playbook

You take a SaaS product onto Microsoft Marketplace and the Teams store. Three separate objects get three separate reviews: the **Teams app** (Microsoft 365 and Copilot program, which also covers Office add-ins and Copilot agents), the **SaaS offer** (marketplace offer), and the **co-sell solution** (collateral on that offer). Most failed plans confuse them.

## Facts that break common plans

- **Teams apps never earn co-sell.** Microsoft excludes apps and add-ins for Teams, Outlook and Excel from co-sell-ready status. The SaaS offer linked to the app stays eligible: co-sell and MACC run on the offer.
- **Non-Azure SaaS lists only with a Microsoft integration.** An offer not primarily platformed on Azure must integrate with or extend a Microsoft product, say how in the description, and accept Entra SSO; it is not purchasable in the Azure portal. A linked Teams app usually meets the integration test; confirm in certification notes. "Primarily" means the Azure-hosted compute or data plane grows fastest with usage.
- **Only transact counts.** Contact me, listing-only trials, Get It Now (Free) and BYOL unlock no MACC, no IP co-sell, no private offers; any live SaaS offer can still reach co-sell ready.
- **MACC needs Azure IP co-sell eligible:** solution type IP, primarily on Azure with technical validation, reference architecture diagram, "Sell through Microsoft", and $100,000 Azure consumed revenue (trailing 12 months) or $100,000 billed through the offer†. A $1M+ MACC customer route is in pilot†. MACC counts per offer and only for usage running in Azure.
- **Co-sell ready is visibility, not pipeline.** It lists the solution in internal seller catalogs. Microsoft's marketplace blog calls it a starting line; practitioners report months before any seller engagement.
- **Program names moved.** AppSource and Azure Marketplace are one Microsoft Marketplace. Frontier Accelerate for Marketplace absorbed ISV Success, Marketplace Rewards and Azure IP co-sell; its FAQ makes enrollment (no-cost tier exists) a prerequisite for any co-sell listing, while the co-sell requirements page names it only for Business Applications†. The Qualified Referral Program is retired; referrals live in Partner Center.

| Rationalization                             | Why it fails                                                                                                       |
| ------------------------------------------- | ------------------------------------------------------------------------------------------------------------------ |
| "List the Teams app, co-sell follows."      | Teams apps are excluded from co-sell. Publish a transactable SaaS offer and link the app to it.                    |
| "Flat rate now, Teams link later."          | The pricing model is fixed per offer, and a Teams link needs per user: a second offer, review and MACC enrollment. |
| "Co-sell ready, now we wait for referrals." | Sellers act on quota. Bring your own opportunities and lead with MACC drawdown once eligible.                      |

## Commitments you cannot undo

Locked once the SaaS offer or plan publishes:

- pricing model: flat rate or per user, same for every plan in the offer;
- plan ID;
- per-user seat minimum and maximum;
- metered dimension IDs and values;
- a public plan going private;
- standard contract versus your own terms.

Decide the Teams question before the first publish: metering exists only on flat-rate plans, and Teams-linked offers must be per user. Build transact from day one, or confirm with Partner Center support first: Microsoft pages disagree on whether a published SaaS offer can switch from listing-only to transact.

## Interview

Ask one question at a time; skip what the request answers. When you cannot ask, state an assumption per gap and flag it:

1. What do customers run with you inside Microsoft 365: nothing, a Teams app, an Outlook or Office add-in, a Copilot agent? This gates the pricing model.
2. Where is the SaaS hosted: primarily Azure, hybrid, another cloud? Does it integrate with a Microsoft product?
3. Pricing: per user, flat with usage overage, enterprise contracts? Do buyers hold Azure commitments (MACC)?
4. Stage: no Partner Center account, building, in validation, live, co-sell submitted?
5. Target date for a first Marketplace transaction, engineering weeks, and whether a partner manager or sales lead will own Microsoft seller outreach.

Re-rank the menu below against answers 2, 3 and 5, and say which answer moved which option. A hard date promotes the Teams app and private offers; a compounding enterprise mandate promotes IP co-sell.

## Choose the path

Efficiency (pipeline unlocked per engineering week): transact SaaS + private offers > + Teams app linked > + Azure IP co-sell > Teams app alone > Contact me. Rows starting with + build on the row above.

| Path                           | You do                                                                              | You get                                                     |
| ------------------------------ | ----------------------------------------------------------------------------------- | ----------------------------------------------------------- |
| Transact SaaS + private offers | landing page, Fulfillment API v2, webhook, Entra SSO; first deals as private offers | Microsoft billing, enterprise procurement path, 3% fee†     |
| + Teams app linked             | Teams validation, attestation, `subscriptionOffer`, per-user plans                  | in-Teams discovery and "Buy a subscription", admin bulk buy |
| + Azure IP co-sell eligible    | Azure platforming, $100K threshold, architecture diagram                            | MACC drawdown, co-sell referrals, seller incentive          |
| Teams app alone (free)         | Teams validation and attestation                                                    | distribution and usage data, no money, no co-sell           |
| Contact me                     | listing copy                                                                        | leads you chase yourself                                    |

- **Default rung:** transact SaaS with private offers. Add the Teams app when answer 1 names Teams; add IP co-sell when answer 2 says Azure and answer 3 names MACC buyers.
- **Starved option:** Microsoft 365 Certification, a yearly third-party audit with pen test. Expensive and slow, it pays only when regulated buyers' security reviews stall deals. Take it when one does.
- **Another cloud (answer 2):** delete IP co-sell unless an Azure migration is already decided, and stop at co-sell ready, which costs days of collateral. With no Microsoft integration, delete the SaaS offer too: ship the Teams app first, or skip Microsoft Marketplace.

## Ship the SaaS offer

1. Create the Partner Center account in the AI Cloud Partner Program; validate tax profile (up to 48 h) before the payout profile.
2. Register a multitenant Entra app accepting work and personal Microsoft accounts; mint API tokens with the tenant and app IDs entered in Technical configuration. Request only `User.Read` during activation; ask for more after.
3. Build the landing page: always up, no `#` in the URL, no secrets shown, no downloads. Resolve the purchase token (valid 24 hours), then activate; the customer is not billed until activation succeeds, unless the plan uses auto activation.
4. Validate every webhook call through the Get Operation API before acting on it. Answer plan and seat changes within 10 seconds, or they are accepted automatically. Send metering hourly per resource and dimension; events older than 24 hours are rejected.
5. Write the Notes for certification: test accounts without MFA or developer interaction, purchase-to-activation steps. Missing notes are a top failure.
6. Test on a separate DEV offer in preview at a nominal price, and never press Go live on it: test purchases are invoiced, refunded only when cancelled within 72 hours†. Publish the real offer to a preview audience, then Go live.

## Pass Teams validation

Read [references/submission-packet.md](references/submission-packet.md) before the first submission. Office add-ins and Copilot agents follow their own Microsoft 365 submission guides; only the Partner Center listing, verification and attestation steps below carry over.

1. Complete Publisher Verification first: it is Must fix.
2. Validate the package in the Teams Developer Portal; test desktop, web and mobile.
3. Submit. A validation report targets 24 working hours; issues come back as Must fix, Good-to-fix, Blocker or Query from the concierge email. Fix, reply, wait for confirmation, resubmit. Budget three to six weeks†, not one day. Office add-ins: 3-4 business days per round, four to six weeks end to end†.
4. Complete Publisher Attestation the day the app goes live: it is a post-listing duty, not a listing gate, since a new app cannot attest before. Renew it yearly; an already listed app attests before each update.
5. Linking needs a live SaaS offer. Submit the Teams app in parallel with the offer build, then add `subscriptionOffer` once the offer is live: that update goes through validation again.
6. Any manifest, screenshot or Partner Center change re-enters validation; web-service-only changes do not.

## Sell through private offers

1. Take every first deal as a private offer: enterprise buyers procure that way.
2. Tick the renewal attestation when creating a private offer for a renewal, a migrated off-marketplace contract or an upsell to an existing customer: the fee halves† for the whole term. It cannot be added after creation. An offer created before October 2024 never qualifies: the customer stops auto-renew and accepts a new attested offer.
3. Use multiparty private offers when a reseller owns the relationship (one channel partner per offer). CSP private offers never count toward MACC.

## Reach co-sell

1. Enroll in Frontier Accelerate for Marketplace.
2. On Co-sell > Solutions: one-pager and pitch deck (Microsoft templates), reference architecture diagram (SaaS), the Microsoft platforms you build on or integrate with, a sales contact per geography. Expect a few weeks of review.
3. Register your own opportunities in Partner Center referrals against Microsoft-managed accounts (unmanaged ones never qualify for IP co-sell registration); map target accounts to Microsoft account executives and pitch MACC drawdown once eligible.
4. After IP co-sell eligibility, check the offer shows MACC "Enrolled" within about a week†.

## Output

Key the answer on stage. A single factual question gets a direct answer plus the rows it touches. A plan check, **No account** and **Building** get all of:

1. Assumptions, one line per missing interview answer.
2. Path from the menu, with the interview answer behind it.
3. Locked-choice register: pricing model, plan IDs, seat limits, dimensions, contract terms; owner and decision date each, written `unassigned` and raised as a question when unknown.
4. Submission plan: Teams validation items, SaaS certification notes, attestation date.
5. Co-sell plan: status targeted, threshold gap, collateral owner, first seller accounts.
6. Timeline backward from the target date, or forward from today when only a start date exists, one failed validation cycle included.

Mark every Microsoft figure (fees, thresholds, durations, prices) with `†`: verify in Partner Center before quoting it, since Microsoft renames programs and moves criteria yearly.

## References

- samber/developer-platform-skills@integration-listing-optimization - listing copy, screenshots, search rank, reviews.
- samber/developer-platform-skills@integration-partnership-strategy - whether Microsoft is worth the effort against other platform partners.
- samber/developer-platform-skills@salesforce-appexchange-playbook - the AppExchange equivalent.
- samber/developer-platform-skills@slack-app-directory-playbook - the Slack Marketplace equivalent for chat apps.
- samber/developer-platform-skills@aws-marketplace-playbook - AWS listings and co-sell, when the SaaS runs on AWS.
- samber/developer-platform-skills@oauth2-provider-design - OAuth behaviour behind your Entra app and APIs.
