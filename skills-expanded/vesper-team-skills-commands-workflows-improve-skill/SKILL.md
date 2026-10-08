---
name: workflows:improve-skill
description: Analyze, score, and improve an existing SKILL.md using parallel audit agents and a weighted quality rubric
argument-hint: "[skill name, skill path, or empty for interactive selection]"
---

# Improve Skill Command

<command_purpose> Analyze, score, and improve existing skills using parallel audit agents and a weighted quality rubric. Combines the capabilities of audit-skill, verify-skill, heal-skill, and skill-enricher into a single orchestrated workflow with before/after measurement. </command_purpose>

## Introduction

<role>Skill Quality Engineer with expertise in SKILL.md structure, progressive disclosure, content accuracy, and agent-facing documentation standards</role>

## Prerequisites

<requirements>
- At least one skill installed in `~/.claude/skills/`
- For freshness verification: internet access (WebSearch)
- Reference rubric: `~/.claude/skills/workflow-improve-skill/references/quality-rubric.md`
- Reference categories: `~/.claude/skills/workflow-improve-skill/references/improvement-categories.md`
</requirements>

## Phase 1: Target Discovery & Baseline

<review_target> #$ARGUMENTS </review_target>

<task_list>

- [ ] Parse `$ARGUMENTS` to determine target skill:
  - **Skill name**: Look in `~/.claude/skills/{name}/SKILL.md`
  - **Skill path**: Use the provided path directly
  - **Empty**: Enumerate `~/.claude/skills/` and present numbered list for selection
- [ ] Read the complete skill structure:
  ```
  ~/.claude/skills/{skill-name}/
  ├── SKILL.md
  ├── references/*.md
  ├── workflows/*.md
  ├── scripts/*
  ├── assets/*
  └── templates/*
  ```
- [ ] Count baseline lines per file using `wc -l`
- [ ] Record full content snapshot for before/after comparison
- [ ] Store baseline data for Phase 7

</task_list>

**Output:** Confirm target skill, list files found, report total lines.

## Phase 2: Parallel Audit Agents

<critical_requirement> Launch ALL 6 agents simultaneously using the Task tool. Each agent reviews independently and returns findings with severity (Critical/Important/Minor) and specific quotes + suggested fixes. </critical_requirement>

<parallel_tasks>

Run ALL 6 agents at the same time:

### Agent 1: Structure Auditor

```
Task(
  subagent_type: "general-purpose",
  prompt: """
## Assignment: Structure Audit

Read the skill at ~/.claude/skills/{skill-name}/ and audit its structural conformance.

### Checklist:
**YAML Frontmatter:**
- [ ] Has `name:` field (lowercase-with-hyphens, matches directory name)
- [ ] Has `description:` field (third person, says what + when to use)
- [ ] Description includes trigger phrases
- [ ] `alwaysAllow:` is appropriate (not overly permissive)

**File Organization:**
- [ ] SKILL.md under 500 lines
- [ ] All files referenced in SKILL.md exist on disk
- [ ] No orphaned files (files that exist but aren't referenced)
- [ ] references/ contains domain knowledge (not procedures)
- [ ] workflows/ contains procedures (not domain knowledge)
- [ ] scripts/ contains executable code (correct shebangs, chmod +x)

**Required Sections:**
- [ ] Has objective or essential_principles
- [ ] Has success_criteria
- [ ] Has process or routing table (for complex skills)
- [ ] XML tags properly closed (if using XML structure)

### Output Format:
For each finding:
- **Severity**: Critical / Important / Minor
- **Category**: frontmatter / file-organization / required-sections / xml-structure
- **Quote**: Exact text from the file showing the issue
- **Location**: File path and line range
- **Suggestion**: Specific fix

Return ALL findings as a structured list.
""",
  description: "Agent 1: Structure Audit"
)
```

### Agent 2: Content Quality Reviewer

```
Task(
  subagent_type: "general-purpose",
  prompt: """
## Assignment: Content Quality Review

Read the skill at ~/.claude/skills/{skill-name}/ and review content quality.

### Evaluate:
**Clarity:**
- [ ] Instructions are specific, not vague ("configure the database" vs "run `createdb myapp_dev`")
- [ ] Each step has a verifiable outcome
- [ ] Technical terms are used consistently throughout
- [ ] No ambiguous pronouns or references

**Actionability:**
- [ ] Steps are concrete and executable
- [ ] Commands can be copy-pasted
- [ ] File paths are real (not placeholders like `/path/to/`)
- [ ] Success criteria are testable (not "user is satisfied")

**Examples:**
- [ ] Examples use realistic data (not foo/bar/baz)
- [ ] Examples show common use cases
- [ ] Examples include expected output
- [ ] Error handling examples present

**Conciseness:**
- [ ] No redundant content across files
- [ ] No filler paragraphs or obvious statements
- [ ] Each sentence adds unique value
- [ ] No unnecessarily verbose explanations

### Output Format:
For each finding:
- **Severity**: Critical / Important / Minor
- **Category**: clarity / actionability / examples / conciseness
- **Quote**: Exact text showing the issue
- **Location**: File path and line range
- **Suggestion**: Rewritten text or specific improvement

Return ALL findings as a structured list.
""",
  description: "Agent 2: Content Quality"
)
```

### Agent 3: Freshness Verifier

```
Task(
  subagent_type: "general-purpose",
  prompt: """
## Assignment: Freshness Verification

Read the skill at ~/.claude/skills/{skill-name}/ and verify external claims are still accurate.

### Process:
1. **Categorize** the skill's primary dependency type:
   | Type | Examples | Verification |
   |------|----------|-------------|
   | API/Service | Stripe, GitHub API | WebSearch for changes |
   | CLI Tools | xcodebuild, npm | Check documented flags |
   | Framework | SwiftUI, React | WebSearch for breaking changes |
   | Integration | OAuth flows | WebSearch for protocol changes |
   | Pure Process | Workflow patterns | No external deps |

2. **Extract verifiable claims**:
   - CLI commands and flags
   - API endpoints and parameters
   - Framework patterns and APIs
   - Version-specific features
   - URLs and links

3. **Verify each claim** using WebSearch:
   - Search for "{tool/service} breaking changes 2025 2026"
   - Search for "{tool/service} deprecated API"
   - Check if documented patterns are still current

4. **Flag deprecated patterns** with current alternatives

### Output Format:
For each finding:
- **Severity**: Critical (broken/removed) / Important (deprecated) / Minor (newer alternative exists)
- **Category**: api-change / cli-change / framework-change / deprecated-pattern / broken-link
- **Claim**: The specific claim from the skill
- **Location**: File path and line range
- **Current Status**: What the docs/search says now
- **Suggestion**: Updated text

Return ALL findings as a structured list.
""",
  description: "Agent 3: Freshness Verify"
)
```

### Agent 4: Progressive Disclosure Analyst

```
Task(
  subagent_type: "general-purpose",
  prompt: """
## Assignment: Progressive Disclosure Analysis

Read the skill at ~/.claude/skills/{skill-name}/ and evaluate its information architecture.

### Principles:
- **SKILL.md** should be a compact router: essential principles + intake + routing table
- **references/** should contain domain knowledge (facts, schemas, rubrics)
- **workflows/** should contain step-by-step procedures
- **scripts/** should contain executable code and large code blocks
- **No monoliths**: No single file should try to do everything

### Checklist:
**SKILL.md Role:**
- [ ] SKILL.md stays under 500 lines
- [ ] Contains only essential principles (not full procedures)
- [ ] Has clear routing to other files (not "see also" buried in paragraphs)
- [ ] Does not contain large code blocks (>20 lines) that belong in scripts/

**Knowledge Separation:**
- [ ] Domain facts are in references/ (not inline in workflows)
- [ ] Procedures are in workflows/ (not crammed into SKILL.md)
- [ ] Reusable patterns are extracted (not duplicated across files)
- [ ] Templates are in templates/ or assets/ (not embedded in markdown)

**Monolith Detection:**
- [ ] No file over 500 lines
- [ ] No file mixing concerns (knowledge + procedure + code)
- [ ] No "wall of text" sections without structure
- [ ] Appropriate use of `<required_reading>` tags in workflows

### Output Format:
For each finding:
- **Severity**: Critical (monolith/unroutable) / Important (poor separation) / Minor (could be split)
- **Category**: monolith / missing-routing / mixed-concerns / embedded-code / poor-separation
- **Quote**: Exact text or line count showing the issue
- **Location**: File path and line range
- **Suggestion**: Where content should move and how to restructure

Return ALL findings as a structured list.
""",
  description: "Agent 4: Progressive Disclosure"
)
```

### Agent 5: Gap Analyst

```
Task(
  subagent_type: "general-purpose",
  prompt: """
## Assignment: Gap Analysis

Read the skill at ~/.claude/skills/{skill-name}/ and identify what's missing.

### Check against enrichment categories:

1. **Installation & Setup**: Dependencies, version requirements, install commands
2. **Configuration**: Config files, env vars, sensitive values
3. **Error Handling**: Common errors, troubleshooting, recovery procedures
4. **Testing**: How to verify the skill works, test data, validation steps
5. **Examples**: End-to-end examples, common use cases, edge cases
6. **Integration Points**: How this skill connects to other skills/tools
7. **Missing Files**: References mentioned but not created, scripts referenced but absent
8. **Templates**: Missing templates that would help execution
9. **Anti-Patterns**: Missing "what NOT to do" section
10. **Success Criteria**: Missing or untestable success criteria

### For each gap found:
- Is it a gap that would cause the skill to FAIL? (Critical)
- Is it a gap that makes the skill HARDER to use? (Important)
- Is it a gap that would make the skill BETTER? (Minor)

### Output Format:
For each finding:
- **Severity**: Critical / Important / Minor
- **Category**: setup / config / error-handling / testing / examples / integration / missing-file / templates / anti-patterns / success-criteria
- **What's Missing**: Specific description of the gap
- **Location**: Where it should be added (file + section)
- **Suggestion**: Draft content or outline for what to add
- **Effort**: S (< 10 lines) / M (10-50 lines) / L (50+ lines)

Return ALL findings as a structured list.
""",
  description: "Agent 5: Gap Analysis"
)
```

### Agent 6: Ecosystem Consistency Reviewer

```
Task(
  subagent_type: "general-purpose",
  prompt: """
## Assignment: Ecosystem Consistency Review

Read the skill at ~/.claude/skills/{skill-name}/ and evaluate how well it fits within the broader skill ecosystem.

### Check:
**Naming Conventions:**
- [ ] Skill name uses lowercase-with-hyphens
- [ ] Name clearly describes what the skill does
- [ ] No naming conflicts with other skills in ~/.claude/skills/

**Description Language:**
- [ ] Description is third person ("Use when..." not "I will...")
- [ ] Description includes trigger phrases for discovery
- [ ] Description states both WHAT it does and WHEN to use it

**Cross-Skill Integration:**
- [ ] Documents how it chains with other skills (e.g., "After this, run /verify-skill")
- [ ] Uses consistent terminology with related skills
- [ ] No duplicate capabilities with existing skills (check for overlapping skills)

**Standard Patterns:**
- [ ] Follows the frontmatter schema used by other skills
- [ ] Uses XML tags consistently (if the ecosystem uses them)
- [ ] Has a "Next Step" or pipeline section (like other workflow skills)
- [ ] Anti-patterns section present and useful

**Enumerate related skills** by listing ~/.claude/skills/ and checking for overlapping functionality.

### Output Format:
For each finding:
- **Severity**: Critical / Important / Minor
- **Category**: naming / description / integration / patterns / duplication
- **Quote**: Relevant text from the skill
- **Location**: File path and line range
- **Suggestion**: Specific fix with reference to ecosystem conventions

Return ALL findings as a structured list.
""",
  description: "Agent 6: Ecosystem Consistency"
)
```

</parallel_tasks>

## Phase 3: Score Synthesis

<thinking>
After all 6 agents return, map their findings to the 7-criterion weighted rubric.
Read the full rubric from references/quality-rubric.md for scoring details.
</thinking>

<task_list>

- [ ] Read `~/.claude/skills/workflow-improve-skill/references/quality-rubric.md`
- [ ] Collect findings from all 6 agents
- [ ] Deduplicate overlapping findings (keep the more specific version)
- [ ] Score each criterion using the rubric:

| Criterion | Weight | Primary Agent | Supporting Agent |
|-----------|--------|--------------|-----------------|
| Structure & Conformance | 15 pts | Structure Auditor | Progressive Disclosure |
| Description Quality | 10 pts | Structure Auditor | Ecosystem Consistency |
| Content Accuracy & Freshness | 20 pts | Freshness Verifier | Gap Analyst |
| Actionability | 20 pts | Content Quality | Gap Analyst |
| Progressive Disclosure | 15 pts | Progressive Disclosure | Structure Auditor |
| Examples & Patterns | 10 pts | Content Quality | Gap Analyst |
| Conciseness | 10 pts | Content Quality | Progressive Disclosure |

- [ ] Calculate total score (0-100) and assign grade:
  - A (90-100): Excellent — minimal or no issues
  - B (70-89): Good — minor improvements needed
  - C (50-69): Fair — significant issues to address
  - D (30-49): Poor — major rework needed
  - F (0-29): Failing — fundamental problems

</task_list>

**Output:** Present the quality report:

```markdown
## Quality Report: {skill-name}

### Overall Score: XX/100 (Grade: X)

### Criterion Breakdown
| Criterion | Score | Max | Notes |
|-----------|-------|-----|-------|
| Structure & Conformance | X | 15 | ... |
| Description Quality | X | 10 | ... |
| Content Accuracy & Freshness | X | 20 | ... |
| Actionability | X | 20 | ... |
| Progressive Disclosure | X | 15 | ... |
| Examples & Patterns | X | 10 | ... |
| Conciseness | X | 10 | ... |

### Strengths
- [What the skill does well]

### Findings by Severity

#### Critical (Must Fix)
1. [Finding] — [Agent] — [File:Line]

#### Important (Should Fix)
1. [Finding] — [Agent] — [File:Line]

#### Minor (Nice to Fix)
1. [Finding] — [Agent] — [File:Line]
```

## Phase 4: Improvement Plan Generation

<task_list>

- [ ] Read `~/.claude/skills/workflow-improve-skill/references/improvement-categories.md`
- [ ] Convert each finding into a concrete improvement action:
  - **What**: Specific change to make
  - **Where**: File path and section
  - **Before**: Current text (exact quote)
  - **After**: Replacement text
  - **Impact**: Expected score improvement (which criterion, how many points)
  - **Effort**: S (quick edit) / M (paragraph rewrite) / L (new file or major restructure)
- [ ] Group by severity: Critical first, then Important, then Minor
- [ ] Within each group, sort by score impact (highest first)
- [ ] Calculate expected total score after all improvements

</task_list>

**Output:** Present the improvement plan:

```markdown
## Improvement Plan: {skill-name}

**Current Score:** XX/100 (Grade: X)
**Expected After:** YY/100 (Grade: Y)

### Critical Improvements (X items)
1. **[Action title]** — {file} — Effort: S/M/L — Impact: +N pts
   > Before: `[current text]`
   > After: `[improved text]`

### Important Improvements (X items)
[same format]

### Minor Improvements (X items)
[same format]
```

## Phase 5: Approval Gate

<critical_requirement> Present 4 options and wait for user response. Do NOT proceed without approval. </critical_requirement>

```
How would you like to proceed?

1. **Apply all** — Execute all improvements (Critical + Important + Minor)
2. **Apply by severity** — Apply Critical first, then confirm for Important, then Minor
3. **Review each** — Show before/after diff per improvement, approve individually
4. **Report only** — No changes, keep the report

Choose (1-4):
```

**Wait for user response before proceeding.**

- If **option 4**: Skip to Phase 7 (report only, no re-score needed)
- If **option 1**: Proceed to Phase 6 with all improvements
- If **option 2**: Proceed to Phase 6 in three batches with confirmation between each
- If **option 3**: Proceed to Phase 6 showing each improvement individually

## Phase 6: Execute Improvements

<task_list>

For each approved improvement:

- [ ] Show the before/after diff:
  ```
  ### Improvement X: [Title]
  **File:** {path}

  **Before:**
  [exact current text]

  **After:**
  [replacement text]
  ```
- [ ] Apply using Edit tool (old_string → new_string)
- [ ] Read back the modified section to verify edit applied correctly
- [ ] Check cross-file consistency:
  - All references in SKILL.md still resolve to existing files
  - No broken cross-references between files
  - No duplicate content introduced
- [ ] If a new file needs to be created (gap fill), use Write tool
- [ ] Track which improvements were applied vs skipped

</task_list>

**If applying by severity (option 2):**
After each severity batch, pause:
```
Critical improvements applied. Continue with Important improvements? (y/n)
```

**If reviewing each (option 3):**
After showing each diff:
```
Apply this improvement? (y/n/edit)
```
- **y**: Apply as shown
- **n**: Skip this improvement
- **edit**: Let user modify the replacement text, then apply

## Phase 7: Verification & Before/After

<task_list>

- [ ] Count final lines per file using `wc -l`
- [ ] Re-score the skill using the same 7-criterion rubric from Phase 3
- [ ] Present comparison table:

```markdown
## Before/After Comparison: {skill-name}

### Score Comparison
| Criterion | Before | After | Change |
|-----------|--------|-------|--------|
| Structure & Conformance | X/15 | Y/15 | +Z |
| Description Quality | X/10 | Y/10 | +Z |
| Content Accuracy & Freshness | X/20 | Y/20 | +Z |
| Actionability | X/20 | Y/20 | +Z |
| Progressive Disclosure | X/15 | Y/15 | +Z |
| Examples & Patterns | X/10 | Y/10 | +Z |
| Conciseness | X/10 | Y/10 | +Z |
| **Total** | **XX/100 (Grade)** | **YY/100 (Grade)** | **+ZZ** |

### Line Count Comparison
| File | Before | After | Change |
|------|--------|-------|--------|
| SKILL.md | X | Y | -Z |
| references/... | X | Y | +Z |
| ... | ... | ... | ... |
| **Total** | **X** | **Y** | **+/-Z** |

### Improvements Applied
- [X] applied / [Y] skipped / [Z] total

### Remaining Issues
- [Any findings not addressed, with severity]
```

</task_list>

## Phase 8: Next-Step Routing

```
What's next?

1. Improve another skill → /workflows:improve-skill [name]
2. Deep-dive freshness verification → /verify-skill (via create-agent-skills)
3. Targeted fix for a specific issue → /heal-skill
4. Commit changes → git add + commit
5. Document learnings → /workflows:compound
```

---

## Workflow Pipeline

```
workflows:plan → workflows:design → workflows:work → workflows:review → workflows:compound
                                                          |
                                  workflows:improve-skill <+--> (standalone utility)
```

| Command | Purpose | Artifacts |
|---------|---------|-----------|
| `/workflows:plan` | Research and plan | `plans/*.md` |
| `/workflows:design` | Visual refinement | Updated components |
| `/workflows:work` | Execute the plan | Code + tests |
| `/workflows:review` | Multi-agent code review | `todos/*.md` |
| `/workflows:improve-skill` | **You are here** — Skill quality improvement | Improved SKILL.md |
| `/workflows:compound` | Document solutions | `docs/solutions/*.md` |

## Rules

- **Read before scoring** — always read the full skill before launching agents
- **All 6 agents run in parallel** — never run them sequentially
- **Deduplicate findings** — agents will overlap; keep the more specific finding
- **Score before AND after** — the before/after comparison is the deliverable
- **Never apply without approval** — Phase 5 is a hard gate
- **Verify after each edit** — read back to confirm the edit applied correctly
- **Cross-file consistency** — after edits, ensure all references still resolve
- **Don't invent content** — improvements should fix existing issues, not add speculative features
- **Preserve the skill's voice** — improve clarity without changing the skill's intended style
- **Effort-aware ordering** — within same severity, prefer high-impact/low-effort improvements first
