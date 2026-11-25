---
name: canon-content-strategy
description: Use when planning content hierarchy, information density, content-first design, microcopy systems, or editorial patterns. Covers the content-before-design principle, content inventory, progressive disclosure, scannability, and content governance. Trigger when the user mentions content strategy, content hierarchy, information architecture, microcopy, or editorial design.
---

# CANON · Content Strategy

Design follows content. Not the other way around. Wireframing with "Lorem ipsum" produces layouts that break when real words arrive.

## Content-first design

1. Write the real content before the layout.
2. Identify the hierarchy: what's the single most important thing on this page?
3. Design the container around the content, not the content around the container.
4. Test with the longest plausible string, not the shortest.

## Content hierarchy per page

Every page answers one question. The hierarchy makes that question and its answer scannable.

```
Page title          ← what is this page
Primary content     ← the answer to why the user is here
Supporting content  ← context that helps the primary
Actions             ← what to do next
Metadata            ← secondary info (dates, authors, tags)
```

## Progressive disclosure

Don't show everything at once. Layer information by relevance:

| Layer | Show | How |
|---|---|---|
| Essential | Always | Visible on load |
| Supplementary | On demand | Expandable sections, tooltips, "Learn more" |
| Reference | On search | Help docs, FAQs, knowledge base |

Each layer deeper should serve fewer users but serve them well.

## Scannability rules

- Front-load key information in every sentence, heading, and label.
- Use headings as statements, not categories. "Your bill is overdue" not "Billing".
- Break text at 2–3 sentence paragraphs for UI context.
- Lists for 3+ parallel items (but follow `canon-ux-writing` for when lists earn their place).
- Bold the one phrase per paragraph that carries the meaning if a user reads nothing else.

## Content inventory

Before redesigning, audit what exists:

| For each content piece | Record |
|---|---|
| What is it? | Page, modal, toast, email, error |
| Who owns it? | Product, marketing, engineering, legal |
| When was it last updated? | Date |
| Is it still accurate? | Yes / No / Partially |
| Does it serve the user's task? | Yes / No |

Delete what fails the last two questions.

## Anti-patterns

| Anti-pattern | Why it fails |
|---|---|
| Lorem ipsum in production-ready mockups | Layout breaks with real content |
| Designing the card, then filling in copy | Content overflows or under-fills |
| No content owner | Copy drifts, goes stale |
| Every section equally weighted | No hierarchy, nothing stands out |
| "Learn more" as the link text | Inaccessible + vague |

## Audit checklist

- [ ] Real content written before layout finalized
- [ ] Page has one clear primary purpose
- [ ] Headings are statements, not categories
- [ ] Progressive disclosure layered by user need
- [ ] Content tested at longest plausible string length
- [ ] Content owners assigned
- [ ] Stale content audited and removed or updated

## Sources

- Sarah Richards · Content Design (book)
- Nielsen Norman · "How Users Read on the Web"
- GDS (UK Government Digital Service) · Content design principles
- `canon-ux-writing` for string-level execution
