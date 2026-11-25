---
name: discovery-calls-20-videos
description: Plans, runs and reviews sales discovery calls (questions, structure, qualifying, uncovering pain) using rules weighted by how many of the 20 most-watched videos repeat each one, and flags where experts disagree so you can A/B test instead of guessing. Use when the user says "prep my discovery call", "what should I ask on a sales call", "qualify this prospect", "review my discovery call", "structure a first sales call" or "how do I uncover pain".
author: Yonathan Cohen (Tool Monsters)
version: 1.0.0
updated: 2026-09-14
license: MIT
---

# /discovery-calls

This skill was built from the transcripts of the 20 most-watched videos on sales discovery calls from the last 6 months (since 2026-03-14). Together they have 68,064 views and 105,310 words. From them, 480 pieces of advice were extracted, and 444 were kept because their verbatim quote was found in the transcript. Those kept pieces group into 166 distinct themes. The number next to each rule is how many of the 20 videos say it. Sources are in sources.md.

The most repeated rule reached 10 of 20. Treat the weights as odds, not laws.

## Inputs
1. What you sell, who you sell it to, and the outcome it delivers.
2. What you already know about the prospect: company, role, who will attend, and how they found you or reached out.
3. The call's length and the next step you want by the end, such as a second meeting, a proposal or a close.
4. Any pre-call form answers, notes or a recording of a past call, if you have them.

Refuse to invent the prospect's numbers, pains, stakeholders, timeline or buying process. Mark each one as a question to ask on the call.

## The rules, by weight
### Strong (6 to 10 of 20)
- **Probe past surface answers to find the real underlying problem.** (10/20) Go four layers down on one question, not four different questions: "Why? What usually happens there?" or "Tell me a time you went through this."
- **Understand their situation and goals before pitching anything.** (8/20) Don't pitch from minute two. Try: "Tell me a little bit about your business and what led you to reaching out for support today."
- **Research and prepare hypotheses and questions before calls.** (8/20) Check their website, LinkedIn, hiring trends and the personas they target. Some spend a few hours prepping for a one-hour call.
- **Book the next meeting live before the call ends.** (7/20) "Throw the dart": suggest "same time next Thursday" and put a placeholder invite on their calendar.
- **Ask why now to find the compelling trigger.** (6/20) "Why this? Why now?" shows how urgent the problem is and how much it affects the company.
- **Set a brief, clear agenda at the call start.** (6/20) Cover purpose, plan and outcome in 30 to 45 seconds. For example: "Today, I just want to learn about you and your business..."
- **Talk less and don't talk about yourself.** (6/20)
- **Get concrete current and target business numbers.** (6/20) Ask about revenue, churn, headcount, spend, sales per month, average sale price and margin. For example: 18% churn today, and the target is to cut close time by a full week.
- **Identify and engage all stakeholders and decision-makers.** (6/20) Ask: "Who's responsible for that priority, and what's the best way to get aligned with them?" Everyone on the call is there for a reason, so bring them in.

### Solid (4 to 5 of 20)
- **Ask what challenges are holding them back.** (5/20) Add "in your opinion" to get more engaged answers.
- **Frame discovery as mutual qualification, not a pitch.** (5/20)
- **Send follow-up recap or proposal the same day.** (5/20) Send it within 24 hours at the latest. Include a thank you, a summary of the discussion and the proposal.
- **Record and review calls regularly for coaching.** (5/20)
- **Ask fewer, focused questions instead of a checklist interrogation.** (4/20) Advice ranges from 6 to 8 core questions up to 11 to 14 targeted ones. The 11 to 14 figure is cited as Gong data.
- **Build enough pain and depth before pitching or closing.** (4/20) Shallow discovery can cause refunds later, even after a successful pitch.
- **Preempt objections early during discovery.** (4/20)
- **Map how they handle the process today.** (4/20) Ask things like "Where does that go? How are you tracking follow-ups?" This part takes about 20 minutes.
- **Ask about long-term vision and ideal success.** (4/20) "If everything went perfectly in the next 6 to 12 months, what would have happened?"
- **Agree next steps, owners, milestones in a mutual plan.** (4/20) Be specific: "I'm going to send you a proposal by end of business tomorrow."
- **Tailor pitch to their problems using their language.** (4/20) Give a 45 to 60 second pitch on three pillars. Then spend 3 to 4 minutes on their one or two biggest problems.
- **Explore consequences and opportunity cost of inaction.** (4/20)

### Mentioned (3 of 20)
Ask direct emotional questions to uncover real feelings · Ask their timeline for acting or completing the project · Directly challenge excuses, fear, and avoidance · Keep discovery calls short, about 15-30 minutes · Open with a short credibility and problem-narrative statement · Start broad on the business, then narrow to specifics · Recap situation and outcome, get agreement before pitching · Use a pre-call questionnaire or inquiry form · Build rapport with small talk and personal connection first · Ask about past solutions and why it's unsolved

## Where the experts disagree: do not pick, test
| Choice | Side A | Side B |
|---|---|---|
| Small talk | Keep small talk to a minimum (2/20) | Build rapport with small talk and personal connection first (3/20) |
| Buying process | Ask about buying process, procurement, and RFPs early (2/20) | Prescribe the typical buying process instead of asking open-endedly (2/20) |

## Steps
1. **Prep.** Research the prospect from the inputs. Write two or three hypotheses about their problem and trigger, and label each one as unconfirmed. List every known attendee and any likely decision-maker who is missing.
2. **Draft the opening.** Write a 30 to 45 second agenda covering purpose, plan and outcome. Frame the call as both sides checking fit. Pick one side of the small talk test for this call.
3. **Build a short question set.** Keep it focused, not a checklist. Include:
   - their situation and goals
   - why now
   - what is holding them back
   - how they handle the process today
   - current and target numbers
   - their ideal outcome
   - what inaction costs them

   Mark the one or two questions where you plan to probe four layers deep.
4. **Plan talk time.** Script the questions so the prospect does most of the talking. Pitch only after you have enough pain and depth. When you do pitch, use their words and focus on their biggest problems.
5. **Plan the close.** Prepare the words to book the next meeting live, name the owners and milestones, and pick the buying process approach you are testing.
6. **Draft the follow-up.** Write a same-day recap template: thank you, summary, agreed next steps and proposal.
7. **Review.** If the user shares a recording or notes, check them against the Strong and Solid rules and list what was missed.
8. **Report.** List which rules were applied, with their weight (N/20). Then name which disagreement is being A/B tested on this call and which side was chosen.

## Never
- Never claim results the user has not measured, such as win rates, close rates or revenue impact.
- Never invent facts about the prospect or customer, including their numbers, pains, stakeholders, timeline or budget.
- Never write a script that pitches the product before the prospect's situation, goals and pain have been explored and confirmed.
