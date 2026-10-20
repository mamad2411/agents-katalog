---
description: Run Data Privacy Engineering and Data Protection Standards Check
globs: ["**/privacy-engineering/**/*.ts", "**/data-protection/**/*.ts", "**/gdpr/**/*.ts", "**/ccpa/**/*.ts"]
---
# Data: Data Privacy Engineering & Data Protection Standards

<audit_rules>
- You MUST implement proper privacy by design with privacy impact assessments.
- You MUST ensure proper data minimization with purpose limitation controls.
- You MUST implement proper consent management with granular consent tracking.
- You MUST configure proper data anonymization with irreversible pseudonymization.
- You MUST ensure proper data subject rights implementation (access, rectification, erasure).
- You MUST implement proper cross-border data transfer compliance with adequacy decisions.
- You MUST configure proper privacy-enhancing technologies integration.
- You MUST ensure proper data breach detection and notification workflows.
- You MUST implement proper privacy policy enforcement and automated compliance.
- You MUST ensure proper data protection officer (DPO) oversight and reporting.
</audit_rules>

<example_good>
```typescript
// Data Privacy Engineering Implementation

export class DataPrivacyEngineer {
  constructor(
    private privacyImpactAssessor: PrivacyImpactAssessor,
    private consentManager: ConsentManager,
    private dataMinimizer: DataMinimizer,
    private anonymizationEngine: AnonymizationEngine,
    private subjectRightsManager: SubjectRightsManager,
    private crossBorderController: CrossBorderController,
    private breachDetector: BreachDetector,
    private privacyPolicyEngine: PrivacyPolicyEngine,
    private dpoOversight: DPOOversight
  ) {}

  async implementPrivacyByDesign(system: SystemDesign): Promise<PrivacyByDesignResult> {
    // Conduct Privacy Impact Assessment (PIA)
    const pia = await this.privacyImpactAssessor.conductPIA(system);
    
    if (pia.riskLevel === 'high') {
      // Require additional safeguards
      await this.implementAdditionalSafeguards(system, pia.recommendations);
    }

    // Implement privacy controls
    const controls = await this.implementPrivacyControls(system, pia);

    // Setup consent management
    const consentSetup = await this.consentManager.setupConsentSystem({
      systemId: system.id,
      consentTypes: pia.requiredConsents,
      granularity: 'fine-grained',
      withdrawal: true,
    });

    // Configure data minimization
    const minimizationConfig = await this.dataMinimizer.configureMinimization({
      systemId: system.id,
      dataFlows: system.dataFlows,
      minimizationRules: pia.minimizationRules,
    });

    return {
      systemId: system.id,
      pia,
      controls,
      consentSetup,
      minimizationConfig,
      privacyLevel: this.calculatePrivacyLevel(pia, controls),
    };
  }

  async manageConsent(consentRequest: ConsentRequest): Promise<ConsentResult> {
    // Validate consent request
    const validation = await this.consentManager.validateRequest(consentRequest);
    if (!validation.valid) {
      throw new Error(`Invalid consent request: ${validation.errors.join(', ')}`);
    }

    // Record consent
    const consentRecord = await this.consentManager.recordConsent({
      userId: consentRequest.userId,
      consentType: consentRequest.consentType,
      purpose: consentRequest.purpose,
      dataCategories: consentRequest.dataCategories,
      duration: consentRequest.duration,
      granted: consentRequest.granted,
      timestamp: Date.now(),
      ipAddress: consentRequest.context.ipAddress,
      userAgent: consentRequest.context.userAgent,
    });

    // Update consent preferences
    await this.consentManager.updatePreferences(consentRequest.userId, {
      [consentRequest.consentType]: {
        granted: consentRequest.granted,
        timestamp: consentRecord.timestamp,
        duration: consentRequest.duration,
      },
    });

    // Trigger data processing actions based on consent
    if (consentRequest.granted) {
      await this.enableDataProcessing(consentRequest);
    } else {
      await this.disableDataProcessing(consentRequest);
    }

    return {
      consentId: consentRecord.id,
      granted: consentRequest.granted,
      timestamp: consentRecord.timestamp,
      expiryDate: consentRequest.duration ? new Date(Date.now() + consentRequest.duration) : null,
    };
  }

  async minimizeData(dataFlow: DataFlow, purpose: string): Promise<MinimizedDataFlow> {
    // Get minimization rules for purpose
    const rules = await this.dataMinimizer.getRulesForPurpose(purpose);
    
    // Apply minimization to data flow
    const minimizedFlow = await this.dataMinimizer.applyMinimization(dataFlow, rules);
    
    // Validate minimization result
    const validation = await this.validateMinimization(minimizedFlow, purpose);
    if (!validation.valid) {
      throw new Error(`Minimization validation failed: ${validation.errors.join(', ')}`);
    }

    // Generate minimization report
    const report = await this.generateMinimizationReport(dataFlow, minimizedFlow);

    return {
      ...minimizedFlow,
      minimizationReport: report,
      dataReduction: this.calculateDataReduction(dataFlow, minimizedFlow),
    };
  }

  async anonymizePersonalData(data: PersonalData, config: AnonymizationConfig): Promise<AnonymizedData> {
    // Validate anonymization requirements
    const validation = await this.validateAnonymizationConfig(config);
    if (!validation.valid) {
      throw new Error(`Invalid anonymization config: ${validation.errors.join(', ')}`);
    }

    // Identify personal data elements
    const personalElements = await this.identifyPersonalElements(data);
    
    // Apply anonymization techniques
    const anonymizedData = await this.anonymizationEngine.anonymize(data, {
      techniques: config.techniques,
      personalElements,
      irreversibility: config.irreversibility || true,
      utility: config.utility || 'high',
    });

    // Verify anonymization quality
    const qualityCheck = await this.verifyAnonymizationQuality(anonymizedData, config);
    if (!qualityCheck.sufficient) {
      throw new Error(`Anonymization quality insufficient: ${qualityCheck.issues.join(', ')}`);
    }

    // Generate anonymization certificate
    const certificate = await this.generateAnonymizationCertificate(anonymizedData, config);

    return {
      ...anonymizedData,
      certificate,
      qualityCheck,
      anonymizationLevel: this.calculateAnonymizationLevel(qualityCheck),
    };
  }

  async handleSubjectRights(request: SubjectRightsRequest): Promise<SubjectRightsResponse> {
    // Authenticate subject
    const authentication = await this.authenticateSubject(request);
    if (!authentication.success) {
      throw new Error('Subject authentication failed');
    }

    // Validate request
    const validation = await this.subjectRightsManager.validateRequest(request);
    if (!validation.valid) {
      throw new Error(`Invalid rights request: ${validation.errors.join(', ')}`);
    }

    let response: SubjectRightsResponse;

    switch (request.right) {
      case 'access':
        response = await this.handleAccessRight(request);
        break;
      case 'rectification':
        response = await this.handleRectificationRight(request);
        break;
      case 'erasure':
        response = await this.handleErasureRight(request);
        break;
      case 'portability':
        response = await this.handlePortabilityRight(request);
        break;
      case 'restriction':
        response = await this.handleRestrictionRight(request);
        break;
      case 'objection':
        response = await this.handleObjectionRight(request);
        break;
      default:
        throw new Error(`Unknown subject right: ${request.right}`);
    }

    // Log rights request
    await this.logRightsRequest(request, response);

    return response;
  }

  async manageCrossBorderTransfer(transfer: CrossBorderTransferRequest): Promise<TransferResult> {
    // Check transfer legality
    const legalityCheck = await this.crossBorderController.checkLegality(transfer);
    if (!legalityCheck.legal) {
      throw new Error(`Transfer not legal: ${legalityCheck.reason}`);
    }

    // Check adequacy decision
    const adequacyCheck = await this.crossBorderController.checkAdequacy(transfer.destinationCountry);
    
    if (!adequacyCheck.adequate) {
      // Require additional safeguards
      const safeguards = await this.implementAdditionalSafeguards(transfer);
      if (!safeguards.sufficient) {
        throw new Error('Insufficient safeguards for cross-border transfer');
      }
    }

    // Apply data protection measures
    const protectionMeasures = await this.applyProtectionMeasures(transfer);

    // Execute transfer
    const transferExecution = await this.executeTransfer(transfer, protectionMeasures);

    // Generate transfer certificate
    const certificate = await this.generateTransferCertificate(transfer, transferExecution);

    return {
      transferId: transferExecution.id,
      status: 'completed',
      certificate,
      protectionMeasures,
      timestamp: Date.now(),
    };
  }

  async detectAndRespondToBreach(breach: BreachIncident): Promise<BreachResponse> {
    // Validate breach report
    const validation = await this.breachDetector.validateBreach(breach);
    if (!validation.valid) {
      throw new Error(`Invalid breach report: ${validation.errors.join(', ')}`);
    }

    // Assess breach severity
    const severityAssessment = await this.breachDetector.assessSeverity(breach);
    
    // Determine notification requirements
    const notificationRequirements = await this.determineNotificationRequirements(severityAssessment);
    
    // Implement containment measures
    const containment = await this.implementContainment(breach, severityAssessment);
    
    // Notify affected parties
    const notifications = await this.notifyAffectedParties(breach, notificationRequirements);
    
    // Report to authorities
    const authorityReports = await this.reportToAuthorities(breach, notificationRequirements);

    return {
      breachId: breach.id,
      severity: severityAssessment.level,
      containment,
      notifications,
      authorityReports,
      responsePlan: await this.generateResponsePlan(breach, severityAssessment),
      timestamp: Date.now(),
    };
  }

  async enforcePrivacyPolicy(policy: PrivacyPolicy): Promise<PolicyEnforcementResult> {
    // Validate policy
    const validation = await this.privacyPolicyEngine.validatePolicy(policy);
    if (!validation.valid) {
      throw new Error(`Invalid privacy policy: ${validation.errors.join(', ')}`);
    }

    // Deploy policy enforcement rules
    const enforcement = await this.privacyPolicyEngine.deployEnforcement(policy);

    // Monitor compliance
    const compliance = await this.monitorPolicyCompliance(policy);

    // Generate enforcement report
    const report = await this.generateEnforcementReport(policy, enforcement, compliance);

    return {
      policyId: policy.id,
      enforcement,
      compliance,
      report,
      violations: compliance.violations,
      remediationActions: compliance.remediationActions,
    };
  }

  private async implementAdditionalSafeguards(system: SystemDesign, recommendations: SafeguardRecommendation[]): Promise<void> {
    for (const recommendation of recommendations) {
      switch (recommendation.type) {
        case 'encryption':
          await this.implementEncryptionSafeguard(system, recommendation);
          break;
        case 'access_control':
          await this.implementAccessControlSafeguard(system, recommendation);
          break;
        case 'audit_logging':
          await this.implementAuditLoggingSafeguard(system, recommendation);
          break;
        case 'data_minimization':
          await this.implementDataMinimizationSafeguard(system, recommendation);
          break;
      }
    }
  }

  private async implementPrivacyControls(system: SystemDesign, pia: PrivacyImpactAssessment): Promise<PrivacyControl[]> {
    const controls = [];

    // Implement encryption controls
    if (pia.requiresEncryption) {
      controls.push(await this.createEncryptionControl(system));
    }

    // Implement access controls
    if (pia.requiresAccessControl) {
      controls.push(await this.createAccessControl(system));
    }

    // Implement audit controls
    if (pia.requiresAuditLogging) {
      controls.push(await this.createAuditControl(system));
    }

    // Implement retention controls
    if (pia.requiresRetentionControl) {
      controls.push(await this.createRetentionControl(system));
    }

    return controls;
  }

  private async handleAccessRight(request: SubjectRightsRequest): Promise<SubjectRightsResponse> {
    // Collect subject's personal data
    const personalData = await this.subjectRightsManager.collectPersonalData(request.subjectId);
    
    // Validate data collection
    const validation = await this.validateCollectedData(personalData, request);
    
    // Prepare data for subject
    const preparedData = await this.prepareDataForSubject(personalData);
    
    // Log access request fulfillment
    await this.logRightsFulfillment(request, 'access', preparedData);

    return {
      requestId: request.id,
      right: 'access',
      status: 'fulfilled',
      data: preparedData,
      format: 'json',
      timestamp: Date.now(),
    };
  }

  private async handleErasureRight(request: SubjectRightsRequest): Promise<SubjectRightsResponse> {
    // Identify subject's data
    const personalData = await this.subjectRightsManager.identifyPersonalData(request.subjectId);
    
    // Check for legal or contractual retention requirements
    const retentionCheck = await this.checkRetentionRequirements(personalData);
    
    // Erase data where possible
    const erasureResult = await this.subjectRightsManager.erasePersonalData(
      request.subjectId,
      retentionCheck.exemptData
    );
    
    // Confirm erasure
    const confirmation = await this.confirmErasure(erasureResult);

    return {
      requestId: request.id,
      right: 'erasure',
      status: confirmation.confirmed ? 'fulfilled' : 'partially_fulfilled',
      erasedRecords: erasureResult.erasedCount,
      exemptRecords: erasureResult.exemptCount,
      timestamp: Date.now(),
    };
  }

  private calculatePrivacyLevel(pia: PrivacyImpactAssessment, controls: PrivacyControl[]): PrivacyLevel {
    const baseScore = pia.privacyScore || 0.5;
    const controlBonus = controls.length * 0.1;
    const adjustedScore = Math.min(1.0, baseScore + controlBonus);

    if (adjustedScore >= 0.9) return 'high';
    if (adjustedScore >= 0.7) return 'medium';
    return 'low';
  }

  private calculateDataReduction(original: DataFlow, minimized: DataFlow): number {
    const originalSize = this.calculateDataSize(original);
    const minimizedSize = this.calculateDataSize(minimized);
    
    return (originalSize - minimizedSize) / originalSize;
  }

  private calculateAnonymizationLevel(qualityCheck: AnonymizationQualityCheck): AnonymizationLevel {
    if (qualityCheck.reidentificationRisk < 0.01) return 'very_high';
    if (qualityCheck.reidentificationRisk < 0.05) return 'high';
    if (qualityCheck.reidentificationRisk < 0.2) return 'medium';
    return 'low';
  }
}

// Consent Manager Implementation
export class ConsentManager {
  constructor(
    private consentStore: ConsentStore,
    private preferenceManager: PreferenceManager,
    private withdrawalProcessor: WithdrawalProcessor
  ) {}

  async setupConsentSystem(config: ConsentSystemConfig): Promise<ConsentSystem> {
    // Create consent types
    const consentTypes = await this.createConsentTypes(config.consentTypes);
    
    // Setup withdrawal mechanisms
    const withdrawalSetup = await this.withdrawalProcessor.setup({
      systemId: config.systemId,
      methods: ['email', 'portal', 'api'],
      retentionPeriod: config.withdrawalRetentionPeriod || 2555, // 7 years
    });

    return {
      systemId: config.systemId,
      consentTypes,
      withdrawalSetup,
      granularity: config.granularity,
      status: 'active',
    };
  }

  async recordConsent(consent: ConsentRecord): Promise<ConsentRecord> {
    // Validate consent record
    await this.validateConsentRecord(consent);
    
    // Store consent
    const stored = await this.consentStore.create(consent);
    
    // Update preferences
    await this.preferenceManager.update(consent.userId, {
      [consent.consentType]: {
        granted: consent.granted,
        timestamp: consent.timestamp,
        duration: consent.duration,
        recordId: stored.id,
      },
    });

    return stored;
  }

  async withdrawConsent(withdrawal: ConsentWithdrawal): Promise<WithdrawalResult> {
    // Find active consent records
    const activeConsents = await this.consentStore.findActive(
      withdrawal.userId,
      withdrawal.consentType
    );

    // Process withdrawal
    const results = [];
    for (const consent of activeConsents) {
      const result = await this.withdrawalProcessor.process(consent, withdrawal);
      results.push(result);
    }

    // Update preferences
    await this.preferenceManager.update(withdrawal.userId, {
      [withdrawal.consentType]: {
        granted: false,
        withdrawnAt: withdrawal.timestamp,
        reason: withdrawal.reason,
      },
    });

    return {
      withdrawalId: withdrawal.id,
      processedConsents: results.length,
      timestamp: Date.now(),
    };
  }

  async checkConsent(userId: string, consentType: string, purpose: string): Promise<ConsentCheck> {
    // Get current consent status
    const consent = await this.consentStore.getCurrent(userId, consentType);
    
    if (!consent) {
      return { granted: false, reason: 'No consent record found' };
    }

    // Check if consent is still valid
    if (consent.expiresAt && consent.expiresAt < Date.now()) {
      return { granted: false, reason: 'Consent expired' };
    }

    // Check if consent has been withdrawn
    if (consent.withdrawnAt) {
      return { granted: false, reason: 'Consent withdrawn' };
    }

    // Check purpose scope
    if (!this.consentCoversPurpose(consent, purpose)) {
      return { granted: false, reason: 'Consent does not cover purpose' };
    }

    return {
      granted: true,
      consentId: consent.id,
      grantedAt: consent.timestamp,
      expiresAt: consent.expiresAt,
    };
  }

  private async createConsentTypes(types: ConsentTypeDefinition[]): Promise<ConsentType[]> {
    const consentTypes = [];

    for (const type of types) {
      const consentType = await this.consentStore.createConsentType({
        id: type.id,
        name: type.name,
        description: type.description,
        purposes: type.purposes,
        dataCategories: type.dataCategories,
        required: type.required || false,
        withdrawalAllowed: type.withdrawalAllowed !== false,
      });
      consentTypes.push(consentType);
    }

    return consentTypes;
  }

  private consentCoversPurpose(consent: ConsentRecord, purpose: string): boolean {
    return consent.purposes.includes(purpose) || consent.purposes.includes('all');
  }
}

// Data Minimizer Implementation
export class DataMinimizer {
  constructor(
    private ruleEngine: MinimizationRuleEngine,
    private dataAnalyzer: DataAnalyzer
  ) {}

  async configureMinimization(config: MinimizationConfig): Promise<MinimizationSetup> {
    // Validate minimization rules
    await this.validateMinimizationRules(config.rules);
    
    // Create minimization profile
    const profile = await this.createMinimizationProfile(config);

    return {
      systemId: config.systemId,
      profile,
      rules: config.rules,
      status: 'active',
    };
  }

  async applyMinimization(dataFlow: DataFlow, rules: MinimizationRule[]): Promise<MinimizedDataFlow> {
    // Analyze data flow
    const analysis = await this.dataAnalyzer.analyze(dataFlow);
    
    // Apply minimization rules
    const minimizedFlow = { ...dataFlow };
    
    for (const rule of rules) {
      const result = await this.ruleEngine.applyRule(rule, analysis, minimizedFlow);
      minimizedFlow.dataFields = result.dataFields;
    }

    // Validate minimization result
    const validation = await this.validateMinimizationResult(minimizedFlow, rules);
    if (!validation.valid) {
      throw new Error(`Minimization validation failed: ${validation.errors.join(', ')}`);
    }

    return minimizedFlow;
  }

  private async createMinimizationProfile(config: MinimizationConfig): Promise<MinimizationProfile> {
    return {
      id: generateId(),
      systemId: config.systemId,
      dataFlows: config.dataFlows,
      rules: config.rules,
      purposeMapping: this.createPurposeMapping(config.dataFlows),
      createdAt: Date.now(),
    };
  }

  private createPurposeMapping(dataFlows: DataFlow[]): Record<string, string[]> {
    const mapping = {};
    
    for (const flow of dataFlows) {
      if (!mapping[flow.purpose]) {
        mapping[flow.purpose] = [];
      }
      mapping[flow.purpose].push(...flow.dataFields.map(f => f.name));
    }
    
    return mapping;
  }
}

// Subject Rights Manager Implementation
export class SubjectRightsManager {
  constructor(
    private dataLocator: PersonalDataLocator,
    private erasureEngine: ErasureEngine,
    private portabilityEngine: PortabilityEngine
  ) {}

  async collectPersonalData(subjectId: string): Promise<PersonalDataCollection> {
    // Locate all personal data for subject
    const locations = await this.dataLocator.locate(subjectId);
    
    // Collect data from all locations
    const collectedData = [];
    
    for (const location of locations) {
      const data = await this.collectFromLocation(location, subjectId);
      collectedData.push(data);
    }

    return {
      subjectId,
      locations,
      data: collectedData,
      collectedAt: Date.now(),
    };
  }

  async erasePersonalData(subjectId: string, exemptions: string[] = []): Promise<ErasureResult> {
    // Locate data to erase
    const locations = await this.dataLocator.locate(subjectId);
    
    // Process erasure for each location
    const results = [];
    let totalErased = 0;
    let totalExempt = 0;

    for (const location of locations) {
      const result = await this.erasureEngine.erase(location, subjectId, exemptions);
      results.push(result);
      totalErased += result.erasedCount;
      totalExempt += result.exemptCount;
    }

    return {
      subjectId,
      results,
      totalErased,
      totalExempt,
      processedAt: Date.now(),
    };
  }

  async exportPersonalData(subjectId: string, format: 'json' | 'csv' | 'xml' = 'json'): Promise<DataExport> {
    // Collect personal data
    const collection = await this.collectPersonalData(subjectId);
    
    // Format data for export
    const formattedData = await this.portabilityEngine.format(collection, format);
    
    return {
      subjectId,
      format,
      data: formattedData,
      exportedAt: Date.now(),
      recordCount: this.countRecords(collection),
    };
  }

  private async collectFromLocation(location: DataLocation, subjectId: string): Promise<LocationData> {
    // Implementation depends on location type
    switch (location.type) {
      case 'database':
        return await this.collectFromDatabase(location, subjectId);
      case 'file_system':
        return await this.collectFromFileSystem(location, subjectId);
      case 'api':
        return await this.collectFromAPI(location, subjectId);
      default:
        throw new Error(`Unknown location type: ${location.type}`);
    }
  }

  private countRecords(collection: PersonalDataCollection): number {
    return collection.data.reduce((total, location) => {
      return total + (location.records?.length || 0);
    }, 0);
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No data privacy engineering
export class BasicDataService {
  // BAD: No privacy by design
  async processUserData(data: any) {
    // BAD: No consent management
    // BAD: No data minimization
    // BAD: No subject rights
    return this.store(data);
  }

  // BAD: No anonymization
  // BAD: No cross-border controls
  // BAD: No breach detection
  // BAD: No policy enforcement
}
```
</example_bad>
