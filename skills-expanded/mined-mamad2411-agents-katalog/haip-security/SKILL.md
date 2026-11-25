---
name: "haip-security"
description: "Use when reviewing HAIP security or privacy requirements. Covers: key management, token binding, attestation-based client authentication, and privacy considerations for high-assurance credential flows."
sections:
  - "7. Requirements for Digital Signatures"
  - "8. Hash Algorithms"
---

<!-- ARF version: 1.0-2025-03-04 -->
<!-- Tokens: ~479 -->

## 7. Requirements for Digital Signatures
Issuers, Verifiers, and Wallets MUST, at a minimum, support ECDSA with P-256 and SHA-256 (JOSE algorithm identifier `ES256`; COSE algorithm identifier `-7` or `-9`, as applicable) for the purpose of validating the following:

- 
          Issuers

- Wallet Attestations (including PoP) when Appendix E of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] is used.

            - Key Attestations when Appendix D of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] is used.

            - 
              `jwt` proof type as specified in Appendix E of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)].

          

        - 
          Verifiers

- the signature of the Verifiable Presentation, e.g., KB-JWT of an SD-JWT VC, or `deviceSignature` CBOR structure in case of ISO mdocs. Verifiers are assumed to determine in advance the cryptographic suites supported by the Ecosystem, e.g. mDL Issuers/Verifiers implementing ISO mdocs.

            - the status information of the Verifiable Credential or Wallet Attestation.

          

        - 
          Wallets

- signed presentation requests.

            - signed Issuer metadata.

          

      
Ecosystem-specific profiles of this specification MAY mandate additional cryptographic suites.
When using this specification alongside other crypto suites, each entity SHOULD make it explicit in its metadata which other algorithms and key types are supported for the cryptographic operations.

---

## 8. Hash Algorithms
The hash algorithm SHA-256 MUST be supported by all the entities to generate and validate the digests in the IETF SD-JWT VC and ISO mdoc.
Ecosystem-specific profiles of this specification MAY mandate additional hashing algorithms.
When using this specification alongside other hash algorithms, each entity SHOULD make it explicit in its metadata which other algorithms are supported.
