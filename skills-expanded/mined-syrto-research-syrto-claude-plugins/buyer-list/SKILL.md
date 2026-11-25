---
name: buyer-list
description: >-
  Build a sell-side buyer universe for an Italian company: strategic acquirers (Italian
  companies only, found and sized in Syrto) and financial sponsors (researched from current
  public sources, Italian funds preferred), tiered on fit, ownership and financial capacity, with deliberate prominence for non-obvious
  "outside-the-box" buyers. Deliverables in Italian: Excel scan, HTML buyer book, HTML
  deep-dive on the top four. Use for a sell-side mandate or an exit, or when asked who could
  buy a company. Triggers: "buyer list", "buyer universe", "potential acquirers", "who would
  buy [company]", "strategic buyers", "financial sponsors", "lista di potenziali acquirenti",
  "lista acquirenti", "chi potrebbe comprare [azienda]", "chi potrebbe acquisire [azienda]",
  "a chi vendere [azienda]", "mandato sell-side", "universo di acquirenti", "fondi interessati
  a [azienda]". Not for buy-side add-on targets (use add-on-finder), a peer group (use
  syrto-comparables) or a sales prospect list (use prospects-scout).
---

# Buyer List

## Suite integration (read first)

Follow `${CLAUDE_PLUGIN_ROOT}/shared/core.md` (method, context, output, efficiency, handoff) and the capability map (`${CLAUDE_PLUGIN_ROOT}/shared/syrto-reference.md`), which says which Syrto tool serves each capability named in this skill. If an upstream skill left a `SYRTO-HANDOFF` for the target (for example `company-analysis`), reuse it in Step 1 and fetch only what is missing.

## Language

**All deliverables (Excel workbook, HTML buyer book, HTML deep-dive) must be written entirely in Italian** — headers, column labels, rationale text, tier names, notes, everything. This applies regardless of the language the user used to request the buyer list. Chat updates to the user should also default to Italian unless the user writes in another language.

## Workflow

### Data-depth ladder — spend effort where it pays off

A buyer universe surfaces many more names than deserve a full deep-dive, so the analysis is deliberately staged in three depth levels. The point is not to cut corners — it is to avoid burning a full financial deep-dive on names that a cheap screen already shows are low-probability, so the saved budget goes to the buyers the seller will actually contact. This applies to both strategic buyers (Step 2) and financial sponsors (Step 3).

- **L0 - Discovery (near-free):** name and activity description, as company search returns them for strategics and current public sources provide them for sponsors. Used to assemble the candidate pool and apply the fit gate. For strategics, put the size floor in the search itself: company search can require a minimum value of production (the target's own, for the reference year) and reports each match's value, so companies smaller than the target never enter the pool. A group shows up through its operating companies; the ownership structure at L2 shows the parent.
- **L1 - Screening (batched, never one read per name):** enough to assign a *provisional* tier and fill the summary table: essentially the size read vs. the target (fatturato/EBITDA and dimensione vs. target), which is where the size test is confirmed. Get it for *all* candidates that cleared L0 by comparing many companies at once, with the target in the same comparison, in as few calls as the tool allows. One comparison returns the buyers side-by-side against the target; a specific metric read per name would take N calls. Every comparison uses the reference year fixed in Step 1; a buyer that has not filed that year yet is read at its latest filed year and labelled as such. Every candidate that clears the L0 gates gets L1. Ownership is *not* pulled here: the full picture (ownership type and the UBO/group chain) comes from a per-company ownership read, so it moves wholesale to the shortlist (see L2).
- **L2 - Deep-dive (the heavy pulls):** multi-year financial trend, leverage/net debt and the market benchmark, all from one financial analysis per buyer over several recent years with its automatic benchmark; the thematic spider profile; a recent-M&A web check; and the full ownership picture from the ownership structure (ownership type and the UBO/group chain). Listed status is not in Syrto: only an S.p.A. or S.a.p.a. can be listed, so the legal form rules most names out, and a web check confirms the rest. **Reserve L2 for provisional Tier 1 and Tier 2 names, every outside-the-box candidate, and the four deep-dive names.** Provisional **Tier 3 names stay at L1** — they are low-probability "broaden the process" names and don't warrant the full pull, so they carry the batched size read but no structure/ownership pull.

**Tiering is provisional then confirmed.** Assign the tier from L1 data, then let L2 promote or demote a name. Any name sitting on the Tier 2/3 borderline should be taken to L2 before finalizing, so a genuinely strong buyer is never left in Tier 3 just because the cheap screen undersold it. Outside-the-box names always get L2 regardless of provisional tier — their whole case rests on a non-obvious point of contact that needs real evidence.

### Step-by-step (high level)

The detailed operating instructions for each step (discovery queries, categories, ownership pulls, rationale frameworks, summary-table columns, output layouts) live in the `references/` files — read the named file at the point of need.

1. **Step 1 - Understand the Target.** Build the target's profile from Syrto (company profile, multi-year financial analysis, ownership structure, thematic spider profile), enriched by the open web. If the target heads a group, read its consolidated statement too and say which basis the valuation uses. Then ask the user once, with a structured choice if your client offers one, otherwise a short numbered question: the sector's median EV/EBITDA multiple (Syrto has no transaction multiples, so never supply one from memory), seller preferences (strategic vs. financial, management continuity, timeline), buyers to include or exclude, and the reference year for the screen (default: the target's latest filed year). Derive the **implied valuation range** from that multiple applied to the target's EBITDA; if the user has no multiple, carry on and mark the range as pending.
2. **Step 2 - Strategic Buyers (Syrto-first, Italian-only).** Discover Italian strategics exclusively through Syrto's company search (semantic, one search at a time, at the default relevance cutoff) across direct competitors, adjacent players, vertical integrators, platform builders, and, with deliberate prominence, 4-8 **outside-the-box** buyers justified by a concrete point of contact. Aggregating a population can size a space before you page through it, but it names no candidates. Gate on the size test (buyer meaningfully larger than the target), then pull ownership and financial capacity from Syrto for the shortlist.
   → **Before Step 1 and Step 2, read `references/strategic-buyers.md`** (discovery categories, outside-the-box hunting, size test, ownership & rationale frameworks, financial-capacity pulls, summary-table columns).
3. **Step 3 — Financial Sponsors (Italian preferred).** Discover funds from current public sources, starting with AIFI's public member directory and the funds' own sites where available. Verify each candidate and its investment criteria from a current source; never invent a fund from memory. Verify Italian portfolio companies in Syrto. Foreign funds need a verifiable Italian footprint.
   → **Before Step 3, read `references/financial-sponsors.md`** (source and screening rules, sponsor categories, add-on logic, ownership, rationale, financial-capacity, summary-table columns).
4. **Step 4 — Prioritization.** Confirm the provisional tiers (L2 may promote/demote): Tier 1 (5-10), Tier 2 (10-15), Tier 3 (10-20). "Fuori dagli schemi" is a cross-cutting flag, not a tier. Every buyer needs a grounded rationale.
5. **Step 5 — Contact Mapping.** For each Tier 1 buyer, map decision-maker, relationship status, constraints and best approach channel, informed by the ownership/UBO work.
6. **Step 6 — Output (all in Italian).** Produce the Excel workbook (scanning tool), the HTML buyer book (complete narrative), and the HTML deep-dive (best 2 strategics + best 2 sponsors). Outside-the-box names must be visually distinct in every output.
   → **Before Steps 4-6, read `references/prioritization-and-output.md`** (tier definitions, contact-mapping fields, full Excel/HTML/deep-dive layout specs).

## Important Notes

- Syrto is the source of record for every Italian company on the list: discovery, ownership and financials. Use current public sources for sponsor discovery and fund-level facts (thesis, check-size, recent deals), and for qualitative colour and strategic-intent signals on companies Syrto has already surfaced. Where Syrto and a web source disagree on an Italian company, Syrto wins. If your client has no web access, ask the user for a current fund list or mark sponsor discovery incomplete; never fill fund names or criteria from memory.
- Ownership type (family, founder, sponsor-backed, state, listed) should inform both the tiering and the contact-mapping decision-maker — it changes who you'd actually approach and how fast they can move.
- Quality over quantity — a focused list of 30-40 well-researched buyers beats a list of 200 names, but don't let that discipline crowd out the outside-the-box names — those are worth the extra research time.
- Check for antitrust concerns with direct competitors — flag any that might face regulatory issues.
- Financial sponsors: check fund vintage and deployment pace — a fund nearing end of investment period may be more motivated.
- Update the list as the process progresses — move buyers between tiers based on feedback.

## Person-anchored discovery (optional)

When a name is in play (a fund partner, a serial acquirer, a known industrial family), find the person, then run a company search anchored on that person as shareholder, beneficial owner or officer. That maps what the person already controls, which surfaces buyers no sector search reaches. The person lookup on its own lists only a few holdings, enough to tell namesakes apart, so do not read it as the full map. This suite never buys contact details.
