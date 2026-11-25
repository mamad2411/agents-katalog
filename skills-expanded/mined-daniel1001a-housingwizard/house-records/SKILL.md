---
name: house-records
description: Public-record due diligence on a house a buyer is considering - violations, permits and certificates of occupancy, ownership and mortgage history, estate or life-estate signals, flood zone, zoning, complaints, and what the listing's own floor plan and photos reveal. Use when a buyer shares an address or listing link and asks "anything wrong with this house", "is this addition legal", "who owns it", "is it in a flood zone", "why is it priced like this", or before an offer, inspection or contract. Includes a free FEMA flood-zone script for any US address and a full New York City records script.
---

# House records: what the public record says

Public records are the only facts in a listing process that nobody is selling you. They are also easy to misread. This skill runs the lookups, then reads them with discipline.

<!-- shared:rules -->
## Ground rules (shared by every HousingWizard skill)

Each one guards against a common, expensive mistake. They apply to every answer.

1. **Tag where each fact came from.** Use `[record]` public record, `[document]` contract, report, disclosure or listing, `[seen]` observed on site by the buyer, `[seller said]` anything relayed from the seller or listing agent, `[estimate]` your arithmetic or market ranges, `[assumption]` a placeholder. Never promote a seller statement or an estimate to a fact.
2. **Zero rows is not clean.** An empty database result means the online dataset has nothing, not that nothing happened. Compare with neighbors before calling anything unusual.
3. **Give the honest counter-case.** For every red flag, first write the innocent explanation and the evidence for it, then why it still deserves a check, and how to check it.
4. **End with a human check.** Close every substantive answer with a short "Human check" list: what must be measured, seen, confirmed or decided by a person, by whom (buyer, inspector, attorney, lender, licensed trade), and what must not happen until it is done.
5. **You are not the buyer's lawyer, agent, inspector or lender.** Turn legal and licensing points into questions for the buyer's attorney, phrased as confirmations, not demands. Cost figures are ranges with a source, never quotes.
6. **Name the jurisdiction.** Say which state and city rules you are applying. If this skill has no reference file for the location, work in generic mode: do not state local rules as facts, ask for the local forms, and route the question to a local professional.
7. **Draft, never act.** Write messages, letters and checklists for the buyer to send or use. Do not send, sign, pay, accept terms, or fill forms on their behalf.
8. **Stop at walls.** At a CAPTCHA, login or paywall, stop and give the buyer the exact steps: URL, what to click, what to type, what to copy back.
9. **Keep the case file true.** Write new facts into the buyer's case file (see house-case-file). When a new fact overturns an old conclusion, change the conclusion and log what changed, instead of appending a note under a stale answer.
10. **Re-check anything time-sensitive.** Rates, taxes, fees, tariffs and code section numbers change. Quote them with the date you checked them, and re-check anything older than two weeks before relying on it.
<!-- /shared:rules -->

## Step 1: confirm the property

Get the full address and, if possible, the parcel ID. Address matching is fuzzy: the same street number can exist in two boroughs or towns. Both scripts below list matches and make you pick one; show the buyer the match and have them confirm it before reading anything. Also confirm the property is inside the jurisdiction you think (border towns differ in tax, schools, permits and records).

## Step 2: run what can be run

- **Any US address, flood zone:** `python3 scripts/us_flood.py "<address>"`, then `--pick N`. Uses the Census geocoder and FEMA's National Flood Hazard Layer, free, no key.
- **New York City:** `python3 scripts/nyc_records.py "<address>"`, then `--pick N`. PLUTO, DOB and ECB violations, HPD, DOB jobs in both systems, certificates of occupancy, DOB complaints, DOF assessment history, ACRIS documents, nearby 311. Read `references/nyc.md` before interpreting it.
- **Elsewhere in the US:** there is no single API. Use `references/generic-us.md` for the sources to check by hand (county assessor, recorder, building department permit portal, code enforcement) and ask the buyer to fetch pages that need a login or CAPTCHA.

If scripts cannot run in this environment (no Python or no network), give the buyer the exact queries or URLs to open instead.

## Step 3: read the listing as evidence

The listing's floor plan and photos are free evidence and often answer the most expensive question first. Read `references/listing-forensics.md`. Compare three areas: recorded building area, listing area, and what the floor plan adds up to. When they disagree, suspect unrecorded work.

## Step 4: interpret with discipline

1. **Zero rows is not clean.** It means the online dataset has nothing. Old permits and sign-offs may exist only on paper or microfilm.
2. **Baseline first.** Before calling something a red flag, check the same field for neighbors on the block. A second building on a lot, for example, may be a detached garage that every house on the street has.
3. **Every conclusion carries a source.** Mark inferences as inferences and give the way to verify each one (who to ask, what to order, what to measure).
4. **Honest counter-case first.** For each finding, write the innocent explanation before the worrying one.
5. **Watch for these patterns, they change strategy:**
   - Renovation mentioned in the listing but no matching permits.
   - Recorded area smaller than listing area.
   - Estate signals: one owner for decades, a senior or other exemption that disappears, a life-estate deed, a seller who is not the owner of record. An estate seller may be exempt from disclosure rules and unable to make repairs or warranties; holdbacks work better than repair promises.
   - Complaints unique to this house compared with neighbors.
   - Building age that triggers known hazards (see `references/age-risks.md`).

## Step 5: decide whether a deep dive is needed

A deep dive (legalization path, zoning math, cost of fixing unpermitted work) is worth it when any of these hold: pre-1960s house with additions, area mismatch, a second kitchen or separate entrance, septic or oil heat, shared driveway, estate signals, or the buyer is weighing a price stretch. Otherwise the checklist in Step 6 is enough.

## Step 6: output

A short report, conclusion first:

1. Verdict in one or two lines: what to worry about, what is fine, what is unknown.
2. Findings table: finding, source, innocent explanation, why it still matters, how to verify, who verifies.
3. Items the buyer must fetch by hand (with steps), and items for the inspector, attorney or surveyor.
4. Fatal-if-true list to resolve before signing: unresolved oil tank, unclear shared driveway rights, septic where sewer was assumed, no gas main where gas was assumed, legal use that does not match the listing, special flood hazard area.
5. Human check.

Write new facts into the case file.
