---
name: deep-analysis
version: 1.0.0
description: Break down complex problems through structured analytical frameworks
uses:
  - analysis/research
requires:
  tools: []
  env: []
security:
  risk_level: read
  capabilities:
    - analysis:execute
  requires_approval: false
---

# Deep Analysis

Break down complex problems through structured analytical frameworks — root cause analysis, comparative evaluation, pattern recognition, and risk assessment.

## Execution Model

This is an **agent-handled skill** (`handler: type: agent`). When `analyze` is invoked, you (the agent) apply the selected analytical framework using your reasoning capabilities. There is no backing code — you follow these instructions directly. The tool schema in tool.yaml defines the external contract; this document guides how you fulfill it. An orchestrator may route this skill to any agent that has `analysis/deep-analysis` in its skill list.

## When to Use

- A problem's cause is unclear and needs systematic investigation
- Multiple options need structured comparison and evaluation
- Patterns or trends need to be identified across data
- Risks need to be assessed before a decision or action
- A situation is too complex to reason about without a framework
- Stakeholders need a defensible, structured rationale

## Methodology

### 1. Frame the Problem

Before selecting a framework, clearly define:
- **Subject**: What exactly are you analyzing?
- **Objective**: What decision or understanding should this analysis enable?
- **Constraints**: What boundaries, assumptions, or limitations apply?
- **Stakeholders**: Who will use this analysis and what do they need?

### 2. Select a Framework

Choose the framework that best fits the problem type:

| Problem Type | Framework | Best For |
|-------------|-----------|----------|
| Unknown cause | **5 Whys** | Finding root cause of failures or issues |
| Unknown cause (complex) | **Fishbone (Ishikawa)** | Multi-factor root cause with categories |
| Choose between options | **Decision Matrix** | Weighted comparison of alternatives |
| Strategic assessment | **SWOT** | Understanding position and opportunities |
| Risk evaluation | **Risk Matrix** | Prioritizing risks by likelihood × impact |
| Process improvement | **Gap Analysis** | Current state vs. desired state |

If unsure, start with **5 Whys** for causal problems or **Decision Matrix** for choices.

### 3. Apply the Framework

#### 5 Whys (Root Cause Analysis)

1. State the problem clearly
2. Ask "Why?" and answer with evidence
3. For each answer, ask "Why?" again
4. Continue until you reach a root cause (typically 3-7 levels)
5. Verify: does addressing the root cause prevent the original problem?

**Caution**: Avoid stopping at surface symptoms. If the answer feels like a symptom rather than a cause, keep asking.

#### Fishbone / Ishikawa (Complex Root Cause)

1. Place the problem at the "head"
2. Define category "bones" (common: People, Process, Technology, Environment, Materials, Measurement)
3. For each category, brainstorm contributing factors
4. For significant factors, drill deeper (sub-bones)
5. Identify the 2-3 most impactful root causes across categories

#### Decision Matrix (Comparing Options)

1. List all viable options as columns
2. Define evaluation criteria as rows
3. Assign weights to criteria (must total 100% or use 1-10 scale)
4. Score each option against each criterion (1-5 scale)
5. Calculate weighted scores
6. Check: does the winner pass the "gut check"? If not, examine your criteria.

#### SWOT (Strategic Assessment)

1. **Strengths**: Internal advantages — what works well?
2. **Weaknesses**: Internal disadvantages — what needs improvement?
3. **Opportunities**: External factors you could leverage
4. **Threats**: External factors that could cause harm
5. Cross-reference: How can strengths address threats? How can opportunities offset weaknesses?

#### Risk Matrix

1. List all identified risks
2. Rate each risk's **likelihood** (1-5: rare to almost certain)
3. Rate each risk's **impact** (1-5: negligible to catastrophic)
4. Calculate risk score = likelihood × impact
5. Prioritize: Critical (20-25), High (12-19), Medium (6-11), Low (1-5)
6. For Critical and High risks, define mitigation strategies

#### Gap Analysis

1. Define **current state** with evidence
2. Define **desired state** with measurable criteria
3. Identify specific gaps between current and desired
4. For each gap, determine root cause and effort to close
5. Prioritize gaps by impact and feasibility

### 4. Identify Assumptions

Every analysis rests on assumptions. Make them explicit:
- What did you assume to be true without verification?
- What would change if those assumptions were wrong?
- Which assumptions carry the most risk?

### 5. Draw Conclusions

Synthesize the framework output into actionable conclusions:
- **Primary finding**: The single most important insight
- **Supporting evidence**: Key data points from the analysis
- **Recommendations**: What should be done based on the findings
- **Confidence level**: How certain are the conclusions (high / medium / low)

### 6. Publish Findings (MANDATORY)

Every completed analysis MUST be saved as an artifact so other agents and humans can discover and use the results.

**Step 1**: Use the `core/publish-artifact` skill to write findings.

The artifact should be written to the shared memory location so other agents
can discover it. Use artifact type `analysis`:

```bash
# Write to the shared analysis artifact location
cat > .os/memory/analysis/{investigation-id}.md << 'EOF'
{your formatted findings from step 5}
EOF
```

The investigation ID should be descriptive, e.g.:
- `investigation-697-artifact-publishing` (issue number + short description)
- `analysis-2026-03-22-performance-regression` (date + topic)

**Step 2**: Publish a bus notification so other agents know findings are available:

```json
{
  "channel": "work",
  "type": "investigation_complete",
  "message": {
    "agent": "{your-agent-name}",
    "investigation_id": "{investigation-id}",
    "artifact_path": ".os/memory/analysis/{investigation-id}.md",
    "subject": "{what was analyzed}",
    "primary_finding": "{one-sentence summary of the key finding}"
  }
}
```

**Why this is mandatory**: An analysis that only exists in the agent's context window is lost when the session ends. Other agents (developers, reviewers) cannot act on findings they cannot read. The artifact is the durable record of the work.

## Output Format

```
## Analysis: [Subject]

### Problem Statement
[Clear description of what's being analyzed and why]

### Framework: [Name]
[Framework-specific output — see templates above]

### Assumptions
- [Assumption 1]: Impact if wrong: [description]
- [Assumption 2]: Impact if wrong: [description]

### Conclusions
- **Primary finding**: [Most important insight]
- **Confidence**: [High / Medium / Low]

### Recommendations
1. [Action] — Priority: [Critical / High / Medium / Low]
2. [Action] — Priority: [Critical / High / Medium / Low]

### Limitations
- [What this analysis does not cover]
- [Where additional data would improve conclusions]
```

## Quality Criteria

- Framework selection is justified and appropriate for the problem
- All steps of the chosen framework are completed
- Assumptions are explicitly stated
- Evidence supports each conclusion
- Confidence levels are honest
- Recommendations are specific and actionable
- Limitations are acknowledged
- **Findings are written to `.os/agents/{agent-name}/artifacts/` and bus notification sent**

## Common Mistakes

- **Choosing the wrong framework**: Use the problem type table to match correctly
- **Skipping "frame the problem"**: Jumping to a framework before clearly defining the question
- **Confirmation bias**: Forcing evidence to fit a predetermined conclusion
- **Stopping at symptoms**: In root cause analysis, ask "why?" until you reach something actionable
- **Ignoring outliers**: The exception often reveals the most about the system
- **Missing assumptions**: If you think you have no assumptions, you haven't looked hard enough
- **Analysis paralysis**: Choose a depth proportional to the decision's impact — not every problem needs a full SWOT
- **Not publishing**: Completing analysis but not writing the artifact file. The findings exist only in context and are lost when the session ends.

## Completion

Analysis is complete when:
- The problem is clearly framed with defined objectives
- An appropriate framework has been applied completely
- All assumptions are identified and stated
- Conclusions are supported by evidence from the analysis
- Recommendations are specific, actionable, and prioritized
- Limitations and confidence levels are honestly assessed
- **Artifact written to `.os/agents/{agent-name}/artifacts/{investigation-id}.md`**
- **Bus notification published with `investigation_complete` type**
