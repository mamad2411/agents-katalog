---
name: "w3c-vcdm-presentations"
description: "Use when implementing verifiable presentations in W3C VCDM. Covers: presentation structure, semantics, and processing considerations."
sections:
  - "4.13 Verifiable Presentations"
  - "Enveloped Verifiable Credentials"
  - "Enveloped Verifiable Presentations"
  - "Presentations Using Derived Credentials"
  - "Presentations Including Holder Claims"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~5537 -->

### 4.13 Verifiable Presentations
        

        
[Verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) MAY be used to aggregate information from
multiple [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        
        
[Verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) SHOULD be extremely short-lived and bound to a
challenge provided by a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). Details for accomplishing this depend
on the securing mechanism, the transport protocol, and [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) policies.
Unless additional requirements are defined by the particular securing mechanism
or embedding protocol, a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) cannot generally assume that the
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) correlates with the presented
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        

        
The [default graph](https://www.w3.org/TR/vc-data-model-2.0/#dfn-default-graph) of a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) is also referred to
as the verifiable presentation graph.
        


        
The following properties are defined for a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation):
        

        
          id
          
The `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is optional. It MAY be used to provide a
unique identifier for the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). If present, the
normative guidance in Section [4.4 Identifiers](https://www.w3.org/TR/vc-data-model-2.0/#identifiers) MUST be followed.
          
          type
          
The `type` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be present. It is used to express the
type of [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). One value of this property MUST be
`VerifiablePresentation`, but additional types MAY be included. The
related normative guidance in Section [4.5 Types](https://www.w3.org/TR/vc-data-model-2.0/#types) MUST be followed.
          
          verifiableCredential
          
The `verifiableCredential` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MAY be present. The value
MUST be one or more [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and/or
[enveloped verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#enveloped-verifiable-credentials)
objects (the values MUST NOT be non-object values such as
numbers, strings, or URLs). These objects are called
[verifiable credential graphs](https://www.w3.org/TR/vc-data-model-2.0/#verifiable-credential-graphs) and
MUST express information that is secured using a
[securing mechanism](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanisms).
See Section [5.12 Verifiable Credential Graphs](https://www.w3.org/TR/vc-data-model-2.0/#verifiable-credential-graphs) for further details.
          
          holder
          
The [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) MAY include a `holder`
[property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property). If present, the value MUST be either a [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) or an object
containing an `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property). It is RECOMMENDED that the
[URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url) in the `holder` or its `id` be one which, if
dereferenced, results in a document containing machine-readable information
about the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) that can be used to [verify](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) the information
expressed in the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
If the `holder` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is absent, information about the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) is obtained either via the securing mechanism or
does not pertain to the [validation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claim-validation) of the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
          
        

        
The example below shows a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation):
        

        
        
    [Example 17](https://www.w3.org/TR/vc-data-model-2.0/#example-basic-structure-of-a-presentation): Basic structure of a presentation
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "id": "urn:uuid:3978344f-8596-4c3a-a978-8fcaba3903c5",
  "type": ["VerifiablePresentation", "ExamplePresentation"],
  "verifiableCredential": [{ ... }]
}
```
      

        
The contents of the `verifiableCredential` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) shown
above are [verifiable credential
graphs](https://www.w3.org/TR/vc-data-model-2.0/#verifiable-credential-graphs), as described by this specification.
        

#### Enveloped Verifiable Credentials
          

          
It is possible for a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) to include one or more
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that have been secured using a securing mechanism
that "envelopes" the payload, such as [Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/) [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)].
This can be accomplished by associating the `verifiableCredential` property with
an object that has a `type` of `EnvelopedVerifiableCredential`.
          

          
            EnvelopedVerifiableCredential
            
They are used to associate an object containing an enveloped
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) with the `verifiableCredential` property in a
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). The `@context` property of the object MUST be
present and include a context, such as the [base context
for this specification](https://www.w3.org/TR/vc-data-model-2.0/#base-context), that defines at least the `id`, `type`, and
`EnvelopedVerifiableCredential` terms as defined by the base context provided
by this specification. The `id` value of the object MUST be a `data:` URL
[[RFC2397](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc2397)] that expresses a secured [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) using an
[enveloping](https://www.w3.org/TR/vc-data-model-2.0/#dfn-enveloping-proof) security scheme, such as
[Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/) [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)]. The `type` value of the object MUST be
`EnvelopedVerifiableCredential`.
            
          

          
The example below shows a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) that contains an
enveloped [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential):
          

          
        
    [Example 18](https://www.w3.org/TR/vc-data-model-2.0/#example-basic-structure-of-a-presentation-0): Basic structure of a presentation
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "type": ["VerifiablePresentation", "ExamplePresentation"],
  "verifiableCredential": [{
    "@context": "https://www.w3.org/ns/credentials/v2",
    "id": "data:application/vc+sd-jwt,QzVjV...RMjU",
    "type": "EnvelopedVerifiableCredential"
  }]
}
```
      

          Note: Processing enveloped content as RDF
It is possible that an implementer might want to process the object described in
this section and the enveloped presentation expressed by the `id` value in an
RDF environment and create linkages between the objects that are relevant to
RDF. The desire and mechanisms for doing so are use case dependent and will,
thus, be implementation dependent.
          

        

#### Enveloped Verifiable Presentations
          

          
It is possible to express a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) that has been secured
using a mechanism that "envelops" the payload, such as
[Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/) [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)]. This can be accomplished by using an
object that has a `type` of `EnvelopedVerifiablePresentation`.
          

          
            EnvelopedVerifiablePresentation
            
Used to express an enveloped [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
The `@context` property of the object MUST be present and include a context,
such as the [base context for this specification](https://www.w3.org/TR/vc-data-model-2.0/#base-context),
that defines at least the `id`, `type`, and `EnvelopedVerifiablePresentation`
terms as defined by the base context provided by this specification. The `id`
value of the object MUST be a `data:` URL [[RFC2397](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc2397)] that expresses a secured
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) using an
[enveloping](https://www.w3.org/TR/vc-data-model-2.0/#dfn-enveloping-proof) securing mechanism, such as
[Securing Verifiable Credentials using JOSE and COSE](https://www.w3.org/TR/vc-jose-cose/) [[VC-JOSE-COSE](https://www.w3.org/TR/vc-data-model-2.0/#bib-vc-jose-cose)]. The `type` value of the object MUST be
`EnvelopedVerifiablePresentation`.
            
          

          
The example below shows an enveloped [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation):
          

          
        
    [Example 19](https://www.w3.org/TR/vc-data-model-2.0/#example-basic-structure-of-an-enveloped-verifiable-presentation): Basic structure of an enveloped verifiable presentation
   ```
{
  "@context": "https://www.w3.org/ns/credentials/v2",
  "id": "data:application/vp+jwt,eyJraWQiO...zhwGfQ",
  "type": "EnvelopedVerifiablePresentation"
}
```
      

        

#### Presentations Using Derived Credentials
          

          
Some zero-knowledge cryptography schemes might enable [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to
indirectly prove they hold [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) from a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
without revealing all claims in that [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential). In these
schemes, a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) might be used to derive presentable
data, which is cryptographically asserted such that a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) can trust
the value if they trust the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers).
          
          
Some selective disclosure schemes can share a subset of [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims)
derived from a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
          

          Note: Presentations using Zero-Knowledge Proofs are possible
For an example of a ZKP-style [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) containing
derived data instead of directly embedded [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), see
Section [5.7 Zero-Knowledge Proofs](https://www.w3.org/TR/vc-data-model-2.0/#zero-knowledge-proofs).
          

          
            
            [Figure 11](https://www.w3.org/TR/vc-data-model-2.0/#fig-a-basic-claim-expressing-that-pat-is-over-the-age-of-21) 
A basic claim expressing that Pat is over the age of 21.
            
          
        
#### Presentations Including Holder Claims
          
          
A [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) MAY use the `verifiableCredential` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) in
a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) to include [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) from
any [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), including themselves. When the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) of a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders), the [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) in that
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are considered *self-asserted*.
Such self-asserted claims can be secured by the same mechanism that secures
the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) in which they are included or by any
mechanism usable for other [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
          
          
The [subject(s)](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) of these self-asserted [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims)
are not limited, so these [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) can include statements about the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders), one of the other included [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or even
the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) in which the self-asserted [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is included. In each case, the `id` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)
is used to identify the specific [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects), in the object where the
[claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) about it are made, just as it is done in
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that are not self-asserted.
          
          
A [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) that includes a self-asserted
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), which is secured only using the same mechanism as
the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), MUST include a `holder`
[property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property).
          
          
All of the normative requirements defined for [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
apply to self-asserted [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
          
          
A [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) in a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) is considered
self-asserted when the value of the `issuer` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) of the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is identical to the value of the `holder`
[property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) of the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
          
          
The example below shows a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) that embeds a
self-asserted [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that is secured using the same
mechanism as the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
          

          
        
    [Example 20](https://www.w3.org/TR/vc-data-model-2.0/#example-a-verifiable-presentation-secured-with-an-embedded-data-integrity-proof-with-a-self-asserted-verifiable-credential): A verifiable presentation, secured with an embedded Data Integrity proof, with a self-asserted verifiable credential
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "type": ["VerifiablePresentation", "ExamplePresentation"],
  "holder": "did:example:12345678",
  "verifiableCredential": [{
    "@context": [
      "https://www.w3.org/ns/credentials/v2",
      "https://www.w3.org/ns/credentials/examples/v2"
    ],
    "type": ["VerifiableCredential", "ExampleFoodPreferenceCredential"],
    "issuer": "did:example:12345678",
    "credentialSubject": {
      "favoriteCheese": "Gouda"
    },
    { ... }
  }],
  "proof": [{ ... }]
}
```
      
          
The example below shows a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) that embeds a
self-asserted [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) holding [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) about the
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). It is secured using the same mechanism as the
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
          

          
        
    [Example 21](https://www.w3.org/TR/vc-data-model-2.0/#example-a-verifiable-presentation-secured-with-an-embedded-data-integrity-proof-with-a-self-asserted-verifiable-credential-about-the-verifiable-presentation): A verifiable presentation, secured with an embedded Data Integrity proof, with a self-asserted verifiable credential about the verifiable presentation
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2"
  ],
  "type": ["VerifiablePresentation", "ExamplePresentation"],
  "id": "urn:uuid:313801ba-24b7-11ee-be02-ff560265cf9b",
  "holder": "did:example:12345678",
  "verifiableCredential": [{
    "@context": [
      "https://www.w3.org/ns/credentials/v2",
      "https://www.w3.org/ns/credentials/examples/v2"
    ],
    "type": ["VerifiableCredential", "ExampleAssertCredential"],
    "issuer": "did:example:12345678",
    "credentialSubject": {
      "id": "urn:uuid:313801ba-24b7-11ee-be02-ff560265cf9b",
      "assertion": "This VP is submitted by the subject as evidence of a legal right to drive"
    },
    "proof": { ... }
  }],
  "proof": { ... }
}
```
