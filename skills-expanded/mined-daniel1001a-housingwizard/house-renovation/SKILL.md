---
name: house-renovation
description: Plan renovation for a house being bought or just bought - a budget split into licensed work, materials and labor, what the owner or a handy relative may legally do themselves, permit order and timing, old-house hazards (lead, asbestos), quote packages per trade, contingency, and when and where to buy appliances, furniture and custom cabinetry (sales seasons, tariffs, overseas orders). Use when a buyer asks "how much will it cost to fix", "can my dad do this himself", "what order should we renovate in", "what should we buy on Black Friday", "should we order cabinets from overseas", or wants quotes organized.
---

# House renovation

Renovation budgets fail in predictable ways: a flat discount for "we will do it ourselves" that ignores licensed trades, permits pulled in the wrong order, and purchases timed against a sale instead of against the schedule. This skill plans around those.

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

## Budget in three layers

Never apply one discount to the whole budget because someone handy will help.

| Layer | Contents | Can the owner save here? |
|---|---|---|
| 1. Licensed and regulated | Electrical, plumbing, gas, structural, abatement (lead, asbestos), permits and legalization fees | No. Price it as if hiring |
| 2. Materials | Everything that gets installed | No. Everyone pays for materials |
| 3. Labor and contractor overhead for unlicensed work | Carpentry, framing, drywall, flooring, paint, tile, cabinets, insulation | Yes. This is where family labor saves money |

Which work needs a licensed trade depends on the place. Some jurisdictions let owner-occupants do their own electrical or plumbing with a permit and inspection; others (New York City is one; see `references/nyc.md`) allow no owner exemption at all. Say which rule you are applying, and in generic mode tell the buyer to confirm with the local building department.

Add a contingency of 15 to 20 percent for old houses, toward the high end before about 1970. Never copy a cost breakdown from one house to another; roof type, windows, heating and construction era change the work entirely.

### When a checked floor plan exists

Do not write the numbers yourself. Use the scripts in house-floorplan, which keep every figure traceable:

1. `takeoff.py` gives quantities, each with a rule ID, JSON pointer and scale source.
2. The buyer fills a costbook with prices they received or looked up. The default costbook is empty and example entries are marked "example, not a price"; never invent or paste a market price into it. Run `costbook_check.py`.
3. `costs.py` multiplies quantity by unit price and sorts the result into the three layers above. A line with no costbook entry stays unpriced, and licensed work (layer 1) is not estimated unless the buyer recorded a quote for it.
4. Report the estimate grade and why it is not higher. A BLS wage is only a `wage_floor`, what a worker earns and not what a contractor charges; never add it to the total or call it a quote.

If the overlay has not been confirmed by a person, say the result is UNCONFIRMED and do not present any number as a budget.

## Order and timing

- Permits generally require the owner's authorization, so they come after closing. Design, quotes and product choices can happen before.
- If there is unpermitted work, decide the legalization path first, then pull other permits. An inspector on site for one permit may notice another problem.
- Do the dusty, lead-disturbing work before a baby or small children move in.
- Order by trade dependency: demolition, structure, rough plumbing, electrical and HVAC, inspections, insulation and drywall, flooring and tile, cabinets, paint and trim, fixtures and appliances.
- If living elsewhere during work, count rent and mortgage together in the budget.

## Quote packages

Group items by trade so each contractor prices the same scope. Use quantities from house-floorplan (floor area by finish, wall paint area, baseboard, stairs, windows, doors). Each package lists: scope, quantities with their source and whether heights were measured, finishes, what is excluded, permit responsibility, and a request for itemized pricing.

With a checked plan, `export_package.py` writes these per trade (`scope.md`, `quantities.csv`, `assumptions.md`) and leaves prices out so contractors do not anchor on an estimate. It sends nothing. The buyer reads each file, sends it, and asks for itemized quotes. A test of whether a package works, with targets set by the project and not yet measured: send it to two or three contractors and expect at least two itemized quotes within 10 days and at most two follow-up questions about missing information. Treat the counts as feedback on the package.

## Buying

Read `references/purchasing.md`. Core rules: pick models and record today's price as a baseline, then compare at each major sale; do not wait for a discount that tariffs may have erased; never pay non-refundable deposits before the contract is signed, and prefer after clear to close; custom overseas orders are only worth it when the factory price is well under half of local custom pricing, after duties, freight and taxes.

## Output

1. Budget by layer with ranges and sources, and the contingency.
2. The work order with dependencies and which items need permits or licensed trades where the house is.
3. Quote packages.
4. A buying timeline tied to the work order.
5. Human check: licensed contractors confirm scope and code; the building department confirms permit needs.
