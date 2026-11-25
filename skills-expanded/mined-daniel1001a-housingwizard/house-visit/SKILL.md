---
name: house-visit
description: Prepare a home buyer for a showing, a second visit or the final walkthrough - a checklist tuned to the house's age, systems and the buyer's plans, the few measurements that decide legal use and cost, how two people split the job, what not to touch, and a prompt that turns a phone AI into a structured note-taker for voice and video. Use when a buyer says "we are seeing a house tomorrow", "what should we look for", "second visit", "final walkthrough", "what should I measure", or shares visit notes, photos or video to organize.
---

# House visit

A visit is where the things no record shows (smell, slope, sound, damp, light, traffic) are noticed or missed. It is also where the measurements that decide legal use get taken, or never are. This skill makes a checklist for this specific house and turns messy notes into usable ones.

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

## Build the checklist

Start from `assets/visit-checklist.md` and cut or add based on what you know:

- **Age and systems** (from house-records or the listing): pre-1978 lead, pre-1980 asbestos materials, oil heat history, panel brand, steam or hot-water heat, septic.
- **Findings to confirm**: every open question in the case file that a person on site can answer.
- **Design plans** (from house-floorplan): each planned change becomes something to measure or look at (wall thickness where a wall might come out, floor-to-grade in a basement room meant for sleeping).
- **Visit type**: a first showing is short and observational; a second visit measures; a final walkthrough tests every system and confirms agreed repairs.

Keep it to what fits in the time available. A first showing checklist longer than one page will not get used.

## The measurements that matter most

Some measurements decide whether a space counts as legal living area, which is often part of what the buyer is paying for:

- Basement: clear height at the lowest beam or duct, and floor level compared with outside ground level.
- Attic: lowest and highest clear height where people would stand.
- Setbacks when an addition is in question: wall, eave edge and steps are three different numbers.
- Door frame depth where an addition meets the old house: interior partitions are about 4 to 5 in deep; an old exterior wall turned interior is usually 8 to 12 in.

Scans, listing plans and photos are not measurements. Bring a laser measure and a tape.

## On site

- Split roles: one person on systems (panel, heating, water heater, basement, signs of old oil tanks, sewer cleanout), one on space (layout, light, storage, circulation, where furniture goes). Both walk the whole house once.
- Record, do not judge, in front of agents or the seller. Keep a voice recorder running.
- Stand still in the main room for 30 seconds and listen. Open closets and smell. Run two taps and flush a toilet together to check pressure.
- Suspected asbestos (chalky pipe wrap, granular gray-brown attic insulation): photograph from a distance. Do not touch, scrape or blow on it.
- Visit twice at different times if it is a serious candidate: a weekday evening for parking and noise, in heavy rain for drainage, and one real commute at the real hour.

## Notes from a phone AI

`assets/notes-assistant-prompt.md` is a prompt for any phone AI with voice or video (for example a custom assistant in the Gemini, ChatGPT or Claude apps). It records observations with timestamps and confidence, and never diagnoses. When the buyer pastes those notes back here, cross-check them against the inspection report and measurements, and send contradictions back to the site rather than guessing which is right.

## Output

A checklist sized for the visit, grouped by room or system, with a short "must measure" block at the top and a "must ask" block for the agent. After the visit, a clean observation log with sources `[seen]` and open questions, written into the case file.

Human check: every measurement in the log should say where exactly it was taken (under the beam, between beams, at the wall).
