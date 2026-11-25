---
name: sent-mail-outcome-tracker
description: Read the user's recent cold-outreach sent mail, look up which messages got replies, classify reply sentiment, and produce an outcome report that surfaces what the responders had in common. Use when the user says "did my cold emails get replies," "what's my reply rate," "sent-mail outcomes," "track outcomes," or "/sent-mail-outcome-tracker." Requires a connected Gmail MCP. Read-only. Never contacts recipients.
---

# Sent-mail outcome tracker

The rest of the toolkit asks "is this email well-written?" This skill asks the only question that actually matters: "did the email get a reply, and what did the messages that replied have in common?"

Composes with `voice-update --source sent-mail` (which audits voice files against sent mail). This skill produces outcome data; voice-update proposes voice updates if patterns emerge.

## Why this exists

Two gaps the existing toolkit does not close:

1. **The critic measures rule recall, not response rate.** The eval harness asserts the inline critic catches em-dashes and vague asks. None of that proves the resulting emails get replies. Reply rate is the only metric the recipient cares about, and it is the only one that compounds.
2. **You learn from outcomes, not from the draft.** A draft that passes every rule and gets ignored teaches you something the rules cannot. A draft that breaks a rule and gets a same-day intro teaches you something the rules will never catch. Both signals live in the sent folder and the inbox, not in the rule library.

Auto-tracking every email is out of scope. The user invokes this on demand, the skill reads, the skill reports. The user judges what to change.

## Inputs

Optional arguments:
- **Time window**: default `last 30 days`. Accept "last week," "last 3 months," "since [date]."
- **Count cap**: default `25 messages`. Cap at 50 to keep token cost bounded.
- **Mode filter**: default `cold outreach only`. The skill applies heuristics to exclude:
  - Replies (any message with `In-Reply-To` header or whose thread already has an inbound message from the same recipient before the sent date)
  - Automated mail (auto-replies, calendar invites, no-reply addresses)
  - One-liners under 30 words
  - Messages to recipients already in the user's recent inbound mail (these are warm threads, not cold outreach)
- **Ask-type tag**: optional. "Only meeting requests / intro requests / job inquiries / advice asks." Different ask types have different baseline reply rates and should not be averaged together.

If the user just says "/sent-mail-outcome-tracker" with no args, use defaults and ask whether to narrow the filter before fetching.

## Process

1. **Confirm scope before fetching.** "I'll pull your last 25 cold-outreach messages from the past 30 days, excluding replies, automated mail, and threads where the recipient had already written to you. Sound right?" Adjust if they want different scope.

2. **Fetch via the Gmail MCP.** Query `from:me` in the sent folder for the window, fetch the full thread for each candidate, apply the cold-outreach filters above. For each kept message:
   - Sent date and time
   - Subject
   - Body (skip quoted threads)
   - Recipient role inferred from the email domain and any signature in prior threads (anonymize by role; never quote the name into the report)

3. **For each sent message, look up the reply state from the same thread.**
   - **No reply** if the thread has only the user's outbound message after the sent date, or replies are auto-generated.
   - **Replied** if the recipient sent a message after the user's sent message.
   - For replied messages, capture: days to reply (rounded), reply word count, and a one-sentence sentiment classification.

4. **Classify each reply by outcome category, not by tone.** The categories are user-meaningful, not sentiment-mining.
   - **Meeting accepted**: recipient proposed or agreed to a call/coffee/Zoom.
   - **Intro provided**: recipient forwarded to someone else or named a person to contact.
   - **Substantive engagement**: recipient answered the substantive question or offered information, without proposing a meeting.
   - **Polite decline**: recipient declined but acknowledged the email.
   - **Deferral**: recipient said "let me get back to you" or "later this quarter" with no concrete action.
   - **No reply**: no inbound message in the thread within the window.

5. **Read the current rule library.** Open `points/cold-email-rules.md`, `points/named-failure-modes.md`, `context/voice-and-style.md`, and `context/about-me.md`. Patterns in the outcome data only matter against the current rules.

6. **Compute the headline stats.** Always include:
   - N cold outreach messages in the window
   - M replied, R reply rate as %
   - Outcome distribution by category (count and %)
   - Median and 75th-percentile days to reply, on the replied subset only
   - Reply rate by ask type if the user filtered by ask-type, otherwise show the breakdown
   - **Sample-size caveat:** if N < 10 print "Sample is small, treat the patterns below as suggestive, not conclusive." If N < 5, refuse to compute pattern stats at all and tell the user to wait for more data.

7. **Surface the patterns that correlate with replies.** Compare the replied set against the non-replied set on:
   - **Subject line length** (median word count, replied vs not)
   - **Subject line type** (specific claim, question, name-drop, role-only): count how many of each in each set
   - **Body word count** (median, replied vs not)
   - **Opening move** (time/place reference, question, observation, ask-first): count and reply rate per type
   - **Named connection in body** (yes/no, reply rate per side)
   - **Specific ask** (precise time, place, deliverable) vs vague ask ("would love to chat"): reply rate per side
   - **Days-of-week sent** (reply rate per weekday)
   - **Time-of-day sent** (rounded to morning / midday / afternoon / evening, reply rate per bucket)

   For each dimension, name the gap if there is one. If there is no gap, say so plainly. Do not invent patterns.

8. **Surface what broke.** Among the no-reply messages, identify which `named-failure-modes.md` failure modes are over-represented vs the replied set. "5 of 7 no-replies opened with a credentials dump (`named-failure-modes:credentials-dump`). 1 of 18 replied messages did." Quote one example per failure mode that the no-reply set hit and the replied set didn't, anonymized.

9. **Propose rule changes if the data warrants it.** If a pattern is strong (e.g., subject lines under 6 words reply at 40%, longer ones reply at 8%) and the rule library doesn't reflect it, suggest a diff to `points/cold-email-rules.md`. Wait for explicit approval. Never auto-write. For approved changes, hand off to `voice-update --source manual`.

10. **End with one concrete experiment.** Pick the single highest-EV change the data suggests, name it, and propose how to test it over the next 10 messages. "Next experiment: cut subject lines to 5 words or fewer. Track reply rate on the next 10 cold emails and re-run this skill in 4 weeks."

## Output structure

The report has six fixed sections, in order:

```
## Sent-mail outcome report, <date range>

## Headline
- N: <count> cold-outreach messages
- Replied: <count> (<rate>%)
- Outcomes: meeting <n>, intro <n>, substantive <n>, decline <n>, deferral <n>
- Median days to reply: <number>
- Sample-size note: <if applicable>

## Patterns that correlate with replies
- Subject length: …
- Subject type: …
- Body word count: …
- Opening move: …
- Named connection: …
- Specific ask: …
- Day/time sent: …

## Failure modes in the no-reply set
- <named failure mode>: <count> in no-reply set, <count> in replied set. Example (anonymized): "<quote>"

## Per-message table
| sent | recipient role | subject (truncated) | outcome | days |
|---|---|---|---|---|
| … | … | … | … | … |

## Proposed rule updates (require approval)
- <file path>: <diff>

## Next experiment
<one concrete change to test on the next 10 messages>
```

## What you do NOT do

- Do NOT quote any recipient's name or any private content from their replies. Anonymize recipients by role ("a senior partner at a Series B firm," "a Stanford professor"). Summarize the reply outcome category; do not paste the recipient's words.
- Do NOT auto-write to any file. All proposed rule updates go through diff + approval, same as `voice-update --source sent-mail`. The actual write happens via `voice-update --source manual`.
- Do NOT contact recipients. This skill is strictly read-only over Gmail.
- Do NOT generalize from a sample under 10 messages. If N < 10, mark patterns "suggestive" not "conclusive." If N < 5, refuse to report patterns at all.
- Do NOT count auto-replies (out-of-office, vacation responder, calendar acknowledgments) as replies. They are not signal.
- Do NOT classify by sentiment ("they sounded warm"). Classify by outcome category (meeting, intro, decline, deferral, no reply). Tone is unreliable, outcome is concrete.
- Do NOT include warm threads in the cold-outreach set. If you replied to a recipient who emailed you first, that is a warm thread and goes in a separate bucket.

## Privacy

The skill reads the user's sent mail and the matching inbound threads via the connected Gmail MCP, in the user's own Claude Code session. Nothing leaves the local environment except the model's analysis call. The model sees the message bodies in-context to compute outcome categories; it does not store them outside the session.

Extra precaution options:
- `--no-quotes`: suppress all example quotes in the failure-modes section.
- Lower the count cap (e.g., 10 messages).
- Pre-filter to a specific label or recipient archetype.

## Example

**User:** "/sent-mail-outcome-tracker last 6 weeks"

**Skill:**

1. "I'll pull your last 25 cold-outreach messages from the past 42 days. Excluding replies, auto-mail, and warm threads. Sound right?"
2. (After yes) Fetches via Gmail MCP, applies filters.
3. Looks up reply state per message from each thread.
4. Reads `points/cold-email-rules.md`, `points/named-failure-modes.md`, `context/voice-and-style.md`, `context/about-me.md`.
5. Produces report:

```
## Sent-mail outcome report, 2026-04-10 to 2026-05-22

## Headline
- N: 24 cold-outreach messages
- Replied: 9 (38%)
- Outcomes: meeting 4, intro 2, substantive 1, decline 1, deferral 1
- Median days to reply: 2 (75th percentile: 5)
- Sample-size note: 24 messages is moderate, patterns below are directional.

## Patterns that correlate with replies
- Subject length: replied set median 5 words, no-reply set median 9. Strong signal.
- Subject type: name-drop subjects ("Re: [mutual] mentioned you") replied 5/6. Generic ("Quick question") replied 0/5.
- Body word count: replied set median 95 words, no-reply 165. Specific ask correlates with shorter body.
- Opening move: time/place reference ("Just back from Athens…") replied 4/5. Credentials dump ("I'm an MBA2 at GSB with five years at…") replied 0/4.
- Named connection: with named connection 7/12, without 2/12. Connection presence > 3x reply rate.
- Specific ask: precise (named time, deliverable) 8/15, vague ("would love to chat") 1/9.
- Day/time sent: Tue-Thu mornings 7/13, weekends 0/4. Send on weekday mornings.

## Failure modes in the no-reply set
- credentials-dump: 4 in no-reply, 0 in replied. Example: "I am an MBA2 at Stanford GSB previously at [redacted]…"
- vague-ask: 6 in no-reply, 1 in replied. Example: "would love to chat sometime if you're open"
- generic-personalization: 3 in no-reply, 0 in replied. Example: "I really admire your work at [redacted]"

## Per-message table
| 04-12 | partner, AI VC | "Re: AI infra at GSB" | no reply | n/a |
| 04-14 | head of PM, frontier lab | "5 min on PM hiring?" | meeting | 1 |
| ... |

## Proposed rule updates (require approval)
- points/cold-email-rules.md: add explicit rule "Subject lines: cap at 6 words for cold outreach. Replied set median was 5; no-reply was 9." (waiting for approval)
- points/named-failure-modes.md: bump credentials-dump severity from medium to high. Current data: 4/4 with this pattern got no reply.

## Next experiment
Cut subject lines to 5 words or fewer for the next 10 cold emails. Re-run this skill in 4 weeks. Target: lift reply rate from 38% to 50% on the next cohort.
```

6. Per proposed update: "Want me to apply (a) the subject-length rule and (b) the credentials-dump severity bump?"
7. For each yes, hand off to `voice-update --source manual` to write the file. Echo back what changed.
