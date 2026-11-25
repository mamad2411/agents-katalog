# Visual Reference Research

## Purpose
Collect, normalize, and synthesize visual references (moodboards, palette extractions, type specimens, layout patterns) into an evidence-linked design direction with explicit tokens, rationale per reference, and documented exclusions.

## Use when
- Kicking off or re-directing a product's visual language and needing comparable references with recorded provenance.
- Extracting palette, typography scale, spacing rhythm, or component patterns from inspirational products or competitors.
- Resolving subjective design disputes with a citable reference board instead of opinion.
- Operating in mode(s): `research`.

## Do not use when
- Auditing live production websites for implementation details (use `website-forensics`).
- Writing production CSS or component code (downstream implementation work, not research).
- Running usability tests or accessibility audits on shipped UI (use dedicated testing flows).

## Required context
- Product requirements (audience, brand adjectives, platform constraints, light/dark scope).
- Design tokens (existing palette, type scale, spacing base if evolving rather than greenfield).
- Wireframe / UI view under exploration (which screens the references must inform).

## Procedure
1. **Frame the brief first**: record 3–5 brand adjectives (e.g. calm, clinical, editorial), the screens in scope, and hard constraints (WCAG AA, existing brand color) before collecting anything.
2. **Collect with provenance**: capture 8–15 references as full-viewport screenshots with source URL, capture date, and viewport size; never store cropped fragments without their source context.
3. **Extract measurable tokens**: sample each reference for dominant palette hex values (5 max per reference), type roles (display/body/mono with families and scale ratios), spacing base (4 vs 8 pt), and radius/shadow language.
4. **Cluster and converge**: group references into 2–3 directions (e.g. dense-utilitarian vs airy-editorial); score each against the brief adjectives and constraints; recommend exactly one direction with runner-up noted.
5. **Record exclusions**: explicitly list references that were rejected and why (e.g. "Reference 7 rejected: 3.2:1 body contrast fails WCAG AA"), so the decision is auditable.
6. **Hand off a token draft**: emit a candidate token table (color roles, type scale, spacing, radius) plus the moodboard file wired in `templates/wireframe-spec.md`.

## Decision rules
- **Provenance mandatory**: every reference carries source URL + capture date; unsourced images are excluded from the board.
- **No reference without rationale**: each kept reference has one sentence linking it to a brief adjective or constraint.
- **Contrast checked at research time**: any palette direction must show AA-passing body-text pairs before recommendation.
- **One recommended direction**: the deliverable converges; it never presents options without a recommendation.

## Evidence required
- Moodboard with 8–15 sourced references and per-reference rationale.
- Candidate token table with contrast ratios computed.
- Passing execution log from `scripts/verify.sh`.

## Output contract
- Design specification / findings (recommended direction + exclusions log).
- Accessibility audit scorecard (contrast pairs, focus-visibility notes per direction).
- UI tests (token-level assertions: palette roles complete, scale ratios consistent).

## Stop conditions
- One direction recommended with token draft, contrast evidence, and exclusions log complete.
- Token budget exhausted.
- Blocked on external dependency.

## Escalation rules
- Escalate to design owner if brand constraints contradict accessibility minimums (e.g. mandated low-contrast palette).
- Escalate if reference licensing prohibits internal reuse of captured imagery.
