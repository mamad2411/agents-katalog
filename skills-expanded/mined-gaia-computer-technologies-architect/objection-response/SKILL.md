---
name: objection-response
description: Group planning objections, neighbour representations and consultee comments by theme, then draft measured responses tied to planning policy, the submitted drawings and evidence, plus proposed amendments where a point is fair. Runs citation-check on every appeal decision, policy or case cited by objectors or by the response itself. Use when the architect wants to "respond to objections", "answer consultee comments", "address the case officer's concerns", "prepare a rebuttal", "summarise representations", or "get ready for planning committee". Pairs with planning-research for the policy base and design-critique to test whether an objection exposes a real weakness.
license: MIT
metadata:
  author: Gaia Computer Technologies, Inc.
  version: "1.0.0"
---

# Objection Response

Answer objections the way a good case officer would read them: by theme, on planning merits, with evidence, and conceding what is fair. A measured response that amends a scheme in two places usually does more than a combative one that defends everything.

## When to use

- Representations or consultee comments have arrived on an application.
- The case officer has raised concerns and asked for a response or amendments.
- A committee date is set and the team needs to anticipate questions.

## Input

- The objection letters, representations or consultee responses (text or PDF).
- The application drawings and supporting documents.
- The applicable policy (from planning-research or supplied), with references and adoption dates.
- The jurisdiction and the authority's procedure (deadlines, whether amendments trigger re-consultation).

## Process

1. **Log every representation.** Number each, record who it is from (neighbour, amenity society, statutory consultee) and the date, and extract each distinct point.
2. **Group by theme.** Typical themes: scale and massing, design and character, heritage, overlooking and privacy, daylight and sunlight, noise, traffic and parking, trees and ecology, flood and drainage, construction impacts, need or use. Count how many representations raise each.
3. **Separate material from non-material considerations.** What counts as a material planning consideration depends on the jurisdiction. Flag points that are usually outside planning (property values, private views, boundary disputes, competition) for a planning professional to confirm, but don't dismiss residents' concerns in the response itself.
4. **Run citation-check** on every appeal decision, policy, or case quoted by objectors and on every reference the response will use. AI-written objection letters have been found citing decisions that don't exist; respond to fabricated citations factually.
5. **Draft responses per theme.** For each: summary of the concern, the relevant policy (with reference), the evidence in the submission (drawing number, report section), and the response. Where the point is fair, propose a specific amendment.
6. **Identify evidence gaps.** If a concern needs a technical report the application doesn't have (daylight, noise, transport, ecology), say so. Don't argue it without evidence.
7. **Prepare committee lines.** Three or four short statements a speaker could make, tied to policy.

## Domain knowledge

- **Volume is not weight.** Fifty identical letters on one point raise one point. Respond to the substance, and acknowledge the strength of local feeling.
- **Statutory consultees carry particular weight.** A highways authority, heritage body, environment agency, or similar objection often needs a technical response, not a design argument.
- **Amend early.** A small, specific amendment (lowering a parapet, obscure-glazing a window, moving a balcony) often resolves a theme. Show it on a drawing.
- **Tone.** Respectful, factual, no sarcasm. The audience is the case officer and committee, not the objector.

## Output format

```
## Objection Response — [Application ref], [Site]

### Representations received
| # | From (type) | Date | Points raised (themes) |
|---|---|---|---|

### Themes
| Theme | No. of reps | Material? (confirm) | Response approach |
|---|---|---|---|

### Citation check on cited references
| Reference | Cited by | Status | Note |
|---|---|---|---|

### Responses
#### [Theme]
- **Concern:** ...
- **Policy:** [ref, plan, adopted date]
- **Evidence in submission:** [drawing no. / report section]
- **Response:** ...
- **Proposed amendment (if any):** ...

### Evidence gaps
- ...

### Committee lines
- ...

> **Disclaimer:** AI-generated analysis for preliminary purposes only. All figures, standards, and references must be verified by a qualified professional before use in design, permitting, costing, contracts, or regulatory submission.
<!-- architect:requires-disclaimer -->
```

Copy the disclaimer exactly as shown, including the `<!-- architect:requires-disclaimer -->` line. That line is the machine-readable marker the plugin checks for, so keep it even in a chat reply.

## What you don't do

- Don't misrepresent an objection to make it easier to answer. Quote or summarise it fairly.
- Don't cite a policy, appeal decision or case that hasn't been checked. Unchecked references stay out.
- Don't predict the committee's decision or give legal advice on procedure or challenge.
- Don't make technical claims (daylight, noise, highways, ecology) without the report that supports them.
