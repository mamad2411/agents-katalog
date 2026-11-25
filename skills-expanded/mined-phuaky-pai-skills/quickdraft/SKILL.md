---
name: QuickDraft
description: Platform-aware message drafting with tone control. USE WHEN draft, write reply, rewrite, message, WhatsApp, email.
---

# QuickDraft

Fast, context-aware drafting for any platform with proper formatting.

---

## Trigger Phrases

- "draft a reply"
- "write a message"
- "rewrite this"
- "make it shorter"
- "break it up for WhatsApp"
- "draft an email"
- "write a thank you"

---

## Platform Formats

### WhatsApp Style
```
- Short chunks (1-3 sentences max per message)
- Conversational tone
- Use line breaks between thoughts
- Emojis sparingly (if appropriate)
- No formal greetings/closings
```

**Example:**
```
Hey!

Thanks for coming yesterday

A few people asked for the slides - here they are:
[link]

Lots of hands went up for more workshops - we're on it
```

### Email Style
```
- Subject line included
- Proper greeting
- Body in paragraphs
- Clear call-to-action
- Professional sign-off
```

**Example:**
```
Subject: Following up from yesterday's workshop

Hi [Name],

Thank you for attending yesterday's Claude Code workshop.

As requested, here are the slides: [link]

We noticed strong interest in follow-up workshops. We're currently planning the next sessions and will share details soon.

Best,
Kuan
```

### X/Twitter Style
```
- Hook in first line
- 280 char limit per tweet
- Thread format if needed
- No hashtags (unless requested)
- Direct, punchy
```

### Slack Style
```
- Concise
- Use bullets
- @mentions where needed
- Thread-friendly
- Action items clear
```

---

## Tone Controls

| Tone | Use For |
|------|---------|
| **Casual** | Friends, community, WhatsApp |
| **Professional** | Clients, formal emails |
| **Warm** | Thank yous, appreciation |
| **Direct** | Action items, requests |
| **Persuasive** | Sales, pitches |

---

## Workflow Routing

| Trigger | Action |
|---------|--------|
| "for WhatsApp" | Break into chunks, casual |
| "email to [client]" | Professional, structured |
| "thank you message" | Warm tone |
| "follow-up" | Direct, action-oriented |
| "rewrite shorter" | Compress while keeping meaning |
| "rewrite better" | Improve clarity and impact |

---

## Quick Commands

### Shorten
Input: Long text
Output: Same meaning, fewer words

### Chunk (WhatsApp)
Input: Long message
Output: Multiple short messages

### Formalize
Input: Casual text
Output: Professional version

### Casualize
Input: Formal text
Output: Conversational version

---

## Context Awareness

When drafting, consider:
- **Who:** Relationship with recipient
- **Platform:** WhatsApp/Email/X/Slack
- **Purpose:** Thank/Request/Update/Sell
- **Tone:** Casual/Professional/Warm

---

## Examples

### Request: "draft a thank you for the event attendees"

**WhatsApp version:**
```
Thanks so much for coming yesterday!

Hope you found the session valuable

Slides are here: [link]

Lots of interest in more workshops - we're planning them now
```

**Email version:**
```
Subject: Thank you for attending the Claude Code workshop

Hi everyone,

Thank you for joining us yesterday for the Claude Code workshop. Your engagement and questions made it a great session.

As promised, the slides are available here: [link]

Based on the strong interest, we're planning additional workshops. Stay tuned for details.

Best,
Kuan
```

---

## Integration

- **MeetingProcessor:** Draft follow-ups from meeting summaries
- **XPoster:** Optimize drafts for X posting
- **FounderOps:** Generate client communications
