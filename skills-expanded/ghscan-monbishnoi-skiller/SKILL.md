# Author a Skiller v3 Skill Contract

Use this prompt with a coding agent after a human has approved a skill dossier.

## Inputs

- Approved skill name and class
- Evidence-backed purpose and task shapes
- Representative positive examples
- Neighboring skills and disambiguation rules
- Typical tool trajectory and constraints
- Proposed lifecycle tier

## Authoring Contract

Create one canonical `<skill-name>/SKILL.md` using the v3 contract in
`prompts/skill-template.md`. Keep the three layers distinct:

1. **WHAT** — frontmatter: identity, behavior summary, use and avoid boundaries,
   related-skill disambiguation, class, lifecycle tier/TTL, and one or two examples.
2. **WHEN** — a compact retrieval card compiled from positive task evidence. Do
   not put rejected or negative examples in the searchable document because
   retrieval systems can strengthen the very association those examples are
   intended to prevent.
3. **HOW** — the Markdown body: complete operating instructions, safeguards,
   tools, workflow, and verification.

## Requirements

- Use only evidence supplied in the approved dossier or verified repository facts.
- Do not invent private paths, credentials, organizations, people, or production data.
- Keep `avoid_when` and related-skill comparisons in WHAT for the selector model;
  keep them out of the searchable WHEN card.
- Set `tier_ttl_days` to the policy value for the selected tier:
  `hot: 2`, `cool: 3`, `cold: 20`, `archive: null`.
- Run `skiller validate <skills-dir>` and `skiller cards <skills-dir>`.
- Review the generated retrieval card and confirm it contains no HOW procedure.
- Run repository tests. Report evidence and remaining ambiguity rather than
  silently expanding the contract.
