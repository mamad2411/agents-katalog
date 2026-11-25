---
name: "w3c-vcdm-privacy-minimization-continued"
description: "Use when implementing later mid-section W3C VCDM privacy mitigations. Covers additional selective disclosure and privacy-preserving design patterns."
sections:
  - "8.12 Storage Providers and Data Mining*This section is non-normative.*"
  - "8.13 Aggregation of Credentials*This section is non-normative.*"
  - "8.14 Patterns of Use*This section is non-normative.*"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~3157 -->

### 8.12 Storage Providers and Data Mining*This section is non-normative.*
        

        
When a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) receives a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) from an
[issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) needs to be stored somewhere
(for example, in a [credential repository](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential-repositories)). [Holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) need to be aware
that the information in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can be sensitive and highly
individualized, making it a prime target for data mining. Services offering
"free of charge" storage of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) might mine personal data
and sell it to organizations interesting in building individualized profiles
on people and organizations.
        
        
[Holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) need to be aware of the terms of service for their
[credential repository](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential-repositories), specifically the correlation and data mining
protections in place for those who store their [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
with the service provider.
        
        
Some effective mitigations for data mining and profiling include using:
        

        
          - 
Service providers that do not sell your information to third parties.
          
          - 
Software that encrypts [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) such that a service
provider cannot view the contents of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential).
          
          - 
Software that stores [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) locally on a device that you
control and that does not upload or analyze your information beyond your
expectations.
          
        

        
In addition to the mitigations above, civil society and regulatory
participation in vendor analysis and auditing can help ensure that legal
protections are enacted and enforced for individuals affected by practices
that are not aligned with their best interests.

---

### 8.13 Aggregation of Credentials*This section is non-normative.*
        

        
Having two pieces of information about the same [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) often reveals
more about the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) than the combination of those two pieces, even
when the pieces are delivered through different channels. Aggregating
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) poses a privacy risk, and all participants in
the ecosystem need to be aware of the risks of data aggregation.
        

        
For example, suppose two [bearer credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-bearer-credentials), one for an email address and
one stating the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) is over 21, are provided to the same [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
across multiple sessions. The [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) of the information now has a unique
identifier (the email address) along with age-related ("over 21") information
for that individual. It is now easy to create a profile for the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders),
building it by adding more and more information as it leaks over time.
Aggregation of such [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) can also be performed by multiple sites
in collusion with each other, leading to privacy violations.
        

        
From a technological perspective, preventing information aggregation is a
challenging privacy problem. While new cryptographic techniques, such as
zero-knowledge proofs, are being proposed as solutions to aggregation and
correlation issues, the existence of long-lived identifiers and
browser-tracking techniques defeats even the most modern cryptographic
techniques.
        

        
The solution to the privacy implications of correlation or aggregation tends
not to be technological in nature, but policy-driven instead. Therefore, if a
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) wishes to avoid the aggregation of their information, they need to
express this in the [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) they transmit, and
by the [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to whom they transmit their
[verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).

---

### 8.14 Patterns of Use*This section is non-normative.*
        

        
Despite best efforts by all involved to assure privacy, using
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can potentially lead to de-anonymization and a
loss of privacy. This correlation can occur when any of the following occurs:
        

        
          - 
The same [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is presented to the same [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
more than once. The [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) could infer that the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) is the
same individual.
          
          - 
The same [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is presented to different
[verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), and either those [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) collude, or a third party
has access to transaction records from both [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). An observant
party could infer that the individual presenting the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is the same person at both services. That is, the
same person controls both accounts.
          
          - 
A [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) identifier of a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) refers to the same
[subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) across multiple [presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) or [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). Even
when different [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) are presented, if the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)
identifier is the same, [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) (and those with access to
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) logs) could infer that the [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)' [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)
are the same entity.
          
          - 
The underlying information in a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) can be used to identify an
individual across services. In this case, using information from other sources
(including information provided directly by the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)), [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
can use information inside the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) to correlate the individual
with an existing profile. For example, if a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) presents
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) that include postal code, age, and gender, a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
can potentially correlate the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) of that [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) with an
established profile. For more information, see [[DEMOGRAPHICS](https://www.w3.org/TR/vc-data-model-2.0/#bib-demographics)].
          
          - 
Passing the identifier of a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) to a centralized revocation server.
The centralized server can correlate uses of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) across
interactions. For example, if a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) is used to prove age in this
manner, the centralized service could know everywhere that [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) was
presented (all liquor stores, bars, adult stores, lottery sellers, and so on).
          
        

        
In part, it is possible to mitigate this de-anonymization and loss of privacy
by:
        

        
          - 
The [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) software providing a globally-unique identifier as the
[subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) for any given [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and never reusing that
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
          
          - 
The [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) using a globally-distributed service for revocation such that
it is not contacted when revocation checks are performed.
          
          - 
Specification authors designing revocation mechanisms that do not depend on
submitting a unique identifier for a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to a query API,
and instead use, for example, a privacy-preserving revocation list.
          
          - 
[Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) avoiding the association of personally identifiable information
with any specific long-lived [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) identifier.
          
        

        
Unfortunately, these mitigation techniques are only sometimes practical or
even compatible with necessary use. Sometimes, correlation is a requirement.
        
        
For example, in some prescription drug monitoring programs, monitoring prescription
use is a requirement. Enforcement entities need to be able to confirm that individuals
are not cheating the system to get multiple prescriptions for controlled
substances. This statutory or regulatory need to correlate prescription
use overrides individual privacy concerns.
        

        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) will also be used to intentionally correlate
individuals across services. For example, when using a common persona to log in
to multiple services, all activity on each of those services is
intentionally linked to the same individual. This is not a privacy issue as
long as each of those services uses the correlation in the expected manner.
        

        
Privacy violations related to the use of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) occur when
unintended or unexpected correlation arises from the presentation of those
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
