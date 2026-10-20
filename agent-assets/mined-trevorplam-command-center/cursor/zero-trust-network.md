---
description: Run Zero Trust Network and Micro-Segmentation Standards Check
globs: ["**/zero-trust/**/*.ts", "**/network-security/**/*.ts", "**/micro-segmentation/**/*.ts"]
---
# Security: Zero Trust Network & Micro-Segmentation Standards

<audit_rules>
- You MUST implement proper zero trust principles with "never trust, always verify" approach.
- You MUST implement proper micro-segmentation with granular network policies between all services.
- You MUST implement proper identity-based access control for all network communications.
- You MUST implement proper network encryption and mutual TLS for all service-to-service communication.
- You MUST implement proper continuous monitoring and anomaly detection for network traffic.
- You MUST implement proper least privilege access with just-in-time access provisioning.
- You MUST implement proper device posture assessment and compliance verification.
- You MUST implement proper network segmentation with east-west traffic controls.
- You MUST implement proper session management with short-lived tokens and continuous re-authentication.
- You MUST implement proper threat detection and automated response for network security incidents.
</audit_rules>

<example_good>
```typescript
// Zero Trust Network Implementation
import { z } from 'zod';
import { IdentityProvider } from './identity';
import { PolicyEngine } from './policy';
import { NetworkSegmenter } from './segmentation';
import { ThreatDetector } from './threat-detection';

export class ZeroTrustNetworkOrchestrator {
  constructor(
    private identityProvider: IdentityProvider,
    private policyEngine: PolicyEngine,
    private networkSegmenter: NetworkSegmenter,
    private threatDetector: ThreatDetector,
    private complianceChecker: ComplianceChecker
  ) {}

  // Never trust, always verify approach
  async establishZeroTrustSession(request: AccessRequest): Promise<ZeroTrustSession> {
    // Multi-factor authentication
    const authResult = await this.authenticateUser(request);
    if (!authResult.success) {
      throw new Error(`Authentication failed: ${authResult.reason}`);
    }

    // Device posture assessment
    const devicePosture = await this.assessDevicePosture(request.deviceInfo);
    if (!devicePosture.compliant) {
      throw new Error(`Device not compliant: ${devicePosture.violations.join(', ')}`);
    }

    // Risk assessment
    const riskAssessment = await this.assessRisk(request, authResult, devicePosture);
    
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
    });

    if (!policyDecision.allow) {
      throw new Error(`Access denied: ${policyDecision.reason}`);
    }

    // Establish micro-segmented session
    const session = await this.createZeroTrustSession({
      user: authResult.user,
      resource: request.resource,
      policy: policyDecision,
      risk: riskAssessment,
      device: devicePosture,
    });

    // Setup network segmentation
    await this.networkSegmenter.setupSegmentation(session);

    // Configure encryption
    await this.setupEncryption(session);

    return session;
  }

  // Micro-segmentation with granular network policies
  async enforceMicroSegmentation(service: Service, policies: SegmentationPolicy[]): Promise<SegmentationEnforcement> {
    // Validate segmentation policies
    await this.validateSegmentationPolicies(policies);

    // Create network segments
    const segments = await this.networkSegmenter.createSegments(service, policies);

    // Implement east-west traffic controls
    const trafficControls = await this.implementTrafficControls(segments, policies);

    // Setup continuous monitoring
    const monitoring = await this.setupSegmentMonitoring(segments);

    return {
      serviceId: service.id,
      segments,
      trafficControls,
      monitoring,
      status: 'active',
    };
  }

  // Identity-based access control for all communications
  async verifyIdentity(context: VerificationContext): Promise<IdentityVerification> {
    // Verify user identity
    const userVerification = await this.identityProvider.verifyUser(context.userId);
    if (!userVerification.valid) {
      return { valid: false, reason: 'Invalid user identity' };
    }

    // Verify service identity
    const serviceVerification = await this.identityProvider.verifyService(context.serviceId);
    if (!serviceVerification.valid) {
      return { valid: false, reason: 'Invalid service identity' };
    }

    // Verify session validity
    const sessionVerification = await this.verifySession(context.sessionId);
    if (!sessionVerification.valid) {
      return { valid: false, reason: 'Invalid or expired session' };
    }

    return {
      valid: true,
      user: userVerification.user,
      service: serviceVerification.service,
      session: sessionVerification.session,
    };
  }

  // Continuous monitoring and anomaly detection
  async monitorNetworkTraffic(sessionId: string): Promise<NetworkMonitoringReport> {
    // Get current network traffic
    const trafficData = await this.collectTrafficData(sessionId);
    
    // Analyze for anomalies
    const anomalies = await this.threatDetector.analyzeTraffic(trafficData);
    
    // Check for policy violations
    const violations = await this.checkPolicyViolations(trafficData, sessionId);
    
    // Generate security score
    const securityScore = this.calculateSecurityScore(anomalies, violations);

    // Take action if needed
    if (securityScore < 0.7) {
      await this.handleSecurityIncident(sessionId, anomalies, violations);
    }

    return {
      sessionId,
      timestamp: new Date(),
      trafficData,
      anomalies,
      violations,
      securityScore,
      recommendations: this.generateSecurityRecommendations(anomalies, violations),
    };
  }

  // Just-in-time access provisioning
  async provisionJustInTimeAccess(request: JITAccessRequest): Promise<JITAccess> {
    // Validate JIT request
    const validation = await this.validateJITRequest(request);
    if (!validation.valid) {
      throw new Error(`Invalid JIT request: ${validation.reasons.join(', ')}`);
    }

    // Risk assessment
    const riskAssessment = await this.assessJITRisk(request);
    
    // Approval workflow if high risk
    if (riskAssessment.level === 'high') {
      const approval = await this.requestApproval(request, riskAssessment);
      if (!approval.approved) {
        throw new Error('JIT access request denied');
      }
    }

    // Create temporary access
    const jitAccess = await this.createTemporaryAccess({
      request,
      riskAssessment,
      duration: request.duration || 3600000, // 1 hour default
      permissions: request.permissions,
    });

    // Setup monitoring
    await this.monitorJITAccess(jitAccess);

    return jitAccess;
  }

  private async authenticateUser(request: AccessRequest): Promise<AuthenticationResult> {
    // Primary authentication
    const primaryAuth = await this.identityProvider.authenticate({
      username: request.username,
      password: request.password,
      mfaToken: request.mfaToken,
    });

    if (!primaryAuth.success) {
      return { success: false, reason: 'Primary authentication failed' };
    }

    // Multi-factor authentication
    const mfaResult = await this.identityProvider.verifyMFA({
      userId: primaryAuth.user.id,
      token: request.mfaToken,
      device: request.deviceInfo,
    });

    if (!mfaResult.success) {
      return { success: false, reason: 'MFA verification failed' };
    }

    // Adaptive authentication based on risk
    const adaptiveAuth = await this.performAdaptiveAuthentication(primaryAuth.user, request);
    if (!adaptiveAuth.success) {
      return { success: false, reason: 'Adaptive authentication failed' };
    }

    return {
      success: true,
      user: primaryAuth.user,
      session: adaptiveAuth.session,
      riskScore: adaptiveAuth.riskScore,
    };
  }

  private async assessDevicePosture(deviceInfo: DeviceInfo): Promise<DevicePosture> {
    const violations = [];

    // Check OS version and patches
    const osCompliance = await this.checkOSCompliance(deviceInfo);
    if (!osCompliance.compliant) {
      violations.push(`OS compliance: ${osCompliance.issues.join(', ')}`);
    }

    // Check security software
    const securityCompliance = await this.checkSecuritySoftware(deviceInfo);
    if (!securityCompliance.compliant) {
      violations.push(`Security software: ${securityCompliance.issues.join(', ')}`);
    }

    // Check configuration settings
    const configCompliance = await this.checkConfigurationCompliance(deviceInfo);
    if (!configCompliance.compliant) {
      violations.push(`Configuration: ${configCompliance.issues.join(', ')}`);
    }

    // Check for malware
    const malwareScan = await this.performMalwareScan(deviceInfo);
    if (malwareScan.detected) {
      violations.push(`Malware detected: ${malwareScan.threats.join(', ')}`);
    }

    return {
      deviceId: deviceInfo.id,
      compliant: violations.length === 0,
      violations,
      trustLevel: this.calculateDeviceTrustLevel(violations),
      lastAssessment: Date.now(),
    };
  }

  private async assessRisk(request: AccessRequest, authResult: AuthenticationResult, devicePosture: DevicePosture): Promise<RiskAssessment> {
    const riskFactors = [];

    // User risk factors
    const userRisk = await this.assessUserRisk(authResult.user);
    riskFactors.push({ type: 'user', score: userRisk.score, factors: userRisk.factors });

    // Location risk
    const locationRisk = await this.assessLocationRisk(request.location);
    riskFactors.push({ type: 'location', score: locationRisk.score, factors: locationRisk.factors });

    // Time risk
    const timeRisk = await this.assessTimeRisk(new Date());
    riskFactors.push({ type: 'time', score: timeRisk.score, factors: timeRisk.factors });

    // Device risk
    const deviceRisk = this.assessDeviceRisk(devicePosture);
    riskFactors.push({ type: 'device', score: deviceRisk.score, factors: deviceRisk.factors });

    // Behavioral risk
    const behaviorRisk = await this.assessBehavioralRisk(authResult.user, request);
    riskFactors.push({ type: 'behavior', score: behaviorRisk.score, factors: behaviorRisk.factors });

    // Calculate overall risk score
    const overallScore = this.calculateOverallRiskScore(riskFactors);
    const riskLevel = this.determineRiskLevel(overallScore);

    return {
      overallScore,
      level: riskLevel,
      factors: riskFactors,
      recommendations: this.generateRiskRecommendations(riskFactors),
    };
  }

  private calculateSecurityScore(anomalies: NetworkAnomaly[], violations: PolicyViolation[]): number {
    const anomalyScore = anomalies.length * 0.3;
    const violationScore = violations.length * 0.5;
    
    return Math.max(0, 1 - (anomalyScore + violationScore));
  }

  private generateSecurityRecommendations(anomalies: NetworkAnomaly[], violations: PolicyViolation[]): string[] {
    const recommendations = [];

    for (const anomaly of anomalies) {
      recommendations.push(`Investigate anomaly: ${anomaly.type}`);
    }

    for (const violation of violations) {
      recommendations.push(`Address policy violation: ${violation.type}`);
    }

    return recommendations;
  }

  private calculateDeviceTrustLevel(violations: string[]): DeviceTrustLevel {
    if (violations.length === 0) return 'trusted';
    if (violations.length <= 2) return 'moderate';
    if (violations.length <= 5) return 'low';
    return 'untrusted';
  }

  private determineRiskLevel(score: number): RiskLevel {
    if (score >= 0.8) return 'critical';
    if (score >= 0.6) return 'high';
    if (score >= 0.4) return 'medium';
    if (score >= 0.2) return 'low';
    return 'minimal';
  }
}

// Network Segmenter Implementation
export class NetworkSegmenter {
  constructor(
    private networkPolicyManager: NetworkPolicyManager,
    private firewallManager: FirewallManager,
    private encryptionManager: EncryptionManager
  ) {}

  async createSegments(service: Service, policies: SegmentationPolicy[]): Promise<NetworkSegment[]> {
    const segments = [];

    // Create service segment
    const serviceSegment = await this.createServiceSegment(service);
    segments.push(serviceSegment);

    // Create data segments
    const dataSegments = await this.createDataSegments(service, policies);
    segments.push(...dataSegments);

    // Create management segment
    const managementSegment = await this.createManagementSegment(service);
    segments.push(managementSegment);

    return segments;
  }

  async implementTrafficControls(segments: NetworkSegment[], policies: SegmentationPolicy[]): Promise<TrafficControl[]> {
    const controls = [];

    for (const segment of segments) {
      const applicablePolicies = policies.filter(p => p.appliesToSegment(segment.id));
      
      for (const policy of applicablePolicies) {
        const control = await this.createTrafficControl(segment, policy);
        controls.push(control);
      }
    }

    return controls;
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
    };
  }

  private async createTrafficControl(segment: NetworkSegment, policy: SegmentationPolicy): Promise<TrafficControl> {
    // Create network policy
    const networkPolicy = await this.networkPolicyManager.createPolicy({
      name: `traffic-control-${segment.id}-${policy.id}`,
      source: {
        segment: segment.id,
        namespace: segment.namespace,
      },
      destination: {
        segment: policy.destinationSegment,
        namespace: policy.destinationNamespace,
      },
      rules: [
        {
          action: policy.action,
          protocols: policy.protocols,
          ports: policy.ports,
          encryption: policy.encryption,
          authentication: policy.authentication,
        },
      ],
    });

    // Create firewall rules
    const firewallRules = await this.firewallManager.createRules({
      policyId: networkPolicy.id,
      source: segment.id,
      destination: policy.destinationSegment,
      action: policy.action,
      protocols: policy.protocols,
      ports: policy.ports,
    });

    return {
      id: networkPolicy.id,
      sourceSegment: segment.id,
      destinationSegment: policy.destinationSegment,
      action: policy.action,
      networkPolicy,
      firewallRules,
      encryption: policy.encryption,
      authentication: policy.authentication,
    };
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
      return true;
    }
    return false;
  }

  // BAD: No identity-based access control
  // BAD: No encryption requirements
  // BAD: No risk assessment
  // BAD: No just-in-time access
}
```
</example_bad>
