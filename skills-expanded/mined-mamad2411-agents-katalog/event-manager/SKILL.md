# Event Manager

Plan, organize, and follow up on events - meetups, hackathons, conferences, and online events.

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| Calendar | Create events, send invites |
| Notion | Track event planning and logistics |
| Canva | Create event graphics and banners |

## Event types

| Type | Typical lead time | Key deliverables |
|------|-------------------|-----------------|
| **Meetup** (hosted) | 3-4 weeks | Venue, speakers, event page, promotion, follow-up |
| **Hackathon** (hosted) | 6-8 weeks | Theme, judges, prizes, registration, logistics |
| **Conference talk** | 4-6 weeks | CFP submission, slides, demo prep |
| **Webinar / online** | 2-3 weeks | Registration page, slides, recording setup |
| **Sponsorship** | Varies | Brief, assets, booth materials |

## Process

1. **Create event brief** - save to `events/_drafts/YYYY-MM-DD_event-slug.md`
   - Event name, date, type, audience
   - Goals (leads, community, brand awareness)
   - Budget estimate
   - Deliverables checklist
2. **Plan logistics** - venue, speakers, sponsors, registration
3. **Create content** - event page copy, social promotion, email invites
   - Use the relevant content skills (linkedin, blog, email-writer)
4. **Pre-event checklist** - run through 1 week before
   - Slides reviewed
   - Demo tested
   - Promotion sent
   - Registration confirmed
5. **Post-event** - within 48 hours
   - Follow-up email to attendees
   - Content recap (blog post or LinkedIn)
   - Update `events/_insights.md` with what worked
   - Log leads in CRM

## Guardrails

- **Never commit budget** without the CAO's approval
- **Never book venues or sign contracts** - present options for the CAO to decide
- **Drafts only** for all outbound communication (invites, promotion, follow-ups)
- **No attendee PII** in public content - names only with permission
- **Log all events** in `events/_published/` after they happen

## Self-improvement

After an event is completed:

1. Move the event brief from `events/_drafts/` to `events/_published/`
2. Update `events/_insights.md` with what worked: attendance, engagement, lead quality, logistics that went well or poorly
3. If the CAO's edits to event briefs or follow-ups reveal a new pattern (e.g. "always include a networking segment", "keep talks to 20 min max"), add it to the Process section
4. If an event format performs well, save the brief and follow-up to `events/_examples/` as a reference template
