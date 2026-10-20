# Copilot Instructions: Agentic Experimentation For High Stakes Ml Systems
Description: A skill for AI agents to safely and efficiently experiment with high-stakes ML systems by modifying features, training models, and deploying pipelines in isolated environments while maintaining production integrity.

# Agentic Experimentation for High-Stakes ML Systems

## Overview
This skill enables AI agents to safely experiment with and improve high-stakes machine learning systems like fraud detection models. The approach centers around using specialized infrastructure (like [Chronon](references/core_concepts.md)) that provides:
- Safe experimentation environments
- Automated feature engineering
- Production-grade pipeline generation

Key principles from the [Core Concepts](references/core_concepts.md) guide the agent's actions to ensure system stability while enabling rapid iteration.

## Step-by-Step Workflow
1. **Establish Isolation**
   - Create a dedicated branch for the experiment
   - Configure isolated compute/storage resources

2. **Feature Modification**
   - Start from existing production feature set
   - Make incremental changes (add/remove/modify features)
   - Use semantic API as shown in [Code Examples](references/code_examples.md)

3. **Data Generation**
   - Generate training data using platform's backfill capability
   - Leverage automatic compute reuse for unchanged features

4. **Model Training**
   - Train new model version on isolated infrastructure
   - Maintain consistency between training/serving pipelines

5. **Evaluation Packaging**
   - Generate comprehensive experiment report
   - Include:
     - Feature changes
     - Model metrics
     - Resource usage
     - Reproducibility instructions

6. **Human Handoff**
   - Present results for human review
   - Prepare materials for potential AB test

## Best Practices
1. **Incremental Changes**: Focus on small, interpretable modifications rather than wholesale redesigns.
2. **Reuse First**: Always build upon existing production features when possible.
3. **Document Everything**: Ensure every experiment is fully documented for review.
4. **Resource Awareness**: Monitor compute usage and stay within allocated budgets.

## Common Pitfalls
1. **Over-Experimentation**: Avoid running too many concurrent experiments without proper resource controls.
2. **Production Contamination**: Never allow experimental code to modify production data directly.
3. **Black Box Changes**: Ensure all feature modifications have clear semantics and documentation.
4. **Cost Blindness**: Monitor infrastructure costs which can scale quickly with many experiments.

## Validation Steps
1. **Consistency Checks**: Verify training/serving data pipelines produce identical outputs given same inputs.
2. **Performance Testing**: Ensure new model versions meet latency/QPS requirements.
3. **Reproducibility**: Confirm experiments can be exactly reproduced from their definitions.
4. **Safety Review**: Human verification that all isolation mechanisms worked correctly.

For implementation details, see the [Practical Guide](references/practical_guide.md) and [Code Examples](references/code_examples.md).

## Reference Guides

### Code Examples

# Code Examples and Templates

## Feature Definition Example (Chronon API)
```python
# Defining a new feature to add to fraud detection model
from chronon import GroupBy, Aggregation

# Reusing existing production features
payment_features = GroupBy(
    sources=["table.payments"],  # Existing production data source
    keys=["user_id"],           # Join key
    aggregations=[
        # Existing 30-day feature
        Aggregation(
            operation="SUM",
            column="amount",
            windows=["30d"]
        ),
        # New 7-day feature proposed by agent
        Aggregation(
            operation="SUM",
            column="amount",
            windows=["7d"],  # New window size
            name="payment_sum_7d"  # Explicit naming
        )
    ]
)
```

## Experiment Workflow Template
```python
# Agent experiment workflow pseudocode
def run_experiment():
    # 1. Create isolated branch
    branch = create_isolated_branch("fraud-model-iteration-42")
    
    # 2. Modify feature set (reusing existing features)
    new_features = modify_features(
        existing="prod_fraud_features",
        modifications=["add_7d_window"]
    )
    
    # 3. Generate training data (automatically reuses computations)
    training_data = generate_training_data(
        features=new_features,
        isolation_branch=branch
    )
    
    # 4. Train model (on isolated resources)
    model = train_model(
        data=training_data,
        target="is_fraud",
        infrastructure="dev"
    )
    
    # 5. Package results for review
    return {
        "branch": branch,
        "feature_changes": diff("prod", branch),
        "model_metrics": model.evaluate(),
        "compute_cost": get_cost(branch)
    }
```

## Safety Checks
```python
# Pre-flight checks before experiment runs
def safety_checks(feature_changes):
    # Ensure no production data will be modified
    assert not feature_changes.affects_production(), \
        "Cannot modify production data directly"
    
    # Validate resource limits
    assert estimated_cost(feature_changes) < MAX_BUDGET, \
        f"Experiment exceeds ${MAX_BUDGET} budget"
    
    # Verify feature semantics are clear
    assert feature_changes.is_semantically_clear(), \
        "Feature changes must have clear semantics"
```

### Core Concepts

# Core Concepts of Agentic Experimentation

Agentic experimentation refers to the process where AI agents autonomously modify and improve high-stakes machine learning systems while maintaining safety, reproducibility, and reviewability. Key concepts include:

1. **Infrastructure Automation**: The agent interacts with a semantic API (like Chronon) that abstracts away complex pipeline management. The API handles training data generation, model serving pipelines, and ensures consistency between training and inference environments.

2. **Resource Isolation**: Experiments run in isolated branches with dedicated compute/storage resources. This prevents interference with production systems while allowing controlled access to production data.

3. **Compute Reuse**: The system intelligently reuses precomputed features and partial aggregates from production to minimize redundant computations during experimentation.

4. **Reviewable Outputs**: All agent-generated changes must be production-ready and understandable by human reviewers before promotion to production.

5. **Safety Mechanisms**: Branch-based isolation, versioned outputs, and semantic hashing ensure experiments can't accidentally modify production data or pipelines.

These concepts work together to enable rapid iteration on critical systems like fraud detection, trust & safety models, and personalization systems where mistakes can have serious business consequences.

### Practical Guide

# Practical Guide to Implementing Agentic Experimentation

## Setting Up the Environment
1. **Infrastructure Foundation**: Deploy Chronon or equivalent feature platform that provides:
   - Unified feature definition API
   - Automated training/serving pipeline generation
   - Branch-based resource isolation

2. **Agent Tooling**: Equip your agent with:
   - Access to the feature platform's API
   - Data exploration capabilities
   - Model training orchestration
   - Resource monitoring/limiting

## Workflow Patterns
1. **Feature Modification**: Agents should:
   - Start from existing production feature sets
   - Make incremental changes (e.g., adding time windows)
   - Leverage platform's compute reuse capabilities

2. **Experiment Lifecycle**:
   - All changes occur in isolated branches
   - Training data generated from modified features
   - Models trained on dev infrastructure
   - Results presented for human review

3. **Promotion Process**:
   - Human reviews all changes
   - AB tests conducted before full production rollout
   - Gradual rollout with monitoring

## Cost Management
- Set resource limits at team/agent level
- Monitor compute usage per experiment
- Establish budgets for experimental infrastructure

## Team Coordination
- Maintain shared feature repository
- Document all experiments
- Establish review protocols for high-stakes changes

### Sources

# Video Sources

The following curated videos were synthesized to create this skill:

1. **[Why AI Agents Shouldn't Replace Your Fraud Models](https://www.youtube.com/watch?v=HaWk8kAD8ZU)** by MLOps.community