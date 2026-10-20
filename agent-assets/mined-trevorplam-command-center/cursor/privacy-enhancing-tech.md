---
description: Run Privacy-Enhancing Technologies and Data Protection Standards Check
globs: ["**/privacy/**/*.ts", "**/pet/**/*.ts", "**/differential-privacy/**/*.ts", "**/homomorphic-encryption/**/*.ts"]
---
# Security: Privacy-Enhancing Technologies & Data Protection Standards

<audit_rules>
- You MUST implement proper differential privacy with epsilon-delta privacy guarantees.
- You MUST ensure homomorphic encryption for secure computation on encrypted data.
- You MUST implement proper secure multi-party computation for collaborative analytics.
- You MUST configure proper zero-knowledge proofs for privacy-preserving verification.
- You MUST ensure proper data anonymization and pseudonymization techniques.
- You MUST implement proper privacy budgeting and tracking for differential privacy.
- You MUST configure proper secure aggregation for federated learning and analytics.
- You MUST ensure proper privacy-preserving machine learning techniques.
- You MUST implement proper data minimization and purpose limitation controls.
- You MUST ensure proper compliance with GDPR, CCPA, and other privacy regulations.
</audit_rules>

<example_good>
```typescript
// Privacy-Enhancing Technologies Implementation

export class PrivacyEnhancingTechOrchestrator {
  constructor(
    private differentialPrivacy: DifferentialPrivacyEngine,
    private homomorphicEncryption: HomomorphicEncryptionEngine,
    private secureAggregation: SecureAggregationEngine,
    private zkProofEngine: ZeroKnowledgeProofEngine,
    private privacyBudgetManager: PrivacyBudgetManager,
    private dataAnonymizer: DataAnonymizer,
    private complianceChecker: ComplianceChecker
  ) {}

  async applyDifferentialPrivacy(dataset: Dataset, config: DPConfig): Promise<DPProtectedDataset> {
    // Validate privacy budget
    const budgetCheck = await this.privacyBudgetManager.checkBudget(config.userId, config.epsilon);
    if (!budgetCheck.available) {
      throw new Error(`Insufficient privacy budget. Available: ${budgetCheck.remaining}`);
    }

    // Apply differential privacy mechanisms
    const protectedData = await this.differentialPrivacy.protect(dataset, {
      epsilon: config.epsilon,
      delta: config.delta || 1e-5,
      mechanism: config.mechanism || 'laplace',
      sensitivity: config.sensitivity,
    });

    // Update privacy budget
    await this.privacyBudgetManager.consumeBudget(config.userId, config.epsilon, {
      operation: 'dp_protection',
      datasetSize: dataset.samples.length,
      timestamp: Date.now(),
    });

    // Generate privacy report
    const privacyReport = await this.generatePrivacyReport(protectedData, config);

    return {
      ...protectedData,
      privacyReport,
      budgetRemaining: budgetCheck.remaining - config.epsilon,
    };
  }

  async performSecureComputation(computation: SecureComputationRequest): Promise<SecureComputationResult> {
    // Validate computation request
    const validation = await this.validateSecureComputation(computation);
    if (!validation.valid) {
      throw new Error(`Invalid computation request: ${validation.errors.join(', ')}`);
    }

    // Setup homomorphic encryption
    const encryptionSetup = await this.homomorphicEncryption.setup({
      scheme: computation.encryptionScheme || 'bfv',
      parameters: computation.encryptionParameters,
    });

    // Encrypt input data
    const encryptedInputs = await this.encryptInputs(computation.inputs, encryptionSetup);

    // Perform secure computation
    const encryptedResult = await this.performComputationOnEncryptedData(
      computation.operation,
      encryptedInputs,
      encryptionSetup
    );

    // Decrypt result
    const result = await this.homomorphicEncryption.decrypt(encryptedResult, encryptionSetup);

    // Generate computation report
    const computationReport = await this.generateComputationReport(computation, result);

    return {
      result,
      computationReport,
      privacyGuarantees: this.getPrivacyGuarantees(computation.privacyTechniques),
    };
  }

  async generateZeroKnowledgeProof(statement: ZKStatement, witness: ZKWitness): Promise<ZKProof> {
    // Validate statement and witness
    const validation = await this.validateZKComponents(statement, witness);
    if (!validation.valid) {
      throw new Error(`Invalid ZK components: ${validation.errors.join(', ')}`);
    }

    // Choose proof system
    const proofSystem = this.selectProofSystem(statement.type);
    
    // Generate proof
    const proof = await this.zkProofEngine.generateProof({
      statement,
      witness,
      proofSystem,
      parameters: statement.parameters,
    });

    // Verify proof
    const verification = await this.zkProofEngine.verifyProof(proof, statement);
    if (!verification.valid) {
      throw new Error('Generated proof failed verification');
    }

    return proof;
  }

  async performSecureAggregation(participants: Participant[], data: AggregatedData[]): Promise<SecureAggregationResult> {
    // Validate participants
    await this.validateParticipants(participants);

    // Setup secure aggregation protocol
    const protocol = await this.secureAggregation.setupProtocol({
      participants: participants.length,
      threshold: Math.floor(participants.length / 2) + 1,
      scheme: 'shamir',
    });

    // Generate secret shares
    const shares = await this.generateSecretShares(data, protocol);

    // Distribute shares to participants
    await this.distributeShares(shares, participants);

    // Collect shares and reconstruct result
    const reconstructedResult = await this.reconstructAggregatedResult(shares, protocol);

    // Generate aggregation report
    const aggregationReport = await this.generateAggregationReport(participants, reconstructedResult);

    return {
      result: reconstructedResult,
      aggregationReport,
      participants: participants.length,
      privacyLevel: this.calculatePrivacyLevel(participants.length, protocol.threshold),
    };
  }

  async anonymizeDataset(dataset: Dataset, config: AnonymizationConfig): Promise<AnonymizedDataset> {
    // Validate anonymization requirements
    const validation = await this.validateAnonymizationConfig(config);
    if (!validation.valid) {
      throw new Error(`Invalid anonymization config: ${validation.errors.join(', ')}`);
    }

    // Apply anonymization techniques
    const anonymizedData = await this.dataAnonymizer.anonymize(dataset, {
      techniques: config.techniques || ['k-anonymity', 'l-diversity'],
      k: config.k || 5,
      l: config.l || 3,
      quasiIdentifiers: config.quasiIdentifiers,
      sensitiveAttributes: config.sensitiveAttributes,
    });

    // Verify anonymization quality
    const qualityCheck = await this.verifyAnonymizationQuality(anonymizedData, config);
    if (!qualityCheck.sufficient) {
      throw new Error(`Anonymization quality insufficient: ${qualityCheck.issues.join(', ')}`);
    }

    // Check compliance
    const complianceCheck = await this.complianceChecker.checkAnonymization(anonymizedData, config.regulations);
    if (!complianceCheck.compliant) {
      throw new Error(`Anonymization not compliant: ${complianceCheck.violations.join(', ')}`);
    }

    return anonymizedData;
  }

  async performPrivacyPreservingML(mlConfig: PrivacyPreservingMLConfig): Promise<MLResult> {
    // Setup federated learning environment
    const flEnvironment = await this.setupFederatedLearning(mlConfig);

    // Train models with privacy preservation
    const models = await this.trainWithPrivacyPreservation(mlConfig, flEnvironment);

    // Aggregate models securely
    const aggregatedModel = await this.secureAggregation.aggregateModels(models, {
      technique: 'secure_aggregation',
      privacyBudget: mlConfig.privacyBudget,
    });

    // Validate model performance
    const performanceValidation = await this.validateModelPerformance(aggregatedModel, mlConfig.testData);

    // Check privacy guarantees
    const privacyGuarantees = await this.calculatePrivacyGuarantees(mlConfig, aggregatedModel);

    return {
      model: aggregatedModel,
      performance: performanceValidation,
      privacyGuarantees,
      compliance: await this.checkMLCompliance(aggregatedModel, mlConfig.regulations),
    };
  }

  private async validateSecureComputation(request: SecureComputationRequest): Promise<ValidationResult> {
    const errors = [];

    // Validate operation
    const validOperations = ['addition', 'multiplication', 'comparison', 'sorting'];
    if (!validOperations.includes(request.operation)) {
      errors.push(`Invalid operation: ${request.operation}`);
    }

    // Validate inputs
    if (!request.inputs || request.inputs.length === 0) {
      errors.push('No inputs provided');
    }

    // Validate privacy techniques
    const validTechniques = ['homomorphic_encryption', 'secure_multiparty_computation', 'oblivious_transfer'];
    for (const technique of request.privacyTechniques) {
      if (!validTechniques.includes(technique)) {
        errors.push(`Invalid privacy technique: ${technique}`);
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private async encryptInputs(inputs: any[], encryptionSetup: EncryptionSetup): Promise<EncryptedInput[]> {
    const encrypted = [];

    for (const input of inputs) {
      const encryptedInput = await this.homomorphicEncryption.encrypt(input, encryptionSetup);
      encrypted.push(encryptedInput);
    }

    return encrypted;
  }

  private async performComputationOnEncryptedData(
    operation: string,
    encryptedInputs: EncryptedInput[],
    encryptionSetup: EncryptionSetup
  ): Promise<EncryptedResult> {
    switch (operation) {
      case 'addition':
        return await this.homomorphicEncryption.add(encryptedInputs, encryptionSetup);
      case 'multiplication':
        return await this.homomorphicEncryption.multiply(encryptedInputs, encryptionSetup);
      case 'comparison':
        return await this.homomorphicEncryption.compare(encryptedInputs, encryptionSetup);
      default:
        throw new Error(`Unsupported operation: ${operation}`);
    }
  }

  private async validateZKComponents(statement: ZKStatement, witness: ZKWitness): Promise<ValidationResult> {
    const errors = [];

    // Validate statement structure
    if (!statement.type || !statement.circuit) {
      errors.push('Invalid statement structure');
    }

    // Validate witness
    if (!witness.values || !witness.publicInputs) {
      errors.push('Invalid witness structure');
    }

    // Check consistency between statement and witness
    if (statement.publicInputs && witness.publicInputs) {
      if (statement.publicInputs.length !== witness.publicInputs.length) {
        errors.push('Public inputs mismatch between statement and witness');
      }
    }

    return {
      valid: errors.length === 0,
      errors,
    };
  }

  private selectProofSystem(statementType: string): ProofSystem {
    const systems = {
      'range_proof': 'bulletproofs',
      'membership_proof': 'zk_snarks',
      'equality_proof': 'zk_starks',
      'computation_proof': 'plonk',
    };

    return systems[statementType] || 'zk_snarks';
  }

  private async validateParticipants(participants: Participant[]): Promise<void> {
    if (participants.length < 3) {
      throw new Error('Minimum 3 participants required for secure aggregation');
    }

    for (const participant of participants) {
      if (!participant.id || !participant.publicKey) {
        throw new Error('Invalid participant configuration');
      }
    }
  }

  private async generateSecretShares(data: AggregatedData[], protocol: AggregationProtocol): Promise<SecretShare[]> {
    const shares = [];

    for (const item of data) {
      const itemShares = await this.secureAggregation.createShares(item.value, protocol);
      shares.push(...itemShares.map((share, index) => ({
        id: `${item.id}_share_${index}`,
        participantId: protocol.participants[index],
        value: share,
        itemId: item.id,
      })));
    }

    return shares;
  }

  private async verifyAnonymizationQuality(data: AnonymizedDataset, config: AnonymizationConfig): Promise<QualityCheck> {
    const issues = [];

    // Check k-anonymity
    if (config.techniques.includes('k-anonymity')) {
      const kAnonymityCheck = await this.checkKAnonymity(data, config.k);
      if (!kAnonymityCheck.satisfied) {
        issues.push(`k-anonymity not satisfied: ${kAnonymityCheck.violations} violations`);
      }
    }

    // Check l-diversity
    if (config.techniques.includes('l-diversity')) {
      const lDiversityCheck = await this.checkLDiversity(data, config.l);
      if (!lDiversityCheck.satisfied) {
        issues.push(`l-diversity not satisfied: ${lDiversityCheck.violations} violations`);
      }
    }

    // Check t-closeness
    if (config.techniques.includes('t-closeness')) {
      const tClosenessCheck = await this.checkTCloseness(data, config.t);
      if (!tClosenessCheck.satisfied) {
        issues.push(`t-closeness not satisfied: ${tClosenessCheck.violations} violations`);
      }
    }

    return {
      sufficient: issues.length === 0,
      issues,
      qualityScore: this.calculateQualityScore(issues.length, config.techniques.length),
    };
  }

  private calculateQualityScore(violations: number, techniques: number): number {
    return Math.max(0, 1 - (violations / techniques));
  }

  private calculatePrivacyLevel(participants: number, threshold: number): PrivacyLevel {
    if (threshold >= participants) return 'high';
    if (threshold >= participants / 2) return 'medium';
    return 'low';
  }
}

// Differential Privacy Engine Implementation
export class DifferentialPrivacyEngine {
  constructor(
    private noiseGenerator: NoiseGenerator,
    private sensitivityCalculator: SensitivityCalculator
  ) {}

  async protect(dataset: Dataset, config: DPConfig): Promise<DPProtectedDataset> {
    const protectedData = {
      ...dataset,
      samples: [],
    };

    for (const sample of dataset.samples) {
      const protectedSample = await this.protectSample(sample, config);
      protectedData.samples.push(protectedSample);
    }

    return {
      ...protectedData,
      epsilon: config.epsilon,
      delta: config.delta,
      mechanism: config.mechanism,
      sensitivity: config.sensitivity,
    };
  }

  async protectSample(sample: any, config: DPConfig): Promise<any> {
    const protectedSample = { ...sample };

    // Apply noise to numerical attributes
    for (const [attribute, value] of Object.entries(sample)) {
      if (typeof value === 'number') {
        const sensitivity = await this.sensitivityCalculator.calculateSensitivity(attribute, config);
        const noise = await this.generateNoise(config.mechanism, sensitivity, config.epsilon);
        protectedSample[attribute] = value + noise;
      }
    }

    return protectedSample;
  }

  private async generateNoise(mechanism: string, sensitivity: number, epsilon: number): Promise<number> {
    switch (mechanism) {
      case 'laplace':
        return this.noiseGenerator.laplace(sensitivity / epsilon);
      case 'gaussian':
        return this.noiseGenerator.gaussian(sensitivity / epsilon);
      case 'exponential':
        return this.noiseGenerator.exponential(sensitivity / epsilon);
      default:
        throw new Error(`Unknown noise mechanism: ${mechanism}`);
    }
  }
}

// Homomorphic Encryption Engine Implementation
export class HomomorphicEncryptionEngine {
  constructor(
    private encryptionScheme: EncryptionScheme,
    private keyManager: HEKeyManager
  ) {}

  async setup(config: HEConfig): Promise<EncryptionSetup> {
    // Generate keys
    const keyPair = await this.keyManager.generateKeys(config);

    return {
      scheme: config.scheme,
      publicKey: keyPair.publicKey,
      secretKey: keyPair.secretKey,
      parameters: config.parameters,
    };
  }

  async encrypt(data: any, setup: EncryptionSetup): Promise<EncryptedData> {
    return await this.encryptionScheme.encrypt(data, setup.publicKey, setup.parameters);
  }

  async decrypt(encryptedData: EncryptedData, setup: EncryptionSetup): Promise<any> {
    return await this.encryptionScheme.decrypt(encryptedData, setup.secretKey, setup.parameters);
  }

  async add(encryptedInputs: EncryptedInput[], setup: EncryptionSetup): Promise<EncryptedResult> {
    return await this.encryptionScheme.add(encryptedInputs, setup.publicKey, setup.parameters);
  }

  async multiply(encryptedInputs: EncryptedInput[], setup: EncryptionSetup): Promise<EncryptedResult> {
    return await this.encryptionScheme.multiply(encryptedInputs, setup.publicKey, setup.parameters);
  }
}

// Secure Aggregation Engine Implementation
export class SecureAggregationEngine {
  constructor(
    private shamirSecretSharing: ShamirSecretSharing,
    private commitmentScheme: CommitmentScheme
  ) {}

  async setupProtocol(config: AggregationProtocolConfig): Promise<AggregationProtocol> {
    return {
      scheme: config.scheme,
      threshold: config.threshold,
      participants: config.participants,
      prime: this.generateLargePrime(),
    };
  }

  async createShares(value: number, protocol: AggregationProtocol): Promise<SecretShare[]> {
    return await this.shamirSecretSharing.split(value, protocol.threshold, protocol.participants, protocol.prime);
  }

  async aggregateModels(models: FederatedModel[], config: SecureAggregationConfig): Promise<AggregatedModel> {
    // Generate shares for each model
    const allShares = [];
    
    for (const model of models) {
      const modelShares = await this.createShares(model.weights, config.protocol);
      allShares.push(modelShares);
    }

    // Aggregate shares
    const aggregatedShares = await this.aggregateShares(allShares, config.protocol);

    // Reconstruct aggregated model
    const aggregatedWeights = await this.reconstructWeights(aggregatedShares, config.protocol);

    return {
      weights: aggregatedWeights,
      participants: models.length,
      privacyBudget: config.privacyBudget,
    };
  }

  private async aggregateShares(shares: SecretShare[][], protocol: AggregationProtocol): Promise<SecretShare[]> {
    const aggregated = [];

    for (let i = 0; i < protocol.threshold; i++) {
      const shareSum = shares.reduce((sum, participantShares) => {
        const share = participantShares[i];
        return sum + share.value;
      }, 0);

      aggregated.push({
        id: `aggregated_share_${i}`,
        value: shareSum,
        index: i,
      });
    }

    return aggregated;
  }

  private async reconstructWeights(shares: SecretShare[], protocol: AggregationProtocol): Promise<number[]> {
    return await this.shamirSecretSharing.reconstruct(shares, protocol.prime);
  }
}

// Zero Knowledge Proof Engine Implementation
export class ZeroKnowledgeProofEngine {
  constructor(
    private proofSystems: Map<string, ZKProofSystem>,
    private circuitBuilder: CircuitBuilder
  ) {}

  async generateProof(config: ZKProofConfig): Promise<ZKProof> {
    const proofSystem = this.proofSystems.get(config.proofSystem);
    if (!proofSystem) {
      throw new Error(`Unknown proof system: ${config.proofSystem}`);
    }

    // Build circuit if needed
    const circuit = await this.circuitBuilder.build(config.statement.circuit);

    // Generate proving key and verification key
    const keys = await proofSystem.setup(circuit);

    // Generate proof
    const proof = await proofSystem.prove({
      circuit,
      witness: config.witness,
      provingKey: keys.provingKey,
      publicInputs: config.statement.publicInputs,
    });

    return {
      proof,
      verificationKey: keys.verificationKey,
      publicInputs: config.statement.publicInputs,
      proofSystem: config.proofSystem,
    };
  }

  async verifyProof(proof: ZKProof, statement: ZKStatement): Promise<ProofVerification> {
    const proofSystem = this.proofSystems.get(proof.proofSystem);
    if (!proofSystem) {
      throw new Error(`Unknown proof system: ${proof.proofSystem}`);
    }

    const isValid = await proofSystem.verify({
      proof: proof.proof,
      verificationKey: proof.verificationKey,
      publicInputs: statement.publicInputs,
    });

    return {
      valid: isValid,
      proofSystem: proof.proofSystem,
    };
  }
}

// Privacy Budget Manager Implementation
export class PrivacyBudgetManager {
  constructor(
    private budgetStore: PrivacyBudgetStore,
    private budgetPolicy: PrivacyBudgetPolicy
  ) {}

  async checkBudget(userId: string, requestedEpsilon: number): Promise<BudgetCheck> {
    const currentBudget = await this.budgetStore.getBudget(userId);
    
    if (!currentBudget) {
      // Initialize budget for new user
      await this.budgetStore.initializeBudget(userId, this.budgetPolicy.defaultBudget);
      return {
        available: true,
        remaining: this.budgetPolicy.defaultBudget - requestedEpsilon,
      };
    }

    const remaining = currentBudget.remaining - requestedEpsilon;
    
    return {
      available: remaining >= 0,
      remaining: Math.max(0, remaining),
    };
  }

  async consumeBudget(userId: string, epsilon: number, metadata: BudgetConsumptionMetadata): Promise<void> {
    const currentBudget = await this.budgetStore.getBudget(userId);
    
    if (!currentBudget || currentBudget.remaining < epsilon) {
      throw new Error('Insufficient privacy budget');
    }

    await this.budgetStore.updateBudget(userId, {
      consumed: currentBudget.consumed + epsilon,
      remaining: currentBudget.remaining - epsilon,
      lastConsumed: Date.now(),
      metadata,
    });
  }

  async resetBudget(userId: string, period: BudgetPeriod): Promise<void> {
    const newBudget = this.budgetPolicy.getBudgetForPeriod(period);
    await this.budgetStore.updateBudget(userId, {
      consumed: 0,
      remaining: newBudget,
      lastReset: Date.now(),
      period,
    });
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No privacy-enhancing technologies
export class BasicDataService {
  // BAD: No privacy protection
  async processData(data: any) {
    // BAD: No differential privacy
    // BAD: No encryption
    // BAD: No anonymization
    return this.transform(data);
  }

  // BAD: No privacy budgeting
  // BAD: No secure computation
  // BAD: No zero-knowledge proofs
  // BAD: No compliance checking
}
```
</example_bad>
