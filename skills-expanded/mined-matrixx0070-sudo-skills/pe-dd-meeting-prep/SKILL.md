---
name: pe-dd-meeting-prep
version: 1.0.0
description: Prepare the question sets, logistics, and follow-up capture for private-equity diligence meetings — management presentations, expert-network calls, and customer reference calls — so each session extracts decision-grade evidence rather than a rehearsed pitch.
author: matrixx0070
tags: [private-equity, due-diligence, management-meeting, expert-calls, customer-references, question-bank, deal-team]
capabilities: []
---

## When to use

Use this in the days before any live diligence session with a human on the other side: the management presentation and follow-up deep-dives, expert-network calls, and customer or channel reference calls. It turns loose curiosity into a sequenced question bank by function, sorts logistics (who attends, who leads, what to send in advance, recording and compliance), and gives you a disciplined way to capture answers and route follow-ups back into the workstreams. Reach for it whenever a meeting could either confirm your thesis or blow it up, and you get one shot in the room — management will be coached, experts are on the clock, and customers will not take a second call.

**Not for:** scoping which workstreams exist and tracking findings to close (use pe-dd-checklist); the pre-LOI go/no-go screen before diligence meetings are even scheduled (use pe-deal-screening); building the origination pipeline and outreach that precedes a deal (use pe-deal-sourcing); modeling the returns the meetings inform (use pe-returns-analysis); dissecting unit economics that a customer call might touch (use pe-unit-economics); assessing AI maturity as a value lever (use pe-ai-readiness); writing up meeting conclusions for the committee (use pe-ic-memo); drafting the value-creation plan management discussions feed (use pe-value-creation-plan); or setting up recurring management reporting after close (use pe-portfolio-monitoring).

This skill is deal-support, not legal or compliance advice. Expert-network engagements carry real regulatory risk (MNPI, non-compete, employer confidentiality); your compliance team and counsel must clear the expert, the topics, and the call terms before you dial.

## Method

1. Set the meeting's job: for each scheduled session, write the one decision it must move — the thesis assumption to confirm, the red flag to close, the number to pressure-test. **Decision:** if a meeting has no decision to move, cancel it; live time is scarcer than data-room time.
2. Choose the right counterpart for each question: management for strategy, plans, and internal numbers; independent experts for market truth and competitive reality; customers for real satisfaction, switching cost, and renewal intent. Do not ask management to grade their own market or a competitor's product.
3. Build the question bank by function — commercial, financial, product/tech, operations, people — laddered from open ("walk us through how you win a deal") to specific ("what was gross churn last year by cohort?") to challenge ("your win rate rose while pricing fell — reconcile that"). Front-load the questions that could kill the deal.
4. Set logistics: attendees and their roles, who leads each block and who scribes, materials sent in advance, timeboxing, recording/consent, and — for expert and customer calls — the compliance script and off-limits topics. **Decision:** assign one lead questioner and one dedicated scribe per session; a room where everyone asks and no one records loses the answers.
5. Run the session to extract, not to be pitched: follow the ladder, ask for evidence not adjectives ("show me the cohort file," not "is retention good?"), and let silence pull detail. Park tangents; protect the kill questions' airtime.
6. Capture in a structured note during the call: question, answer, evidence promised, and — critically — every follow-up with an owner and a due date routed back to the right workstream in the checklist.
7. Debrief within hours while memory is fresh: what confirmed, what broke, what changed the model, and what the next session must now cover. Feed conclusions to the IC memo and open items to the tracker.

## Example

A sponsor diligencing a $40M-ARR vertical SaaS company runs three sessions in one week. The management presentation is scoped to one decision — is the 118% net revenue retention durable or propped up by a few big expansions? The commercial block, led by the deal partner with an associate scribing, ladders from "walk us through land-and-expand" to "show us NRR by cohort and by customer" and uncovers that two enterprise logos drove 40% of last year's expansion — a finding routed as a follow-up to the QoE workstream. Two expert-network calls (compliance-cleared, competitor-employee experts screened out) reveal a well-funded entrant winning on price in the low end, reframing the churn risk. Three customer reference calls — deliberately including one the seller did *not* hand-pick, sourced independently — show high satisfaction among large accounts but a small-account customer who is actively evaluating the new entrant, confirming the expert view. The debrief downgrades the NRR-durability assumption from "confirmed" to "confirmed for enterprise, at-risk for SMB," changes the returns model's expansion assumption, and generates four follow-ups with owners and dates before the next data-room drop.

## Pitfalls

- **Taking the seller's reference list at face value.** Curated references are advocates. Insist on a mix including references you source independently, and weight what non-selected customers say — the risk lives in the accounts the seller did not offer.
- **Letting management run the clock.** A polished presentation is designed to fill the hour and pre-empt hard questions. Timebox the pitch, protect airtime for your kill questions, and interrupt to go deep where it matters.
- **Skipping expert-call compliance.** Expert networks can put MNPI, non-competes, or a competitor's confidential information in your hands. Screen the expert, clear the topics, and run a compliance script — a single tainted call can jeopardize the deal.
- **No scribe, no follow-up owner.** If the same person leads and records, the best answers evaporate and follow-ups drift. One lead, one scribe, every follow-up owned and dated back to a workstream.
- **Asking the wrong counterpart.** Management cannot objectively size their market or rate a rival; customers cannot explain internal margin. Match each question to the person who actually knows, or you collect confident answers that are worthless.

## Output format

```
# DD Meeting Prep — <target> — <session type> — <date>
Meeting objective (one decision to move): <...>
Attendees: <names / roles>   Lead questioner: <name>   Scribe: <name>
Logistics: <format / duration / recording+consent / materials sent>
Compliance (expert/customer calls): <cleared? off-limits topics>

## Question bank (by function)
### Commercial
- OPEN: <...>   | SPECIFIC: <...>   | CHALLENGE: <...>
### Financial
- OPEN / SPECIFIC / CHALLENGE ...
### Product / Tech
### Operations
### People / Management
### Kill questions (must ask — thesis-breakers)
- <...>

## Live capture
| # | Question | Answer | Evidence promised | Follow-up | Owner | Due | Workstream |

## Do's and don'ts
- DO: <...>   DON'T: <...>

## Debrief
- Confirmed: ...   Broke: ...   Model change: ...   Next session must cover: ...
```

## Reference

Substantive overview of PE diligence-meeting practice below — accurate to common market approach, not legal or compliance advice. Expert and customer engagements must be cleared by compliance/counsel first.

### The three meeting types — and what each is good for

Each counterpart knows something the others cannot, and mismatching question to source is the most common waste of a session:

| Meeting type | Counterpart | Best for | Blind spot |
|-------------|------------|----------|-----------|
| **Management presentation / deep-dives** | Target's leadership | Strategy, internal numbers, plans, culture, the value-creation story | Coached, self-interested; cannot objectively grade own market/competitors |
| **Expert-network calls** | Independent industry experts | Market reality, competitive dynamics, technology trends, pricing truth | Compliance risk; expert may lack company-specific detail |
| **Customer / channel reference calls** | Target's customers, partners | Real satisfaction, switching cost, renewal intent, competitive alternatives | Seller-curated bias; individual anecdote ≠ base rate |

### Question laddering

Structure each functional block as a ladder so you open the counterpart up before you press:

| Rung | Purpose | Example |
|------|---------|---------|
| **Open** | Get them talking, reveal their framing | "Walk us through how a typical deal is won." |
| **Specific** | Pin a number or fact | "What was gross and net churn last year by cohort?" |
| **Challenge** | Reconcile a tension you already see | "Win rate rose while ASP fell — how?" |
| **Evidence** | Convert claim to artifact | "Can you share the cohort file so we can trace it?" |

### Question banks by function (starter set)

| Function | Representative questions |
|----------|-------------------------|
| **Commercial** | How do you win vs. lose? Pipeline coverage and conversion? Customer concentration and contract terms? Pricing power and recent changes? |
| **Financial** | What drives EBITDA quality? One-offs in the last three years? Working-capital seasonality? Cash conversion? Budget vs. actual track record? |
| **Product / Tech** | Architecture and scalability? Tech debt and roadmap cost? Security posture? Key-person dependencies in engineering? |
| **Operations** | Capacity and utilization? Supply-chain concentration? Unit-cost trend? Bottlenecks to growth? |
| **People / Management** | Depth below the CEO? Retention and incentives? Gaps the plan needs to fill? Culture and turnover? |

### Do's and don'ts

| Do | Don't |
|----|-------|
| Timebox the pitch; protect kill-question airtime | Let management fill the hour uninterrupted |
| Ask for evidence, not adjectives | Accept "retention is strong" without the file |
| Use one lead and one dedicated scribe | Have everyone ask and no one record |
| Independently source some customer references | Rely only on the seller's curated list |
| Clear experts and topics with compliance first | Discuss a competitor's confidential info or MNPI |
| Let silence draw out detail | Fill every pause yourself |

### Expert-network compliance essentials

Expert calls are the highest-risk diligence activity. Before dialing, confirm: the expert has been screened (not a current employee of the target or a direct competitor bound by confidentiality), the topics are pre-cleared and MNPI is off-limits, a compliance script opens the call, and the engagement runs through a reputable network with its own compliance controls. When in doubt, counsel clears the call — a tainted call can contaminate the whole deal, not just the session.

### Capturing and routing follow-ups

A meeting's value is realized only when its follow-ups close. Every answer that promises evidence or raises a new question becomes a tracked item — question, owner, due date, and the workstream it belongs to — routed back into the DD checklist so the finding is diligenced, not merely heard. Debrief the same day: memory decays fast, and the difference between "management said retention is fine" and "management could not produce cohort-level NRR when asked" is the difference between a confirmed assumption and a red flag.
