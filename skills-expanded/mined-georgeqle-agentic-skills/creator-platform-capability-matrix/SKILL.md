---
name: creator-platform-capability-matrix
description: Map creator platforms to free/manual evidence sources, available fields, audit depth, operational risk, and recommended next skill
type: research
version: v0.6
argument-hint: "[creator or project slug]"
interview_depth: none
visual_tier: visual
---

## Pack Availability Guard

Before telling the user to run a skill from another project-local pack, check `.agents/project.json.enabled_packs`. If the target pack is not enabled, recommend `npx skillpacks install <pack>` from the project shell. Global skills are always valid. Skills from this same pack are valid because the current skill is already running from that pack.

# Creator Platform Capability Matrix

Invoke as `$creator-platform-capability-matrix`.

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

1. Identify the creator, project, and platforms in scope from the user request and repo context.
2. Prefer free, open-source, owner-provided, and manual evidence paths. Do not require paid APIs, privileged platform programs, logged-in scraping, or access-control bypasses.
3. Write `research/creator-platforms/capability-matrix.md`.
4. Include a row for every platform in the baseline matrix, even when no evidence is currently available.
5. Add extra platform rows only when the repo or user request gives a concrete reason.

## Baseline Platforms

Include these rows:

- LinkedIn personal profile
- LinkedIn company page
- Personal website/blog
- Newsletter
- Podcast
- GitHub
- X/Threads/Instagram/TikTok
- Bluesky/Mastodon

## Collection Methods

Classify every evidence source with one or more of these collection methods:

- `export`: owner-provided platform export, CSV, ZIP, or analytics download.
- `manual_snapshot`: user-saved page, screenshot, CSV, Markdown note, copied post text, or manually captured URL list.
- `rss_feed`: RSS, Atom, JSON feed, podcast feed, sitemap, or newsletter feed.
- `public_page_capture`: public unauthenticated page capture with polite retrieval.
- `open_source_tool`: OSS tooling such as feed parsers, Playwright screenshots, `trafilatura`, or allowed public-media tools.
- `free_api`: official free API or public protocol with no paid dependency.

## Matrix Columns

The matrix must include these columns:

- Platform
- Content types
- Evidence sources
- Collection methods
- Likely fields
- Missing fields
- Metric availability
- Body availability
- Media availability
- Transcript availability
- Peer benchmarking practicality
- Operational risk
- Audit depth
- Recommended next skill

## Platform Guidance

- LinkedIn personal profile: start with owner export plus manual snapshots, public unauthenticated page captures, and user-provided files. Treat profile analytics, search appearances, connection data, private messages, private contacts, relationship data, and sensitive account fields as unavailable unless the owner provides already-redacted evidence.
- LinkedIn company page: start with owner/admin export plus manual snapshots and public unauthenticated page captures. Treat company/page analytics and API fields as unavailable unless owner-provided or already authorized. Treat official LinkedIn API use as a later authorized lane only when credentials, permissions, and scope are already in place.
- Personal website/blog: prefer RSS, sitemap, and public page capture for body text and metadata.
- Newsletter: prefer export, RSS, and public archives. Treat subscribers and private analytics as owner-only.
- Podcast: prefer RSS, public show pages, and manual transcripts. Do not invent transcripts.
- GitHub: use public API, public repo evidence, and manual repo notes for projects and proof assets.
- X/Threads/Instagram/TikTok: prefer manual snapshots and exports. Treat metrics as owner-only unless public counters are visible.
- Bluesky/Mastodon: use public protocol/API where available and respect instance or service limits.

## LinkedIn Baseline

For LinkedIn rows, the default collection lane is owner exports, manual snapshots, public unauthenticated page captures, and user-provided files. Do not attempt logged-in scraping, bot-protection bypass, paywall access, access-control circumvention, or private-data collection.

Before any LinkedIn analysis, require redaction or exclusion of private contacts, private messages, relationship data, sensitive account data, unrelated personal information, and any employer/customer confidential material. If the only available LinkedIn source is high-risk, stop and ask for an owner export, manual snapshot, public unauthenticated capture, or redacted user-provided file.

## Operational Risk

Classify each row as:

- `low`: export, user-supplied files, RSS/feed, public protocol/API, or public repo evidence.
- `medium`: public page capture or OSS tooling where platform limits, robots rules, or stale snapshots need care.
- `high`: access-controlled, bot-protected, logged-in, paywalled, private, or ToS-sensitive surfaces.

High-risk rows must recommend manual snapshots, owner exports, or stopping for user-provided evidence instead of automated capture.

## Output Requirements

Create the `research/creator-platforms/` directory if it does not exist.

`research/creator-platforms/capability-matrix.md` must contain:

- Scope and capture date.
- Source assumptions and exclusions.
- The full capability matrix.
- Evidence gaps by platform.
- Recommended collection order.
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

When this skill produces durable deliverables (research, specs, plans, reports, prototypes, or any document output), build a full-depth HTML alignment page following `ALIGNMENT-PAGE.md` in this skill's directory. Output: `alignment/creator-platform-capability-matrix-{topic}.html`.

## Constraints

- Do not mutate external accounts or collect private data.
- Do not bypass bot protections, rate limits, paywalls, login walls, or access controls.
- Do not use logged-in LinkedIn scraping, paid API dependency, bot-protection bypass, access-control circumvention, or private-data collection as a baseline path.
- Do not imply YouTube-equivalent metrics, transcripts, thumbnails, or benchmarking are available for every platform.
- Record missing metrics, missing bodies, and missing transcripts as evidence gaps.
- Require LinkedIn private contacts, messages, relationship data, sensitive account data, and unrelated personal information to be redacted or excluded before analysis.
- Cite repo paths and source URLs when available.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
