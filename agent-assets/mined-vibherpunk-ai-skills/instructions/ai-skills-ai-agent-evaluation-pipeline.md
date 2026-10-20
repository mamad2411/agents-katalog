# Copilot Instructions: Ai Agent Evaluation Pipeline
Description: A comprehensive skill for building and running evaluation pipelines for AI agents, focusing on offline and online evaluations, LM judges, and continuous improvement.

## Overview

Building a robust evaluation pipeline for AI agents is critical to ensure they perform well in production. This skill covers the end-to-end process, from offline evaluations using simulated conversations to online evaluations with real user interactions. Key components include creating synthetic datasets, defining evaluation criteria, using LM judges, and continuous learning.

### Core Concepts

- **Offline Evaluation**: Simulate multi-turn conversations using synthetic datasets to test agent performance before deployment.
- **Online Evaluation**: Monitor and grade agent performance in production using tracing tools and human-in-the-loop feedback.
- **LM Judge**: Use language models to evaluate agent interactions, ensuring scores are actionable and tied to business outcomes.
- **Continuous Learning**: Feed evaluation insights back into the agent to improve model weights, context, and harness.

For a deeper dive into these concepts, see [Core Concepts](references/core_concepts.md).

## Step-by-Step Workflow

1. **Develop Synthetic Dataset**: Create a dataset representative of production traffic. Use real production data and mutate it to cover edge cases.
2. **Run Offline Evaluation**: Simulate multi-turn conversations between the AI agent and a user LM. Use an LM judge to grade interactions.
3. **Define Evaluation Criteria**: Collaborate with domain experts to create actionable metrics tied to business goals.
4. **Validate LM Judge**: Treat the LM judge as a classifier. Use precision and recall to validate its performance.
5. **Deploy to Production**: After passing offline evaluations, deploy the agent and monitor its performance using online evaluation tools.
6. **Continuous Improvement**: Use error analysis to identify failure modes and feed insights back into the agent.

For a detailed guide on implementing this workflow, see [Practical Guide](references/practical_guide.md).

## Code Snippets and Prompt Templates

### Synthetic Dataset Creation
```python
# Sample code to create synthetic dataset
from langchain import LLMChain

# Define user personas
user_personas = {
    'loyal_customer': 'A long-time Lyft customer frustrated with earnings.',
    'refund_seeker': 'A customer seeking a refund for a recent ride.'
}

# Generate synthetic queries
for persona, description in user_personas.items():
    prompt = f"Generate a customer support query for a {persona}: {description}"
    query = LLMChain.run(prompt)
    print(query)
```

### LM Judge Prompt Template
```markdown
You are an evaluator for a customer support AI agent. Your task is to grade the agent's response based on the following criteria:
1. **Helpfulness**: Did the agent resolve the customer's issue?
2. **Appropriateness**: Was the agent's response appropriate for the situation?
3. **Completeness**: Did the agent provide a complete response?

Please provide a score from 1 to 5 for each criterion and a brief explanation.
```

For more code examples, see [Code Examples](references/code_examples.md).

## Best Practices and Common Pitfalls

### Best Practices
- **Collaborate with Domain Experts**: Ensure evaluation metrics are actionable and aligned with business goals.
- **Validate LM Judges**: Use precision and recall to validate LM judge performance.
- **Continuous Improvement**: Regularly analyze errors and feed insights back into the agent.

### Common Pitfalls
- **Generic Metrics**: Avoid using pre-built metrics that are not actionable. Instead, create metrics tied to specific business outcomes.
- **Noisy LM Judges**: Ensure LM judges are calibrated and produce consistent scores.
- **Ignoring Data**: Always base evaluations on real production data to avoid unrealistic simulations.

For more on avoiding common pitfalls, see [Common Pitfalls](references/common_pitfalls.md).

## Validation and Testing

1. **Precision and Recall**: Validate LM judge performance using precision and recall metrics.
2. **Confidence Intervals**: Add confidence intervals to evaluation scores to ensure statistical rigor.
3. **Error Analysis**: Continuously analyze errors to identify and fix failure modes.

## References

```json
[
    {
        "filename": "core_concepts.md",
        "content": "## Core Concepts\n\n### Offline Evaluation\nOffline evaluation involves simulating multi-turn conversations between the AI agent and a user LM. This is done using synthetic datasets that are representative of production traffic. The goal is to ensure the agent performs well before deployment.\n\n### Online Evaluation\nOnline evaluation monitors the agent's performance in production. This includes tracing tools to track executions and context, as well as human-in-the-loop feedback to identify failure modes.\n\n### LM Judge\nAn LM judge is a language model used to evaluate agent interactions. It grades the agent's responses based on predefined criteria, ensuring scores are actionable and tied to business outcomes.\n\n### Continuous Learning\nContinuous learning involves feeding evaluation insights back into the agent to improve its performance. This can include updating model weights, context, and harness."
    },
    {
        "filename": "practical_guide.md",
        "content": "## Practical Guide\n\n### Step 1: Develop Synthetic Dataset\nCreate a dataset that closely resembles production traffic. Use real production data and mutate it to cover edge cases.\n\n### Step 2: Run Offline Evaluation\nSimulate multi-turn conversations between the AI agent and a user LM. Use an LM judge to grade interactions.\n\n### Step 3: Define Evaluation Criteria\nCollaborate with domain experts to create actionable metrics tied to business goals.\n\n### Step 4: Validate LM Judge\nTreat the LM judge as a classifier. Use precision and recall to validate its performance.\n\n### Step 5: Deploy to Production\nAfter passing offline evaluations, deploy the agent and monitor its performance using online evaluation tools.\n\n### Step 6: Continuous Improvement\nUse error analysis to identify failure modes and feed insights back into the agent."
    },
    {
        "filename": "code_examples.md",
        "content": "## Code Examples\n\n### Synthetic Dataset Creation\n```python\n# Sample code to create synthetic dataset\nfrom langchain import LLMChain\n\n# Define user personas\nuser_personas = {\n    'loyal_customer': 'A long-time Lyft customer frustrated with earnings.',\n    'refund_seeker': 'A customer seeking a refund for a recent ride.'\n}\n\n# Generate synthetic queries\nfor persona, description in user_personas.items():\n    prompt = f\"Generate a customer support query for a {persona}: {description}\"\n    query = LLMChain.run(prompt)\n    print(query)\n```\n\n### LM Judge Prompt Template\n```markdown\nYou are an evaluator for a customer support AI agent. Your task is to grade the agent's response based on the following criteria:\n1. **Helpfulness**: Did the agent resolve the customer's issue?\n2. **Appropriateness**: Was the agent's response appropriate for the situation?\n3. **Completeness**: Did the agent provide a complete response?\n\nPlease provide a score from 1 to 5 for each criterion and a brief explanation.\n```"
    },
    {
        "filename": "common_pitfalls.md",
        "content": "## Common Pitfalls\n\n### Generic Metrics\nAvoid using pre-built metrics that are not actionable. Instead, create metrics tied to specific business outcomes.\n\n### Noisy LM Judges\nEnsure LM judges are calibrated and produce consistent scores. Validate their performance using precision and recall.\n\n### Ignoring Data\nAlways base evaluations on real production data to avoid unrealistic simulations. Use synthetic datasets that closely resemble production traffic."
    }
]
```

## Reference Guides

### Code Examples

## Code Examples

### Synthetic Dataset Creation
```python
# Sample code to create synthetic dataset
from langchain import LLMChain

# Define user personas
user_personas = {
    'loyal_customer': 'A long-time Lyft customer frustrated with earnings.',
    'refund_seeker': 'A customer seeking a refund for a recent ride.'
}

# Generate synthetic queries
for persona, description in user_personas.items():
    prompt = f"Generate a customer support query for a {persona}: {description}"
    query = LLMChain.run(prompt)
    print(query)
```

### LM Judge Prompt Template
```markdown
You are an evaluator for a customer support AI agent. Your task is to grade the agent's response based on the following criteria:
1. **Helpfulness**: Did the agent resolve the customer's issue?
2. **Appropriateness**: Was the agent's response appropriate for the situation?
3. **Completeness**: Did the agent provide a complete response?

Please provide a score from 1 to 5 for each criterion and a brief explanation.
```

### Common Pitfalls

## Common Pitfalls

### Generic Metrics
Avoid using pre-built metrics that are not actionable. Instead, create metrics tied to specific business outcomes.

### Noisy LM Judges
Ensure LM judges are calibrated and produce consistent scores. Validate their performance using precision and recall.

### Ignoring Data
Always base evaluations on real production data to avoid unrealistic simulations. Use synthetic datasets that closely resemble production traffic.

### Core Concepts

## Core Concepts

### Offline Evaluation
Offline evaluation involves simulating multi-turn conversations between the AI agent and a user LM. This is done using synthetic datasets that are representative of production traffic. The goal is to ensure the agent performs well before deployment.

### Online Evaluation
Online evaluation monitors the agent's performance in production. This includes tracing tools to track executions and context, as well as human-in-the-loop feedback to identify failure modes.

### LM Judge
An LM judge is a language model used to evaluate agent interactions. It grades the agent's responses based on predefined criteria, ensuring scores are actionable and tied to business outcomes.

### Continuous Learning
Continuous learning involves feeding evaluation insights back into the agent to improve its performance. This can include updating model weights, context, and harness.

### Practical Guide

## Practical Guide

### Step 1: Develop Synthetic Dataset
Create a dataset that closely resembles production traffic. Use real production data and mutate it to cover edge cases.

### Step 2: Run Offline Evaluation
Simulate multi-turn conversations between the AI agent and a user LM. Use an LM judge to grade interactions.

### Step 3: Define Evaluation Criteria
Collaborate with domain experts to create actionable metrics tied to business goals.

### Step 4: Validate LM Judge
Treat the LM judge as a classifier. Use precision and recall to validate its performance.

### Step 5: Deploy to Production
After passing offline evaluations, deploy the agent and monitor its performance using online evaluation tools.

### Step 6: Continuous Improvement
Use error analysis to identify failure modes and feed insights back into the agent.

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Build Evals That Actually Matter - Nick Ung, Lyft](https://www.youtube.com/watch?v=3z2uT5aDx_Y)** by AI Engineer