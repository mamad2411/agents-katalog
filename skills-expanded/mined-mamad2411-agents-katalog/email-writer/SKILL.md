# Email Drafting Skill

```yaml
name: email-writer
description: >
  Drafts emails in the user's authentic voice and tone. Handles replies,
  cold outreach, follow-ups, introductions, and internal communication.
  Used by zero-inbox and any email drafting task.
triggers:
  - draft an email
  - reply to this email
  - write an email
  - email response
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Gmail | Send drafted emails |

## Greetings

Match formality to the relationship:

<!-- Customize: add columns for each language the CAO writes in. Run /sylph-setup-skill email to auto-configure. -->

| Relationship | English | [Other language] |
|-------------|---------|--------|
| Friends / close peers | "Hey [name]," | [casual greeting] |
| Colleagues / warm contacts | "Hi [name]," | [warm greeting] |
| Prospects / cold contacts | "Hello [name]," | [formal greeting] |
| Formal / unknown | "Dear [name]," | [formal greeting] |

**Always follow the greeting with a warm opener:**
- English: "Hope you're doing well!"
- [Other language]: [equivalent warm opener]

Never skip the opener. It bridges the greeting and the body.

---

## Closings

<!-- Customize: match language columns to your Greetings table above. -->

| Context | English | [Other language] |
|---------|---------|--------|
| Warm / friendly | "Best," | [warm closing] |
| Professional | "Thanks," | [professional closing] |
| After a request | "Thanks in advance," | [request closing] |
| Formal | "Kind regards," | [formal closing] |
| Internal / quick | "Cheers," | [casual closing] |

---

## Structure Pattern

Every email follows this three-part structure:

### 1. Acknowledge
Reference the context: what they said, what happened, or why you're writing.
- Reply: "Thanks for sending this over."
- Cold: "I came across [specific thing] and wanted to reach out."
- Follow-up: "Just circling back on our conversation from [date]."

### 2. Answer / Content
The substance of the email. Keep it tight:
- One main point per paragraph
- If there are multiple items, use bullet points
- If there's a question, answer it directly before adding context

### 3. Next Step
Always end with a clear next action:
- "Let me know if [specific question]."
- "Want to jump on a quick call this week?"
- "I'll send the doc by Friday."

Never end an email without a next step. Even "No action needed on your end" is a next step.

---

## Language Matching

**Match the language of the thread.** If the incoming email is in French, reply in French. If it is in English, reply in English. If the thread switches languages, follow the most recent message.

Do not ask the user which language to use. Just match.

---

## Presentation Rules

- **Plain text only.** Never wrap drafts in blockquotes (`>`), code blocks, or italic formatting.
- **Copy-pasteable.** The draft should be ready to paste directly into an email client.
- **No subject line unless asked.** If replying, the subject already exists.
- **For new emails**, suggest a subject line separately above the body.

---

## Storage Rule

**Email drafts go to the email client only, never to the repo.**

Do not save email drafts to `content/` or `_drafts/` folders. Emails are ephemeral and belong in the email tool (Gmail, Outlook, etc.) or in the conversation. The only exception is outbound campaign templates, which go in `sales/outbound/campaigns/`.

---

## Tone Calibration

- Write like a real person, not a bot
- Short sentences. Get to the point.
- Confident but not pushy
- Warm but not sycophantic
- Match the energy of the sender (casual thread = casual reply)

---

## What NOT to Do

| Don't | Why | Do Instead |
|-------|-----|------------|
| Start with "I hope this email finds you well" | Cliche, robotic | Use the standard opener for the relationship |
| Write paragraphs longer than 3 sentences | Nobody reads long email paragraphs | Break it up or use bullets |
| Use "per my last email" | Passive-aggressive | Reference the specific point directly |
| CC people without reason | Creates noise | Only CC people who need to act or be informed |
| Use em dashes (--) | Formatting rule | Use hyphens (-) or colons (:) |
| End without a next step | Leaves the thread hanging | Always state what happens next |
| Use "please do the needful" | Dated and unclear | Be specific about what you need |
| Over-apologize | Undermines confidence | Acknowledge once, then move forward |
| Write "As per our discussion" | Stiff | "Following up on our chat" or just reference the topic |
| Add a signature block | The email client handles this | Just end with the closing |
| Save drafts to the repo | Emails are ephemeral | Send via email tool or present in conversation |
| Invent a tone the user hasn't used | Feels off-brand | Match previous emails from the user |

## Self-improvement

After the CAO edits an email draft before sending:

1. Diff what was drafted vs what she sent - identify patterns in her edits to tone, structure, or phrasing
2. If her edits reveal a voice rule not captured here, add it to the Tone Calibration or What NOT to Do sections
3. If she consistently rewrites openers, closings, or CTAs in a specific way, update the Structure section
4. Update `.claude/MEMORY.md` if the pattern applies across channels (not just email)
5. Note: email drafts don't go to `_published/` (they're ephemeral), but the rules learned still update this skill file
