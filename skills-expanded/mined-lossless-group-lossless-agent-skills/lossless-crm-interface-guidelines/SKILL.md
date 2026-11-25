---
name: lossless-crm-interface-guidelines
description: Conventions for reading and writing the operator's Twenty CRM instances (Lossless, Palmer AI, The Water Foundation) via MCP. Use whenever adding or enriching a company, person, deal, thesis, event, or portfolio relationship; when triaging a list or export into the CRM; or when extending the CRM schema. Encodes instance routing, the custom object model (Investment, Deal Source, Deal Prospect, Thesis, Thesis Fit, Events, Interaction), the forced-choice scoring standard, provenance rules, the companion-timeline-row rule that makes custom objects visible on a Person or Company timeline, and known MCP pitfalls.
---

# Lossless CRM Interface Guidelines

Operating manual for working inside the operator's Twenty CRM estate. Read before the
first write of a session. The goal is a CRM that a partner could open cold and trust.

---

## 1. Who this is for

**Load `config/private.json` before the first write of a session.** This skill is
deliberately identity-free; every operator-specific value lives in that file, which is
gitignored. `config/private.example.json` is the public template — copy it to
`config/private.json` and fill it in.

If `config/private.json` is absent, say so and ask. Do not guess a name, a firm, or a
role, and do not backfill any of it from model knowledge.

Two blocks drive behaviour here:

- **`operator`** — who the CRM belongs to. Used for attribution ("Per <shortName>,
  <date>") and for the second-person voice this skill assumes.
- **`affiliations`** — the firm → role map, keyed by role (`venturePartner`, `scout`,
  `informal`). This is the *only* authority for the Deal Prospect `My Role` field:

  | `affiliations` key | Deal Prospect `My Role` |
  |---|---|
  | `venturePartner` | `VENTURE_PARTNER` |
  | `scout` | `SCOUT` |
  | `informal` | `INFORMAL` |

The operator is a career VC working across several firms rather than one house.
Consequences:

- Never assume a company is "for the fund." Ask which firm, or leave routing unset.
- Never set `My Role` to a formal value for a firm that is not listed under
  `venturePartner` or `scout` in `config/private.json`. Use `INFORMAL`.
- The same company can be routed to several firms with different rationales. That is
  the normal case, not an edge case.
- Read `affiliations.notes` before acting on a firm — it records where a relationship is
  self-appointed or brokered through a person rather than a formal mandate.

They are a sophisticated operator. Do not hedge, do not lead with risk, do not warn about
things a professional already knows. Lead with the upside case and what would have to be
true for a fund-returner outcome. Risk matters only when it caps upside or kills the
company. State it once, plainly, and move on.

---

## 2. Instance routing

Three separate Twenty workspaces. They do **not** share data.

| Instance | Scope |
|---|---|
| **Lossless Twenty** | Primary. Default target. Dealflow, hard tech, investors, network. |
| **Palmer AI Twenty** | Edtech and workforce. |
| **The Water Foundation Twenty** | Ocean, climate, environmental. |

Rules:

- Default to **Lossless** unless told otherwise.
- If asked for "both," confirm which two.
- A record in one instance is not a duplicate of a record in another. Never "merge"
  across instances.
- **Parity rule:** when the same entity exists in more than one instance, copy missing
  fields across so neither record is thinner — domain, LinkedIn, address, description,
  title, GitHub. Push in whichever direction has the data.
- Schema differs between instances. Lossless has the richest schema. Before writing a
  field in a non-Lossless instance, confirm it exists there.

---

## 3. Non-negotiable habits

### 3.1 Dedupe before every create

Always query first. Match on name *and* domain, and use `ilike` with wildcards.

```
find_many_companies { or: [ {name:{ilike:"%acme%"}},
                            {domainName:{primaryLinkUrl:{ilike:"%acme.com%"}}} ],
                      select:["id","name","domainName"] }
```

If a near-match exists, enrich it rather than creating a second record. If it is a real
but distinct entity with a colliding name, disambiguate **both** records in their
descriptions (see §3.5).

### 3.2 Fetch first

Fetch the company's own site before writing a description. Facts from a fetch beat facts
from model parameters, and inferred domains have been wrong repeatedly
(thebuildersfund.com not buildersvc.com; caprock.com not thecaprockgroup.com).

**When a site is inaccessible through tool calls** — JS-rendered, bot-blocked,
security-overkill, paywalled, or any other reason — say so plainly and name the reason.
Do not quietly backfill from model knowledge. The operator can open the site themselves,
paste the relevant content, or give their own perspective, and that becomes the
enrichment source. A stated blocker invites a two-second fix; a silent one produces a record nobody
knows to distrust.

### 3.3 Model knowledge: offer it, disclose it, don't smuggle it

Information from model parameters and memory is genuinely useful and worth surfacing.
The problem is never that it was used — it is that it was used *invisibly*. Inaccurate or
confusing data written without a marker becomes indistinguishable from verified data, and
surfaces later as a wrong domain in an outbound email or a stale valuation in a memo.

Default behaviour:

- **Offer, don't assume.** Say what you know and let the operator green-light it before
  it lands in a field. "I have Legora as Stockholm-founded, formerly Leya — want that in?"
- **If it goes in, mark it.** Say "from memory, not fetched" in the reply, and where the
  claim is load-bearing, mark it in the field itself.
- **Attribute other sources too.** "Per <operator.shortName>, <date>" for their input.
  Name the aggregator ("per Tracxn") and flag when sources disagree.
- **An empty field is data. A wrong field is damage.** Prefer the gap.

**Expediency override.** The operator may ask for speed over caution — clearing a
backlog, working through a list, filling out records fast. When they do: write the best
available information without pausing for per-item confirmation, keep disclosure to one
compact line at the end ("descriptions for these six are from memory"), and drop the
offer-first step. The override applies to *asking*, never to *labelling*. Provenance
marking survives every speed setting. It also expires — treat it as scoped to the current
run of work, not a standing instruction.

Never invent a domain, LinkedIn slug, job title, or funding figure to fill a field, at
any speed setting.

### 3.4 Attach research as a Note

Analysis belongs on the record, not only in chat. Create a Note and target it at every
relevant record (company *and* person, when both apply).

Notes should carry: the thesis or upside case, hard numbers with their source, caveats,
conflicting data, name collisions, open diligence questions, and a source line with the
fetch date.

```
create_one_note { title, bodyV2:{markdown:"..."}, position:"first" }
create_one_note_target { noteId, targetCompanyId, position:"first" }
create_one_note_target { noteId, targetPersonId,  position:"first" }
```

### 3.5 Flag name collisions in both records

When two real entities share a name, say so on each. Examples in the estate:

- **Watershed** (watershed.com, carbon accounting) vs **Watershed VC** (watershed.vc)
- **Sundt Construction** (US contractor) vs **Sundt AS** (Norwegian family office)
- **GCM Grosvenor** — explicitly unaffiliated with UK Grosvenor Group
- **Jump Crypto** vs **Jump Capital** — related but distinct
- Off Season II demo-day startups with generic names carry an `(Off Season II)` suffix

### 3.6 Correct names from evidence

Export spellings are frequently wrong. LinkedIn slugs and email local-parts are better
evidence than a spreadsheet cell. Corrections made this way should be surfaced to
the operator, not silently applied.

The recurring failure modes are transposed vowels, dropped diacritics, and anglicised
respellings of non-English given names — check those first. A running list of the
specific corrections observed in this estate belongs in `config/private.json`, not here:
it is a roster of real people in the operator's network.

---

## 4. Profile links architecture

**Problem:** hardcoding a field per source (Crunchbase, PitchBook, Tracxn, CB Insights,
BuiltIn, YC, Wellfound…) pollutes the form with empty fields and still misses the long
tail.

**Solution:** two tiers.

**Tier 1 — dedicated fields**, for sources that exist for almost every record and get
queried often:

| Field | Object | Why dedicated |
|---|---|---|
| `domainName` | Company | Native, and the duplicate-detection key |
| `linkedinLink` | Company, Person | Near-universal |
| `github` | Company | High signal for dev tools, infra, open source |

**Tier 2 — one `Profiles` LINKS field** on both Company and Person, for everything else.
Twenty's LINKS type carries a primary link plus an arbitrary array of labelled secondary
links, so it behaves like a flexible JSON bag while staying clickable and renderable.

```
profiles: {
  primaryLinkLabel: "Crunchbase",
  primaryLinkUrl:   "https://www.crunchbase.com/organization/acme",
  secondaryLinks: [
    { label: "PitchBook",   url: "..." },
    { label: "Tracxn",      url: "..." },
    { label: "CB Insights", url: "..." },
    { label: "BuiltIn",     url: "..." },
    { label: "X",           url: "..." },
    { label: "Bluesky",     url: "..." }
  ]
}
```

Rules:

- Label every secondary link. An unlabelled URL is nearly useless later.
- Primary = the most information-dense profile for that company, not a fixed source.
- Promote to a dedicated field only when a source proves near-universal *and* gets
  filtered on. Otherwise Tier 2.
- Same pattern on Person: X, Bluesky, GitHub, personal site, Substack, Kauffman Fellows.
- `domainName.secondaryLinks` is for the company's *own* pages (team, portfolio,
  pricing, docs). Third-party profiles go in `Profiles`. Keep that boundary.

---

## 5. Custom object model

Beyond Twenty's native Company / Person / Note / Task, Lossless carries these. Each is a
join object because the relationship itself holds data — and because **Twenty has no
many-to-many at all**. `RelationType` in `twenty-shared` is literally two values,
`MANY_TO_ONE` and `ONE_TO_MANY` (verified against v2.24.1). This is a product limit, not
an MCP one: no tool, API call or UI action can widen a singular relation. Whenever a
record needs to hold *several* people or companies, the answer is always a join object.

### Investment — who invested in whom

`Investor → Company` · `Portfolio Company → Company` · Round · Date · Lead · Source

Round is optional by design. A scraped portfolio page produces a row with a blank round;
that blank means "investor, stage unknown," which is itself information. Two rows for
the same pair are correct when a firm invested twice at different stages.

### Deal Source — where a deal came from

`Company Sourced → Company` · `Referred By → Person` · `Referring Firm → Company` ·
`Referring Firm (if any)` (text, for referrers with no firm) · `Sourced At Event → Event`
· Date Sourced · Channel · Relationship Type · Notes

`Relationship Type` answers what the referrer *is* to the deal: their portfolio,
sharing allocation, tracking, works there, unspecified. Independent SPV promoters have
no firm record — use the text field, not a fabricated company.

### Deal Prospect — which firm to route a deal to

`Company → Company` · `Prospect For (Firm) → Company` · `Thesis → Thesis` ·
`Route To (Person) → Person` · Fit Rationale · **Fit Score** · Status · My Role ·
Date Flagged · Date Sent · Notes

Status: identified → sent → in diligence → invested / passed / stale.
One row per company↔firm pair. Status diverges the moment one firm engages and another
passes, which is exactly why this is a join and not a multi-select.

### Thesis + Thesis Fit — investment theses and what belongs in them

**Thesis:** Statement · Why Now · What Would Have To Be True · Open Questions · Status ·
Fund / Vehicle · `Parent Thesis → Thesis` (self-referencing, so sub-theses nest).

**Thesis Fit:** `Thesis` · `Company` · Rationale · **Fit Score** · Date Mapped.

Write theses as arguments, not labels. "What Would Have To Be True" should be falsifiable
and uncomfortable. Open Questions should be the things you'd actually need answered
before deploying.

### Events — Event Series / Event / Event Participation

Modelled to survive the VC-specific hierarchy: an **organizer** runs an **Event Series**,
which nests via `Parent Series` (SuperReturn → SuperReturn Berlin), and each dated
instance is an **Event** (SuperReturn Berlin 2024).

**Event Series:** `Organizer → Company` · `Parent Series → Event Series` · Description ·
Website · Region
**Event:** `Series` · Start / End Date · Location · Website · Notes ·
Cost (Ticket) · Cost (Travel & Lodging) · Days Spent · **Worth Repeating**
**Event Participation:** `Event` · `Company` · `Person` · Participation Role ·
Met In Person · Notes

The point of the cost fields is the ROI question. Because Deal Source carries
`Sourced At Event`, you can ask: this event cost $X and Y days, produced N participations,
M of which became deal sources, K of which became investments. That question is
unanswerable without a persistent record, which is why events get modelled properly
rather than written into a note.

### Interaction — a single touchpoint, and its timeline row

`Person` · `Organisation` · Interaction Date · Channel · Direction · Summary · Verbatim ·
Needs Response

The object that answers "when did I last speak to X" and "what has gone quiet" — questions
Notes cannot. Paste the message exactly into `Verbatim`: verbatim is evidence, paraphrase
is not. Analysis still belongs in a Note.

`Channel` was enumerated generously at creation (`WHATSAPP`, `EMAIL`, `PHONE_CALL`,
`VIDEO_CALL`, `IN_PERSON`, `SMS`, `LINKEDIN`, `SIGNAL`, `TELEGRAM`, `SLACK`, `X_DM`,
`EVENT`, `DATA_ROOM`, `BROADCAST`, `OTHER`) and **must never be edited now that records
exist**. `Direction` distinguishes `BROADCAST` — sent to a list, not to the operator
personally — from a direct approach. That distinction is signal, so set it honestly.

Interaction is also the answer to "I want *these* meetings in the CRM, with their content."
It carries full text, it is created one record at a time by deliberate choice, and it needs
no calendar connection — so it works for an operator who will not sync a calendar. Prefer
it over any attempt to hand-write `calendarEvent` (see §8).

#### Interaction Participation — the plural participants

`Interaction` · `Person` · `Company` · Participation Role · Notes

`Interaction.Person` and `Interaction.Organisation` are MANY_TO_ONE, so they hold the
**primary counterpart** and nothing more. A three-person meeting cannot live in them.
Interaction Participation is the join that carries everyone, exactly mirroring Event
Participation.

`Participation Role`: `ORGANIZER` (called or hosted it) · `PRESENTER` (demoed, pitched
or presented) · `ATTENDEE` (present, not presenting) · `COPIED` (on the thread, passive)
· `UNKNOWN`. **Never edit this option list now that records exist.**

When to write participations:

- **Multi-party interactions — always.** Without a row, a second attendee is invisible to
  `find_many_interaction_participations`, which is the query that answers "when did I last
  speak to X". A timeline row alone makes them *visible* but not *queryable*; that is not
  the same thing and is not sufficient.
- **1:1 interactions — don't bother.** The singular fields already carry it. A join row per
  WhatsApp message is noise.
- **Leave the role null rather than guess.** On a backfill where you weren't told who did
  what, an empty role is data; an invented one is damage.
- One row per participant, and the company gets its own row when the org itself was a
  party (the presenting company, the firm on the other side of the table).

#### Always write the companion timeline row

Creating an Interaction generates its own `interaction.created` activity, but that row
targets the *Interaction*. The Person's and Company's timelines stay empty. Twenty only
fans a `linked-<object>.created` row out to a parent record for `noteTarget` and
`taskTarget` — hardcoded as a two-entry map in `timeline-activity.service.ts` — so custom
objects never propagate on their own. There is no setting for this.

Write the row yourself, one per populated relation:

```
create_one_timeline_activity {
  position: "first",
  name: "linked-interaction.created",
  happensAt: <interactionDate>,          // the interaction's date, NOT now()
  linkedRecordId: <interaction id>,
  linkedRecordCachedName: <interaction name>,
  linkedObjectMetadataId: <interaction object metadata id>,
  targetPersonId: <personId>,            // and/or targetCompanyId — one row each
  workspaceMemberId: <operator's workspace member id>
}
```

Rules that make it stick:

- **Leave `properties` unset.** The frontend's `filterOutInvalidTimelineActivities` drops
  any row whose `properties.diff` keys don't validate against the target object's fields.
  A `.created` row with no diff skips validation entirely and survives. Adding a diff is
  how you make the row silently vanish.
- **`happensAt` is the interaction's date.** The timeline sorts on it. Defaulting to now
  puts a three-week-old conversation at the top of the feed.
- **Fetch `linkedObjectMetadataId` per workspace** with
  `get_object_metadata {objectName:"interaction"}`. It is not portable between instances.
- **One row per relation.** An Interaction with both `personId` and `organisationId` needs
  two rows to appear on both timelines. Once participations exist, write one row per
  *participant* — otherwise the people who were in the room but aren't the primary
  counterpart never see the interaction on their timeline.

Expect generic copy, and don't chase it. `EventRowDynamicComponent` switches on the linked
object's name with cases only for `calendarEvent`, `message`, `task`, and `note`; anything
else falls through to `EventRowMainObject`, which renders from the action (`created`) alone.
The entry lands on the timeline at the right time with the right author, but it won't read
"created a related Interaction → <name>". That card needs a case added to the frontend
switch — a patched fork, and not worth carrying yet.

### Lists — working sets

A `Lists` MULTI_SELECT on Person, for filterable working sets (e.g.
`Venture Investors - Active`, `SF Bay Area Contacts`, `202608_Impulse-AI-Fundraise-Export`).

Note: Twenty also has a **native** many-to-many Lists relation visible in the UI, but MCP
does not expose write tools for it. The multi-select is the machine-writable path. Don't
confuse the two when the user asks about "Lists."

---

## 6. Scoring standard — forced choice, no neutral

Every rating field uses a **6-point scale with no midpoint**. Values `S0`–`S5`, labels
`0`–`5`. The absence of a middle forces a call.

| Value | Label | Meaning |
|---|---|---|
| `S0` | 0 | Likely-Unfit |
| `S1` | 1 | Adjacent-Fit |
| `S2` | 2 | Loose-Fit |
| `S3` | 3 | Potential-Fit |
| `S4` | 4 | Strong-Fit |
| `S5` | 5 | Perfect-Fit |

0–2 are negative, 3–5 positive. Colour ramp red → orange → yellow → blue → turquoise →
green.

**Store the numeral, not the word.** The words live in the field description so the
vocabulary can be renamed without touching a record. Apply this shape to any new
rating, conviction, or fit field — never a 3- or 5-point scale, never a neutral middle.

---

## 7. Batch triage workflow

For an export or list of 50–400 rows:

1. Inspect the file with bash first — header, row count, contact-per-row distribution.
2. Tier by signal strength (strong / ambiguous / excluded) and show the reasoning, not
   just the output.
3. Present a numbered batch of 20–50 as a scannable table with a flag on anything
   already in the CRM, any name collision, and any stale-looking entry.
4. Wait for selection. Do not create records from a list the user hasn't triaged.
5. Create companies first, capture the returned IDs, then create people referencing
   those IDs in the same turn.
6. Apply list tags on create. Retrofitting tags is slower than setting them once.
7. Report corrections and skips explicitly.

Skip person records for handle-only contacts (single mononyms, Discord-style handles).
They cannot be matched or contacted later. Say which ones were skipped and why.

**Turn size matters.** Very long turns have caused client freezes. Keep to roughly 8–12
tool calls per turn; split a large batch across turns rather than doing everything at
once.

---

## 8. MCP pitfalls

Learned the hard way. Each of these has cost a real mistake.

- **`learn_tools` before first use.** Schemas are not guessable. `create_one_note` takes
  `bodyV2:{markdown}`, not `body`. `create_one_note_target` takes `targetCompanyId`, not
  `companyId`. `create_many_field_metadata` takes `fields`, not `items`.
- **Never guess a record ID.** `upsert_many_*` with an unknown ID silently **creates**
  blank records instead of failing. Always query for the ID first. This has happened.
- **`update_many_*` uses `{filter, data}`**, not a records array.
- **Reserved names.** `event`, `role`, and others are reserved. Use `eventInstance`,
  `participationRole`; the display label can still read "Event" and "Role."
- **Domain uniqueness spans the trash.** A soft-deleted record still holds its domain and
  will block an update with "duplicate entry detected." Query `deletedAt is NOT_NULL` to
  find it; a `www.`/non-`www.` variant is a workaround, emptying trash is the fix.
- **Deletes are soft and reversible.** Recoverable from trash. Still confirm before
  deleting anything with attached notes or relations, and re-point note targets first.
- **`select` is required** on find queries. `select:["*"]` works when you need everything.
- **`position:"first"`** puts new records at the top of manual sort order. Sort by
  Created At if you want chronological.
- **Stale UI.** Twenty does not always live-refresh while an external client writes.
  If the user says records are missing, verify with a query before re-creating anything.
- **Never hand-create a `calendarEvent`.** MCP exposes no create tool for it, and the REST
  path is a trap: `CalendarEventCleanerService` deletes every calendarEvent with no
  `calendarChannelEventAssociation`, and it runs at the end of every calendar import, on
  connected-account destroy, and on blocklist changes. With no calendar connected the rows
  sit there looking fine — until the day someone connects one, and then they are gone.
  Use an Interaction instead. (`create_calendar_event` is a different tool: it writes an
  event onto a connected Google/Microsoft account and can email invitations. It is not a
  CRM record insert.)
- **Custom objects do not reach a parent's timeline by themselves.** Any custom object
  related to a Person or Company needs a companion `linked-<object>.created` row written
  explicitly. See the Interaction section in §5 for the recipe; it generalises.

---

## 9. Anti-patterns

- Creating a record without checking for an existing one.
- Writing a description from memory when the site was fetchable.
- Silently backfilling from model knowledge when a fetch failed, instead of naming the
  blocker and letting the operator supply the content.
- Using model knowledge without disclosing it — at any speed setting.
- Inventing a domain or LinkedIn slug to avoid an empty field.
- Leaving analysis in chat where it dies with the conversation.
- Leading with risk, hedging, or warning a professional about professional things.
- A neutral middle in any score.
- Setting a formal `My Role` on a firm where no arrangement exists.
- Creating an Interaction without its companion timeline row, leaving the touchpoint
  invisible on the Person and Company timelines where it is actually looked for.
- Merging records across instances.
- Silently applying a name correction without surfacing it.
- Dumping 40+ tool calls into one turn.