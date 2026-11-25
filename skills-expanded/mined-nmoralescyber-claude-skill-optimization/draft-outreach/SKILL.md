---
name: draft-outreach
description: Researches a sales prospect (person + company) then drafts personalized outbound outreach (cold email, LinkedIn message, follow-up sequence). Always researches first — never sends generic templates. Make sure to use this skill whenever the user says draft outreach to [person/company], write a cold email to [prospect], reach out to [name at company], send a connect note to [LinkedIn person], or describes wanting to contact a prospect they don't have a relationship with yet. Works standalone with web search; supercharged when CRM (Close, HubSpot), enrichment (Clay, ZoomInfo), or LinkedIn connectors are connected. Do NOT use for: replies to existing customers (use customer-support:draft-response), marketing content for a broad audience (use marketing:draft-content), internal team messages (use product-management:stakeholder-update), or legal/formal contractual correspondence (use legal:legal-response). Defining characteristic: "outbound to a named individual who is not yet a customer."
---

# Draft Outreach

Researches a sales prospect then drafts personalized outreach.

## When to use vs. adjacent skills

| Use this skill when... | Use a different skill when... |
|---|---|
| Reaching out to a named prospect who is NOT yet a customer | Replying to an existing customer → `customer-support:draft-response` |
| The outreach is 1:1, personalized | The content is for a broad audience (newsletter, blog) → `marketing:draft-content` |
| The audience is external (prospect company) | The audience is internal team or stakeholders → `product-management:stakeholder-update` |
| Goal is to start a sales conversation | Goal is contractual / regulatory / formal legal → `legal:legal-response` |

## Research-first principle

Never draft outreach without researching the prospect first. Templates are noise. Research surfaces the angle that makes the message worth opening.

**Research depth tiers (pick based on deal size):**

- **Quick (5 min)** — LinkedIn profile, company About page, last funding announcement. For volume outreach to a similar ICP.
- **Standard (15 min)** — Above + recent posts (last 30 days), 2-3 LinkedIn comments by them, news mentions, ICP fit signals from website (tech stack, hiring, customer logos).
- **Deep (45+ min)** — Above + podcast/conference appearances, GitHub if technical, board/investor connections, recent product changes from changelog, mutual connections worth name-dropping. Reserved for strategic accounts.

## Personalization layer (what makes it not look like a template)

Every message must include AT LEAST ONE of:

1. **Specific reference** to something they posted, said, shipped, or were quoted on (with date or context)
2. **Named mutual connection** ("Sarah at AcmeCorp mentioned...") — only if true and the connection is OK with it
3. **Specific signal about their company** ("Saw you're hiring 3 SecEng roles — usually means...")
4. **Insight tied to their problem space** that demonstrates you've actually thought about their world, not just your pitch

If you can't fit one of these, you don't have enough research. Go back.

## Message structure (cold email)

```
Subject: [Hook tied to their world, not your product]

[Personalized opener — references the specific thing from research, 1-2 sentences]

[Bridge to relevance — why you're reaching out, what triggered this, 1-2 sentences]

[Value or insight — give before asking. A specific observation, a benchmark, an offer, 1-3 sentences]

[Soft CTA — low-friction next step. NOT "30-min demo". Try "worth a 10-min call to compare notes?" or a specific async question]

[Sign-off, name, title]
```

Length: under 120 words. Mobile-readable. No images. No tracking pixels in cold email (kills deliverability).

## Subject line discipline

Skip:
- ALL CAPS
- Emojis (unless brand voice supports)
- "Quick question" / "Following up" / "Touching base" — flagged as spam by both filters and humans
- Personalization tokens that look like personalization tokens ("Hey {{first_name}}!")

Try:
- Questions tied to their context ("How are you handling [specific problem]?")
- Specific benchmarks ("Most SOC 2 audits take 6 months — yours?")
- Curiosity gaps ("Saw your post on [topic] — quick thought")
- Mutual connection name when permission given ("[Name] suggested I reach out")

## Sequence design (when multi-touch)

Default cadence (adjust per segment):
- **Touch 1 (Day 0)** — Email, the researched-and-personalized version above
- **Touch 2 (Day 4)** — LinkedIn connect with personalized note
- **Touch 3 (Day 9)** — Follow-up email with NEW value (not "just bumping this") — share a relevant resource, benchmark, or insight
- **Touch 4 (Day 18)** — Different channel (Twitter reply, comment on their post, etc.)
- **Touch 5 (Day 30)** — Final email with explicit "should I close the loop?" — gives permission to say no, often gets a response

Stop the sequence the moment they reply (positive or negative).

## Output

Always produce:
1. Research summary (3-5 bullets) — what you found that informs the angle
2. The drafted message
3. Subject line + 2 alternatives
4. Suggested follow-up cadence
5. CRM note suggestion (1 line for logging the touch)
