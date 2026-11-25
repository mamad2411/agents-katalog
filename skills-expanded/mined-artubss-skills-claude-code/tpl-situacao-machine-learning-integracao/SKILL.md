---
name: tpl-situacao-machine-learning-integracao
description: Template do pack (situacao/16-machine-learning-integracao.md). Orienta o agente em tarefas situacionais como debug, seguranca e refactor alinhado a esse contexto.
metadata:
  version: 1.0.0
  source_template: situacao/16-machine-learning-integracao.md
  generated_by: install_pack_templates_as_claude_skills
---

# SITUATION: Machine Learning Model Integration

Skill gerado a partir do pack `templates-claude-code`. Arquivo de origem: `situacao/16-machine-learning-integracao.md`. Use como baseline e adapte ao projeto antes de mudancas grandes.

## Conteudo do template

## CONTEXT
Use this configuration when integrating a trained machine learning model into a production application — whether it's a recommendation engine, fraud classifier, sentiment analyzer, content moderator, or any model served via API or embedded SDK. ML models in production have unique failure modes that differ from traditional software: they can be "right" statistically but wrong for individual cases, they degrade silently as data distributions shift, and they require careful A/B testing to safely update.

## OBJECTIVES
- Serve model predictions reliably with graceful fallback when the model is unavailable
- Validate all inputs before inference to prevent nonsensical predictions
- Monitor for data drift and model performance degradation post-launch
- Enable safe A/B testing of model versions without code deploys
- Collect ground truth for continuous model improvement

## APPROACH RULES

1. **Input validation before inference is mandatory.** Never pass raw user input to a model. Validate type, range, cardinality, and format. A model given garbage input produces confident garbage output — this is worse than an error.

2. **Always have a fallback.** When the model is unavailable (service down, timeout, error), fall back to a reasonable default: most popular items, rule-based logic, or graceful degradation (show without personalization). Never fail the entire request because the model is unavailable.

3. **Log every prediction for ground truth collection.** Log: input features, prediction output, confidence score, model version, and the user's eventual action. Without ground truth, you cannot measure model accuracy in production.

4. **Model versions are deployment artifacts.** Like Docker images, model versions must be immutable, tagged, and deployed explicitly. Never load "the latest model" automatically from a shared location in production.

5. **A/B test every model change.** Updating a model is a behavior change. It must go through the same A/B testing process as a product feature change. Traffic splitting, metric collection, and winner determination process must all apply.

6. **Confidence thresholds, not just predictions.** For high-stakes decisions (fraud, content moderation), set a confidence threshold below which the model defers to a human or applies a conservative default. A 51% confidence fraud prediction should not automatically block an account.

7. **Feature drift is the #1 cause of production ML failures.** Monitor input feature distributions. If the distribution of features being sent for inference drifts significantly from training distribution, model accuracy degrades silently.

## ROUTING TABLE

| If you encounter | Then |
|-----------------|------|
| Model service timeout | Activate fallback immediately. Log the timeout. Alert if timeout rate > 1%. |
| Model returns confidence < threshold | Apply conservative fallback logic. Do not act on low-confidence predictions for high-stakes decisions. |
| Input feature out of expected range | Reject or clip the value. Log as a data quality anomaly. Monitor frequency — could indicate upstream bug. |
| Model accuracy metrics degrading | Check: input feature drift, data pipeline issues, population shift. Trigger re-evaluation process. |
| New model version ready to deploy | Use A/B test with 5% → 20% → 50% → 100% rollout. Define success metric before starting. |
| Model serving latency increasing | Check: batch size, hardware utilization, model size. Consider: model quantization, caching, async serving. |
| Missing feature values | Apply agreed-upon imputation strategy (mean, median, mode, zero). Never send NULL to model. |
| Model predicts poorly on a subgroup | Evaluate dataset bias. Auditability required. Consult domain experts. Do not ship biased predictions for protected groups. |
| No ground truth collection | Build it before model goes live. Without ground truth, you cannot measure or improve. |
| Model file too large for web (frontend ML) | Quantize, prune, or use knowledge distillation. Or move to server-side inference. |

## Model Serving Architecture

```typescript
interface ModelPrediction {
  result: string | number | boolean
  confidence: number
  modelVersion: string
  latencyMs: number
}

class RecommendationService {
  constructor(
    private modelClient: ModelClient,
    private fallback: FallbackRecommendations,
    private logger: Logger,
    private metrics: MetricsClient
  ) {}

  async getRecommendations(userId: string, context: UserContext): Promise<Product[]> {
    const start = Date.now()
    
    try {
      // 1. Validate and prepare features
      const features = this.prepareFeatures(userId, context)
      this.validateFeatures(features)
      
      // 2. Call model with timeout
      const prediction = await Promise.race([
        this.modelClient.predict(features),
        timeout(500, new Error('Model timeout'))
      ])
      
      // 3. Apply confidence threshold
      if (prediction.confidence < 0.6) {
        this.logger.warn({ userId, confidence: prediction.confidence }, 'Low confidence prediction')
        return this.fallback.getPopularItems(context.category)
      }
      
      // 4. Log prediction for ground truth
      this.logPrediction(userId, features, prediction)
      
      this.metrics.histogram('model.latency', Date.now() - start)
      this.metrics.increment('model.predictions.served')
      
      return prediction.result as Product[]
      
    } catch (err) {
      this.metrics.increment('model.predictions.fallback')
      this.logger.error({ err, userId }, 'Model inference failed, using fallback')
      return this.fallback.getPopularItems(context.category)
    }
  }

  private logPrediction(userId: string, features: Features, prediction: ModelPrediction): void {
    // Critical: store this for ground truth collection
    this.predictionLog.save({
      timestamp: new Date().toISOString(),
      userId,
      features,
      prediction: prediction.result,
      confidence: prediction.confidence,
      modelVersion: prediction.modelVersion
    })
  }
}
```

## Feature Drift Monitoring

```python
from scipy import stats
import numpy as np

class FeatureDriftMonitor:
    def __init__(self, reference_distribution: dict):
        """
        reference_distribution: {feature_name: np.array of training values}
        """
        self.reference = reference_distribution
        
    def check_drift(self, current_window: dict, threshold: float = 0.05) -> dict:
        """
        Uses KS test to detect distribution drift.
        Returns: {feature_name: {'drifted': bool, 'p_value': float}}
        """
        results = {}
        for feature, current_values in current_window.items():
            if feature not in self.reference:
                continue
            
            ks_stat, p_value = stats.ks_2samp(
                self.reference[feature],
                current_values
            )
            
            drifted = p_value < threshold
            results[feature] = {'drifted': drifted, 'p_value': p_value, 'ks_stat': ks_stat}
            
            if drifted:
                logger.warning({'feature': feature, 'p_value': p_value}, 'Feature drift detected')
                metrics.increment('ml.feature_drift', tags=[f'feature:{feature}'])
        
        return results
```

## DO NOT

- **DO NOT** deploy a new model version to 100% of traffic without A/B testing
- **DO NOT** make irreversible decisions (account banning, transaction blocking) without a human review step for borderline cases
- **DO NOT** skip input validation — garbage in produces confident garbage out
- **DO NOT** use a single aggregate accuracy metric — slice by user segments and time periods
- **DO NOT** ignore low-confidence predictions — they often signal distribution shift
- **DO NOT** load ML models synchronously in web request handlers — pre-load at startup
- **DO NOT** store raw PII as features in prediction logs — hash/anonymize user identifiers
- **DO NOT** serve a model that wasn't tested on data representative of production distribution

## OUTPUT FORMAT

For each ML integration, deliver:

**ML Integration Spec:**
```markdown
## ML Integration: [Model Name]

### Model
- Type: Recommendation / Classification / Regression
- Framework: scikit-learn 1.3 / PyTorch 2.1 / ONNX
- Version: v2.4.1 (immutable artifact SHA: abc123)
- Training data: transactions 2023-01 to 2024-01

### Serving
- Endpoint: https://ml-api.internal/v1/recommend
- Method: REST POST / gRPC / embedded
- SLA: P95 < 200ms
- Timeout: 500ms (then fallback)

### Input Features
| Feature | Type | Range/Values | Handling if Missing |
|---------|------|-------------|--------------------| 
| user_age_days | int | 0-3650 | median imputation (365) |
| purchase_count | int | 0-999+ | clip at 999 |
| category | enum | [electronics, clothing, ...] | "unknown" category |

### Fallback Strategy
- Model unavailable: serve most popular items for the session's category
- Low confidence (< 0.6): serve curated editorial picks
- Feature validation failure: serve bestsellers

### Monitoring
- Latency tracking: P50, P95, P99 histograms
- Error rate: model unavailable, timeout, validation failure
- Feature drift: daily KS test vs training distribution
- Business metric: click-through rate on recommendations

### Ground Truth Collection
- Log: prediction request + features + output + model version
- Ground truth: user click/purchase on predicted item (join after 24h)
- Accuracy report: weekly, sliced by user segment and model version
```

## QUALITY GATES

- [ ] Input validation implemented and tested with adversarial inputs
- [ ] Fallback path tested independently (works without model available)
- [ ] Model version pinned and immutable in production config
- [ ] Ground truth collection implemented before first prediction served
- [ ] Confidence threshold defined and applied for high-stakes predictions
- [ ] Feature drift monitoring in place with alert threshold
- [ ] P95 inference latency < SLA with model loaded (test before launch)
- [ ] A/B test framework in place before first model update
- [ ] No PII stored in raw form in prediction logs
- [ ] On-call runbook for: model unavailable, high error rate, detected drift
