---
name: n8n-agent-builder
description: Design, plan, and build n8n workflows, AI agents, automations, and integrations — with Claude acting as the n8n expert. Use when the user wants to automate a repetitive task, connect two or more apps, build an AI-powered agent workflow in n8n, or turn a described business process into a working n8n JSON spec. Outputs a complete workflow plan and, where possible, a pasteable n8n JSON skeleton. Source: @the.wealth.lab "6 Favorite Claude Skills That Automate Almost Anything."
---

# n8n Agent Builder

Source: @the.wealth.lab "6 Favorite Claude Skills That Automate Almost Anything."

> Create complete n8n workflows, AI agents, automations, and integrations with Claude — without starting from scratch. Turn repetitive tasks into automated workflows and save hours of development time.

## What this skill does

Turns a described business process or automation goal into a concrete n8n implementation plan:
- Chooses the right trigger (webhook, schedule, app event, manual)
- Maps the node sequence: trigger → data transformation → conditions → actions → error handling
- Identifies which n8n built-in nodes and community nodes are needed
- Produces a human-readable workflow description AND a pasteable n8n JSON skeleton where the logic is deterministic enough to pre-build
- Flags credentials and API keys the user will need to supply

## Workflow design process

1. **Clarify the trigger** — What starts this workflow? (A form submission, a new row in a spreadsheet, a time schedule, an inbound webhook from another tool?)
2. **Map the happy path** — Step by step from trigger to final action: what data flows, what gets transformed, what gets sent where?
3. **Add conditions and branches** — If X, do Y; if not, do Z. Error paths belong here too.
4. **Select nodes** — Match each step to an n8n node (HTTP Request, IF, Set, Code, OpenAI, Gmail, Slack, Airtable, etc.)
5. **Output the spec** — Produce a numbered node list with connection map, then the JSON skeleton.

## Copy-paste prompt to use

```
You are an expert n8n workflow builder.

I want to automate: [DESCRIBE THE TASK OR PROCESS]

My tools/apps involved: [LIST APPS, e.g. Gmail, Airtable, Slack, OpenAI, Notion]
Trigger: [WHAT STARTS THE WORKFLOW, e.g. "new email arrives", "every morning at 8am", "form submitted"]
End result: [WHAT SHOULD HAPPEN AT THE END]

Please:
1. Design the full workflow step by step (trigger → nodes → final action)
2. Identify every n8n node I need (built-in and community)
3. Note which credentials/API keys I must supply
4. Give me a pasteable n8n JSON skeleton for the workflow
5. Flag anything I'd need to test or adjust before going live

Be specific. Don't give me vague steps — give me exact node names and connection logic.
```

## Common automation patterns

| Goal | Trigger | Key nodes |
|---|---|---|
| Lead capture → CRM | Webhook / Form | HTTP Request, Set, Airtable/HubSpot |
| Daily report email | Schedule | HTTP Request, Code (format), Gmail |
| AI email triage | Gmail trigger | OpenAI (classify), IF, Gmail (label/reply) |
| New row → Slack alert | Airtable/Sheets trigger | Set, Slack |
| Content to social post | Manual / webhook | OpenAI, HTTP Request (social API) |
| Customer onboarding | Webhook | Wait, Email, Slack, CRM update |

## Reducing hallucinated nodes — the grounding-project technique

Claude can invent n8n node names/parameters that don't exist, especially for
less common integrations. A dedicated Claude Project with real reference
material cuts this down before it starts:

1. **Create a Project** named something like "n8n Workflows."
2. **Set project instructions** telling Claude to check its work against the
   real n8n source before inventing anything:
   ```
   // Grounding rules
   Always reference the "n8n-io/n8n" Github repo before building anything.
   Never invent nodes or features that don't exist.
   ```
3. **Upload 2-3 of your own real, exported n8n workflow JSON files** to the
   Project (Settings → project knowledge). This isn't decorative — Claude
   pattern-matches the exact JSON shape (node types, `parameters` keys,
   `connections` structure) your actual n8n version produces, instead of
   guessing at a plausible-looking but wrong schema.
4. **Use Sonnet, not a lighter model, for this Project.** Node-schema
   accuracy is exactly the kind of task `claude-usage-limits`'s model-matching
   tip (procedure) puts in the "Sonnet" tier, not Haiku.
5. Then use the copy-paste prompt above as normal, inside this Project.

This doesn't replace testing the generated workflow in a real n8n instance
before trusting it in production — it reduces how often that test fails on
an invented node, it doesn't eliminate the need for the test.

## Related skills

- **saas-mvp-24h**: If the workflow is the backbone of a product, combine with this skill for the full build stack
- **lean-software-stack** / **open-source-devtools-2026**: n8n is itself on the lean-stack tier — self-hostable, replaces Zapier/Make
- **content-repurposing-service**: An n8n workflow can automate the extract/draft/deliver pipeline from that skill
- **new-client-system**: Outreach sequences and follow-ups can run as n8n automations
- **claude-usage-limits** (procedure): The model-matching and Project-caching guidance behind step 4 above
- **ai-agents-for-beginners**: The Microsoft-stack equivalent of this skill's tool-use/planning patterns, taught as a structured curriculum rather than a build-it-now workflow — useful if the underlying design pattern (not the n8n implementation) needs more grounding first
