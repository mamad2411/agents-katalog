---
name: "w3c-vcdm-security"
description: "Use when reviewing W3C VCDM security or privacy considerations. Covers: security concerns for verifiable credentials and ecosystem deployments."
sections:
  - "9. Security Considerations*This section is non-normative.*"
  - "9.1 Cryptography Suites and Libraries*This section is non-normative.*"
  - "9.2 Key Management*This section is non-normative.*"
  - "9.3 Content Integrity Protection*This section is non-normative.*"
  - "9.4 Unsigned Claims*This section is non-normative.*"
  - "9.5 Man-in-the-Middle (MITM), Replay, and Cloning Attacks*This section is non-normative.*"
  - "9.6 Bundling Dependent Claims*This section is non-normative.*"
  - "9.7 Highly Dynamic Information*This section is non-normative.*"
  - "9.8 Device Theft and Impersonation*This section is non-normative.*"
  - "9.9 Acceptable Use*This section is non-normative.*"
  - "9.10 Code Injection*This section is non-normative.*"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~6008 -->

## 9. Security Considerations*This section is non-normative.*
      

      
[Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders), and [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) should be aware of a number of
security considerations when processing data described by this specification.
Ignoring or not understanding the implications of this section can result in
security vulnerabilities.
      

      
While this section highlights a broad set of security considerations, it is a
partial list. Implementers of mission-critical systems using the technology
described in this specification are strongly encouraged to consult security and
cryptography professionals for comprehensive guidance.
      

### 9.1 Cryptography Suites and Libraries*This section is non-normative.*
        

        
Cryptography can protect some aspects of the data model described in this
specification. It is important for implementers to understand the cryptography
suites and libraries used to create and process [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) and
[presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation). Implementing and auditing cryptography systems generally
requires substantial experience. Effective
[red teaming](https://en.wikipedia.org/wiki/Red_team) can also
help remove bias from security reviews.
        

        
Cryptography suites and libraries have a shelf life and eventually succumb to
new attacks and technological advances. Production quality systems need to take
this into account and ensure mechanisms exist to easily and proactively upgrade
expired or broken cryptography suites and libraries, and to invalidate and
replace existing [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential). Regular monitoring is important to
ensure the long term viability of systems processing [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential).
        
      

### 9.2 Key Management*This section is non-normative.*
        
        
The security of most digital signature algorithms, used to secure [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), depends on the quality and
protection of their *private signing keys*. The management of
cryptographic keys encompasses a vast and complex field. For comprehensive
recommendations and in-depth discussion, readers are directed to
[[NIST-SP-800-57-Part-1](https://www.w3.org/TR/vc-data-model-2.0/#bib-nist-sp-800-57-part-1)]. As strongly recommended in both [[FIPS-186-5](https://www.w3.org/TR/vc-data-model-2.0/#bib-fips-186-5)] and
[[NIST-SP-800-57-Part-1](https://www.w3.org/TR/vc-data-model-2.0/#bib-nist-sp-800-57-part-1)], a private signing key is not to be used for multiple
purposes; for example, a private signing key is not to be used for encryption
as well as signing.
        
        
[[NIST-SP-800-57-Part-1](https://www.w3.org/TR/vc-data-model-2.0/#bib-nist-sp-800-57-part-1)] strongly advises that private signing keys and
*public verification keys* have limited *cryptoperiods*, where
a *cryptoperiod* is "the time span during which a specific key is
authorized for use by legitimate entities or the keys for a given system will
remain in effect." [[NIST-SP-800-57-Part-1](https://www.w3.org/TR/vc-data-model-2.0/#bib-nist-sp-800-57-part-1)] gives extensive
guidance on cryptoperiods for different key types under various conditions
and recommends a one to three year cryptoperiod for a private signing key.
        
        
To deal with potential private key compromises, [[NIST-SP-800-57-Part-1](https://www.w3.org/TR/vc-data-model-2.0/#bib-nist-sp-800-57-part-1)]
provides recommendations for protective measures, harm reduction, and
revocation. Although this section focuses primarily on the security of the
private signing key, [[NIST-SP-800-57-Part-1](https://www.w3.org/TR/vc-data-model-2.0/#bib-nist-sp-800-57-part-1)] also highly recommends
confirmation of the validity of all [verification material](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verification-material) before using it.
        
      

### 9.3 Content Integrity Protection*This section is non-normative.*
        

        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) often contain URLs to data that resides outside
the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). Linked content that exists outside a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) — such as images, JSON-LD extension contexts,
JSON Schemas, and other machine-readable data — is not protected
against tampering because the data resides outside of the protection of the
[securing mechanism](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms) on the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        

        
Section [5.3 Integrity of Related Resources](https://www.w3.org/TR/vc-data-model-2.0/#integrity-of-related-resources) of this specification provides an
optional mechanism for ensuring the integrity of the content of external
resources. This mechanism is not necessary for external resources that do not
impact the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)'s security. However, its implementation
is crucial for external resources where content changes could potentially
introduce security vulnerabilities.
        

        
Implementers need to recognize the potential security risks associated with
unprotected URLs of external machine-readable content. Such vulnerabilities
could lead to successful attacks on their applications. Where changes to
external resources might compromise security, implementers will benefit by
employing the content integrity protection mechanism outlined in this
specification.
        

      

### 9.4 Unsigned Claims*This section is non-normative.*
        

        
This specification enables the creation of [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) without signatures
or proofs. These [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) classes are often useful for intermediate
storage or self-asserted information, analogous to filling out a form on a web
page. Implementers ought to be aware that these [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) types are not
[verifiable](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) because the authorship either is unknown or cannot be trusted.
        
      

### 9.5 Man-in-the-Middle (MITM), Replay, and Cloning Attacks*This section is non-normative.*
        

        
The data model does not inherently prevent
[Man-in-the-Middle (MITM)](https://en.wikipedia.org/wiki/Man-in-the-middle_attack),
[replay](https://en.wikipedia.org/wiki/Replay_attack), and
[spoofing](https://en.wikipedia.org/wiki/Spoofing_attack) attacks.
Both online and offline use cases might be susceptible to these attacks, where
an adversary intercepts, modifies, re-uses, and/or replicates the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) data during transmission or storage.
        
#### 9.5.1 Man-in-the-Middle (MITM) Attack

        
A [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might need to ensure it is the intended recipient of a
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) and not the target of a
[man-in-the-middle attack](https://en.wikipedia.org/wiki/Man-in-the-middle_attack). Some [securing
mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms), like [Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/) [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)] and
[Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/) [[VC-DATA-INTEGRITY](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-data-integrity)], provide an
option to specify a [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation)'s intended audience or domain, which can
help reduce this risk.
        
        
Other approaches, such as token binding [[RFC8471](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc8471)], which ties the request for
a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) to the response, can help secure the protocol.
Any unsecured protocol is susceptible to man-in-the-middle attacks.
        
#### 9.5.2 Replay Attack

        
A [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might wish to limit the number of times that
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) can be used. For example, multiple individuals
presenting the same [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) representing an event ticket
might be granted entry to the event, undermining the purpose of the ticket
from the perspective of its [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers). To prevent such replay attacks,
[verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) require [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to include additional security measures
in their [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). Examples include the following:
          
            - 
A [challenge](https://en.wikipedia.org/wiki/Challenge%E2%80%93response_authentication)
provided by the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), which the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) incorporates into
a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). The [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) enforces challenge
uniqueness to prevent replay attacks.
            
            - 
A [validity period](https://www.w3.org/TR/vc-data-model-2.0/#validity-period), limiting the window
during which the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) is valid.
            
          
        
#### 9.5.3 Spoofing Attack

        
[Verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might have a vested interest in knowing that a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) is
authorized to present the [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) inside of a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
While the data model outlines the structure and data elements necessary for a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), it does not include a mechanism to ascertain the
authorization of presented [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential). To address this concern,
implementers might need to explore supplementary methods, such as binding
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to strong authentication mechanisms or using
additional properties in [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation)
to enable proof of control.
        
      
### 9.6 Bundling Dependent Claims*This section is non-normative.*
        

        
It is considered best practice for [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to atomize information in a
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) or use a signature scheme that allows for selective
disclosure. When atomizing information, if it is not done securely by the
[issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), the [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) might bundle together [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) from different
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) in ways that the [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) did not intend.
        

        
Consider a university issuing two [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to an individual.
Each [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) contains two properties that, when combined, indicate the
person's "role" in a specific "department." For instance, one [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
pair might designate "Staff Member" in the "Department of Computing," while
another could signify "Post Graduate Student" in the "Department of Economics."
Atomizing these [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) results in the university issuing
four separate [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) to the individual. Each [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) contains
a single designation: "Staff Member", "Post Graduate Student", "Department of
Computing", or "Department of Economics". The [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) might then present
the "Staff Member" and "Department of Economics" [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to
a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), which, together, would comprise a false [claim](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims).
        
      

### 9.7 Highly Dynamic Information*This section is non-normative.*
        

        
When [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) contain highly dynamic information, careful
consideration of validity periods becomes crucial. Issuing [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) with validity periods that extend beyond their intended use creates
potential security vulnerabilities that malicious actors could exploit. Validity
periods shorter than the timeframe where the information expressed by the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is expected to be used creates a burden on
[holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). It is, therefore, important to set validity
periods for [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) appropriate to the use case and the
expected lifetime of the information contained in the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        
      

### 9.8 Device Theft and Impersonation*This section is non-normative.*
        

        
Storing [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) on a device poses risks if the device is
lost or stolen. An attacker gaining possession of such a device potentially
acquires unauthorized access to systems using the victim's [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). Ways to mitigate this type of attack include:
        

        
          - 
Enabling password, pin, pattern, or biometric screen unlock protection on the
device.
          
          - 
Enabling password, biometric, or multi-factor authentication for the
[credential repository](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential-repositories).
          
          - 
Enabling password, biometric, or multi-factor authentication when accessing
cryptographic keys.
          
          - 
Using a separate hardware-based signature device.
          
          - 
All or any combination of the above.
          
        

        
Furthermore, instances of impersonation can manifest in various forms,
including situations where an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) attempts to disavow its actions.
Elevating trust and security within the realm of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
entails more than averting impersonation; it also involves implementing
non-repudiation mechanisms. These mechanisms solidify an [entity's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities)
responsibility for its actions or transactions, reinforcing accountability and
deterring malicious behavior. Attainment of non-repudiation is a
multifaceted endeavor, encompassing an array of techniques including
[securing mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms), proofs of possession,
and authentication schemes in various protocols designed to foster trust and
reliability.
        
      
### 9.9 Acceptable Use*This section is non-normative.*
        

        
Ensuring alignment between an [entity's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) actions — such as [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation),
and the intended purpose of those actions — is essential. It involves having the
authorization to use [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and using [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) in a
manner that adheres to their designated scope(s) and objective(s). Two critical
aspects in this context are Unauthorized Use and Inappropriate Use.
        
#### 9.9.1 Unauthorized Use
        
Entities using [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation)
beyond their intended purpose are engaging in unauthorized activity. One class
of unauthorized use is a confidentiality violation. Consider a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
that shares a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) with a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
to establish their age and residency status. If the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) then proceeds
to employ the [holder's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) data without proper consent, such as by selling the
data to a data broker, that would constitute an unauthorized use of the data,
violating an expectation of privacy that the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) might have in the
transaction.
        
        
Similarly, an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) can employ a [termsOfUse](https://www.w3.org/TR/vc-data-model-2.0/#terms-of-use)
property to specify how and when a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) might be permitted and expected
to use a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential). A [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) using [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) outside of the
scope(s) defined in the `termsOfUse` would be considered to be unauthorized.
        
        Note: Digital Rights Management is out of scope
Further study is required to determine how a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) can assert and
enforce authorized use of their data after [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation).
        
#### 9.9.2 Inappropriate Use
        
While valid cryptographic signatures and successful status checks signify the
reliability of [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), they do not signify that all
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) are interchangeable for all contexts. It is crucial that
[verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) also [validate](https://www.w3.org/TR/vc-data-model-2.0/#validation) any relevant [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims),
considering the source and nature of the [claim](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) alongside the purpose
for which the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) presents the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential).
        
        
For instance, in scenarios where a certified medical diagnosis is required, a
self-asserted [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) carrying the necessary data might not suffice
because it lacks validity from an authoritative medical source. To ensure proper
[credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) use, stakeholders need to assess the
[credential's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) relevance and authority within the
specific context of their intended application.
        
      

### 9.10 Code Injection*This section is non-normative.*
        

        
Data in [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can include injectable code or code from
scripting languages. Authors of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) benefit from avoiding
such inclusions unless necessary and only after mitigating associated risks to
the fullest extent possible.

        

        
For example, a single natural language string containing multiple languages or
annotations often requires additional structure or markup for correct
presentation. Markup languages, such as HTML, can label text spans in different
languages or supply string-internal markup needed to display [bidirectional text](https://www.w3.org/TR/i18n-glossary/#dfn-bidirectional-text) properly. It is also possible to use the `rdf:HTML` datatype to encode
such values accurately in JSON-LD.
        

        
Despite the ability to encode information as HTML, implementers are strongly
discouraged from doing so for the following reasons:
        

        
          - 
It requires some version of an HTML processor, which increases the burden of
processing language and base direction information.
          
          - 
It increases the security attack surface when using this data model,
because naively processing HTML could result in the execution of a `script`
tag that an attacker injected at some point during the data production process.
          
        

        
If implementers feel they need to use HTML, or other markup languages capable of
containing executable scripts, to address a specific use case, they are advised
to analyze how an attacker could use the markup to mount injection attacks
against a consumer of the markup. This analysis should be followed by the
proactive deployment of mitigations against the identified attacks, such as
running the HTML rendering engine in a sandbox with no ability to access the
network.
