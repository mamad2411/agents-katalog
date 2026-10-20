---
name: "w3c-vcdm-terminology"
description: "Use when looking up W3C VCDM 2.0 terminology or understanding key term definitions. Covers core vocabulary used across the specification."
sections:
  - "2. Terminology"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~2941 -->

## 2. Terminology
      

      
The following terms are used to describe concepts in this specification.
      

      
        claim
        
An assertion made about a [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects).
        
        credential
        
A set of one or more [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) made by an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers). The [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims)
in a credential can be about different [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects). The definition of
credential used in this specification differs from,
[NIST's definitions of
credential](https://csrc.nist.gov/glossary/term/credential).
        
        decentralized identifier
        
A portable URL-based identifier, also known as a ***DID***,
is associated with an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities). These identifiers are most often used in a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and are associated with [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) such that a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can be easily ported from one
[credential repository](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential-repositories) to another without reissuing the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential).
An example of a DID is `did:example:123456abcdef`. See the
[Decentralized Identifiers (DIDs) v1.0](https://www.w3.org/TR/did-core/) specification for further details.
        
        
        
        default graph
        
The [graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs) containing all [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) that are not explicitly part of
a [named graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-named-graphs).
        
        
        
        entity
        
Anything that can be referenced in statements as an abstract or concrete noun.
Entities include but are not limited to people, organizations, physical things,
documents, abstract concepts, fictional characters, and arbitrary text. Any
entity might perform roles in the ecosystem, if it can do so. Note
that some entities fundamentally cannot take actions, for example, the string "abc"
cannot issue credentials.
        
        graph
        
A set of claims, forming a network of information composed of [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)
and their relationship to other [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) or data. Each [claim](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) is
part of a graph; either explicit in the case of [named graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-named-graphs), or
implicit for the [default graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-default-graph).
        
        holder
        
A role an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) might perform by possessing one or more
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and generating [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation)
from them. A holder is often, but not always, a [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) of the
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) they are holding. Holders store their
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) in [credential repositories](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential-repositories).
        
        issuer
        
A role an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) can perform by asserting [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) about one or
more [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects), creating a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) from these
[claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims), and transmitting the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to a
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
        
        named graph
        
A [graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs) associated with specific properties, such as
`verifiableCredential`. These properties
result in separate [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs) that contain all [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) defined in the
corresponding JSON objects.
        
        presentation
        
Data derived from one or more [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) issued by one or
more [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) that is shared with a specific [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
        
        credential repository
        
Software, such as a file system, storage vault, or personal [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) wallet, that stores and protects access to [holders'](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        
        selective disclosure
        
The ability of a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to make fine-grained decisions about what
information to share.
        
        unlinkable disclosure
        
A type of [selective disclosure](https://www.w3.org/TR/vc-data-model-2.0/#dfn-selective-disclosure) where [presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) cannot be correlated
between [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
        
        subject
        
A thing about which [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) are made.
        
        
        
        validation
        
The assurance that a [claim](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) from a specific [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) satisfies the business
requirements of a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) for a particular use. This specification defines
how verifiers verify [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). It also specifies that [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) validate claims in
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) before relying on them. However, the means for such
validation vary widely and are outside the scope of this specification.
[Verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) trust certain [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) for certain claims and apply their own
rules to determine which claims in which [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) are suitable for use by
their systems.
        
        verifiable credential
        
A tamper-evident [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) whose authorship can be cryptographically
verified. Verifiable credentials can be used to build
[verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), which can also be cryptographically verifiable.
        
        verifiable data registry
        
A role a system might perform by mediating the creation and [verification](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify)
of identifiers, [verification material](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verification-material), and other relevant data, such as
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) schemas, revocation registries,
and so on, which might require using [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). Some
configurations might require correlatable identifiers for [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects). Some
registries, such as ones for UUIDs and [verification material](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verification-material), might act
as namespaces for identifiers.
        
        verifiable presentation
        
A tamper-evident presentation of information encoded in such a way that
authorship of the data can be trusted after a process of cryptographic
verification. Certain types of verifiable presentations might contain data that
is synthesized from, but does not contain, the original [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
(for example, zero-knowledge proofs).
        
        verification
        
The evaluation of whether a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) is an authentic and current statement of the issuer or presenter,
respectively. This includes checking that the credential or presentation
conforms to the specification, the securing mechanism is satisfied, and, if
present, the status check succeeds. Verification of a credential does not imply
evaluation of the truth of [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) encoded in the credential.
        
        verifier
        
A role an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) performs by receiving one or more
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), optionally inside a
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) for processing. Other specifications might refer
to this concept as a relying party.
        
        verification material
        
Information that is used to verify the security of cryptographically
protected information. For example, a cryptographic public key is used to verify
a digital signature associated with a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        
        URL
        
A Uniform Resource Locator, as defined by the [URL Standard](https://url.spec.whatwg.org/). URLs can be
dereferenced to result in a resource, such as a document. The rules
for dereferencing, or fetching, a URL are defined by the URL [scheme](https://url.spec.whatwg.org/#concept-url-scheme).
This specification does not use the term URI or IRI because those terms have
been deemed to be confusing to Web developers.
