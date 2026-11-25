---
name: hubspot-interface
description: Operate a client's HubSpot CRM from Claude (Desktop, claude.ai, Teams, Claude Code) through HubSpot's remote MCP server at mcp.hubspot.com, via HubSpot's native Claude connector or a custom MCP connector, with the REST API as the operator's escape hatch. Use when someone asks about a contact, company, or deal ("is X in HubSpot?", "what stage is this deal?", "who owns this account?"), wants a call, meeting, or note logged, wants records created, updated, or associated, wants a pipeline roundup, or asks to touch properties, pipelines, segments, campaigns, marketing emails, or website content. Supplies the safety tiers that separate record writes from account-wide schema changes and public publishing, the internal-name-versus-label rule for properties and stages, the dedupe rules (contacts dedupe on email, companies do not dedupe on domain over the API, and there is no merge tool over MCP), and the discipline of reporting only what the records support.
---

# HubSpot Interface

> **Status: Draft (2026-10-25).** Built from HubSpot's published MCP docs
> (page last modified 2026-09-30), **not yet verified against a live
> portal.** Anything marked *(verify)* is a belief to confirm on first
> connect. When a live call disagrees with this file, the live call wins.
> Fix the file.

**HubSpot is the client's system of record. We don't host it.** This skill is
how a person (or the operator) drives it from Claude through HubSpot's own
remote MCP server, and what to do when that server isn't enough.

> *"Who at Acme have we talked to this quarter?"*, *"log this call against the
> deal"*, *"which open deals have no next step?"*. One connector, the person's
> own HubSpot login, and the CRM answers in conversation.

**Read [Safety](#safety--four-tiers) before your first write.** Most HubSpot MCP
writes ask the user to confirm, but that confirmation doesn't tell a record
edit apart from a change that alters the CRM for **every user in the
account**. Those are different tiers here.

## 0. Resolve the portal first

Read `config/private.json` (gitignored; shape in
`config/private.example.json`). It maps a client slug to portal facts:
portal ID, Hubs and tiers, whether Sensitive Data is on, which connector the
team uses, custom objects, and the client-stack folder that holds
credentials.

- **If the file or the client's entry is missing, say so and ask. Don't
  guess.** A wrong portal means writes land in someone else's CRM.
- Never copy a value from that file into this one. This skill is public.
- Credentials are never in config. They live in the client-stack folder the
  entry points to (`<client_stack>/hubspot/.env`).

## The surface

| | |
|---|---|
| Remote MCP | `https://mcp.hubspot.com`. Streamable HTTP. GA 2026-04-13, all tiers |
| Tools | **32 public tools**, varying by subscription, user permissions, and account config. Full tiered map: [`references/tool-map.md`](references/tool-map.md) |
| Team-member auth | OAuth 2.1 + S256 PKCE, **per user**. Acts as that HubSpot user and respects their permissions |
| DCR | **None.** A custom connector needs an MCP connector's client ID + secret (HubSpot → Development → MCP Connectors). The native Claude connector needs neither |
| Operator auth | Private-app access token (`pat-…`) against REST, `https://api.hubapi.com`, as `Authorization: Bearer <token>` |
| Human docs | `developers.hubspot.com/docs/apps/developer-platform/build-apps/integrate-with-the-remote-hubspot-mcp-server`; full index at `developers.hubspot.com/docs/llms.txt` |

The three ways to connect, and which one to pick:
[`references/connector-setup.md`](references/connector-setup.md).

## Ground yourself before anything else

Every session, before reasoning about the CRM:

1. **`get_user_details`**: who you're acting as, the account, and
   **per-object read/write access and which tools exist for this user**. Tool
   availability is tier- and permission-gated. A tool in the map that isn't
   here doesn't exist for this person. Never promise it.
2. **`discover_hubspot_schema`**: the object types this portal actually
   has, including custom objects, and whether you can read or write each.
3. **`tool_guidance`**: call it before the first `query_crm_data`, before any
   association write, and before campaign attribution. HubSpot's own docs
   require it for those, and the inputs are not guessable.

Then fetch what the task needs: `search_properties` → `get_properties` for
field names and enum values, `search_owners` for people on the team.

## The data model, in the order you reason about it

1. **Objects.** Contacts, companies, deals, tickets, leads, plus whatever
   `discover_hubspot_schema` returned (custom objects, appointments, courses,
   listings, projects, services; revenue objects are beta).
2. **Properties.** Every field has an **internal name** (`lifecyclestage`,
   `dealstage`, `hs_lead_status`) and a **label** ("Lifecycle Stage").
   Enumeration options have an **internal value** and a **label** too, and
   they are often different strings. **Write internal names and values. Show
   labels.** Look both up with `get_properties`; never write a label into an
   enum.
3. **Pipelines and stages.** Deals and tickets live in a pipeline, and each
   stage has an **ID** (often numeric or a generated string) separate from its
   label. Stage IDs are per-portal. **Never guess a stage.** Stages can carry
   **required properties**; the MCP server enforces those conditional
   validations, so a stage move can fail until the required fields are set.
4. **Associations.** Records link through associations, optionally
   **labelled** (e.g. a contact is "Decision maker" on a deal). A deal with no
   associated company is invisible from the company record. Associations are
   the HubSpot equivalent of a foreign key, and they're what's most often
   missing.
5. **Activities.** Calls, emails, meetings, notes, and tasks are objects of
   their own, **associated** to contacts, companies, and deals. A note isn't
   "on" a record. It's linked to one or more records, so it shows up on every
   record you associate it with. Associate deliberately.
6. **Owners.** `hubspot_owner_id` holds an owner ID, not an email or name.
   Resolve with `search_owners`.

## Finding things

- **`search_crm_objects`** for "is X here?" and filtered lists. Up to 5
  filter groups × 6 filters; filters inside a group are AND, groups are OR;
  **200 results per page, so page until done**. A first page isn't "all".
- **`get_crm_objects`** to fetch by ID, ≤100 IDs per call.
- **`query_crm_data`** for counts, sums, group-bys. SQL-ish, with **no joins,
  column aliases, subqueries, association traversal, or currency
  conversion**. Confirm every property name with `search_properties` first.
- Search is the CRM search API. There's **no semantic or vector search**:
  "the edtech company we met in Denver" has to become filters on real
  properties, or a question back to the person.
- Questions that cross objects ("contacts at companies with open deals")
  need several calls stitched by ID. Say you're doing that, and say when a
  result was truncated.

## Safety — four tiers

| Tier | What | Rule |
|---|---|---|
| **0 · Read** | search, get, query, analytics, schema discovery | Free. Still mind conversations and intent signals: they're private, so quote them only to the person who asked |
| **1 · Record write** | `manage_crm_objects` (create/update records, activities, associations), static `manage_segment` edits, `manage_onboarding` | HubSpot shows a proposed-changes summary and asks for confirmation. **For anything beyond one or two records, propose first in a table** (record, field: old → new) so the person approves the batch, not twenty separate prompts |
| **2 · Account-wide schema** | `manage_custom_properties`, `manage_custom_pipelines`, dynamic segments | Changes the CRM **for every user**, and can break workflows, reports, and forms that reference it. **Never as a side effect of a record task.** Name the change, say who it affects, and get an explicit yes from someone with admin authority. On a client portal, that's the client's admin plus the operator |
| **3 · Public or outbound** | publishing landing pages, website pages, or blog posts; navigation edits; `manage_campaign_objects`; `manage_marketing_email` drafts; `manage_aeo_recommendations` actions; `submit_feedback` | Visible outside the team, or sends data to HubSpot. Draft freely; **publish only on an explicit instruction that names the asset.** After publishing, `render_asset` and show the result |

There's **no delete tool** in the public MCP list. Deleting and merging are
REST-only, and therefore operator-only. That's a good default; don't work
around it from a team member's session.

## Never create a duplicate

- **Contacts dedupe on email.** Creating a contact with an email that
  already exists fails, typically as a `409` conflict over REST *(verify the
  MCP error shape)*. Search by email first anyway. A contact with no email
  has no natural key and is the usual source of duplicates.
- **Companies do *not* dedupe on domain over the API** *(verify)*. Two
  creates with `domain: acme.com` make two companies. Always
  `search_crm_objects` on `domain` (and on `name`) before creating a
  company.
- **There is no merge tool over MCP.** HubSpot merges are done in the UI or
  over REST, and **a merge cannot be undone** *(verify)*. A name match is a
  candidate, not a verdict: compare email, domain, associations, and owner,
  then bring the evidence to a human. Never merge from inference.
- When a batch contains a likely duplicate, list it separately in the
  proposal. Don't silently skip it or silently create it.

## Recurring jobs

### A. Answer a question about a person or company

`search_crm_objects` by email or domain → `get_crm_objects` with the
properties you need → follow associations to deals and recent activities.
Report what the record says, with dates. If a field is empty, say it's empty.
Don't fill it from general knowledge without saying where it came from.

### B. Log a conversation

1. Find every record involved (contact, company, deal) **before** writing.
2. Create the activity (note, call, or meeting) with a real timestamp
   (`hs_timestamp`). When the call happened, not now, if the person gave the
   time.
3. Associate it with **each** relevant record in the same operation. A note
   associated only to the contact won't show on the deal.
4. If the account has **Sensitive Data on**, activities are blocked over MCP
   (it's an MCP-only restriction; REST still works). Say so, and offer the
   operator channel or a manual paste.

### C. Move a deal

`get_crm_objects` the deal → `get_properties` on `dealstage` for this
pipeline's stage IDs → check the target stage's required properties → propose
the stage change and any required fields together → write. If the write fails
on validation, report which fields it wants. Don't invent values to get past
it.

### D. Intake a batch (a list, an export, a pile of cards)

1. Normalize keys: email for contacts, domain for companies.
2. Search for every row. Classify: exists / new / ambiguous.
3. Propose one table: what gets created, what gets updated (field: old →
   new), what's ambiguous and needs a human.
4. Write in chunks after approval. Associate contacts to companies as you go.
5. Report counts: created, updated, skipped, and why.

### E. Roundups and reports

Measure coverage before reporting on a field. Count how many records actually
have it set. A pipeline report on `amount` where 30% of deals have an amount
is a report on 30% of deals, and has to say so. Also:

- **`hs_lastmodifieddate` is not contact recency.** Any edit, import, or
  workflow bumps it. For "when did we last talk", use the activity-based
  properties (e.g. `notes_last_contacted`; confirm the name with
  `search_properties`) or read the activities themselves.
- Use `query_crm_data` for counts and sums. Use paginated search when you
  need the rows.

## Operator channel (REST)

For what MCP can't do (merges, deletes, bulk association reads, property
history, Sensitive Data accounts) the operator uses a **private app** token
from the client-stack's `.env`:

```bash
set -a; . <client_stack>/hubspot/.env; set +a
curl -s https://api.hubapi.com/crm/v3/objects/contacts/search \
  -H "Authorization: Bearer $HUBSPOT_PRIVATE_APP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"filterGroups":[{"filters":[{"propertyName":"email","operator":"EQ","value":"x@example.com"}]}],"properties":["firstname","lastname","email"]}'
```

- A private app acts **as the app, not a person**. HubSpot attributes its
  writes to the integration. Use it for reads and repairs, not for logging a
  team member's activity under their name.
- Scope the app to what the job needs. Every scope added is a scope that
  leaks with the token.
- Watch the `X-HubSpot-RateLimit-*` response headers *(verify)* rather than
  assuming a number. Limits vary by tier and app type.
- Same tiers apply. A REST delete or merge is Tier 2 at minimum: propose,
  then wait for a yes.

## Gotchas

- **Labels in enum writes.** Writing `"Customer"` to `lifecyclestage` fails
  or misbehaves; the value is `customer`. Custom enum values can be anything,
  so look them up.
- **Lifecycle stage only moves forward** by default in HubSpot *(verify per
  portal)*. Setting an earlier stage can silently no-op. To go backwards, the
  property has to be cleared first, which is a deliberate act. Ask.
- **A tool listed in the map can be absent.** Pages and blog tools only
  exist in Claude, ChatGPT, and Gemini clients; AEO needs Marketing Hub
  Pro/Enterprise; quotes need Revenue Hub Pro/Enterprise. Trust
  `get_user_details`, not the map.
- **Scopes are fixed at connector install.** When HubSpot adds tools,
  existing users must **reinstall** the connector to get the new scopes. "The
  tool isn't there" on one person's machine is often this.
- **Free-tools accounts can't create custom pipelines**, only edit the
  default one.
- **Conversations inbox access is restricted per user or team.** One
  person's query can see threads another's can't, so don't treat it as
  complete.

## See also

- [`references/connector-setup.md`](references/connector-setup.md): native connector vs MCP connector vs operator token
- [`references/tool-map.md`](references/tool-map.md): all 32 tools, tiered
- `lossless-crm-interface-guidelines`: the provenance habits (fetch first, offer model knowledge rather than smuggling it in) apply here unchanged, even though that skill's instances are Twenty
- `decilehub-interface` (self-host-stack): the same operating-layer shape over a different BYO-SaaS CRM
