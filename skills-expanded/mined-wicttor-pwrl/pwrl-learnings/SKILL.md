---
name: pwrl-learnings
description: Extract, classify, deduplicate, structure, and save learnings from code, commits, tasks, and documentation
argument-hint: "[Optional: source material to extract from]"
---

# PWRL Learnings Orchestrator

Complete learning lifecycle management through 5-phase micro-skill pipeline.

## Interaction Method

- Use platform's `ask_user_question`, `ask_user`, `ask_user_input`, `vscode/askQuestions` or any available extension/tool for user interaction for all decisions
- Ask one question at a time
- Use multiple-choice questions when possible
- If input is empty, ask: "What would you like to extract learnings from? Provide source material (code, commit, docs) or describe the topic."
- Provide clear recovery suggestions when errors occur

## Architecture

```
Input (code/commit/task/documentation)
  ↓
Phase 1: pwrl-learnings-extract
  ├ Extract learnings from source
  ├ Identify candidates (gotcha, pattern, decision, technical_fix, workflow)
  ├ Output: extraction artifact
  ↓
Phase 2: pwrl-learnings-classify
  ├ Refine classification and priority
  ├ Assign domains and tags
  ├ Detect duplicates
  ├ Output: classification artifact
  ↓
Phase 3: pwrl-learnings-structure
  ├ Normalize format
  ├ Generate metadata and storage paths
  ├ Create indexes
  ├ Output: structured artifact
  ↓
Phase 4: pwrl-learnings-dedup
  ├ Identify and merge duplicates
  ├ Manage archived learnings
  ├ Preserve lineage
  ├ Output: deduplicated artifact
  ↓
Phase 5: pwrl-learnings-save
  ├ Create backups
  ├ Write to persistent storage
  ├ Generate indexes
  ├ Git commit changes
  ├ Output: saved artifact (ready for access)
  ↓
COMPLETE
```

## 5 Micro-Skills

### U4.1: pwrl-learnings-extract

**Extracts learnings** from various sources (code, commits, tasks, documentation, errors, reviews).

- Input: Source content and type
- Output: Extraction artifact with candidates
- **Quality Gate Validation:** Run `/pwrl-phase-checkpoint learnings 1 [artifact-path]` to validate phase completion. See [pwrl-phase-checkpoint](../pwrl-phase-checkpoint/SKILL.md) for validation rules.
- See: [README](../pwrl-learnings-extract/README.md)

### U4.2: pwrl-learnings-classify

**Classifies and prioritizes** learnings by type, domain, severity, and applicability.

- Input: Extraction artifact (extracted learnings)
- Output: Classification artifact (refined, prioritized)
- **Quality Gate Validation:** Run `/pwrl-phase-checkpoint learnings 2 [artifact-path]` to validate phase completion. See [pwrl-phase-checkpoint](../pwrl-phase-checkpoint/SKILL.md) for validation rules.
- See: [README](../pwrl-learnings-classify/README.md)

### U4.3: pwrl-learnings-structure

**Structures learnings** for persistent storage with metadata and indexes.

- Input: Classification artifact
- Output: Structure artifact (formatted, indexed, ready to save)
- **Quality Gate Validation:** Run `/pwrl-phase-checkpoint learnings 3 [artifact-path]` to validate phase completion. See [pwrl-phase-checkpoint](../pwrl-phase-checkpoint/SKILL.md) for validation rules.
- See: [README](../pwrl-learnings-structure/README.md)

### U4.4: pwrl-learnings-dedup

**Deduplicates and merges** identical or very similar learnings.

- Input: Structure artifact
- Output: Deduplicated artifact (with archive mapping)
- **Quality Gate Validation:** Run `/pwrl-phase-checkpoint learnings 4 [artifact-path]` to validate phase completion. See [pwrl-phase-checkpoint](../pwrl-phase-checkpoint/SKILL.md) for validation rules.
- See: [README](../pwrl-learnings-dedup/README.md)

### U4.5: pwrl-learnings-save

**Saves learnings** to permanent storage with backups and git versioning.

- Input: Deduplicated artifact
- Output: Saved artifact (persistent, indexed, accessible)
- **Quality Gate Validation:** Run `/pwrl-phase-checkpoint learnings 5 [artifact-path]` to validate phase completion. See [pwrl-phase-checkpoint](../pwrl-phase-checkpoint/SKILL.md) for validation rules.
- See: [README](../pwrl-learnings-save/README.md)

## Key References

- [Extract Learnings Workflow](pwrl-learnings-extract/references/extract-learnings-detailed-workflow.md) — Complete step-by-step extraction process
- [Classify Learnings Workflow](pwrl-learnings-classify/references/classify-learnings-detailed-workflow.md) — Classification, priority, domain, and early duplicate detection
- [Structure Learnings Workflow](pwrl-learnings-structure/references/structure-learnings-detailed-workflow.md) — Normalization, metadata, and index generation
- [Dedup Learnings Workflow](pwrl-learnings-dedup/references/dedup-learnings-detailed-workflow.md) — Fingerprinting, merging, and archive mapping
- [Save Learnings Workflow](pwrl-learnings-save/references/save-learnings-detailed-workflow.md) — Persistence, backup, and validation
- [Duplicate Handling Consolidated](references/duplicate-handling-consolidated.md) — Single source of truth for all duplicate detection logic

## Usage

```bash
/pwrl-learnings                              # Extract from current context
/pwrl-learnings code                         # Extract from code
/pwrl-learnings commit                       # Extract from git commit
/pwrl-learnings task                         # Extract from task description
/pwrl-learnings documentation                # Extract from docs
/pwrl-learnings error                        # Extract from error trace
```

## Learning Categories

| Type              | Definition                                 | Example                                   |
| ----------------- | ------------------------------------------ | ----------------------------------------- |
| **gotcha**        | Unexpected behavior, trap, surprise        | JavaScript type coercion, closure scope   |
| **pattern**       | Reusable solution, best practice, idiom    | Error handling pattern, caching strategy  |
| **decision**      | Why something was chosen over alternatives | Technology choice, architectural decision |
| **technical_fix** | Solution to specific problem               | Debugging steps, workaround, bug fix      |
| **workflow**      | Process improvement, efficiency gain       | Git workflow, code review technique       |

## Quality Criteria

**EXTRACTED:**

- ✓ Candidates identified from source
- ✓ Type classifications assigned
- ✓ Source references tracked

**CLASSIFIED:**

- ✓ Types refined and confirmed
- ✓ Severity/priority assessed
- ✓ Domains and tags assigned
- ✓ Duplicates detected

**STRUCTURED:**

- ✓ Normalized format
- ✓ Metadata generated
- ✓ Storage paths determined
- ✓ Indexes created

**DEDUPLICATED:**

- ✓ Exact duplicates merged
- ✓ High similarity flagged
- ✓ Archive mapping created
- ✓ Lineage preserved

**SAVED:**

- ✓ Persisted to disk
- ✓ Backup created
- ✓ Indexes updated
- ✓ Git history maintained
- ✓ Ready for search/retrieval

## Workflow: 5-Phase Pipeline

Each phase is executed sequentially by the orchestrator. The orchestrator invokes the micro-skill, validates output with quality gates, and passes the artifact to the next phase.

### Phase 1: Extract Learnings

Extract learning candidates from source material (code, commits, tasks, documentation, errors, reviews). Identify signal patterns, create candidates, set interaction mode.

**See detailed workflow:** [extract-learnings-detailed-workflow.md](pwrl-learnings-extract/references/extract-learnings-detailed-workflow.md)

### Phase 2: Classify Learnings

Refine type classifications, assign priority and domain, score applicability, detect potential duplicates. Flag early duplicate warnings for improved coverage.

**See detailed workflow:** [classify-learnings-detailed-workflow.md](pwrl-learnings-classify/references/classify-learnings-detailed-workflow.md)

### Phase 3: Structure Learnings

Normalize format, generate metadata (slugs, fingerprints, indexes), determine storage paths, create full-text search indexes.

**See detailed workflow:** [structure-learnings-detailed-workflow.md](pwrl-learnings-structure/references/structure-learnings-detailed-workflow.md)

### Phase 4: Deduplicate Learnings

Calculate fingerprints, find exact/semantic/high-similarity matches, merge with lineage preservation, link complementary learnings.

**See detailed workflow:** [dedup-learnings-detailed-workflow.md](pwrl-learnings-dedup/references/dedup-learnings-detailed-workflow.md)

### Phase 5: Save Learnings

Validate environment, create backup, write files with metadata, update indexes, commit to git, validate data integrity.

**See detailed workflow:** [save-learnings-detailed-workflow.md](pwrl-learnings-save/references/save-learnings-detailed-workflow.md)

## Interaction Mode Propagation

Interaction mode (`detailed | smart | yolo`) is set in Phase 1 (via `pwrl-learnings-extract` Step 1.5) and propagated through all five phases. The mode is stored in the extraction artifact's `interactionMode` field.

- **`detailed`** — Step-by-step interaction at each phase. Pause for every ambiguous classification in Phase 2 (classify) and every dedup decision in Phase 4 (dedup); inspect candidate learnings before they are committed. Maximum control. Best for curating a high-quality personal learnings library.
- **`smart`** — Phases run automatically; pause only for HIGH-confidence-low-applicability entries and for dedup decisions where the existing entry is itself low-confidence. v1 simplification: behaves like Yolo with a single confirmation prompt at workflow start.
- **`yolo`** — Full automation from Phase 1 through Phase 5. Only final confirmation before persisting. Auto-decisions use conservative thresholds (high confidence). Fastest. Best for routine session-end batch extraction or trusted source materials.

**Note:** The scanning itself (FIXME/HACK/TODO detection, commit-message analysis, etc.) is identical in all three modes — only the confirmations and dedup resolutions differ.

**Exception:** Error recovery steps always pause the pipeline for user action, regardless of mode. See `docs/learnings/pattern/interaction-mode-three-mode-propagation-2026-06-29.md` for the full contract.

## Duplicate Detection: Early + Late Coverage

**Early detection (Phase 2):** Classify phase checks extracted learnings against existing knowledge base. Flags candidates that appear to update existing learnings (suggest update instead of create).

**Late resolution (Phase 4):** Dedup phase runs full fingerprinting and merge algorithm. Handles exact, semantic, and high-similarity matches with archive mapping.

**Result:** Significantly reduced duplicates through multi-stage coverage.

## Integration Points

### Input From

- pwrl-work (code changes, execution context)
- pwrl-plan (planning context, decisions)
- pwrl-review (code review insights)
- GitHub (issues, PRs, discussions)
- Error logs and debugging sessions
- Manual input from user

### Output To

- `docs/learnings/` directory (persistent knowledge base)
- Git repository (with version history)
- Search indexes (for retrieval)
- Other PWRL phases (as reference material)

## Patterns Established

1. **Pure Skill Pipeline** — 5 micro-skills in sequence, no branching
2. **Explicit Artifacts** — Each phase produces typed output for next phase
3. **Comprehensive Testing** — 240+ tests covering all scenarios
4. **Error Recovery** — Every error has user-facing explanation + fix
5. **Documentation** — README for each micro-skill + protocols
6. **Traceability** — UUID tracking from extraction through saving

## Output Structure

After successful save, learnings available in:

```
docs/learnings/
├── INDEX.md                 (all learnings)
├── BY_TYPE.md              (organized by type)
├── BY_DOMAIN.md            (organized by domain)
├── BY_SEVERITY.md          (organized by severity)
├── RECENT.md               (latest 20)
├── .index.json             (machine-readable)
├── .backups/               (recovery backups)
│   └── 2026-06-12-14-58-00.tar.gz
├── gotcha/                 (type-based folders)
│   ├── async-race-condition.md
│   └── closure-scope-trap.md
├── pattern/
├── decision/
├── technical_fix/
├── workflow/
└── archived/               (merged/deprecated)
```

## Performance Expectations

- **Extract:** <5 seconds for typical code files
- **Classify:** <2 seconds per 100 learnings
- **Structure:** <3 seconds per 100 learnings
- **Dedup:** <5 seconds per 100 learnings
- **Save:** <10 seconds for 100+ learnings (includes git commit)
- **Full Pipeline:** <30 seconds for complete workflow

## Next Phase

Phase 5: Consolidation utilities (4 micro-skills)

- Learning search and retrieval
- Analytics and reporting
- Learning export/import
- Integration with other PWRL phases

### 9. Completion Summary

Provide:

- File path created
- Brief 1-line description
- Index row added/updated in `docs/learnings/INDEX.md`
- Suggestion: any related learnings to cross-reference or update

### 10. Consider Refresh (Optional)

After documenting the new learning, evaluate whether related learnings might need updates.

**Suggest `/pwrl-refresh-learnings [scope]` when:**

- This learning contradicts or supersedes an older documented approach
- A better solution was found for a previously documented problem
- Similar/overlapping learnings were found in step 6 that could benefit from consolidation
- This fills a gap that makes an older doc incomplete or outdated

**Skip refresh when:** No related learnings found, or existing docs are still current and consistent.

**How to suggest:** Provide specific scope based on findings (e.g., file:specific-doc.md, topic-name, or category). Let user decide whether to run refresh now.

## Output

Creates categorized learning document in `docs/learnings/[category]/[slug]-[date].md` with:

- YAML frontmatter (title, date, category, tags, severity)
- Structured content following category template
- Code examples and concrete details
- Cross-references to related learnings

Also updates `docs/learnings/INDEX.md` so every learning has a short description entry.

**Directory structure example:**

- `docs/learnings/technical-fix/` — Bug fixes and error resolutions
- `docs/learnings/pattern/` — Reusable patterns and architecture
- `docs/learnings/workflow/` — Process improvements and tooling
- `docs/learnings/gotcha/` — Non-obvious behaviors and edge cases
- `docs/learnings/concept/` — Technology and framework understanding
- `docs/learnings/decision/` — Why specific approaches were chosen

## Best Practices

- **Capture while fresh**: Document right after solving, while context is loaded
- **Be specific**: Include exact error messages, file paths, code snippets
- **Explain why**: Future you won't have the context you have now
- **Tag liberally**: Use 3-5 tags that you'd actually search for
- **Link related learnings**: Reference other docs that connect
- **Update > duplicate**: If a similar doc exists, enhance it rather than creating a new one
