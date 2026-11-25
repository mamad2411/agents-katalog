---
name: prfaq-amazon
description: Write a PR/FAQ (a one-page press release plus an FAQ) per Amazon's Working Backwards process, as Amazon describes it (aboutamazon.com "An insider look at Amazon's culture and processes"; AWS re:Invent 2020 session INO206) and as Colin Bryar and Bill Carr teach it (workingbackwards.com PR/FAQ template). Use when the user says "write a PR/FAQ", "PRFAQ", "working backwards doc", "write the press release before we build it", or "Amazon-style press release", or must pitch a new product, feature, or initiative from the customer's point of view.
---

# PR/FAQ (Amazon Working Backwards)

Start with the customer experience, then work backwards to what you must build.

## The core rule

**Write the launch press release and its FAQ before you build, from the customer's point of view.** Use it to get clarity, not to document what you already decided. If the press release cannot show a specific customer a product that is meaningfully better (faster, easier, or cheaper), the idea is not worth building.

Workflow: `name the customer and the problem` → `draft the press release (1 page)` → `draft the external FAQ, then the internal FAQ (5 pages max)` → `add the hard questions` → `run the Verify checklist`.

## Mechanics

1. **Length caps.** Press release: a few paragraphs, always less than one page. FAQ: five pages or less. More pages earn nothing; cut to fit.
2. **Press release sections, in this order.**
   - *Heading:* one sentence that names the product in words the target customer understands.
   - *Subheading:* one sentence that names the specific customer segment and the benefit they get.
   - *Date line and summary:* open with city, media outlet, and planned launch date ("SEATTLE–(BUSINESS WIRE)–August 31, 2014 –"), then summarize the product and its benefit. Use a date you expect to hit.
   - *Problem:* the customer's problem, from the customer's point of view.
   - *Solution:* how the product solves that problem, directly and simply. Name the current alternatives: "Today, customers with this problem use x, y, or z."
   - *Leader quote:* one quote from the company spokesperson.
   - *Customer experience:* how the customer gets started and how easy it is.
   - *Customer quote:* one quote from a hypothetical customer.
   - *Call to action:* where to go to start (a URL).
3. **One specific customer.** Name the segment ("finance teams that reconcile Shopify orders"), never "everyone" or "users". A product for everyone is a product for no one.
4. **Customer language in the PR and external FAQ.** No corporate jargon, internal team names, system names, code names, internal costs, or P&L. Those go in the internal FAQ. The customer's price belongs in the external FAQ.
5. **Specific, not vague.** Long, vague, or high-level descriptions fail. Each benefit says what gets faster, easier, or cheaper for the customer. Use numbers the author supplied; mark a missing one `[TBD: what is needed]`, never invent it.
6. **Quotes a person would say.** Reviewers test each quote with "Would a customer really say this?" A customer quote states what changed for them, not a slogan.
7. **External FAQ: customer and press questions.** Price, how it works, how to get help, where to buy, refunds, and how it differs from what the customer uses today.
8. **Internal FAQ: stakeholder questions.** Ask what finance, legal, operations, support, and leadership would ask. Cover: customer evidence so far, market size (TAM), unit economics and upfront investment, partners and dependencies, legal and regulatory issues, options considered and rejected, one-way doors, what customers will be most disappointed in, the top three reasons it will fail, and the decisions needed today.
9. **Answer the hard questions.** Be optimistic but realistic. Keep a question that makes the idea look weak, and answer it.

Output shape:

```
[Heading]
[Subheading: segment + main benefit]
CITY–(OUTLET)–[Launch date] – [Summary]
[Problem]  [Solution, incl. "Today, customers ... use x, y, or z."]
"[Leader quote]," said [name, title].
[How to get started]
"[Customer quote]," said [hypothetical customer].
To get started, go to [URL].
External FAQ — Q/A pairs   |   Internal FAQ — Q/A pairs
```

## Verify

- Press release fits on one page; FAQ is five pages or less
- All nine press release sections are present, in the Mechanics order
- Heading and subheading are one sentence each; the subheading names a customer segment
- Date line has a city, a media outlet, and a launch date
- Problem paragraph speaks from the customer's view and names no internal team or system
- Solution names what customers use today
- Zero jargon, code names, internal costs, or P&L figures in the press release or external FAQ (the customer's price is allowed)
- Every benefit states what gets faster, easier, or cheaper
- FAQ has separate External and Internal sections; Internal covers TAM, unit economics, dependencies, legal, and the top three failure reasons
- Every number traces to the author's input; every gap is marked `[TBD: ...]`
- Last step: run the `de-ai` skill on the draft before you deliver it

## Do not

- Open with the company or the feature ("Acme is excited to announce our platform"). Open with the customer and the benefit.
- Write the PR/FAQ after the decision, to justify it
- Use "revolutionary" or "best-in-class" in place of what gets faster, easier, or cheaper
- Put internal questions (margin, headcount, architecture) in the external FAQ
- Drop or soften a hard question to make the idea look better
- Pad the document; length is not rigor

## Example transformations

**Before:** "We are excited to announce that the Platform team has launched SyncFlow, a next-generation, AI-powered integration engine that leverages our robust event bus to deliver best-in-class synchronization. SyncFlow cuts sync time from 24 hours to 15 minutes for finance teams that reconcile Shopify orders in NetSuite. It is projected to add $2M ARR."

**After:** "*Heading:* SyncFlow puts Shopify orders in NetSuite within 15 minutes.
*Subheading:* Finance teams that reconcile Shopify orders in NetSuite now see each order 15 minutes after the sale, not 24 hours later.
*Problem:* [TBD: what the 24-hour wait costs the finance team, in their words.]
(Move "Platform team", "event bus", and "$2M ARR" to the internal FAQ.)"

**Before:** "FAQ. Q: How much will it cost? A: Pricing is still being finalized, but we are confident customers will see tremendous value. Q: What is the projected margin? A: 40% at scale."

**After:** "External FAQ. Q: How much will it cost? A: [TBD: the price. 'Tremendous value' does not answer the question.]
Internal FAQ. Q: What is the projected margin? A: 40% at scale. [TBD: the volume at which 'scale' starts.]"
