---
name: fine-tuning-workflow
version: 1.0.0
min_mindforge_version: 0.1.0
status: stable
triggers: fine tuning, dataset preparation, training config, eval during training, model deployment, model A/B test, LoRA adapter, training data quality, hyperparameter tuning, model versioning, training pipeline, fine tune evaluation
---

# Skill — Fine-Tuning Workflow

## When this skill activates
Any task involving LLM fine-tuning, training dataset preparation, LoRA/QLoRA
adaptation, model evaluation during training, or model deployment with A/B testing.

## Mandatory actions when this skill is active

### Before writing any code
1. Define the fine-tuning objective (style adaptation, domain knowledge, task specialization).
2. Audit training data quality (deduplication, format consistency, bias check).
3. Establish baseline metrics with the un-tuned model.

### During implementation
- Run evaluation on held-out validation set at regular intervals during training.
- Implement early stopping on quality degradation.
- Track training metrics: loss, eval metrics, learning rate schedule.

### After implementation
- Compare fine-tuned model against baseline on the eval suite.
- Deploy with canary traffic (shadow or A/B testing).
- Document the model card with training details and performance.

## Dataset Preparation

### Data Requirements by Objective
| Objective | Min Examples | Quality Requirement |
|-----------|-------------|-------------------|
| Style/tone adaptation | 100-500 | High quality exemplars of target style |
| Domain knowledge | 1,000-10,000 | Accurate, diverse domain Q&A pairs |
| Task specialization | 500-5,000 | Varied task examples with edge cases |
| Instruction following | 1,000+ | Diverse instruction/response pairs |

### Data Format (Instruction Tuning)
```jsonl
{"messages": [
  {"role": "system", "content": "You are a helpful coding assistant."},
  {"role": "user", "content": "Write a function to reverse a string in Python."},
  {"role": "assistant", "content": "def reverse_string(s: str) -> str:\n    return s[::-1]"}
]}
```

### Data Quality Checklist
- [ ] Deduplicated (no exact or near-duplicate examples).
- [ ] Consistent format across all examples.
- [ ] Balanced across categories/topics.
- [ ] No PII or sensitive data (unless intentional and consented).
- [ ] Correct and high-quality responses (garbage in = garbage out).
- [ ] Diverse inputs (length, complexity, edge cases).

### Data Cleaning Pipeline
1. **Deduplication**: hash-based exact dedup + embedding-based semantic dedup.
2. **Format validation**: ensure all examples match expected schema.
3. **Quality filtering**: remove low-quality examples (too short, incoherent).
4. **Balance check**: verify distribution across categories.
5. **Contamination check**: ensure eval data not in training set.

## Training Approaches

### Full Fine-Tuning
- Updates all model parameters.
- Use for: significant behavior changes, large datasets.
- Cost: high (full model in GPU memory, long training time).
- Risk: catastrophic forgetting of base model capabilities.

### LoRA (Low-Rank Adaptation)
- Adds small trainable matrices alongside frozen base model.
- Use for: most fine-tuning tasks (efficient, less forgetting).
- Cost: low (only adapter weights in GPU memory).
- Benefit: merge adapter with base model for zero-overhead inference.

### QLoRA (Quantized LoRA)
- Base model quantized to 4-bit, LoRA adapters in 16-bit.
- Use for: large models on limited GPU memory.
- Cost: very low (fits 70B model on single GPU for training).
- Trade-off: slight quality reduction from quantization.

### Key Hyperparameters
| Parameter | Typical Range | Notes |
|-----------|--------------|-------|
| Learning rate | 1e-5 to 5e-5 | Lower for larger models |
| Batch size | 4-32 | Larger = more stable, needs more memory |
| Epochs | 1-5 | More epochs risk overfitting |
| LoRA rank | 8-64 | Higher = more capacity, more compute |
| LoRA alpha | 16-128 | Usually 2x rank |
| Warmup steps | 5-10% of total | Prevents early divergence |

## Evaluation During Training

### Validation Set
- Hold out 10-20% of data as validation (never train on it).
- Evaluate every N steps (e.g., every 100 steps or every epoch).
- Track: validation loss, task-specific metrics.

### Early Stopping
- Stop training if validation metric doesn't improve for N evaluations.
- Prevents overfitting (model memorizes training data).
- Save checkpoint at best validation score, not last step.

### Evaluation Metrics
| Metric | Use Case | What It Measures |
|--------|----------|-----------------|
| Perplexity | General quality | Model confidence on held-out data |
| ROUGE-L | Summarization | Overlap with reference summaries |
| Exact Match | Q&A, classification | Correct answer percentage |
| Human preference | Style/quality | A/B comparison by annotators |
| Task-specific | Custom tasks | Domain-specific correctness |

## Model Deployment

### Deployment Pipeline
```
Train → Evaluate → Register → Shadow Test → Canary → Full Rollout
```

### Model Registry
- Version every model with: training data hash, hyperparameters, eval scores.
- Store model artifacts in versioned storage (S3, GCS, MLflow).
- Link to training run for full reproducibility.

### Shadow Traffic Testing
- Deploy new model alongside production model.
- Route production traffic to both (only serve old model's response).
- Compare outputs offline (quality, latency, error rate).
- Promote to canary only if shadow results are satisfactory.

### Canary Rollout
- Route 5% of traffic to new model.
- Monitor: quality metrics, latency p99, error rate, user feedback.
- If metrics are good after 24-48 hours: increase to 25% → 50% → 100%.
- Rollback instantly if any metric degrades.

## A/B Testing

### Experiment Design
- Split users randomly (not requests — same user should see same model).
- Define primary metric (quality score, user satisfaction, task completion).
- Define guardrail metrics (latency, error rate, cost).
- Run for statistical significance (typically 1-2 weeks).

### Analysis
- Compare primary metric between control (old model) and treatment (new model).
- Verify guardrail metrics haven't degraded.
- Check for segment effects (does new model help some users but hurt others?).
- Document results and decision in model card.

## Model Versioning (Model Card)

```yaml
model_card:
  name: customer-support-assistant-v3
  base_model: llama-3-8b
  adapter: LoRA (rank 32)
  training_data:
    source: customer_support_conversations_2024
    examples: 5,432
    hash: sha256:def456...
  hyperparameters:
    learning_rate: 2e-5
    epochs: 3
    batch_size: 16
    lora_rank: 32
  evaluation:
    held_out_accuracy: 0.89
    human_preference_win_rate: 0.72
    latency_p99_ms: 340
  deployed_at: 2024-01-20
  parent_version: customer-support-assistant-v2
```

## Self-check before task completion

Before marking a task done when this skill was active:

- [ ] Did I read the full SKILL.md before starting? (Not just the triggers)
- [ ] Is training data deduplicated, validated, and quality-checked?
- [ ] Is evaluation running on held-out validation set during training?
- [ ] Is early stopping configured to prevent overfitting?
- [ ] Are baseline metrics established for comparison?
- [ ] Is the model versioned with full training lineage?
- [ ] Is deployment using canary/A/B testing (not instant full rollout)?
