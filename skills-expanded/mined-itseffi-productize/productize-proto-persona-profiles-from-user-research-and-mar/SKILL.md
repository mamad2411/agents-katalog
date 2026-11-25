---
name: productize-proto-persona-profiles-from-user-research-and-market-data
description: >-
  Proto-persona profiles from user research and market data. Use when the user needs a product
  workflow for user research related to proto-persona profiles from user research and market
  data. Trigger terms: user-research, personas, ux.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Proto-persona profiles from user research and market data

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

- **Skill**: `proto-persona-profiles-from-user-research-and-market-data`
- **Lifecycle**: Discover
- **Category**: Discovery
- **Primary artifact**: Proto-persona profiles from user research and market data research brief with evidence, insight clusters, assumptions, and next validation steps

Use this skill to run the Productize prompt contract for **Proto-persona profiles from user research and market data**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- `{{USER_RESEARCH}}`: Interview notes, quotes, observations, transcripts.
- `{{MARKET_DATA}}`: Segment size, competitors, market trends.
- `{{BEHAVIORAL_INSIGHTS}}`: Analytics, JTBD signals, usage patterns.
- `{{DEMOGRAPHICS}}`: Age, location, income, education, and related profile context.
- `{{CONSTRAINTS}}` (optional): Industry, region, compliance, accessibility constraints.
- `{{PREFERENCES}}` (optional): `tone`, `depth` (`brief|standard|deep`), `number_of_personas` (default `1`).
</provided_inputs>

GOAL
Synthesize mixed research inputs into concise, evidence-linked proto-persona profile(s) ready for early product decisions and validation.
Success metric:
- Persona profiles are internally consistent and clearly distinguish evidence from assumptions.
- Each profile includes confidence, explicit unknowns, and prioritized probing questions.
- Output follows required markdown canvas structure exactly.

CONSTRAINTS
- Use only provided inputs; if data is missing, write `TBD` and cover it in Probing Questions.
- Extract concrete signals first (quotes, facts, metrics), then synthesize into pains/goals/behaviors.
- Clearly mark each claim as evidence-based or assumption with confidence (`High|Med|Low`).
- Use bracketed source tags (for example: `[UR#3]`, `[GA]`, `[MD]`) wherever evidence is cited.
- Avoid demographic stereotyping; unsupported demographics must be `TBD` or explicit assumptions.
- Ensure behaviors are observable and distinct from goals.
- If `number_of_personas > 1`, output distinct personas.
- Output markdown only; no JSON, XML, or HTML.
- Keep each persona under 400 words unless `depth = deep`.

FORMAT
- Return one markdown code block per persona.
- Inside each code block, render exactly this structure:

```markdown
# Proto Persona: {{Alliterative Name}}

## Bio & Demographics
- Age: {{x-y}}, Location: {{region/city}}, Education: {{...}}
- Role/Status: {{job title or life stage}}
- Income/Spending Power: {{range or TBD}}
- Household/Partner Status: {{...}}
- Digital/Channel Habits: {{top channels/devices}}
- Leisure & Interests: {{...}}
- Notable Constraints: {{time, budget, compliance, accessibility}}

## Representative Quotes
- "{{quote}}" - [{{source tag}}]
- "{{quote}}" - [{{source tag}}]
- "{{quote}}" - [{{source tag}}]

## Pains
- {{pain statement}} [evidence|assumption, {{confidence}}, {{source|TBD}}]
- {{...}}

## What They're Trying to Accomplish (Behaviors & JTBD)
- {{job story or observed behavior}} [evidence|assumption, {{confidence}}, {{source|TBD}}]
- {{...}}

## Goals
- {{goal}} [evidence|assumption, {{confidence}}, {{source|TBD}}]
- {{...}}

## Attitudes & Influences
- **Decision-Making Authority:** {{buyer|user|champion|blocker|none}} [{{confidence}}]
- **Decision Influencers:** {{roles/peers/communities}} [{{confidence}}]
- **Beliefs & Attitudes:** {{heuristics, risk posture, trust signals}} [{{confidence}}]

## Purchasing & Adoption Signals (Optional)
- Triggers: {{events that start the search}}
- Selection Criteria: {{top 3 decision criteria}}
- Objections: {{anticipated blockers}}
- Success Metrics: {{how they judge value}}

## Accessibility & Inclusion (Optional)
- Considerations: {{access, language, bandwidth, cognitive load}}

## Evidence & Confidence Summary
- Evidence Sources: {{list with counts, e.g., UR:6, GA:1, MD:2}}
- Assumptions: {{key assumptions}}
- Overall Confidence: {{High|Med|Low}} - {{1-2 sentence rationale}}

## Probing Questions (Prioritized)
1. {{highest-value unknown}}
2. {{next unknown}}
3. {{next unknown}}
```

FAILURE
- Output is not markdown code block(s), or required persona section headings are missing.
- `number_of_personas > 1` is requested but personas are not distinct or separated.
- Quotes/sources do not support key pains, goals, or JTBD claims.
- Claims are untagged (missing evidence/assumption + confidence + source markers).
- `TBD`/low-confidence gaps are not reflected in prioritized probing questions.
- Content exceeds 400 words per persona when `depth` is not `deep`.
- Output includes JSON/XML/HTML or generic filler not grounded in provided inputs.

## Extended Reference

Load `references/extended-reference.md` when the request mentions `user personas`, `proto persona`, `persona from research`, `segment profiles`. Use this reference material to sharpen this Productize skill.
