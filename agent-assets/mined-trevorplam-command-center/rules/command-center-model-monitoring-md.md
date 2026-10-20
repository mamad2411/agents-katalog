---
description: Run Model Monitoring and Explainability Standards Check
globs: ['**/model-monitoring/**/*.ts', '**/explainability/**/*.ts', '**/ml-observability/**/*.ts']
---

# AI/ML: Model Monitoring & Explainability Standards

<audit_rules>

- You MUST implement proper model performance monitoring with accuracy, precision, recall, and F1 metrics.
- You MUST ensure proper data drift detection with statistical tests and visualization.
- You MUST implement proper model explainability using SHAP, LIME, or similar techniques.
- You MUST configure proper bias detection and fairness monitoring across protected attributes.
- You MUST ensure proper model interpretability for regulatory compliance (GDPR, CCPA).
- You MUST implement proper anomaly detection for model predictions and input data.
- You MUST configure proper alerting and incident response for model degradation.
- You MUST ensure proper model version comparison and A/B testing capabilities.
- You MUST implement proper cost monitoring for model inference and maintenance.
- You MUST ensure proper user feedback collection and model improvement loops.
  </audit_rules>

<example_good>

```typescript
// Model Monitoring & Explainability Implementation

export class ModelMonitoringOrchestrator {
  constructor(
    private performanceMonitor: PerformanceMonitor,
    private driftDetector: DriftDetector,
    private biasMonitor: BiasMonitor,
    private explainabilityEngine: ExplainabilityEngine,
    private alertingService: AlertingService,
    private feedbackCollector: FeedbackCollector
  ) {}

  async setupModelMonitoring(config: ModelMonitoringConfig): Promise<ModelMonitoringSetup> {
    // Setup performance monitoring
    const performanceSetup = await this.performanceMonitor.setup({
      modelId: config.modelId,
      metrics: config.performanceMetrics || ['accuracy', 'precision', 'recall', 'f1'],
      evaluationInterval: config.evaluationInterval || 300000, // 5 minutes
      thresholds: config.performanceThresholds,
    })

    // Setup drift detection
    const driftSetup = await this.driftDetector.setup({
      modelId: config.modelId,
      referenceData: config.referenceData,
      driftThresholds: config.driftThresholds || { feature_drift: 0.05, concept_drift: 0.1 },
      monitoringFeatures: config.monitoringFeatures || ['all'],
    })

    // Setup bias monitoring
    const biasSetup = await this.biasMonitor.setup({
      modelId: config.modelId,
      protectedAttributes: config.protectedAttributes || [],
      fairnessMetrics: config.fairnessMetrics || ['demographic_parity', 'equal_opportunity'],
      evaluationInterval: config.biasEvaluationInterval || 600000, // 10 minutes
    })

    // Setup explainability
    const explainabilitySetup = await this.explainabilityEngine.setup({
      modelId: config.modelId,
      techniques: config.explainabilityTechniques || ['shap', 'lime'],
      sampleSize: config.explainabilitySampleSize || 100,
    })

    // Setup alerting
    const alertingSetup = await this.alertingService.setup({
      modelId: config.modelId,
      channels: config.alertingChannels || ['email', 'slack'],
      thresholds: config.alertingThresholds,
      escalationPolicy: config.escalationPolicy,
    })

    return {
      modelId: config.modelId,
      performance: performanceSetup,
      drift: driftSetup,
      bias: biasSetup,
      explainability: explainabilitySetup,
      alerting: alertingSetup,
      status: 'active',
    }
  }

  async monitorModelPerformance(modelId: string): Promise<ModelPerformanceReport> {
    // Get current performance metrics
    const currentMetrics = await this.performanceMonitor.getCurrentMetrics(modelId)

    // Get baseline metrics
    const baselineMetrics = await this.performanceMonitor.getBaselineMetrics(modelId)

    // Calculate performance degradation
    const degradation = this.calculatePerformanceDegradation(baselineMetrics, currentMetrics)

    // Get performance trend
    const trend = await this.performanceMonitor.getPerformanceTrend(modelId, '24h')

    // Generate performance insights
    const insights = await this.generatePerformanceInsights(currentMetrics, baselineMetrics, trend)

    return {
      modelId,
      timestamp: Date.now(),
      current: currentMetrics,
      baseline: baselineMetrics,
      degradation,
      trend,
      insights,
      status: this.calculatePerformanceStatus(degradation),
    }
  }

  async monitorModelDrift(modelId: string): Promise<ModelDriftReport> {
    // Get current feature statistics
    const currentStats = await this.driftDetector.getCurrentStatistics(modelId)

    // Get reference statistics
    const referenceStats = await this.driftDetector.getReferenceStatistics(modelId)

    // Calculate feature drift
    const featureDrift = await this.driftDetector.calculateFeatureDrift(
      currentStats,
      referenceStats
    )

    // Calculate concept drift
    const conceptDrift = await this.driftDetector.calculateConceptDrift(modelId)

    // Get drift trend
    const driftTrend = await this.driftDetector.getDriftTrend(modelId, '24h')

    // Generate drift insights
    const insights = await this.generateDriftInsights(featureDrift, conceptDrift, driftTrend)

    return {
      modelId,
      timestamp: Date.now(),
      featureDrift,
      conceptDrift,
      trend: driftTrend,
      insights,
      status: this.calculateDriftStatus(featureDrift, conceptDrift),
    }
  }

  async monitorModelBias(modelId: string): Promise<ModelBiasReport> {
    // Get current bias metrics
    const currentMetrics = await this.biasMonitor.getCurrentMetrics(modelId)

    // Get baseline bias metrics
    const baselineMetrics = await this.biasMonitor.getBaselineMetrics(modelId)

    // Calculate bias changes
    const biasChanges = this.calculateBiasChanges(baselineMetrics, currentMetrics)

    // Get bias trend
    const biasTrend = await this.biasMonitor.getBiasTrend(modelId, '24h')

    // Generate bias insights
    const insights = await this.generateBiasInsights(currentMetrics, baselineMetrics, biasTrend)

    return {
      modelId,
      timestamp: Date.now(),
      current: currentMetrics,
      baseline: baselineMetrics,
      changes: biasChanges,
      trend: biasTrend,
      insights,
      status: this.calculateBiasStatus(currentMetrics),
    }
  }

  async generateModelExplanation(
    modelId: string,
    input: ModelInput,
    config: ExplanationConfig
  ): Promise<ModelExplanation> {
    // Generate explanations using configured techniques
    const explanations = {}

    for (const technique of config.techniques) {
      switch (technique) {
        case 'shap':
          explanations.shap = await this.explainabilityEngine.generateSHAPExplanation(
            modelId,
            input
          )
          break
        case 'lime':
          explanations.lime = await this.explainabilityEngine.generateLIMEExplanation(
            modelId,
            input
          )
          break
        case 'permutation_importance':
          explanations.permutationImportance =
            await this.explainabilityEngine.generatePermutationImportance(modelId, input)
          break
        case 'partial_dependence':
          explanations.partialDependence =
            await this.explainabilityEngine.generatePartialDependence(modelId, input)
          break
      }
    }

    // Generate global explanations if requested
    if (config.globalExplanation) {
      explanations.global = await this.explainabilityEngine.generateGlobalExplanation(modelId)
    }

    // Validate explanation quality
    const validation = await this.validateExplanationQuality(explanations)

    return {
      modelId,
      input: this.sanitizeInput(input),
      explanations,
      validation,
      timestamp: Date.now(),
    }
  }

  async collectFeedback(
    modelId: string,
    feedback: ModelFeedback
  ): Promise<FeedbackCollectionResult> {
    // Validate feedback
    const validation = await this.feedbackCollector.validateFeedback(feedback)
    if (!validation.isValid) {
      throw new Error(`Invalid feedback: ${validation.errors.join(', ')}`)
    }

    // Store feedback
    const storedFeedback = await this.feedbackCollector.storeFeedback(modelId, feedback)

    // Update model metrics based on feedback
    await this.updateModelMetrics(modelId, storedFeedback)

    // Check if retraining is needed
    const retrainingTrigger = await this.evaluateRetrainingNeed(modelId, storedFeedback)

    return {
      feedbackId: storedFeedback.id,
      collected: true,
      retrainingTrigger,
      impact: await this.calculateFeedbackImpact(modelId, storedFeedback),
    }
  }

  private calculatePerformanceDegradation(
    baseline: PerformanceMetrics,
    current: PerformanceMetrics
  ): PerformanceDegradation {
    const degradation = {}

    for (const metric of ['accuracy', 'precision', 'recall', 'f1']) {
      const baselineValue = baseline[metric]
      const currentValue = current[metric]

      if (baselineValue > 0) {
        degradation[metric] = {
          absolute: baselineValue - currentValue,
          relative: (baselineValue - currentValue) / baselineValue,
          status: this.getDegradationStatus(baselineValue, currentValue),
        }
      }
    }

    return degradation
  }

  private calculatePerformanceStatus(degradation: PerformanceDegradation): PerformanceStatus {
    const severeDegradation = Object.values(degradation).some((d) => d.relative > 0.2) // 20% threshold
    const moderateDegradation = Object.values(degradation).some((d) => d.relative > 0.1) // 10% threshold

    if (severeDegradation) return 'critical'
    if (moderateDegradation) return 'warning'
    return 'healthy'
  }

  private calculateDriftStatus(
    featureDrift: FeatureDrift,
    conceptDrift: ConceptDrift
  ): DriftStatus {
    const severeFeatureDrift = Object.values(featureDrift.featureDrifts).some((d) => d > 0.1)
    const severeConceptDrift = conceptDrift.driftMagnitude > 0.15

    if (severeFeatureDrift || severeConceptDrift) return 'critical'
    if (featureDrift.hasDrift || conceptDrift.hasDrift) return 'warning'
    return 'healthy'
  }

  private calculateBiasStatus(currentMetrics: BiasMetrics): BiasStatus {
    const severeBias = Object.values(currentMetrics.fairnessMetrics).some((m) => m < 0.7) // 70% fairness threshold
    const moderateBias = Object.values(currentMetrics.fairnessMetrics).some((m) => m < 0.8) // 80% fairness threshold

    if (severeBias) return 'critical'
    if (moderateBias) return 'warning'
    return 'healthy'
  }

  private async generatePerformanceInsights(
    current: PerformanceMetrics,
    baseline: PerformanceMetrics,
    trend: PerformanceTrend
  ): Promise<PerformanceInsight[]> {
    const insights = []

    // Performance trend analysis
    if (trend.direction === 'decreasing' && trend.significance > 0.05) {
      insights.push({
        type: 'trend',
        severity: 'high',
        message: 'Performance is significantly decreasing',
        recommendation: 'Consider retraining the model',
        metrics: trend.affectedMetrics,
      })
    }

    // Metric-specific insights
    for (const metric of ['accuracy', 'precision', 'recall', 'f1']) {
      const currentValue = current[metric]
      const baselineValue = baseline[metric]

      if (currentValue < baselineValue * 0.9) {
        // 10% drop
        insights.push({
          type: 'metric_degradation',
          severity: 'medium',
          message: `${metric} has degraded significantly`,
          recommendation: `Investigate ${metric} degradation causes`,
          metric,
          degradation: baselineValue - currentValue,
        })
      }
    }

    return insights
  }

  private async generateDriftInsights(
    featureDrift: FeatureDrift,
    conceptDrift: ConceptDrift,
    trend: DriftTrend
  ): Promise<DriftInsight[]> {
    const insights = []

    // Feature drift insights
    if (featureDrift.hasDrift) {
      insights.push({
        type: 'feature_drift',
        severity: featureDrift.maxDrift > 0.1 ? 'high' : 'medium',
        message: 'Feature drift detected',
        recommendation: 'Update training data or retrain model',
        driftedFeatures: featureDrift.driftedFeatures,
        maxDrift: featureDrift.maxDrift,
      })
    }

    // Concept drift insights
    if (conceptDrift.hasDrift) {
      insights.push({
        type: 'concept_drift',
        severity: conceptDrift.driftMagnitude > 0.15 ? 'high' : 'medium',
        message: 'Concept drift detected',
        recommendation: 'Retrain model with new data',
        driftMagnitude: conceptDrift.driftMagnitude,
        affectedClasses: conceptDrift.affectedClasses,
      })
    }

    return insights
  }

  private async generateBiasInsights(
    current: BiasMetrics,
    baseline: BiasMetrics,
    trend: BiasTrend
  ): Promise<BiasInsight[]> {
    const insights = []

    // Fairness metric insights
    for (const [attribute, metrics] of Object.entries(current.protectedAttributes)) {
      for (const [metric, value] of Object.entries(metrics)) {
        if (value < 0.7) {
          // 70% fairness threshold
          insights.push({
            type: 'fairness_violation',
            severity: value < 0.5 ? 'high' : 'medium',
            message: `Fairness violation detected for ${attribute}`,
            recommendation: 'Apply bias mitigation techniques',
            attribute,
            metric,
            value,
          })
        }
      }
    }

    // Bias trend insights
    if (trend.direction === 'increasing') {
      insights.push({
        type: 'bias_trend',
        severity: 'medium',
        message: 'Bias is increasing over time',
        recommendation: 'Monitor bias trends and consider mitigation',
        trend: trend.direction,
      })
    }

    return insights
  }
}

// Performance Monitor Implementation
export class PerformanceMonitor {
  constructor(
    private metricsCollector: MetricsCollector,
    private database: Database,
    private alertingService: AlertingService
  ) {}

  async setup(config: PerformanceMonitoringConfig): Promise<PerformanceMonitoringSetup> {
    // Initialize metrics collection
    await this.metricsCollector.initialize({
      modelId: config.modelId,
      metrics: config.metrics,
      interval: config.evaluationInterval,
    })

    // Setup alerting
    for (const metric of config.metrics) {
      const threshold = config.thresholds[metric]
      if (threshold) {
        await this.alertingService.setupAlert({
          modelId: config.modelId,
          metric,
          threshold: threshold.min || threshold.max,
          operator: threshold.min ? 'lt' : 'gt',
        })
      }
    }

    return {
      modelId: config.modelId,
      metrics: config.metrics,
      interval: config.evaluationInterval,
      thresholds: config.thresholds,
      status: 'active',
    }
  }

  async getCurrentMetrics(modelId: string): Promise<PerformanceMetrics> {
    const latest = await this.database.query(
      `
      SELECT * FROM model_performance_metrics 
      WHERE model_id = $1 
      ORDER BY timestamp DESC 
      LIMIT 1
    `,
      [modelId]
    )

    if (!latest[0]) {
      throw new Error(`No performance metrics found for model: ${modelId}`)
    }

    return {
      accuracy: latest[0].accuracy,
      precision: latest[0].precision,
      recall: latest[0].recall,
      f1: latest[0].f1,
      latency: latest[0].latency,
      throughput: latest[0].throughput,
      errorRate: latest[0].error_rate,
      timestamp: latest[0].timestamp.getTime(),
    }
  }

  async getBaselineMetrics(modelId: string): Promise<PerformanceMetrics> {
    const baseline = await this.database.query(
      `
      SELECT * FROM model_performance_baseline 
      WHERE model_id = $1
    `,
      [modelId]
    )

    if (!baseline[0]) {
      throw new Error(`No baseline metrics found for model: ${modelId}`)
    }

    return {
      accuracy: baseline[0].accuracy,
      precision: baseline[0].precision,
      recall: baseline[0].recall,
      f1: baseline[0].f1,
      latency: baseline[0].latency,
      throughput: baseline[0].throughput,
      errorRate: baseline[0].error_rate,
      timestamp: baseline[0].created_at.getTime(),
    }
  }

  async getPerformanceTrend(modelId: string, period: string): Promise<PerformanceTrend> {
    const metrics = await this.database.query(
      `
      SELECT * FROM model_performance_metrics 
      WHERE model_id = $1 AND timestamp >= NOW() - INTERVAL '${period}'
      ORDER BY timestamp ASC
    `,
      [modelId]
    )

    const trend = this.calculateTrend(metrics)

    return {
      period,
      direction: trend.direction,
      significance: trend.significance,
      affectedMetrics: trend.affectedMetrics,
      dataPoints: metrics.length,
    }
  }

  private calculateTrend(metrics: any[]): TrendCalculation {
    // Simple linear regression for trend detection
    const trends = {}

    for (const metric of ['accuracy', 'precision', 'recall', 'f1']) {
      const values = metrics.map((m) => m[metric])
      const trend = this.linearRegression(values)
      trends[metric] = trend
    }

    // Determine overall trend
    const decreasingMetrics = Object.entries(trends)
      .filter(([_, trend]) => trend.slope < -0.01)
      .map(([metric, _]) => metric)

    const direction =
      decreasingMetrics.length > Object.keys(trends).length / 2 ? 'decreasing' : 'stable'
    const significance = this.calculateSignificance(trends)

    return {
      direction,
      significance,
      affectedMetrics: decreasingMetrics,
    }
  }

  private linearRegression(values: number[]): { slope: number; intercept: number; r2: number } {
    const n = values.length
    const x = Array.from({ length: n }, (_, i) => i)
    const y = values

    const sumX = x.reduce((a, b) => a + b, 0)
    const sumY = y.reduce((a, b) => a + b, 0)
    const sumXY = x.reduce((a, b, i) => a + b * y[i], 0)
    const sumX2 = x.reduce((a, b) => a + b * b, 0)

    const slope = (n * sumXY - sumX * sumY) / (n * sumX2 - sumX * sumX)
    const intercept = (sumY - slope * sumX) / n

    // Calculate R²
    const yMean = sumY / n
    const ssTotal = y.reduce((a, b) => a + Math.pow(b - yMean, 2), 0)
    const ssResidual = y.reduce((a, b, i) => a + Math.pow(b - (slope * x[i] + intercept), 2), 0)
    const r2 = 1 - ssResidual / ssTotal

    return { slope, intercept, r2 }
  }

  private calculateSignificance(trends: any): number {
    // Simple significance calculation based on R² values
    const r2Values = Object.values(trends).map((t: any) => t.r2)
    return r2Values.reduce((a, b) => a + b, 0) / r2Values.length
  }
}

// Explainability Engine Implementation
export class ExplainabilityEngine {
  constructor(
    private shapExplainer: SHAPExplainer,
    private limeExplainer: LIMEExplainer,
    private permutationExplainer: PermutationImportanceExplainer
  ) {}

  async generateSHAPExplanation(modelId: string, input: ModelInput): Promise<SHAPExplanation> {
    const explanation = await this.shapExplainer.explain(modelId, input)

    return {
      technique: 'shap',
      values: explanation.values,
      baseValue: explanation.baseValue,
      featureNames: explanation.featureNames,
      plot: explanation.plot,
      interpretation: this.interpretSHAPValues(explanation),
    }
  }

  async generateLIMEExplanation(modelId: string, input: ModelInput): Promise<LIMEExplanation> {
    const explanation = await this.limeExplainer.explain(modelId, input)

    return {
      technique: 'lime',
      localExplanation: explanation.localExplanation,
      featureImportance: explanation.featureImportance,
      score: explanation.score,
      interpretation: this.interpretLIMEExplanation(explanation),
    }
  }

  async generatePermutationImportance(
    modelId: string,
    input: ModelInput
  ): Promise<PermutationImportanceExplanation> {
    const explanation = await this.permutationExplainer.explain(modelId, input)

    return {
      technique: 'permutation_importance',
      importances: explanation.importances,
      baselineScore: explanation.baselineScore,
      interpretation: this.interpretPermutationImportance(explanation),
    }
  }

  async generateGlobalExplanation(modelId: string): Promise<GlobalExplanation> {
    // Combine multiple techniques for global explanation
    const shapGlobal = await this.shapExplainer.explainGlobal(modelId)
    const permutationGlobal = await this.permutationExplainer.explainGlobal(modelId)

    return {
      technique: 'global',
      shapSummary: shapGlobal.summary,
      permutationImportance: permutationGlobal.importances,
      featureRanking: this.combineFeatureRankings(shapGlobal, permutationGlobal),
      interpretation: this.interpretGlobalExplanation(shapGlobal, permutationGlobal),
    }
  }

  private interpretSHAPValues(explanation: any): SHAPInterpretation {
    const positiveFeatures = []
    const negativeFeatures = []

    for (let i = 0; i < explanation.values.length; i++) {
      const value = explanation.values[i]
      const featureName = explanation.featureNames[i]

      if (value > 0) {
        positiveFeatures.push({ feature: featureName, contribution: value })
      } else {
        negativeFeatures.push({ feature: featureName, contribution: Math.abs(value) })
      }
    }

    // Sort by contribution magnitude
    positiveFeatures.sort((a, b) => b.contribution - a.contribution)
    negativeFeatures.sort((a, b) => b.contribution - a.contribution)

    return {
      positiveFeatures: positiveFeatures.slice(0, 5),
      negativeFeatures: negativeFeatures.slice(0, 5),
      summary: this.generateSHAPSummary(positiveFeatures, negativeFeatures),
    }
  }

  private interpretLIMEExplanation(explanation: any): LIMEInterpretation {
    const topFeatures = explanation.featureImportance
      .sort((a, b) => Math.abs(b.importance) - Math.abs(a.importance))
      .slice(0, 10)

    return {
      topFeatures,
      localFidelity: explanation.score,
      summary: this.generateLIMESummary(topFeatures),
    }
  }

  private interpretPermutationImportance(explanation: any): PermutationImportanceInterpretation {
    const sortedImportance = explanation.importances.sort((a, b) => b.importance - a.importance)

    return {
      rankedFeatures: sortedImportance,
      topFeatures: sortedImportance.slice(0, 10),
      summary: this.generatePermutationSummary(sortedImportance),
    }
  }

  private interpretGlobalExplanation(shap: any, permutation: any): GlobalInterpretation {
    const combinedRanking = this.combineFeatureRankings(shap, permutation)

    return {
      overallImportance: combinedRanking.slice(0, 20),
      keyInsights: this.generateGlobalInsights(combinedRanking),
      recommendations: this.generateGlobalRecommendations(combinedRanking),
    }
  }

  private combineFeatureRankings(shap: any, permutation: any): FeatureRanking[] {
    const shapRanking = shap.summary.feature_importance
    const permutationRanking = permutation.importances

    // Combine rankings using weighted average
    const combined = {}

    for (const feature of Object.keys(shapRanking)) {
      const shapScore = shapRanking[feature]
      const permutationScore = permutationRanking[feature] || 0

      combined[feature] = shapScore * 0.6 + permutationScore * 0.4
    }

    return Object.entries(combined)
      .sort(([, a], [, b]) => b - a)
      .map(([feature, score]) => ({ feature, score }))
  }
}

// Bias Monitor Implementation
export class BiasMonitor {
  constructor(
    private fairnessCalculator: FairnessCalculator,
    private database: Database,
    private alertingService: AlertingService
  ) {}

  async setup(config: BiasMonitoringConfig): Promise<BiasMonitoringSetup> {
    // Initialize fairness calculation
    await this.fairnessCalculator.initialize({
      modelId: config.modelId,
      protectedAttributes: config.protectedAttributes,
      fairnessMetrics: config.fairnessMetrics,
    })

    // Setup bias alerts
    for (const attribute of config.protectedAttributes) {
      for (const metric of config.fairnessMetrics) {
        await this.alertingService.setupAlert({
          modelId: config.modelId,
          metric: `bias_${attribute}_${metric}`,
          threshold: 0.7, // 70% fairness threshold
          operator: 'lt',
        })
      }
    }

    return {
      modelId: config.modelId,
      protectedAttributes: config.protectedAttributes,
      fairnessMetrics: config.fairnessMetrics,
      evaluationInterval: config.evaluationInterval,
      status: 'active',
    }
  }

  async getCurrentMetrics(modelId: string): Promise<BiasMetrics> {
    const latest = await this.database.query(
      `
      SELECT * FROM model_bias_metrics 
      WHERE model_id = $1 
      ORDER BY timestamp DESC 
      LIMIT 1
    `,
      [modelId]
    )

    if (!latest[0]) {
      throw new Error(`No bias metrics found for model: ${modelId}`)
    }

    return {
      protectedAttributes: latest[0].protected_attributes,
      fairnessMetrics: latest[0].fairness_metrics,
      timestamp: latest[0].timestamp.getTime(),
    }
  }

  async calculateBiasMetrics(modelId: string, predictions: PredictionData): Promise<BiasMetrics> {
    const metrics = {}

    for (const attribute of predictions.protectedAttributes) {
      metrics[attribute] = {}

      for (const metric of ['demographic_parity', 'equal_opportunity', 'equalized_odds']) {
        const fairness = await this.fairnessCalculator.calculateFairness(
          predictions,
          attribute,
          metric
        )
        metrics[attribute][metric] = fairness.score
      }
    }

    return {
      protectedAttributes: Object.keys(metrics),
      fairnessMetrics: metrics,
      timestamp: Date.now(),
    }
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No model monitoring or explainability
export class BasicModelService {
  // BAD: No performance monitoring
  async predict(data: any) {
    // BAD: No bias detection
    // BAD: No explainability
    // BAD: No drift detection
    const model = await this.loadModel()
    return model.predict(data)
  }

  // BAD: No monitoring setup
  // BAD: No alerting
  // BAD: No feedback collection
}
```

</example_bad>
