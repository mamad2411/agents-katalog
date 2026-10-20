---
description: Run Zero Trust Network and Micro-Segmentation Standards Check
globs: ['**/zero-trust/**/*.ts', '**/micro-segmentation/**/*.ts', '**/network-security/**/*.ts']
---

# Security: Zero Trust Network & Micro-Segmentation Standards

<audit_rules>

- You MUST implement proper zero trust principles with "never trust, always verify" approach.
- You MUST ensure micro-segmentation with granular network policies between all services.
- You MUST implement proper identity-based access control for all network communications.
- You MUST configure proper network encryption and mutual TLS for all service-to-service communication.
- You MUST implement proper continuous monitoring and anomaly detection for network traffic.
- You MUST ensure proper least privilege access with just-in-time access provisioning.
- You MUST implement proper device posture assessment and compliance verification.
- You MUST configure proper network segmentation with east-west traffic controls.
- You MUST ensure proper session management with short-lived tokens and continuous re-authentication.
- You MUST implement proper threat detection and automated response for network security incidents.
  </audit_rules>

<example_good>

```typescript
// Zero Trust Network Implementation

export class ZeroTrustNetworkOrchestrator {
  constructor(
    private identityProvider: IdentityProvider,
    private policyEngine: PolicyEngine,
    private networkSegmenter: NetworkSegmenter,
    private encryptionManager: EncryptionManager,
    private threatDetector: ThreatDetector,
    private complianceChecker: ComplianceChecker
  ) {}

  async establishZeroTrustSession(request: AccessRequest): Promise<ZeroTrustSession> {
    // Multi-factor authentication
    const authResult = await this.authenticateUser(request)
    if (!authResult.success) {
      throw new Error(`Authentication failed: ${authResult.reason}`)
    }

    // Device posture assessment
    const devicePosture = await this.assessDevicePosture(request.deviceInfo)
    if (!devicePosture.compliant) {
      throw new Error(`Device not compliant: ${devicePosture.violations.join(', ')}`)
    }

    // Risk assessment
    const riskAssessment = await this.assessRisk(request, authResult, devicePosture)

    // Policy evaluation
    const policyDecision = await this.policyEngine.evaluate({
      user: authResult.user,
      resource: request.resource,
      context: {
        device: devicePosture,
        risk: riskAssessment,
        location: request.location,
        time: new Date(),
      },
    })

    if (!policyDecision.allow) {
      throw new Error(`Access denied: ${policyDecision.reason}`)
    }

    // Establish micro-segmented session
    const session = await this.createZeroTrustSession({
      user: authResult.user,
      resource: request.resource,
      policy: policyDecision,
      risk: riskAssessment,
      device: devicePosture,
    })

    // Setup network segmentation
    await this.networkSegmenter.setupSegmentation(session)

    // Configure encryption
    await this.encryptionManager.setupSessionEncryption(session)

    return session
  }

  async enforceMicroSegmentation(
    service: Service,
    policies: SegmentationPolicy[]
  ): Promise<SegmentationEnforcement> {
    // Validate segmentation policies
    await this.validateSegmentationPolicies(policies)

    // Create network segments
    const segments = await this.networkSegmenter.createSegments(service, policies)

    // Implement east-west traffic controls
    const trafficControls = await this.implementTrafficControls(segments, policies)

    // Setup continuous monitoring
    const monitoring = await this.setupSegmentMonitoring(segments)

    return {
      serviceId: service.id,
      segments,
      trafficControls,
      monitoring,
      status: 'active',
    }
  }

  async monitorZeroTrustCompliance(session: ZeroTrustSession): Promise<ComplianceReport> {
    // Continuous authentication verification
    const authVerification = await this.verifyContinuousAuthentication(session)

    // Device compliance monitoring
    const deviceCompliance = await this.monitorDeviceCompliance(session)

    // Network traffic analysis
    const trafficAnalysis = await this.analyzeNetworkTraffic(session)

    // Policy compliance check
    const policyCompliance = await this.checkPolicyCompliance(session)

    // Threat detection
    const threatAnalysis = await this.threatDetector.analyzeSession(session)

    const overallCompliance = this.calculateOverallCompliance({
      authVerification,
      deviceCompliance,
      trafficAnalysis,
      policyCompliance,
      threatAnalysis,
    })

    // Take action if non-compliant
    if (!overallCompliance.compliant) {
      await this.handleNonCompliance(session, overallCompliance)
    }

    return overallCompliance
  }

  async implementJustInTimeAccess(request: JITAccessRequest): Promise<JITAccess> {
    // Validate JIT request
    const validation = await this.validateJITRequest(request)
    if (!validation.valid) {
      throw new Error(`JIT request invalid: ${validation.reasons.join(', ')}`)
    }

    // Risk assessment for JIT access
    const riskAssessment = await this.assessJITRisk(request)

    // Approval workflow if high risk
    if (riskAssessment.level === 'high') {
      const approval = await this.requestApproval(request, riskAssessment)
      if (!approval.approved) {
        throw new Error('JIT access request denied')
      }
    }

    // Create temporary access
    const jitAccess = await this.createTemporaryAccess({
      request,
      riskAssessment,
      duration: request.duration || 3600000, // 1 hour default
      permissions: request.permissions,
    })

    // Setup monitoring
    await this.monitorJITAccess(jitAccess)

    return jitAccess
  }

  private async authenticateUser(request: AccessRequest): Promise<AuthenticationResult> {
    // Primary authentication
    const primaryAuth = await this.identityProvider.authenticate({
      username: request.username,
      password: request.password,
      mfaToken: request.mfaToken,
    })

    if (!primaryAuth.success) {
      return { success: false, reason: 'Primary authentication failed' }
    }

    // Multi-factor authentication
    const mfaResult = await this.identityProvider.verifyMFA({
      userId: primaryAuth.user.id,
      token: request.mfaToken,
      device: request.deviceInfo,
    })

    if (!mfaResult.success) {
      return { success: false, reason: 'MFA verification failed' }
    }

    // Adaptive authentication based on risk
    const adaptiveAuth = await this.performAdaptiveAuthentication(primaryAuth.user, request)
    if (!adaptiveAuth.success) {
      return { success: false, reason: 'Adaptive authentication failed' }
    }

    return {
      success: true,
      user: primaryAuth.user,
      session: adaptiveAuth.session,
      riskScore: adaptiveAuth.riskScore,
    }
  }

  private async assessDevicePosture(deviceInfo: DeviceInfo): Promise<DevicePosture> {
    const violations = []

    // Check OS version and patches
    const osCompliance = await this.checkOSCompliance(deviceInfo)
    if (!osCompliance.compliant) {
      violations.push(`OS compliance: ${osCompliance.issues.join(', ')}`)
    }

    // Check security software
    const securityCompliance = await this.checkSecuritySoftware(deviceInfo)
    if (!securityCompliance.compliant) {
      violations.push(`Security software: ${securityCompliance.issues.join(', ')}`)
    }

    // Check configuration settings
    const configCompliance = await this.checkConfigurationCompliance(deviceInfo)
    if (!configCompliance.compliant) {
      violations.push(`Configuration: ${configCompliance.issues.join(', ')}`)
    }

    // Check for malware
    const malwareScan = await this.performMalwareScan(deviceInfo)
    if (malwareScan.detected) {
      violations.push(`Malware detected: ${malwareScan.threats.join(', ')}`)
    }

    return {
      deviceId: deviceInfo.id,
      compliant: violations.length === 0,
      violations,
      trustLevel: this.calculateDeviceTrustLevel(violations),
      lastAssessment: Date.now(),
    }
  }

  private async assessRisk(
    request: AccessRequest,
    authResult: AuthenticationResult,
    devicePosture: DevicePosture
  ): Promise<RiskAssessment> {
    const riskFactors = []

    // User risk factors
    const userRisk = await this.assessUserRisk(authResult.user)
    riskFactors.push({ type: 'user', score: userRisk.score, factors: userRisk.factors })

    // Location risk
    const locationRisk = await this.assessLocationRisk(request.location)
    riskFactors.push({ type: 'location', score: locationRisk.score, factors: locationRisk.factors })

    // Time risk
    const timeRisk = await this.assessTimeRisk(new Date())
    riskFactors.push({ type: 'time', score: timeRisk.score, factors: timeRisk.factors })

    // Device risk
    const deviceRisk = this.assessDeviceRisk(devicePosture)
    riskFactors.push({ type: 'device', score: deviceRisk.score, factors: deviceRisk.factors })

    // Behavioral risk
    const behaviorRisk = await this.assessBehavioralRisk(authResult.user, request)
    riskFactors.push({ type: 'behavior', score: behaviorRisk.score, factors: behaviorRisk.factors })

    // Calculate overall risk score
    const overallScore = this.calculateOverallRiskScore(riskFactors)
    const riskLevel = this.determineRiskLevel(overallScore)

    return {
      overallScore,
      level: riskLevel,
      factors: riskFactors,
      recommendations: this.generateRiskRecommendations(riskFactors),
    }
  }

  private async createZeroTrustSession(config: SessionConfig): Promise<ZeroTrustSession> {
    const session = {
      id: generateSessionId(),
      userId: config.user.id,
      resourceId: config.resource.id,
      policy: config.policy,
      risk: config.risk,
      device: config.device,
      createdAt: Date.now(),
      expiresAt: Date.now() + (config.policy.sessionDuration || 3600000), // 1 hour default
      status: 'active',
    }

    // Store session
    await this.storeSession(session)

    return session
  }

  private async implementTrafficControls(
    segments: NetworkSegment[],
    policies: SegmentationPolicy[]
  ): Promise<TrafficControl[]> {
    const controls = []

    for (const segment of segments) {
      const applicablePolicies = policies.filter((p) => p.appliesToSegment(segment.id))

      for (const policy of applicablePolicies) {
        const control = await this.networkSegmenter.createTrafficControl({
          sourceSegment: segment.id,
          destinationSegment: policy.destinationSegment,
          action: policy.action, // allow, deny, log
          protocols: policy.protocols,
          ports: policy.ports,
          encryption: policy.requireEncryption,
          authentication: policy.requireAuthentication,
        })

        controls.push(control)
      }
    }

    return controls
  }

  private async monitorNetworkTraffic(session: ZeroTrustSession): Promise<TrafficAnalysis> {
    // Collect traffic data
    const trafficData = await this.collectTrafficData(session)

    // Analyze for anomalies
    const anomalies = await this.detectTrafficAnomalies(trafficData)

    // Check for policy violations
    const violations = await this.checkTrafficViolations(trafficData, session.policy)

    // Performance analysis
    const performance = await this.analyzeTrafficPerformance(trafficData)

    return {
      sessionId: session.id,
      trafficData,
      anomalies,
      violations,
      performance,
      riskScore: this.calculateTrafficRiskScore(anomalies, violations),
    }
  }

  private async handleNonCompliance(
    session: ZeroTrustSession,
    compliance: ComplianceReport
  ): Promise<void> {
    // Log compliance violation
    await this.logComplianceViolation(session, compliance)

    // Take action based on severity
    switch (compliance.severity) {
      case 'critical':
        await this.terminateSession(session)
        await this.triggerIncidentResponse(session, compliance)
        break
      case 'high':
        await this.restrictSession(session)
        await this.notifySecurityTeam(session, compliance)
        break
      case 'medium':
        await this.warnUser(session, compliance)
        await this.increaseMonitoring(session)
        break
      case 'low':
        await this.logIncident(session, compliance)
        break
    }
  }

  private calculateDeviceTrustLevel(violations: string[]): DeviceTrustLevel {
    if (violations.length === 0) return 'trusted'
    if (violations.length <= 2) return 'moderate'
    if (violations.length <= 5) return 'low'
    return 'untrusted'
  }

  private calculateOverallRiskScore(riskFactors: RiskFactor[]): number {
    const weights = {
      user: 0.3,
      location: 0.2,
      time: 0.1,
      device: 0.25,
      behavior: 0.15,
    }

    let totalScore = 0
    for (const factor of riskFactors) {
      const weight = weights[factor.type] || 0.1
      totalScore += factor.score * weight
    }

    return totalScore
  }

  private determineRiskLevel(score: number): RiskLevel {
    if (score >= 0.8) return 'critical'
    if (score >= 0.6) return 'high'
    if (score >= 0.4) return 'medium'
    if (score >= 0.2) return 'low'
    return 'minimal'
  }
}

// Network Segmenter Implementation
export class NetworkSegmenter {
  constructor(
    private networkPolicyManager: NetworkPolicyManager,
    private firewallManager: FirewallManager,
    private encryptionManager: EncryptionManager
  ) {}

  async createSegments(
    service: Service,
    policies: SegmentationPolicy[]
  ): Promise<NetworkSegment[]> {
    const segments = []

    // Create service segment
    const serviceSegment = await this.createServiceSegment(service)
    segments.push(serviceSegment)

    // Create data segments
    const dataSegments = await this.createDataSegments(service, policies)
    segments.push(...dataSegments)

    // Create management segment
    const managementSegment = await this.createManagementSegment(service)
    segments.push(managementSegment)

    return segments
  }

  async createTrafficControl(config: TrafficControlConfig): Promise<TrafficControl> {
    // Create network policy
    const networkPolicy = await this.networkPolicyManager.createPolicy({
      name: `traffic-control-${config.sourceSegment}-${config.destinationSegment}`,
      source: {
        segment: config.sourceSegment,
        namespace: config.sourceNamespace,
      },
      destination: {
        segment: config.destinationSegment,
        namespace: config.destinationNamespace,
      },
      rules: [
        {
          action: config.action,
          protocols: config.protocols,
          ports: config.ports,
          encryption: config.encryption,
          authentication: config.authentication,
        },
      ],
    })

    // Create firewall rules
    const firewallRules = await this.firewallManager.createRules({
      policyId: networkPolicy.id,
      source: config.sourceSegment,
      destination: config.destinationSegment,
      action: config.action,
      protocols: config.protocols,
      ports: config.ports,
    })

    return {
      id: networkPolicy.id,
      sourceSegment: config.sourceSegment,
      destinationSegment: config.destinationSegment,
      action: config.action,
      networkPolicy,
      firewallRules,
      encryption: config.encryption,
      authentication: config.authentication,
    }
  }

  private async createServiceSegment(service: Service): Promise<NetworkSegment> {
    return {
      id: `service-${service.id}`,
      name: `${service.name}-segment`,
      type: 'service',
      services: [service.id],
      policies: [
        {
          type: 'ingress',
          action: 'deny',
          protocols: ['all'],
          description: 'Default deny ingress',
        },
        {
          type: 'egress',
          action: 'deny',
          protocols: ['all'],
          description: 'Default deny egress',
        },
      ],
      encryption: 'required',
      authentication: 'required',
    }
  }

  private async createDataSegments(
    service: Service,
    policies: SegmentationPolicy[]
  ): Promise<NetworkSegment[]> {
    const segments = []

    for (const policy of policies) {
      if (policy.type === 'data') {
        const segment = {
          id: `data-${policy.resource}`,
          name: `${policy.resource}-data-segment`,
          type: 'data',
          resources: [policy.resource],
          policies: [policy],
          encryption: 'required',
          authentication: 'required',
        }
        segments.push(segment)
      }
    }

    return segments
  }
}

// Policy Engine Implementation
export class PolicyEngine {
  constructor(
    private policyStore: PolicyStore,
    private riskCalculator: RiskCalculator,
    private contextEnricher: ContextEnricher
  ) {}

  async evaluate(request: PolicyEvaluationRequest): Promise<PolicyDecision> {
    // Enrich context
    const enrichedContext = await this.contextEnricher.enrich(request.context)

    // Get applicable policies
    const policies = await this.getApplicablePolicies(request.user, request.resource)

    // Evaluate each policy
    const evaluations = []
    for (const policy of policies) {
      const evaluation = await this.evaluatePolicy(policy, request, enrichedContext)
      evaluations.push(evaluation)
    }

    // Combine policy decisions
    const combinedDecision = this.combinePolicyDecisions(evaluations)

    return {
      allow: combinedDecision.allow,
      reason: combinedDecision.reason,
      policies: evaluations,
      conditions: combinedDecision.conditions,
      expiresAt: combinedDecision.expiresAt,
      sessionDuration: combinedDecision.sessionDuration,
    }
  }

  private async getApplicablePolicies(user: User, resource: Resource): Promise<Policy[]> {
    return await this.policyStore.getPolicies({
      userId: user.id,
      userRoles: user.roles,
      resourceType: resource.type,
      resourceId: resource.id,
    })
  }

  private async evaluatePolicy(
    policy: Policy,
    request: PolicyEvaluationRequest,
    context: any
  ): Promise<PolicyEvaluation> {
    const conditions = policy.conditions || []

    for (const condition of conditions) {
      const result = await this.evaluateCondition(condition, request, context)
      if (!result.satisfied) {
        return {
          policyId: policy.id,
          satisfied: false,
          reason: `Condition not satisfied: ${condition.description}`,
          condition: condition,
        }
      }
    }

    return {
      policyId: policy.id,
      satisfied: true,
      reason: 'All conditions satisfied',
      conditions: conditions,
    }
  }

  private async evaluateCondition(
    condition: PolicyCondition,
    request: PolicyEvaluationRequest,
    context: any
  ): Promise<ConditionEvaluation> {
    switch (condition.type) {
      case 'time':
        return this.evaluateTimeCondition(condition, context)
      case 'location':
        return this.evaluateLocationCondition(condition, context)
      case 'device':
        return this.evaluateDeviceCondition(condition, context)
      case 'risk':
        return this.evaluateRiskCondition(condition, context)
      case 'role':
        return this.evaluateRoleCondition(condition, request)
      default:
        return { satisfied: false, reason: `Unknown condition type: ${condition.type}` }
    }
  }

  private evaluateTimeCondition(condition: PolicyCondition, context: any): ConditionEvaluation {
    const now = new Date()
    const currentTime = now.getHours() * 60 + now.getMinutes()

    const satisfied = currentTime >= condition.startTime && currentTime <= condition.endTime

    return {
      satisfied,
      reason: satisfied ? 'Time condition satisfied' : 'Outside allowed time range',
    }
  }

  private evaluateLocationCondition(condition: PolicyCondition, context: any): ConditionEvaluation {
    const userLocation = context.location
    const allowedLocations = condition.allowedLocations || []

    const satisfied =
      allowedLocations.includes(userLocation.country) ||
      allowedLocations.includes(userLocation.region)

    return {
      satisfied,
      reason: satisfied ? 'Location condition satisfied' : 'Location not allowed',
    }
  }

  private evaluateDeviceCondition(condition: PolicyCondition, context: any): ConditionEvaluation {
    const device = context.device
    const requiredTrustLevel = condition.requiredTrustLevel || 'trusted'

    const satisfied =
      device.trustLevel === requiredTrustLevel ||
      this.isTrustLevelSufficient(device.trustLevel, requiredTrustLevel)

    return {
      satisfied,
      reason: satisfied ? 'Device condition satisfied' : 'Device trust level insufficient',
    }
  }

  private evaluateRiskCondition(condition: PolicyCondition, context: any): ConditionEvaluation {
    const riskScore = context.risk.overallScore
    const maxAllowedRisk = condition.maxRiskScore || 0.5

    const satisfied = riskScore <= maxAllowedRisk

    return {
      satisfied,
      reason: satisfied ? 'Risk condition satisfied' : 'Risk score too high',
    }
  }

  private evaluateRoleCondition(
    condition: PolicyCondition,
    request: PolicyEvaluationRequest
  ): ConditionEvaluation {
    const userRoles = request.user.roles
    const requiredRoles = condition.requiredRoles || []

    const satisfied = requiredRoles.some((role) => userRoles.includes(role))

    return {
      satisfied,
      reason: satisfied ? 'Role condition satisfied' : 'Insufficient role privileges',
    }
  }

  private isTrustLevelSufficient(current: string, required: string): boolean {
    const trustLevels = { untrusted: 0, low: 1, moderate: 2, trusted: 3 }
    return trustLevels[current] >= trustLevels[required]
  }

  private combinePolicyDecisions(evaluations: PolicyEvaluation[]): CombinedPolicyDecision {
    const allSatisfied = evaluations.every((e) => e.satisfied)

    if (allSatisfied) {
      return {
        allow: true,
        reason: 'All policies satisfied',
        conditions: evaluations.flatMap((e) => e.conditions || []),
        expiresAt: Date.now() + 3600000, // 1 hour
        sessionDuration: 3600000,
      }
    } else {
      const failedEvaluations = evaluations.filter((e) => !e.satisfied)
      return {
        allow: false,
        reason: failedEvaluations.map((e) => e.reason).join('; '),
        conditions: [],
        expiresAt: Date.now(),
        sessionDuration: 0,
      }
    }
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No zero trust principles
export class BasicNetworkService {
  // BAD: Traditional perimeter-based security
  async allowAccess(user: any, resource: any) {
    // BAD: No continuous verification
    // BAD: No micro-segmentation
    // BAD: No device posture check
    if (this.hasPermission(user, resource)) {
      return true
    }
    return false
  }

  // BAD: No identity-based access control
  // BAD: No encryption requirements
  // BAD: No risk assessment
  // BAD: No just-in-time access
}
```

</example_bad>
