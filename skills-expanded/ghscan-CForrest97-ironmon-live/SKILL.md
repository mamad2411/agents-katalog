---
name: new-decision
description: Scaffold a new DEC-### decision record with a valid ID, filename, frontmatter, required sections, and README index entry, and wire it into any PRD or context that references it. Use only when explicitly asked to create a decision record; do not use for repository structure, tooling, agent workflow, or CI policy choices.
---

# New decision

`docs/decisions/README.md` is explicit: decision records are for consequential
product and domain choices only, never for repository structure, tooling
preferences, agent workflow, or CI policy. Confirm the choice qualifies before
scaffolding.

1. List `docs/decisions/*.md` and pick the next unused `DEC-###`.
2. Copy `docs/decisions/_template.md` to
   `docs/decisions/DEC-###-short-name.md`, where `short-name` is a lowercase,
   hyphenated slug.
3. Fill frontmatter: `id` (matching the filename), `title`, `status`
   (`proposed` unless told otherwise), `category` (`product` or `domain`),
   `supersedes` (an array of `DEC-###` IDs, or `[]`).
4. Set the `# H1` to exactly match `title`.
5. Fill every required section — Context, Decision, Consequences,
   Alternatives, Supersedes, Open Questions — with real content. Never leave
   `TBD`, `TODO`, `{{...}}`, `[fill...]`, or `replace with`.
6. The Supersedes section must name every ID listed in the `supersedes`
   field, or say exactly `None.` when the field is empty.
7. If `status` is `accepted`, Open Questions must say exactly `None.`
8. Add a Markdown list entry linking the new title to
   `DEC-###-short-name.md` to the Index in `docs/decisions/README.md`,
   matching the format of the existing entries there.
9. If a `PRD-###` or `CTX-###` document motivated this decision, add the new
   `DEC-###` to that document's `decisions` metadata array and make its
   Decisions section mention the ID — the validator treats this as a required
   two-way reference, not optional cleanup.
10. Run `npm run validate:docs` (or `npm run check`) and fix any reported
    error before treating the record as scaffolded.
