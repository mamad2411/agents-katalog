---
name: "haip-protocol-profile"
description: "Use when implementing HAIP protocol requirements. Covers: OpenID4VP profile (request/response modes, client_id, session transcript), OpenID4VCI profile (credential offer, authorization, credential endpoint), and credential-format-specific profiles (ISO mdocs, SD-JWT VC)."
sections:
  - "5. OpenID for Verifiable Presentations"
  - "5.1. OpenID for Verifiable Presentations via Redirects"
  - "5.2. OpenID for Verifiable Presentations via W3C Digital Credentials API"
  - "5.3. Requirements specific to Credential Formats"
  - "6. OpenID4VC Credential Format Profiles"
  - "6.1. IETF SD-JWT VC Profile"
---

<!-- ARF version: 1.0-2025-03-04 -->
<!-- Tokens: ~4353 -->

## 5. OpenID for Verifiable Presentations
The following requirements apply to OpenID for Verifiable Presentations, irrespective of the flow and Credential Format:

- The Wallet and Verifier MUST support at least one of the following Credential Format Profiles defined in [Section 6](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#vc-profiles): IETF SD-JWT VC or ISO mdoc. Ecosystems SHOULD clearly indicate which of these formats, IETF SD-JWT VC, ISO mdoc, or both, are required to be supported.

        - The Response type MUST be `vp_token`.

        - For signed requests, the Verifier MUST use, and the Wallet MUST accept the Client Identifier Prefix `x509_hash` as defined in Section 5.9.3 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)]. The X.509 certificate of the trust anchor MUST NOT be included in the `x5c` JOSE header of the signed request. The X.509 certificate signing the request MUST NOT be self-signed. X.509 certificate profiles to be used with `x509_hash` are out of scope of this specification.

        - The DCQL query and response MUST be used as defined in Section 6 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)].

        - Response encryption MUST be performed as specified in [Section 8.3](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)]. The JWE `alg` (algorithm) header parameter (see [Section 4.1.1](https://rfc-editor.org/rfc/rfc7516) of [[RFC7516](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7516)])
value `ECDH-ES` (as defined in [Section 4.6](https://rfc-editor.org/rfc/rfc7518) of [[RFC7518](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7518)]), with key agreement utilizing keys on the `P-256` curve (see [Section 6.2.1.1](https://rfc-editor.org/rfc/rfc7518) of [[RFC7518](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7518)]) MUST be supported.
The JWE `enc` (encryption algorithm) header parameter (see [Section 4.1.2](https://rfc-editor.org/rfc/rfc7516) of [[RFC7516](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7516)]) values `A128GCM` and `A256GCM` (as defined in [Section 5.3](https://rfc-editor.org/rfc/rfc7518) of [[RFC7518](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7518)]) MUST be supported by Verifiers. Wallets MUST support `A128GCM` or `A256GCM`, or both. If both are supported, the Wallet SHOULD use `A256GCM` for the JWE `enc`. Verifiers MUST list both `A128GCM` and `A256GCM` in `encrypted_response_enc_values_supported` in their client metadata.

        - Verifiers MUST supply ephemeral encryption public keys specific to each Authorization Request passed via client metadata as specified in Section 8.3 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)].

        - The Authority Key Identifier (`aki`)-based Trusted Authority Query (`trusted_authorities`) for DCQL, as defined in section 6.1.1.1 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)], MUST be supported. Note that the Authority Key Identifiers mechanism can be used to support multiple X.509-based trust mechanisms, such as ISO mDL VICAL (as introduced in [[ISO.18013-5](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#ISO.18013-5)]) or ETSI Trusted Lists [[ETSI.TL](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#ETSI.TL)]. This is achieved by collecting the relevant X.509 certificates for the trusted Issuers and including the encoded Key Identifiers from the certificates in the `aki` array .

      
Additional requirements for OpenID4VP are defined in [Section 5.1](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#oid4vp-redirects), [Section 5.2](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#oid4vp-dc-api), [Section 5.3](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#oid4vp-credential-formats), [Section 7](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#crypto-suites) and [Section 8](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#hash-algorithms).
Note that while this specification does not define profiles for X.509 certificates used in Verifier authentication (e.g., with the `x509_hash` Client Identifier Prefix), Ecosystems are encouraged to select suitable certificate issuing policies and certificate profiles (for example, an mDL Ecosystem can use the Reader Authentication Certificate profile defined in Annex B of ISO/IEC 18013-5 with `x509_hash`), or define new ones if there is a good reason to do so. Such policies and profiles MAY specify how information in the certificate corresponds to information in the presentation flows. For example, an Ecosystem might require that the Wallet verifies that the `redirect_uri`, `response_uri`, `origin`, or `expected_origin` request parameters match with information contained in the Verifier's end-entity certificate (e.g., its DNS name).


### 5.1. OpenID for Verifiable Presentations via Redirects
The following requirements apply to OpenID for Verifiable Presentations via redirects:

- As a way to invoke the Wallet, the custom URL scheme `haip-vp://` MAY be supported by the Wallet and the Verifier. Implementations MAY support other ways to invoke the Wallets as agreed upon by trust frameworks/Ecosystems/jurisdictions, including but not limited to using other custom URL schemes or claimed "https" scheme URIs.

          - Signed Authorization Requests MUST be used by utilizing JWT-Secured Authorization Request (JAR) [[RFC9101](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC9101)] with the `request_uri` parameter.

          - Response encryption MUST be used by utilizing response mode `direct_post.jwt`, as defined in Section 8.3 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)]. Security considerations in Section 14.3 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)] MUST be applied.

          - 
            Verifiers and Wallets MUST support the "same-device" flow. Verifiers are RECOMMENDED to use only the "same-device" flow unless the Verifier does not rely on session binding for phishing resistance, e.g. in a proximity scenario. If "same-device" flow is used, then:

- Verifiers MUST include `redirect_uri` in the HTTP response to the Wallet's HTTP POST to the `response_uri`, as defined in Section 8.2 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)].

              - Wallets MUST follow the redirect to `redirect_uri`.

              - Verifiers MUST reject presentations if Wallets do not follow the redirect back or the redirect back arrives in a different user session to the one the request was initiated in.

              - Implementation considerations can be found in Section 13.3 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)] and security considerations in Section 14.2 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)].

            

        


### 5.2. OpenID for Verifiable Presentations via W3C Digital Credentials API
The following requirements apply to OpenID for Verifiable Presentations via the W3C Digital Credentials API:

- The Wallet MUST support Wallet Invocation via the W3C Digital Credentials API or an equivalent platform API. The Verifier MUST use Wallet Invocation via the W3C Digital Credentials API or an equivalent platform API.

          - The Wallet MUST support the Response Mode `dc_api.jwt`. The Verifier MUST use the Response Mode `dc_api.jwt`.

          - The Verifier and Wallet MUST use Appendix A in [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)] that defines how to use OpenID4VP over the W3C Digital Credentials API.

          - The Wallet MUST support unsigned, signed, and multi-signed requests as defined in Appendices A.3.1 and A.3.2 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)]. The Verifier MUST support at least one of these options.

        
Note that unsigned requests depend on the origin information provided by the platform and the web PKI for request integrity protection and to authenticate the Verifier. Signed requests introduce a separate layer for request integrity protection and Verifier authentication that can be validated by the Wallet.


### 5.3. Requirements specific to Credential Formats


#### 5.3.1. ISO Mobile Documents or mdocs (ISO/IEC 18013 and ISO/IEC 23220 series)
The following requirements apply to all OpenID4VP flows when the mdoc Credential Format is used (as defined in Appendix B.2. of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)]):

- The Credential Format identifier MUST be `mso_mdoc`.

            - When multiple ISO mdocs are being returned, each ISO mdoc MUST be returned in a separate `DeviceResponse` (as defined in 8.3.2.1.2.2 of [[ISO.18013-5](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#ISO.18013-5)]), each matching to a respective DCQL query. Therefore, the resulting `vp_token` contains multiple `DeviceResponse` instances.

            - The Credential Issuer MAY include the MSO revocation mechanism in the issued mdoc. When doing so, it MUST use one of the mechanisms defined in ISO/IEC 18013-5 ([[ISO.18013-5.second.edition](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#ISO.18013-5.second.edition)]).

          


#### 5.3.2. IETF SD-JWT VC
The following requirements apply to all OpenID4VP flows when the SD-JWT VC Credential Format is used:

- The Credential Format identifier MUST be `dc+sd-jwt`.

---

## 6. OpenID4VC Credential Format Profiles
Credential Format Profiles are defined as follows:

- 
          IETF SD-JWT VCs (as specified in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)]), subject to the additional requirements defined in [Section 6.1](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#sd-jwt-vc):

- 
              [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] - Appendix A.3

            - 
              [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)] - Appendix B.3

          

        - 
          ISO mdocs:

- 
              [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] - Appendix A.2

            - 
              [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)] - Appendix B.2

          

      


### 6.1. IETF SD-JWT VC Profile
This specification defines the following additional requirements for IETF SD-JWT VCs as defined in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)].

- Compact serialization MUST be supported as defined in [[RFC9901](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC9901)]. JSON serialization MAY be supported.

          - It is RECOMMENDED that Issuers limit the validity period when issuing SD-JWT VC. When doing so, the Issuer MUST use an `exp` claim, a `status` claim, or both.

          - The `cnf` claim [[RFC7800](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7800)] MUST conform to the definition given in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)]. Implementations conforming to this specification MUST include the JSON Web Key [[RFC7517](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#RFC7517)] in the `jwk` member if the corresponding Credential Configuration requires cryptographic holder binding.

          - The `status` claim, if present, MUST contain `status_list` as defined in [[I-D.ietf-oauth-status-list](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-status-list)]

          - The public key used to validate the signature on the Status List Token defined in [I-D.ietf-oauth-status-list] MUST be included in the `x5c` JOSE header of the Token. The X.509 certificate of the trust anchor MUST NOT be included in the `x5c` JOSE header of the Status List Token. The X.509 certificate signing the request MUST NOT be self-signed.

        
Each Credential MUST have its own unique, unpredictable status list index, even when multiple Credentials reference the same status list URI (see section 13.2 of [[I-D.ietf-oauth-status-list](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-status-list)]). Refer to section 12.5 of [[I-D.ietf-oauth-status-list](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-status-list)] for additional privacy considerations on unlinkability.
Note: For guidance on preventing linkability by colluding parties, such as Issuer/Verifier pairs, multiple Verifiers, or repeated interactions with the same Verifier, see Section 15.4.1 of [[OIDF.OID4VCI](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VCI)] and Section 15.5 of [[OIDF.OID4VP](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.OID4VP)].
Note: If there is a requirement to communicate information about the verification status and identity assurance data of the claims about the subject, the syntax defined by [[OIDF.ekyc-ida](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#OIDF.ekyc-ida)] SHOULD be used. It is up to each jurisdiction and Ecosystem, whether to require it to the implementers of this specification.
Note: If there is a requirement to provide the Subject’s identifier assigned and maintained by the Issuer, the `sub` claim MAY be used. There is no requirement for a binding to exist between the `sub` and `cnf` claims. See the Implementation Considerations section in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)].
Note: In some Credential Types, it is not desirable to include an expiration date (e.g., diploma attestation). Therefore, this specification leaves its inclusion to the Issuer, or the body defining the respective Credential Type.


#### 6.1.1. Issuer identification and key resolution to validate an issued Credential
This specification mandates the support for X.509 certificate-based key resolution to validate the issuer signature of an SD-JWT VC. This MUST be supported by all entities (Issuer, Wallet, Verifier). The SD-JWT VC MUST contain the credential issuer's signing certificate along with a trust chain in the `x5c` JOSE header parameter as described in section 3.5 of [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)]. The X.509 certificate of the trust anchor MUST NOT be included in the `x5c` JOSE header of the SD-JWT VC. The X.509 certificate signing the request MUST NOT be self-signed.


##### 6.1.1.1. Cryptographic Holder Binding between VC and VP

- If the credential has cryptographic holder binding, a KB-JWT, as defined in [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid4vc-high-assurance-interoperability-profile-1_0.html#I-D.ietf-oauth-sd-jwt-vc)], MUST always be present when presenting an SD-JWT VC.
