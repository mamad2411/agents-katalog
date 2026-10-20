---
name: "w3c-vcdm-data-model-concepts"
description: "Use when understanding W3C VCDM core data model concepts. Covers: claims, credentials, and presentations."
sections:
  - "3. Core Data Model*This section is non-normative.*"
  - "3.1 Claims*This section is non-normative.*"
  - "3.2 Credentials*This section is non-normative.*"
  - "3.3 Presentations*This section is non-normative.*"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5915 -->

## 3. Core Data Model*This section is non-normative.*
      

      
The following sections outline core data model concepts, such as [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims),
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), [presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation), [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), and
[verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), which form the foundation of this
specification.
      

      Note: The difference between a credential and a verifiable credential
Readers might note that some concepts described in this section, such as
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) and [presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation), do not have media types defined by
this specification. However, the concepts of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or a
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) are defined as [conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) and
have associated media types. The concrete difference between these concepts
— between [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) and [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) vs. [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) — is simply the fact
that the "verifiable" objects are secured in a cryptographic
way, and the others are not. For more details, see Section
[4.12 Securing Mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms).
      

### 3.1 Claims*This section is non-normative.*
        

        
A [claim](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) is a statement about a [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects). A [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) is a
thing about which [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) can be made. [Claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) are expressed using
***subject***-
property-value relationships.
        

        
          
          [Figure 2](https://www.w3.org/TR/vc-data-model-2.0/#basic-structure) 
The basic structure of a claim.
          
        

        
The data model for [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims), illustrated in [Figure 2](https://www.w3.org/TR/vc-data-model-2.0/#basic-structure)
above, is powerful and can be used to express a large variety of statements. For
example, whether someone graduated from a particular university can be expressed
as shown in [Figure 3](https://www.w3.org/TR/vc-data-model-2.0/#basic-example) below.
        

        
          
          [Figure 3](https://www.w3.org/TR/vc-data-model-2.0/#basic-example) 
A basic claim expressing that Pat is an alum of "Example University".
          
        

        
Individual [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) can be merged together to express a [graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs) of
information about a [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects). The example shown in
[Figure 4](https://www.w3.org/TR/vc-data-model-2.0/#multiple-claims) below extends the previous [claim](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) by
adding the [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) that Pat knows Sam and that Sam is employed as a
professor.
        

        
          
          [Figure 4](https://www.w3.org/TR/vc-data-model-2.0/#multiple-claims) 
Multiple claims can be combined to express a graph of information.
          
        

        
To this point, the concepts of a [claim](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) and a [graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs) of information
are introduced. More information is expected to be added to the graph in order
to be able to trust [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims), more information is
expected to be added to the graph.
        
      

### 3.2 Credentials*This section is non-normative.*
        

        
A [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) is a set of one or more [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) made by the same [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities).
[Credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) might also include an identifier and metadata to describe
properties of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), such as the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), the validity date and
time period, a representative image, [verification material](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verification-material), status
information, and so on. A
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is a set of tamper-evident [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) and metadata
that cryptographically prove who issued it. Examples of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) include, but are not limited to, digital employee identification
cards, digital driver's licenses, and digital educational certificates.
        

        
          
          [Figure 5](https://www.w3.org/TR/vc-data-model-2.0/#basic-vc) 
Basic components of a verifiable credential.
          
        

        
[Figure 5](https://www.w3.org/TR/vc-data-model-2.0/#basic-vc) above shows the basic components of a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), but abstracts the details about how [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims)
are organized into information [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs), which are then organized into
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).

        
[Figure 6](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vc) below shows a more complete depiction of a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) using an [embedded proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-embedded-proof) based on
[Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/). It is composed of at least two information [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs).
The first of these information [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs), the [verifiable credential graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential-graph)
(the [default graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-default-graph)), expresses the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
itself through [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) metadata and other [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims). The second
information [graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs), referred to by the `proof` property, is the
proof graph of the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and is a separate
[named graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-named-graphs). The [proof graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph) expresses the digital proof, which, in this
case, is a digital signature. Readers who are interested in the need for
multiple information graphs can refer to Section
[5.12 Verifiable Credential Graphs](https://www.w3.org/TR/vc-data-model-2.0/#verifiable-credential-graphs).
        

        
        
          [Figure 6](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vc) 
Information graphs associated with a basic verifiable credential, using an [embedded proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-embedded-proof)
based on [Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/) [[VC-DATA-INTEGRITY](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-data-integrity)].
          
        

        
[Figure 7](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vc-jwt) below shows the same [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
as [Figure 6](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vc), but secured using JOSE [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)]. The
payload contains a single information graph, which is the [verifiable credential graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential-graph) containing [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) metadata and other [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims).
        

        
          
          [Figure 7](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vc-jwt) 
            Information graphs associated with a basic verifiable credential,
            using an [enveloping proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-enveloping-proof) based on [Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/)
            [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)].
          
        

      

### 3.3 Presentations*This section is non-normative.*
        

        
Enhancing privacy is a key design feature of this specification. Therefore, it
is crucial for [entities](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) using this technology to express only
the portions of their personas that are appropriate for given situations. The
expression of a subset of one's persona is called a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
Examples of different personas include a person's professional persona,
online gaming persona, family persona, or incognito persona.
        

        
A [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) is created by a
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders), can express data from multiple [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), and can
contain arbitrary additional data. They are used to present [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) to a
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). It is also possible to present [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
directly.
        

        
The data in a [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) is often about the same [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) but might
have been issued by multiple [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers). The aggregation of this information
expresses an aspect of a person, organization, or [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities).
        

        
          
          [Figure 8](https://www.w3.org/TR/vc-data-model-2.0/#basic-vp) 
Basic components of a verifiable presentation.
          
        

        
[Figure 8](https://www.w3.org/TR/vc-data-model-2.0/#basic-vp) above shows the components of a
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) but abstracts the details about how
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are organized into information [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs),
which are then organized into [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
        
        
[Figure 9](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vp) below shows a more complete depiction of a
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) using an [embedded proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-embedded-proof)
based on [Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/).
It is composed of at least four information [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs).
The first of these information [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs), the [verifiable presentation graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation-graph)
(the [default graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-default-graph)), expresses the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation)
itself through [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) metadata.
The [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) refers, via the `verifiableCredential` property,
to a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
This [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) is a self-contained [verifiable credential graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential-graph)
containing [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) metadata and other [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims). This [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential)
refers to a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) [proof graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph) via a `proof` property,
expressing the proof (usually a digital signature) of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential).
This [verifiable credential graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential-graph) and its linked [proof graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph) constitute
the second and third information [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs), respectively, and each is a
separate [named graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-named-graphs). The [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) also refers, via the `proof`
property, to the [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation)'s [proof graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph), the fourth information
[graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs) (another [named graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-named-graphs)). This [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) [proof graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph)
represents the digital signature of the [verifiable presentation graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation-graph),
the [verifiable credential graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential-graph), and the [proof graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph) linked from the
[verifiable credential graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential-graph).
        

        
        
          [Figure 9](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vp) 
Information [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs) associated with a basic [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) that
uses an [embedded proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-embedded-proof) based on [Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/).
          
        

        
[Figure 10](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vp-jwt) below shows the same [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) as [Figure 9](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vp), but using an [enveloping proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-enveloping-proof) based on [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)]. The payload contains only two information
graphs: the [verifiable presentation graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation-graph) expressing the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) through presentation metadata and the corresponding
[verifiable credential graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential-graph), referred to by the `verifiableCredential`
property. The [verifiable credential graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential-graph) contains a single
[EnvelopedVerifiableCredential](https://www.w3.org/TR/vc-data-model-2.0/#defn-EnvelopedVerifiableCredential)
instance referring, via a `data:` URL [[RFC2397](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc2397)], to the verifiable credential
secured via an [enveloping proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-enveloping-proof) shown in [Figure 7](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vc-jwt).
        

        
          
          [Figure 10](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vp-jwt) 
Information graphs associated with a basic [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) that is
using an [enveloping proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-enveloping-proof) based on [Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/). The `data:` URL
refers to the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) shown in
[Figure 7](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vc-jwt).
          
        


        Note: Presentations can contain multiple verifiable credentials
It is possible to have a [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation), such as a collection of university
credentials, which draws on multiple [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) about different [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)
that are often, but not required to be, related. This is achieved by using the
`verifiableCredential` property to refer to multiple [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
See Appendix [D. Additional Diagrams for Verifiable Presentations](https://www.w3.org/TR/vc-data-model-2.0/#additional-diagrams-for-verifiable-presentations) for more
details.
        

        Note: Presentations can be presented by issuers and verifiers
As described in Section [1.2 Ecosystem Overview](https://www.w3.org/TR/vc-data-model-2.0/#ecosystem-overview), an [entity](https://www.w3.org/TR/vc-data-model-2.0/#dfn-entities) can take
on one or more roles as they enter a particular credential exchange.
While a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) is typically expected to generate [presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation), an
[issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) or [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might generate a presentation to identify itself
to a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders). This might occur if the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) needs higher assurance
from the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) or [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) before handing over sensitive information
as part of a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
