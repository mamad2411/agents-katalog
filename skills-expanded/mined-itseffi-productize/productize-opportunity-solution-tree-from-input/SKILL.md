---
name: productize-opportunity-solution-tree-from-input
description: >-
  Opportunity Solution Tree from input. Use when the user needs a product workflow for user
  research related to opportunity solution tree from input. Trigger terms: user-research, ost,
  continuous-discovery.
---
<!-- AUTO-GENERATED from SKILL.md.tmpl - do not edit directly -->
<!-- Regenerate: npm run skills:generate -->

# Opportunity Solution Tree from input

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

- **Skill**: `opportunity-solution-tree-from-input`
- **Lifecycle**: Discover
- **Category**: Discovery
- **Primary artifact**: Opportunity Solution Tree from input research brief with evidence, insight clusters, assumptions, and next validation steps

Use this skill to run the Productize prompt contract for **Opportunity Solution Tree from input**.

## Instructions

1. Treat every `{{PLACEHOLDER}}` in the contract as an input to collect, infer, or mark as missing.
2. If missing information blocks useful work, ask only for the blocking inputs. If work can proceed, state assumptions explicitly.
3. Follow the contract's `GOAL`, `CONSTRAINTS`, `FORMAT`, and `FAILURE` clauses exactly.
4. Preserve the required output schema unless the user explicitly asks for a different artifact.
5. Keep claims grounded in the provided inputs and disclose gaps.

## Prompt Contract

INPUTS
<provided_inputs>
- `{{business_outcome}}`: The business outcome the OST must support.
- `{{journey_nodes_as_list}}`: Ordered list of journey moments (for example: `["Add to calendar", "Edit calendar", "Review calendar"]`).
- `{{interview_transcripts_or_story_snippets}}`: Interview material with speaker labels and timestamps when available.
- `{{constraints_or_principles}}` (optional): Guardrails, principles, or constraints to respect.
</provided_inputs>

GOAL
Transform interview evidence into a Teresa Torres-aligned Opportunity Solution Tree with distinct, properly nested opportunity nodes by journey moment.
Success metric:
- Output includes all required parts (A-E) with complete, internally consistent references.
- Opportunity nodes are user-need statements (not solutions), evidence-linked, and structurally valid.
- Prioritization is computable and traceable to interview evidence and `{{business_outcome}}`.

CONSTRAINTS
- Use only provided inputs; if data is missing or ambiguous, state assumptions in Part E.
- Phrase opportunities from the end-user perspective.
- Assign each opportunity to exactly one primary moment from `{{journey_nodes_as_list}}`; if needed, list secondary moments in `alt_moments`.
- Enforce sibling distinctness: if two siblings cannot be pursued independently, merge or reframe.
- Enforce parent-child logic: solving a child must partially solve its parent.
- Remove generic parents that have only one specific child.
- Collapse duplicates into the clearest phrasing and preserve traceability.
- Keep opportunities specific when supported by quotes; keep general opportunities only when they organize multiple specific children.
- Include only opportunity nodes in the OST (no solutions).
- Preserve short supporting quotes and avoid introducing new facts not present in inputs.
- Use stable IDs and ensure all references resolve (`parent_id`, `duplicates_of`, `traceability`).

FORMAT
Return all sections below in this exact order.

Part A - Opportunity Inventory (Markdown Table)
- Include both parent and leaf opportunities.
- Use exactly these columns:
`| id | moment | opportunity_reframed (user-need) | parent_id | duplicates_of | representative_quotes | frequency_count | confidence (low/med/high) | alt_moments | notes/reframe_rationale |`
- `duplicates_of` is blank unless collapsed into another ID.

Part B - Structured OST (Strict JSON in `<ost_json>` tags)
- Output must be wrapped exactly as:
`<ost_json>`
`{ ... }`
`</ost_json>`
- JSON schema:
```json
{
  "outcome": "{{business_outcome}}",
  "moments": [
    {
      "moment": "<journey moment>",
      "tree": [
        {
          "id": "A0",
          "title": "<user need>",
          "type": "opportunity",
          "children": []
        }
      ]
    }
  ],
  "traceability": {
    "A0": {
      "quotes": ["..."],
      "frequency_count": 1,
      "confidence": "low"
    }
  }
}
```
- Every node must include `id`, `title`, `type`, `children`.
- `type` must always be `"opportunity"`.
- Top-level moments must come from `{{journey_nodes_as_list}}`.
- JSON must be valid and parseable.

Part C - Markdown Tree View (Human-readable)
- For each moment, render an indented opportunity tree:
`## <moment>`
`- <parent opportunity>`
`  - <child opportunity>`
`    - <grandchild opportunity>`
- Include opportunities only (no solutions).

Part D - Prioritized Leaf Backlog (Markdown Table)
- Include only leaf opportunities.
- Use exactly these columns:
`| id | moment | leaf_opportunity | impact (1-5) | frequency (1-5) | alignment_to_outcome (1-5) | priority_score | rationale |`
- Compute `priority_score = impact * frequency * alignment_to_outcome`.

Part E - Assumptions & Open Questions
- Include:
- Uncertainties in placement/reframing.
- Potential missing siblings to test in future interviews.
- Ambiguities or contradictory evidence in quotes.
- Any hypotheses not supported by current interview evidence.

FAILURE
- Any required part (A-E), required table column, or required JSON field is missing.
- JSON is malformed, non-parseable, or violates required schema/rules.
- Output includes solutions inside the OST opportunity tree.
- Opportunities are generic/overlapping and fail distinctness or parent-child logic.
- Claims are not traceable to interview evidence.
- IDs or references are inconsistent/unresolved.
- Priority scores are missing or incorrectly computed.
- Assumptions/ambiguities exist but are not explicitly listed in Part E.

## Extended Reference

Load `references/extended-reference.md` when the request mentions `opportunity solution tree`, `ost`, `continuous discovery`. Use this reference material to sharpen this Productize skill.
