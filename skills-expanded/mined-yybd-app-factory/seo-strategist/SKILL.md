---
name: seo-strategist
description: >-
  The SEO lead for a website in the age of AI answers: sets an exposure target from a
  measured baseline and judges each period against it, decides what would actually move
  it — a fix, a rewrite, a new page, off-site work — plans content from real demand, and
  writes the brief an article is then written from. Covers classic search, AI answer
  engines and agents, and re-checks its own dated knowledge. Use when the user wants to
  promote a site in search, asks for an SEO strategy or a content plan, what to write
  next, an article brief, an exposure target, whether the site is on target, how to be
  cited by ChatGPT or AI Overviews, or when a new site is being planned ("קדם את האתר",
  "אסטרטגיית SEO", "יעד חשיפה", "מה כדאי לכתוב", "שרטט מאמר", "איך להופיע בתשובות AI").
  It does NOT take the reading or audit pages — `web-seo` does — does NOT write the
  article (`article-writer`) or edit wording (`copy-edit`), and never publishes or posts.
---

# seo-strategist — the target, the plan, and what to make next

A site is found when four things hold in order: the right bots can reach it, it is in
the indexes answers are drawn from, it ranks for what people and engines actually
search, and what it says is worth quoting. This skill owns the judgment across all
four: **where the site should be, whether it is getting there, and the cheapest thing
that would move it.**

It is one of three. **`web-seo`** is the technician — it audits pages and takes the
reading. **This skill** reads that reading against a target, decides, and briefs.
**`article-writer`** writes from the brief. The strategist never writes prose and never
publishes; it ends in a decision, a brief, or an instruction to another skill.

**What it knows is dated.** [references/knowledge.md](references/knowledge.md) is the
state of the evidence on a named day, distilled from six research reports kept in this
skill's source repository. Search changes under it, so the skill
carries the list of facts likely to have moved and re-checks them (§6). What running it
taught is in [LESSONS.md](LESSONS.md).

**It works for any site.** Nothing here assumes an app, a studio or a hub. What the site
is for, where its facts come from and where this skill keeps its records are named in
the site's own descriptor, `.claude/seo-site.json` — the shape is in `web-seo`'s
[site-descriptor.md](../web-seo/references/site-descriptor.md):

| descriptor key | what it tells this skill | without it |
|---|---|---|
| `state_dir` | where readings, targets, actions, briefs and the panel are kept | `.seo/` in the site's repo |
| `brand_terms` | the pattern that separates branded queries from the rest | ask the owner once, and record it |
| `conversion_events` | the action the site exists for | ask; a site with no conversion has only an exposure target |
| `product_facts` | the source of truth for what the product is | the site's own product document or pages |
| `voice` | the document that says how this site writes | the site's shipped copy sets the standard |
| `articles` | where article sources live, in which languages, and the build command | the writer asks |
| `offsite_board` | an existing record of listings and outreach | one is started in the state directory |
| `video_pipeline` | the repo and entry skill that produce video from a brief | video briefs go to the owner |

## Prerequisites

- **Tools:** Python 3 for `scripts/seo_state.py`, `scripts/access_check.py`, `scripts/page_facts.py` and `scripts/volatile.py` (standard library only, nothing to install); a web search or fetch tool for the live checks and the knowledge refresh.
- **Credentials:** none of its own — the reading that feeds it is `web-seo`'s, with the credentials the site's descriptor names. A prompt panel run through an engine's API needs that engine's key, which the owner supplies and this skill never stores.
- **Hub (`$APP_HUB`):** optional — where the descriptor points `state_dir` or `product_facts` into a hub, that is where the records and the product's own words are; without one, both live in the site's repo.
- **Other tracks:** `copy-edit` and `store-metadata-writer` (shared-track) and `announce` (announce-track) are where some decisions are sent; none is required to run this.

## 0. Which run is this?

| the request | the run | section |
|---|---|---|
| a new site is being planned, or this is the first time on an existing one | **setup** — access, indexes, baseline, proposed target | §2 |
| "are we on target", the monthly read, a scheduled run | **review** — reading → verdict → one action | §3 |
| "what should we write", "content plan", "what would move this", a missed target that points at a gap | **plan** — one ranked backlog across pages, articles, store, video and off-site | §4 |
| "who are we up against", a new product, the yearly look | **compete** — who holds the result pages and the answers, and what they have that we do not | §4a |
| "brief this", "outline the article" | **brief** — and hand to `article-writer` | §5 |
| items overdue in `volatile.py due`, or "is this still true?" | **refresh** — re-check the dated facts | §6 |

A request that fits none of these and is about one page's wording, one page's markup,
or "why is there no traffic" is `copy-edit`'s or `web-seo`'s.

## 1. Every run starts the same way

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/skills/seo-strategist/scripts/seo_state.py status
python3 ${CLAUDE_PLUGIN_ROOT}/skills/seo-strategist/scripts/volatile.py due
```

1. Read the descriptor and `status`: what readings, targets and briefs exist, and what
   is due. A site with nothing recorded is a **setup** run whatever was asked.
2. Read [references/knowledge.md](references/knowledge.md), and
   `knowledge-updates.md` in the state directory if there is one — it holds what
   re-checks found since this copy of the skill was installed, and it wins where the
   two disagree.
3. **Check whether a Google core or spam update is rolling out** (the status page is in
   [references/volatile.json](references/volatile.json), item `core-updates`). During a
   rollout: no baseline, no verdict of "missed", no rewrite in response to a drop.
   Record it with `seo_state.py annotate`.
4. If `volatile.py due` lists items, say so in the report; re-check the ones this run
   leans on before leaning on them (§6).

## 2. Setup — a new site, or the first run on an old one

**For a site not built yet**, the strategist's part is
[references/build-checklist.md](references/build-checklist.md): the decisions that are
free now and expensive later — where each kind of content lives, one product one page,
languages as separate URLs, the conversion event, and the per-page list. `page-builder`
decides the structure; `web-seo`'s audit enforces the mechanical half once files exist.

**For a site that exists**, in this order, because each step is the precondition of the
next:

0. **The toolbox.** [references/tools.md](references/tools.md) lists what must exist
   (Search Console with API access or exports, a count of the conversion), what is
   recommended and free (Bing Webmaster Tools, the host's bot log, page-speed
   measurement), and what is optional and paid, in the order worth buying. Report
   present / missing, write it to `toolbox.md` in the state directory, and **stop on a
   missing required tool** before proposing any target.
1. **Access.** `python3 ${CLAUDE_PLUGIN_ROOT}/skills/seo-strategist/scripts/access_check.py`
   — the served `robots.txt` against the repo's, and the same pages requested as each AI
   user agent. A refusal here outranks everything below it. It catches user-agent rules
   only; where a CDN or host keeps a bot log, read that too
   ([references/agents.md](references/agents.md)).
2. **Indexes.** The site is verified in Search Console *and* Bing Webmaster Tools, the
   sitemaps are submitted, and a `site:` search in Brave returns it. Each engine answers
   from a different index ([knowledge.md](references/knowledge.md) §1).
3. **The audit and the reading** — `web-seo`. Do not re-implement either.
4. **Record the baseline**: one `seo_state.py record` per site for the last complete
   28-day period, with at least `nonbranded_impressions`, `impressions`, `clicks`,
   `indexed`, `indexable` and the conversion count. Name the snapshot it came from in
   `--source`.
5. **Propose the target**: `seo_state.py propose --site <host>`. It names the stage and
   proposes a threshold or a growth target with its basis
   ([references/targets.md](references/targets.md)). Where most impressions are on queries
   Search Console does not name, it sets the target on total impressions and says so. **Show it to the owner; they approve
   or change it; only then `set-target`.** A baseline taken during a core update is
   provisional and says so.
6. **The entity pass and the off-site board** —
   [references/offsite.md](references/offsite.md): one name everywhere, every profile
   pointing home. Drafted here, done by the owner.
7. **The prompt panel**: write `panel.json` in the state directory (15–30 prompts per
   site and language, in the three groups in targets.md) and take a first run, by hand
   or — if the owner agrees to the cost — through an engine's API.

## 3. The review — reading, verdict, one action

Every 28 days, and not sooner: nothing here moves faster, and a reading taken the
morning after a change reports it as a failure that has not happened yet.

1. Have `web-seo` take the reading. Record it: `seo_state.py record …`.
2. `seo_state.py review` gives each active target one of: **too early · blocked · on
   track · behind · below once · missed · met**. Only **blocked** and **missed** trigger
   work. *Too early* means leave the page alone; *below once* means wait a period.
3. Read what moved against the noise rules in targets.md: under twenty events, raw
   numbers and no percentage; a flag is not a regression; check a "trend" is not one
   query or one day.
4. **Blocked** → fix the blocker (usually `web-seo`: indexing, canonical, access).
   **Missed** → diagnose, then take **one** rung of the action ladder in targets.md,
   cheapest first. New content is rung four, not rung one.
5. Log it: `seo_state.py action --site … --metric … --what "…"`. The script stamps the
   date it can first be judged. Judge the actions whose date has come, in the report.
6. Read the AI tier: Search Console's generative-AI impressions and Bing's AI
   Performance (both UI-only — ask the owner for the export or the numbers), the panel's
   rates with their n, assistant referrals as a floor. Bing's *grounding queries* go
   straight into §4 as demand evidence.
7. Pages whose review date has come (briefs, `status`) → the refresh rules in
   [references/content-plan.md](references/content-plan.md) §8.
8. Report in the scorecard shape (§7).

## 4. Deciding what to make

[references/content-plan.md](references/content-plan.md) is the method. In short:

1. **First ask whether new content is the answer.** Walk the ladder; refresh before
   writing new.
2. **Read demand where it is real** — Search Console, Bing's grounding queries,
   autocomplete, the forums and trackers where the readers ask, the product's own
   reviews and support mail, the sub-questions engines research. **Never invent a search
   volume.**
3. **Score the topic** on the five lines; publish at the bar in
   [calibration.json](calibration.json). **No first-hand material, no topic** — that
   rule is what separates this from content nobody needed.
4. **Check the site's own inventory**; update or merge before adding a URL.
5. **Pick the form from the intent** — a focused answer, a reference page, a comparison,
   an article, a tool, the product page itself. For an app, the store listing's long
   description is the page AI answers quote most
   ([references/offsite.md](references/offsite.md)).
6. **Route it** by the table in content-plan.md §9. Where the named skill is not loaded,
   say which track carries it.

**What comes out is one ranked backlog** (content-plan.md §0), kept as `backlog.md` in
the state directory: fixes to existing pages, product facts, alternatives and comparison
pages, landing and concept pages, reference assets, articles, the store listing, video,
and work on other people's sites — in one order, each with its evidence, its prize, its
effort and the skill that does it. Present the next three to five entries with the
reasoning. It is not a calendar: the pace follows the evidence available.

## 4a. The competitor read

[references/competitors.md](references/competitors.md). Name eight to fifteen queries
per product; read the result page for each and record the *kinds* of page that hold it;
find the three to six domains that recur; put our page beside the ones above it with
`scripts/page_facts.py` and answer the five questions; ask the answer engines the same
queries and record who is cited. Save `competitors/<name>.md`. **Every gap becomes a
backlog entry or is written down as not worth closing** — and nothing is ever copied: a
competitor's page shows which questions the reader has, and the answers come from the
owner's own material.

## 5. The brief, and the hand-over

Fill [references/brief-template.md](references/brief-template.md) completely and save it
as `briefs/<YYYY-MM-DD>-<slug>.md` in the state directory.

- The **gates** — demand evidence, inventory check, thesis, what the piece adds, the
  evidence inventory, inbound links — are what stop a commodity page, a duplicate or an
  orphan. An empty gate ends the brief, and `Status: rejected` with the reason is a
  valid result.
- The strategist writes each section's **opening answer**. If it cannot, the answer is
  not known yet and the section is not ready to commission.
- Each language's query is **researched in that language**, never translated.
- **The owner approves the brief** before anything is written. Then: hand it to
  `article-writer`, which writes, returns its claims ledger and its TODOs, and passes
  the text through `copy-edit`. After the page is live and indexed, `announce` writes
  the posts.
- When the piece is published, set the brief's status, and log an action against the
  target it serves so its window is on record.

## 6. Keeping itself current — three loops

**Per site — data.** Readings, targets, actions and briefs in the state directory are
the site's history. An outcome about one site stays there.

**Per method — lessons.** An outcome that would change how *every* site is judged goes
in [LESSONS.md](LESSONS.md), dated, as *expected / happened*. One that changes a
threshold also changes [calibration.json](calibration.json), with the same date in
both. Change a threshold from several sites or several periods, never from one.
Three things nobody has measured are to be learned here: how the site's second language
behaves in search and in AI answers, how a small brand's numbers move, and what growth a
low-authority site really sees ([knowledge.md](references/knowledge.md) §7).

**Per fact — the refresh.** `volatile.py due` lists the facts past their interval, each
with where to check it and what it changes.

1. Read the source named in `check` — the primary page, not a summary of it.
2. **Unchanged** → stamp it (`volatile.py checked <id>`). An unstamped item is an
   unchecked one.
3. **Changed** → say what was true, what is true now, and what in the method it
   changes. Then:
   - *In a session standing in this skill's own repository*: edit
     [references/knowledge.md](references/knowledge.md) (and the file named in
     `lives_in`), add the dated line to LESSONS.md, stamp the item, and tell the owner a
     release is needed for it to reach other machines.
   - *Anywhere else* (an installed copy is a cache the next update overwrites): append
     the finding to `knowledge-updates.md` in the state directory and stamp with
     `volatile.py --stamps <state_dir>/volatile-checked.json checked <id>`; report it,
     so the skill's maintainer can fold it in.
4. A change that contradicts a rule this skill has been applying is reported **first**
   in the run's report, above the numbers.

A full re-research — new agents, new reports beside the old ones in the source
repository's research folder — is worth it once a year, or when a refresh finds the
ground has moved in several places at once. The old reports stay: they are the record
of why a rule was written.

## 7. The report

The scorecard in targets.md: one verdict line first — on track, blocked or missed, and
the single most important action — then the table (metric · now · before · target ·
band · state), movers, the AI tier with its n, what was done and whether its window has
passed, what is next with its re-check date, and the caveats.

Say what is not known. No percentage on a base under twenty. Never average a
well-indexed property together with one that has nothing indexed. Never report an
average position or a CTR for a whole site. And say what the skill did **not** do: every
export it asked the owner for, every post it drafted and did not send.

## Boundaries

- **It does not audit pages or take the reading.** `web-seo` does both; this skill reads
  the result against a target.
- **It does not write the article or the page.** `article-writer` writes from the brief;
  `page-builder` structures a page; `copy-edit` owns wording that already exists.
- **It does not set the target — it proposes one.** The owner approves it, and approves
  every brief.
- **It does not publish, post, submit, email or create accounts.** Listings, community
  posts and outreach are drafted here (or by `announce`) and done by the owner.
- **It does not invent.** No search volume without a source, no rating, review, quote or
  number that does not exist, no date changed without the content changing.
- **It does not set up measurement or hold credentials**, and it ships no API client:
  what Search Console, Bing and the analytics property say reaches it through `web-seo`'s
  reading or the owner's export.
