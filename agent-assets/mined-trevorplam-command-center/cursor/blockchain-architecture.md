---
description: Run Blockchain Architecture and Modular Systems Standards Check
globs: ["**/blockchain/**/*.ts", "**/layer2/**/*.ts", "**/rollups/**/*.ts", "**/zk/**/*.ts"]
---
# Architecture: Blockchain Architecture & Modular Systems Standards

<audit_rules>
- You MUST implement proper modular blockchain architecture separating consensus, execution, and data availability layers.
- You MUST configure appropriate rollup strategies (optimistic vs ZK) based on use case requirements.
- You MUST implement proper cross-chain communication using secure bridges and relays.
- You MUST ensure proper data availability verification for off-chain data storage.
- You MUST implement proper validator selection and staking mechanisms.
- You MUST configure proper gas fee optimization and transaction batching.
- You MUST implement proper state management and pruning strategies.
- You MUST ensure proper network synchronization and peer discovery.
- You MUST implement proper cryptographic security for consensus mechanisms.
- You MUST configure proper monitoring and alerting for blockchain infrastructure.
</audit_rules>

<example_good>
```typescript
// Modular Blockchain Architecture Implementation

// Data Availability Layer
export class DataAvailabilityLayer {
  constructor(
    private celestiaClient: CelestiaClient,
    private eigenLayer: EigenLayerClient
  ) {}

  async submitData(data: BlockData): Promise<DASubmission> {
    // Submit to Celestia for data availability
    const celestiaSubmission = await this.celestiaClient.submitBlob({
      namespace: this.generateNamespace(),
      data: this.encodeData(data),
    });

    // Submit to EigenLayer for additional security
    const eigenSubmission = await this.eigenLayer.submitData({
      dataHash: celestiaSubmission.hash,
      quorumNumbers: [0, 1, 2], // Multiple quorums for security
    });

    return {
      celestia: celestiaSubmission,
      eigenLayer: eigenSubmission,
    };
  }

  async verifyAvailability(submissionId: string): Promise<boolean> {
    const [celestiaAvailable, eigenAvailable] = await Promise.all([
      this.celestiaClient.verifyAvailability(submissionId),
      this.eigenLayer.verifyAvailability(submissionId),
    ]);

    return celestiaAvailable && eigenAvailable;
  }

  private generateNamespace(): string {
    return generateNamespaceId('my-app', 'v1');
  }

  private encodeData(data: BlockData): Buffer {
    return Buffer.from(JSON.stringify(data));
  }
}

// ZK-Rollup Execution Layer
export class ZKRollupExecutor {
  constructor(
    private starknetClient: StarknetClient,
    private provingService: ProvingService
  ) {}

  async executeTransaction(tx: Transaction): Promise<TxReceipt> {
    // Execute transaction locally
    const result = await this.executeLocally(tx);
    
    // Generate ZK proof
    const proof = await this.provingService.generateProof({
      transaction: tx,
      result: result,
      previousState: await this.getCurrentState(),
    });

    // Submit to Starknet
    const receipt = await this.starknetClient.submitTransaction({
      proof: proof,
      calldata: this.encodeCalldata(tx),
    });

    return receipt;
  }

  async verifyProof(proof: ZKProof): Promise<boolean> {
    return await this.provingService.verifyProof(proof);
  }

  private async executeLocally(tx: Transaction): Promise<ExecutionResult> {
    // Local transaction execution logic
    return {
      success: true,
      gasUsed: tx.gasLimit,
      logs: [],
      returnValue: tx.data,
    };
  }
}

// Cross-Chain Bridge
export class SecureBridge {
  constructor(
    private layerZero: LayerZeroClient,
    private hyperlane: HyperlaneClient
  ) {}

  async bridgeToken(
    token: Token,
    amount: bigint,
    fromChain: ChainId,
    toChain: ChainId
  ): Promise<BridgeReceipt> {
    // Lock tokens on source chain
    const lockReceipt = await this.lockTokens(token, amount, fromChain);
    
    // Send cross-chain message
    const message = {
      token: token.address,
      amount: amount,
      recipient: await this.getRecipientAddress(toChain),
      nonce: lockReceipt.nonce,
    };

    // Use LayerZero for bridging
    const lzReceipt = await this.layerZero.send({
      dstChainId: toChain,
      payload: this.encodeMessage(message),
      refundAddress: await this.getRefundAddress(),
    });

    return {
      lockReceipt,
      bridgeReceipt: lzReceipt,
    };
  }

  async verifyBridgeMessage(message: BridgeMessage): Promise<boolean> {
    // Verify message authenticity
    const isValid = await this.hyperlane.verifyMessage(message);
    
    if (isValid) {
      // Mint tokens on destination chain
      await this.mintTokens(message.token, message.amount, message.recipient);
    }

    return isValid;
  }

  private async lockTokens(token: Token, amount: bigint, chain: ChainId): Promise<LockReceipt> {
    // Token locking logic
    return { nonce: generateNonce(), timestamp: Date.now() };
  }
}

// Validator Management
export class ValidatorManager {
  constructor(
    private stakingContract: StakingContract,
    private slashingContract: SlashingContract
  ) {}

  async registerValidator(validator: Validator): Promise<void> {
    // Check minimum stake requirement
    const minStake = await this.stakingContract.getMinimumStake();
    require(validator.stake >= minStake, "Insufficient stake");

    // Register validator
    await this.stakingContract.registerValidator({
      address: validator.address,
      stake: validator.stake,
      commission: validator.commission,
    });
  }

  async proposeBlock(validator: Validator, block: Block): Promise<BlockReceipt> {
    // Verify validator is active
    const isActive = await this.stakingContract.isActive(validator.address);
    require(isActive, "Validator not active");

    // Submit block proposal
    const receipt = await this.stakingContract.proposeBlock({
      validator: validator.address,
      blockHash: block.hash,
      transactions: block.transactions,
    });

    return receipt;
  }

  async slashValidator(validatorAddress: string, reason: SlashReason): Promise<void> {
    await this.slashingContract.slash({
      validator: validatorAddress,
      reason: reason,
      amount: await this.calculateSlashAmount(validatorAddress),
    });
  }

  private async calculateSlashAmount(validatorAddress: string): Promise<bigint> {
    const stake = await this.stakingContract.getStake(validatorAddress);
    return stake / 10n; // Slash 10% of stake
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: Monolithic blockchain architecture
export class MonolithicBlockchain {
  // BAD: Everything in one contract
  async processTransaction(tx: any) {
    // BAD: No separation of concerns
    this.validateTransaction(tx);
    this.executeTransaction(tx);
    this.updateState(tx);
    this.broadcastTransaction(tx);
    this.verifyConsensus(tx);
  }

  // BAD: No modular architecture
  async validateTransaction(tx: any) {
    // BAD: No data availability verification
    // BAD: No ZK proof verification
    // BAD: No cross-chain communication
  }

  // BAD: No proper validator management
  async addValidator(validator: any) {
    // BAD: No staking requirements
    // BAD: No slashing mechanism
    // BAD: No commission tracking
  }
}
```
</example_bad>
