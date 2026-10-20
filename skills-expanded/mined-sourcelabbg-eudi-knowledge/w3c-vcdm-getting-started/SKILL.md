---
name: "w3c-vcdm-getting-started"
description: "Use when getting started with the W3C VCDM core model. Covers: getting started, verifiable credentials, and contexts."
sections:
  - "4.1 Getting Started*This section is non-normative.*"
  - "4.2 Verifiable Credentials"
  - "4.3 Contexts"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~2693 -->

### 4.1 Getting Started*This section is non-normative.*
        

        
This specification is designed to ease the prototyping of new types of
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). Developers can copy the template below and paste it
into common [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) tooling to start issuing, holding, and
verifying prototype credentials.
        

        
A developer will change `MyPrototypeCredential` below to the type of credential
they would like to create. Since [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) talk about subjects,
each property-value pair in the `credentialSubject` object expresses a
particular property of the credential subject. Once a developer has added a
number of these property-value combinations, the modified object can be sent to
a [conforming issuer implementation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-issuer-implementation), and a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) will be
created for the developer. From a prototyping standpoint, that is all a
developer needs to do.
        

        
        
    [Example 1](https://www.w3.org/TR/vc-data-model-2.0/#example-a-template-for-creating-prototype-verifiable-credentials): A template for creating prototype verifiable credentials
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "type": ["VerifiableCredential", "MyPrototypeCredential"],
  "credentialSubject": {
    "mySubjectProperty": "mySubjectValue"
  }
}
```
      

        
After stabilizing all credential properties, developers are advised to generate
and publish vocabulary and context files at stable URLs to facilitate
interoperability with other developers. The
`https://www.w3.org/ns/credentials/examples/v2` URL above
would then be replaced with the URL of a use-case-specific context. This
process is covered in Section [5.2 Extensibility](https://www.w3.org/TR/vc-data-model-2.0/#extensibility). Alternatively,
developers can reuse existing vocabulary and context files that happen to fit
their use case. They can explore the [Verifiable Credential Extensions](https://w3c.github.io/vc-extensions/)
for reusable resources.

---

### 4.2 Verifiable Credentials
        

        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are used to express properties of one or more
[subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) as well as properties of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) itself. The following
properties are defined in this specification for a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential):
        

        
          @context
          
Defined in Section [4.3 Contexts](https://www.w3.org/TR/vc-data-model-2.0/#contexts).
          
          id
          
Defined in Section [4.4 Identifiers](https://www.w3.org/TR/vc-data-model-2.0/#identifiers).
          
          type
          
Defined in Section [4.5 Types](https://www.w3.org/TR/vc-data-model-2.0/#types).
          
          name
          
Defined in Section [4.6 Names and Descriptions](https://www.w3.org/TR/vc-data-model-2.0/#names-and-descriptions).
          
          description
          
Defined in Section [4.6 Names and Descriptions](https://www.w3.org/TR/vc-data-model-2.0/#names-and-descriptions).
          
          issuer
          
Defined in Section [4.7 Issuer](https://www.w3.org/TR/vc-data-model-2.0/#issuer).
          
          credentialSubject
          
Defined in Section [4.8 Credential Subject](https://www.w3.org/TR/vc-data-model-2.0/#credential-subject).
          
          validFrom
          
Defined in Section [4.9 Validity Period](https://www.w3.org/TR/vc-data-model-2.0/#validity-period).
          
          validUntil
          
Defined in Section [4.9 Validity Period](https://www.w3.org/TR/vc-data-model-2.0/#validity-period).
          
          status
          
Defined in Section [4.10 Status](https://www.w3.org/TR/vc-data-model-2.0/#status).
          
          credentialSchema
          
Defined in Section [4.11 Data Schemas](https://www.w3.org/TR/vc-data-model-2.0/#data-schemas).
          
          refreshService
          
Defined in Section [5.4 Refreshing](https://www.w3.org/TR/vc-data-model-2.0/#refreshing).
          
          termsOfUse
          
Defined in Section [5.5 Terms of Use](https://www.w3.org/TR/vc-data-model-2.0/#terms-of-use).
          
          evidence
          
Defined in Section [5.6 Evidence](https://www.w3.org/TR/vc-data-model-2.0/#evidence).
          
        

        
A [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) can be extended to have additional properties
through the extension mechanism defined in Section [5.2 Extensibility](https://www.w3.org/TR/vc-data-model-2.0/#extensibility).

---

### 4.3 Contexts
        

        
When two software systems need to exchange data, they need to use terminology
that both systems understand. Consider how two people communicate effectively
by using the same language, where the words they use, such as "name" and
"website," mean the same thing to each individual. This is sometimes referred
to as *the context of a conversation*. This specification uses a similar
concept to achieve similar results for software systems by establishing a
context in which to communicate.
        
        
Software systems that process [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) identify terminology by using [URLs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) for each term. However,
those [URLs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) can be long and not very human-friendly, while short-form,
human-friendly aliases can be more helpful. This specification uses the
`@context` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) to map short-form aliases to the [URLs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url).
        
        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) MUST include a
`@context` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property). Application developers MUST understand every JSON-LD
context used by their application, at least to the extent that it affects the
meaning of the terms used by their application. One mechanism for
doing so is described in the Section on
[Validating Contexts](https://www.w3.org/TR/vc-data-integrity/#validating-contexts) in
the [Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/) specification. Other specifications that build
upon this specification MAY require that JSON-LD contexts be integrity protected
by using the `relatedResource` feature described in Section
[5.3 Integrity of Related Resources](https://www.w3.org/TR/vc-data-model-2.0/#integrity-of-related-resources) or any effectively equivalent mechanism.
        

        
          @context
          
The value of the `@context` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be an [ordered set](https://infra.spec.whatwg.org/#ordered-set)
where the first item is a [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) with the value
`https://www.w3.org/ns/credentials/v2`.
Subsequent items in the [ordered set](https://infra.spec.whatwg.org/#ordered-set) MUST be composed of any combination of
[URLs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) and objects, where each is processable as a
[JSON-LD Context](https://www.w3.org/TR/json-ld11/#the-context).
          
        

        
        
    [Example 2](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-context-property): Use of the @context property
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "http://university.example/credentials/58473",
  "type": ["VerifiableCredential", "ExampleAlumniCredential"],
  "issuer": "did:example:2g55q912ec3476eba2l9812ecbfe",
  "validFrom": "2010-01-01T00:00:00Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "alumniOf": {
      "id": "did:example:c276e12ec21ebfeb1f712ebc6f1",
      "name": "Example University"
    }
  }
}
```
      

        
The example above uses the base context [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url)
(`https://www.w3.org/ns/credentials/v2`) to establish that the data exchange is
about a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). This concept is further detailed in
Section [5.2 Extensibility](https://www.w3.org/TR/vc-data-model-2.0/#extensibility). The data available at
`https://www.w3.org/ns/credentials/v2` is a permanently cacheable static
document with instructions for processing it provided in Appendix
[B.1 Base Context](https://www.w3.org/TR/vc-data-model-2.0/#base-context). The associated human-readable vocabulary document for the
Verifiable Credentials Data Model is available at
[https://www.w3.org/2018/credentials/](https://www.w3.org/2018/credentials/).
        

        
The second [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) (`https://www.w3.org/ns/credentials/examples/v2`) is used to
demonstrate examples. Implementations are expected to not use
this [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) for any other purpose, such as in pilot or production systems.
        

        Note: See JSON-LD for more information about @context.
The `@context` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is further elaborated upon in
[Section 3.1: The Context](https://www.w3.org/TR/json-ld11/#the-context)
of the [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) specification.
