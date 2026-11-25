---
name: aws-marketplace-playbook
description: "Takes a B2B SaaS vendor onto AWS Marketplace as the ISV seller - whether to list, irreversible account and pricing model choices, going public, private offers, CPPO resale authorizations, EDP/PPA commit drawdown, and co-selling through ACE and ISV Accelerate. Use whenever a vendor mentions AWS Marketplace, a private offer, CPPO, burning a customer's AWS commit, the Deployed on AWS badge, or ACE, ISV Accelerate or FTR for its listing, even if they only ask how to sell through AWS. ISV side only: not buyers, not resellers. Do NOT use for listing copy or search rank (use samber/developer-platform-skills@integration-listing-optimization), for your own marketplace's billing (use samber/developer-platform-skills@app-marketplace-monetization-model), or for metering code."
license: MIT
metadata:
  author: Samuel Berthe
  version: "1.0.0"
---

# AWS Marketplace playbook

You take a SaaS product onto AWS Marketplace as the ISV seller. The listing is a procurement rail, not a demand channel: revenue comes from private offers to buyers who already spend on AWS.

## Commitments you cannot undo

- **Seller account**: the AWS account you register becomes seller of record and cannot change once a product is listed. Use a fresh standalone account, or an organization whose accounts all share your legal entity: with tax inheritance, a member account takes the management account's legal entity.
- **SaaS pricing model** (subscription, contract, contract with consumption, free) is fixed once the product is published to Limited. The wrong model means a new product.
- **Dimension API names** never change; custom dimensions added for offers cannot be removed.
- **Public price increases** freeze every further pricing update for at least 90 days† and reach existing subscribers only after AWS notifies them. Lower prices first, then raise.
- **Selling authorizations** to resellers cannot be edited or extended once published; only deactivated.
- **Seller opt-out of an auto-renewal** cannot be reversed; the buyer then needs a new offer.
- **Accepted offer terms**: signed payment schedules and net terms are frozen. Changing them takes a replacement offer the buyer must accept.

| Rationalization                                          | Why it fails                                                                                                                                                       |
| -------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| "Register with our main production account."             | It becomes seller of record forever and mixes Marketplace finance with infrastructure billing.                                                                     |
| "Start with pay-as-you-go, switch to contracts later."   | SaaS pricing models never switch. Pick the model your sales team actually closes.                                                                                  |
| "List it and AWS buyers will find us."                   | Public listings draw little inbound. Plan for private offers on deals you source.                                                                                  |
| "Buyers can burn their AWS commit with us."              | Only products holding the Deployed on AWS badge may still count, inside a share set in each buyer's private AWS contract. AWS must review your architecture first. |
| "We'll test with private offers on the Limited listing." | Your seller account needs at least one public listing priced above zero before any private offer. A first product cannot carry one while Limited.                  |

## Interview

Ask one question at a time; skip what the request answers. When you cannot ask, state an assumption per gap and flag it:

1. Where do the application plane, control plane and any third-party service touching customer data run: fully on AWS, partly, elsewhere?
2. Who buys: enterprise accounts with an AWS commitment, mid-market on card, self-serve?
3. How do you sell today: annual or multi-year contracts, seats or tiers, usage, overage? Typical deal size?
4. Stage: not registered, registered, integrating, Limited, Public, first offer sent, co-selling? Any other public paid product?
5. Any reseller or distributor a buyer insists on? Company country and buyer countries?
6. Target date for the first Marketplace deal, engineering weeks available, owner for offers.

Re-rank the menus below against answers 1, 2 and 6, and say which answer moved which option.

## Fit verdict first

| Verdict                  | When                                                                                         | Do differently                                                                                                |
| ------------------------ | -------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------- |
| **Transact with commit** | Answer 1 fully on AWS, answer 2 enterprise buyers holding AWS commitments                    | Earn the badge before the first offer; sell "burn your commit" with the buyer's AWS team confirming           |
| **Transact, no commit**  | Off-AWS hosting, or buyers wanting AWS billing for vendor consolidation or procurement speed | No commit language in decks or offers; pitch one invoice and pre-approved terms; weigh a fully-on-AWS edition |
| **Skip for now**         | Self-serve or card buyers, no AWS-committed accounts in the pipeline, no one to own offers   | Revisit when a named deal asks for it                                                                         |

## Choose the listing type and pricing model

Default rung: **SaaS contract** (public terms of 1, 12, 24 or 36 months†; custom lengths in private offers), because it maps to enterprise contracts and private offers. Move to contract with consumption when overage is part of your price book; to subscription only when the product is billed purely by metered usage.

| Model                          | Fits                                                                                   | Your product must                           |
| ------------------------------ | -------------------------------------------------------------------------------------- | ------------------------------------------- |
| SaaS contract                  | annual or multi-year seats, tiers; installments and auto-renewal need a contract model | check entitlements on every customer change |
| SaaS contract with consumption | commit plus overage                                                                    | check entitlements and meter overage hourly |
| SaaS subscription              | pure usage, monthly bills                                                              | meter every customer every hour             |
| SaaS free                      | lead capture                                                                           | all dimensions at zero                      |

- Every SaaS model supports a Marketplace free trial (7-90 days†); trials hosted off Marketplace may not be advertised.
- Bill everything through listed dimensions: no card capture, no links to other clouds.
- AMI, container and ML listings run in the buyer's account and pay a 20% public fee†. This skill treats them only as bring-your-own-license add-ons to a SaaS listing; their packaging and scanning rules sit in AWS's seller guide.
- Professional services list separately and pair well with a SaaS private offer.

## Path to the first deal

Run registration and engineering in parallel; the slowest step is rarely AWS review.

1. Create the seller account, then register: tax interview, bank account, a USD disbursement method (mandatory outside India), bank verification, and KYC when you sell into EMEA or use a UK bank. Practitioners report up to two weeks for KYC; editing details after approval restarts it.
2. Build the integration and test it against the review list in [references/private-offer-desk.md](references/private-offer-desk.md).
3. Publish to **Limited** at a reduced test price, allowlist test accounts, cancel every test subscription.
4. Request **Public** with the real price: Seller Operations reviews in 7-10 business days† from the request, longer on errors. Plan 3-6 weeks† from registration to Public. For a first product, no private offer goes out before this step passes.
5. Submit the architecture diagram for the Deployed on AWS badge when answer 1 qualifies. Link your AWS Partner Central and AWS Marketplace seller accounts, so offers attach to co-sell opportunities.
6. Send the first private offer to a deal already late-stage outside Marketplace, after the buyer pre-check in the reference.

When a renewal date falls before Public can realistically pass, extend the customer briefly on your own paper; at the next renewal, set the renewal flag below. Never promise a Marketplace signature date earlier than review allows.

## Private offers

- Keep the public price at list and discount in private offers. To show no public price at all, use the Request private offer button (a preview feature†): it needs ACE eligibility, linked Partner Central and seller accounts, a contract-based listing and zero active subscriptions, test ones included.
- Flag existing customers moving their renewal onto Marketplace as **Existing Customer Moving to AWS Marketplace**: renewals pay 1.5%† instead of 3%†. Set the same renewal flag on a reseller's selling authorization.
- Re-include unbilled installments when replacing an agreement: the replacement cancels the old pending payments.
- For a buyer's chosen reseller, issue a CPPO selling authorization with a wholesale price. The extra 0.5%† fee comes out of your payout, computed on the wholesale price: price it into the partner discount. The reseller becomes seller of record for that deal's refunds and cancellations.

Expiry, installments, net terms, future-dated renewals, geo-targeting, Private Marketplace approval and acceptance blockers live in [references/private-offer-desk.md](references/private-offer-desk.md). Read it before drafting any offer.

## Co-sell with AWS

Ranked by deals unblocked per hour of effort: answer AWS-referred opportunities within 5 business days > submit your own opportunities to ACE with real AWS consumption > Foundational Technical Review (FTR) > ISV Accelerate > promotion credits on a closing deal.

| Rung                      | You get                                                                     | You owe                                                                                                                                                                                |
| ------------------------- | --------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| ACE opportunities         | AWS sees and validates your deal                                            | net-new AWS usage; "for visibility only" entries count toward no threshold                                                                                                             |
| FTR                       | Validated status                                                            | an architecture and security review, roughly 2-4 weeks                                                                                                                                 |
| ISV Accelerate            | AWS account managers paid incentives on your private offers; funding access | GA listing, Validated status, Payee Central account, 5 launched and 15 qualified opportunities in 12 months, one trained seller, $2,000† AWS revenue; AWS invites you once you qualify |
| Promotion credits (MPOPP) | AWS credits to the buyer after acceptance                                   | a request to your AWS partner team before the buyer accepts†                                                                                                                           |

- Default rung: ACE from the first deal. ISV Accelerate arrives by invitation once the pipeline already meets the thresholds; never plan around applying early.
- AWS sellers do not prospect for an unknown ISV. Expect field engagement 6-12 months after listing.

## Money and the sales team

- Fees†, on pre-tax total contract value whatever the payment schedule: 3% SaaS public; new private offers 3% under $1M, 2% to $10M, 1.5% above; every renewal 1.5% at any size; CPPO +0.5%; South Korea buyers +1%; professional services 0.5%, 0% inside a qualifying multi-product offer set.
- AWS invoices the buyer and, where marketplace-facilitator law applies, collects and remits the tax. Finance tracks the order without sending its own customer invoice.
- AWS pays only after it collects, daily or monthly, so net terms move your cash by the same days; a buyer who never pays delays you, not AWS.
- Pay reps the same commission and quota credit as direct, on acceptance. A fee deducted from commission routes deals around Marketplace.
- Never inflate the public price to recover the fee.

## Output

Key the answer on the stage. A single question gets a direct answer plus the rows it touches. A full plan contains:

1. Assumptions, one line per missing interview answer.
2. Fit verdict with the answer behind it.
3. Irreversible-choice register: seller account, pricing model, dimensions, reseller authorizations; owner and date each.
4. Timeline to the first deal, counted forward from today.
5. First-offer plan: buyer pre-check, fee tier, renewal flag, payment terms.
6. Co-sell rung for this quarter and the condition that moves up a rung.

Mark every AWS figure (fees, durations, thresholds) with `†` and a footnote: verify against the current AWS Marketplace Seller Guide before quoting it.

## References

- samber/developer-platform-skills@integration-listing-optimization - listing copy, media, search rank, reviews.
- samber/developer-platform-skills@integration-partnership-strategy - whether AWS is the right partner to invest in.
- samber/developer-platform-skills@salesforce-appexchange-playbook - the same job on Salesforce.
