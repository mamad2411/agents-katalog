---
sap_id: SAP-002
version: 1.0.0
status: active
last_updated: 2025-11-20
progressive_loading:
  phase_1: "0-4k tokens (quick reference)"
  phase_2: "4-9k tokens (implementation)"
  phase_3: "9k+ tokens (comprehensive)"
---

# Claude Code Awareness: chora-base Template Repository

**SAP ID**: SAP-002
**Capability**: chora-base (Meta-SAP - Self-Description)
**Version**: 1.0.0
**Audience**: Claude Code (VSCode Extension)

---

## Progressive Loading

```yaml
phase_1_quick_reference:
  lines: 1-150
  tokens: ~4k
  use_when: "Quick chora-base operations and navigation"

phase_2_implementation:
  lines: 150-350
  tokens: ~9k
  use_when: "Scaffolding projects, installing SAPs, working with chora-base files"

phase_3_optimization:
  lines: 350-end
  tokens: ~12k
  use_when: "Advanced workflows, ecosystem integration, contributing to chora-base"
```

---

## 📖 Quick Reference

**New to SAP-002?** → Read **[README.md](README.md)** first (10-min read) for architecture overview, SAP categories, and meta-capability demonstration.

**This CLAUDE.md provides**: Claude Code-specific tool patterns (Read, Write, Edit, Bash) for scaffolding projects, adopting SAPs, and navigating the chora-base ecosystem.

---

## 1. Claude Code Tool Patterns

### Primary Tools for chora-base Operations

| Operation | Primary Tool | Secondary Tools | Rationale |
|-----------|--------------|-----------------|-----------|
| **Scaffold new project** | Bash (setup.py or cp) | Write (for manual template substitution) | Bash executes generator or copies template efficiently |
| **Adopt SAP** | Read → Bash → Write/Edit | Grep (find config files) | Read adoption-blueprint.md, Bash for CLI commands, Write for new configs, Edit for modifications |
| **Navigate SAP catalog** | Read (INDEX.md) | Grep (search by keyword) | Read INDEX.md for structured catalog, Grep for keyword search |
| **Create new SAP** | Write (5 artifacts) | Bash (generate-sap.py if SAP-029 adopted) | Write each of 5 artifacts, or Bash to run generator |
| **Update awareness files** | Edit (AGENTS.md, CLAUDE.md) | Read (to verify current content) | Edit for targeted changes, Read before editing |
| **Validate links** | Bash (validate-awareness-links.sh) | - | Bash runs validation script |

---

## 2. Common Workflows

### Workflow 1: Scaffold New Project with Bash and Write

**Scenario**: User says "Create a new project using chora-base"

**Claude Code Pattern**:

**Phase 1: Determine Project Type** (Bash for quick check):
```markdown
Claude: I'll help you scaffold a new project from chora-base. Let me first check what templates are available.

1. Check available templates:
   Bash: ls -la static-template/
   # Shows: Python structure (src/, tests/, pyproject.toml) or TypeScript/React (package.json, tsconfig.json)

2. Ask user for project details:
   - Project name? (e.g., "my-app")
   - Language/framework? (Python / TypeScript / React)
   - Author name?
```

**Phase 2: Scaffold Project** (Bash for generation or cp):

**Option A: Blueprint-Based Generation** (Python projects):
```markdown
Claude: I'll use chora-base's blueprint generator to create your Python project.

1. Run generator:
   Bash: python setup.py
   # Note: setup.py is interactive - not ideal for Claude Code
   # Better: Use Option B (static template copy) for non-interactive workflow

2. If setup.py supports --project flag (check first):
   Bash: python setup.py --project my-app --author "Your Name" --no-input
```

**Option B: Static Template Copy** (recommended for Claude Code):
```markdown
Claude: I'll copy the static template and customize it for your project.

1. Copy template to new directory:
   Bash: cp -r static-template ../my-app && cd ../my-app

2. Read template files to find placeholders:
   Read: ../my-app/README.md
   # Look for: {{project_name}}, {{author}}, {{package_name}}

3. Replace placeholders (use Edit for each file):
   Edit: ../my-app/README.md
   # old_string: {{project_name}}
   # new_string: my-app

   Edit: ../my-app/pyproject.toml (or package.json)
   # old_string: {{package_name}}
   # new_string: my_app (Python) or myApp (TypeScript)

4. Initialize git:
   Bash: git init && git add . && git commit -m "Initial commit from chora-base template"

5. Verify structure:
   Bash: ls -la
   # Expected: CLAUDE.md, AGENTS.md, README.md, src/, tests/, pyproject.toml (or package.json)
```

**Phase 3: Install Dependencies** (Bash):
```markdown
Claude: Now I'll install dependencies and verify the project is ready.

1. Install Python dependencies:
   Bash: pip install -e .

   OR for TypeScript/React:
   Bash: npm install

2. Run tests to verify:
   Bash: pytest  # Python
   # OR
   Bash: npm test  # TypeScript/React

3. Report success:
   "Your project 'my-app' is ready! Next steps:
    - Adopt SAPs: SAP-004 (testing), SAP-005 (ci-cd), SAP-015 (task-tracking)
    - Start developing: cd ../my-app"
```

**Tools Used**: Bash (5x), Read (1x), Edit (2-3x), Write (0x - Edit for modifications)

**Token Estimate**: ~8-12k (Phase 1: 2k, Phase 2: 4-6k, Phase 3: 2-4k)

---

### Workflow 2: Adopt SAP with Read, Bash, Write, Edit

**Scenario**: User says "Add task tracking to my project" (SAP-015)

**Claude Code Pattern**:

**Phase 1: Read Adoption Blueprint** (Read):
```markdown
Claude: I'll help you adopt SAP-015 (beads task tracking). Let me read the installation guide.

1. Read adoption blueprint:
   Read: docs/skilled-awareness/task-tracking/adoption-blueprint.md
   # Focus on lines 20-100 (installation steps, prerequisites)

2. Check prerequisites:
   Read: docs/skilled-awareness/task-tracking/adoption-blueprint.md
   # Lines 10-20: Prerequisites section
   # Example: "Node.js 18+, npm 9+"

3. Verify prerequisites met:
   Bash: node --version && npm --version
   # Ensure versions match requirements
```

**Phase 2: Install SAP** (Bash for CLI, Write for configs):
```markdown
Claude: Prerequisites met. Installing beads CLI and initializing configuration.

1. Install CLI:
   Bash: npm install -g @beads/bd

2. Initialize beads:
   Bash: bd init
   # Creates:
   #   .beads/config.yaml
   #   .beads/issues.jsonl (git-tracked)
   #   .beads/beads.db (gitignored)

3. Read generated config to verify:
   Read: .beads/config.yaml
   # Verify default settings

4. If config needs customization (based on adoption-blueprint.md):
   Edit: .beads/config.yaml
   # old_string: default_assignee: null
   # new_string: default_assignee: "me"
```

**Phase 3: Update Project Awareness Files** (Read then Edit):
```markdown
Claude: SAP-015 installed. Now I'll update your project's awareness files.

1. Read current AGENTS.md to find insertion point:
   Read: AGENTS.md
   # Find "## Adopted SAPs" section (or create it)

2. Add SAP-015 entry:
   Edit: AGENTS.md
   # old_string: ## Adopted SAPs
   # new_string: ## Adopted SAPs

   ### SAP-015 (task-tracking)
   **CLI**: `bd` (beads task tracker)
   **Storage**: `.beads/issues.jsonl` (git-committed)

   **Agent Workflow**:
   1. Find work: `bd ready --json`
   2. Claim task: `bd update {id} --status in_progress --assignee me`
   3. Complete: `bd close {id} --reason "Done"`

3. Update CLAUDE.md (Claude-specific patterns):
   Read: CLAUDE.md
   # Find "## Tool Patterns" or create section

   Edit: CLAUDE.md
   # Add Claude Code-specific beads usage patterns
```

**Phase 4: Verify Installation** (Bash):
```markdown
Claude: Verifying SAP-015 installation.

1. Create test task:
   Bash: bd create "Test task tracking" --priority low --status open

2. List tasks:
   Bash: bd list --status open --json
   # Should show newly created task

3. Close test task:
   Bash: bd close {id} --reason "Verification complete"

4. Report success:
   "SAP-015 (beads) successfully installed!
    - CLI: `bd` available globally
    - Storage: .beads/issues.jsonl (commit this to git)
    - Cache: .beads/beads.db (add to .gitignore)
    - Awareness files updated: AGENTS.md, CLAUDE.md"
```

**Tools Used**: Read (4x), Bash (6x), Edit (2x), Write (0x - Edit for modifications)

**Token Estimate**: ~10-15k (Phase 1: 3k, Phase 2: 3-4k, Phase 3: 2-3k, Phase 4: 2-3k)

---

### Workflow 3: Navigate SAP Catalog with Read and Grep

**Scenario**: User asks "What React capabilities does chora-base have?"

**Claude Code Pattern**:

**Phase 1: Quick Lookup with Grep** (Grep for keyword search):
```markdown
Claude: Let me search for React-related SAPs in the catalog.

1. Search INDEX.md for "react":
   Grep: pattern: "react"
         path: docs/skilled-awareness/INDEX.md
         output_mode: content
   # Returns lines mentioning SAP-020 through SAP-025

2. If Grep not available, use Read:
   Read: docs/skilled-awareness/INDEX.md
   # Lines 53-58 (React SAPs section based on structure)
```

**Phase 2: Read SAP Summaries** (Read AGENTS.md for each):
```markdown
Claude: Found 6 React SAPs. Let me get quick summaries.

1. Read SAP-020 summary:
   Read: docs/skilled-awareness/react-foundation/AGENTS.md
   # Lines 1-50 (What is section + summary)

2. Read SAP-021 summary:
   Read: docs/skilled-awareness/react-testing/AGENTS.md
   # Lines 1-50

... (repeat for SAP-022 through SAP-025)

3. Synthesize and report to user:
   "chora-base has 6 React SAPs:
    - SAP-020 (react-foundation): Next.js 15, Vite 7, project scaffolding
    - SAP-021 (react-testing): Vitest 4, RTL 16, MSW 2.x
    - SAP-022 (react-linting): ESLint 9, Prettier 3
    - SAP-023 (react-state-management): TanStack Query, Zustand, React Hook Form
    - SAP-024 (react-styling): Tailwind v4, shadcn/ui
    - SAP-025 (react-performance): Core Web Vitals, Lighthouse CI

    Would you like to adopt any of these?"
```

**Tools Used**: Grep (1x), Read (6x - one per SAP summary)

**Token Estimate**: ~8-12k (Phase 1: 1k, Phase 2: 7-11k for 6 summaries)

**Optimization**: If user asks about ALL SAPs, read INDEX.md only (~50 lines, 1.5k tokens) instead of reading 6 AGENTS.md files (~300 lines each, 7k tokens each = 42k total).

---

## 3. Claude-Specific Tips

### Tip 1: Use Bash for Non-Interactive Operations, Write for File Creation

**Scenario**: Scaffolding new project from chora-base

**Best Practice**:
- ✅ **Use Bash**: `cp -r static-template/ ../my-app` (fast, non-interactive)
- ✅ **Use Edit**: Replace placeholders in existing files (targeted modifications)
- ❌ **Avoid Bash**: `python setup.py` (interactive prompts, can't provide input)
- ❌ **Avoid Write**: Don't write entire files with replaced placeholders (use Edit instead)

**Why**: Bash cp is instant, Edit for placeholders is cleaner than Write for entire files.

---

### Tip 2: Read Adoption Blueprint BEFORE Installing SAPs

**Scenario**: User says "Install SAP-021 (react-testing)"

**Best Practice**:
- ✅ **First**: Read adoption-blueprint.md (lines 1-100 for prerequisites, steps)
- ✅ **Then**: Execute Bash commands from blueprint
- ❌ **Don't**: Guess installation steps without reading blueprint

**Why**: Adoption blueprints include prerequisites, dependency checks, verification commands. Skipping this causes failures.

**Example**:
```markdown
1. Read: docs/skilled-awareness/react-testing/adoption-blueprint.md (lines 1-100)
   # Finds: "Prerequisites: Node.js 18+, SAP-020 (react-foundation) must be installed"

2. Verify prerequisites:
   Bash: node --version  # Check Node.js 18+
   Bash: ls src/features/  # Check SAP-020 structure exists

3. If prerequisites missing, install SAP-020 first:
   "SAP-021 requires SAP-020 (react-foundation). Let me install SAP-020 first..."
```

---

### Tip 3: Update AGENTS.md and CLAUDE.md After Adopting SAPs

**Scenario**: Just installed SAP-015 (beads), now update project awareness

**Best Practice**:
- ✅ **Read** current AGENTS.md to find insertion point
- ✅ **Edit** AGENTS.md to add SAP-015 patterns (targeted change)
- ✅ **Edit** CLAUDE.md to add Claude-specific patterns
- ❌ **Don't** forget this step (agent won't know SAP is available)

**Why**: Awareness files are how agents discover capabilities in future sessions.

**Example**:
```markdown
1. Read: AGENTS.md (find "## Adopted SAPs" section)

2. Edit: AGENTS.md
   # old_string: ## Adopted SAPs
   # new_string: ## Adopted SAPs\n\n### SAP-015 (task-tracking)\n**CLI**: `bd`...

3. Read: CLAUDE.md (find "## Tool Patterns" section)

4. Edit: CLAUDE.md
   # Add: "### SAP-015 Beads Usage\n**Finding work**: Bash: bd ready --json"
```

---

### Tip 4: Use Grep for Catalog Search, Read for Structured Navigation

**Scenario**: User asks "Does chora-base have CI/CD?"

**Best Practice**:
- ✅ **Quick search**: Grep for "ci-cd" or "ci/cd" in INDEX.md
- ✅ **Then**: Read AGENTS.md for SAP-005 summary (lines 1-50)
- ❌ **Don't**: Read entire INDEX.md (500+ lines) when searching for single SAP

**Why**: Grep finds keyword instantly (1-2 lines), Read entire INDEX.md costs 15k tokens.

**Example**:
```markdown
1. Grep: pattern: "ci-cd|CI/CD"
         path: docs/skilled-awareness/INDEX.md
         output_mode: content
   # Finds: "| SAP-005 | ci-cd-workflows | 1.0.0 | Draft | ..."

2. Read: docs/skilled-awareness/ci-cd-workflows/AGENTS.md (lines 1-50)
   # Quick summary of SAP-005 capabilities

3. Report to user:
   "Yes! SAP-005 (ci-cd-workflows) provides GitHub Actions for test, lint, security, docs, and release automation."
```

---

### Tip 5: Validate Links After Creating Awareness Files

**Scenario**: Just created new AGENTS.md/CLAUDE.md for a SAP

**Best Practice**:
- ✅ **After** creating awareness files: Bash: `bash scripts/validate-awareness-links.sh`
- ✅ **Fix** any broken links before committing
- ❌ **Don't** skip validation (broken links degrade agent experience)

**Why**: Link validation catches broken references before they reach production.

**Example**:
```markdown
1. Write: docs/skilled-awareness/my-new-sap/AGENTS.md

2. Write: docs/skilled-awareness/my-new-sap/CLAUDE.md

3. Validate links:
   Bash: bash scripts/validate-awareness-links.sh | grep "my-new-sap"
   # Check for "❌ BROKEN" links

4. If broken links found:
   Edit: docs/skilled-awareness/my-new-sap/AGENTS.md
   # Fix broken link paths

5. Re-validate:
   Bash: bash scripts/validate-awareness-links.sh | grep "my-new-sap"
   # Ensure all links ✅ PASS
```

---

## 4. Common Pitfalls

### Pitfall 1: Using Bash for Interactive Commands

**Problem**: Running `python setup.py` (interactive) via Bash tool, can't provide input, command hangs.

**Fix**: Use static template copy (`cp -r static-template/`) + Edit for placeholder replacement instead.

**Example**:
```markdown
❌ Bad:
Bash: python setup.py  # Prompts for input, Claude Code can't respond

✅ Good:
Bash: cp -r static-template ../my-app
Edit: ../my-app/README.md  # Replace {{project_name}} → my-app
```

---

### Pitfall 2: Writing Entire Files Instead of Editing

**Problem**: After reading a config file, using Write to create entire new version (loses comments, formatting).

**Fix**: Use Edit for targeted changes (preserves file structure).

**Example**:
```markdown
❌ Bad:
Read: .beads/config.yaml
Write: .beads/config.yaml  # Entire new file (loses comments)

✅ Good:
Read: .beads/config.yaml
Edit: .beads/config.yaml
# old_string: default_assignee: null
# new_string: default_assignee: "me"
```

---

### Pitfall 3: Not Verifying SAP Dependencies

**Problem**: Installing SAP-021 (react-testing) without SAP-020 (react-foundation), causes import errors.

**Fix**: Always check `Dependencies` in INDEX.md, install dependencies first.

**Example**:
```markdown
1. User: "Install SAP-021 (react-testing)"

2. Read: docs/skilled-awareness/INDEX.md
   # Find SAP-021 row: Dependencies: SAP-000, SAP-004, SAP-020

3. Check if SAP-020 installed:
   Bash: ls src/features/  # SAP-020 creates feature-based structure
   # If missing: "SAP-021 requires SAP-020. Let me install SAP-020 first..."

4. Install SAP-020, then SAP-021
```

---

### Pitfall 4: Reading All 5 SAP Artifacts for Quick Questions

**Problem**: User asks "What is SAP-015?", Claude reads capability-charter.md + protocol-spec.md + awareness-guide.md + adoption-blueprint.md + ledger.md (50k+ tokens).

**Fix**: Read AGENTS.md only (lines 1-50 for summary, ~1.5k tokens).

**Example**:
```markdown
User: "What is SAP-015?"

❌ Bad: Read all 5 artifacts (50k tokens)
✅ Good: Read AGENTS.md lines 1-50 (1.5k tokens)
```

---

### Pitfall 5: Not Updating Awareness Files After Adopting SAPs

**Problem**: SAP-015 installed, but AGENTS.md/CLAUDE.md not updated. Agent in next session doesn't know beads CLI is available.

**Fix**: Always Edit AGENTS.md and CLAUDE.md after installing SAP.

**Example**:
```markdown
1. Install SAP-015:
   Bash: npm install -g @beads/bd && bd init

2. Update AGENTS.md:
   Edit: AGENTS.md
   # Add SAP-015 patterns under "## Adopted SAPs"

3. Update CLAUDE.md:
   Edit: CLAUDE.md
   # Add Claude Code-specific beads usage

4. Commit:
   Bash: git add AGENTS.md CLAUDE.md .beads/ && git commit -m "feat: Adopt SAP-015 (beads task tracking)"
```

---

## 5. Integration with Other SAPs

### SAP-009 (agent-awareness)

**Pattern**: chora-base uses nested awareness pattern throughout.

**Claude Code Workflow**:
1. **Root navigation**: Read `/CLAUDE.md` for navigation tree
2. **Domain navigation**: Read `docs/skilled-awareness/CLAUDE.md` for SAP-specific patterns
3. **SAP navigation**: Read `docs/skilled-awareness/{sap-name}/CLAUDE.md` for capability details

**Tool Pattern**: Always Read CLAUDE.md files (not AGENTS.md) for Claude Code-specific guidance.

---

### SAP-015 (task-tracking)

**Pattern**: Use beads for multi-session task persistence.

**Claude Code Workflow**:
1. **Session start**: Bash: `bd ready --json` to find unblocked work
2. **Claim task**: Bash: `bd update {id} --status in_progress --assignee me`
3. **Complete task**: Bash: `bd close {id} --reason "Completed X"`

**Tool Pattern**: Bash for all beads CLI commands (read-only or state-changing).

---

### SAP-001 (inbox-coordination)

**Pattern**: Cross-repo coordination requests.

**Claude Code Workflow**:
1. **Check active work**: Read: `inbox/coordination/active.jsonl`
2. **Create coordination request**: Write: `inbox/incoming/coordination/COORD-2025-XXX.json`
3. **Broadcast**: Bash: `python scripts/broadcast-coordination.py --id COORD-2025-XXX`

**Tool Pattern**: Read for status, Write for new requests, Bash for broadcast.

---

## 6. Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2025-11-05 | Initial CLAUDE.md for SAP-002 (chora-base meta-SAP) - 3 workflows: scaffold with Bash/Write, adopt SAP with Read/Bash/Edit, navigate with Read/Grep |

---

**Next Steps**:
1. **Scaffold project?** Use Workflow 1 (Bash cp + Edit for placeholders)
2. **Adopt SAP?** Use Workflow 2 (Read blueprint, Bash install, Edit awareness)
3. **Navigate SAPs?** Use Workflow 3 (Grep for search, Read for summaries)

**Remember**: Always Read CLAUDE.md files for Claude Code-specific patterns, use Bash for non-interactive commands, Edit for targeted file modifications.
