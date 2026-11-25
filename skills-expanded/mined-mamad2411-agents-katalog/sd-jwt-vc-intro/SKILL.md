---
name: "sd-jwt-vc-intro"
description: "Use when understanding the SD-JWT VC credential format. Covers: introduction, terminology, and the vct (Verifiable Credential Type) claim."
sections:
  - "1. Introduction"
  - "1.1. Issuer-Holder-Verifier Model"
  - "1.2. SD-JWT as a Credential Format"
  - "1.3. Requirements Notation and Conventions"
  - "1.4. Terms and Definitions"
  - "2. Scope"
  - "3. Verifiable Credentials based on SD-JWT"
  - "3.1. Media Type"
  - "3.2. Data Format"
  - "3.3. Example"
  - "3.4. Verification and Processing"
  - "3.5. Issuer-signed JWT Verification Key Validation"
---

<!-- ARF version: draft-08 -->
<!-- Tokens: ~7740 -->

## 1. Introduction


### 1.1. Issuer-Holder-Verifier Model
In the so-called Issuer-Holder-Verifier Model, Issuers issue so-called Verifiable Credentials to a
Holder, who can then present the Verifiable Credentials to Verifiers. Verifiable
Credentials are cryptographically secured statements about a Subject, typically the Holder.

          
```
+------------+
         |            |
         |   Issuer   |
         |            |
         +------------+
               |
    Issues Verifiable Credential
               |
               v
         +------------+
         |            |
         |   Holder   |
         |            |
         +------------+
               |
  Presents Verifiable Credential
               |
               v
         +-------------+
         |             |+                          +------------+
         |  Verifiers  ||+                         |   Status   |
         |             |||----- optionally ------->|  Provider  |
         +-------------+||   retrieve status of    |            |
          +-------------+|  Verifiable Credential  +------------+
           +-------------+
```

Figure 1:
Issuer-Holder-Verifier Model with optional Status Provider
          
Verifiers can check the authenticity of the data in the Verifiable Credentials
and optionally enforce Key Binding, i.e., ask the Holder to prove that they
are the intended holder of the Verifiable Credential, for example, by proving possession of a
cryptographic key referenced in the credential. This process is further
described in [[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)].
To support revocation of Verifiable Credentials, revocation information can
optionally be retrieved from a Status Provider. The role of a Status Provider
can be fulfilled by either a fourth party or by the Issuer.


### 1.2. SD-JWT as a Credential Format
JSON Web Tokens (JWTs) [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7519)] can in principle be used to express
Verifiable Credentials in a way that is easy to understand and process as it
builds upon established web primitives.
Selective Disclosure JWT (SD-JWT) [[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)] is
a specification that introduces conventions to support selective disclosure for
JWTs: For an SD-JWT document, a Holder can decide which claims to release (within
bounds defined by the Issuer).
SD-JWT is a superset of JWT as it can also be used when there are no selectively
disclosable claims and also supports JWS JSON serialization, which is useful for
long term archiving and multi signatures. However, SD-JWT itself does not define
the claims that must be used within the payload or their semantics.
This specification uses SD-JWT and the well-established JWT content rules and
extensibility model as basis for representing Verifiable Credentials with JSON
payloads. These Verifiable Credentials are called SD-JWT VCs. The use of
selective disclosure in SD-JWT VCs is OPTIONAL.
SD-JWTs VC can contain claims that are registered in "JSON Web Token Claims"
registry as defined in [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7519)], as well as public and
private claims.
Note: This specification does not utilize the W3C's Verifiable Credentials Data Model v1.0, v1.1, or v2.0.


### 1.3. Requirements Notation and Conventions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD",
"SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this
document are to be interpreted as described in RFC 2119 [[RFC2119](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC2119)].


### 1.4. Terms and Definitions
This specification uses the terms "Holder", "Issuer", "Verifier", "Key Binding", and "Key Binding JWT" defined by
[[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)].

          Consumer:
          Applications using the Type Metadata specified in [Section 6](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#type-metadata) are called Consumer. This typically includes Issuers, Verifiers, and Wallets.

          
Verifiable Credential (VC):
          An assertion with claims about a Subject that is cryptographically secured by an Issuer (usually by a digital signature).

          
SD-JWT-based Verifiable Credential (SD-JWT VC):
          A Verifiable Credential encoded using the format defined in
[[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)]. It may or may not contain
selectively disclosable claims.

          
Unsecured Payload of an SD-JWT VC:
          A JSON object containing all selectively disclosable and non-selectively disclosable claims
of the SD-JWT VC. The Unsecured Payload acts as the input JSON object to issue
an SD-JWT VC complying to this specification.

          
Status Provider:
          An entity that provides status information (e.g. revocation) about a Verifiable Credential.

---

## 2. Scope

- 
          This specification defines

- Data model and media types for Verifiable Credentials based on SD-JWTs.

            - Validation and processing rules for Verifiers and Holders.

---

## 3. Verifiable Credentials based on SD-JWT
This section defines encoding, validation and processing rules for SD-JWT VCs.


### 3.1. Media Type
SD-JWT VCs compliant with this specification MUST use the media type
`application/dc+sd-jwt` as defined in [Section 3.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#media-type).
The base subtype name `dc` is meant to stand for "digital credential", which is
a term that is emerging as a conceptual synonym for "verifiable credential".


### 3.2. Data Format
SD-JWT VCs MUST be encoded using the SD-JWT format defined in Section 4 of
[[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)]. A presentation of an SD-JWT VC MAY
contain a Key Binding JWT.
Note that in some cases, an SD-JWT VC MAY have no selectively disclosable
claims, and therefore the encoded SD-JWT will not contain any Disclosures.


#### 3.2.1. JOSE Header
This section defines JWT header parameters for the SD-JWT component of the
SD-JWT VC.
The `typ` header parameter of the SD-JWT MUST be present. The `typ` value MUST
use `dc+sd-jwt`. This indicates that the payload of the SD-JWT contains plain
JSON and follows the rules as defined in this specification. It further
indicates that the SD-JWT is a SD-JWT component of a SD-JWT VC.
The following is a non-normative example of a decoded SD-JWT header:

```
{
  "alg": "ES256",
  "typ": "dc+sd-jwt"
}
```

Note that this draft used `vc+sd-jwt` as the value of the `typ` header from its inception in July 2023 until November 2024 when it was changed to `dc+sd-jwt` to avoid conflict with the `vc` media type name registered by the W3C's Verifiable Credentials Data Model draft. In order to facilitate a minimally disruptive transition, it is RECOMMENDED that Verifiers and Holders accept both `vc+sd-jwt` and `dc+sd-jwt` as the value of the `typ` header for a reasonable transitional period.


#### 3.2.2. JWT Claims Set
This section defines the claims that can be included in the payload of
SD-JWT VCs.


##### 3.2.2.1. New JWT Claims


###### 3.2.2.1.1. Verifiable Credential Type - vct Claim
This specification defines the JWT claim `vct` (for verifiable credential type). The `vct` value MUST be a
case-sensitive `StringOrURI` (see [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7519)]) value serving as an identifier
for the type of the SD-JWT VC. The `vct` value MUST be a Collision-Resistant
Name as defined in Section 2 of [[RFC7515](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7515)].
A type is associated with rules defining which claims may or must appear in the
Unsecured Payload of the SD-JWT VC and whether they may, must, or must not be
selectively disclosable. This specification does not define any `vct` values; instead
it is expected that ecosystems using SD-JWT VCs define such values including
the semantics of the respective claims and associated rules (e.g., policies for issuing and
validating credentials beyond what is defined in this specification).
The following is a non-normative example of how `vct` is used to express
a type:

```
{
  "vct": "https://credentials.example.com/identity_credential"
}
```

For example, a value of `https://credentials.example.com/identity_credential` can be associated with rules that define that at least the registered JWT claims `given_name`, `family_name`, `birthdate`, and `address` must appear in the Unsecured Payload. Additionally, the registered JWT claims `email` and `phone_number`, and the private claims `is_over_18`, `is_over_21`, and `is_over_65` may be used. The type might also indicate that any of the aforementioned claims can be selectively disclosable.


##### 3.2.2.2. Registered JWT Claims
SD-JWT VCs MAY use any claim registered in the "JSON Web Token Claims"
registry as defined in [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7519)].
If present, the following registered JWT claims MUST be included in the SD-JWT
and MUST NOT be included in the Disclosures, i.e. cannot be selectively
disclosed:

- 
                `iss`

- REQUIRED. The Issuer of the Verifiable Credential. The value of `iss`
MUST be a URI. See [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7519)] for more information.

                

              - 
                `nbf`

- OPTIONAL. The time before which the Verifiable Credential MUST NOT be
accepted before validating. See [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7519)] for more information.

                

              - 
                `exp`

- OPTIONAL. The expiry time of the Verifiable Credential after which the
Verifiable Credential is no longer valid. See [[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7519)] for more
information.

                

              - 
                `cnf`

- OPTIONAL unless cryptographic Key Binding is to be supported, in which case it is REQUIRED. Contains the confirmation method identifying the proof of possession key as defined in [[RFC7800](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7800)]. It is RECOMMENDED that this contains a JWK as defined in Section 3.2 of [[RFC7800](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7800)]. For proof of cryptographic Key Binding, the Key Binding JWT in the presentation of the SD-JWT MUST be secured by the key identified in this claim.

                

              - 
                `vct`

- REQUIRED. The type of the Verifiable Credential, e.g.,
`https://credentials.example.com/identity_credential`, as defined in [Section 3.2.2.1.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#type-claim).

                

              - 
                `status`

- OPTIONAL. The information on how to read the status of the Verifiable
Credential. See [[I-D.ietf-oauth-status-list](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-status-list)]
for more information.

                

            
The following registered JWT claims MAY be contained in the SD-JWT or in the
Disclosures and MAY be selectively disclosed:

- 
                `sub`

- OPTIONAL. The identifier of the Subject of the Verifiable Credential.
The Issuer MAY use it to provide the Subject
identifier known by the Issuer. There is no requirement for a binding to
exist between `sub` and `cnf` claims.

                

              - 
                `iat`

- OPTIONAL. The time of issuance of the Verifiable Credential. See
[[RFC7519](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7519)] for more information.

                

            


##### 3.2.2.3. Public JWT claims
Additional public claims MAY be used in SD-JWT VCs depending on the
application.


##### 3.2.2.4. SD-JWT VC without Selectively Disclosable Claims
An SD-JWT VC MAY have no selectively disclosable claims.
In that case, the SD-JWT VC MUST NOT contain the `_sd` claim in the JWT body. It also
MUST NOT have any Disclosures.


### 3.3. Example
The following is a non-normative example of the user data of an unsecured payload of an
SD-JWT VC.

```
{
  "vct": "https://credentials.example.com/identity_credential",
  "given_name": "John",
  "family_name": "Doe",
  "email": "johndoe@example.com",
  "phone_number": "+1-202-555-0101",
  "address": {
    "street_address": "123 Main St",
    "locality": "Anytown",
    "region": "Anystate",
    "country": "US"
  },
  "birthdate": "1940-01-01",
  "is_over_18": true,
  "is_over_21": true,
  "is_over_65": true
}
```

The following is a non-normative example of how the unsecured payload of the
SD-JWT VC above can be used in an SD-JWT where the resulting SD-JWT VC contains
only claims about the Subject that are selectively disclosable:

```
{
  "_sd": [
    "09vKrJMOlyTWM0sjpu_pdOBVBQ2M1y3KhpH515nXkpY",
    "2rsjGbaC0ky8mT0pJrPioWTq0_daw1sX76poUlgCwbI",
    "EkO8dhW0dHEJbvUHlE_VCeuC9uRELOieLZhh7XbUTtA",
    "IlDzIKeiZdDwpqpK6ZfbyphFvz5FgnWa-sN6wqQXCiw",
    "JzYjH4svliH0R3PyEMfeZu6Jt69u5qehZo7F7EPYlSE",
    "PorFbpKuVu6xymJagvkFsFXAbRoc2JGlAUA2BA4o7cI",
    "TGf4oLbgwd5JQaHyKVQZU9UdGE0w5rtDsrZzfUaomLo",
    "jdrTE8YcbY4EifugihiAe_BPekxJQZICeiUQwY9QqxI",
    "jsu9yVulwQQlhFlM_3JlzMaSFzglhQG0DpfayQwLUK4"
  ],
  "iss": "https://example.com/issuer",
  "iat": 1683000000,
  "exp": 1883000000,
  "vct": "https://credentials.example.com/identity_credential",
  "_sd_alg": "sha-256",
  "cnf": {
    "jwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "TCAER19Zvu3OHF4j4W4vfSVoHIP1ILilDls7vCeGemc",
      "y": "ZxjiWWbZMQGHVWKVQ4hbSIirsVfuecCE6t4jT9F2HZQ"
    }
  }
}
```

Note that a `cnf` claim has been added to the SD-JWT payload to express the
confirmation method of the Key Binding.
The following are the Disclosures belonging to the SD-JWT payload above:
**Claim `given_name`**:

- SHA-256 Hash: `jsu9yVulwQQlhFlM_3JlzMaSFzglhQG0DpfayQwLUK4`

          - Disclosure:
            `WyIyR0xDNDJzS1F2ZUNmR2ZyeU5STjl3IiwgImdpdmVuX25hbWUiLCAiSm9o`
            `biJd`

          - Contents:
`["2GLC42sKQveCfGfryNRN9w", "given_name", "John"]`

        
**Claim `family_name`**:

- SHA-256 Hash: `TGf4oLbgwd5JQaHyKVQZU9UdGE0w5rtDsrZzfUaomLo`

          - Disclosure:
            `WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImZhbWlseV9uYW1lIiwgIkRv`
            `ZSJd`

          - Contents:
`["eluV5Og3gSNII8EYnsxA_A", "family_name", "Doe"]`

        
**Claim `email`**:

- SHA-256 Hash: `JzYjH4svliH0R3PyEMfeZu6Jt69u5qehZo7F7EPYlSE`

          - Disclosure:
            `WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgImVtYWlsIiwgImpvaG5kb2VA`
            `ZXhhbXBsZS5jb20iXQ`

          - Contents:
`["6Ij7tM-a5iVPGboS5tmvVA", "email", "johndoe@example.com"]`

        
**Claim `phone_number`**:

- SHA-256 Hash: `PorFbpKuVu6xymJagvkFsFXAbRoc2JGlAUA2BA4o7cI`

          - Disclosure:
            `WyJlSThaV205UW5LUHBOUGVOZW5IZGhRIiwgInBob25lX251bWJlciIsICIr`
            `MS0yMDItNTU1LTAxMDEiXQ`

          - Contents:
`["eI8ZWm9QnKPpNPeNenHdhQ", "phone_number",`
            `"+1-202-555-0101"]`

        
**Claim `address`**:

- SHA-256 Hash: `IlDzIKeiZdDwpqpK6ZfbyphFvz5FgnWa-sN6wqQXCiw`

          - Disclosure:
            `WyJRZ19PNjR6cUF4ZTQxMmExMDhpcm9BIiwgImFkZHJlc3MiLCB7InN0cmVl`
            `dF9hZGRyZXNzIjogIjEyMyBNYWluIFN0IiwgImxvY2FsaXR5IjogIkFueXRv`
            `d24iLCAicmVnaW9uIjogIkFueXN0YXRlIiwgImNvdW50cnkiOiAiVVMifV0`

          - Contents:
`["Qg_O64zqAxe412a108iroA", "address", {"street_address":`
            `"123 Main St", "locality": "Anytown", "region": "Anystate",`
            `"country": "US"}]`

        
**Claim `birthdate`**:

- SHA-256 Hash: `jdrTE8YcbY4EifugihiAe_BPekxJQZICeiUQwY9QqxI`

          - Disclosure:
            `WyJBSngtMDk1VlBycFR0TjRRTU9xUk9BIiwgImJpcnRoZGF0ZSIsICIxOTQw`
            `LTAxLTAxIl0`

          - Contents:
`["AJx-095VPrpTtN4QMOqROA", "birthdate", "1940-01-01"]`

        
**Claim `is_over_18`**:

- SHA-256 Hash: `09vKrJMOlyTWM0sjpu_pdOBVBQ2M1y3KhpH515nXkpY`

          - Disclosure:
            `WyJQYzMzSk0yTGNoY1VfbEhnZ3ZfdWZRIiwgImlzX292ZXJfMTgiLCB0cnVl`
            `XQ`

          - Contents:
`["Pc33JM2LchcU_lHggv_ufQ", "is_over_18", true]`

        
**Claim `is_over_21`**:

- SHA-256 Hash: `2rsjGbaC0ky8mT0pJrPioWTq0_daw1sX76poUlgCwbI`

          - Disclosure:
            `WyJHMDJOU3JRZmpGWFE3SW8wOXN5YWpBIiwgImlzX292ZXJfMjEiLCB0cnVl`
            `XQ`

          - Contents:
`["G02NSrQfjFXQ7Io09syajA", "is_over_21", true]`

        
**Claim `is_over_65`**:

- SHA-256 Hash: `EkO8dhW0dHEJbvUHlE_VCeuC9uRELOieLZhh7XbUTtA`

          - Disclosure:
            `WyJsa2x4RjVqTVlsR1RQVW92TU5JdkNBIiwgImlzX292ZXJfNjUiLCB0cnVl`
            `XQ`

          - Contents:
`["lklxF5jMYlGTPUovMNIvCA", "is_over_65", true]`

        
The SD-JWT and the Disclosures would then be serialized by the Issuer into the following format for issuance to the Holder:

```
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImRjK3NkLWp3dCIsICJraWQiOiAiZG9jLXNp
Z25lci0wNS0yNS0yMDIyIn0.eyJfc2QiOiBbIjA5dktySk1PbHlUV00wc2pwdV9wZE9C
VkJRMk0xeTNLaHBINTE1blhrcFkiLCAiMnJzakdiYUMwa3k4bVQwcEpyUGlvV1RxMF9k
YXcxc1g3NnBvVWxnQ3diSSIsICJFa084ZGhXMGRIRUpidlVIbEVfVkNldUM5dVJFTE9p
ZUxaaGg3WGJVVHRBIiwgIklsRHpJS2VpWmREd3BxcEs2WmZieXBoRnZ6NUZnbldhLXNO
NndxUVhDaXciLCAiSnpZakg0c3ZsaUgwUjNQeUVNZmVadTZKdDY5dTVxZWhabzdGN0VQ
WWxTRSIsICJQb3JGYnBLdVZ1Nnh5bUphZ3ZrRnNGWEFiUm9jMkpHbEFVQTJCQTRvN2NJ
IiwgIlRHZjRvTGJnd2Q1SlFhSHlLVlFaVTlVZEdFMHc1cnREc3JaemZVYW9tTG8iLCAi
amRyVEU4WWNiWTRFaWZ1Z2loaUFlX0JQZWt4SlFaSUNlaVVRd1k5UXF4SSIsICJqc3U5
eVZ1bHdRUWxoRmxNXzNKbHpNYVNGemdsaFFHMERwZmF5UXdMVUs0Il0sICJpc3MiOiAi
aHR0cHM6Ly9leGFtcGxlLmNvbS9pc3N1ZXIiLCAiaWF0IjogMTY4MzAwMDAwMCwgImV4
cCI6IDE4ODMwMDAwMDAsICJ2Y3QiOiAiaHR0cHM6Ly9jcmVkZW50aWFscy5leGFtcGxl
LmNvbS9pZGVudGl0eV9jcmVkZW50aWFsIiwgIl9zZF9hbGciOiAic2hhLTI1NiIsICJj
bmYiOiB7Imp3ayI6IHsia3R5IjogIkVDIiwgImNydiI6ICJQLTI1NiIsICJ4IjogIlRD
QUVSMTladnUzT0hGNGo0VzR2ZlNWb0hJUDFJTGlsRGxzN3ZDZUdlbWMiLCAieSI6ICJa
eGppV1diWk1RR0hWV0tWUTRoYlNJaXJzVmZ1ZWNDRTZ0NGpUOUYySFpRIn19fQ.2CyX0
v3AAFG9y-A_Z46uz9hHsNbr0yWTbDQaajLCrsxo-JxVh4a9dAMFVYZ8GFG2wgj2jKnA4
2wSgv7xVM64PA~WyIyR0xDNDJzS1F2ZUNmR2ZyeU5STjl3IiwgImdpdmVuX25hbWUiLC
AiSm9obiJd~WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImZhbWlseV9uYW1lIiwgI
kRvZSJd~WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgImVtYWlsIiwgImpvaG5kb2VA
ZXhhbXBsZS5jb20iXQ~WyJlSThaV205UW5LUHBOUGVOZW5IZGhRIiwgInBob25lX251b
WJlciIsICIrMS0yMDItNTU1LTAxMDEiXQ~WyJRZ19PNjR6cUF4ZTQxMmExMDhpcm9BIi
wgImFkZHJlc3MiLCB7InN0cmVldF9hZGRyZXNzIjogIjEyMyBNYWluIFN0IiwgImxvY2
FsaXR5IjogIkFueXRvd24iLCAicmVnaW9uIjogIkFueXN0YXRlIiwgImNvdW50cnkiOi
AiVVMifV0~WyJBSngtMDk1VlBycFR0TjRRTU9xUk9BIiwgImJpcnRoZGF0ZSIsICIxOT
QwLTAxLTAxIl0~WyJQYzMzSk0yTGNoY1VfbEhnZ3ZfdWZRIiwgImlzX292ZXJfMTgiLC
B0cnVlXQ~WyJHMDJOU3JRZmpGWFE3SW8wOXN5YWpBIiwgImlzX292ZXJfMjEiLCB0cnV
lXQ~WyJsa2x4RjVqTVlsR1RQVW92TU5JdkNBIiwgImlzX292ZXJfNjUiLCB0cnVlXQ~
```

Examples of what presentations of SD-JWT VCs might look like are provided in [Section 4.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#presentation-examples).


### 3.4. Verification and Processing
The recipient (Holder or Verifier) of an SD-JWT VC MUST process and verify an
SD-JWT VC as described in Section 8 of
[[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)].
If Key Binding is required (refer to the security considerations in Section 9.5 of [[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)]), the Verifier MUST verify the Key Binding JWT
according to Section 7 of [[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)]. To verify
the Key Binding JWT, the `cnf` claim of the SD-JWT MUST be used.
Furthermore, the recipient of the SD-JWT VC MUST validate the public verification key
for the Issuer-signed JWT as defined in [Section 3.5](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#issuer-signed-jwt-verification-key-validation).
If a schema is provided in the Type Metadata, a recipient MUST validate the schema as defined in [Section 6.5](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#schema-type-metadata).
If there are no selectively disclosable claims, there is no need to process the
`_sd` claim nor any Disclosures.
If `status` is present in the verified payload of the SD-JWT, the status SHOULD
be checked. It depends on the Verifier policy to reject or accept a presentation
of a SD-JWT VC based on the status of the Verifiable Credential.
Any claims used that are not understood MUST be ignored.
Additional validation rules MAY apply, but their use is out of the scope of this
specification.


### 3.5. Issuer-signed JWT Verification Key Validation
A recipient of an SD-JWT VC MUST apply the following rules to validate that the public
verification key for the Issuer-signed JWT corresponds to the `iss` value:

- JWT VC Issuer Metadata: If a recipient supports JWT VC Issuer Metadata and if the `iss` value contains an HTTPS URI, the recipient MUST
obtain the public key using JWT VC Issuer Metadata as defined in [Section 5](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#jwt-vc-issuer-metadata).

          - 
            X.509 Certificates: If the recipient supports X.509 Certificates and the `iss` value contains an HTTPS URI, the recipient MUST

- obtain the public key from the end-entity certificate of the certificates from the `x5c` header parameter of the Issuer-signed JWT and validate the X.509 certificate chain accordingly, and

              - ensure that the `iss` value matches a `uniformResourceIdentifier` SAN entry of the end-entity certificate or that the domain name in the `iss` value matches the `dNSName` SAN entry of the end-entity certificate.

            

          - DID Document Resolution: If a recipient supports DID Document Resolution and if the `iss` value contains a DID [[W3C.DID](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#W3C.DID)], the recipient MUST retrieve the public key from the DID Document resolved from the DID in the `iss` value. In this case, if the `kid` JWT header parameter is present, the `kid` MUST be a relative or absolute DID URL of the DID in the `iss` value, identifying the public key.

        
Separate specifications or ecosystem regulations MAY define rules complementing the rules defined above, but such rules are out of scope of this specification. See [Section 10.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#ecosystem-verification-rules) for security considerations.
If a recipient cannot validate that the public verification key corresponds to the `iss` value of the Issuer-signed JWT, the SD-JWT VC MUST be rejected.
