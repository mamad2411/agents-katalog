---
name: "w3c-vcdm-intro"
description: "Use when understanding W3C Verifiable Credentials Data Model 2.0 introduction. Covers: document overview, what is a verifiable credential, ecosystem overview, and conformance requirements."
sections:
  - "1. Introduction*This section is non-normative.*"
  - "1.1 What is a Verifiable Credential?*This section is non-normative.*"
  - "1.2 Ecosystem Overview*This section is non-normative.*"
  - "1.3 ConformanceAs well as sections marked as non-normative, all authoring guidelines, diagrams, examples, and notes in this specification are non-normative. Everything else in this specification is normative."
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~4958 -->

## 1. Introduction*This section is non-normative.*
      

      
[Credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) are integral to our daily lives: driver's licenses confirm
our capability to operate motor vehicles; university degrees assert our level
of education; and government-issued passports attest to our citizenship when
traveling between countries. This specification provides a mechanism for
expressing these sorts of [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) on the Web in a way that is
cryptographically secure, privacy respecting, and machine verifiable. These
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) provide benefits to us when used in the physical world, but
their use on the Web continues to be elusive.
      

      
It is currently difficult to express educational qualifications, healthcare
data, financial account details, and other third-party-[verified](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify)
personal information in a machine readable way on the Web. The challenge of
expressing digital [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) on the Web hinders our ability to receive
the same benefits from them that physical [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) provide in the
real world.
      
      
For those unfamiliar with the concepts related to
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), the following sections provide an overview of:
      

      
        - 
The components that constitute a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
        
        - 
The components that constitute a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation)
        
        - 
An ecosystem where [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) are useful
        
      
      
The use cases and requirements that informed this specification can be found
in [Verifiable Credentials Use Cases](https://www.w3.org/TR/vc-use-cases/) [[VC-USE-CASES](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-use-cases)].
      

### 1.1 What is a Verifiable Credential?*This section is non-normative.*
        

        
In the physical world, a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) might consist of:
        

        
          - 
Information related to identifying the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
(for example, a photo, name, or identification number)
          
          - 
Information related to the issuing authority (for example, a city government,
national agency, or certification body)
          
          - 
Information related to the type of [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) (for example, a
Dutch passport, an American driving license, or a health insurance card)
          
          - 
Information related to specific properties asserted by
the issuing authority about the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) (for example, nationality,
date of birth, or the classes of vehicle they're qualified to drive)
          
          - 
Evidence by which a [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) was demonstrated to have satisfied the
qualifications required for issuance of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) (for example,
a measurement, proof of citizenship, or test result)
          
          - 
Information related to constraints on the credential (for example,
validity period, or terms of use).
          
        

        
A [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can represent all the same information that a
physical [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) represents. Adding technologies such as
digital signatures can make [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) more tamper-evident and
trustworthy than their physical counterparts.
        

        
[Holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can generate
[verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) and then share these
[verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) with [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to prove they possess
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) with specific characteristics.
        

        
Both [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) can be
transmitted rapidly, making them more convenient than their physical
counterparts when establishing trust at a distance.
        

        
While this specification attempts to improve the ease of expressing digital
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), it also aims to balance this goal with several
privacy-preserving goals. The persistence of digital information, and the ease
with which disparate sources of digital data can be collected and correlated,
comprise a privacy concern that the use of [verifiable](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) and easily
machine-readable [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) threatens to make worse. This document
outlines and attempts to address several of these issues in Section
[8. Privacy Considerations](https://www.w3.org/TR/vc-data-model-2.0/#privacy-considerations). Examples of how to use this data model
using privacy-enhancing technologies, such as zero-knowledge proofs, are also
provided throughout this document.
        

        
The word "verifiable" in the terms [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) refers to the characteristic of a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
or [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) as being able to be [verified](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) by a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier),
as defined in this document. Verifiability of a credential does not imply
the truth of [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) encoded therein. Instead, upon establishing the
authenticity and currency of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) validates the included [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) using
their own business rules before relying on them. Such reliance only occurs after
evaluating the issuer, the proof, the subject, and the claims against one or
more verifier policies.
        
      

### 1.2 Ecosystem Overview*This section is non-normative.*
        

        
This section describes the roles of the core actors and the relationships
between them in an ecosystem where one expects [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
to be useful. A role is an abstraction that might be implemented in many
different ways. The separation of roles suggests likely interfaces and
protocols for standardization. This specification introduces the following
roles:
        

        
          [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
          
A role an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) might perform by possessing one or more [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and generating [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) from them. A holder is
often, but not always, a [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) of the [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) they are
holding. Holders store their [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) in [credential repositories](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential-repositories).
Example holders include students, employees, and customers.
          
          [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers)
          
A role an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) can perform by asserting [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) about one or more
[subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects), creating a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) from these [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims), and
transmitting the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders). For example, issuers
include corporations, non-profit organizations, trade associations, governments,
and individuals.
          
          [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)
          
A thing about which [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) are made. Example subjects include human beings,
animals, and things.
          
          [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
          
A role an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) performs by receiving one or more [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), optionally inside a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) for processing.
Example verifiers include employers, security personnel, and websites.
          
          [verifiable data registry](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-data-registries)
          
A role a system might perform by mediating the creation and [verification](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) of
identifiers, [verification material](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verification-material), and other relevant data, such as
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) schemas, revocation registries, and so on, which might
require using [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). Some configurations might require
correlatable identifiers for [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects). Some registries, such as ones for
UUIDs and [verification material](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verification-material), might just act as namespaces for
identifiers. Examples of verifiable data registries include trusted databases,
decentralized databases, government ID databases, and distributed ledgers. Often,
more than one type of verifiable data registry used in an ecosystem.
          
        

        
          
          [Figure 1](https://www.w3.org/TR/vc-data-model-2.0/#roles) 
            The roles and information flows forming the basis for this
            specification.
          
        

        Note: Other types of ecosystems exist
[Figure 1](https://www.w3.org/TR/vc-data-model-2.0/#roles) above provides an example ecosystem to ground the
rest of the concepts in this specification. Other ecosystems exist, such as
protected environments or proprietary systems, where
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) also provide benefits.
        

        
This ecosystem contrasts with the typical two-party or federated identity
provider models. An identity provider, sometimes abbreviated as *IdP*,
is a system for creating, maintaining, and managing identity information for
[holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) while providing authentication services to [relying party](https://www.w3.org/TR/vc-data-model-2.0/#dfn-relying-parties)
applications within a federation or distributed network. In a federated
identity model, the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) is tightly bound to the identity provider.
This specification avoids using "identity provider," "federated identity," or
"relying party" terminology, except when comparing or mapping these concepts
to other specifications. This specification decouples the identity provider
concept into two distinct concepts: the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
        

        Note: Subjects are not always Holders
In many cases, the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is the subject, but
in some instances it is not. For example, a parent (the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)) might hold
the [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) of a child (the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)), or a pet owner (the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)) might hold the [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) of their pet (the
[subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)). For more information about these exceptional cases, see the
[Subject-Holder Relationships](https://w3c.github.io/vc-imp-guide/#subject-holder-relationships) section in the [Verifiable Credentials Implementation Guidelines 1.0](https://www.w3.org/TR/vc-imp-guide/).
        

        
For a deeper exploration of the [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) ecosystem and
a concrete lifecycle example, please refer to [Verifiable Credentials Overview](https://www.w3.org/TR/vc-overview/) [[VC-OVERVIEW](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-overview)].
        
      

### 1.3 ConformanceAs well as sections marked as non-normative, all authoring guidelines, diagrams, examples, and notes in this specification are non-normative. Everything else in this specification is normative.
        The key words MAY, MUST, MUST NOT, OPTIONAL, RECOMMENDED, REQUIRED, SHOULD, and SHOULD NOT in this document
        are to be interpreted as described in
        [BCP 14](https://www.rfc-editor.org/info/bcp14)
        [[RFC2119](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc2119)] [[RFC8174](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc8174)]
        when, and only when, they appear in all
        capitals, as shown here.
      
        
A conforming document is a
[compacted](https://www.w3.org/TR/json-ld11-api/#compaction-algorithms) JSON-LD
document that complies with all of the relevant "MUST" statements in this
specification. Specifically, the relevant normative "MUST" statements in
Sections [4. Basic Concepts](https://www.w3.org/TR/vc-data-model-2.0/#basic-concepts), [5. Advanced Concepts](https://www.w3.org/TR/vc-data-model-2.0/#advanced-concepts), and
[6. Syntaxes](https://www.w3.org/TR/vc-data-model-2.0/#syntaxes) of this document MUST be enforced.
A conforming document MUST be either a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
with a media type of `application/vc` or a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation)
with a media type of `application/vp`. A conforming document MUST be
secured by at least one securing mechanism as described in Section
[4.12 Securing Mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms).
        

        
A conforming issuer implementation produces
[conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document), MUST include all required properties in the
[conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) it produces, and MUST secure the [conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) it produces using a securing mechanism described in Section
[4.12 Securing Mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms).
        

        
A conforming verifier implementation
consumes [conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document), MUST perform [verification](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) on a
[conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) as described in Section
[4.12 Securing Mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms), MUST check that each
required property satisfies the normative requirements for that property, and
MUST produce errors when non-[conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) are detected.
        

        
This specification includes both required and optional properties. Optional
properties MAY be ignored by [conforming issuer implementations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-issuer-implementation) and
[conforming verifier implementations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-verifier-implementation).
        

        
This document also contains examples that contain characters that are invalid
JSON, such as inline comments (`//`) and the use of ellipsis
(`...`) to denote information that adds little value to the example.
Implementers are cautioned to remove this content if they desire to use the
information as a valid document.
        

        Note: Human-readable texts in English are illustrative
Examples provided throughout this document include descriptive properties, such as
`name` and `description`, with values in English to simplify the concepts in each
example of the specification. These examples do not necessarily reflect the data
structures needed for international use, described in more detail in
Section [11. Internationalization Considerations](https://www.w3.org/TR/vc-data-model-2.0/#internationalization-considerations).
