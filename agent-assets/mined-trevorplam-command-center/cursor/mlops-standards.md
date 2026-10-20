---
description: Run MLOps and Production Machine Learning Standards Check
globs: ["**/ml/**/*.ts", "**/mlops/**/*.ts", "**/model-serving/**/*.ts", "**/model-training/**/*.ts"]
---
# AI/ML: MLOps & Production Machine Learning Standards

<audit_rules>
- You MUST implement proper model versioning and registry for all ML models in production.
- You MUST implement proper data validation and preprocessing pipelines with feature stores.
- You MUST implement proper model monitoring for performance drift and data drift detection.
- You MUST implement proper A/B testing and canary deployments for model rollouts.
- You MUST implement proper model explainability and interpretability for compliance.
- You MUST implement proper training pipeline automation with reproducible builds.
- You MUST implement proper model serving with autoscaling and load balancing.
- You MUST implement proper data privacy and bias detection in ML pipelines.
- You MUST implement proper model rollback and disaster recovery procedures.
- You MUST implement proper cost management for ML infrastructure and model serving.
</audit_rules>

<example_good>
```typescript
// MLOps Implementation
import { z } from 'zod';
import { ModelRegistry } from './model-registry';
import { FeatureStore } from './feature-store';
import { ModelMonitor } from './model-monitor';
import { ModelServing } from './model-serving';

// Model Versioning and Registry
export class ProductionMLSystem {
  constructor(
    private modelRegistry: ModelRegistry,
    private featureStore: FeatureStore,
    private modelMonitor: ModelMonitor,
    private modelServing: ModelServing,
    private dataValidator: DataValidator,
    private biasDetector: BiasDetector
  ) {}

  // Training pipeline automation with reproducible builds
  async trainModel(trainingConfig: TrainingConfig): Promise<ModelTrainingResult> {
    // Validate training configuration
    const validatedConfig = await this.validateTrainingConfig(trainingConfig);
    
    // Create reproducible training environment
    const trainingEnv = await this.createTrainingEnvironment(validatedConfig);
    
    // Validate training data
    const dataValidation = await this.dataValidator.validateTrainingData(validatedConfig.dataPath);
    if (!dataValidation.valid) {
      throw new Error(`Training data validation failed: ${dataValidation.issues.join(', ')}`);
    }

    // Check for bias in training data
    const biasCheck = await this.biasDetector.analyzeTrainingData(validatedConfig.dataPath);
    if (biasCheck.hasBias) {
      throw new Error(`Bias detected in training data: ${biasCheck.issues.join(', ')}`);
    }

    // Execute training with reproducible pipeline
    const trainingResult = await this.executeTraining(trainingEnv, validatedConfig);
    
    // Register model with versioning
    const modelVersion = await this.modelRegistry.registerModel({
      modelId: trainingResult.modelId,
      version: trainingResult.version,
      metadata: {
        trainingConfig: validatedConfig,
        trainingEnv: trainingEnv,
        metrics: trainingResult.metrics,
        dataValidation,
        biasCheck,
        timestamp: new Date(),
      },
    });

    // Set up monitoring for new model
    await this.modelMonitor.setupMonitoring(modelVersion);

    return {
      modelVersion,
      trainingResult,
      dataValidation,
      biasCheck,
    };
  }

  // Model deployment with A/B testing
  async deployModel(deploymentConfig: ModelDeploymentConfig): Promise<DeploymentResult> {
    // Validate deployment configuration
    const validatedConfig = await this.validateDeploymentConfig(deploymentConfig);
    
    // Get model from registry
    const model = await this.modelRegistry.getModel(validatedConfig.modelId, validatedConfig.version);
    if (!model) {
      throw new Error(`Model not found: ${validatedConfig.modelId}:${validatedConfig.version}`);
    }

    // Setup A/B testing if enabled
    if (validatedConfig.abTesting) {
      return await this.deployWithABTesting(model, validatedConfig);
    }

    // Canary deployment
    if (validatedConfig.canary) {
      return await this.deployCanary(model, validatedConfig);
    }

    // Full deployment
    return await this.deployFull(model, validatedConfig);
  }

  // Model monitoring and drift detection
  async monitorModel(modelId: string, version: string): Promise<ModelMonitoringReport> {
    // Get current model metrics
    const currentMetrics = await this.modelMonitor.getCurrentMetrics(modelId, version);
    
    // Get baseline metrics
    const baselineMetrics = await this.modelMonitor.getBaselineMetrics(modelId, version);
    
    // Detect performance drift
    const performanceDrift = await this.detectPerformanceDrift(currentMetrics, baselineMetrics);
    
    // Detect data drift
    const dataDrift = await this.detectDataDrift(modelId, version);
    
    // Check model explainability
    const explainabilityReport = await this.generateExplainabilityReport(modelId, version);
    
    // Check for bias in predictions
    const biasReport = await this.biasDetector.analyzePredictions(modelId, version);

    return {
      modelId,
      version,
      timestamp: new Date(),
      currentMetrics,
      baselineMetrics,
      performanceDrift,
      dataDrift,
      explainabilityReport,
      biasReport,
      recommendations: this.generateMonitoringRecommendations({
        performanceDrift,
        dataDrift,
        explainabilityReport,
        biasReport,
      }),
    };
  }

  // Model rollback and disaster recovery
  async rollbackModel(modelId: string, fromVersion: string, toVersion: string): Promise<RollbackResult> {
    // Validate rollback request
    const validation = await this.validateRollbackRequest(modelId, fromVersion, toVersion);
    if (!validation.valid) {
      throw new Error(`Rollback validation failed: ${validation.issues.join(', ')}`);
    }

    // Get target model
    const targetModel = await this.modelRegistry.getModel(modelId, toVersion);
    if (!targetModel) {
      throw new Error(`Target model not found: ${modelId}:${toVersion}`);
    }

    // Perform rollback
    const rollbackResult = await this.modelServing.rollbackModel({
      modelId,
      fromVersion,
      toVersion,
      targetModel,
    });

    // Update monitoring
    await this.modelMonitor.switchMonitoring(modelId, fromVersion, toVersion);

    return rollbackResult;
  }

  private async deployWithABTesting(model: Model, config: ValidatedDeploymentConfig): Promise<DeploymentResult> {
    // Create A/B test configuration
    const abConfig = {
      modelA: model,
      modelB: await this.modelRegistry.getModel(config.modelId, config.compareVersion),
      trafficSplit: config.trafficSplit || { modelA: 0.5, modelB: 0.5 },
      metrics: config.metrics || ['accuracy', 'latency', 'cost'],
      duration: config.abDuration || 7 * 24 * 60 * 60 * 1000, // 7 days
    };

    // Deploy both models
    const deploymentA = await this.modelServing.deployModel({
      model: abConfig.modelA,
      endpoint: `${config.endpoint}-A`,
      traffic: abConfig.trafficSplit.modelA,
    });

    const deploymentB = await this.modelServing.deployModel({
      model: abConfig.modelB,
      endpoint: `${config.endpoint}-B`,
      traffic: abConfig.trafficSplit.modelB,
    });

    // Setup A/B testing monitoring
    await this.modelMonitor.setupABTesting(abConfig);

    return {
      deploymentId: generateId(),
      type: 'ab-testing',
      modelA: deploymentA,
      modelB: deploymentB,
      abConfig,
      status: 'active',
    };
  }

  private async deployCanary(model: Model, config: ValidatedDeploymentConfig): Promise<DeploymentResult> {
    // Deploy canary with small traffic percentage
    const canaryDeployment = await this.modelServing.deployModel({
      model,
      endpoint: config.endpoint,
      traffic: config.canaryTraffic || 0.1, // 10% traffic
      canary: true,
    });

    // Keep existing model for majority of traffic
    const stableDeployment = await this.modelServing.deployModel({
      model: await this.modelRegistry.getModel(config.modelId, config.stableVersion),
      endpoint: config.endpoint,
      traffic: 0.9, // 90% traffic
      stable: true,
    });

    // Setup canary monitoring
    await this.modelMonitor.setupCanaryMonitoring(canaryDeployment, stableDeployment);

    return {
      deploymentId: generateId(),
      type: 'canary',
      canary: canaryDeployment,
      stable: stableDeployment,
      status: 'monitoring',
    };
  }

  private detectPerformanceDrift(current: ModelMetrics, baseline: ModelMetrics): PerformanceDrift {
    const drift = {};
    
    for (const metric of ['accuracy', 'precision', 'recall', 'f1', 'latency', 'throughput']) {
      const currentValue = current[metric];
      const baselineValue = baseline[metric];
      
      if (currentValue && baselineValue) {
        const driftAmount = Math.abs(currentValue - baselineValue) / baselineValue;
        drift[metric] = {
          current: currentValue,
          baseline: baselineValue,
          drift: driftAmount,
          significant: driftAmount > 0.05, // 5% threshold
        };
      }
    }

    return {
      hasDrift: Object.values(drift).some(d => d.significant),
      metrics: drift,
      overallDrift: this.calculateOverallDrift(drift),
    };
  }

  private detectDataDrift(modelId: string, version: string): DataDrift {
    // Implement data drift detection using statistical tests
    // This would compare current data distribution with training data distribution
    return {
      hasDrift: false, // Placeholder
      driftScore: 0.0,
      features: {},
    };
  }

  private generateExplainabilityReport(modelId: string, version: string): ExplainabilityReport {
    // Generate model explainability report using SHAP, LIME, or similar
    return {
      modelId,
      version,
      explainability: 'high',
      methods: ['shap', 'lime'],
      featureImportance: {}, // Placeholder
      timestamp: new Date(),
    };
  }

  private generateMonitoringRecommendations(analysis: MonitoringAnalysis): string[] {
    const recommendations = [];

    if (analysis.performanceDrift.hasDrift) {
      recommendations.push('Consider retraining model due to performance drift');
    }

    if (analysis.dataDrift.hasDrift) {
      recommendations.push('Update training data due to data drift');
    }

    if (analysis.explainabilityReport.explainability === 'low') {
      recommendations.push('Improve model explainability for compliance');
    }

    if (analysis.biasReport.hasBias) {
      recommendations.push('Address bias issues in model predictions');
    }

    return recommendations;
  }
}

// Model Registry Implementation
export class ModelRegistry {
  constructor(private db: Database) {}

  async registerModel(model: ModelRegistration): Promise<ModelVersion> {
    const version = {
      id: generateId(),
      modelId: model.modelId,
      version: model.version,
      metadata: model.metadata,
      createdAt: new Date(),
      status: 'registered',
    };

    await this.db.modelVersion.create({ data: version });
    return version;
  }

  async getModel(modelId: string, version: string): Promise<Model | null> {
    const modelVersion = await this.db.modelVersion.findFirst({
      where: { modelId, version },
      include: { model: true },
    });

    return modelVersion?.model || null;
  }

  async listModels(modelId: string): Promise<ModelVersion[]> {
    return await this.db.modelVersion.findMany({
      where: { modelId },
      orderBy: { createdAt: 'desc' },
    });
  }
}

// Feature Store Implementation
export class FeatureStore {
  constructor(redis: Redis) {
    this.redis = redis;
  }

  async getFeatures(featureIds: string[]): Promise<Record<string, any>> {
    const features = {};
    
    for (const featureId of featureIds) {
      const value = await this.redis.get(`feature:${featureId}`);
      if (value) {
        features[featureId] = JSON.parse(value);
      }
    }

    return features;
  }

  async storeFeatures(features: Record<string, any>): Promise<void> {
    for (const [featureId, value] of Object.entries(features)) {
      await this.redis.setex(
        `feature:${featureId}`,
        3600, // 1 hour TTL
        JSON.stringify(value)
      );
    }
  }
}

// Model Monitor Implementation
export class ModelMonitor {
  constructor(
    private metrics: MetricsService,
    private alerting: AlertingService
  ) {}

  async setupMonitoring(modelVersion: ModelVersion): Promise<void> {
    // Setup metrics collection
    await this.metrics.createDashboard({
      modelId: modelVersion.modelId,
      version: modelVersion.version,
      metrics: ['accuracy', 'precision', 'recall', 'f1', 'latency', 'throughput'],
    });

    // Setup alerts
    await this.alerting.createRules({
      modelId: modelVersion.modelId,
      version: modelVersion.version,
      rules: [
        { metric: 'accuracy', threshold: 0.8, operator: 'lt' },
        { metric: 'latency', threshold: 1000, operator: 'gt' },
        { metric: 'error_rate', threshold: 0.05, operator: 'gt' },
      ],
    });
  }

  async getCurrentMetrics(modelId: string, version: string): Promise<ModelMetrics> {
    return await this.metrics.getCurrentMetrics(modelId, version);
  }

  async getBaselineMetrics(modelId: string, version: string): Promise<ModelMetrics> {
    return await this.metrics.getBaselineMetrics(modelId, version);
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No MLOps practices
export class BasicMLService {
  // BAD: No model versioning
  async trainModel(data: any): Promise<any> {
    // BAD: No reproducible training environment
    const model = this.train(data);
    return model;
  }

  // BAD: No monitoring
  async predict(input: any): Promise<any> {
    // BAD: No drift detection
    // BAD: No explainability
    return this.model.predict(input);
  }

  // BAD: No A/B testing
  async deployModel(model: any): Promise<void> {
    // BAD: Direct deployment without testing
    this.deploy(model);
  }

  // BAD: No rollback mechanism
  // BAD: No cost management
  // BAD: No bias detection
}
```
</example_bad>
