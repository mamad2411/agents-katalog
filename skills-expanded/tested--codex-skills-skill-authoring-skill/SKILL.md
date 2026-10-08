---
name: skill-authoring
description: Create, revise, route, validate, or audit tested repo-local skills as a progressive-disclosure engineering handbook. Use when changing AGENTS.md or .codex/skills, adding durable tested contracts, reorganizing routes, synchronizing skill UI metadata, removing placeholders, or checking reachability and routing integrity.
---

# Skill Authoring

## Inherit the default workflow

Read and apply the installed `$skill-creator` skill completely before changing
a repo-local skill. Apply its naming, initialization, frontmatter, imperative
writing, progressive disclosure, resource selection, UI metadata, validation,
and forward-testing guidance.

Do not initialize an existing skill again. For a new skill, use the installed
initializer once, then replace every placeholder and remove every unused
example or resource directory. Keep repository rules additive; do not weaken
the default skill requirements.

## Author concise engineering contracts

Keep each `SKILL.md` focused on durable, non-obvious knowledge another agent
needs to implement or verify behavior:

- responsibility and exclusions;
- inputs, outputs, state, and lifecycle;
- invariants, ordering, bounds, and decision rules;
- errors, cancellation, partial evidence, cleanup, and recovery;
- security and compatibility boundaries;
- language-neutral acceptance scenarios.

Use imperative or infinitive wording. Keep source-symbol inventories and
session transcripts out of the contract. Prefer observable behavior and
package ownership; mention an algorithm only when compatibility or correctness
depends on it.

Keep detailed variants in a directly linked `references` file only when they
would bloat the body. Keep references one level from `SKILL.md`, explain exactly
when to read each one, and do not duplicate its content in the body. Add scripts
only for repeated deterministic work and test every added script. Add assets
only when they are consumed in repository output.

## Maintain skill metadata

Use a sibling directory named exactly `.codex/skills/<skill-name>`. Use
lowercase letters, digits, and hyphens and keep the name under 64 characters.

Put only `name` and `description` in `SKILL.md` frontmatter. Make the
description state both the capability and concrete trigger conditions because
it controls discovery before the body loads.

Keep `agents/openai.yaml` synchronized with the finished skill:

- derive a human-facing display name from the skill;
- keep the short description concise and aligned with the responsibility;
- make the default prompt explicitly invoke `$<skill-name>` for a representative
  task;
- include no optional interface fields unless they are deliberately supplied.

Regenerate metadata with the installed `$skill-creator` generator when it is
stale. Do not hand-maintain divergent descriptions.

## Build forward-only actionable routing

Store every discoverable skill as a direct sibling under `.codex/skills`.
Express hierarchy only with an actionable Markdown sentence that:

1. starts with the imperative `Use`;
2. links the exact skill name to its relative `SKILL.md`;
3. contains `to` followed by a concrete task or trigger;
4. appears in the narrowest router able to make that decision.

Treat only that complete sentence form as hierarchy. A supporting prose link is
not a route. Do not add parent metadata, ancestry sections, routing-only
backlinks, or a leaf routing section with no delegates.

Keep this canonical topology:

- route only `implementation-architecture`, `skill-authoring`, and
  `source-code-management` from `AGENTS.md`;
- route `coding-directives`, `implementation-test-pipeline`,
  `implementation-coverage`, `implementation-reporting`, and
  `scripts-and-automation` from `implementation-architecture`;
- keep those specialized skills as leaves unless a future cohesive domain
  justifies a forward child.

Ensure every route points forward, every target exists, every action is
selective, every sibling is reachable from `AGENTS.md`, and no cycle exists.
Put shared invariants in the router and specialized behavior in its leaf rather
than copying the same contract into both.

## Revision workflow

1. Read `AGENTS.md`, inventory every sibling skill and `agents/openai.yaml`, and
   follow all current actionable routes.
2. Read the source, tests, raw logs, or user correction that establishes the
   durable behavior. Distinguish required behavior from implementation status.
3. Select the narrowest existing owner. Add a new skill only when loading the
   concern independently improves cohesion or context use.
4. Edit the contract in imperative form. Mark unimplemented or partial behavior
   honestly instead of describing intended automation as present.
5. Add or change one forward actionable route at the narrowest dispatch point.
6. Refresh UI metadata when responsibility or triggering changed.
7. Remove all initializer instructions, unfinished markers, example placeholders,
   unused resources, duplicate guidance, and routing-only backlinks.
8. Run `make skills-check`. Treat this dependency-free repository validator as
   the CI authority for frontmatter, UI metadata, placeholders, exact route
   targets, canonical topology, reachability, and cycle detection. When the
   installed `quick_validate.py` and its YAML dependency are available, run it
   against every changed skill as a supplementary compatibility check.
9. Review the validator's route inventory starting at `AGENTS.md`; resolve any
   missing target, ambiguous action, topology mismatch, cycle, or unreachable
   sibling instead of weakening the check.
10. Report the repository-relative routing chain and every validator result.

## Validation expectations

Treat frontmatter validation as the minimum, not the complete audit. Also
confirm:

- directory and frontmatter names match;
- frontmatter contains only the two allowed fields;
- descriptions contain concrete triggers;
- bodies are imperative, concise, and free of placeholders;
- every `agents/openai.yaml` matches its skill;
- all sibling skills are reachable through the canonical forward graph;
- specialized implementation contracts retain raw-evidence, status,
  incompleteness, security, compatibility, determinism, and verification
  requirements relevant to their owner.

Keep `scripts/skillcheck` standard-library-only and test malformed metadata,
stale prompts, missing targets, cycles, unreachable skills, and unfinished
placeholders. Update its canonical topology expectation in the same change as
an intentional handbook route change.

Forward-test a complex or substantially revised skill with a fresh agent when
that can be done safely. Give it the skill path and a realistic task, not the
intended answer or prior diagnosis, then revise the skill if it cannot guide the
task without leaked context.
