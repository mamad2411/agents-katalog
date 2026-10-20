---
context: fork
allowed-tools:
  - Read
  - Glob
  - Bash(ls:*)
  - Bash(mkdir:*)
  - Bash(lok:*)
  - Write
---

# /design-doc:review - AI Review of Design Documents

**Purpose**: Automatically review design documents with Ollama/Codex and Claude as a guaranteed fallback. Identifies architectural issues, ADR compliance, blind spots, and provides actionable feedback before human review.

**Usage**:
- `/design-doc:review CLO-XX` - Review with the Ollama reviewer + Claude fallback if needed
- `/design-doc:review CLO-XX --persona all` - Run all domain-specific persona reviews
- `/design-doc:review` - Interactive mode

**Resilience guarantees**:
- Pre-flight health check skips an unreachable model immediately (no 5-minute timeout waste)
- Empty output short-circuit avoids burning validator API calls on trivially detectable failures
- Claude fallback reviewer activates when the external model fails - at least one review is always produced
- Synthesis adapts format: multi-review (Agreement/Disagreement) vs single-review (Key Findings)

**Google models are not part of this pipeline** (removed 2026-08-03). The `gemini` backend still ships in lok for user workflows; it is not wired into the repo's own review tooling.

---

## The reviewer: Ollama via Codex

| Aspect | Ollama (Codex) |
|--------|----------------|
| **File Reading** | Shell commands in read-only sandbox (`cat`, `find`, `head`) |
| **Directory Access** | Full project read access via `--sandbox read-only` |
| **Approach** | Agent reads files via shell |
| **Command** | `ollama launch codex --model MODEL -- exec "..." --sandbox read-only --oss --local-provider ollama` |
| **Sandbox** | Codex `--sandbox read-only` (no writes allowed) |

---

## When to Use

This command is typically invoked:
1. Automatically by `/task:orchestrate` after `/design-doc:create` completes
2. Manually when requesting an AI review of any design document

---

## Unified Review Prompt

**The Codex/Ollama reviewer and the Claude fallback receive the same review prompt.** Only the file-reading instructions differ slightly.

```
You are a senior software architect reviewing a design document.

TASK: Review the design document at: docs/design-docs/[DESIGN_DOC_FILENAME]

Read these files to gather context:
1. docs/design-docs/[DESIGN_DOC_FILENAME] — The design document to review
2. docs/arch/ — Architecture documents (read all .md files in this directory)
3. docs/adrs/ — Architecture Decision Records (60+ files). List filenames first, then read ONLY the ADRs relevant to this design document's topic (typically 5-10 most relevant)
4. docs/ROADMAP.md — Current project phase and task status
5. docs/DEPENDENCIES.md — Task dependency graph
6. docs/PROJECT.md — Active work and blockers

If the design document references specific source files, read those too for validation.

PROJECT CONTEXT:
- This is a Rust CLI tool for multi-LLM orchestration
- Linear workspace: cloud-ai
- Issue prefix: CLO

REVIEW CRITERIA:

1. COMPLETENESS (check all sections are present and meaningful)
   - Summary: Clear problem statement and solution
   - Background: Sufficient context
   - Architecture: Component overview
   - Detailed Design: Implementation approach
   - Implementation Plan: Phased approach with clear tasks
   - Acceptance Criteria: Testable success metrics

2. ARCHITECTURE QUALITY
   - Appropriate design patterns
   - Clear separation of concerns
   - Scalability considerations
   - Error handling strategy

3. ADR COMPLIANCE
   - List all ADR filenames in docs/adrs/ to understand the full decision landscape
   - Read the ADRs most relevant to this design document's topic (typically 5-10)
   - For each relevant ADR, check if the design document follows or contradicts the decisions
   - Flag any violations or deviations from established ADRs
   - Note if the design document introduces patterns that should become a new ADR

4. CODE QUALITY
   - Clean interfaces
   - Proper abstractions
   - Testability

5. SECURITY POSTURE
   - Input validation
   - Authentication/Authorization (if applicable)
   - No hardcoded secrets

6. OPERATIONAL READINESS
   - Logging and monitoring considered
   - Error recovery addressed
   - Rollback plan exists

7. ARCHITECTURAL ALIGNMENT
   - Aligns with existing architecture (from docs/arch and docs/adrs)
   - Follows established patterns
   - Fits within current project phase and dependencies

8. BLIND SPOTS
   - What is NOT covered in the design document that should be?
   - What edge cases or failure modes are missing?
   - What assumptions are made but not stated?
   - What cross-cutting concerns (logging, metrics, error handling, accessibility) are overlooked?
   - What integration points with existing code might cause unexpected issues?

OUTPUT FORMAT:

## 1. Completeness Check
[List sections present/missing with brief assessment]

## 2. Architecture Assessment
**Strengths**: [What's done well]
**Concerns**: [Issues to address]

## 3. ADR Compliance
[For each ADR in docs/arch/, state whether the design follows it]
**Violations**: [Any ADR violations found]
**New ADR Needed**: [If the design introduces patterns worthy of a new ADR]

## 4. Security Review
[Assessment of security posture]

## 5. Implementation Concerns
[Feedback on implementation plan]

## 6. Blind Spots
[What the design document misses or doesn't address]
- Missing edge cases
- Unstated assumptions
- Overlooked failure modes
- Missing cross-cutting concerns

## 7. Verdict
[One of: APPROVE | APPROVE_WITH_SUGGESTIONS | NEEDS_REVISION]

## 8. Actionable Feedback
[Prioritized list of specific, actionable items]
```

---

## Command Execution Instructions

### Step 1: Extract Task Number and Model Selection

1. **Parse arguments**:
   - Extract task number (e.g., `CLO-21` or `clo-21`)
   - Check for `--persona [security|concurrency|backend-integration|all]` (optional, adds domain-specific reviews)

2. **If no task number provided**:
   - Ask: "Which design document do you want to review? (e.g., CLO-21)"
   - Wait for response

### Step 2: Locate Design Document

```bash
ls docs/design-docs/clo-XX-*.md
```

**If NOT found**:
```
ERROR: Design document not found
Expected: docs/design-docs/clo-XX-*.md
Create one first: /design-doc:create CLO-XX
```
Exit command.

**If found**: Note the full filename (e.g., `clo-21-websocket-handler.md`)

### Step 3: Verify Context Files

Verify these files exist (the reviewer needs them):
- `docs/design-docs/clo-XX-*.md` — The design document to review
- `docs/arch/` — Architecture documents directory
- `docs/adrs/` — Architecture Decision Records (60+ files)
- `docs/ROADMAP.md` — Project phases and task status
- `docs/DEPENDENCIES.md` — Task dependency graph
- `docs/PROJECT.md` — Active work and blockers

If any are missing, warn but proceed.

### Step 4: Create Reviews Directory

```bash
mkdir -p docs/reviews
```

### Step 5: Build the Review Prompt

Construct the unified prompt (from the template above) by replacing `[DESIGN_DOC_FILENAME]` with the actual filename. **The reviewer and the fallback get the same prompt.**

### Step 6: Run AI reviews via lok

Run the lok design-review workflow. The workflow executes this pipeline:

1. **Health check** (10s) - verifies Ollama is reachable. An unreachable model is skipped immediately instead of timing out after 300s.
2. **Ollama review** (up to 300s) - short-circuits on empty output.
3. **Claude fallback** (up to 120s) - runs only if the Ollama review failed. Reads the design doc and context files directly to guarantee at least one review.
4. **Synthesis** - cross-references all successful reviews, includes reviewer status table with failure reasons.
5. **Write files** - saves individual reviews and synthesis.

Run in background:
```bash
lok run .lok/workflows/design-review.toml \
  "docs/design-docs/[DESIGN_DOC_FILENAME]" \
  "clo-[XX]" \
  --dir . \
  --verbose
```

This produces:
- `docs/reviews/clo-[XX]-review-ollama.md` (validated Ollama review or REVIEW_FAILED)
- `docs/reviews/clo-[XX]-review-claude-fallback.md` (only if the Ollama review failed)
- `docs/reviews/clo-[XX]-review-synthesis.md` (cross-referenced synthesis with reviewer status)

### Step 7: Save Review Outputs

**Ollama review**: `docs/reviews/clo-XX-review-ollama.md`
**Claude fallback** (only when the Ollama leg failed): `docs/reviews/clo-XX-review-claude-fallback.md`

**Format for each**:
```markdown
# Design Review: CLO-XX - [Title]

**Reviewed**: [Current Date YYYY-MM-DD]
**Reviewer**: [Codex via Ollama (glm-5.3:cloud) | Claude (fallback)]
**Design Document**: docs/design-docs/clo-XX-[description].md
**Review Duration**: [X seconds]

---

[AI REVIEW OUTPUT]

---

*This review was automatically generated. Human judgment should be applied when interpreting these suggestions.*
```

### Step 7.5: Run Persona Reviews (if --persona flag provided)

If `--persona` flag was provided, run additional domain-specific reviews. These run as Claude subagents, each reading the persona template and the design document.

**Available personas** (templates in `.claude/templates/review-personas/`):

| Persona | Template | Focus |
|---------|----------|-------|
| `security` | `review-personas/security.md` | API key handling, process execution, input validation |
| `concurrency` | `review-personas/concurrency.md` | Async safety, tokio patterns, race conditions |
| `backend-integration` | `review-personas/backend-integration.md` | Backend trait, error handling, timeout management |

**For each requested persona** (or all three if `--persona all`):

1. Read the persona template from `.claude/templates/review-personas/{persona}.md`
2. Build the persona review prompt by combining the template's review prompt with:
   - The design document path
   - Relevant source files (based on persona focus)
   - The persona's output format
3. Run as a subagent (Agent tool) with the persona prompt
4. Save output to `docs/reviews/clo-XX-review-{persona}.md`

**Output files**: `docs/reviews/clo-XX-review-security.md`, etc.

---

### Step 8: Analyze All Reviews and Produce Synthesis

After all reviews complete (Ollama or its Claude fallback, plus optional personas), read all review files and produce a synthesis following the template at `.claude/templates/review-synthesis.md`:

```markdown
## Review Synthesis

### Agreement (High Confidence)
[Items where 2+ reviewers independently identified the same concern]

### Disagreement (Needs Human Decision)
[Items where reviewers hold divergent positions]

### Novel Insights (Single Reviewer)
[Items found by only one reviewer]

### Persona Summary (if applicable)
| Persona | Verdict | Key Finding |
|---------|---------|-------------|
| Audio Safety | [verdict] | [1-line summary] |
| FFI Safety | [verdict] | [1-line summary] |
| State Machine | [verdict] | [1-line summary] |

### Consolidated Verdict
[Apply consensus rules: ANY NEEDS_REVISION -> NEEDS_REVISION, all APPROVE -> APPROVE, else APPROVE_WITH_SUGGESTIONS]

### Priority Actions
1. [Highest priority - agreement items first]
2. [Second priority]
3. [Third priority]
```

Save synthesis to `docs/reviews/clo-XX-review-synthesis.md`.

### Step 9: Return Summary

```
========================================
DESIGN REVIEW COMPLETE
========================================

Design Document: docs/design-docs/clo-XX-[description].md

Reviews Generated:
  - docs/reviews/clo-XX-review-ollama.md (Xs)
  - docs/reviews/clo-XX-review-claude-fallback.md (only if the Ollama leg failed)
  - docs/reviews/clo-XX-review-synthesis.md
  [If personas ran:]
  - docs/reviews/clo-XX-review-security.md
  - docs/reviews/clo-XX-review-concurrency.md
  - docs/reviews/clo-XX-review-backend-integration.md

Verdicts:
  - Ollama: [APPROVE | APPROVE_WITH_SUGGESTIONS | NEEDS_REVISION]
  - Synthesis: [APPROVE | APPROVE_WITH_SUGGESTIONS | NEEDS_REVISION]
  [If personas ran:]
  - Security: [SAFE | CONCERNS_HIGH | CONCERNS_MEDIUM]
  - Concurrency: [SAFE | CONCERNS_HIGH | CONCERNS_MEDIUM]
  - Backend Integration: [CORRECT | CONCERNS_HIGH | CONCERNS_MEDIUM]

Consensus: [APPROVE | NEEDS_REVISION | MIXED]

Key Findings:
1. [Top finding from synthesis]
2. [Second finding]
3. [Third finding]

Full reviews saved to: docs/reviews/
```

---

## Error Handling

**Check review results**

Read `docs/reviews/clo-[XX]-review-synthesis.md`. The synthesis always starts with a **Reviewer Status** table showing which models succeeded, failed, or were skipped.

**Interpreting the synthesis:**

| Scenario | Synthesis format | What happened |
|----------|-----------------|---------------|
| 2+ reviews valid | Multi Review (Agreement/Disagreement/Novel) | Normal multi-perspective synthesis |
| 1 review valid | Single Review (Key Findings) | One external model + possibly Claude fallback |
| Claude fallback only | Single Review, source = Claude | Both external models failed, fallback activated |
| `NO_REVIEWS_AVAILABLE` | Status table only | All reviewers failed (rare - Claude fallback should prevent this) |

**Failure diagnostics:**

The Reviewer Status table in the synthesis includes failure reasons inline:

```
## Reviewer Status
| Reviewer | Status | Detail |
|----------|--------|--------|
| Ollama | REVIEW_FAILED | Empty output, CLI startup failure |
| Claude (fallback) | OK | Produced full review |
```

For deeper diagnostics:
- Ollama stderr: `/tmp/lok-ollama-stderr.log`

**The `NO_REVIEWS_AVAILABLE` case should be rare.** The Claude fallback reviewer has no external dependencies - it reads files directly. If even the fallback fails, it indicates a problem with the lok pipeline itself, not network issues.

---

## Configuration

### Default Models

| Provider | Model | Integration | Notes |
|----------|-------|-------------|-------|
| Ollama | `glm-5.3:cloud` | Codex | `ollama launch codex --model MODEL --oss --local-provider ollama` |

### Environment Variables

- `OLLAMA_MODEL` - Override default Ollama model (default: `glm-5.3:cloud`)
- `OLLAMA_TIMEOUT` - Override Ollama timeout in seconds (default: 300)

---

## Output Files

| File | Purpose | When created |
|------|---------|--------------|
| `docs/reviews/clo-XX-review-ollama.md` | Codex/Ollama AI review | Always (may contain REVIEW_FAILED) |
| `docs/reviews/clo-XX-review-claude-fallback.md` | Claude fallback review | Only when the Ollama review failed |
| `docs/reviews/clo-XX-review-synthesis.md` | Cross-referenced synthesis with reviewer status | Always |

---

## Example: Running the review manually

```bash
DESIGN_DOC="clo-125-flat-model-list.md"
REVIEW_PROMPT="You are a senior software architect reviewing a design document.

TASK: Review the design document at: docs/design-docs/${DESIGN_DOC}

Read these files to gather context:
1. docs/design-docs/${DESIGN_DOC}
2. docs/arch/ (all .md files — Architecture Decision Records)
3. docs/ROADMAP.md
4. docs/DEPENDENCIES.md
5. docs/PROJECT.md

If the design document references specific source files, read those too.

PROJECT CONTEXT: Rust CLI tool for multi-LLM orchestration. Linear workspace: cloud-ai. Issue prefix: CLO.

[... full review criteria and output format ...]"

# Run Ollama/Codex
start=$(date +%s)
env -u CLAUDECODE timeout 300 ollama launch codex --model glm-5.3:cloud -- \
  exec "$REVIEW_PROMPT" \
  --sandbox read-only \
  --oss --local-provider ollama \
  --ephemeral \
  -o docs/reviews/clo-125-review-ollama.md
echo -e "\n\n**Duration**: $(($(date +%s) - start))s" >> docs/reviews/clo-125-review-ollama.md
echo "Review complete."
```

Prefer `lok run .lok/workflows/design-review.toml` over this - the manual
form skips the output validators, the Claude fallback, and the synthesis.

---

## Integration Notes

**Called by**: `/task:orchestrate` after `/design-doc:create` completes

**Creates**:
- `docs/reviews/clo-XX-review-ollama.md` (always)
- `docs/reviews/clo-XX-review-claude-fallback.md` (only when the Ollama review failed)
- `docs/reviews/clo-XX-review-synthesis.md` (always)
- `docs/reviews/clo-XX-review-{persona}.md` (if --persona used)

**Updates**: Nothing (read-only analysis)
