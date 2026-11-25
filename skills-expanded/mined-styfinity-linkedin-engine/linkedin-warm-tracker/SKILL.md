---
name: linkedin-warm-tracker
description: Maintain a one-row-per-person state machine that outputs each person's single next action and due date, sorted by what is due today. Use to run the day's warming and outreach follow-ups so nobody slips through.
argument-hint: "[paste the people in play with last touch + last reply state, or a path to the list]"
---

# LinkedIn Warm Tracker

The day-driver for warming and outreach. One row per person, one next action each, nothing leaks.

## Inputs
- The current list of people in play with their last touch and last reply state (paste the list or give a path): $ARGUMENTS
- The brief (persona, offer, pains) loads automatically.

## Do this
For each person:
1. Read their stage: new / warming / connect-sent / accepted / in-conversation / qualifying / booked / cold.
2. Read their last touch date and last reply state (replied, no reply yet, went quiet).
3. Compute the single NEXT ACTION for that stage. Examples: warming = engage on a recent post; connect-sent (no accept, 4+ days) = withdraw or wait; accepted = send first DM; in-conversation = reply with the next angle; qualifying = book the call; went quiet (7+ days) = one soft re-open then mark cold.
4. Compute the DUE date from the last touch plus the stage cadence. Anything overdue is due today.
5. Sort the table by due date, soonest first, and within today put the warmest stage (qualifying, in-conversation) at the top.

## Output
A table with columns: person, stage, last touch, NEXT ACTION, due. Sorted by due date. Below it, a one-line count of how many rows are due today. End with the single warmest row to action first.

## Rules
- One row per person. Every person always gets a next action, even if that action is "mark cold". Nothing leaks.
- This drives the day. It does not send anything. Drafting a message is /linkedin-first-dm; running /linkedin-humanizer on the draft; hot replies go to /linkedin-reply-triager.
- When the action is to send, sending happens only through the connected CLI/MCP layer on the user's own session or provider key, drafts are shown and approved first, and the 20 actions/day cap applies to new accounts.
- No em-dashes. No guaranteed-result promises.
