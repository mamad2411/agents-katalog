---
name: mlops-pipeline-orchestrator
description: "Orchestrates the end-to-end MLOps lifecycle: from data preparation and model training to deployment, monitoring, and continuous improvement. Ensures models are production-ready, performant, and compliant with best practices. Keywords: mlops, machine-learning, ml-pipeline, model-deployment, ml-monitoring, training-workflow."
version: 1
created: "2024-05-22"
updated: "2024-05-22"
---

# MLOps Pipeline Orchestrator - Production ML Lifecycle

This skill manages the transition of machine learning models from experimental research to production-grade services. It ensures that training, deployment, and monitoring are treated as a unified, repeatable pipeline.

## When to Use
Use this skill when:
- Deploying a new ML model to production.
- Setting up an automated training pipeline.
- Monitoring model performance and identifying drift.
- Scaling an ML inference service.

## The Orchestrated Workflow
This skill executes the following phases in sequence:

### Phase 1: Foundation & Training
1. **Best Practice Alignment**: Invoke `ml-best-practices` to establish the analysis steps, metrics, and evaluation criteria.
2. **Model Engineering**: Invoke `ml-engineer` to build the training logic, handle feature engineering, and implement model architecture.
3. **Pipeline Construction**: Invoke `ml-pipeline-workflow` to build the end-to-end pipeline (data $\rightarrow$ training $\rightarrow$ validation).

### Phase 2: Deployment & Infrastructure
4. **MLOps Engineering**: Invoke `mlops-engineer` to set up experiment tracking, model registries, and deployment infrastructure (e.g., Kubeflow, MLflow).
5. **Inference Optimization**: Invoke `ml-engineer` to optimize inference for production environments.

### Phase 3: Monitoring & Governance
6. **Performance Monitoring**: Use `ml-best-practices` to define SLIs/SLOs for the model.
7. **Continuous Improvement**: Invoke `ml-pipeline-workflow` to automate retraining loops based on performance metrics.

## Freedom Calibration & Constraints
- **Constraint Level: Medium**
  - **Rigidity**: The sequence of training $\rightarrow$ deployment $\rightarrow$ monitoring is mandatory.
  - **Freedom**: The choice of framework (PyTorch, TensorFlow) and specific hyperparameters is left to the ML engineer.

## Critical Anti-Patterns (NEVER List)
| Anti-Pattern | Description | Alternative / Solution |
| :--- | :--- | :--- |
| **NEVER** ignore data drift | Models degrade over time; production models must be monitored. | Use `mlops-engineer` to set up monitoring. |
| **NEVER** skip validation | Never deploy a model without a formal validation step against a holdout set. | Invoke `ml-pipeline-workflow` for automated validation. |
| **NEVER** manual deployment | Manually moving weights to production is prone to errors. | Use `mlops-engineer` for automated deployment. |

## Verification
1. A validated model is trained and evaluated against best practices.
2. A production deployment pipeline is established.
3. Monitoring and alerting for model performance are configured.
4. An experiment tracking system is active.
