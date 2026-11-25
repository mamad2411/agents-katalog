---
name: social-brand-manager
description: Founder brand manager playbook for multi-lane founders
version: 1.0.0
author: Hermes Agent
license: MIT
category: social-media
metadata:
  hermes:
    tags: [brand, social-media, founder-brand, content-strategy, social-media-manager, personal-brand, agency-brand]
    triggers: [build a brand, social media manager, founder brand, brand strategy, content strategy, social media strategy, grow my audience, personal brand, agency brand, content calendar]
    related_skills: [social-media-automation, website-landlord-astro-builder, local-service-websites, business-voice-outreach, humanizer]
---

# Social Brand Manager

Playbook for acting as a founder's social media manager and building a durable personal/agency brand.

## When to Use

User says any of: You are my social media manager, build a brand, grow my audience, content strategy, personal brand, agency brand, I need to post more consistently. Especially when the founder runs multiple revenue lanes.

## The Multi-Lane Founder Model

One personal brand feeds several offers:

| Lane | Example | Content Angle |
|------|---------|---------------|
| Services | Website agency for local businesses | Behind the build, client wins, niche insights |
| Digital assets | Rank-and-rent / website landlord | Traffic proof, niche research, lead-gen mechanics |
| High-ticket systems | AI agents / operating systems | Case studies, systems thinking, transformation stories |

Rule: one founder face, many offers. Each offer gets its own landing page or repo; the social narrative stays personal and consistent.

## Brand Architecture

1. Primary identity: founder name
2. Agency umbrella: service brand
3. Sub-brands: productized offers
4. URL strategy: each sub-brand gets its own site; agency domain ties them together

## Asset Audit (Always First)

Before creating anything, audit:
- [ ] Existing GitHub repos and live sites
- [ ] Domain registrar and DNS status (do not touch live DNS without approval)
- [ ] Existing email addresses configured in Hermes
- [ ] Existing social handles across X, LinkedIn, Instagram, YouTube, TikTok
- [ ] Existing scheduling/automation tooling
- [ ] CRM, calendar, and lead routing setup

## Identity Setup Strategy

Email:
- Prefer branded email at agency domain if DNS can be modified safely
- Otherwise use a dedicated Gmail/Workspace account
- Store credentials in Hermes .env or auth files, never hardcode

Social handles:
- Target consistent handle across platforms: firstnamelastname or agency name
- Use browser automation to check availability and attempt registration
- Phone/email verification usually requires human collaboration; prepare the user to receive codes
- Document claimed handles, passwords, and 2FA setup in a secure note

## Postiz as Command Center

Deploy Postiz for multi-platform scheduling and agent integration. See social-media-automation for tooling details.

- Self-host on Docker via gitroomhq/postiz-app
- Connect X, LinkedIn, Instagram, YouTube, TikTok, Bluesky, Threads
- Use the MCP server or CLI to let agents schedule posts

## Content Strategy

Pillars:

| Pillar | Purpose | Frequency |
|--------|---------|-----------|
| Build in public | Show work, sites, systems | 3x/week |
| Niche education | Teach local SEO, AI agents, lead gen | 2x/week |
| Proof and wins | Traffic, leads, revenue milestones | 1x/week |
| Founder POV | Opinions, lessons, decisions | 1x/week |
| Offer CTA | Direct pitch for services or systems | 1x/week |

Calendar template: see references/brand-architecture-template.md.

## Operating Rhythm

- Weekly: plan next week's posts, batch-create media
- Daily: engage 15-30 min (replies, DMs, comments)
- Monthly: review analytics, adjust pillars, surface best performers as long-form content

## Pitfalls

- Do not create social accounts before defining brand architecture
- Do not deploy scheduling tools before accounts exist
- Do not start posting before an offer landing page is live
- Do not post mock data or unverified claims
- Do not touch live DNS or email without explicit approval
- Do not set up engagement bots before organic posting rhythm is established

## Verification Checklist

- [ ] Asset audit documented
- [ ] Brand architecture decided and written down
- [ ] Email account configured and tested
- [ ] Core social handles claimed
- [ ] Postiz deployed and integrations listed
- [ ] Content pillars and 30-day calendar drafted
- [ ] First week of posts scheduled or published
- [ ] Landing page or repo for primary offer is live

## Related Skills

- social-media-automation — Postiz, instagrapi, InstaPy, Remotion tooling
- website-landlord-astro-builder — build rank-and-rent sites
- local-service-websites — generate local service business sites
- business-voice-outreach — calibrate writing to founder's voice
- humanizer — strip AI-isms from drafted posts