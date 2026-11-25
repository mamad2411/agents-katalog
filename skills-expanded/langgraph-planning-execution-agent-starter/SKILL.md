# LangGraph Planning Execution Agent Starter

Use this skill to decompose a scientific task into deterministic step queries, route each step to candidate local skills, and return an execution-ready plan.

## What it does

- Uses a small LangGraph `StateGraph` to plan, route, and summarize.
- Converts a free-text goal into step queries such as literature search, marker ranking, or interactive reporting.
- Routes each step through the local skill registry.
- Returns compact JSON with recommended skills and preview commands.

## When to use it

- You need a local starter for planning-and-execution agents without external LM credentials.
- You want a deterministic bridge between the taxonomy, the skill registry, and execution previews.

## Example

```bash
slurm/envs/agents/bin/python skills/scientific-agents-and-automation/langgraph-planning-execution-agent-starter/scripts/run_langgraph_planning_agent.py \
  --goal "single-cell marker ranking with an interactive report" \
  --out scratch/agents/planning_agent_summary.json
```

## Verification

- Skill-local tests: `python3 -m unittest discover -s skills/scientific-agents-and-automation/langgraph-planning-execution-agent-starter/tests -p 'test_*.py'`
- Repository smoke: `python3 -m unittest tests.smoke.test_phase25_agent_and_clinical_skills -v`
