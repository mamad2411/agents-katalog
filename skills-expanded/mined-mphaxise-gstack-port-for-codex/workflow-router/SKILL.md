---
name: workflow-router
description: Natural-language router for GStack, GBrain, browser QA, automations, memory, design, review, ship, and Praneet extension skills; choose the smallest useful skill set.
---

# Workflow Router

Use this skill when the user speaks naturally and should not have to remember the exact skill names.

This router is repo-local. Its job is to translate a plain-English request into the smallest useful combination of installed skills.

Default posture: act like the user's chief of staff for skill selection. The user is deliberately delegating more skill-picking judgment to Codex, so consider the available skill surface proactively instead of waiting for exact skill names.

Read `references/intent-map.md` before routing if the match is not obvious.

## Workflow

1. Cast a generous first-pass net.
   - list every skill that could plausibly add leverage
   - include operating-context skills such as `brain-ops`, `query`, `reports`, `capture`, `outcome-memory`, or `responsible-design-review` when the task has memory, decision, ethics, or follow-up implications
   - do not stop at the first matching skill
2. Classify the request by intent:
   - planning
   - spec or issue creation
   - diagramming
   - engineering design
   - brain lookup
   - signal capture
   - brain setup or sync
   - brain taxonomy or schema
   - idea lineage
   - skill optimization
   - source or meeting ingest
   - research or enrichment
   - responsible design or accessibility
   - founder strategy
   - design leadership
   - maintenance or testing
   - iOS app work
   - browser QA
   - automation
   - review or ship
   - publishing or reporting
3. Critically pare down the candidate list:
   - Is this a one-time task or a repeated workflow?
   - Is the user asking for execution, review, strategy, memory, or governance?
   - Is the work high-stakes enough to justify safety, responsible design, accessibility, security, or research checks?
   - Would the skill add real context or quality, or just process overhead?
   - Is there a natural pipeline, or is one skill enough?
4. Pick the smallest useful final set of skills:
   - usually one skill
   - sometimes two in sequence
   - rarely three if there is a natural pipeline
5. Tell the user briefly which skill(s) you are using and why.
6. Execute the chosen skill workflow instead of asking the user to reformulate the request.

## Default Routing Rules

- If one specific skill clearly fits, use that skill and skip extra routing overhead.
- If the user asks for founder-style or scope pressure-testing, use `plan-ceo-review`.
- If the user is still brainstorming, validating whether to build something, or shaping a pre-plan idea, use `office-hours`.
- If the user asks to spec something out, file an issue, or write a ticket, use `spec`.
- If the user wants the planning stack run in one pass, use `autoplan`.
- If the product direction is chosen and architecture or execution rigor is needed, use `plan-eng-review`.
- If the user wants pre-implementation design critique, use `plan-design-review`.
- If the user wants responsible design, human impact, social ethics, consent, dark patterns, or vulnerable-user review, use `responsible-design-review`.
- If the user wants accessibility, inclusive interaction quality, WCAG-style review, screen reader/keyboard review, or cognitive load review, use `accessibility-review`.
- If the user wants CDO-level design governance, critique culture, design principles, or stakeholder design alignment, use `design-leadership-review`.
- If the user wants pre-implementation developer-experience critique, use `plan-devex-review`.
- If the user wants live visual polish or a design audit, use `design-review`.
- If interface work needs shared context, deterministic checks, browser evidence, or an Impeccable runtime fallback, use `design-quality`.
- If the user wants iOS app QA, bug fixing, design review, debug bridge refresh, or bridge cleanup, use `ios-qa`, `ios-fix`, `ios-design-review`, `ios-sync`, or `ios-clean`.
- If the user wants a stronger design system or visual direction, use `design-consultation`.
- If the user wants multiple design directions, use `design-shotgun`.
- If the user wants a design turned into code, use `design-html`.
- If the user wants an architecture diagram, flowchart, or visual map, use `diagram`.
- If the user wants a real onboarding or docs audit for developers, use `devex-review`.
- If the user wants memory-grounded answers, use `query` or `brain-ops`.
- If the user wants to trace how an idea evolved, use `idea-lineage`.
- If the user wants to set up, refresh, or check GBrain health, use `setup-gbrain`, `sync-gbrain`, or `gbrain-advisor`.
- If the user wants to update upstream GBrain, use `gbrain-upgrade`.
- If the user wants Impeccable drift or adoption status, use `gstack-upgrade` with the Impeccable capability map.
- If the user wants something saved into the brain, use `capture`, then `brain-taxonomist` if the filing target is unclear.
- If the user wants a specialized ingest, use `signal-detector`, `ingest`, `idea-ingest`, `media-ingest`, or `meeting-ingestion` based on the artifact.
- If the user wants to change where brain pages belong, use `schema-author` after `brain-taxonomist`.
- If the user wants to consolidate brain page types or migrate schema packs, use `schema-unify`.
- If the user wants current research, academic verification, article enrichment, strategic reading, or concept synthesis, use `perplexity-research`, `academic-verify`, `article-enrichment`, `strategic-reading`, or `concept-synthesis`.
- If the user wants research distilled into decision-ready design or product insight, use `research-synthesis`.
- If the user wants startup, founder, product-market, or investment-style judgment, use `startup-memo`.
- If the user wants a competitive landscape or category map, use `market-map`.
- If the user wants archive, book, voice-note, or PDF brain processing, use `archive-crawler`, `book-mirror`, `voice-note-ingest`, or `brain-pdf`.
- If the user wants a work-session organization pass, use `eiirp`.
- If the user wants to learn from whether a prior plan or review worked, use `outcome-memory`.
- If the user wants to optimize or tune an existing skill, use `skill-optimizer`.
- If the user wants skillpack health or post-restart validation, use `skillpack-check` or `smoke-test`.
- If the user wants recurring work, use `cron-scheduler`.
- For a bug, check its cause directly and verify the fix on the failing path.
- For claims in a report use `fact-check`. For an ambiguous identity use `resolve-before-asking`.
- Use `eval-plan` for a model comparison and `design-motion` for a loop based on an approved still.
- If the user wants pre-landing scrutiny, use `review`.
- If the user wants to push and open a PR, use `ship` after `review`.
- If the user wants to merge and verify production, use `land-and-deploy`.
- If the user wants a documentation sync after shipping, use `document-release`.
- If the user wants missing docs generated, use `document-generate`.
- If the user wants a PDF made from markdown, use `make-pdf`.
- If the user wants a landing queue or release slot report, use `landing-report`.
- If the user wants QA or browser verification, use `qa` and `browse`.
- If the user wants read-only web data extraction, use `scrape`; if the flow should become reusable, use `skillify`.
- If the user wants report-only QA, use `qa-only`.
- If the user wants a security audit, use `cso`.
- If the user wants to save or resume working state, use `context-save` or `context-restore`; use `checkpoint` only for legacy compatibility.
- If the user wants general GStack routing, use `gstack`.
- If the user wants repo or corpus health, use `health`, `maintain`, `testing`, or `gbrain-advisor`.

## Guardrails

- Do not ask the user to memorize skill keywords.
- Do not route to multiple skills when one will do.
- Do not overload a simple task with a parade of skills just because they are available.
- Do not skip the first-pass candidate scan for ambiguous, strategic, repeated, or high-stakes work.
- Do not claim a skill was used if you only borrowed the idea.
- If no installed skill meaningfully helps, proceed normally instead of forcing a bad match.
