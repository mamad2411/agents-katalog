# Agent Awareness Guide: Actionable Quality Infrastructure

**Capability ID**: SAP-054
**Modern Namespace**: chora.quality.actionable_infrastructure
**Type**: Meta-Pattern
**Status**: Draft
**Version**: 1.0.0
**Last Updated**: 2025-11-20

---

## Quick Start for Agents

This guide provides agent-specific patterns for building actionable quality infrastructure that transforms detection-only checks (L0) into complete feedback loops (L1-L4).

**What You'll Learn**:
- How to identify incomplete quality feedback loops
- How to implement L1 (CLASSIFY) phase for any quality check
- How to build L2 (REMEDIATE) auto-fix scripts
- How to integrate L3 (TRACK) metrics and L4 (PREVENT) pre-commit hooks
- How to calculate ROI for quality infrastructure investments

**Prerequisites**:
- Python 3.9+ for classification and remediation scripts
- Access to quality check outputs (JSON format preferred)
- Understanding of SAP-006 (Quality Gates) for L4 pre-commit integration
- Understanding of SAP-010 (Memory System) for L3 metrics tracking

**Core Principle**: **"Detection without action is noise"**

Any quality check at L0 (DETECT-only) creates ongoing toil. Use SAP-054 patterns to progress to L2 (REMEDIATE) for 85-90% toil reduction.

---

## Common Agent Workflows

### Workflow 1: Identify Incomplete Quality Feedback Loops

**User Request**: "Why do these quality checks create so much toil?"

**Agent Action**:

```python
def audit_quality_feedback_loops() -> dict:
    """
    Identify quality checks stuck at L0 (DETECT-only)

    Returns:
        dict with incomplete_loops (list), toil_estimate (hours/week)
    """
    incomplete_loops = []

    # Check for L0 (DETECT-only) patterns:
    # 1. Script produces list of violations
    # 2. No auto-classification logic
    # 3. No auto-fix recipes (no "just health-fix-*")
    # 4. No metrics tracking over time
    # 5. No pre-commit hook integration

    checks_to_audit = [
        'manifest-discovery',
        'script-refactoring-audit',
        'link-validation',
        'traceability-validation'
    ]

    for check_name in checks_to_audit:
        # Check if classification exists
        classify_script = Path(f'scripts/classify-{check_name}.py')
        has_classify = classify_script.exists() or \
                      '--phase classify' in Path(f'scripts/{check_name}.py').read_text()

        # Check if remediation exists
        has_remediate = Path(f'scripts/remediate-{check_name}.py').exists() or \
                       f'health-fix-{check_name}' in Path('justfile').read_text()

        # Check if tracking exists
        has_track = f'health-track-{check_name}' in Path('justfile').read_text() or \
                   f'quality_metrics_snapshot.*{check_name}' in \
                   Path('.chora/memory/events/').glob('*.jsonl')

        # Check if prevention exists
        has_prevent = f'prevent-{check_name}' in \
                     Path('.pre-commit-config.yaml').read_text()

        # Determine level
        level = 0
        if has_classify: level = 1
        if has_remediate: level = 2
        if has_track: level = 3
        if has_prevent: level = 4

        if level < 2:  # L0 or L1 only
            incomplete_loops.append({
                'check_name': check_name,
                'current_level': f'L{level}',
                'toil_estimate_hours_per_week': estimate_toil(check_name),
                'recommended_next_level': f'L{level + 1}'
            })

    return {
        'incomplete_loops': incomplete_loops,
        'total_toil_estimate_hours_per_week': sum(
            loop['toil_estimate_hours_per_week'] for loop in incomplete_loops
        )
    }

def estimate_toil(check_name: str) -> float:
    """Estimate weekly toil for a quality check at L0-L1"""
    # Heuristic: L0 = 2-3 hours/week, L1 = 1-1.5 hours/week
    return 2.5  # Conservative estimate
```

**Agent Response Template**:
```
I've audited your quality infrastructure:

❌ Incomplete Quality Feedback Loops (4 found):

1. manifest-discovery: L0 (DETECT-only)
   - Weekly toil: ~2.5 hours
   - Recommendation: Add CLASSIFY phase (L1) → 60% toil reduction

2. script-refactoring-audit: L0 (DETECT-only)
   - Weekly toil: ~2.5 hours
   - Recommendation: Add CLASSIFY phase (L1) → 60% toil reduction

3. link-validation: L0 (DETECT-only)
   - Weekly toil: ~2.5 hours
   - Recommendation: Add CLASSIFY phase (L1) → 60% toil reduction

4. traceability-validation: L0 (DETECT-only)
   - Weekly toil: ~2.5 hours
   - Recommendation: Add CLASSIFY phase (L1) → 60% toil reduction

📊 Total estimated toil: 10 hours/week
💡 Potential savings: 6 hours/week with L1 adoption (400-500% ROI)

Would you like me to implement L1 (CLASSIFY) for one of these checks?
```

---

### Workflow 2: Implement L1 (CLASSIFY) Phase

**User Request**: "Add classification to manifest discovery"

**Agent Action**:

```python
def implement_l1_classification(check_name: str):
    """
    Add CLASSIFY phase to existing L0 quality check

    Steps:
    1. Read existing DETECT output schema
    2. Add classification logic (auto-fixable / investigate / false-positive)
    3. Update output schema with classification metadata
    4. Add --phase classify CLI argument
    """

    # Example: Manifest Discovery L1 implementation
    if check_name == 'manifest-discovery':
        # Add classification function to existing script
        classification_code = '''
def classify_manifest_violation(violation: dict) -> dict:
    """
    Classify untracked feature as auto-fixable, investigation, or false-positive

    Classification Rules:
    1. False Positive: Feature already in manifest (cross-reference failed)
    2. Auto-fixable: Clear deliverables (commits > 10, notes > 0)
    3. Investigation: Unclear boundaries or event-only features
    """

    # Rule 1: Check if already in manifest
    feature_id = violation['id']
    if feature_exists_in_manifest(feature_id):
        return {
            "category": "false_positive",
            "reason": f"Feature {feature_id} already documented in manifest",
            "auto_action": "skip",
            "suggestion": "Cross-reference check should filter this in DETECT phase"
        }

    # Rule 2: Check for clear deliverables
    evidence = violation.get('evidence', {})
    if evidence.get('commits', 0) > 10 and evidence.get('notes', 0) > 0:
        return {
            "category": "auto_fixable",
            "reason": "Feature has clear deliverables and traceability",
            "auto_action": "add_to_manifest",
            "suggestion": f"Generate manifest entry from {evidence['commits']} commits and {evidence['notes']} notes"
        }

    # Rule 3: Default to investigation
    return {
        "category": "investigation",
        "reason": "Unclear feature boundaries",
        "auto_action": "none",
        "suggestion": "Review events/commits to determine if feature tracking is appropriate"
    }

def feature_exists_in_manifest(feature_id: str) -> bool:
    """Check if feature already documented in manifest"""
    manifest = Path('feature-manifest.yaml')
    if manifest.exists():
        content = manifest.read_text()
        return f'id: {feature_id}' in content or \\
               f'{feature_id}' in content.lower()
    return False
'''

        # Add CLI argument for classification phase
        cli_update = '''
@click.option('--phase', type=click.Choice(['detect', 'classify']),
              default='detect', help='Quality check phase')
def main(output, phase):
    """Manifest discovery with optional classification"""

    # DETECT phase (existing logic)
    violations = detect_untracked_features()

    # CLASSIFY phase (new logic)
    if phase == 'classify':
        for violation in violations:
            violation['classification'] = classify_manifest_violation(violation)

    # Output results
    if output == 'json':
        print(json.dumps(violations, indent=2))
'''

        return {
            'status': 'implemented',
            'changes': [
                'Added classify_manifest_violation() function',
                'Added feature_exists_in_manifest() helper',
                'Added --phase CLI argument',
                'Updated output schema with classification metadata'
            ],
            'test_command': 'python scripts/manifest-discover.py --phase classify --output json'
        }
```

**Agent Response Template**:
```
I've implemented L1 (CLASSIFY) for manifest-discovery:

✅ Changes Applied:
  - Added classify_manifest_violation() function (3 classification rules)
  - Added feature_exists_in_manifest() cross-reference helper
  - Updated CLI with --phase classify argument
  - Enhanced output schema with classification metadata

📋 Classification Rules:
  1. False Positive: Feature already in manifest
  2. Auto-fixable: Clear deliverables (commits > 10, notes > 0)
  3. Investigation: Unclear boundaries or event-only features

🧪 Test Command:
  python scripts/manifest-discover.py --phase classify --output json

📊 Expected Impact:
  - Before: 12 violations, all require manual triage (45-60 min)
  - After: 5 auto-fixable, 1 investigate, 6 false-positive (20-30 min triage)
  - Toil Reduction: 60% (from 45-60 min → 20-30 min)

Next Step: Implement L2 (REMEDIATE) for auto-fixable violations?
```

---

### Workflow 3: Implement L2 (REMEDIATE) Phase

**User Request**: "Build auto-fix script for manifest discovery"

**Agent Action**:

```python
def implement_l2_remediation(check_name: str):
    """
    Add REMEDIATE phase with auto-fix scripts

    Steps:
    1. Create remediation script (scripts/remediate-{check_name}.py)
    2. Read CLASSIFY output and filter auto-fixable violations
    3. Generate remediation plan (preview changes)
    4. Apply fixes with confirmation prompt
    5. Validate post-fix (run original quality check)
    6. Add justfile recipe: just health-fix-{check_name}
    """

    if check_name == 'manifest-discovery':
        remediation_script = '''
#!/usr/bin/env python3
"""
Remediate manifest discovery violations (L2 phase)

Usage:
    python scripts/remediate-manifest-discovery.py --interactive
    python scripts/remediate-manifest-discovery.py --auto-approve --input classify-output.json
"""

import click
import json
from pathlib import Path

@click.command()
@click.option('--input', type=click.Path(exists=True), help='Classification output JSON')
@click.option('--interactive/--auto-approve', default=True, help='Prompt for confirmation')
def main(input, interactive):
    """Auto-fix manifest discovery violations"""

    # Read classification output
    if input:
        with open(input) as f:
            data = json.load(f)
    else:
        # Run classify phase inline
        result = subprocess.run(
            ['python', 'scripts/manifest-discover.py', '--phase', 'classify', '--output', 'json'],
            capture_output=True, text=True
        )
        data = json.loads(result.stdout)

    # Filter auto-fixable violations
    auto_fixable = [
        v for v in data.get('violations', [])
        if v.get('classification', {}).get('category') == 'auto_fixable'
    ]

    if not auto_fixable:
        print("No auto-fixable violations found")
        return

    print(f"Found {len(auto_fixable)} auto-fixable violations")

    # Generate remediation plan
    for violation in auto_fixable:
        print(f"\\n📋 Violation: {violation['id']}")
        print(f"   Action: {violation['classification']['auto_action']}")

        if violation['classification']['auto_action'] == 'add_to_manifest':
            # Generate manifest entry
            entry = generate_manifest_entry(violation)
            print(f"   Preview:\\n{entry[:200]}...")

            # Prompt for confirmation
            if interactive:
                response = input("   Apply this fix? [y/N] ")
                if response.lower() != 'y':
                    print("   Skipped")
                    continue

            # Apply fix
            insert_manifest_entry(entry, after_line=find_insertion_point())
            print("   ✅ Applied")

    # Validate post-fix
    print("\\n🧪 Validating fixes...")
    result = subprocess.run(
        ['python', 'scripts/validate-traceability.py'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print("✅ Validation passed")
    else:
        print("❌ Validation failed - rollback recommended")

def generate_manifest_entry(violation: dict) -> str:
    """Generate YAML manifest entry from violation data"""
    # Implementation would extract from git/events/notes
    pass

def find_insertion_point() -> int:
    """Find appropriate line to insert new entry"""
    # Logic to find insertion point in feature-manifest.yaml
    pass

def insert_manifest_entry(entry: str, after_line: int):
    """Insert entry into manifest file"""
    # Implementation would update feature-manifest.yaml
    pass

if __name__ == '__main__':
    main()
'''

        justfile_recipe = '''
# Auto-fix manifest discovery violations (L2 phase)
health-fix-manifest-discovery:
    #!/usr/bin/env bash
    echo "🔍 Running manifest discovery classification..."
    CLASSIFY_OUTPUT=$(python scripts/manifest-discover.py --phase classify --output json)

    # Count auto-fixable violations
    AUTO_FIXABLE=$(echo "$CLASSIFY_OUTPUT" | jq '[.violations[] | select(.classification.category == "auto_fixable")] | length')

    if [ "$AUTO_FIXABLE" -eq 0 ]; then
        echo "✅ No auto-fixable violations found"
        exit 0
    fi

    echo "Found $AUTO_FIXABLE auto-fixable violations"
    echo ""

    # Run remediation script
    python scripts/remediate-manifest-discovery.py --interactive
'''

        return {
            'status': 'implemented',
            'files_created': [
                'scripts/remediate-manifest-discovery.py',
                'justfile (added health-fix-manifest-discovery recipe)'
            ],
            'test_command': 'just health-fix-manifest-discovery'
        }
```

**Agent Response Template**:
```
I've implemented L2 (REMEDIATE) for manifest-discovery:

✅ Files Created:
  - scripts/remediate-manifest-discovery.py (auto-fix script)
  - justfile recipe: health-fix-manifest-discovery

🔧 Remediation Workflow:
  1. Read CLASSIFY output (filter auto-fixable violations)
  2. Generate remediation plan (preview YAML entries)
  3. Prompt for confirmation (--interactive mode)
  4. Apply fixes to feature-manifest.yaml
  5. Validate with scripts/validate-traceability.py
  6. Rollback on validation failure

🧪 Test Command:
  just health-fix-manifest-discovery

📊 Expected Impact:
  - Before: Manual addition of 5 features (60-90 min)
  - After: One-command batch operation (5-10 min)
  - Toil Reduction: 85-90% (from 60-90 min → 5-10 min)

🎯 Total L0→L2 Impact:
  - L0: 2-3 hours/week (manual triage + manual fixes)
  - L2: 20-30 min/week (auto-classification + auto-fix)
  - Overall Toil Reduction: 85-90%

Next Step: Implement L3 (TRACK) for trend monitoring?
```

---

### Workflow 4: Implement L3 (TRACK) Phase

**User Request**: "Add quality metrics tracking over time"

**Agent Action**:

```python
def implement_l3_tracking(check_name: str):
    """
    Add TRACK phase with time-series metrics

    Steps:
    1. Define metrics snapshot schema (A-MEM event format)
    2. Emit metrics event after each health check run
    3. Create trend analysis script
    4. Add dashboard/report generation (optional)
    5. Add justfile recipe: just health-track-{check_name}
    """

    if check_name == 'script-refactoring-audit':
        tracking_code = '''
def emit_metrics_snapshot(metrics: dict):
    """
    Emit quality metrics snapshot to A-MEM

    Metrics are stored in .chora/memory/events/ for time-series analysis
    """
    from datetime import datetime
    import json

    event = {
        "event_type": "quality_metrics_snapshot",
        "timestamp": datetime.now().isoformat() + "Z",
        "check_name": "script-refactoring-audit",
        "metrics": metrics,
        "metadata": {
            "trace_id": f"weekly-health-{datetime.now().strftime('%Y-%m-%d')}",
            "context": "sprint-10"
        }
    }

    # Append to monthly event log
    event_file = Path(f'.chora/memory/events/{datetime.now().strftime("%Y-%m")}.jsonl')
    with open(event_file, 'a') as f:
        f.write(json.dumps(event) + '\\n')

    return event

# Usage in quality check script
metrics = {
    "utf8_compliance": {
        "value": 65.6,
        "unit": "percent",
        "numerator": 84,
        "denominator": 128,
        "target": 100.0
    },
    "jsonexporter_usage": {
        "value": 24.8,
        "unit": "percent",
        "numerator": 34,
        "denominator": 137,
        "target": 100.0
    }
}

emit_metrics_snapshot(metrics)
'''

        trend_analysis_script = '''
#!/usr/bin/env python3
"""
Analyze quality metrics trends over time (L3 phase)

Usage:
    python scripts/track-quality-metrics.py --check script-refactoring-audit --period 90
"""

import click
import json
from datetime import datetime, timedelta
from pathlib import Path

@click.command()
@click.option('--check', required=True, help='Quality check name')
@click.option('--period', default=90, help='Period in days')
def main(check, period):
    """Analyze quality metrics trends"""

    # Read all metrics snapshots for this check
    snapshots = []
    cutoff = datetime.now() - timedelta(days=period)

    for event_file in Path('.chora/memory/events/').glob('*.jsonl'):
        with open(event_file) as f:
            for line in f:
                event = json.loads(line)
                if (event.get('event_type') == 'quality_metrics_snapshot' and
                    event.get('check_name') == check):
                    timestamp = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                    if timestamp >= cutoff:
                        snapshots.append(event)

    if len(snapshots) < 5:
        print(f"⚠️  Insufficient data: {len(snapshots)} snapshots (need ≥5)")
        return

    # Analyze trends for each metric
    for metric_name in snapshots[0].get('metrics', {}).keys():
        values = [(s['timestamp'], s['metrics'][metric_name]['value'])
                  for s in snapshots]
        values.sort(key=lambda x: x[0])

        # Calculate velocity (change per week)
        first_value = values[0][1]
        last_value = values[-1][1]
        days_elapsed = (datetime.fromisoformat(values[-1][0].replace('Z', '+00:00')) -
                       datetime.fromisoformat(values[0][0].replace('Z', '+00:00'))).days
        velocity = (last_value - first_value) / (days_elapsed / 7) if days_elapsed > 0 else 0

        # Determine trend direction
        if abs(velocity) < 0.5:
            direction = "stable"
            alert = "warning" if last_value < snapshots[0]['metrics'][metric_name].get('target', 100) else "info"
        elif velocity > 0.5:
            direction = "improving"
            alert = "info"
        else:
            direction = "degrading"
            alert = "error"

        print(f"\\n📊 {metric_name}:")
        print(f"   Current: {last_value:.1f}%")
        print(f"   Velocity: {velocity:+.2f}%/week")
        print(f"   Trend: {direction}")
        print(f"   Alert: {alert}")

        if direction == "stable" and alert == "warning":
            print(f"   💡 Recommendation: Trigger L2 remediation phase")

if __name__ == '__main__':
    main()
'''

        justfile_recipe = '''
# Track quality metrics trends (L3 phase)
health-track-{{check_name}}:
    python scripts/track-quality-metrics.py --check {{check_name}} --period 90
'''

        return {
            'status': 'implemented',
            'changes': [
                'Added emit_metrics_snapshot() to quality check',
                'Created scripts/track-quality-metrics.py',
                'Added justfile recipe: health-track-{check_name}'
            ],
            'test_command': f'just health-track-{check_name}'
        }
```

**Agent Response Template**:
```
I've implemented L3 (TRACK) for script-refactoring-audit:

✅ Changes Applied:
  - Added emit_metrics_snapshot() to audit script
  - Created scripts/track-quality-metrics.py (trend analysis)
  - Added justfile recipe: health-track-script-refactoring-audit

📊 Tracking Metrics:
  - utf8_compliance (target: 100%)
  - jsonexporter_usage (target: 100%)
  - emoji_removal (target: 100%)

🔍 Trend Analysis:
  - Analyzes last 90 days of snapshots (≥5 required)
  - Calculates velocity (%/week change)
  - Detects: improving, stable, degrading trends
  - Alerts: error (degrading), warning (stable below target), info (improving)

🧪 Test Command:
  just health-track-script-refactoring-audit

📈 Example Output:
  📊 utf8_compliance:
     Current: 65.6%
     Velocity: +0.2%/week
     Trend: stable
     Alert: warning
     💡 Recommendation: Trigger L2 remediation phase

Next Step: Implement L4 (PREVENT) with pre-commit hooks?
```

---

### Workflow 5: Implement L4 (PREVENT) Phase

**User Request**: "Block new violations with pre-commit hooks"

**Agent Action**:

```python
def implement_l4_prevention(check_name: str):
    """
    Add PREVENT phase with pre-commit hooks

    Steps:
    1. Create baseline file (.quality-baseline.json)
    2. Create pre-commit hook script (scripts/prevent-{check_name}.py)
    3. Add hook to .pre-commit-config.yaml
    4. Hook blocks NEW violations only (allows pre-existing)
    5. Exit code 0 (no new violations), 1 (new violations), 2 (pre-existing warnings)
    """

    if check_name == 'manifest-discovery':
        baseline_schema = {
            "check_name": "manifest-discovery",
            "baseline_date": "2025-11-20",
            "known_violations": [
                {
                    "id": "FEAT-LEGACY-001",
                    "type": "untracked_feature",
                    "acknowledged": True,
                    "acknowledged_by": "victorpiper",
                    "acknowledged_date": "2025-11-20",
                    "reason": "Legacy feature from before manifest adoption"
                }
            ],
            "prevention_rules": {
                "block_new_violations": True,
                "allow_pre_existing": True,
                "require_acknowledgement": True
            }
        }

        prevention_hook = '''
#!/usr/bin/env python3
"""
Pre-commit hook: Prevent untracked features (L4 phase)

Exit codes:
- 0: No new violations (commit allowed)
- 1: New violations detected (commit blocked)
- 2: Pre-existing violations (warning, commit allowed)
"""

import sys
import json
from pathlib import Path

def main():
    # Load baseline
    baseline = json.loads(Path('.quality-baseline.json').read_text())
    known_ids = {v['id'] for v in baseline['known_violations']}

    # Run detection on staged changes only
    result = subprocess.run(
        ['python', 'scripts/manifest-discover.py', '--staged-only', '--output', 'json'],
        capture_output=True, text=True
    )
    current_violations = json.loads(result.stdout).get('violations', [])

    # Separate new vs pre-existing
    new_violations = [v for v in current_violations if v['id'] not in known_ids]
    pre_existing = [v for v in current_violations if v['id'] in known_ids]

    # Output results
    if new_violations:
        print(f"❌ BLOCKED: {len(new_violations)} new untracked features detected")
        for v in new_violations:
            print(f"   - {v['id']}: {v['description']}")
        print("\\n💡 Fix: just health-fix-manifest-discovery")
        return 1  # Block commit

    if pre_existing:
        print(f"⚠️  WARNING: {len(pre_existing)} pre-existing violations (acknowledged)")
        return 2  # Allow commit with warning

    print("✅ No new violations detected")
    return 0  # Allow commit

if __name__ == '__main__':
    sys.exit(main())
'''

        pre_commit_config = '''
repos:
  - repo: local
    hooks:
      - id: prevent-manifest-discovery
        name: Prevent untracked features
        entry: scripts/prevent-untracked-features.py
        language: python
        stages: [commit]
        pass_filenames: false
        args:
          - --baseline=.quality-baseline.json
'''

        return {
            'status': 'implemented',
            'files_created': [
                '.quality-baseline.json',
                'scripts/prevent-untracked-features.py',
                '.pre-commit-config.yaml (updated)'
            ],
            'test_command': 'git commit -m "test" (will trigger hook)'
        }
```

**Agent Response Template**:
```
I've implemented L4 (PREVENT) for manifest-discovery:

✅ Files Created:
  - .quality-baseline.json (acknowledged pre-existing violations)
  - scripts/prevent-untracked-features.py (pre-commit hook)
  - .pre-commit-config.yaml (hook configuration)

🚫 Prevention Rules:
  - Block NEW violations (untracked features in this commit)
  - Allow PRE-EXISTING violations (acknowledged in baseline)
  - Exit 0: No new violations (commit allowed)
  - Exit 1: New violations (commit BLOCKED)
  - Exit 2: Pre-existing warnings (commit allowed)

🧪 Test Commands:
  # Create baseline
  python scripts/create-quality-baseline.py --check manifest-discovery

  # Test hook manually
  python scripts/prevent-untracked-features.py

  # Test via git commit
  git commit -m "test: trigger prevention hook"

📊 Complete L0→L4 Journey:
  ✅ L0 (DETECT): Find untracked features (12 violations)
  ✅ L1 (CLASSIFY): Categorize (5 auto-fixable, 1 investigate, 6 false-positive)
  ✅ L2 (REMEDIATE): Auto-fix 5 features (60-90 min → 5-10 min)
  ✅ L3 (TRACK): Monitor manifest completeness trend over time
  ✅ L4 (PREVENT): Block new untracked features at commit time

🎯 Total Impact:
  - L0: 2-3 hours/week toil
  - L4: 10-15 min/week monitoring only
  - Toil Reduction: 90-95%
  - ROI: 650-870% (12 months)
```

---

## Quick Reference Patterns

### Quality Check Maturity Checklist

Use this checklist to assess any quality check:

**L0 (DETECT-only)** - 🔴 Incomplete Feedback Loop
- [ ] Script finds violations
- [ ] Output is list of violations (often JSON)
- [ ] Human triages manually every time
- ❌ No classification logic
- ❌ No auto-fix scripts
- ❌ No metrics tracking
- ❌ No pre-commit integration

**L1 (CLASSIFY)** - 🟡 Classification Added (2x toil reduction)
- [x] All L0 capabilities
- [x] Classification logic (auto-fixable / investigate / false-positive)
- [x] `--phase classify` CLI argument
- [x] JSON output includes `classification` field
- ❌ No auto-fix scripts
- ❌ No metrics tracking
- ❌ No pre-commit integration

**L2 (REMEDIATE)** - 🟢 Auto-fix Added (5x toil reduction, target for 400-500% ROI)
- [x] All L1 capabilities
- [x] Auto-fix script: `scripts/remediate-{check-name}.py`
- [x] Justfile recipe: `just health-fix-{check-name}`
- [x] Confirmation prompt (--interactive mode)
- [x] Post-fix validation
- ❌ No metrics tracking
- ❌ No pre-commit integration

**L3 (TRACK)** - 🟦 Metrics Added (1.2x improvement via trend detection)
- [x] All L2 capabilities
- [x] Metrics snapshot emission (A-MEM events)
- [x] Trend analysis script: `scripts/track-quality-metrics.py`
- [x] Justfile recipe: `just health-track-{check-name}`
- [x] Alert generation (degrading metrics)
- ❌ No pre-commit integration

**L4 (PREVENT)** - 🟪 Prevention Added (1.3x improvement, quality baseline maintained)
- [x] All L3 capabilities
- [x] Quality baseline: `.quality-baseline.json`
- [x] Pre-commit hook: `scripts/prevent-{check-name}.py`
- [x] Hook config: `.pre-commit-config.yaml`
- [x] Blocks NEW violations only (allows pre-existing)
- [x] Exit codes: 0 (allow), 1 (block), 2 (warn)

---

## Common Agent Pitfalls

### Pitfall 1: Jumping Directly to L2 Without L1 Classification

**❌ Bad Pattern**:
```
User: "Build auto-fix script for quality check"
Agent: *Creates remediation script without classification logic*
→ Result: Auto-fixes ALL violations, including ones that shouldn't be auto-fixed
```

**✅ Good Pattern**:
```
User: "Build auto-fix script for quality check"
Agent: "First, let me add L1 classification to identify which violations are auto-fixable"
Agent: *Implements CLASSIFY phase first*
Agent: "Now I'll create L2 remediation for the auto-fixable subset (60-80% of violations)"
```

**Why**: Classification is prerequisite for safe auto-fixing. Remediating unclassified violations risks destructive changes.

---

### Pitfall 2: L4 Prevention Blocking on Pre-existing Violations

**❌ Bad Pattern**:
```python
# Pre-commit hook blocks ALL violations (including pre-existing)
if violations:
    print(f"❌ BLOCKED: {len(violations)} violations")
    return 1  # Blocks commit even for pre-existing issues
```

**✅ Good Pattern**:
```python
# Pre-commit hook blocks NEW violations only
baseline = load_quality_baseline()
new_violations = [v for v in violations if v['id'] not in baseline['known_ids']]

if new_violations:
    print(f"❌ BLOCKED: {len(new_violations)} NEW violations")
    return 1  # Blocks commit only for new issues

if violations:
    print(f"⚠️  WARNING: {len(violations)} pre-existing (acknowledged)")
    return 2  # Allows commit with warning
```

**Why**: Blocking on pre-existing violations drives `--no-verify` bypass culture. L4 should prevent regressions, not block all development.

---

### Pitfall 3: No Post-fix Validation in L2 Remediation

**❌ Bad Pattern**:
```python
# Apply fix without validation
insert_manifest_entry(entry)
print("✅ Fix applied")
# No validation, assumes fix is correct
```

**✅ Good Pattern**:
```python
# Apply fix with validation
insert_manifest_entry(entry)

# Validate post-fix
result = subprocess.run(['python', 'scripts/validate-traceability.py'])
if result.returncode == 0:
    print("✅ Fix applied and validated")
else:
    print("❌ Fix validation failed - rolling back")
    rollback_changes()
    sys.exit(1)
```

**Why**: Auto-fix scripts can introduce bugs. Post-fix validation catches errors before they're committed.

---

### Pitfall 4: Overly Complex Classification Rules

**❌ Bad Pattern**:
```python
# 20 classification rules with complex conditional logic
def classify_violation(violation):
    if (violation['evidence']['commits'] > 10 and
        violation['evidence']['notes'] > 0 and
        violation['evidence']['events'] > 5 and
        not violation['description'].startswith('WIP') and
        'test' in violation.get('tags', []) and
        ...):  # 15 more conditions
        return {"category": "auto_fixable"}
```

**✅ Good Pattern**:
```python
# Start with 2-3 simple rules, iterate based on feedback
def classify_violation(violation):
    # Rule 1: False positive (already in manifest)
    if feature_exists_in_manifest(violation['id']):
        return {"category": "false_positive"}

    # Rule 2: Auto-fixable (clear deliverables)
    if violation['evidence']['commits'] > 10 and violation['evidence']['notes'] > 0:
        return {"category": "auto_fixable"}

    # Default: Investigation required
    return {"category": "investigation"}
```

**Why**: Start simple, refine based on classification accuracy metrics. Complex rules are hard to maintain and debug.

---

## Integration with Other SAPs

### SAP-006 (Quality Gates)

**Integration**: L4 prevention phase uses SAP-006 pre-commit hook framework

**Pattern**:
```yaml
# .pre-commit-config.yaml (SAP-006)
repos:
  - repo: local
    hooks:
      # SAP-054 L4 prevention hooks
      - id: prevent-manifest-discovery
        entry: scripts/prevent-untracked-features.py
        language: python
        stages: [commit]

      - id: prevent-script-regression
        entry: scripts/prevent-script-regression.py
        language: python
        types: [python]
        stages: [commit]
```

---

### SAP-010 (Memory System)

**Integration**: L3 tracking phase uses A-MEM for metrics storage

**Pattern**:
```python
# Emit quality metrics as A-MEM events
event = {
    "event_type": "quality_metrics_snapshot",
    "timestamp": datetime.now().isoformat() + "Z",
    "check_name": "script-refactoring-audit",
    "metrics": {...},
    "metadata": {
        "trace_id": f"weekly-health-{datetime.now().strftime('%Y-%m-%d')}"
    }
}

# Append to .chora/memory/events/2025-11.jsonl
with open(event_file, 'a') as f:
    f.write(json.dumps(event) + '\\n')
```

---

### SAP-050 (SAP Adoption Verification)

**Integration**: SAP-050 itself should adopt SAP-054 pattern

**Recommendation**: Apply SAP-054 to SAP-050 verification:
- L1: Classify verification failures (auto-fixable / investigate)
- L2: Auto-fix missing sections (generate templates)
- L3: Track SAP quality over time
- L4: Pre-commit hook blocks incomplete SAP structure

---

### SAP-056 (Lifecycle Traceability)

**Integration**: Traceability validation is reference implementation for SAP-054

**Pattern**:
- L0: 60% pass rate (40% violations)
- L1: Classify missing vision_ref (auto-fixable) vs missing tests (investigation)
- L2: Auto-add vision_ref, auto-add test type=manual for process features
- L3: Track traceability compliance over time
- L4: Block commits introducing new traceability violations

---

## Adoption Checklist

Use this checklist when implementing SAP-054 for a quality check:

### Phase 1: Assessment (30 min)
- [ ] Identify quality check currently at L0
- [ ] Estimate weekly toil (hours)
- [ ] Analyze violation patterns (what types of violations occur?)
- [ ] Determine classification categories (auto-fixable? investigation? false-positive?)

### Phase 2: L1 Implementation (2-3 hours)
- [ ] Add classification function (3-5 classification rules)
- [ ] Update quality check script with `--phase classify`
- [ ] Enhance JSON output with `classification` field
- [ ] Test classification accuracy (>80% target)
- [ ] Document classification rules

### Phase 3: L2 Implementation (4-6 hours)
- [ ] Create remediation script (`scripts/remediate-{check-name}.py`)
- [ ] Implement auto-fix logic for each auto-fixable category
- [ ] Add confirmation prompt (--interactive mode)
- [ ] Add post-fix validation
- [ ] Create justfile recipe (`just health-fix-{check-name}`)
- [ ] Test auto-fix on sample violations

### Phase 4: L3 Implementation (2-3 hours)
- [ ] Add metrics snapshot emission (A-MEM events)
- [ ] Create trend analysis script (`scripts/track-quality-metrics.py`)
- [ ] Add justfile recipe (`just health-track-{check-name}`)
- [ ] Collect ≥5 snapshots for trend validation
- [ ] Test trend detection (improving / stable / degrading)

### Phase 5: L4 Implementation (3-4 hours)
- [ ] Create quality baseline (`.quality-baseline.json`)
- [ ] Create prevention hook script (`scripts/prevent-{check-name}.py`)
- [ ] Update `.pre-commit-config.yaml` with new hook
- [ ] Test hook: blocks new violations, allows pre-existing
- [ ] Document bypass procedure (when to use `--no-verify`)

### Phase 6: Validation (1-2 hours)
- [ ] Run weekly health check workflow end-to-end
- [ ] Measure toil reduction (before/after comparison)
- [ ] Calculate ROI (time invested vs time saved)
- [ ] Document results in knowledge note
- [ ] Update SAP-054 ledger with adoption

---

**Version**: 1.0.0
**Status**: Draft
**Next Review**: After L1 reference implementation validation (OPP-2025-040)
