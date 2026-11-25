---
name: "sd-jwt-security"
description: "Use when reviewing SD-JWT security considerations. Covers: threat model, hash collision, claim name collisions, key binding enforcement, and privacy considerations for selective disclosure."
sections:
  - "9. Security Considerations"
  - "9.1. Mandatory Signing of the Issuer-Signed JWT"
  - "9.2. Manipulation of Disclosures"
  - "9.3. Entropy of the Salt"
  - "9.4. Choice of a Hash Algorithm"
  - "9.5. Key Binding"
  - "9.6. Concealing Claim Names"
  - "9.7. Selectively Disclosable Validity Claims"
  - "9.8. Distribution and Rotation of Issuer Signature Verification Key"
  - "9.9. Forwarding Credentials"
  - "9.10. Integrity of SD-JWTs and SD-JWT+KBs"
  - "9.11. Explicit Typing"
  - "9.12. Key Pair Generation and Lifecycle Management"
  - "10. Privacy Considerations"
  - "10.1. Unlinkability"
  - "10.2. Storage of User Data"
  - "10.3. Confidentiality During Transport"
  - "10.4. Decoy Digests"
  - "10.5. Issuer Identifier"
  - "11. IANA Considerations"
  - "11.1. JSON Web Token Claims Registration"
  - "11.2. Media Type Registrations"
  - "11.3. Structured Syntax Suffixes Registration"
---

<!-- ARF version: RFC-9901 -->
<!-- Tokens: ~7571 -->

## 9. Security Considerations
The security considerations help achieve the following properties:

        Selective Disclosure:
        An adversary in the role
  of the Verifier cannot obtain information from an SD-JWT about any claim
  name or claim value that was not explicitly disclosed by the Holder unless
  that information can be derived from other disclosed claims or sources other
  than the presented SD-JWT.

        
Integrity:
        
          A malicious Holder cannot modify
  names or values of selectively disclosable claims without detection by the
  Verifier.

      

Additionally, as described in [Section 9.5](https://www.rfc-editor.org/rfc/rfc9901.html#key_binding_security), the application of Key Binding can ensure that the presenter of an SD-JWT credential is the Holder of the credential.


### 9.1. Mandatory Signing of the Issuer-Signed JWT
The JWT MUST be signed by the Issuer to protect the integrity of the issued
claims. An attacker can modify or add claims if this JWT is not signed (e.g.,
change the "email" attribute to take over the victim's account or add an
attribute indicating a fake academic qualification).
The Verifier MUST always check the signature of the Issuer-signed JWT to ensure that it
has not been tampered with since its issuance. The Issuer-signed JWT MUST be rejected if the signature cannot be verified.
The security of the Issuer-signed JWT depends on the security of the signature algorithm.
Per the last paragraph of [Section 5.2](https://rfc-editor.org/rfc/rfc7515#section-5.2) of [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)], it is an
application-specific decision to choose the appropriate JWS
algorithm from [[JWS.Algs](https://www.rfc-editor.org/rfc/rfc9901.html#JWS.Algs)], including post-quantum algorithms, when they are ready.


### 9.2. Manipulation of Disclosures
Holders can manipulate the Disclosures by changing the values of the claims
before sending them to the Verifier. The Verifier MUST check the Disclosures to
ensure that the values of the claims are correct, i.e., the digests of the Disclosures are actually present in the signed SD-JWT.
A naive Verifier that extracts
all claim values from the Disclosures (without checking the hashes) and inserts them into the SD-JWT payload
is vulnerable to this attack. However, in a structured SD-JWT, without comparing the digests of the
Disclosures, such an implementation could not determine the correct place in a
nested object where a claim needs to be inserted. Therefore, the naive implementation
would not only be insecure, but also incorrect.
The steps described in [Section 7.3](https://www.rfc-editor.org/rfc/rfc9901.html#verifier_verification) ensure that the Verifier
checks the Disclosures correctly.


### 9.3. Entropy of the Salt
The security model that conceals the plaintext claims relies on the high entropy
random data of the salt as additional input to the hash function. The randomness
ensures that the same plaintext claim value does not produce the same digest value. It also
makes it infeasible to guess the preimage of the digest (thereby learning the
plaintext claim value) by enumerating the potential value
space for a claim into the hash function to search for a matching digest value.
It is therefore vitally important that unrevealed salts cannot be learned or guessed,
even if other salts have been revealed. As such, each salt MUST be created
in such a manner that it is cryptographically random, sufficiently long, and
has high enough entropy that it is infeasible to guess. A
new salt MUST be chosen for each claim independently of other salts.
See "Randomness Requirements for Security" [[RFC4086](https://www.rfc-editor.org/rfc/rfc9901.html#RFC4086)] for considerations
on generating random values.
The RECOMMENDED minimum length of the randomly generated portion of the salt is 128 bits.
The Issuer MUST ensure that a new salt value is chosen for each claim,
including when the same claim name occurs at different places in the
structure of the SD-JWT. This can be seen in the example in [Appendix A.2](https://www.rfc-editor.org/rfc/rfc9901.html#example-complex-structured-sd-jwt),
where multiple claims with the name `type` appear, but each of them has
a different salt.


### 9.4. Choice of a Hash Algorithm
To ensure privacy of claims that are selectively disclosable but are not being disclosed in a given presentation,
the hash function MUST ensure that it is infeasible to calculate any portion of the three elements
(salt, claim name, claim value) from a particular digest. This implies the hash function MUST
be preimage resistant and should also not allow an observer to infer any partial information about
the undisclosed content. In the terminology of cryptographic commitment schemes, the hash function
needs to be computationally hiding.
To ensure the integrity of selectively disclosable claims, the hash function MUST be second-preimage
resistant. That is, for any combination of salt, claim name, and claim value, it is infeasible to find a different combination of salt,
claim name, and claim value that results in the same digest.
The hash function SHOULD also be collision resistant. Although not essential to the anticipated uses of
SD-JWT, without collision resistance an Issuer may be able to find multiple Disclosures that have the
same hash value. In which case, the signature over the SD-JWT would not then commit the Issuer to the contents of the
JWT. The collision resistance of the hash function used to generate digests SHOULD
match the collision resistance of the hash function used by the signature scheme. For example, use of
the ES512 signature algorithm would require a Disclosure hash function with at least 256-bit collision
resistance, such as SHA-512.
Inclusion in the "Named Information Hash Algorithm Registry" [[Hash.Algs](https://www.rfc-editor.org/rfc/rfc9901.html#Hash.Algs)]
alone does not indicate a hash algorithm's suitability for use in SD-JWT (it contains several
heavily truncated digests, such as `sha-256-32` and `sha-256-64`, which are unfit for security
applications).


### 9.5. Key Binding
Key Binding aims to ensure that the presenter of an SD-JWT credential is actually the Holder of the credential.
An SD-JWT compatible with Key Binding contains a public key, or a reference to a public key, that corresponds to a private key possessed by the Holder.
The Verifier requires that the Holder prove possession of that private key when presenting the SD-JWT credential.
Without Key Binding, a Verifier only gets the proof that the
credential was issued by a particular Issuer, but the credential itself
can be replayed by anyone who gets access to it. This means that, for
example, after the credential was leaked to an attacker, the attacker can
present the credential to any Verifier that does not require a
binding. Also, a malicious Verifier to which the Holder presented the
credential can present the credential to another Verifier if that other
Verifier does not require Key Binding.
Verifiers MUST decide whether Key Binding is required for a
particular use case before verifying a credential. This decision
can be informed by various factors including but not limited to the following:
business requirements, the use case, the type of
binding between a Holder and its credential that is required for a use
case, the sensitivity of the use case, the expected properties of a
credential, the type and contents of other credentials expected to be
presented at the same time, etc.
It is important that a Verifier not make its security policy
decisions based on data that can be influenced by an attacker. For this reason, when deciding whether or not Key
Binding is required, Verifiers MUST NOT take into account
whether the Holder has provided an SD-JWT+KB or a bare SD-JWT; otherwise, an
attacker could strip the KB-JWT from an SD-JWT+KB and present the resultant SD-JWT.
Furthermore, Verifiers should be aware that Key Binding information may have been added to an SD-JWT in a format that they do not recognize and therefore may not be able to tell whether or not the SD-JWT supports Key Binding.
If a Verifier determines that Key Binding is required for a
particular use case and the Holder presents either a bare SD-JWT or an SD-JWT+KB with
an invalid Key Binding JWT, then the Verifier will reject the presentation
when following the verification steps described in [Section 7.3](https://www.rfc-editor.org/rfc/rfc9901.html#verifier_verification).


### 9.6. Concealing Claim Names
SD-JWT ensures that names of claims that are selectively disclosable are
always concealed unless the claim's value is disclosed. This prevents an attacker from learning the names of such
claims. However, the names of the claims that are permanently
disclosed are not hidden. This includes the keys of objects that themselves
are not concealed, but contain concealed claims. This limitation
needs to be taken into account by Issuers when creating the structure of
the SD-JWT.


### 9.7. Selectively Disclosable Validity Claims
An Issuer MUST NOT allow any content to be selectively disclosable that is critical for evaluating the
SD-JWT's authenticity or validity.
The exact list of such content will depend on the application
and SHOULD be listed by any application-specific profiles of SD-JWT.
The following is a list of registered JWT claim names that SHOULD be considered as
security critical:

- 
            `iss` (Issuer)

          - 
            `aud` (Audience), although issuers MAY allow individual entries in the array to be selectively disclosable

          - 
            `exp` (Expiration Time)

          - 
            `nbf` (Not Before)

          - 
            `cnf` (Confirmation Key)

        
Issuers will typically include claims controlling the validity of the SD-JWT
in plaintext in the SD-JWT payload, but there is no guarantee they will do so. Therefore, Verifiers cannot
reliably depend on that and need to operate as though security-critical claims might be
selectively disclosable.
Verifiers therefore MUST ensure that all claims they deem necessary for checking
the validity of an SD-JWT in the given context are present (or disclosed, respectively) during
validation of the SD-JWT. This is implemented in the last
step of the verification defined in [Section 7.1](https://www.rfc-editor.org/rfc/rfc9901.html#sd_jwt_verification).
The precise set of required validity claims will typically be defined by
operating environment rules, an application-specific profile, or the credential format, and MAY include claims other than
those listed herein.


### 9.8. Distribution and Rotation of Issuer Signature Verification Key
This specification does not define how signature verification keys of
Issuers are distributed to Verifiers. However, it is RECOMMENDED that
Issuers publish their keys in a way that allows for efficient and secure
key rotation and revocation, for example, by publishing keys at a
predefined location using the JSON Web Key Set (JWKS) format [[RFC7517](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7517)].
Verifiers need to ensure that they are not using expired or revoked keys
for signature verification using reasonable and appropriate means for the given
key-distribution method.


### 9.9. Forwarding Credentials
Any entity in possession of an SD-JWT (including an SD-JWT extracted from an SD-JWT+KB) can forward it to any third party
that does not enforce Key Binding.
When doing so, that entity may remove Disclosures such that the receiver
learns only a subset of the claims contained in the original SD-JWT.
For example, a device manufacturer might produce an SD-JWT
containing information about upstream and downstream supply chain contributors.
Each supply chain party can verify only the claims that were selectively disclosed to them
by an upstream party, and they can choose to further reduce the disclosed claims
when presenting to a downstream party.
In some scenarios, this behavior could be desirable;
if it is not, Issuers need to support and Verifiers need to enforce Key Binding.


### 9.10. Integrity of SD-JWTs and SD-JWT+KBs
With an SD-JWT, the Issuer-signed JWT is integrity protected by the Issuer's
signature, and the values of the Disclosures are integrity protected by the digests
included therein. The specific set of Disclosures, however,
is not integrity protected; the SD-JWT can be modified by adding or
removing Disclosures and still be valid.
With an SD-JWT+KB, the set of selected Disclosures is integrity protected.
The signature in the Key Binding JWT covers a
specific SD-JWT, with a specific Issuer-signed JWT and a specific set of
Disclosures.  Thus, the signature on the Key Binding JWT, in addition to proving
Key Binding, also assures the authenticity and integrity of the set of
Disclosures the Holder disclosed.  The set of Disclosures in an SD-JWT+KB is the set
that the Holder intended to send; no intermediate party has added, removed, or
modified the list of Disclosures.


### 9.11. Explicit Typing
[Section 3.11](https://rfc-editor.org/rfc/rfc8725#section-3.11) of [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)] describes the use of explicit typing as one mechanism to prevent confusion attacks
(described in [Section 2.8](https://rfc-editor.org/rfc/rfc8725#section-2.8) of [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)]) in which one kind of JWT is mistaken for another. SD-JWTs are also potentially
subject to such confusion attacks, so in the absence of other techniques, it is RECOMMENDED that application profiles of SD-JWT specify an explicit type
by including the `typ` header parameter when the SD-JWT is issued, and that Verifiers check this value.
When explicit typing using the `typ` header is employed for an SD-JWT, it is RECOMMENDED that a media type name of the format
"application/example+sd-jwt" be used, where "example" is replaced by the identifier for the specific kind of SD-JWT.
The definition of `typ` in [Section 4.1.9](https://rfc-editor.org/rfc/rfc7515#section-4.1.9) of [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)] recommends that the "application/" prefix be omitted, so
"example+sd-jwt" would be the value of the `typ` header parameter.
Use of the `cty` content type header parameter to indicate the content type of the SD-JWT payload can also be used to distinguish different types of JSON objects or different kinds of JWT Claim Sets.


### 9.12. Key Pair Generation and Lifecycle Management
Implementations of SD-JWT rely on asymmetric cryptographic keys and must therefore ensure that key pair generation,
handling, storage, and lifecycle management are performed securely.
While the specific mechanisms for secure key management are out of scope for this document, implementers
should follow established best practices, such as those outlined in NIST SP 800-57 Part 1 [[NIST.SP.800-57pt1r5](https://www.rfc-editor.org/rfc/rfc9901.html#NIST.SP.800-57pt1r5)].
This includes:

- Secure Generation: Using cryptographically secure methods and random number generators.

          - Secure Storage: Protecting private keys from unauthorized access.

          - Lifecycle Management: Ensuring secure key rotation, revocation, and disposal as needed.

        
Appropriate key management is essential, as any compromise can lead to unauthorized disclosure or forgery of SD-JWTs.

---

## 10. Privacy Considerations


### 10.1. Unlinkability
Unlinkability is a property whereby adversaries are prevented from correlating
credential presentations of the same user beyond the user's consent.
Without unlinkability, an adversary might be able to learn more about the user than the user
intended to disclose, for example:

- Cooperating Verifiers might want to track users across services to build
advertising profiles.

          - Issuers might want to track where users present their credentials to enable
surveillance.

          - After a data breach at multiple Verifiers, publicly available information
might allow linking identifiable information presented to Verifier A with
originally anonymous information presented to Verifier B, therefore revealing
the identities of users of Verifier B.

        
The following types of unlinkability are discussed below:

- Presentation Unlinkability: A Verifier should not be able to link two
presentations of the same credential.

          - Verifier/Verifier Unlinkability: The presentations made to two different
Verifiers should not reveal that the same credential was presented (e.g., if the two
Verifiers collude, or if they are forced by a third party to reveal the presentations
made to them, or data leaks from one Verifier to the other).

          - Issuer/Verifier Unlinkability (Honest Verifier): An Issuer of a credential
should not be able to know that a user presented this credential unless
the Verifier is sharing presentation data with the Issuer
accidentally, deliberately, or because it is forced to do so.

          - Issuer/Verifier Unlinkability (Careless/Colluding/Compromised/Coerced Verifier): >An Issuer of a
credential should under no circumstances be able to tell that a user presented this credential to
a certain Verifier. In particular, this includes cases when the Verifier accidentally or deliberately shares
presentation data with the Issuer or is forced to do so.

        
In all cases, unlinkability is limited to cases where the disclosed claims do
not contain information that directly or indirectly identifies the user. For
example, when a taxpayer identification number is contained in the disclosed claims, the Issuer and
Verifier can easily link the user's transactions. However, when the user only
discloses a birthdate to one Verifier and a postal code to another Verifier, the two Verifiers should not be able to determine that they were interacting with the same user.
Issuer/Verifier unlinkability with a careless, colluding, compromised, or coerced Verifier cannot be
achieved in salted hash-based selective disclosure approaches, such as SD-JWT, as the
issued credential with the Issuer's signature is directly presented to the Verifier, who can forward it to
the Issuer. To reduce the risk of revealing the data later on, [Section 10.2](https://www.rfc-editor.org/rfc/rfc9901.html#data_storage) defines
requirements to reduce the amount of data stored.
In considering Issuer/Verifier unlinkability, it is important to note the potential for an asymmetric power dynamic
between Issuers and Verifiers. This dynamic can compel an otherwise Honest Verifier into collusion.
For example, a governmental Issuer might have the authority to mandate that a Verifier report back information
about the credentials presented to it. Legal requirements could further enforce this, explicitly undermining
Issuer/Verifier unlinkability. Similarly, a large service provider issuing credentials might implicitly pressure
Verifiers into collusion by incentivizing participation in their larger operating environment.
Deployers of SD-JWT must be aware of these potential power dynamics,
mitigate them as much as possible, and/or make the risks transparent to the user.
Contrary to that, Issuer/Verifier unlinkability with an Honest Verifier can generally be achieved.
However, a callback from the Verifier to the Issuer, such as a revocation check, could potentially
disclose information about the credential's usage to the Issuer.
Where such callbacks are necessary, they need to be executed in a manner that
preserves privacy and does not disclose details about the credential to the Issuer
(the mechanism described in [[TSL](https://www.rfc-editor.org/rfc/rfc9901.html#I-D.ietf-oauth-status-list)] is an example of an approach
that discloses minimal information towards the Issuer). It is
important to note that the timing of such requests could potentially serve as a side channel.
Verifier/Verifier unlinkability and presentation unlinkability can be achieved using batch issuance: A batch
of credentials based on the same claims is issued to the Holder instead of just
a single credential. The Holder can then use a different credential for each
Verifier or even for each session with a Verifier. New Key Binding keys and
salts MUST be used for each credential in the batch to ensure that the Verifiers
cannot link the credentials using these values. Likewise, claims carrying time
information, like `iat`, `exp`, and `nbf`, MUST either be randomized within a
time period considered appropriate (e.g., randomize `iat` within the last 24
hours and calculate `exp` accordingly) or rounded (e.g., rounded down to the
beginning of the day).
SD-JWT only conceals the value of claims that are not revealed.
It does not meet the security properties for anonymous credentials [[CL01](https://www.rfc-editor.org/rfc/rfc9901.html#CL01)]. In
particular, colluding Verifiers and Issuers can know when they have seen the same
credential no matter what fields have been disclosed, even when none have been disclosed.
This behavior may not align with what users naturally anticipate or are guided to
expect from user-interface interactions, potentially causing them to make decisions
they might not otherwise make. Workarounds such as batch issuance, as
described above, help with keeping
Verifiers from linking different presentations, but cannot work for Issuer/Verifier unlinkability.
This issue applies to all salted hash-based approaches,
including mDL/mDoc [[ISO.18013-5](https://www.rfc-editor.org/rfc/rfc9901.html#ISO.18013-5)] and SD-CWT [[SD-CWT](https://www.rfc-editor.org/rfc/rfc9901.html#I-D.ietf-spice-sd-cwt)].


### 10.2. Storage of User Data
Wherever user data is stored, it represents a potential
target for an attacker. This target can be of particularly
high value when the data is signed by a trusted authority like an
official national identity service. For example, in OpenID Connect [[OpenID.Core](https://www.rfc-editor.org/rfc/rfc9901.html#OpenID.Core)],
signed ID Tokens can be stored by Relying Parties. In the case of
SD-JWT, Holders have to store SD-JWTs,
and Issuers and Verifiers may decide to do so as well.
Not surprisingly, a leak of such data risks revealing private data of users
to third parties. Signed user data, the authenticity of which
can be easily verified by third parties, further exacerbates the risk.
As discussed in [Section 9.5](https://www.rfc-editor.org/rfc/rfc9901.html#key_binding_security), leaked
SD-JWTs may also allow attackers to impersonate Holders unless Key
Binding is enforced and the attacker does not have access to the
Holder's cryptographic keys.
Due to these risks, and the risks described in [Section 10.1](https://www.rfc-editor.org/rfc/rfc9901.html#unlinkability), systems implementing SD-JWT SHOULD be designed to minimize
the amount of data that is stored. All involved parties SHOULD NOT store SD-JWTs
longer than strictly necessary, including in log files.
After Issuance, Issuers SHOULD NOT store the Issuer-signed JWT or the respective
Disclosures.
Holders SHOULD store SD-JWTs only in
encrypted form, and, wherever possible, use hardware-backed encryption
in particular for the private Key Binding key. Decentralized storage
of data, e.g., on user devices, SHOULD be preferred for user
credentials over centralized storage. Expired SD-JWTs SHOULD be deleted
as soon as possible.
After Verification, Verifiers SHOULD NOT store the Issuer-signed JWT or the
respective Disclosures. It may be
sufficient to store the result of the verification and any user data that is
needed for the application.
Exceptions from the rules above can be made if there are strong requirements to do
so (e.g., functional requirements or legal audit requirements), secure storage can
be ensured, and the privacy impact has been assessed.


### 10.3. Confidentiality During Transport
If an SD-JWT or SD-JWT+KB is transmitted over an insecure
channel during issuance or presentation, an adversary may be able to
intercept and read the user's personal data or correlate the information with previous uses.
Usually, transport protocols for issuance and presentation of credentials
are designed to protect the confidentiality of the transmitted data, for
example, by requiring the use of TLS.
This specification therefore considers the confidentiality of the data to be
provided by the transport protocol and does not specify any encryption
mechanism.
Implementers MUST ensure that the transport protocol provides confidentiality
if the privacy of user data or correlation attacks by passive observers are a concern.
To encrypt an SD-JWT or SD-JWT+KB during transit over potentially insecure or leakage-prone channels, implementers MAY use JSON Web Encryption (JWE) [[RFC7516](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7516)], encapsulating the SD-JWT or SD-JWT+KB as the plaintext payload of the JWE.
Especially, when an SD-JWT is transmitted via a URL and information may be stored/cached in the browser or end up in web server logs, the SD-JWT SHOULD be encrypted using JWE.


### 10.4. Decoy Digests
The use of decoy digests is RECOMMENDED when the number of claims (or the existence of particular claims) can be a side channel disclosing information about otherwise undisclosed claims. In particular, if a claim in an SD-JWT is present only if a certain condition is met (e.g., a membership number is only contained if the user is a member of a group), the Issuer SHOULD add decoy digests when the condition is not met.
Decoy digests increase the size of the SD-JWT. The number of decoy digests (or whether to use them at all) is a trade-off between the size of the SD-JWT and the privacy of the user's data.


### 10.5. Issuer Identifier
An Issuer issuing only one type of SD-JWT might have privacy implications, because if the Holder has an SD-JWT issued by that Issuer, its type and claim names can be determined.
For example, if a cancer research institute only issued SD-JWTs with cancer registry information, it is possible to deduce that the Holder owning its SD-JWT is a cancer patient.
Moreover, the Issuer identifier alone may reveal information about the user.
For example, when a military organization or a drug rehabilitation center issues a vaccine credential, Verifiers can deduce that the Holder is a military member or may have a substance use disorder.
To mitigate this issue, a group of issuers may elect to use a common Issuer identifier. A group signature scheme outside the scope of this specification may also be used, instead of an individual signature.

---

## 11. IANA Considerations


### 11.1. JSON Web Token Claims Registration
IANA has registered the following Claims in the
"JSON Web Token Claims" registry [[JWT.Claims](https://www.rfc-editor.org/rfc/rfc9901.html#JWT.Claims)] established by [[RFC7519](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7519)].

          Claim Name:
          
            `_sd`

          
Claim Description:
          Digests of Disclosures for object properties

          
Change Controller:
          IETF

          
Specification Document(s):
          
            [Section 4.2.4.1](https://www.rfc-editor.org/rfc/rfc9901.html#embedding_object_properties) of RFC 9901

        


          Claim Name:
          
            `...`

          
Claim Description:
          Digest of the Disclosure for an array element

          
Change Controller:
          IETF

          
Specification Document(s):
          
            [Section 4.2.4.2](https://www.rfc-editor.org/rfc/rfc9901.html#embedding_array_elements) of RFC 9901

        


          Claim Name:
          
            `_sd_alg`

          
Claim Description:
          Hash algorithm used to generate Disclosure digests and digest over presentation

          
Change Controller:
          IETF

          
Specification Document(s):
          
            [Section 4.1.1](https://www.rfc-editor.org/rfc/rfc9901.html#hash_function_claim) of RFC 9901

        


          Claim Name:
          
            `sd_hash`

          
Claim Description:
          Digest of the SD-JWT to which the KB-JWT is tied

          
Change Controller:
          IETF

          
Specification Document(s):
          
            [Section 4.3](https://www.rfc-editor.org/rfc/rfc9901.html#kb-jwt) of RFC 9901

        


### 11.2. Media Type Registrations
IANA has registered the following media types [[RFC2046](https://www.rfc-editor.org/rfc/rfc9901.html#RFC2046)] in
the "Media Types" registry [[MediaTypes](https://www.rfc-editor.org/rfc/rfc9901.html#MediaTypes)] in the manner described
in [[RFC6838](https://www.rfc-editor.org/rfc/rfc9901.html#RFC6838)].

          Note: For the media type value used in the `typ` header in the Issuer-signed JWT
itself, see [Section 9.11](https://www.rfc-editor.org/rfc/rfc9901.html#explicit_typing).


#### 11.2.1. SD-JWT Content
To indicate that the content is an SD-JWT:

            Type name:
            application

            
Subtype name:
            sd-jwt

            
Required parameters:
            n/a

            
Optional parameters:
            n/a

            
Encoding considerations:
            binary; application/sd-jwt values are a series of base64url-encoded values (some of which may be the empty string) separated by period ('.') and tilde ('~') characters.

            
Security considerations:
            See the Security Considerations sections of RFC 9901, [[RFC7519](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7519)], and [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)].

            
Interoperability considerations:
            n/a

            
Published specification:
            RFC 9901

            
Applications that use this media type:
            Applications requiring selective disclosure of integrity-protected content.

            
Fragment identifier considerations:
            n/a

            
Additional information:
            
              

                Magic number(s):
                n/a

                
File extension(s):
                n/a

                
Macintosh file type code(s):
                n/a

              


            
Person & email address to contact for further information:
            Daniel Fett, mail@danielfett.de

            
Intended usage:
            COMMON

            
Restrictions on usage:
            none

            
Author:
            Daniel Fett, mail@danielfett.de

            
Change Controller:
            IETF

          


#### 11.2.2. JWS JSON Serialized SD-JWT Content
To indicate that the content is a JWS JSON serialized SD-JWT:

            Type name:
            application

            
Subtype name:
            sd-jwt+json

            
Required parameters:
            n/a

            
Optional parameters:
            n/a

            
Encoding considerations:
            binary; application/sd-jwt+json values are represented as a JSON Object.

            
Security considerations:
            See the Security Considerations sections of RFC 9901 and [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)].

            
Interoperability considerations:
            n/a

            
Published specification:
            RFC 9901

            
Applications that use this media type:
            Applications requiring selective disclosure of content protected by ETSI JAdES compliant signatures.

            
Fragment identifier considerations:
            n/a

            
Additional information:
            
              

                Magic number(s):
                n/a

                
File extension(s):
                n/a

                
Macintosh file type code(s):
                n/a

              


            
Person & email address to contact for further information:
            Daniel Fett, mail@danielfett.de

            
Intended usage:
            COMMON

            
Restrictions on usage:
            none

            
Author:
            Daniel Fett, mail@danielfett.de

            
Change Controller:
            IETF

          


#### 11.2.3. Key Binding JWT Content
To indicate that the content is a Key Binding JWT:

            Type name:
            application

            
Subtype name:
            kb+jwt

            
Required parameters:
            n/a

            
Optional parameters:
            n/a

            
Encoding considerations:
            binary; A Key Binding JWT is a JWT; JWT values are encoded as a series of base64url-encoded values separated by period ('.') characters.

            
Security considerations:
            See the Security Considerations sections of RFC 9901, [[RFC7519](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7519)], and [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)].

            
Interoperability considerations:
            n/a

            
Published specification:
            RFC 9901

            
Applications that use this media type:
            Applications utilizing a JWT-based proof-of-possession mechanism.

            
Fragment identifier considerations:
            n/a

            
Additional information:
            
              

                Magic number(s):
                n/a

                
File extension(s):
                n/a

                
Macintosh file type code(s):
                n/a

              


            
Person & email address to contact for further information:
            Daniel Fett, mail@danielfett.de

            
Intended usage:
            COMMON

            
Restrictions on usage:
            none

            
Author:
            Daniel Fett, mail@danielfett.de

            
Change Controller:
            IETF

          


### 11.3. Structured Syntax Suffixes Registration
IANA has registered "+sd-jwt" in
the "Structured Syntax Suffixes" registry [[StructuredSuffix](https://www.rfc-editor.org/rfc/rfc9901.html#StructuredSuffix)] in
the manner described in [[RFC6838](https://www.rfc-editor.org/rfc/rfc9901.html#RFC6838)], which can be used to indicate that
the media type is encoded as an SD-JWT.

          Name:
          SD-JWT

          
+suffix:
          +sd-jwt

          
References:
          RFC 9901

          
Encoding considerations:
          binary; SD-JWT values are a series of base64url-encoded values (some of which may be the empty string) separated by period ('.') or tilde ('~') characters.

          
Interoperability considerations:
          n/a

          
Fragment identifier considerations:
          n/a

          
Security considerations:
          See the Security Considerations sections of RFC 9901, [[RFC7519](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7519)], and [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)].

          
Contact:
          Daniel Fett, mail@danielfett.de

          
Author/Change controller:
          IETF
