---
name: reach-outreach-rules-check
description: Lists the rules questions one message raises, with the channel, where the recipient is and what kind of address it is, the questions each official page raises, what is unknown and the questions to take to an adviser. Use for "run reach-outreach-rules-check", "outreach rules check", "is cold email legal", "CAN-SPAM", "cold email GDPR", "can I email this person", "anti-spam rules", "outreach compliance questions", part of the Claude Guide for Outreach Pack by 90n.
---

# Outreach Rules Check

## When To Use
You write across borders and do not know which rule applies. This does not tell you what the law is. It answers a narrower question: for this message, to this person, in this place, which questions do the official pages raise, and which of them can I not answer?

## When Not To Use
This is not legal advice and gives no verdict of "compliant". If you send in volume, run a newsletter or use bought lists, you are outside what this guide is for: check with a qualified adviser before you send anything. For the quality of the message, use Message Checklist.

## Inputs
- The message as you will send it, and the channel: email, a platform message, a phone call.
- Where the recipient works, as far as a public source says, and where you are.
- The kind of address or number: a company address, a sole trader's, a personal one, or unknown.
If you have none of this, I start from the channel and the country and mark most answers "unknown".

## Approach
Official guidance read as questions, not answers. Each row comes from a public page: the US Federal Trade Commission's CAN-SPAM compliance guide, the UK Information Commissioner's Office page on business-to-business marketing, the Government of Canada's anti-spam legislation site, the French regulator CNIL's page on prospecting by electronic mail as one example from the European Union, and LinkedIn Help on prohibited software. Pages change, countries differ and most are not covered here. Every point: check with a qualified adviser. The failure it prevents is assuming that because a message is one to one and polite, no rule applies.

## Workflow
1. Ask at most three questions: the channel, where the recipient is, and what kind of address or number you are using.
2. Record the three facts and the source for each. "Unknown" stays unknown; whether an address belongs to a company or a sole trader often cannot be seen from outside, and that changes the questions.
3. Ask, about your own message, the questions each page raises. From the US guide: does it say who you are, is the subject line truthful, is there a plain way to say stop and how fast will you act on it. From the UK page: is this a company address or a sole trader's, and has this person objected before. From the French page: is the person told who is writing, can they object simply, does the message relate to their job.
4. Ask the consent question as a question, as the Canadian site and others raise it: does this place expect consent or another basis before a first message, for this kind of address? I record the question and the page, never a conclusion.
5. Ask the platform question: does the platform's own rule allow how this will be sent? Anything automated on LinkedIn is not allowed by its published rules.
6. Answer each with yes, no or unknown about your message only, with the page the question came from.
7. Turn every "unknown" and every "no" into a question for an adviser, in plain words.

## Output Format
```markdown
# Outreach Rules Check
Message to: [name, role] | Channel: [email / platform message / call] | Checked: [date] | This is a list of questions, not legal advice
## The facts
| Fact | Answer | Source |
|---|---|---|
| Where the recipient works | [country, or unknown] | [link] |
| Kind of address or number | [company / sole trader / personal / unknown] | [how you know] |
## Questions the official pages raise
| Question about your message | Yes, no or unknown | Official page the question comes from |
|---|---|---|
| Does it say who you are? | [ ] | [page] |
| Is the subject line truthful? | [ ] | [page] |
| Is there a plain way to say stop, and how fast will you act on it? | [ ] | [page] |
| Does this place expect consent or another basis first? | [ ] | [page] |
| Does it relate to the person's job? | [ ] | [page] |
| Does the platform allow how it will be sent? | [ ] | [page] |
## Questions for an adviser
1. [question in plain words]
## Decision
[Your name] decides by [date] whether to send, change the message or ask an adviser first. Check with a qualified adviser.
```

## Done When
- Channel, place and address type are recorded, with "unknown" where true.
- Every question shows the official page it came from.
- No row states what the law requires or says the message is compliant.
- Every "unknown" and "no" appears in the questions for an adviser.

## Quality Bar
- Questions, never conclusions: this skill does not interpret law.
- A country with no page listed here is marked "not covered", not guessed from a neighbour.
- A request to stop is honoured at once, whatever any rule allows.
- Every legal point ends the same way: check with a qualified adviser.
- Claude lists the questions; you decide whether to send, and nothing is sent for you.

## Next
Run reach-run-of-ten (Run of Ten Plan) to place this message in this week's small run.

## About the makers

This pack is made by 90n ([90n.ai](https://90n.ai)): AI-native ways of working and tools for Product, Marketing and HR teams, built by ex-McKinsey founders. We map where time and money leak, redesign the work around AI and stay until your people run it themselves, and we run our own company on Claude. If your team has outgrown the self-serve version, message Pauline (linkedin.com/in/paulinebertry).
