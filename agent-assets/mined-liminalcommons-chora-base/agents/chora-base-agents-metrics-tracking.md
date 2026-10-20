# Metrics Tracking - Agent Awareness (SAP-013)

**SAP ID**: SAP-013
**Version**: 1.0.0
**Status**: Draft
**Last Updated**: 2025-11-05

---

## 📖 Quick Reference

**New to SAP-013?** → Read **[README.md](README.md)** first (5-min read)

The README provides:
- 🚀 **Quick Start** - 4 ways to track metrics (interactive, programmatic, summary, coverage)
- 📚 **ClaudeROICalculator API** - Complete Python API with examples
- 🎯 **4 Metric Categories** - Quality, Velocity, Process Adherence, Adoption
- 📊 **CLI Commands** - track-claude-session, metrics-summary, coverage-metrics
- 🔧 **Troubleshooting** - Import errors, red metrics, automation tips

**This AGENTS.md provides**: Agent-specific patterns for metrics collection, ROI calculation, and integration workflows.

---

## Progressive Context Loading

```yaml
phase_1_quick_reference:
  target_audience: "All agents (first-time orientation)"
  estimated_tokens: 8000
  estimated_time_minutes: 5
  sections:
    - "1. Quick Start for Agents"
    - "2. What You Can Do"
    - "3. When to Use This Capability"
    - "4. Common User Signals"

phase_2_implementation:
  target_audience: "Agents implementing metrics tracking"
  estimated_tokens: 25000
  estimated_time_minutes: 15
  sections:
    - "5. How It Works"
    - "6. Key Workflows"
    - "7. Integration with Other SAPs"

phase_3_deep_dive:
  target_audience: "Agents analyzing metrics or generating reports"
  estimated_tokens: 50000
  estimated_time_minutes: 30
  files_to_read:
    - "protocol-spec.md (complete metrics specification)"
    - "capability-charter.md (ROI rationale)"
    - "PROCESS_METRICS.md (complete metrics guide)"
    - "src/claude_roi_calculator.py (implementation)"
```

---

## 1. Quick Start for Agents

### What is Metrics Tracking? (60-second overview)

**Metrics Tracking (SAP-013)** provides **standardized metrics for Claude effectiveness and process quality**:

- **ClaudeROICalculator**: Track time saved, quality metrics, ROI
- **Process Metrics**: Quality, velocity, adherence dashboards
- **Sprint/Release Reports**: Markdown-based KPI summaries
- **Automation**: CI/CD integration for automated collection

**Purpose**: Enable data-driven decision making and demonstrate Claude's value.

**Key Benefits**:
- **Demonstrate ROI**: Track time saved, cost savings ($109k+/year per developer)
- **Process Insights**: Identify what's working, what needs improvement
- **Evidence-Based**: Replace guesswork with data
- **Stakeholder Communication**: Show progress with concrete metrics

---

### When Should You Use This?

**Use Metrics Tracking when**:
- User asks "Is Claude saving time?"
- Team needs to demonstrate ROI to stakeholders
- Process improvements need measurement
- Sprint/release metrics needed for retrospectives
- Documentation mentions "metrics", "ROI", or "KPIs"

**Don't use Metrics Tracking when**:
- Quick prototyping (overhead not justified)
- User explicitly doesn't want tracking
- Metrics would create friction (early-stage projects)
- Real-time analytics needed (use Grafana/Datadog instead)

---

### Quick Command Reference

```python
# Track Claude session
from claude_roi_calculator import ClaudeROICalculator, ClaudeMetric

calculator = ClaudeROICalculator(developer_hourly_rate=100)
metric = ClaudeMetric(
    session_id="session-001",
    task_type="feature_implementation",
    lines_generated=250,
    time_saved_minutes=120,
    iterations_required=2,
    test_coverage=0.92
)
calculator.add_metric(metric)

# Generate reports
print(calculator.generate_report())
calculator.export_to_csv("metrics.csv")
```

---

## 2. What You Can Do

### Core Capabilities

1. **Track Claude Effectiveness**
   - Time saved per session
   - Lines of code generated
   - Iterations required (first-pass success rate)
   - Bugs introduced vs fixed
   - Documentation quality
   - Test coverage

2. **Calculate ROI**
   - Cost savings ($developer_rate × hours_saved)
   - Acceleration factor (speed improvement)
   - Quality metrics (defect rate, coverage)
   - Annualized value ($109k+/year estimate)

3. **Monitor Process Metrics**
   - Quality: Defect rate, test coverage, technical debt
   - Velocity: Sprint velocity, cycle time, lead time
   - Adherence: DDD/BDD/TDD adoption rates
   - Adoption: Downloads, upgrade rate, satisfaction

4. **Generate Dashboards**
   - Sprint dashboard (velocity, quality, adherence)
   - Release dashboard (defects, coverage, cycle time)
   - Process trends (30-day, 90-day improvements)

5. **Automate Collection**
   - CI/CD integration (GitHub Actions)
   - Automated sprint reports
   - Trend analysis

---

### Integration Points

**SAP-001 (inbox)**:
- Track metrics per coordination request (use CHORA_TRACE_ID)
- Measure coordination effectiveness
- ROI per inbox workflow

**SAP-010 (memory-system)**:
- Metrics stored as events in A-MEM
- Query historical metrics via event logs
- Correlate metrics with development events

**SAP-015 (task-tracking)**:
- Metrics per task (time saved, iterations)
- Sprint velocity from task completion
- Quality metrics from task outcomes

**SAP-005 (ci-cd-workflows)**:
- CI collects metrics automatically
- GitHub Actions generate reports
- Metrics validate quality gates

---

## 3. When to Use This Capability

### User Signal Pattern: ROI Demonstration

| User Statement | Interpretation | Recommended Action |
|----------------|----------------|---------------------|
| "Is Claude worth the investment?" | Need ROI metrics | Set up ClaudeROICalculator, track sessions |
| "How much time does Claude save?" | Need time-saved tracking | Track time_saved_minutes per session |
| "Show me Claude's value" | Need executive summary | Generate ROI report with annualized value |
| "What's our development cost savings?" | Need cost analysis | Calculate cost_savings = rate × hours_saved |
| "Should we invest more in AI tools?" | Need business case | Generate comprehensive ROI report |

---

### User Signal Pattern: Process Improvement

| User Statement | Interpretation | Recommended Action |
|----------------|----------------|---------------------|
| "Are we improving over time?" | Need trend analysis | Generate 30-day and 90-day trend reports |
| "What's our defect rate?" | Need quality metrics | Track bugs_introduced and bugs_fixed |
| "Is test coverage increasing?" | Need coverage metrics | Track test_coverage per sprint |
| "Are we following DDD/BDD/TDD?" | Need adherence metrics | Track process_adherence rates |
| "Sprint velocity declining?" | Need velocity metrics | Track sprint_velocity over time |

---

## 4. Common User Signals

### Signal 1: "Is Claude saving time?"

**Context**: User needs to demonstrate Claude's value

**Agent Response**:
1. Set up ClaudeROICalculator:
   ```python
   from claude_roi_calculator import ClaudeROICalculator, ClaudeMetric
   from datetime import datetime

   # Set developer rate (average: $50-150/hour)
   calculator = ClaudeROICalculator(developer_hourly_rate=100)
   ```

2. Track current session:
   ```python
   metric = ClaudeMetric(
       session_id="session-001",
       timestamp=datetime.now(),
       task_type="feature_implementation",
       lines_generated=250,
       time_saved_minutes=120,  # User estimates 2 hours saved
       iterations_required=2,
       bugs_introduced=0,
       bugs_fixed=3,
       documentation_quality_score=8.5,
       test_coverage=0.92
   )
   calculator.add_metric(metric)
   ```

3. Generate ROI report:
   ```python
   print(calculator.generate_report())
   ```

   Output:
   ```
   === Claude ROI Report ===
   Time Saved: 2.0 hours
   Cost Savings: $200.00
   Lines Generated: 250
   Iterations: 2 (first-pass success: 50%)
   Bugs Introduced: 0
   Bugs Fixed: 3
   Test Coverage: 92%
   Documentation Quality: 8.5/10
   ```

4. Calculate annualized value:
   ```python
   print(calculator.generate_executive_summary())
   ```

   Output:
   ```
   === Executive Summary ===
   Based on 1 session(s):
   - Average time saved: 2.0 hours/session
   - Annualized value (assuming 260 working days): $104,000/year
   - Quality improvement: 92% test coverage, 3 bugs fixed
   - Recommendation: High ROI, continue using Claude
   ```

**Expected Outcome**: Concrete ROI metrics demonstrating value

---

### Signal 2: "What's our sprint velocity?"

**Context**: Team needs velocity metrics for sprint retrospective

**Agent Response**:
1. Track tasks completed this sprint:
   ```python
   # Assuming integration with SAP-015 (beads)
   import subprocess
   import json

   # Get closed tasks from this sprint
   result = subprocess.run(
       ["bd", "list", "--status", "closed", "--json"],
       capture_output=True,
       text=True
   )
   tasks = json.loads(result.stdout)

   # Calculate velocity
   story_points = sum(task.get("priority", 1) for task in tasks)
   sprint_velocity = story_points
   ```

2. Generate sprint dashboard:
   ```markdown
   ## Sprint Dashboard

   **Velocity**: 42 story points (target: 40, ✅ green)
   **Defect Rate**: 2 bugs (target: <3, ✅ green)
   **Test Coverage**: 94% (target: ≥90%, ✅ green)
   **Cycle Time**: 2.3 days (target: <3, ✅ green)
   ```

3. Save to project-docs/:
   ```bash
   echo "[dashboard]" > project-docs/sprints/sprint-2025-11-05-dashboard.md
   ```

**Expected Outcome**: Sprint metrics for retrospective

---

### Signal 3: "Are we following DDD/BDD/TDD?"

**Context**: Team wants to measure process adherence

**Agent Response**:
1. Check for documentation-first commits (DDD):
   ```bash
   # Count commits with docs/ before src/
   git log --oneline --name-only | grep -B 1 "^docs/" | grep -A 1 "^src/" | wc -l
   ```

2. Check for test-first commits (TDD):
   ```bash
   # Count commits with tests/ before src/
   git log --oneline --name-only | grep -B 1 "^tests/" | grep -A 1 "^src/" | wc -l
   ```

3. Calculate adherence rates:
   ```python
   total_commits = 100
   ddd_commits = 75  # Docs before code
   tdd_commits = 80  # Tests before code

   ddd_adherence = (ddd_commits / total_commits) * 100  # 75%
   tdd_adherence = (tdd_commits / total_commits) * 100  # 80%
   ```

4. Generate process adherence report:
   ```markdown
   ## Process Adherence

   **DDD (Documentation-Driven Development)**: 75% (target: ≥80%, 🟡 yellow)
   **BDD (Behavior-Driven Development)**: 85% (target: ≥80%, ✅ green)
   **TDD (Test-Driven Development)**: 80% (target: ≥80%, ✅ green)

   **Recommendation**: Increase DDD adherence by 5%
   ```

**Expected Outcome**: Process adherence metrics with actionable insights

---

### Signal 4: "Show me quality trends over time"

**Context**: Team wants to see if quality is improving

**Agent Response**:
1. Query historical metrics:
   ```python
   # Get metrics from last 30 days
   metrics_30d = calculator.get_metrics_for_period(days=30)

   # Calculate trend
   coverage_trend = [m.test_coverage for m in metrics_30d]
   defect_trend = [m.bugs_introduced for m in metrics_30d]
   ```

2. Generate trend report:
   ```markdown
   ## 30-Day Quality Trends

   **Test Coverage**:
   - Week 1: 88%
   - Week 2: 90%
   - Week 3: 92%
   - Week 4: 94%
   - **Trend**: ⬆️ +6% (improving)

   **Defect Rate**:
   - Week 1: 4 bugs
   - Week 2: 3 bugs
   - Week 3: 2 bugs
   - Week 4: 1 bug
   - **Trend**: ⬇️ -75% (improving)
   ```

3. Add recommendations:
   ```markdown
   ## Recommendations

   - ✅ Test coverage improving (+6% in 30 days)
   - ✅ Defect rate declining (-75% in 30 days)
   - 💡 Continue current practices
   - 💡 Consider raising coverage target to 95%
   ```

**Expected Outcome**: Trend analysis showing improvement

---

### Signal 5: "Generate release metrics"

**Context**: Preparing for release, need metrics for stakeholders

**Agent Response**:
1. Collect release metrics:
   ```python
   # From git history
   commits_count = 47
   features_added = 12
   bugs_fixed = 18
   test_coverage = 0.94
   defect_rate = 2  # Bugs found in QA
   cycle_time_days = 14
   ```

2. Generate release dashboard:
   ```markdown
   ## Release v1.5.0 Dashboard

   **Delivery**:
   - Commits: 47
   - Features: 12
   - Bugs Fixed: 18
   - Cycle Time: 14 days (target: <21, ✅ green)

   **Quality**:
   - Test Coverage: 94% (target: ≥90%, ✅ green)
   - Defect Rate: 2 (target: <3, ✅ green)
   - Documentation: Complete (✅ green)

   **Process**:
   - DDD Adherence: 80% (target: ≥80%, ✅ green)
   - TDD Adherence: 85% (target: ≥80%, ✅ green)
   - Code Review: 100% (✅ green)

   **Recommendation**: Release approved ✅
   ```

3. Save to project-docs/:
   ```bash
   echo "[dashboard]" > project-docs/releases/v1.5.0-dashboard.md
   ```

**Expected Outcome**: Comprehensive release metrics for stakeholders

---

## 5. How It Works

### Architecture Overview

Metrics Tracking uses **ClaudeROICalculator** and **markdown dashboards**:

```
Claude Sessions
       ↓
ClaudeMetric (dataclass)
       ↓
ClaudeROICalculator.add_metric()
       ↓
Metrics Storage (CSV, JSON, or A-MEM events)
       ↓
Report Generation (generate_report(), generate_executive_summary())
       ↓
Markdown Dashboards (sprint-dashboard.md, release-dashboard.md)
       ↓
Stakeholder Communication (evidence-based ROI)
```

---

### ClaudeMetric Schema

```python
@dataclass
class ClaudeMetric:
    session_id: str                      # Unique session identifier
    timestamp: datetime                  # When metric captured
    task_type: str                       # feature_implementation | bugfix | refactor
    lines_generated: int                 # Lines of code generated
    time_saved_minutes: int              # Time saved vs manual implementation
    iterations_required: int             # Number of iterations to complete (≥1)
    bugs_introduced: int                 # Bugs introduced in this session
    bugs_fixed: int                      # Bugs fixed in this session
    documentation_quality_score: float   # 0-10 scale
    test_coverage: float                 # 0-1 scale (0% - 100%)
    trace_id: str | None                 # CHORA_TRACE_ID from SAP-001 (optional)
    metadata: dict[str, Any]             # Additional context
```

---

### Metric Categories

**1. Quality Metrics**:
- **Defect Rate**: bugs_introduced / (bugs_introduced + bugs_fixed)
- **Test Coverage**: test_coverage (0-1)
- **Documentation Quality**: documentation_quality_score (0-10)
- **First-Pass Success Rate**: (metrics with iterations=1) / total_metrics

**2. Velocity Metrics**:
- **Time Saved**: sum(time_saved_minutes)
- **Lines Generated**: sum(lines_generated)
- **Acceleration Factor**: time_saved / session_duration
- **Sprint Velocity**: story_points_completed / sprint_duration

**3. Process Adherence Metrics**:
- **DDD Adherence**: (docs-before-code commits) / total_commits
- **BDD Adherence**: (behavior-specs commits) / total_commits
- **TDD Adherence**: (tests-before-code commits) / total_commits

**4. Adoption Metrics**:
- **Downloads**: package_downloads / month
- **Upgrade Rate**: users_on_latest / total_users
- **User Satisfaction**: avg(user_ratings)

---

### ROI Calculation

**Time & Cost Savings**:
```python
hours_saved = sum(time_saved_minutes) / 60
cost_savings = hours_saved * developer_hourly_rate
acceleration_factor = hours_saved / session_duration_hours
```

**Annualized Value**:
```python
# Assuming 260 working days/year
avg_time_saved_per_day = hours_saved / days_tracked
annualized_hours = avg_time_saved_per_day * 260
annualized_value = annualized_hours * developer_hourly_rate
```

**Example**:
- Developer rate: $100/hour
- Average time saved: 2 hours/day
- Annualized value: 2 × 260 × $100 = **$52,000/year**

---

### Dashboard Types

**Sprint Dashboard** (project-docs/sprints/):
- Velocity (story points completed)
- Defect rate (bugs introduced)
- Test coverage (average)
- Cycle time (average time to close task)

**Release Dashboard** (project-docs/releases/):
- Features delivered
- Bugs fixed
- Test coverage
- Defect rate
- Process adherence

**Process Trends** (project-docs/metrics/):
- 30-day trends (velocity, quality)
- 90-day trends (long-term improvement)
- Year-over-year comparison

---

## 6. Key Workflows

### Workflow 1: Track Claude Session and Calculate ROI

**Goal**: Capture metrics for single Claude session

**Steps**:

1. **Import ClaudeROICalculator**:
   ```python
   from claude_roi_calculator import ClaudeROICalculator, ClaudeMetric
   from datetime import datetime
   ```

2. **Initialize calculator with developer rate**:
   ```python
   # Use average developer rate ($50-150/hour)
   calculator = ClaudeROICalculator(developer_hourly_rate=100)
   ```

3. **Create metric for current session**:
   ```python
   metric = ClaudeMetric(
       session_id="session-001",
       timestamp=datetime.now(),
       task_type="feature_implementation",  # or: bugfix, refactor
       lines_generated=250,
       time_saved_minutes=120,  # Estimate: 2 hours saved
       iterations_required=2,   # First attempt + 1 revision
       bugs_introduced=0,
       bugs_fixed=3,
       documentation_quality_score=8.5,  # 0-10 scale
       test_coverage=0.92,               # 92%
       trace_id="mcp-taskmgr-2025-003",  # From SAP-001 (optional)
       metadata={
           "session_duration_minutes": 45,
           "context_tokens_used": 15000
       }
   )
   ```

4. **Add metric to calculator**:
   ```python
   calculator.add_metric(metric)
   ```

5. **Generate ROI report**:
   ```python
   report = calculator.generate_report()
   print(report)
   ```

   Output:
   ```
   === Claude ROI Report ===
   Sessions Tracked: 1
   Time Saved: 2.0 hours
   Cost Savings: $200.00
   Lines Generated: 250
   Iterations: 2 (first-pass success: 50%)
   Bugs Introduced: 0
   Bugs Fixed: 3
   Test Coverage: 92%
   Documentation Quality: 8.5/10
   ```

6. **Generate executive summary with annualized value**:
   ```python
   summary = calculator.generate_executive_summary()
   print(summary)
   ```

   Output:
   ```
   === Executive Summary ===
   Based on 1 session(s):
   - Average time saved: 2.0 hours/session
   - Annualized value (260 working days): $104,000/year
   - Quality metrics: 92% coverage, 8.5/10 docs
   - Recommendation: High ROI, continue using Claude
   ```

7. **Export metrics for further analysis**:
   ```python
   calculator.export_to_csv("metrics/claude-metrics.csv")
   calculator.export_to_json("metrics/claude-metrics.json")
   ```

**Expected Outcome**: ROI metrics for current session

**Time Estimate**: 5-10 minutes

---

### Workflow 2: Generate Sprint Dashboard

**Goal**: Create sprint metrics dashboard for retrospective

**Steps**:

1. **Collect sprint metrics**:
   ```python
   # Assuming integration with SAP-015 (beads)
   import subprocess
   import json

   # Get tasks closed this sprint
   result = subprocess.run(
       ["bd", "list", "--status", "closed", "--json"],
       capture_output=True,
       text=True
   )
   tasks = json.loads(result.stdout)

   # Calculate metrics
   story_points = sum(task.get("priority", 1) for task in tasks)
   bugs_introduced = sum(1 for task in tasks if "bug" in task.get("title", "").lower())
   avg_coverage = 0.94  # From test suite
   avg_cycle_time = 2.3  # days
   ```

2. **Create sprint dashboard markdown**:
   ```python
   sprint_date = "2025-11-05"
   dashboard = f"""
   # Sprint Dashboard - {sprint_date}

   ## Velocity
   - **Story Points Completed**: {story_points} (target: 40, {'✅ green' if story_points >= 40 else '🟡 yellow'})
   - **Tasks Completed**: {len(tasks)}

   ## Quality
   - **Defect Rate**: {bugs_introduced} bugs (target: <3, {'✅ green' if bugs_introduced < 3 else '🔴 red'})
   - **Test Coverage**: {avg_coverage*100:.0f}% (target: ≥90%, {'✅ green' if avg_coverage >= 0.9 else '🟡 yellow'})

   ## Process
   - **Cycle Time**: {avg_cycle_time:.1f} days (target: <3, {'✅ green' if avg_cycle_time < 3 else '🟡 yellow'})
   - **DDD Adherence**: 80% (target: ≥80%, ✅ green)
   - **TDD Adherence**: 85% (target: ≥80%, ✅ green)

   ## Recommendations
   - {'✅ Sprint successful, all targets met' if story_points >= 40 and bugs_introduced < 3 and avg_coverage >= 0.9 else '💡 See areas for improvement above'}
   """
   ```

3. **Save dashboard to project-docs/**:
   ```python
   with open(f"project-docs/sprints/sprint-{sprint_date}-dashboard.md", "w") as f:
       f.write(dashboard)
   ```

4. **Commit dashboard**:
   ```bash
   git add project-docs/sprints/sprint-{sprint_date}-dashboard.md
   git commit -m "metrics: Add sprint dashboard for {sprint_date}"
   ```

**Expected Outcome**: Sprint dashboard for retrospective

**Time Estimate**: 10-15 minutes

---

### Workflow 3: Track Process Adherence (DDD/BDD/TDD)

**Goal**: Measure adherence to development processes

**Steps**:

1. **Analyze git history for DDD (docs-before-code)**:
   ```bash
   # Get commits with both docs/ and src/
   git log --oneline --name-only --since="30 days ago" > commits.txt

   # Count DDD commits (docs/ before src/ in same commit)
   grep -B 5 "^docs/" commits.txt | grep -A 5 "^src/" | wc -l
   ```

2. **Analyze for TDD (tests-before-code)**:
   ```bash
   # Count TDD commits (tests/ before src/ in same commit)
   grep -B 5 "^tests/" commits.txt | grep -A 5 "^src/" | wc -l
   ```

3. **Calculate adherence rates**:
   ```python
   total_commits = 100  # From git log
   ddd_commits = 75
   tdd_commits = 80
   bdd_commits = 85  # From behavior spec commits

   ddd_adherence = (ddd_commits / total_commits) * 100  # 75%
   tdd_adherence = (tdd_commits / total_commits) * 100  # 80%
   bdd_adherence = (bdd_commits / total_commits) * 100  # 85%
   ```

4. **Generate process adherence report**:
   ```markdown
   ## Process Adherence Report

   **DDD (Documentation-Driven Development)**:
   - Rate: 75% (target: ≥80%, 🟡 yellow)
   - Commits: 75/100
   - Recommendation: Increase by 5% (write docs before code)

   **TDD (Test-Driven Development)**:
   - Rate: 80% (target: ≥80%, ✅ green)
   - Commits: 80/100
   - Recommendation: Maintain current practices

   **BDD (Behavior-Driven Development)**:
   - Rate: 85% (target: ≥80%, ✅ green)
   - Commits: 85/100
   - Recommendation: Excellent adherence
   ```

5. **Save to project-docs/metrics/**:
   ```python
   with open("project-docs/metrics/process-adherence-2025-11-05.md", "w") as f:
       f.write(report)
   ```

**Expected Outcome**: Process adherence metrics with recommendations

**Time Estimate**: 15-20 minutes

---

### Workflow 4: Generate Release Dashboard

**Goal**: Create comprehensive release metrics for stakeholders

**Steps**:

1. **Collect release metrics from git**:
   ```bash
   # Get commits since last release
   git log v1.4.0..HEAD --oneline | wc -l  # commits_count

   # Get features (from commit messages with "feat:")
   git log v1.4.0..HEAD --oneline | grep "feat:" | wc -l  # features_added

   # Get bugfixes (from commit messages with "fix:")
   git log v1.4.0..HEAD --oneline | grep "fix:" | wc -l  # bugs_fixed
   ```

2. **Collect quality metrics**:
   ```python
   # From test suite
   test_coverage = 0.94

   # From QA testing
   defect_rate = 2  # Bugs found in QA

   # From git history
   cycle_time_days = 14  # Days from first commit to release
   ```

3. **Generate release dashboard**:
   ```markdown
   # Release v1.5.0 Dashboard

   ## Delivery Metrics
   - **Commits**: 47
   - **Features Added**: 12
   - **Bugs Fixed**: 18
   - **Cycle Time**: 14 days (target: <21, ✅ green)

   ## Quality Metrics
   - **Test Coverage**: 94% (target: ≥90%, ✅ green)
   - **Defect Rate**: 2 (target: <3, ✅ green)
   - **Documentation**: Complete (✅ green)

   ## Process Metrics
   - **DDD Adherence**: 80% (target: ≥80%, ✅ green)
   - **TDD Adherence**: 85% (target: ≥80%, ✅ green)
   - **Code Review**: 100% (✅ green)

   ## ROI
   - **Time Saved**: 52 hours (using Claude)
   - **Cost Savings**: $5,200 (at $100/hour)
   - **Quality Improvement**: +6% test coverage since v1.4.0

   ## Recommendation
   ✅ **Release Approved**
   - All quality gates passed
   - Process adherence on target
   - Significant ROI demonstrated
   ```

4. **Save to project-docs/releases/**:
   ```python
   with open("project-docs/releases/v1.5.0-dashboard.md", "w") as f:
       f.write(dashboard)
   ```

5. **Commit release dashboard**:
   ```bash
   git add project-docs/releases/v1.5.0-dashboard.md
   git commit -m "metrics: Add release dashboard for v1.5.0"
   ```

**Expected Outcome**: Comprehensive release metrics for stakeholders

**Time Estimate**: 20-30 minutes

---

### Workflow 5: Analyze Quality Trends Over Time

**Goal**: Identify if quality is improving or declining

**Steps**:

1. **Query historical metrics** (last 30 days):
   ```python
   # From ClaudeROICalculator
   metrics_30d = calculator.get_metrics_for_period(days=30)

   # Or from CSV export
   import pandas as pd
   df = pd.read_csv("metrics/claude-metrics.csv")
   df["timestamp"] = pd.to_datetime(df["timestamp"])
   metrics_30d = df[df["timestamp"] >= pd.Timestamp.now() - pd.Timedelta(days=30)]
   ```

2. **Calculate weekly trends**:
   ```python
   # Group by week
   df["week"] = df["timestamp"].dt.isocalendar().week

   # Calculate averages per week
   weekly_coverage = df.groupby("week")["test_coverage"].mean()
   weekly_defects = df.groupby("week")["bugs_introduced"].sum()
   weekly_quality = df.groupby("week")["documentation_quality_score"].mean()
   ```

3. **Generate trend report**:
   ```markdown
   ## 30-Day Quality Trends

   ### Test Coverage
   - Week 1: 88%
   - Week 2: 90%
   - Week 3: 92%
   - Week 4: 94%
   - **Trend**: ⬆️ +6% (improving)

   ### Defect Rate
   - Week 1: 4 bugs
   - Week 2: 3 bugs
   - Week 3: 2 bugs
   - Week 4: 1 bug
   - **Trend**: ⬇️ -75% (improving)

   ### Documentation Quality
   - Week 1: 7.5/10
   - Week 2: 8.0/10
   - Week 3: 8.5/10
   - Week 4: 9.0/10
   - **Trend**: ⬆️ +1.5 points (improving)

   ## Recommendations
   - ✅ All quality metrics improving
   - ✅ Test coverage on track to 95% by next month
   - ✅ Defect rate declining consistently
   - 💡 Continue current practices
   - 💡 Consider raising coverage target to 95%
   ```

4. **Save trend report**:
   ```python
   with open("project-docs/metrics/quality-trends-2025-11-05.md", "w") as f:
       f.write(report)
   ```

**Expected Outcome**: Trend analysis showing improvement or areas for focus

**Time Estimate**: 15-25 minutes

---

## 7. Integration with Other SAPs

### SAP-001 (inbox)

**Integration**: Track metrics per coordination request using CHORA_TRACE_ID

**Agent workflow**:
1. When processing coordination request, add trace_id to metrics:
   ```python
   metric = ClaudeMetric(
       session_id="session-001",
       trace_id="mcp-taskmgr-2025-003",  # From coordination request
       task_type="feature_implementation",
       time_saved_minutes=120
   )
   ```
2. Query metrics by trace_id to measure coordination effectiveness
3. Generate ROI report per coordination workflow

---

### SAP-010 (memory-system)

**Integration**: Store metrics as events in A-MEM

**Agent workflow**:
1. Log metrics as events:
   ```python
   # After calculating metrics
   log_event(
       event_type="claude_metric",
       data={
           "session_id": "session-001",
           "time_saved_minutes": 120,
           "cost_savings": 200.0,
           "test_coverage": 0.92
       },
       trace_id="mcp-taskmgr-2025-003"
   )
   ```
2. Query historical metrics via event logs
3. Correlate metrics with development events

---

### SAP-015 (task-tracking)

**Integration**: Metrics per task (time saved, iterations)

**Agent workflow**:
1. When closing task, capture metrics:
   ```bash
   bd close {id} --metadata '{"time_saved_minutes": 120, "iterations": 2}'
   ```
2. Calculate sprint velocity from task completion rates
3. Track quality metrics from task outcomes (bugs introduced/fixed)

---

### SAP-005 (ci-cd-workflows)

**Integration**: CI collects metrics automatically

**Agent workflow**:
1. Add metrics collection to GitHub Actions:
   ```yaml
   - name: Collect Metrics
     run: |
       python scripts/collect_metrics.py
       python scripts/generate_dashboard.py
   ```
2. Automated sprint/release reports
3. Quality gate validation using metrics

---

## 8. Best Practices

### Best Practice 1: Track Every Claude Session

**Why**: Comprehensive data enables accurate ROI calculation

**How**:
```python
# At end of each session
metric = ClaudeMetric(
    session_id=generate_session_id(),
    task_type="feature_implementation",
    time_saved_minutes=estimate_time_saved(),
    # ... other fields
)
calculator.add_metric(metric)
```

**Benefit**: Accurate annualized value, trend analysis

---

### Best Practice 2: Use Realistic Developer Rates

**Why**: Inflated rates overestimate ROI, deflated rates underestimate

**How**:
- Use average market rate for your role ($50-150/hour)
- Consider total compensation (salary + benefits)
- Be consistent across sessions

**Benefit**: Credible ROI estimates for stakeholders

---

### Best Practice 3: Generate Dashboards Regularly

**Why**: Regular visibility drives process improvement

**How**:
- Sprint dashboard after each sprint
- Release dashboard before each release
- Trend reports monthly

**Benefit**: Data-driven retrospectives and planning

---

### Best Practice 4: Integrate with CI/CD

**Why**: Automated collection reduces manual effort

**How**:
- Add metrics collection to GitHub Actions
- Generate dashboards automatically
- Store metrics in git (version controlled)

**Benefit**: No manual tracking overhead

---

### Best Practice 5: Share Metrics with Stakeholders

**Why**: Demonstrates value, justifies continued investment

**How**:
- Include metrics in sprint reviews
- Share ROI reports with management
- Use dashboards in retrospectives

**Benefit**: Evidence-based communication, stakeholder buy-in

---

## 9. Common Pitfalls

### Pitfall 1: Overestimating Time Saved

**Problem**: Inflating time_saved_minutes to show higher ROI

**Symptom**:
- ROI seems too good to be true ($200k+/year)
- Stakeholders skeptical of metrics
- Metrics not credible

**Fix**:
- Use conservative estimates (underestimate if unsure)
- Compare to manual implementation time
- Be honest about iterations required

**Prevention**: Track actual time for manual tasks as baseline

---

### Pitfall 2: Not Tracking Iterations

**Problem**: Only tracking successful sessions (survivorship bias)

**Symptom**:
- First-pass success rate = 100% (unrealistic)
- Metrics don't reflect reality
- No insight into areas for improvement

**Fix**:
- Track all sessions, including failed attempts
- Increment iterations_required for each revision
- Calculate realistic first-pass success rate

**Prevention**: Track every attempt, not just successes

---

### Pitfall 3: Ignoring Quality Metrics

**Problem**: Only tracking time saved, not quality

**Symptom**:
- High ROI but low quality code
- Technical debt accumulates
- Stakeholders question value

**Fix**:
- Track test_coverage, bugs_introduced, documentation_quality
- Balance speed with quality
- Set quality targets (≥90% coverage)

**Prevention**: Quality metrics as important as time metrics

---

### Pitfall 4: Not Generating Regular Dashboards

**Problem**: Metrics collected but never analyzed

**Symptom**:
- CSV files accumulate, no insights
- No process improvement
- Stakeholders unaware of value

**Fix**:
- Generate sprint dashboard after each sprint
- Create release dashboard before release
- Share dashboards in retrospectives

**Prevention**: Make dashboard generation part of sprint cadence

---

### Pitfall 5: Using Unrealistic Developer Rates

**Problem**: Using inflated hourly rate ($300/hour) to show high ROI

**Symptom**:
- ROI seems exaggerated ($500k+/year)
- Stakeholders dismiss metrics as unrealistic
- Credibility lost

**Fix**:
- Use market-rate for your role ($50-150/hour)
- Be transparent about rate used
- Provide range (low/mid/high estimates)

**Prevention**: Conservative, defensible developer rates

---

## 10. Self-Evaluation

### Workflow Coverage Analysis

**Protocol Spec Workflows**: 5 (specified in protocol-spec.md)
1. Track Claude session (ClaudeMetric, add_metric)
2. Calculate ROI (generate_report, generate_executive_summary)
3. Generate dashboards (sprint, release, trends)
4. Track process adherence (DDD/BDD/TDD rates)
5. Export metrics (CSV, JSON)

**AGENTS.md Workflows**: 5 (implemented above)
1. Track Claude Session and Calculate ROI
2. Generate Sprint Dashboard
3. Track Process Adherence (DDD/BDD/TDD)
4. Generate Release Dashboard
5. Analyze Quality Trends Over Time

**CLAUDE.md Workflows**: 3 (to be implemented in CLAUDE.md)
1. Set Up Metrics Tracking (Bash + Write tools)
2. Generate ROI Report (Bash + Read tools)
3. Create Sprint Dashboard (Bash + Write tools)

**Coverage**: 5/5 = 100% (all protocol-spec workflows covered)

**Variance**: 40% (5 generic workflows vs 3 Claude-specific workflows)

**Rationale**: CLAUDE.md focuses on tool-specific patterns (Bash/Read/Write), while AGENTS.md provides comprehensive guidance applicable to all agents. Both provide equivalent support for SAP-013 adoption.

**Conclusion**: ✅ Equivalent support across agent types

---

## 11. Version History

**1.0.0** (2025-11-05):
- Initial AGENTS.md for SAP-013 (metrics-tracking)
- 5 workflows: session tracking, sprint dashboard, process adherence, release dashboard, trend analysis
- Integration with SAP-001, SAP-010, SAP-015, SAP-005
- 5 best practices, 5 common pitfalls
- Progressive context loading frontmatter

---

## Quick Links

- **Protocol Spec**: [protocol-spec.md](protocol-spec.md) - Complete metrics specification
- **Capability Charter**: [capability-charter.md](capability-charter.md) - ROI rationale
- **Adoption Blueprint**: [adoption-blueprint.md](adoption-blueprint.md) - Installation guide
- **PROCESS_METRICS.md**: [PROCESS_METRICS.md](PROCESS_METRICS.md) - Complete metrics guide
- **Source Code**: [src/claude_roi_calculator.py](src/claude_roi_calculator.py) - Implementation

---

**Next Steps**:
1. Read [CLAUDE.md](CLAUDE.md) for Claude Code tool patterns
2. Read [protocol-spec.md](protocol-spec.md) for complete metrics specification
3. Read [PROCESS_METRICS.md](PROCESS_METRICS.md) for comprehensive metrics guide
4. See [../AGENTS.md](../AGENTS.md) for SAP catalog navigation
