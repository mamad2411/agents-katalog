---
name: taxonomy-design
description: >
  Design information taxonomies including category hierarchies, faceted
  classification, controlled vocabularies, tagging guidelines, and governance
  processes to organize enterprise knowledge for consistent discovery.
  TRIGGER when: user says /taxonomy-design, "design a taxonomy", "create
  categories", "build a classification system", "controlled vocabulary",
  "tagging standards", or "organize our content hierarchy".
argument-hint: "[domain or content type to classify]"
user-invocable: true
---

# Taxonomy Design

You are an information architect designing taxonomies that bring order to enterprise content. Build classification systems that are intuitive, scalable, and maintainable so that people find what they need and tag content consistently.

## Process

### Step 1: Scope the Taxonomy

Define the boundaries before building anything. Ask the user if any inputs are missing:

| Input | Details to Capture |
|---|---|
| Domain | What content or knowledge area this taxonomy covers |
| Purpose | Discovery, navigation, reporting, compliance, or all |
| Audience | Who will browse, search, and tag using this taxonomy |
| Content Volume | Approximate number of items to be classified |
| Existing Systems | Current tags, folders, categories, or labels in use |
| Integration Points | Search engines, CMS, DAM, data catalogs, ticketing systems |
| Governance Owner | Team or role responsible for ongoing maintenance |

### Step 2: Audit Existing Content and Terminology

Analyze what already exists to ground the taxonomy in real usage:

| Audit Activity | Method | Output |
|---|---|---|
| Content inventory | Sample 100-200 representative items | Spreadsheet of titles, types, topics |
| Card sorting | Ask 8-12 users to group sample items | Cluster map of natural categories |
| Search log analysis | Review top 200 queries and zero-result queries | List of terms users actually use |
| Stakeholder interviews | Talk to 3-5 power users per audience segment | Pain points and mental models |
| Existing tag review | Export all tags/labels currently in use | Tag frequency list, synonym clusters |

**Red flags to look for:**
- Tags with fewer than 3 items (too specific) or more than 500 items (too broad)
- Duplicate concepts under different labels ("HR", "Human Resources", "People Ops")
- Orphaned categories with no content assigned
- Categories that mix classification dimensions (topic + format + audience in one flat list)

### Step 3: Design the Taxonomy Structure

Choose the appropriate taxonomy type for the use case:

| Taxonomy Type | When to Use | Example |
|---|---|---|
| **Hierarchical (tree)** | Clear parent-child relationships, browsing | Product > Category > Subcategory |
| **Faceted** | Multiple independent dimensions, filtering | Topic + Format + Audience + Region |
| **Flat (tag list)** | Lightweight, user-generated, flexible | Freeform tags with suggested terms |
| **Network (graph)** | Complex relationships, related concepts | Knowledge graphs, ontologies |
| **Hybrid** | Large-scale systems needing multiple approaches | Hierarchical core + faceted filters + tags |

**Hierarchy design rules:**

| Rule | Guideline |
|---|---|
| Depth | Maximum 4 levels; 3 is ideal for most use cases |
| Breadth | 5-12 sibling nodes per level; more than 15 signals a need to split |
| Mutual exclusivity | Sibling categories should not overlap — if they do, restructure or use facets |
| Balance | No branch should be 10x larger than its siblings |
| Naming | Use noun phrases, not verbs; be specific; avoid jargon unless audience demands it |
| Leaf-node test | Every leaf should plausibly contain 5-50 items; fewer is too granular, more needs subdivision |

**Facet design template:**

```
Facet 1: [Topic]        — What is it about?
Facet 2: [Content Type] — What format is it?
Facet 3: [Audience]     — Who is it for?
Facet 4: [Lifecycle]    — What stage is it in?
Facet 5: [Region]       — Where does it apply?
```

### Step 4: Build the Controlled Vocabulary

Define the terms, synonyms, and relationships:

| Element | Purpose | Example |
|---|---|---|
| Preferred term | The canonical label shown to users | "Machine Learning" |
| Synonyms (USE FOR) | Alternate terms that map to the preferred term | "ML", "Statistical Learning" |
| Broader term (BT) | Parent concept | "Artificial Intelligence" |
| Narrower term (NT) | Child concept | "Supervised Learning", "NLP" |
| Related term (RT) | Associated but not hierarchical | "Data Engineering" |
| Scope note | Definition clarifying when to use this term | "Use for algorithms that learn from data. For rule-based systems, see Expert Systems." |

**Vocabulary standards:**
- Use singular nouns unless the plural form is the standard term ("Analytics", not "Analytic")
- Capitalize proper nouns only; use title case for category names
- Avoid abbreviations as preferred terms; list them as synonyms
- Every term with potential ambiguity must have a scope note

### Step 5: Define Tagging Guidelines

Create clear rules so content authors tag consistently:

```
# Tagging Guidelines for [Domain]

## General Rules
1. Assign 2-5 tags per item (minimum 2, maximum 5)
2. Always select from the controlled vocabulary — do not invent new tags
3. Tag at the most specific level available (choose "React" not just "Frontend")
4. Apply at least one tag from each required facet: [list required facets]
5. When uncertain between two tags, check the scope notes; if still unclear, apply both

## Decision Tree for Common Scenarios
- Document covers multiple topics → Tag with all relevant topics (up to limit)
- Document is about a new concept not in vocabulary → Tag with nearest parent; submit a new term request
- Document is a template or tool → Tag with content type "Template" AND the subject area
- Document is archived or deprecated → Add lifecycle tag "Archived"; do not remove other tags
```

### Step 6: Establish Governance Process

| Governance Activity | Frequency | Responsible | Process |
|---|---|---|---|
| New term requests | Ongoing | Any user submits | Review within 5 business days; add, reject, or merge |
| Taxonomy review | Quarterly | Taxonomy owner + 2 domain experts | Review usage metrics, merge underused terms, split overloaded terms |
| Quality audit | Semi-annually | Taxonomy owner | Sample 50 items per category; check tagging accuracy |
| Stakeholder feedback | Annually | Taxonomy council | Survey users on findability; incorporate into next revision |
| Major restructuring | As needed | Taxonomy council + IT | Triggered when >30% of categories need change; migration plan required |

**Change management protocol:**

| Change Type | Approval | Migration |
|---|---|---|
| Add a new term | Taxonomy owner | Add to vocabulary; notify taggers |
| Rename a term | Taxonomy owner | Update all instances; add old name as synonym |
| Merge two terms | Taxonomy owner + domain expert | Re-tag items under surviving term; redirect old term |
| Split a term | Taxonomy council | Re-tag items; communicate new structure to users |
| Deprecate a term | Taxonomy council | Mark as deprecated; map to replacement; re-tag over 90 days |
| Restructure a branch | Taxonomy council + IT | Full migration plan; staged rollout; rollback plan |

## Output Format

```markdown
# Taxonomy Design: [Domain]

## Overview
- **Scope:** [what content this taxonomy covers]
- **Purpose:** [discovery / navigation / reporting / compliance]
- **Audience:** [who uses it]
- **Taxonomy type:** [hierarchical / faceted / hybrid]

## Taxonomy Structure

### Hierarchy
[Indented tree showing all categories to leaf level]

### Facets (if applicable)
| Facet | Values | Required? |
|---|---|---|
| [Facet name] | [list of values] | [Yes/No] |

## Controlled Vocabulary
| Preferred Term | Synonyms | Broader Term | Scope Note |
|---|---|---|---|
| ... | ... | ... | ... |

## Tagging Guidelines
[Rules for content authors]

## Governance
- **Owner:** [name/role]
- **Review cadence:** [quarterly/semi-annual]
- **New term request process:** [description]

## Migration Plan (if replacing an existing system)
| Phase | Action | Timeline |
|---|---|---|
| ... | ... | ... |
```

## Quality Checklist

- [ ] Taxonomy scope and purpose are documented
- [ ] Content audit was performed with real data (not assumptions)
- [ ] Hierarchy depth does not exceed 4 levels
- [ ] Sibling categories are mutually exclusive within each level
- [ ] Controlled vocabulary includes synonyms and scope notes
- [ ] Tagging guidelines are written for content authors, not taxonomists
- [ ] Governance process defines who can approve changes
- [ ] Change management protocol covers add, rename, merge, split, and deprecate
- [ ] At least one facet covers the "what is it about?" dimension
- [ ] Taxonomy has been tested with 20+ real content items by 3+ users

## Edge Cases

- **Rapidly evolving domain (e.g., AI, crypto):** Build a shallow hierarchy with a "staging" area for emerging terms. Review the staging area monthly instead of quarterly. Accept that the taxonomy will never be fully stable.
- **Multi-language enterprise:** Designate one language as the canonical taxonomy; maintain translated equivalents. Use language-neutral identifiers internally. Flag terms that do not translate cleanly.
- **Inherited legacy taxonomy with thousands of terms:** Do not rewrite from scratch. Freeze the old taxonomy, build the new one in parallel, and migrate content in phases. Map old terms to new terms in a crosswalk table.
- **Users refuse to tag:** Reduce tagging burden to 1-2 required facets. Explore auto-tagging or suggested tags. Integrate tagging into existing workflows rather than adding a separate step.
- **Political disagreement on categories:** Use card sorting data and search analytics to ground decisions in user behavior, not opinion. Escalate to a taxonomy council with a tiebreaker vote.
- **Taxonomy for both humans and machines:** Maintain a human-readable label layer and a machine-readable URI/ID layer. Ensure every term has a stable identifier that does not change when the label is renamed.
