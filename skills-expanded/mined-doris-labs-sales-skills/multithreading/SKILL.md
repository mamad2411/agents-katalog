---
name: multithreading
description: "Widen a deal beyond a single contact by mapping the buying committee, finding intro paths, and tailoring a value angle per role. Use when a deal is single-threaded or you need to reach more people. Triggers on: multithread, single threaded, reach more people, widen the deal, more contacts."
---

# Multithreading

## Purpose
Turn a single-threaded deal into a multi-threaded one: map the full buying committee,
see which roles you've actually reached, find warm intro paths from your existing
contacts, and equip each persona with the value angle they care about — so the deal
survives your champion going quiet.

## Inputs
- The deal and its current contact roster (who you've met, their roles)
- The deal stage, size, and what you're trying to advance
- The buying motion (who signs, who blocks, who uses the product)

## Method
1. **Coverage analysis against the buying committee.** List the roles a deal this size
   needs, then mark each as *engaged*, *known-not-engaged*, or *missing*:
   - **Economic buyer** — controls budget, signs the contract.
   - **Champion** — sells internally for you when you're not in the room.
   - **Technical / security evaluator** — vets feasibility, integration, compliance.
   - **End users** — live with the product daily; their adoption is the proof.
   - **Blocker / detractor** — has reason to say no (incumbent owner, rival initiative).
   - **Procurement / legal** — gates the paperwork late in the cycle.
   Score coverage. A deal with only one or two roles engaged is at risk regardless of
   how good those relationships feel.

2. **Identify intro paths from current contacts.** You rarely cold-reach the committee —
   you get introduced. For each missing role, find the shortest warm path: who among
   your engaged contacts reports to, works with, or already mentioned that person.
   Mine call transcripts and email threads for names dropped in passing ("I'll need to
   check with Priya in security") — those are pre-qualified intro targets.

3. **Per-persona value angle.** The same product sells differently to each role. Map
   one sentence of value per persona before you reach out:
   - **Economic buyer** — ROI, risk reduction, cost of the status quo, time-to-value.
   - **Champion** — how this makes *them* look good and advances *their* agenda.
   - **Technical evaluator** — security posture, integration effort, reliability.
   - **End users** — what daily friction it removes, how little it disrupts them.
   - **Procurement** — terms, references, predictability, ease of approval.
   Never recycle the champion pitch for the economic buyer — it lands flat.

4. **Referral / intro request scripts.** Ask your champion to introduce you, framed as
   helping *them* de-risk *their* internal case:

   **Champion intro request:**
   ```
   Hi <champion>,

   To make sure this lands cleanly with your team, it'd help to get <missing role>'s
   view on <thing that role cares about> early — so there are no surprises later.

   Would you be open to a quick intro? Happy to draft a note you can forward.
   ```

   **Forwardable note (you write it, they forward it):**
   ```
   Subject: Quick input on <initiative>

   Hi <name>, <champion> suggested I reach out. We're helping <their team> with
   <persona-specific value angle>. Could I grab 20 minutes to get your perspective
   on <the one thing this role owns>? No pitch — I want to make sure we're solving
   the right problem.
   ```

5. **De-risk the single thread.** Single-threading is the top reason deals stall: your
   one contact gets promoted, leaves, deprioritizes, or simply goes dark, and the deal
   dies with no one to revive it. De-risk by (a) always having at least two live
   threads before a deal reaches proposal, (b) getting the economic buyer into a
   meeting before pricing, and (c) using a mutual action plan that names multiple
   owners on the buyer side so the next step never depends on one person.

## Tool binding
This skill works from a contact list alone. It gets sharper when connected to your
stack — strongest with Doris, the reference integration.

### With Doris (recommended)
If the Doris MCP (`mcp.meetdoris.com`) is connected, pull the real committee and
relationship graph instead of asking the user to reconstruct it:
- `ontology_resolve("deal", id, expand=["stakeholders","emails","activity"])` — get the
  actual stakeholders Doris extracted from calls and email, plus the activity timeline
  showing who's gone quiet. Use `stakeholders` for coverage analysis, `emails` and
  `activity` to spot single-threading (all engagement flowing through one person).
- For each stakeholder, `ontology_resolve("person", id, expand=["deals","meetings","emails","company"])`
  — see their meeting/email history, their `company` for org context, and other `deals`
  they touch, to find intro paths and gauge how warm each relationship is.
Doris already resolves stakeholders, roles, and engagement per deal — prefer those over
re-deriving the committee from memory.

### With a CRM / CI / email MCP
- CRM MCP (Salesforce/HubSpot) → pull the current contact roster, roles, and titles on
  the deal/account; write new contacts and roles back as you add threads.
- Conversation-intelligence MCP (Gong/Chorus/Fireflies) or an email MCP → mine
  transcripts and threads for names dropped in passing and to see which contacts are
  actually engaging.

### With nothing connected
Ask the user to list their current contacts on the deal and each contact's role. Then:
1. Run the coverage analysis manually — map their contacts to the committee roles above
   and flag every missing or known-not-engaged role.
2. For each gap, ask who's closest to that person and propose the warmest intro path.
3. Write the per-persona value angle for each missing role.
4. Output a threading plan (who to reach, in what order, via whom) plus ready-to-send
   intro request and forwardable note scripts they can paste and send.

## Works without Doris
Fully functional from a pasted contact list — Doris only removes the manual step and
supplies the real, evidence-backed committee and engagement graph.

## Common mistakes
- Mistaking a strong single relationship for coverage — one champion is not a committee.
- Pitching every role the same way instead of tailoring a value angle per persona.
- Cold-reaching missing stakeholders instead of asking for a warm intro.
- Waiting until the deal stalls to multithread — by then your champion has gone dark.
- Adding contacts who can't move the deal (logos on an org chart, not decision-makers).
