---
name: buyer-persona
description: >
  Creating B2B Buyer Personas in the Ananas-Agency model.
  Use this skill when the user wants to: create a buyer persona, define the target segment,
  define who the company sells to, describe customers' problems and challenges, match
  value propositions to decision-makers, prepare strategic input for prospecting,
  marketing or sales. Trigger: "buyer persona", "who do we sell to", "target
  segment", "who is our customer", "customer problems", "customer challenges",
  "persona", "target group", "target", "market segment".
---

# Creating a B2B Buyer Persona (Ananas-Agency)

## Goal

Guide the user through building 1-2 complete B2B Buyer Personas: documents that describe a market segment, the people involved in the purchase, their problems, challenges, objections, and the value propositions matched to each of them.

## What a Buyer Persona is

A Buyer Persona is the company's compass: it points to whom we sell, with what, and why. It is a living document that evolves alongside the company. One persona = one market segment (no matter how many people are involved in the decision; we treat the company as a single buying entity).

**A B2B Buyer Persona is NOT a B2C-style consumer profile.** A B2C consumer profile describes an individual's demographics and lifestyle (age, hobbies, habits). A B2B Buyer Persona describes business mechanisms: the market segment (firmographics), the decision-making roles, and the business problems and challenges. The segment/firmographic layer corresponds to the **Ideal Customer Profile (ICP)**; the persona then adds the buying roles on top of it.

## Why a Buyer Persona

- Prospecting: messaging tailored to the role and the problem, with continuous testing of what converts
- Marketing: a content strategy built around real problems, plus landing pages and campaigns
- Sales: meeting preparation, segment-specific offers, and objection handling
- Input for: landing pages, offers, cold email, call scripts, content marketing

## Prerequisite: List of Value Propositions

**A Buyer Persona requires a finished list of value propositions (PSO (Problem · Solution · Outcome)).** Without it, you cannot correctly match values to the people in the segment.

If the user does not have a PSO (Problem · Solution · Outcome) list, let them know:
> "A Buyer Persona requires a finished list of value propositions in the PSO (Problem · Solution · Outcome) format. Without it, I'm unable to create a complete persona. Would you like to build a list of values first?"

Do not generate a persona without a PSO (Problem · Solution · Outcome) list, and do not improvise a simplified list on the fly.

## Buyer Persona structure

Each persona contains:

**Mandatory:**
1. **Segment** — industry, sub-industry, company size, headcount, revenue, location (this block is the Ideal Customer Profile (ICP) layer of the persona)
2. **Segment condition** — growing / stagnant / declining
3. **Buying process length** — short (up to 1 month), medium (1-6 months), long (6+ months)
4. **Purchase trigger** — what most often starts the buying process in this segment
5. **People involved in the purchase** (the buying committee / Decision-Making Unit, DMU) — for each person:
   - Role (not a job title!) — e.g. "manages sales", "responsible for finances"
   - Role in the buying process — e.g. "initiates the purchase", "approves the budget", "blocks the decision", "end user", "advises technically"
   - Personal trigger — what has to happen for THIS person to start looking for a solution (e.g. "lost 3 deals in a row", "got an ultimatum from the board")
   - Problems (hurts today, requires immediate action)
   - Challenges (doesn't hurt today, but we have to do it)
   - Objections and buying difficulties
   - Matched value propositions from the PSO (Problem · Solution · Outcome) list
6. **Justification for choosing the segment** — why this segment, and how strong the values are that we hold for it

## Conversation flow

> **How to run this session — read before you start.** Treat this as a **discovery conversation**: a guided working session with the user, closer to a strategy call or workshop than a questionnaire. The entire value of the result comes from what you draw out of them, so slow down and dig in. A rushed exchange that jumps straight to a draft produces a generic, forgettable persona; a proper working session produces one grounded in the user's real market and real customers.
> - **Open first, then move to choices — keep it balanced.** Make the *first* question on a topic open (*"before I ask specifics, tell me in your own words how you see this"*), then **stop asking everything open**: once you see the shape, switch to targeted questions and fill only genuine gaps with more open follow-ups.
> - **Prefer selectable answers to keep the pace.** Whenever a question has a small, knowable set of likely answers, present them as a **pickable list** (the user selects, and can add their own) rather than another open prompt — an all-open interview drags; balance one open opener with quick pickable questions. Always still push for the specifics behind whatever they pick.
> - **Pace and depth.** Work through the topics as a genuine back-and-forth, asking **2–3 questions at a time** so you never overwhelm the user. Across the whole session expect to ask roughly **8–15 questions** before you have enough to build. If you catch yourself moving to a draft after only two or three answers, you have stopped too early. There is almost always more to uncover, and the difference shows in the output.
> - **Cover the checklist before you build.** Do not move on to matching values (Step 6) or to producing the deliverable until every item in **Required inputs** below has genuinely been captured, or the user has explicitly chosen to skip it, or told you they don't know. A missing item is a gap to close in conversation, not a blank for you to quietly fill on their behalf.
> - **Push past the first answer.** People give you the surface answer first — "we're faster", "better service", "good quality". Treat every vague or general reply as an invitation to go one level deeper: ask for a concrete example, a number, a percentage, an amount in €, a timeframe, or the specific situation that prompted it. Stay on a single point, following up, until the answer is specific enough to actually act on. This is where a good session earns its value.
> - **Ask before you assume.** Never invent a fact the user could have given you. Your default is always to ask them first. If the user genuinely cannot answer, or would rather not, you may fill the gap yourself, but you must label it clearly as **[Assumption]** in the output and flag it so they can confirm or correct it later.

### Required inputs — capture before drafting
Check each off (or mark "skip") before Step 6 (matching) and delivery:
- [ ] PSO (Problem · Solution · Outcome) value list received, IDs intact
- [ ] Segment — industry, sub-industry, size (headcount / revenue), location
- [ ] Segment condition — growing / stagnant / declining
- [ ] Buying-process length — short / medium / long
- [ ] Purchase trigger — what most often starts the buying process in this segment
- [ ] For **each** DMU role: role (not title) · role in the buying process · personal trigger · problems · challenges · 3–5 objections (raw + expanded) · matched value IDs
- [ ] Segment justification — why this segment and how strong the values are for it

### Step 1: Collect the list of value propositions

Ask the user for their finished PSO (Problem · Solution · Outcome) list. If they don't have one, stop the process (see the prerequisite). If they do, ask them to paste it in or attach the file.

### Step 2: Get to know the company and market

If the user has a **Company Brief** (from the `company-brief` skill), ask them to paste it and skip any questions it already answers. Otherwise, ask the following questions.

Ask:
- What does the company do? (industry, product/service)
- Which segments does the company sell to today?
- Which segments bring in the most revenue?
- Are there segments the company would like to reach but hasn't yet?

If the user provides a website URL, analyze it.

### Step 3: Choose segments (max 2 to start)

Based on the information about the company and the PSO (Problem · Solution · Outcome) list, propose 1-2 segments. Advise the user:
> "To start, let's create at most 2 buyer personas: that way we can actually validate them before spreading thin (the next skill runs a one-week test with real customers, which realistically covers 1–2 personas), and each extra persona multiplies the work in every later skill. It's worth adding more only once these first ones are working and delivering results."

This cap is a **starting gate, not a hard limit**: once the first personas are validated, the user can add more.

**The Pineapple rule — choosing segment breadth:**
Suggest the BROADEST possible segment, as long as that entire broad segment shares a problem for which the company has a strong value proposition. Narrow it only when:
- Conversion is too low across the broad segment
- The market is crowded and you need to stand out
- The company's values speak only to a narrow niche

Example: "B2B SaaS companies with 50–200 employees" is fine if the company's values address the problems of that entire segment. Don't narrow it to "HR-software vendors in a single city" without a reason.

Segment evaluation criteria — see: [references/rules-buyer-persona.md](references/rules-buyer-persona.md)

### Step 4: Define the people in the segment

For each segment, ask:
- Who takes part in the buying decision? (roles, not job titles!)
- Who initiates the purchase? Who approves the budget? Who can block it?
- Who is the end user?

Prompt the user: "Give the role, not the job title. For example, 'manages sales', because in practice that might be a Sales Director, VP Sales, CSO, or even the CEO in a small company."

**Look for roles specific to the segment.** Once you've defined the obvious roles (manages the company, manages sales), probe further: "Who else influences the decision in THIS SPECIFIC segment?" For example, in IT it's the CTO; in manufacturing, the production manager; in distribution, the logistics specialist; in healthcare, the specialist physician. Don't copy roles from one persona to another: each segment has its own dynamics.

### Step 5: Extract problems, challenges, triggers and objections

For each person, ask probing questions (max 2-3 per turn):
- Questions about problems and challenges — see: [references/rules-buyer-persona.md](references/rules-buyer-persona.md)

**Personal trigger:** For each person, ask: "What has to happen for this person to start ACTIVELY looking for a solution?" Look for specific events, not generalities, e.g. "lost 3 deals in a row", "got an ultimatum from the board", "a key employee left".

**Objections:** Propose 3-5 typical objections per person, based on the problems and values you've collected. Each should include both raw, short forms (the way the customer actually says them: "Too expensive", "Not now", "I have to check with someone") and expanded versions. Validate with the user: "Here are the objections I think this person might raise. Does that ring true? What would you add?"

### Step 6: Match value propositions to people

From the finished PSO (Problem · Solution · Outcome) list, assign values to specific people: the same value can go to different people, but with a different emphasis. Keep in mind:
- Person managing finances -> values affecting cashflow, ROI, financial risk
- Person managing operations -> values affecting performance, time, reliability
- Technical person -> product values, parameters, compatibility

Cite each matched value by its ID so the persona stays linked to the value list — but **never show a bare ID in the conversation**: always pair it with a short label, e.g. `PV-03 (one-order logistics)`, so the user immediately knows what it means.

Validate with the user: "Here's how I matched the values to each person. Would you change anything?"

### Step 7: Deliver the final list as files

Generate TWO files (`.md` and a styled, self-contained `.html`) and share them with the user. The `.html` must follow the shared navigation rules: cross-links to the other deliverables, hover hints on short terms, and the **Next** button to the next file in the sequence (see the reference's Output file format). Format — see: [references/rules-buyer-persona.md](references/rules-buyer-persona.md), section "Output file format".

Save both files and share them with the user for download.

### Step 8: Offer to add more personas

Once the first persona(s) are delivered, **explicitly offer to build more** — don't quietly stop at the cap. The max-2 start is a gate for *validation*, not a limit on how many the user actually needs:

> "That's your [first / two] persona[s]. We capped it here so the next skill can validate [it / them] with real customers before spreading wider — but if you sell to clearly distinct segments, I can build another persona now. Want to add one, or move on to the next skill?"

If the user wants more, repeat Steps 3–7 for the additional segment(s). If they'd rather move on, remind them they can come back and add personas later, once the first ones are validated.

## Add to the Strategy Dossier

This suite runs as one continuous session. **Deliver only your own two files now** — the **Strategy Dossier** is an **internal running document**, not delivered until the end (by the final skill), so don't create or hand over a dossier file mid-session. Record the **Buyer Personas** section into that internal dossier with the persona(s) you just built (segment/ICP, DMU roles, objections, matched value IDs). Full format: [dossier-format.md](../dossier-format.md).

## Critical rules

1. **No PSO (Problem · Solution · Outcome) list, no persona.** Do not generate a persona without a finished list of value propositions.
2. **Max 2 personas to start.** So they can be validated (the next skill's one-week test realistically covers 1–2) before spreading, and because each extra persona multiplies the work in Skills 5–7. It's a starting gate, not a hard cap; add more once the first ones are working.
3. **A segment is a company, not a person.** 1 persona = 1 market segment, regardless of the number of decision-makers.
4. **Roles, not job titles.** "Manages sales" instead of "Sales Director".
5. **Problems ≠ Challenges.** A problem hurts TODAY. A challenge is something we have to do, but it doesn't hurt yet.
6. **Non-obvious problems.** "The CEO wants sales growth": everyone knows that. Look for problems no one else targets.
7. **Broad segment, strong value.** Narrow it only when there's a reason (low conversion, heavy competition).
8. **A Buyer Persona is a living document.** Remind the user that the persona should be validated through experiments with real customers.
9. **A discovery conversation, not a form.** Follow the session guidance at the top of the conversation flow: cover the Required-inputs checklist before you build, push every vague answer toward a specific, and label any gap you fill yourself **[Assumption]**.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
