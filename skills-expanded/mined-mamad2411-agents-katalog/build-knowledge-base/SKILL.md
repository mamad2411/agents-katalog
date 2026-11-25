---
name: build-knowledge-base
description: Use when a Boom customer needs to prepare the context for their AI agent: the durable brand identity (brand, voice, glossary, product, customers, guardrails) plus a brief per job (win-back, support, research, onboarding, lead qualification, data collection). Runs a guided interview, researches the company's own website when given a URL, and outputs a structured markdown bundle to hand to Boom. Triggers on "build our knowledge base", "prepare our context for Boom", "onboard our agent".
---

# Build your knowledge base

Help a Boom customer turn what's in their heads into a **rich, structured knowledge
base** their AI agent can use. The output is a folder of markdown files they send to
Boom, which Boom turns into the agent's context.

This is a guided interview, not a form. You ask questions one at a time, research the
company's own website when given a URL, and write the files for them.

**A company is one agent identity + one or more use cases.** The same agent can run
several jobs — research, then churn recovery, then lead qualification — added over
time. So the bundle has two layers: the **durable identity** (gathered once, shared by
every use case) and a **brief per use case** (the goal, audience, and rules for that
specific job). You capture the identity first, then a brief for each use case they want
now — and they can come back for more later.

## Tools used

This skill needs no Boom MCP tools — it produces files to hand to Boom, it doesn't call
the platform. It uses only general agent tools, and degrades gracefully when they're
absent:

| Tool | Purpose | Scope |
|---|---|---|
| Web fetch / web search | Read the customer's **own** public pages to pre-fill answers | read-only |
| File write | Save the `knowledge-base/` bundle | local |

If no web tool is available, skip research and rely entirely on the interview.

## The one thing to get right

**Customers send strategy; agents need durable fact.** When people are asked for a
"knowledge base," they hand over campaign goals, growth tactics, and quarterly OKRs.
None of that helps the agent. What makes an agent good is the boring, stable stuff a
new employee would need on day one:

- **who the brand is** and how it talks,
- **what its words mean** (glossary),
- **what it sells** and how the product/service actually works,
- **who its customers are** (ICP + personas),
- **what the agent must never do** and when to hand off to a human.

Your job is to *pull that out of them*, and to gently redirect when they give you
strategy instead of fact.

**Litmus test for anything they offer:** *"Would a new hire need to know this on day
one, is it true today, and is it published or brand-confirmed?"* If yes → it's
knowledge, keep it. If it's about what they *want to achieve* → that's a plan for
Boom's team, not agent context; set it aside.

<HARD-GATE>
Do NOT write the final bundle until you have (a) gathered sources / done available web
research, (b) identified the use case(s), (c) interviewed the user through the durable
identity sections AND each use-case brief, and (d) shown them drafts and gotten
confirmation. Never invent facts. If something is unknown, mark it as a gap for a human
to fill — do not guess. **Capture a use-case BRIEF, never a step-by-step playbook** —
Boom writes the playbook from your brief (see "Use cases" below).
</HARD-GATE>

## Checklist

Create a task for each and complete in order:

1. **Frame it & gather sources** — explain what you're building (one short paragraph), then ask for their website URL and any existing material (brand guide, product one-pager, FAQ, help center). One ask.
2. **Identify the use case(s)** — ask what they want the agent to *do*, and map it to Boom's use cases (research, churn recovery, data collection/conversion — see "Use cases" below). Multiple are fine; ask which is first. Tell them they can add more later. Each selected use case becomes one brief.
3. **Research their own sources** — if a URL was given and web tools are available, read their public pages (home, product, about, pricing, FAQ/help, contact). Summarize what you learned and ask them to confirm/correct. **Own sources only** — their site and material they give you; never pull in press, competitors, or third-party claims.
4. **Interview the durable identity, section by section** — walk the seven identity sections below, **one question at a time**, pre-filling from research so you ask sharper questions ("Your site says X — is that how you'd want the agent to say it?"). Prefer multiple-choice when you can.
5. **Interview each use-case brief** — for every use case picked in step 2, ask that use case's brief questions (`references/use-case-briefs.md`). Capture goal, audience, what's on the table, rules, escalation, and never-say. A **brief, not a playbook**.
6. **Draft each file and confirm** — as a section or brief firms up, draft that file and show it. Adjust from their reaction. Keep language plain — no jargon.
7. **Write the bundle** — save the durable identity to `knowledge-base/`, one brief per use case to `knowledge-base/use-cases/`, plus a `README.md` index.
8. **Self-review** — scan for placeholders, strategy-masquerading-as-fact, unverified claims, and any playbook/internal leakage in the briefs. Fix or flag as gaps.
9. **Hand-off** — tell them how to send the folder to Boom.

## The durable identity — seven sections → `knowledge-base/`

This is the agent's identity, gathered **once** and shared by every use case. Interview
around these seven buckets; each becomes one file. Full question prompts are in
`references/question-bank.md`; file shapes and examples are in
`references/file-templates.md`.

| # | File | What you're eliciting |
|---|---|---|
| 1 | `01-brand-and-identity.md` | Who the brand is: name, one-line description, mission, what makes it different, and how the agent should present itself. |
| 2 | `02-voice-and-tone.md` | How the brand talks: concrete *do-say / don't-say* examples, formality, language/dialect, emoji, and tone for common situations (happy, frustrated, confused). |
| 3 | `03-glossary.md` | The brand's own words and product terms — plus words to avoid. |
| 4 | `04-product-and-company.md` | What they sell and how it works: products/plans, the buying/using flow, operations the customer touches (payments, billing, delivery, support), and company facts. |
| 5 | `05-customers-icp-personas.md` | Who the customers are: ideal customer profile, the main personas/segments, and the language *those* customers use. |
| 6 | `06-policies-and-guardrails.md` | What the agent must and must not do or say: hard rules, sensitive topics, claims it can't make, and things that have gone wrong before. |
| 7 | `07-scope-and-escalation.md` | The agent's job boundary: what it handles, what it must NOT try to handle, and exactly when to hand off to a human. Also flags whether the agent will share back a customer's own records/account data. |

## Use cases → one brief each in `knowledge-base/use-cases/`

On top of the shared identity, each thing the agent *does* is a **use case**, and each
gets its own **brief**. Boom's use cases (name them in plain language):

| Use case | It means | The brief captures |
|---|---|---|
| **Research / discovery** | Interviews, NPS, understanding churn reasons | Objective, the questions to explore, audience/cohort, how deep to probe, how to frame identity |
| **Churn recovery / win-back** | Reactivate customers who left | Who to win back, **what's on the table** (e.g. "a discount up to X — *you* own the exact limits"), when to escalate, what to never say (internal codes, coupons) |
| **Data collection / conversion** | Qualify leads, book, onboard, collect info | What to collect/qualify, what counts as success (a booking, a hand-off), disqualification, escalation |

Per-use-case questions and the brief file templates are in
`references/use-case-briefs.md`.

**Capture a brief, not a playbook.** Get the *goal and the rules*, not a step-by-step
script — Boom writes the playbook from your brief. This is deliberate: a hand-written
playbook tends to leak internal mechanics (tier codes, coupon codes, internal system
names) and bake in assumptions that don't fit the runtime. So for "what's on the
table," capture the **envelope** ("up to X% off, you decide the exact amount per
customer") — never internal codes, exact matrices, or coupon strings.

## How to run the interview

- **One question per message.** If a topic needs depth, break it into several turns.
- **Lead with what you found.** After research, anchor questions in their own site:
  "Your About page says you were founded in 2019 to help X — should the agent lean on
  that story?" This is faster and higher-quality than blank-page questions.
- **Prefer examples over adjectives.** For voice, don't accept "friendly and
  professional" — get *actual sentences* they'd say and wouldn't say. Ask them to
  paste a real reply they loved and one they'd reject.
- **Redirect strategy to fact.** If they start describing a campaign or a growth goal:
  "That's really useful for the Boom team to know — I'll note it separately. For the
  agent's knowledge base, what I need is [the underlying fact]." Keep strategy out of
  the files.
- **Name the gaps.** If they don't know something (e.g. no glossary yet), don't invent
  it. Write `> ⚠️ Gap: <what's missing>` in the file so a human can fill it. A visible
  gap is better than a confident fabrication.
- **Scale to the business.** A solo founder's bundle can be short; an enterprise's will
  be rich. Don't pad. Cover every section, but let each be as long as it needs to be.

## Web research rules

- Only when a URL/source is provided **and** web tools (web fetch/search) are available.
  If not, skip gracefully and rely on the interview.
- **Own sources only:** the customer's website and material they hand you. Do NOT
  incorporate press coverage, review sites, competitor pages, or social media unless the
  customer explicitly provides and vouches for them.
- Read the high-value pages: home, product/features, about, pricing/plans, FAQ/help
  center, contact/support.
- **Cite and date** what you pull: each fact in the files should be traceable to "their
  site (<date>)" or "provided by <name>". Add a source line at the top of files built
  from research.
- **Never elaborate beyond the source.** If the site doesn't say it, it isn't a fact.

## Self-review before hand-off

Look at the bundle with fresh eyes and fix inline:

1. **Placeholder scan** — any `TODO`, `TBD`, empty section? Resolve or convert to a
   clearly-marked `⚠️ Gap`.
2. **Strategy leak** — did any campaign goal / OKR / sales tactic sneak into a knowledge
   file? Move it out.
3. **Unverified claims** — any fact not from the customer's own site or their own mouth?
   Cut it or flag it.
4. **Voice check** — are do/don't examples real utterances, not adjectives?
5. **Consistency** — does the brand name, tone, and terminology match across all files?

## Hand-off

Close by telling the user:

> Your knowledge base is in the `knowledge-base/` folder — the durable identity plus a
> brief for each use case under `use-cases/`. Zip it (or share the folder) and send it
> to your Boom contact; they'll use it to build your agent's context. The `README.md`
> inside lists what's included, which use cases are covered, and anything still missing.

Then list any `⚠️ Gap` items you left, and remind them they can add more use cases
later without redoing the identity.

## What NOT to do

- Don't accept strategy, tactics, or goals as agent knowledge.
- Don't invent facts, terms, personas, or policies to fill a section — flag gaps instead.
- Don't pull in third-party or competitor content; own sources only.
- Don't use Boom's internal jargon in the files ("runtime", "microVM", "snapshot",
  "runtime contract"). Write in the customer's own plain language.
- Don't dump the whole interview into one file — produce the seven identity files plus
  one brief per use case under `use-cases/`.
- Don't let a use case turn into a hand-written playbook — capture the goal, the
  envelope, and the rules; Boom writes the steps. Never record internal codes, discount
  matrices, or coupon strings.
- Don't re-gather the identity for each use case — it's shared; gather it once.
