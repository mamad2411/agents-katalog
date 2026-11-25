---
name: "w3c-vcdm-syntaxes-algorithms"
description: "Use when implementing W3C VCDM syntax handling and algorithms. Covers: JSON-LD, media types, type-specific processing, verification procedures, and problem details."
sections:
  - "6. Syntaxes"
  - "6.1 JSON-LD"
  - "6.2 Media Types"
  - "6.3 Type-Specific Credential Processing*This section is non-normative.*"
  - "7. Algorithms"
  - "7.1 Verification"
  - "7.2 Problem Details"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~7857 -->

## 6. Syntaxes
      

      
The data model as described in Sections [3. Core Data Model](https://www.w3.org/TR/vc-data-model-2.0/#core-data-model),
[4. Basic Concepts](https://www.w3.org/TR/vc-data-model-2.0/#basic-concepts), and [5. Advanced Concepts](https://www.w3.org/TR/vc-data-model-2.0/#advanced-concepts) is the canonical structural
representation of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
All syntaxes are representations of that data model in a specific format. This
section specifies how the data model is serialized in JSON-LD for
`application/vc` and `application/vp`, the base media types for [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), respectively. Although syntactic
mappings are only provided for JSON-LD, applications and services can use any
other data representation syntax (such as XML, YAML, or CBOR) that is capable of
being mapped back to `application/vc` or `application/vp`. As the
[verification](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify) and [validation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claim-validation) requirements are defined in terms of the
data model, all serialization syntaxes have to be deterministically translated
to the data model for processing, [validation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claim-validation), or comparison.
      

      
The expected arity of the property values in this specification, and the
resulting datatype which holds those values, can vary depending on the property.
If present, the following properties are represented as a single value: `id`
(Section [4.4 Identifiers](https://www.w3.org/TR/vc-data-model-2.0/#identifiers)), `issuer` (Section [4.7 Issuer](https://www.w3.org/TR/vc-data-model-2.0/#issuer)), and
`validFrom`/`validUntil` (Section [4.9 Validity Period](https://www.w3.org/TR/vc-data-model-2.0/#validity-period)). All other properties,
if present, are represented as either a single value or an array of values.
      

### 6.1 JSON-LD
        

        
This specification uses [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) to serialize the data model described in
this specification. JSON-LD is useful because it enables the expression of the
[graph-based data model](https://www.w3.org/TR/vc-data-model-2.0/#core-data-model) on which [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are based,
[machine-readable
semantics](https://en.wikipedia.org/wiki/Semantic_technology), and is also useful when extending the data model (see Sections
[3. Core Data Model](https://www.w3.org/TR/vc-data-model-2.0/#core-data-model) and [5.2 Extensibility](https://www.w3.org/TR/vc-data-model-2.0/#extensibility)).
        

        
JSON-LD is a JSON-based format used to serialize
[Linked Data](https://www.w3.org/TR/ld-glossary/#linked-data). Linked
Data is modeled using Resource Description Framework (RDF) [[RDF11-CONCEPTS](https://www.w3.org/TR/vc-data-model-2.0/#bib-rdf11-concepts)].
RDF is a technology for modeling graphs of statements. Each statement is a
single subject→property→value (also known as
entity→attribute→value) relationship, which is referred to as a
[claim](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) in this specification. JSON-LD is a technology that enables the
expression of RDF using idiomatic JSON, enabling developers familiar with JSON
to write applications that consume RDF as JSON. See
[Relationship of JSON-LD to RDF](https://www.w3.org/TR/json-ld11/#relationship-to-rdf)
for more details.
        

#### Notable JSON-LD Features
          

          
In general, the data model and syntax described in this document enables
developers to largely treat [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) as JSON documents,
allowing them to copy and paste examples, with minor modification, into their
software systems. The design goal of this approach is to provide a low barrier
to entry while still ensuring global interoperability between a heterogeneous
set of software systems. This section describes some of the JSON-LD features
that are used to make this possible, which will likely go unnoticed by most
developers, but whose details might be of interest to implementers. The most
noteworthy features in [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) used by this specification include:
          

          
            - 
The `@id` and `@type` keywords are aliased to
`id` and `type` respectively, enabling developers to use
this specification as idiomatic JSON.
            
            - 
Data types, such as integers, dates, units of measure, and URLs, are
automatically typed to provide stronger type guarantees for use cases that
require them.
            
            - 
The `verifiableCredential` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property)
is defined as a
[JSON-LD 1.1 graph
container](https://www.w3.org/TR/json-ld11/#graph-containers). This requires the creation of [named graphs](https://www.w3.org/TR/vc-data-model-2.0/#dfn-named-graphs), used to isolate
sets of data asserted by different entities. This ensures, for example, proper
cryptographic separation between the data graph provided by each [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers)
and the one provided by the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) presenting the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to ensure the provenance of the information for each graph is
preserved.
            
            - 
The `@protected` properties feature of [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) is used to ensure that
terms defined by this specification cannot be overridden. This means that as
long as the same `@context` declaration is made at the top of a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), interoperability is guaranteed for
all terms understood by users of the data model whether or not they use a
[JSON-LD 1.1](https://www.w3.org/TR/json-ld11/) processor.
            
          
        

#### Restrictions on JSON-LD
          

          
In order to increase interoperability, this specification restricts the use of
JSON-LD representations of the data model. JSON-LD [compacted document
form](https://www.w3.org/TR/json-ld/#compacted-document-form) MUST be used for all representations of the data model using the
`application/vc` or `application/vp` media type.
          

          
As elaborated upon in Section
[6.3 Type-Specific Credential Processing](https://www.w3.org/TR/vc-data-model-2.0/#type-specific-credential-processing), some software applications
might not perform generalized JSON-LD processing. Authors of [conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) are advised that interoperability might be reduced if JSON-LD
keywords in the `@context` value are used to globally affect values in a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation), such as by
setting either or both of the `@base` or `@vocab` keywords. For example, setting
these values might trigger a failure in a mis-implemented JSON Schema test of
the `@context` value in an implementation that is performing [type-specific credential processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type-specific-credential-processing) and not expecting the `@base` and/or `@vocab` value to
be expressed in the `@context` value.
          

          
In order to increase interoperability, [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) authors are
urged to not use JSON-LD features that are not easily detected when performing
[type-specific credential processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type-specific-credential-processing). These features include:
          

          
            - 
In-line declaration of JSON-LD keywords in the `@context` value that globally
modify document term and value processing, such as setting `@base` or `@vocab`
            
            - 
Use of JSON-LD contexts that override declarations in previous contexts, such as
resetting `@vocab`
            
            - 
In-line declaration of JSON-LD contexts in the `@context` property
            
            - 
Use of full URLs for JSON-LD terms and types (for example,
`https://www.w3.org/2018/credentials#VerifiableCredential` or
`https://vocab.example/myvocab#SomeNewType`) instead of the short forms of
any such values (for example, `VerifiableCredential` or `SomeNewType`) that are
explicitly defined in JSON-LD `@context` mappings (for example, in
`https://www.w3.org/ns/credentials/v2`)
            
          

          
While this specification cautions against the use of `@vocab`, there are
legitimate uses of the feature, such as to ease experimentation, development,
and localized deployment. If an application developer wants to use `@vocab` in
production, which is advised against to reduce term collisions and leverage the
benefits of semantic interoperability, they are urged to understand that any use
of `@vocab` will disable reporting of "undefined term" errors, and
later use(s) will override any previous `@vocab` declaration(s). Different values
of `@vocab` can change the semantics of the information contained in the document,
so it is important to understand whether and how these changes will affect the
application being developed.
          

        

#### Lists and Arrays
          
          
Lists, arrays, and even lists of lists, are possible when using [JSON-LD 1.1](https://www.w3.org/TR/json-ld11/).
We encourage those who want RDF semantics in use cases requiring lists and
arrays to follow the guidance on
[lists in JSON-LD 1.1](https://www.w3.org/TR/json-ld11/#lists).
          
          
In general, a JSON array is ordered, while a JSON-LD array is not ordered unless
that array uses the `@list` keyword.
          
          Note: Array order might not matter
While it is possible to use this data model by performing [type-specific credential processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type-specific-credential-processing), those who do so and make use of arrays need to be aware
that unless the above guidance is followed, the order of items in an array
are not guaranteed in JSON-LD. This might lead to unexpected behavior.
          
          
If JSON structure or ordering is important to your application, we recommend you
mark such elements as `@json` via an `@context` that is specific to your
use case. An example of such a declaration is shown below.
          
          
        
    [Example 33](https://www.w3.org/TR/vc-data-model-2.0/#example-a-context-file-that-defines-a-matrix-as-an-embedded-json-data-structure): A @context file that defines a matrix as an embedded JSON data structure
   ```
{
  "@context":
    {
      "matrix": {
        "@id": "https://website.example/vocabulary#matrix",
        "@type": "@json"
      }
    }
}
```
      

          
When the context shown above is used in the example below, by including the
`https://website.example/matrix/v1` context in the `@context` property, the
value in `credentialSubject.matrix` retains its JSON semantics; the exact order
of all elements in the two dimensional matrix is preserved.
          

          
        
    [Example 34](https://www.w3.org/TR/vc-data-model-2.0/#example-a-verifiable-credential-with-an-embedded-json-data-structure): A verifiable credential with an embedded JSON data structure
   ```
{
  "@context": [
    "https://www.w3.org/ns/credentials/v2",
    "https://www.w3.org/ns/credentials/examples/v2",
    "https://website.example/matrix/v1"
  ],
  "id": "http://university.example/credentials/1872",
  "type": [
    "VerifiableCredential",
    "ExampleMatrixCredential"
  ],
  "issuer": "https://university.example/issuers/565049",
  "validFrom": "2010-01-01T19:23:24Z",
  "credentialSubject": {
    "id": "did:example:ebfeb1f712ebc6f1c276e12ec21",
    "matrix": [
      [1,2,3,4,5,6,7,8,9,10,11,12],
      [1,1,1,1,1,1,1,1,0,0,0,0],
      [0,0,1,1,1,1,1,1,1,0,0,0]
    ]
  }
}
```
      
        
      
### 6.2 Media Types
        

        
Media types, as defined in [[RFC6838](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc6838)], identify the syntax used to express a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) as well as other useful processing guidelines.
        
        
Syntaxes used to express the data model in this specification SHOULD be
identified by a media type, and conventions outlined in this section SHOULD be
followed when defining or using media types with [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
        
        
There are two media types associated with the core data model, which are
listed in the Section [C. IANA Considerations](https://www.w3.org/TR/vc-data-model-2.0/#iana-considerations):
`application/vc` and `application/vp`.
        
        
The `application/vc` and `application/vp` media types do not
imply any particular securing mechanism, but are intended to be used in
conjunction with securing mechanisms. A securing mechanism needs to be applied
to protect the integrity of these media types. Do not assume security of content
regardless of the media type used to communicate it.
        

#### Media Type Precision*This section is non-normative.*
          

          
At times, developers or systems might use lower precision media types to convey
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). Some of the reasons
for use of lower precision media types include:
          

          
            - 
A web server defaults to `text/plain` or `application/octet-stream` when a file
extension is not available and it cannot determine the media type.
            
            - 
A developer adds a file extension that leads to a media type that is less
specific than the content of the file. For example, `.json` could result in a
media type of `application/json` and `.jsonld` might result in a media type of
`application/ld+json`.
            
            - 
A protocol requires a less precise media type for a particular transaction; for
example, `application/json` instead of `application/vp`,
            
          

          
Implementers are urged to not raise errors when it is possible to determine the
intended media type from a payload, provided that the media type used is
acceptable in the given protocol. For example, if an application only accepts
payloads that conform to the rules associated with the `application/vc` media
type, but the payload is tagged with `application/json` or `application/ld+json`
instead, the application might perform the following steps to determine whether
the payload also conforms to the higher precision media type:
          

          
            - 
Parse the payload as a JSON document.
            
            - 
Ensure that the first element of the `@context` property matches
`https://www.w3.org/ns/credentials/v2`.
            
            - 
Assume an `application/vp` media type if the JSON document contains a top-level
`type` property containing a `VerifiablePresentation` element. Additional
subsequent checks are still expected to be performed (according to this
specification) to ensure the payload expresses a conformant
[verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation).
            
            - 
Assume an `application/vc` media type if the JSON document contains a top-level
`type` property containing a `VerifiableCredential` element. Additional
subsequent checks are still expected to be performed (according to this
specification) to ensure the payload expresses a conformant
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential).
            
          

          
Whenever possible, implementers are advised to use the most precise (the highest
precision) media type for all payloads defined by this specification.
Implementers are also advised to recognize that a payload tagged with a lower
precision media type does not mean that the payload does not meet the rules
necessary to tag it with a higher precision type. Similarly, a payload tagged
with a higher precision media type does not mean that the payload will meet the
requirements associated with the media type. Receivers of payloads, regardless
of their associated media type, are expected to perform appropriate checks to
ensure that payloads conform with the requirements for their use in a given
system.
          
          
HTTP clients and servers use media types associated with [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) in accept headers and when
indicating content types. Implementers are warned that HTTP servers might ignore
the accept header and return another content type, or return an error code such
as [415 Unsupported Media Type](https://httpwg.org/specs/rfc7231.html#rfc.section.6.5.13).
          
        
      

### 6.3 Type-Specific Credential Processing*This section is non-normative.*
          

          
As JSON can be used to express different kinds of information, a consumer of
a particular JSON document can only properly interpret the author's intent if they
possess information that contextualizes and disambiguates it from other possible
expressions. Information to assist with this interpretation can either be wholly
external to the JSON document or linked from within it. Compacted JSON-LD documents
include a `@context` property that internally expresses or links to
contextual information to express [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims). These features
enable generalized processors to be written to convert JSON-LD documents from one
context to another, but this is not needed when consumers receive JSON-LD documents
that already use the context and shape that they expect. Authors of JSON-LD
documents, such as [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), are required
to provide proper JSON-LD contexts and follow these rules in order to facilitate
interoperability.
          

          
The text below helps consumers understand how to ensure a JSON-LD document is
expressed in a context and shape that their application already understands
such that they do not need to transform it in order to consume its contents.
Notably, this does not mean that consumers do not need to understand any
context at all; rather, consuming applications only need to understand a chosen
set of contexts and document shapes to work with and not others. Issuers can
publish contexts and information about their [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to
aid consumers who do not use generalized processors, just as can be done
with any other JSON-formatted data.
          

          
General JSON-LD processing is defined as a mechanism that uses a
JSON-LD software library to process a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) by performing
various [transformations](https://www.w3.org/TR/json-ld11/#forms-of-json-ld).
Type-specific credential processing is defined as a lighter-weight
mechanism for processing [conforming documents](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document), that doesn't require
a JSON-LD software library. Some consumers of [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential)
only need to consume credentials with specific types. These consumers can use
type-specific credential processing instead of generalized processing. Scenarios
where type-specific credential processing can be desirable include, but are not
limited to, the following:
          

          
            - 
Before applying a securing mechanism to a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document), or after
verifying a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) protected by a securing mechanism, to
ensure
[data integrity](https://csrc.nist.gov/glossary/term/data_integrity).
            
            - 
When performing JSON Schema validation, as described in Section
[4.11 Data Schemas](https://www.w3.org/TR/vc-data-model-2.0/#data-schemas).
            
            - 
When serializing or deserializing [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or
[verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) into systems that store or index their contents.
            
            - 
When operating on [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or [verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) in a software application, after verification or validation
is performed for securing mechanisms that require
[general JSON-LD processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-general-json-ld-processing).
            
            - 
When an application chooses to process the media type using the `+json`
structured media type suffix.
            
          

          
That is, [type-specific credential processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type-specific-credential-processing) is allowed as long as the
document being consumed or produced is a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document).
          

          
If [type-specific credential processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type-specific-credential-processing) is desired, an implementer is advised
to follow this rule:

Ensure that all values associated with a `@context` property are in the expected
order, the contents of the context files match known good cryptographic hashes
for each file, and domain experts have deemed that the contents are appropriate
for the intended use case.
          

          
Using static context files with a JSON Schema is one acceptable approach to
implementing the rule above. This can ensure proper term identification,
typing, and order, when performing [type-specific credential processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type-specific-credential-processing).
          

          
The rule above guarantees semantic interoperability between the two processing
mechanisms for mapping literal JSON keys to URIs via the `@context` mechanism.
While [general JSON-LD processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-general-json-ld-processing) can use previously unseen `@context`
values provided in its algorithms to verify that all terms are correctly
specified, implementations that perform [type-specific credential processing](https://www.w3.org/TR/vc-data-model-2.0/#dfn-type-specific-credential-processing) only accept specific `@context` values which the implementation
is engineered ahead of time to understand, resulting in the same semantics
without invoking any JSON-LD APIs. In other words, the context in which the data
exchange happens is explicitly stated for both processing mechanisms by using
`@context` in a way that leads to the same [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) semantics.

---

## 7. Algorithms
      

      
This section contains algorithms that can be used by implementations to perform
common operations, such as [verification](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verify). Conformance requirements phrased as
algorithms use normative concepts from the [Infra Standard](https://infra.spec.whatwg.org/) [[INFRA](https://www.w3.org/TR/vc-data-model-2.0/#bib-infra)]. See the
section on [Algorithm Conformance](https://infra.spec.whatwg.org/#algorithm-conformance)
in the [Infra Standard](https://infra.spec.whatwg.org/) for more guidance on implementation requirements.
      

      Note: Implementers can include additional checks, warnings, and errors.
Implementers are advised that the algorithms in this section contain the bare
minimum set of checks used by implementations to test conformance to this
specification. Implementations are expected to provide additional checks that
report helpful warnings for developers to help debug potential issues.
Similarly, implementations are likely to provide additional checks that
could result in new types of errors being reported in order to stop harmful
content. Any of these additional checks might be integrated into future
versions of this specification.
      

### 7.1 Verification
        

        
This section contains an algorithm that [conforming verifier implementations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-verifier-implementation)
MUST run when verifying a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) or a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation). This algorithm takes a media type ([string](https://infra.spec.whatwg.org/#string) inputMediaType)
and secured data ([byte sequence](https://infra.spec.whatwg.org/#byte-sequence) inputData) and returns a [map](https://infra.spec.whatwg.org/#ordered-map) that
contains the following:
        

        
          - 
a status ([boolean](https://infra.spec.whatwg.org/#boolean) status)
          
          - 
a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) ([map](https://infra.spec.whatwg.org/#ordered-map) document)
          
          - 
a media type ([string](https://infra.spec.whatwg.org/#string) mediaType)
          
          - 
a controller of the verification method associated with the securing mechanism
([string](https://infra.spec.whatwg.org/#string) controller)
          
          - 
a controlled identifier document that is associated with the verification method
used to verify the securing mechanism ([map](https://infra.spec.whatwg.org/#ordered-map) controlledIdentifierDocument)
          
          - 
zero or more warnings ([list](https://infra.spec.whatwg.org/#list) of [ProblemDetails](https://www.w3.org/TR/vc-data-model-2.0/#dfn-problemdetails) warnings)
          
          - 
zero or more errors ([list](https://infra.spec.whatwg.org/#list) of [ProblemDetails](https://www.w3.org/TR/vc-data-model-2.0/#dfn-problemdetails) errors)
          
        

        
The verification algorithm is as follows:
        

        
          - 
Ensure that the securing mechanism has properly protected the
[conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) by performing the following steps:
            
             - 
Set the verifyProof function by using the inputMediaType and the
[Securing Mechanisms](https://w3c.github.io/vc-extensions/#securing-mechanisms)
section of the [Verifiable Credential Extensions](https://w3c.github.io/vc-extensions/) document, or other mechanisms known to the
implementation, to determine the cryptographic suite to use when verifying the
securing mechanism. The verifyProof function MUST implement the interface
described in [5.13 Securing Mechanism Specifications](https://www.w3.org/TR/vc-data-model-2.0/#securing-mechanism-specifications).
              
              - 
If the verifyProof function expects a [byte sequence](https://infra.spec.whatwg.org/#byte-sequence), provide
inputMediaType and inputData to the algorithm. If the verifyProof function
expects a [map](https://infra.spec.whatwg.org/#ordered-map), provide inputMediaType and the result of [parse JSON bytes to an Infra value](https://infra.spec.whatwg.org/#parse-json-bytes-to-an-infra-value) given inputData. Set result to the result of the
call to the verifyProof function. If the call was successful, result will
contain the status, document, mediaType, controller,
controlledIdentifierDocument, warnings, and errors properties.
              
              - 
If result.status is set to `false`, add a
[CRYPTOGRAPHIC_SECURITY_ERROR](https://www.w3.org/TR/vc-data-model-2.0/#CRYPTOGRAPHIC_SECURITY_ERROR) to
result.errors.
              
            
          
          - 
If result.status is set to `true`, ensure that
result.document is a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document). If it is
not, set result.status to `false`, remove the
document property from result, and add at least
one [MALFORMED_VALUE_ERROR](https://www.w3.org/TR/vc-data-model-2.0/#MALFORMED_VALUE_ERROR) to
result.errors. Other warnings and errors MAY be included
to aid any debugging process.
          
          - 
Return result.
          
        

        
The steps for verifying the state of the securing mechanism and verifying
that the input document is a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) MAY be performed in
a different order than that provided above as long as the
implementation returns errors for the same invalid inputs.
Implementations MAY produce different errors than described above.
        

      

### 7.2 Problem Details
        

        
When an implementation detects an anomaly while processing a document, a
ProblemDetails object can be used to report the issue to other
software systems. The interface for these objects follow [[RFC9457](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc9457)]
to encode the data. A [ProblemDetails](https://www.w3.org/TR/vc-data-model-2.0/#dfn-problemdetails) object consists of the following
properties:
        

        
          type
          
The `type` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) MUST be present and its value MUST be a [URL](https://www.w3.org/TR/vc-data-model-2.0/#dfn-url)
identifying the type of problem.
          
          title
          
The `title` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) SHOULD provide a short
but specific human-readable string for the problem.
          
          detail
          
The `detail` [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) SHOULD provide a
longer human-readable string for the problem.
          
        

        
The following problem description types are defined by this specification:
        

        
          
https://www.w3.org/TR/vc-data-model#PARSING_ERROR
          
          
There was an error while parsing input.
          
          
https://www.w3.org/TR/vc-data-model#CRYPTOGRAPHIC_SECURITY_ERROR
          
          
The securing mechanism for the document has detected a
modification in the contents of the document since it was created;
potential tampering detected. See Section
[7.1 Verification](https://www.w3.org/TR/vc-data-model-2.0/#verification).
          
          
https://www.w3.org/TR/vc-data-model#MALFORMED_VALUE_ERROR
          
          
The value associated with a particular [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) is malformed. The
name of the [property](https://www.w3.org/TR/vc-data-model-2.0/#dfn-property) and the path to the property SHOULD be provided
in the [ProblemDetails](https://www.w3.org/TR/vc-data-model-2.0/#dfn-problemdetails) object. See Section
[7.1 Verification](https://www.w3.org/TR/vc-data-model-2.0/#verification).
          
          
https://www.w3.org/TR/vc-data-model#RANGE_ERROR
          
          
A provided value is outside of the expected range of an associated value,
such as a given index value for an array being larger than the current size
of the array.
          
        

        
Implementations MAY extend the [ProblemDetails](https://www.w3.org/TR/vc-data-model-2.0/#dfn-problemdetails) object by specifying
additional types or properties. See the
[Extension Member](https://www.rfc-editor.org/rfc/rfc9457#name-extension-members) section
in [[RFC9457](https://www.w3.org/TR/vc-data-model-2.0/#bib-rfc9457)] for further guidance on using this mechanism.
