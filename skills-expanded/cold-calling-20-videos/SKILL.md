---
name: cold-calling-20-videos
description: Builds cold call openers, scripts, first-30-second handling, and meeting-booking asks from rules weighted by how many of the 20 most-watched cold calling videos repeat each one, and flags the choices where experts disagree so you A/B test them instead of guessing. Use when the user says "write my cold call script", "help me with my cold call opener", "how do I handle the first 30 seconds", "book more meetings by phone", "cold calling objections", or "fix my cold calls".
author: Yonathan Cohen (Tool Monsters)
version: 1.0.0
updated: 2026-09-14
license: MIT
---

# /cold-calling

This skill is built from the transcripts of the 20 most-watched videos on cold calling from the last 6 months (since 2026-03-14). Together they have 943,342 views and 80,940 words. From them, 452 pieces of advice were extracted, and 412 were kept because their verbatim quote was found in the transcript, grouped into 203 distinct themes. The number next to each rule is how many of the 20 videos say it. Sources are in sources.md.

The most repeated rule reached 7 of 20. Treat weights as odds, not laws.

## Inputs
1. What you sell, your price or deal size, and any free trial, sample, or demo you can actually offer.
2. Who you are calling: role, industry, and any facts about them you have verified (for example, a visible problem like no website on Google).
3. The meeting you want: length, format, and the real days and times you are free.
4. Results you have measured yourself: call logs, conversion rates, customer outcomes.

Refuse to invent prospect facts, pain numbers, customer results, or conversion rates the user has not provided.

## The rules, by weight
### Strong (5 to 7 of 20)
- **Sound calm and conversational, not enthusiastic or salesy.** (7/20)
- **Ask for a short time window before pitching.** (6/20) One example: "I know I'm catching you out of the blue here, but do you mind if I grab half a minute, tell you why I called, and you can tell me if it's even in your world?"
- **Propose specific meeting days and times.** (6/20) Offer exact slots like "4:00 p.m. or 5:00 p.m.", not "sometime next week."
- **Frame the meeting as no-obligation service, not sales.** (5/20) One example: "This is not an attempt to pitch you. This is about getting you clarity."
- **Push through early brush-offs and not-interested responses.** (5/20) One video says expect 3 to 4 no's before a yes.
- **Treat calling as a numbers game and increase volume.** (5/20) Examples given ranged around 100 calls to 1 or 2 sales.

### Solid (4 of 20)
- **Tell their problem story instead of pitching features up front.** (4/20)
- **Quantify their pain and competitor gap in dollars.** (4/20) Example math from one video: 9 missed calls x $300 x 12 = $32,000 a year. Use only the prospect's real numbers.
- **Offer a free trial, sample, or demo to remove risk.** (4/20) Example: 2 weeks free, then $97 a month.
- **Diagnose their pain before pitching.** (4/20) One formula: acknowledge the pain, offer a specific solution, gauge interest.
- **Keep dialing through rejection without dwelling on it.** (4/20)

### Mentioned (3 of 20)
Avoid generic or vague cliché openers · Acknowledge your call is an out-of-the-blue interruption · Don't over-research; just start dialing · Speak as an equal peer; never apologize or beg · Follow up across multiple channels · Send confirmations and reminders to prevent no-shows · Directly ask to book the meeting on the spot · End calls politely and briefly when they decline · Open with a specific visible problem · Use confident downward inflection · Acknowledge objections before responding · Research prospects thoroughly before calling · Give pricing only when asked · Pre-build the offer or demo before pitching · Log every call and outcome · Block a fixed daily cold calling window

## Where the experts disagree: do not pick, test
| Choice | Side A | Side B |
|---|---|---|
| Permission at the start | Ask for a short time window before pitching (6/20) | Don't ask for time or permission at call start (2/20) |
| Research before calling | Don't over-research; just start dialing (3/20) | Research prospects thoroughly before calling (3/20) |
| Opener style | Avoid generic or vague cliché openers (3/20) | Open with name, company, and "How you doing?" (2/20) |
| Opener content | Avoid generic or vague cliché openers (3/20) | Open with name, company, and what you do (2/20) |
| Small talk | Compliment their work to build rapport before pitching (2/20) | Go straight for the meeting without small talk (2/20) |

## Steps
1. Collect the inputs. If a prospect fact, pain number, or result is missing, ask for it or leave a clearly marked blank.
2. Write the opener: a calm, conversational tone, a request for a short time window (or the no-permission version if that is the side being tested), and one specific, verified problem if the user has one.
3. Write the first 30 seconds: diagnose their pain with a question or two, tell their problem story, and quantify the cost in dollars only with numbers the user supplied.
4. Write the ask: frame the meeting as no-obligation service, propose two specific days and times, and mention a free trial, sample, or demo only if the user actually offers one.
5. Write brush-off and objection lines: acknowledge first, then respond, with one or two follow-up attempts after an early "not interested", and a short, polite close when they clearly decline.
6. Set up the routine: a daily volume target, a fixed calling window, a call log with outcomes, and confirmations and reminders for booked meetings.
7. Pick one disagreement from the table to A/B test. Run each version for the same number of calls and compare results from the call log.
8. List which rules were applied with their weight (for example, "Sound calm and conversational, 7/20"), and name the choice being A/B tested with both sides.

## Never
- Never claim results, conversion rates, or benchmarks the user has not measured. Label any figure from the videos as coming from the videos.
- Never invent facts about the prospect or customer, including their tools, problems, missed calls, or revenue.
- Never script a false pretext or fake familiarity, such as "following up on our last chat" when there was none, to get past the first 30 seconds.
