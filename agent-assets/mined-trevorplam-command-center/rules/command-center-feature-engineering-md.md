---
description: Run Feature Engineering and Data Pipeline Standards Check
globs: ['**/features/**/*.ts', '**/feature-store/**/*.ts', '**/data-pipeline/**/*.ts']
---

# AI/ML: Feature Engineering & Data Pipeline Standards

<audit_rules>

- You MUST implement proper feature validation and schema enforcement for all features.
- You MUST ensure proper feature versioning and backward compatibility in feature stores.
- You MUST implement proper data drift detection and feature monitoring pipelines.
- You MUST configure proper feature freshness and staleness management.
- You MUST ensure proper feature transformation and preprocessing consistency.
- You MUST implement proper feature lineage and metadata tracking.
- You MUST configure proper feature access controls and data privacy compliance.
- You MUST ensure proper feature quality metrics and data quality monitoring.
- You MUST implement proper feature caching and performance optimization.
- You MUST ensure proper feature documentation and business context tracking.
  </audit_rules>

<example_good>

```typescript
// Feature Engineering Implementation

export class FeatureEngineeringOrchestrator {
  constructor(
    private featureStore: FeatureStore,
    private featureValidator: FeatureValidator,
    private dataQualityMonitor: DataQualityMonitor,
    private featureRegistry: FeatureRegistry,
    private transformationEngine: TransformationEngine,
    private lineageTracker: FeatureLineageTracker
  ) {}

  async createFeaturePipeline(config: FeaturePipelineConfig): Promise<FeaturePipeline> {
    // Validate feature definitions
    await this.validateFeatureDefinitions(config.features)

    // Setup feature lineage
    const lineageConfig = await this.setupFeatureLineage(config.features)

    // Create transformation pipeline
    const transformationPipeline = await this.createTransformationPipeline(config.transformations)

    // Setup data quality monitoring
    const qualityConfig = await this.setupDataQualityMonitoring(config.features)

    // Configure feature freshness
    const freshnessConfig = await this.setupFeatureFreshness(config.features)

    return {
      id: config.id,
      features: config.features,
      transformations: transformationPipeline,
      lineage: lineageConfig,
      quality: qualityConfig,
      freshness: freshnessConfig,
      status: 'active',
    }
  }

  async processFeatureData(
    pipeline: FeaturePipeline,
    rawData: RawData
  ): Promise<ProcessedFeatures> {
    // Validate input data
    const dataValidation = await this.featureValidator.validateInputData(rawData)
    if (!dataValidation.isValid) {
      throw new Error(`Input data validation failed: ${dataValidation.errors.join(', ')}`)
    }

    // Apply transformations
    const transformedData = await this.transformationEngine.transform(
      rawData,
      pipeline.transformations
    )

    // Validate transformed features
    const featureValidation = await this.validateFeatures(transformedData, pipeline.features)
    if (!featureValidation.isValid) {
      throw new Error(`Feature validation failed: ${featureValidation.errors.join(', ')}`)
    }

    // Update feature lineage
    await this.lineageTracker.updateLineage(pipeline.id, {
      input: rawData,
      output: transformedData,
      transformations: pipeline.transformations,
      timestamp: Date.now(),
    })

    // Store features
    const storedFeatures = await this.featureStore.storeFeatures(transformedData, {
      pipelineId: pipeline.id,
      freshness: pipeline.freshness,
      metadata: {
        validation: featureValidation,
        lineage: await this.lineageTracker.getLineage(pipeline.id),
        quality: await this.dataQualityMonitor.getQualityMetrics(pipeline.id),
      },
    })

    // Update quality metrics
    await this.dataQualityMonitor.updateQualityMetrics(pipeline.id, storedFeatures)

    return storedFeatures
  }

  async monitorFeatureQuality(pipelineId: string): Promise<FeatureQualityReport> {
    // Get current quality metrics
    const currentMetrics = await this.dataQualityMonitor.getQualityMetrics(pipelineId)

    // Check for data drift
    const driftAnalysis = await this.analyzeFeatureDrift(pipelineId, currentMetrics)

    // Check for staleness
    const stalenessAnalysis = await this.analyzeFeatureStaleness(pipelineId)

    // Check for missing values
    const missingValueAnalysis = await this.analyzeMissingValues(pipelineId)

    // Check for outliers
    const outlierAnalysis = await this.analyzeOutliers(pipelineId)

    return {
      pipelineId,
      timestamp: Date.now(),
      overall: this.calculateOverallQuality(currentMetrics, driftAnalysis, stalenessAnalysis),
      metrics: currentMetrics,
      drift: driftAnalysis,
      staleness: stalenessAnalysis,
      missingValues: missingValueAnalysis,
      outliers: outlierAnalysis,
      recommendations: this.generateQualityRecommendations({
        currentMetrics,
        driftAnalysis,
        stalenessAnalysis,
        missingValueAnalysis,
        outlierAnalysis,
      }),
    }
  }

  async createFeatureDefinition(definition: FeatureDefinition): Promise<Feature> {
    // Validate feature definition
    await this.validateFeatureDefinition(definition)

    // Register feature
    const feature = await this.featureRegistry.registerFeature(definition)

    // Setup validation rules
    await this.setupFeatureValidation(feature)

    // Setup monitoring
    await this.setupFeatureMonitoring(feature)

    return feature
  }

  private async validateFeatureDefinitions(features: FeatureDefinition[]): Promise<void> {
    for (const feature of features) {
      await this.validateFeatureDefinition(feature)
    }
  }

  private async validateFeatureDefinition(definition: FeatureDefinition): Promise<void> {
    // Validate feature name
    if (!definition.name || definition.name.length === 0) {
      throw new Error('Feature name is required')
    }

    // Validate feature type
    const validTypes = ['numerical', 'categorical', 'text', 'boolean', 'datetime', 'array']
    if (!validTypes.includes(definition.type)) {
      throw new Error(`Invalid feature type: ${definition.type}`)
    }

    // Validate data source
    if (!definition.dataSource) {
      throw new Error('Data source is required')
    }

    // Validate transformation
    if (definition.transformation) {
      await this.validateTransformation(definition.transformation)
    }

    // Check for duplicate names
    const existingFeature = await this.featureRegistry.getFeature(definition.name)
    if (existingFeature && existingFeature.version !== definition.version) {
      throw new Error(`Feature ${definition.name} already exists with different version`)
    }
  }

  private async createTransformationPipeline(
    transformations: TransformationConfig[]
  ): Promise<TransformationPipeline> {
    const pipeline = []

    for (const transformConfig of transformations) {
      const transformation = await this.transformationEngine.createTransformation(transformConfig)
      pipeline.push(transformation)
    }

    return {
      transformations: pipeline,
      dependencies: this.calculateTransformationDependencies(transformations),
      parallelizable: this.identifyParallelizableTransformations(transformations),
    }
  }

  private async setupFeatureLineage(features: FeatureDefinition[]): Promise<FeatureLineageConfig> {
    const lineageConfig = {
      features: features.map((f) => ({
        name: f.name,
        source: f.dataSource,
        transformations: f.transformation ? [f.transformation] : [],
        dependencies: f.dependencies || [],
      })),
      tracking: true,
      metadata: {
        created: Date.now(),
        version: '1.0',
      },
    }

    await this.lineageTracker.initializeLineage(lineageConfig)
    return lineageConfig
  }

  private async setupDataQualityMonitoring(
    features: FeatureDefinition[]
  ): Promise<DataQualityConfig> {
    const qualityRules = features.map((feature) => ({
      feature: feature.name,
      rules: this.generateQualityRules(feature),
      thresholds: feature.qualityThresholds || this.getDefaultThresholds(feature.type),
    }))

    return {
      rules: qualityRules,
      monitoring: true,
      alerting: {
        enabled: true,
        channels: ['email', 'slack'],
        threshold: 0.8, // 80% quality threshold
      },
    }
  }

  private async setupFeatureFreshness(features: FeatureDefinition[]): Promise<FreshnessConfig> {
    const freshnessRules = features.map((feature) => ({
      feature: feature.name,
      maxAge: feature.maxAge || 3600000, // 1 hour default
      updateFrequency: feature.updateFrequency || 300000, // 5 minutes default
      stalenessThreshold: feature.stalenessThreshold || 0.9, // 90% freshness threshold
    }))

    return {
      rules: freshnessRules,
      monitoring: true,
      cleanup: {
        enabled: true,
        retentionPeriod: 86400000, // 24 hours
      },
    }
  }

  private async validateFeatures(
    features: ProcessedData,
    definitions: FeatureDefinition[]
  ): Promise<FeatureValidationResult> {
    const errors = []
    const warnings = []

    for (const definition of definitions) {
      const feature = features[definition.name]

      if (!feature) {
        errors.push(`Missing required feature: ${definition.name}`)
        continue
      }

      // Validate feature type
      if (!this.validateFeatureType(feature, definition.type)) {
        errors.push(`Invalid type for feature ${definition.name}: expected ${definition.type}`)
      }

      // Validate feature values
      const valueValidation = await this.validateFeatureValues(feature, definition)
      if (!valueValidation.isValid) {
        errors.push(...valueValidation.errors.map((e) => `${definition.name}: ${e}`))
        warnings.push(...valueValidation.warnings.map((w) => `${definition.name}: ${w}`))
      }

      // Validate business rules
      const businessValidation = await this.validateBusinessRules(feature, definition)
      if (!businessValidation.isValid) {
        errors.push(...businessValidation.errors.map((e) => `${definition.name}: ${e}`))
        warnings.push(...businessValidation.warnings.map((w) => `${definition.name}: ${w}`))
      }
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    }
  }

  private async analyzeFeatureDrift(
    pipelineId: string,
    currentMetrics: QualityMetrics
  ): Promise<FeatureDriftAnalysis> {
    // Get reference metrics
    const referenceMetrics = await this.dataQualityMonitor.getReferenceMetrics(pipelineId)

    if (!referenceMetrics) {
      return {
        hasDrift: false,
        reason: 'No reference metrics available',
      }
    }

    // Calculate drift for each feature
    const featureDrifts = {}
    let hasDrift = false
    let maxDrift = 0

    for (const [featureName, currentMetric] of Object.entries(currentMetrics.featureMetrics)) {
      const referenceMetric = referenceMetrics.featureMetrics[featureName]
      if (referenceMetric) {
        const drift = this.calculateFeatureDrift(currentMetric, referenceMetric)
        featureDrifts[featureName] = drift
        hasDrift = hasDrift || drift > 0.1 // 10% drift threshold
        maxDrift = Math.max(maxDrift, drift)
      }
    }

    return {
      hasDrift,
      maxDrift,
      driftedFeatures: Object.entries(featureDrifts)
        .filter(([_, drift]) => drift > 0.1)
        .map(([name, _]) => name),
      featureDrifts,
    }
  }

  private async analyzeFeatureStaleness(pipelineId: string): Promise<FeatureStalenessAnalysis> {
    const freshnessMetrics = await this.dataQualityMonitor.getFreshnessMetrics(pipelineId)

    const staleFeatures = []
    let overallStaleness = 0

    for (const [featureName, freshness] of Object.entries(freshnessMetrics)) {
      const stalenessScore = this.calculateStalenessScore(freshness)
      overallStaleness += stalenessScore

      if (stalenessScore > 0.5) {
        // 50% staleness threshold
        staleFeatures.push({
          feature: featureName,
          stalenessScore,
          lastUpdate: freshness.lastUpdate,
          maxAge: freshness.maxAge,
        })
      }
    }

    overallStaleness = overallStaleness / Object.keys(freshnessMetrics).length

    return {
      overallStaleness,
      isStale: overallStaleness > 0.3, // 30% overall staleness threshold
      staleFeatures,
    }
  }

  private generateQualityRules(feature: FeatureDefinition): QualityRule[] {
    const rules = []

    // Basic validation rules
    rules.push({
      type: 'not_null',
      description: 'Feature should not be null',
      severity: 'error',
    })

    // Type-specific rules
    switch (feature.type) {
      case 'numerical':
        rules.push({
          type: 'range_check',
          description: 'Value should be within valid range',
          severity: 'warning',
          parameters: {
            min: feature.minValue,
            max: feature.maxValue,
          },
        })
        break
      case 'categorical':
        rules.push({
          type: 'allowed_values',
          description: 'Value should be in allowed categories',
          severity: 'error',
          parameters: {
            values: feature.allowedValues,
          },
        })
        break
      case 'text':
        rules.push({
          type: 'length_check',
          description: 'Text length should be within limits',
          severity: 'warning',
          parameters: {
            minLength: feature.minLength,
            maxLength: feature.maxLength,
          },
        })
        break
    }

    // Business rules
    if (feature.businessRules) {
      rules.push(...feature.businessRules)
    }

    return rules
  }

  private getDefaultThresholds(featureType: string): QualityThresholds {
    const defaults = {
      numerical: {
        completeness: 0.95,
        accuracy: 0.9,
        consistency: 0.9,
      },
      categorical: {
        completeness: 0.95,
        consistency: 0.95,
        uniqueness: 0.8,
      },
      text: {
        completeness: 0.9,
        consistency: 0.85,
      },
      boolean: {
        completeness: 0.98,
        consistency: 0.95,
      },
    }

    return defaults[featureType] || defaults.numerical
  }

  private calculateOverallQuality(
    metrics: QualityMetrics,
    drift: FeatureDriftAnalysis,
    staleness: FeatureStalenessAnalysis
  ): number {
    const qualityScore = metrics.overallScore
    const driftPenalty = drift.hasDrift ? 0.2 : 0
    const stalenessPenalty = staleness.isStale ? 0.15 : 0

    return Math.max(0, qualityScore - driftPenalty - stalenessPenalty)
  }

  private generateQualityRecommendations(analysis: QualityAnalysis): Recommendation[] {
    const recommendations = []

    // Drift recommendations
    if (analysis.driftAnalysis.hasDrift) {
      recommendations.push({
        type: 'drift',
        priority: 'high',
        action: 'retrain_pipeline',
        reason: 'Feature drift detected',
        details: `Max drift: ${analysis.driftAnalysis.maxDrift}`,
      })
    }

    // Staleness recommendations
    if (analysis.stalenessAnalysis.isStale) {
      recommendations.push({
        type: 'staleness',
        priority: 'medium',
        action: 'update_freshness',
        reason: 'Features are stale',
        details: `Overall staleness: ${analysis.stalenessAnalysis.overallStaleness}`,
      })
    }

    // Missing value recommendations
    if (analysis.missingValueAnalysis.hasMissingValues) {
      recommendations.push({
        type: 'missing_values',
        priority: 'medium',
        action: 'impute_missing',
        reason: 'Missing values detected',
        details: `Missing rate: ${analysis.missingValueAnalysis.missingRate}`,
      })
    }

    // Outlier recommendations
    if (analysis.outlierAnalysis.hasOutliers) {
      recommendations.push({
        type: 'outliers',
        priority: 'low',
        action: 'investigate_outliers',
        reason: 'Outliers detected',
        details: `Outlier rate: ${analysis.outlierAnalysis.outlierRate}`,
      })
    }

    return recommendations
  }
}

// Feature Store Implementation
export class FeatureStore {
  constructor(
    private onlineStore: OnlineFeatureStore,
    private offlineStore: OfflineFeatureStore,
    private cacheManager: CacheManager
  ) {}

  async storeFeatures(features: ProcessedFeatures, config: StoreConfig): Promise<StoredFeatures> {
    const stored = {
      online: {},
      offline: {},
    }

    // Store features based on their access pattern
    for (const [featureName, feature] of Object.entries(features)) {
      const featureConfig = config.features[featureName]

      if (featureConfig.access === 'online') {
        stored.online[featureName] = await this.onlineStore.store(featureName, feature, {
          ttl: featureConfig.ttl || 3600,
          freshness: config.freshness,
        })
      } else {
        stored.offline[featureName] = await this.offlineStore.store(featureName, feature, {
          partitioning: featureConfig.partitioning,
          compression: featureConfig.compression,
        })
      }
    }

    // Update cache
    await this.cacheManager.updateCache(stored.online)

    return {
      ...stored,
      metadata: {
        storedAt: Date.now(),
        config,
      },
    }
  }

  async getFeatures(entityId: string, featureNames: string[]): Promise<FeatureValues> {
    const features = {}
    const cacheHits = []
    const cacheMisses = []

    // Try cache first
    for (const featureName of featureNames) {
      const cached = await this.cacheManager.get(entityId, featureName)
      if (cached !== null) {
        features[featureName] = cached
        cacheHits.push(featureName)
      } else {
        cacheMisses.push(featureName)
      }
    }

    // Fetch from stores for cache misses
    for (const featureName of cacheMisses) {
      const feature = await this.onlineStore.get(entityId, featureName)
      if (feature !== null) {
        features[featureName] = feature
        // Update cache
        await this.cacheManager.set(entityId, featureName, feature)
      }
    }

    return features
  }

  async getBatchFeatures(entityIds: string[], featureNames: string[]): Promise<BatchFeatureValues> {
    const results = {}

    for (const entityId of entityIds) {
      results[entityId] = await this.getFeatures(entityId, featureNames)
    }

    return results
  }
}

// Transformation Engine
export class TransformationEngine {
  private transformations = new Map<string, Transformation>()

  constructor() {
    this.registerDefaultTransformations()
  }

  async createTransformation(config: TransformationConfig): Promise<Transformation> {
    const transformation = this.transformations.get(config.type)
    if (!transformation) {
      throw new Error(`Unknown transformation type: ${config.type}`)
    }

    return transformation.create(config)
  }

  async transform(data: RawData, pipeline: TransformationPipeline): Promise<ProcessedData> {
    let currentData = data

    for (const transformation of pipeline.transformations) {
      currentData = await transformation.transform(currentData)
    }

    return currentData
  }

  private registerDefaultTransformations(): void {
    // Numerical transformations
    this.transformations.set('normalize', new NormalizationTransformation())
    this.transformations.set('standardize', new StandardizationTransformation())
    this.transformations.set('log_transform', new LogTransformation())
    this.transformations.set('binning', new BinningTransformation())

    // Categorical transformations
    this.transformations.set('one_hot_encode', new OneHotEncodingTransformation())
    this.transformations.set('label_encode', new LabelEncodingTransformation())
    this.transformations.set('target_encode', new TargetEncodingTransformation())

    // Text transformations
    this.transformations.set('tokenize', new TokenizationTransformation())
    this.transformations.set('vectorize', new VectorizationTransformation())
    this.transformations.set('stem', new StemmingTransformation())

    // Date/time transformations
    this.transformations.set('extract_date_parts', new DatePartsExtractionTransformation())
    this.transformations.set('calculate_age', new AgeCalculationTransformation())
  }
}

// Feature Validator
export class FeatureValidator {
  async validateInputData(data: RawData): Promise<DataValidationResult> {
    const errors = []
    const warnings = []

    // Check for required fields
    if (!data.samples || data.samples.length === 0) {
      errors.push('No samples provided')
    }

    // Check for consistent schema
    if (data.samples.length > 0) {
      const schema = this.extractSchema(data.samples[0])
      for (let i = 1; i < data.samples.length; i++) {
        const currentSchema = this.extractSchema(data.samples[i])
        if (!this.schemasMatch(schema, currentSchema)) {
          errors.push(`Schema mismatch at sample ${i}`)
        }
      }
    }

    // Check for data quality issues
    const qualityIssues = await this.checkDataQuality(data)
    errors.push(...qualityIssues.errors)
    warnings.push(...qualityIssues.warnings)

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
      schema: data.samples.length > 0 ? this.extractSchema(data.samples[0]) : null,
    }
  }

  async validateFeatureValues(
    feature: any,
    definition: FeatureDefinition
  ): Promise<FeatureValueValidationResult> {
    const errors = []
    const warnings = []

    // Type validation
    if (!this.validateFeatureType(feature, definition.type)) {
      errors.push(`Invalid type: expected ${definition.type}`)
    }

    // Range validation for numerical features
    if (definition.type === 'numerical') {
      if (definition.minValue !== undefined && feature < definition.minValue) {
        errors.push(`Value below minimum: ${feature} < ${definition.minValue}`)
      }
      if (definition.maxValue !== undefined && feature > definition.maxValue) {
        errors.push(`Value above maximum: ${feature} > ${definition.maxValue}`)
      }
    }

    // Allowed values validation for categorical features
    if (definition.type === 'categorical' && definition.allowedValues) {
      if (!definition.allowedValues.includes(feature)) {
        warnings.push(`Value not in allowed values: ${feature}`)
      }
    }

    return {
      isValid: errors.length === 0,
      errors,
      warnings,
    }
  }

  private validateFeatureType(feature: any, expectedType: string): boolean {
    switch (expectedType) {
      case 'numerical':
        return typeof feature === 'number' && !isNaN(feature)
      case 'categorical':
        return typeof feature === 'string'
      case 'text':
        return typeof feature === 'string'
      case 'boolean':
        return typeof feature === 'boolean'
      case 'datetime':
        return (
          feature instanceof Date || (typeof feature === 'string' && !isNaN(Date.parse(feature)))
        )
      case 'array':
        return Array.isArray(feature)
      default:
        return false
    }
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No feature engineering standards
export class BasicFeatureProcessor {
  // BAD: No validation
  async processFeatures(data: any) {
    // BAD: No lineage tracking
    // BAD: No quality monitoring
    // BAD: No freshness management
    return this.transform(data)
  }

  // BAD: No feature store
  // BAD: No transformation validation
  // BAD: No data quality checks
}
```

</example_bad>
