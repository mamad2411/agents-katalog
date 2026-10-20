---
description: Run Global Standards and International Compliance Standards Check
globs:
  ['**/global/**/*.ts', '**/international/**/*.ts', '**/compliance/**/*.ts', '**/standards/**/*.ts']
---

# Future-Proof: Global Standards & International Compliance Standards

<audit_rules>

- You MUST implement proper GDPR compliance with data subject rights and privacy by design.
- You MUST ensure proper CCPA/CPRA compliance with consumer privacy rights and opt-outs.
- You MUST implement proper ISO 27001 information security management system.
- You MUST ensure proper SOC 2 Type II compliance with security controls and attestations.
- You MUST implement proper HIPAA compliance for healthcare data protection.
- You MUST ensure proper PCI DSS compliance for payment card industry standards.
- You MUST implement proper regional compliance (Brazil LGPD, China PIPL, India PDPB).
- You MUST ensure proper accessibility compliance with WCAG 2.1 and Section 508.
- You MUST implement proper environmental compliance with carbon footprint tracking.
- You MUST ensure proper international data transfer compliance with adequacy decisions.
  </audit_rules>

<example_good>

```typescript
// Global Standards Implementation

export class GlobalComplianceOrchestrator {
  constructor(
    private gdprManager: GDPRComplianceManager,
    private ccpaManager: CCPAComplianceManager,
    private iso27001Manager: ISO27001Manager,
    private soc2Manager: SOC2ComplianceManager,
    private hipaaManager: HIPAAComplianceManager,
    private pciDssManager: PCIDSSManager,
    private regionalCompliance: RegionalComplianceManager,
    private accessibilityManager: AccessibilityComplianceManager,
    private environmentalManager: EnvironmentalComplianceManager
  ) {}

  async establishGlobalCompliance(config: GlobalComplianceConfig): Promise<GlobalComplianceSetup> {
    // Initialize GDPR compliance
    const gdprSetup = await this.gdprManager.initialize({
      regions: config.gdpr?.regions || ['EU', 'UK'],
      dataSubjectRights: config.gdpr?.dataSubjectRights || ['access', 'rectification', 'erasure'],
      privacyByDesign: config.gdpr?.privacyByDesign || true,
      dpoRequired: config.gdpr?.dpoRequired || true,
    })

    // Initialize CCPA compliance
    const ccpaSetup = await this.ccpaManager.initialize({
      regions: config.ccpa?.regions || ['California'],
      consumerRights: config.ccpa?.consumerRights || ['know', 'delete', 'opt-out'],
      privacyPolicy: config.ccpa?.privacyPolicy || true,
      doNotSell: config.ccpa?.doNotSell || true,
    })

    // Initialize ISO 27001 compliance
    const iso27001Setup = await this.iso27001Manager.initialize({
      certification: config.iso27001?.certification || true,
      scope: config.iso27001?.scope || 'all_operations',
      riskAssessment: config.iso27001?.riskAssessment || true,
      continuousMonitoring: config.iso27001?.continuousMonitoring || true,
    })

    // Initialize SOC 2 compliance
    const soc2Setup = await this.soc2Manager.initialize({
      type: config.soc2?.type || 'Type II',
      trustServices: config.soc2?.trustServices || ['Security', 'Availability', 'Confidentiality'],
      reportingPeriod: config.soc2?.reportingPeriod || 12,
      attestation: config.soc2?.attestation || true,
    })

    // Initialize HIPAA compliance (if applicable)
    let hipaaSetup = null
    if (config.hipaa?.enabled) {
      hipaaSetup = await this.hipaaManager.initialize({
        coveredEntity: config.hipaa?.coveredEntity || false,
        businessAssociate: config.hipaa?.businessAssociate || false,
        phiProtection: config.hipaa?.phiProtection || true,
        breachNotification: config.hipaa?.breachNotification || true,
      })
    }

    // Initialize PCI DSS compliance (if applicable)
    let pciDssSetup = null
    if (config.pciDss?.enabled) {
      pciDssSetup = await this.pciDssManager.initialize({
        cardholderData: config.pciDss?.cardholderData || false,
        encryption: config.pciDss?.encryption || true,
        accessControl: config.pciDss?.accessControl || true,
        networkSecurity: config.pciDss?.networkSecurity || true,
      })
    }

    // Initialize regional compliance
    const regionalSetup = await this.regionalCompliance.initialize({
      brazil: config.regional?.brazil || false,
      china: config.regional?.china || false,
      india: config.regional?.india || false,
      canada: config.regional?.canada || false,
      australia: config.regional?.australia || false,
    })

    return {
      setupId: generateId(),
      gdprSetup,
      ccpaSetup,
      iso27001Setup,
      soc2Setup,
      hipaaSetup,
      pciDssSetup,
      regionalSetup,
      establishedAt: Date.now(),
    }
  }

  async handleDataSubjectRequest(request: DataSubjectRequest): Promise<DataSubjectResponse> {
    // Identify applicable regulations
    const applicableRegulations = await this.identifyApplicableRegulations(request)

    // Validate request authenticity
    const validation = await this.validateDataSubjectRequest(request, applicableRegulations)
    if (!validation.valid) {
      throw new Error(`Invalid request: ${validation.errors.join(', ')}`)
    }

    // Process request based on type
    let response: DataSubjectResponse

    switch (request.type) {
      case 'access':
        response = await this.handleAccessRequest(request, applicableRegulations)
        break
      case 'rectification':
        response = await this.handleRectificationRequest(request, applicableRegulations)
        break
      case 'erasure':
        response = await this.handleErasureRequest(request, applicableRegulations)
        break
      case 'portability':
        response = await this.handlePortabilityRequest(request, applicableRegulations)
        break
      case 'objection':
        response = await this.handleObjectionRequest(request, applicableRegulations)
        break
      case 'restriction':
        response = await this.handleRestrictionRequest(request, applicableRegulations)
        break
      default:
        throw new Error(`Unknown request type: ${request.type}`)
    }

    // Log request for compliance
    await this.logDataSubjectRequest(request, response, applicableRegulations)

    return response
  }

  async conductComplianceAudit(audit: ComplianceAudit): Promise<ComplianceAuditResult> {
    // Validate audit configuration
    const validation = await this.validateAuditConfig(audit)
    if (!validation.valid) {
      throw new Error(`Invalid audit configuration: ${validation.errors.join(', ')}`)
    }

    const auditResults = {}

    // GDPR audit
    if (audit.frameworks.includes('gdpr')) {
      auditResults.gdpr = await this.gdprManager.conductAudit({
        scope: audit.scope,
        dateRange: audit.dateRange,
        sampleSize: audit.sampleSize,
      })
    }

    // CCPA audit
    if (audit.frameworks.includes('ccpa')) {
      auditResults.ccpa = await this.ccpaManager.conductAudit({
        scope: audit.scope,
        dateRange: audit.dateRange,
        sampleSize: audit.sampleSize,
      })
    }

    // ISO 27001 audit
    if (audit.frameworks.includes('iso27001')) {
      auditResults.iso27001 = await this.iso27001Manager.conductAudit({
        scope: audit.scope,
        controls: audit.iso27001?.controls || 'all',
        evidence: audit.iso27001?.evidence || true,
      })
    }

    // SOC 2 audit
    if (audit.frameworks.includes('soc2')) {
      auditResults.soc2 = await this.soc2Manager.conductAudit({
        scope: audit.scope,
        trustServices: audit.soc2?.trustServices || ['Security'],
        testing: audit.soc2?.testing || true,
      })
    }

    // HIPAA audit
    if (audit.frameworks.includes('hipaa')) {
      auditResults.hipaa = await this.hipaaManager.conductAudit({
        scope: audit.scope,
        phiAudit: audit.hipaa?.phiAudit || true,
        breachAudit: audit.hipaa?.breachAudit || true,
      })
    }

    // PCI DSS audit
    if (audit.frameworks.includes('pciDss')) {
      auditResults.pciDss = await this.pciDssManager.conductAudit({
        scope: audit.scope,
        requirements: audit.pciDss?.requirements || 'all',
        testing: audit.pciDss?.testing || true,
      })
    }

    // Regional compliance audit
    if (audit.frameworks.includes('regional')) {
      auditResults.regional = await this.regionalCompliance.conductAudit({
        scope: audit.scope,
        regions: audit.regional?.regions || ['brazil', 'china', 'india'],
      })
    }

    // Calculate overall compliance score
    const overallScore = this.calculateOverallComplianceScore(auditResults)

    return {
      auditId: audit.id,
      framework: audit.frameworks,
      results: auditResults,
      overallScore,
      findings: this.aggregateFindings(auditResults),
      recommendations: this.generateAuditRecommendations(auditResults),
      auditedAt: Date.now(),
    }
  }

  async manageInternationalDataTransfer(
    transfer: InternationalDataTransfer
  ): Promise<TransferResult> {
    // Validate transfer request
    const validation = await this.validateDataTransfer(transfer)
    if (!validation.valid) {
      throw new Error(`Invalid data transfer: ${validation.errors.join(', ')}`)
    }

    // Check source and destination regulations
    const sourceRegulation = await this.identifySourceRegulation(transfer.sourceCountry)
    const destinationRegulation = await this.identifyDestinationRegulation(
      transfer.destinationCountry
    )

    // Check adequacy decision
    const adequacyCheck = await this.checkAdequacyDecision(transfer.destinationCountry)

    // Apply appropriate transfer mechanism
    let transferMechanism: TransferMechanism

    if (adequacyCheck.adequate) {
      transferMechanism = await this.transferWithAdequacy(transfer)
    } else {
      transferMechanism = await this.transferWithSafeguards(
        transfer,
        sourceRegulation,
        destinationRegulation
      )
    }

    // Execute transfer
    const execution = await this.executeDataTransfer(transfer, transferMechanism)

    // Generate transfer certificate
    const certificate = await this.generateTransferCertificate(transfer, transferMechanism)

    return {
      transferId: transfer.id,
      sourceCountry: transfer.sourceCountry,
      destinationCountry: transfer.destinationCountry,
      mechanism: transferMechanism,
      execution,
      certificate,
      transferredAt: Date.now(),
    }
  }

  async ensureAccessibility(
    accessibilityConfig: AccessibilityConfig
  ): Promise<AccessibilityCompliance> {
    // Validate accessibility configuration
    const validation = await this.validateAccessibilityConfig(accessibilityConfig)
    if (!validation.valid) {
      throw new Error(`Invalid accessibility configuration: ${validation.errors.join(', ')}`)
    }

    // Check WCAG 2.1 compliance
    const wcagCompliance = await this.accessibilityManager.checkWCAGCompliance({
      level: accessibilityConfig.wcagLevel || 'AA',
      guidelines: accessibilityConfig.wcagGuidelines || [
        'perceivable',
        'operable',
        'understandable',
        'robust',
      ],
      testing: accessibilityConfig.testing || true,
    })

    // Check Section 508 compliance
    const section508Compliance = await this.accessibilityManager.checkSection508Compliance({
      scope: accessibilityConfig.section508Scope || 'all',
      testing: accessibilityConfig.testing || true,
    })

    // Generate accessibility report
    const report = await this.generateAccessibilityReport({
      wcagCompliance,
      section508Compliance,
      timestamp: Date.now(),
    })

    return {
      wcagCompliance,
      section508Compliance,
      report,
      overallScore: this.calculateAccessibilityScore(wcagCompliance, section508Compliance),
    }
  }

  async trackEnvironmentalImpact(
    tracking: EnvironmentalTrackingConfig
  ): Promise<EnvironmentalImpact> {
    // Validate tracking configuration
    const validation = await this.validateEnvironmentalTracking(tracking)
    if (!validation.valid) {
      throw new Error(`Invalid environmental tracking: ${validation.errors.join(', ')}`)
    }

    // Calculate carbon footprint
    const carbonFootprint = await this.environmentalManager.calculateCarbonFootprint({
      scope: tracking.scope || ['scope1', 'scope2', 'scope3'],
      period: tracking.period || 'monthly',
      methodology: tracking.methodology || 'ghg_protocol',
    })

    // Track energy consumption
    const energyConsumption = await this.environmentalManager.trackEnergyConsumption({
      sources: tracking.energySources || ['electricity', 'gas', 'renewable'],
      period: tracking.period || 'monthly',
    })

    // Monitor waste generation
    const wasteGeneration = await this.environmentalManager.monitorWaste({
      types: tracking.wasteTypes || ['electronic', 'paper', 'general'],
      period: tracking.period || 'monthly',
      recycling: tracking.recycling || true,
    })

    // Generate environmental report
    const report = await this.generateEnvironmentalReport({
      carbonFootprint,
      energyConsumption,
      wasteGeneration,
      timestamp: Date.now(),
    })

    return {
      carbonFootprint,
      energyConsumption,
      wasteGeneration,
      report,
      sustainabilityScore: this.calculateSustainabilityScore(
        carbonFootprint,
        energyConsumption,
        wasteGeneration
      ),
    }
  }

  private async identifyApplicableRegulations(request: DataSubjectRequest): Promise<string[]> {
    const regulations = []

    // Check GDPR applicability
    if (await this.gdprManager.isApplicable(request)) {
      regulations.push('gdpr')
    }

    // Check CCPA applicability
    if (await this.ccpaManager.isApplicable(request)) {
      regulations.push('ccpa')
    }

    // Check regional regulations
    const regionalRegs = await this.regionalCompliance.getApplicableRegulations(request)
    regulations.push(...regionalRegs)

    return regulations
  }

  private async handleAccessRequest(
    request: DataSubjectRequest,
    regulations: string[]
  ): Promise<DataSubjectResponse> {
    // Collect personal data
    const personalData = await this.collectPersonalData(request.subjectId, regulations)

    // Apply redactions if required
    const redactedData = await this.applyRedactions(personalData, regulations)

    // Format response
    const formattedData = await this.formatDataResponse(redactedData, request.format)

    return {
      requestId: request.id,
      type: 'access',
      data: formattedData,
      format: request.format,
      regulations,
      processedAt: Date.now(),
    }
  }

  private async handleErasureRequest(
    request: DataSubjectRequest,
    regulations: string[]
  ): Promise<DataSubjectResponse> {
    // Identify personal data to erase
    const dataToErase = await this.identifyPersonalData(request.subjectId, regulations)

    // Check for legal holds and retention requirements
    const retentionCheck = await this.checkRetentionRequirements(dataToErase, regulations)

    // Erase data where allowed
    const erasureResult = await this.erasePersonalData(dataToErase, retentionCheck.exemptData)

    // Confirm erasure
    const confirmation = await this.confirmErasure(erasureResult)

    return {
      requestId: request.id,
      type: 'erasure',
      erasedRecords: erasureResult.erasedCount,
      exemptRecords: erasureResult.exemptCount,
      regulations,
      confirmation,
      processedAt: Date.now(),
    }
  }

  private calculateOverallComplianceScore(results: ComplianceAuditResults): number {
    const scores = []

    for (const [framework, result] of Object.entries(results)) {
      if (result.score !== undefined) {
        scores.push(result.score)
      }
    }

    if (scores.length === 0) return 0

    return scores.reduce((sum, score) => sum + score, 0) / scores.length
  }

  private aggregateFindings(results: ComplianceAuditResults): ComplianceFinding[] {
    const findings = []

    for (const [framework, result] of Object.entries(results)) {
      if (result.findings) {
        findings.push(...result.findings.map((f) => ({ ...f, framework })))
      }
    }

    return findings.sort((a, b) => b.severity.localeCompare(a.severity))
  }

  private generateAuditRecommendations(
    results: ComplianceAuditResults
  ): ComplianceRecommendation[] {
    const recommendations = []

    for (const [framework, result] of Object.entries(results)) {
      if (result.recommendations) {
        recommendations.push(...result.recommendations.map((r) => ({ ...r, framework })))
      }
    }

    return recommendations
  }

  private calculateAccessibilityScore(
    wcag: WCAGCompliance,
    section508: Section508Compliance
  ): number {
    const wcagScore = wcag.overallScore || 0
    const section508Score = section508.overallScore || 0

    return (wcagScore + section508Score) / 2
  }

  private calculateSustainabilityScore(
    carbon: CarbonFootprint,
    energy: EnergyConsumption,
    waste: WasteGeneration
  ): number {
    // Calculate sustainability score based on environmental metrics
    const carbonScore = Math.max(0, 1 - carbon.tonsCO2 / 1000) // Normalize against 1000 tons
    const energyScore = Math.max(0, 1 - energy.renewablePercentage / 100) // Higher renewable is better
    const wasteScore = Math.max(0, 1 - waste.recyclingRate / 100) // Higher recycling is better

    return (carbonScore + energyScore + wasteScore) / 3
  }
}

// GDPR Compliance Manager Implementation
export class GDPRComplianceManager {
  constructor(
    private dataProcessor: DataProcessor,
    private consentManager: ConsentManager,
    private breachManager: BreachManager,
    private dpoManager: DPOManager
  ) {}

  async initialize(config: GDPRConfig): Promise<GDPRSetup> {
    // Setup lawful basis processing
    await this.setupLawfulBasis(config.lawfulBasis || ['consent', 'legitimate_interest'])

    // Setup data subject rights
    await this.setupDataSubjectRights(config.dataSubjectRights)

    // Setup privacy by design
    await this.setupPrivacyByDesign(config.privacyByDesign)

    // Setup DPO if required
    if (config.dpoRequired) {
      await this.dpoManager.setup()
    }

    return {
      config,
      lawfulBasis: config.lawfulBasis,
      dataSubjectRights: config.dataSubjectRights,
      privacyByDesign: config.privacyByDesign,
      dpoAppointed: config.dpoRequired,
      initializedAt: Date.now(),
    }
  }

  async isApplicable(request: DataSubjectRequest): Promise<boolean> {
    // Check if request is from EU/UK resident
    const isEUResident = await this.checkEUResidency(request)

    // Check if processing occurs in EU/UK
    const isEUProcessing = await this.checkEUProcessing(request)

    // Check if goods/services offered to EU/UK
    const isEUTargeted = await this.checkEUTargeting(request)

    return isEUResident || isEUProcessing || isEUTargeted
  }

  async conductAudit(audit: GDPRAuditConfig): Promise<GDPRAuditResult> {
    const results = {
      lawfulBasis: await this.auditLawfulBasis(audit.scope),
      consentManagement: await this.auditConsentManagement(audit.scope),
      dataSubjectRights: await this.auditDataSubjectRights(audit.scope),
      breachProcedures: await this.auditBreachProcedures(audit.scope),
      privacyByDesign: await this.auditPrivacyByDesign(audit.scope),
      internationalTransfers: await this.auditInternationalTransfers(audit.scope),
    }

    const score = this.calculateGDPRScore(results)
    const findings = this.aggregateGDPRFindings(results)
    const recommendations = this.generateGDPRRecommendations(results)

    return {
      ...results,
      score,
      findings,
      recommendations,
      auditedAt: Date.now(),
    }
  }

  private async setupLawfulBasis(bases: LawfulBasis[]): Promise<void> {
    for (const basis of bases) {
      await this.dataProcessor.setupLawfulBasis(basis)
    }
  }

  private async setupDataSubjectRights(rights: DataSubjectRight[]): Promise<void> {
    for (const right of rights) {
      await this.dataProcessor.setupDataSubjectRight(right)
    }
  }

  private async setupPrivacyByDesign(enabled: boolean): Promise<void> {
    if (enabled) {
      await this.dataProcessor.enablePrivacyByDesign()
    }
  }

  private calculateGDPRScore(results: GDPAuditResults): number {
    const scores = [
      results.lawfulBasis.score,
      results.consentManagement.score,
      results.dataSubjectRights.score,
      results.breachProcedures.score,
      results.privacyByDesign.score,
      results.internationalTransfers.score,
    ]

    return scores.reduce((sum, score) => sum + score, 0) / scores.length
  }
}

// CCPA Compliance Manager Implementation
export class CCPAComplianceManager {
  constructor(
    private privacyManager: PrivacyManager,
    private consumerRightsManager: ConsumerRightsManager,
    private optOutManager: OptOutManager
  ) {}

  async initialize(config: CCPAConfig): Promise<CCPASetup> {
    // Setup consumer privacy rights
    await this.setupConsumerRights(config.consumerRights)

    // Setup "Do Not Sell" mechanism
    if (config.doNotSell) {
      await this.optOutManager.setupDoNotSell()
    }

    // Setup privacy policy
    if (config.privacyPolicy) {
      await this.privacyManager.setupPrivacyPolicy()
    }

    return {
      config,
      consumerRights: config.consumerRights,
      doNotSell: config.doNotSell,
      privacyPolicy: config.privacyPolicy,
      initializedAt: Date.now(),
    }
  }

  async isApplicable(request: DataSubjectRequest): Promise<boolean> {
    // Check if request is from California resident
    const isCaliforniaResident = await this.checkCaliforniaResidency(request)

    // Check if business operates in California
    const isCaliforniaBusiness = await this.checkCaliforniaBusiness()

    // Check if meets revenue/data thresholds
    const meetsThresholds = await this.checkThresholds()

    return isCaliforniaResident && isCaliforniaBusiness && meetsThresholds
  }

  async conductAudit(audit: CCPAAuditConfig): Promise<CCPAAuditResult> {
    const results = {
      consumerRights: await this.auditConsumerRights(audit.scope),
      doNotSell: await this.auditDoNotSell(audit.scope),
      privacyPolicy: await this.auditPrivacyPolicy(audit.scope),
      dataMinimization: await this.auditDataMinimization(audit.scope),
      nonDiscrimination: await this.auditNonDiscrimination(audit.scope),
    }

    const score = this.calculateCCPAScore(results)
    const findings = this.aggregateCCPAFindings(results)
    const recommendations = this.generateCCPARecommendations(results)

    return {
      ...results,
      score,
      findings,
      recommendations,
      auditedAt: Date.now(),
    }
  }

  private async setupConsumerRights(rights: ConsumerRight[]): Promise<void> {
    for (const right of rights) {
      await this.consumerRightsManager.setupRight(right)
    }
  }

  private calculateCCPAScore(results: CCPAAuditResults): number {
    const scores = [
      results.consumerRights.score,
      results.doNotSell.score,
      results.privacyPolicy.score,
      results.dataMinimization.score,
      results.nonDiscrimination.score,
    ]

    return scores.reduce((sum, score) => sum + score, 0) / scores.length
  }
}

// ISO 27001 Manager Implementation
export class ISO27001Manager {
  constructor(
    private ismsManager: ISMSManager,
    private riskManager: RiskManager,
    private controlManager: ControlManager
  ) {}

  async initialize(config: ISO27001Config): Promise<ISO27001Setup> {
    // Establish ISMS
    await this.ismsManager.establish({
      scope: config.scope,
      informationSecurityPolicy: true,
      riskAssessment: config.riskAssessment,
      statementOfApplicability: true,
    })

    // Setup controls
    await this.controlManager.setupControls({
      annexA: true,
      customControls: config.customControls || [],
      implementation: true,
    })

    return {
      config,
      isms: await this.ismsManager.getStatus(),
      controls: await this.controlManager.getControls(),
      initializedAt: Date.now(),
    }
  }

  async conductAudit(audit: ISO27001AuditConfig): Promise<ISO27001AuditResult> {
    const results = {
      isms: await this.auditISMS(audit.scope),
      controls: await this.auditControls(audit.controls),
      riskManagement: await this.auditRiskManagement(audit.scope),
      documentation: await this.auditDocumentation(audit.scope),
    }

    const score = this.calculateISO27001Score(results)
    const findings = this.aggregateISO27001Findings(results)
    const recommendations = this.generateISO27001Recommendations(results)

    return {
      ...results,
      score,
      findings,
      recommendations,
      auditedAt: Date.now(),
    }
  }

  private calculateISO27001Score(results: ISO27001AuditResults): number {
    const scores = [
      results.isms.score,
      results.controls.score,
      results.riskManagement.score,
      results.documentation.score,
    ]

    return scores.reduce((sum, score) => sum + score, 0) / scores.length
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No global standards implementation
export class BasicCompliance {
  // BAD: No GDPR compliance
  async processData(data: any) {
    // BAD: No CCPA compliance
    // BAD: No ISO 27001
    // BAD: No SOC 2
    return this.store(data)
  }

  // BAD: No international data transfer
  // BAD: No accessibility compliance
  // BAD: No environmental tracking
  // BAD: No regional compliance
}
```

</example_bad>
