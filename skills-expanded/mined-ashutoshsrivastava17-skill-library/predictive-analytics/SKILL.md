---
name: predictive-analytics
description: >
  Design predictive analytics solutions — feature engineering, model selection,
  validation strategy, deployment planning, and business impact estimation.
  TRIGGER when: user says /predictive-analytics, wants to predict outcomes,
  needs forecasting models, or asks about building predictive models.
argument-hint: "[outcome to predict and available data]"
user-invocable: true
---

# Predictive Analytics

You are a data science specialist. Guide the user through designing a predictive analytics solution from problem framing to deployment.

## Process

### Step 1: Frame the Problem

| Question | Answer Needed |
|----------|--------------|
| What are you predicting? | Target variable definition |
| Why does this prediction matter? | Business value and decisions it enables |
| What actions will be taken? | How predictions drive interventions |
| What time horizon? | Next day, week, month, quarter? |
| What accuracy is "good enough"? | Business-acceptable error rate |
| What's the baseline? | Current heuristic or naive prediction |

### Step 2: Assess Data Readiness

| Dimension | Check |
|-----------|-------|
| Target variable | Is it well-defined and available historically? |
| Feature availability | Are predictive signals available at prediction time? |
| Data volume | Enough historical examples (1000+ for most ML) |
| Label quality | Are historical outcomes accurately recorded? |
| Data freshness | How often is data updated? |
| Leakage risk | Any features that encode the outcome? |

### Step 3: Engineer Features

| Feature Type | Examples |
|-------------|---------|
| Behavioral | Usage frequency, recency, intensity |
| Temporal | Day of week, seasonality, time since event |
| Aggregate | Rolling averages, cumulative counts, percentiles |
| Categorical | Segment, plan type, geography |
| Interaction | Feature crosses, ratios |
| External | Market data, weather, economic indicators |

### Step 4: Select and Train Models

| Model | Strengths | Best For |
|-------|----------|----------|
| Logistic regression | Interpretable, fast | Binary classification baseline |
| Random forest | Handles non-linearity, robust | Tabular data, feature importance |
| Gradient boosting (XGBoost/LightGBM) | High accuracy, handles missing data | Most tabular prediction tasks |
| Neural networks | Complex patterns | Large datasets, embeddings |
| Time series (ARIMA, Prophet) | Temporal patterns | Forecasting |

### Step 5: Validate Rigorously

| Validation Method | When to Use |
|-------------------|------------|
| K-fold cross-validation | Standard, sufficient data |
| Time-series split | Temporal data (no future leakage) |
| Stratified split | Imbalanced classes |
| Holdout test set | Final unbiased evaluation |
| Backtesting | Simulate predictions on historical periods |

**Metrics by problem type:**

| Problem | Primary Metric | Secondary |
|---------|---------------|-----------|
| Binary classification | AUC-ROC, PR-AUC | Precision, Recall, F1 |
| Multi-class | Macro F1, Accuracy | Per-class metrics |
| Regression | RMSE, MAE | MAPE, R² |
| Ranking | NDCG, MAP | Precision@K |

### Step 6: Plan Deployment

| Phase | Activities |
|-------|-----------|
| Scoring pipeline | Batch vs real-time, frequency, infrastructure |
| Monitoring | Prediction drift, feature drift, outcome feedback |
| Retraining | Cadence, triggers, automated vs manual |
| Decision integration | How predictions feed into workflows/UIs |
| Impact measurement | A/B test predictions vs baseline |

## Output Format

```markdown
## Predictive Analytics Design

### Problem: Predict [target] for [entity] over [time horizon]
### Business Impact: [decisions enabled, estimated value]

### Model Performance
| Metric | Baseline | Model | Lift |
|--------|----------|-------|------|
| [metric] | X | X | +X% |

### Feature Importance (Top 10)
| Rank | Feature | Importance |
|------|---------|-----------|
| 1 | [feature] | X% |

### Deployment Plan
- Scoring: [batch/real-time] | Retraining: [cadence]
- Integration: [how predictions are consumed]
```

## Quality Checklist

- [ ] Problem is well-framed with clear business value
- [ ] No data leakage in features
- [ ] Validation uses appropriate time-aware splits
- [ ] Model compared against meaningful baseline
- [ ] Feature importance is reviewed for sanity
- [ ] Monitoring plan covers drift detection
- [ ] Retraining cadence is defined

## Edge Cases

- If target event is rare (< 1%), use stratified sampling and PR-AUC
- For cold-start predictions (new users), build separate heuristic models
- If features have high latency, use only features available at prediction time
- For regulated decisions (credit, hiring), ensure model explainability
- If data distribution shifts seasonally, retrain more frequently
