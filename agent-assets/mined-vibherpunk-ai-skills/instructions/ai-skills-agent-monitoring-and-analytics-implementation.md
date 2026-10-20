# Copilot Instructions: Agent Monitoring And Analytics Implementation
Description: Implement comprehensive monitoring and analytics for AI agents to track runs, detect failures, and improve trust through actionable insights.

# Agent Monitoring and Analytics Skill

## Overview
Effective agent monitoring requires shifting from traditional session-based analytics to **run-level telemetry** that captures workflow success, user trust signals, and permission boundaries. Learn more in [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow
1. **Instrument Agent Runs**
   - Generate unique run IDs at task initiation
   - Tag all subsequent events (tool calls, approvals) with this ID
   - Implement the [tracking decorator pattern](references/code_examples.md) for critical operations

2. **Capture Three Key Events**
   - **Run Start**: User intent and workflow classification
   - **Mid-Run Corrections**: User edits/denials (tag with [schema](references/practical_guide.md))
   - **Completion**: Final state and user acceptance

3. **Build Analytical Views**
   - Completion vs acceptance rate divergence
   - Correction heatmaps by workflow step
   - Permission failure clusters

4. **Implement Guardrails**
   - Auto-throttle workflows with >20% correction rates
   - Require manual approval for actions with frequent permission errors

## Best Practices
- **Correlation**: Pipe engineering traces (API errors) into the same run context as product events
- **Thresholds**: Investigate workflows where correction rates exceed 15%
- **Anomaly Detection**: Flag runs with:
  - Multiple permission boundary violations
  - Excessive retries on destructive operations

## Common Pitfalls
- **Vanity Metrics**: Monitoring chat volume instead of work completion (as in the database deletion incident)
- **Over-Reliance on Traces**: Engineering data alone won't reveal if failures impacted user trust
- **Late Detection**: Missing correction patterns that predict major failures

## Validation Steps
1. **Test Instrumentation**
   - Verify run IDs persist across all events in a workflow
   - Confirm destructive operations emit criticality flags

2. **Benchmark Metrics**
   - Establish baseline completion/acceptance rates by workflow
   - Set SLOs for maximum correction rates

3. **Simulate Failures**
   - Trigger permission errors in test runs
   - Verify correction events appear in analytics

For implementation templates, see [Code Examples](references/code_examples.md) and [Practical Guide](references/practical_guide.md).

## Reference Guides

### Code Examples

# Code Examples for Agent Telemetry

## Python Instrumentation
```python
# Decorator for tool call tracking
def track_tool_call(tool_name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            run_id = get_current_run_id()  # From thread-local/context
            emit_event(run_id, {
                'eventType': 'tool_call',
                'tool': tool_name,
                'timestamp': datetime.utcnow().isoformat()
            })
            try:
                result = func(*args, **kwargs)
                emit_event(run_id, {'status': 'success'})  # Success follow-up
                return result
            except PermissionError as e:
                emit_event(run_id, {
                    'status': 'permission_denied',
                    'error': str(e)
                })
                raise
        return wrapper
    return decorator

# Usage example
@track_tool_call('database.execute')
def execute_sql(query):
    # ... actual DB logic
```

## Critical Prompts
**Agent Self-Reporting Template**:
```
You are assisting with {workflow_type}. Before taking any action, you MUST:

1. Confirm the current run ID is {run_id}
2. Classify this step as one of:
   - [INFO_LOOKUP] Gathering data
   - [ACTION] Attempting change
   - [REVIEW] Seeking approval
3. If hitting a permission boundary, report:
   "PERMISSION_CHECK_FAILED: {reason}"

After completion, summarize:
"RUN_STEP_COMPLETE: {outcome} with {retries} retries"
```

**Correction Analysis Query** (SQL):
```sql
SELECT 
  workflow_type,
  COUNT(CASE WHEN eventType = 'correction' THEN 1 END) * 100.0 / COUNT(*) as correction_rate,
  AVG(CASE WHEN completionState = 'success' THEN 1 ELSE 0 END) as completion_rate
FROM agent_events
GROUP BY workflow_type
HAVING correction_rate > 15  # Threshold for investigation
```

### Core Concepts

# Core Concepts of Agent Analytics

Agent analytics fundamentally shifts from traditional product metrics (clicks, sessions) to tracking **delegated work units**. Key concepts:

1. **Agent Run**: The complete lifecycle of an agent attempting a task, from instruction to completion. Unlike sessions, runs track workflow success/failure states.

2. **Correction Signals**: User interventions (edits, denials, interruptions) that reveal agent misunderstandings. These are the 'new clicks' for agent products.

3. **Completion vs Acceptance**: 
   - Completion: Task reached an end state
   - Acceptance: User trusted the output
   Gap between these indicates trust issues.

4. **Work Unit Telemetry**: Must capture:
   - Initial instruction context
   - Tool calls attempted/succeeded
   - Permission boundary hits
   - Retry patterns
   - User corrections

Example: A database deletion incident could be predicted by analyzing patterns of excessive retries on destructive operations or frequent permission boundary violations in similar workflows.

5. **Three Critical Events**:
   - Run start (intent capture)
   - Task completion (workflow state)
   - Mid-run corrections (real-time feedback)

Without this granular view, teams risk monitoring 'activity' (e.g., chat volume) while missing actual workflow failures.

### Practical Guide

# Practical Implementation Guide

## Instrumentation Layers
1. **Engineer Observability**:
   - Model call tracing
   - Tool execution logs
   - Error rate monitoring
   - Latency/cost metrics

2. **Product Analytics**:
   - Workflow completion rates
   - User acceptance metrics
   - Correction frequency by task type
   - Permission boundary hits

## Implementation Steps
1. **Tagging Strategy**:
   - Unique run IDs persisting across all events
   - Workflow type classification (e.g., 'db_operation', 'report_generation')
   - Criticality flags for destructive actions

2. **Event Schema**:
```typescript
interface AgentRunEvent {
  runId: string;
  workflowType: string;
  timestamp: ISO8601;
  eventType: 'start' | 'tool_call' | 'permission_check' | 'correction' | 'completion';
  payload: {
    // Contextual data specific to event type
    toolsAttempted?: string[];
    userCorrection?: 'edit' | 'denial' | 'interruption';
    completionState?: 'success' | 'partial' | 'failed';
  };
}
```

3. **Dashboard Essentials**:
   - Completion/acceptance rate divergence
   - Correction heatmaps by workflow step
   - Permission failure clusters
   - Tool call success rate trends

**Critical Integration**: Pipe engineering traces (e.g., OpenAI API errors) into the same run context as product events to correlate technical failures with user impact.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[A Cursor Agent Wiped a Database in 9 Seconds. Agent Analytics Would Have Seen It Coming.](https://www.youtube.com/watch?v=n0nC1kmztSk)** by AI News & Strategy Daily | Nate B Jones