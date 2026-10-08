---
description: Run the full skill improvement cycle (diagnose → research → fix → validate) on a specific skill
argument-hint: "<skill-name> [--diagnose-only]"
---

# Improve Skill

Run the complete improvement cycle on a skill that failed or scored low in evaluation.

Initial request: $ARGUMENTS

## Phase 1: Locate and Assess

**Goal**: Find the skill, its eval results, and establish the baseline.

**Actions**:
1. Parse `$ARGUMENTS` for the skill name. If empty, ask user which skill to improve.
2. **Validate the skill name exists** before proceeding:
   <!-- Security: validate skill name against the skills directory to prevent
        path traversal attacks (e.g. "../../.ssh/config" as a skill name). -->
   - List the contents of the `skills/` directory.
   - Confirm the parsed skill name matches an existing subdirectory exactly.
   - If the name does not match any skill directory, **stop and report an error**:
     "Skill '{name}' not found. Available skills: {list}". Do NOT attempt to
     read or open paths for unrecognized skill names.
3. Read the skill's `SKILL.md` from the validated skills directory.
3. Look for evaluation results in `results/` — find the most recent `effectiveness-*.json` file.
4. Run Tier 1 validation to get current lint + score baseline:
   ```bash
   python scripts/lint-skills.py
   python scripts/score-skills.py
   ```
5. Summarize: current score, pass/fail status, and any prior improvement docs (`results/improve-{skill}*.md`).

---

## Phase 2: Diagnose

**Goal**: Extract exactly why the skill is underperforming.

**Actions**:
1. Parse the eval results JSON for this skill's judge reasoning.
2. Classify the failure:
   - **Inaccuracy**: Skill states something wrong (HIGH priority — fix immediately)
   - **Missing content**: Judge expected specific detail that isn't present (HIGH priority)
   - **Insufficient depth**: Content exists but is too terse (MEDIUM priority)
   - **Poor examples**: Code examples don't demonstrate the asked concept (MEDIUM priority)
3. Identify the specific lines/sections of SKILL.md that need changes.
4. Write a diagnosis summary. If `--diagnose-only` was passed, stop here and report.

---

## Phase 3: Research

**Goal**: Verify facts before editing. Never add content without checking official sources.

**Actions**:
1. For each diagnosed issue, identify the authoritative source:
   - Programming languages → official docs (go.dev, doc.rust-lang.org, etc.)
   - Frameworks/tools → official API docs, changelogs
   - Cloud services → provider documentation
2. Fetch the relevant pages using `web_fetch` or Context7.
3. Extract the specific facts, syntax, or API shapes needed.
4. Cross-reference against what the skill currently says — note any inaccuracies.
5. Save research notes to `results/research-{skill}-{topic}.md` for future reference.

---

## Phase 4: Fix

**Goal**: Make surgical, minimal edits to SKILL.md that address the diagnosed issues.

**Actions**:
1. Apply edits using the `edit` tool — change only what the diagnosis identified.
2. Follow these rules:
   - **Add missing content** near related existing content, not at the end.
   - **Replace inaccurate content** with researched correct content.
   - **Expand terse sections** with concrete examples from research.
   - **Keep the skill's existing structure** — don't reorganize unless necessary.
   - **Preserve all working content** — only change what's broken.
3. Ensure code examples are:
   - Complete and runnable (not fragments)
   - Annotated with comments explaining key points
   - Using the latest stable API/syntax from research

---

## Phase 5: Validate

**Goal**: Confirm the fix didn't break anything and improved quality.

**Actions**:
1. Run Tier 1 validation:
   ```bash
   python scripts/lint-skills.py
   python scripts/score-skills.py
   ```
2. Compare scores to Phase 1 baseline.
3. Verify: lint still passes, score maintained or improved.
4. Check trigger coverage — ensure the skill's test queries still match:
   ```bash
   python scripts/trigger-coverage.py
   ```
5. Report the before/after comparison.

---

## Phase 6: Document and Commit

**Goal**: Record what was done for future reference.

**Actions**:
1. Save improvement notes to `results/improve-{skill}-v{N}.md` (increment version from prior docs).
2. Stage and commit with a descriptive message:
   ```
   fix: improve {skill} skill — {brief description of what changed}
   ```
3. Summarize the cycle: diagnosis → research sources → edits made → validation results.

## CI/CD Alternative: Agentic Workflows

This improvement cycle also runs autonomously via GitHub Agentic Workflows:

- **`skill-improver` workflow**: Triggered by issues labeled `skill-improvement` or via manual dispatch.
  Runs the same diagnose → research → fix → validate cycle and creates a PR with the changes.
- **`skill-eval-orchestrator` workflow**: Evaluates all 25 skills weekly and dispatches `skill-improver`
  workers for any below threshold (80% lint, 85 score).
- **`gepa-optimizer` workflow**: For stubborn skills — uses evolutionary search with LLM-guided mutation
  to evolve the SKILL.md through multiple generations until it outscores the baseline.

```bash
gh aw run skill-improver -- --skill_name golang --threshold_score 85
gh aw run gepa-optimizer -- --skill_name golang --generations 5
```

## Success Criteria

- [ ] Skill passes lint (structural)
- [ ] Skill score ≥ 90/100
- [ ] All trigger coverage queries still match
- [ ] Edits are minimal and surgical
- [ ] Research sources are documented
- [ ] Changes committed with descriptive message
