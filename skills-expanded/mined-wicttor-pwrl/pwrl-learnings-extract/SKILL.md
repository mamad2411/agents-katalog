---
name: pwrl-learnings-extract
description: "Extract actionable learnings from code, commits, tasks, documentation, errors, and reviews."
argument-hint: "[source type: code|commit|task|documentation|error|review, and source content]"
---

# pwrl-learnings-extract — Learning Extraction

**Purpose:** Entry point to the learnings workflow. Scans source materials (code, commits, tasks, docs, errors, reviews) for learning signals and extracts actionable learning candidates. Produces extraction artifact consumed by pwrl-learnings-classify.

## Interaction Method

- Accepts source type and content as input.
- The level of interaction is controlled by the `interactionMode` selected in Step 1.5 below. The scanning itself is identical in all three modes; only the confirmations and dedup resolutions differ.
- Ask user only if source ambiguous: "Is this code or configuration?"
- Show extraction progress and candidate count.
- No approval gate; proceed to next skill.

## Input

User provides:

```
source_type: code | commit | task | documentation | error | review
source_content: [File content, commit message, error trace, etc.]
context:
  file_path: [optional]
  line_range: [optional]
  task_id: [optional]
  timestamp: [optional]
```

## Output: Extraction Artifact

Emit extraction artifact (YAML + markdown):

```yaml
---
format: pwrl-learnings-extract-artifact
version: "1.0"
extract_id: YYYY-MM-DD-NNN-extract
created: ISO-8601-timestamp
source_type: code | commit | task | documentation | error | review
source_ref: [file_path | commit_hash | task_id | error_id]
interactionMode: detailed | smart | yolo
---

# Learning Extraction Results

## Summary
- **Total Learnings Found:** [count]
- **By Category:**
  - Gotchas: [count]
  - Patterns: [count]
  - Decisions: [count]
  - Technical Fixes: [count]
  - Workflows: [count]

## Extracted Learnings

### Learning 1
- **Type:** [gotcha | pattern | decision | technical_fix | workflow]
- **Title:** [Concise 1-line title]
- **Problem:** [What problem does this learning address?]
- **Application:** [How/when to apply this learning?]
- **Source Context:** [File:line or relevant snippet]
- **Confidence:** [high | medium | low]
- **Linked Issues:** [GitHub issue numbers if available]

[Additional learnings...]

## Extraction Status
- **Status:** success
- **Quality:** [all|most|some] learnings are actionable
- **Coverage:** Scanned [N] lines / [N] items

## Ready for Classification
- **Next Skill:** pwrl-learnings-classify
- **Artifacts Passed:** This extraction artifact + source reference
- **Interaction Mode:** [chosen-value]
```

Artifact passed to `pwrl-learnings-classify`.

### Step 1.5: Select Interaction Mode

Before scanning source materials, ask the user to choose their engagement level for this extraction. Use the platform's `ask_user_question` extension (or equivalent) to present the following three options:

**Question:** "How would you like to proceed with this extraction?"

**Options:**

- **Detailed (Step-by-Step)** — Pause for confirmation on every ambiguous classification in Phase 2 (classify) and every dedup decision in Phase 4 (dedup); inspect candidate learnings before they are committed. Maximum control. Best for curating a high-quality personal learnings library.
- **Smart (Risk-gated automation)** — Phases run automatically; pause only for HIGH-confidence-low-applicability entries (those that are technically certain but whose actionability is unclear) and for any dedup decision where the existing entry is itself low-confidence. v1 simplification: behaves like Yolo with a single confirmation prompt at workflow start.
- **Yolo (Full Automation)** — Every candidate is auto-classified, dedup is auto-resolved, and only the final extraction report is shown. Fastest. Best for routine session-end batch extraction or trusted source materials.

> **Note:** In Yolo mode (the default for users who skip the prompt), the workflow proceeds as it did before this mode ask was added.

Store the selection in the extraction artifact (replacing the placeholder in the schema above):

```yaml
interactionMode: detailed | smart | yolo
```

**Mode-aware behavior propagation:** The `interactionMode` value flows into `pwrl-learnings-classify`, `pwrl-learnings-dedup`, `pwrl-learnings-structure`, and `pwrl-learnings-save` artifacts. Each downstream phase reads the value and adjusts its confirmation behavior:

- **Detailed:** Pause for every ambiguous classification and dedup decision; show candidate learning before saving.
- **Smart:** Auto-classify with high confidence; pause only for low-applicability or low-confidence-conflicting entries; auto-resolve obvious dedup.
- **Yolo:** Auto-resolve every classification and dedup; report only the final extraction + save summary.

---

## Detailed Workflow

For complete step-by-step instructions, see [extract-learnings-detailed-workflow.md](references/extract-learnings-detailed-workflow.md).

This SKILL.md provides an overview. The detailed workflow document contains:

- Exact steps for signal scanning by source type
- Learning candidate creation templates
- Metadata extraction details
- Validation checklists
- Error handling table
- Testing scenarios

## Quality Gate Validation

After completing this phase, run quality gate validation:

```bash
/pwrl-phase-checkpoint learnings 1 [artifact-path]
```

See [pwrl-phase-checkpoint](../../pwrl-phase-checkpoint/SKILL.md) for validation rules.

---

1. Check that source type is one of: code, commit, task, documentation, error, review
2. Verify source content is provided
3. If context available, validate timestamps and references
4. **If validation fails:**
   - Ask user to clarify source type
   - Retry validation

### Step 2: Scan for Learning Signals

**For source_type = "code":**

1. **Code comment signals:**
   - FIXME: [description] → Learning: "Known issue/workaround"
   - HACK: [description] → Learning: "Temporary solution or limitation"
   - TODO: [description] → Learning: "Incomplete but important pattern"
   - NOTE: [description] → Learning: "Cautionary note or gotcha"

2. **Code pattern signals:**
   - Unusual algorithms (not standard library)
   - Memoization or caching patterns
   - Complex error handling
   - Resource management (acquire/release patterns)
   - Synchronization/concurrency patterns

3. **Code quality signals:**
   - Deeply nested logic (>4 levels) → Learning: "Complex branching gotcha"
   - Long parameter lists (>5) → Learning: "API design pattern"
   - Duplicated logic → Learning: "Missing abstraction"
   - Magic numbers → Learning: "Configuration gotcha"

**For source_type = "commit":**

1. **Commit message analysis:**
   - Extract intent from commit message
   - Identify if fix, feature, refactor, or chore
   - Look for issue numbers

2. **Diff pattern analysis:**
   - File count and types (code, tests, docs)
   - LOC added/deleted ratio
   - If heavy refactoring: "Refactoring decision"
   - If cross-module: "Integration pattern"

3. **Linked issues:**
   - Extract GitHub issue numbers
   - Categorize by issue type

**For source_type = "task":**

1. **Requirements analysis:**
   - Extract acceptance criteria
   - Note constraints or blockers
   - Identify dependencies

2. **Learning signals:**
   - "Why this design?" → Learning: "Architectural decision"
   - "Constraint: X" → Learning: "System limitation"
   - "Blocked by Y" → Learning: "Dependency management"

**For source_type = "documentation":**

1. **Architecture sections:**
   - System design decisions
   - Tradeoffs and rationale
   - Known limitations

2. **Setup/configuration:**
   - Common pitfalls mentioned
   - Configuration gotchas
   - Environment-specific issues

3. **FAQ/troubleshooting:**
   - Common errors and solutions
   - Preventative measures

**For source_type = "error":**

1. **Error trace analysis:**
   - Extract error type and message
   - Identify root cause
   - Note affected code

2. **Symptom-to-fix mapping:**
   - What manifested? (symptom)
   - Why did it happen? (root cause)
   - How was it fixed? (solution)
   - How to prevent? (prevention)

**For source_type = "review":**

1. **Review feedback patterns:**
   - Comments praising patterns → Learning: "Praised approach"
   - Comments questioning approaches → Learning: "Anti-pattern"
   - Suggestions for improvement → Learning: "Best practice"

2. **Categories:**
   - Security feedback → Learning: "Security gotcha"
   - Performance feedback → Learning: "Performance pattern"
   - Style feedback → Learning: "Coding standard"

### Step 3: Create Learning Candidates

**For each signal found, create learning object:**

```
Learning Candidate:
  Type: [gotcha | pattern | decision | technical_fix | workflow]
  Title: [Concise, actionable title]
  Problem: [Clear statement of problem/opportunity]
  Application: [How to use this learning]
  Confidence: [high | medium | low]
  Source: [File:line or commit hash or task_id]
```

**Confidence levels:**

- **High:** Clear, explicit signal (FIXME comment, documented decision)
- **Medium:** Inferred from code/commit pattern
- **Low:** Uncertain interpretation; may need human review

### Step 4: Categorize Learnings

**Assign preliminary types:**

- **Gotcha:** "Beware of X" or "Don't do X"
  - Example: "Race condition when accessing shared state"

- **Pattern:** "Effective approach for Y"
  - Example: "Memoization for expensive computations"

- **Decision:** "Why we chose X over Y"
  - Example: "Chose async/await over callbacks for readability"

- **Technical Fix:** "How to solve specific problem Z"
  - Example: "Fix import cycle by moving type to separate file"

- **Workflow:** "Process or best practice"
  - Example: "Always update docs when changing public API"

### Step 5: Extract Metadata

**For each learning, collect:**

- Source reference: file path, line range, or commit hash
- Source type: what kind of source was scanned
- Timestamp: when extraction occurred
- Context: task ID, related files, linked issues
- Confidence: high/medium/low
- Tags: optional categorization (security, performance, etc.)

### Step 6: Validate Extraction

**Check each candidate learning has:**

- ✓ Title (1 line, actionable)
- ✓ Problem (clear statement)
- ✓ Application (how/when to apply)
- ✓ Source reference (traceable)
- ✓ Type (one of 5 types)

**If validation fails:**

- Mark as low-confidence
- Continue (don't discard)

### Step 7: Generate Extraction Artifact

**Emit artifact with:**

- All extracted learning candidates
- Metadata and source references
- Confidence levels
- Extraction status (success, quality notes)
- Ready flag for next skill

## Source-Specific Guidance

### Code Scanning

**Look for these signals:**

```javascript
// FIXME: Race condition when multiple instances access cache
class Cache {
  constructor() {
    this.data = {};
  }
  // ^^ Learning: "Race condition gotcha"
}

// HACK: Temporary workaround until DB migration complete
if (legacyFormat) {
  data = convertFromLegacy(data);
}
// ^^ Learning: "Technical fix or temporary solution"

// Complex logic with nested conditions
if (auth && perms && !banned && date < expiry && verified) {
  // 5-level nesting
  // ^^ Learning: "Condition complexity pattern"
}
```

### Commit Message Scanning

```
Commit: "Fix: Race condition in cache access (closes #456)"
Extract:
  Type: technical_fix
  Title: "Use mutex to prevent race condition"
  Problem: "Multiple threads accessing shared cache"
  Application: "Add locking for shared mutable state"
  Issue: #456
```

### Error Trace Scanning

```
Error: TypeError: Cannot read property 'foo' of undefined
Stack: at app.js:42 in processData()
Extract:
  Type: gotcha
  Title: "Null/undefined check before property access"
  Problem: "Uninitialized object passed to function"
  Application: "Always validate inputs; add null checks"
  Prevention: "Use TypeScript or strict null checking"
```

## Error Handling

| Error               | Recovery                                    |
| ------------------- | ------------------------------------------- |
| Invalid source_type | Ask user to clarify (code/commit/task/etc.) |
| Empty source        | Return error; ask user to provide content   |
| Unreadable format   | Ask user to provide plain text or summary   |
| No signals found    | Return empty artifact; continue to classify |
| Parse error         | Log issue; continue with parsed portion     |

## Testing Coverage

Test file: `tests/pwrl-learnings/extract-learnings.test.ts`

**Happy Path Tests:**

- ✅ Code with FIXME/HACK/TODO comments (3+ learnings)
- ✅ Commit message with issue number (1+ learnings)
- ✅ Task with constraints (2+ learnings)
- ✅ Error trace with root cause (1+ learnings)
- ✅ Review feedback (2+ learnings)
- ✅ Documentation with tradeoffs (2+ learnings)

**Edge Cases:**

- ✅ Code with no comments (no learnings)
- ✅ Very long source (50+ lines scanned)
- ✅ Special characters in comments (handled)
- ✅ Multiple different signal types (all categorized)
- ✅ Conflicting signals (both extracted)

**Output Validation Tests:**

- ✅ Artifact structure complete
- ✅ All learnings have required fields
- ✅ Confidence levels reasonable
- ✅ Source references traceable
- ✅ Ready flag set correctly
