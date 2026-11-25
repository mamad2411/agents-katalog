---
name: skill-creator-meta
version: 1.0.0
min_mindforge_version: 10.0.5
status: stable
triggers: create skill, skill creator, author skill, build skill, new skill, skill development, skill writing, skill testing, skill eval, meta-skill, skill optimization, skill iteration
compose: eval-harness
---

# Skill — Skill Creator Meta (Iterative Skill Authoring & Optimization)

## When this skill activates

When creating, authoring, testing, or optimizing MindForge skills. This is the
meta-skill that governs the lifecycle of all other skills — from initial interview
through eval-driven iteration to final registration. Use whenever a new skill needs
to be created, an existing skill needs optimization, or skill quality needs
systematic validation.

Core principle: **Eval-driven iteration** — skills are not "done" until they
demonstrably outperform the no-skill baseline on realistic test cases.

## Mandatory actions when this skill is active

### Before skill creation begins

1. **Interview for specification:**
   - What does this skill do? (one-sentence purpose)
   - When should it trigger? (specific user intents, not vague categories)
   - What is the output format? (file, inline response, structured data)
   - What edge cases exist? (partial matches, ambiguous triggers, conflicting skills)
   - What dependencies does it have? (other skills via compose, external tools, MCP servers)

2. **Validate against existing skills:**
   - Check MANIFEST.md for trigger overlap (jaccard > 0.3 = conflict)
   - Verify the skill covers a genuinely distinct capability
   - If overlap exists: either extend existing skill or document why separation is needed

3. **Define the skill schema constraints:**
   - SKILL.md must be under 500 lines (enforced)
   - YAML frontmatter must include: name, version, min_mindforge_version, status, triggers
   - Optional: compose (list of skill dependencies activated alongside)
   - Body must include: "When this skill activates", "Mandatory actions when this skill is active" (Before/During/After), "Self-check before task completion"

### During skill creation

**Phase 1 — Draft:**
- Write the SKILL.md following the schema exactly
- Triggers should be 8-15 phrases covering natural language variations
- Body should be action-oriented (imperative verbs, numbered steps)
- Include concrete examples where behavior might be ambiguous

**Phase 2 — Create test cases:**
```
.mindforge/evals/[skill-name]/
├── test-cases.json   # 2-3 realistic prompts complex enough to trigger loading
├── assertions.json   # objectively verifiable success criteria
└── benchmark.json    # aggregated results across iterations
```

Test case structure:
```json
{
  "test_cases": [
    {
      "id": "tc-001",
      "prompt": "realistic user prompt that should trigger this skill",
      "context": "any relevant project state",
      "expected_behaviors": ["specific", "verifiable", "outcomes"],
      "should_trigger": true
    }
  ]
}
```

**Phase 3 — Parallel evaluation:**
- Run each test case WITH the skill loaded (experimental condition)
- Run each test case WITHOUT the skill loaded (baseline condition)
- Compare outputs on defined assertions
- Skill must demonstrably improve output quality over baseline

**Phase 4 — Trigger optimization:**
- Generate 20 trigger evaluation queries:
  - 10 that SHOULD trigger the skill (true positives)
  - 10 that should NOT trigger (true negatives — related but distinct intents)
- Test trigger matching accuracy
- Iterate on name/description/triggers up to 5 times until precision > 90%

**Phase 5 — User review:**
- Present: skill draft, test case outputs, benchmark scores, trigger accuracy
- Collect feedback on: missing behaviors, unnecessary behaviors, trigger gaps
- Document feedback for improvement phase

**Phase 6 — Improvement:**
- Generalize from specific feedback to patterns
- Bundle repeated helper logic into `scripts/` directory within skill folder
- Rewrite sections that received negative feedback
- Ensure changes don't regress previously-passing test cases

**Phase 7 — Final iteration:**
- Rerun all test cases against improved skill
- Compare to previous iteration (must not regress)
- If regression: investigate, fix, rerun

### After skill creation

1. **Register in MANIFEST.md:**
   - Add entry with name, version, triggers, status
   - Verify no trigger conflicts with existing entries

2. **Verify file structure:**
   ```
   .mindforge/skills/[skill-name]/
   ├── SKILL.md          # the skill definition (required)
   ├── scripts/          # helper scripts if needed (optional)
   └── README.md         # usage examples (optional)
   ```

3. **Store eval artifacts:**
   ```
   .mindforge/evals/[skill-name]/
   ├── test-cases.json
   ├── assertions.json
   ├── benchmark.json
   └── iterations/       # historical results per iteration
   ```

4. **Final quality gate:**
   - Skill passes all test cases
   - Trigger precision > 90% on 20-query eval set
   - Skill outperforms baseline on all assertions
   - No trigger conflicts in MANIFEST.md
   - Under 500 lines

## Self-check before task completion

Before marking a skill creation task done:

- [ ] Did I interview for edge cases and dependencies?
- [ ] Did I create eval test cases (2-3 realistic prompts)?
- [ ] Did I run parallel comparison (with-skill vs baseline)?
- [ ] Did I optimize triggers with 20 evaluation queries (10 should, 10 should-not)?
- [ ] Did I iterate based on user feedback?
- [ ] Did I verify no trigger conflicts in MANIFEST.md?
- [ ] Is the skill under 500 lines?
- [ ] Does the final iteration outperform all previous iterations?
