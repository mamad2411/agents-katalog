---
name: domain-name-advisor
description: Run a naming and acquisition-path consultation and present a small verified shortlist in either of two modes. Project mode turns vague or open-ended requirements into a generator-ready brief, delegates creative generation to domain-generator, and adds lifecycle inventory when appropriate. Taken-target mode extracts what the user values in an unavailable target, delegates creative variants to domain-generator, and searches dropped, expiring, for-sale, or brokered alternatives. Use when a user needs naming direction or recommendations across acquisition paths. Do not use for a simple availability check (use available / bulk_available), creative variations from an already-defined seed with no lifecycle comparison (use domain-generator), or analysis of a domain itself (use domain-analyze).
---

# Domain Name Advisor

**What this does:** consults on naming and presents a small verified shortlist, in one of two modes:

- **Project mode** (no target yet): briefly diagnose needs, prepare a generator-ready project brief, delegate all creative candidate work to domain-generator, and add lifecycle options when appropriate.
- **Taken-target mode** (a specific target is already taken): confirm the target is actually unavailable, extract what the user values in it, delegate all creative variant work to domain-generator, and search relevant lifecycle inventory without re-running an open naming consultation.

Both modes converge on the same cross-channel comparison and delivery. Most candidates are registrable names verified as available at check time; when the user accepts the relevant acquisition paths, the shortlist may also include already-registered candidates (expired / backorder or for-sale listings), which are verified by lifecycle and acquisition status, not as "available".

**Data interfaces it needs.** DomainKits MCP supplies part of the acquisition evidence through the tools below; host-provided web access supplies public-page verification. Equivalent providers are acceptable. Never assume an MCP result contains a field that is absent from its actual payload. Mark missing fields or capabilities `Unavailable` and continue.

- Availability check, DomainKits: `bulk_available`
- A TLD's standard registration and renewal price, DomainKits: `price`
- Premium status and a name's actual registration price: host web access to the registrar's own page
- Cross-TLD registration data (a lightweight crowding signal), DomainKits: `tld_check`
- Lifecycle inventory, DomainKits: `deleted`, `expired`, `market`, `aged` (how each is used is set out in workflow step 4)
- Web access for a lightweight public-web check on obvious brand collisions; for confirming a named broker before a brokered candidate is offered; and, optionally, for a past sale price only from a named verifiable sales record.

**Skill dependency:** use `domain-generator` as the sole creative-generation component. This advisor owns project or target diagnosis, generator handoff, lifecycle sourcing, cross-channel comparison, and final recommendation. Domain-generator owns the creative frame, semantic distances, naming territories, construction methods, intrinsic filtering, and creative iteration. Do not reproduce or maintain any of those rules here. Install domain-generator together with this skill. If it is not available, tell the user it is needed for creative candidates, and continue with the lifecycle channels only (deleted, expired, for-sale listings, brokered) without creating creative candidates here.

## Evidence discipline

- **Availability is point-in-time, and applies only to registrable candidates.** Only a successful per-domain `bulk_available` result that explicitly reports the domain as available qualifies as "available at check time"; attach an observation timestamp. Any other status, a missing domain row, a failed request, or an unrecognized response does not qualify. An already-registered candidate (expired / backorder, or a for-sale listing) is never labeled "available": verify and label it by its own status (current lifecycle and backorder / auction status for expired; current listing and asking price for a for-sale listing), each with an observation timestamp. Do not run `bulk_available` on an already-registered candidate; it measures registrability only.
- **Separate facts from judgment.** Source factual claims (availability, price, registration data). Present naming-quality judgments as reasoned creative assessments, not objective facts.
- **Price is data, and its shape depends on the acquisition path.** The fields for each path are listed under Output format. Premium status comes from the registrar's own page; otherwise it is Not Provided. Never carry standard-registration first-year / renewal fields onto an already-registered candidate, and never estimate a price.
- **A lightweight public-web check may catch obvious existing brands, but it is not trademark clearance. Never describe a candidate as legally safe.**

## Workflow

Use what the user has already told you (project, audience, style, TLD, or a specific target) and proceed. Ask at most one concise question at a time, and only when a missing detail would materially change the naming direction. Do not force a full diagnosis when the brief is already clear.

**Determine the mode first.** If the user has a specific taken target they want to replace, use the taken-target entry (step 1T). Otherwise use the project entry (steps 1 to 2). Both entries then hand creative work to domain-generator and use this advisor for lifecycle sourcing, comparison, and delivery.

1. **Brief (project mode).** Establish the essentials: project or industry, target audience, and what the name is for. If those are already given, move on. Ask a single question only when the answer changes direction (for example, tone, or whether the user is committed to `.com`).

1T. **Understand the target (taken-target mode).** Confirm the target is actually unavailable, unless a fresh conclusive result already exists in the conversation; do not search for alternatives to a domain that may still be registrable. An unclear, missing, failed, or unrecognized availability result is inconclusive, not proof that the target is taken. Extract plausible keyword and pattern interpretations (for example, `getflow.com` may be prefix + root) and record what the user values in it: literal word, meaning, length, sound, rhythm, image, construction, or brevity. Record TLD scope and willingness to backorder or buy a registered domain. Then go to step 3; domain-generator will turn this target brief into a creative frame.

2. **Prepare the generator handoff (project mode).** Turn the diagnosis into a compact brief containing the project or category, audience, use case, positioning or desired outcome, desired brand qualities, user-supplied words or concepts, literal constraints, TLD scope, language or regional constraints, and what may transform. Preserve any direction the user has chosen. Do not invent candidates, semantic distances, naming territories, construction methods, or filtering rules; domain-generator determines those from the brief.

3. **Use domain-generator for the creative channel.** In project mode, pass the generator-ready brief; its project or category, positioning, or user-supplied concept serves as the conceptual input. In taken-target mode, pass the full target plus the valued literal, semantic, phonetic, visual, and structural features. Domain-generator owns creative framing, generation, intrinsic filtering, brand-collision checks, initial availability verification, and creative rationale. Resume this workflow only after it returns its curated candidates. If domain-generator is not available, skip to step 4 with the lifecycle channels only. Do not create, extend, filter, or iterate creative candidates inside this skill. If the request is only for creative variants and no lifecycle comparison or advisory synthesis is needed, hand off directly to domain-generator and let it deliver the result.

4. **Gather lifecycle channels.** Scope every channel to what the user accepts. In taken-target mode, lifecycle sources are a primary channel; in project mode, use them when the registrable creative shortlist is thin or the user explicitly wants purchase / backorder options. Search the selected keyword or seed at both start and end where the source supports it:
   - `deleted` for dropped names that may be registrable; retain one as registrable only when its `bulk_available` result meets the availability rule in Evidence discipline.
   - `expired`, only when the user accepts backorder; verify lifecycle stage, backorder / auction status, and provider. Do not use `bulk_available` on a name that remains registered.
   - `market` for for-sale listings, with `aged` as a supplement for names with long registration histories, only when the user accepts purchasing a registered domain; verify the current marketplace listing, asking price, and listing type. A public listing is a purchase path, never brokered.
   - A brokered path only as a last resort for a registered candidate the user specifically wants, usually the original target, when no public listing exists. Confirm a named broker via the public web. Exclude the candidate if neither a listing nor a confirmable broker exists; never look up or use anyone's personal contact details.

5. **Verify, compare, and shortlist across channels.** Preserve domain-generator's naming territory, semantic distance, formation, creative concept, and seed connection. Re-run `bulk_available` only when a creative candidate's availability result is no longer fresh. Run the lightweight public-web collision check on any lifecycle candidate not already checked. Use `tld_check` only as a crowding / distribution signal, never as demand or quality. Compare all candidates on user fit, what they preserve from the brief or taken target, pronunciation, spelling, language risk, current acquisition status, cost basis, and acquisition complexity. Present up to 5 to 10 verified candidates, grouped from easiest to most involved: standard registration, backorderable, purchasable, then brokered. Availability alone does not make a candidate worth recommending.

6. **Iterate and follow up.** Route creative feedback back through domain-generator by semantic distance, image, sound, or formation; do not create a second prefix-swapping loop here. Adjust lifecycle channels when the user's acquisition tolerance changes. If the current best is already strong, do not force weaker options. Tailor next steps to the selected candidate: monitoring, deeper analysis with domain-analyze, or substitution-based current-market positioning with domain-cma-valuation.

## Output format

Present each shortlisted candidate with:

- **Domain**: the candidate.
- **Origin**: domain-generator creative candidate, deleted find, expired opportunity, for-sale listing, or brokered target; include the project territory or relation to the taken target.
- **Creative concept / formation** (for domain-generator candidates): preserve its naming territory, semantic distance, formation, and intended creative rationale.
- **Why it matches**: in project mode, its relation to the project's positioning and creative brief; in taken-target mode, what it preserves from the original target (literal word, meaning, pattern, length, sound, rhythm, image, or brevity).
- **Pronunciation / spelling notes**: readability and the radio test.
- **Current status, matched to the path**, with observation timestamp and labeled as Evidence discipline defines: "available at check time" for a registrable candidate; the current lifecycle and backorder / auction status for expired; the current listing status for a for-sale listing; the confirmed broker for brokered.
- **Acquisition path**: standard registration, backorder, purchase, or brokered.
- **Status / cost basis, matched to the acquisition path** (do not force first-year + renewal onto every path):
  - Standard registration: standard vs premium status, first-year price, and renewal price, with currency.
  - Backorder (expired): backorder fee and current bid where shown, with currency; note that securing the name is not guaranteed and renewal pricing applies only after it is caught.
  - For-sale purchase: the listing / asking price and listing type (BIN, minimum offer, current bid), with currency; an asking price is not a sale price.
  - Brokered: "Price unknown / negotiation required" (do not estimate), and the confirmed broker.
- **Historical sale price** (optional, include only when a named verifiable source provides it): a past confirmed sale from a named sales record or marketplace announcement, with that source and the sale date, kept as a separate field and never presented as the current asking or registration price. This skill has no dedicated sales-history data source, so omit this field when no such source is at hand; never estimate or infer a past price. For current market pricing, hand off to domain-cma-valuation, which positions a domain against current for-sale listings (it does not build a range from past sales); for a domain's sale history as part of due diligence, use domain-analyze.
- **Source and observation date**: where the price came from and when checked.
- **Language / brand caveats**: cross-language meaning issues or possible brand collisions.

## Key principles

- This advisor diagnoses, hands creative work to domain-generator, sources lifecycle inventory, compares acquisition paths, and delivers the shortlist; it does not generate creative candidates itself.
- Determine the mode first, diagnose briefly, and ask one question at a time, only when the answer changes direction.
- Label availability only as Evidence discipline defines it; verify an already-registered candidate by its own status.
- Scope every lifecycle channel to what the user accepts; the brokered and purchase paths are mutually exclusive.
- Match the cost basis to the acquisition path, and never estimate a price.
- Present a small verified shortlist grouped from easiest to most involved acquisition; availability alone does not make a candidate worth recommending.
- Source factual claims; naming-quality judgments are creative assessments, and a public-web check is not trademark clearance.
