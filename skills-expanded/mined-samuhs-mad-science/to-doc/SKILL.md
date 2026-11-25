---
name: to-doc
description: "Turn the current conversation into an experiment doc (hypothesis, premises, baseline, success metrics, experiment stories) and publish it to the project docs, with no new interview. Use after /hypothesys, or when the user says 'write the experiment doc', 'document this experiment' or 'turn this into a doc'."
mode: true
icon: crown
color: red
---

This skill takes the current conversation context and codebase understanding and produces documentation. Do NOT interview the user; just synthesize what you already know.

## Process

1- Explore the repo to understand the current state of the codebase, if you haven't already. Use the project's domain glossary vocabulary throughout the docs.

2- Sketch out the validation checkpoints at which you're going to evaluate the experiment. Existing pipeline splits and validation metrics should be preferred to new ones. Evaluate at the highest level possible (e.g., end-to-end model performance or business metrics). If new checkpoints are needed, propose them at the highest point you can in the pipeline. The fewer disjointed evaluation scripts across the workflow, the better - the ideal number is one unified evaluation step.

Check with the user that these seams match their expectations.

3- Write the doc using the template below, then publish it to the project documentation.


## Hypothesis
The hypothesis that the user is facing, from the user's or business's perspective.

## Premises
The premises to the problem and the underlying assumptions, from the user's perspective.

## Baseline & Current State
What the experiment is trying to beat. Describe the current environment, whether it is an existing model, a manual human process, or hardcoded business rules (e.g., "if score > 50, approve").

## Success Metrics & Goals
The exact definition of how success will be measured. This should be divided into:

- Offline Metrics: Model evaluation metrics during training (e.g., RMSE, F1-Score, Precision, Recall).
- Online/Business Metrics: Business impact metrics when the model is in production (e.g., Conversion rate, LTV, Churn reduction).

## Experiment Stories
A LONG, numbered list of user experiments or testable hypotheses. Each story should be in the format of:

As a [role], I want a [feature/test], so that [outcome]

As a Data Scientist, I want to test the inclusion of geolocation features, so that I can see if it increases the F1-Score by 5%.
As a mobile bank customer, I want to see a spending forecast, so that I can make better-informed decisions about my budget.

This list of experiment stories should be extremely extensive and cover all aspects of the problem and modeling iterations.

## Data Sources & Target Definition
Data Sources: Where the data comes from (specific databases, tables, external APIs, or data lakes).

Target Definition: The exact mathematical or logical definition of the target variable (e.g., "Churn = customer has not made a transaction in the last 30 days").

## Validation Strategy
How the data will be split and evaluated to prevent data leakage and simulate real-world performance fairly. Detail the data splits (Train/Validation/Test), validation methods (e.g., Out-of-Time split, K-Fold Cross-validation), and the specific pipeline checkpoints used for evaluation.

## Implementation Decisions
A list of implementation decisions that were made regarding both software engineering and data science. This can include:

- Algorithm selections and feature engineering techniques.

- The modules that will be built/modified.

- The interfaces of those modules that will be modified.

- Technical clarifications from the developer/data engineer.

- Architectural decisions.

- Specific interactions.

Do NOT include specific file paths or code snippets. They may end up being outdated very quickly.
Exception: If a prototype produced a snippet that encodes a decision more precisely than prose can (state machine, reducer, schema, type shape), inline it within the relevant decision and note briefly that it came from a prototype. Trim to the decision-rich parts, not a working demo, just the important bits.

## Risks, Constraints & Caveats
The limitations of the experiment and system constraints. This includes latency requirements (e.g., model must respond in < 100ms), potential data bias, computational limits, and privacy/compliance concerns (e.g., GDPR/LGPD restrictions).

## Further Notes
Any further notes, context, or references about the experiment.

Confirm the doc with the user before save. When user confirms save the file on docs folder with this pattern name: `docs/experiments-doc/<today_date>_<hypothesis>.md`