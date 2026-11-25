---
name: acct-reason-to-call
description: Proposes three possible reasons to contact one person, each checked for true and useful, with two or three points per reason, the stock openers to avoid and the reason you choose, without writing the message. Use for "run acct-reason-to-call", "reason to call", "reason to reach out", "what do I say to this contact", "get back in touch with a customer", "not just checking in", "why now for this person", "re-engage a contact", part of the Claude for Account Executives Pack by 90n.
---

# Reason to Call

## When To Use
You want to get back in touch without "just checking in" or pretending you know each other. Run this for one person in one of your accounts. It answers: what do you have that is true and useful to say to this person, before you say anything about your offer?

## When Not To Use
If you have not chosen who to contact yet, run Weekly Call List. If you have your reason and want the words for the call, run Call Talk Track. This skill stops at the chosen reason and its points; it writes no message.

## Inputs
- The person's name, job role and account, and what you have already exchanged.
- One or two recent facts about them or their company, with the source (an announcement, a publication, your notes).
- What you could share that is useful: a lesson from similar work, a resource, an introduction.
If you have none of this, I start from the person's job role and the reason on your call list, and mark the output as a first draft.

## Approach
You get in touch to be useful to the other person, not to place an offer; every fact is sourced; and you go one person at a time, in small runs of about ten. This is a working method described generically, with no public source to cite. The failure it prevents is the generic compliment or the invented familiarity, which the person spots at once and which closes the door for the next real reason.

## Workflow
1. I ask at most three questions: what link you already have with this person, what you know about them from a sure source, and what you could give them without asking for anything.
2. I always propose three reasons, one of each kind. Share: something useful to them with no ask attached. Congratulate: a recent event found in a public source, with the source. Suggest a conversation: a topic you both care about, easy to decline.
3. Each reason passes three checks: is it true, is it useful to them, is the source dated? A reason that is not true for this person is deleted, even if it sounds good, and I say which one went and why.
4. For each reason that survives I write two or three points of a few sentences each. They are about the person's subject and never push your offer.
5. I give one line on the upside and the risk of each reason. You choose; I do not choose for you.
6. I list the stock openers to keep out of whatever you say or write: "just checking in", "I hope this finds you well", "circling back", praise with no fact behind it, false urgency, a first-name warmth you have not earned.
7. I write no subject line, no greeting and no message. You say it or write it in your own words.

## Output Format
```markdown
# Reason to Call
Person: [name, job role] · Account: [name] · Prepared: [date]
## Three possible reasons
| Kind | Reason | True and useful to them? | Source and date |
|---|---|---|---|
| Share | [reason] | [yes or no, why] | [source] |
| Congratulate | [recent event] | [yes or no, why] | [link, date] |
| Suggest a conversation | [shared topic] | [yes or no, why] | [source] |
## Points per reason
- Share: [two or three points]
- Congratulate: [points]
- Suggest a conversation: [points]
## Upside and risk
| Reason | Upside | Risk |
|---|---|---|
| [reason] | [upside] | [risk] |
## Openers to avoid
- [stock phrase] · say instead: [the fact]
## Decision
[You] choose the reason for [name] and the day you call or write, by [date].
```

## Done When
- All three kinds of reason are present, or a deleted one is shown with why.
- Every fact has a dated source.
- No point sells anything.
- The chosen reason is yours, and no message has been drafted.

## Quality Bar
- No invented familiarity: you do not act as if you know each other.
- No invented compliment or event; you speak about what the person published or did, dated, never about who they are.
- One person at a time, in small runs; no variants for a bulk send.
- The reason serves the other person and rests on a true, sourced fact; you write or say it yourself and Claude contacts no one.

## Next
Run acct-call-talk-track (Call Talk Track) to turn the reason you chose into keywords for the call.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
