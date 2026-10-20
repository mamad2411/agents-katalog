---
sap_id: SAP-000
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 11
progressive_loading:
  phase_1: "lines 1-200"   # Quick Start + Core Workflows
  phase_2: "lines 201-400" # Advanced Operations
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 4500
phase_2_token_estimate: 9000
phase_3_token_estimate: 12000
---

# SAP Framework (SAP-000) - Claude-Specific Awareness

**SAP ID**: SAP-000
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for working with the SAP Framework.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic SAP workflows
2. Use this file for Claude Code tool integration (Read for artifacts, Write for creation, Bash for validation)
3. Always validate SAP structure before committing

### SAP Structure

Every SAP has exactly 5 artifacts:

```
docs/skilled-awareness/<capability-name>/
├── capability-charter.md      # Read for problem/scope
├── protocol-spec.md            # Read for technical contract
├── awareness-guide.md          # Read for workflows
├── adoption-blueprint.md       # Read for installation
└── ledger.md                   # Edit for adoption tracking
```

---

## Claude Code SAP Workflows

### Workflow 1: Creating New SAP with Write and Bash

```markdown
User: "Create new SAP for metrics tracking"

Claude (Phase 1: Generate ID - 0-5k tokens):
1. Find next available SAP ID:
   Bash: ls docs/skilled-awareness/ | grep -E "^[a-z]+-[a-z]+" | wc -l
   # Count: 25 SAPs → Next: SAP-025

2. Create SAP directory:
   Bash: mkdir -p docs/skilled-awareness/metrics-tracking

Claude (Phase 2: Create Artifacts - 5-50k tokens):
3. Read template for structure:
   Read docs/skilled-awareness/document-templates.md

4. Create capability-charter.md:
   Write docs/skilled-awareness/metrics-tracking/capability-charter.md
   ---
   sap_id: SAP-025
   version: 1.0.0
   status: draft
   last_updated: 2025-11-04
   ---

   # Capability Charter: Metrics Tracking

   ## 1. Problem Statement
   [Problem description based on user input]

   ## 2. Proposed Solution
   [Solution approach]

   [... remaining sections ...]

5. Create protocol-spec.md:
   Write docs/skilled-awareness/metrics-tracking/protocol-spec.md
   # Technical contract with schemas, interfaces

6. Create awareness-guide.md:
   Write docs/skilled-awareness/metrics-tracking/awareness-guide.md
   # Agent workflows and patterns

7. Create adoption-blueprint.md:
   Write docs/skilled-awareness/metrics-tracking/adoption-blueprint.md
   # Installation and validation steps

8. Create ledger.md:
   Write docs/skilled-awareness/metrics-tracking/ledger.md
   # Adoption tracking table

Claude (Phase 3: Validate - 50-60k tokens):
9. Validate structure:
   Bash: python scripts/sap-evaluator.py --deep SAP-025

10. Update catalog:
    Read sap-catalog.json
    Edit sap-catalog.json
    # Add entry for SAP-025

Claude (response to user):
"✅ Created SAP-025 (metrics-tracking):
   - 5 artifacts generated
   - YAML frontmatter added to all files
   - Validation: PASS
   - Catalog updated

   Files created:
   - capability-charter.md (2.5k tokens)
   - protocol-spec.md (4k tokens)
   - awareness-guide.md (3k tokens)
   - adoption-blueprint.md (2k tokens)
   - ledger.md (0.5k tokens)

   Next: Add AGENTS.md and CLAUDE.md awareness files"

Result: New SAP created with all required artifacts
```

---

### Workflow 2: Installing SAP with Read and Bash

```markdown
User: "Install SAP-010 (memory system)"

Claude (Phase 1: Read Blueprint - 0-10k tokens):
1. Read adoption blueprint:
   Read docs/skilled-awareness/memory-system/adoption-blueprint.md

2. Check prerequisites from blueprint:
   Bash: python --version  # Check Python 3.11+
   Bash: which jq          # Check jq installed

Claude (Phase 2: Execute Installation - 10-30k tokens):
3. Follow installation steps from blueprint:
   # Step 1: Create memory structure
   Bash: mkdir -p .chora/memory/{events,knowledge/notes,agent-profiles}

   # Step 2: Initialize event logs
   Bash: touch .chora/memory/events/{script-usage,errors,coordination}.jsonl

   # Step 3: Create agent profile
   Write .chora/memory/agent-profiles/claude-sonnet-4.yaml
   agent_id: claude-sonnet-4
   version: 1.0.0
   preferences: {}
   capabilities: {}

Claude (Phase 3: Validate - 30-40k tokens):
4. Run validation from blueprint:
   Bash: ls .chora/memory/events/*.jsonl | wc -l
   # Expected: 3 files

5. Test event logging:
   Bash: echo '{"timestamp":"2025-11-04T10:30:00Z","event":"test"}' >> .chora/memory/events/coordination.jsonl
   Bash: tail -1 .chora/memory/events/coordination.jsonl | jq .
   # Verify JSON valid

Claude (Phase 4: Update Ledger - 40-50k tokens):
6. Read ledger:
   Read docs/skilled-awareness/memory-system/ledger.md

7. Add adoption entry:
   Edit docs/skilled-awareness/memory-system/ledger.md
   # Add row:
   | 2025-11-04 | chora-base | 1.0.0 | L0 (Aware) | Initial installation |

Claude (response to user):
"✅ SAP-010 (memory-system) installed:
   - Prerequisites: Python 3.11 ✅, jq ✅
   - Memory structure: Created
   - Event logs: Initialized (3 files)
   - Agent profile: Created
   - Validation: PASS
   - Ledger: Updated

   You can now use:
   - Event logging: echo '{...}' >> .chora/memory/events/coordination.jsonl
   - Knowledge notes: Write .chora/memory/knowledge/notes/NNN-topic.md

   Next: Log first event to start using memory"

Result: SAP-010 installed and validated
```

---

### Workflow 3: Validating SAP Structure with Bash

```markdown
User: "Validate SAP-003"

Claude (Phase 1: Quick Check - 0-5k tokens):
1. Check artifacts exist:
   Bash: ls docs/skilled-awareness/project-bootstrap/ | grep -E "(capability-charter|protocol-spec|awareness-guide|adoption-blueprint|ledger)\.md"

   Output:
   capability-charter.md
   protocol-spec.md
   awareness-guide.md
   adoption-blueprint.md
   ledger.md
   # All 5 present ✅

Claude (Phase 2: Deep Validation - 5-15k tokens):
2. Run evaluator:
   Bash: python scripts/sap-evaluator.py --deep SAP-003

   Output:
   SAP-003 (project-bootstrap) Evaluation
   ======================================
   Status: PASS
   Level: L3 (Autonomous)

   Artifact Checks:
   ✅ capability-charter.md exists (3.2k tokens)
   ✅ protocol-spec.md exists (5.8k tokens)
   ✅ awareness-guide.md exists (4.1k tokens)
   ✅ adoption-blueprint.md exists (2.9k tokens)
   ✅ ledger.md exists (1.2k tokens)

   YAML Frontmatter:
   ✅ All artifacts have valid frontmatter
   ✅ SAP ID consistent: SAP-003
   ✅ Version format valid: 1.0.0

   Awareness Files:
   ✅ AGENTS.md exists
   ✅ CLAUDE.md exists

   Gaps: 0 P1, 1 P2
   P2 Gaps:
   - Coverage variance: AGENTS.md has 6 workflows, CLAUDE.md has 4 (33% difference)

Claude (Phase 3: Check Frontmatter - 15-20k tokens):
3. Verify YAML in each artifact:
   Bash: for file in capability-charter protocol-spec awareness-guide adoption-blueprint ledger; do echo "=== ${file}.md ===" && head -10 "docs/skilled-awareness/project-bootstrap/${file}.md" | grep -A 5 "^---$" | head -6; done

   # Shows frontmatter for each file

Claude (response to user):
"✅ SAP-003 validation results:
   - All 5 artifacts present ✅
   - YAML frontmatter valid ✅
   - Awareness files present ✅
   - Status: PASS (L3 Autonomous)
   - Gaps: 0 P1, 1 P2 (acceptable)

   P2 gap (low priority):
   - AGENTS.md has 6 workflows, CLAUDE.md has 4
   - Reason: Different organization (pattern tables vs explicit workflows)
   - Impact: Low - both provide equivalent guidance

   SAP-003 is production-ready."

Result: Validation complete, SAP structure confirmed
```

---

### Workflow 4: Upgrading SAP Version with Read and Edit

```markdown
User: "Upgrade SAP-010 to v1.1.0"

Claude (Phase 1: Check Current Version - 0-10k tokens):
1. Read ledger to find current version:
   Read docs/skilled-awareness/memory-system/ledger.md
   # Last entry: v1.0.0

2. Read protocol-spec for migration guide:
   Read docs/skilled-awareness/memory-system/protocol-spec.md
   # Section 8: Versioning & Migration

Claude (Phase 2: Apply Migration - 10-40k tokens):
3. Follow migration steps from protocol-spec:
   # Migration v1.0.0 → v1.1.0:
   # - Add event tag taxonomy support
   # - No breaking changes

4. Update memory structure:
   Bash: mkdir -p schemas/
   Write schemas/event-tag-taxonomy.yaml
   # New taxonomy file for v1.1.0

5. Update event logging script:
   Read scripts/query-events-by-tag.py
   # Already exists, no changes needed

Claude (Phase 3: Update Artifacts - 40-60k tokens):
6. Update version in all artifacts:
   Read docs/skilled-awareness/memory-system/capability-charter.md
   Edit docs/skilled-awareness/memory-system/capability-charter.md
   # old_string: version: 1.0.0
   # new_string: version: 1.1.0

   # Repeat for protocol-spec.md, awareness-guide.md, adoption-blueprint.md, ledger.md

7. Update YAML frontmatter in AGENTS.md and CLAUDE.md:
   Edit docs/skilled-awareness/memory-system/AGENTS.md
   # Update version field

   Edit docs/skilled-awareness/memory-system/CLAUDE.md
   # Update version field

Claude (Phase 4: Validate Upgrade - 60-70k tokens):
8. Run validation:
   Bash: python scripts/sap-evaluator.py --deep SAP-010

9. Update ledger with upgrade event:
   Edit docs/skilled-awareness/memory-system/ledger.md
   # Add row:
   | 2025-11-04 | chora-base | 1.1.0 | L3 (Autonomous) | Upgraded from v1.0.0, added event tagging |

Claude (response to user):
"✅ SAP-010 upgraded to v1.1.0:
   - Migration: v1.0.0 → v1.1.0 (backward compatible)
   - Changes:
     • Added event tag taxonomy (schemas/event-tag-taxonomy.yaml)
     • Added query-events-by-tag.py script
     • No breaking changes
   - Artifacts updated: 7 files (5 SAP artifacts + 2 awareness files)
   - Validation: PASS
   - Ledger: Updated with upgrade entry

   New capabilities:
   - Query events by tag: python scripts/query-events-by-tag.py --tags domain:tag

   Next: Test event tagging workflow"

Result: SAP-010 upgraded to v1.1.0
```

---

### Workflow 5: Querying SAP Catalog with Read and Grep

```markdown
User: "Show me all active SAPs"

Claude (Phase 1: Read Catalog - 0-5k tokens):
1. Read SAP catalog:
   Read sap-catalog.json

Claude (Phase 2: Filter by Status - 5-10k tokens):
2. Use jq to filter active SAPs:
   Bash: cat sap-catalog.json | jq '.saps[] | select(.status=="active") | {id: .sap_id, name: .name, version: .version}'

   Output:
   {"id":"SAP-000","name":"sap-framework","version":"1.0.0"}
   {"id":"SAP-001","name":"inbox","version":"1.0.0"}
   {"id":"SAP-003","name":"project-bootstrap","version":"1.0.0"}
   {"id":"SAP-008","name":"automation-scripts","version":"1.0.0"}
   {"id":"SAP-009","name":"agent-awareness","version":"1.1.0"}
   {"id":"SAP-010","name":"memory-system","version":"1.1.0"}
   ...

Claude (Phase 3: Check Adoption Levels - 10-20k tokens):
3. For each SAP, check ledger for adoption level:
   Bash: for sap in sap-framework inbox project-bootstrap automation-scripts agent-awareness memory-system; do echo "=== $sap ===" && tail -1 "docs/skilled-awareness/$sap/ledger.md" | grep -o "L[0-3]"; done

   Output:
   === sap-framework ===
   L2
   === inbox ===
   L2
   === project-bootstrap ===
   L3
   === automation-scripts ===
   L3
   === agent-awareness ===
   L3
   === memory-system ===
   L3

Claude (response to user):
"✅ Active SAPs (6 total):

   **Level 3 (Autonomous - Strategic Capability)**:
   - SAP-003: project-bootstrap (v1.0.0)
   - SAP-008: automation-scripts (v1.0.0)
   - SAP-009: agent-awareness (v1.1.0)
   - SAP-010: memory-system (v1.1.0)

   **Level 2 (Adopting - Embedded in Practice)**:
   - SAP-000: sap-framework (v1.0.0)
   - SAP-001: inbox (v1.0.0)

   **Adoption Maturity**: 67% at L3, 33% at L2

   All 6 SAPs have:
   - Complete 5-artifact structure ✅
   - Awareness files (AGENTS.md + CLAUDE.md) ✅
   - Active maintenance ✅

   Next: Review SAP-000 and SAP-001 for L3 promotion criteria"

Result: Catalog queried, SAPs listed by adoption level
```

---

## Claude-Specific Tips

### Tip 1: Use Write for All 5 Artifacts When Creating SAP

**Pattern**:
```markdown
# Create all 5 artifacts in sequence
Write docs/skilled-awareness/<name>/capability-charter.md
Write docs/skilled-awareness/<name>/protocol-spec.md
Write docs/skilled-awareness/<name>/awareness-guide.md
Write docs/skilled-awareness/<name>/adoption-blueprint.md
Write docs/skilled-awareness/<name>/ledger.md
```

**Why**: Write tool ensures consistent YAML frontmatter and structure

---

### Tip 2: Use Bash for SAP Validation, Not Manual Checks

**Pattern**:
```markdown
# ✅ GOOD: Automated validation
Bash: python scripts/sap-evaluator.py --deep SAP-025

# ❌ BAD: Manual artifact checks
Read each artifact individually, check structure manually
```

**Why**: Evaluator checks YAML, links, sections comprehensively

---

### Tip 3: Read Adoption Blueprint Before Installation

**Pattern**:
```markdown
# ALWAYS read blueprint first
Read docs/skilled-awareness/<name>/adoption-blueprint.md

# THEN follow installation steps
# (Create dirs, install deps, validate)
```

**Why**: Blueprint documents prerequisites, validation, configuration

---

### Tip 4: Use Edit for Version Updates Across Artifacts

**Pattern**:
```markdown
# When upgrading SAP version:
# Update ALL artifacts with Edit tool

Edit docs/skilled-awareness/<name>/capability-charter.md
# old_string: version: 1.0.0
# new_string: version: 1.1.0

# Repeat for all 5 artifacts + awareness files
```

**Why**: Consistent versioning across all SAP files

---

### Tip 5: Use jq for Catalog Queries

**Pattern**:
```markdown
# Filter catalog by various criteria
Bash: cat sap-catalog.json | jq '.saps[] | select(.status=="active")'
Bash: cat sap-catalog.json | jq '.saps[] | select(.version | startswith("2."))'
Bash: cat sap-catalog.json | jq '.saps[] | {id: .sap_id, name: .name}'
```

**Why**: jq provides powerful JSON filtering

---

## Common Pitfalls for Claude Code

### Pitfall 1: Creating Incomplete SAP (Missing Artifacts)

**Problem**: Create SAP with only 3-4 artifacts instead of 5

**Fix**: ALWAYS create all 5 artifacts

```markdown
# ❌ BAD: Incomplete SAP
Write capability-charter.md
Write protocol-spec.md
# Missing awareness-guide, adoption-blueprint, ledger

# ✅ GOOD: Complete SAP
Write capability-charter.md
Write protocol-spec.md
Write awareness-guide.md
Write adoption-blueprint.md
Write ledger.md
```

**Why**: Missing artifacts cause validation failures, reduce adoption

---

### Pitfall 2: Forgetting YAML Frontmatter

**Problem**: Create artifact file without YAML frontmatter

**Fix**: ALWAYS start files with frontmatter

```markdown
# ❌ BAD: No frontmatter
# Capability Charter
...

# ✅ GOOD: Frontmatter first
---
sap_id: SAP-025
version: 1.0.0
status: draft
last_updated: 2025-11-04
---

# Capability Charter
...
```

**Why**: Frontmatter enables parsing, validation, metadata extraction

---

### Pitfall 3: Not Updating Ledger After Adoption Events

**Problem**: Install SAP or upgrade version but don't update ledger

**Fix**: Update ledger immediately after events

```markdown
# After installation or upgrade:
Edit docs/skilled-awareness/<name>/ledger.md
# Add row with current date, version, level
```

**Why**: Ledger tracks adoption timeline, enables trend analysis

---

### Pitfall 4: Not Validating Before Committing

**Problem**: Create or modify SAP artifacts without running evaluator

**Fix**: ALWAYS validate before git commit

```markdown
# After SAP changes:
Bash: python scripts/sap-evaluator.py --deep SAP-025

# Only commit if PASS
git add docs/skilled-awareness/<name>/
git commit -m "feat(sap-025): ..."
```

**Why**: Catch structural issues early, prevent broken SAPs

---

### Pitfall 5: Inconsistent Versions Across Artifacts

**Problem**: Update version in capability-charter.md but forget protocol-spec.md

**Fix**: Update version in ALL artifacts simultaneously

```markdown
# Use Edit for each artifact:
Edit capability-charter.md (version: 1.0.0 → 1.1.0)
Edit protocol-spec.md (version: 1.0.0 → 1.1.0)
Edit awareness-guide.md (version: 1.0.0 → 1.1.0)
Edit adoption-blueprint.md (version: 1.0.0 → 1.1.0)
Edit ledger.md (version: 1.0.0 → 1.1.0)
Edit AGENTS.md (version: 1.0.0 → 1.1.0)
Edit CLAUDE.md (version: 1.0.0 → 1.1.0)
```

**Why**: Version consistency critical for validation, adoption tracking

---

## Support & Resources

**SAP-000 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic SAP framework workflows
- [Capability Charter](capability-charter.md) - SAP framework problem and scope
- [Protocol Spec](protocol-spec.md) - Technical contract and artifact schemas
- [Awareness Guide](awareness-guide.md) - Detailed SAP workflows
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Adoption tracking

**Templates**:
- [Document Templates](../document-templates.md) - Templates for all 5 artifacts
- [SAP Catalog Schema](../../schemas/sap-catalog.schema.json) - Catalog format

**Scripts**:
- `scripts/sap-evaluator.py` - Validate SAP structure
- `scripts/generate-sap.py` - Generate new SAP from template
- `scripts/batch-evaluate-saps.py` - Validate all SAPs

**Related SAPs**:
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - SAP generation during project init
- [SAP-009 (agent-awareness)](../agent-awareness/) - Awareness file patterns
- [SAP-019 (sap-self-evaluation)](../sap-self-evaluation/) - Validation and evaluation

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-000
  - 5 workflows: Create with Write/Bash, Install with Read/Bash, Validate with Bash, Upgrade with Read/Edit, Query with Read/Grep
  - Tool patterns: Write for artifacts, Read for blueprints, Edit for updates, Bash for validation
  - 5 Claude-specific tips, 5 common pitfalls
  - jq patterns for catalog queries

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic SAP workflows
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [document-templates.md](../document-templates.md) for artifact templates
4. Create new SAP: Follow Workflow 1 (Create New SAP)
5. Validate: `python scripts/sap-evaluator.py --deep SAP-NNN`
