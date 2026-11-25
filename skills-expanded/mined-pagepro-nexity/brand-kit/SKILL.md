---
name: brand-kit
description: Use when asked to build, generate, refresh or reverse-engineer a brand kit, a `BRAND.md`, brand foundations or a brand voice profile for a company from its website URL — "zrób brand kit", "brand kit for <company>", "fill in BRAND.md", "what does our site actually say about us", or when preparing a company's site for AI content production. Reads the public site and its listings, writes a short `BRAND.md` that people and AI agents work from, and a report of what the site contradicts or cannot prove. Written for the team that owns the site; works on any company's site. Needs only a public URL to start.
---

# Brand Kit

Reverse-engineer a brand from public sources and hand over two things:

1. **`BRAND.md`**: a short file (under 200 lines) in the structure every Nexity project
   uses, which a person or an AI agent reads before writing copy, building a section or
   working in another system. This is the product.
2. **The report** (`brand-kit.html`): the same brand at a glance, with every fact linked
   to its source, the conflicts between pages, and the questions only the company's own
   people can answer. This is the proof, and the to-do list.

**Core principle: nothing enters the kit without a source.** Every number, customer
name, partnership and claim must have a row in `evidence.md` with the URL it came from.
A fact you cannot source becomes a question, never a sentence. A sentence that is your
reading of the site and not something the site or a customer said is marked "inferred".
A short kit with honest gaps beats a fluent one with invented retention rates.

**Second principle: short enough to be used.** The research is wide, the kit is narrow.
Every field has a length limit in `brand-template.md`. What does not fit stays in
`evidence.md`. If a section reads like an essay, it is wrong.

## 0. Setup

Input: the company's website URL, usually your own. That is all that's required; extra
materials (decks, docs, review exports) are welcome additions to the evidence base.

Create the run directory `.brand-kits/<company-slug>/` in the project root (slug = bare
domain without TLD, e.g. `acme`). All outputs land there. It is working material about a
company: add `/.brand-kits/` to the project's `.gitignore` if it is missing. If the
directory exists from an earlier run, this is a refresh: see §9.

When the company is the one that owns the project, its own materials (case studies,
internal docs the user hands over) count as sources too; cite them in `evidence.md` like
any page.

If `.site-contradictions/<slug>/evidence.md` exists and is less than 30 days old, read
it first: it has the same row format, so reuse its rows and its contradictions and fetch
only what it lacks. One company, one set of facts.

## The data file and the build

You write two files by hand in the run directory, and a script writes the rest:

- **`kit.json`** holds everything the research finds and everything the report shows:
  the evidence rows, voice samples, sources, conflicts, claims, questions, and the short
  texts of the report's top half. `kit.example.json` (same directory as this skill) is a
  complete small example: copy its shape.
- **`BRAND.md`**, written from `brand-template.md` (§5).

Then run `python3 <this skill's directory>/build.py <run directory>`. It numbers the
evidence rows (`e1..eN` in the order of the `evidence` array), writes `evidence.md`,
`claims.md`, `gap-questionnaire.md` and `brand-kit.html`, fills every count, and refuses
to write anything while a check fails (a proof line that cites an unverified or
conflicted fact, a question with two question marks, a conflict with no action, a
`BRAND.md` over its limit or pointing at a question that does not exist). Fix what it
reports and run it again. `--check` runs the checks without writing.

Every report shows the version of the plugin the skill ships in (Nexity Marketing
Skills) next to `/brand-kit` in the top bar and in the footer, and `evidence.md` opens
with it, so a reader can tell which release a run followed. The build reads the number
from the plugin's own manifest (`.claude-plugin/plugin.json` of an installed copy, or
the repository's `.claude-plugin/marketplace.json`); it is never typed into the skill.
A copy of the skill with no manifest above it shows no version. To change the number,
bump the plugin's `version` as `CONTRIBUTING.md` says.

Three marks work in any text field of `kit.json`: `{key|words}` links the words to the
evidence row with that key, `{v3|words}` to voice sample 3 (strong samples are 1 to 10,
weak ones follow from 11), and `[i]…[/i]` marks a sentence as your reading, not a
sourced fact. Never number rows yourself: refer to them by key, and add, drop or reorder
rows freely.

The sections below say what goes into each part of `kit.json`; where they describe a
file the script writes, read it as the matching part of the data. Without Python, write
the four files by hand in the formats the sections describe and fill `html-template.html`
slot by slot: its comments show the markup for each.

## 1. What kind of company this is

Read the homepage, the main navigation and the pricing or shop page first, and write
three lines before anything else (`type` in `kit.json`; they open `evidence.md`):

- **Sells:** what, in the site's own words.
- **To:** businesses, consumers, or both.
- **How:** a sales conversation, a self-serve plan, a basket and checkout, an app
  store, in person, or donations and membership.

From those, name the type. It decides where customers speak, which outside records
exist and what shape the offer takes. Nothing else in the skill depends on it.

| Type | Customers speak on | Outside record | The offer is |
|---|---|---|---|
| B2B services (agency, consultancy, studio) | Clutch, G2, quotes in case studies | partner directories, company register | service lines: for whom, proof, price |
| Software (SaaS, apps, developer tools) | G2, Capterra, app stores, community forums | status page, integration listings, changelog, public repository | plans: price, limits, for whom |
| Shop (e-commerce, consumer brand) | Trustpilot, Google, reviews on product pages, marketplaces | marketplace storefronts, returns and delivery terms | categories and best-sellers, delivery and returns |
| Local business (venue, clinic, trades) | Google Maps, TripAdvisor, booking platforms | the map listing, trade or licence registers | services, area served, opening hours |
| Organisation (charity, association, school) | stories from the people it serves, member quotes | charity or company register, annual report | programmes and ways to take part or give |

The table is a starting list, not the rule. **The rule is: follow the site first.**
Badges, "read our reviews on…" links, partner logos, app store buttons and footer links
say where this company's reviews and records live; read those before anything from the
table, and skip a table source the company plainly does not use. A company that is two
types at once (software with a services arm) gets a main type and a second one, and the
sources of both. A type that is not in the table gets its own three answers.

## 2. Research sweep

Collect raw material as rows of the `evidence` array before writing a single kit
sentence: a short `key` you choose, the `fact`, the `url` and the verbatim `quote`.
Sweep, in order:

1. **The site itself.** Start from `/llms.txt` and `/sitemap.xml` when they exist (a
   Nexity site serves every page as Markdown at its URL plus `.md`; read that twin).
   A Markdown twin can leave out what the page renders from components: stat blocks,
   pricing tables, the header and the structured data. Read the HTML as well for the
   homepage, the contact page and every page that sells something, and take the
   `application/ld+json` block from the homepage (founding date, legal names, review
   count).
   Then the homepage, about page, every page that sells something (walk the main
   navigation and the footer, which often lists lines the nav hides), pricing, careers
   (team size, locations), contact and legal pages (entity, addresses, years). For a
   shop, read the category pages, the 5 to 10 products the site features, and the
   delivery, returns and guarantee pages; not the whole catalogue.
2. **Proof in depth.** Read in full the 3 to 4 pages the site leans on most as proof:
   case studies for services and software, the best-reviewed products for a shop, the
   impact or results pages for an organisation. A page the kit will call the flagship
   needs its key numbers in `evidence.md`, with the tool and date when the page gives
   them. Fewer than three proof pages read in full means the sweep is too shallow,
   unless the site has fewer; then say so. (A dense about page that supplies a fifth of
   the facts is normal, and is not a sign of that.)
3. **Writing samples for voice.** 3 to 5 pieces of the site's own long writing (blog
   posts, guides, product descriptions, campaign pages; recent and most-linked), plus
   the proof pages above. Save 5+ verbatim sentences that show how the brand writes at its
   best, and 5+ from its weakest pages. Count the filler words on the pages read
   ("seamless", "cutting-edge"...) and the devices the base rules ban (em dashes,
   "not X, it's Y").
4. **Customers in their own words.** The review source for this company (§1: what the
   site links to, then the table): rating, review count, and the text of up to 10
   recent reviews. Plus testimonials on the site that name a person, and customer
   quotes on the proof pages. For consumer reviews, save what the person wanted, what
   nearly stopped them and what they say afterwards; a first name and the platform are
   attribution enough. A review site that refuses the fetch gets one plain
   request and no more: log it under "Not fetched" and use the named quotes the company
   publishes. Save verbatim sentences under `## Customer
   language`: the problem they had, why they chose the company, what they doubted. These
   feed Audiences. No reviews found is a finding: log it.
5. **Third-party record.** The outside records for this type (§1), wherever the site
   makes a claim an outsider can confirm: a partner or reseller status, a
   certification, a marketplace storefront, a register entry, a public repository. Add
   the company register and, when it loads, the LinkedIn page (headcount range,
   founding year). Check a claim at the place that would know, not at a random mention.
6. **Search backfill.** `"<brand>" review`, plus the proof word for the type (`case
   study`, `partner`, `returns`, `complaints`), for anything the sweep above missed.

`evidence.md` is a markdown table, one row per fact, ids `e1..eN` in file order:

```
| Fact | Source URL | Verbatim quote or number |
|---|---|---|
```

One fact per row. A row that would hold a settled value and a disputed one (a rating
that is fine next to a review count that differs between pages) is two rows, so the
report does not paint the settled value as a conflict.

Plus these sections: `## Sources checked` (one line per page fetched: URL and what it
yielded, including "nothing"; web searches that yielded a fact without a page fetch get
one prose line at the end and do not count toward `{{SOURCE_COUNT}}`); `## Voice
samples` (strong, then weak, each with its URL); `## Customer language`; `## Not fetched
/ not found`.

Fetching gotcha: on JS-rendered sites the fetch tool may return only the page `<title>`.
Don't retry it in a loop: fall back to `curl -sL <url>` via Bash and strip the HTML.
Skip any URL that doesn't respond promptly, log it under "Not fetched" and move on.

Budget: the sweep is done when new pages stop yielding new facts, typically 20 to 40
pages. Log what you could NOT find as you go. That list becomes §6.

## 3. Voice analysis

From the voice samples (never from your impression of the industry), write a `## Voice
analysis` section at the end of `evidence.md`: sentence length and register; how claims
are backed (numbers, named clients, cited sources); which pages hold the strongest
writing and which the weakest; the filler-word and device counts. End it with a
decision: **which pages are the model** for new content. When the site has two voices
(new pages and old ones), say so and pick one, with the reason.

## 4. Claims register

From `evidence.md`, extract every checkable claim the company makes publicly into
`claims.md`.

**Conflicts first**, numbered C1.., most damaging first (a conflict = sources state
different values for the same fact). Each conflict has:

- both values, each with every page it appears on;
- exactly one action. **Fix now** when a source already settles it (the company
  register, the linked profile, the page that is plainly newer): the text to change and
  the pages to change it on. Otherwise **Ask `<role>`**: one question, and the role best
  placed to answer it (CEO, sales lead, delivery lead, marketing, legal). The role is a
  suggestion; the team reassigns;
- the wording a writer uses until it is settled ("write that X removes setup work and
  give no percentage").

**Then the other claims**, a table `| claim | on record / note | status | evidence refs |`
sorted weakest first, with status one of:

| Status | Meaning | A writer may |
|---|---|---|
| `unverified` | a strong claim with no source a reader can check | not use it |
| `tension` | figures that collide when cited together | check first |
| `single source` | stated in one place by the company | use it |
| `third-party` | stated only off-site (a directory, a review site) | use it, naming the source |
| `corroborated` | two independent sources agree | use it |

A claim row cites only the evidence rows that state that claim. Rows that merely bear
on it are named in the note, in words: the report marks every cited row with the
claim's status, so citing a solid case study result under an unverified general claim
would mark the result as unverified too.

A claim lives in the C-list or the table, never both. `{{USABLE_COUNT}}` is the number of
rows with the last three statuses, `{{CHECK_COUNT}}` the number with the first two.

## 5. Write `BRAND.md`

Fill `brand-template.md` (same directory as this skill) top to bottom into
`.brand-kits/<slug>/BRAND.md`. The template's placeholders are the spec: follow their
limits. Rules that override fluency:

- **Usable facts only.** A figure with a conflict row, a `tension` or an `unverified`
  status never appears as proof, an outcome or a promise. It goes under "Open decisions"
  with the wording to use meanwhile.
- **Proof points** are `corroborated`, or `single source` with a named client, a tool
  and a date.
- **"Needs to see" is your reading** unless a customer said it: the report marks the
  line "inferred" when it cites no evidence row. That is fine. Inventing a quote to
  avoid the mark is not.
- **Audiences come from evidence.** A business buyer is a role in a situation ("Head of
  Digital whose team has outgrown the CMS"). A consumer is a person at a moment ("a
  parent buying a first bike before the summer"): the occasion and the need, never an
  age bracket. Each has a sourced situation and, when the research
  found one, a verbatim customer sentence. A fear or a need with no row behind it ends
  with "(inferred)", one per audience at most. Two well-evidenced audiences beat four
  guessed ones.
- **Voice is shown, not described.** The "Write / Not" table holds verbatim sentences
  from the site, both columns. Rules are the ones this brand's best pages already keep.
  Do not copy general AI-writing rules into the file: that is `work-humanizer`'s job.
- **The offer is how the company sells today,** in the shape its type calls for (§1):
  service lines, plans, categories with best-sellers, services with area and hours, or
  programmes. 3 to 8 rows, the main one first. Fold thin or legacy pages into their
  parent row (a footer with 25 service pages is a navigation choice, not 25 lines), and
  never list a catalogue: a shop's rows are its categories, with one or two named
  products each. What every buyer needs whatever they pick (delivery, returns,
  contract term, opening hours) gets its own last row.
- **Team-only fields stay honest.** The promise (when the site states none), the
  personality table and the principles are the team's to state. With no answer yet the
  field is left out and listed under "To fill in"; never
  invent a personality.
- Write in English regardless of the site's language, unless asked otherwise.
- The file's own prose avoids the words it tells writers to avoid. Verbatim quotes stay
  untouched even when they break a rule.

## 6. Questions for the team

Write `gap-questionnaire.md`: what the public site does not say and content needs.
Conflicts are not repeated here: each carries its own question in `claims.md`.

- **One question per row.** One question mark. A row that needs "and" is two rows.
- **Each row names a role** to answer it and one line on why it matters for content.
- **At most 8 rows**, most useful first. More than 8 candidates: keep the 8 that unblock
  the most content, and list the rest under `## Later` (not shown in the report).

Typical gaps (ask only what the research failed to answer): the method behind a proof
metric; which line, plan or category leads; which audience is the priority; what the
company deliberately does not do; the promise in one sentence; three "is / is not"
personality traits; whether a signature device of the brand's writing (em dashes,
negative parallelism) overrides the usual hygiene. By type, the gaps that recur: for
services, retention and what a named result was measured against; for software, what a
plan limit means in practice and which integrations are official; for a shop, who
settles a delivery or returns term stated two ways; for a local business, the area
served and who owns the map listing; for an organisation, the period and the source of
an impact figure.

## 7. The report

Run the build (see "The data file and the build"). It renders `brand-kit.html` from
`html-template.html`, whose design is documented in `DESIGN-NOTES.md`: do not restyle
it.

What you supply in `kit.json` for the top half, with the same limits as `BRAND.md`:
`one_liner` (30 words at most), two or three `fields` of two sentences (the "does not
do" field only when the site or the team states it), 3 to 6 `proof` lines, the
`audiences`, the `voice_line`, the voice `pairs`, `rules`, `words` and `pages`, the four
`offer_head` headings that fit the type, and one `offer` row per line (mark the row for
what applies to every purchase with `"shared": true`). Wrap every claim that has an
evidence row in `{key|words}`: provenance links are the point of the page.

What the build does for you: the brief under the masthead (the first five conflicts, or
the ones you list in `brief`; with no conflict at all, the unverified claims a writer
would reach for), every count, the status marks on fact links, the conflict tags, the
cross-links and the Copy buttons. It embeds `BRAND.md` whole, so run it again whenever
`BRAND.md` changes, for instance after the interview (§8).

What it cannot judge, and you check by reading the page once: that each "words" inside a
`{key|words}` link says what its evidence row says, and that nothing in the top half is
a paragraph where a sentence was asked for.

If your agent can publish an artifact (Claude's Artifact tool), publish
`brand-kit.html`: icon `card`, title from the file's `<title>`. First publish for a
company gets a new URL; a refresh passes the existing artifact URL as `url` so the link
stays stable. The artifact is private until the user shares it: say so when handing over
the link. Without an artifact tool, the handover is the local file: give its path and
suggest opening it in a browser.

## 8. Self-check, deliver, then close the loop

**Self-check.** The build runs the mechanical half of these on every run (limits,
references, statuses, counts). The reading half is yours.

1. **Source audit.** Grep `BRAND.md` and the report's top half for every digit-bearing
   claim; each must match an `evidence.md` row exactly (surrounding prose may
   paraphrase). Remove or move to a question anything unmatched.
2. **Usable-facts audit.** No figure from a conflict, a `tension` or an `unverified` row
   outside "Open decisions" and the Conflicts section. Prices count: a price in
   `tension` is an open decision, not an offer line.
3. **Reference audit, on `BRAND.md` line by line.** Every `question N` and `C N` points
   at a row that asks or states exactly that. Every source path equals the URL of its
   evidence row. Every sentence that is not a quote, a sourced fact or one of the three
   "To fill in" rows is checked: if it explains, guesses or states a rule the site
   never states (how a name is capitalised, why a field is empty), delete it. "Absent"
   lists only what does not exist; what exists and was not read goes under "Exists, not
   read in this run".
4. **Length audit.** `BRAND.md` under 200 lines without "Open decisions", no `<...>` placeholder left, all
   template headings present ("Principles" may be left out, see the template), every
   field left out has its row under "To fill in"; the questionnaire at 8 rows or fewer, one question mark
   each.

**Deliver** the report (artifact link, or the file path), the path to the draft
`BRAND.md` with the note that the report's "Copy BRAND.md" button gives the same file, and a 5-line summary: the one-liner, the strongest usable proof, the
conflict count with the worst one, the top 3 questions. Do not paste the kit into chat.

**Then, when the user is from the company:**

- **Interview.** Ask the questions that only need the person in front of you, starting
  from the "To fill in" list (promise,
  personality, principles, flagship, priority audience), 5 at most, one at a time or as
  one short form. Write each answer into `BRAND.md` in their words, marked "from the
  team", and strike the row from the questionnaire. Skipped questions stay open.
- **Resolve.** When the team answers a conflict ("brand-kit resolve", or the answers
  pasted into chat): move the settled value into "Capabilities and claims", delete its
  "Open decisions" line, and write `fix-list.md`: one row per page still showing the
  old value, `| page | text now | change to |`. In a project that owns the site, offer
  to make those edits through the project's own content workflow. Never write to a CMS
  or a live site unasked.
- **Install.** In a project that keeps a root `BRAND.md`: when its first line is the
  `brand-template` marker, offer to replace it with the draft. When it is already
  filled, show a section-by-section diff and ask per section. Never overwrite a filled
  `BRAND.md` without asking, and never replace text the team wrote with text read from
  the site.

## 9. Refresh

A run directory from an earlier run means the site may have moved. Keep the old
`evidence.md` as `evidence.prev.md`, run the sweep again, and lead the delivery with
what changed: conflicts closed, new conflicts, claims whose value changed, prices that
changed. Lines in `BRAND.md` marked "from the team" survive a refresh untouched. Pass
the existing artifact URL when publishing so the link stays the same.

## 10. Compare mode

`brand-kit compare <slug-a> <slug-b>` (`/brand-kit compare …` in Claude Code): a
competitive comparison of two finished runs, judged through slug-a's lens (slug-a is
"us"). Both `.brand-kits/<slug>/` runs must exist; generate any missing one with the
normal pipeline first. The comparison is **internal working material**, never published.

1. Read both runs' `BRAND.md`, `claims.md`, `evidence.md`, `gap-questionnaire.md`.
2. When slug-a is the user's own company, ask for any internal competitive notes and
   cite them like evidence.
3. Write `.brand-kits/<a>-vs-<b>/comparison.md` covering, in order: verdict (wins /
   where they're stronger / attack surface, i.e. their conflicted or unverified claims /
   worth adopting), positioning head-to-head, proof density (counts from both claims
   registers), claims head-to-head (shared categories, both values, who is better
   evidenced **on the record**), service map (line-by-line: head-to-head / only-us /
   only-them, packaging differences), ICP overlap (same-buyer collisions first), voice.
   Every judgement cites the underlying claim or evidence entry by id and run
   (`acme e13`).
4. Fill `compare-template.html` (same directory as this skill) exactly as §7 fills the
   report template: replace `{{A_NAME}}`, `{{A_DOMAIN}}`, `{{B_NAME}}`, `{{B_DOMAIN}}`,
   `{{RUN_DATE}}`, `{{H2H_COUNT}}`, and `{{A_ARTIFACT_URL}}` / `{{B_ARTIFACT_URL}}`
   (each run's published report link, or `../<slug>/brand-kit.html` without an artifact
   tool), fill every `<!-- SLOT: ... -->`, run the same self-check, write
   `.brand-kits/<a>-vs-<b>/comparison.html`, and publish it like §7 (stable URL on
   refresh) when the agent can.
5. Deliver: the comparison (link or path), both report links or paths, `comparison.md`
   path, and a 5-line verdict summary in chat.

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing "Who we are" from industry knowledge | Only facts with an `evidence.md` row enter the kit |
| Filling the HTML template by hand and numbering rows yourself | Write `kit.json`, refer to rows by key, run `build.py` |
| Looking for every company on Clutch, G2 and partner directories | Name the type first (§1), follow what the site links to, then the table |
| A consumer audience written as a job title or an age bracket | A person at a moment: the occasion and the need |
| A shop's offer as a list of products | Categories with one or two named products, and a row for delivery and returns |
| A paragraph where the template asks for a sentence | Cut to the limit; the detail is already in `evidence.md` |
| Describing voice with adjectives ("professional, friendly") | Put two real sentences side by side in the table |
| Audience fears written as facts | Source them from reviews, or mark the sentence "(inferred)" |
| A conflicted figure used as proof because it is on the homepage | It goes under "Open decisions" until the team settles it |
| Bundling three questions into one row to stay under the limit | One question mark per row; the overflow goes under "Later" |
| Leaving a conflict with "see question N" and nothing else | Every conflict has "Fix now" or "Ask `<role>`", and the interim wording |
| Copying general AI-writing rules into `BRAND.md` | Brand rules only; `work-humanizer` holds the general ones |
| Inventing a personality or a promise to fill the section | Leave it out, list it under "To fill in", and ask |
| A note about a gap inside a section ("Not decided yet…", "the mission follows the flagship") | Leave the field out; one row under "To fill in" |
| "(question 3)" when question 3 asks something else | Check every number against the questionnaire |
| Listing a review or a profile as absent because the fetch failed | "Exists, not read in this run" |
