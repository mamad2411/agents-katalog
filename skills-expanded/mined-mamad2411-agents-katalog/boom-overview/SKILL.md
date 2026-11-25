---
name: boom-overview
description: Use when the user is new to Boom, asks "what is Boom", "how does Boom work", "what can I do with Boom", wants a tour of the platform's objects (initiatives, journeys, templates, segments, CDP, extraction), or when it's unclear which Boom skill applies to their request. Orientation and router — read this first, then hand off to the specific skill.
---

# Boom Overview

Boom is **infrastructure for AI conversations with your customers**. One central agent per organization, briefed from your knowledge base, does the talking; you configure what each conversation is for and who it reaches.

That covers a lot of jobs with the same pieces: winning back customers who dropped off, support, product research, onboarding and activation, qualifying leads, collecting documents or data, NPS follow-up, drip sequences. The agent handles the conversation end to end and escalates the rare ones that need a person.

**Channels.** WhatsApp is the conversational one: the agent replies, and handles images, voice notes and location. Email is outbound only for now, a send step inside a flow, with no reply loop back to the agent.

## Tools used

| Tool | Purpose | Scope |
|---|---|---|
| `initiatives_list` / `initiatives_get` | See what's already running | read |
| `whatsapp_numbers_list` | The org's WhatsApp sender numbers | read |
| `templates_list` | Pre-approved opening messages | read |
| `segments_list` / `segments_catalog` | Saved audiences + filterable attributes | read |
| `journeys_list` | Message workflows behind initiatives | read |

All read-only — safe to call while orienting. Tool names follow `domain_action`; if a call fails with `tool_not_found`, list available tools and match by that pattern.

## The object model — 60 seconds

```
Segment / CSV / API  ──►  Participants  ──►  Initiative  ──►  Insights & reports
       (who)                (enrolled)      (the campaign)      (what you learned)
                                  │
                          Journey (workflow: which template,
                          when to follow up, when the AI converses)
                                  │
                          WhatsApp Template (pre-approved opener)
```

- **Initiative** — one mission. Carries its `objective`, a Markdown `context` briefing the agent, guiding questions, and lifecycle (`DRAFT → ACTIVE → COMPLETED`). Everything hangs off it.
- **Participant** — one person enrolled in one initiative. No global list, no delete (stopping retains data).
- **Journey** — the workflow graph behind the initiative (send template → wait → AI conversation → follow-ups). A new initiative starts **without one**; you **author and publish it via MCP** (create draft → add/connect nodes → validate → publish) or build it in Boom's visual builder — both act on the same graph.
- **Template** — a WhatsApp opener pre-approved by Meta (~24–48h review). Required to start any WhatsApp conversation.
- **Segment / CDP** — persons, custom objects, and events; segments are saved filters that define WHO an initiative reaches.
- **Extraction schema** — the typed fields (yes/no, number, choice, free text) the initiative pulls out of its conversations. This is how talk becomes structured data you can export or segment on, for any kind of conversation.

## Lifecycle of a typical project

1. **Prepare context** — brand voice + product knowledge the agent speaks with → `build-knowledge-base`
2. **(Optional) sync your data** — connect a database/Shopify so audiences stay fresh → `connect-your-data`
3. **Define the audience** — query the CDP, build a segment → `cdp-and-segments`
4. **Create the initiative** — objective, context, guiding questions → `launch-initiative`
5. **Get the opener approved** — WhatsApp template → `whatsapp-templates` (or an email template, no approval needed → `email-templates`)
6. **Shape the workflow** — follow-up rounds, branching, timing → `design-journey`
7. **Enroll & launch** — add participants, start outreach → `launch-initiative` / `manage-participants`
8. **Read the results** — summaries, transcripts, themes → `analyze-results`

## When a customer writes first, no initiative involved

Inbound has no authoring skill because there's nothing to author: when a customer messages your WhatsApp number without being enrolled anywhere, the same central agent answers with the same knowledge base, and can escalate to a person at any point, same as in outreach. There's no journey, no trigger, no first message someone designed, it starts because the customer decided to write. Whether it answers at all is a per-channel setting with an org-level fallback, configured in the Boom app; with no answering agent configured, the message is stored and nothing replies, by design. Don't route a support-shaped ask to `launch-initiative`, that skill starts a *new* mission with its own audience and trigger, which is the wrong shape for a conversation that already started itself. Read one back the same way `analyze-results` reads any conversation.

## Which skill do I need?

| The user wants to… | Skill |
|---|---|
| Understand Boom / decide what's possible | this one |
| Prepare brand/agent context for Boom | `build-knowledge-base` |
| Connect a Postgres/MySQL/Shopify data source | `connect-your-data` |
| Find people, build or refresh an audience | `cdp-and-segments` |
| Create & launch a new initiative, whatever the job | `launch-initiative` |
| Write or fix a WhatsApp opening message | `whatsapp-templates` |
| Build, publish or send an email template | `email-templates` |
| Create, edit or launch a Lead Capture pop-up on a website, or read its leads | `lead-capture` |
| Design follow-up rounds, branching, timing | `design-journey` |
| Hold sends for review, approve or reject drafts | `design-journey` ("Hold sends for approval") |
| Add/stop/inspect people in a running initiative | `manage-participants` |
| Summarize what an initiative learned | `analyze-results` |
| A customer wrote in first, no campaign involved | this one, see above; there's no authoring skill for it |

## Permissions & guardrails

- Reading and authoring work for any member of the organization. **Outreach writes** — adding participants, launching, canceling — require the signed-in user to be an **org admin**.
- Launching messages **real customers**. Always confirm with the user before `initiatives_launch` or `initiatives_participants_add`.
- **Do Not Contact is enforced server-side** — suppressed people are silently skipped; never work around it.
- Spanish-first: >98% of production initiatives run in Spanish (`language: "es"` is the default). Phone numbers are E.164 (`+5215512345678`).
- Two things the customer sees that this API doesn't cover: the **shared inbox**, where a person takes over an escalated conversation, and the **knowledge base** that briefs the agent. Send them to the Boom app for those rather than inventing tools.

See [`CONTEXT.md`](../../CONTEXT.md) for the full domain model and vocabulary rules.
