---
name: ia-practitioner
description: >
  Apply practitioner Information Architecture frameworks to any design project.
  Built from Spencer, Morville & Rosenfeld, Covert, Marquis, Krug, Glushko, and
  Resmini & Rosati. Use whenever working on site structure, navigation, content
  organisation, labelling, classification schemes, search systems, card sorting,
  IA testing, sitemap creation, or any UX task involving how to group, label, or
  connect content. Apply even when the question is phrased as a WordPress/Elementor
  design question — IA underpins all navigation and menu decisions.
---

# IA Practitioner — Multi-Source Framework

Built from seven practitioner texts. See reference files for depth on specific topics.

---

## Core Model: People × Content × Context
*(Morville & Rosenfeld / Spencer)*

Every IA decision lives at the intersection of three things:

| Dimension | What to understand |
|---|---|
| **People** | Tasks, mental models, terminology, knowledge level, context of use |
| **Content** | What exists, structure, format, volume, dynamism, metadata quality |
| **Context** | Business goals, constraints, tech stack, stakeholders, org culture |

Missing any one of these = guaranteed IA failure.

---

## The Three Jobs of IA

1. **Organise** content into groups that make sense to users (not to the org)
2. **Describe** those groups with labels users recognise
3. **Provide paths** for users to reach what they need

---

## IA Project Phases

```
1. Define    → Goals, constraints, stakeholders, tech, culture
2. Research  → Learn about People + Content
3. Design    → Draft IA, labels, nav
4. Test      → Validate before building
5. Build     → Implement + communicate rationale
6. Maintain  → Document decisions + guidelines
```

Research + communication take more time than design. Never skip them.

---

## Understanding People

### What to learn
- What tasks they need to do (not what they think they need)
- Their **exact terminology** for things — this is the most valuable research output
- What they already know (topic + technology)
- Where and when they use the site
- Their mental model of how things group together

### Information-seeking behaviours *(Spencer / Marquis)*

| Mode | Behaviour | IA support needed |
|---|---|---|
| **Known-item** | Knows exactly what they want, not where to find it | A-Z index, search, direct labelling |
| **Exploratory** | Browsing, learning, doesn't know exactly what's there | Clear categories, related links, serendipity |
| **Re-finding** | Looking for something previously found | Search, recent, bookmarks |
| **"Don't know what I need"** | Exploratory but no starting question | Guided paths, progressive disclosure |
| **AI-mediated** *(Svetlana)* | Asks an AI assistant about the site instead of — or before — navigating it | Explicit facts near headings, plain-language labels, terminology consistent on- and off-site |

Design for all five modes. Most IA is built only for exploratory seeking. AI-mediated
seeking doesn't replace the others — it wraps around them: an AI reads the site on
the user's behalf, so implicit, buried, or jargon-labelled information gets omitted
or misstated before the user ever arrives. → Detail in `references/user-analysis.md`.

### How users really behave *(Krug)*

**Users scan, not read.** They look for words that match their task. Design for billboards at 60 mph, not novels.

**Users satisfice.** They click the first link that looks plausible — not the best option. Every question mark on a page costs cognitive energy and erodes confidence.

**Users muddle through.** They get things done with incomplete mental models. "Getting it" is better UX than "muddling through" — it's faster, more error-free, and builds return visits.

### Research methods — when to use each

| Method | Best for |
|---|---|
| **Interview** | Rich, contextual understanding; exploring why |
| **Observation** | Seeing real behaviour (call centres, fast-paced tasks) |
| **Card sorting** | How users mentally group content; terminology |
| **Survey** | Volume; collecting common info needs in users' words |
| **Web analytics** | What's being used; entry points; popular terms |
| **Search logs** | What people call things; unmet needs |
| **Existing data** | Fast start: emails, help-desk tickets, forums |

Use at least two methods. Direct (interview/observation) reveals why. Indirect (analytics/search) reveals what.

---

## Understanding Content

### Content audit process *(Marquis)*

Distinguish: **audit** (the process) vs. **inventory** (the spreadsheet output).

Audit types that work best together:
- **Scoping audit** — high-level page count, content types, structural health, quality sample
- **Automated audit** — crawl tool output; parse for page distribution, word counts, readability trends
- **Structural audit** — walk the site as a user; track hierarchy, crosslinks, inconsistencies in a spreadsheet

**Verification rule *(Svetlana)*:** Every audit finding is one of three states — **Present / Absent / Unverified**. Never report "absent" unless absence was directly confirmed; if a pass couldn't check something (limited access, tool stripped it, JS-only rendering), record it as Unverified with the reason. A gap you didn't check for is not the same as a gap that doesn't exist. → Detail in `references/user-analysis.md`.

Before designing, answer:
1. How much content is on the site?
2. What kind of content is it?
3. How is it structured?
4. How effective is it?
5. How is it managed (and by whom)?

### Content planning — what to define per content type
- Format (article, video, tool, PDF, FAQ)
- Length range
- Target audience
- Tasks it supports
- Accuracy/update frequency
- Structured fields (if applicable)

### Structured vs unstructured
- **Structured**: all items of a type share the same fields — use for database-pattern content
- **Unstructured**: one-off pages — fine for static, low-volume content

Only structure content when you will actually use that structure.

---

## LATCH — Five Ways to Organise Anything *(Wurman via Marquis)*

| Method | Use when |
|---|---|
| **Location** | Geography is the primary user mental model; users navigate by place |
| **Alphabet** | Known-item lookup in large lists; indexes; dictionaries |
| **Time** | News, events, history, social feeds; recency adds meaning |
| **Category** | Most websites; flexible, robust, discovery-oriented |
| **Hierarchy** | Ordering by value, weight, priority, or rank |

LATCH is a starting framework, not a complete system. Category and Hierarchy overlap; ordering methods (L, A, T) differ from grouping methods (C, H). Real sites combine multiple LATCH methods.

---

## Classification Schemes

→ Full decision rules in `references/classification-schemes.md`

Quick selector:

| Scheme | Use when |
|---|---|
| **Hierarchical (subject/topic)** | General-purpose; most common |
| **Task-based** | Users have clear, frequent tasks |
| **Audience** | Clearly distinct user groups — but use as **entry points**, not primary nav |
| **Time** | News, events, history, sequential content |
| **Alphabetical** | Known-item lookup; best as secondary scheme (A-Z index) |
| **Geographical** | Location is primary attribute AND users know the geography |
| **Format** | Secondary only — users think topic first, then format |
| **Organisational** | Intranets where dept is genuinely meaningful to users (rare) |

**Critical rule:** Audience-based navigation rarely works as the sole primary scheme. Users can't reliably self-identify, content overlaps between audiences, and it creates duplication. Use audience as **focused entry points** over a subject hierarchy instead.

**Conway's Law warning *(Marquis)***: Organisations tend to build navigation that mirrors their org chart. Fight this — users don't care how internal teams are structured.

---

## Criteria Matching — How Categorisation Actually Works *(Marquis)*

Categorising content is not arbitrary grouping — it is **criteria matching**:
1. Define the criteria for the category (what belongs here and why)
2. Assess each content item against that criteria

The four factors that should shape category criteria:

| Factor | What it means |
|---|---|
| **User needs** | What are users trying to do? Focus on actions/verbs, not audience labels |
| **Business goals** | What story is the organisation trying to tell? The category structure IS part of the narrative |
| **Current state** | What's in the inventory? Use audit insights; don't ignore existing equity |
| **Future state** | What content will exist post-launch? What can the content team actually produce? |

Categories without rationale are arbitrary. Arbitrary categories cause harm.

---

## IA Patterns

→ Full pattern details in `references/ia-patterns.md`

Quick reference:

| Pattern | Suits | Key challenge |
|---|---|---|
| **Hierarchy** | Varied content, small/medium sites | Breadth vs depth balance |
| **Database** | Consistent-structure content, large sets | Don't over-collect metadata |
| **Hypertext (wiki)** | Evolving content, unknown structure upfront | Authors must link actively |
| **Linear** | Sequential instruction (use sparingly) | Frustrating unless truly sequential |
| **Hierarchy + Database** | Most real sites | Decide what to structure vs leave flat |
| **Catalogue** | E-commerce, product listings | Gallery page is the hardest-working page |
| **Hub & Spoke** | Apps with a central home base | Navigation style, not structure |
| **Subsites** | Large orgs, diverse content, multiple brands | Consistent nav/brand across subsites |
| **Focused Entry Points** | Multiple audiences, no single best path | Audience/task entry points over a main hierarchy |
| **Tagged** | Large diverse collections, user-driven discovery | Who tags, and how consistently |

Most real sites are **Hierarchy + Database**. Don't over-engineer.

---

## Labels and Language

### What makes a good label *(Spencer / Marquis / Covert)*
- Uses your users' **exact terminology** — not internal jargon, not invented terms
- Consistent throughout the site
- **Clarity** — straightforward, familiar, free of ambiguity
- **Specificity** — no catch-all "Resources" or "Information" buckets (junk drawers)
- **Inclusivity** — won't alienate users from marginalised groups; consider who is excluded
- **Consistency** — parallel structure in grouped labels (all gerunds, all nouns, etc.)

### Labelling guidelines *(Marquis)*
- Test clarity: show users top-level labels, ask what they'd expect to find inside
- Avoid first/second person possessive inconsistency ("About Us" + "My Account" = "us" vs "my")
- Beware: "Moments", "Explore", "Discover" — creative labels require marketing to explain themselves
- The clearest label is not always the most obvious first choice — push it further

### Controlled vocabulary *(Covert / Morville)*
A controlled vocabulary is an organised list of terms with canonical spellings, accepted synonyms, and defined scope.

Document:
- Terms you DO say (and their authorised variants/spellings)
- Terms you DON'T say (and why — historical baggage, internal jargon, confusion with user terms)
- Homographs — words that mean different things in different contexts
- Acronym expansions
- **On-site / off-site consistency** — the controlled vocabulary applies beyond your pages: directory listings, social profiles, and third-party mentions should use the same preferred terms. AI-mediated seekers get answers assembled from all of these; inconsistent naming across sources produces inconsistent answers about you.

→ Full vocabulary and thesaurus guidance in `references/classification-schemes.md`

### Ontology *(Covert)*
When you decide that a word holds a specific meaning in a specific context, you are practising **ontology** — declaring meaning for your domain. Do this explicitly with stakeholders and users before designing with the language. Use sticky notes: write terms, arrange by relationship, test against user language.

---

## Search Systems *(Morville & Rosenfeld)*

Search is a navigation system — not a substitute for good IA.

### Does your product need search?

Add search when:
- Content volume makes browsing impractical
- The site is fragmented (siloed content, distributed authorship)
- Content is highly dynamic and can't be manually indexed
- Users expect it (it's become a default convention)

Don't add search as a band-aid for poor navigation. Fix the navigation first.

### Search system design decisions

**What to index:**
- Search zones — subsets of content indexed separately (by topic, audience, content type, date)
- Navigation pages vs destination pages — index destination pages, exclude nav pages from results
- Content components — which fields within a document to make searchable

**Result presentation:**
- Show less for known-item searchers (just title + author)
- Show more for exploratory searchers (summary, category, key metadata)
- Always show: total results count, query restatement, ability to revise
- Relevance ranking, date sorting, and popularity ranking are three different strategies — choose based on user need

**No dead ends policy**: When search returns zero results, always offer:
- A way to revise the search
- Search tips
- A browse path (sitemap/nav)
- A human contact

**Autocomplete/autosuggest**: Surfaces controlled vocabulary terms and query patterns — dramatically improves search quality and reduces zero-result failures.

→ Full search design guidance in `references/navigation-design.md`

---

## Cross-Channel IA *(Resmini & Rosati)*

Modern information exists across multiple channels, devices, and environments simultaneously. Design principles for pervasive IA:

| Heuristic | What it means |
|---|---|
| **Place-making** | Help users know where they are across physical and digital spaces |
| **Consistency** | Semantic structures should be recognisable across channels (mobile app, website, signage) — not identical, but coherent |
| **Resilience** | The system should accommodate different information-seeking behaviours and contexts |
| **Reduction** | Reduce cognitive load; apply Hick's Law — too much choice delays decision |
| **Correlation** | Connect related content and services across channels; break down silos |

**Internal consistency**: The IA serves its own context well.
**External consistency**: The IA preserves its logic across different media and environments.

Cross-channel IA does not mean "design the same thing for every channel." It means designing **semantic structures** that can be instantiated appropriately for each channel's constraints and affordances.

---

## Organising Systems Framework *(Glushko)*

Glushko's framework provides a vocabulary for describing any organising system:

**Core concepts:**
- **Resource** — anything being organised (documents, products, people, physical objects, data)
- **Collection** — a set of resources treated as a unit
- **Organising principle** — the property or rule used to arrange resources (alphabetical, topical, by frequency of use)
- **Agent** — who or what does the organising (human cataloguer, algorithm, user tagging, automated crawler)
- **Interaction** — what users can do with the organised resources (find, browse, compare, filter, download)
- **Interaction resource** — a trace of user behaviour that can itself become data (search logs, click patterns, ratings)

**Key insight:** Physical resources can only be in one place at a time — they must choose a single organising principle. Digital resources can be organised in multiple ways simultaneously (the iTunes problem — content is freed from its container).

**Organising properties:**
- **Intrinsic** — properties inherent to the resource (title, date, format, size)
- **Extrinsic** — properties assigned through description (subject tags, categories, ratings)
- **Aboutness** — what a resource is about; requires intellectual effort to determine; the basis of subject classification

**Colocation**: Putting all resources of a type together. The simplest organising principle; often the starting point for personal systems; insufficient at scale.

---

## How to Create IA — The Design Process

1. **Review research** — people needs, content inventory, context
2. **Choose a classification scheme** — match to user mental models
3. **Choose an IA pattern** — match to content + site scale
4. **First draft** — brainstorm groups using user language (sticky notes, index cards)
5. **Gut check** — does every piece of content fit? Does anything fall in two places?
6. **Test with users** (tree test or card sort validation)
7. **Iterate** — change labels, move items, test again
8. **Document rationale** — why this structure, what you tried and rejected

Never show an IA to stakeholders without navigation and page layouts alongside it — too abstract on its own.

---

## Testing IA

### Tree testing (recommended first)
Show users the IA as a hierarchy. Give them a scenario (not using your labels). Ask where they'd look.

**Preparation:**
- Draft IA (can still be rough)
- 8–12 realistic scenarios (avoid using label words in scenario text)
- Describe the user's situation, not the object: "You've just found out you're having a baby. What are you entitled to?" — not "Find the maternity leave policy."
- Participants: 5–8 for qualitative insight; 30–50 if you will report success percentages → numbers guidance in `references/user-analysis.md`
- Scenario design check: for each scenario, ask "would this user browse for this, or ask an AI assistant?" Tasks likely to be AI-mediated still need a findable on-site home — the AI reads the same structure

**When to change the IA:**
- Consistent wrong choice → move the content there
- Inconsistent choices → the label is ambiguous, rewrite it
- Everyone goes backwards → the category above is misleading

**Tools:** Optimal Workshop Treejack, UXtweak, or paper cards

### Card sorting
**Open card sort** → users create their own groups. Use to discover mental models early. Capture the words users write on group headers — this is your label vocabulary.

**Closed card sort** → users sort into your predefined categories. Use to validate an existing IA.

### First-click testing *(Krug)*
Ask users: given this scenario, what's the first thing you'd click? Simple, fast, highly predictive — the first click strongly correlates with task success.

### Analytics signals that IA is failing
- High search use (users can't find via nav)
- High bounce rate from section landing pages
- High back-button use from deep pages
- Direct URL entry for buried content
- Users arriving to wrong sections from search

---

## Documenting IA

### Sitemap types *(Marquis)*

| Format | Best for |
|---|---|
| **Box-and-arrow diagram** | Stakeholder presentations; high-level overview; smaller sites |
| **Outline** | Completionist scenarios; every page at every level; text-heavy projects |
| **Spreadsheet** | Migration planning; template mapping; page IDs; multi-column metadata |

Distinguish: **parent-child relationships** (hierarchy levels) vs. **sibling relationships** (pages at the same level). Sitemaps capture these two; they do not capture every cross-link.

Include in sitemap documentation:
- Page IDs (numbered by hierarchy level: 1.0, 1.1, 1.2)
- Differentiate single pages from dynamic collections (e.g., "[News articles]")
- Rationale for structural decisions
- What you decided NOT to do and why

### What to document beyond the sitemap
- Why this structure, what each section contains, what was rejected and why
- Maintenance guide: rules for adding new content, what goes where
- Cross-links (track in content document, not on the sitemap)

---

## Quick Decision Checklists

### Starting an IA project
- [ ] Do I know the business goals and constraints?
- [ ] Do I understand who the users are and what they need?
- [ ] Do I have a content inventory (or at least a content list)?
- [ ] Do I know which content is structured vs unstructured?

### Choosing a classification scheme
- [ ] What mental model do users have? (Check card sort / interview data)
- [ ] Are there clearly distinct tasks? → task scheme
- [ ] Are there distinct audiences with very different needs? → audience entry points (not primary scheme)
- [ ] Is there a natural, exact scheme (time/geography)? → verify users care about it

### Before designing navigation
- [ ] Is the IA tested and stable?
- [ ] Do I have user terminology confirmed?
- [ ] Do I know the IA pattern I'm using?
- [ ] Have I identified all navigation structure types (main, secondary, utility, search, social, footer)?

### Labelling review
- [ ] Does every label use user language, not internal jargon?
- [ ] Is the labelling parallel in structure across grouped items?
- [ ] Is there a controlled vocabulary documenting authorised terms?
- [ ] Are there any junk-drawer catch-all categories?
- [ ] Have labels been tested with tree testing or first-click?

### Audit reporting
- [ ] Is every finding marked Present, Absent, or Unverified — with reasons for Unverified?
- [ ] Was anything reported "absent" without direct confirmation? (Not allowed)

---

## Reference Files

| File | When to read |
|---|---|
| `references/classification-schemes.md` | Choosing how to organise content; all 8 schemes; LATCH detail; controlled vocabulary and thesauri |
| `references/ia-patterns.md` | Choosing a structural pattern; all combined patterns with examples |
| `references/user-analysis.md` | Deep analysis methods: affinity mapping, mental models, quantitative card sort and tree test analysis, verification states, AI-mediated seeking |
| `references/navigation-design.md` | Navigation types, design principles, search systems, wayfinding, anti-patterns, healthcare IA |
| `references/audit-methodology.md` | Running a full IA audit: framing, evaluation lenses, issue cards, severity, before/after restructure, client report |
