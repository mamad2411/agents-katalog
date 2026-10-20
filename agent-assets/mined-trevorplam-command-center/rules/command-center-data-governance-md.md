---
description: Run Data Governance and Data Quality Standards Check
globs:
  [
    '**/governance/**/*.ts',
    '**/data-quality/**/*.ts',
    '**/data-catalog/**/*.ts',
    '**/data-lineage/**/*.ts',
  ]
---

# Data: Data Governance & Data Quality Standards

<audit_rules>

- You MUST implement proper data cataloging with metadata management and business context.
- You MUST ensure data lineage tracking with end-to-end data flow visualization.
- You MUST implement proper data quality monitoring with automated validation rules.
- You MUST configure proper data classification and sensitivity labeling.
- You MUST ensure proper data retention policies and automated deletion workflows.
- You MUST implement proper data access controls with role-based permissions.
- You MUST configure proper data privacy controls with GDPR/CCPA compliance.
- You MUST ensure proper data governance policies with automated enforcement.
- You MUST implement proper data stewardship workflows and ownership tracking.
- You MUST ensure proper data quality metrics and KPI monitoring dashboards.
  </audit_rules>

<example_good>

```typescript
// Data Governance Implementation

export class DataGovernanceOrchestrator {
  constructor(
    private dataCatalog: DataCatalog,
    private dataLineageTracker: DataLineageTracker,
    private dataQualityMonitor: DataQualityMonitor,
    private dataClassifier: DataClassifier,
    private accessController: DataAccessController,
    private retentionManager: DataRetentionManager,
    private complianceEngine: ComplianceEngine,
    private stewardshipManager: StewardshipManager
  ) {}

  async onboardDataset(dataset: DatasetOnboardingRequest): Promise<OnboardingResult> {
    // Validate dataset metadata
    const metadataValidation = await this.validateDatasetMetadata(dataset)
    if (!metadataValidation.valid) {
      throw new Error(`Metadata validation failed: ${metadataValidation.errors.join(', ')}`)
    }

    // Classify data sensitivity
    const classification = await this.dataClassifier.classify(dataset.data, {
      autoClassify: true,
      manualOverride: dataset.classification,
    })

    // Create data catalog entry
    const catalogEntry = await this.dataCatalog.createEntry({
      name: dataset.name,
      description: dataset.description,
      owner: dataset.owner,
      steward: dataset.steward,
      classification,
      schema: dataset.schema,
      tags: dataset.tags,
      businessContext: dataset.businessContext,
    })

    // Setup data lineage tracking
    const lineageConfig = await this.dataLineageTracker.setupLineage({
      datasetId: catalogEntry.id,
      sources: dataset.sources,
      transformations: dataset.transformations,
      destinations: dataset.destinations,
    })

    // Configure data quality monitoring
    const qualityConfig = await this.dataQualityMonitor.setupMonitoring({
      datasetId: catalogEntry.id,
      rules: dataset.qualityRules || this.getDefaultQualityRules(classification),
      schedule: dataset.qualitySchedule || 'daily',
    })

    // Setup access controls
    const accessConfig = await this.accessController.setupAccess({
      datasetId: catalogEntry.id,
      permissions: dataset.permissions || this.getDefaultPermissions(classification),
      approvalWorkflow: dataset.approvalWorkflow,
    })

    // Configure retention policy
    const retentionConfig = await this.retentionManager.setupRetentionPolicy({
      datasetId: catalogEntry.id,
      retentionPeriod: dataset.retentionPeriod || this.getDefaultRetentionPeriod(classification),
      archivalPolicy: dataset.archivalPolicy,
    })

    // Check compliance
    const complianceCheck = await this.complianceEngine.checkCompliance(
      catalogEntry,
      dataset.regulations
    )

    return {
      catalogEntry,
      lineage: lineageConfig,
      quality: qualityConfig,
      access: accessConfig,
      retention: retentionConfig,
      compliance: complianceCheck,
      status: 'active',
    }
  }

  async monitorDataQuality(datasetId: string): Promise<DataQualityReport> {
    // Get current quality metrics
    const currentMetrics = await this.dataQualityMonitor.getCurrentMetrics(datasetId)

    // Get quality trends
    const trends = await this.dataQualityMonitor.getQualityTrends(datasetId, '30d')

    // Get quality incidents
    const incidents = await this.dataQualityMonitor.getIncidents(datasetId, '7d')

    // Analyze quality issues
    const issueAnalysis = await this.analyzeQualityIssues(currentMetrics, incidents)

    // Generate quality recommendations
    const recommendations = await this.generateQualityRecommendations(
      currentMetrics,
      trends,
      incidents
    )

    return {
      datasetId,
      timestamp: Date.now(),
      overallScore: currentMetrics.overallScore,
      metrics: currentMetrics.dimensions,
      trends,
      incidents,
      issueAnalysis,
      recommendations,
      status: this.calculateQualityStatus(currentMetrics.overallScore),
    }
  }

  async trackDataLineage(datasetId: string, query: LineageQuery): Promise<LineageResult> {
    // Get lineage graph
    const lineageGraph = await this.dataLineageTracker.getLineageGraph(datasetId, query)

    // Analyze data flow
    const dataFlow = await this.analyzeDataFlow(lineageGraph, query)

    // Identify impact analysis
    const impactAnalysis = await this.performImpactAnalysis(datasetId, lineageGraph)

    // Get transformation details
    const transformations = await this.getTransformationDetails(lineageGraph)

    return {
      datasetId,
      query,
      graph: lineageGraph,
      dataFlow,
      impactAnalysis,
      transformations,
      timestamp: Date.now(),
    }
  }

  async enforceDataAccess(request: DataAccessRequest): Promise<AccessDecision> {
    // Authenticate user
    const authResult = await this.authenticateUser(request.user)
    if (!authResult.success) {
      return { allowed: false, reason: 'Authentication failed' }
    }

    // Check data classification
    const dataset = await this.dataCatalog.getDataset(request.datasetId)
    if (!dataset) {
      return { allowed: false, reason: 'Dataset not found' }
    }

    // Evaluate access policies
    const policyEvaluation = await this.accessController.evaluatePolicies({
      user: authResult.user,
      dataset,
      requestedAccess: request.accessType,
      context: request.context,
    })

    // Check compliance requirements
    const complianceCheck = await this.complianceEngine.checkAccessCompliance({
      user: authResult.user,
      dataset,
      accessType: request.accessType,
      jurisdiction: request.context.jurisdiction,
    })

    // Make access decision
    const decision = this.makeAccessDecision(policyEvaluation, complianceCheck)

    // Log access attempt
    await this.logAccessAttempt(request, decision)

    return decision
  }

  async manageDataRetention(datasetId: string): Promise<RetentionReport> {
    // Get retention policy
    const policy = await this.retentionManager.getRetentionPolicy(datasetId)

    // Identify data for retention actions
    const retentionActions = await this.identifyRetentionActions(datasetId, policy)

    // Execute retention actions
    const executionResults = await this.executeRetentionActions(retentionActions)

    // Generate retention report
    const report = await this.generateRetentionReport(datasetId, policy, executionResults)

    return report
  }

  async ensureCompliance(datasetId: string, regulations: string[]): Promise<ComplianceReport> {
    // Get dataset information
    const dataset = await this.dataCatalog.getDataset(datasetId)

    // Check compliance for each regulation
    const complianceResults = []

    for (const regulation of regulations) {
      const result = await this.complianceEngine.checkRegulationCompliance(dataset, regulation)
      complianceResults.push(result)
    }

    // Analyze compliance gaps
    const gaps = await this.analyzeComplianceGaps(complianceResults)

    // Generate remediation plan
    const remediationPlan = await this.generateRemediationPlan(gaps)

    return {
      datasetId,
      regulations,
      results: complianceResults,
      overallCompliance: this.calculateOverallCompliance(complianceResults),
      gaps,
      remediationPlan,
      timestamp: Date.now(),
    }
  }

  async manageStewardship(datasetId: string): Promise<StewardshipReport> {
    // Get stewardship information
    const stewardship = await this.stewardshipManager.getStewardship(datasetId)

    // Check steward responsibilities
    const responsibilityCheck = await this.checkStewardResponsibilities(stewardship)

    // Get steward activity metrics
    const activityMetrics = await this.stewardshipManager.getActivityMetrics(datasetId)

    // Identify stewardship gaps
    const gaps = await this.identifyStewardshipGaps(stewardship, activityMetrics)

    // Generate stewardship recommendations
    const recommendations = await this.generateStewardshipRecommendations(gaps)

    return {
      datasetId,
      stewardship,
      responsibilityCheck,
      activityMetrics,
      gaps,
      recommendations,
      timestamp: Date.now(),
    }
  }

  private async validateDatasetMetadata(
    dataset: DatasetOnboardingRequest
  ): Promise<ValidationResult> {
    const errors = []

    // Required fields
    if (!dataset.name) errors.push('Dataset name is required')
    if (!dataset.owner) errors.push('Dataset owner is required')
    if (!dataset.schema) errors.push('Dataset schema is required')

    // Schema validation
    if (dataset.schema) {
      const schemaValidation = await this.validateSchema(dataset.schema)
      if (!schemaValidation.valid) {
        errors.push(...schemaValidation.errors)
      }
    }

    // Business context validation
    if (dataset.businessContext) {
      const contextValidation = await this.validateBusinessContext(dataset.businessContext)
      if (!contextValidation.valid) {
        errors.push(...contextValidation.errors)
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    }
  }

  private async analyzeQualityIssues(
    metrics: DataQualityMetrics,
    incidents: QualityIncident[]
  ): Promise<QualityIssueAnalysis> {
    const analysis = {
      criticalIssues: [],
      recurringIssues: [],
      trendAnalysis: {},
      impactAssessment: {},
    }

    // Identify critical issues
    for (const [dimension, metric] of Object.entries(metrics.dimensions)) {
      if (metric.score < 0.7) {
        // Below 70% threshold
        analysis.criticalIssues.push({
          dimension,
          score: metric.score,
          issues: metric.issues,
          impact: this.assessDimensionImpact(dimension, metric.score),
        })
      }
    }

    // Identify recurring issues
    const recurringIncidents = this.groupRecurringIncidents(incidents)
    analysis.recurringIssues = recurringIncidents

    // Analyze trends
    analysis.trendAnalysis = await this.analyzeQualityTrends(metrics)

    return analysis
  }

  private async generateQualityRecommendations(
    metrics: DataQualityMetrics,
    trends: QualityTrend,
    incidents: QualityIncident[]
  ): Promise<QualityRecommendation[]> {
    const recommendations = []

    // Dimension-specific recommendations
    for (const [dimension, metric] of Object.entries(metrics.dimensions)) {
      if (metric.score < 0.8) {
        recommendations.push({
          dimension,
          priority: metric.score < 0.5 ? 'high' : 'medium',
          action: this.getDimensionRecommendation(dimension, metric),
          expectedImprovement: this.calculateExpectedImprovement(dimension, metric.score),
        })
      }
    }

    // Trend-based recommendations
    if (trends.direction === 'decreasing') {
      recommendations.push({
        dimension: 'overall',
        priority: 'high',
        action: 'Implement proactive quality monitoring',
        expectedImprovement: 0.15,
      })
    }

    // Incident-based recommendations
    const frequentIncidents = incidents.filter((i) => i.frequency > 5)
    if (frequentIncidents.length > 0) {
      recommendations.push({
        dimension: 'reliability',
        priority: 'medium',
        action: 'Address root causes of frequent quality incidents',
        expectedImprovement: 0.1,
      })
    }

    return recommendations
  }

  private makeAccessDecision(
    policyEval: PolicyEvaluation,
    complianceCheck: ComplianceCheck
  ): AccessDecision {
    if (!policyEval.allowed) {
      return {
        allowed: false,
        reason: policyEval.reason,
        policies: policyEval.evaluatedPolicies,
      }
    }

    if (!complianceCheck.compliant) {
      return {
        allowed: false,
        reason: complianceCheck.reason,
        complianceIssues: complianceCheck.issues,
      }
    }

    return {
      allowed: true,
      reason: 'Access granted',
      policies: policyEval.evaluatedPolicies,
      conditions: policyEval.conditions,
      expiresAt: policyEval.expiresAt,
    }
  }

  private calculateQualityStatus(score: number): QualityStatus {
    if (score >= 0.9) return 'excellent'
    if (score >= 0.8) return 'good'
    if (score >= 0.7) return 'fair'
    if (score >= 0.6) return 'poor'
    return 'critical'
  }

  private calculateOverallCompliance(results: RegulationComplianceResult[]): ComplianceLevel {
    const compliantCount = results.filter((r) => r.compliant).length
    const complianceRatio = compliantCount / results.length

    if (complianceRatio >= 0.95) return 'fully_compliant'
    if (complianceRatio >= 0.8) return 'mostly_compliant'
    if (complianceRatio >= 0.6) return 'partially_compliant'
    return 'non_compliant'
  }
}

// Data Catalog Implementation
export class DataCatalog {
  constructor(
    private metadataStore: MetadataStore,
    private searchEngine: CatalogSearchEngine,
    private tagManager: TagManager
  ) {}

  async createEntry(entry: CatalogEntryCreation): Promise<CatalogEntry> {
    // Validate entry
    await this.validateEntry(entry)

    // Store metadata
    const storedEntry = await this.metadataStore.create({
      name: entry.name,
      description: entry.description,
      owner: entry.owner,
      steward: entry.steward,
      classification: entry.classification,
      schema: entry.schema,
      tags: entry.tags,
      businessContext: entry.businessContext,
      createdAt: Date.now(),
      updatedAt: Date.now(),
    })

    // Index for search
    await this.searchEngine.index(storedEntry)

    // Process tags
    if (entry.tags) {
      await this.tagManager.associateTags(storedEntry.id, entry.tags)
    }

    return storedEntry
  }

  async search(query: CatalogSearchQuery): Promise<CatalogSearchResult> {
    return await this.searchEngine.search(query)
  }

  async getDataset(datasetId: string): Promise<CatalogEntry | null> {
    return await this.metadataStore.getById(datasetId)
  }

  async updateDataset(datasetId: string, updates: CatalogEntryUpdate): Promise<CatalogEntry> {
    const existing = await this.metadataStore.getById(datasetId)
    if (!existing) {
      throw new Error(`Dataset not found: ${datasetId}`)
    }

    const updated = await this.metadataStore.update(datasetId, {
      ...updates,
      updatedAt: Date.now(),
    })

    // Reindex for search
    await this.searchEngine.reindex(updated)

    return updated
  }

  private async validateEntry(entry: CatalogEntryCreation): Promise<void> {
    // Validate required fields
    if (!entry.name || entry.name.trim().length === 0) {
      throw new Error('Dataset name is required')
    }

    if (!entry.owner) {
      throw new Error('Dataset owner is required')
    }

    // Validate name uniqueness
    const existing = await this.metadataStore.findByName(entry.name)
    if (existing) {
      throw new Error(`Dataset with name '${entry.name}' already exists`)
    }

    // Validate schema
    if (entry.schema) {
      await this.validateSchema(entry.schema)
    }

    // Validate classification
    if (entry.classification) {
      await this.validateClassification(entry.classification)
    }
  }

  private async validateSchema(schema: DataSchema): Promise<void> {
    // Validate schema structure
    if (!schema.fields || schema.fields.length === 0) {
      throw new Error('Schema must have at least one field')
    }

    // Validate field definitions
    for (const field of schema.fields) {
      if (!field.name || field.name.trim().length === 0) {
        throw new Error('All schema fields must have a name')
      }

      if (!field.type) {
        throw new Error(`Field '${field.name}' must have a type`)
      }

      if (!this.isValidDataType(field.type)) {
        throw new Error(`Invalid data type for field '${field.name}': ${field.type}`)
      }
    }
  }

  private isValidDataType(type: string): boolean {
    const validTypes = [
      'string',
      'integer',
      'float',
      'boolean',
      'date',
      'datetime',
      'array',
      'object',
      'binary',
      'text',
      'json',
      'uuid',
    ]
    return validTypes.includes(type)
  }
}

// Data Lineage Tracker Implementation
export class DataLineageTracker {
  constructor(
    private lineageStore: LineageStore,
    private graphProcessor: LineageGraphProcessor
  ) {}

  async setupLineage(config: LineageConfig): Promise<LineageSetup> {
    // Create lineage graph
    const graph = await this.createLineageGraph(config)

    // Store lineage configuration
    const stored = await this.lineageStore.create({
      datasetId: config.datasetId,
      sources: config.sources,
      transformations: config.transformations,
      destinations: config.destinations,
      graph,
      createdAt: Date.now(),
    })

    return {
      lineageId: stored.id,
      graph,
      status: 'active',
    }
  }

  async getLineageGraph(datasetId: string, query: LineageQuery): Promise<LineageGraph> {
    const lineage = await this.lineageStore.getByDatasetId(datasetId)
    if (!lineage) {
      throw new Error(`No lineage found for dataset: ${datasetId}`)
    }

    // Filter graph based on query
    const filteredGraph = await this.graphProcessor.filter(lineage.graph, query)

    return filteredGraph
  }

  async updateLineage(datasetId: string, update: LineageUpdate): Promise<void> {
    const lineage = await this.lineageStore.getByDatasetId(datasetId)
    if (!lineage) {
      throw new Error(`No lineage found for dataset: ${datasetId}`)
    }

    // Update graph
    const updatedGraph = await this.graphProcessor.update(lineage.graph, update)

    // Store updated lineage
    await this.lineageStore.update(lineage.id, {
      graph: updatedGraph,
      updatedAt: Date.now(),
    })
  }

  private async createLineageGraph(config: LineageConfig): Promise<LineageGraph> {
    const nodes = []
    const edges = []

    // Add dataset node
    nodes.push({
      id: config.datasetId,
      type: 'dataset',
      name: config.datasetId,
      metadata: {},
    })

    // Add source nodes and edges
    for (const source of config.sources) {
      nodes.push({
        id: source.id,
        type: 'source',
        name: source.name,
        metadata: source.metadata,
      })

      edges.push({
        from: source.id,
        to: config.datasetId,
        type: 'data_flow',
        metadata: source.flowMetadata,
      })
    }

    // Add transformation nodes and edges
    for (const transformation of config.transformations) {
      nodes.push({
        id: transformation.id,
        type: 'transformation',
        name: transformation.name,
        metadata: transformation.metadata,
      })

      edges.push({
        from: transformation.input,
        to: transformation.output,
        type: 'transformation',
        metadata: transformation.transformationMetadata,
      })
    }

    // Add destination nodes and edges
    for (const destination of config.destinations) {
      nodes.push({
        id: destination.id,
        type: 'destination',
        name: destination.name,
        metadata: destination.metadata,
      })

      edges.push({
        from: config.datasetId,
        to: destination.id,
        type: 'data_flow',
        metadata: destination.flowMetadata,
      })
    }

    return {
      nodes,
      edges,
      metadata: {
        createdAt: Date.now(),
        version: '1.0',
      },
    }
  }
}

// Data Quality Monitor Implementation
export class DataQualityMonitor {
  constructor(
    private qualityStore: QualityStore,
    private ruleEngine: QualityRuleEngine,
    private metricsCollector: MetricsCollector
  ) {}

  async setupMonitoring(config: QualityMonitoringConfig): Promise<QualityMonitoringSetup> {
    // Validate quality rules
    await this.validateQualityRules(config.rules)

    // Create monitoring configuration
    const monitoring = await this.qualityStore.create({
      datasetId: config.datasetId,
      rules: config.rules,
      schedule: config.schedule,
      enabled: true,
      createdAt: Date.now(),
    })

    // Schedule quality checks
    await this.scheduleQualityChecks(monitoring)

    return {
      monitoringId: monitoring.id,
      rules: config.rules,
      schedule: config.schedule,
      status: 'active',
    }
  }

  async getCurrentMetrics(datasetId: string): Promise<DataQualityMetrics> {
    const latest = await this.qualityStore.getLatestMetrics(datasetId)

    if (!latest) {
      throw new Error(`No quality metrics found for dataset: ${datasetId}`)
    }

    return {
      overallScore: latest.overallScore,
      dimensions: latest.dimensions,
      timestamp: latest.timestamp,
      recordCount: latest.recordCount,
    }
  }

  async runQualityCheck(datasetId: string): Promise<QualityCheckResult> {
    // Get monitoring configuration
    const monitoring = await this.qualityStore.getByDatasetId(datasetId)
    if (!monitoring) {
      throw new Error(`No quality monitoring configured for dataset: ${datasetId}`)
    }

    // Execute quality rules
    const ruleResults = await this.ruleEngine.executeRules(monitoring.rules, datasetId)

    // Calculate metrics
    const metrics = await this.calculateQualityMetrics(ruleResults)

    // Store results
    await this.qualityStore.storeMetrics(datasetId, {
      ...metrics,
      ruleResults,
      timestamp: Date.now(),
    })

    return {
      datasetId,
      metrics,
      ruleResults,
      timestamp: Date.now(),
    }
  }

  private async calculateQualityMetrics(
    ruleResults: QualityRuleResult[]
  ): Promise<DataQualityMetrics> {
    const dimensions = {}
    let totalScore = 0
    let dimensionCount = 0

    // Group results by dimension
    const resultsByDimension = this.groupResultsByDimension(ruleResults)

    // Calculate dimension scores
    for (const [dimension, results] of Object.entries(resultsByDimension)) {
      const dimensionScore = this.calculateDimensionScore(results)
      dimensions[dimension] = {
        score: dimensionScore,
        issues: results.filter((r) => !r.passed).map((r) => r.issue),
        rules: results.length,
        passed: results.filter((r) => r.passed).length,
      }

      totalScore += dimensionScore
      dimensionCount++
    }

    const overallScore = dimensionCount > 0 ? totalScore / dimensionCount : 0

    return {
      overallScore,
      dimensions,
      timestamp: Date.now(),
      recordCount: this.getTotalRecordCount(ruleResults),
    }
  }

  private calculateDimensionScore(results: QualityRuleResult[]): number {
    if (results.length === 0) return 1.0

    const passedCount = results.filter((r) => r.passed).length
    return passedCount / results.length
  }

  private groupResultsByDimension(
    results: QualityRuleResult[]
  ): Record<string, QualityRuleResult[]> {
    const grouped = {}

    for (const result of results) {
      const dimension = result.dimension || 'general'
      if (!grouped[dimension]) {
        grouped[dimension] = []
      }
      grouped[dimension].push(result)
    }

    return grouped
  }

  private getTotalRecordCount(results: QualityRuleResult[]): number {
    // Return the maximum record count from all rules
    return Math.max(...results.map((r) => r.recordCount || 0))
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No data governance implementation
export class BasicDataService {
  // BAD: No data catalog
  async storeData(data: any) {
    // BAD: No lineage tracking
    // BAD: No quality monitoring
    // BAD: No access controls
    return this.database.save(data)
  }

  // BAD: No retention policies
  // BAD: No compliance checking
  // BAD: No stewardship management
  // BAD: No metadata management
}
```

</example_bad>
