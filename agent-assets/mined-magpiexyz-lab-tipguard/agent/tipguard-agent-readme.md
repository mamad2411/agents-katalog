# Agent Taxonomy

26 sub-agents in `.claude/agents/`. Each agent is a specialized subprocess with constrained tools, model tier, and scope.

Categories are mutually exclusive -- each agent appears in exactly one category, grouped by the lifecycle skill that invokes it.

## Categories

### 1. Scaffold agents (8) -- /bootstrap

Edit/Write, invoked during /bootstrap to build initial project structure. Each handles a distinct build phase with different inputs/outputs.

`scaffold-setup`, `scaffold-init`, `scaffold-images`, `scaffold-libs`, `scaffold-pages`, `scaffold-landing`, `scaffold-wire`, `scaffold-externals`

scaffold-pages vs scaffold-landing stay separate: different self-check rubrics (utility 6-dim vs persuasion 7-dim), different data inputs (image-manifest.json vs messaging.md), different write territories. scaffold-externals is read-only (classifies dependencies, doesn't create them).

### 2. Implementation agents (2) -- /change

Edit/Write with worktree isolation. Shared TDD logic extracted to `procedures/tdd-cycle.md`.

`implementer`, `visual-implementer`

Kept separate because: (a) different output contracts (visual-implementer has DESIGN field), (b) 6+ consuming files reference both names in hooks/globs/traces, (c) `skills: [frontend-design]` is a declarative frontmatter field with no runtime conditional loading.

### 3. Verify agents (14) -- /verify

Invoked across /verify phases. Sub-grouped by phase:

**Quality scanners** (5) -- Phase 1 parallel, read-only:
`accessibility-scanner`, `behavior-verifier`, `build-info-collector`, `performance-reporter`, `spec-reviewer`

Each has deeply specialized instructions (WCAG rules, golden path steps, git diff extraction, Core Web Vitals thresholds, experiment.yaml fidelity). Different model tiers: opus for behavioral reasoning (behavior-verifier), sonnet for checklist verification (spec-reviewer), haiku for data extraction (build-info-collector).

**Design & UX** (4) -- Phase 3, serial execution:
`design-critic` (edit-capable), `design-consistency-checker` (read-only), `ux-journeyer` (edit-capable), `quality-fixer` (edit-capable)

Different scopes: per-page visual, cross-page consistency, end-to-end flow. Edit-capable agents run serially to prevent git conflicts.

**Security** (3) -- Phase 1 scan + Phase 4 fix:
`security-attacker` (opus, read-only), `security-defender` (sonnet, read-only), `security-fixer` (opus, edit-capable)

Attacker vs defender use fundamentally different cognitive frames (adversary vs compliance) AND different model tiers (opus for creative exploit paths, sonnet for binary checklist). Fixer consumes both outputs.

**Observation & learning** (2) -- Phase 6 + Phase 8:
`observer` (read-only), `pattern-classifier` (edit-capable)

observer attributes build-fix root causes to template files and files GitHub issues. pattern-classifier writes fix patterns to stack files or memory -- it has Write/Edit tools because its job is knowledge persistence.

### 4. Cross-skill agents (2)

`gate-keeper` (read-only, sonnet) -- invoked by /change (G1-G6 gates) and /bootstrap (BG1-BG4 gates) for process compliance enforcement.

`provision-scanner` (read-only, sonnet) -- invoked by /deploy and /teardown to verify cloud resource state.

## Description Convention

- **Creative agents** (6): "World-champion" priming preserved in description field -- identity framing improves subjective creative output. Agents: design-critic, scaffold-images, scaffold-init, scaffold-landing, scaffold-pages, pattern-classifier.
- **Functional agents** (19): `<What it does> -- <Scope constraint>` template.

## Files that reference agent names

Update these if renaming an agent:

- `.claude/procedures/change-feature.md` -- implementer/visual-implementer dispatch
- `.claude/procedures/tdd-task-generation.md` -- agent type table
- `.claude/procedures/worktree-merge-verification.md` -- merge logic
- `.claude/skills/change/state-10-implement.md` -- trace globs, gate checks
- `.claude/patterns/state-registry.json` -- VERIFY commands
- `.claude/hooks/skill-agent-gate.sh` -- manifest-driven agent checks
- `.claude/hooks/artifact-integrity-gate.sh` -- scaffold_prefixes list
- `.claude/hooks/skill-commit-gate.sh` -- commit convention gates
