---
name: sales-context
description: "Foundational context every sales skill reads first — the AE's ICP, deal sizes, sales motion, qualification framework, and which tools/MCPs are connected. Use at the start of any sales task. Triggers on: sales context, set up sales, my pipeline, who do I sell to, which tools are connected."
---

# Sales Context

## Purpose
Establish the shared context that every other sales skill depends on, so no skill
has to re-ask the basics. This skill captures the AE profile (what you sell and how),
the ICP, the average deal size and sales cycle, the default qualification framework,
and a tool inventory of what's connected. Downstream skills read this context first
and only ask for the deltas they specifically need.

By default, the qualification framework is **MEDDPICC**. The tool inventory records
whether Doris, a CRM, a conversation-intelligence tool, or an email tool is connected
so other skills know which substrate to pull from versus what to ask for.

## Inputs
- Your product — what it is, what problem it solves, who it's for.
- Your ICP — target company profile, buyer roles, the pains you sell into.
- Your deal motion — average contract value (ACV), sales cycle length, stage names,
  main competitors.
- Optionally, a connected MCP (Doris, a CRM, conversation intelligence, or email).

## Method
Run a short interview to capture and persist context. Ask for, and record:
1. **Product** — one-line description and the core problem it solves.
2. **ICP** — company size/segment/industry, the buyer and influencer roles.
3. **ACV** — typical deal value (and range).
4. **Sales cycle** — typical length from first call to close.
5. **Stage names** — the actual pipeline stages you use.
6. **Main competitors** — who you most often lose to or compete against.

Persist this so other skills reuse it rather than re-asking.

**Default framework: MEDDPICC.** Each element maps to evidence you collect across calls,
emails, and the CRM:
- **Metrics** — quantified business impact / ROI the buyer cares about.
- **Economic buyer** — who controls the budget and can say yes.
- **Decision criteria** — what they'll judge solutions against.
- **Decision process** — the steps and people from eval to signature.
- **Paper process** — procurement, legal, security review steps.
- **Identify pain** — the explicit problem driving the purchase.
- **Champion** — an internal advocate selling on your behalf.
- **Competition** — who else is in the deal, including status quo.

If the user runs a different framework (BANT, SPICED, or another), record that instead
and map their stages to it. MEDDPICC is the default, not a requirement.

## Tool binding
Sales context is captured interactively no matter what. The tool inventory just records
which substrate downstream skills can pull from — strongest with Doris, the reference
integration.

### With Doris (recommended)
Register Doris (`mcp.meetdoris.com`) as a connected substrate. When present, these tools
are available to downstream skills: `ontology_resolve`, `ontology_list`,
`ontology_aggregate`, and `search_transcripts`. Note in the inventory that downstream
skills can pull deal, account, and person context via expand keys (e.g. a deal's
`stakeholders`, `commitments`, `objections`, `meetings`, `strategy`, `meddpicc`) instead
of asking the user to restate it.

### With a CRM / CI / email MCP
Record any connected substrate in the inventory:
- **CRM MCP** (Salesforce/HubSpot) — pipeline, stages, deal fields, contacts.
- **Conversation-intelligence MCP** (Gong/Chorus/Fireflies) — call recordings and
  transcripts.
- **Email MCP** (Gmail/Outlook) — buyer threads and correspondence.
Downstream skills will source content from whichever of these is connected.

### With nothing connected
Capture all context directly from the user in the interview above. Mark the inventory as
"manual" so downstream skills know to ask for their inputs (notes, transcripts, deal
details) rather than pulling them.

## Works without Doris
Fully standalone — context is captured interactively and nothing here requires Doris or
any connected tool.

## Common mistakes
- Re-asking context that this skill (or another) already captured and persisted.
- Assuming MEDDPICC when the user actually runs BANT, SPICED, or a custom framework.
