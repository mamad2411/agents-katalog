---
name: acct-objection-handling
description: Builds an objection register in the customer's own words with, for each objection, the questions to explore, a restatement to check, a response backed by real proof and the question to ask when the objection is real. Use for "run acct-objection-handling", "objection handling", "handle this objection", "it's too expensive", "how do I respond to a price objection", "common sales objections", "the customer said not now", "objection response", part of the Claude for Account Executives Pack by 90n.
---

# Objection Handling

## When To Use
"It's too expensive" makes you drop the price before you understand it. Run this before or after a meeting, on the objections you really heard. It answers: what sits behind this objection, and how do you answer it with proof instead of a discount?

## When Not To Use
When the conversation really is about price and terms, run Negotiation Plan. To build the proof itself, run FAB Statements. This skill makes no price move at all.

## Inputs
- The objections you heard, in the customer's exact words, with the date and the job role of the speaker.
- Your FAB Statements or the list of proof you can cite.
- The stage of the deal.
If you have none of this, I start from one objection as you report it, and mark the output as a first draft.

## Approach
Four moves in a fixed order, a widely taught practice described here generically: listen, acknowledge, explore, respond. You do not answer an objection you have not understood, so the response comes last and is checked afterwards. The failure it prevents: the discount given on an objection that was really about risk, timing or the person who decides.

## Workflow
1. I ask at most three questions: which objections did you hear, word for word, when and from which job role; what stage is the deal at; and which proof can you cite.
2. Listen: I record each objection as it was said, with date and job role. One reported second-hand is marked as such, and I do not sharpen the wording.
3. Acknowledge: one sentence that restates the objection so the customer can confirm or correct it ("if I understand you, what matters is..."). It agrees with nothing and argues with nothing.
4. Explore: two or three open questions to find what is behind it ("expensive compared with what?", "what makes you say that?"). An objection often changes shape here, and the register keeps both versions.
5. Respond: an answer resting on a proof from your FAB Statements. With no proof available I write that, and the gap goes to the missing-proof list.
6. Check: one question to confirm the point is settled. If a new objection appears, it gets its own row and starts at the top.
7. Real objections (no budget this year, wrong time, a decision already made) are accepted and recorded, with the question that keeps the door open: "what would have to change for this to come back, and when?". No price reduction here: price is prepared in Negotiation Plan, against something in return.

## Output Format
```markdown
# Objection Register
[Account] · [deal stage] · [date]
## Objections heard
| Objection (their words) | Date, job role | Acknowledge (restatement) | Explore (questions) | Respond (proof, source) | Check |
|---|---|---|---|---|---|
| "[words]" | [date], [role] | [sentence] | [questions] | [answer] ([source]) | [question] |
## Real objections
| Objection | What makes it real | Question that keeps the door open | Revisit on |
|---|---|---|---|
| [objection] | [fact] | [question] | [date] |
## Missing proof
- [objection with no proof available] · how to get it: [step]
## Decision
[You] choose the responses you stand behind before the next conversation on [date].
```

## Done When
- Every objection is recorded in the customer's words, with date and job role.
- Every response rests on a proof that exists, or the gap is written down.
- Every real objection has its revisit question and date.

## Quality Bar
- Explore before you respond, every time.
- No manipulation technique, no pressure, no false urgency.
- An objection is tied to a job role and a need, never to someone's character.
- Cues to say in your own words, not lines to recite.
- No discount or price is proposed here; you answer with real proof, and no proof is invented.

## Next
Run acct-call-notes (Sales Call Notes) to write up the meeting and the objections while they are fresh.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
