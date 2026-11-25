# Newsletter Writer

```yaml
name: newsletter-writer
description: >
  Writes short-form email newsletters. Optimized for open rates,
  click-throughs, and subscriber retention.
triggers:
  - newsletter
  - email newsletter
  - weekly update email
```

---

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Email platform | Send newsletter (e.g., Mailchimp, Substack, ConvertKit) |

## What Works

- **Short.** 200-400 words max for the main content. Readers skim email.
- **Hook-first.** The first sentence after the subject line determines if they keep reading.
- **One CTA.** Every newsletter has exactly one primary call-to-action. Don't split attention.
- **Consistent structure.** Readers should know what to expect each time.
- **Personal tone.** Write like you're emailing one person, not broadcasting to thousands.
- **Value upfront.** The best newsletters give the takeaway in the email, not behind a click.

## What Doesn't Work

- Long intros before getting to the point
- Multiple CTAs competing for attention
- Generic "this week in [industry]" roundups with no POV
- Formal language ("Dear subscriber")
- Walls of text without formatting

---

## Subject Line Discipline

The subject line is the most important line. Rules:

- **Under 50 characters** (renders fully on mobile)
- **Specific over clever.** "3 things that broke our pipeline" beats "Newsletter #47"
- **No ALL CAPS or excessive punctuation**
- **Preview text (preheader)** should extend the subject, not repeat it

| Good Subject | Bad Subject |
|-------------|------------|
| "We tested 5 tools. One stood out." | "Weekly Update #23" |
| "The metric nobody tracks (but should)" | "Important News Inside!" |
| "What I got wrong about [topic]" | "Don't Miss This!!" |

---

## Newsletter Structure

```
[Subject Line]
[Preheader text - extends the subject]

[Greeting - casual, first name if available]

[Hook - 1-2 sentences, the reason to keep reading]

[Body - the substance, 2-4 short paragraphs or bullet points]

[CTA - one clear action: read, try, reply, register]

[Sign-off - brief, personal]

[P.S. - optional, for a secondary link or personal note]
```

---

## Formatting Rules

- Short paragraphs: 2-3 sentences max
- Use bold for key phrases readers need to catch while scanning
- Bullet points for lists
- One link per CTA (don't scatter links everywhere)
- P.S. lines get read more than body text - use them strategically

---

## Self-Improvement Step

After each send:

1. Record open rate, click rate, and unsubscribe count in frontmatter
2. Compare subject line patterns: which styles drive opens?
3. Compare CTA patterns: which placements drive clicks?
4. Update `content/newsletter/_insights.md` with findings
5. Promote high-performing issues to `content/newsletter/_examples/`
