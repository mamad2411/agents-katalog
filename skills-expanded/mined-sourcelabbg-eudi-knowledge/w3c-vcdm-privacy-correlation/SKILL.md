---
name: "w3c-vcdm-privacy-correlation"
description: "Use when reviewing early-section W3C VCDM privacy guidance. Covers: privacy architecture and correlation-related risks and mitigations."
sections:
  - "8.1 Spectrum of Privacy*This section is non-normative.*"
  - "8.2 Software Trust Boundaries*This section is non-normative.*"
  - "8.3 Personally Identifiable Information*This section is non-normative.*"
  - "8.4 Identifier-Based Correlation*This section is non-normative.*"
  - "8.5 Signature-Based Correlation*This section is non-normative.*"
  - "8.6 Metadata-based Correlation*This section is non-normative.*"
  - "8.7 Device Tracking and Fingerprinting*This section is non-normative.*"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5167 -->

### 8.1 Spectrum of Privacy*This section is non-normative.*
        

        
It is important to recognize there is a spectrum of privacy ranging from
pseudonymous to strongly identified. Depending on the use case, people have
different comfort levels about the information they are willing to provide
and the information that can be derived from it.
        

        
          
          [Figure 13](https://www.w3.org/TR/vc-data-model-2.0/#fig-privacy-spectrum-ranging-from-pseudonymous-to-fully-identified) 
Privacy spectrum ranging from pseudonymous to fully identified.
          
        

        
Privacy solutions are use case specific.
For example, many people would prefer to remain anonymous when purchasing
alcohol because the regulation is only to verify whether a purchaser is
above a specific age. In contrast, when filling prescriptions written by
a medical professional for a patient, the pharmacy is legally required
to more strongly identify both the prescriber and the patient. No single
approach to privacy works for all use cases.
        

        Note: Proof of age might be insufficient for some use cases
Even those who want to remain anonymous when purchasing alcohol might need
to provide photo identification to appropriately assure the merchant. The
merchant might not need to know your name or any details other than that
you are over a specific age, but in many cases, simple proof of age might
be insufficient to meet regulations.
        

        
The Verifiable Credentials Data Model strives to support the full privacy
spectrum and does not take philosophical positions on the correct level of
anonymity for any specific transaction. The following sections will guide
implementers who want to avoid specific scenarios that are hostile to
privacy.

---

### 8.2 Software Trust Boundaries*This section is non-normative.*
        

        
A variety of trust relationships exist in the
[ecosystem described by this specification](https://www.w3.org/TR/vc-data-model-2.0/#ecosystem-overview). An
individual using a web browser trusts the web browser, also known as a [user agent](https://www.w3.org/TR/UAAG20/#def-user-agent), to preserve
that trust by not uploading their personal information to a data broker;
similarly, entities filling the roles in the ecosystem described by this
specification trust the software that operates on behalf of each of those roles.
Examples include the following:
        

        
          - 
An [issuer's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers)
[user agent](https://www.w3.org/TR/UAAG20/#def-user-agent)
(issuer software), such as an online education platform, is expected to
issue [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) only to individuals that the issuer asserts
have completed their educational program.
          
          - 
A [verifier's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
[user agent](https://www.w3.org/TR/UAAG20/#def-user-agent)
(verification software), such as a hiring website, is expected to only allow
access to individuals with a valid verification status for
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) provided to
the platform by such individuals.
          
          - 
A [holder's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
[user agent](https://www.w3.org/TR/UAAG20/#def-user-agent)
(holder software), such as a digital wallet, is expected to only divulge
information to a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) when the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) consents to
releasing that information.
          
        

        
The examples above are not exhaustive, and the users in these roles can also
expect various other things from the software they use to achieve their
goals. In short, the user expects the software to operate in the user's best
interests; any violations of this expectation breach trust and can lead to the
software's replacement with a more trustworthy alternative. Implementers are
strongly encouraged to create software that preserves user trust. Additionally,
they are encouraged to include auditing features that enable users or trusted
third parties to verify that the software is operating in alignment with their
best interests.
        

        
Readers are advised that some software, like a website providing services
to a single [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) and multiple [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders), might operate as a
[user agent](https://www.w3.org/TR/UAAG20/#def-user-agent) to both
roles but might not always be able to operate simultaneously in the best
interests of all parties. For example, suppose a website detects an attempt at
fraudulent [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) use among multiple [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders). In that
case, it might report such an anomaly to the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), which might be
considered not to be in all [holders'](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) best interest, but would be in the
best interest of the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) and any [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) *not* committing
such a violation. It is imperative that when software operates in this manner,
it is made clear in whose best interest(s) the software is operating, through
mechanisms such as a website use policy.

---

### 8.3 Personally Identifiable Information*This section is non-normative.*
        

        
Data associated with [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) stored in the
`credential.credentialSubject` property is susceptible to privacy violations
when shared with [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). Personally identifying data, such as a
government-issued identifier, shipping address, or full name, can be easily
used to determine, track, and correlate an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities). Even information that
does not seem personally identifiable, such as the combination of a
birthdate and a postal code, has powerful correlation and de-anonymization
capabilities.
        

        
Implementers of software used by [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) are strongly advised to warn
[holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) when they share data with these kinds of characteristics.
[Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) are strongly advised to provide privacy-protecting [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) when possible — for example, by issuing `ageOver` [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) instead of `dateOfBirth` [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) for use when a
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) wants to determine whether an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) is at least 18 years of age.
        

        
Because a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) often contains personally identifiable
information (PII), implementers are strongly advised to use mechanisms while
storing and transporting [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that protect the data from
those who ought not have access to it. Mechanisms that could be considered include
Transport Layer Security (TLS) or other means of encrypting the data while in
transit, as well as encryption or access control mechanisms to protect
the data in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) when at rest.
        

        
Generally, individuals are advised to assume that a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential),
like most physical credentials, will leak personally identifiable information
when shared. To combat such leakage, [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and their
securing mechanisms need to be carefully designed to prevent correlation.
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) specifically designed to protect against leakage
of personally identifiable information are available. Individuals and
implementers are encouraged to choose these credential types over those not
designed to protect personally identifiable information.

---

### 8.4 Identifier-Based Correlation*This section is non-normative.*
        

        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) might contain long-lived identifiers that could be
used to correlate individuals. These identifiers include [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)
identifiers, email addresses, government-issued identifiers, organization-issued
identifiers, addresses, healthcare vitals, and many other long-lived
identifiers. Implementers of software for [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) are encouraged to
detect identifiers in [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that could be used
to correlate individuals and to warn [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) before they share this
information. The rest of this section elaborates on guidance related to
using long-lived identifiers.
        

        
[Subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are identified using the `id`
property, as defined in Section [4.4 Identifiers](https://www.w3.org/TR/vc-data-model-2.0/#identifiers) and used in places such
as the `credentialSubject.id` property. The identifiers used to identify a
[subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) create a greater correlation risk when the identifiers are
long-lived or used across more than one web domain. Other types of identifiers
that fall into this category are email addresses, government-issued identifiers,
and organization-issued identifiers.
        

        
Similarly, disclosing the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) identifier (as in
[Example 3](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-id-property)) can lead to situations where multiple
[verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), or an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), can collude to correlate the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
        

        
[Holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) aiming to reduce correlation are encouraged to use [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) from [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) that support selectively disclosing correlating
identifiers in a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). Such approaches expect the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to generate the identifier and might even allow hiding the identifier
from the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) through techniques like
[blind signatures](https://en.wikipedia.org/wiki/Blind_signature),
while still keeping the identifier embedded and signed in the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        

        
[Securing mechanism](https://www.w3.org/TR/vc-data-model-2.0/#dfn-securing-mechanism) specification authors are advised to avoid enabling
identifier-based correlation by designing their technologies to avoid the use
of correlating identifiers that cannot be selectively disclosed.
        

        
If strong anti-correlation properties are required in a [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) system, it is essential that identifiers meet one or more
of the following criteria:
        

        
          - 
Selectively disclosable
          
          - 
Bound to a single origin
          
          - 
Single-use
          
          - 
Not used and instead replaced by short-lived, single-use bearer tokens.

---

### 8.5 Signature-Based Correlation*This section is non-normative.*
        

        
The contents of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are secured using a [securing mechanism](https://www.w3.org/TR/vc-data-model-2.0/#dfn-securing-mechanism). Values representing the securing mechanism pose a greater
risk of correlation when they remain the same across multiple sessions
or domains. Examples of these include the following values:
        

        
          - 
the binary value of the digital signature
          
          - 
timestamp information associated with the creation of the digital signature
          
          - 
cryptographic material associated with the digital signature, such as
a public key identifier
          
        

        
When strong anti-correlation properties are required, [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) are encouraged
to produce [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) where signature values and metadata can
be regenerated for each [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). This can be achieved using
technologies that support unlinkable disclosure, such as the [Data Integrity BBS Cryptosuites v1.0](https://www.w3.org/TR/vc-di-bbs/)
specification. When possible, [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) are encouraged to prefer
[verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) that use this technology in order to enhance
privacy for [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects).
        

        Note: Unlinkability is not a complete solution
Even with unlinkable signatures, a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) might contain
other information that undermines the anti-correlation properties of the
cryptography used. See Sections [8.3 Personally Identifiable Information](https://www.w3.org/TR/vc-data-model-2.0/#personally-identifiable-information),
[8.4 Identifier-Based Correlation](https://www.w3.org/TR/vc-data-model-2.0/#identifier-based-correlation), [8.6 Metadata-based Correlation](https://www.w3.org/TR/vc-data-model-2.0/#metadata-based-correlation),
[8.11 Correlation During Validation](https://www.w3.org/TR/vc-data-model-2.0/#correlation-during-validation), and most other subsections of
Section [8. Privacy Considerations](https://www.w3.org/TR/vc-data-model-2.0/#privacy-considerations).

---

### 8.6 Metadata-based Correlation*This section is non-normative.*
        

        
Different extension points, such as those described in Section
[4. Basic Concepts](https://www.w3.org/TR/vc-data-model-2.0/#basic-concepts) and Section [5. Advanced Concepts](https://www.w3.org/TR/vc-data-model-2.0/#advanced-concepts), can
unintentionally or undesirably serve as a correlation mechanism, if relatively
few [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) use a specific extension type or combination of types.
For example, using certain cryptographic methods unique to particular
nation-states, revocation formats specific to certain jurisdictions,
or credential types employed by specific localities, can serve as mechanisms
that reduce the pseudonymity a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) might expect when selectively
disclosing information to a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
        

        
[Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) are encouraged to minimize metadata-based correlation risks when
issuing [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) intended for pseudonymous use by limiting
the types of extensions that could reduce the [holder's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) pseudonymity.
Credential types, extensions, and technology profiles with global adoption are
most preferable, followed by those with national use; those with only local
use are least preferable.

---

### 8.7 Device Tracking and Fingerprinting*This section is non-normative.*
        

        
There are mechanisms external to [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that
track and correlate individuals on the Internet and the Web. These
mechanisms include Internet protocol (IP) address tracking, web browser
fingerprinting, evercookies, advertising network trackers, mobile network
position information, and in-application Global Positioning System (GPS) APIs.
Using [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) cannot prevent the use of these other
tracking technologies; rather, using these technologies alongside
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can reveal new correlatable information. For
instance, a birthdate combined with a GPS position can strongly correlate
an individual across multiple websites.
        

        
Privacy-respecting systems ought to aim to prevent the combination of other
tracking technologies with [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). In some instances,
tracking technologies might need to be disabled on devices that
transmit [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) on behalf of a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
        

        
The Oblivious HTTP protocol [[RFC9458](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc9458)] is one mechanism implementers
might consider using when fetching external resources associated with a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
Oblivious HTTP allows a client to make multiple requests to an origin server
without that server being able to link those requests to that client or even to
identify those requests as having come from a single client, while placing only
limited trust in the nodes used to forward the messages. Oblivious HTTP
is one privacy-preserving mechanism that can reduce the possibility
of device tracking and fingerprinting. Below are some concrete examples of
ways that Oblivious HTTP can benefit ecosystem participants.
        

        
          - 
A [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) using a digital wallet can reduce the chances that they
will be tracked by a 3rd party when accessing external links within a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) stored in their digital wallet.
For example, a digital wallet might fetch and render linked images, or
it might check the validity of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) by fetching
an externally linked revocation list.
          
          - 
A [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) can reduce its likelihood of signaling to an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers)
that the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) has received a specific [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
For example, a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might fetch an externally linked revocation
list while performing status checks on a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
