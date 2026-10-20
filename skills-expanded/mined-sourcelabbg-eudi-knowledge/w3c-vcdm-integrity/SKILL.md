---
name: "w3c-vcdm-integrity"
description: "Use when implementing integrity requirements in W3C VCDM. Covers integrity-related claims and processing expectations."
sections:
  - "5.3 Integrity of Related Resources"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~1647 -->

### 5.3 Integrity of Related Resources
        
        
When including a link to an external resource in a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), it
is desirable to know whether the resource has been modified since the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) was issued. This applies to cases where there is an
external resource that is remotely retrieved, as well as to cases where the
[issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and/or [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might have locally cached copies of a resource.
It can also be desirable to know that the contents of the JSON-LD context(s)
used in the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) are the same when used by the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
as they were when used by the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers).
        

        
To extend integrity protection to a related resource, an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) of a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) MAY include the `relatedResource` property:
        

        
          relatedResource
          
The value of the `relatedResource` property MUST be one or more objects of the
following form:
            
              
                Property
                Description
              
              
                
                  `id`
                  
The identifier for the resource is REQUIRED and conforms to the format defined
in Section [4.4 Identifiers](https://www.w3.org/TR/vc-data-model-2.0/#identifiers). The value MUST be unique among the list of
related resource objects.
                  
                
                
                  `mediaType`
                  
An OPTIONAL valid media type as listed in the
[IANA Media Types](https://www.iana.org/assignments/media-types/media-types.xhtml) registry.
                  
                
                
                  `digestSRI`
                  
One or more cryptographic digests, as defined by the `hash-expression` ABNF
grammar defined in the [Subresource Integrity](https://www.w3.org/TR/SRI/) specification,
[Section 3.5: The integrity
attribute](https://www.w3.org/TR/SRI/#the-integrity-attribute).
                  
                
                
                  `digestMultibase`
                  
One or more cryptographic digests, as defined by the `digestMultibase`
property in the [Verifiable Credential Data Integrity 1.0](https://www.w3.org/TR/vc-data-integrity/)
specification, [Section 2.6: Resource Integrity](https://www.w3.org/TR/vc-data-integrity/#resource-integrity).
                  
                

              
            
Each object associated with `relatedResource` MUST contain at least a
`digestSRI` or a `digestMultibase` value.
          
        

        
If a `mediaType` is listed, implementations that retrieve the resource
identified by the `id` property using [HTTP Semantics](https://httpwg.org/specs/rfc9110.html) SHOULD:
        
        
          - 
use the media type in the `Accept` HTTP Header, and
          
          - 
reject the response if it includes a `Content-Type` HTTP Header with a different
media type.
          
        

        
Any object in the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) that contains an `id`
property MAY be annotated with integrity information by adding either the
`digestSRI` or `digestMultibase` property, either of which MAY be
accompanied by the additionally optional `mediaType` property.
        

        
Any objects for which selective disclosure or unlinkable disclosure is desired
SHOULD NOT be included as an object in the `relatedResource` array.
        

        
A [conforming verifier implementation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-verifier-implementation) that makes use of a resource based on
the `id` of a `relatedResource` object inside a [conforming document](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-document) with a
corresponding cryptographic digest appearing in a `relatedResource` object value
MUST compute the digest of the retrieved resource. If the digest provided by the
[issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) does not match the digest computed for the retrieved resource, the
[conforming verifier implementation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-conforming-verifier-implementation) MUST produce an error.
        

        
Implementers are urged to consult appropriate sources, such as the
[FIPS 180-4 Secure Hash Standard](https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.180-4.pdf) and the
[Commercial National Security Algorithm Suite 2.0](https://en.wikipedia.org/wiki/Commercial_National_Security_Algorithm_Suite) to ensure that they are
choosing a current and reliable hash algorithm. At the time of this writing
`sha384` SHOULD be considered the minimum strength hash algorithm for use by
implementers.
        
        
An example of a related resource integrity object referencing JSON-LD contexts.
        

        
        
    [Example 25](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-digestsri-property-base64-encoded-sha2-384): Use of the digestSRI property (base64-encoded SHA2-384)
   ```
"relatedResource": [{
  "id": "https://www.w3.org/ns/credentials/v2",
  "digestSRI":
    "sha384-Ml/HrjlBCNWyAX91hr6LFV2Y3heB5Tcr6IeE4/Tje8YyzYBM8IhqjHWiWpr8+ZbYU"
},{
  "id": "https://www.w3.org/ns/credentials/examples/v2",
  "digestSRI":
    "sha384-MzNNbQTWCSUSi0bbz7dbua+RcENv7C6FvlmYJ1Y+I727HsPOHdzwELMYO9Mz68M26"
}]
```
      

        
        
    [Example 26](https://www.w3.org/TR/vc-data-model-2.0/#example-use-of-the-digestmultibase-property-base64-url-nopad-encoded-sha2-256): Use of the digestMultibase property (base64-url-nopad-encoded SHA2-256)
   ```
"relatedResource": [{
  "id": "https://www.w3.org/ns/credentials/v2",
  "digestMultibase": "uEiBZlVztZpfWHgPyslVv6-UwirFoQoRvW1htfx963sknNA"
},{
  "id": "https://www.w3.org/ns/credentials/examples/v2",
  "digestMultibase": "uEiBXOT-8adbvubm13Jy2uYgLCUQ2Cr_i6vRZyeWM8iedfA"
}]
```
