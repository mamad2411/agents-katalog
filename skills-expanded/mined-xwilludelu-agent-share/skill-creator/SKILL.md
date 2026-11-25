---
name: skill-creator
description: "Author and evaluate skills end to end: capability/trigger design, scaffolding, validation, baselines, iteration, description optimization, and packaging. Use for explicit or implicit requests to create, review, improve, repair, or benchmark a skill. In managed .agent-share libraries, skill-manager owns writes, provenance, materialization, and final audit; this skill supplies the authoring/evaluation method."
---

# Skill Creator

End-to-end skill lifecycle: scaffold, write, validate, evaluate, iterate,
optimize triggering, and package. This skill wraps two sibling guides bundled
as relative symlinks — `openai-skill-creator/` for authoring and
`anthropic-skill-creator/` for evaluation and optimization — so their scripts
and references stay current. Drive both through this skill; never invoke either
directly.

## Produce portable skills

Resolve this `SKILL.md` through symlinks to its canonical path, then set
`<library-dir>` to the parent of its containing directory (where the sibling
`openai-skill-creator/` and `anthropic-skill-creator/` symlinks point). Confirm
both sibling directories exist before running commands. Never derive bundled
script paths from a lexical runtime symlink or the caller's project. Run
scripts with `python3` (or a verified Python 3 environment such as
`.venv/bin/python` when PyYAML is required).

Both bundled guides target a single vendor (Claude/Anthropic, Codex/OpenAI).
Strip that vendor bias from every skill you produce:

- Read product, agent, org, and model names (`Claude`, `Anthropic`, `Cowork`,
  `Claude.ai`, `Codex`, `OpenAI`, `GPT`) as generic terms ("the agent", "the
  platform", "the model"). Keep generated skill names, descriptions, and bodies
  vendor-neutral unless the skill genuinely targets that product.
- Treat `openai-skill-creator`'s "UI Metadata and Invocation Policy" section as
  Codex-specific reference material; pass `--interface` during scaffolding only
  when explicitly targeting OpenAI/Codex.
- Adapt environment-specific workflows (`Claude.ai`, `Cowork`, CLI-bound
  scripts) to live capabilities: run sequentially when independent subagents
  are unavailable, write static HTML or review inline without a browser or
  display, and apply description optimization manually when the required agent
  CLI is absent. Report reduced evidence whenever a fallback is used.

## Workflow

Start at the user's current stage; skip formal evaluation when the user wants
to iterate informally.

1. **Capture intent and concrete examples.** Define what the skill does, when
   it triggers, the output format, and how outputs are judged. Use assertions
   for objectively verifiable outputs; for subjective writing or design, use
   realistic cases, a predefined qualitative rubric or blind comparison, and
   user review instead of forced quantitative assertions. Extract existing
   workflows from the conversation first. See "Create or Update a Skill" in
   `openai-skill-creator/SKILL.md` and "Capture Intent" in
   `anthropic-skill-creator/SKILL.md`.
2. **Plan reusable contents** — scripts, references, assets — and choose
   degrees of freedom and progressive-disclosure layout. See "Anatomy of a
   Skill" and "Progressive Disclosure in Practice" in
   `openai-skill-creator/SKILL.md`.
3. **Scaffold:** `python3
   <library-dir>/openai-skill-creator/scripts/init_skill.py <name> --path <dir>
   [--resources scripts,references,assets]`. Omit `--interface` unless
   targeting OpenAI/Codex.
4. **Write SKILL.md.** The `description` is the trigger: state both what the
   skill does and when to use it, leaning slightly assertive to counter
   under-triggering. Keep the body concise (<500 lines) and push details into
   `references/`. See `openai-skill-creator/SKILL.md` for anatomy and writing
   patterns.
5. **Validate.** In managed `.agent-share` libraries, run the `skill-manager`
   audit (using a PyYAML-enabled Python such as `.venv/bin/python`). For
   standalone skills, check against the
   [Agent Skills format](https://agentskills.io/specification). Test changed
   entry points when warranted.
6. **Evaluate.** Follow "Running and evaluating test cases" in
   `anthropic-skill-creator/SKILL.md`: write `evals/evals.json`, spawn
   with-skill and baseline runs in parallel when supported, and grade objective
   outputs against assertions (`anthropic-skill-creator/agents/grader.md`;
   schemas in `anthropic-skill-creator/references/schemas.md`). Aggregate via
   `(cd <library-dir>/anthropic-skill-creator && python3 -m
   scripts.aggregate_benchmark ...)`, launch
   `<library-dir>/anthropic-skill-creator/eval-viewer/generate_review.py` for
   user review before forming your own judgment, then read `feedback.json`.
7. **Improve and iterate.** Generalize from feedback rather than overfitting,
   keep instructions lean, explain the *why*, and bundle scripts that test runs
   repeatedly recreate. See "Improving the skill" in
   `anthropic-skill-creator/SKILL.md`. Re-run into a new iteration until the
   user is satisfied or progress stalls.
8. **Optimize description triggering.** Build ~20 realistic queries split
   between should-trigger and should-not-trigger (favor near-misses over
   obvious cases), hold out a test split, and select by held-out score.
   Automated: `(cd <library-dir>/anthropic-skill-creator && python3 -m
   scripts.run_loop ...)` when the agent CLI is available; otherwise run the
   same loop manually.
9. **Package:** `python3 <library-dir>/skill-creator/scripts/package_skill.py
   <skill-folder> [output-dir]` (with a PyYAML-enabled Python such as
   `.venv/bin/python`) when a `.skill` archive is requested. This wrapper
   enforces the shared `skill-manager` frontmatter rules (including boolean
   `disable-model-invocation`), delegates zip creation to
   `anthropic-skill-creator/scripts/package_skill.py`, and rejects output
   directories inside the bundled creators.

## Routing

| Need | Go to |
|---|---|
| Scaffold, structure, naming, degrees of freedom | `openai-skill-creator/` |
| Test cases, grading, benchmarks, viewer, blind compare, description optimization | `anthropic-skill-creator/` |
| Packaging (with shared library validation) | `scripts/package_skill.py` |
| Progressive disclosure, anatomy, description-as-trigger | either (`openai-skill-creator/` is canonical) |
