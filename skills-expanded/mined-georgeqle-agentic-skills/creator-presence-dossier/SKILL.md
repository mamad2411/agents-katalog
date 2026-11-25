---
name: creator-presence-dossier
description: Build a repo-backed Markdown dossier of a creator's public professional presence, career arc, proof assets, platform roles, and next strategy route
type: research
version: v0.4
argument-hint: "[creator or project slug]"
interview_depth: none
---

# Creator Presence Dossier

Invoke as `$creator-presence-dossier`.

## Report-First Approval Gate

Default to scope-first approval: before synthesized research, inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions in a `review` alignment page plus a concise conversation summary.

Do not perform synthesized research, rank candidates, make recommendations, or write working packets or canonical deliverables until final compiled YAML approves the research scope. Minimal pre-approval discovery may identify available files, source categories, and open questions; label it as scope evidence, not findings.

After approved research-scope YAML, perform the research and write only the non-canonical working packet defined in the staged workflow. Then update the `review` alignment page with findings and stop again for feedback-only YAML or final compiled YAML artifact approval before creating or updating canonical research, spec, or task files.

Do not include `Recommended next skill`, `Recommended next command`, or downstream routing language. The approval request itself is the next action. Only emit next-skill routing after the approved artifact has been written or updated.

## Staged Research Workflow

Use this staged workflow for synthesized research or report outputs that would create or update canonical research, spec, or task files.

1. **Stage 1 - Scope discovery and approval.** Inspect only enough repository, user, and source context to propose research scope, source plan, assumptions, output paths, and approval questions. Build the `review` HTML alignment page before synthesized research. The page must render the proposed scope, available source categories, known context, assumptions/confidence, proposed working-packet and canonical output paths, and research-scope approval gates. Stop for final compiled YAML approval of the research scope. Do not perform synthesized research, rank candidates, make recommendations, or write working packets, canonical research, spec, or task files in Stage 1.
2. **Stage 2 - Research and artifact review.** Only after approved research-scope YAML with no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback, perform the synthesized research, run required source/code checks, and write only a non-canonical working packet: flat mode uses `research/_working/preliminary-<skill>-research.md`; product-path mode uses `research/{slug}/_working/preliminary-<skill>-research.md`. Replace `<skill>` with this skill's `name` value. Raw evidence or search logs may remain as supporting evidence where this skill already requires them, but synthesized deliverables stay in the working packet. Update the `review` HTML alignment page with the full preliminary packet, evidence matrix, assumptions/confidence register, source coverage gaps, proposed canonical file changes, and artifact approval gates. Stop for either feedback-only YAML or final compiled YAML. Feedback-only YAML revises the working packet and page, then remains in Stage 2.
3. **Stage 3 - Finalize approved artifacts.** Consume final compiled YAML for artifact approval only when it has no unresolved `needs-clarification`, unresolved `down` feedback, or other unresolved negative feedback. Apply approved edits first, archive the working packet to `docs/history/archive/YYYY-MM-DD/HHMMSS/<original-working-path>`, remove the active working packet, write the approved canonical artifacts to the unchanged output paths below, and convert the alignment page to `confirmed` with the approval record preserved.

Canonical output paths remain unchanged. Search logs and other supporting evidence remain allowed only where this skill's output contract already requires them.

## Evidence And Feedback Handling

Treat user feedback as input to evaluate, not as automatic ground truth.

- For factual, evidentiary, technical, or source-backed claims: verify against available evidence. If the user appears to misunderstand the evidence or states something factually incorrect, push back clearly and cite the evidence. Do not rewrite findings merely to agree.
- For taste, brand, positioning preference, risk appetite, prioritization, or other subjective judgment calls: weigh user feedback heavily and adapt the recommendation unless it conflicts with verified evidence.
- When feedback mixes facts and preference, separate them explicitly: correct the factual part, then incorporate the preference where it is a legitimate judgment call.
- When uncertain, say what is known, what is inferred, and what would change the conclusion.

## Process

1. Identify the creator, project slug, platforms, and existing evidence paths from the user request and repo context.
2. Read `research/creator-platforms/capability-matrix.md` if it exists. If it is missing, recommend `$creator-platform-capability-matrix` before synthesis.
3. Read `research/creator-platforms/evidence-schema.md` if it exists. If it is missing, recommend `$creator-evidence-schema` before synthesis.
4. Inspect available normalized and raw creator evidence under `research/creator-platforms/data/<platform>/<slug>/` and any user-specified evidence paths.
5. Cite the normalized evidence paths, raw evidence paths, source URLs, and capture dates used before making claims.
6. Write or update `research/creator-presence/<slug>.md`.
7. Separate public/professional evidence from private repo planning context. Exclude private planning context unless the user explicitly asks to preserve it as internal notes.
8. End with a next-skill recommendation based on the dossier findings.

## Evidence Boundaries

The dossier is for public and professional presence: profiles, posts, articles, talks, podcasts, newsletters, repos, product docs, public company pages, and owner-provided exports the user chooses to include.

Do not include private repo planning context, private messages, private contacts, unpublished strategy notes, credentials, sensitive account data, or unrelated personal information in the public dossier. If the user explicitly wants internal planning context captured, place it in a clearly labeled internal notes section and mark the source boundary.

When evidence contains sensitive or mixed public/private material, ask the user to redact or exclude the private material before analysis. Do not infer private facts from public artifacts.

## LinkedIn Evidence Handling

LinkedIn evidence must come from user-provided or public-safe sources only:

- Owner-provided LinkedIn exports.
- Profile snapshots supplied by the user.
- Public unauthenticated profile or company page captures.
- User-provided post, share, article, newsletter, rich media, recommendation, skill, position, education, certification, or company page snapshots.
- User-provided admin or analytics exports only when the user explicitly says they are authorized to share them.

Do not collect LinkedIn evidence through logged-in scraping, bot-protection bypass, paywall access, access-control circumvention, paid API dependency, private-data collection, or private relationship graph extraction.

Before synthesis, classify every LinkedIn source in the evidence register as one of:

- `public`: public profile, public company page, public post/share/article, public recommendation, public rich media, or public career milestone.
- `owner-provided`: owner export, profile snapshot, post/article snapshot, recommendation snapshot, skills export, positions export, education export, or authorized analytics/admin export.
- `admin-provided`: company/page analytics or admin material supplied by an authorized owner/admin.
- `internal notes`: private repo notes the user explicitly asks to preserve outside the public dossier.
- `mixed/redaction needed`: any source containing private contacts, private messages, relationship data, sensitive account data, unrelated personal information, confidential employer/customer material, or a mix of public and private fields.

For `mixed/redaction needed` LinkedIn evidence, stop before synthesis and ask the user for a redacted version or permission to exclude the private fields. If the user has already provided a redacted extract, cite only the redacted path and record the excluded fields as evidence gaps. Never summarize private contacts, private messages, relationship data, or unrelated personal information into the public dossier.

## Source Types

Support these source families when evidence is present:

- LinkedIn personal profiles, company pages, exports, posts, articles, recommendations, and manual/public snapshots.
- Personal websites, blogs, portfolios, public bios, RSS feeds, and sitemaps.
- GitHub profiles, public repos, contribution evidence, READMEs, releases, and product proof.
- Podcasts, interviews, guest appearances, show pages, feeds, and transcripts when available.
- Talks, slide decks, event pages, conference bios, and video descriptions.
- Newsletters, public archives, owner exports, and subscriber or performance notes when owner-provided.
- Product docs, launch notes, case studies, changelogs, public company pages, and customer-facing proof assets.

## Output Requirements

Create the `research/creator-presence/` directory if it does not exist.

`research/creator-presence/<slug>.md` must contain:

- Scope, capture date, and source assumptions.
- Identity.
- Current public promise.
- Career timeline.
- Platform map.
- Core themes.
- Expertise claims.
- Proof assets.
- Signature formats.
- Audience/community signals.
- Product/company connections.
- Gaps, contradictions, and stale positioning.
- Evidence register.
- Next collection tasks.
- Recommended next skills.

Do not invent missing metrics, private context, career milestones, content bodies, transcripts, or audience signals. Record missing fields as evidence gaps.

## Markdown Contract

Use these sections in the dossier, keeping unsupported sections brief with explicit evidence gaps rather than omitting them:

1. `# <Creator or Project Name> Presence Dossier`
2. `## Scope and Capture`
   - Creator or project slug.
   - Capture date.
   - Source assumptions.
   - Included platforms and excluded platforms.
   - Public/professional boundary summary.
3. `## Identity`
   - Public names, roles, affiliations, locations only when publicly stated, and canonical profile links.
   - Distinguish confirmed identity facts from inferred identity signals.
4. `## Current Public Promise`
   - The creator's current public positioning, promise, audience, and category.
   - Confidence and evidence gaps for each claim.
5. `## Career Timeline`
   - Chronological public milestones, roles, launches, talks, publications, repos, and product/company events.
   - Include dates or date ranges when available; mark undated items as gaps.
6. `## Platform Map`
   - Platform, handle or URL, role of the platform, activity state, evidence coverage, and collection gaps.
   - Support LinkedIn, personal websites/blogs, GitHub, podcasts, talks, newsletters, and product docs when evidence is present.
   - For LinkedIn, distinguish personal profile, company page, posts/shares, articles/newsletters, recommendations, skills, positions, education, rich media, and owner/admin-provided analytics when present.
7. `## Core Themes`
   - Recurring subjects, categories, language patterns, and audience problems.
8. `## Expertise Claims`
   - Claimed expertise, evidence supporting each claim, confidence, and missing proof.
9. `## Proof Assets`
   - Public artifacts that substantiate credibility: posts, articles, repos, talks, case studies, product docs, launches, testimonials, podcasts, newsletters, and public metrics.
10. `## Signature Formats`
    - Repeated formats, hooks, series, talk structures, newsletter styles, repo/doc formats, and content patterns.
11. `## Audience and Community Signals`
    - Public engagement signals, community roles, collaborator signals, comments, testimonials, recommendations, event participation, and owner-provided metrics.
    - LinkedIn recommendations, reactions, comments, follower counts, impressions, or company/page analytics may appear only when they are public, owner-provided, admin-provided, or already redacted.
12. `## Product and Company Connections`
    - Companies, products, docs, launches, customer proof, open-source projects, and founder/operator narratives tied to the creator.
13. `## Gaps, Contradictions, and Stale Positioning`
    - Missing evidence, outdated profiles, contradictory claims, unsupported metrics, stale bios, unclear role changes, and collection risks.
14. `## Evidence Register`
    - A table with one row per material source.
15. `## Next Collection Tasks`
    - Prioritized tasks to close evidence gaps, with target platform, collection method, owner, and reason.
16. `## Recommended Next Skills`
    - The next creator-media skills to run and why, using the routing rules below.

## Evidence Register

Every material source must appear in the evidence register. Each row must include:

- `Source path or URL`: repo path, raw evidence path, normalized evidence path, or public URL.
- `Capture date`: the date the source was collected or last verified; use `unknown` only when the date is unavailable and record that as a gap.
- `Source family`: LinkedIn, personal website/blog, GitHub, podcast, talk, newsletter, product docs, YouTube, owner export, or other.
- `Public/private boundary`: `public`, `owner-provided`, `internal notes`, or `mixed/redaction needed`.
- `Confidence level`: `high`, `medium`, or `low`.
- `Claims supported`: the dossier claims this source supports.
- `Evidence gaps`: missing dates, missing body text, unavailable metrics, stale captures, missing transcripts, unclear attribution, or private material that must be excluded.

For LinkedIn rows, `Claims supported` should identify the specific evidence kind when relevant: profile export, profile snapshot, post/share, article/newsletter, rich media, recommendation, skill, position, education, certification, company page, public snapshot, owner-provided analytics, or admin-provided analytics.

Use confidence levels consistently:

- `high`: primary public source, owner-provided export, or directly captured artifact with a capture date.
- `medium`: secondary public source, partial capture, or credible source with incomplete metadata.
- `low`: inferred signal, stale capture, ambiguous attribution, or source with unresolved gaps.

## Approved Artifact Handoff

After an approved synthesized write, explicit write/update mode, or any direct artifact mutation:

- List every created or updated synthesized artifact path in the final response.
- State the verification performed, such as readback, schema/check command, or why no executable verification applies for a Markdown-only strategy artifact.
- Check and report the relevant git status for intended artifacts when the project is a git repository. If intended artifacts are modified or untracked, make the next action shipping, committing, or an explicit dirty-artifact handoff before recommending downstream strategy work.
- Do not imply the research workflow is complete while approved artifacts remain untracked or uncommitted unless the user explicitly asked not to ship.
- If stopping for approval before writing, the approval request remains the next action; do not include downstream routing.

## Intent-Aware Routing

Before applying the default `## Next-Skill Routing` sequence, classify the user's immediate intent and route to the missing action that best serves that intent:

- Strategy refresh: recommend the missing or stale positioning, programming, portfolio, metrics, or product-media artifact.
- Recording prep: recommend the missing series spec, script, build proof, walkthrough guide, or validation artifact needed before recording.
- Upload prep: recommend packaging, title/thumbnail, description, chapters, or final metadata work before broader strategy work.
- Performance review: recommend metrics, cadence, portfolio, peer benchmark, or owner-analytics export work before new content planning.
- Owner analytics or private/manual platform evidence: route to an explicit manual/guide handoff instead of inventing unavailable metrics.
- Dirty intended artifacts: route to shipping/commit/handoff first, not another creator strategy skill.

Use the default next-skill sequence only when no stronger user intent, missing artifact, manual blocker, or dirty-artifact handoff applies.

## Alignment Page

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/creator-presence-dossier-{topic}.html`.

## Constraints

- Do not mutate external accounts or publish content.
- Do not bypass bot protections, rate limits, paywalls, login walls, or access controls.
- Do not require paid APIs, privileged platform programs, or logged-in scraping.
- Do not treat missing metrics, missing bodies, or unavailable transcripts as failures; record them as evidence gaps.
- Cite source paths, source URLs, capture dates, and confidence levels for substantive claims.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
