---
description: "Authoring and review contract for AI customization files, including agents, instructions, prompts, skills, hooks, and workspace guidance."
globs: "**/*.agent.md,**/*.agents.md,**/*.instructions.md,**/*.prompt.md,**/copilot-instructions.md,**/skills/**/SKILL.md,**/hooks/**/*.json,**/*.mdc,**/AGENTS.md,**/agents.md,**/.cursor/rules/**/*.mdc,**/.cursor/AGENTS.md,**/.cursor/skills/**/SKILL.md"
alwaysApply: false
---

# AI Customization Contract

Cursor counterpart of `.github/instructions/ai-customization.instructions.md`. Same enforceable contract; routing and workspace baseline differ by product as noted below.

## Dependencies

- Read the workspace baseline before creating or changing an AI customization file: `AGENTS.md` for Cursor guidance, or `copilot-instructions.md` for Copilot guidance.
- Read the applicable domain contracts before editing a file that they govern: `.cursor/rules/*.mdc` topic rules for Cursor, or `.github/instructions/*.instructions.md` for Copilot.
- Treat a missing required instruction, reference, or template as a blocker. Do not silently bypass it or invent a substitute.

## Scope and ownership

- Keep workspace-wide behavior in `AGENTS.md` (Cursor) or `copilot-instructions.md` (Copilot).
- Keep reusable authoring and review rules for AI customization files in this contract (`ai-customization.mdc` / `ai-customization.instructions.md`).
- Keep topic-specific implementation rules in the narrowest applicable file: Cursor `.mdc` rules under `.cursor/rules/`, Copilot `*.instructions.md` under `.github/instructions/`.
- Keep one canonical owner for each shared policy. Reference that owner instead of duplicating the policy in other files.
- Limit each file to the behavior implied by its name, description, and routing pattern.

## Metadata and routing

- Give every customization file the metadata required by its file type and product.
- Write `description` so the file's purpose and trigger conditions are discoverable.
- **Copilot instruction files** (`*.instructions.md`, `copilot-instructions.md`): use YAML frontmatter with `description` and `applyTo`. Use the narrowest `applyTo` pattern that covers the intended files without accidental matches.
- **Cursor rule files** (`.mdc`): use YAML frontmatter with `description`, `globs`, and `alwaysApply`. Prefer `alwaysApply: false` for topic-specific contracts; route them with the narrowest `globs` that match the governed paths. Keep always-on workspace behavior in `AGENTS.md`, not in topic `.mdc` files unless a file is explicitly designed as a broad entry contract.
- Add `argument-hint` when a prompt requires user-provided input.
- Check routing patterns for overlap with existing files before adding or changing them.
- Preserve technical literals exactly, including paths, commands, URLs, identifiers, configuration keys, and versions, unless they are demonstrably incorrect.

## Authoring rules

- Use direct, imperative language for mandatory behavior.
- Mark optional behavior explicitly as optional.
- Keep one enforceable behavior per rule or bullet.
- Split compound rules when they contain independent decisions or conditions.
- Keep each section focused on one purpose, with a heading that matches its contents.
- Put rules in the order the governed workflow encounters them.
- Keep instruction contracts product-agnostic and reusable across real projects.
  Never reference tutorial repos, sample module paths, learning-catalog numbers,
  or project-specific folders/networks from teaching material.
- Remove filler only when doing so preserves the rule's meaning and enforceability.
- Preserve existing behavior when improving wording unless the user explicitly approves a behavior change.
- Do not turn a style preference or optional rewrite into a defect, requirement, or safety rule.

## Duplication and conflict control

- Search for an existing rule before adding a new one.
- Add a rule only when it changes a default decision or closes a real gap.
- Do not restate the same policy as both a positive rule and its negative form.
- Resolve contradictions explicitly by rewriting the rule or defining precedence.
- When files disagree, identify the canonical owner and update references rather than silently choosing a winner.
- Search existing templates before creating a new template.
- Use references for required canonical content instead of copying large examples into multiple files.
- Keep review findings tied to concrete behavior, routing, enforceability, correctness, safety, duplication, contradiction, or material clarity.
- Do not report wording preferences, optional rewrites, or alternative styles as problems.

## Review and change safety

- Review the complete target file before proposing a change.
- Show proposed wording or behavior changes and wait for approval when the user requests review before editing.
- After an approved change, verify that the file's original meaning and governing behavior remain intact.
- Do not modify unrelated customization files or silently repair adjacent issues.
- Do not create, update, or delete a review ledger without explicit authorization.
- If a required dependency is missing, report the blocker and ask whether to create, restore, remove, or replace it. Do not add a workaround without approval.

## Agent-specific rules

- List only the tools the agent role actually requires.
- Include a `## Constraints` section in every custom agent file.
- Grant the `agent` tool only to orchestrator agents.
- Use the singular `.agent.md` suffix for discoverable custom agents.
- Write each agent `description` so the parent can route by intent; keep descriptions
  specific and non-overlapping with sibling agents.
- Use imperative MUST/DO NOT language for mandatory agent behavior. Do not use soft
  phrasing for safety, scope, or handoff rules.
- Orchestrator agents must classify user intent before delegating and must not expand
  into stages the user did not request without explicit confirmation.
- Orchestrator agents must pass a delegation charter on every subagent invoke: mode,
  in-scope/out-of-scope items, the task for that agent only, required artifacts, and a
  directive to return structured output without owning the user conversation.
- Subagent files must state that when invoked by a parent they return structured output
  only, stay in role, and do not start another agent's pipeline.
- Spec/interview agents must read the user prompt and mandatory domain instruction
  or rule contracts before asking questions, and must not re-ask decisions those sources already
  fix.
- Reviewer agents must require evidence for every finding (path, excerpt, verbatim
  instruction clause) and must list the instruction files opened before a clean pass.
- Reviewer agents must define severity (`blocker`|`major`|`minor`) and treat project
  non-negotiables and explicit instruction-clause breaches as `blocker`.
- Prefer a small Spring Boot workgroup: Orchestrator, Architect, Coder, and one Reviewer.
  Do not split review into multiple default agents unless a named constraint requires it.
  Cap automated fix loops at two Coder+Reviewer rounds so unresolved failures escalate to
  the user instead of thrashing. Frame that cap as quality process control, never as a
  reason to skip instruction obedience or ship approximate code.
- For Spring Boot agents, state that primary success is code matching the project's
  instruction contracts and the user's style. Token or loop reduction is only a
  consequence of a correct first pass—not a competing goal.
- Only the human user may override a mandatory instruction clause. When they explicitly
  request a conflict, agents must propose an ADR Instruction override for approval, then
  code and review against it—never invent an override and never hard-stop without that path.
- Coder and orchestrator agents must treat matching instruction contracts as binding
  law, not optional references, and must not report clean while unresolved blockers remain.
- Agents that consume Spring Boot contracts must resolve them from workspace
  `.cursor/rules/` (Cursor) or `.github/instructions/` (Copilot) first, else
  `~/.agents/instructions/` when that overlay is used.
- State each agent rule once. Approach = order of operations; Constraints = only rules
  the order does not already force. Prefer checklists over essays.
- Cite instruction section names the agent must open; do not paste those instruction
  bodies into the agent file.
- Keep evidence and clean-pass requirements in `## Output Format` when that already
  enforces them; do not also mirror them as Constraints.

## References

- Use the workspace `AGENTS.md` (Cursor) or `copilot-instructions.md` (Copilot) for universal interaction, safety, and workflow rules.
- Use the `review-ai-customization-files` skill's ledger and convergence rules when auditing customization files across multiple runs.
