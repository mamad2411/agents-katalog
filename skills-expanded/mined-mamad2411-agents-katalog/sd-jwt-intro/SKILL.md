---
name: "sd-jwt-intro"
description: "Use when understanding SD-JWT (Selective Disclosure JWT) concepts and terminology. Covers: introduction, use cases, and key definitions."
sections:
  - "1. Introduction"
  - "1.1. Feature Summary"
  - "1.2. Conventions and Terminology"
  - "2. Flow Diagram"
---

<!-- ARF version: RFC-9901 -->
<!-- Tokens: ~1828 -->

## 1. Introduction
The exchange of JSON data between systems is often secured against modification using JSON Web Signatures (JWSs) [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)].
A popular application of JWS is the JSON Web Token (JWT) [[RFC7519](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7519)], a format that is often used to represent a user's identity.
An ID Token as defined in OpenID Connect [[OpenID.Core](https://www.rfc-editor.org/rfc/rfc9901.html#OpenID.Core)], for example, is a JWT containing the user's claims created by the server for consumption by a relying party.
In cases where the JWT is sent immediately from the server to the relying party, as in OpenID Connect, the server can select at the time of issuance which user claims to include in the JWT, minimizing the information shared with the relying party who validates the JWT.
Another model is emerging that fully decouples the issuance of a JWT from its presentation.
In this model, a JWT containing many claims is issued to an intermediate party, who holds the JWT (the Holder).
The Holder can then present the JWT to different verifying parties (Verifiers) that each may only require a subset of the claims in the JWT.
For example, the JWT may contain claims representing both an address and a birthdate.
The Holder may elect to disclose only the address to one Verifier, and only the birthdate to a different Verifier.
Privacy principles of minimal disclosure in conjunction with this model demand a mechanism enabling selective disclosure of data elements while ensuring that Verifiers can still check the authenticity of the data provided.
This specification defines such a mechanism for JSON payloads of JWSs, with JWTs as the primary use case.
Selectively Disclosable JWT (SD-JWT) is based on an approach called "salted hashes": For any data element that should be selectively disclosable, the Issuer of the SD-JWT does not include the cleartext of the data in the JSON payload of the JWS structure; instead, a digest of the data takes its place.
For presentation to a Verifier, the Holder sends the signed payload along with the cleartext of those claims it wants to disclose.
The Verifier can then compute the digest of the cleartext data and confirm it is included in the signed payload.
To ensure that Verifiers cannot guess cleartext values of non-disclosed data elements, an additional salt value is used when creating the digest and sent along with the cleartext when disclosing it.
To prevent attacks in which an SD-JWT is presented to a Verifier without the Holder's consent, this specification additionally defines a mechanism for binding the SD-JWT to a key under the control of the Holder (Key Binding).
When Key Binding is enforced, a Holder has to prove possession of a private key belonging to a public key contained in the SD-JWT itself.
It usually does so by signing over a data structure containing transaction-specific data, herein defined as the Key Binding JWT.
An SD-JWT with a Key Binding JWT is called "SD-JWT+KB" in this specification.


### 1.1. Feature Summary
This specification defines two primary data formats:

- 
            SD-JWT is a composite structure, consisting of a JWS plus optional Disclosures, enabling selective disclosure of portions of the JWS payload. It comprises the following:

- A format for enabling selective disclosure in nested JSON data structures,
supporting selectively disclosable object properties (name/value pairs) and array elements.

              - A format for encoding the selectively disclosable data items.

              - A format extending the JWS Compact Serialization, allowing for the combined
transport of the Issuer-signed JSON data structure and the disclosable data items.

              - An alternate format extending the JWS JSON Serialization, also allowing for
transport of the Issuer-signed JSON data structure and Disclosure data.

            

          - 
            SD-JWT+KB is a composite structure of an SD-JWT and a cryptographic Key Binding that can be presented to and verified by the Verifier. It comprises the following:

- A mechanism for associating an SD-JWT with a key pair.

              - A format for a Key Binding JWT (KB-JWT) that allows proof of possession of the private key of
the associated key pair.

              - A format extending the SD-JWT format for the combined transport of the SD-JWT
and the KB-JWT.

            

        


### 1.2. Conventions and Terminology

    The key words "MUST", "MUST NOT",
    "REQUIRED", "SHALL", "SHALL NOT",
    "SHOULD", "SHOULD NOT",
    "RECOMMENDED", "NOT RECOMMENDED",
    "MAY", and "OPTIONAL" in this document are to be
    interpreted as described in BCP 14 [[RFC2119](https://www.rfc-editor.org/rfc/rfc9901.html#RFC2119)] [[RFC8174](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8174)] when, and only when, they appear in all capitals, as
    shown here.

          Base64url:
          Denotes the URL-safe base64 encoding without padding defined in
 [Section 2](https://rfc-editor.org/rfc/rfc7515#section-2) of [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)].

          
Claim:
          In this document, refers generally to
object properties (name/value pairs) as well as array elements.

          
Selective Disclosure:
          Process of a Holder disclosing to a Verifier a subset of claims contained in a JWT issued by an Issuer.

          
Selectively Disclosable JWT (SD-JWT):
          A composite structure, consisting of an Issuer-signed JWT (JWS; see [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)]) and zero or more Disclosures, which
supports selective disclosure as defined in this document. It can contain both regular claims and digests of selectively disclosable claims.

          
Disclosure:
          A base64url-encoded string of a JSON array that contains a salt, a claim name (present when the claim is a name/value pair and absent when the claim is an array element), and a claim value. The Disclosure is used to calculate a digest for the respective claim. The term Disclosure refers to the whole base64url-encoded string.

          
Key Binding:
          Ability of the Holder to prove possession of an SD-JWT by proving
control over a private key during the presentation. When utilizing Key Binding, an SD-JWT contains
the public key corresponding to the private key controlled by the Holder (or a reference to this public key).

          
Key Binding JWT (KB-JWT):
          A Key Binding JWT is said to "be tied to" a particular SD-JWT when its payload
is signed using the key included in the SD-JWT payload, and the KB-JWT contains
a hash of the SD-JWT in its `sd_hash` claim. Its format is defined in [Section 4.3](https://www.rfc-editor.org/rfc/rfc9901.html#kb-jwt).

          
Selectively Disclosable JWT with Key Binding (SD-JWT+KB):
          A composite structure, comprising an SD-JWT and a Key Binding JWT tied to that SD-JWT.

          
Processed SD-JWT Payload:
          The JSON object resulting from verification and processing of the Issuer-signed SD-JWT,
with digest placeholders replaced by the corresponding values from the Disclosures.

          
Issuer:
          An entity that creates SD-JWTs.

          
Holder:
          An entity that received SD-JWTs from the Issuer and has control over them. In the context of this document, the term may refer to the actual user, the supporting hardware and software in their possession, or both.

          
Verifier:
          An entity that requests, checks, and extracts the claims from an SD-JWT with its respective Disclosures.

---

## 2. Flow Diagram

        
```
+------------+
           |            |
           |   Issuer   |
           |            |
           +------------+
                 |
            Issues SD-JWT
      including all Disclosures
                 |
                 v
           +------------+
           |            |
           |   Holder   |
           |            |
           +------------+
                 |
     Presents SD-JWT or SD-JWT+KB
    including selected Disclosures
                 |
                 v
           +-------------+
           |             |+
           |  Verifiers  ||+
           |             |||
           +-------------+||
            +-------------+|
             +-------------+
```

Figure 1:
SD-JWT Issuance and Presentation Flow
