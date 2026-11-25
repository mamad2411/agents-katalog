---
name: cli-forge-profile
description: "Create, rewrite, audit, and optimize professional identity content: CV/resume, cover letters, LinkedIn headline/About/experience/skills, Reddit/community bios, GitHub profile READMEs, portfolio case studies, speaker bios, freelance-platform profiles, freelance positioning, recruiter-facing narratives, recommendation requests, and maintainable profile Markdown files. Use when the user asks to improve a public professional profile, bio, headline, experience bullet, skills list, profile README, or readability/comprehension/memorability of a profile or bio. Do not use for general technical README editing, product documentation, landing pages, or product copy that is not about a person's professional identity."
---

# Profile Forge

Optimize professional identity text so it is clear, credible, searchable, and ready to paste into the target platform.

This skill is worth using when the artifact represents a person: CV/resume, LinkedIn, GitHub profile README, Reddit/community bio, portfolio case study, speaker bio, freelance profile, recommendation request, or a maintained profile fact base. For project, product, repo, or company pages, hand off to `cli-forge-readme`, `cli-forge-doc`, `cli-forge-prez`, or `ui-ux-pro-max` instead.

## Core Rule

Write from verified facts. Separate final copy from editorial notes. Never present planned, archived, speculative, or R&D-only work as delivered experience.

Default to confidentiality. Do not name clients, sectors, regulated contexts, architectures, metrics, repositories, or security-sensitive details unless the user has explicitly made them public or approved their use. Prefer disclosable categories such as "regulated infrastructure", "PCI-DSS fintech", or "air-gapped environment" only when they do not reveal protected operational context.

When the user gives existing files, preserve their source-of-truth role:
- Raw extraction stays raw.
- Optimized profile files contain paste-ready copy.
- Strategy files contain rationale, checklists, and next actions.
- CV files prioritize ATS, density, proof, and role fit.

For maintained profile systems, keep verified facts in one canonical file such as `profile/career-facts.yml` or an existing `cv-data.yaml`, then derive CV, LinkedIn, GitHub, Reddit, freelance, and portfolio files from it. Track which language is canonical when maintaining `*.fr.md` and `*.en.md` pairs.

## Relationship With Other cli-* Skills

Use this skill as the personal-identity layer. Recommend, do not auto-run:

| Situation | Better handoff |
|---|---|
| Outreach message, recruiter reply, relance, everyday email/DM | `cli-forge-plume` |
| Public repo README or product README | `cli-forge-readme` |
| Full project documentation, onboarding, architecture docs | `cli-forge-doc` |
| Speaker deck, meetup talk, pitch slides | `cli-forge-prez` |
| Portfolio site UI or landing page design | `ui-ux-pro-max` |
| Proof project deserves a live demo script | `cli-forge-demo` |
| Public code needs authorship/IP protection | `cli-watermark` |
| Profile claims depend on code quality or project proof | `cli-cycle` on the proof repo |

If installed alongside `cli-code-skills`, the shared reconnaissance model in `../shared/recon.md` is useful. Adapt it to a person: what they do, who reads the profile, what expensive problem they solve, headline proof, differentiator, and next action.

## Workflow

1. Identify the target surface: CV, cover letter, LinkedIn, Reddit, GitHub/profile README, portfolio, speaker bio, freelance service page, freelance platform profile, or recommendation/message.
2. Extract the profile reconnaissance brief:
   - target reader,
   - target role or mission,
   - top 3 proof points,
   - constraints and forbidden claims,
   - language, geography, and market norms,
   - next action expected from the reader.
3. Build the copy hierarchy:
   - Hook: who, for whom, with what outcome.
   - Proof: quantified outcomes, recognizable environments, shipped artifacts.
   - Scope: tools, domains, sectors, constraints.
   - CTA: what the reader should do next.
4. Build or update the fact ledger before polishing language:
   - facts verified,
   - facts inferred,
   - facts forbidden for confidentiality,
   - facts needing user approval,
   - proof artifacts linked to each claim.
5. For CV/LinkedIn work, extract 8-12 target keywords from the role or mission brief and place them naturally in the profile and relevant proof bullets.
6. Rewrite with platform constraints, applying the editorial lens by default (trajectory + scan-and-recall + the anti-flou table from `references/editorial-lenses.md`), not only when an author is named.
7. Proofread the result in its own pass before the gate: grammar, spelling, agreements, articles and prepositions, anglicisms, and phrasing/clarity, in the target language (e.g. French accents and agreements). Mandatory for any published copy.
8. Run the publication gate before final output.
9. Remove AI-assistant process markers from publishable profile files: no GPT/Claude mentions, model scores, "validated by AI", generation notes, or generic AI-like filler. Preserve factual AI product names only when they are part of the user's real work, a quoted public artifact, or a technical keyword.
10. Add a short publication checklist when the output is a `.md` working file.
11. Flag uncertain claims with `NEEDS-REVIEW` instead of smoothing them over.

## Read References On Demand

- Read `references/platforms.md` before writing platform-specific output or checking character/structure constraints.
- Read `references/editorial-lenses.md` **by default for every CV / LinkedIn / profile / freelance rewrite** — apply the trajectory + scan-and-recall lenses and the anti-flou table on every pass — and also whenever the request mentions narrative, attention, memorability, comprehension, Christian Jacq, Fabien Olicard, storytelling, or reader psychology.
- Read `references/method-bank.md` when the user asks for best practices, books, videos, methods, research-backed writing, or source-informed optimization.

## Output Shapes

### Paste-Ready Rewrite

Use this for direct user requests such as "rewrite my LinkedIn About" or "optimize this CV bullet".

```markdown
## Version recommandee
[final copy]

## Pourquoi ca marche
- [short reasoning tied to reader/search/proof]

## Points a verifier
- [only factual checks, limits, or risk]
```

Match the user's language unless they ask for translation or bilingual output.

### Markdown Profile File

Use this when editing or creating `.md` files that are working documents.

```markdown
# [Surface] - [Name] - [Language/Target]

## Statut
- Source canonique: oui/non
- Fichier faits: [profile/career-facts.yml / cv-data.yaml / other]
- Cible: [reader / mission / role]
- Derniere validation: [date if known]
- Langue canonique: [fr/en/other]
- Niveau anonymisation: [public / anonymized / confidential]
- Ne pas presenter comme realise: [guardrails]

## A copier
[platform-ready sections]

## Checklist publication
- [ ] Limits checked
- [ ] Claims verified
- [ ] Sensitive clients/sectors/metrics anonymized or approved
- [ ] Keywords present without stuffing
- [ ] CTA present
- [ ] AI-assistant process markers removed from publishable fields
- [ ] Source-of-truth updated if this is not canonical

## Notes editoriales
[rationale, variants, manual actions]
```

### Canonical Fact Ledger

Use this shape when the user wants a maintainable profile system or when claims are spread across CV, LinkedIn, GitHub, and portfolio files.

```yaml
person:
  canonical_language: fr
  target_markets: [France, remote-eu]
  public_positioning: ""
claims:
  - id: claim-001
    text: ""
    status: verified # verified | inferred | needs-review | forbidden
    evidence: ""
    surfaces: [cv, linkedin, github, portfolio]
    confidentiality: public # public | anonymized | private
    last_checked: YYYY-MM-DD
```

Do not invent this file if the user only wants a one-off rewrite. Suggest it when the same facts must feed multiple surfaces or languages.

### Audit

Lead with findings, then fixes.

Score each dimension 0-10:
- Clarity: can a recruiter understand the profile in 10 seconds?
- Proof: are claims backed by concrete outcomes?
- Searchability: are platform keywords present naturally?
- Differentiation: is the candidate memorable without exaggeration?
- Fit: does the text match the target mission or role?
- Risk: are claims defensible and non-confidential?

Use the same `NEEDS-REVIEW` label for any claim that blocks a confident rewrite.

## Publication Gate

Before delivering final copy, check:

- **Pre-conditions:** target reader, target surface, language, geography, and forbidden claims are known.
- **During:** one positioning direction is edited at a time; keep variants separate instead of blending them.
- **Post-verification:** character limits fit, first screen passes the 10-second test, claims map to evidence, confidentiality is preserved, keywords are present without stuffing, CTA is clear, a language proofread pass was done (grammar, spelling, agreements, articles/prepositions, anglicisms, phrasing — in the target language), and canonical facts were updated when required.
- **Publishability:** public fields and ready-to-copy files contain no AI-assistant process markers such as GPT/Claude notes, model scores, "validated by AI", generation comments, or meta-rationale intended only for the working document.

If a gate fails, provide the best safe draft plus a `Points a verifier` section. Do not hide factual gaps by making the copy more generic.

## Writing Standards

- Prefer "problem -> action -> result -> proof" over abstract positioning.
- Use one idea per sentence in top sections.
- Put the strongest commercial/recruiter signal in the first 2-3 lines.
- Assume scan-first reading: headings, bullets, and first words carry more weight than middle prose.
- Repeat the same strategic keywords consistently; do not create synonym soup.
- Treat "I help [X] achieve [Y] with [Z]" as a starting scaffold, not a mandatory shape. Do not reuse the same sentence skeleton across LinkedIn, freelance pages, GitHub, and portfolio copy.
- Keep jargon only when it is either searchable or immediately proven.
- Replace "I am passionate about" with delivered work, constraint, or result.
- Replace vague words like "governance", "souverainete", "control layer", or "transformation" with concrete mechanisms when possible: DLP, audit logs, air-gapped deployment, CI/CD policy, IAM, runbook, SLO, migration, cost reduction.
- Remove AI-assistant process markers from publishable copy: no GPT/Claude mentions, model scores, "AI validated" claims, generation notes, or generic AI-like filler. Keep factual AI product names only when they are part of the user's real work, a quoted artifact, or a technical keyword.
- Avoid vanity adjectives: excellent, innovative, cutting-edge, world-class, passionate.
- Preserve confidentiality: anonymize clients, sectors, numbers, personal contact details, proprietary architectures, abandoned/private repositories, testimonials without consent, and protected personal characteristics when needed.

## Platform Defaults

When the user gives no target, optimize for LinkedIn first if the source is a profile, and for ATS CV first if the source is a resume/CV.

For senior technical profiles, default to:
- headline: role + niche + proof domain + core technologies;
- About: 3-line hook, 3-5 proof bullets, current focus, CTA;
- Experience: 2-4 bullets per role, each with scope/result/constraint;
- Skills: select only labels that support the target role and can be connected to experience or proof; count follows platform capacity, search value, and evidence density rather than a fixed quota;
- CV: prefer the shortest version that preserves relevant evidence; commonly one page for earlier careers and one to two pages for experienced industry candidates, unless market, academic, or application instructions require otherwise.

## Guardrails

- Do not imitate a living author's style. If the user names a writer or public figure, convert it into abstract, high-level editorial principles.
- Do not invent metrics, employers, dates, certifications, talks, publications, repositories, or client outcomes.
- Do not optimize toward hype if it weakens trust. A profile should be memorable because it is precise.
- Do not mix final copy and private reasoning in fields that will be pasted publicly.

## Final Handoffs

End with handoffs only when useful:

- `cli-forge-readme` for a proof repository whose README needs to support the profile.
- `cli-forge-prez` for a speaker bio that needs a talk deck.
- `cli-forge-demo` for a portfolio proof project that needs a reproducible demo.
- `cli-watermark` when public code is part of the professional proof and IP defense matters.
