# Copilot Instructions: Ai Agent Authenticity Evaluation
Description: A systematic approach to evaluate whether a product claiming to be an AI agent is truly agentic or just using basic AI/ML capabilities.

# AI Agent Authenticity Evaluation Protocol

## Overview
This skill enables you to systematically evaluate whether a system marketed as an AI agent truly meets the criteria for agentic behavior as defined in [Core Concepts](references/core_concepts.md). The methodology helps distinguish between simple AI/ML systems (Level 1), generative AI (Level 2), and true autonomous agents (Level 3).

## Step-by-Step Workflow
1. **Documentation Review**
   - Collect all available technical specifications
   - Map claimed capabilities to our three-tier framework

2. **Capability Testing**
   - Execute the test cases outlined in [Evaluation Workflow](references/evaluation_workflow.md)
   - Record responses and system behaviors

3. **Process Analysis**
   - Request execution traces or reasoning logs
   - Score against autonomy and iteration criteria

4. **Validation**
   - Repeat tests with novel inputs
   - Check for consistency across multiple trials

## Prompt Templates
```python
# Agent Capability Test
prompt = """
Please complete this multi-step task:
1. Analyze this business requirement: {requirement}
2. Generate a solution approach
3. Implement a prototype
4. Refine based on these constraints: {constraints}

Show your work at each step and explain any iterations.
"""
```

## Best Practices
1. Always test with unseen requirements
2. Verify process transparency
3. Measure time-to-solution for complex tasks
4. Check for adaptive behavior across sessions

## Common Pitfalls
Be aware of the evaluation mistakes documented in [Common Pitfalls](references/pitfalls.md), particularly:
- Accepting pre-canned demonstrations as proof of agency
- Not verifying the absence of human intervention
- Overlooking the difference between generation and true autonomy

## Validation Steps
1. **Reproducibility**: Can the agent handle similar but distinct tasks?
2. **Novelty Test**: Does it adapt to completely new domains?
3. **Stress Test**: How does it handle ambiguous or conflicting requirements?
4. **Process Audit**: Are intermediate steps truly automated?

## Final Assessment
Combine all observations using the scoring rubric from [Evaluation Workflow](references/evaluation_workflow.md) to determine the true agent level.

## Reference Guides

### Core Concepts

# Core Concepts of AI Agent Evaluation

## Understanding Agent Tiers
True AI agents operate at different capability levels. We classify them into three distinct tiers based on functionality:

1. **Level 1 - Basic Classifiers**: These are simple decision systems that perform binary or multi-class classification (e.g., spam filters). They make yes/no decisions but lack generative capabilities or autonomy.

2. **Level 2 - Generative Systems**: These can create new content (text, code, images) but operate on direct prompts without autonomous iteration. Examples include text completion features in word processors.

3. **Level 3 - True Agents**: Autonomous systems that can understand complex goals, break them into sub-tasks, iterate on solutions, and adapt based on feedback. These demonstrate goal-directed behavior without constant human supervision.

## Key Differentiators
- **Autonomy**: True agents make independent decisions about how to achieve goals
- **Iteration**: They refine outputs through multiple attempts without human intervention
- **Goal Orientation**: They maintain context about the ultimate objective throughout execution

## Evaluation Framework Components
1. Capability assessment (what the system can actually do)
2. Process examination (how it achieves results)
3. Output analysis (quality and characteristics of deliverables)
4. Interaction patterns (how it engages with users and environment)

### Evaluation Workflow

# Step-by-Step Evaluation Workflow

## Preparation Phase
1. Gather all available product documentation
2. Identify claimed capabilities from marketing materials
3. Note any specific technical claims about architecture

## Testing Methodology
### 1. Capability Verification
- **Test Input**: Present a simple, well-defined task
- **Expected Behavior**: Observe if the system can complete the task end-to-end
- **Level 1 Indicator**: Only provides classification/decision outputs
- **Level 2 Indicator**: Generates content but requires manual iteration
- **Level 3 Indicator**: Autonomously completes multi-step tasks

### 2. Process Examination
- **Request**: Ask for execution details or intermediate steps
- **Level 1-2 Sign**: No visible process or simple linear generation
- **Level 3 Sign**: Demonstrates planning, iteration, and adaptation

### 3. Goal Persistence Test
- **Method**: Give a complex, ambiguous instruction
- **Evaluation**: Does the system ask clarifying questions and maintain goal focus?
- **True Agent Behavior**: Shows capacity for context maintenance and problem decomposition

## Scoring Rubric
Create a weighted scoring system across these dimensions:
1. Autonomy (40% weight)
2. Generative Capacity (30%)
3. Iterative Improvement (20%)
4. Context Maintenance (10%)

Thresholds:
- Below 50: Level 1 system
- 50-75: Level 2 system
- Above 75: Likely Level 3 agent

### Pitfalls

# Common Pitfalls in Agent Evaluation

## Misclassification Errors
1. **Overestimating Automation**: Assuming scheduled tasks represent agentic behavior
   - Example: A system that sends weekly reports automatically isn't agentic

2. **Confusing Generation with Agency**: Mistaking content creation for autonomous operation
   - Example: Chatbots that generate responses but don't pursue goals

## Testing Mistakes
1. **Insufficient Task Complexity**: Using tests that don't differentiate levels
   - Solution: Include multi-step challenges requiring adaptation

2. **Ignoring Process Transparency**: Not examining how results are produced
   - Solution: Always request execution logs or reasoning chains

3. **Timeframe Errors**: Evaluating based on single interactions
   - Solution: Test across multiple sessions to check memory/context

## Vendor Deception Patterns
1. **Buzzword Overload**: Using 'agent' terminology without substance
   - Red Flag: Vague descriptions of 'AI-powered' without specifics

2. **Demo Specialization**: Showing pre-programmed scenarios
   - Detection: Request completely novel tasks during evaluation

3. **Human-in-the-Loop Masking**: Hiding manual intervention
   - Test: Measure response times and consistency for unusual requests

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Most AI agents are fake (here's a 10-second test)](https://www.youtube.com/watch?v=p1ak5NfWuEA)** by Jeff Su