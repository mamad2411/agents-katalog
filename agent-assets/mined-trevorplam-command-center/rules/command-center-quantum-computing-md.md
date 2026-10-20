---
description: Run Quantum Computing and Post-Quantum Cryptography Standards Check
globs:
  [
    '**/quantum/**/*.ts',
    '**/post-quantum/**/*.ts',
    '**/quantum-algorithms/**/*.ts',
    '**/quantum-security/**/*.ts',
  ]
---

# Future-Proof: Quantum Computing & Post-Quantum Cryptography Standards

<audit_rules>

- You MUST implement proper post-quantum cryptographic algorithms for quantum-resistant security.
- You MUST ensure proper quantum algorithm selection with complexity analysis and optimization.
- You MUST implement proper quantum circuit design with error correction and fault tolerance.
- You MUST configure proper quantum hardware integration with cloud quantum services.
- You MUST ensure proper quantum-classical hybrid algorithms for practical applications.
- You MUST implement proper quantum key distribution (QKD) for secure communication.
- You MUST configure proper quantum simulation and testing environments.
- You MUST ensure proper quantum error mitigation and noise reduction techniques.
- You MUST implement proper quantum resource management and qubit optimization.
- You MUST ensure proper quantum security threat modeling and migration planning.
  </audit_rules>

<example_good>

```typescript
// Quantum Computing Implementation

export class QuantumComputingOrchestrator {
  constructor(
    private quantumHardware: QuantumHardwareInterface,
    private postQuantumCrypto: PostQuantumCryptography,
    private quantumAlgorithms: QuantumAlgorithmLibrary,
    private quantumSimulator: QuantumSimulator,
    private quantumQKD: QuantumKeyDistribution,
    private errorCorrection: QuantumErrorCorrection,
    private hybridProcessor: HybridQuantumClassicalProcessor
  ) {}

  async deployPostQuantumSecurity(
    config: PostQuantumSecurityConfig
  ): Promise<PostQuantumDeployment> {
    // Validate security requirements
    const validation = await this.validatePostQuantumRequirements(config)
    if (!validation.valid) {
      throw new Error(`Invalid post-quantum security config: ${validation.errors.join(', ')}`)
    }

    // Select appropriate post-quantum algorithms
    const algorithmSelection = await this.selectPostQuantumAlgorithms(config)

    // Generate post-quantum key pairs
    const keyPairs = await this.postQuantumCrypto.generateKeyPairs(algorithmSelection)

    // Deploy post-quantum cryptographic services
    const cryptoServices = await this.deployCryptoServices(keyPairs, config)

    // Setup quantum key distribution if available
    let qkdSetup = null
    if (config.enableQKD) {
      qkdSetup = await this.quantumQKD.setupQKD(config.qkdConfig)
    }

    // Configure migration strategy
    const migrationStrategy = await this.createMigrationStrategy(config, algorithmSelection)

    return {
      deploymentId: generateId(),
      algorithmSelection,
      keyPairs,
      cryptoServices,
      qkdSetup,
      migrationStrategy,
      deployedAt: Date.now(),
    }
  }

  async executeQuantumAlgorithm(
    algorithm: QuantumAlgorithmRequest
  ): Promise<QuantumAlgorithmResult> {
    // Validate algorithm request
    const validation = await this.validateAlgorithmRequest(algorithm)
    if (!validation.valid) {
      throw new Error(`Invalid quantum algorithm request: ${validation.errors.join(', ')}`)
    }

    // Select quantum hardware or simulator
    const executionTarget = await this.selectExecutionTarget(algorithm)

    // Optimize quantum circuit
    const optimizedCircuit = await this.optimizeQuantumCircuit(algorithm.circuit, executionTarget)

    // Apply error correction if needed
    const errorCorrectedCircuit = await this.errorCorrection.applyErrorCorrection(
      optimizedCircuit,
      executionTarget.errorRates
    )

    // Execute quantum algorithm
    const execution = await this.executeQuantumCircuit(errorCorrectedCircuit, executionTarget)

    // Process results
    const processedResults = await this.processQuantumResults(execution.results, algorithm)

    return {
      algorithmId: algorithm.id,
      executionId: execution.id,
      target: executionTarget.type,
      results: processedResults,
      executionTime: execution.duration,
      qubitsUsed: execution.qubitsUsed,
      fidelity: execution.fidelity,
      errorRates: execution.errorRates,
      timestamp: Date.now(),
    }
  }

  async runHybridAlgorithm(hybridRequest: HybridAlgorithmRequest): Promise<HybridAlgorithmResult> {
    // Validate hybrid algorithm request
    const validation = await this.validateHybridRequest(hybridRequest)
    if (!validation.valid) {
      throw new Error(`Invalid hybrid algorithm request: ${validation.errors.join(', ')}`)
    }

    // Decompose hybrid algorithm into quantum and classical parts
    const decomposition = await this.hybridProcessor.decompose(hybridRequest.algorithm)

    // Execute quantum part
    const quantumResults = await this.executeQuantumPart(decomposition.quantumPart, hybridRequest)

    // Execute classical part with quantum results as input
    const classicalResults = await this.executeClassicalPart(
      decomposition.classicalPart,
      quantumResults,
      hybridRequest
    )

    // Combine results
    const combinedResults = await this.hybridProcessor.combineResults(
      quantumResults,
      classicalResults,
      decomposition.combinationStrategy
    )

    return {
      algorithmId: hybridRequest.id,
      quantumResults,
      classicalResults,
      combinedResults,
      executionTime: quantumResults.executionTime + classicalResults.executionTime,
      timestamp: Date.now(),
    }
  }

  async establishQuantumKeyDistribution(qkdRequest: QKDRequest): Promise<QKDResult> {
    // Validate QKD request
    const validation = await this.validateQKDRequest(qkdRequest)
    if (!validation.valid) {
      throw new Error(`Invalid QKD request: ${validation.errors.join(', ')}`)
    }

    // Setup quantum channel
    const quantumChannel = await this.quantumQKD.setupQuantumChannel(qkdRequest.parties)

    // Generate quantum keys
    const keyGeneration = await this.quantumQKD.generateKeys(quantumChannel, {
      keyLength: qkdRequest.keyLength || 256,
      algorithm: qkdRequest.algorithm || 'BB84',
      errorThreshold: qkdRequest.errorThreshold || 0.05,
    })

    // Perform error estimation and correction
    const errorCorrection = await this.quantumQKD.performErrorCorrection(
      keyGeneration.rawKeys,
      keyGeneration.errorEstimate
    )

    // Perform privacy amplification
    const privacyAmplification = await this.quantumQKD.performPrivacyAmplification(
      errorCorrection.correctedKeys,
      keyGeneration.leakageEstimate
    )

    return {
      sessionId: qkdRequest.sessionId,
      parties: qkdRequest.parties,
      finalKeys: privacyAmplification.finalKeys,
      keyLength: privacyAmplification.finalKeys[0].length,
      securityParameters: {
        algorithm: qkdRequest.algorithm,
        errorRate: keyGeneration.errorEstimate,
        informationLeakage: keyGeneration.leakageEstimate,
      },
      establishedAt: Date.now(),
    }
  }

  async simulateQuantumSystem(
    simulation: QuantumSimulationRequest
  ): Promise<QuantumSimulationResult> {
    // Validate simulation request
    const validation = await this.validateSimulationRequest(simulation)
    if (!validation.valid) {
      throw new Error(`Invalid simulation request: ${validation.errors.join(', ')}`)
    }

    // Configure quantum simulator
    const simulatorConfig = await this.quantumSimulator.configure({
      qubits: simulation.qubitCount,
      noiseModel: simulation.noiseModel,
      simulationMethod: simulation.method || 'state_vector',
      precision: simulation.precision || 'double',
    })

    // Initialize quantum state
    const initialState = await this.quantumSimulator.initializeState(simulation.initialState)

    // Apply quantum circuit
    const evolvedState = await this.quantumSimulator.applyCircuit(initialState, simulation.circuit)

    // Measure results
    const measurementResults = await this.quantumSimulator.measure(
      evolvedState,
      simulation.measurements
    )

    // Analyze results
    const analysis = await this.analyzeSimulationResults(measurementResults, simulation)

    return {
      simulationId: simulation.id,
      qubitCount: simulation.qubitCount,
      circuitDepth: this.calculateCircuitDepth(simulation.circuit),
      results: measurementResults,
      analysis,
      simulationTime: measurementResults.executionTime,
      fidelity: measurementResults.fidelity,
      timestamp: Date.now(),
    }
  }

  async assessQuantumThreats(assessment: QuantumThreatAssessment): Promise<QuantumThreatReport> {
    // Analyze current cryptographic infrastructure
    const cryptoAnalysis = await this.analyzeCurrentCrypto(assessment.currentInfrastructure)

    // Assess quantum computing timeline
    const timelineAnalysis = await this.assessQuantumTimeline(assessment.scenario)

    // Identify vulnerable systems
    const vulnerableSystems = await this.identifyVulnerableSystems(cryptoAnalysis, timelineAnalysis)

    // Calculate risk scores
    const riskScores = await this.calculateRiskScores(vulnerableSystems, timelineAnalysis)

    // Generate migration recommendations
    const migrationPlan = await this.generateMigrationPlan(vulnerableSystems, riskScores)

    return {
      assessmentId: assessment.id,
      scenario: assessment.scenario,
      cryptoAnalysis,
      timelineAnalysis,
      vulnerableSystems,
      riskScores,
      migrationPlan,
      urgency: this.calculateUrgency(riskScores, timelineAnalysis),
      timestamp: Date.now(),
    }
  }

  private async selectPostQuantumAlgorithms(
    config: PostQuantumSecurityConfig
  ): Promise<PostQuantumAlgorithmSelection> {
    const selection = {
      keyExchange: null,
      signatures: null,
      encryption: null,
    }

    // Select key exchange algorithm
    if (config.requirements.keyExchange) {
      selection.keyExchange = await this.selectKeyExchangeAlgorithm(config.requirements.keyExchange)
    }

    // Select signature algorithm
    if (config.requirements.signatures) {
      selection.signatures = await this.selectSignatureAlgorithm(config.requirements.signatures)
    }

    // Select encryption algorithm
    if (config.requirements.encryption) {
      selection.encryption = await this.selectEncryptionAlgorithm(config.requirements.encryption)
    }

    return selection
  }

  private async selectKeyExchangeAlgorithm(
    requirements: KeyExchangeRequirements
  ): Promise<PostQuantumAlgorithm> {
    const candidates = [
      { name: 'Kyber', type: 'lattice-based', security: 256, performance: 'high' },
      { name: 'NTRU', type: 'lattice-based', security: 256, performance: 'medium' },
      { name: 'SIKE', type: 'isogeny-based', security: 256, performance: 'low' },
    ]

    // Select based on requirements
    const suitable = candidates.filter(
      (c) =>
        c.security >= requirements.securityLevel &&
        this.performanceMeetsRequirements(c.performance, requirements.performance)
    )

    return suitable[0] || candidates[0]
  }

  private async selectSignatureAlgorithm(
    requirements: SignatureRequirements
  ): Promise<PostQuantumAlgorithm> {
    const candidates = [
      { name: 'Dilithium', type: 'lattice-based', security: 256, size: 'medium' },
      { name: 'Falcon', type: 'lattice-based', security: 256, size: 'small' },
      { name: 'SPHINCS+', type: 'hash-based', security: 256, size: 'large' },
    ]

    const suitable = candidates.filter(
      (c) =>
        c.security >= requirements.securityLevel &&
        this.sizeMeetsRequirements(c.size, requirements.signatureSize)
    )

    return suitable[0] || candidates[0]
  }

  private async optimizeQuantumCircuit(
    circuit: QuantumCircuit,
    target: ExecutionTarget
  ): Promise<OptimizedQuantumCircuit> {
    // Apply circuit optimization techniques
    let optimizedCircuit = circuit

    // Gate fusion
    optimizedCircuit = await this.fuseGates(optimizedCircuit, target.gateSet)

    // Qubit mapping
    optimizedCircuit = await this.mapQubits(optimizedCircuit, target.topology)

    // Error mitigation
    optimizedCircuit = await this.applyErrorMitigation(optimizedCircuit, target.errorModel)

    return optimizedCircuit
  }

  private async executeQuantumCircuit(
    circuit: QuantumCircuit,
    target: ExecutionTarget
  ): Promise<QuantumExecution> {
    if (target.type === 'hardware') {
      return await this.quantumHardware.execute(circuit, target.hardwareConfig)
    } else {
      return await this.quantumSimulator.execute(circuit, target.simulatorConfig)
    }
  }

  private async processQuantumResults(
    results: QuantumMeasurement,
    algorithm: QuantumAlgorithmRequest
  ): Promise<ProcessedQuantumResults> {
    // Apply measurement post-processing
    const processed = {
      measurements: results.measurements,
      probabilities: this.calculateProbabilities(results.measurements),
      expectationValues: this.calculateExpectationValues(
        results.measurements,
        algorithm.observables
      ),
      classicalOutput: this.extractClassicalOutput(results.measurements, algorithm.outputFormat),
    }

    return processed
  }

  private calculateProbabilities(measurements: QuantumMeasurement[]): number[] {
    // Calculate measurement probabilities
    const counts = measurements.reduce((acc, m) => {
      acc[m.outcome] = (acc[m.outcome] || 0) + 1
      return acc
    }, {})

    const total = measurements.length
    return Object.values(counts).map((count) => count / total)
  }

  private calculateExpectationValues(
    measurements: QuantumMeasurement[],
    observables: Observable[]
  ): number[] {
    return observables.map((obs) => {
      return (
        measurements.reduce((sum, m) => {
          const value = this.measureObservable(m.state, obs)
          return sum + value
        }, 0) / measurements.length
      )
    })
  }

  private measureObservable(state: QuantumState, observable: Observable): number {
    // Simple expectation value calculation
    return Math.random() // Placeholder
  }

  private extractClassicalOutput(measurements: QuantumMeasurement[], format: OutputFormat): any {
    switch (format) {
      case 'binary_string':
        return measurements.map((m) => m.outcome).join('')
      case 'integer':
        return parseInt(measurements.map((m) => m.outcome).join(''), 2)
      case 'probability_distribution':
        return this.calculateProbabilities(measurements)
      default:
        return measurements
    }
  }

  private performanceMeetsRequirements(
    performance: string,
    required: PerformanceRequirement
  ): boolean {
    const levels = { low: 1, medium: 2, high: 3 }
    return levels[performance] >= levels[required]
  }

  private sizeMeetsRequirements(size: string, required: SizeRequirement): boolean {
    const levels = { small: 1, medium: 2, large: 3 }
    return levels[size] <= levels[required]
  }

  private calculateUrgency(riskScores: RiskScore[], timeline: QuantumTimeline): UrgencyLevel {
    const maxRisk = Math.max(...riskScores.map((r) => r.score))
    const timeToQuantum = timeline.yearsToPracticalQuantum

    if (maxRisk > 0.8 && timeToQuantum < 5) return 'critical'
    if (maxRisk > 0.6 && timeToQuantum < 10) return 'high'
    if (maxRisk > 0.4 && timeToQuantum < 15) return 'medium'
    return 'low'
  }
}

// Post-Quantum Cryptography Implementation
export class PostQuantumCryptography {
  constructor(
    private keyGenerator: PostQuantumKeyGenerator,
    private cryptoEngine: PostQuantumCryptoEngine,
    private migrationTool: CryptoMigrationTool
  ) {}

  async generateKeyPairs(selection: PostQuantumAlgorithmSelection): Promise<PostQuantumKeyPairs> {
    const keyPairs = {}

    // Generate key exchange keys
    if (selection.keyExchange) {
      keyPairs.keyExchange = await this.keyGenerator.generateKeyPair(selection.keyExchange)
    }

    // Generate signature keys
    if (selection.signatures) {
      keyPairs.signatures = await this.keyGenerator.generateKeyPair(selection.signatures)
    }

    // Generate encryption keys
    if (selection.encryption) {
      keyPairs.encryption = await this.keyGenerator.generateKeyPair(selection.encryption)
    }

    return keyPairs
  }

  async encrypt(
    data: Buffer,
    keyPair: PostQuantumKeyPair,
    algorithm: PostQuantumAlgorithm
  ): Promise<EncryptedData> {
    // Validate key pair
    if (!keyPair.publicKey) {
      throw new Error('Public key required for encryption')
    }

    // Encrypt using post-quantum algorithm
    const encrypted = await this.cryptoEngine.encrypt(data, keyPair.publicKey, algorithm)

    return {
      ciphertext: encrypted.ciphertext,
      algorithm: algorithm.name,
      keyId: keyPair.id,
      metadata: encrypted.metadata,
    }
  }

  async decrypt(encryptedData: EncryptedData, keyPair: PostQuantumKeyPair): Promise<Buffer> {
    // Validate key pair
    if (!keyPair.privateKey) {
      throw new Error('Private key required for decryption')
    }

    // Decrypt using post-quantum algorithm
    const decrypted = await this.cryptoEngine.decrypt(
      encryptedData.ciphertext,
      keyPair.privateKey,
      encryptedData.algorithm
    )

    return decrypted.plaintext
  }

  async sign(
    message: Buffer,
    keyPair: PostQuantumKeyPair,
    algorithm: PostQuantumAlgorithm
  ): Promise<DigitalSignature> {
    // Validate key pair
    if (!keyPair.privateKey) {
      throw new Error('Private key required for signing')
    }

    // Sign using post-quantum algorithm
    const signature = await this.cryptoEngine.sign(message, keyPair.privateKey, algorithm)

    return {
      signature: signature.signature,
      algorithm: algorithm.name,
      keyId: keyPair.id,
      metadata: signature.metadata,
    }
  }

  async verify(
    message: Buffer,
    signature: DigitalSignature,
    publicKey: PostQuantumPublicKey
  ): Promise<boolean> {
    // Verify using post-quantum algorithm
    const verification = await this.cryptoEngine.verify(
      message,
      signature.signature,
      publicKey,
      signature.algorithm
    )

    return verification.valid
  }

  async migrateFromClassic(
    classicKeys: ClassicKeyPairs,
    targetAlgorithms: PostQuantumAlgorithmSelection
  ): Promise<MigrationResult> {
    const migrationResults = []

    // Migrate each key type
    for (const [keyType, classicKey] of Object.entries(classicKeys)) {
      const targetAlgorithm = targetAlgorithms[keyType]
      if (targetAlgorithm) {
        const result = await this.migrationTool.migrateKey(classicKey, targetAlgorithm)
        migrationResults.push(result)
      }
    }

    return {
      migrationId: generateId(),
      results: migrationResults,
      success: migrationResults.every((r) => r.success),
      migratedAt: Date.now(),
    }
  }
}

// Quantum Algorithm Library Implementation
export class QuantumAlgorithmLibrary {
  constructor(
    private algorithmRegistry: QuantumAlgorithmRegistry,
    private optimizer: QuantumOptimizer,
    private analyzer: QuantumAnalyzer
  ) {}

  async getAlgorithm(name: string, parameters: AlgorithmParameters): Promise<QuantumAlgorithm> {
    const algorithm = await this.algorithmRegistry.get(name)
    if (!algorithm) {
      throw new Error(`Algorithm not found: ${name}`)
    }

    // Configure algorithm with parameters
    const configured = await this.configureAlgorithm(algorithm, parameters)

    return configured
  }

  async createCustomAlgorithm(specification: AlgorithmSpecification): Promise<QuantumAlgorithm> {
    // Validate specification
    const validation = await this.validateSpecification(specification)
    if (!validation.valid) {
      throw new Error(`Invalid algorithm specification: ${validation.errors.join(', ')}`)
    }

    // Create quantum circuit
    const circuit = await this.buildCircuit(specification)

    // Optimize circuit
    const optimized = await this.optimizer.optimize(circuit)

    return {
      id: generateId(),
      name: specification.name,
      circuit: optimized,
      specification,
      complexity: this.analyzeComplexity(optimized),
    }
  }

  async analyzeAlgorithm(algorithm: QuantumAlgorithm): Promise<AlgorithmAnalysis> {
    // Calculate complexity
    const complexity = await this.analyzer.calculateComplexity(algorithm.circuit)

    // Estimate resource requirements
    const resources = await this.analyzer.estimateResources(algorithm.circuit)

    // Analyze error sensitivity
    const errorSensitivity = await this.analyzer.analyzeErrorSensitivity(algorithm.circuit)

    return {
      algorithmId: algorithm.id,
      complexity,
      resources,
      errorSensitivity,
      recommendations: this.generateOptimizationRecommendations(
        complexity,
        resources,
        errorSensitivity
      ),
    }
  }

  private async configureAlgorithm(
    algorithm: QuantumAlgorithm,
    parameters: AlgorithmParameters
  ): Promise<QuantumAlgorithm> {
    // Apply parameter configuration
    const configured = { ...algorithm }

    // Adjust circuit based on parameters
    if (parameters.qubitCount) {
      configured.circuit = await this.adjustQubitCount(algorithm.circuit, parameters.qubitCount)
    }

    if (parameters.depth) {
      configured.circuit = await this.adjustCircuitDepth(algorithm.circuit, parameters.depth)
    }

    return configured
  }

  private analyzeComplexity(circuit: QuantumCircuit): ComplexityAnalysis {
    return {
      timeComplexity: this.calculateTimeComplexity(circuit),
      spaceComplexity: this.calculateSpaceComplexity(circuit),
      gateComplexity: this.calculateGateComplexity(circuit),
    }
  }

  private calculateTimeComplexity(circuit: QuantumCircuit): string {
    const depth = this.calculateCircuitDepth(circuit)
    return `O(${depth})`
  }

  private calculateSpaceComplexity(circuit: QuantumCircuit): string {
    const qubits = circuit.qubits
    return `O(${qubits})`
  }

  private calculateGateComplexity(circuit: QuantumCircuit): number {
    return circuit.gates.length
  }

  private calculateCircuitDepth(circuit: QuantumCircuit): number {
    // Simple depth calculation - in production use proper circuit analysis
    return circuit.gates.length
  }
}

// Quantum Key Distribution Implementation
export class QuantumKeyDistribution {
  constructor(
    private quantumChannel: QuantumChannel,
    private classicalChannel: ClassicalChannel,
    private errorCorrection: QKDErrorCorrection,
    privacyAmplification: QKDPrivacyAmplification
  ) {}

  async setupQuantumChannel(parties: QKDParty[]): Promise<QuantumChannelSetup> {
    // Validate parties
    if (parties.length < 2) {
      throw new Error('At least 2 parties required for QKD')
    }

    // Establish quantum channel
    const channel = await this.quantumChannel.establish({
      parties,
      protocol: 'BB84',
      securityLevel: 256,
    })

    // Setup classical channel for sifting and error correction
    const classical = await this.classicalChannel.establish(parties)

    return {
      channelId: channel.id,
      parties,
      protocol: 'BB84',
      quantumChannel: channel,
      classicalChannel: classical,
      establishedAt: Date.now(),
    }
  }

  async generateKeys(
    channel: QuantumChannelSetup,
    config: KeyGenerationConfig
  ): Promise<KeyGenerationResult> {
    // Quantum transmission phase
    const quantumTransmission = await this.performQuantumTransmission(channel, config)

    // Sifting phase
    const sifting = await this.performSifting(quantumTransmission, channel)

    // Error estimation
    const errorEstimation = await this.estimateErrorRate(sifting)

    // Error correction
    const errorCorrection = await this.errorCorrection.correct(
      sifting.keys,
      errorEstimation.errorRate
    )

    // Privacy amplification
    const privacyAmplification = await this.privacyAmplification.amplify(
      errorCorrection.correctedKeys,
      errorEstimation.informationLeakage
    )

    return {
      rawKeys: quantumTransmission.rawKeys,
      sifting,
      errorEstimation,
      errorCorrection,
      privacyAmplification,
      finalKeys: privacyAmplification.finalKeys,
      keyLength: privacyAmplification.finalKeys[0].length,
    }
  }

  private async performQuantumTransmission(
    channel: QuantumChannelSetup,
    config: KeyGenerationConfig
  ): Promise<QuantumTransmission> {
    // Generate random quantum states
    const states = await this.generateQuantumStates(config.keyLength)

    // Transmit quantum states
    const transmission = await this.quantumChannel.transmit(channel.quantumChannel, states)

    // Measure received states
    const measurements = await this.measureStates(transmission.receivedStates)

    return {
      transmittedStates: states,
      receivedStates: transmission.receivedStates,
      measurements,
      rawKeys: this.extractRawKeys(measurements),
    }
  }

  private async generateQuantumStates(keyLength: number): Promise<QuantumState[]> {
    const states = []

    for (let i = 0; i < keyLength; i++) {
      // Random basis selection (0: Z, 1: X)
      const basis = Math.random() < 0.5 ? 0 : 1

      // Random bit value
      const bit = Math.random() < 0.5 ? 0 : 1

      // Create quantum state
      const state = this.createQuantumState(bit, basis)
      states.push(state)
    }

    return states
  }

  private createQuantumState(bit: number, basis: number): QuantumState {
    // Create quantum state based on bit and basis
    if (basis === 0) {
      // Z basis
      return {
        state: bit === 0 ? '|0⟩' : '|1⟩',
        basis: 'Z',
        bit,
      }
    } else {
      // X basis
      return {
        state: bit === 0 ? '|+⟩' : '|-⟩',
        basis: 'X',
        bit,
      }
    }
  }

  private async measureStates(states: QuantumState[]): Promise<QuantumMeasurement[]> {
    return states.map((state) => ({
      state,
      measurement: Math.random() < 0.5 ? 0 : 1, // Random measurement
      basis: Math.random() < 0.5 ? 'Z' : 'X', // Random basis
    }))
  }

  private extractRawKeys(measurements: QuantumMeasurement[]): RawKey[] {
    return measurements.map((m) => ({
      bit: m.measurement,
      basis: m.basis,
      state: m.state,
    }))
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No quantum computing preparation
export class BasicCryptoService {
  // BAD: No post-quantum cryptography
  async encrypt(data: any, key: any) {
    // BAD: No quantum threat assessment
    // BAD: No quantum algorithms
    // BAD: No QKD implementation
    return this.classicalEncrypt(data, key)
  }

  // BAD: No quantum simulation
  // BAD: No hybrid algorithms
  // BAD: No quantum security migration
}
```

</example_bad>
