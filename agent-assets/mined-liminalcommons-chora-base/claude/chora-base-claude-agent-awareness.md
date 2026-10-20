---
sap_id: SAP-009
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: claude_code
complexity: intermediate
estimated_reading_time: 9
progressive_loading:
  phase_1: "lines 1-160"   # Quick Start + Core Workflows
  phase_2: "lines 161-300" # Advanced Operations
  phase_3: "full"          # Complete including tips and pitfalls
phase_1_token_estimate: 3500
phase_2_token_estimate: 7000
phase_3_token_estimate: 10000
---

# Agent Awareness (SAP-009) - Claude-Specific Awareness

**SAP ID**: SAP-009
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-04

---

## 📖 Quick Reference

**New to SAP-009?** → Read **[README.md](README.md)** first (8-min read)

The README provides:
- 🚀 **Quick Start** - 5-minute guide to nested AGENTS.md/CLAUDE.md pattern with examples
- 📚 **Time Savings** - 60-70% token reduction through progressive loading and domain-specific awareness files
- 🎯 **5-Level Hierarchy** - Root → domain → SAP → feature → component navigation with "nearest file wins"
- 🔧 **Progressive Loading** - Three phases (0-10k, 10-50k, 50-200k tokens) optimize context usage
- 📊 **Universal Adoption** - 100% of 32+ SAPs use this pattern for agent discoverability
- 🔗 **Integration** - Works with all SAPs (universal foundation for agent awareness)

This CLAUDE.md provides: Claude Code-specific workflows using Read tool for progressive loading, domain-specific navigation patterns.

---

## Quick Start for Claude

This file provides **Claude Code-specific patterns** for using the AGENTS.md/CLAUDE.md awareness file system.

### First-Time Session

1. Read [AGENTS.md](AGENTS.md) for generic awareness patterns
2. Use this file for Claude Code tool integration (Read for awareness files, progressive loading)
3. **Always read nearest AGENTS.md + CLAUDE.md** for your working directory

### Nearest File Wins Pattern

```
/AGENTS.md                                           # Layer 1: Root context
/docs/skilled-awareness/inbox/AGENTS.md               # Layer 2: Domain context
/docs/skilled-awareness/inbox/CLAUDE.md               # Layer 2: Claude-specific
```

**Rule**: Read awareness files closest to code you're editing

---

## Claude Code Awareness Workflows

### Workflow 1: Discovering Awareness Files with Read

```markdown
User: "Help me work on the inbox"

Claude (Phase 1: Discover Awareness - 0-5k tokens):
1. Identify working directory:
   User wants to work on: inbox/

2. Check for domain-specific awareness files:
   Read docs/skilled-awareness/inbox/AGENTS.md

3. Also read Claude-specific file:
   Read docs/skilled-awareness/inbox/CLAUDE.md

Claude (Phase 2: Apply Context - 5-15k tokens):
4. Parse awareness file sections:
   - User Signal Patterns → Understand user intent mappings
   - Common Workflows → Know available operations
   - Best Practices → Follow domain conventions
   - Common Pitfalls → Avoid known errors

5. Use awareness context to complete task:
   # Now have domain-specific context for inbox operations

Claude (response to user):
"✅ Loaded inbox awareness context:
   - AGENTS.md: 4 user signal patterns, 3 workflows
   - CLAUDE.md: Read/Edit/Bash patterns for inbox operations

   Ready to help with inbox. What would you like to do?"

Result: Domain-specific context loaded, ready for work
```

---

### Workflow 2: Progressive Context Loading with Read

```markdown
User: "Refactor the backend gateway"

Claude (Phase 1: Essential Context - 0-10k tokens):
1. Read nearest awareness file:
   Read docs/skilled-awareness/gateway/AGENTS.md
   Read docs/skilled-awareness/gateway/CLAUDE.md

2. Read only files being edited:
   Read src/gateway/server.py

Claude (Phase 2: Extended Context - 10-30k tokens):
3. If needed, read related modules:
   Read src/gateway/config.py
   Read tests/test_gateway.py

4. Check protocol-spec for contracts:
   Read docs/skilled-awareness/gateway/protocol-spec.md

Claude (Phase 3: Full Context - 30-50k tokens, only if complex):
5. If major refactor, read dependencies:
   Read src/gateway/*.py (all gateway modules)

6. Read integration tests:
   Read tests/integration/test_gateway_*.py

Claude (response to user):
"✅ Context loaded progressively:
   - Phase 1 (8k tokens): AGENTS.md + CLAUDE.md + server.py
   - Phase 2 (15k tokens): config.py + tests

   Ready for refactoring. Current token usage: 23k/200k"

Result: Optimal context loaded without token waste
```

---

### Workflow 3: Creating Awareness Files with Write

```markdown
User: "Create awareness file for new metrics module"

Claude (Phase 1: Check Structure - 0-5k tokens):
1. Identify target directory:
   New module: docs/skilled-awareness/metrics-tracking/

2. Check if awareness files already exist:
   Bash: ls docs/skilled-awareness/metrics-tracking/AGENTS.md 2>/dev/null
   # Not found → Need to create

Claude (Phase 2: Read Template - 5-15k tokens):
3. Read protocol-spec for structure requirements:
   Read docs/skilled-awareness/agent-awareness/protocol-spec.md
   # Section 4: Content guidelines

4. Read example awareness file:
   Read docs/skilled-awareness/docker-operations/AGENTS.md
   # Use as template

Claude (Phase 3: Create Files - 15-30k tokens):
5. Write AGENTS.md (generic context):
   Write docs/skilled-awareness/metrics-tracking/AGENTS.md
   # Include: User signals, workflows, best practices, pitfalls

6. Write CLAUDE.md (Claude-specific):
   Write docs/skilled-awareness/metrics-tracking/CLAUDE.md
   # Include: Tool patterns (Read, Edit, Bash), progressive loading

Claude (Phase 4: Validate - 30-35k tokens):
7. Validate structure:
   Bash: python scripts/sap-evaluator.py --deep SAP-013
   # Check awareness file requirements

Claude (response to user):
"✅ Created awareness files for metrics-tracking:
   - AGENTS.md: 5 workflows, 4 user signal patterns
   - CLAUDE.md: 3 workflows, tool-specific patterns
   - Validation: PASS (protocol-spec compliant)

   Files: docs/skilled-awareness/metrics-tracking/{AGENTS.md,CLAUDE.md}"

Result: New awareness files created following protocol
```

---

### Workflow 4: Optimizing Token Usage with Progressive Loading

```markdown
User: "Fix small bug in script-usage.jsonl parsing"

Claude (Phase 1: Minimal Context - 0-5k tokens):
1. Read only essential file:
   Read .chora/memory/events/script-usage.jsonl
   # Lines 1-50 (just see structure)

2. Identify bug:
   # Parse error on line 42

3. Fix bug:
   Edit .chora/memory/events/script-usage.jsonl
   # Fix JSON syntax error

4. Verify:
   Bash: jq . .chora/memory/events/script-usage.jsonl > /dev/null

Claude (response to user):
"✅ Bug fixed with minimal context:
   - Token usage: 3k tokens (0-5k Phase)
   - No awareness file needed (simple fix)
   - Verified: jq parses successfully

   Saved 190k tokens by avoiding full context load!"

Result: Efficient fix using minimal context

---

Contrast: If loading full context unnecessarily

Claude (AVOID THIS PATTERN):
1. Read entire codebase awareness files (20k tokens)
2. Read all event logs (50k tokens)
3. Read all memory system docs (30k tokens)
4. Total: 100k tokens for 1-line JSON fix ❌

**Key**: Match context to task complexity
```

---

## Claude-Specific Tips

### Tip 1: Read Nearest AGENTS.md + CLAUDE.md First

**Pattern**:
```markdown
# When starting work on directory:
Read <directory>/AGENTS.md        # Generic context
Read <directory>/CLAUDE.md        # Claude-specific patterns

# ALWAYS read both if they exist
```

**Why**: CLAUDE.md contains tool-specific patterns (Read, Edit, Bash) optimized for Claude Code

---

### Tip 2: Use Progressive Loading for Large Tasks

**Pattern**:
```markdown
# Phase 1 (0-10k): Essential only
Read <directory>/AGENTS.md
Read files being edited

# Phase 2 (10-30k): Add related modules IF NEEDED
Read related modules
Read tests

# Phase 3 (30-50k+): Full context ONLY for complex refactors
Read all modules in directory
Read integration tests
```

**Why**: Prevents token waste, maintains context budget

---

### Tip 3: Check Protocol-Spec for Validation Criteria

**Pattern**:
```markdown
# When creating awareness files:
Read docs/skilled-awareness/agent-awareness/protocol-spec.md
# Section 4: Content guidelines
# Section 9.5: Self-evaluation criteria

# Validate structure:
Bash: python scripts/sap-evaluator.py --deep SAP-XXX
```

**Why**: Ensures awareness files follow SAP-009 protocol

---

### Tip 4: Use Glob to Discover Awareness Files

**Pattern**:
```markdown
# Find all AGENTS.md files:
Glob: pattern="**/AGENTS.md"

# Find all CLAUDE.md files:
Glob: pattern="**/CLAUDE.md"

# Check specific directory:
Bash: ls docs/skilled-awareness/*/AGENTS.md
```

**Why**: Quickly discover available awareness files

---

### Tip 5: Reference YAML Frontmatter for Progressive Loading

**Pattern**:
```markdown
# Read awareness file frontmatter:
Read docs/skilled-awareness/docker-operations/CLAUDE.md
# Check YAML:
#   phase_1: "lines 1-110"
#   phase_2: "lines 111-200"
#   phase_3: "full"

# Load appropriate phase:
# Small task → Phase 1 only
# Medium task → Phase 1 + Phase 2
# Complex task → Full
```

**Why**: YAML frontmatter specifies optimal loading phases

---

## Common Pitfalls for Claude Code

### Pitfall 1: Not Reading Nearest Awareness File

**Problem**: Work on domain-specific code without reading domain AGENTS.md/CLAUDE.md

**Fix**: ALWAYS read nearest awareness files

```markdown
# ❌ BAD: Work on inbox without reading awareness
User: "Help with inbox"
Claude: Starts working without domain context

# ✅ GOOD: Read awareness first
User: "Help with inbox"
Claude: Read docs/skilled-awareness/inbox/AGENTS.md
Claude: Read docs/skilled-awareness/inbox/CLAUDE.md
# Now have domain-specific context
```

**Why**: Awareness files contain domain patterns, avoid reinventing solutions

---

### Pitfall 2: Loading Full Context for Simple Tasks

**Problem**: Read entire codebase awareness files for 1-line fix

**Fix**: Match context to task complexity

```markdown
# ❌ BAD: Load everything
Read all AGENTS.md files (50k tokens)
Read all protocol-specs (100k tokens)
# For: Fix typo in README.md

# ✅ GOOD: Minimal context
Read README.md
Edit README.md
# Total: 1k tokens
```

**Why**: Token budget is finite (200k), save for complex tasks

---

### Pitfall 3: Not Creating Awareness Files for New Domains

**Problem**: Create new SAP directory without AGENTS.md/CLAUDE.md

**Fix**: ALWAYS create awareness files for new domains

```markdown
# After creating new SAP:
Write docs/skilled-awareness/my-sap/AGENTS.md
Write docs/skilled-awareness/my-sap/CLAUDE.md

# Validate:
Bash: python scripts/sap-evaluator.py --deep SAP-XXX
```

**Why**: Future agents need domain context, awareness files enable discovery

---

### Pitfall 4: Not Following Protocol-Spec Structure

**Problem**: Create awareness file with missing required sections

**Fix**: Follow protocol-spec content guidelines

```markdown
# Read guidelines first:
Read docs/skilled-awareness/agent-awareness/protocol-spec.md
# Section 4: Content guidelines

# Required sections:
# - User Signal Patterns
# - Common Workflows
# - Best Practices
# - Common Pitfalls
# - Integration with Other SAPs
```

**Why**: Consistent structure enables agents to parse awareness files predictably

---

### Pitfall 5: Not Reading CLAUDE.md (Only AGENTS.md)

**Problem**: Read AGENTS.md but skip CLAUDE.md for same directory

**Fix**: ALWAYS read both if they exist

```markdown
# ❌ BAD: Read only AGENTS.md
Read docs/skilled-awareness/docker-operations/AGENTS.md
# Missing Claude-specific tool patterns

# ✅ GOOD: Read both
Read docs/skilled-awareness/docker-operations/AGENTS.md
Read docs/skilled-awareness/docker-operations/CLAUDE.md
# Have generic + Claude-specific patterns
```

**Why**: CLAUDE.md contains tool-specific optimizations (Read, Edit, Bash patterns)

---

## Support & Resources

**SAP-009 Documentation**:
- [AGENTS.md](AGENTS.md) - Generic awareness patterns
- [Capability Charter](capability-charter.md) - Design principles, nearest-file-wins
- [Protocol Spec](protocol-spec.md) - File structure, content guidelines
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [Ledger](ledger.md) - Awareness adoption tracking

**Awareness File Examples**:
- [docker-operations/CLAUDE.md](../docker-operations/CLAUDE.md) - Tool patterns
- [project-bootstrap/CLAUDE.md](../project-bootstrap/CLAUDE.md) - Progressive loading
- [memory-system/CLAUDE.md](../memory-system/CLAUDE.md) - Grep/Read/Bash patterns

**Related SAPs**:
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - Awareness file generation
- [SAP-008 (automation-scripts)](../automation-scripts/) - Script awareness
- [SAP-010 (memory-system)](../memory-system/) - Memory awareness
- [SAP-019 (sap-self-evaluation)](../sap-self-evaluation/) - Evaluation awareness

---

## Version History

- **1.0.0** (2025-11-04): Initial CLAUDE.md for SAP-009
  - 4 workflows: Discover with Read, Progressive Loading, Create with Write, Optimize Token Usage
  - Tool patterns: Read for awareness files, Write for creation, Bash for validation
  - 5 Claude-specific tips, 5 common pitfalls
  - Progressive loading phases (essential → extended → full)
  - Nearest-file-wins pattern documentation

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for generic awareness patterns
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [capability-charter.md](capability-charter.md) for design rationale
4. Discover awareness files: `Glob: pattern="**/AGENTS.md"`
