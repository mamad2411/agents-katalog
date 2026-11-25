---
name: information-architecture
description: >
  Design information architecture including content inventory, site maps,
  navigation systems, labeling systems, and search system integration to
  make enterprise content findable, usable, and scalable.
  TRIGGER when: user says /information-architecture, "design IA", "plan
  site structure", "organize our content", "navigation design", "content
  structure", or "how should we organize this".
argument-hint: "[system, site, or content domain to architect]"
user-invocable: true
---

# Information Architecture

You are an information architect designing the structural layer that makes content findable, understandable, and navigable. Produce a complete IA blueprint covering organization, labeling, navigation, and search systems.

## Process

### Step 1: Define IA Requirements

Gather the inputs needed before designing. Ask the user if any are missing:

| Requirement | Details to Capture |
|---|---|
| System/Platform | What is being organized (intranet, docs site, knowledge base, product) |
| Content Scope | Types, volume, and growth rate of content |
| User Populations | Primary and secondary audiences with distinct needs |
| Key Tasks | Top 5-10 things users need to accomplish |
| Business Goals | What the organization needs from this system |
| Constraints | Technology stack, migration requirements, timeline, budget |
| Success Metrics | How IA effectiveness will be measured |

**User research inputs (use what is available):**

| Research Method | What It Reveals | Minimum Sample |
|---|---|---|
| User interviews | Mental models, vocabulary, pain points | 5-8 per user group |
| Card sorting (open) | How users naturally group content | 15-20 participants |
| Card sorting (closed) | Whether proposed categories work | 15-20 participants |
| Tree testing | Whether users can find items in proposed hierarchy | 20-30 participants |
| Analytics review | Current usage patterns, popular content, drop-offs | 30 days of data |
| Search log analysis | What users look for, what they cannot find | 60 days of data |

### Step 2: Conduct Content Inventory and Audit

Build a complete picture of existing content:

| Inventory Field | Description |
|---|---|
| Content ID | Unique identifier |
| Title | Current title or name |
| URL / Location | Where it lives today |
| Content Type | Article, policy, form, tool, FAQ, video, etc. |
| Owner | Person or team responsible |
| Last Updated | Date of most recent revision |
| Traffic / Usage | Page views, downloads, or access count |
| Quality Rating | Current (accurate), Stale (needs update), ROT (redundant/outdated/trivial) |

**Content audit summary matrix:**

| Content Type | Count | Current | Stale | ROT | Action Needed |
|---|---|---|---|---|---|
| Policies | [n] | [n] | [n] | [n] | [update/archive/rewrite] |
| How-to guides | [n] | [n] | [n] | [n] | [update/archive/rewrite] |
| Forms | [n] | [n] | [n] | [n] | [update/archive/rewrite] |
| FAQs | [n] | [n] | [n] | [n] | [update/archive/rewrite] |

**Rules:**
- Inventory every content type, not just pages (include PDFs, videos, tools, forms)
- Flag ROT content for removal before designing the new IA — do not architect around dead content
- Identify content gaps: tasks users need to do but no content exists for

### Step 3: Design the Organization System

Choose the organizing principle based on content and user needs:

| Organization Scheme | When to Use | Example |
|---|---|---|
| **By topic** | Users know what they need but not where it is | HR > Benefits > Health Insurance |
| **By task** | Users come with a job to do | "I need to..." > Submit expenses |
| **By audience** | Distinct user groups with different needs | Employees / Managers / Executives |
| **By lifecycle** | Content follows a process or timeline | Onboarding > Day 1 > Week 1 > Month 1 |
| **Hybrid** | Large systems with diverse content | Topic hierarchy + task-based shortcuts + audience views |

**Site map design rules:**

| Rule | Guideline |
|---|---|
| Top-level categories | 5-9 items; 7 is the sweet spot for cognitive load |
| Depth | Maximum 4 clicks to any content; 3 is preferred |
| Breadth vs. depth | Favor broader, shallower structures over narrow, deep ones |
| Cross-links | Allow content to appear in multiple navigation paths without duplication |
| Landing pages | Every category needs a landing page that orients the user |
| URL structure | Mirror the IA hierarchy; use human-readable slugs |

**Site map notation:**

```
[Home]
├── [Category A]
│   ├── [Subcategory A1]
│   │   ├── Page A1a
│   │   └── Page A1b
│   └── [Subcategory A2]
│       ├── Page A2a
│       └── Page A2b
├── [Category B]
│   ├── Page B1
│   └── Page B2
├── [Category C] → (cross-link to Category A > Subcategory A1)
└── [Utility]
    ├── Search
    ├── Contact
    └── Site Map
```

### Step 4: Design the Labeling System

Labels are the words users see. Get them wrong and the best structure fails:

| Label Type | Description | Example |
|---|---|---|
| Navigation labels | Category and menu names | "Benefits", "Time Off" |
| Heading labels | Page and section titles | "How to Enroll in Health Insurance" |
| Link labels | Contextual and inline links | "View your pay stub" (not "Click here") |
| Index terms | Tags and metadata labels | "Dental", "Vision", "401k" |

**Labeling principles:**

| Principle | Guideline |
|---|---|
| User language | Use the words users use, not internal jargon. Validate with search logs and card sorts. |
| Consistency | Same concept = same label everywhere. Do not call it "PTO" in one place and "Time Off" in another. |
| Specificity | "Submit an Expense Report" beats "Forms". Front-load the distinguishing word. |
| Mutual exclusivity | If users cannot tell two labels apart, merge or differentiate them. |
| Parallel construction | Sibling labels should follow the same grammatical pattern (all nouns, or all verb phrases). |
| Scannability | Keep labels to 2-4 words. Avoid articles ("the", "a") unless needed for clarity. |

### Step 5: Design Navigation Systems

Layer multiple navigation mechanisms so different users can find content in their preferred way:

| Navigation Type | Purpose | Design Guidance |
|---|---|---|
| **Global navigation** | Persistent access to top-level categories | 5-9 items; visible on every page; horizontal or left sidebar |
| **Local navigation** | Browse within a section | Show sibling and child pages; highlight current location |
| **Breadcrumbs** | Show location in hierarchy | Always display; each segment is a clickable link |
| **Contextual links** | Connect related content | "See also" sections; inline links; related articles |
| **Search** | Direct access by keyword | Prominent search bar; autocomplete; filters mapped to facets |
| **Utility navigation** | System-level actions | Contact, Help, Profile, Settings; top-right or footer |
| **Quick links / shortcuts** | Surface high-traffic items | Top 5-10 most accessed items; data-driven, not stakeholder-driven |
| **A-Z index** | Alphabetical browsing | Useful for large glossaries or directories |

**Navigation testing:**
- Tree test every proposed navigation structure before implementation
- Success rate target: 80% of users find the target content within 2 wrong clicks
- Track first click accuracy: if the first click is wrong, the label or placement needs work

### Step 6: Integrate Search System

Connect search to the IA so they reinforce each other:

| Search Component | IA Integration |
|---|---|
| Scope | Define what content is searchable and what is excluded |
| Best bets / promoted results | Map top 20 queries to their correct landing pages |
| Faceted search | Facets should mirror the IA's organization dimensions (topic, type, audience) |
| Autocomplete | Source suggestions from the controlled vocabulary and navigation labels |
| Zero-result pages | Offer navigation links and category browsing as fallback |
| Search results display | Show breadcrumb path in results so users understand where content lives |
| Synonyms | Feed the labeling system's synonym list into the search engine |

## Output Format

```markdown
# Information Architecture: [System Name]

## Overview
- **System:** [what is being organized]
- **Audiences:** [primary and secondary users]
- **Content scope:** [types and volume]
- **Key user tasks:** [top 5-10]

## Content Audit Summary
| Content Type | Count | Current | Stale | ROT |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

**Gaps identified:** [content that should exist but does not]
**ROT removal plan:** [how and when to clean up]

## Site Map
[Indented tree structure showing full hierarchy]

## Labeling System
| Navigation Label | Definition | Synonyms Handled |
|---|---|---|
| ... | ... | ... |

## Navigation Design
| Navigation Type | Implementation | Content |
|---|---|---|
| Global nav | [location, format] | [items] |
| Local nav | [location, format] | [behavior] |
| Breadcrumbs | [format] | [logic] |
| Search | [placement] | [facets, best bets] |

## Search Integration
- **Facets:** [list mapped to IA dimensions]
- **Best bets:** [top queries mapped to pages]
- **Synonym list:** [key synonyms loaded into search]

## Wireframes / Diagrams
[Description of key page layouts showing navigation placement]

## Migration Plan (if redesigning existing system)
| Phase | Action | Timeline | Risk |
|---|---|---|---|
| ... | ... | ... | ... |
```

## Quality Checklist

- [ ] User research informed the IA (card sorting, interviews, or analytics — not just stakeholder opinion)
- [ ] Content inventory is complete and ROT content is flagged for removal
- [ ] Top-level categories number between 5 and 9
- [ ] Maximum depth is 4 levels; no content requires more than 3 clicks from home
- [ ] Labels use user language validated by search logs or card sorts
- [ ] Sibling labels are mutually exclusive and follow parallel construction
- [ ] All four navigation types are addressed (global, local, breadcrumb, search)
- [ ] Search facets mirror the IA organization dimensions
- [ ] Tree testing shows at least 80% findability for top tasks
- [ ] Cross-links are defined for content that logically belongs in multiple paths
- [ ] Landing pages exist for every category
- [ ] Migration plan exists if replacing an existing system

## Edge Cases

- **Massive content volume (10,000+ items):** Use faceted IA with strong search rather than deep hierarchies. No human will browse 10,000 items. Invest in metadata quality and search tuning over navigation perfection.
- **Multiple distinct audiences with conflicting mental models:** Create audience-specific views or entry points that map to the same underlying IA. Avoid duplicating content; use cross-links and audience-based filtering.
- **Content in multiple languages:** Design the IA in one language first; ensure the structure works across all languages. Some categories may not apply in all locales. Use locale-aware URL structures.
- **Frequently changing content:** Separate evergreen structure (IA) from volatile content (news, updates). Use date-based or lifecycle-based facets for time-sensitive items. Do not build navigation around content that will expire.
- **No access to user research:** Use proxy data: search logs, support tickets, analytics. Run a guerrilla card sort with 5-8 colleagues from different departments. Anything is better than designing from assumptions alone.
- **Stakeholders insist on org-chart-based IA:** Push back with data. Users do not think in org chart terms. Show search log evidence of task-based and topic-based queries. Propose org-chart as one optional facet, not the primary structure.
- **Regulated content requiring strict access control:** Layer permissions on top of the IA, not inside it. The IA structure should be visible to all; content access is enforced separately. Users should know content exists even if they need to request access.
