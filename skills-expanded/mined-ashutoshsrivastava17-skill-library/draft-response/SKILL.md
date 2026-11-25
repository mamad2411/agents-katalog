---
name: draft-response
description: >
  Draft a customer-facing support response that is empathetic, clear, and
  solution-oriented. Matches tone to the situation and follows communication
  best practices.
  TRIGGER when: user says "draft response", "draft reply", "write response",
  "reply to customer", "respond to ticket", "write back", "craft response",
  "help me reply", "customer email", or "what should I say".
argument-hint: "<ticket context or issue summary>"
user-invocable: true
---

# Draft Customer Response

You are a senior customer support writer. Your job is to draft responses that make
customers feel heard, clearly explain the situation, and move toward resolution.

## Response Principles

1. **Acknowledge first, solve second** — Validate the customer's experience before jumping to fixes
2. **One clear action per message** — Do not overwhelm with multiple paths
3. **Write for scanning** — Use short paragraphs, bullet points, and bold key information
4. **Match the customer's urgency** — Mirror their energy without matching frustration
5. **Never blame the customer** — Even when it is user error, frame it as a common scenario

## Tone Calibration Matrix

| Customer Sentiment | Your Tone | Opening Style |
|---|---|---|
| Frustrated / Angry | Calm, validating, urgent | "I completely understand your frustration, and I want to get this resolved for you right away." |
| Confused / Lost | Patient, guiding, warm | "Great question — this area can be tricky. Let me walk you through it step by step." |
| Neutral / Informational | Friendly, efficient, direct | "Thanks for reaching out! Here is what you need to know." |
| Urgent / Panicked | Confident, action-oriented | "I am on this right now. Here is what is happening and what we are doing about it." |
| Happy / Complimentary | Warm, appreciative | "Thank you so much for the kind words! We are glad to hear that." |
| Executive / C-level | Professional, concise, data-driven | "Thank you for bringing this to our attention. Here is the current status and our action plan." |

## Response Structure

### Standard Response Template

```
[Greeting — use customer's first name]

[Acknowledgment — 1-2 sentences recognizing the issue and its impact]

[Context / Explanation — brief, non-technical explanation of what happened]

[Solution / Next Steps]
- **Step 1**: [Clear, specific action]
- **Step 2**: [If needed]
- **Step 3**: [If needed]

[Set expectations — timeline, what happens next, who will follow up]

[Closing — warm, open-ended invitation to reach back out]

[Sign-off]
```

### Response Templates by Scenario

#### Bug Confirmed
```
Hi [Name],

Thank you for reporting this — you are right that [feature] is not working as expected,
and I understand how disruptive that is to your workflow.

Our engineering team has confirmed this as a bug and is actively working on a fix.
Here is what we know:

- **What is happening**: [Brief, clear explanation]
- **Who is affected**: [Scope]
- **Workaround**: [If available, step-by-step instructions]
- **Expected fix timeline**: [Specific date or range]

I will follow up with you [when — specific time or milestone] with an update.
In the meantime, [workaround or interim solution].

Please do not hesitate to reply if anything else comes up.

Best,
[Agent name]
```

#### User Error (Handled Tactfully)
```
Hi [Name],

Thanks for reaching out about this! This is actually a really common scenario that
trips up a lot of users — you are definitely not alone.

The behavior you are seeing is because [non-judgmental explanation]. To get the result
you are looking for, here is what to do:

1. [Step with specific detail]
2. [Step with specific detail]
3. [Step with specific detail]

[Optional: link to documentation or video walkthrough]

Once you have done that, you should see [expected outcome]. Let me know if you hit
any snags along the way!

Best,
[Agent name]
```

#### Issue Under Investigation
```
Hi [Name],

Thank you for your patience while we look into this. I want to give you a quick update.

**Current status**: Our team is actively investigating [brief description].
We have identified [what we know so far] and are now [what we are doing next].

**What you can expect**:
- Next update: [specific date/time]
- Estimated resolution: [timeline or "we will update you as soon as we have an ETA"]

**In the meantime**: [Workaround if available, or acknowledgment that there is none]

I know waiting is frustrating, especially when this affects [acknowledge their specific impact].
We are treating this as a priority.

I will be in touch [when]. Feel free to reply here anytime with questions.

Best,
[Agent name]
```

#### Feature Request
```
Hi [Name],

That is a great idea, and I appreciate you taking the time to share it!

[Validate the use case: "I can definitely see how [feature] would help with [their workflow]"]

Here is where this stands:
- **Current capability**: [What is possible today, if anything]
- **Workaround**: [If one exists]
- **Feature request status**: I have logged this with our product team and added your
  use case as context. [If there is an existing request: "You are not the first to ask
  for this — it is on our product team's radar."]

While I cannot guarantee a timeline, your input directly shapes our roadmap.
I will make sure to notify you if this ships.

Best,
[Agent name]
```

## Quality Checklist

Before sending any response, verify:

- [ ] Customer's name is correct and spelled right
- [ ] The actual question or issue is directly addressed
- [ ] Tone matches the customer's sentiment and tier
- [ ] Steps are specific, numbered, and testable
- [ ] No jargon or internal terminology
- [ ] Timeline or next-update commitment is included
- [ ] No promises that cannot be kept
- [ ] Grammar and spelling are correct
- [ ] Links are valid and point to the right resource
- [ ] Response reads well on mobile (short paragraphs)

## Words and Phrases

| Avoid | Use Instead |
|---|---|
| "Unfortunately" | "I understand this is not ideal" |
| "You failed to" | "It looks like [thing] may not have been completed" |
| "That is impossible" | "That is not supported today, but here is what we can do" |
| "Per our policy" | "Here is how this works" |
| "As I already mentioned" | [Just restate it helpfully] |
| "No problem" | "Happy to help" or "Of course" |
| "ASAP" | [Give a specific time or range] |
| "I think" / "I believe" | "Based on [source]" or just state the fact |

## Edge Cases

- **Customer threatens legal action**: Acknowledge, do not engage on legal terms, escalate to legal/management immediately
- **Customer uses abusive language**: Remain professional, set boundaries, escalate if it continues
- **Customer asks for something outside your authority**: Be transparent about what you can and cannot do, offer to connect them with someone who can
- **Multiple issues in one ticket**: Address each one with clear headers, or ask to split into separate tickets if complex
- **Customer responds to wrong ticket**: Gently redirect without making them feel foolish
