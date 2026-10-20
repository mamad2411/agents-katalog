---
description: Run Real-Time Security and Stream Processing Security Standards Check
globs: ["**/security/**/*.ts", "**/streaming-security/**/*.ts", "**/realtime-security/**/*.ts"]
---
# Security: Real-Time Security & Stream Processing Security

<audit_rules>
- You MUST implement proper authentication and authorization for streaming data producers and consumers.
- You MUST ensure end-to-end encryption for sensitive streaming data.
- You MUST implement proper input validation and sanitization for all stream events.
- You MUST configure proper rate limiting and quota management for stream producers.
- You MUST implement proper audit logging for all streaming operations.
- You MUST ensure proper data privacy and PII protection in streaming pipelines.
- You MUST configure proper network security for streaming infrastructure.
- You MUST implement proper anomaly detection and threat monitoring for streaming data.
- You MUST ensure proper secure key management for stream encryption.
- You MUST implement proper secure state management for stream processing applications.
</audit_rules>

<example_good>
```typescript
// Real-Time Security Implementation

export class StreamingSecurityManager {
  constructor(
    private authManager: StreamingAuthManager,
    private encryptionService: StreamingEncryptionService,
    private rateLimiter: StreamingRateLimiter,
    private auditLogger: StreamingAuditLogger,
    private anomalyDetector: StreamingAnomalyDetector,
    private keyManager: StreamingKeyManager
  ) {}

  async secureStreamProducer(producerConfig: ProducerConfig): Promise<SecureProducer> {
    // Authenticate producer
    const authResult = await this.authManager.authenticateProducer(producerConfig);
    if (!authResult.success) {
      throw new Error(`Producer authentication failed: ${authResult.reason}`);
    }

    // Authorize producer for topics
    await this.authorizeProducerForTopics(authResult.identity, producerConfig.topics);

    // Setup encryption
    const encryptionConfig = await this.setupProducerEncryption(producerConfig);

    // Setup rate limiting
    const rateLimitConfig = await this.setupProducerRateLimiting(producerConfig);

    // Create secure producer
    const producer = await this.createSecureProducer({
      ...producerConfig,
      auth: authResult,
      encryption: encryptionConfig,
      rateLimit: rateLimitConfig,
    });

    // Setup audit logging
    await this.auditLogger.logProducerCreation(producer.id, authResult.identity);

    return producer;
  }

  async secureStreamConsumer(consumerConfig: ConsumerConfig): Promise<SecureConsumer> {
    // Authenticate consumer
    const authResult = await this.authManager.authenticateConsumer(consumerConfig);
    if (!authResult.success) {
      throw new Error(`Consumer authentication failed: ${authResult.reason}`);
    }

    // Authorize consumer for topics
    await this.authorizeConsumerForTopics(authResult.identity, consumerConfig.topics);

    // Setup decryption
    const decryptionConfig = await this.setupConsumerDecryption(consumerConfig);

    // Setup rate limiting
    const rateLimitConfig = await this.setupConsumerRateLimiting(consumerConfig);

    // Create secure consumer
    const consumer = await this.createSecureConsumer({
      ...consumerConfig,
      auth: authResult,
      decryption: decryptionConfig,
      rateLimit: rateLimitConfig,
    });

    // Setup audit logging
    await this.auditLogger.logConsumerCreation(consumer.id, authResult.identity);

    return consumer;
  }

  async processSecureEvent(event: RawEvent, context: SecurityContext): Promise<ProcessedEvent> {
    // Validate event structure
    await this.validateEventStructure(event);

    // Authenticate event source
    const authResult = await this.authManager.authenticateEvent(event, context);
    if (!authResult.success) {
      await this.auditLogger.logEventAuthenticationFailure(event, authResult.reason);
      throw new Error(`Event authentication failed: ${authResult.reason}`);
    }

    // Decrypt event if encrypted
    const decryptedEvent = await this.decryptEventIfNeeded(event, authResult);

    // Validate and sanitize event data
    const sanitizedEvent = await this.validateAndSanitizeEvent(decryptedEvent);

    // Check for anomalies
    const anomalyResult = await this.anomalyDetector.analyzeEvent(sanitizedEvent, context);
    if (anomalyResult.isAnomalous) {
      await this.handleAnomalousEvent(sanitizedEvent, anomalyResult);
    }

    // Apply data privacy controls
    const privacyFilteredEvent = await this.applyPrivacyControls(sanitizedEvent, context);

    // Log event processing
    await this.auditLogger.logEventProcessing(privacyFilteredEvent.id, context);

    return privacyFilteredEvent;
  }

  async setupStreamEncryption(streamConfig: StreamConfig): Promise<EncryptionConfig> {
    // Generate encryption keys
    const keyId = await this.keyManager.generateKey({
      algorithm: 'AES-256-GCM',
      usage: 'encrypt/decrypt',
      rotationPeriod: 86400000, // 24 hours
    });

    // Setup key rotation
    await this.keyManager.setupKeyRotation(keyId, {
      rotationInterval: 86400000,
      retentionPeriod: 604800000, // 7 days
    });

    return {
      keyId,
      algorithm: 'AES-256-GCM',
      keyRotation: true,
      dataClassification: streamConfig.dataClassification,
    };
  }

  async authorizeProducerForTopics(identity: ProducerIdentity, topics: string[]): Promise<void> {
    for (const topic of topics) {
      const hasPermission = await this.authManager.checkTopicPermission(
        identity,
        topic,
        'produce'
      );

      if (!hasPermission) {
        throw new Error(`Producer not authorized to produce to topic: ${topic}`);
      }
    }
  }

  async authorizeConsumerForTopics(identity: ConsumerIdentity, topics: string[]): Promise<void> {
    for (const topic of topics) {
      const hasPermission = await this.authManager.checkTopicPermission(
        identity,
        topic,
        'consume'
      );

      if (!hasPermission) {
        throw new Error(`Consumer not authorized to consume from topic: ${topic}`);
      }
    }
  }

  private async validateEventStructure(event: RawEvent): Promise<void> {
    const requiredFields = ['id', 'type', 'timestamp', 'source'];
    
    for (const field of requiredFields) {
      if (!event[field]) {
        throw new Error(`Missing required field: ${field}`);
      }
    }

    // Validate timestamp
    const eventTime = new Date(event.timestamp);
    const now = new Date();
    const maxAge = 300000; // 5 minutes

    if (Math.abs(now.getTime() - eventTime.getTime()) > maxAge) {
      throw new Error('Event timestamp is too old or too far in the future');
    }

    // Validate event size
    const eventSize = JSON.stringify(event).length;
    const maxEventSize = 1024 * 1024; // 1MB

    if (eventSize > maxEventSize) {
      throw new Error('Event size exceeds maximum allowed size');
    }
  }

  private async decryptEventIfNeeded(event: RawEvent, authResult: AuthResult): Promise<DecryptedEvent> {
    if (!event.encrypted) {
      return event as DecryptedEvent;
    }

    const keyId = event.encryptionKeyId;
    if (!keyId) {
      throw new Error('Encrypted event missing encryption key ID');
    }

    // Check if we have access to the key
    const hasKeyAccess = await this.keyManager.checkKeyAccess(authResult.identity, keyId);
    if (!hasKeyAccess) {
      throw new Error('No access to encryption key');
    }

    // Decrypt event
    const decryptedData = await this.encryptionService.decrypt(event.data, keyId);
    
    return {
      ...event,
      data: decryptedData,
      encrypted: false,
    };
  }

  private async validateAndSanitizeEvent(event: DecryptedEvent): Promise<ValidatedEvent> {
    // Validate event type
    const validEventTypes = ['user_action', 'system_event', 'transaction', 'sensor_data'];
    if (!validEventTypes.includes(event.type)) {
      throw new Error(`Invalid event type: ${event.type}`);
    }

    // Sanitize event data
    const sanitizedData = await this.sanitizeEventData(event.data, event.type);

    // Validate event data schema
    await this.validateEventDataSchema(sanitizedData, event.type);

    return {
      ...event,
      data: sanitizedData,
      validated: true,
    };
  }

  private async sanitizeEventData(data: any, eventType: string): Promise<any> {
    switch (eventType) {
      case 'user_action':
        return this.sanitizeUserActionData(data);
      case 'system_event':
        return this.sanitizeSystemEventData(data);
      case 'transaction':
        return this.sanitizeTransactionData(data);
      case 'sensor_data':
        return this.sanitizeSensorData(data);
      default:
        throw new Error(`Unknown event type for sanitization: ${eventType}`);
    }
  }

  private sanitizeUserActionData(data: any): any {
    // Remove or mask sensitive fields
    const sanitized = { ...data };

    // Mask PII
    if (sanitized.email) {
      sanitized.email = this.maskEmail(sanitized.email);
    }

    if (sanitized.phoneNumber) {
      sanitized.phoneNumber = this.maskPhoneNumber(sanitized.phoneNumber);
    }

    // Remove sensitive fields
    delete sanitized.password;
    delete sanitized.ssn;
    delete sanitized.creditCard;

    return sanitized;
  }

  private sanitizeSystemEventData(data: any): any {
    // Remove sensitive system information
    const sanitized = { ...data };

    delete sanitized.internalIP;
    delete sanitized.systemKey;
    delete sanitized.adminToken;

    return sanitized;
  }

  private sanitizeTransactionData(data: any): any {
    // Mask financial information
    const sanitized = { ...data };

    if (sanitized.accountNumber) {
      sanitized.accountNumber = this.maskAccountNumber(sanitized.accountNumber);
    }

    if (sanitized.cardNumber) {
      sanitized.cardNumber = this.maskCardNumber(sanitized.cardNumber);
    }

    return sanitized;
  }

  private sanitizeSensorData(data: any): any {
    // Validate sensor data ranges
    const sanitized = { ...data };

    if (sanitized.temperature !== undefined) {
      if (sanitized.temperature < -100 || sanitized.temperature > 200) {
        throw new Error('Temperature value out of valid range');
      }
    }

    if (sanitized.humidity !== undefined) {
      if (sanitized.humidity < 0 || sanitized.humidity > 100) {
        throw new Error('Humidity value out of valid range');
      }
    }

    return sanitized;
  }

  private async validateEventDataSchema(data: any, eventType: string): Promise<void> {
    const schemas = {
      'user_action': {
        required: ['userId', 'action', 'timestamp'],
        optional: ['metadata', 'sessionId'],
      },
      'system_event': {
        required: ['systemId', 'event', 'timestamp'],
        optional: ['severity', 'details'],
      },
      'transaction': {
        required: ['transactionId', 'amount', 'currency', 'timestamp'],
        optional: ['metadata', 'status'],
      },
      'sensor_data': {
        required: ['sensorId', 'timestamp'],
        optional: ['temperature', 'humidity', 'pressure'],
      },
    };

    const schema = schemas[eventType];
    if (!schema) {
      throw new Error(`No schema found for event type: ${eventType}`);
    }

    // Check required fields
    for (const field of schema.required) {
      if (!data[field]) {
        throw new Error(`Missing required field: ${field}`);
      }
    }

    // Validate field types
    await this.validateFieldTypes(data, eventType);
  }

  private async validateFieldTypes(data: any, eventType: string): Promise<void> {
    const typeValidators = {
      'user_action': {
        userId: 'string',
        action: 'string',
        timestamp: 'number',
      },
      'transaction': {
        transactionId: 'string',
        amount: 'number',
        currency: 'string',
        timestamp: 'number',
      },
    };

    const validators = typeValidators[eventType];
    if (!validators) return;

    for (const [field, expectedType] of Object.entries(validators)) {
      if (data[field] !== undefined && typeof data[field] !== expectedType) {
        throw new Error(`Field ${field} must be of type ${expectedType}`);
      }
    }
  }

  private async handleAnomalousEvent(event: ValidatedEvent, anomalyResult: AnomalyResult): Promise<void> {
    // Log anomaly
    await this.auditLogger.logAnomalousEvent(event.id, anomalyResult);

    // Block event if high severity
    if (anomalyResult.severity === 'high') {
      throw new Error('Event blocked due to high-severity anomaly');
    }

    // Add security metadata
    event.securityMetadata = {
      anomalyScore: anomalyResult.score,
      anomalyReasons: anomalyResult.reasons,
      processedWithWarning: true,
    };
  }

  private async applyPrivacyControls(event: ValidatedEvent, context: SecurityContext): Promise<ProcessedEvent> {
    // Apply data retention policies
    const retentionFiltered = await this.applyDataRetention(event, context);

    // Apply geographical restrictions
    const geoFiltered = await this.applyGeographicalRestrictions(retentionFiltered, context);

    // Apply purpose limitation
    const purposeFiltered = await this.applyPurposeLimitation(geoFiltered, context);

    return purposeFiltered;
  }

  private maskEmail(email: string): string {
    const [username, domain] = email.split('@');
    const maskedUsername = username.slice(0, 2) + '*'.repeat(username.length - 2);
    return `${maskedUsername}@${domain}`;
  }

  private maskPhoneNumber(phone: string): string {
    return phone.slice(0, 3) + '*'.repeat(phone.length - 6) + phone.slice(-3);
  }

  private maskAccountNumber(account: string): string {
    return '*'.repeat(account.length - 4) + account.slice(-4);
  }

  private maskCardNumber(card: string): string {
    return '*'.repeat(card.length - 4) + card.slice(-4);
  }
}

// Streaming Authentication Manager
export class StreamingAuthManager {
  async authenticateProducer(config: ProducerConfig): Promise<AuthResult> {
    // Validate producer credentials
    const credentials = config.credentials;
    
    if (!credentials.apiKey || !credentials.apiSecret) {
      return { success: false, reason: 'Missing API credentials' };
    }

    // Verify API key and secret
    const isValid = await this.verifyApiCredentials(credentials.apiKey, credentials.apiSecret);
    if (!isValid) {
      return { success: false, reason: 'Invalid API credentials' };
    }

    // Get producer identity
    const identity = await this.getIdentityFromApiKey(credentials.apiKey);

    return {
      success: true,
      identity,
      permissions: await this.getProducerPermissions(identity),
    };
  }

  async authenticateConsumer(config: ConsumerConfig): Promise<AuthResult> {
    // Validate consumer credentials
    const credentials = config.credentials;
    
    if (!credentials.token) {
      return { success: false, reason: 'Missing authentication token' };
    }

    // Verify JWT token
    const tokenPayload = await this.verifyJwtToken(credentials.token);
    if (!tokenPayload) {
      return { success: false, reason: 'Invalid authentication token' };
    }

    return {
      success: true,
      identity: tokenPayload.identity,
      permissions: await this.getConsumerPermissions(tokenPayload.identity),
    };
  }

  async authenticateEvent(event: RawEvent, context: SecurityContext): Promise<AuthResult> {
    // Verify event signature
    if (event.signature) {
      const isValidSignature = await this.verifyEventSignature(event);
      if (!isValidSignature) {
        return { success: false, reason: 'Invalid event signature' };
      }
    }

    // Check source authorization
    const isAuthorized = await this.checkSourceAuthorization(event.source, context);
    if (!isAuthorized) {
      return { success: false, reason: 'Source not authorized' };
    }

    return {
      success: true,
      identity: { type: 'system', id: event.source },
      permissions: ['produce'],
    };
  }

  private async verifyApiCredentials(apiKey: string, apiSecret: string): Promise<boolean> {
    // Implement API key verification logic
    return true; // Placeholder
  }

  private async getIdentityFromApiKey(apiKey: string): Promise<ProducerIdentity> {
    // Implement identity resolution from API key
    return {
      type: 'service',
      id: 'service-123',
      name: 'my-service',
      organization: 'my-org',
    };
  }

  private async verifyJwtToken(token: string): Promise<JwtPayload | null> {
    // Implement JWT verification logic
    return null; // Placeholder
  }
}

// Streaming Rate Limiter
export class StreamingRateLimiter {
  async checkProducerRate(identity: ProducerIdentity, topic: string): Promise<RateLimitResult> {
    const key = `producer:${identity.id}:${topic}`;
    const limit = await this.getProducerRateLimit(identity, topic);
    const current = await this.getCurrentRate(key);

    if (current >= limit) {
      return {
        allowed: false,
        limit,
        current,
        resetTime: await this.getResetTime(key),
      };
    }

    await this.incrementRate(key);
    
    return {
      allowed: true,
      limit,
      current: current + 1,
      resetTime: await this.getResetTime(key),
    };
  }

  private async getProducerRateLimit(identity: ProducerIdentity, topic: string): Promise<number> {
    // Implement rate limit logic based on identity and topic
    return 1000; // Placeholder
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No real-time security measures
export class InsecureStreamProcessor {
  // BAD: No authentication
  async processEvent(event: any) {
    // BAD: No validation
    // BAD: No encryption
    // BAD: No rate limiting
    // BAD: No audit logging
    // BAD: No anomaly detection
    return await this.process(event);
  }

  // BAD: No security controls
  // BAD: No privacy protection
  // BAD: No threat monitoring
}
```
</example_bad>
