# Create Outbound Campaign

Build targeted outbound campaigns from ICP definition through personalized sequences.

## MCP connectors

| Connector | Purpose |
|-----------|---------|
| CRM | Import leads, track campaign performance |
| LinkedIn | Research targets, send connection requests |
| Gmail | Send outbound email sequences |

## Process

1. **Define ICP** - who are we targeting?
   - Industry, company size, role, tech stack
   - Pain point we're solving for this segment
   - Why now? (trigger event, market shift, etc.)

2. **Build list** - identify target accounts and contacts
   - Use LinkedIn search for prospecting
   - Cross-reference with Twenty CRM to avoid existing customers
   - Target: 20-50 contacts per campaign batch

3. **Choose channel** - where do we reach them?
   - Cold email: best for VP/C-level, longer messages OK
   - LinkedIn DM: best for peers, keep it short
   - Multi-touch: email + LinkedIn for high-value targets

4. **Write the sequence** - draft 3-4 touch messages
   - Touch 1: Hook + relevance + soft CTA
   - Touch 2: Value add (share content, insight, or data point)
   - Touch 3: Social proof + direct CTA
   - Touch 4: Break-up (last chance, no pressure)
   - Space touches 3-5 business days apart

5. **Personalize** - customize per contact
   - Reference their company, role, or recent activity
   - Use their tech stack or public data as hooks
   - No generic "I noticed your company" - be specific

6. **Save** - `sales/outbound/campaigns/YYYY-MM-DD_campaign-slug.md`
   - Include: ICP definition, contact list, full sequence, personalization notes

## Sequence rules

- **Subject lines**: under 10 words, no caps lock, no spam triggers
- **Email body**: under 150 words per touch
- **LinkedIn DM**: under 100 words
- **Always include opt-out** in emails
- **Use the CAO's voice** - load `email-writer` skill
- **Open with** "Hope you're doing well!" for warm leads

## Guardrails

- **Drafts only** - never send any outbound message directly
- **No pricing** in outbound messages - CTA is always a call or demo
- **No purchased lists** - build lists from research only
- **CRM check** - verify targets are not existing customers before adding
- **No spam** - respect unsubscribe requests and do not contact list
- **Save all campaigns** to `sales/outbound/campaigns/` with proper naming
- **The CAO approves** before any campaign is sent

## Self-improvement

After the CAO reviews and approves a campaign:

1. Move the final version from `sales/outbound/campaigns/` draft to its final location
2. Diff what was drafted vs what the CAO kept - identify patterns in her edits to messaging, targeting, or sequence structure
3. Update `sales/_insights.md` with what worked: which hooks, personalization approaches, or CTAs she kept vs rewrote
4. If her edits reveal a new rule (e.g. "never lead with company size", "always reference a specific trigger event"), add it to the Sequence rules section above
5. If a campaign gets strong reply rates, save it to `sales/outbound/_examples/` with performance annotations
