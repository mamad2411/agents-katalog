---
name: "sd-jwt-vc-metadata"
description: "Use when configuring SD-JWT VC issuer or type metadata. Covers: header parameters, registered claims, issuer-signed JWT, issuer metadata, and type metadata resolution."
sections:
  - "4. Presenting Verifiable Credentials"
  - "4.1. Key Binding JWT"
  - "4.2. Examples"
  - "5. JWT VC Issuer Metadata"
  - "5.1. JWT VC Issuer Metadata Request"
  - "5.2. JWT VC Issuer Metadata Response"
  - "5.3. JWT VC Issuer Metadata Validation"
---

<!-- ARF version: draft-08 -->
<!-- Tokens: ~3947 -->

## 4. Presenting Verifiable Credentials
This section defines encoding, validation and processing rules for presentations
of SD-JWT VCs.


### 4.1. Key Binding JWT
If the presentation of the SD-JWT VC includes a Key Binding JWT, the Key Binding
JWT MUST adhere to the rules defined in Section 4.3 of
[[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)].
The Key Binding JWT MAY include additional claims which, when not understood, MUST
be ignored by the Verifier.


### 4.2. Examples
The following is a non-normative example of a presentation of the SD-JWT shown in [Section 3.3](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#vc-sd-jwt-example) including a Key Binding JWT.
In this presentation, the Holder provides only the Disclosures for the `address` and `is_over_65` claims.
Other claims are not disclosed to the Verifier.

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
2wSgv7xVM64PA~WyJsa2x4RjVqTVlsR1RQVW92TU5JdkNBIiwgImlzX292ZXJfNjUiLC
B0cnVlXQ~WyJRZ19PNjR6cUF4ZTQxMmExMDhpcm9BIiwgImFkZHJlc3MiLCB7InN0cmV
ldF9hZGRyZXNzIjogIjEyMyBNYWluIFN0IiwgImxvY2FsaXR5IjogIkFueXRvd24iLCA
icmVnaW9uIjogIkFueXN0YXRlIiwgImNvdW50cnkiOiAiVVMifV0~eyJhbGciOiAiRVM
yNTYiLCAidHlwIjogImtiK2p3dCJ9.eyJub25jZSI6ICIxMjM0NTY3ODkwIiwgImF1ZC
I6ICJodHRwczovL2V4YW1wbGUuY29tL3ZlcmlmaWVyIiwgImlhdCI6IDE3MzMyMzAxND
AsICJzZF9oYXNoIjogIkhWVjBCcG5FTHlHTnRVVFlCLU5nWHhmN2pvTjZBekprYVdEOU
VkNVo1VjgifQ.FJLPPlBB2wOWEYLLtwd7WYlaTpIz0ALlRuskPi0fSYFDEn25gGkXSSJ
sQxjhryxqN4aLbwMRRfcvDdk1A_eLHQ
```

After validation, the Verifier will have the following processed SD-JWT payload available for further handling:

```
{
  "iss": "https://example.com/issuer",
  "iat": 1683000000,
  "exp": 1883000000,
  "vct": "https://credentials.example.com/identity_credential",
  "cnf": {
    "jwk": {
      "kty": "EC",
      "crv": "P-256",
      "x": "TCAER19Zvu3OHF4j4W4vfSVoHIP1ILilDls7vCeGemc",
      "y": "ZxjiWWbZMQGHVWKVQ4hbSIirsVfuecCE6t4jT9F2HZQ"
    }
  },
  "is_over_65": true,
  "address": {
    "street_address": "123 Main St",
    "locality": "Anytown",
    "region": "Anystate",
    "country": "US"
  }
}
```

The following example shows a presentation of a (similar but different) SD-JWT without a
Key Binding JWT:

```
eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImRjK3NkLWp3dCJ9.eyJfc2QiOiBbIjA5dkt
ySk1PbHlUV00wc2pwdV9wZE9CVkJRMk0xeTNLaHBINTE1blhrcFkiLCAiMnJzakdiYUM
wa3k4bVQwcEpyUGlvV1RxMF9kYXcxc1g3NnBvVWxnQ3diSSIsICJFa084ZGhXMGRIRUp
idlVIbEVfVkNldUM5dVJFTE9pZUxaaGg3WGJVVHRBIiwgIklsRHpJS2VpWmREd3BxcEs
2WmZieXBoRnZ6NUZnbldhLXNONndxUVhDaXciLCAiSnpZakg0c3ZsaUgwUjNQeUVNZmV
adTZKdDY5dTVxZWhabzdGN0VQWWxTRSIsICJQb3JGYnBLdVZ1Nnh5bUphZ3ZrRnNGWEF
iUm9jMkpHbEFVQTJCQTRvN2NJIiwgIlRHZjRvTGJnd2Q1SlFhSHlLVlFaVTlVZEdFMHc
1cnREc3JaemZVYW9tTG8iLCAiamRyVEU4WWNiWTRFaWZ1Z2loaUFlX0JQZWt4SlFaSUN
laVVRd1k5UXF4SSIsICJqc3U5eVZ1bHdRUWxoRmxNXzNKbHpNYVNGemdsaFFHMERwZmF
5UXdMVUs0Il0sICJpc3MiOiAiaHR0cHM6Ly9leGFtcGxlLmNvbS9pc3N1ZXIiLCAiaWF
0IjogMTY4MzAwMDAwMCwgImV4cCI6IDE4ODMwMDAwMDAsICJ2Y3QiOiAiaHR0cHM6Ly9
jcmVkZW50aWFscy5leGFtcGxlLmNvbS9pZGVudGl0eV9jcmVkZW50aWFsIiwgIl9zZF9
hbGciOiAic2hhLTI1NiJ9.GetJdLXOuLJJrbBYR0zYlMq97qmmLoInT5-Vcq2gXQytHn
ERrQ-W_7Bf2TWme58A1dPgK98-nTDPz00oigMstA~WyJsa2x4RjVqTVlsR1RQVW92TU5
JdkNBIiwgImlzX292ZXJfNjUiLCB0cnVlXQ~WyJRZ19PNjR6cUF4ZTQxMmExMDhpcm9B
IiwgImFkZHJlc3MiLCB7InN0cmVldF9hZGRyZXNzIjogIjEyMyBNYWluIFN0IiwgImxv
Y2FsaXR5IjogIkFueXRvd24iLCAicmVnaW9uIjogIkFueXN0YXRlIiwgImNvdW50cnki
OiAiVVMifV0~
```

The Verifier will have the following processed SD-JWT payload after validation:

```
{
  "iss": "https://example.com/issuer",
  "iat": 1683000000,
  "exp": 1883000000,
  "vct": "https://credentials.example.com/identity_credential",
  "is_over_65": true,
  "address": {
    "street_address": "123 Main St",
    "locality": "Anytown",
    "region": "Anystate",
    "country": "US"
  }
}
```

---

## 5. JWT VC Issuer Metadata
This specification defines the JWT VC Issuer Metadata to retrieve the JWT VC
Issuer Metadata configuration of the Issuer of the SD-JWT VC. The Issuer
is identified by the `iss` claim in the JWT. Use of the JWT VC Issuer Metadata
is OPTIONAL.
Issuers publishing JWT VC Issuer Metadata MUST make a JWT VC Issuer Metadata
configuration available at the location formed by inserting the well-known string
`/.well-known/jwt-vc-issuer` between the host component and the path
component (if any) of the `iss` claim value in the JWT. The `iss` MUST
be a case-sensitive URL using the HTTPS scheme that contains scheme, host and,
optionally, port number and path components, but no query or fragment
components.


### 5.1. JWT VC Issuer Metadata Request
A JWT VC Issuer Metadata configuration MUST be queried using an HTTP `GET` request
at the path defined in [Section 5](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#jwt-vc-issuer-metadata).
The following is a non-normative example of an HTTP request for the JWT VC Issuer
Metadata configuration when `iss` is set to `https://example.com`:

```
GET /.well-known/jwt-vc-issuer HTTP/1.1
Host: example.com
```

If the `iss` value contains a path component, any terminating `/` MUST be
removed before inserting `/.well-known/` and the well-known URI suffix
between the host component and the path component.
The following is a non-normative example of a HTTP request for the JWT VC Issuer
Metadata configuration when `iss` is set to `https://example.com/tenant/1234`:

```
GET /.well-known/jwt-vc-issuer/tenant/1234 HTTP/1.1
Host: example.com
```


### 5.2. JWT VC Issuer Metadata Response
A successful response MUST use the `200 OK HTTP` and return the JWT VC Issuer
Metadata configuration using the `application/json` content type.
An error response uses the applicable HTTP status code value.
This specification defines the following JWT VC Issuer Metadata configuration
parameters:

- 
            `issuer`

- REQUIRED. The Issuer identifier, which MUST be identical to the `iss`
value in the JWT.

            

          - 
            `jwks_uri`

- OPTIONAL. URL string referencing the Issuer's JSON Web Key (JWK) Set
[[RFC7517](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7517)] document which contains the Issuer's public keys. The value of
this field MUST point to a valid JWK Set document.

            

          - 
            `jwks`

- OPTIONAL. Issuer's JSON Web Key Set [[RFC7517](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC7517)] document value, which
contains the Issuer's public keys. The value of this field MUST be a JSON
object containing a valid JWK Set.

            

        
JWT VC Issuer Metadata MUST include either `jwks_uri` or `jwks` in their JWT VC
Issuer Metadata, but not both.
It is RECOMMENDED that the JWT contains a `kid` JWT header parameter that can
be used to look up the public key in the JWK Set included by value or referenced
in the JWT VC Issuer Metadata.
The following is a non-normative example of a JWT VC Issuer Metadata configuration
including `jwks`:

```
{
   "issuer":"https://example.com",
   "jwks":{
      "keys":[
         {
            "kid":"doc-signer-05-25-2022",
            "e":"AQAB",
            "n":"nj3YJwsLUFl9BmpAbkOswCNVx17Eh9wMO-_AReZwBqfaWFcfG
   HrZXsIV2VMCNVNU8Tpb4obUaSXcRcQ-VMsfQPJm9IzgtRdAY8NN8Xb7PEcYyk
   lBjvTtuPbpzIaqyiUepzUXNDFuAOOkrIol3WmflPUUgMKULBN0EUd1fpOD70p
   RM0rlp_gg_WNUKoW1V-3keYUJoXH9NztEDm_D2MQXj9eGOJJ8yPgGL8PAZMLe
   2R7jb9TxOCPDED7tY_TU4nFPlxptw59A42mldEmViXsKQt60s1SLboazxFKve
   qXC_jpLUt22OC6GUG63p-REw-ZOr3r845z50wMuzifQrMI9bQ",
            "kty":"RSA"
         }
      ]
   }
}
```

The following is a non-normative example of a JWT VC Issuer Metadata
configuration including `jwks_uri`:

```
{
   "issuer":"https://example.com",
   "jwks_uri":"https://jwt-vc-issuer.example.org/my_public_keys.jwks"
}
```

Additional JWT VC Issuer Metadata configuration parameters MAY also be used.


### 5.3. JWT VC Issuer Metadata Validation
The `issuer` value returned MUST be identical to the `iss` value of the
JWT. If these values are not identical, the data contained in the response
MUST NOT be used.
