---
name: salesbrain-skill
description: "Evidence-graded sales judgment for any selling situation. Replying to objections and stalls (\"too expensive\", \"need to think it over\", \"send me some info\", \"happy with our current vendor\", \"no budget\"), prepping and running discovery calls, qualifying leads, writing cold emails and cold-call openers, follow-up cadences and prospects who went dark, ending calls with a next step, pricing and three-tier proposals, pitches, decks and demos, negotiation and discount requests, sales hiring, coaching, comp plans, and seller slumps or burnout. Use whenever the user is trying to win, price or advance a deal, even if they never say \"sales\": a quote, proposal, prospect, buyer, lead, pipeline, demo, or a client who went quiet. Every rule carries an evidence tag and every number a source, and it corrects common guru advice that research contradicts. Not for support replies, internal emails, marketing landing copy, recruiting, or CRM data cleanup."
metadata:
  version: "0.1.0"
  evidence-tags: "study | data (vendor, correlational) | practitioner | opinion"
---

# salesbrain-skill

Judgment layer for selling. Research, enrichment and CRM data come from other tools; this skill decides
what to say, ask, price and do next, and says how strong the evidence behind each move is.

## 1. Get the context, without blocking

Work with what the user gave. Ask only what changes the advice, in one short batch, then proceed and mark
gaps `[NEEDS INPUT]`:

- Motion: small-ticket single-call, or complex B2B with a committee? Price band? (Changes pressure tolerance,
  who owns next steps, which framework applies.)
- Buyer: role, how many people decide, what they already know or tried.
- Stage: first touch, discovery, proposal sent, negotiation, stalled.
- What the user already did or said to this prospect.

## 2. Route to the reference

Open one file per task. Headers inside each file are situations; grep them.

| Situation                                                                                                                                                        | Open                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| Any objection, stall, brush-off, "think it over", competitor comparison, discount request                                                                        | `references/objections.md`                                    |
| Ending a call, asking for commitment, indecisive buyer, mutual action plan, procurement, negotiation and anchoring, methodology selector (BANT / MEDDICC / JTBD) | `references/closing.md`                                       |
| Call prep, discovery questions, qualification, user interviews, demo-before-discovery                                                                            | `references/discovery.md`                                     |
| Cold email, cold call, cadence, went dark, LinkedIn, inbound lead, referral ask, targeting                                                                       | `references/outreach.md`                                      |
| Positioning, pricing, tiers, payment terms, "no decision" forces, Hormozi-style offers                                                                           | `references/offer-positioning.md`                             |
| Pitch, deck, demo, storytelling, delivery, proposal narrative                                                                                                    | `references/pitching.md`                                      |
| Openers, first meeting, hostile or curt buyer, trust, AI seller disclosure                                                                                       | `references/rapport.md`                                       |
| "What does the research say about scarcity / social proof / framing / consistency"                                                                               | `references/persuasion-psychology.md`                         |
| Founder brand, thought leadership, social selling                                                                                                                | `references/personal-branding.md`                             |
| Process design, SDR benchmarks, hiring, ramp, coaching, comp, promotion, AI-human split, buying groups                                                           | `references/sales-process-team.md`                            |
| Slump, nerves, lost deal, burnout, motivation                                                                                                                    | `references/mindset.md`                                       |
| "Role-play the buyer with me" | pick the motion in `references/closing.md`, object using the motive table in `references/objections.md`, stay in character, debrief against the rules below |
| Before stating any statistic, study or guru claim                                                                                                                | `references/claims-audit.md`, then `references/benchmarks.md` |
| "Who says that?"                                                                                                                                                 | `references/sources.md`                                       |

## 3. Rules the model usually gets wrong

These override default instincts. The tag says how strong the evidence is.

1. Diagnose indecision versus status-quo preference before responding. 40–60% of deals end in no decision, and
   fear or urgency made indecisive buyers more indecisive 84% of the time (Dixon, ~2.5M conversations). `[data]`
2. Pause, then ask one clarifying question before answering an objection; answer with one strong reason, not a
   stack (Gong, 67,149 demos; Weaver 2012 presenter's paradox). `[data] [study]`
3. Replace the close with a buyer-owned, dated next step. Closing techniques lowered trust (Hawes 1996); close
   rates fell 71% when the first call skipped next steps (Gong 2018, 28,833 deals). `[study] [data]`
4. Question type beats question count: 11–14 questions spread through the call (Gong 2017, 519k calls; a 2025
   sample put won deals at 15–16), and no solution until the buyer states an explicit need (SPIN, 35,000+ coded
   calls). `[data]`
5. Talk ratio is a diagnostic, not a target. No uninterrupted monologue past ~76 seconds (Gong 2017 demos). `[data]`
6. Raise price on the first call, late in the call: 42% win rate when price came up on call one versus 5% when
   never (Gong 2020, 11,331 opportunities). `[data]`
7. Cold email: under 75 words, one interest-based ask, no ROI claims, no social proof in a first touch (Gong: ROI
   −15%, social proof −22%; Lavender; Sahni 2018 personalization RCTs) `[data] [study]`; leave the word "AI" out
   and describe the outcome instead `[practitioner]`.
8. Open a cold call with a reason or permission. "Did I catch you at a bad time?" was the worst opener (2.15% vs
   11.24% best, Gong, 300M+ calls); "how are you?" is fine. `[data]`
9. Build three genuinely different tiers and recommend the middle; decoys work only in numeric side-by-side
   comparisons; anchor only with a reasoned number (Neumann 2016; Yang & Lynn 2014; Röseler & Schütz). `[study]`
10. Quantify the problem first, then tell the customer story. Statistics move beliefs, stories move intention;
    complex B2B buyers process carefully, so lead with the business case (Zebregs 2015; Carpenter 2015). `[study]`
11. Buyers see tactics coming, most in personal selling (Eisend & Tarrahi 2022). Scarcity, consistency traps,
    loss framing and "but you are free" are weak or backfire; candour is the evidence-consistent move. `[study]`
12. Rapport is responsiveness, not openers or compliments (Kaski 2018, recorded B2B meetings). Trust earns future
    business more than today's choice (Doney & Cannon 1997). `[study]`

Tactics marked `(small-ticket, single-call)` in the references are exceptions for that motion only. They are
never the default for complex B2B.

## 4. Guardrails

- Never invent a customer name, metric, quote, case study or statistic. Write `[NEEDS INPUT]` instead.
- Vendor data (Gong, Dixon/JOLT, Bridge Group, Belkins, Lavender, 6sense, Gartner) is correlational and
  self-selected. Quote it with its sample and say so.
- Before repeating a study or a guru's number, check `references/claims-audit.md`. If the user's claim is on the
  do-not-cite list, say so in one line and give the safe wording.
- Length caps hold in every deliverable: emails under 75 words, spoken scripts under 40 words, one ask per
  message, one reason per objection.
- When two sources conflict, the references state `Default: X. Exception: Y.` Follow the default unless the
  user's context matches the exception.
- End every deliverable with the three-line footer in `assets/deliverable-footer.md`: Assumed / Evidence /
  Not checked.

## 5. Output templates

| Deliverable                         | Template                       |
| ----------------------------------- | ------------------------------ |
| Cold or follow-up email             | `assets/cold-email.md`         |
| Objection reply (spoken or written) | `assets/objection-reply.md`    |
| Discovery call guide                | `assets/discovery-guide.md`    |
| Footer for every deliverable        | `assets/deliverable-footer.md` |

## 6. When not to use this skill

- Internal or non-sales writing: team emails, support replies, recruiting, marketing landing copy.
- One-line factual questions the model answers without sources.
- Company research, contact finding, enrichment, CRM updates, report generation: use a data skill or MCP
  server, then come back here for what to say.
- Not covered yet: selling to existing customers (QBRs, renewals, upsell, churn saves) and RFP bid/no-bid
  beyond the procurement notes in `references/closing.md`. Say so rather than improvising a playbook.

## 7. Related

- Data and workflow skills (CRM, enrichment, prospect research, pipeline reports) supply facts; this skill
  supplies judgment. If an installed sales plugin also has an objections or outreach skill, disable it so the
  two do not compete on the same prompts.
- Notes layer (transcripts, per-source notes, evidence grades) lives outside this skill and is never loaded.
  `AUTHORING.md` holds the rules every line here had to pass.
