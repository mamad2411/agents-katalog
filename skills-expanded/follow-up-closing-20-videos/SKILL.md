---
name: follow-up-closing-20-videos
description: Writes sales follow-ups and closing next steps using the rules repeated most often across the 20 most-watched videos on the topic, weighting each rule by how many of those videos say it, and flags any expert disagreements to A/B test. Use when the user says "write my follow-up", "the prospect went quiet", "how do I close this deal", "what do I send after the sales call", "help me book the next meeting", or "they said they need to think about it".
author: Yonathan Cohen (Tool Monsters)
version: 1.0.0
updated: 2026-09-14
license: MIT
---

# /follow-up-closing

This skill comes from the transcripts of the 20 most-watched videos on following up after sales calls and closing deals, published in the last 6 months (since 2026-03-14). Together they have 55,981 views and 96,926 words. From them, 407 pieces of advice were extracted, and 379 were kept because their verbatim quote was found in a transcript. Those pieces of advice fall into 211 distinct themes. The number next to each rule is how many of the 20 videos say it. Sources are in sources.md.

The most repeated rule reached 7 of 20. Treat the weights as odds, not laws.

## Inputs
1. The call notes or transcript, including the exact pain points and current approach the prospect described.
2. Where the deal stands: date of last contact, how many follow-ups have been sent, and whether a next meeting is already booked.
3. The stakeholders you know by name and role, and who has not been involved yet.
4. What you are offering, including price and terms, and what you want this message or call to achieve.

Do not invent pain points, quotes, names, roles, budgets, prices, or deadlines the user has not provided.

## The rules, by weight
### Strong (7 of 20)
- **Avoid generic, repetitive follow-ups; personalize every message.** (7/20) Drop "just circling back" and "just checking in." Refer to the exact pain points the prospect shared on the call.

### Solid (4 of 20)
- **Diagnose pain and current approach before pitching.** (4/20) Ask: "How are you handling things today without those capabilities?"
- **Uncover and challenge the real objection behind stalls.** (4/20) Ask: "Is this because you don't have the budget, or because you don't see the value in what we do?"
- **Book the next meeting live on the call.** (4/20) Book a meeting from a meeting. In the last third of the call, ask: "How does next Tuesday look at this exact same time?"

### Mentioned (3 of 20)
Use pattern-interrupt messages to re-engage prospects · Send a takeaway text asking if they are still open or if you should close the file · Always ask for the sale or next step on every call · Multi-thread with multiple stakeholders early · Send follow-ups and proposals within minutes of meetings (5 to 10 minutes, not 2 to 3 days) · Keep following up persistently, even after rejection

## Where the experts disagree: do not pick, test
The data showed no disagreements among the 20 videos, so no A/B test is assigned by default.

## Steps
1. Read the call notes. List the prospect's pain points and current approach in their own words. If either is missing, recommend asking the diagnosis question on the next call before pitching again.
2. Decide the situation: right after a call, a stall or objection, or a prospect who has gone quiet.
3. Right after a call: draft the follow-up or proposal to send within 5 to 10 minutes. Reference the specific pains, confirm the next meeting if one was booked, and propose a specific day and time if one was not.
4. Stall or objection: write one question that separates the real objection (for example, budget versus value) and include a clear ask for the next step.
5. Gone quiet: count the follow-ups already sent. If the prospect has not replied, write a personalized follow-up or a pattern-interrupt message. When it fits, offer a takeaway text asking if they are still open or if you should close the file.
6. Check the stakeholder list. If only one contact is involved, suggest bringing in another named role, using only names and roles the user has provided.
7. Review every draft against the Strong rule. Remove any generic line that could be sent to any prospect.
8. Finish by listing each rule applied with its weight (for example, "Personalize every message, 7/20"). Then state which choice is being A/B tested. If the user did not name one, say that no disagreement was found in the data, so no test is running.

## Never
- Never claim close rates, reply rates, or other results the user has not measured.
- Never invent facts about the prospect or customer, including pains, quotes, stakeholders, budget, or timing.
- Never send a follow-up that only says "just checking in" or "just circling back" with no reference to the prospect's situation.
