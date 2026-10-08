---
name: maid-methodology
description: Provides guidance on the MAID (Manifest-driven AI Development) methodology including creating manifests, writing behavioral tests, implementing code with TDD, validation, and using MAID subagents. Use when the user mentions MAID, manifests, manifest-driven development, task manifests, behavioral tests, or validation implementations.
---

# MAID Methodology

**MAID** = Manifest-driven AI Development

A methodology for developing software with AI assistance by explicitly declaring what files can be modified, what code artifacts should be created, and how to validate changes.

**Supported Languages**: Python (`.py`) and TypeScript/JavaScript (`.ts`, `.tsx`, `.js`, `.jsx`)

---

## Core Principles

- **Explicitness**: Every task context is explicitly defined in manifests
- **Extreme Isolation**: Tasks touch minimal files, specified in manifest
- **Test-Driven Validation**: Tests define success, not subjective assessment
- **Verifiable Chronology**: Current state = sequential manifest application
- **Subagent Delegation**: Each phase uses its designated subagent

**TDD at two levels:**
- **Planning Loop**: Iterative test-manifest refinement (micro TDD)
- **Overall Workflow**: Red (failing tests) → Green (passing implementation) → Refactor

---

## MAID Subagents (Required)

**You MUST delegate to the appropriate subagent for each phase.**

| Phase | Subagent | Purpose |
|-------|----------|---------|
| **Phase 1** | `maid-runner:maid-manifest-architect` | Create/modify manifests |
| **Phase 1-2 Gate** | `maid-runner:maid-plan-reviewer` | Review before implementation |
| **Phase 2** | `maid-runner:maid-test-designer` | Create behavioral tests |
| **Phase 3** | `maid-runner:maid-developer` | Implement code (TDD) |
| **Phase 3 Support** | `maid-runner:maid-fixer` | Fix validation/test failures |
| **Phase 3.5** | `maid-runner:maid-refactorer` | Improve code quality |
| **Audit** | `maid-runner:maid-auditor` | Check MAID compliance |

### Invoking Subagents

Use the **Task tool** to delegate:

```
Task tool parameters:
- subagent_type: "maid-runner:maid-manifest-architect" (or other maid-runner agent)
- prompt: "Create a manifest for [goal]"
- description: "Phase 1: Create manifest"
```

For detailed invocation patterns, see [SUBAGENT-PATTERNS.md](SUBAGENT-PATTERNS.md).

---

## MAID Workflow Overview

### Phase 1: Manifest Creation
**Subagent: `maid-runner:maid-manifest-architect`**

1. Confirm goal with user
2. Invoke subagent to create `manifests/task-XXX-description.manifest.json`
3. Validate: `maid validate <path> --use-manifest-chain`

### Phase 2: Test Design
**Subagent: `maid-runner:maid-test-designer`**

1. Invoke subagent to create behavioral tests
2. Tests must USE artifacts and ASSERT on behavior
3. Validate: `maid validate <path> --validation-mode behavioral`
4. **Quality Gate**: Invoke `maid-runner:maid-plan-reviewer` before implementation

### Phase 3: Implementation
**Subagent: `maid-runner:maid-developer`**

1. Confirm Red phase (tests fail)
2. Invoke subagent to implement code
3. Validate: `maid validate <path> --validation-mode implementation`
4. Run tests until all pass

**Error Recovery**: Invoke `maid-runner:maid-fixer` if validation fails.

### Phase 3.5: Refactoring
**Subagent: `maid-runner:maid-refactorer`**

1. Invoke subagent to improve code quality
2. Maintain passing tests
3. Keep public API unchanged

### Phase 4: Integration

```bash
maid validate        # Validate ALL manifests
maid test            # Run ALL validation commands
pytest tests/ -v     # Full test suite (Python)
npm test             # Full test suite (TypeScript)
```

For detailed phase workflows, see [WORKFLOW-DETAILS.md](WORKFLOW-DETAILS.md).

---

## Essential CLI Commands

```bash
# Primary validation
maid validate                                    # All manifests
maid validate <path> --use-manifest-chain        # Single manifest with chain

# Validation modes
maid validate <path> --validation-mode behavioral      # Phase 2
maid validate <path> --validation-mode implementation  # Phase 3

# Manifest creation
maid manifest create <file> --goal "description"

# Run tests
maid test                    # All validation commands
maid test --manifest <path>  # Single manifest
```

For complete CLI reference, see [CLI-REFERENCE.md](CLI-REFERENCE.md).

---

## Manifest Rules (Critical)

1. **Manifest Immutability**: Current task's manifest can be modified; prior manifests are immutable.

2. **One File Per Manifest**: `expectedArtifacts` defines artifacts for ONE file only.

3. **Multi-File Changes**: Create separate sequential manifests for each file.

4. **Definition of Done**: Both `maid validate` and `maid test` must pass 100%.

For manifest templates and examples, see [MANIFEST-TEMPLATES.md](MANIFEST-TEMPLATES.md).

---

## Quick Manifest Template

```json
{
  "goal": "Clear task description",
  "taskType": "edit|create|refactor",
  "supersedes": [],
  "creatableFiles": [],
  "editableFiles": [],
  "readonlyFiles": [],
  "expectedArtifacts": {
    "file": "path/to/file.py",
    "contains": [
      {
        "type": "function|class",
        "name": "artifact_name",
        "args": [{"name": "arg1", "type": "str"}],
        "returns": "ReturnType"
      }
    ]
  },
  "validationCommand": ["pytest", "tests/test_file.py", "-v"]
}
```

---

## Artifact Rules

- **Public** (no `_` prefix): MUST be in manifest
- **Private** (`_` prefix): Optional in manifest
- **creatableFiles**: Strict validation (exact match)
- **editableFiles**: Permissive validation (contains at least)

---

## Testing Standards

Tests must follow the unit testing rules:

1. **Test behavior, not implementation details**
2. **Minimize mocking to essential dependencies**
3. **Make tests deterministic and independent**
4. **Test for failure conditions, not just happy paths**
5. **Follow AAA pattern**: Arrange, Act, Assert

For complete testing guidelines, see `@${CLAUDE_PLUGIN_ROOT}/docs/unit-testing-rules.md`.

---

## When to Create a Manifest

**Create a manifest for:**
- Public API changes (functions, classes, methods without `_` prefix)
- New features
- Bug fixes

**Exempt from MAID:**
- Pure documentation changes (only `.md` files)
- Private implementation refactoring (with `_` prefix)

---

## Key Reminders

- **NEVER** modify code without a manifest
- **NEVER** skip validation
- **NEVER** access files not listed in manifest
- **ALWAYS** use the appropriate subagent for each phase
- **ALWAYS** follow: Manifest → Tests → Implementation → Validate

---

## Available Slash Commands

| Command | Description |
|---------|-------------|
| `/spike` | Explore idea before creating manifest |
| `/plan` | Complete Phase 1 & 2 (manifest + tests) |
| `/maid-run` | Full MAID workflow |
| `/generate-manifest` | Create manifest (Phase 1) |
| `/validate-manifest` | Validate manifest (Quality gate) |
| `/generate-tests` | Create tests (Phase 2) |
| `/implement` | Implement code (Phase 3) |
| `/fix` | Fix validation errors |
| `/refactor` | Improve code quality (Phase 3.5) |
| `/audit` | Check MAID compliance |

---

## Additional Resources

- **Subagent Patterns**: [SUBAGENT-PATTERNS.md](SUBAGENT-PATTERNS.md)
- **CLI Reference**: [CLI-REFERENCE.md](CLI-REFERENCE.md)
- **Manifest Templates**: [MANIFEST-TEMPLATES.md](MANIFEST-TEMPLATES.md)
- **Workflow Details**: [WORKFLOW-DETAILS.md](WORKFLOW-DETAILS.md)
- **Full MAID Specification**: `@${CLAUDE_PLUGIN_ROOT}/docs/maid_specs.md`
- **Unit Testing Rules**: `@${CLAUDE_PLUGIN_ROOT}/docs/unit-testing-rules.md`
- **MAID Runner Repository**: https://github.com/mamertofabian/maid-runner
