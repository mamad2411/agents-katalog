---
name: authoring
description: Draft, review, evaluate, and improve SKILL.md files using a compiled knowledge base of best practices and anti-patterns. Use when writing a new skill, reviewing an existing one, measuring skill behavior, or debugging why a skill does not trigger.
---

# Skill Authoring

A meta-skill that queries the Skill Factory wiki to help you write better SKILL.md files.

## When to use

- Writing a new skill from scratch (idea or rough draft)
- Reviewing an existing skill for quality
- Improving a skill's description (most common failure point)
- Adapting a skill for a different host (Cursor, Codex, Claude Code)
- Debugging why a skill doesn't trigger
- Proving whether a skill improves outcomes over the no-skill baseline
- Deciding whether a capability skill can be retired

## Workflow

### Step 1: Intake

Accept one of:
- A draft SKILL.md (read the file)
- A plain-English description of what the skill should do
- An existing skill directory to review

If no input provided, ask: "What should this skill do? Describe in 1-2 sentences."

### Step 2: Load the wiki index

Read the wiki index to understand what knowledge is available. All paths below are relative to the skill-factory root directory.

Read the file `wiki/INDEX.md`.

This is the master table of contents with one-line summaries. Use it to pick which articles to read next.

### Step 3: Targeted retrieval

Based on the task, read the most relevant wiki articles. Do NOT read all of them. Pick 3-5:

**Always read for any task:**
- `wiki/research/anatomy-of-a-good-skill.md` (the quality checklist)
- `wiki/concepts/description-writing.md` (most common failure point)

**Read if writing from scratch:**
- `wiki/concepts/progressive-disclosure.md`
- `wiki/concepts/naming-conventions.md`
- `wiki/concepts/skill-discovery.md`

**Read if reviewing:**
- `wiki/research/anti-patterns.md`
- `wiki/concepts/token-budget.md`

**Read if the skill has scripts:**
- `wiki/concepts/error-handling-in-scripts.md`
- `wiki/concepts/validation-loops.md`

**Read if multi-host:**
- `wiki/concepts/host-compatibility.md`
- `wiki/research/host-differences.md`

**Read if the skill has complex workflows:**
- `wiki/concepts/checklist-workflows.md`
- `wiki/concepts/plan-validate-execute.md`
- `wiki/concepts/template-patterns.md`

**Always read before calling a skill behaviorally validated:**
- `wiki/concepts/skill-evaluations.md`
- `wiki/concepts/evidence-lifecycle.md`
- `evals/README.md`

### Step 3a: Review adopted source boundaries

When adapting external material, read `wiki/concepts/skill-supply-chain.md`.
Pin the source revision and sampled paths, check the applicable license, and
inspect scripts/hooks as well as prose. A repository HEAD change is a review
trigger; a whole-package fingerprint detects changes outside SKILL.md.

For a skill used in a large catalog, read
`wiki/concepts/retrieval-and-interference.md`. Keep ranking, actual activation,
and task outcomes separate. Do not add source setup instructions to the active
host without authorization.

### Step 4: Gap analysis

Compare the draft against the quality spec. Read the file `SKILL_SPEC.md`.

Check each of these (in order of importance):

1. **Description quality** -- Does it have a WHAT verb and a WHEN trigger? Third person? Under 1024 chars? Specific keywords?
2. **Name quality** -- Lowercase, hyphens, matches directory, not vague?
3. **Body length** -- Under 500 lines? If over, should it use progressive disclosure?
4. **Anti-patterns** -- Read `wiki/research/anti-patterns.md` and check against each one
5. **Content necessity** -- Is everything in the body something the agent doesn't already know?
6. **Examples** -- Does it include concrete input/output examples?
7. **Consistency** -- Consistent terminology throughout?
8. **Output format** -- If the skill produces output, is the format specified?
9. **Routing evidence** -- Are there natural positive and adjacent negative prompts?
10. **Outcome evidence** -- Does an isolated, repeated skill-versus-baseline eval show a useful delta?
11. **No-ops** -- Can generic directives be deleted without reducing eval performance?
12. **Pointers** -- Does each disclosed reference name its distinct trigger branch? Keep shared invariants inline and branch-specific detail behind an explicit pointer.
13. **Execution contract** -- If delegation is part of the authorized workflow, name foreground/background behavior, deadline, result schema, failure handling, and mutation owner for the actual host.

### Step 5: Draft or rewrite

If writing from scratch:
1. Start with the frontmatter (name + description first, get those right)
2. Write a concise overview (2-4 sentences)
3. Write "When to use" triggers (bullet points)
4. Write the main workflow (numbered steps)
5. Add examples (input/output pairs)
6. Check line count -- split to reference files if over 500

If reviewing/improving:
1. List every issue found in Step 4
2. For each issue, show the current text and the proposed fix
3. Apply all fixes
4. Verify the result

### Step 6: Validate

Run the automated validator:

```
bun run scripts/validate-skill.ts <path-to-skill-directory>
```

If it fails, fix the issues and re-run until it passes.

### Step 7: Quality examples

If helpful, read exemplary skills for inspiration. List the files in `wiki/examples/good/` and read the one most similar to the skill being authored.

### Step 8: Behavioral evaluation

Do not equate Step 6's static validator with behavioral proof.

1. Classify the skill as capability or preference, and model-triggered or user-invoked.
2. Create 10-20 cases with positive triggers, adjacent negative controls, functional outcomes, and known failures.
3. Prefer deterministic checks and privacy-safe real traces.
4. Separate development and selection cases from an untouched final holdout. A set used to pick the best description is validation, even if upstream calls it test. Freeze thresholds, model/CLI identity, and evaluator/suite/skill/adapter fingerprints.
5. Run the same model and harness with zero or one target skill in clean, host-isolated workspaces for 3-6 trials.
6. Checkpoint normalized records, exclude raw trajectories/credentials, and clean disposable temp/auth state.
7. Report trigger accuracy, skill and baseline outcome pass rates, delta, reliability, and exact evidence identity. Missing activation telemetry is unknown, not a successful negative control. Exclude eval answers and grader assets from agent-visible skill packages.
8. Keep failed or diagnostic evidence without weakening gates or mixing incompatible runs.
9. If a real isolated adapter is unavailable, label behavioral evaluation blocked; do not call the skill validated.

Use `evals/README.md` and run:

```bash
bun run scripts/evaluate-skill.ts evals/<suite>.json
```

### Step 9: File insights back

If this session produced useful observations about skill authoring (a new anti-pattern, a useful pattern, a host-specific gotcha), create a new file at `wiki/queries/observation-YYYYMMDD-TOPIC.md` with this structure:

```markdown
# Observation: [TITLE]
Date: [today's date]
Context: [what skill was being authored]

## Finding
[what was discovered]

## Recommendation
[how to apply this in future skills]
```

### Step 10: Output

Deliver:
1. The final SKILL.md (complete and structurally validated)
2. A summary of changes made (if reviewing)
3. Validation results (should be passing)
4. Behavioral eval results, or an explicit blocked/not-run label
5. Durable paths for the skill, references, eval definition, checkpoint/report, and any diagnostic evidence

## Key principles (from the wiki)

- **Description is the #1 failure point.** Get the WHAT verb + WHEN trigger right before anything else.
- **Concise beats thorough.** Only include what the agent doesn't already know.
- **Defaults over menus.** Pick one tool/approach, mention alternatives as escape hatch.
- **Procedures over declarations.** Teach approach, not specific answers.
- **Test against real tasks.** A skill that doesn't improve on the baseline isn't needed.
- **Evaluate outcomes, not paths.** Preserve valid agent freedom while checking the final state and safety constraints.
- **Retire with evidence.** Remove a capability skill when the repeated no-skill baseline catches up, but keep its eval suite.
- **Evidence has distinct homes.** Active procedure, historical context, eval definitions, checkpoints, reports, and production proof are not interchangeable.
- **Failed evals are data.** Retain them, fix named cases, and rerun under a new fingerprint without moving the gate.
- **Progressive disclosure.** Keep SKILL.md under 500 lines. Split details into reference files.
- **Gotchas are gold.** Environment-specific facts that defy assumptions are the highest-value content.

## Gotchas

- Run repository-relative commands from the Skill Factory root; an authoring
  target may live elsewhere, but the wiki, validator, and eval harness live here.
- Do not edit immutable `raw/` captures to make a conclusion read better. Update
  the canonical wiki or skill and preserve the source receipt.
- Host credentials may make a live eval possible without making its output safe
  to commit. Persist normalized evidence only and clean disposable auth state.
