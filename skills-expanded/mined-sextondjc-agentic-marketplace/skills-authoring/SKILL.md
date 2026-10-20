---
name: skills-authoring
description: Use when creating or updating skills and validating they are discoverable, specialized, and reusable.
---

# Skills Authoring

## Specialization

Author and maintain high-quality SKILL.md assets that are discoverable, concise, operationally clear, and mature enough for expert Copilot usage.

## L4 Copilot Target

Use this L4 target for expert-grade outcomes:

- Build a complete capability map: objective, boundaries, triggers, workflow, and done criteria must fully cover the real request shape.
- Require evidence-based decisions with explicit assumptions, trade-offs, and one final recommendation.
- Preserve deterministic execution by default; only allow bounded exploration with explicit closure.
- Ensure output quality is reusable across sessions without hidden context.

L4 is achieved only when all three dimensions pass:

- Maintenance dimension: source freshness and relevance are verified before content changes are finalized.
- Learning dimension: depth-calibrated topic decomposition is explicit and mapped to outcomes.
- Reasoning dimension: assumptions, trade-offs, blockers, and one recommendation are explicit and testable.

Copilot compatibility is mandatory for L4:

- `name` must be lowercase hyphenated and match the skill directory name.
- Keep `name` within 64 characters and `description` within 1024 characters.
- Use optional frontmatter fields (`argument-hint`, `user-invocable`, `disable-model-invocation`) only when the invocation model requires them.
- Reference in-skill resources with relative markdown links so progressive loading can discover them.

## Trigger Conditions

- A new skill is needed.
- An existing skill needs remediation.
- Skill quality must be validated before release.
- A skill must be upgraded to expert-level Copilot usability (L4 depth and reasoning quality).
- A skill has ambiguous trade-offs or hidden assumptions that reduce execution reliability.

## Inputs

- Target skill name and purpose.
- Trigger conditions and scope boundaries.
- Required references, scripts, or templates.
- Growth-governance baseline: reuse-before-create, delta-first edits, concise wording, and explicit auditability.
- Consumer context for Copilot usage (user intent, constraints, and expected artifacts).
- Known assumptions, risks, and options that affect recommendation quality.
- Evaluation date in ISO format (`YYYY-MM-DD`) for source freshness checks.
- Source catalog path when applicable (default: `./references/source-catalog.md`).
- Freshness threshold in days (default: 30).

## Required Outputs

- Updated SKILL.md with valid frontmatter.
- Clear trigger language and specialization boundaries.
- Canonical sections: Inputs, Required Outputs, Workflow.
- Registered references and catalog updates when needed.
- L4 coverage matrix that maps each requested outcome to a concrete skill section or explicit decision.
- Reasoning package: assumptions, trade-off summary, open blockers, and one recommended path.
- Pragmatic stop rule that defines when the authored skill is complete enough to execute safely.
- Determinism status: full coverage confirmation or a bounded exception record.
- Source-governance summary: relevance, authority, freshness, and actionability disposition for each active source.
- Source ledger with evaluated date, URL, relevance note, and resulting skill delta.
- Implementation-ready delta list for impacted skill files.
- Post-update validation checklist with pass/fail outcomes.

## Workflow

1. Run baseline validation and identify gaps.
2. Re-evaluate active sources for relevance, authority, freshness, and actionability.
3. Record source status updates and extract implementation deltas that affect the target skill.
4. Run a pre-authoring growth gate and record any exception before drafting: reuse-before-create, singular scope, concise delta-only edits, and deterministic verification outputs.
5. Draft minimal frontmatter and specialization-first content.
6. Build a depth-calibrated topic map (domain -> subdomain -> specialization) and prune branches that do not serve the target outcome.
7. Build an L4 coverage matrix: map requested outcomes to required sections, and identify gaps before drafting details.
8. Add canonical execution-context sections.
9. Evaluate assumptions and trade-offs; remove weak options and keep one clear recommendation.
10. Add references to improve reuse; a `references/` directory is not optional and required.
11. Validate deterministic completeness: required outputs and workflow must cover the intended scope without omission.
12. If exploration logic is required, keep it bounded with hypothesis, boundary, time-box, success criteria, and closure decision.
13. Run self-validation against the core rules, L4 target, source-governance summary, and reasoning package before finalizing.

## Core Rules

- Keep one objective per skill.
- Keep wording concise and non-redundant.
- Prefer reusable assets over inline duplication.
- Use lowercase hyphenated skill names.
- Default to deterministic behavior and explicit output contracts.
- Treat exploration as an explicit, rare exception pattern, not a default execution mode.
- Never create root-level folders in any workspace.
- Never create top-level reference folders; keep references under the owning asset path (for example `.github/skills/<skill>/references/`).
- **Skills MUST NOT reference, invoke, or delegate to other named skills within their guidance body.** All execution content must be entirely self-contained. Cross-referencing between skills is a SKR-M4 violation and a governance fail. If two skills genuinely require shared logic, introduce a dedicated orchestrator skill as the indirection layer rather than referencing from either skill.
- Prefer a canonical shared reference over repeating growth-policy text across multiple skill bodies.

## Done Criteria

- Frontmatter is valid and name matches folder.
- Trigger conditions are explicit and testable.
- Skill is self-contained and concise.
- Required outputs are explicit, deterministic, and complete for in-scope requests.
- L4 coverage matrix shows complete mapping of requested outcomes.
- Reasoning package is present with assumptions, trade-offs, blockers, and one recommendation.
- Active sources used by the skill are freshness-checked and have explicit status.
- Implementation deltas and post-update validation outcomes are captured.
- Source ledger entries are current for all active sources used in this pass.
- Review checks pass with no MUST failures.
