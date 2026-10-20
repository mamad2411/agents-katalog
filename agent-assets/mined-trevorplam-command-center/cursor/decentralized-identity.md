---
description: Run Decentralized Identity and Verifiable Credentials Standards Check
globs: ["**/identity/**/*.ts", "**/did/**/*.ts", "**/verifiable-credentials/**/*.ts", "**/ssi/**/*.ts"]
---
# Security: Decentralized Identity & Verifiable Credentials Standards

<audit_rules>
- You MUST implement proper DID (Decentralized Identifier) resolution and validation.
- You MUST ensure verifiable credentials follow W3C VC standards with proper cryptographic signatures.
- You MUST implement proper credential presentation and verification workflows.
- You MUST configure proper DID methods support (did:ethr, did:web, did:key, etc.).
- You MUST ensure proper key management for DID controllers and credential issuers.
- You MUST implement proper credential revocation and status checking mechanisms.
- You MUST configure proper privacy-preserving credential sharing with selective disclosure.
- You MUST ensure proper credential schema validation and type checking.
- You MUST implement proper audit logging for all identity and credential operations.
- You MUST ensure proper compliance with GDPR and privacy regulations for identity data.
</audit_rules>

<example_good>
```typescript
// Decentralized Identity Implementation

export class DecentralizedIdentityManager {
  constructor(
    private didResolver: DIDResolver,
    private credentialIssuer: CredentialIssuer,
    private credentialVerifier: CredentialVerifier,
    private keyManager: DIDKeyManager,
    private vaultManager: VaultManager,
    private auditLogger: IdentityAuditLogger
  ) {}

  async createDID(method: DIDMethod, controller: string, options: DIDCreationOptions): Promise<DIDDocument> {
    // Validate DID method
    if (!this.isValidDIDMethod(method)) {
      throw new Error(`Unsupported DID method: ${method}`);
    }

    // Generate key pairs for DID
    const keyPairs = await this.keyManager.generateKeyPairs(options.keyTypes || ['Ed25519', 'secp256k1']);
    
    // Create DID document
    const didDocument = await this.createDIDDocument(method, controller, keyPairs, options);
    
    // Register DID on blockchain or network
    const registration = await this.registerDID(didDocument, method);
    
    // Store keys securely
    await this.keyManager.storeKeys(didDocument.id, keyPairs);
    
    // Log DID creation
    await this.auditLogger.logDIDCreation({
      did: didDocument.id,
      method,
      controller,
      keyTypes: Object.keys(keyPairs),
      timestamp: Date.now(),
    });

    return didDocument;
  }

  async issueCredential(credentialRequest: CredentialIssuanceRequest): Promise<VerifiableCredential> {
    // Validate issuer DID
    const issuerDID = await this.didResolver.resolve(credentialRequest.issuer);
    if (!issuerDID) {
      throw new Error(`Issuer DID not found: ${credentialRequest.issuer}`);
    }

    // Validate subject DID
    const subjectDID = await this.didResolver.resolve(credentialRequest.subject);
    if (!subjectDID) {
      throw new Error(`Subject DID not found: ${credentialRequest.subject}`);
    }

    // Validate credential schema
    const schemaValidation = await this.validateCredentialSchema(credentialRequest);
    if (!schemaValidation.valid) {
      throw new Error(`Credential schema validation failed: ${schemaValidation.errors.join(', ')}`);
    }

    // Create credential
    const credential = await this.createCredential(credentialRequest);
    
    // Sign credential
    const signedCredential = await this.signCredential(credential, credentialRequest.issuer);
    
    // Store credential hash for revocation
    await this.storeCredentialHash(signedCredential);
    
    // Log credential issuance
    await this.auditLogger.logCredentialIssuance({
      credentialId: signedCredential.id,
      issuer: credentialRequest.issuer,
      subject: credentialRequest.subject,
      type: credentialRequest.type,
      timestamp: Date.now(),
    });

    return signedCredential;
  }

  async verifyCredential(credential: VerifiableCredential, options: VerificationOptions): Promise<CredentialVerificationResult> {
    // Verify credential signature
    const signatureVerification = await this.verifyCredentialSignature(credential);
    if (!signatureVerification.valid) {
      return {
        valid: false,
        reason: `Signature verification failed: ${signatureVerification.reason}`,
        checks: { signature: false },
      };
    }

    // Verify issuer DID
    const issuerVerification = await this.verifyIssuer(credential.issuer);
    if (!issuerVerification.valid) {
      return {
        valid: false,
        reason: `Issuer verification failed: ${issuerVerification.reason}`,
        checks: { signature: true, issuer: false },
      };
    }

    // Check credential status/revocation
    const statusVerification = await this.verifyCredentialStatus(credential);
    if (!statusVerification.valid) {
      return {
        valid: false,
        reason: `Credential status verification failed: ${statusVerification.reason}`,
        checks: { signature: true, issuer: true, status: false },
      };
    }

    // Verify credential schema
    const schemaVerification = await this.validateCredentialSchema(credential);
    if (!schemaVerification.valid) {
      return {
        valid: false,
        reason: `Schema validation failed: ${schemaVerification.errors.join(', ')}`,
        checks: { signature: true, issuer: true, status: true, schema: false },
      };
    }

    // Verify expiration and issuance dates
    const dateVerification = await this.verifyCredentialDates(credential);
    if (!dateVerification.valid) {
      return {
        valid: false,
        reason: `Date verification failed: ${dateVerification.reason}`,
        checks: { signature: true, issuer: true, status: true, schema: true, dates: false },
      };
    }

    // Verify subject if provided
    let subjectVerification = { valid: true };
    if (options.subject) {
      subjectVerification = await this.verifySubject(credential, options.subject);
    }

    const allChecks = {
      signature: signatureVerification.valid,
      issuer: issuerVerification.valid,
      status: statusVerification.valid,
      schema: schemaVerification.valid,
      dates: dateVerification.valid,
      subject: subjectVerification.valid,
    };

    return {
      valid: Object.values(allChecks).every(check => check),
      checks: allChecks,
      issuer: issuerVerification.issuerDID,
      subject: credential.credentialSubject,
      type: credential.type,
      issuanceDate: credential.issuanceDate,
      expirationDate: credential.expirationDate,
    };
  }

  async createPresentation(presentationRequest: PresentationRequest): Promise<VerifiablePresentation> {
    // Verify holder DID
    const holderDID = await this.didResolver.resolve(presentationRequest.holder);
    if (!holderDID) {
      throw new Error(`Holder DID not found: ${presentationRequest.holder}`);
    }

    // Select credentials for presentation
    const selectedCredentials = await this.selectCredentials(
      presentationRequest.credentials,
      presentationRequest.inputDescriptors
    );

    // Apply selective disclosure if requested
    const disclosedCredentials = await this.applySelectiveDisclosure(
      selectedCredentials,
      presentationRequest.selectiveDisclosure
    );

    // Create presentation
    const presentation = await this.createPresentation({
      holder: presentationRequest.holder,
      credentials: disclosedCredentials,
      domain: presentationRequest.domain,
      challenge: presentationRequest.challenge,
    });

    // Sign presentation
    const signedPresentation = await this.signPresentation(presentation, presentationRequest.holder);

    // Log presentation creation
    await this.auditLogger.logPresentationCreation({
      presentationId: signedPresentation.id,
      holder: presentationRequest.holder,
      verifier: presentationRequest.verifier,
      credentialCount: disclosedCredentials.length,
      timestamp: Date.now(),
    });

    return signedPresentation;
  }

  async verifyPresentation(presentation: VerifiablePresentation, options: PresentationVerificationOptions): Promise<PresentationVerificationResult> {
    // Verify presentation signature
    const signatureVerification = await this.verifyPresentationSignature(presentation);
    if (!signatureVerification.valid) {
      return {
        valid: false,
        reason: `Presentation signature verification failed: ${signatureVerification.reason}`,
        checks: { signature: false },
      };
    }

    // Verify holder DID
    const holderVerification = await this.verifyHolder(presentation.holder);
    if (!holderVerification.valid) {
      return {
        valid: false,
        reason: `Holder verification failed: ${holderVerification.reason}`,
        checks: { signature: true, holder: false },
      };
    }

    // Verify all credentials in presentation
    const credentialVerifications = [];
    for (const credential of presentation.verifiableCredential) {
      const verification = await this.verifyCredential(credential, options);
      credentialVerifications.push(verification);
    }

    const allCredentialsValid = credentialVerifications.every(v => v.valid);
    
    // Verify presentation freshness
    const freshnessVerification = await this.verifyPresentationFreshness(presentation, options);
    
    const allChecks = {
      signature: signatureVerification.valid,
      holder: holderVerification.valid,
      credentials: allCredentialsValid,
      freshness: freshnessVerification.valid,
    };

    return {
      valid: Object.values(allChecks).every(check => check),
      checks: allChecks,
      holder: presentation.holder,
      verifier: presentation.verifier,
      credentials: credentialVerifications,
      domain: presentation.domain,
      challenge: presentation.challenge,
    };
  }

  async revokeCredential(credentialId: string, reason: string, revoker: string): Promise<RevocationResult> {
    // Verify revoker authority
    const authorityVerification = await this.verifyRevocationAuthority(credentialId, revoker);
    if (!authorityVerification.authorized) {
      throw new Error(`Not authorized to revoke credential: ${credentialId}`);
    }

    // Create revocation entry
    const revocationEntry = await this.createRevocationEntry(credentialId, reason, revoker);
    
    // Publish revocation
    const publication = await this.publishRevocation(revocationEntry);
    
    // Update credential status
    await this.updateCredentialStatus(credentialId, 'revoked', revocationEntry.id);
    
    // Log revocation
    await this.auditLogger.logCredentialRevocation({
      credentialId,
      reason,
      revoker,
      revocationEntryId: revocationEntry.id,
      timestamp: Date.now(),
    });

    return {
      credentialId,
      revoked: true,
      revocationEntryId: revocationEntry.id,
      reason,
      timestamp: Date.now(),
    };
  }

  private async createDIDDocument(method: DIDMethod, controller: string, keyPairs: KeyPairs, options: DIDCreationOptions): Promise<DIDDocument> {
    const did = this.generateDID(method, options);
    
    const verificationMethods = [];
    for (const [keyId, keyPair] of Object.entries(keyPairs)) {
      verificationMethods.push({
        id: `${did}#${keyId}`,
        type: this.getVerificationMethodType(keyPair.type),
        controller: controller,
        publicKeyJwk: keyPair.publicKeyJwk,
      });
    }

    const authentication = verificationMethods.map(vm => vm.id);
    const assertionMethod = verificationMethods.map(vm => vm.id);
    const capabilityInvocation = verificationMethods.map(vm => vm.id);
    const capabilityDelegation = verificationMethods.map(vm => vm.id);

    return {
      '@context': ['https://www.w3.org/ns/did/v1'],
      id: did,
      controller: controller,
      verificationMethod: verificationMethods,
      authentication,
      assertionMethod,
      capabilityInvocation,
      capabilityDelegation,
      service: options.services || [],
      created: new Date().toISOString(),
      updated: new Date().toISOString(),
    };
  }

  private async createCredential(request: CredentialIssuanceRequest): Promise<Credential> {
    return {
      '@context': [
        'https://www.w3.org/2018/credentials/v1',
        ...request.context || [],
      ],
      id: `urn:uuid:${generateUUID()}`,
      type: ['VerifiableCredential', ...request.type],
      issuer: request.issuer,
      issuanceDate: new Date().toISOString(),
      expirationDate: request.expirationDate,
      credentialSubject: request.credentialSubject,
      credentialSchema: request.credentialSchema,
      evidence: request.evidence,
      refreshService: request.refreshService,
      termsOfUse: request.termsOfUse,
    };
  }

  private async signCredential(credential: Credential, issuerDID: string): Promise<VerifiableCredential> {
    // Get issuer's signing key
    const signingKey = await this.keyManager.getSigningKey(issuerDID);
    if (!signingKey) {
      throw new Error(`No signing key found for DID: ${issuerDID}`);
    }

    // Create credential without proof
    const credentialCopy = { ...credential };
    
    // Create proof
    const proof = await this.createProof({
      type: 'Ed25519Signature2018',
      creator: `${issuerDID}#${signingKey.keyId}`,
      proofPurpose: 'assertionMethod',
      verificationMethod: `${issuerDID}#${signingKey.keyId}`,
      challenge: generateNonce(),
      domain: undefined,
    }, credentialCopy, signingKey);

    return {
      ...credentialCopy,
      proof,
    };
  }

  private async createPresentation(config: PresentationConfig): Promise<Presentation> {
    return {
      '@context': ['https://www.w3.org/2018/credentials/v1'],
      type: ['VerifiablePresentation'],
      holder: config.holder,
      verifiableCredential: config.credentials,
      id: `urn:uuid:${generateUUID()}`,
      domain: config.domain,
      challenge: config.challenge,
    };
  }

  private async signPresentation(presentation: Presentation, holderDID: string): Promise<VerifiablePresentation> {
    // Get holder's signing key
    const signingKey = await this.keyManager.getSigningKey(holderDID);
    if (!signingKey) {
      throw new Error(`No signing key found for DID: ${holderDID}`);
    }

    // Create presentation without proof
    const presentationCopy = { ...presentation };
    
    // Create proof
    const proof = await this.createProof({
      type: 'Ed25519Signature2018',
      creator: `${holderDID}#${signingKey.keyId}`,
      proofPurpose: 'authentication',
      verificationMethod: `${holderDID}#${signingKey.keyId}`,
      challenge: presentation.challenge,
      domain: presentation.domain,
    }, presentationCopy, signingKey);

    return {
      ...presentationCopy,
      proof,
    };
  }

  private async applySelectiveDisclosure(
    credentials: VerifiableCredential[],
    selectiveDisclosure: SelectiveDisclosureConfig
  ): Promise<VerifiableCredential[]> {
    if (!selectiveDisclosure.enabled) {
      return credentials;
    }

    const disclosedCredentials = [];

    for (const credential of credentials) {
      const disclosedCredential = await this.createDisclosedCredential(
        credential,
        selectiveDisclosure.disclosedFields
      );
      disclosedCredentials.push(disclosedCredential);
    }

    return disclosedCredentials;
  }

  private async createDisclosedCredential(
    originalCredential: VerifiableCredential,
    disclosedFields: string[]
  ): Promise<VerifiableCredential> {
    // Create derived credential with only disclosed fields
    const derivedSubject = {};
    
    for (const field of disclosedFields) {
      if (originalCredential.credentialSubject[field]) {
        derivedSubject[field] = originalCredential.credentialSubject[field];
      }
    }

    return {
      ...originalCredential,
      id: `urn:uuid:${generateUUID()}`,
      credentialSubject: derivedSubject,
      derivedFrom: originalCredential.id,
    };
  }

  private async verifyCredentialSignature(credential: VerifiableCredential): Promise<SignatureVerification> {
    if (!credential.proof) {
      return { valid: false, reason: 'No proof found' };
    }

    try {
      const proof = credential.proof;
      const verificationMethod = proof.verificationMethod;
      
      // Resolve verification method
      const did = verificationMethod.split('#')[0];
      const didDocument = await this.didResolver.resolve(did);
      
      if (!didDocument) {
        return { valid: false, reason: 'DID not found' };
      }

      // Find verification method
      const vm = didDocument.verificationMethod.find(vm => vm.id === verificationMethod);
      if (!vm) {
        return { valid: false, reason: 'Verification method not found' };
      }

      // Verify signature
      const isValid = await this.verifySignature(proof, credential, vm.publicKeyJwk);
      
      return {
        valid: isValid,
        reason: isValid ? 'Signature valid' : 'Signature invalid',
        verificationMethod,
      };
    } catch (error) {
      return { valid: false, reason: `Signature verification error: ${error.message}` };
    }
  }

  private async verifyCredentialStatus(credential: VerifiableCredential): Promise<StatusVerification> {
    // Check credential status list
    if (credential.credentialStatus) {
      const statusList = await this.checkStatusList(credential.credentialStatus);
      if (statusList.revoked) {
        return { valid: false, reason: 'Credential revoked' };
      }
    }

    // Check revocation registry
    const revocationCheck = await this.checkRevocationRegistry(credential.id);
    if (revocationCheck.revoked) {
      return { valid: false, reason: 'Credential revoked' };
    }

    return { valid: true };
  }

  private async validateCredentialSchema(credential: VerifiableCredential | CredentialIssuanceRequest): Promise<SchemaValidation> {
    if (!credential.credentialSchema) {
      return { valid: true }; // Schema is optional
    }

    try {
      // Load schema
      const schema = await this.loadSchema(credential.credentialSchema.id);
      
      // Validate credential against schema
      const validation = await this.validateAgainstSchema(credential, schema);
      
      return validation;
    } catch (error) {
      return { valid: false, errors: [`Schema validation error: ${error.message}`] };
    }
  }

  private async verifyCredentialDates(credential: VerifiableCredential): Promise<DateVerification> {
    const now = new Date();
    
    // Check issuance date
    if (credential.issuanceDate) {
      const issuanceDate = new Date(credential.issuanceDate);
      if (issuanceDate > now) {
        return { valid: false, reason: 'Credential issued in future' };
      }
    }

    // Check expiration date
    if (credential.expirationDate) {
      const expirationDate = new Date(credential.expirationDate);
      if (expirationDate < now) {
        return { valid: false, reason: 'Credential expired' };
      }
    }

    return { valid: true };
  }

  private generateDID(method: DIDMethod, options: DIDCreationOptions): string {
    switch (method) {
      case 'did:ethr':
        return `did:ethr:${options.network || 'mainnet'}:${options.address}`;
      case 'did:web':
        return `did:web:${options.domain}:${options.path}`;
      case 'did:key':
        return `did:key:${options.publicKeyMultibase}`;
      default:
        throw new Error(`Unsupported DID method: ${method}`);
    }
  }

  private isValidDIDMethod(method: string): boolean {
    const supportedMethods = ['did:ethr', 'did:web', 'did:key', 'did:ion', 'did:sol'];
    return supportedMethods.includes(method);
  }

  private getVerificationMethodType(keyType: string): string {
    const typeMap = {
      'Ed25519': 'Ed25519VerificationKey2018',
      'secp256k1': 'EcdsaSecp256k1VerificationKey2019',
      'RSA': 'RsaVerificationKey2018',
    };
    
    return typeMap[keyType] || 'Ed25519VerificationKey2018';
  }
}

// DID Resolver Implementation
export class DIDResolver {
  constructor(
    private resolvers: Map<string, DIDMethodResolver>,
    private cache: DIDCache
  ) {}

  async resolve(did: string): Promise<DIDDocument | null> {
    // Check cache first
    const cached = await this.cache.get(did);
    if (cached && !this.isExpired(cached)) {
      return cached.document;
    }

    // Extract DID method
    const method = this.extractDIDMethod(did);
    const resolver = this.resolvers.get(method);
    
    if (!resolver) {
      throw new Error(`Unsupported DID method: ${method}`);
    }

    // Resolve DID
    const document = await resolver.resolve(did);
    
    // Cache result
    await this.cache.set(did, {
      document,
      cachedAt: Date.now(),
      expiresAt: Date.now() + 3600000, // 1 hour
    });

    return document;
  }

  private extractDIDMethod(did: string): string {
    const match = did.match(/^did:(\w+):/);
    return match ? match[1] : '';
  }

  private isExpired(cached: CachedDIDDocument): boolean {
    return Date.now() > cached.expiresAt;
  }
}

// Credential Verifier Implementation
export class CredentialVerifier {
  constructor(
    private didResolver: DIDResolver,
    private schemaValidator: SchemaValidator,
    private statusChecker: StatusChecker
  ) {}

  async verify(credential: VerifiableCredential, options: VerificationOptions): Promise<CredentialVerificationResult> {
    const checks = {};

    // Signature verification
    const signatureCheck = await this.verifySignature(credential);
    checks.signature = signatureCheck.valid;

    // Issuer verification
    const issuerCheck = await this.verifyIssuer(credential.issuer);
    checks.issuer = issuerCheck.valid;

    // Status verification
    const statusCheck = await this.statusChecker.check(credential);
    checks.status = statusCheck.valid;

    // Schema verification
    const schemaCheck = await this.schemaValidator.validate(credential);
    checks.schema = schemaCheck.valid;

    // Date verification
    const dateCheck = this.verifyDates(credential);
    checks.dates = dateCheck.valid;

    const allValid = Object.values(checks).every(check => check);

    return {
      valid: allValid,
      checks,
      issuer: credential.issuer,
      subject: credential.credentialSubject,
      type: credential.type,
      issuanceDate: credential.issuanceDate,
      expirationDate: credential.expirationDate,
    };
  }

  private async verifySignature(credential: VerifiableCredential): Promise<{ valid: boolean; reason?: string }> {
    // Implementation similar to DecentralizedIdentityManager.verifyCredentialSignature
    return { valid: true };
  }

  private async verifyIssuer(issuer: string): Promise<{ valid: boolean; issuerDID?: string; reason?: string }> {
    try {
      const didDocument = await this.didResolver.resolve(issuer);
      return { valid: true, issuerDID: issuer };
    } catch (error) {
      return { valid: false, reason: `Issuer resolution failed: ${error.message}` };
    }
  }

  private verifyDates(credential: VerifiableCredential): { valid: boolean; reason?: string } {
    const now = new Date();
    
    if (credential.expirationDate && new Date(credential.expirationDate) < now) {
      return { valid: false, reason: 'Credential expired' };
    }

    return { valid: true };
  }
}
```
</example_good>

<example_bad>
```typescript
// BAD: No decentralized identity standards
export class BasicIdentityService {
  // BAD: Traditional centralized identity
  async createUser(userData: any) {
    // BAD: No DID support
    // BAD: No verifiable credentials
    // BAD: No cryptographic signatures
    return this.database.users.create(userData);
  }

  // BAD: No credential verification
  // BAD: No selective disclosure
  // BAD: No revocation mechanisms
  // BAD: No privacy controls
}
```
</example_bad>
