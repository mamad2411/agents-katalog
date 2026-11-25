---
name: creator-evidence-schema
description: Define normalized creator evidence records, raw evidence paths, confidence fields, privacy notes, and collection constraints for multi-platform audits
type: research
version: v0.6
argument-hint: "[creator or project slug]"
interview_depth: none
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Creator Evidence Schema

Invoke as `$creator-evidence-schema`.

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

1. Identify the creator, project, platforms, and evidence already present in repo context.
2. Read `research/creator-platforms/capability-matrix.md` if it exists. If it is missing, recommend `$creator-platform-capability-matrix` before collection.
3. Write `research/creator-platforms/evidence-schema.md`.
4. Define raw evidence folders under `research/creator-platforms/data/<platform>/<slug>/`.
5. Define normalized records that future audits can store as JSONL when machine-generated or Markdown tables when manually curated.
6. Record missing metrics, missing bodies, private fields, stale captures, and unavailable transcripts as explicit evidence gaps.

## Collection Methods

Every normalized record must declare exactly one `capture_method` from this vocabulary:

- `export`: owner-provided platform export, CSV, ZIP, or analytics download.
- `manual_snapshot`: user-saved page, screenshot, CSV, Markdown note, copied post text, or manually captured URL list.
- `rss_feed`: RSS, Atom, JSON feed, podcast feed, sitemap, or newsletter feed.
- `public_page_capture`: public unauthenticated page capture with polite retrieval.
- `open_source_tool`: OSS tooling such as feed parsers, Playwright screenshots, `trafilatura`, `yt-dlp`, or allowed public-media tools.
- `free_api`: official free API or public protocol with no paid dependency.

## Raw Evidence Layout

Use this root for source artifacts:

```text
research/creator-platforms/data/<platform>/<slug>/
```

Recommended subpaths:

- `raw/` for original exports, saved HTML, screenshots, copied text, feed payloads, and media metadata.
- `text/` for extracted body text, transcripts, descriptions, and manually cleaned readable content.
- `normalized/` for JSONL or Markdown evidence registers.
- `notes/` for collection notes, privacy redactions, and reviewer observations.

Raw files must be cited by local repo path. Do not summarize private or sensitive raw material into public-facing artifacts unless the user explicitly authorizes it.

## LinkedIn Evidence Baseline

For LinkedIn evidence, allow only these baseline capture paths unless the user has already provided explicit authorization and credentials for a later API lane:

- owner exports or admin exports supplied by the user;
- manual snapshots, screenshots, copied post/article text, or manually captured URL lists;
- public unauthenticated page captures with polite retrieval;
- redacted user-provided files.

LinkedIn personal analytics, company/page analytics, private contacts, private messages, relationship data, sensitive account data, and API-only fields are unavailable unless owner-provided, admin-provided, already authorized, and redacted where needed. Do not use logged-in scraping, bot-protection bypass, paywall access, access-control circumvention, paid API dependency, or private-data collection as a baseline collection path.

Before normalizing LinkedIn records, require `privacy_notes` to state whether private contacts, messages, relationship data, sensitive account data, unrelated personal information, and confidential employer/customer material were redacted, excluded, or absent.

## Normalized Record Fields

Each evidence record must define these fields or record why the field is unavailable:

- `evidence_id`: stable local ID.
- `platform`: source platform.
- `source_type`: post, article, video, podcast, talk, repo, profile, comment, newsletter, press, milestone, or other documented source type.
- `source_url`: canonical URL when available.
- `raw_path`: local raw evidence path.
- `captured_at`: capture date/time.
- `capture_method`: one collection method from this skill.
- `auth_context`: public, owner_export, admin_export, manual, or unknown.
- `terms_risk`: low, medium, or high.
- `title`: title or short label.
- `body_text_path`: path to extracted text if present.
- `published_at`: publication date when available.
- `creator_role`: author, speaker, host, guest, founder, maintainer, commenter, curator, or other documented role.
- `media_type`: text, image, video, audio, code, slide, mixed, or other documented media type.
- `topic_tags`: curated topic tags.
- `content_role`: acquisition, trust-building, proof, education, launch support, community, career signal, or other documented role.
- `metrics`: platform-specific metrics object.
- `metric_confidence`: observed, owner-provided, estimated, or unavailable.
- `evidence_confidence`: high, medium, or low.
- `privacy_notes`: redactions, sensitive fields excluded, private context boundaries, or sharing restrictions.
- `review_notes`: human review notes, conflicts, stale evidence, and quality caveats.

LinkedIn records must use `auth_context` values conservatively: `public` for public unauthenticated captures, `owner_export` for personal exports, `admin_export` for company/page exports or analytics supplied by an authorized admin, and `manual` for user-saved snapshots or notes. Do not normalize private LinkedIn contacts, messages, relationship data, or sensitive account fields unless the user explicitly supplies redacted evidence for that purpose.

## Metrics Object

Metrics are optional and must not be invented. Include only metrics that are directly observed, owner-provided, or clearly marked as estimated.

Allowed metric keys include:

- views
- impressions
- reads
- listens
- likes
- reactions
- comments
- replies
- reposts
- shares
- saves
- clicks
- subscribers
- followers
- engagement_rate

If metrics are unavailable, set `metric_confidence` to `unavailable` and record the gap. If metrics exist but body text is missing, do not infer content-quality causes from performance alone.

## Confidence Guidance

Use `evidence_confidence` consistently:

- `high`: owner export, public repo/API/protocol record, preserved raw artifact, or source URL plus captured raw copy.
- `medium`: manual snapshot, copied text, public page capture, feed item, or evidence with partial raw support.
- `low`: stale snapshot, missing source URL, incomplete raw evidence, conflicting platform fields, or unverifiable manual note.

Use `terms_risk` consistently:

- `low`: export, user-supplied file, RSS/feed, public protocol/API, or public repo evidence.
- `medium`: public page capture or OSS tooling where platform limits, robots rules, or stale snapshots need care.
- `high`: access-controlled, bot-protected, logged-in, paywalled, private, or ToS-sensitive surfaces.

High-risk evidence must recommend manual snapshots, owner exports, or stopping for user-provided files instead of automated capture.

## Output Requirements

Create the `research/creator-platforms/` directory if it does not exist.

`research/creator-platforms/evidence-schema.md` must contain:

- Scope and capture date.
- Source assumptions and exclusions.
- Raw evidence root and recommended subpaths.
- Collection method vocabulary.
- Normalized record schema.
- Metrics object schema.
- Metric confidence and evidence confidence rules.
- Privacy and redaction notes.
- Evidence gap rules for missing metrics, bodies, media, and transcripts.
- Recommended next skill.

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

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/creator-evidence-schema-{topic}.html`.

## Constraints

- Do not mutate external accounts or collect private data.
- Do not bypass bot protections, rate limits, paywalls, login walls, or access controls.
- Do not require paid APIs, privileged platform programs, or logged-in scraping.
- Do not use logged-in LinkedIn scraping, bot-protection bypass, paid API dependency, access-control circumvention, or private-data collection as a baseline path.
- Do not invent optional metrics, bodies, media assets, or transcripts.
- Do not treat missing metrics or missing bodies as failures; record them as evidence gaps.
- Ask the user to redact or exclude private contacts, private messages, sensitive account data, and unrelated personal data before analysis.
- For LinkedIn, also ask the user to redact or exclude relationship data and confidential employer/customer material before analysis.
- Cite raw repo paths and source URLs when available.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
