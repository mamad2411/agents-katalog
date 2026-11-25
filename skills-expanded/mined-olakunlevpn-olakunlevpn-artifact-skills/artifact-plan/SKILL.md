---
name: artifact-plan
description: OUTPUT IS ALWAYS A `.html` FILE (or a small folder of `.html` files for multi-page plans) — never `.md`, never plain markdown. The file extension on a "PLAN" deliverable is `.html`, not `.md`. Use this skill whenever the user asks for an implementation plan, technical plan, project plan, roadmap, milestone breakdown, comparison sheet, options analysis, RFC, design doc, technical proposal, "weigh three approaches", "lay out the work", "break this into phases", "compare X vs Y vs Z", or any forward-looking planning artifact that should be delivered as a polished HTML document with milestones, risk tables, open questions, and decision criteria. Pair with artifact-css for the underlying design system. Do NOT use for one-paragraph "yeah let's do that" answers or for already-decided execution checklists with no open questions left.
---

# artifact-plan

> ## OUTPUT CONTRACT
>
> **Produces ONE `.html` file. Not markdown. Not `.md`. Not plain text.**
>
> Plans, comparison sheets, and roadmaps are HTML artifacts. The file extension is `.html`. The content is HTML elements (`<h1>`, `<table>`, `<aside class="callout">`, `<div class="timeline">`, etc.) — never markdown syntax (`# heading`, `| pipe table |`, `* bullet`, `**bold**`).
>
> This holds even when the plan is "internal", "working", "for me to track", or "for the project's PLAN file". If a planning artifact comes from this skill, it is HTML.
>
> The file name is typically `PLAN.html`, `IMPLEMENTATION-PLAN.html`, `<topic>-plan.html`, `<decision>-comparison.html`, or `roadmap-<period>.html`. NEVER `PLAN.md`.
>
> Use the templates in `templates/`. Inline `artifact.css` inside `<style>` (Mode B — single-file portable) or `<link>` to it. Use the class vocabulary from `artifact-css/SKILL.md`.

---

Forward-looking planning artifacts. Three closely related shapes: the implementation plan (one approach laid out in milestones), the comparison sheet (multiple approaches weighed side-by-side), and the roadmap (longer horizon, multiple workstreams, dates and risks).

Read `artifact-css/SKILL.md` first for the full OUTPUT CONTRACT, the design system, the page skeleton, the token reference, and the optional jQuery interactivity layer. This skill does NOT use jQuery — every plan template is pure HTML and CSS.

## Three subtypes

| Subtype | Template | Use when |
|---|---|---|
| Implementation plan | `templates/implementation-plan.html` | One approach already chosen. Break it into milestones, ordered, with clear owners, dates, risks, open questions. |
| Comparison sheet | `templates/comparison-sheet.html` | Decision still open. Two or three approaches need side-by-side weighing on cost, complexity, risk, and time-to-value. |
| Roadmap | `templates/roadmap.html` | Longer horizon (quarter to year). Multiple workstreams. Date-driven commitments + softer "looking into" items. |

If the user's request doesn't match cleanly, start from the implementation plan template and adapt.

## Anatomy of an implementation plan

Every implementation plan is built from seven blocks. Use this order.

1. **Header.** Eyebrow with the team or system name, h1 with the plan title ("New billing engine — phase 1"), and a `.lead` paragraph stating what changes after this plan ships. If the plan was generated from a specific request, include the `.prompt-box`.
2. **Summary band.** A `.kv-strip` with: total scope (e.g., "~6 weeks"), milestones count, owner / DRI, target ship date, current status (`.badge` chip — proposed / approved / in-flight). Not stat cards — this is qualitative information.
3. **Why now.** A short `.callout` (oat) with two to four sentences. What forced this onto the roadmap. The cost of doing nothing. The reader who reads only the callout still knows why they're being asked to staff it.
4. **Milestones.** A `.timeline` with three to six `.milestone` rows. Each milestone has: the `when` slot (week or date range), an `.axis` with a `.dot` (clay = upcoming, olive = done, rust = at risk), and a `.body` with an h3 (the deliverable), one paragraph of detail, an optional `.tag-list` of touched packages or services, and an optional risk note (`.note-warn` for "watch out for X").
5. **Scope and non-scope.** A `.grid-2` with two `.panel`s side-by-side. "In scope" on the left as a bulleted list. "Explicitly out of scope" on the right. Be aggressive about what's out — non-scope is the highest-leverage section for setting reviewer expectations.
6. **Risks and mitigations.** A `.table` with three columns: risk · likelihood (`.badge-warn` / `.badge-danger` / `.badge-info`) · mitigation. Five rows max — if you have more, the plan isn't ready.
7. **Open questions.** A `.highlights` list of decisions still owed. Each question begins with the verb "Decide" or "Choose" and ends with the name of who decides. If the list is empty, drop the section. If the list has more than five items, the plan is premature.

End the page with a tiny meta line (`.muted .small`): "Generated 2026-05-12. Last updated 2026-05-12."

## Anatomy of a comparison sheet

The decision artifact. Goal: a reader who hasn't been in the conversation can finish this page and recommend a choice with confidence.

1. **Header.** Eyebrow with the decision name ("Pick a queue backend"), h1, `.lead` framing the constraint set in one sentence ("must handle 50k jobs/min, exactly-once semantics, ops team has Postgres expertise only").
2. **Recommendation band.** A `.callout` with the recommended option named explicitly, plus three sentences: what it gets us, what it costs us, what we'll have to revisit in six months. If the recommendation is "no decision yet, kick to next quarter", say so — that's a valid output.
3. **Side-by-side panels.** A `.grid-3` (or `.grid-2` if only two options) of `.panel`s. Each panel has the option name as an h3, a `.tag` row with one-word descriptors ("managed", "self-hosted", "rewritten"), a `.kv-strip` of the same six dimensions per panel (cost / time-to-implement / ops burden / blast radius if wrong / vendor lock-in / team familiarity), and a short prose paragraph stating the case for this option.
4. **Scoring table.** A `.table` of the same dimensions as rows and the options as columns. Cells are short verdicts ("low", "medium", "high", or specific numbers). The recommended option's column header gets `.badge-clay` to flag it. This is the page the reader screenshots.
5. **Tradeoff prose.** Two or three paragraphs walking through the most consequential dimensions. Comparison cells are signal; this section is the explanation. Lead each paragraph with the dimension in bold.
6. **What would change the recommendation.** A `.highlights` list of three to five conditions. Each item starts with "If…" and ends with "…then pick option B instead." This forces the recommender to commit to the conditions under which they'd reverse course.
7. **Decision and owner.** A small `.kv-strip` at the bottom: decision · owner · decision-by date · expiry of this analysis (when assumptions go stale).

## Anatomy of a roadmap

Long horizon. The most common failure is treating it like a status report. Resist that — roadmaps are about commitments and bets, not delivery numbers.

1. **Header.** Eyebrow with the time period ("Q3-Q4 2026"), h1 with the roadmap title ("Platform roadmap — H2"), `.lead` with the overall thesis ("Stabilize the multi-tenant data plane while quietly building toward GA of the workflow engine").
2. **Pillars.** A `.grid-3` of `.panel`s — one per workstream / pillar. Each panel has an h3 (pillar name), a one-line goal statement, and a `.kv-strip` of "owner" + "target shipping window" + "confidence" (`.badge-success` "high" / `.badge-warn` "medium" / `.badge-danger` "low"). Pillars are usually three to four.
3. **Timeline.** A `.timeline` spanning the full period. Each `.milestone` has a date range as `when`, a `.dot` (clay = planned, olive = done, sky = stretch, rust = at risk), and a `.body` with the deliverable, the pillar it belongs to (`.tag`), and a one-line "what this unlocks for users" or "what this unblocks internally".
4. **Bets and risks.** Two columns in a `.grid-2`. Left panel: "Bets we are making" — three to five items, each one a one-sentence statement of an assumption the roadmap depends on. Right panel: "Risks we are tracking" — three to five items, each with a likelihood `.badge`.
5. **What's intentionally not on the roadmap.** A short list. The act of naming this is what separates a roadmap from a wishlist.
6. **Cadence and review.** A `.kv-strip` at the bottom: review cadence · next review date · owner of the document · how readers should flag scope changes.

## Voice and density rules

1. **Verbs before nouns.** "Migrate billing to event-sourced" beats "Migration of billing to event-sourcing".
2. **Dates over relative time.** "By 2026-07-15" beats "End of next quarter".
3. **Names over roles.** "Aisha owns this" beats "TBD assignment".
4. **Confidence is explicit.** Every milestone or commitment carries a confidence chip. Hidden uncertainty is the #1 reason plans rot.
5. **Out-of-scope > scope.** Spend more words on what you're not doing than what you are. Reviewers project ambiguity onto silence.
6. **No padding.** "We will work closely with the data team to ensure alignment on schemas" is filler. Cut it. Either there's a meeting on the calendar or there isn't.

## Common mistakes

- **Milestone soup.** Six milestones with no dates, no dependencies, no owners. Forces the reader to interpret. Plans must commit.
- **Risk table that lists nothing risky.** "Could introduce a small bug" is not a risk. If you can't write a risk that would make a director uncomfortable, the table is decoration.
- **Comparison sheet without a recommendation.** Refusing to commit isn't neutrality — it's punting work to the reader. State a preference. The reader can disagree.
- **Hidden assumptions.** A plan that depends on "the platform team finishing the new auth service first" without naming that dependency is a plan that will slip. Name it in scope or in risks.
- **Roadmap with too many pillars.** Five-plus workstreams = no strategy. Compress or split into separate documents.
- **Open questions that have already been answered.** Keep the section honest. Move resolved items to "decisions made" or delete them.

## Linkage

If a plan was generated from a specific RFC, ticket, or thread, link to it from the header eyebrow:

```html
<p class="eyebrow with-rule">Platform · RFC-247 · billing rewrite</p>
```

If the plan supersedes an earlier plan, link to it with a `.note-info` at the top:

```html
<aside class="note note-info">
  <strong>Supersedes</strong> the 2026-04-02 draft. Major changes: dropped phase 2, moved cutover earlier, added two risks.
</aside>
```

## After the artifact

Always offer the plain-text Slack-paste summary alongside the HTML. For plans, the paste version is: title · DRI · ship date · top-three risks · top-three open questions. Five lines max.
