---
name: "oid4vci-security"
description: "Use when reviewing security or privacy considerations for OpenID4VCI. Covers: credential replay prevention, TLS requirements, proof of possession security, nonce management, and privacy considerations for credential issuance."
sections:
  - "14. Implementation Considerations"
  - "14.1. Claims-based Holder Binding of the Credential to the End-User possessing the Credential"
  - "14.2. Binding of the Credential without Cryptographic Key Binding or Claims-based Holder Binding"
  - "14.3. Multiple Accesses to the Credential Endpoint"
  - "14.4. Relationship between the Credential Issuer Identifier in the Metadata and the Issuer Identifier in the Issued Credential"
  - "14.5. Refreshing Issued Credentials"
  - "14.6. Batch Issuing Credentials"
  - "14.7. Pre-Final Specifications"
  - "15. Privacy Considerations"
  - "15.1. User Consent"
  - "15.2. Minimum Disclosure"
  - "15.3. Storage of the Credentials"
  - "15.4. Correlation"
  - "15.5. Identifying the Credential Issuer"
  - "15.6. Identifying the Wallet"
  - "15.7. Untrusted Wallets"
---

<!-- ARF version: 1.0-2025-02-03 -->
<!-- Tokens: ~3276 -->

## 14. Implementation Considerations


### 14.1. Claims-based Holder Binding of the Credential to the End-User possessing the Credential
Credentials not cryptographically bound to the identifier of the End-User possessing it (see [Section 8.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-binding)), should be bound to the End-User possessing the Credential, based on the claims included in the Credential.
In Claims-based Holder Binding, no Cryptographic Key Binding material is provided. Instead, the issued Credential includes End-User claims that can be used by the Verifier to verify possession of the Credential by requesting presentation of existing forms of physical or digital identification that includes the same claims (e.g., a driving license or other ID cards in person, or an online ID verification service).


### 14.2. Binding of the Credential without Cryptographic Key Binding or Claims-based Holder Binding
Some Credential Issuers might choose to issue bearer Credentials without either Cryptographic Key Binding or Claims-based Holder Binding because they are meant to be presented without proof of possession.
One such use case is low assurance Credentials, such as coupons or tickets.
Another use case is when the Credential Issuer uses cryptographic schemes that can provide binding to the End-User possessing that Credential without explicit cryptographic material being supplied by the application used by that End-User. For example, in the case of the BBS Signature Scheme, the issued Credential itself is a secret and only a derivation from the Credential is presented to the Verifier. Effectively, the Credential is bound to the Credential Issuer's signature on the Credential, which becomes a shared secret transferred from the Credential Issuer to the End-User.


### 14.3. Multiple Accesses to the Credential Endpoint
The Credential Endpoint can be accessed multiple times by a Wallet using the same Access Token, even for the same Credential. The Credential Issuer determines if the subsequent successful requests will return the same or an updated Credential, such as having a new expiration time or using the most current End-User claims.
The Credential Issuer MAY also decide to no longer accept the Access Token and a re-authentication or Token Refresh (see [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)], Section 6) MAY be required at the Credential Issuer's discretion. The policies between the Credential Endpoint and the Authorization Server that MAY change the behavior of what is returned with a new Access Token are beyond the scope of this specification (see Section 7 of [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)]).
The Credential Issuer SHOULD NOT revoke previously issued, valid Credentials solely as a result of a subsequent successful Credential Request. This, for example, ensures that the Wallet can keep a desired number of Credentials without causing additional revocation and issuance overhead.
The action leading to the Wallet performing another Credential Request can also be triggered by a background process, or by the Credential Issuer using an out-of-band mechanism (SMS, email, etc.) to inform the End-User.


### 14.4. Relationship between the Credential Issuer Identifier in the Metadata and the Issuer Identifier in the Issued Credential
The Credential Issuer Identifier is always a URL using the `https` scheme, as defined in [Section 12.2.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-identifier). Depending on the Credential Format, the Issuer Identifier in the issued Credential may not be a URL using the `https` scheme. Some other forms that it can take are a DID included in the `issuer` property in a [[VC_DATA](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#VC_DATA)] format, or the `Subject` value of the document signer certificate included in the `x5chain` element in an [[ISO.18013-5](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#ISO.18013-5)] format.
When the Issuer Identifier in the issued Credential is a DID, a non-exhaustive list of mechanisms the Credential Issuer MAY use to bind to the Credential Issuer Identifier is as follows:

- Use the [[DIF.Well-Known_DID](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#DIF.Well-Known_DID)] Specification to provide binding between a DID and a certain domain.

          - If the Issuer Identifier in the issued Credential is an object, add to the object a `credential_issuer` claim, as defined in [Section 12.2.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-issuer-identifier).

        
The Wallet MAY check the binding between the Credential Issuer Identifier and the Issuer Identifier in the issued Credential.


### 14.5. Refreshing Issued Credentials
After a Verifiable Credential has been issued to the Holder, claim values about the subject of a Credential or a signature on the Credential may need to be updated. There are two possible mechanisms to do so.
First, the Wallet may receive an updated version of a Credential from a Credential Endpoint using a valid Access Token. This does not involve interaction with the End-User. If the Credential Issuer issued a Refresh Token to the Wallet, the Wallet would obtain a fresh Access Token by making a request to the Token Endpoint, as defined in Section 6 of [[RFC6749](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC6749)].
Second, the Credential Issuer can reissue the Credential by starting the issuance process from the beginning. This would involve interaction with the End-User. A Credential needs to be reissued if the Wallet does not have a valid Access Token or a valid Refresh Token. With this approach, when a new Credential is issued, the Wallet might need to check if it already has a Credential of the same type and, if necessary, delete the old Credential. Otherwise, the Wallet might end up with more than one Credential of the same type, without knowing which one is the latest.
Credential Refresh can be initiated by the Wallet independently from the Credential Issuer, or the Credential Issuer can send a signal to the Wallet asking it to request Credential refresh. How the Credential Issuer sends such a signal is out of scope of this specification.
It is up to the Credential Issuer whether to update both the signature and the claim values, or only the signature.


### 14.6. Batch Issuing Credentials
The Credential Issuer determines the number of the Credentials issued in the Credential Response, regardless of number of proofs/keys contained in the `proofs` parameter in the Credential Request.


### 14.7. Pre-Final Specifications
Implementers should be aware that this specification uses several specifications that are not yet final specifications. Those specifications are:

- OpenID Federation 1.0 draft -43 [[OpenID.Federation](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#OpenID.Federation)]

          - SD-JWT-based Verifiable Credentials (SD-JWT VC) draft -11 [[I-D.ietf-oauth-sd-jwt-vc](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-sd-jwt-vc)]

          - Attestation-Based Client Authentication draft -07 [[I-D.ietf-oauth-attestation-based-client-auth](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-attestation-based-client-auth)]

          - Token Status List draft -12 [[I-D.ietf-oauth-status-list](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#I-D.ietf-oauth-status-list)]

        
While breaking changes to the specifications referenced in this specification are not expected, should they occur, OpenID4VCI implementations should continue to use the specifically referenced versions above in preference to the final versions, unless updated by a profile or new version of this specification.

---

## 15. Privacy Considerations
When [[RFC9396](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9396)] is used, the Privacy Considerations of that specification also apply.
The privacy principles of [[ISO.29100](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#ISO.29100)] should be adhered to.


### 15.1. User Consent
The Credential Issuer SHOULD obtain the End-User's consent before issuing Credential(s)
to the Wallet. It SHOULD be made clear to the End-User what information is being included in the
Credential(s) and for what purpose.


### 15.2. Minimum Disclosure
To ensure minimum disclosure and prevent Verifiers from obtaining claims unnecessary for the
transaction at hand, when issuing Credentials that are intended to be created once and then used a
number of times by the End-User, the Credential Issuers and the Wallets SHOULD implement
Credential Formats that support selective disclosure, or consider issuing a separate Credential
for each user claim.


### 15.3. Storage of the Credentials
To prevent a leak of End-User data, especially when it is signed, which risks revealing private data of End-Users to
third parties, systems implementing this specification SHOULD be designed to minimize the amount
of End-User data that is stored. All involved parties SHOULD store Verifiable Credentials
containing privacy-sensitive data only for as long as needed, including in log files. Any logging of
End-User data should be carefully considered as to whether it is necessary at all. The time logs are retained
for should be minimized.
After Issuance, Credential Issuers SHOULD NOT store the Issuer-signed Credentials if they
contain privacy-sensitive data. Wallets SHOULD store Credentials only in encrypted form, and,
wherever possible, use hardware-backed encryption. Wallets SHOULD not store
Credentials longer than needed.


### 15.4. Correlation


#### 15.4.1. Unique Values Encoded in the Credential
Issuance/presentation or two presentation sessions by the same End-User can be linked on the basis of
unique values encoded in the Credential (End-User claims, identifiers, Issuer signature, etc.) either by colluding Issuer/Verifier or Verifier/Verifier pairs, or by the same Verifier.
To prevent these types of correlation, Credential Issuers and Wallets SHOULD use
methods, including but not limited to the following ones:

- Issue a batch of Credentials with the same Credential Dataset to facilitate the use of a unique Credential per presentation or per Verifier. This approach solely aids in achieving Verifier-to-Verifier unlinkability.

            - Use cryptographic schemes that can provide non-correlation.

          
Claims containing time-related information, such as issuance or expiration dates, SHOULD be either individually randomized within an appropriate time window (e.g., within the last 24 hours), or rounded (e.g., to the start of the day), to avoid unintended correlation factors.
Credential Issuers specifically SHOULD discard values that can be used in collusion with a Verifier to track a user, such as the Issuer's signature or cryptographic key material to which an issued credential was bound to.


#### 15.4.2. Credential Offer
The Privacy Considerations in Section 11.2 of [[RFC9101](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#RFC9101)] apply to the `credential_offer` and
`credential_offer_uri` parameters defined in [Section 4.1](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#credential-offer).


#### 15.4.3. Authorization Request
The Wallet SHOULD NOT include potentially sensitive information in the Authorization Request,
for example, by including clear-text session information as a `state` parameter value or encoding
it in a `redirect_uri` parameter. A third party may observe such information through browser
history, etc. and correlate the user's activity using it.


#### 15.4.4. Wallet Attestation Subject
The Wallet Attestation as defined in [Appendix E](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#walletattestation) SHOULD NOT introduce a unique identifier specific to a single client.
The subject claim for the Wallet Attestation SHOULD be a value that is shared by all Wallet instances using this type of
wallet implementation. The value should be understood as an identifier of the Wallet type, rather than the specific Wallet
instance itself.


### 15.5. Identifying the Credential Issuer
Information in the credential identifying a particular Credential Issuer, such as a Credential Issuer Identifier,
issuer's certificate, or issuer's public key may reveal information about the End-User.
For example, when a military organization or a drug rehabilitation center issues a vaccine
credential, verifiers can deduce that the owner of the Wallet storing such a Credential is a
military member or may have a substance use disorder.
In addition, when a Credential Issuer issues only one type of Credential, it might have privacy implications,
because if the Wallet has a Credential issued by that Issuer, its type and claim names can be
determined.
For example, if the National Cancer Institute only issued Credentials with cancer registry
information, it is possible to deduce that the owner of the Wallet storing such a Credential is a
cancer patient.
To mitigate these issues, a group of organizations may elect to use a common Credential Issuer,
such that any credentials issued by this Issuer cannot be attributed to a particular organization
through identifiers of the Credential Issuers alone. A group signature scheme may also be used
instead of an individual signature.
When a common Credential Issuer is used, appropriate guardrails need to be in place to prevent
one organization from issuing illegitimate credentials on behalf of other organizations.


### 15.6. Identifying the Wallet
There is a potential for leaking information about the Wallet to third parties when the
Wallet reacts to a Credential Offer. An attacker may send Credential Offers using different
custom URL schemes or claimed https urls, see if the
Wallet reacts (e.g., whether the wallet retrieves Credential Issuer metadata hosted by an
attacker's server), and, therefore, learn which Wallet is installed. To avoid this, the Wallet SHOULD
require user interaction or establish trust in the Issuer before fetching any `credential_offer_uri`
or acting on the received Credential Offer.


### 15.7. Untrusted Wallets
The Wallet transmits and stores sensitive information about the End-User. To ensure that the
Wallet can handle those appropriately (i.e., according to a certain trust framework or a
regulation), the Credential Issuer should properly authenticate the Wallet and ensure it is a trusted entity. For more details, see [Section 13.3](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html#trust-between-wallet-and-issuer).
