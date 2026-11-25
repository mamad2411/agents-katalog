---
name: gbrain-ingest
description: Ingest meetings, articles, docs, and conversations into the brain. Updates existing pages with new info, creates pages for new entities, maintains cross-references.
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: [gbrain]
---

# Ingest Skill

## Workflow

1. **Read the source.** Meeting transcript, article, document, conversation log.
   Identify: participants, companies, topics, decisions, action items.

2. **For each entity mentioned:**
   - `gbrain search "<name>"` — does a page exist?
   - **If yes:** `gbrain get <slug>` to read current compiled_truth. Rewrite State section with new info.
     Append to timeline. `cat updated.md | gbrain put <slug>` with updated content.
   - **If no:** Create page using the appropriate template (see Page Templates below).
     `cat new.md | gbrain put <slug>` with new content.

3. **Extract and create links.**
   - For every entity-to-entity reference in the source:
     `gbrain link <from> <to> --context "the sentence containing the reference"`
   - Links are stored directionally. Create both directions if both pages exist and the relationship is mutual.

4. **Parse timeline entries.**
   - For each datable event:
     `gbrain timeline-add <slug> --date YYYY-MM-DD --summary "one line" --source "meeting/doc-ref"`

5. **Tag appropriately.**
   - `gbrain tag <slug> <tag>` — use lowercase, hyphenated tags (e.g. yc-alum, investor, active-deal)

6. **Verify.**
   - `gbrain stats` — confirm page counts look right.
   - `gbrain get <slug>` — spot-check a few pages.

## Entry criteria

Not everything gets a page. The bar:
- Anyone you met 1:1 or in a small group: YES
- People discussed in substantive context: YES
- Companies in deal or investment context: YES
- Concepts worth tracking: YES
- Casual passing mentions with no substance: NO

## Page templates

### Person
```markdown
---
title: Full Name
type: person
tags: []
linkedin: ""
twitter: ""
---
# Full Name
> One-sentence summary of who this person is and why they matter.

## State
Current role, company, location. What's relevant right now.

## Background
Education, career arc (condensed).

## Open Threads
- [ ] Action items or follow-ups

---

## Timeline
- **YYYY-MM-DD** | source — What happened.
```

### Company
```markdown
---
title: Company Name
type: company
tags: []
website: ""
---
# Company Name
> One-sentence summary.

## State
What the company does, stage, key people, current status.

## Assessment
Thesis, risks, opportunities.

## Open Threads
- [ ] Action items

---

## Timeline
- **YYYY-MM-DD** | source — What happened.
```

## Quality rules

- Executive summary (blockquote at top) must reflect latest state
- State section gets REWRITTEN, not appended to — it's the compiled truth
- Timeline is append-only, reverse-chronological (newest first)
- Open Threads: add new items, remove resolved ones (move to timeline)
- Every wiki link: `[Name](../people/name.md)` relative path format
- Slugs: lowercase, hyphens only, with type prefix: `people/jane-doe`, `companies/acme-corp`
