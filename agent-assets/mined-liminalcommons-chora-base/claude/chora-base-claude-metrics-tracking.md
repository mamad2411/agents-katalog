# Metrics Tracking - Claude-Specific Awareness (SAP-013)

**SAP ID**: SAP-013
**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-05

---

## 📖 Quick Reference

**New to SAP-013?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - Interactive and programmatic tracking examples
- 📚 **ClaudeROICalculator API** - Python dataclasses and methods
- 🎯 **4 Metric Categories** - Quality, Velocity, Process, Adoption with targets
- 📊 **CLI Commands** - All justfile recipes with examples
- 🔧 **Troubleshooting** - 3 common problems with solutions

**This CLAUDE.md provides**: Claude Code tool integration patterns (Bash for metrics commands, Read for reports, Write for custom tracking).

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "Claude (first-time orientation)"
  estimated_tokens: 5000
  estimated_time_minutes: 3
  sections:
    - "1. Quick Start for Claude"
    - "2. When to Use Metrics Tracking"
    - "3. Tool Integration Patterns"

phase_2_implementation:
  target_audience: "Claude implementing metrics tracking"
  estimated_tokens: 15000
  estimated_time_minutes: 10
  sections:
    - "4. Key Workflows (Claude Code)"
    - "5. Integration with Other SAPs"

phase_3_deep_dive:
  target_audience: "Claude analyzing metrics"
  estimated_tokens: 30000
  estimated_time_minutes: 20
  files_to_read:
    - "protocol-spec.md (complete metrics specification)"
    - "PROCESS_METRICS.md (comprehensive metrics guide)"
    - "src/claude_roi_calculator.py (implementation)"
```

---

## 1. Quick Start for Claude

### What is Metrics Tracking? (Claude perspective)

**Metrics Tracking (SAP-013)** provides **ROI calculation and process metrics** for Claude effectiveness:
- **ClaudeROICalculator**: Track time saved, cost savings, quality
- **Dashboards**: Sprint, release, and trend reports
- **Process Adherence**: DDD/BDD/TDD tracking

**Claude's Role**:
- Track sessions using **Bash tool** (Python scripts)
- Generate reports using **Bash tool** (ClaudeROICalculator)
- Create dashboards using **Write tool** (markdown)
- Export metrics using **Bash tool** (CSV/JSON)

---

### When Should Claude Use This?

**Use Metrics Tracking when**:
- User asks "Is Claude saving time?"
- Need to demonstrate ROI to stakeholders
- Sprint/release metrics needed
- Process improvement measurement required

**Don't use Metrics Tracking when**:
- Quick prototyping (overhead not justified)
- User doesn't want tracking
- Real-time analytics needed (use Grafana instead)

---

### Tool Integration Patterns

**Bash tool** (for tracking and reporting):
```bash
# Track session using Python
python -c "
from claude_roi_calculator import ClaudeROICalculator, ClaudeMetric
from datetime import datetime

calculator = ClaudeROICalculator(developer_hourly_rate=100)
metric = ClaudeMetric(
    session_id='session-001',
    timestamp=datetime.now(),
    task_type='feature_implementation',
    lines_generated=250,
    time_saved_minutes=120,
    iterations_required=2,
    test_coverage=0.92
)
calculator.add_metric(metric)
print(calculator.generate_report())
"

# Generate sprint dashboard
python scripts/generate_sprint_dashboard.py
```

**Read tool** (for existing metrics):
```bash
# Read existing metrics CSV
Read metrics/claude-metrics.csv

# Read existing dashboards
Read project-docs/sprints/sprint-2025-11-05-dashboard.md
```

**Write tool** (for dashboards):
```bash
# Create sprint dashboard
Write project-docs/sprints/sprint-2025-11-05-dashboard.md
# Content: Velocity, quality, adherence metrics

# Create release dashboard
Write project-docs/releases/v1.5.0-dashboard.md
# Content: Delivery, quality, process, ROI metrics
```

---

## 2. When to Use Metrics Tracking

### User Signal Detection

| User Statement | Claude Action | Tools Used |
|----------------|---------------|------------|
| "Is Claude saving time?" | Track session, generate ROI report | Bash (Python script) |
| "Show sprint velocity" | Generate sprint dashboard | Bash + Write (dashboard) |
| "Are we improving?" | Analyze quality trends | Bash (trend analysis) |
| "Generate release metrics" | Create release dashboard | Bash + Write (dashboard) |
| "What's our ROI?" | Calculate annualized value | Bash (ROI calculator) |

---

## 3. Tool Integration Patterns

### Pattern 1: Track-Report-Export

**Always follow this sequence**:

```markdown
Step 1: Track metrics
Bash: python track_session.py --time-saved 120 --coverage 0.92

Step 2: Generate report
Bash: python generate_roi_report.py

Step 3: Export for analysis
Bash: python export_metrics.py --format csv --output metrics/
```

**Don't**: Generate reports without tracking first

---

### Pattern 2: Dashboard-First Approach

**Create dashboards proactively**:

```markdown
Step 1: Collect metrics
Bash: python collect_sprint_metrics.py

Step 2: Generate dashboard
Write project-docs/sprints/sprint-YYYY-MM-DD-dashboard.md

Step 3: Commit dashboard
Bash: git add project-docs/sprints/
Bash: git commit -m "metrics: Add sprint dashboard"
```

**Don't**: Wait for user to ask for dashboard (create proactively)

---

### Pattern 3: Validate-Before-Report

**Always validate metrics before reporting**:

```markdown
Step 1: Check metrics quality
Read metrics/claude-metrics.csv
# Verify: coverage 0-1, quality 0-10, iterations ≥1

Step 2: Fix invalid metrics if found
# Remove or correct invalid entries

Step 3: Generate report
Bash: python generate_roi_report.py
```

**Don't**: Generate reports from invalid metrics (credibility loss)

---

## 4. Key Workflows (Claude Code)

### Workflow 1: Set Up Metrics Tracking

**Goal**: Initialize metrics tracking for project

**Tools**: Bash (install), Write (config), Read (verify)

**Steps**:

1. **Check if ClaudeROICalculator exists**:
   ```bash
   Bash: ls src/claude_roi_calculator.py
   # If exists, already set up
   ```

2. **If missing, create from SAP template**:
   ```bash
   Read docs/skilled-awareness/metrics-tracking/src/claude_roi_calculator.py
   # Copy template

   Write src/claude_roi_calculator.py
   # Paste template code
   ```

3. **Create metrics directory**:
   ```bash
   Bash: mkdir -p metrics
   Bash: mkdir -p project-docs/sprints
   Bash: mkdir -p project-docs/releases
   ```

4. **Initialize first metric**:
   ```bash
   Bash: python -c "
from src.claude_roi_calculator import ClaudeROICalculator, ClaudeMetric
from datetime import datetime

calculator = ClaudeROICalculator(developer_hourly_rate=100)
metric = ClaudeMetric(
    session_id='session-001',
    timestamp=datetime.now(),
    task_type='feature_implementation',
    lines_generated=100,
    time_saved_minutes=60,
    iterations_required=1,
    test_coverage=0.90
)
calculator.add_metric(metric)
calculator.export_to_csv('metrics/claude-metrics.csv')
print('Metrics tracking initialized')
"
   ```

5. **Verify setup**:
   ```bash
   Bash: ls metrics/claude-metrics.csv
   # Should exist

   Read metrics/claude-metrics.csv
   # Should have first metric
   ```

**Expected Outcome**: Metrics tracking initialized

**Time Estimate**: 5-10 minutes

---

### Workflow 2: Generate ROI Report

**Goal**: Calculate and display ROI for current project

**Tools**: Bash (calculator), Read (metrics)

**Steps**:

1. **Read existing metrics**:
   ```bash
   Read metrics/claude-metrics.csv
   # Verify metrics exist
   ```

2. **Generate ROI report**:
   ```bash
   Bash: python -c "
from src.claude_roi_calculator import ClaudeROICalculator
import csv

calculator = ClaudeROICalculator(developer_hourly_rate=100)

# Load metrics from CSV
with open('metrics/claude-metrics.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # Parse and add metrics
        pass  # Implementation details

print(calculator.generate_report())
print('\n=== Executive Summary ===')
print(calculator.generate_executive_summary())
"
   ```

3. **Save report to file**:
   ```bash
   Bash: python generate_roi_report.py > project-docs/metrics/roi-report-$(date +%Y-%m-%d).md
   ```

4. **Commit report**:
   ```bash
   Bash: git add project-docs/metrics/
   Bash: git commit -m "metrics: Add ROI report"
   ```

**Expected Outcome**: ROI report showing time saved, cost savings, annualized value

**Time Estimate**: 5-10 minutes

---

### Workflow 3: Create Sprint Dashboard

**Goal**: Generate sprint metrics dashboard for retrospective

**Tools**: Bash (collect metrics), Write (dashboard)

**Steps**:

1. **Collect sprint metrics**:
   ```bash
   # If using SAP-015 (beads)
   Bash: bd list --status closed --json > sprint-tasks.json

   # Calculate velocity
   Bash: python -c "
import json
with open('sprint-tasks.json') as f:
    tasks = json.load(f)
story_points = sum(t.get('priority', 1) for t in tasks)
print(f'Sprint velocity: {story_points}')
"
   ```

2. **Create sprint dashboard**:
   ```bash
   Write project-docs/sprints/sprint-2025-11-05-dashboard.md
   ```

   Content:
   ```markdown
   # Sprint Dashboard - 2025-11-05

   ## Velocity
   - **Story Points Completed**: 42 (target: 40, ✅ green)
   - **Tasks Completed**: 15

   ## Quality
   - **Defect Rate**: 2 bugs (target: <3, ✅ green)
   - **Test Coverage**: 94% (target: ≥90%, ✅ green)

   ## Process
   - **Cycle Time**: 2.3 days (target: <3, ✅ green)
   - **DDD Adherence**: 80% (target: ≥80%, ✅ green)
   - **TDD Adherence**: 85% (target: ≥80%, ✅ green)

   ## Recommendations
   ✅ Sprint successful, all targets met
   ```

3. **Commit dashboard**:
   ```bash
   Bash: git add project-docs/sprints/sprint-2025-11-05-dashboard.md
   Bash: git commit -m "metrics: Add sprint dashboard"
   ```

**Expected Outcome**: Sprint dashboard for retrospective

**Time Estimate**: 10-15 minutes

---

## 5. Integration with Other SAPs

### SAP-001 (inbox)

**Integration**: Track metrics per coordination request

**Claude workflow**:
1. When processing coordination request, add trace_id to metrics:
   ```python
   metric = ClaudeMetric(
       trace_id="mcp-taskmgr-2025-003",  # From coordination request
       # ... other fields
   )
   ```

### SAP-015 (task-tracking)

**Integration**: Collect metrics from task completions

**Claude workflow**:
1. After closing tasks, collect metrics:
   ```bash
   Bash: bd list --status closed --json > closed-tasks.json
   # Calculate velocity from task completions
   ```

### SAP-005 (ci-cd-workflows)

**Integration**: Automate metrics collection in CI

**Claude workflow**:
1. Add metrics collection to GitHub Actions:
   ```yaml
   - name: Collect Metrics
     run: python scripts/collect_metrics.py
   ```

---

## 6. Claude-Specific Tips

### Tip 1: Track Every Session Proactively

**Pattern**:
```markdown
At end of each session:
Bash: python track_session.py --time-saved [estimate] --coverage [value]
```

**Why**: Comprehensive tracking enables accurate ROI

### Tip 2: Generate Dashboards Automatically

**Pattern**:
```markdown
After sprint ends:
Write project-docs/sprints/sprint-[date]-dashboard.md
# Auto-generate from metrics
```

**Why**: Regular visibility drives improvement

### Tip 3: Use Conservative Estimates

**Pattern**:
```python
# Underestimate time saved if unsure
time_saved_minutes=90  # Conservative (vs 120 optimistic)
```

**Why**: Credible metrics, stakeholder trust

### Tip 4: Export Metrics Regularly

**Pattern**:
```bash
Bash: python export_metrics.py --format csv --output metrics/
```

**Why**: Backup, external analysis, version control

### Tip 5: Share Reports with Stakeholders

**Pattern**:
```markdown
After generating report:
- Include in sprint review
- Share with management
- Use in retrospectives
```

**Why**: Evidence-based communication

---

## 7. Common Pitfalls

### Pitfall 1: Overestimating Time Saved

**Problem**: Inflating time_saved_minutes for higher ROI

**Fix**: Use conservative estimates, compare to manual baseline

### Pitfall 2: Not Tracking Failed Attempts

**Problem**: Only tracking successful sessions (survivorship bias)

**Fix**: Track all sessions, increment iterations_required

### Pitfall 3: Ignoring Quality Metrics

**Problem**: Only tracking speed, not quality

**Fix**: Always track test_coverage, bugs_introduced, documentation_quality

### Pitfall 4: Not Generating Dashboards

**Problem**: Metrics collected but never analyzed

**Fix**: Generate dashboard after each sprint/release

### Pitfall 5: Using Unrealistic Developer Rates

**Problem**: Inflated hourly rate for exaggerated ROI

**Fix**: Use market rate ($50-150/hour), be transparent

---

## 8. Quick Reference

### Common Bash Commands

```bash
# Track session
python track_session.py --time-saved 120 --coverage 0.92

# Generate ROI report
python generate_roi_report.py

# Export metrics
python export_metrics.py --format csv

# Collect sprint metrics
python collect_sprint_metrics.py

# Generate dashboard
python generate_dashboard.py --type sprint
```

---

### ClaudeMetric Fields

```python
session_id: str                    # Unique identifier
task_type: str                     # feature_implementation | bugfix | refactor
lines_generated: int               # Lines of code generated
time_saved_minutes: int            # Time saved estimate
iterations_required: int           # ≥1
bugs_introduced: int               # Bugs introduced
bugs_fixed: int                    # Bugs fixed
documentation_quality_score: float # 0-10
test_coverage: float               # 0-1
```

---

## 9. Version History

**1.0.0** (2025-11-05):
- Initial CLAUDE.md for SAP-013 (metrics-tracking)
- 3 workflows: setup, ROI report, sprint dashboard
- Integration with SAP-001, SAP-015, SAP-005
- 5 Claude-specific tips, 5 common pitfalls
- Tool usage patterns (Bash, Read, Write)

---

## Quick Links

- **AGENTS.md**: [AGENTS.md](AGENTS.md) - Generic agent patterns (5 workflows)
- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete metrics specification
- **PROCESS_METRICS.md**: [PROCESS_METRICS.md](PROCESS_METRICS.md) - Comprehensive guide
- **Source Code**: [src/claude_roi_calculator.py](src/claude_roi_calculator.py) - Implementation

---

**Next Steps**:
1. Read [AGENTS.md](AGENTS.md) for comprehensive workflow details
2. Read [protocol-spec.md](protocol-spec.md) for complete specification
3. Read [PROCESS_METRICS.md](PROCESS_METRICS.md) for metrics guide
4. See [../AGENTS.md](../AGENTS.md) for SAP catalog navigation
