# Agent Awareness Guide: SAP Adoption Verification & Quality Assurance

**Capability ID**: SAP-050
**Modern Namespace**: chora.awareness.sap_adoption_verification
**Type**: Pattern
**Status**: Active
**Version**: 1.1.0
**Last Updated**: 2025-11-20

---

## Quick Start for Agents

This guide provides agent-specific patterns for verifying SAP structure, completeness, and quality. Use these patterns to validate SAPs before recommending adoption or promoting status.

**What You'll Learn**:
- How to verify SAP has all required artifacts
- How to check for required sections and completeness
- How to validate documentation links
- How to evaluate quality gates for status promotion
- How to track adoption metrics

**Prerequisites**:
- Python 3.9+ with `pyyaml` library
- Access to `docs/skilled-awareness/` and `capabilities/` directories

---

## Common Agent Workflows

### Workflow 1: Verify SAP Structure

**User Request**: "Is SAP-015 properly structured?"

**Agent Action**:

```python
from pathlib import Path

def verify_sap_structure(sap_name: str) -> dict:
    """Verify SAP has all 5 required artifacts"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    missing = []

    # Check required artifacts
    required = [
        'capability-charter.md',
        'protocol-spec.md',
        'adoption-blueprint.md',
        'ledger.md'
    ]

    for artifact in required:
        if not (sap_dir / artifact).exists():
            missing.append(artifact)

    # Check awareness guide (either name acceptable)
    if not (sap_dir / 'AGENTS.md').exists() and not (sap_dir / 'awareness-guide.md').exists():
        missing.append('AGENTS.md (or awareness-guide.md)')

    # Check YAML manifest
    manifest_pattern = sap_name.replace('-', '_')
    manifest_found = any(
        manifest_pattern in str(m)
        for m in Path('capabilities').glob('chora.*.yaml')
    )

    if not manifest_found:
        missing.append('capability manifest (YAML)')

    return {
        'passed': len(missing) == 0,
        'missing': missing
    }

# Example usage
result = verify_sap_structure('task-tracking')
if result['passed']:
    print("✓ SAP structure is valid (all required artifacts present)")
else:
    print(f"✗ SAP structure incomplete. Missing: {', '.join(result['missing'])}")
```

**Agent Response Template**:
```
I've verified SAP-015 (task-tracking) structure:

✓ SAP structure is valid
  - capability-charter.md: Present
  - protocol-spec.md: Present
  - AGENTS.md: Present
  - adoption-blueprint.md: Present
  - ledger.md: Present
  - Capability manifest: Present (chora.awareness.task_tracking.yaml)

All required artifacts are in place!
```

---

### Workflow 2: Check SAP Completeness

**User Request**: "Does this SAP have all required sections?"

**Agent Action**:

```python
def verify_sap_completeness(sap_name: str) -> dict:
    """Verify artifacts contain required sections"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    issues = []

    # Check charter sections
    charter = sap_dir / 'capability-charter.md'
    if charter.exists():
        content = charter.read_text()
        required_sections = [
            'Executive Summary',
            'Problem Statement',
            'Solution Design',
            'Success Metrics'
        ]
        for section in required_sections:
            if section not in content:
                issues.append(f"capability-charter.md missing: {section}")

    # Check AGENTS sections
    agents = sap_dir / 'AGENTS.md'
    if not agents.exists():
        agents = sap_dir / 'awareness-guide.md'

    if agents.exists():
        content = agents.read_text()
        if 'Quick Start' not in content:
            issues.append("AGENTS.md missing: Quick Start section")
        if 'Workflow' not in content:
            issues.append("AGENTS.md missing: Workflow section")

    # Check blueprint sections
    blueprint = sap_dir / 'adoption-blueprint.md'
    if blueprint.exists():
        content = blueprint.read_text()
        if 'Adoption Checklist' not in content:
            issues.append("adoption-blueprint.md missing: Adoption Checklist")

    # Check ledger
    ledger = sap_dir / 'ledger.md'
    if ledger.exists():
        content = ledger.read_text()
        if 'Version History' not in content:
            issues.append("ledger.md missing: Version History")

    return {
        'passed': len(issues) == 0,
        'issues': issues
    }

# Example usage
result = verify_sap_completeness('task-tracking')
if result['passed']:
    print("✓ SAP completeness verified (all required sections present)")
else:
    print(f"✗ Completeness issues found:")
    for issue in result['issues']:
        print(f"  - {issue}")
```

**Agent Response Template**:
```
I've checked SAP-015 completeness:

✓ All required sections are present:
  - capability-charter.md: Executive Summary, Problem Statement, Solution Design, Success Metrics ✓
  - AGENTS.md: Quick Start, Workflows ✓
  - adoption-blueprint.md: Adoption Checklist, Prerequisites ✓
  - ledger.md: Version History ✓

The SAP documentation is complete!
```

---

### Workflow 3: Validate Documentation Links

**User Request**: "Check for broken links in this SAP"

**Agent Action**:

```python
import re

def verify_sap_links(sap_name: str) -> dict:
    """Verify markdown links are valid"""
    sap_dir = Path(f'docs/skilled-awareness/{sap_name}')
    broken = []

    for md_file in sap_dir.glob('*.md'):
        content = md_file.read_text()

        # Extract markdown links: [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^\)]+)\)', content)

        for text, url in links:
            # Skip external URLs and anchors
            if url.startswith('http') or url.startswith('#'):
                continue

            # Resolve relative path
            target = (md_file.parent / url).resolve()

            if not target.exists():
                broken.append({
                    'file': md_file.name,
                    'link': url,
                    'text': text
                })

    return {
        'passed': len(broken) == 0,
        'broken_links': broken
    }

# Example usage
result = verify_sap_links('task-tracking')
if result['passed']:
    print("✓ All documentation links are valid")
else:
    print(f"✗ Found {len(result['broken_links'])} broken link(s):")
    for link in result['broken_links']:
        print(f"  - {link['file']}: '{link['text']}' → {link['link']}")
```

**Agent Response Template**:
```
I've validated all documentation links in SAP-015:

✓ All links are valid (0 broken links found)

The documentation cross-references are intact!
```

---

### Workflow 4: Evaluate Quality Gate for Promotion

**User Request**: "Can we promote SAP-015 to production status?"

**Agent Action**:

```python
def evaluate_quality_gate(sap_name: str, target_status: str) -> dict:
    """Evaluate SAP against quality gate criteria"""
    unmet = []
    met = []

    # Check structure
    structure = verify_sap_structure(sap_name)
    if structure['passed']:
        met.append("Structure verification: PASS")
    else:
        unmet.append(f"Structure verification: FAIL ({len(structure['missing'])} missing artifacts)")

    # Check completeness
    completeness = verify_sap_completeness(sap_name)
    if completeness['passed']:
        met.append("Completeness verification: PASS")
    else:
        unmet.append(f"Completeness verification: FAIL ({len(completeness['issues'])} issues)")

    # Check links
    links = verify_sap_links(sap_name)
    broken_count = len(links['broken_links'])
    if broken_count == 0:
        met.append("Link validation: PASS (0 broken links)")
    elif target_status == 'pilot' and broken_count <= 3:
        met.append(f"Link validation: ACCEPTABLE ({broken_count} broken links, ≤3 for pilot)")
    else:
        unmet.append(f"Link validation: FAIL ({broken_count} broken links)")

    # Pilot/Production requirements
    if target_status in ['pilot', 'production']:
        ledger = Path(f'docs/skilled-awareness/{sap_name}/ledger.md')
        if ledger.exists():
            content = ledger.read_text().lower()

            # Dogfooding
            if 'dogfooding' in content or 'usage' in content:
                met.append("Dogfooding evidence: PASS")
            else:
                unmet.append("Dogfooding evidence: FAIL")

            # Feedback
            feedback_count = content.count('feedback')
            if feedback_count >= 1:
                met.append(f"Feedback: PASS ({feedback_count} entries)")
            else:
                unmet.append("Feedback: FAIL")

    # Production requirements
    if target_status == 'production':
        if ledger.exists():
            content = ledger.read_text().lower()

            # Adoptions
            adoption_count = content.count('adopted')
            if adoption_count >= 3:
                met.append(f"Adoptions: PASS ({adoption_count})")
            else:
                unmet.append(f"Adoptions: FAIL ({adoption_count}/3)")

            # Metrics
            if 'metrics' in content:
                met.append("Metrics: PASS")
            else:
                unmet.append("Metrics: FAIL")

    return {
        'passed': len(unmet) == 0,
        'target_status': target_status,
        'unmet_criteria': unmet,
        'met_criteria': met
    }

# Example usage
result = evaluate_quality_gate('task-tracking', 'production')
if result['passed']:
    print(f"✓ SAP meets all criteria for {result['target_status']} status")
else:
    print(f"✗ SAP does not meet {result['target_status']} criteria:")
    for criteria in result['unmet_criteria']:
        print(f"  ✗ {criteria}")
    print(f"\nMet criteria:")
    for criteria in result['met_criteria']:
        print(f"  ✓ {criteria}")
```

**Agent Response Template**:
```
I've evaluated SAP-015 against production quality gates:

✗ Not ready for production (2 unmet criteria):
  ✗ Adoptions: FAIL (1/3 required)
  ✗ Metrics: FAIL (no metrics tracked)

✓ Met criteria:
  ✓ Structure verification: PASS
  ✓ Completeness verification: PASS
  ✓ Link validation: PASS (0 broken links)
  ✓ Dogfooding evidence: PASS
  ✓ Feedback: PASS (3 entries)

Recommendation: SAP-015 needs 2 more documented adoptions and adoption metrics tracking before promoting to production. Consider keeping it in pilot status for now.
```

---

### Workflow 5: Track Adoption Metrics

**User Request**: "What are the adoption metrics for SAP-015?"

**Agent Action**:

```python
def track_adoption_metrics(sap_name: str) -> dict:
    """Track SAP adoption from ledger"""
    ledger = Path(f'docs/skilled-awareness/{sap_name}/ledger.md')

    if not ledger.exists():
        return {'error': 'Ledger not found'}

    content = ledger.read_text()
    content_lower = content.lower()

    metrics = {
        'adoptions': content_lower.count('adopted'),
        'feedback_entries': content_lower.count('feedback:'),
        'issues_reported': content_lower.count('issue:'),
        'version_count': content.count('###'),  # Version headers
        'has_dogfooding': 'dogfooding' in content_lower,
        'has_metrics': 'metrics' in content_lower
    }

    # Extract status
    import re
    status_match = re.search(r'\*\*Current Status\*\*:\s*(\w+)', content)
    if status_match:
        metrics['current_status'] = status_match.group(1)

    return metrics

# Example usage
metrics = track_adoption_metrics('task-tracking')
print(f"SAP-015 Adoption Metrics:")
print(f"  - Current status: {metrics.get('current_status', 'unknown')}")
print(f"  - Adoptions: {metrics['adoptions']}")
print(f"  - Feedback entries: {metrics['feedback_entries']}")
print(f"  - Issues reported: {metrics['issues_reported']}")
print(f"  - Version count: {metrics['version_count']}")
print(f"  - Dogfooding evidence: {'Yes' if metrics['has_dogfooding'] else 'No'}")
print(f"  - Metrics tracked: {'Yes' if metrics['has_metrics'] else 'No'}")
```

**Agent Response Template**:
```
SAP-015 (Task Tracking) adoption metrics:

Current Status: pilot
Adoptions: 5 documented
Feedback: 8 entries
Issues: 2 reported (2 resolved)
Versions: 3 releases
Dogfooding: Yes (2 internal usage examples)
Metrics Tracking: Yes

The SAP shows healthy adoption with positive engagement!
```

---

## Quick Reference Patterns

### Pattern: Verify Before Recommending

```python
# Always verify structure before recommending a SAP
sap_name = 'task-tracking'
result = verify_sap_structure(sap_name)

if result['passed']:
    print(f"I recommend adopting SAP-015 ({sap_name})")
else:
    print(f"⚠️ SAP-015 is incomplete. Missing: {', '.join(result['missing'])}")
```

---

### Pattern: Check Quality Gate Before Status Change

```python
# Before promoting status, check quality gate
result = evaluate_quality_gate('example-sap', 'pilot')

if result['passed']:
    print("✓ Ready for pilot promotion")
else:
    print(f"✗ Not ready. Unmet criteria:")
    for criteria in result['unmet_criteria']:
        print(f"  - {criteria}")
```

---

### Pattern: Validate Links in PR

```python
# Check links when reviewing documentation changes
result = verify_sap_links('example-sap')

if not result['passed']:
    print(f"⚠️ Found {len(result['broken_links'])} broken link(s). Please fix before merging.")
```

---

## Common Agent Pitfalls

### Pitfall 1: Not Verifying Structure Before Recommending

**Problem**: Agent recommends incomplete SAP

**Impact**: Users try to adopt broken SAP

**Solution**: Always verify structure first

```python
# Bad: Direct recommendation
"You should adopt SAP-015"

# Good: Verify first
result = verify_sap_structure('task-tracking')
if result['passed']:
    "SAP-015 is properly structured and ready for adoption"
else:
    "SAP-015 is incomplete (missing artifacts). I don't recommend adopting it yet."
```

---

### Pitfall 2: Ignoring Quality Gates

**Problem**: Agent promotes SAP status without checking criteria

**Impact**: Low-quality SAPs marked as production-ready

**Solution**: Evaluate quality gate before status change

```python
# Bad: Automatic promotion
"Let's promote this to production"

# Good: Check quality gate
result = evaluate_quality_gate('example-sap', 'production')
if result['passed']:
    "This SAP meets all production criteria and can be promoted"
else:
    "This SAP doesn't meet production criteria yet. Unmet: {result['unmet_criteria']}"
```

---

### Pitfall 3: Not Tracking Broken Links

**Problem**: Agent doesn't validate links, documentation becomes stale

**Impact**: Users follow broken links, poor experience

**Solution**: Run link validation regularly

```python
# Good: Validate links when modifying documentation
result = verify_sap_links('example-sap')
if not result['passed']:
    print("Fix broken links before committing")
```

---

## Integration with Other SAPs

### SAP-027 (Dogfooding Patterns)

**Use Case**: Verify dogfooding evidence before pilot promotion

```python
# Check for dogfooding in ledger
ledger_content = Path('docs/skilled-awareness/task-tracking/ledger.md').read_text()

if 'dogfooding' in ledger_content.lower():
    print("✓ Dogfooding evidence found")
else:
    print("✗ No dogfooding evidence. See SAP-027 for dogfooding patterns.")
```

---

### SAP-029 (SAP Generation)

**Use Case**: Verify generated SAPs have correct structure

```python
# After generating SAP with SAP-029, verify it
newly_generated_sap = 'new-capability'
result = verify_sap_structure(newly_generated_sap)

if not result['passed']:
    print(f"⚠️ Generated SAP incomplete. Missing: {result['missing']}")
    print("Check SAP-029 generation template")
```

---

## Bash Quick Reference

### Verify SAP Structure (Manual)

```bash
sap_name="task-tracking"

# Check required files
for file in capability-charter.md protocol-spec.md AGENTS.md adoption-blueprint.md ledger.md; do
  if [ -f "docs/skilled-awareness/${sap_name}/${file}" ]; then
    echo "✓ $file"
  else
    echo "✗ $file (missing)"
  fi
done

# Check YAML manifest
if ls capabilities/chora.*.${sap_name//-/_}.yaml 1> /dev/null 2>&1; then
  echo "✓ capability manifest"
else
  echo "✗ capability manifest (missing)"
fi
```

---

## Troubleshooting

### Issue: "Ledger not found"

**Diagnosis**: SAP missing ledger.md

**Solution**: Create ledger.md with Version History section

---

### Issue: "False positive on completeness"

**Diagnosis**: Section exists but not detected (case/spelling mismatch)

**Solution**: Check exact section heading format in protocol-spec.md

---

## SAP Quality Ecosystem Integration

### The Complete Quality Stack

SAP-050 is the **orchestrator** of a multi-SAP quality ecosystem. Understanding how these SAPs work together is critical for effective usage.

#### Foundation Layer: SAP-000

```
SAP-000: SAP Framework (The Constitution)
├─ Defines 5-artifact structure
├─ Dublin Core metadata standard
├─ Quality requirements for all SAPs
└─ Used by: SAP-050 for structure validation
```

**SAP-050 Integration**: Structure verification checks SAP-000 compliance
```python
# SAP-050 validates against SAP-000 requirements
required = ['capability-charter.md', 'protocol-spec.md',
            'adoption-blueprint.md', 'ledger.md']  # SAP-000 § 2
```

---

#### Infrastructure Layer: SAP-008, SAP-016, SAP-049

```
SAP-008: Automation Scripts       SAP-016: Link Validation        SAP-049: Namespace Resolution
├─ justfile (30+ commands)        ├─ validate-links.py            ├─ Alias mapping
├─ 25 automation scripts          ├─ Internal + external links    ├─ SAP-XXX → modern NS
├─ L3/L4 test infrastructure      ├─ CI/CD integration            ├─ Deprecation timeline
└─ Used by: CI/CD workflows       └─ Used by: SAP-050 § 3         └─ Used by: Migration workflows
```

**SAP-050 Integration**: Link validation delegates to SAP-016
```python
# SAP-050 uses SAP-016 instead of duplicating logic
result = subprocess.run(
    ['python', 'scripts/validate-links.py', str(sap_dir), '--json'],
    capture_output=True
)
# Returns: {'passed': bool, 'broken_links': [...], 'validated_by': 'SAP-016'}
```

---

#### Orchestration Layer: SAP-050 (This SAP)

```
SAP-050: SAP Adoption Verification (THE ORCHESTRATOR)
├─ Uses SAP-000 standards for structure requirements
├─ Uses SAP-016 for link validation
├─ Uses SAP-027 dogfooding as quality gate criteria
├─ Uses SAP-049 for namespace validation (planned)
└─ Orchestrates, doesn't duplicate!
```

**Integration Pattern**: Composition over duplication
- ✅ Delegates link validation to SAP-016
- ✅ References SAP-000 for structure standards
- ✅ Checks SAP-027 dogfooding evidence
- ⏳ Will integrate SAP-049 for namespace checks

---

#### Creation Layer: SAP-029

```
SAP-029: SAP Generation
├─ Generates SAPs from templates
├─ Uses SAP-050 for verification
└─ Should integrate SAP-016, SAP-027, SAP-019
```

**SAP-050 Integration**: SAP-029 should call SAP-050 after generation
```python
# Recommended SAP-029 workflow
def generate_sap(sap_id):
    create_from_template(sap_id)

    # Use SAP-050 for verification
    result = verify_sap_structure(sap_id)
    if not result['passed']:
        print(f"Generated SAP incomplete: {result['missing']}")
        return False

    return True
```

---

#### Validation Layer: SAP-027

```
SAP-027: Dogfooding Patterns
├─ 5-week pilot methodology
├─ GO/NO-GO criteria
├─ ROI analysis
└─ Used by: SAP-050 quality gates
```

**SAP-050 Integration**: Quality gates require dogfooding evidence
```python
# SAP-050 checks for SAP-027 dogfooding in quality gates
def verify_quality_gate(sap_name, target_status):
    if target_status in ['pilot', 'production']:
        ledger = Path(f'docs/skilled-awareness/{sap_name}/ledger.md')
        content = ledger.read_text()

        # Check for SAP-027 dogfooding evidence
        if 'dogfooding' not in content.lower():
            unmet.append("No SAP-027 dogfooding evidence")
```

---

#### Maturity Layer: SAP-019

```
SAP-019: SAP Self-Evaluation
├─ Level 1/2/3 assessment
├─ Gap analysis
├─ Roadmap generation
└─ Uses SAP-050 to check quality first
```

**SAP-050 Integration**: SAP-019 should verify quality before maturity assessment
```python
# Recommended SAP-019 workflow
def evaluate_adoption(sap_name):
    # First: Check quality with SAP-050
    quality = verify_sap_structure(sap_name)
    if not quality['passed']:
        return {'error': 'SAP quality issues must be fixed first'}

    # Then: Assess adoption maturity
    maturity = assess_maturity_level(sap_name)
    return maturity
```

---

### The Complete SAP Lifecycle Workflow

This workflow shows how all SAPs work together from creation to maturity:

```
┌─────────────────────────────────────────────────────────────┐
│                    SAP LIFECYCLE JOURNEY                     │
└─────────────────────────────────────────────────────────────┘

Phase 1: CREATION (SAP-029 + SAP-050)
┌──────────────┐
│  SAP-029     │  Generate SAP from templates
│  Generation  │  → 5 artifacts + manifest
└──────┬───────┘
       │
       ▼
┌──────────────┐
│  SAP-050     │  Verify generated SAP
│  Verification│  → Structure ✓ (SAP-000 compliance)
└──────┬───────┘  → Completeness ✓ (required sections)
       │          → Links ✓ (SAP-016 validation)
       │          → Quality gate (draft→pilot criteria)
       ▼
    ✅ PASS → Move to Phase 2
    ❌ FAIL → Fix issues, re-verify

Phase 2: DOGFOODING (SAP-027 + SAP-050)
┌──────────────┐
│  SAP-027     │  Run dogfooding pilot
│  Dogfooding  │  → 5-week validation
└──────┬───────┘  → ROI analysis
       │          → GO/NO-GO decision
       ▼
┌──────────────┐
│  SAP-050     │  Check quality gate (pilot→production)
│  Verification│  → Dogfooding evidence ✓ (SAP-027)
└──────┬───────┘  → Feedback entries ✓
       │          → ≥1 adoption ✓
       ▼
    ✅ PASS → Move to Phase 3
    ❌ FAIL → More dogfooding needed

Phase 3: ADOPTION (SAP-019 + SAP-027)
┌──────────────┐
│  SAP-019     │  Evaluate adoption maturity
│  Self-Eval   │  → Level 1/2/3 assessment
└──────┬───────┘  → Gap analysis
       │          → Roadmap generation
       ▼
    Low maturity? → Use SAP-027 (more dogfooding)
    High maturity? → Success! ✅

Throughout: SAP-008 provides automation (justfile, scripts)
Throughout: SAP-016 validates links
Throughout: SAP-049 resolves namespaces
```

---

### Integration Quick Reference

| SAP | Role | Provides To SAP-050 | SAP-050 Uses It For |
|-----|------|---------------------|---------------------|
| **SAP-000** | Standards | 5-artifact requirements | Structure validation |
| **SAP-008** | Automation | justfile, scripts | L3/L4 testing (planned) |
| **SAP-016** | Link Validation | validate-links.py | Link verification |
| **SAP-019** | Maturity Eval | Adoption assessment | Post-quality maturity check |
| **SAP-027** | Dogfooding | Pilot methodology | Quality gate criteria |
| **SAP-029** | Generation | Template creation | Calls SAP-050 for verification |
| **SAP-049** | Namespace | Alias resolution | Namespace validation (planned) |

---

### Example: Complete Integration Workflow

```python
#!/usr/bin/env python3
"""Complete SAP creation workflow using the quality ecosystem"""

from sap_verify import verify_structure, verify_completeness, verify_links

# Step 1: Generate SAP (SAP-029)
def create_new_sap(sap_id, metadata):
    print(f"Creating {sap_id} using SAP-029...")
    # Generate from templates
    generate_from_template(sap_id, metadata)

    # Step 2: Verify structure (SAP-050 using SAP-000, SAP-016)
    print(f"Verifying {sap_id} using SAP-050...")

    structure = verify_structure(sap_id)  # SAP-000 compliance
    if not structure['passed']:
        print(f"Structure FAIL: {structure['missing']}")
        return False

    completeness = verify_completeness(sap_id)  # Section checks
    if not completeness['passed']:
        print(f"Completeness FAIL: {completeness['issues']}")
        return False

    links = verify_links(sap_id)  # SAP-016 delegation
    if not links['passed']:
        print(f"Links FAIL: {links['broken_links']}")
        print(f"Validated by: {links['validated_by']}")  # "SAP-016"
        return False

    print(f"✅ {sap_id} structure verified!")

    # Step 3: Run dogfooding pilot (SAP-027)
    print(f"Running SAP-027 dogfooding pilot...")
    pilot_result = run_dogfooding_pilot(sap_id, weeks=5)

    if not pilot_result['go_no_go']:
        print(f"Dogfooding FAIL: {pilot_result['issues']}")
        return False

    # Step 4: Check pilot quality gate (SAP-050 + SAP-027)
    print(f"Checking pilot promotion criteria...")
    gate = verify_quality_gate(sap_id, 'pilot')

    if not gate['passed']:
        print(f"Quality gate FAIL: {gate['unmet_criteria']}")
        return False

    print(f"✅ {sap_id} ready for pilot!")

    # Step 5: After adoption, evaluate maturity (SAP-019)
    print(f"Evaluating adoption maturity with SAP-019...")
    maturity = evaluate_adoption_maturity(sap_id)
    print(f"Maturity: Level {maturity['level']}")

    return True

# Usage
create_new_sap('SAP-051', {
    'name': 'service-health-monitoring',
    'problem': 'No standardized service health checks',
    'solution': 'Heartbeat monitoring with TTL leases'
})
```

---

## References

- [Protocol Specification](protocol-spec.md) - Complete technical spec
- [Capability Charter](capability-charter.md) - Problem and solution
- [Adoption Blueprint](adoption-blueprint.md) - Installation guide
- [SAP-000: SAP Framework](../sap-framework/protocol-spec.md) - SAP structure requirements
- [SAP-016: Link Validation](../link-validation-reference-management/protocol-spec.md) - Link validation infrastructure
- [SAP-027: Dogfooding Patterns](../dogfooding-patterns/AGENTS.md) - Validation methodology
- [SAP-029: SAP Generation](../sap-generation/AGENTS.md) - Template-based creation

---

**Version**: 1.1.0
**Status**: Active
**Last Updated**: 2025-11-20
