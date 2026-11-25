---
name: buying-process
description: >
  Creating a description of the B2B buying process of a segment in the Ananas-Agency model.
  Use this skill when the user wants to: describe how customers buy, map the buying process
  of a segment, understand the stages of the customer's buying decision, prepare a strategy for reaching
  the customer per stage, create recommendations for salespeople and marketing tailored to
  the buying process. Trigger: "buying process", "how the customer buys", "buying stages",
  "buying journey", "B2B customer journey", "how to reach the customer", "outreach
  strategy", "buying process mapping".
---

# Describing the B2B Buying Process of a Segment (Ananas-Agency)

## Goal

Using the buyer persona and the value propositions, build a description of how the segment behaves throughout the buying process across its 5 stages, along with outreach recommendations for sales and supporting suggestions for marketing.

## Prerequisites

**The buying process requires TWO completed documents:**
1. **List of value propositions (PSO (Problem · Solution · Outcome))** — without it, you don't know what problem the company solves
2. **Buyer Persona** — without it, you don't know who buys and why

If the user is missing one or both, let them know:
> "The buying process description requires a completed list of value propositions (PSO (Problem · Solution · Outcome)) and a buyer persona. Without them I can't produce a complete description. Which of these documents would you like to create first?"

Do not generate a buying process description unless both documents are in place.

If the user has run Persona Experiments (Skill 4), build on the **validated** PSO/persona: values tagged `Source: validated` are tested ground; treat `hypothesis` values with appropriate caution. If no experiments have been run yet, proceed with the hypotheses, but flag that the description rests on untested inputs.

## The 5 stages of the buying process

The buying process (the buyer's journey) is **non-linear**: buyers don't move neatly through 1->2->3->4->5. They loop back, jump ahead, pause for months, or drop out entirely. Picture it as a loop buyers cycle back through, not a straight line.

### Stage 1: Problem identification
Something has knocked the customer out of the status quo: an event that sets off thinking about change. Without a strong enough trigger, the purchase will never happen.

### Stage 2: Solution exploration
The customer explores and orients themselves among the OPTIONS for a solution: not among suppliers yet, but among directions. "Do I need a CRM system, or is Excel enough? Should I hire a salesperson, or buy a service?" At this point they're interested in a ballpark price. The stage can last months, or barely exist at all (the customer already knows the concept).

### Stage 3: Requirements building
The customer digs into the CHOSEN concept. They look for detailed information, compare solutions, meet with salespeople, read case studies, and watch demos.

### Stage 4: Supplier selection
The customer decides WHAT EXACTLY they will buy and FOR HOW MUCH. Requirements, a specification, and a budget take shape. The "what we're buying" decision is made, but not necessarily "from whom".

### Stage 5: Validation / Purchase
The customer looks for a VENDOR. They compare suppliers, negotiate terms, and weigh the price-to-value ratio. This is where the "who we're buying from" decision is made.

### When the purchase doesn't happen
- The problem wasn't strong enough (the trigger was too weak)
- The company lacked the resources (budget, people, time)
- More pressing priorities came up
- The customer got stuck at the Solution exploration stage and never settled on a direction

## Structure of the buying process description

For each segment (buyer persona), the description includes:

**Per stage (5 stages):**
1. **What the customer does** — specific actions (searches Google, calls contacts, watches webinars, sends requests for quotes)
2. **Where they do it** — channels and places (Google, LinkedIn, trade fairs, conferences, industry groups, a phone call to an industry contact)
3. **Who is involved** — which roles from the buyer persona are active at this stage
4. **How long it lasts** — an estimated duration of the stage for this segment
5. **What can stop the process** — risks and blockers at this stage

**Recommendations (per stage):**
1. **For the salesperson** — whom to reach, why, and with what message
2. **For marketing** — what is worth creating to support conversion at this stage

## Conversation flow

> **How to run this session — read before you start.** Treat this as a **discovery conversation**: a guided working session with the user, closer to a strategy call or workshop than a questionnaire. The entire value of the result comes from what you draw out of them, so slow down and dig in. A rushed exchange that jumps straight to a draft produces a generic, forgettable buying-process description; a proper working session produces one grounded in the user's real business.
> - **Open first, then move to choices — keep it balanced.** Make the *first* question on a topic open (*"before I ask specifics, tell me in your own words how you see this"*), then **stop asking everything open**: once you see the shape, switch to targeted questions and fill only genuine gaps with more open follow-ups.
> - **Prefer selectable answers to keep the pace.** Whenever a question has a small, knowable set of likely answers, present them as a **pickable list** (the user selects, and can add their own) rather than another open prompt — an all-open interview drags; balance one open opener with quick pickable questions. Always still push for the specifics behind whatever they pick.
> - **Pace and depth.** Work through the topics as a genuine back-and-forth, asking **2–3 questions at a time** so you never overwhelm the user. Across the whole session expect to ask roughly **8–12 questions** before you have enough to build. If you catch yourself moving to a draft after only two or three answers, you have stopped too early. There is almost always more to uncover, and the difference shows in the output.
> - **Cover the checklist before you build.** Do not move on to writing the outreach recommendations (Step 5) or to producing the deliverable until every item in **Required inputs** below has genuinely been captured, or the user has explicitly chosen to skip it, or told you they don't know. A missing item is a gap to close in conversation, not a blank for you to quietly fill on their behalf.
> - **Push past the first answer.** People give you the surface answer first — "we're faster", "better service", "good quality". Treat every vague or general reply as an invitation to go one level deeper: ask for a concrete example, a number, a percentage, an amount in €, a timeframe, or the specific situation that prompted it. Stay on a single point, following up, until the answer is specific enough to actually act on. This is where a good session earns its value.
> - **Ask before you assume.** Never invent a fact the user could have given you. Your default is always to ask them first. If the user genuinely cannot answer, or would rather not, you may fill the gap yourself, but you must label it clearly as **[Assumption]** in the output and flag it so they can confirm or correct it later.

### Required inputs — capture before drafting
Check each off (or mark "skip") before Step 5 (outreach recommendations):
- [ ] PSO (Problem · Solution · Outcome) list + Buyer Persona received
- [ ] Segment chosen (if the persona covers more than one)
- [ ] For **each** of the 5 stages: what the customer does · where they do it · who's involved · how long it lasts · what can stop them
- [ ] Drop-off picture — where customers most often stall, why, and rough conversion %

### Step 1: Collect the input documents

Ask the user for:
- A completed list of value propositions (PSO (Problem · Solution · Outcome))
- A completed buyer persona

If one or both are missing, stop the process (see prerequisites).

### Step 2: Choose a segment to work on

If the buyer persona covers more than 1 segment, ask which one to work on first. Each segment has its OWN buying process.

### Step 3: Map the behaviors per stage

**Start open, then fill the gaps.** Before drilling into the 5 stages, ask the user to **describe their current buying process in their own words** — how a typical customer in this segment goes from "no idea they need this" to signing, in whatever order and detail comes naturally: *"Walk me through how a customer in this segment actually buys today — from the first moment they realise they have a problem, all the way to the purchase. Tell it however it really happens."* Let them talk; capture what they give you and map it onto the 5 stages yourself.

Then, for each of the 5 stages, ask targeted probing questions **only for what their description left open** (max 2-3 per turn) — don't re-ask what they already told you. For the questions, see: [references/rules-buying-processes.md](references/rules-buying-processes.md)

After each answer, update the process map and tell the user what you already have and what is still missing.

### Step 4: Identify blockers and drop-off moments

Ask:
- At which stage do customers most often drop off?
- Why do customers give up (no budget, no urgency, the competition)?
- What percentage of inquiries/leads end in a purchase?

### Step 5: Create outreach recommendations

Based on the mapped process, create:
- **Recommendations for the salesperson** per stage — whom, with what message, through which channel
- **Suggestions for marketing** per stage — what content/materials to create to support the customer

The recommendations must be grounded in the value propositions from the PSO (Problem · Solution · Outcome) list, not generic. Each salesperson message must cite the specific value proposition it is built on by its ID — and **never as a bare code**: always pair the ID with a short label, e.g. `PV-03 (one-order logistics)`, so the reader knows what it means.

### Step 6: Deliver the final description as files

Generate TWO files (`.md` and a styled, self-contained `.html`) and share them with the user. The `.html` must follow the shared navigation rules: cross-links to the other deliverables, hover hints on short terms, and the **Next** button to the next file in the sequence (see the reference's Output file format). For the format, see: [references/rules-buying-processes.md](references/rules-buying-processes.md), section "Output file format".

Save both files and share them with the user for download.

## Add to the Strategy Dossier

This suite runs as one continuous session. **Deliver only your own two files now** — the **Strategy Dossier** is an **internal running document**, not delivered until the end, so don't create or hand over a dossier file mid-session. Record the **Buying Process** section into that internal dossier with the mapped 5-stage journey and the per-stage recommendations (each cited by value ID with a short label). Full format: [dossier-format.md](../dossier-format.md).

## Critical rules

1. **No PSO (Problem · Solution · Outcome) and buyer persona, no process description.** Do not generate without both documents.
2. **The process is non-linear.** Always make the point that the customer doesn't move in a straight line. Describe the typical path, but flag where the customer loops back or jumps ahead.
3. **Describe the BUYING process, not the SELLING process.** Look through the customer's eyes, not the salesperson's. Capture what the CUSTOMER does, not what the salesperson should do (that belongs in the recommendations).
4. **A separate process per segment.** A manufacturing company buys differently than a SaaS company.
5. **Specific actions, not generalities.** Not "the customer looks for information" but "the customer types 'CRM system for manufacturing comparison' into Google, reads the ranking on Capterra, and asks an industry contact in a LinkedIn group".
6. **Recommendations grounded in value.** The salesperson's message must point to a specific value proposition from the PSO (Problem · Solution · Outcome) list, not to generalities.
7. **Account for drop-off moments.** Every stage carries the risk that the customer stalls. Describe what blocks them and how to prevent it.
8. **A discovery conversation, not a form.** Follow the session guidance at the top of the conversation flow: cover the Required-inputs checklist before you build, push every vague answer toward a specific, and label any gap you fill yourself **[Assumption]**.


---

## License

Copyright (c) 2026 Kostiantyn Ivanov (Ananas-Agency, ananas-agency.com).

Released under the MIT License — keeping the copyright notice is all that is required, and a credit to the author is warmly appreciated. Full license text: [LICENSE](../../LICENSE)
