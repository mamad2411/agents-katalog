---
name: "w3c-vcdm-ecosystem-graphs"
description: "Use when implementing ecosystem compatibility and VC graph features in W3C VCDM. Covers ecosystem compatibility, VC graphs, and securing specifications."
sections:
  - "5.11 Ecosystem Compatibility"
  - "5.12 Verifiable Credential Graphs"
  - "5.13 Securing Mechanism Specifications"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~3343 -->

### 5.11 Ecosystem Compatibility
        

        
There are a number of digital credential formats that do not natively use the
data model provided in this document, but are aligned with a number of concepts
in this specification. At the time of publication, examples of these digital
credential formats include
[JSON Web Tokens](https://www.rfc-editor.org/rfc/rfc7519.html) (JWTs),
[CBOR Web Tokens](https://www.rfc-editor.org/rfc/rfc8392.html) (CWTs),
[JSON Advanced Electronic Signature](https://www.etsi.org/deliver/etsi_ts/119100_119199/11918201/01.01.01_60/ts_11918201v010101p.pdf) (JAdES),
[ISO-18013-5:2021](https://www.iso.org/standard/69084.html)
(mDLs),
[AnonCreds](https://hyperledger.github.io/anoncreds-spec/),
[Gordian Envelopes](https://datatracker.ietf.org/doc/draft-mcnally-envelope/), and
[Authentic Chained Data Containers](https://datatracker.ietf.org/doc/draft-ssmith-acdc/) (ACDCs).
        

        
If conceptually aligned digital credential formats can be transformed into a
[conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) according to the rules provided in this section, they
are considered *"compatible with the W3C Verifiable Credentials
ecosystem"*. Specification authors are advised to adhere to the following
rules when documenting transformations that enable compatibility with the
Verifiable Credentials ecosystem. The transformation specification —
        

        
          - 
MUST identify whether the transformation to this data model is one-way-only or
round-trippable.
          
          - 
MUST preserve the `@context` values when performing round-trippable
transformation.
          
          - 
MUST result in a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) when transforming to the data
model described by this specification.
          
          - 
MUST specify a registered media type for the input document.
          
          - 
SHOULD provide a test suite that demonstrates that the specified transformation
algorithm to the data model in this specification results in
a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document).
          
          - 
SHOULD ensure that all semantics used in the transformed
[conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) follow best practices for Linked Data. See
Section [4.1 Getting Started](https://www.w3.org/TR/vc-data-model-2.0/#getting-started), Section
[5.2 Extensibility](https://www.w3.org/TR/vc-data-model-2.0/#extensibility), and Linked Data Best Practices [[LD-BP](https://www.w3.org/TR/vc-data-model-2.0/#bib-ld-bp)]
for additional guidance.
          
        

        Note: What constitutes a verifiable credential?
Readers are advised that a digital credential is only considered compatible with
the W3C Verifiable Credentials ecosystem if it is a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document)
and it uses at least one securing mechanism, as described by their
respective requirements in this specification. While some communities might call
some digital credential formats that are not [conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document)
"verifiable credentials", doing so does NOT make that digital credential
compliant to this specification.

---

### 5.12 Verifiable Credential Graphs
        

        
When expressing [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) (for example in a
[presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation)), it is important to ensure that data in one [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is not mistaken to be the same data in another [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). For example, if one has two [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), each
containing an object of the following form: `{"type": "Person", "name": "Jane
Doe"}`, it is not possible to tell if one object is describing the same person
as the other object. In other words, merging data between two [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) without confirming that they are discussing the same entities
and/or properties, can lead to a corrupted data set.
        

        
To ensure that data from different [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are not
accidentally co-mingled, the concept of a verifiable
credential graph is used to encapsulate each [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
For simple [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), that is, when the JSON-LD document
contains a single credential with, possibly, associated proofs, this graph is
the [default graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-default-graph). For [presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation), each value associated with
the `verifiableCredential` property of the [presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) is a separate
[named graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-named-graphs) of type VerifiableCredentialGraph
which contains a single [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or an
[enveloped verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#enveloped-verifiable-credentials).
        
        
Using these [graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-graphs) has a concrete effect when performing JSON-LD
processing, which properly separates graph node identifiers in one graph from
those in another graph. Implementers that limit their inputs to
application-specific JSON-LD documents will also need to keep this in mind if
they merge data from one [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) with data from another,
such as when the `credentialSubject.id` is the same in both [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), but the object might contain objects of the "Jane Doe" form
described in the previous paragraph. It is important to not merge objects that
seem to have similar properties but do not contain an `id` property that uses a
global identifier, such as a URL.

---

### 5.13 Securing Mechanism Specifications
        

        
As described in Section [4.12 Securing Mechanisms](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms), there are
multiple strategies that an implementer can use when securing a
[conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document). In order to maximize utility and interoperability,
specification authors that desire to author new ways of securing
[conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) are provided with the guidance in this section.
        

        
Securing mechanism specifications MUST document normative algorithms that
provide content integrity protection for [conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document). The
algorithms MAY be general in nature and MAY be used to secure data other than
[conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document).
        

        
Securing mechanism specifications MUST provide a verification algorithm that
returns the information in the [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) that has been secured, in
isolation, without including any securing mechanism information, such as `proof` or
JOSE/COSE header parameters and signatures. Verification algorithms MAY return
additional information that might be helpful (for example, during validation or
for debugging purposes), such as details of the securing mechanism. A verification
algorithm MUST provide an interface that receives a media type ([string](https://infra.spec.whatwg.org/#string)
inputMediaType) and input data ([byte sequence](https://infra.spec.whatwg.org/#byte-sequence) or [map](https://infra.spec.whatwg.org/#ordered-map) inputData).
Securing mechanism specifications MAY provide algorithms and interfaces in
addition to the ones specified in this document. The verification algorithm
returns a verification result with at least the following [items](https://infra.spec.whatwg.org/#struct-item):
        

        
          [boolean](https://infra.spec.whatwg.org/#boolean) verified
          
A verification status whose value is `true` if the verification succeeded and
`false` if it did not.
          
          [map](https://infra.spec.whatwg.org/#ordered-map) verifiedDocument
          
A document that only contains information that was successfully secured.
          
          [string](https://infra.spec.whatwg.org/#string) mediaType
          
A media type as defined in [[RFC6838](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc6838)].
          
        

        
Securing mechanism specifications SHOULD provide integrity protection for any
information referenced by a URL that is critical to validation. Mechanisms that
can achieve this protection are discussed in Section
[5.3 Integrity of Related Resources](https://www.w3.org/TR/vc-data-model-2.0/#integrity-of-related-resources) and Section
[B.1 Base Context](https://www.w3.org/TR/vc-data-model-2.0/#base-context).
        

        
A securing mechanism specification that creates a new type of [embedded proof](https://www.w3.org/TR/vc-data-model-2.0/#dfn-embedded-proof)
MUST specify a [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) that relates the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) to a [proof graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph).
The requirements on the securing mechanism are as follow:
        
        
          - 
The securing mechanism MUST define all terms used by the [proof graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph). For
example, the mechanism could define vocabulary specifications and `@context`
files in the same manner as they are used by this specification.
          
          - 
The securing mechanism MUST secure all graphs in the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
or the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), except for any [proof graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph) securing
the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) itself.
          

        

      Note
The last requirement means that the securing mechanism secures the [default graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-default-graph) and, for [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), each [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
of the presentation, together with their respective [proof graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-proof-graph).
See also [Figure 9](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vp) or [Figure 14](https://www.w3.org/TR/vc-data-model-2.0/#info-graph-vp-mult-creds).
      

      
The `proof` property as defined in [[VC-DATA-INTEGRITY](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-data-integrity)] MAY be used by the
embedded securing mechanism.
      

      
Securing mechanism specifications SHOULD register the securing mechanism in the
[Securing Mechanisms](https://w3c.github.io/vc-extensions/#securing-mechanisms)
section of the [Verifiable Credential Extensions](https://w3c.github.io/vc-extensions/) document.
        

        Note: Choice of securing mechanism is use-case dependent
There are multiple acceptable securing mechanisms, and this specification does
not mandate any particular securing mechanism for use with
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
The Working Group that produced this specification did standardize two
securing mechanism options, which are:
[Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/) [[VC-DATA-INTEGRITY](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-data-integrity)] and [Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/)
[[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)]. Other securing mechanisms that are known to the community
can be found in the
[Securing Mechanisms](https://w3c.github.io/vc-extensions/#securing-mechanisms)
section of the [Verifiable Credential Extensions](https://w3c.github.io/vc-extensions/) document.
