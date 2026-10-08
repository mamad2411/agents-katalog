# AeneasSoft Observability Skill for OpenClaw

## Description
Instruments your OpenClaw agent with AeneasSoft observability.
Every LLM call is automatically traced, costs are calculated, and
causal graphs are generated. EU AI Act compliance reports on demand.

## Setup
Add to your OpenClaw config:
```
OPENAI_BASE_URL=http://localhost:8080/openai
ANTHROPIC_BASE_URL=http://localhost:8080/anthropic
PRODUCTNAME_API_KEY=your-key
PRODUCTNAME_URL=http://localhost:8080
```

## Tools

### start_trace
Starts a named trace session. Returns a trace_id that groups all
subsequent LLM calls into one observable workflow.
- name (string): Human-readable name for this agent run
- agent_id (string, optional): Identifier for this agent instance

### end_trace
Ends the current trace and returns the dashboard URL.
- trace_id (string): The trace_id from start_trace

### get_trace_cost
Returns the total cost in USD for a completed trace.
- trace_id (string): The trace to query

### compliance_report
Downloads the EU AI Act compliance PDF for a trace.
- trace_id (string): The trace to generate a report for

## Notes
- All LLM calls are traced automatically via proxy — no code changes needed
- Zero Data Retention mode: set ZERO_DATA_RETENTION=true to disable input/output logging
- Dashboard: http://localhost:3000
