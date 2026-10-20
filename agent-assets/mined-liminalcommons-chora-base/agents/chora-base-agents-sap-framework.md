---
sap_id: SAP-000
version: 1.0.0
status: active
last_updated: 2025-11-04
type: reference
audience: agents
complexity: intermediate
estimated_reading_time: 12
progressive_loading:
  phase_1: "lines 1-240"   # Quick Reference + Core Workflows
  phase_2: "lines 241-480" # Advanced Workflows + Governance
  phase_3: "full"          # Complete including troubleshooting
phase_1_token_estimate: 5000
phase_2_token_estimate: 10000
phase_3_token_estimate: 13000
---

# SAP Framework (SAP-000) - Agent Awareness

**SAP ID**: SAP-000
**Last Updated**: 2025-11-04
**Audience**: Generic AI Coding Agents

---

## 📖 Quick Reference

**New to SAP-000?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - 30-minute guide to understanding SAP structure and generating your first SAP
- 📚 **Time Savings** - 90% documentation time reduction (30 hours manual → 3 hours with templates)
- 🎯 **Standardized Structure** - 5 required artifacts (capability-charter, protocol-spec, awareness-guide, adoption-blueprint, ledger)
- 🔧 **Validation Automation** - Automated scripts enforce README structure, Quick Reference format, and link integrity
- 📊 **Progressive Loading** - Three-tier token strategy (300-500 → 2-5k → 10-50k tokens) optimizes agent context usage
- 🔗 **Integration** - Works with SAP-019 (Self-Evaluation), SAP-029 (Generation), SAP-016 (Link Validation)

This AGENTS.md provides: Agent-specific workflows for creating, validating, and upgrading SAPs, including command-line patterns and troubleshooting decision trees.

### SAP Structure

Every SAP consists of 5 required artifacts:

```
docs/skilled-awareness/<capability-name>/
├── capability-charter.md      # Problem, scope, outcomes
├── protocol-spec.md            # Technical contract
├── awareness-guide.md          # Agent execution patterns
├── adoption-blueprint.md       # Installation steps
└── ledger.md                   # Adopter tracking
```

### SAP Lifecycle States

| State | Meaning | When to Use |
|-------|---------|-------------|
| **Draft** | Being authored | Initial creation |
| **Pilot** | Testing with early adopters | Beta phase |
| **Active** | Production-ready | General use |
| **Deprecated** | Being phased out | Migration period |
| **Archived** | No longer maintained | Historical reference |

---

## User Signal Patterns

### SAP Creation

| User Says | Formal Action | Expected Time | Notes |
|-----------|---------------|---------------|-------|
| "create new SAP" | generate_sap_artifacts() | 15-30 min | Generate 5 artifacts |
| "package this capability" | generate_sap_artifacts() | 15-30 min | Same as above |
| "new capability package" | generate_sap_artifacts() | 15-30 min | Variation |
| "generate SAP for X" | generate_sap_artifacts(name=X) | 15-30 min | With parameter |

### SAP Installation

| User Says | Formal Action | Expected Time | Notes |
|-----------|---------------|---------------|-------|
| "install SAP-NNN" | install_sap(id="SAP-NNN") | 5-15 min | Follow adoption blueprint |
| "adopt SAP-NNN" | install_sap(id="SAP-NNN") | 5-15 min | Same intent |
| "enable capability X" | install_sap(name=X) | 5-15 min | By name |

### SAP Validation

| User Says | Formal Action | Expected Time | Notes |
|-----------|---------------|---------------|-------|
| "validate SAP-NNN" | validate_sap_structure(id="SAP-NNN") | 1-2 min | Check artifacts |
| "check SAP structure" | validate_sap_structure() | 1-2 min | All SAPs |
| "verify artifacts" | validate_sap_structure() | 1-2 min | Variation |
| "lint SAP-NNN" | validate_sap_structure(id="SAP-NNN") | 1-2 min | Same intent |

### SAP Upgrade

| User Says | Formal Action | Expected Time | Notes |
|-----------|---------------|---------------|-------|
| "upgrade SAP-NNN" | upgrade_sap(id="SAP-NNN") | 10-30 min | Follow migration |
| "migrate to v2.0.0" | upgrade_sap(version="2.0.0") | 10-30 min | Specific version |
| "update SAP-NNN" | upgrade_sap(id="SAP-NNN") | 10-30 min | Variation |

---

## Common Workflows

### Workflow 1: Create New SAP (15-30 minutes)

**User signal**: "Create new SAP", "Package this capability", "Generate SAP for X"

**Purpose**: Generate 5 required artifacts for new capability

**Steps**:
1. Identify capability to package:
   - What problem does it solve?
   - What are the key workflows?
   - Who are the stakeholders?

2. Generate SAP ID:
   ```bash
   # Find next available ID
   ls docs/skilled-awareness/ | grep -E "^[0-9]+-" | sort -n | tail -1
   # Last: SAP-024 → Next: SAP-025
   ```

3. Create SAP directory:
   ```bash
   mkdir -p docs/skilled-awareness/capability-name
   ```

4. Generate 5 artifacts using template:
   ```bash
   # Read template structure
   cat docs/skilled-awareness/document-templates.md

   # Create each artifact:
   # 1. capability-charter.md - Problem, scope, outcomes
   # 2. protocol-spec.md - Technical contract
   # 3. awareness-guide.md - Agent patterns
   # 4. adoption-blueprint.md - Installation steps
   # 5. ledger.md - Adopter tracking
   ```

5. Add YAML frontmatter to each artifact:
   ```yaml
   ---
   sap_id: SAP-025
   version: 1.0.0
   status: draft
   last_updated: 2025-11-04
   ---
   ```

6. Validate structure:
   ```bash
   python scripts/sap-evaluator.py --deep SAP-025
   ```

7. Update SAP catalog:
   ```bash
   # Add entry to sap-catalog.json
   {
     "sap_id": "SAP-025",
     "name": "capability-name",
     "status": "draft",
     "version": "1.0.0",
     "path": "docs/skilled-awareness/capability-name/"
   }
   ```

**Expected outcome**: New SAP with 5 artifacts, ready for pilot phase

---

### Workflow 2: Install SAP (5-15 minutes)

**User signal**: "Install SAP-NNN", "Adopt SAP-NNN", "Enable capability X"

**Purpose**: Add SAP capability to project following adoption blueprint

**Steps**:
1. Read SAP's adoption blueprint:
   ```bash
   cat docs/skilled-awareness/<capability-name>/adoption-blueprint.md
   ```

2. Check prerequisites:
   ```bash
   # Example from adoption blueprint:
   # - Python 3.11+
   # - Docker installed
   # - Git configured
   ```

3. Follow installation steps from blueprint:
   ```bash
   # Step-by-step instructions from adoption-blueprint.md
   # Example:
   # 1. Install dependencies: pip install -r requirements.txt
   # 2. Configure: cp config.example.yaml config.yaml
   # 3. Initialize: python scripts/initialize.py
   ```

4. Run validation checks:
   ```bash
   # Validation commands from blueprint
   # Example: python scripts/validate-installation.py
   ```

5. Update ledger:
   ```bash
   # Add adoption entry to SAP's ledger.md
   # Format:
   # | 2025-11-04 | project-name | 1.0.0 | L0 (Aware) | Initial installation |
   ```

6. Log adoption event:
   ```bash
   echo '{"timestamp":"2025-11-04T10:30:00Z","event":"sap_adopted","sap_id":"SAP-025","version":"1.0.0"}' >> .chora/memory/events/coordination.jsonl
   ```

**Expected outcome**: SAP capability installed and validated

---

### Workflow 3: Validate SAP Structure (1-2 minutes)

**User signal**: "Validate SAP-NNN", "Check SAP structure", "Verify artifacts"

**Purpose**: Ensure SAP has all required artifacts and valid structure

**Steps**:
1. Check required artifacts exist:
   ```bash
   ls docs/skilled-awareness/<capability-name>/ | grep -E "(capability-charter|protocol-spec|awareness-guide|adoption-blueprint|ledger)\.md"
   ```

2. Validate YAML frontmatter:
   ```bash
   # Check each artifact has frontmatter
   for file in capability-charter protocol-spec awareness-guide adoption-blueprint ledger; do
     head -10 "docs/skilled-awareness/<capability-name>/${file}.md" | grep -q "^---$" && echo "${file}.md: OK" || echo "${file}.md: MISSING FRONTMATTER"
   done
   ```

3. Run deep evaluation:
   ```bash
   python scripts/sap-evaluator.py --deep SAP-025
   ```

4. Check for common issues:
   - Missing required sections
   - Invalid YAML syntax
   - Broken internal links
   - Missing version fields

5. Review evaluation report:
   ```
   SAP-025 (capability-name) Evaluation
   =====================================
   Status: PASS
   Level: L0 (Aware)

   Artifact Checks:
   ✅ capability-charter.md exists
   ✅ protocol-spec.md exists
   ✅ awareness-guide.md exists
   ✅ adoption-blueprint.md exists
   ✅ ledger.md exists

   Gaps: 0 P1, 2 P2
   ```

**Expected outcome**: Validation report showing structure compliance

---

### Workflow 4: Upgrade SAP Version (10-30 minutes)

**User signal**: "Upgrade SAP-NNN", "Migrate to v2.0.0", "Update SAP-NNN"

**Purpose**: Migrate SAP from one version to next following upgrade path

**Steps**:
1. Check current version in ledger:
   ```bash
   grep "$(hostname)" docs/skilled-awareness/<capability-name>/ledger.md | tail -1
   # Current: 1.0.0
   ```

2. Check available versions:
   ```bash
   git tag | grep "SAP-025-v"
   # Available: v1.0.0, v1.1.0, v2.0.0
   ```

3. Read upgrade guide from protocol-spec:
   ```bash
   # Section: Versioning & Migration
   cat docs/skilled-awareness/<capability-name>/protocol-spec.md | grep -A 20 "Migration Path"
   ```

4. Follow migration steps:
   ```bash
   # Example migration from v1.0.0 → v2.0.0:
   # 1. Backup current config
   # 2. Update dependencies
   # 3. Run migration script
   # 4. Validate new version
   ```

5. Update ledger entry:
   ```bash
   # Add new row to ledger.md:
   # | 2025-11-04 | project-name | 2.0.0 | L2 (Adopting) | Upgraded from v1.0.0 |
   ```

6. Validate upgrade:
   ```bash
   python scripts/validate-installation.py --version 2.0.0
   ```

**Expected outcome**: SAP upgraded to new version, ledger updated

---

### Workflow 5: Query SAP Catalog (30 seconds)

**User signal**: "List SAPs", "Show available capabilities", "What SAPs exist?"

**Purpose**: Discover available SAPs and their status

**Steps**:
1. Read SAP catalog:
   ```bash
   cat sap-catalog.json | jq '.saps[] | {id: .sap_id, name: .name, status: .status, version: .version}'
   ```

2. Filter by status:
   ```bash
   # Active SAPs only
   cat sap-catalog.json | jq '.saps[] | select(.status=="active")'
   ```

3. Filter by domain:
   ```bash
   # Find all testing-related SAPs
   cat sap-catalog.json | jq '.saps[] | select(.name | contains("test"))'
   ```

4. Check adoption level:
   ```bash
   # Read ledger for specific SAP
   cat docs/skilled-awareness/<capability-name>/ledger.md | grep "$(hostname)"
   ```

**Expected outcome**: List of SAPs with metadata

---

## Best Practices

### Practice 1: Always Follow 5-Artifact Structure

**Pattern**:
```bash
# EVERY SAP must have exactly 5 artifacts
docs/skilled-awareness/<capability-name>/
├── capability-charter.md      # ✅ Required
├── protocol-spec.md            # ✅ Required
├── awareness-guide.md          # ✅ Required
├── adoption-blueprint.md       # ✅ Required
└── ledger.md                   # ✅ Required
```

**Why**: Consistency enables agents to parse SAPs predictably

---

### Practice 2: Use Semantic Versioning

**Pattern**:
```
v1.0.0 → v1.0.1 (patch: bug fixes)
v1.0.0 → v1.1.0 (minor: backward-compatible features)
v1.0.0 → v2.0.0 (major: breaking changes)
```

**Why**: Clear upgrade paths, backward compatibility guarantees

---

### Practice 3: Update Ledger on Every Adoption Event

**Pattern**:
```markdown
| Date | Adopter | Version | Level | Notes |
|------|---------|---------|-------|-------|
| 2025-11-04 | project-name | 1.0.0 | L0 | Initial installation |
| 2025-11-05 | project-name | 1.0.0 | L1 | First successful use |
| 2025-11-10 | project-name | 1.1.0 | L2 | Upgraded, using regularly |
```

**Why**: Track adoption progress, understand usage patterns

---

### Practice 4: Validate Before Committing

**Pattern**:
```bash
# ALWAYS validate before git commit
python scripts/sap-evaluator.py --deep SAP-025

# Only commit if validation passes
git add docs/skilled-awareness/<capability-name>/
git commit -m "feat(sap-025): Add new capability"
```

**Why**: Catch structural issues early, maintain quality

---

### Practice 5: Link Related SAPs

**Pattern**:
```markdown
## Integration with Other SAPs

- **SAP-003** (project-bootstrap): Generates SAP structure during project init
- **SAP-009** (agent-awareness): Provides awareness file patterns
- **SAP-019** (sap-self-evaluation): Validates SAP structure
```

**Why**: Build capability graph, enable discovery

---

### Practice 6: Discoverability-First Adoption

**The Meta-Discoverability Principle**:

> **"The better the pattern, the worse the impact if undiscoverable"**

Implementation quality is irrelevant if agents cannot discover the capability exists. Without strong discoverability, excellent implementations remain invisible, creating a meta-discoverability paradox where sophisticated patterns become liabilities instead of assets.

**Anti-Pattern** (common mistake):
```
Day 1:  Implement SAP (excellent quality, 20 hours)
Day 2-30: Use SAP internally (works great)
Day 30: Mark L1 complete
Day 60: Run discoverability audit → 40/100
Day 90: Other agents still can't find SAP
ROI: $0 (invisible to others)
```

**Correct Pattern** (discoverability-first):
```
Day 1:  Implement SAP (excellent quality, 20 hours)
Day 2:  Add discoverability (README, AGENTS, justfile, 3-5 hours)
Day 2:  Validate discoverability ≥80/100
Day 2:  Mark L1 complete
Day 3+: Natural adoption (agents discover via root files)
ROI: Projected value realized from day 1
```

**Time Investment**: 3-5 hours (12-20% overhead on implementation)
**Returns**: 10-15 min saved per session per agent
**Break-even**: 20-30 sessions (1-2 months for single agent)
**12-Month ROI**: 250-400% (typical)

**L1 Checklist** (before marking complete):
```bash
# 1. README.md dedicated section (≥30 lines)
grep -A 40 "### SAP-XXX" README.md | wc -l  # Target: ≥30

# 2. AGENTS.md dedicated section (≥60 lines)
grep -A 70 "### SAP-XXX" AGENTS.md | wc -l  # Target: ≥60

# 3. justfile recipes (≥3 with comments)
grep -A 20 "SAP-XXX" justfile | grep "^[a-z]" | wc -l  # Target: ≥3

# 4. Direct links (if nested hierarchy)
grep -o "\[.*AGENTS.md\](.*AGENTS.md)" CLAUDE.md  # Should have links

# 5. Discoverability audit
python scripts/sap-evaluator.py --disc SAP-XXX  # Target: ≥80/100
```

**Why**: Without discoverability ≥80/100, other agents never find the SAP, resulting in zero adoption and negative ROI. Discoverability is a **prerequisite for L1 completion**, not an optional enhancement.

**Special Case: Advanced Patterns**

If your SAP uses advanced patterns (SAP-009 nested hierarchies, SAP-012 planning frameworks):
- **Higher threshold**: ≥85/100 (vs ≥80/100 for standard SAPs)
- **Required elements**:
  - Explicit token savings statement (e.g., "60-70% reduction")
  - Read time estimates (e.g., "8-min, 5k tokens")
  - Direct links from root to nested files (not optional)
  - "Navigation tip" sections

**Rationale**: Without extra discoverability, navigation tax exceeds pattern benefits, making advanced patterns net negative.

**Template**: See [discoverability-checklist.md](../templates/discoverability-checklist.md) for complete guidance.

---

## Common Pitfalls

### Pitfall 1: Missing Required Artifacts

**Problem**: Create SAP with only 3 artifacts instead of 5

**Fix**: ALWAYS create all 5 artifacts

```bash
# ❌ BAD: Incomplete SAP
docs/skilled-awareness/my-sap/
├── capability-charter.md
└── protocol-spec.md

# ✅ GOOD: Complete SAP
docs/skilled-awareness/my-sap/
├── capability-charter.md
├── protocol-spec.md
├── awareness-guide.md
├── adoption-blueprint.md
└── ledger.md
```

**Why**: Missing artifacts break agent workflows, reduce adoption

---

### Pitfall 2: No YAML Frontmatter

**Problem**: Artifact files missing YAML frontmatter

**Fix**: ALWAYS include frontmatter

```markdown
❌ BAD:
# Capability Charter
...

✅ GOOD:
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

### Pitfall 3: Not Updating Ledger

**Problem**: Install SAP but forget to update ledger.md

**Fix**: Update ledger immediately after adoption event

```bash
# After installation:
# Add entry to ledger.md
| 2025-11-04 | project-name | 1.0.0 | L0 (Aware) | Initial installation |
```

**Why**: Ledger tracks adoption, enables usage analysis

---

### Pitfall 4: Breaking Changes Without Major Version Bump

**Problem**: Make breaking change but only bump minor version

**Fix**: Follow semantic versioning rules

```bash
# ❌ BAD: Breaking change in minor version
v1.0.0 → v1.1.0 (but removed required field)

# ✅ GOOD: Breaking change in major version
v1.0.0 → v2.0.0 (removed required field, updated migration guide)
```

**Why**: Semantic versioning communicates compatibility expectations

---

### Pitfall 5: No Adoption Blueprint Validation

**Problem**: Adoption blueprint has no validation section

**Fix**: ALWAYS include validation steps

```markdown
## Validation

After installation, verify:

1. Required files exist:
   ```bash
   ls config.yaml schemas/*.json
   ```

2. Dependencies installed:
   ```bash
   pip list | grep required-package
   ```

3. Tests pass:
   ```bash
   pytest tests/
   ```
```

**Why**: Validation confirms successful installation, prevents silent failures

---

## Integration with Other SAPs

### SAP-003 (project-bootstrap)
- Generates SAP structure during `just init`
- Creates 5 artifact templates
- Integration: `python scripts/generate-sap.py --name <capability>`

### SAP-009 (agent-awareness)
- AGENTS.md/CLAUDE.md awareness files follow SAP structure
- Progressive loading pattern standardized
- Integration: Awareness files reference SAP artifacts

### SAP-019 (sap-self-evaluation)
- Validates SAP structure and completeness
- Checks 5-artifact requirement
- Integration: `python scripts/sap-evaluator.py --deep SAP-NNN`

### SAP-012 (development-lifecycle)
- SAP adoption follows DDD→BDD→TDD pattern
- Lifecycle phases documented in capability charter
- Integration: SAP evolution tracked in ledger

---

## Support & Resources

**SAP-000 Documentation**:
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
- [SAP-003 (project-bootstrap)](../project-bootstrap/) - SAP generation
- [SAP-009 (agent-awareness)](../agent-awareness/) - Awareness patterns
- [SAP-019 (sap-self-evaluation)](../sap-self-evaluation/) - Validation

---

## Version History

- **1.0.0** (2025-11-04): Initial AGENTS.md for SAP-000
  - 5 workflows: Create SAP, Install SAP, Validate Structure, Upgrade Version, Query Catalog
  - 4 user signal pattern tables (Creation, Installation, Validation, Upgrade)
  - 5 best practices, 5 common pitfalls
  - Integration with SAP-003, SAP-009, SAP-012, SAP-019

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code-specific patterns
2. Review [protocol-spec.md](protocol-spec.md) for technical contracts
3. Check [document-templates.md](../document-templates.md) for artifact templates
4. Validate SAP: `python scripts/sap-evaluator.py --deep SAP-NNN`
