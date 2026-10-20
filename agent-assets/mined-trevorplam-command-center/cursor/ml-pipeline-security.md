---
description: Run ML Pipeline Security and Model Validation Standards Check
globs: ["**/ml-security/**/*.ts", "**/model-validation/**/*.ts", "**/data-poisoning/**/*.ts"]
---
# AI/ML: ML Pipeline Security & Model Validation Standards

<audit_rules>
- You MUST implement proper data poisoning detection and prevention in ML pipelines.
- You MUST ensure model validation with adversarial testing and robustness checks.
- You MUST implement proper input sanitization and validation for ML inference endpoints.
- You MUST configure proper model integrity verification and tamper detection.
- You MUST ensure proper access control for model training and deployment operations.
- You MUST implement proper audit logging for all ML pipeline operations.
- You MUST configure proper privacy preservation techniques like differential privacy.
- You MUST ensure proper model watermarking for intellectual property protection.
- You MUST implement proper secure model aggregation for federated learning.
- You MUST ensure proper explainability and transparency for regulatory compliance.
</audit_rules>

<example_good>
```typescript
// ML Pipeline Security Implementation

export class MLPipelineSecurityManager {
  constructor(
    private dataValidator: MLDataValidator,
    private modelValidator: ModelValidator,
    private poisoningDetector: DataPoisoningDetector,
    private adversarialTester: AdversarialTester,
    private privacyPreserver: PrivacyPreserver,
    private auditLogger: MLAuditLogger
  ) {}

  async secureTrainingPipeline(pipeline: TrainingPipelineConfig): Promise<SecureTrainingResult> {
    // Validate training data integrity
    const dataIntegrity = await this.validateTrainingDataIntegrity(pipeline.trainingData);
    if (!dataIntegrity.isValid) {
      throw new Error(`Training data integrity validation failed: ${dataIntegrity.issues.join(', ')}`);
    }

    // Detect data poisoning
    const poisoningAnalysis = await this.poisoningDetector.analyzeTrainingData(pipeline.trainingData);
    if (poisoningAnalysis.hasPoisoning) {
      await this.handleDataPoisoning(poisoningAnalysis, pipeline);
    }

    // Apply privacy preservation
    const privacyEnhancedData = await this.privacyPreserver.applyPrivacyTechniques(pipeline.trainingData, {
      technique: pipeline.privacyTechnique || 'differential_privacy',
      epsilon: pipeline.privacyEpsilon || 1.0,
    });

    // Secure training with monitoring
    const trainingResult = await this.executeSecureTraining({
      ...pipeline,
      trainingData: privacyEnhancedData,
      monitoring: {
        integrityChecks: true,
        performanceMonitoring: true,
        anomalyDetection: true,
      },
    });

    // Validate trained model
    const modelValidation = await this.modelValidator.validateModel(trainingResult.model, {
      robustnessTests: true,
      adversarialTests: true,
      biasTests: true,
      performanceTests: true,
    });

    // Apply model watermarking
    const watermarkedModel = await this.applyModelWatermarking(trainingResult.model, pipeline.watermarkConfig);

    // Log training completion
    await this.auditLogger.logTrainingCompletion({
      pipelineId: pipeline.id,
      modelId: watermarkedModel.id,
      dataIntegrity,
      poisoningAnalysis,
      modelValidation,
      timestamp: Date.now(),
    });

    return {
      model: watermarkedModel,
      validation: modelValidation,
      privacyMetrics: await this.calculatePrivacyMetrics(privacyEnhancedData),
      securityMetrics: await this.calculateSecurityMetrics(trainingResult),
    };
  }

  async secureInferencePipeline(inferenceConfig: InferenceConfig): Promise<SecureInferenceResult> {
    // Validate input data
    const inputValidation = await this.validateInferenceInput(inferenceConfig.input);
    if (!inputValidation.isValid) {
      throw new Error(`Input validation failed: ${inputValidation.issues.join(', ')}`);
    }

    // Check for adversarial inputs
    const adversarialAnalysis = await this.adversarialTester.analyzeInput(inferenceConfig.input);
    if (adversarialAnalysis.isAdversarial) {
      await this.handleAdversarialInput(adversarialAnalysis, inferenceConfig);
    }

    // Verify model integrity
    const modelIntegrity = await this.verifyModelIntegrity(inferenceConfig.model);
    if (!modelIntegrity.isValid) {
      throw new Error('Model integrity verification failed');
    }

    // Execute secure inference
    const inferenceResult = await this.executeSecureInference({
      ...inferenceConfig,
      input: inputValidation.sanitizedInput,
      monitoring: {
        inputValidation: true,
        outputValidation: true,
        anomalyDetection: true,
      },
    });

    // Validate output
    const outputValidation = await this.validateInferenceOutput(inferenceResult.output);

    // Log inference
    await this.auditLogger.logInference({
      modelId: inferenceConfig.model.id,
      inputHash: this.hashInput(inputValidation.sanitizedInput),
      outputValidation,
      timestamp: Date.now(),
    });

    return {
      output: inferenceResult.output,
      confidence: inferenceResult.confidence,
      inputValidation,
      outputValidation,
      securityMetrics: await this.calculateInferenceSecurityMetrics(inferenceResult),
    };
  }

  async detectDataPoisoning(dataset: Dataset): Promise<DataPoisoningAnalysis> {
    // Analyze data distribution anomalies
    const distributionAnalysis = await this.analyzeDataDistribution(dataset);
    
    // Check for label poisoning
    const labelAnalysis = await this.analyzeLabelPoisoning(dataset);
    
    // Check for feature poisoning
    const featureAnalysis = await this.analyzeFeaturePoisoning(dataset);
    
    // Check for backdoor patterns
    const backdoorAnalysis = await this.analyzeBackdoorPatterns(dataset);
    
    // Calculate overall poisoning score
    const poisoningScore = this.calculatePoisoningScore({
      distributionAnalysis,
      labelAnalysis,
      featureAnalysis,
      backdoorAnalysis,
    });

    return {
      hasPoisoning: poisoningScore > 0.3, // 30% threshold
      poisoningScore,
      suspiciousSamples: this.identifySuspiciousSamples(dataset, {
        distributionAnalysis,
        labelAnalysis,
        featureAnalysis,
      }),
      poisoningTypes: this.identifyPoisoningTypes({
        distributionAnalysis,
        labelAnalysis,
        featureAnalysis,
        backdoorAnalysis,
      }),
      recommendations: this.generatePoisoningRecommendations(poisoningScore),
    };
  }

  async validateModelRobustness(model: Model, robustnessConfig: RobustnessConfig): Promise<RobustnessValidation> {
    // Adversarial robustness testing
    const adversarialRobustness = await this.testAdversarialRobustness(model, robustnessConfig);
    
    // Noise robustness testing
    const noiseRobustness = await this.testNoiseRobustness(model, robustnessConfig);
    
    // Distribution shift robustness
    const distributionRobustness = await this.testDistributionShift(model, robustnessConfig);
    
    // Concept drift robustness
    const conceptDriftRobustness = await this.testConceptDrift(model, robustnessConfig);

    return {
      overallScore: this.calculateRobustnessScore({
        adversarialRobustness,
        noiseRobustness,
        distributionRobustness,
        conceptDriftRobustness,
      }),
      adversarialRobustness,
      noiseRobustness,
      distributionRobustness,
      conceptDriftRobustness,
      recommendations: this.generateRobustnessRecommendations({
        adversarialRobustness,
        noiseRobustness,
        distributionRobustness,
        conceptDriftRobustness,
      }),
    };
  }

  private async validateTrainingDataIntegrity(data: Dataset): Promise<DataIntegrityResult> {
    const issues = [];

    // Check for duplicate samples
    const duplicates = await this.detectDuplicates(data);
    if (duplicates.length > 0) {
      issues.push(`Found ${duplicates.length} duplicate samples`);
    }

    // Check for missing values
    const missingValues = await this.detectMissingValues(data);
    if (missingValues.length > 0) {
      issues.push(`Missing values in features: ${missingValues.join(', ')}`);
    }

    // Check for outliers
    const outliers = await this.detectOutliers(data);
    if (outliers.length > data.samples.length * 0.05) { // More than 5% outliers
      issues.push(`High number of outliers: ${outliers.length}`);
    }

    // Check data consistency
    const consistency = await this.checkDataConsistency(data);
    if (!consistency.isConsistent) {
      issues.push(`Data consistency issues: ${consistency.issues.join(', ')}`);
    }

    return {
      isValid: issues.length === 0,
      issues,
      duplicates,
      missingValues,
      outliers,
      consistency,
    };
  }

  private async handleDataPoisoning(analysis: DataPoisoningAnalysis, pipeline: TrainingPipelineConfig): Promise<void> {
    // Log poisoning detection
    await this.auditLogger.logDataPoisoningDetection({
      pipelineId: pipeline.id,
      analysis,
      timestamp: Date.now(),
    });

    // Remove suspicious samples
    if (analysis.suspiciousSamples.length > 0) {
      const cleanedData = await this.removeSuspiciousSamples(pipeline.trainingData, analysis.suspiciousSamples);
      pipeline.trainingData = cleanedData;
    }

    // Apply robust training techniques
    pipeline.robustTraining = true;
    pipeline.outlierDetection = true;
    pipeline.noiseInjection = true;
  }

  private async applyModelWatermarking(model: Model, watermarkConfig: WatermarkConfig): Promise<WatermarkedModel> {
    const watermark = {
      id: generateId(),
      owner: watermarkConfig.owner,
      timestamp: Date.now(),
      technique: watermarkConfig.technique || 'deep_signatures',
    };

    // Apply watermarking based on technique
    switch (watermark.technique) {
      case 'deep_signatures':
        return await this.applyDeepSignaturesWatermark(model, watermark);
      case 'adversarial_watermark':
        return await this.applyAdversarialWatermark(model, watermark);
      case 'backdoor_watermark':
        return await this.applyBackdoorWatermark(model, watermark);
      default:
        throw new Error(`Unknown watermarking technique: ${watermark.technique}`);
    }
  }

  private async verifyModelIntegrity(model: Model): Promise<ModelIntegrityResult> {
    // Verify model checksum
    const expectedChecksum = model.checksum;
    const actualChecksum = await this.calculateModelChecksum(model);
    
    if (expectedChecksum !== actualChecksum) {
      return {
        isValid: false,
        reason: 'Model checksum mismatch',
        expected: expectedChecksum,
        actual: actualChecksum,
      };
    }

    // Verify watermark
    const watermarkVerification = await this.verifyWatermark(model);
    if (!watermarkVerification.isValid) {
      return {
        isValid: false,
        reason: 'Watermark verification failed',
        watermark: watermarkVerification,
      };
    }

    return {
      isValid: true,
      checksum: actualChecksum,
      watermark: watermarkVerification,
    };
  }

  private async testAdversarialRobustness(model: Model, config: RobustnessConfig): Promise<AdversarialRobustnessResult> {
    const attacks = config.adversarialAttacks || ['fgsm', 'pgd', 'cw'];
    const results = {};

    for (const attack of attacks) {
      const attackResult = await this.executeAdversarialAttack(model, attack, config);
      results[attack] = attackResult;
    }

    return {
      attacks: results,
      averageRobustness: this.calculateAverageRobustness(results),
      weakestAttack: this.findWeakestAttack(results),
      recommendations: this.generateAdversarialRecommendations(results),
    };
  }

  private async executeAdversarialAttack(model: Model, attackType: string, config: RobustnessConfig): Promise<AdversarialAttackResult> {
    // Generate adversarial examples
    const adversarialExamples = await this.generateAdversarialExamples(model, attackType, config);
    
    // Test model on adversarial examples
    const originalAccuracy = await this.evaluateModel(model, config.testData);
    const adversarialAccuracy = await this.evaluateModel(model, adversarialExamples);
    
    // Calculate robustness score
    const robustnessScore = adversarialAccuracy / originalAccuracy;

    return {
      attackType,
      originalAccuracy,
      adversarialAccuracy,
      robustnessScore,
      adversarialExamples: adversarialExamples.length,
    };
  }
}

// Data Poisoning Detector
export class DataPoisoningDetector {
  async analyzeDataDistribution(dataset: Dataset): Promise<DistributionAnalysis> {
    const analysis = {
      normalityTests: {},
      outlierScores: {},
      clusterAnalysis: {},
    };

    // Perform normality tests for each feature
    for (const feature of dataset.features) {
      analysis.normalityTests[feature.name] = await this.performNormalityTest(feature.values);
    }

    // Calculate outlier scores
    analysis.outlierScores = await this.calculateOutlierScores(dataset);

    // Perform cluster analysis
    analysis.clusterAnalysis = await this.performClusterAnalysis(dataset);

    return {
      isAnomalous: this.detectDistributionAnomaly(analysis),
      analysis,
    };
  }

  async analyzeLabelPoisoning(dataset: Dataset): Promise<LabelAnalysis> {
    // Check for label flipping patterns
    const labelFlipping = await this.detectLabelFlipping(dataset);
    
    // Check for inconsistent labeling
    const inconsistency = await this.detectLabelInconsistency(dataset);
    
    // Check for targeted poisoning
    const targetedPoisoning = await this.detectTargetedPoisoning(dataset);

    return {
      hasLabelPoisoning: labelFlipping.hasFlipping || inconsistency.hasInconsistency || targetedPoisoning.hasTargeted,
      labelFlipping,
      inconsistency,
      targetedPoisoning,
    };
  }

  private async detectLabelFlipping(dataset: Dataset): Promise<LabelFlippingResult> {
    const flippedSamples = [];
    const confidenceThreshold = 0.9;

    // Train a simple classifier to detect label anomalies
    const classifier = await this.trainAnomalyDetector(dataset);
    
    for (const sample of dataset.samples) {
      const prediction = await classifier.predict(sample.features);
      const confidence = await classifier.predict_proba(sample.features);
      
      // Check if prediction differs from label with high confidence
      if (prediction !== sample.label && confidence > confidenceThreshold) {
        flippedSamples.push({
          sampleId: sample.id,
          originalLabel: sample.label,
          predictedLabel: prediction,
          confidence,
        });
      }
    }

    return {
      hasFlipping: flippedSamples.length > 0,
      flippedSamples,
      flippingRate: flippedSamples.length / dataset.samples.length,
    };
  }
}

// Adversarial Tester
export class AdversarialTester {
  async analyzeInput(input: ModelInput): Promise<AdversarialAnalysis> {
    // Check for common adversarial patterns
    const patternAnalysis = await this.detectAdversarialPatterns(input);
    
    // Check for perturbation signatures
    const perturbationAnalysis = await this.detectPerturbations(input);
    
    // Check for backdoor triggers
    const backdoorAnalysis = await this.detectBackdoorTriggers(input);

    return {
      isAdversarial: patternAnalysis.hasPattern || perturbationAnalysis.hasPerturbation || backdoorAnalysis.hasTrigger,
      confidence: this.calculateAdversarialConfidence(patternAnalysis, perturbationAnalysis, backdoorAnalysis),
      patternAnalysis,
      perturbationAnalysis,
      backdoorAnalysis,
    };
  }

  private async detectAdversarialPatterns(input: ModelInput): Promise<PatternAnalysis> {
    const patterns = {
      gradientBased: await this.detectGradientBasedPatterns(input),
      decisionBased: await this.detectDecisionBasedPatterns(input),
      queryBased: await this.detectQueryBasedPatterns(input),
    };

    return {
      hasPattern: Object.values(patterns).some(p => p.detected),
      patterns,
    };
  }

  private async detectGradientBasedPatterns(input: ModelInput): Promise<GradientPattern> {
    // Analyze input for gradient-based attack signatures
    const gradientSignature = await this.calculateGradientSignature(input);
    const threshold = 0.1; // Threshold for gradient-based detection

    return {
      detected: gradientSignature > threshold,
      signature: gradientSignature,
      attackType: this.classifyGradientAttack(gradientSignature),
    };
  }
}

// Privacy Preserver
export class PrivacyPreserver {
  async applyPrivacyTechniques(data: Dataset, config: PrivacyConfig): Promise<PrivacyEnhancedDataset> {
    let enhancedData = data;

    switch (config.technique) {
      case 'differential_privacy':
        enhancedData = await this.applyDifferentialPrivacy(data, config);
        break;
      case 'federated_learning':
        enhancedData = await this.applyFederatedLearning(data, config);
        break;
      case 'homomorphic_encryption':
        enhancedData = await this.applyHomomorphicEncryption(data, config);
        break;
      case 'secure_aggregation':
        enhancedData = await this.applySecureAggregation(data, config);
        break;
      default:
        throw new Error(`Unknown privacy technique: ${config.technique}`);
    }

    return enhancedData;
  }

  private async applyDifferentialPrivacy(data: Dataset, config: PrivacyConfig): Promise<PrivacyEnhancedDataset> {
    const epsilon = config.epsilon || 1.0;
    const delta = config.delta || 1e-5;

    // Add Laplace noise to sensitive features
    const noisyFeatures = await this.addLaplaceNoise(data.features, epsilon);
    
    // Apply privacy-preserving aggregation
    const aggregatedData = await this.privacyPreservingAggregation(data, epsilon, delta);

    return {
      ...data,
      features: noisyFeatures,
      aggregatedData,
      privacyMetrics: await this.calculatePrivacyMetrics(data, epsilon, delta),
    };
  }

  private async addLaplaceNoise(features: Feature[], epsilon: number): Promise<Feature[]> {
    return features.map(feature => ({
      ...feature,
      values: feature.values.map(value => {
        const scale = 1 / epsilon;
        const noise = this.generateLaplaceNoise(0, scale);
        return value + noise;
      }),
    }));
  }

  private generateLaplaceNoise(location: number, scale: number): number {
    // Laplace noise generation
    const uniform = Math.random() - 0.5;
    return location - scale * Math.sign(uniform) * Math.log(1 - 2 * Math.abs(uniform));
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No ML pipeline security
export class BasicMLPipeline {
  // BAD: No data poisoning detection
  async trainModel(data: any) {
    // BAD: No data validation
    // BAD: No privacy protection
    // BAD: No model watermarking
    const model = await this.train(data);
    return model;
  }

  // BAD: No adversarial testing
  // BAD: No model integrity verification
  // BAD: No explainability
}
```
</example_bad>
