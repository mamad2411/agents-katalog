---
description: Run Edge AI and On-Device Machine Learning Standards Check
globs: ["**/edge-ai/**/*.ts", "**/on-device-ml/**/*.ts", "**/tinyml/**/*.ts", "**/edge-inference/**/*.ts"]
---
# IoT: Edge AI & On-Device Machine Learning Standards

<audit_rules>
- You MUST implement proper model optimization for edge devices with quantization and pruning.
- You MUST ensure proper on-device inference with memory and compute constraints.
- You MUST implement proper federated learning with privacy-preserving aggregation.
- You MUST configure proper model update mechanisms with delta updates and compression.
- You MUST ensure proper edge-to-cloud coordination with fallback mechanisms.
- You MUST implement proper on-device data preprocessing and feature extraction.
- You MUST configure proper model monitoring and performance optimization on edge devices.
- You MUST ensure proper edge AI security with model protection and secure inference.
- You MUST implement proper edge AI lifecycle management and version control.
- You MUST ensure proper resource management and power optimization for edge AI.
</audit_rules>

<example_good>
```typescript
// Edge AI Implementation

export class EdgeAIManager {
  constructor(
    private modelOptimizer: EdgeModelOptimizer,
    private inferenceEngine: EdgeInferenceEngine,
    private federatedLearning: FederatedLearningEngine,
    private modelUpdater: EdgeModelUpdater,
    private resourceManager: EdgeResourceManager,
    private securityManager: EdgeSecurityManager
  ) {}

  async deployEdgeModel(deployment: EdgeModelDeployment): Promise<EdgeModelDeploymentResult> {
    // Validate deployment requirements
    const validation = await this.validateDeployment(deployment);
    if (!validation.valid) {
      throw new Error(`Invalid deployment: ${validation.errors.join(', ')}`);
    }

    // Optimize model for edge device
    const optimizedModel = await this.modelOptimizer.optimizeForEdge(deployment.model, {
      targetDevice: deployment.deviceId,
      constraints: deployment.constraints,
      optimizationLevel: deployment.optimizationLevel || 'high',
    });

    // Validate optimized model
    const modelValidation = await this.validateOptimizedModel(optimizedModel, deployment);
    if (!modelValidation.valid) {
      throw new Error(`Model validation failed: ${modelValidation.errors.join(', ')}`);
    }

    // Deploy model to edge device
    const deploymentResult = await this.deployToDevice(deployment.deviceId, optimizedModel);

    // Setup inference engine
    const inferenceSetup = await this.inferenceEngine.setup({
      deviceId: deployment.deviceId,
      model: optimizedModel,
      configuration: deployment.inferenceConfig,
    });

    // Configure monitoring
    const monitoringConfig = await this.setupModelMonitoring(deployment.deviceId, optimizedModel);

    return {
      deploymentId: deploymentResult.id,
      deviceId: deployment.deviceId,
      modelId: optimizedModel.id,
      modelSize: optimizedModel.size,
      inferenceSetup,
      monitoringConfig,
      deploymentTimestamp: Date.now(),
    };
  }

  async runInference(request: EdgeInferenceRequest): Promise<EdgeInferenceResult> {
    // Validate inference request
    const validation = await this.inferenceEngine.validateRequest(request);
    if (!validation.valid) {
      throw new Error(`Invalid inference request: ${validation.errors.join(', ')}`);
    }

    // Check device resources
    const resourceCheck = await this.resourceManager.checkResources(request.deviceId);
    if (!resourceCheck.sufficient) {
      throw new Error(`Insufficient resources: ${resourceCheck.issues.join(', ')}`);
    }

    // Preprocess input data
    const preprocessedData = await this.preprocessInput(request.input, request.preprocessing);

    // Run inference
    const inferenceResult = await this.inferenceEngine.infer({
      deviceId: request.deviceId,
      input: preprocessedData,
      modelId: request.modelId,
      options: request.options,
    });

    // Postprocess results
    const postprocessedResult = await this.postprocessOutput(
      inferenceResult.output,
      request.postprocessing
    );

    // Log inference metrics
    await this.logInferenceMetrics(request, inferenceResult);

    return {
      ...inferenceResult,
      output: postprocessedResult,
      deviceId: request.deviceId,
      inferenceTime: inferenceResult.inferenceTime,
      memoryUsage: inferenceResult.memoryUsage,
      timestamp: Date.now(),
    };
  }

  async participateInFederatedLearning(participation: FederatedLearningParticipation): Promise<FederatedLearningResult> {
    // Validate participation request
    const validation = await this.validateFederatedLearningParticipation(participation);
    if (!validation.valid) {
      throw new Error(`Invalid federated learning participation: ${validation.errors.join(', ')}`);
    }

    // Get local training data
    const localData = await this.getLocalTrainingData(participation.deviceId, participation.dataConfig);

    // Train local model
    const localTraining = await this.trainLocalModel(participation, localData);

    // Apply differential privacy
    const privateModel = await this.applyDifferentialPrivacy(localTraining.model, participation.privacyConfig);

    // Submit to federated learning coordinator
    const submission = await this.federatedLearning.submitUpdate({
      deviceId: participation.deviceId,
      modelUpdate: privateModel,
      metadata: {
        samples: localData.length,
        epochs: localTraining.epochs,
        accuracy: localTraining.accuracy,
        timestamp: Date.now(),
      },
    });

    // Wait for global model update
    const globalUpdate = await this.waitForGlobalModel(submission.roundId);

    // Update local model
    await this.updateLocalModel(participation.deviceId, globalUpdate.model);

    return {
      participationId: participation.id,
      roundId: submission.roundId,
      localAccuracy: localTraining.accuracy,
      globalAccuracy: globalUpdate.accuracy,
      improvement: globalUpdate.accuracy - localTraining.accuracy,
      timestamp: Date.now(),
    };
  }

  async updateEdgeModel(update: EdgeModelUpdate): Promise<EdgeModelUpdateResult> {
    // Validate update request
    const validation = await this.validateModelUpdate(update);
    if (!validation.valid) {
      throw new Error(`Invalid model update: ${validation.errors.join(', ')}`);
    }

    // Check update compatibility
    const compatibilityCheck = await this.checkUpdateCompatibility(update);
    if (!compatibilityCheck.compatible) {
      throw new Error(`Update not compatible: ${compatibilityCheck.reason}`);
    }

    // Download model update
    const modelUpdate = await this.downloadModelUpdate(update.updateUrl);

    // Verify model integrity
    const integrityCheck = await this.securityManager.verifyModelIntegrity(modelUpdate, update.signature);
    if (!integrityCheck.verified) {
      throw new Error('Model integrity verification failed');
    }

    // Apply delta update if applicable
    const updatedModel = await this.modelUpdater.applyDeltaUpdate({
      deviceId: update.deviceId,
      currentModel: update.currentModel,
      deltaUpdate: modelUpdate,
      strategy: update.strategy || 'delta',
    });

    // Deploy updated model
    const deployment = await this.deployToDevice(update.deviceId, updatedModel);

    // Validate updated model
    const validationResults = await this.validateUpdatedModel(update.deviceId, updatedModel);

    return {
      updateId: update.id,
      deviceId: update.deviceId,
      deployment,
      validationResults,
      updateTimestamp: Date.now(),
    };
  }

  async monitorEdgeAI(deviceId: string): Promise<EdgeAIMonitoringReport> {
    // Get device performance metrics
    const performanceMetrics = await this.resourceManager.getPerformanceMetrics(deviceId);
    
    // Get inference metrics
    const inferenceMetrics = await this.inferenceEngine.getInferenceMetrics(deviceId);
    
    // Get model health metrics
    const modelHealth = await this.getModelHealthMetrics(deviceId);
    
    // Get security metrics
    const securityMetrics = await this.securityManager.getSecurityMetrics(deviceId);

    // Analyze overall performance
    const performanceAnalysis = await this.analyzePerformance({
      performance: performanceMetrics,
      inference: inferenceMetrics,
      model: modelHealth,
      security: securityMetrics,
    });

    return {
      deviceId,
      timestamp: Date.now(),
      performanceMetrics,
      inferenceMetrics,
      modelHealth,
      securityMetrics,
      performanceAnalysis,
      recommendations: this.generateOptimizationRecommendations(performanceAnalysis),
    };
  }

  private async validateDeployment(deployment: EdgeModelDeployment): Promise<ValidationResult> {
    const errors = [];

    // Check device exists
    if (!deployment.deviceId) {
      errors.push('Device ID is required');
    }

    // Check model exists
    if (!deployment.model) {
      errors.push('Model is required');
    }

    // Check constraints
    if (!deployment.constraints) {
      errors.push('Device constraints are required');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private async optimizeModelForEdge(model: AIModel, config: EdgeOptimizationConfig): Promise<OptimizedModel> {
    // Apply quantization
    const quantizedModel = await this.modelOptimizer.quantize(model, {
      precision: config.precision || 'int8',
      calibrationData: config.calibrationData,
    });

    // Apply pruning
    const prunedModel = await this.modelOptimizer.prune(quantizedModel, {
      sparsity: config.sparsity || 0.5,
      method: config.pruningMethod || 'magnitude',
    });

    // Apply knowledge distillation if specified
    let distilledModel = prunedModel;
    if (config.distillation && config.teacherModel) {
      distilledModel = await this.modelOptimizer.distill(prunedModel, config.teacherModel);
    }

    // Optimize for target hardware
    const hardwareOptimized = await this.modelOptimizer.optimizeForHardware(
      distilledModel,
      config.targetDevice
    );

    return {
      ...hardwareOptimized,
      originalSize: model.size,
      optimizedSize: hardwareOptimized.size,
      compressionRatio: model.size / hardwareOptimized.size,
      accuracy: await this.measureAccuracy(hardwareOptimized, config.testData),
    };
  }

  private async preprocessInput(input: any, config: PreprocessingConfig): Promise<any> {
    let processed = input;

    // Apply normalization
    if (config.normalization) {
      processed = await this.normalizeData(processed, config.normalization);
    }

    // Apply resizing
    if (config.resizing) {
      processed = await this.resizeData(processed, config.resizing);
    }

    // Apply data augmentation if specified
    if (config.augmentation) {
      processed = await this.augmentData(processed, config.augmentation);
    }

    return processed;
  }

  private async postprocessOutput(output: any, config: PostprocessingConfig): Promise<any> {
    let processed = output;

    // Apply softmax if classification
    if (config.softmax && Array.isArray(processed)) {
      processed = this.applySoftmax(processed);
    }

    // Apply thresholding
    if (config.thresholding) {
      processed = this.applyThresholding(processed, config.thresholding);
    }

    // Format output
    if (config.formatting) {
      processed = this.formatOutput(processed, config.formatting);
    }

    return processed;
  }

  private async applyDifferentialPrivacy(model: AIModel, config: DifferentialPrivacyConfig): Promise<PrivateModel> {
    // Add noise to model weights
    const noisyWeights = await this.addNoiseToWeights(model.weights, config.epsilon, config.delta);

    // Clip gradients if training
    if (config.gradientClipping) {
      const clippedGradients = await this.clipGradients(model.gradients, config.gradientClipping);
      return { ...model, weights: noisyWeights, gradients: clippedGradients };
    }

    return { ...model, weights: noisyWeights };
  }

  private async analyzePerformance(metrics: PerformanceMetrics): Promise<PerformanceAnalysis> {
    const analysis = {
      overallScore: 0,
      bottlenecks: [],
      recommendations: [],
    };

    // Calculate overall score
    const scores = [
      metrics.performance.cpuUsage ? 1 - (metrics.performance.cpuUsage / 100) : 0,
      metrics.performance.memoryUsage ? 1 - (metrics.performance.memoryUsage / 100) : 0,
      metrics.inference.averageLatency ? 1 - (metrics.inference.averageLatency / 1000) : 0,
      metrics.model.accuracy || 0,
    ];

    analysis.overallScore = scores.reduce((sum, score) => sum + score, 0) / scores.length;

    // Identify bottlenecks
    if (metrics.performance.cpuUsage > 80) {
      analysis.bottlenecks.push({
        type: 'cpu',
        severity: 'high',
        description: 'High CPU usage detected',
        value: metrics.performance.cpuUsage,
      });
    }

    if (metrics.performance.memoryUsage > 85) {
      analysis.bottlenecks.push({
        type: 'memory',
        severity: 'high',
        description: 'High memory usage detected',
        value: metrics.performance.memoryUsage,
      });
    }

    if (metrics.inference.averageLatency > 500) {
      analysis.bottlenecks.push({
        type: 'latency',
        severity: 'medium',
        description: 'High inference latency',
        value: metrics.inference.averageLatency,
      });
    }

    return analysis;
  }

  private generateOptimizationRecommendations(analysis: PerformanceAnalysis): OptimizationRecommendation[] {
    const recommendations = [];

    for (const bottleneck of analysis.bottlenecks) {
      switch (bottleneck.type) {
        case 'cpu':
          recommendations.push({
            type: 'model_optimization',
            priority: 'high',
            action: 'Apply model quantization and pruning',
            expectedImprovement: '30-50% CPU reduction',
          });
          break;
        case 'memory':
          recommendations.push({
            type: 'resource_optimization',
            priority: 'high',
            action: 'Reduce model size and implement memory pooling',
            expectedImprovement: '40-60% memory reduction',
          });
          break;
        case 'latency':
          recommendations.push({
            type: 'inference_optimization',
            priority: 'medium',
            action: 'Optimize inference pipeline and use hardware acceleration',
            expectedImprovement: '20-40% latency reduction',
          });
          break;
      }
    }

    return recommendations;
  }

  private applySoftmax(array: number[]): number[] {
    const max = Math.max(...array);
    const exp = array.map(x => Math.exp(x - max));
    const sum = exp.reduce((a, b) => a + b, 0);
    return exp.map(x => x / sum);
  }

  private applyThresholding(data: any, config: ThresholdConfig): any {
    if (Array.isArray(data)) {
      return data.map(value => value > config.threshold ? 1 : 0);
    }
    return data > config.threshold ? 1 : 0;
  }

  private formatOutput(data: any, config: FormatConfig): any {
    switch (config.type) {
      case 'json':
        return JSON.stringify(data);
      case 'binary':
        return Buffer.from(JSON.stringify(data));
      case 'tensor':
        return { data: data, shape: config.shape };
      default:
        return data;
    }
  }
}

// Edge Model Optimizer Implementation
export class EdgeModelOptimizer {
  constructor(
    private quantizer: ModelQuantizer,
    private pruner: ModelPruner,
    private distiller: ModelDistiller,
    private hardwareOptimizer: HardwareOptimizer
  ) {}

  async optimizeForEdge(model: AIModel, config: EdgeOptimizationConfig): Promise<OptimizedModel> {
    let optimizedModel = model;

    // Apply quantization
    if (config.quantization) {
      optimizedModel = await this.quantizer.quantize(optimizedModel, config.quantization);
    }

    // Apply pruning
    if (config.pruning) {
      optimizedModel = await this.pruner.prune(optimizedModel, config.pruning);
    }

    // Apply knowledge distillation
    if (config.distillation && config.teacherModel) {
      optimizedModel = await this.distiller.distill(optimizedModel, config.teacherModel);
    }

    // Optimize for target hardware
    if (config.targetDevice) {
      optimizedModel = await this.hardwareOptimizer.optimize(optimizedModel, config.targetDevice);
    }

    return optimizedModel;
  }

  async quantize(model: AIModel, config: QuantizationConfig): Promise<QuantizedModel> {
    // Calibrate model if needed
    let calibratedModel = model;
    if (config.calibrationData) {
      calibratedModel = await this.calibrateModel(model, config.calibrationData);
    }

    // Apply quantization
    const quantizedWeights = await this.quantizer.quantizeWeights(
      calibratedModel.weights,
      config.precision
    );

    return {
      ...calibratedModel,
      weights: quantizedWeights,
      quantizationPrecision: config.precision,
      calibrationData: config.calibrationData,
    };
  }

  async prune(model: AIModel, config: PruningConfig): Promise<PrunedModel> {
    // Calculate importance scores
    const importanceScores = await this.calculateImportanceScores(model, config.method);

    // Apply pruning based on importance scores
    const prunedWeights = await this.pruner.pruneWeights(
      model.weights,
      importanceScores,
      config.sparsity
    );

    return {
      ...model,
      weights: prunedWeights,
      sparsity: config.sparsity,
      pruningMethod: config.method,
      importanceScores,
    };
  }

  private async calculateImportanceScores(model: AIModel, method: string): Promise<number[]> {
    switch (method) {
      case 'magnitude':
        return this.calculateMagnitudeImportance(model.weights);
      case 'gradient':
        return this.calculateGradientImportance(model.weights, model.gradients);
      case 'taylor':
        return this.calculateTaylorImportance(model.weights, model.gradients);
      default:
        return new Array(model.weights.length).fill(1.0);
    }
  }

  private calculateMagnitudeImportance(weights: number[]): number[] {
    return weights.map(Math.abs);
  }

  private calculateGradientImportance(weights: number[], gradients: number[]): number[] {
    return weights.map((weight, index) => Math.abs(weight * (gradients[index] || 0)));
  }

  private calculateTaylorImportance(weights: number[], gradients: number[]): number[] {
    return weights.map((weight, index) => Math.abs(weight * weight * (gradients[index] || 0)));
  }
}

// Edge Inference Engine Implementation
export class EdgeInferenceEngine {
  constructor(
    private modelLoader: EdgeModelLoader,
    private runtimeManager: RuntimeManager,
    private metricsCollector: MetricsCollector
  ) {}

  async setup(config: InferenceSetupConfig): Promise<InferenceSetup> {
    // Load model
    const model = await this.modelLoader.loadModel(config.modelId, config.deviceId);

    // Initialize runtime
    const runtime = await this.runtimeManager.initialize({
      deviceId: config.deviceId,
      model,
      configuration: config.configuration,
    });

    // Setup metrics collection
    await this.metricsCollector.setup({
      deviceId: config.deviceId,
      modelId: config.modelId,
      metrics: ['latency', 'memory', 'accuracy', 'throughput'],
    });

    return {
      deviceId: config.deviceId,
      modelId: config.modelId,
      runtime,
      configuration: config.configuration,
    };
  }

  async infer(request: InferenceRequest): Promise<InferenceResult> {
    const startTime = performance.now();

    // Load model if not loaded
    const model = await this.modelLoader.getLoadedModel(request.deviceId, request.modelId);

    // Prepare input
    const preparedInput = await this.prepareInput(request.input, model);

    // Run inference
    const output = await this.runtimeManager.runInference({
      deviceId: request.deviceId,
      modelId: request.modelId,
      input: preparedInput,
      options: request.options,
    });

    const endTime = performance.now();

    // Collect metrics
    const metrics = await this.metricsCollector.record({
      deviceId: request.deviceId,
      modelId: request.modelId,
      latency: endTime - startTime,
      memoryUsage: await this.getMemoryUsage(request.deviceId),
      output,
    });

    return {
      output,
      inferenceTime: endTime - startTime,
      memoryUsage: metrics.memoryUsage,
      deviceId: request.deviceId,
      modelId: request.modelId,
      timestamp: Date.now(),
    };
  }

  async validateRequest(request: EdgeInferenceRequest): Promise<ValidationResult> {
    const errors = [];

    if (!request.deviceId) {
      errors.push('Device ID is required');
    }

    if (!request.modelId) {
      errors.push('Model ID is required');
    }

    if (!request.input) {
      errors.push('Input data is required');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private async prepareInput(input: any, model: AIModel): Promise<any> {
    // Convert input to model's expected format
    const expectedFormat = model.inputFormat;
    
    switch (expectedFormat) {
      case 'tensor':
        return this.convertToTensor(input);
      case 'array':
        return Array.isArray(input) ? input : [input];
      case 'object':
        return typeof input === 'object' ? input : { data: input };
      default:
        return input;
    }
  }

  private convertToTensor(input: any): any {
    // Simple tensor conversion - in production use proper tensor library
    if (Array.isArray(input)) {
      return {
        data: input,
        shape: [input.length],
        dtype: 'float32',
      };
    }
    return input;
  }

  private async getMemoryUsage(deviceId: string): Promise<number> {
    // Get memory usage from device
    return Math.random() * 100; // Placeholder
  }
}

// Federated Learning Engine Implementation
export class FederatedLearningEngine {
  constructor(
    private aggregator: FederatedAggregator,
    private privacyManager: PrivacyManager,
    private coordinator: FederatedCoordinator
  ) {}

  async submitUpdate(submission: FederatedSubmission): Promise<FederatedSubmissionResult> {
    // Validate submission
    const validation = await this.validateSubmission(submission);
    if (!validation.valid) {
      throw new Error(`Invalid submission: ${validation.errors.join(', ')}`);
    }

    // Apply privacy protection
    const protectedUpdate = await this.privacyManager.protect(submission.modelUpdate, {
      epsilon: 1.0,
      delta: 1e-5,
    });

    // Submit to coordinator
    const result = await this.coordinator.submitUpdate({
      ...submission,
      modelUpdate: protectedUpdate,
    });

    return {
      submissionId: submission.id,
      roundId: result.roundId,
      accepted: result.accepted,
      contribution: result.contribution,
      timestamp: Date.now(),
    };
  }

  async waitForGlobalModel(roundId: string): Promise<GlobalModelUpdate> {
    // Poll for global model update
    let attempts = 0;
    const maxAttempts = 60; // 5 minutes with 5-second intervals

    while (attempts < maxAttempts) {
      const update = await this.coordinator.getGlobalModel(roundId);
      if (update.available) {
        return update;
      }

      await this.sleep(5000); // Wait 5 seconds
      attempts++;
    }

    throw new Error('Timeout waiting for global model update');
  }

  private async validateSubmission(submission: FederatedSubmission): Promise<ValidationResult> {
    const errors = [];

    if (!submission.deviceId) {
      errors.push('Device ID is required');
    }

    if (!submission.modelUpdate) {
      errors.push('Model update is required');
    }

    if (!submission.metadata) {
      errors.push('Metadata is required');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private sleep(ms: number): Promise<void> {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No edge AI optimization
export class BasicEdgeDevice {
  // BAD: No model optimization
  async runModel(input: any) {
    // BAD: No resource management
    // BAD: No federated learning
    // BAD: No model updates
    const model = this.loadModel();
    return model.predict(input);
  }

  // BAD: No edge AI monitoring
  // BAD: No security for edge AI
  // BAD: No power optimization
}
```
</example_bad>
