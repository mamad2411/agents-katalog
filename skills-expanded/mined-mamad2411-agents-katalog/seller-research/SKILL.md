---
name: seller-research
description: Use when researching a merchant, storefront, marketplace seller, or merchant of record for a buying decision, especially when identity, refund terms, fulfillment, counterfeit risk, domain history, or independent buyer outcomes are uncertain.
---

# Seller research

Treat a seller conclusion as evidence about one exact storefront and merchant of record, not its platform, catalog, or product quality. Keep a seller result visibly provisional when identity or required evidence is missing. Seller legitimacy and platform reputation are not product-quality evidence and must never be converted into a product score.

Construct one exact research `subjectIdentity` before claims: storefront name, full domain or exact marketplace storefront, merchant of record (or `unknown`), and buyer geography (or `unknown`). Copy that string byte-for-byte into both `subjectIdentity` and `sellerIdentity` on every claim. A dissolved entity, lookalike business, platform, or direct-store alternative belongs in context or counterevidence; it never becomes the claim subject identity.

## Claim construction recipe

Build one complete internal source ledger before **Claims**: for every supplied or read `sourceId`, record its controller, one `sourceRelationship`, and intended `sourceUse`. A record's `ownership` field names that controller; it does not select the `owner` relationship enum. Build **Claims** by iterating one relationship bucket at a time. Each claim cites one source or multiple sources only from that same bucket. End **Claims** after those atomic bucket records. Put every cross-relationship synthesis in conflicts, unknowns, the counterevidence receipt, or the stop receipt. A summary or identity conclusion is not an additional claim record: its evidence stays in the separate atomic records plus one conflict object.

### Required pre-output audit

The Claims array is valid only when every record maps each `sourceId` through the complete ledger to a relationship set of size exactly `1` and has the constructed `subjectIdentity` byte-for-byte. Emit no structured JSON until that audit passes. The array ends with atomic ledger records; synthesis or summary appears only in conflicts, unknowns, or receipts. A commercial source with `subject_evidence` is invalid: route storefront promotional content to `commercial_claim`, route unresolved creator-compensation or no-publisher-found records through their `unknown` ledger entry, and put registry or legal facts in separate primary `subject_evidence` claims.

## Required research contract

Resolve the exact storefront before binding a seller claim: storefront name, full URL and domain, marketplace storefront or shop ID when applicable, merchant-of-record legal name, payment recipient if shown, sale geography, and the observation date. Record uncertainty rather than transferring evidence from a lookalike business, a similarly named seller, another marketplace shop, or the platform itself.

Use this source ladder in order. A lower rung can corroborate or suggest a lead, but cannot silently replace a blocked higher rung.

1. Merchant legal/business identity, marketplace seller identity, registration where accessible, and merchant-of-record/payment disclosures.
2. Official storefront policy text for returns, warranty, fulfillment, contacts, and terms; capture the effective date and sale geography.
3. Payment, fulfillment, inventory, and contactability facts: checkout identity, delivery promise, carrier/warehouse details, reachable support channels, and response evidence where available.
4. Disinterested domain/business records and independently operated reporting for domain age, identity consistency, enforcement history, and ownership context.
5. Independent buyer outcomes that identify the exact seller and geography, with date, transaction context, and recurring pattern separated from a single anecdote.
6. Seller testimonials, marketplace-wide ratings, creator/affiliate content, copied catalog text, and social posts only as quarantined claims.

Classify source relationship from evidence, not its headline or a supplied record's `ownership` controller label. `sourceRelationship` describes who produced or controls the source, not whether its finding is positive or conclusive. Inspect disclosure, outbound links or codes, commission/creator compensation, seller/platform control, testimonial ownership, copied wording, review solicitation, and the source's exact seller identity:

- **Primary:** authoritative merchant-of-record, official seller/direct-store policy, business-registry, or domain record.
- **Independent:** evidenced disinterested exact-seller buyer outcome, comparison, or verification/search record; retain its date and geography where applicable.
- **Owner:** an actual exact-seller buyer-owner report only when that is the source relationship; a seller, platform, manufacturer, marketplace, or record controller label is never `owner`.
- **Commercial:** evidenced affiliate, paid creator, seller, platform, promotional, sponsored, testimonial, or copied-catalog material.
- **Unknown:** source control or relationship is unresolved, including a creator/social source with no compensation disclosure or a no-publisher/source-found outcome search.

Make the internal source ledger as one `sourceId → controller, sourceRelationship, sourceUse` entry for every supplied or read source. Seller-controlled branding, promotion, and testimonials are `commercial`; an official checkout disclosure that names the legal merchant or payment recipient and an official seller/direct-store policy fact are `primary`; business, domain, and address records are `primary`; an evidenced disinterested exact-seller outcome or comparison is `independent`; a creator/social source with unresolved compensation and a no-publisher/source-found outcome search are `unknown`. A seller storefront's bare card checkout or missing legal merchant-of-record disclosure is `commercial` with `commercial_claim`, not primary `subject_evidence`. A false-positive-only record, including a virtual-office caution, is `context_only` or `counterevidence`, never `subject_evidence` about the seller.

Separate a marketplace's buyer-protection program and platform rating from the storefront's evidence. They may describe platform recourse, but do not establish the seller's identity, fulfillment, authenticity, or refund performance.

For each exact seller, answer separately: who is merchant of record; who handles returns; return window; opened-item eligibility; restocking cost; return shipping; damaged/misdescribed-item remedy; warranty issuer and claim route; fulfillment location and promised delivery; support address/phone/email/contact form; domain age/history; and dated buyer outcomes in the buyer's geography.

Run a bounded pass: at most 8 focused queries and 12 source reads per storefront, unless the buyer authorizes more. Reserve two queries and two source reads for counterevidence. Stop expanding when the budget is exhausted and issue the applicable receipt.

Use focused query recipes, replacing bracketed terms with the exact storefront identity:

- `"[storefront name]" "[domain]" merchant of record OR legal name`
- `site:[domain] return OR refund OR restocking OR warranty OR shipping`
- `"[storefront name]" "[domain]" reviews OR complaint OR return OR delivery`
- `"[domain]" domain history OR registration OR business address`
- `"[storefront name]" counterfeit OR dropship OR copied catalog OR scam`
- `"[storefront name]" "[buyer geography]" return OR delivery OR support`

Search counterevidence even when the first pass looks legitimate or suspicious. For a suspicious impression, seek a benign explanation such as a new lawful business, a changed fulfillment partner, regional policy difference, legitimate liquidation, or an unrelated same-name business. For a favorable impression, seek the most consequential plausible downside: failed returns, delayed delivery, counterfeit or misdescribed goods, unreachable support, or conflicting merchant identity. Record the found counter-source or an honestly unresolved search. Every source actually used for a downside, benign alternative, or distinct-merchant recourse comparison belongs in `counterevidenceSourceIds`.

## Red flags with false-positive cautions

Treat these as leads requiring corroboration, not proof: copied catalog images/text; implausibly low prices; countdown or stock urgency; counterfeit or dropship signals; conflicting legal/address/contact identities; policy text that names another business; recently created or rapidly changed domains; and seller testimonials that lack transaction detail.

A new/private domain, virtual office, overseas fulfillment, a low price, template policy, or a marketplace storefront is not alone proof of fraud, counterfeiting, dropshipping, or bad faith. A record supplied only for that false-positive caution is context or counterevidence, not proof about the seller. Verify the exact merchant, date, geography, and alternative explanation before assigning a conclusion.

## Checklist

- [ ] `seller.identity` — Resolve the exact storefront, merchant of record, payment recipient where shown, sale geography, and observation date.
- [ ] `seller.platform-separation` — Separate marketplace-wide reputation/protection from evidence about this individual storefront and merchant.
- [ ] `seller.policies` — Decompose return window, opened-item eligibility, restocking, return shipping, damage remedy, warranty issuer, and warranty claim route.
- [ ] `seller.fulfillment-contact` — Verify fulfillment location/promise and reachable support identity, address, phone, email, or contact route.
- [ ] `seller.domain-business-records` — Check disinterested domain and business records for age, history, ownership, and identity consistency.
- [ ] `seller.independent-outcomes` — Seek dated, geography-preserving independent buyer outcomes tied to the exact seller.
- [ ] `seller.commercial-claims` — Quarantine seller testimonials, marketplace-wide ratings, affiliate/creator material, and copied catalog claims with their relationship.
- [ ] `seller.red-flags` — Investigate copied catalogs, implausible price, urgency, counterfeit/dropship indicators, and conflicting identities with false-positive cautions.
- [ ] `seller.counterevidence` — Complete the reserved contrary-evidence search and record a material downside, benign explanation, or unresolved result.
- [ ] `seller.unknowns` — Maintain an explicit conflict and unknown ledger for decision-relevant gaps, including geography and recency limits.
- [ ] `seller.stop-receipt` — State completion or the observable stop condition, remaining markers, source/read counts, and next decisive evidence.

## Claim record and output

For every material seller fact, emit a claim object in this shape. `checklistIds` contains the applicable stable checklist markers. Bind `seller.independent-outcomes` only to a dated buyer outcome whose independence and exact seller/geography are evidenced. Bind each commercial or commercial/unknown claim to `seller.commercial-claims` and any genuinely applicable non-independent marker; this keeps commercial evidence in its own evidence lane.

`sourceRelationship` records the ledger bucket for the claim. A seller-controlled storefront promotion or missing-disclosure observation is a `commercial_claim`; a separate checkout disclosure that names a legal merchant or payment recipient can be a primary `subject_evidence` claim. Keep `sourceUrl` and `sourceType` for normal delivery; add the source-ID fields below for structured research delivery.

Use these exact enums:

- `sourceRelationship`: `primary`, `independent`, `owner`, `commercial`, or `unknown`, using the definitions above.
- `sourceUse`: `subject_evidence` for exact-seller factual support; `counterevidence` for a material downside or benign alternative; `commercial_claim` for a seller/platform/affiliate assertion; `context_only` for a lookalike, different merchant, or different geography.

Every `conflicts` entry is an object with a `description` and every relevant `sourceIds`. A material disagreement between an official seller policy and an exact-seller buyer outcome gets one conflict object containing both IDs. A no-outcome search with no publisher/source found is `unknown`; if it was used to test an initial impression, it is counterevidence and appears in `counterevidenceSourceIds`.

```json
{
  "lane": "seller",
  "checklistIds": ["seller.identity", "seller.policies"],
  "sellerIdentity": "Storefront name — https://store.example — merchant of record: Example Trading Ltd — buyer geography: US",
  "subjectIdentity": "Storefront name — https://store.example — merchant of record: Example Trading Ltd — buyer geography: US",
  "claim": "The return policy allows unopened goods within 30 days and requires buyer-paid return shipping.",
  "sourceIds": ["store-return-policy"],
  "sourceRelationship": "primary",
  "sourceUse": "subject_evidence",
  "sourceUrl": "https://store.example/returns",
  "sourceType": "official seller return policy",
  "observedAt": "2026-08-19T12:00:00Z",
  "confidence": "high",
  "conflicts": [],
  "unknowns": []
}
```

Return, in order: resolved seller identity; platform-versus-seller separation; **Claims** as one JSON array of claim objects; policy and fulfillment answers; independent buyer outcomes; quarantined commercial claims; red flags and counterevidence; conflict/unknown ledger; sources searched; and a completion or stop receipt. Populate every material claim in that array with every field in the shape above. Then emit one structured research receipt with the exact research `subjectIdentity`, `checklistItemIds` listing every canonical seller marker considered (open or satisfied), `counterevidenceSourceIds` listing every source actually used for a downside, benign alternative, or distinct-merchant recourse comparison, and `provisional`. Do not score product quality, and do not recommend a seller as verified while a required stop condition applies.

## Stop conditions

Stop and mark the result **provisional** when any observable condition applies:

- missing identity: storefront, merchant of record, payment recipient where shown, or applicable sale geography cannot be resolved;
- blocked access: a consequential identity, policy, payment, or fulfillment source cannot be read or verified;
- jurisdiction mismatch: the available policy/outcome evidence is for a different buyer geography or the applicable terms cannot be identified;
- conflicting merchant-of-record evidence: reliable sources name incompatible legal sellers, payment recipients, or return/warranty entities;
- insufficient evidence: the bounded pass ends with a decision-relevant unknown, unresolved conflict, or no usable independent buyer outcome where seller risk is consequential.

Name the condition, remaining checklist markers, query/read counts, and one next evidence item that could change the result. A seller testimonial, platform-wide rating, or affiliate assertion cannot clear a stop condition alone.

## Worked provisional example

Buyer: "Can I safely buy the fictional Norvale Audio X1 from BrightSound Outlet for delivery to Canada? I care about returns and warranty. Do not assess the headphones' quality."

Research seller identity: **BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada**. MarketplaceHub's buyer-protection page is platform evidence only, not evidence about BrightSound Outlet.

Internal source ledger: `brightsound-storefront → commercial`; `brightsound-registry → primary`; `brightsound-returns → primary`; `consumer-forum-complaint → independent`; `brightsound-lookalike-registry → primary`.

```json
[
  {
    "lane": "seller",
    "checklistIds": ["seller.identity", "seller.policies", "seller.unknowns"],
    "sellerIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "subjectIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "claim": "The storefront return page says unopened items may be returned within 14 days, but does not identify the legal return recipient, return-shipping payer, restocking cost, or warranty issuer.",
    "sourceIds": ["brightsound-returns"],
    "sourceRelationship": "primary",
    "sourceUse": "subject_evidence",
    "sourceUrl": "https://brightsound.example.test/ca/returns",
    "sourceType": "official storefront policy",
    "observedAt": "2026-08-19T12:00:00Z",
    "confidence": "medium",
    "conflicts": [],
    "unknowns": ["Merchant of record and warranty responsibility are not disclosed."]
  },
  {
    "lane": "seller",
    "checklistIds": ["seller.independent-outcomes", "seller.counterevidence", "seller.unknowns"],
    "sellerIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "subjectIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "claim": "A Canadian buyer complaint dated 2026-07 reports an unanswered return request; the outcome is one transaction, not a general fulfillment rate.",
    "sourceIds": ["consumer-forum-complaint"],
    "sourceRelationship": "independent",
    "sourceUse": "counterevidence",
    "sourceUrl": "https://consumer-forum.example.test/posts/brightsound-return-july-2026",
    "sourceType": "independent buyer outcome",
    "observedAt": "2026-08-19T12:05:00Z",
    "confidence": "low",
    "conflicts": [{"description": "The return policy offers a 14-day return window, while the dated buyer outcome reports an unanswered return request; practical return access is unresolved.", "sourceIds": ["brightsound-returns", "consumer-forum-complaint"]}],
    "unknowns": ["No independent pattern was found within the remaining budget."]
  },
  {
    "lane": "seller",
    "checklistIds": ["seller.commercial-claims"],
    "sellerIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "subjectIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "claim": "The seller-controlled storefront branding and testimonial carousel say buyers received authentic goods quickly, but do not disclose a legal merchant or independent collection method.",
    "sourceIds": ["brightsound-storefront"],
    "sourceRelationship": "commercial",
    "sourceUse": "commercial_claim",
    "sourceUrl": "https://brightsound.example.test/ca",
    "sourceType": "seller-authored testimonial",
    "observedAt": "2026-08-19T12:07:00Z",
    "confidence": "unverified",
    "conflicts": [],
    "unknowns": ["The storefront does not identify a legal merchant, and testimonials identify neither transactions nor independent collection method."]
  },
  {
    "lane": "seller",
    "checklistIds": ["seller.identity", "seller.counterevidence", "seller.unknowns"],
    "sellerIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "subjectIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "claim": "A UK registry record for BrightSound Electronics Ltd. names a different merchant and geography; it is a same-name benign alternative, not evidence about BrightSound Outlet.",
    "sourceIds": ["brightsound-lookalike-registry"],
    "sourceRelationship": "primary",
    "sourceUse": "context_only",
    "sourceUrl": "https://registry.example.test/uk/brightsound-electronics-ltd",
    "sourceType": "business registry record for a different merchant",
    "observedAt": "2026-08-19T12:09:00Z",
    "confidence": "high",
    "conflicts": [],
    "unknowns": ["No ownership link between the two similarly named businesses was found."]
  },
  {
    "lane": "seller",
    "checklistIds": ["seller.identity", "seller.domain-business-records", "seller.unknowns"],
    "sellerIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "subjectIdentity": "BrightSound Outlet — https://brightsound.example.test/ca — merchant of record: unknown — buyer geography: Canada",
    "claim": "The Canadian business registry does not identify a legal merchant matching BrightSound Outlet.",
    "sourceIds": ["brightsound-registry"],
    "sourceRelationship": "primary",
    "sourceUse": "subject_evidence",
    "sourceUrl": "https://registry.example.test/ca/brightsound-outlet",
    "sourceType": "Canadian business registry search",
    "observedAt": "2026-08-19T12:10:00Z",
    "confidence": "medium",
    "conflicts": [{"description": "The seller-controlled storefront presents BrightSound Outlet without a legal merchant disclosure, while the registry does not identify a matching legal merchant; merchant of record remains unresolved.", "sourceIds": ["brightsound-storefront", "brightsound-registry"]}],
    "unknowns": ["A current legal merchant and payment recipient have not been identified."]
  }
]
```

Quarantined commercial claims: the testimonial carousel is seller-controlled and does not corroborate authenticity, delivery, or returns. A low launch price and a recently registered domain are red-flag leads, not proof; a possible benign explanation is a newly opened authorized-liquidation business, but no merchant identity or authorization evidence was found.

Unknown ledger: merchant of record, payment recipient, Canadian return recipient, return-shipping/restocking terms, warranty issuer, and a recurring independent-outcome pattern. Sources searched: 8 queries, 12 reads, including 2 counterevidence queries and 2 reads.

```json
{
  "checklistItemIds": ["seller.identity", "seller.platform-separation", "seller.policies", "seller.fulfillment-contact", "seller.domain-business-records", "seller.independent-outcomes", "seller.commercial-claims", "seller.red-flags", "seller.counterevidence", "seller.unknowns", "seller.stop-receipt"],
  "openChecklistItemIds": ["seller.identity", "seller.policies", "seller.independent-outcomes", "seller.unknowns", "seller.stop-receipt"],
  "provisional": true
}
```

Stop receipt: **provisional — missing identity and insufficient evidence**. Open work: resolve the merchant of record/payment recipient and obtain Canada-applicable return and warranty terms; then seek a dated independent buyer outcome tied to the exact storefront. Do not mark BrightSound Outlet verified or infer headphone quality from this seller research.
