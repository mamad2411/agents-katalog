---
name: prompt-intelligence
description: "Session-start skill that loads learned behaviors from cortex annotations. Reads accumulated user corrections and builds a LEARNED BEHAVIORS context block that shapes agent behavior for the entire session. Run at session start or on-demand via /prompt-intelligence."
---

# Prompt Intelligence — Learned Behavior Loader

Load accumulated user corrections from cortex and build a behavioral context block.

---

## Phase 1: Load Lessons

```bash
# Load all feedback annotations from cortex
cortex_lessons(tag='feedback')
```

Call `cortex_lessons` with tag `feedback` to retrieve all accumulated corrections and learned behaviors.

If cortex_lessons is unavailable or returns empty, fall back to reading `.cortex/knowledge.jsonl` directly:

```bash
if [ -f "${CLAUDE_PROJECT_DIR}/.cortex/knowledge.jsonl" ]; then
  grep '"feedback"' "${CLAUDE_PROJECT_DIR}/.cortex/knowledge.jsonl"
fi
```

---

## Phase 2: Categorize and Count

Group lessons by correction category:

| Category | Tag Pattern | Meaning |
|----------|-------------|---------|
| Proof | `feedback` + `proof` | Agent must run tests and paste output |
| Autonomy | `feedback` + `autonomy` | Execute without asking after plan approval |
| Execute | `feedback` + `execute` | Do tasks yourself, don't instruct user |
| Process | `feedback` + `process` | Never skip pipeline steps |
| Testing | `feedback` + `testing` | E2E test everything |
| Sizing | `feedback` + `sizing` | Small tasks per agent |
| Classification | `feedback` + `misclass` | Classifier got the intent wrong |

Count occurrences per category. Categories with 3+ corrections are **auto-enforced** (non-negotiable behavioral rules). Categories with 1-2 are **reminders** (apply when relevant).

---

## Phase 3: Build LEARNED BEHAVIORS Block

Construct the context block and present it:

```markdown
## LEARNED BEHAVIORS (loaded from {N} corrections across {M} sessions)

### Auto-Enforced (3+ corrections — these are non-negotiable):
- [each auto-enforced behavior with occurrence count]

### Reminders (1-2 corrections — apply when relevant):
- [each reminder behavior]

### Classification Accuracy:
- Misclassifications detected: {count}
- Most common misclass: {pattern}
```

This block should be internalized — it shapes behavior for the entire session.

---

## Phase 4: Sync to Obsidian

Push learned knowledge to Obsidian for cross-agent visibility:

```bash
cortex_sync_knowledge()
```

This ensures Codex agents and other Claude sessions can access the same learned patterns.

---

## Phase 5: Bootstrap (First Run Only)

If `.cortex/knowledge.jsonl` has zero feedback entries, seed from existing memory files:

| Memory File | Tags |
|-------------|------|
| `feedback_proof_or_stfu.md` | `['feedback', 'proof', 'auto-enforce']` |
| `feedback_stop_asking_questions.md` | `['feedback', 'autonomy', 'auto-enforce']` |
| `feedback_process_is_not_optional.md` | `['feedback', 'process', 'auto-enforce']` |
| `feedback_no_assumptions_as_proof.md` | `['feedback', 'proof', 'verify']` |
| `feedback_e2e_contract_gate.md` | `['feedback', 'testing', 'auto-enforce']` |
| `feedback_agent_task_sizing.md` | `['feedback', 'sizing', 'auto-enforce']` |

For each memory file that exists in `~/.claude/projects/-Users-you-my-project/memory/`:
1. Read the file content
2. Write a JSONL entry to `.cortex/knowledge.jsonl` with the appropriate tags
3. Mark with `"author": "bootstrap"` so they aren't double-seeded

After seeding, re-run Phase 1-3 to load the bootstrapped data.

---

## When This Skill Runs

- **Session start**: Automatically suggested by environment hooks
- **On demand**: User invokes `/prompt-intelligence`
- **After compaction**: Re-load to ensure learned behaviors survive context compression

The classify-prompt.sh hook handles per-prompt classification. This skill handles session-level behavioral loading.
