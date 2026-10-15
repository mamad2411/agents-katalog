---
name: emdash-sitewide-content-pass
description: >-
  Orchestrate a site-wide content improvement pass for any EmDash site. Use
  when auditing or rewriting top-level pages, archive surfaces, conversion
  copy, metadata, and AI/SEO readiness across a whole site. Sequences
  strategy, voice, SEO/E-E-A-T, copy editing, metadata, and QA. Not for
  single-article drafting, plugin work, or block-only implementation.
---

# EmDash Sitewide Content Pass

Run a full-site content improvement pass without turning it into a pile of
unscoped rewrites.

This is an orchestration skill. Its job is to decide:

- which surfaces should be included
- which surfaces should be deferred to a later wave
- which placeholder or low-value surfaces should be excluded
- which search and competitor signals should reshape route assumptions
- which specialized skills should be stacked, and in what order
- which artifacts should be created before editing begins

It is deliberately generic for any EmDash site in this repo.

## Use This When

- The user wants a site-wide copy or content improvement pass
- The user wants to review and rewrite homepage, about, service, archive,
  legal, search, or conversion surfaces together
- The user wants one workflow that combines content strategy, voice work,
  editing, SEO, AEO, and verification
- The site has a mix of durable pages and placeholder collection entries, and
  those need to be separated before rewriting

## Do Not Use This When

- The task is one page only
- The task is one article, newsletter issue, or email
- The task is plugin, schema, or block development without a content-pass goal
- The task is pure measurement only

For those cases, use the narrower skill directly.

## Core Principle

Define route role before changing prose.

On an EmDash site, bad rewrite passes usually fail because they start editing
text before answering these questions:

1. Which routes are durable?
2. Which routes are placeholders, stubs, or seed-only detail entries?
3. What is each included route supposed to do?
4. Which copy is page-local, which is shared, and which is global chrome?
5. Which route families are one decision, and which actually need
   route-by-route attention?
6. What does the live SERP imply about how those pages should compete?

Do not skip that classification step.

## Inputs To Resolve First

Resolve these in order. Only ask the user when the repo and site do not answer
them.

1. The target EmDash site root and preview URL
2. The included route set
3. The deferred route set
4. The excluded placeholder route set
5. Whether this is:
   - audit only
   - prep plus rewrite planning
   - full rewrite plus implementation
6. Any existing copy source material:
   - `copy-resources/`
   - transcripts
   - launch specs
   - brand docs
   - route audits
7. Any approved voice constraints or anti-patterns

## Skill Stack

Use these skills as a stack, not as a grab bag.

### 1. Route Framing

Use first when route roles are unclear:

- `dataforseo-operator`
- `keyword-research`
- `competitive-intelligence`
- `gstack/office-hours`
- `content-strategy`

Purpose:

- decide what each top-level route is for
- decide which routes are durable enough to rewrite now
- separate searchable, shareable, conversion, legal, and support surfaces
- pressure-test those assumptions against keyword and competitor reality

### 2. Voice System

Use before substantive rewriting:

- `brand-voice`
- `style-forensics` when you need a measured voice fingerprint

Purpose:

- create a reusable house voice
- extract measurable traits from strong existing copy
- keep later edits consistent across the site

### 3. Page-Level Audit

Use before rewriting:

- `seo-content`
- `fact-checker`
- `optimize-for-ai`

Purpose:

- score content quality and E-E-A-T
- catch weak, stale, or unsupported claims
- identify AI-citation and extraction weaknesses

Defer `meta-optimizer` until the body copy is stable.

### 4. Rewrite Execution

Use for the actual page edits:

- `copy-editor`

Use these only when needed:

- `style-writer` for net-new sections that must match a measured voice
- `content-writer` for net-new long-form content from scratch

Default assumption:

- most site-wide passes are editing passes, not blank-page drafting passes

### 5. Metadata and AEO Finish

Use after the main copy settles:

- `meta-optimizer`
- `aeo-scorecard` after implementation, for measurement rather than drafting

### 6. Verification

Use after edits land:

- `gstack/qa-only`
- browser-based rendered checks

Purpose:

- verify hierarchy, responsiveness, and copy placement
- confirm that shared components did not create regressions across routes

## Standard Workflow

### Phase 1: Scope the Pass

Build a route inventory from the live surface, usually via:

- sitemap
- explicit system routes such as `404`, search, contact-success, or utility pages

For each route, classify:

- durable vs placeholder
- route owner
- route type
- content origin
- status:
  - include
  - defer
  - exclude
- route family
- why the route is in that bucket

Use `defer` aggressively.

`Defer` is for routes that are real, but are not first-wave rewrite surfaces.
Common examples:

- taxonomy archives with durable structure but thin content
- template-level pages that are not placeholders, but are not yet worth
  rewriting
- archive-supporting surfaces that should follow the primary positioning pages

Use route-family compression before creating rewrite waves.

Examples of route families:

- `/blog/topic/*`
- `/blog/service/*`
- any repeated archive-taxonomy surface such as
  `/<collection>/<taxonomy>/*`
- any repeated collection category surface that shares one template shell

Default rule:

- treat a route family as one planning unit unless there is evidence that the
  members materially diverge in role, voice, or structure

If a collection-detail surface is obviously placeholder-driven, exclude it from
the first rewrite wave and usually from the first rewrite pass entirely.

### Phase 2: Create Working Artifacts

Create artifacts before rewriting. Keep one durable ledger per pass.

Recommended artifacts:

1. Route inventory table
2. Search-intelligence packet
3. Header inventory table
4. Copy-surface inventory
5. CTA and shared-module inventory
6. Page-role matrix
7. Rewrite ledger with:
   - route
   - route family
   - current role
   - target role
   - status (`include`, `defer`, `exclude`)
   - wave
   - priority
   - blockers
   - approval state

Read [references/workflow-artifacts.md](references/workflow-artifacts.md) when
creating these files. It contains the recommended columns and artifact shapes.
Read [references/search-intelligence-packet.md](references/search-intelligence-packet.md)
when the rewrite pass needs live keyword and competitor pressure-testing.

The audit is not complete when only headings are inventoried.

Before drafting begins, the pass should also inventory the core non-header copy
surfaces that actually do commercial work:

- hero support lines
- lead paragraphs
- proof blocks and stat strips
- testimonial excerpts
- CTA labels and CTA ladders
- form labels, placeholders, and helper text
- FAQ answer quality
- empty and placeholder states
- post-submit reassurance
- newsletter and insider value propositions

Prefer project-local audit folders such as:

- `plans/audits/`
- `copy-resources/`
- another repo-approved content-review location

Do not scatter findings across chat only.

## Required Subagent Prompting Protocol

When this workflow uses subagents, the prompt MUST include all of the
following:

1. **Exact skill file(s) to load**
   - Do not assume the subagent will discover the right local skill on its own.
   - Point to the exact file under
     `your local agent-skills directory`.
   - Example:
     `the `style-forensics` skill`

2. **Exact CLI or tool surface to use**
   - Do not say "use the browser" generically.
   - Name the tool or CLI explicitly.
   - For headless browser work, always direct the subagent to use
     `agent-browser` as the default browser surface.

3. **Exact source surface**
   - Give the exact URL or exact local file to analyze.
   - If a fallback or alternate winner is allowed, say the selection rule out
     loud.
   - Example:
     `Analyze https://kwnyc.com/`
     or
     `Start from the packet, then choose the strongest non-directory winner for
the query family if the named URL is clearly weaker.`

4. **Exact context artifacts**
   - Name the context file(s) the subagent should read first.
   - For this workflow, that usually includes the current search-intelligence
     packet and any prior synthesis notes.

5. **Owned output path**
   - Each subagent gets one output file or one disjoint write set.
   - Never let two subagents write to the same audit file.

6. **Task-local success standard**
   - Tell the subagent what a good result looks like.
   - For copy forensics, require measurable observations, proof devices,
     framing patterns, steal guidance, avoid guidance, and a usefulness verdict.

7. **Output contract**
   - Require: files inspected, commands run, file written, evidence found,
     blockers, and final verdict.

If those instructions are missing, the subagent prompt is incomplete.

## Required Skill Smoke Test

Skills are effectively code.

Do not treat a new or changed skill as delivered until it has been smoke
tested through the same workflow it is supposed to enable.

Minimum smoke-test rule:

1. Pick at least **two** representative targets or exemplars.
2. Run at least **two `gpt-5.4-mini` subagents** against those targets using
   the concrete prompt template above.
3. Verify the actual written output files, not just the agent summaries.
4. Compare the outputs for:
   - method fidelity
   - evidence density
   - usefulness of steal and avoid guidance
   - cleanup cost
5. If the outputs are inconsistent or weak, tighten the skill and rerun the
   smoke test before claiming delivery.

If the user explicitly asks for a stronger-model comparison, rerun the same
targets with `gpt-5.5` and compare on the same rubric.

For copy-forensics fan-out, use a concrete template like this:

```text
You are not alone in the codebase. Do not revert or overwrite other agents'
or the user's edits.

Own ONLY this file:
<output-file>

Load and follow:
- the `style-forensics` skill

Read these context files first:
- <current-search-intelligence-packet>
- <any prior synthesis or comparator note>

Use this exact source surface:
- <source-url>

If a different live winner may be better, use this rule:
- <selection rule>

Use `agent-browser` as the default headless browser surface.

The output file must include:
- source URL
- why the page is being mined
- measurable voice observations
- sentence and paragraph rhythm observations
- trust and proof devices
- framing patterns
- conversion posture
- what to steal
- what to avoid
- overall usefulness verdict
- what this specifically teaches the rewrite

Final response must list:
- files inspected
- commands run
- file written
- blockers
- final verdict
```

### Phase 3: Build The Search-Intelligence Packet

Before voice work or rewriting, build a live search-intelligence packet for the
included or first-wave routes.

This is the missing step between route scoping and rewrite execution.

Use:

- `dataforseo-operator`
- `keyword-research`
- `competitive-intelligence`

Use the helper scripts when local execution is appropriate:

- `scripts/dataforseo-runtime.ts`
- `scripts/sitewide-serp-intelligence.ts`

If the packet yields three or more strong non-directory exemplars, fan out
style forensics in parallel.

Default fan-out pattern:

- use multiple `gpt-5.4-mini` subagents unless the user asks for a stronger
  model comparison
- assign one exemplar per subagent
- assign one output file per subagent under a dedicated audit folder such as
  `plans/audits/serp-style-forensics/`
- require each subagent to load
  `the `style-forensics` skill`
- require each subagent to use `agent-browser` for headless browser work
- require each subagent prompt to name the exact source URL, exact context
  files, exact owned output path, and the exact required report sections
- synthesize the resulting notes before updating the house voice or rewrite
  plan

Default packet goals:

- discover the strongest candidate query families for the included routes
- identify whether the query intent is clean or split
- identify who dominates the live SERP
- inspect what type of surfaces are winning:
  - local pack
  - directory
  - brokerage
  - boutique practice
  - editorial content
- surface repeated title and framing patterns
- extract tone, voice, and framing signals from the winning pages
- use those findings to confirm or revise the first-wave route roles

Do not let internal route labels or prior copy alone define page strategy when
the live market is signaling something different.
Do not let voice work happen in a vacuum when the winning pages are clearly
using a repeatable framing pattern.
Keywords are the discovery mechanism for this step, not the actual objective.
The actual objective is better copy, sharper positioning, and stronger
conversion language grounded in what the market is already rewarding.

### Phase 4: Lock Route Roles

Before editing any page, define:

- the page's job
- the audience stage
- the conversion expectation
- whether the page is primarily:
  - positioning
  - proof
  - search capture
  - archive navigation
  - legal or support

If the page role is unclear, use `gstack/office-hours` and then
`content-strategy`.

Do not lock page roles without also locking shared-module ownership.

At minimum, identify whether these are page-local or shared:

- contact capture modules
- newsletter modules
- footer headings and labels
- archive intro modules
- repeated CTA rows

If shared copy is driving multiple routes, treat it as a system surface with
its own review row, not as a repeated page-level note.

### Phase 5: Build the House Voice

If the site lacks a stable voice guide:

- run `brand-voice`
- optionally run `style-forensics` on the best existing materials

Do this once, then reuse it for the whole pass.

### Phase 6: Audit Included Pages

Audit only the included route set with:

- `seo-content`
- `fact-checker`
- `optimize-for-ai`

Flag:

- weak heading hierarchy
- stale or unsupported claims
- low-trust or low-E-E-A-T pages
- repeated shared chrome that should not dominate rewrite time
- pages where the role and the current copy are mismatched

Run a lighter classification-only audit on deferred surfaces.

The point of `defer` is not to ignore the surface. The point is to avoid
letting it steal rewrite energy from the durable high-leverage wave.

### Phase 7: Rewrite in Waves

Recommended wave order:

1. Homepage and primary positioning pages
2. Service or audience pages
3. Conversion pages
4. Archive pages
5. Legal, support, and utility pages
6. Shared/global chrome

Keep global repeated copy separate from page-local copy so the same decision is
not made ten times.

Apply a wave budget.

Default planning budget:

- Wave 1: up to 5-10 durable primary routes plus any shared modules they depend on
- Wave 2: one archive family at a time
- Wave 3: utility, legal, and repeated chrome

If a wave grows because a route family contains many members, compress it back
to the family shell unless the members genuinely need different copy.

### Phase 8: Apply to the EmDash Site

Once copy is approved, route it into the actual EmDash surfaces:

- CMS page content
- seed content
- shared block data
- site settings
- SEO fields

Read these local skills when needed:

- `../building-emdash-site/SKILL.md` for EmDash content and rendering patterns
- `../emdash-cli/SKILL.md` for CLI-based CMS operations

Do not start schema or plugin changes unless the content pass genuinely needs
them.

### Phase 9: Verify the Rendered Site

After implementation:

- run `gstack/qa-only`
- verify the included routes in the browser
- check desktop and mobile heading flow
- confirm shared components do not reintroduce duplicate or stale copy

If AI visibility matters, run `aeo-scorecard` after the copy ships.

## Default Defer Rules

Unless the user says otherwise, consider deferring these to a later wave:

- taxonomy archives with mostly repeated structure
- thin but durable archive-support pages
- template-confirmation pages that are not pure placeholders
- support and compliance routes that do not shape the site's positioning
- partner, category, or topic pages that are structurally real but currently
  underfilled

## Default Exclusion Rules

Unless the user says otherwise, consider excluding these from the first rewrite
wave:

- placeholder collection-detail entries
- seed-only or demo entries
- routes that exist only to exercise a template
- unstable archive-detail surfaces whose underlying content model is still in
  flux

Keep the template or archive shell in scope if it is durable, even when the
underlying entries are not.

## Output Contract

A good run of this skill should produce:

- the included route set
- the deferred route set with reasons
- the excluded route set with reasons
- the route-family compression decisions
- the search-intelligence packet
- the exact skill stack being used
- the ordered workflow
- the audit artifacts created
- the rewrite queue
- the verification plan

If implementation is in scope, also produce:

- the specific EmDash surfaces to edit
- the shared components at risk of copy drift
- the post-implementation QA route list
- the wave budget actually being used

## Anti-Patterns

- Rewriting page copy before defining route role
- Rewriting route families one page at a time before proving the members differ
- Rewriting page copy before checking what the live SERP and competitor field
  imply about page role
- Treating placeholder entries like durable launch surfaces
- Treating every non-placeholder route as first-wave
- Using binary include vs exclude when `defer` is the correct answer
- Mixing repeated global chrome with page-local hero copy in one review bucket
- Skipping a shared-module inventory and then rediscovering the same copy issue
  across many routes
- Letting keyword and competitor research happen too late, after voice and copy
  decisions have already hardened
- Optimizing metadata before the page argument is stable
- Using `content-writer` by default for an editing-heavy pass
- Leaving findings in chat instead of a durable ledger
- Overfitting the workflow to one site's route names or one client's copy set

## Related Skills

- `dataforseo-operator` for choosing the right live DataForSEO bundle
- `keyword-research` for the query universe
- `competitive-intelligence` for framing and competitor pressure
- `content-strategy` for portfolio-level page-role and pillar decisions
- `brand-voice` for a reusable voice guide
- `style-forensics` for measured voice extraction
- `copy-editor` for existing-copy rewrites
- `seo-content` for E-E-A-T and structure audits
- `meta-optimizer` for final metadata tightening
- `optimize-for-ai` for citation-readiness improvements
- `fact-checker` for claim verification
- `gstack/qa-only` for rendered verification after edits
