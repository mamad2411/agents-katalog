---
description: Run MLOps and Production Machine Learning Standards Check
globs: ['**/ml/**/*.ts', '**/models/**/*.ts', '**/training/**/*.ts', '**/inference/**/*.ts']
---

# AI/ML: MLOps & Production Machine Learning Standards

<audit_rules>

- You MUST implement proper model versioning and registry for all ML models in production.
- You MUST ensure proper data validation and preprocessing pipelines with feature stores.
- You MUST implement proper model monitoring for performance drift and data drift detection.
- You MUST configure proper A/B testing and canary deployments for model rollouts.
- You MUST ensure proper model explainability and interpretability for compliance.
- You MUST implement proper training pipeline automation with reproducible builds.
- You MUST configure proper model serving with autoscaling and load balancing.
- You MUST ensure proper data privacy and bias detection in ML pipelines.
- You MUST implement proper model rollback and disaster recovery procedures.
- You MUST configure proper cost management for ML infrastructure and model serving.
  </audit_rules>

<example_good>

```typescript
// MLOps Implementation

export class MLOpsOrchestrator {
  constructor(
    private modelRegistry: ModelRegistry,
    private featureStore: FeatureStore,
    private modelMonitor: ModelMonitor,
    private deploymentManager: ModelDeploymentManager,
    private dataValidator: DataValidator,
    private biasDetector: BiasDetector
  ) {}

  async deployModel(modelConfig: ModelDeploymentConfig): Promise<ModelDeployment> {
    // Validate model configuration
    await this.validateModelConfig(modelConfig)

    // Register model version
    const modelVersion = await this.modelRegistry.registerModel({
      name: modelConfig.modelName,
      version: modelConfig.version,
      framework: modelConfig.framework,
      artifacts: modelConfig.artifacts,
      metadata: modelConfig.metadata,
    })

    // Validate training data
    const dataValidation = await this.dataValidator.validateTrainingData(modelConfig.trainingData)
    if (!dataValidation.isValid) {
      throw new Error(`Training data validation failed: ${dataValidation.issues.join(', ')}`)
    }

    // Check for bias in training data
    const biasAnalysis = await this.biasDetector.analyzeTrainingData(modelConfig.trainingData)
    if (biasAnalysis.hasBias) {
      await this.handleBiasDetection(biasAnalysis)
    }

    // Setup feature store
    const featureConfig = await this.setupFeatureStore(modelConfig.features)

    // Deploy model with canary strategy
    const deployment = await this.deploymentManager.deploy({
      modelVersion,
      strategy: modelConfig.deploymentStrategy || 'canary',
      traffic: modelConfig.trafficSplit || { canary: 0.1, stable: 0.9 },
      monitoring: {
        performanceMetrics: modelConfig.performanceMetrics,
        dataDriftDetection: true,
        biasMonitoring: true,
      },
    })

    // Setup monitoring
    await this.setupModelMonitoring(deployment, modelConfig)

    return deployment
  }

  async monitorModelPerformance(deploymentId: string): Promise<ModelPerformanceReport> {
    const deployment = await this.deploymentManager.getDeployment(deploymentId)

    // Get performance metrics
    const performance = await this.modelMonitor.getPerformanceMetrics(deploymentId)

    // Check for performance drift
    const driftAnalysis = await this.modelMonitor.analyzePerformanceDrift(deploymentId, performance)

    // Check for data drift
    const dataDrift = await this.modelMonitor.analyzeDataDrift(deploymentId)

    // Check for bias drift
    const biasDrift = await this.biasDetector.analyzeInferenceBias(deploymentId)

    // Generate recommendations
    const recommendations = await this.generateRecommendations({
      performance,
      driftAnalysis,
      dataDrift,
      biasDrift,
    })

    return {
      deploymentId,
      timestamp: Date.now(),
      performance,
      driftAnalysis,
      dataDrift,
      biasDrift,
      recommendations,
      status: this.calculateModelStatus(performance, driftAnalysis, dataDrift, biasDrift),
    }
  }

  async retrainModel(deploymentId: string, trigger: RetrainingTrigger): Promise<ModelRetraining> {
    const deployment = await this.deploymentManager.getDeployment(deploymentId)

    // Collect new training data
    const trainingData = await this.collectRetrainingData(deployment, trigger)

    // Validate new data
    const dataValidation = await this.dataValidator.validateTrainingData(trainingData)
    if (!dataValidation.isValid) {
      throw new Error(`Retraining data validation failed: ${dataValidation.issues.join(', ')}`)
    }

    // Setup training pipeline
    const trainingPipeline = await this.setupTrainingPipeline({
      modelConfig: deployment.modelConfig,
      trainingData,
      hyperparameters: await this.optimizeHyperparameters(deployment.modelConfig, trainingData),
    })

    // Execute training
    const trainingResult = await this.executeTraining(trainingPipeline)

    // Validate new model
    const modelValidation = await this.validateTrainedModel(
      trainingResult,
      deployment.baselineMetrics
    )

    if (modelValidation.isValid) {
      // Deploy new model
      const newDeployment = await this.deployModel({
        ...deployment.modelConfig,
        version: trainingResult.modelVersion,
        artifacts: trainingResult.artifacts,
        metadata: {
          ...deployment.modelConfig.metadata,
          retrainingTrigger: trigger,
          parentVersion: deployment.modelVersion,
        },
      })

      // Gradual traffic shift
      await this.gradualTrafficShift(deploymentId, newDeployment.id)

      return {
        success: true,
        newDeploymentId: newDeployment.id,
        modelVersion: trainingResult.modelVersion,
        performance: modelValidation.performance,
        improvement: this.calculateImprovement(
          deployment.baselineMetrics,
          modelValidation.performance
        ),
      }
    } else {
      return {
        success: false,
        reasons: modelValidation.issues,
      }
    }
  }

  private async setupFeatureStore(features: FeatureConfig[]): Promise<FeatureStoreConfig> {
    const featureDefinitions = features.map((feature) => ({
      name: feature.name,
      type: feature.type,
      transformation: feature.transformation,
      validation: feature.validation,
      freshness: feature.freshness,
      source: feature.source,
    }))

    return {
      features: featureDefinitions,
      store: 'online', // or 'offline' for batch features
      ttl: 3600, // 1 hour
      monitoring: true,
    }
  }

  private async setupModelMonitoring(
    deployment: ModelDeployment,
    config: ModelDeploymentConfig
  ): Promise<void> {
    // Setup performance monitoring
    await this.modelMonitor.setupPerformanceMonitoring(deployment.id, {
      metrics: config.performanceMetrics || ['accuracy', 'precision', 'recall', 'f1'],
      threshold: config.performanceThreshold || 0.8,
      evaluationInterval: config.evaluationInterval || 300000, // 5 minutes
    })

    // Setup data drift monitoring
    await this.modelMonitor.setupDataDriftMonitoring(deployment.id, {
      referenceData: config.referenceData,
      driftThreshold: config.driftThreshold || 0.05,
      features: config.driftFeatures || ['all'],
    })

    // Setup bias monitoring
    await this.biasDetector.setupBiasMonitoring(deployment.id, {
      protectedAttributes: config.protectedAttributes || [],
      fairnessMetrics: config.fairnessMetrics || ['demographic_parity', 'equal_opportunity'],
    })
  }

  private async generateRecommendations(analysis: ModelAnalysis): Promise<Recommendation[]> {
    const recommendations = []

    // Performance recommendations
    if (analysis.performance.accuracy < 0.8) {
      recommendations.push({
        type: 'performance',
        priority: 'high',
        action: 'retrain',
        reason: 'Model accuracy below threshold',
        details: `Current accuracy: ${analysis.performance.accuracy}`,
      })
    }

    // Drift recommendations
    if (analysis.driftAnalysis.hasDrift) {
      recommendations.push({
        type: 'drift',
        priority: 'medium',
        action: 'retrain',
        reason: 'Performance drift detected',
        details: `Drift magnitude: ${analysis.driftAnalysis.driftMagnitude}`,
      })
    }

    // Data drift recommendations
    if (analysis.dataDrift.hasDrift) {
      recommendations.push({
        type: 'data_drift',
        priority: 'medium',
        action: 'retrain',
        reason: 'Data drift detected',
        details: `Drifted features: ${analysis.dataDrift.driftedFeatures.join(', ')}`,
      })
    }

    // Bias recommendations
    if (analysis.biasDrift.hasBias) {
      recommendations.push({
        type: 'bias',
        priority: 'high',
        action: 'investigate',
        reason: 'Bias detected in model predictions',
        details: `Biased attributes: ${analysis.biasDrift.biasedAttributes.join(', ')}`,
      })
    }

    return recommendations
  }

  private calculateModelStatus(
    performance: PerformanceMetrics,
    driftAnalysis: DriftAnalysis,
    dataDrift: DataDrift,
    biasDrift: BiasDrift
  ): ModelStatus {
    if (biasDrift.hasBias) return 'critical'
    if (performance.accuracy < 0.7) return 'critical'
    if (driftAnalysis.hasDrift || dataDrift.hasDrift) return 'warning'
    if (performance.accuracy < 0.8) return 'warning'
    return 'healthy'
  }
}

// Model Registry Implementation
export class ModelRegistry {
  constructor(
    private database: Database,
    private storage: StorageService
  ) {}

  async registerModel(model: ModelRegistration): Promise<ModelVersion> {
    // Validate model artifacts
    await this.validateModelArtifacts(model.artifacts)

    // Store model artifacts
    const artifactPaths = await this.storeArtifacts(model.artifacts)

    // Register model in database
    const modelVersion = await this.database.query(
      `
      INSERT INTO model_versions (name, version, framework, artifacts, metadata, created_at)
      VALUES ($1, $2, $3, $4, $5, NOW())
      RETURNING *
    `,
      [
        model.name,
        model.version,
        model.framework,
        JSON.stringify(artifactPaths),
        JSON.stringify(model.metadata),
      ]
    )

    return {
      id: modelVersion.id,
      name: model.name,
      version: model.version,
      framework: model.framework,
      artifacts: artifactPaths,
      metadata: model.metadata,
      createdAt: modelVersion.created_at,
    }
  }

  async getModel(modelName: string, version?: string): Promise<ModelVersion> {
    const query = version
      ? 'SELECT * FROM model_versions WHERE name = $1 AND version = $2'
      : 'SELECT * FROM model_versions WHERE name = $1 ORDER BY version DESC LIMIT 1'

    const params = version ? [modelName, version] : [modelName]
    const result = await this.database.query(query, params)

    if (!result[0]) {
      throw new Error(`Model not found: ${modelName}${version ? ` v${version}` : ''}`)
    }

    return {
      id: result[0].id,
      name: result[0].name,
      version: result[0].version,
      framework: result[0].framework,
      artifacts: JSON.parse(result[0].artifacts),
      metadata: JSON.parse(result[0].metadata),
      createdAt: result[0].created_at,
    }
  }

  private async validateModelArtifacts(artifacts: ModelArtifacts): Promise<void> {
    // Validate model file exists and is valid
    if (!artifacts.modelFile) {
      throw new Error('Model file is required')
    }

    // Validate model format
    const validFormats = ['pickle', 'onnx', 'tensorflow', 'pytorch']
    if (!validFormats.includes(artifacts.format)) {
      throw new Error(`Invalid model format: ${artifacts.format}`)
    }

    // Validate preprocessing code
    if (artifacts.preprocessingCode) {
      await this.validatePreprocessingCode(artifacts.preprocessingCode)
    }
  }

  private async storeArtifacts(artifacts: ModelArtifacts): Promise<StoredArtifacts> {
    const stored = {}

    // Store model file
    if (artifacts.modelFile) {
      stored.modelFile = await this.storage.storeFile(artifacts.modelFile, 'models')
    }

    // Store preprocessing code
    if (artifacts.preprocessingCode) {
      stored.preprocessingCode = await this.storage.storeFile(
        artifacts.preprocessingCode,
        'preprocessing'
      )
    }

    // Store configuration
    if (artifacts.config) {
      stored.config = await this.storage.storeFile(artifacts.config, 'configs')
    }

    return stored
  }
}

// Feature Store Implementation
export class FeatureStore {
  constructor(
    private onlineStore: OnlineFeatureStore,
    private offlineStore: OfflineFeatureStore,
    private featureRegistry: FeatureRegistry
  ) {}

  async getFeatures(entityId: string, featureNames: string[]): Promise<FeatureValues> {
    const features = {}

    for (const featureName of featureNames) {
      const feature = await this.featureRegistry.getFeature(featureName)

      if (feature.store === 'online') {
        features[featureName] = await this.onlineStore.getFeature(entityId, featureName)
      } else {
        features[featureName] = await this.offlineStore.getFeature(entityId, featureName)
      }
    }

    return features
  }

  async ingestFeatures(features: FeatureData[]): Promise<void> {
    const onlineFeatures = features.filter((f) => f.store === 'online')
    const offlineFeatures = features.filter((f) => f.store === 'offline')

    // Ingest to online store
    if (onlineFeatures.length > 0) {
      await this.onlineStore.ingestFeatures(onlineFeatures)
    }

    // Ingest to offline store
    if (offlineFeatures.length > 0) {
      await this.offlineStore.ingestFeatures(offlineFeatures)
    }
  }

  async createFeature(feature: FeatureDefinition): Promise<void> {
    // Validate feature definition
    await this.validateFeatureDefinition(feature)

    // Register feature
    await this.featureRegistry.registerFeature(feature)

    // Create tables/stores if needed
    if (feature.store === 'online') {
      await this.onlineStore.createFeatureTable(feature)
    } else {
      await this.offlineStore.createFeatureTable(feature)
    }
  }

  private async validateFeatureDefinition(feature: FeatureDefinition): Promise<void> {
    // Validate feature name
    if (!feature.name || feature.name.length === 0) {
      throw new Error('Feature name is required')
    }

    // Validate feature type
    const validTypes = ['numerical', 'categorical', 'text', 'boolean']
    if (!validTypes.includes(feature.type)) {
      throw new Error(`Invalid feature type: ${feature.type}`)
    }

    // Validate transformation
    if (feature.transformation) {
      await this.validateTransformation(feature.transformation)
    }
  }
}

// Model Monitor Implementation
export class ModelMonitor {
  constructor(
    private metricsCollector: MetricsCollector,
    private alertingService: AlertingService,
    private driftDetector: DriftDetector
  ) {}

  async setupPerformanceMonitoring(
    deploymentId: string,
    config: PerformanceMonitoringConfig
  ): Promise<void> {
    await this.metricsCollector.setupMetricsCollection(deploymentId, {
      metrics: config.metrics,
      interval: config.evaluationInterval,
      threshold: config.threshold,
    })

    await this.alertingService.setupAlerts(deploymentId, {
      type: 'performance',
      threshold: config.threshold,
      channels: ['email', 'slack'],
    })
  }

  async getPerformanceMetrics(deploymentId: string): Promise<PerformanceMetrics> {
    const metrics = await this.metricsCollector.getMetrics(deploymentId)

    return {
      accuracy: metrics.accuracy,
      precision: metrics.precision,
      recall: metrics.recall,
      f1: metrics.f1,
      latency: metrics.latency,
      throughput: metrics.throughput,
      errorRate: metrics.errorRate,
      timestamp: Date.now(),
    }
  }

  async analyzePerformanceDrift(
    deploymentId: string,
    currentMetrics: PerformanceMetrics
  ): Promise<DriftAnalysis> {
    // Get baseline metrics
    const baseline = await this.getBaselineMetrics(deploymentId)

    // Calculate drift
    const driftMagnitude = this.calculateDriftMagnitude(baseline, currentMetrics)

    return {
      hasDrift: driftMagnitude > 0.1, // 10% drift threshold
      driftMagnitude,
      driftedMetrics: this.getDriftedMetrics(baseline, currentMetrics),
      baseline,
      current: currentMetrics,
    }
  }

  async analyzeDataDrift(deploymentId: string): Promise<DataDrift> {
    // Get current feature statistics
    const currentStats = await this.getCurrentFeatureStatistics(deploymentId)

    // Get reference statistics
    const referenceStats = await this.getReferenceFeatureStatistics(deploymentId)

    // Calculate drift for each feature
    const featureDrifts = {}
    let hasDrift = false
    let maxDrift = 0

    for (const [featureName, currentStat] of Object.entries(currentStats)) {
      const referenceStat = referenceStats[featureName]
      if (referenceStat) {
        const drift = this.calculateFeatureDrift(currentStat, referenceStat)
        featureDrifts[featureName] = drift
        hasDrift = hasDrift || drift > 0.05 // 5% drift threshold
        maxDrift = Math.max(maxDrift, drift)
      }
    }

    return {
      hasDrift,
      maxDrift,
      driftedFeatures: Object.entries(featureDrifts)
        .filter(([_, drift]) => drift > 0.05)
        .map(([name, _]) => name),
      featureDrifts,
    }
  }

  private calculateDriftMagnitude(
    baseline: PerformanceMetrics,
    current: PerformanceMetrics
  ): number {
    const drifts = [
      Math.abs(baseline.accuracy - current.accuracy) / baseline.accuracy,
      Math.abs(baseline.precision - current.precision) / baseline.precision,
      Math.abs(baseline.recall - current.recall) / baseline.recall,
      Math.abs(baseline.f1 - current.f1) / baseline.f1,
    ]

    return drifts.reduce((sum, drift) => sum + drift, 0) / drifts.length
  }

  private calculateFeatureDrift(current: FeatureStatistics, reference: FeatureStatistics): number {
    // Use Population Stability Index (PSI) for drift calculation
    return this.calculatePSI(current.distribution, reference.distribution)
  }

  private calculatePSI(current: Distribution, reference: Distribution): number {
    // PSI calculation implementation
    const bins = this.createBins(current, reference)
    let psi = 0

    for (const bin of bins) {
      const currentPercent = bin.currentCount / current.total
      const referencePercent = bin.referenceCount / reference.total

      if (referencePercent > 0) {
        const ratio = currentPercent / referencePercent
        psi += (currentPercent - referencePercent) * Math.log(ratio)
      }
    }

    return psi
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No MLOps practices
export class BasicMLService {
  // BAD: No model versioning
  async predict(data: any) {
    // BAD: No feature store
    // BAD: No monitoring
    // BAD: No drift detection
    const model = await this.loadModel()
    return model.predict(data)
  }

  // BAD: No model registry
  // BAD: No A/B testing
  // BAD: No bias detection
  // BAD: No explainability
}
```

</example_bad>
