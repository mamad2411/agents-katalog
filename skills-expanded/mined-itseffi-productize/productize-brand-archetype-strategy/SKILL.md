---
name: productize-brand-archetype-strategy
description: >-
  Define brand narrative, voice, imagery, symbols, and channel storytelling using brand
  archetypes. Use for brand strategy, minimum viable brand, narrative consistency, archetype
  selection, personal brand positioning, and brand story design.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Brand Archetype Strategy

## Productize Preamble

Before producing the artifact, implementation step, or code change, classify the work:

- **User/persona**: founder, product leader, AI PM, AI builder, stakeholder, or mixed/unknown.
- **Product stage**: idea, validation, PMF search, growth, scale, pivot, or unknown.
- **Artifact mode**: strategy memo, PRD, research plan, positioning, experiment, deck, roadmap, execution brief, diagnostic, or decision record.
- **Artifact format**: Markdown for short, repo-native, diff-sensitive artifacts; self-contained HTML for long, visual, shareable, interactive, or explicitly requested artifacts.
- **Evidence standard**: what is known, assumed, missing, and risky.
- **Decision mode**: recommend, ask for a blocking input, or proceed with explicit assumptions.

Operating rules:

1. Do not produce generic product strategy filler. Tie every recommendation to the user's context, evidence, stage, and decision pressure.
2. Separate facts from assumptions. Convert high-risk assumptions into tests, research prompts, or instrumentation.
3. Search existing context, attached docs, repo files, or prior Productize artifacts before inventing new structure when those sources are available.
4. Ask only for inputs that materially change the output. If the next step is obvious, proceed and state assumptions.
5. If another Productize skill is a better fit, name it and explain the routing in one sentence before continuing.
6. Enforce the output contract for this skill. Produce the artifact, implementation step, verification evidence, or code change; do not stop at a meta-explanation of the method.
7. End with the concrete next action, decision owner, validation step, metric, or artifact handoff when applicable.
8. Use the user's saved Productize preferences when available, but do not let stale preferences override explicit instructions in the current request.
9. If you must ask a blocking question, use this compact format: `AskUserQuestion: <one question> Why it matters: <decision it changes>`.
10. Record completion status for durable work as `completed`, `blocked`, `deferred`, or `needs-review` when runtime hooks are available.

Artifact format policy:

- Default to Markdown for short notes, repo-native documentation, changelog fragments, or artifacts where clean source diffs matter.
- Use a self-contained HTML file when the user asks for HTML, the artifact is likely to exceed about 100 lines, the reader needs diagrams/tables/comparisons/screenshots, the artifact is meant to be shared, or interaction/export controls would help the user stay in the loop.
- Route by product job first, then choose the format. Do not create a generic HTML workflow when a Productize playbook, gate, or routed skill owns the work.
- HTML artifacts must be local-first and portable: one file, embedded CSS/JS, no remote dependencies unless explicitly requested, readable without a dev server, responsive, accessible, and easy to skim.
- Prefer semantic sections, tables, SVG diagrams, annotated code blocks, status chips, collapsible detail, and copy/export buttons when they improve review speed. Avoid decorative complexity that hides the decision.
- For implementation work with ambiguities, use `$implementation-notes` when the user asks for a running notes file, especially `implementation-notes.html` or `implementation-notes.md`.

Runtime hooks, if available:

- Use `productize-workflow start "<user request>"` at the beginning of durable product work; it restores context, routes the request, records the session, and returns the required artifact contract.
- Use `productize-workflow complete --id <id> --status completed|blocked|deferred|needs-review --artifact-type <type> --summary <summary>` before ending durable product work; it records the artifact, saves context, and logs completion status.
- Use `productize-update-check --strict` at the start of maintenance, setup, release, or generated-output work.
- Use `productize-config` to read or write user/team preferences such as persona, artifact mode, evidence threshold, or update-check policy.
- Use `productize-session-log` to record important workflow decisions.
- Use `productize-artifact-log` when a durable artifact is produced.
- Use `productize-context-restore` before restarting long-running product work from scratch.
- Use `productize-context-save` after producing a durable strategy, research, spec, or stakeholder artifact.
- Use `productize-registry-search` or `productize-skill-router` when routing is ambiguous.
- Use `productize-completion-status` to log whether the workflow completed, blocked, deferred, or needs review.

Telemetry standard:

- Keep telemetry local by default in `.productize/` or `PRODUCTIZE_STATE_DIR`.
- Log artifact type, routing decision, evidence gaps, and completion status; do not log secrets or private customer data unless the user explicitly asks for it.

Current skill metadata:

- **Skill**: `brand-archetype-strategy`
- **Lifecycle**: Strategize
- **Category**: Marketing
- **Primary artifact**: Brand Archetype Strategy strategy memo with choices, tradeoffs, risks, and recommended next move

Use this skill when the user needs to make a brand story more coherent, memorable, and strategically expressive.

Do not use it for measuring brand health, campaign scoring, or growth funnel diagnosis unless the task includes brand narrative or identity choices.

## Core Idea

Brand archetypes are familiar narrative patterns that help people understand what a brand stands for. The archetype should shape the brand story, language, imagery, content, and channel behavior.

In a digital environment, a brand can express a primary archetype with supporting archetypes across channels and customer-journey moments. The blend must still feel intentional.

## Archetype Set

Use these archetypes as the working set:

- **Innocent**: purity, goodness, happiness, trust, simplicity, honesty.
- **Sage**: knowledge, wisdom, truth, expertise, interpretation, teaching.
- **Explorer**: discovery, freedom, adventure, individuality, curiosity.
- **Outlaw**: rebellion, disruption, rule breaking, radical change.
- **Magician**: transformation, vision, charisma, making dreams possible.
- **Hero**: courage, challenge, strength, competition, perseverance.
- **Creator**: imagination, invention, beauty, experimentation, originality.
- **Ruler**: control, order, authority, responsibility, power, structure.
- **Caregiver**: care, protection, comfort, support, empathy, commitment.
- **Everyperson**: belonging, friendship, practicality, down-to-earth connection.
- **Jester**: play, entertainment, cleverness, lightness, spontaneity.
- **Lover**: intimacy, pleasure, beauty, passion, relationship, sensuality.

## Workflow

1. **Clarify the strategic base**
   - Identify mission, promise, intended experience, and desired movement.
   - Capture target audience, category, competitors, and current perception.

2. **Infer candidate archetypes**
   - Map audience motivation and brand ambition to 2-4 plausible archetypes.
   - Reject archetypes that sound attractive but conflict with product reality, culture, or proof.

3. **Choose a primary archetype**
   - Select one dominant archetype for memory structure and consistency.
   - Explain why it fits the audience, category tension, promise, and evidence.

4. **Define supporting archetypes**
   - Add supporting archetypes only when they serve specific journey moments, channels, or audiences.
   - Specify where each supporting archetype appears and where it must not appear.

5. **Translate into expression**
   - Define voice, vocabulary, imagery, behavior, content themes, rituals, and proof points.
   - Include language to use and language to avoid.

6. **Stress test consistency**
   - Check whether the archetype makes the brand more distinctive.
   - Check whether the archetype can survive product, support, sales, hiring, and community touchpoints.

## Output

Return:

- **Brand Context**: audience, category, current perception, desired shift.
- **Archetype Recommendation**: primary archetype and 1-2 optional supporting archetypes.
- **Rationale**: fit with mission, promise, audience motivation, and category opportunity.
- **Narrative Platform**: core story, tension, promise, and proof.
- **Expression System**: voice, words, imagery, symbols, content themes, behaviors.
- **Journey/Channel Map**: how the archetype shows up across key touchpoints.
- **Do/Don't Rules**: concrete creative and messaging guardrails.
- **Consistency Risks**: where the archetype may break down.

## Quality Bar

- Do not choose archetypes by taste alone.
- Avoid making every brand a Hero, Sage, or Creator by default.
- Do not dilute the brand with a random archetype mix.
- Tie archetype choices to observable brand behavior and customer meaning.
