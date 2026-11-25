---
name: event-prep
description: The Lossless Group's method for preparing for, working, and recapping a conference or summit — the "company brain" event workflow across markdown notes in the content repo and the operator's Twenty CRM. Use whenever the user shares an event URL and asks who to meet, says "prep me for <event>", "build an event map", "who's going to be at", "rank the speakers", "what sessions should I attend", "log who I met at", "re-sync the event map", or "recap <event>"; whenever a file under content/sources/Events/ or client-content/<client>/Events/ is created or edited; and whenever badge photos, business cards, or an attendee export from an event need to land in the CRM. Encodes the lifecycle (series note → prep map → event → interaction logging → recap re-sync), lens-based routing to the right folder and Twenty instance, the priority and touchpoint keys, the top-conversations table with asks and opening lines, the unverified-marking and sources-footer discipline, and the propose-before-write pattern for CRM records. Composes with lossless-crm-interface-guidelines, which owns every CRM write rule.
---

# Event Prep

> **Status: draft (2026-10-14).** Reverse-engineered from three events done informally
> (OceanX 2026, Cloudflare Connect 2026, Yotta 2026) and being refined against a live run
> (RAISE Global Summit 2026). Expect changes after that run.

An event is worth the ticket only if you walk in knowing who matters and why, and walk
out with every touchpoint on a record. The skill turns a public event page into a
ranked, lens-specific plan before the event, and turns badge photos and business cards
into CRM records and a recap afterwards.

All of it lives in two places: **markdown in the content repo** (the readable brain) and
**the Twenty CRM** (the queryable record). The markdown is generated from research and
from the CRM. It never replaces the CRM.

---

## 1. Intake: four questions before any research

Answer these first. Ask the operator for any that aren't clear from the request.

| Question | Why it matters | Example answers |
|---|---|---|
| **Whose lens?** | Decides what "relevant" means, which folder, and which Twenty instance | Lossless / the operator; a client (TWF, LFG) |
| **What does the lens want from this room?** | Becomes the segment columns and the priority key | TWF: LP capital, deal flow, government mandates. LFG: platform channel partners |
| **Attending, or observing?** | Prep map vs. a recap of an event nobody attended | OceanX: attending, nobody met yet. Deep Tech Week: not attended |
| **What's the source list?** | The plan is only as good as the list of who's in the room | Public speaker and sponsor pages; attendee app export; agenda; a list the operator received by email |

Whether there's a list decides how much you can trust the result. With only a public speaker
page, everything about who will actually be there is unverified and must say so.
Gated attendee lists (Cvent, Swapcard, Brella) are better. Ask for an export before
reaching for web research.

---

## 2. Routing by lens

| Lens | Series note | Instance prep / map | CRM instance |
|---|---|---|---|
| Operator (Lossless) | `content/sources/Events/<Series>.md` | `content/sources/Events/<Series> <Year>.md` | Lossless Twenty |
| Client with its own Twenty (TWF, Palmer AI) | `content/sources/Events/<Series>.md` | see open question below | that client's Twenty |
| Client without a Twenty (LFG) | `content/sources/Events/<Series>.md` | `content/client-content/<Client>/Events/<Event>-<Year>.md` | Lossless Twenty, if anything |

The **series note** is always public knowledge about the event and always lives in
`sources/Events/`, regardless of lens. Instance routing for the CRM follows
`lossless-crm-interface-guidelines` §2: default to Lossless, never merge across instances.

> **Open question (unresolved in practice):** OceanX 2026 was prepped for TWF but lives in
> `sources/Events/`, while Cloudflare Connect for LFG lives in `client-content/`. Pick one
> rule for client-lens prep docs before codifying further.

---

## 3. The lifecycle

### Phase 1 — Series note (`Event-Series`)

Check `sources/Events/` first (`ls`, and grep for aliases). Most series already have a
stub. If not, create one:

- Frontmatter: `url`, `date_created`, `date_modified`, `tags: [Event-Series]`, plus the
  `og_*` block (`og_title`, `og_description`, `og_image`, `og_favicon`, `og_last_fetch`)
  from a fetch of the series homepage. `maintained_by:` a wikilink to the organizer if
  known. `for_clients:` when the series is relevant to specific clients.
- Body: wikilinks to each instance note and map, the organizer, the topic concepts,
  and `[[moc/Events and Conferences MoC]]`.
- Organizers that run many series (Informa) get `tags: [Events-Producers]`.

Nested series (Deep Tech Week → Deep Tech Week Austin TX 2026) mirror the CRM's
`parentSeries`.

### Phase 2 — Research the room

1. **Fetch the event's own pages first**: home, speakers, sponsors, agenda/sessions,
   partners, venue. Record each URL and the fetch date for the sources footer. If a page
   is gated or JS-rendered and the fetch comes back thin, say so and ask for the
   content (per the CRM skill §3.2). Don't fill the gap from memory without saying so.
2. **Pull what the CRM already knows.** For every organization and person on the list,
   query the routed instance (dedupe rules in the CRM skill §3.1). Anyone already there gets a
   **CRM** marker and their existing relationship contacts named. A shared contact is the
   best opener there is.
3. **Research each organization through the lens**: what they do, their role at the event, the
   named contacts and their titles, and *the specific fact that makes them relevant to this lens*
   (a fund, a mandate, a programme, a product launch). One hard number beats three
   adjectives.
4. **Flag non-obvious structure**: GPs vs. LPs ("These are GPs, not LPs. The ask is…"),
   "nobody on stage is a deal", "no multilateral is published", unannounced attendees
   from prior years.

**Fetching friction:**

- **Cvent event sites** render their lists (selected firms, LP logo walls, side events)
  inside iframes. Firecrawl returns an almost-empty page and `document.body.innerText`
  misses the iframe content. Use the Playwright MCP, save `browser_snapshot` to a file in
  the scratchpad, and parse it there. Sub-pages (e.g. `/<event>/2026-agenda`) may hold
  content the home page doesn't link.
- **The prior year's archived page** (on the organizer's main site) often has the
  rules (who gets the participant list, how 1:1s are requested) and the previous
  speakers. Use it, and mark everything from it "prior year; 2026 attendance unverified".
- **LinkedIn is blocked** for Firecrawl. A Tavily search surfaces "selected for /
  speaking at <event>" posts well enough to confirm names.
- **Bulk CRM matching** of hundreds of names: an `or` of ~90 `ilike` tokens per
  `find_many_companies` call works, but generic tokens produce false positives
  (`Maven` → Maven Clinic, `Scop` → Descope). Verify every hit before marking it **CRM**.
  For `lists`-type fields, filter with `containsAny`; `in` errors.

**More friction:**

- **Check what year the lists are before assuming.** A homepage can still link last year's
  lists while the speaker and program pages are already this year's. Label every entry by
  year and treat prior-year-only lists (logo walls, side-event catalogues) as map-only.
- **Server-rendered sites:** `curl` plus HTML parsing beats Firecrawl markdown. Strip
  `<script>` blocks first, or inline JS pollutes the name lists.
- **Logo-only sections** (selection committees, last year's cohort) carry no names. Get
  them from image filenames or from social posts (Tavily advanced search finds the
  LinkedIn and Instagram announcements).
- **Sibling events across series:** organizers co-host ("Brand x Brand" events). Read
  the existing series notes for cross-references before building a new map.
- **Name matching:** constrain people matches on first *and* last name. Never substring-match
  short firm names (EQT matched eleQtron, NEA matched Linear, First matched FirstMark).

**Inferring the operator's own lens:** when the lens is the operator's and they don't
state the goal, read the routed CRM's `funds`, `theses` (`fundVehicle`), and
`lp_profiles` first. Put the inferred lens at the top of the map as an **assumption to
confirm**, never as fact.

### Phase 3 — The prep map (`Event-Instance`, `Event-Map`)

Filename: `<Series> <Year>.md` in the routed folder. One file per instance. Skeleton in
[`references/templates.md`](references/templates.md). Sections, in order:

1. **Header paragraph**: event link, dates, venue, format, size; *for whom*; what it
   was built from (public list / CRM / web research, with dates); "Nobody here has been
   met yet."
2. **Lens**: the two to four kinds of contact wanted, in one bold-labelled line each.
3. **Priority key**: `A` = seek out, prepared ask. `B` = worth a deliberate
   conversation. `C` = only if it happens naturally. `CRM` = already in the CRM.
   Modifiers `A-` / `B+` are allowed. No neutral tier.
4. **Segments at a glance**: one table, segment → organizations, with segment names
   as `[[#anchor]]` links.
5. **One section per segment**: a table of `Organization | What they do | Role at event |
   Contacts | <Lens> relevance | Pri.` A one-line framing sentence under the heading when the
   segment needs it.
6. **Operator / founder prep**:
   - *The one-line positioning* for this specific room, and how to angle it for this
     audience ("lead with freshwater as the ocean's upstream").
   - *Top N conversations, in order*: `# | Who | Ask | Opening line`. Each ask is concrete.
     Each opening line is something you could actually say, and references a fact you found.
   - *Sessions to attend* (when the agenda is published): `Session | Why | When`.
     Also list what to **skip** and why.
   - *Protocol*: forms of address, deference, who routes through whom, what not to
     imply, how to follow up (especially with government and political figures).
   - *Posture*, when the host is itself a target or competitor (Cloudflare Connect:
     "work the room, not the host").
   - *Logistics* when travel is in play: arrive/depart, hotel radius, pass tier,
     adjacent events worth extending for.
   - *Before the event*: a numbered checklist (outreach a week out, warm-path check
     with the client so no one is approached twice, one-pager to bring).
   - *Dates to hold*: follow-on deadlines and events surfaced during research.
   - *After the event*: which CRM instance and event record to log against.
7. **Sources footer** (italic): the event pages and fetch dates; the CRM instance and
   which records were pulled, with the date; web sources by domain; then an explicit
   **Unverified:** list.

### Phase 4 — Seed the CRM (propose, then write)

The prep map points at CRM records. Before writing any:

1. Present the proposed writes as a table: the `event_series` (and parent), the
   `event_instance` (dates, location, website, ticket cost), and one
   `event_participation` per organization or person seen on the public list. Mark which are new
   and which enrich an existing record.
2. Wait for the operator's go-ahead. Then write following `lossless-crm-interface-guidelines`
   (dedupe, fetch first, provenance).
3. Pre-event participations are **observations**: `metInPerson: false`, a
   `participationRole` from `SPEAKER | SPONSOR | EXHIBITOR | ORGANIZER | ATTENDEE |
   PORTFOLIO_PRESENT | UNKNOWN`, and `participationNotes` saying where it was seen
   ("Speaker, '<session>' (<room>, <time>). Seen on session card; not met.").

Reserved-name pitfall: the object is `eventInstance`, not `event`.

### Phase 5 — At the event

Capture is the operator's job. Make it cheap: badge photos, business cards, booth
photos, session slides. A photo of a badge is not a conversation. Keep the two apart
from the moment of capture.

### Phase 6 — Log touchpoints

For each captured touchpoint, in the routed instance:

- An **Interaction**, named `Met <Person> (<Org>) at <Event>`, or `Met <Org> at <Event>
  (booth)` when no name was captured. Set `interactionDate` to the day it happened, `channel`, and
  `direction: MUTUAL`. The `summary` says what the evidence is ("exchanged business card",
  "seen via badge photo", "visited booth; no contact name captured").
- Flip or create the matching **event_participation** with `metInPerson: true` and
  "See interaction record." in its notes.
- The companion **timeline rows** and multi-party **interaction participations** follow
  the CRM skill §5. Don't restate them here, but don't skip them.
- Fill the instance's ROI fields: `costTicket`, `costTravel`, `daysSpent`,
  `worthRepeating` (`YES | MAYBE | NO | TOO_EARLY`).

### Phase 7 — Recap re-sync

Regenerate the map from the CRM, not from memory. Pull every participation and every
interaction tied to the instance, group by segment, and rewrite the map (Yotta 2026 is
the reference shape):

- Header: "Every organization in the <instance> CRM tied to **<Event>**", count, and
  what it was drawn from.
- **Touchpoint key** replaces the priority key: *Met in person* = conversation or card.
  *Booth / badge* = visited or photographed. *Speaker / host / pitch* = seen on stage, not
  met. *Observed attendee* = on a list or slide, not confirmed met.
- An **Off-Theme or Unverified** section and an **Unaffiliated contacts** list.
- **Observed themes**: three to six bold-led bullets on what the floor was actually about.
- Footer: `*Source: <instance> Twenty CRM, eventInstance '<name>', pulled <date>,
  re-synced <date>.*`

A prep map turns into a recap map in place (same file, `Event-Map` tag kept), or as a
sibling `<Series> <Year> Event Map.md`. See drift notes. Keep the prep sections the
operator still wants for next year's repeat.

---

### Awareness mode (not registered, not attending)

Get value from an event just by knowing it is happening, without registering or
attending. Skip Phases 5–6. Instead:

1. **Event records:** create the series and instances in Twenty as usual, with `costTicket` 0,
   `daysSpent` 0, `worthRepeating: TOO_EARLY`, and an `eventNotes` line naming the experiment and
   a grading date about 90 days out.
2. **Observations only:** one `event_participation` per (organization, instance) with
   `metInPerson: false` and the most significant role (fold any other roles into the notes).
   Give it a non-empty name, `<Org> @ <Instance> (observed)`, and notes recording the source
   list and fetch date. **Never create Interactions.**
3. **New companies** get minimal fields plus `needsReview: true`. Set a domain only when the
   source page or a fetched site confirms it.
4. **Vault notes:** new VC firms go in `vertical-toolkits/Venture-Capital-Firms/` and named
   speakers in `Sources/People/`, both with `publish: false` and an "Observed at … Observed,
   not met." line. Wikilink the prep map with vault-root paths
   (`[[Sources/People/X|X]]`). The vault folder is `Sources/`; the repo folder is `sources/`.
   Index the whole vault first so you link an existing note instead of duplicating it.
5. **Grade it:** on the grading date, count observed organizations that turned into a
   conversation, deal flow, or an LP lead, then set `worthRepeating`.

**Bulk-write pitfalls:**

- Batch writes cap at 20 records per call and return only IDs. Append each batch's IDs to a
  scratchpad manifest so it can always be rebuilt.
- Dedupe by domain *and* name. Domain catches what name matching misses ("14B Venture Capital"
  vs "14B.vc"). Short names need exact patterns (`"X"`, `"X %"`), not `%X%`.
- Roster "firm" strings don't match company names ("Sequoia", "Langdock / Visionaries
  Club", "Baobab Ventures (ex ElevenLabs…)"). Map them to company records explicitly before
  linking people. Take each participation's source URL from that event's own page, not from
  whichever list first surfaced the organization (that may be last year's).
- Clicking a bare `[[Name]]` in Obsidian creates an empty note at the vault root. Point links at
  the real path, and remove the 0-byte stub only when it collides with a real note.

## 4. Discipline that runs through every phase

- **Mark the unverified.** Inline ("(unverified)", "owner and date unverified") and again
  in the footer list. A list of who's speaking isn't proof of who's in the room, and a
  badge photo isn't proof of a conversation.
- **Disclose model knowledge.** Same rule as the CRM skill §3.3. Never invent a title,
  AUM, fund size, or attendance.
- **Rank, don't list.** Every organization gets a priority. Every top conversation gets an ask
  and an opening line. A plan that doesn't say who comes first isn't a plan.
- **Name the shared contact.** When the CRM holds a relationship at a target org, put the
  name in the Contacts cell and in the opening line.
- **Analysis lives in the file, not the chat.** Findings go into the map. The chat gets a
  short summary and the path.
- **Wikilink what exists.** Link organizations and people that already have notes. Don't create
  stub notes for every name as a side effect.
- **Dates are absolute.** "Oct 22, 2026", never "next Thursday".

---

## 5. Anti-patterns

- Treating the published speaker list as the attendee list.
- Writing "Met" on an Interaction whose only evidence is a badge photo, without saying so
  in the summary.
- Writing CRM records from a prep run before the operator has approved the proposed
  writes.
- Pitching the host at its own event when the host is the end-game target (posture
  failure).
- A priority column with no `C`s. If everything is A or B, nothing was ranked.
- Opening lines that are generic ("Love what you're doing in climate").
- A recap written from memory instead of re-synced from the CRM.
- Logging interactions with no `event_participation`, so the event's ROI query can't
  see them.
- Silent normalization of older event notes while prepping a new one. Note drift and
  leave it.

---

## 6. Worked examples

| Example | Shape | Lens | Path |
|---|---|---|---|
| OceanX 2026 | Prep map, client lens, full operator-prep section | TWF | `content/sources/Events/OceanX 2026.md` |
| Cloudflare Connect 2026 | Client plan: posture, travel, ranked speakers, sessions, schedule | LFG | `content/client-content/Link-Freedom-Group/Events/Cloudflare-Connect-2026.md` |
| Yotta 2026 | Recap map re-synced from CRM | Lossless | `content/sources/Events/Yotta 2026 Event Map.md` |
| Deep Tech Week ATX 2026 | Observed-only map (not attended) | Lossless | `content/sources/Events/Deep Tech Week Austin TX 2026 Event Map.md` |

### Worked example: RAISE Global Summit 2026

`content/sources/Events/RAISE.md` (series) and
`content/sources/Events/RAISE Global Summit 2026.md` (prep map). This was the first
run against the drafted skill.

- **Lens:** the operator's own, inferred from the Lossless Twenty and flagged as an
  assumption. It has two sides: a Hypernova venture partner sourcing emerging managers
  (the 101 RAISE Select GPs), and HumainVC fundraising (the 330+ LPs).
- **Source list:** no attendee export, so public research only. The Cvent iframes
  (Select roster, LP logo wall, side events) yielded about 200 names via Playwright.
  Thirteen Select firms and six LPs were already in the CRM.
- **What the gap cost:** LP attendance is inferred from a logo wall, not a participant
  list. Every attendee receives the list after registering, so for a registered operator
  that list should replace the logo-wall guesswork.
- **CRM writes:** proposed in the map's "After the event" section; none written yet.
  Approval status: _pending_.
- **Skill corrections from this run:** the Phase 2 fetching-friction notes and the
  lens-inference step.
