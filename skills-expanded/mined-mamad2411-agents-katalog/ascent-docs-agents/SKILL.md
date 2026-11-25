# Agents

Six specialised agents, each a Microsoft Agent Framework `ChatAgent` backed by a Foundry
model. Grounding is injected by the orchestrator from the IQ adapters, and every output is
validated by the Critic before it is shown or acted on.

| Agent | Model | Grounding | Input → Output |
| --- | --- | --- | --- |
| **Learning Path Curator** | gpt-4o | Fabric IQ (skills) + Foundry IQ (cited content) | role + target cert → grounded path items, each citing a `source_id` |
| **Study Plan Generator** | gpt-4o | Fabric IQ (hours/prereqs) + Work IQ (capacity/windows) | path → weekly schedule, milestones, blocks placed in focus windows |
| **Engagement** | gpt-4o-mini | Work IQ (rhythm) | plan + work signals → adaptive, privacy-conscious reminder cadence |
| **Assessment** | gpt-4o | Foundry IQ (cited questions) + Fabric IQ (threshold) | cert + weak skills → cited MCQs, score, pass/fail, weak-skill feedback |
| **Manager Insights** | gpt-4o | Fabric IQ (aggregate rollup) + Work IQ (capacity) | team id → aggregate readiness briefing, risks, recommendations (no PII) |
| **Critic / Verifier** | deterministic | knowledge base + ontology | any output → approve / revise-with-reasons |

## Responsibilities and guarantees

### Learning Path Curator — `agents/curator.py`
- One item per skill area; **every item must cite a known `source_id`** — items citing
  unknown sources are dropped at the data boundary.
- External tool: the **Microsoft Learn MCP server** (`microsoft_docs_search` et al.) —
  each path item also carries a real `learn.microsoft.com` URL found via MCP. The
  Critic treats these as a distinct citation class (must be a genuine MS Learn URL;
  Microsoft's own content is not re-validated). MCP outage degrades gracefully —
  citations are the contract, links are the enrichment.
- No unsupported free-text recommendations.

### Study Plan Generator — `agents/planner.py`
- Respects the Work IQ weekly capacity and the Fabric IQ daily study cap (2h).
- Extends the timeline when recommended hours exceed capacity (never overloads a week).
- On a re-prepare loop, front-loads the learner's weak skills.

### Engagement — `agents/engagement.py`
- Times reminders to the learner's preferred slot and focus windows.
- Reduces frequency and pressure for capacity-constrained learners (>20 meeting h/wk).
- Never one-size-fits-all.

### Assessment — `agents/assessment.py`
- Generates 4-option MCQs grounded only in retrieved sources, each citing its `source_id`.
- Two grading modes: **interactive** (grade real answers) and **simulated** (derive a score
  from the synthetic profile, improving each loop — for autonomous demo/eval).
- Readiness decided by the orchestrator against the Fabric IQ 75% threshold.

### Manager Insights — `agents/manager_insights.py`
- Reasons only over **aggregate** rollups; raw learner ids are stripped before the model
  sees them — privacy by construction.

### Critic / Verifier — `agents/critic.py`
- Checks: citations present & valid, plan within capacity and daily cap, questions grounded
  with in-range answers, no PII. A failed verdict drives **one self-reflection retry** with
  the findings fed back into the agent prompt.

## Orchestration

`orchestration/workflow.py` exposes:
- `run_learner_flow(...)` — autonomous end-to-end (simulated scoring) for CLI / eval / demo.
- `step_curate / step_plan / step_engage / step_assess` — granular steps the Streamlit UI
  drives interactively.
- `run_manager_flow(team_id)` — the manager briefing.
