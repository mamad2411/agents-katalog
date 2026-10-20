---
description: Run IoT Security and Device Management Standards Check
globs: ["**/iot/**/*.ts", "**/device-security/**/*.ts", "**/firmware/**/*.ts", "**/embedded/**/*.ts"]
---
# Security: IoT Security & Device Management Standards

<audit_rules>
- You MUST implement proper device authentication with unique device identities and certificates.
- You MUST ensure secure firmware updates with signed packages and rollback protection.
- You MUST implement proper device-to-device and device-to-cloud communication encryption.
- You MUST configure proper device lifecycle management from provisioning to decommissioning.
- You MUST ensure proper device monitoring and anomaly detection for security threats.
- You MUST implement proper secure boot and trusted execution environments.
- You MUST configure proper device segmentation and network isolation.
- You MUST ensure proper data encryption at rest and in transit for IoT devices.
- You MUST implement proper vulnerability management and patch management for IoT devices.
- You MUST ensure proper physical security controls for IoT device deployments.
</audit_rules>

<example_good>
```typescript
// IoT Security Implementation

export class IoTSecurityManager {
  constructor(
    private deviceAuthenticator: DeviceAuthenticator,
    private firmwareManager: FirmwareManager,
    private networkSecurity: IoTNetworkSecurity,
    private deviceLifecycle: DeviceLifecycleManager,
    private threatDetector: IoTThreatDetector,
    private secureBoot: SecureBootManager,
    private vulnerabilityManager: VulnerabilityManager,
    private physicalSecurity: PhysicalSecurityManager
  ) {}

  async provisionDevice(device: DeviceProvisioningRequest): Promise<ProvisionedDevice> {
    // Validate device provisioning request
    const validation = await this.validateProvisioningRequest(device);
    if (!validation.valid) {
      throw new Error(`Invalid provisioning request: ${validation.errors.join(', ')}`);
    }

    // Generate unique device identity
    const deviceId = await this.generateDeviceIdentity(device);
    
    // Create device certificates
    const certificates = await this.deviceAuthenticator.createDeviceCertificates(deviceId, device);
    
    // Setup secure boot
    const secureBootConfig = await this.secureBoot.setupSecureBoot(deviceId, device.hardware);
    
    // Configure network security
    const networkConfig = await this.networkSecurity.configureDeviceNetworking(deviceId, device);
    
    // Initialize device monitoring
    const monitoringConfig = await this.setupDeviceMonitoring(deviceId);
    
    // Register device in lifecycle management
    const lifecycleState = await this.deviceLifecycle.registerDevice(deviceId, {
      state: 'provisioned',
      owner: device.owner,
      location: device.location,
      type: device.type,
      firmware: device.firmware,
    });

    return {
      deviceId,
      certificates,
      secureBootConfig,
      networkConfig,
      monitoringConfig,
      lifecycleState,
      provisioningTimestamp: Date.now(),
    };
  }

  async authenticateDevice(authRequest: DeviceAuthRequest): Promise<DeviceAuthResult> {
    // Validate device certificate
    const certValidation = await this.deviceAuthenticator.validateCertificate(authRequest.certificate);
    if (!certValidation.valid) {
      return { authenticated: false, reason: 'Invalid device certificate' };
    }

    // Check device status
    const deviceStatus = await this.deviceLifecycle.getDeviceStatus(authRequest.deviceId);
    if (deviceStatus.state !== 'active') {
      return { authenticated: false, reason: `Device not active: ${deviceStatus.state}` };
    }

    // Verify device integrity
    const integrityCheck = await this.secureBoot.verifyDeviceIntegrity(authRequest.deviceId);
    if (!integrityCheck.verified) {
      return { authenticated: false, reason: 'Device integrity verification failed' };
    }

    // Check for security threats
    const threatCheck = await this.threatDetector.checkDeviceThreats(authRequest.deviceId);
    if (threatCheck.hasThreats) {
      return { authenticated: false, reason: 'Security threats detected' };
    }

    // Generate device session token
    const sessionToken = await this.deviceAuthenticator.generateSessionToken(authRequest.deviceId);

    return {
      authenticated: true,
      deviceId: authRequest.deviceId,
      sessionToken,
      expiresAt: Date.now() + 3600000, // 1 hour
      permissions: await this.getDevicePermissions(authRequest.deviceId),
    };
  }

  async updateFirmware(updateRequest: FirmwareUpdateRequest): Promise<FirmwareUpdateResult> {
    // Validate update request
    const validation = await this.validateFirmwareUpdate(updateRequest);
    if (!validation.valid) {
      throw new Error(`Invalid firmware update: ${validation.errors.join(', ')}`);
    }

    // Get device status
    const deviceStatus = await this.deviceLifecycle.getDeviceStatus(updateRequest.deviceId);
    if (deviceStatus.state !== 'active') {
      throw new Error(`Cannot update device in state: ${deviceStatus.state}`);
    }

    // Verify firmware signature
    const signatureVerification = await this.firmwareManager.verifyFirmwareSignature(
      updateRequest.firmware,
      updateRequest.signature
    );
    if (!signatureVerification.valid) {
      throw new Error('Firmware signature verification failed');
    }

    // Check firmware compatibility
    const compatibilityCheck = await this.firmwareManager.checkCompatibility(
      updateRequest.deviceId,
      updateRequest.firmware
    );
    if (!compatibilityCheck.compatible) {
      throw new Error(`Firmware not compatible: ${compatibilityCheck.reason}`);
    }

    // Create backup of current firmware
    const backup = await this.firmwareManager.createBackup(updateRequest.deviceId);

    // Schedule firmware update
    const updateSchedule = await this.firmwareManager.scheduleUpdate({
      deviceId: updateRequest.deviceId,
      firmware: updateRequest.firmware,
      backup,
      scheduledTime: updateRequest.scheduledTime || Date.now(),
      rollbackEnabled: updateRequest.rollbackEnabled !== false,
    });

    return {
      updateId: updateSchedule.id,
      deviceId: updateRequest.deviceId,
      firmwareVersion: updateRequest.firmware.version,
      scheduledTime: updateSchedule.scheduledTime,
      backupId: backup.id,
      status: 'scheduled',
    };
  }

  async monitorDeviceSecurity(deviceId: string): Promise<DeviceSecurityReport> {
    // Get current device status
    const deviceStatus = await this.deviceLifecycle.getDeviceStatus(deviceId);
    
    // Check authentication status
    const authStatus = await this.deviceAuthenticator.getAuthenticationStatus(deviceId);
    
    // Analyze network traffic
    const networkAnalysis = await this.networkSecurity.analyzeNetworkTraffic(deviceId);
    
    // Detect threats
    const threatAnalysis = await this.threatDetector.analyzeDeviceThreats(deviceId);
    
    // Check firmware integrity
    const integrityCheck = await this.secureBoot.verifyFirmwareIntegrity(deviceId);
    
    // Check for vulnerabilities
    const vulnerabilityCheck = await this.vulnerabilityManager.checkDeviceVulnerabilities(deviceId);
    
    // Analyze physical security
    const physicalSecurityCheck = await this.physicalSecurity.checkPhysicalSecurity(deviceId);

    // Calculate overall security score
    const securityScore = this.calculateSecurityScore({
      authStatus,
      networkAnalysis,
      threatAnalysis,
      integrityCheck,
      vulnerabilityCheck,
      physicalSecurityCheck,
    });

    return {
      deviceId,
      timestamp: Date.now(),
      deviceStatus,
      securityScore,
      authStatus,
      networkAnalysis,
      threatAnalysis,
      integrityCheck,
      vulnerabilityCheck,
      physicalSecurityCheck,
      recommendations: this.generateSecurityRecommendations({
        authStatus,
        networkAnalysis,
        threatAnalysis,
        integrityCheck,
        vulnerabilityCheck,
        physicalSecurityCheck,
      }),
    };
  }

  async handleSecurityIncident(incident: SecurityIncident): Promise<IncidentResponse> {
    // Validate incident
    const validation = await this.validateSecurityIncident(incident);
    if (!validation.valid) {
      throw new Error(`Invalid security incident: ${validation.errors.join(', ')}`);
    }

    // Assess incident severity
    const severityAssessment = await this.assessIncidentSeverity(incident);
    
    // Isolate affected devices
    const isolation = await this.isolateAffectedDevices(incident.deviceIds);
    
    // Implement containment measures
    const containment = await this.implementContainment(incident, severityAssessment);
    
    // Notify security team
    const notification = await this.notifySecurityTeam(incident, severityAssessment);
    
    // Create incident response plan
    const responsePlan = await this.createResponsePlan(incident, severityAssessment);

    return {
      incidentId: incident.id,
      severity: severityAssessment.level,
      isolation,
      containment,
      notification,
      responsePlan,
      timestamp: Date.now(),
    };
  }

  private async generateDeviceIdentity(device: DeviceProvisioningRequest): Promise<DeviceIdentity> {
    // Generate unique device ID
    const deviceId = this.generateDeviceId(device.type, device.hardware.serialNumber);
    
    // Create device identity record
    const identity = {
      id: deviceId,
      type: device.type,
      manufacturer: device.hardware.manufacturer,
      model: device.hardware.model,
      serialNumber: device.hardware.serialNumber,
      hardwareId: device.hardware.id,
      createdAt: Date.now(),
    };

    return identity;
  }

  private async setupDeviceMonitoring(deviceId: string): Promise<DeviceMonitoringConfig> {
    const monitoringConfig = {
      deviceId,
      metrics: [
        'cpu_usage',
        'memory_usage',
        'network_traffic',
        'error_rate',
        'authentication_failures',
        'firmware_integrity',
      ],
      thresholds: {
        cpu_usage: 80,
        memory_usage: 85,
        error_rate: 5,
        authentication_failures: 3,
      },
      alerting: {
        enabled: true,
        channels: ['email', 'sms'],
        escalation: true,
      },
    };

    return monitoringConfig;
  }

  private calculateSecurityScore(checks: SecurityChecks): number {
    const weights = {
      authStatus: 0.25,
      networkAnalysis: 0.20,
      threatAnalysis: 0.20,
      integrityCheck: 0.15,
      vulnerabilityCheck: 0.15,
      physicalSecurityCheck: 0.05,
    };

    let totalScore = 0;
    for (const [check, weight] of Object.entries(weights)) {
      const score = this.getCheckScore(checks[check]);
      totalScore += score * weight;
    }

    return totalScore;
  }

  private getCheckScore(check: any): number {
    if (!check) return 0;
    
    if (check.score !== undefined) {
      return check.score;
    }
    
    if (check.valid !== undefined) {
      return check.valid ? 1.0 : 0.0;
    }
    
    if (check.verified !== undefined) {
      return check.verified ? 1.0 : 0.0;
    }
    
    return 0.5; // Default score
  }

  private generateSecurityRecommendations(checks: SecurityChecks): SecurityRecommendation[] {
    const recommendations = [];

    // Authentication recommendations
    if (checks.authStatus && !checks.authStatus.healthy) {
      recommendations.push({
        category: 'authentication',
        priority: 'high',
        action: 'Renew device certificates',
        reason: 'Device authentication issues detected',
      });
    }

    // Network security recommendations
    if (checks.networkAnalysis && checks.networkAnalysis.anomalies.length > 0) {
      recommendations.push({
        category: 'network',
        priority: 'medium',
        action: 'Review network traffic patterns',
        reason: 'Network anomalies detected',
      });
    }

    // Threat recommendations
    if (checks.threatAnalysis && checks.threatAnalysis.hasThreats) {
      recommendations.push({
        category: 'threat',
        priority: 'high',
        action: 'Investigate security threats',
        reason: 'Security threats detected',
      });
    }

    // Integrity recommendations
    if (checks.integrityCheck && !checks.integrityCheck.verified) {
      recommendations.push({
        category: 'integrity',
        priority: 'critical',
        action: 'Restore firmware integrity',
        reason: 'Firmware integrity compromised',
      });
    }

    // Vulnerability recommendations
    if (checks.vulnerabilityCheck && checks.vulnerabilityCheck.vulnerabilities.length > 0) {
      recommendations.push({
        category: 'vulnerability',
        priority: 'medium',
        action: 'Apply security patches',
        reason: 'Vulnerabilities detected',
      });
    }

    return recommendations;
  }

  private async assessIncidentSeverity(incident: SecurityIncident): Promise<SeverityAssessment> {
    const factors = {
      affectedDevices: incident.deviceIds.length,
      incidentType: incident.type,
      impact: incident.impact,
      exploitability: incident.exploitability,
    };

    // Calculate severity score
    let score = 0;
    
    // Device count factor
    if (factors.affectedDevices > 100) score += 0.4;
    else if (factors.affectedDevices > 10) score += 0.2;
    else if (factors.affectedDevices > 1) score += 0.1;
    
    // Incident type factor
    const typeScores = {
      'compromise': 0.4,
      'dos': 0.3,
      'data_breach': 0.5,
      'unauthorized_access': 0.3,
      'malware': 0.4,
    };
    score += typeScores[factors.incidentType] || 0.2;
    
    // Impact factor
    const impactScores = {
      'critical': 0.3,
      'high': 0.2,
      'medium': 0.1,
      'low': 0.05,
    };
    score += impactScores[factors.impact] || 0.1;
    
    // Exploitability factor
    const exploitabilityScores = {
      'high': 0.3,
      'medium': 0.15,
      'low': 0.05,
    };
    score += exploitabilityScores[factors.exploitability] || 0.1;

    // Determine severity level
    let level: SeverityLevel;
    if (score >= 0.8) level = 'critical';
    else if (score >= 0.6) level = 'high';
    else if (score >= 0.4) level = 'medium';
    else level = 'low';

    return {
      level,
      score,
      factors,
    };
  }

  private generateDeviceId(type: string, serialNumber: string): string {
    const hash = this.hashString(`${type}:${serialNumber}:${Date.now()}`);
    return `iot-${type}-${hash.substring(0, 12)}`;
  }

  private hashString(input: string): string {
    // Simple hash implementation - in production use proper cryptographic hash
    let hash = 0;
    for (let i = 0; i < input.length; i++) {
      const char = input.charCodeAt(i);
      hash = ((hash << 5) - hash) + char;
      hash = hash & hash; // Convert to 32-bit integer
    }
    return Math.abs(hash).toString(16);
  }
}

// Device Authenticator Implementation
export class DeviceAuthenticator {
  constructor(
    private certificateManager: CertificateManager,
    private tokenManager: TokenManager,
    private deviceRegistry: DeviceRegistry
  ) {}

  async createDeviceCertificates(deviceId: string, device: DeviceProvisioningRequest): Promise<DeviceCertificates> {
    // Create device certificate signing request
    const csr = await this.createCSR(deviceId, device);
    
    // Sign device certificate
    const deviceCert = await this.certificateManager.signCertificate(csr, {
      commonName: deviceId,
      organization: device.owner,
      deviceType: device.type,
      validity: 365 * 24 * 60 * 60 * 1000, // 1 year
    });

    // Create CA certificate chain
    const caChain = await this.certificateManager.getCertificateChain();

    return {
      deviceId,
      deviceCertificate: deviceCert,
      caChain,
      privateKey: csr.privateKey,
      publicKey: csr.publicKey,
      issuedAt: Date.now(),
      expiresAt: Date.now() + (365 * 24 * 60 * 60 * 1000),
    };
  }

  async validateCertificate(certificate: DeviceCertificate): Promise<CertificateValidation> {
    // Check certificate format
    if (!this.isValidCertificateFormat(certificate)) {
      return { valid: false, reason: 'Invalid certificate format' };
    }

    // Check certificate chain
    const chainValidation = await this.certificateManager.validateChain(certificate);
    if (!chainValidation.valid) {
      return { valid: false, reason: 'Certificate chain validation failed' };
    }

    // Check certificate expiration
    if (certificate.expiresAt < Date.now()) {
      return { valid: false, reason: 'Certificate expired' };
    }

    // Check certificate revocation
    const revocationCheck = await this.certificateManager.checkRevocation(certificate);
    if (revocationCheck.revoked) {
      return { valid: false, reason: 'Certificate revoked' };
    }

    return {
      valid: true,
      deviceId: certificate.deviceId,
      issuer: certificate.issuer,
      expiresAt: certificate.expiresAt,
    };
  }

  async generateSessionToken(deviceId: string): Promise<SessionToken> {
    const token = {
      deviceId,
      sessionId: this.generateSessionId(),
      issuedAt: Date.now(),
      expiresAt: Date.now() + 3600000, // 1 hour
      permissions: await this.getDevicePermissions(deviceId),
    };

    const signedToken = await this.tokenManager.signToken(token);

    return {
      token: signedToken,
      deviceId,
      sessionId: token.sessionId,
      expiresAt: token.expiresAt,
    };
  }

  async getAuthenticationStatus(deviceId: string): Promise<AuthenticationStatus> {
    const device = await this.deviceRegistry.getDevice(deviceId);
    if (!device) {
      return { healthy: false, reason: 'Device not found' };
    }

    const certValidation = await this.validateCertificate(device.certificates.deviceCertificate);
    if (!certValidation.valid) {
      return { healthy: false, reason: 'Certificate validation failed' };
    }

    return {
      healthy: true,
      lastAuthentication: device.lastAuthentication,
      certificateExpiresAt: certValidation.expiresAt,
    };
  }

  private async createCSR(deviceId: string, device: DeviceProvisioningRequest): Promise<CertificateSigningRequest> {
    // Generate key pair
    const keyPair = await this.generateKeyPair();
    
    // Create CSR
    const csr = {
      deviceId,
      commonName: deviceId,
      organization: device.owner,
      organizationalUnit: device.type,
      country: device.location.country || 'US',
      publicKey: keyPair.publicKey,
      privateKey: keyPair.privateKey,
    };

    return csr;
  }

  private async generateKeyPair(): Promise<KeyPair> {
    // In production, use proper cryptographic library
    const publicKey = `public_key_${Date.now()}`;
    const privateKey = `private_key_${Date.now()}`;
    
    return { publicKey, privateKey };
  }

  private generateSessionId(): string {
    return `session_${Date.now()}_${Math.random().toString(36).substring(2)}`;
  }

  private isValidCertificateFormat(certificate: DeviceCertificate): boolean {
    return !!(certificate.deviceId && certificate.publicKey && certificate.signature);
  }
}

// Firmware Manager Implementation
export class FirmwareManager {
  constructor(
    private signatureValidator: SignatureValidator,
    private compatibilityChecker: CompatibilityChecker,
    private backupManager: BackupManager,
    private updateScheduler: UpdateScheduler
  ) {}

  async verifyFirmwareSignature(firmware: Firmware, signature: string): Promise<SignatureVerification> {
    // Validate signature format
    if (!this.isValidSignatureFormat(signature)) {
      return { valid: false, reason: 'Invalid signature format' };
    }

    // Verify signature against firmware
    const verification = await this.signatureValidator.verify(firmware.hash, signature);
    
    return {
      valid: verification.valid,
      signer: verification.signer,
      timestamp: verification.timestamp,
    };
  }

  async checkCompatibility(deviceId: string, firmware: Firmware): Promise<CompatibilityCheck> {
    // Get device information
    const device = await this.getDeviceInfo(deviceId);
    
    // Check hardware compatibility
    const hardwareCheck = await this.compatibilityChecker.checkHardwareCompatibility(
      device.hardware,
      firmware.requirements.hardware
    );
    
    if (!hardwareCheck.compatible) {
      return {
        compatible: false,
        reason: `Hardware incompatibility: ${hardwareCheck.issues.join(', ')}`,
      };
    }

    // Check software compatibility
    const softwareCheck = await this.compatibilityChecker.checkSoftwareCompatibility(
      device.currentFirmware,
      firmware
    );
    
    if (!softwareCheck.compatible) {
      return {
        compatible: false,
        reason: `Software incompatibility: ${softwareCheck.issues.join(', ')}`,
      };
    }

    return {
      compatible: true,
      migrationRequired: softwareCheck.migrationRequired,
    };
  }

  async createBackup(deviceId: string): Promise<FirmwareBackup> {
    // Get current firmware
    const currentFirmware = await this.getCurrentFirmware(deviceId);
    
    // Create backup
    const backup = await this.backupManager.createBackup({
      deviceId,
      firmware: currentFirmware,
      timestamp: Date.now(),
    });

    return backup;
  }

  async scheduleUpdate(schedule: UpdateSchedule): Promise<ScheduledUpdate> {
    // Validate update schedule
    const validation = await this.validateUpdateSchedule(schedule);
    if (!validation.valid) {
      throw new Error(`Invalid update schedule: ${validation.errors.join(', ')}`);
    }

    // Schedule update
    const scheduled = await this.updateScheduler.schedule({
      id: generateId(),
      deviceId: schedule.deviceId,
      firmware: schedule.firmware,
      backup: schedule.backup,
      scheduledTime: schedule.scheduledTime,
      rollbackEnabled: schedule.rollbackEnabled,
      status: 'scheduled',
    });

    return scheduled;
  }

  private async getCurrentFirmware(deviceId: string): Promise<Firmware> {
    // Implementation to get current firmware from device
    return {
      version: '1.0.0',
      hash: 'current_hash',
      size: 1024000,
      requirements: {
        hardware: { ram: 512, storage: 1024 },
        software: { os: 'linux', version: '5.0' },
      },
    };
  }

  private async getDeviceInfo(deviceId: string): Promise<DeviceInfo> {
    // Implementation to get device information
    return {
      id: deviceId,
      hardware: {
        manufacturer: 'Example Corp',
        model: 'IoT-Device-1000',
        serialNumber: 'SN123456',
        ram: 512,
        storage: 1024,
        processor: 'ARM Cortex-M4',
      },
      currentFirmware: {
        version: '1.0.0',
        hash: 'current_hash',
      },
    };
  }

  private isValidSignatureFormat(signature: string): boolean {
    return signature && signature.length > 0;
  }

  private async validateUpdateSchedule(schedule: UpdateSchedule): Promise<ValidationResult> {
    const errors = [];

    // Check scheduled time
    if (schedule.scheduledTime && schedule.scheduledTime < Date.now()) {
      errors.push('Scheduled time cannot be in the past');
    }

    // Check firmware
    if (!schedule.firmware || !schedule.firmware.version) {
      errors.push('Firmware information is required');
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }
}

// IoT Network Security Implementation
export class IoTNetworkSecurity {
  constructor(
    private networkSegmenter: NetworkSegmenter,
    private trafficAnalyzer: TrafficAnalyzer,
    private encryptionManager: EncryptionManager
  ) {}

  async configureDeviceNetworking(deviceId: string, device: DeviceProvisioningRequest): Promise<NetworkConfig> {
    // Create network segment
    const segment = await this.networkSegmenter.createSegment({
      deviceId,
      deviceType: device.type,
      location: device.location,
      securityLevel: this.determineSecurityLevel(device.type),
    });

    // Configure encryption
    const encryptionConfig = await this.encryptionManager.configureDeviceEncryption({
      deviceId,
      algorithms: ['AES-256-GCM', 'ChaCha20-Poly1305'],
      keyRotation: 86400000, // 24 hours
    });

    // Setup traffic monitoring
    const monitoringConfig = await this.setupTrafficMonitoring(deviceId, segment);

    return {
      deviceId,
      segment,
      encryption: encryptionConfig,
      monitoring: monitoringConfig,
      firewall: await this.configureFirewall(deviceId, segment),
    };
  }

  async analyzeNetworkTraffic(deviceId: string): Promise<NetworkTrafficAnalysis> {
    // Collect traffic data
    const trafficData = await this.collectTrafficData(deviceId);
    
    // Analyze for anomalies
    const anomalies = await this.trafficAnalyzer.detectAnomalies(trafficData);
    
    // Check for suspicious patterns
    const suspiciousPatterns = await this.trafficAnalyzer.detectSuspiciousPatterns(trafficData);
    
    // Analyze communication patterns
    const communicationAnalysis = await this.analyzeCommunicationPatterns(trafficData);

    return {
      deviceId,
      timestamp: Date.now(),
      trafficVolume: trafficData.volume,
      connectionCount: trafficData.connections.length,
      anomalies,
      suspiciousPatterns,
      communicationAnalysis,
      riskScore: this.calculateNetworkRiskScore(anomalies, suspiciousPatterns),
    };
  }

  private determineSecurityLevel(deviceType: string): SecurityLevel {
    const levels = {
      'sensor': 'medium',
      'actuator': 'high',
      'gateway': 'high',
      'controller': 'critical',
    };
    
    return levels[deviceType] || 'medium';
  }

  private calculateNetworkRiskScore(anomalies: TrafficAnomaly[], patterns: SuspiciousPattern[]): number {
    const anomalyScore = anomalies.length * 0.3;
    const patternScore = patterns.length * 0.5;
    
    return Math.min(1.0, anomalyScore + patternScore);
  }

  private async setupTrafficMonitoring(deviceId: string, segment: NetworkSegment): Promise<TrafficMonitoringConfig> {
    return {
      deviceId,
      segmentId: segment.id,
      monitoringEnabled: true,
      alertThresholds: {
        connectionCount: 100,
        dataVolume: 1048576, // 1MB
        anomalyScore: 0.7,
      },
      retentionPeriod: 86400000, // 24 hours
    };
  }

  private async configureFirewall(deviceId: string, segment: NetworkSegment): Promise<FirewallConfig> {
    return {
      deviceId,
      segmentId: segment.id,
      rules: [
        {
          action: 'allow',
          protocol: 'tcp',
          destination: 'cloud-server',
          port: 443,
          description: 'Allow HTTPS to cloud server',
        },
        {
          action: 'allow',
          protocol: 'udp',
          destination: 'time-server',
          port: 123,
          description: 'Allow NTP for time synchronization',
        },
        {
          action: 'deny',
          protocol: 'all',
          destination: 'any',
          description: 'Deny all other traffic',
        },
      ],
      logging: true,
    };
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No IoT security implementation
export class BasicIoTDevice {
  // BAD: No device authentication
  async connect(device: any) {
    // BAD: No secure boot
    // BAD: No firmware security
    // BAD: No network encryption
    return this.network.connect(device);
  }

  // BAD: No device monitoring
  // BAD: No threat detection
  // BAD: No vulnerability management
  // BAD: No physical security
}
```
</example_bad>
