---
name: "sd-jwt-verification"
description: "Use when implementing SD-JWT verification or JWS serialization. Covers: SD-JWT verification, holder processing, verifier verification, JWS JSON serialization formats."
sections:
  - "7. Verification and Processing"
  - "7.1. Verification of the SD-JWT"
  - "7.2. Processing by the Holder"
  - "7.3. Verification by the Verifier"
  - "8. JWS JSON Serialization"
  - "8.1. New Unprotected Header Parameters"
  - "8.2. Flattened JSON Serialization"
  - "8.3. General JSON Serialization"
  - "8.4. Verification of the JWS JSON Serialized SD-JWT"
---

<!-- ARF version: RFC-9901 -->
<!-- Tokens: ~5953 -->

## 7. Verification and Processing


### 7.1. Verification of the SD-JWT
Upon receiving an SD-JWT, either directly or as a component of an SD-JWT+KB, a Holder
or Verifier needs to ensure that:

- the Issuer-signed JWT is valid, and

          - all Disclosures are valid and correspond to a respective digest value in the Issuer-signed JWT (directly in the payload or recursively included in the contents of other Disclosures).

        
The Holder or the Verifier MUST perform the following checks when receiving
an SD-JWT to validate the SD-JWT and extract the payload:

- Separate the SD-JWT into the Issuer-signed JWT and the Disclosures (if any).

          - 
            Validate the Issuer-signed JWT:

- Ensure that the used signing algorithm was deemed secure for the application. Refer to [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)], Sections [3.1](https://rfc-editor.org/rfc/rfc8725#section-3.1) and [3.2](https://rfc-editor.org/rfc/rfc8725#section-3.2) for details. The "none" algorithm MUST NOT be accepted.

              - Validate the signature over the Issuer-signed JWT per [Section 5.2](https://rfc-editor.org/rfc/rfc7515#section-5.2) of [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)].

              - Validate the Issuer and that the signing key belongs to this Issuer.

              - Check that the `_sd_alg` claim value is understood and the hash algorithm is deemed secure according to the Holder or Verifier's policy (see [Section 4.1.1](https://www.rfc-editor.org/rfc/rfc9901.html#hash_function_claim)).

            

          - 
            Process the Disclosures and embedded digests in the Issuer-signed JWT as follows:

- 
                For each Disclosure provided:

- Calculate the digest over the base64url-encoded string as described in [Section 4.2.3](https://www.rfc-editor.org/rfc/rfc9901.html#hashing_disclosures).

                

              - 
                (*) Identify all embedded digests in the Issuer-signed JWT as follows:

- Find all objects having an `_sd` key that refers to an array of strings.

                  - Find all array elements that are objects with one key, that key being `...` and referring to a string.

                

              - 
                (**) For each embedded digest found in the previous step:

- Compare the value with the digests calculated previously and find the matching Disclosure. If no such Disclosure can be found, the digest MUST be ignored.

                  - 
                    If the digest was found in an object's `_sd` key:

- If the contents of the respective Disclosure is not a JSON array of three elements (salt, claim name, claim value), the SD-JWT MUST be rejected.

                      - If the claim name is `_sd` or `...`, the SD-JWT MUST be rejected.

                      - If the claim name already exists at the level of the `_sd` key, the SD-JWT MUST be rejected.

                      - Insert, at the level of the `_sd` key, a new claim using the claim name and claim value from the Disclosure.

                      - Recursively process the value using the steps described in (*) and (**).

                    

                  - 
                    If the digest was found in an array element:

- If the contents of the respective Disclosure is not a JSON array of two elements (salt, value), the SD-JWT MUST be rejected.

                      - Replace the array element with the value from the Disclosure.

                      - Recursively process the value using the steps described in (*) and (**).

                    

                

              - Remove all array elements for which the digest was not found in the previous step.

              - Remove all `_sd` keys and their contents from the Issuer-signed JWT payload. If this results in an object with no properties, it should be represented as an empty object `{}`.

              - Remove the claim `_sd_alg` from the SD-JWT payload.

            

          - If any digest value is encountered more than once in the Issuer-signed JWT payload (directly or recursively via other Disclosures), the SD-JWT MUST be rejected.

          - If any Disclosure was not referenced by digest value in the Issuer-signed JWT (directly or recursively via other Disclosures), the SD-JWT MUST be rejected.

          - Check that the SD-JWT is valid using claims such as `nbf`, `exp`, and `aud` in the processed payload, if present. If a required validity-controlling claim is missing (see [Section 9.7](https://www.rfc-editor.org/rfc/rfc9901.html#sd-validity-claims)), the SD-JWT MUST be rejected.

        
If any step fails, the SD-JWT is not valid, and processing MUST be aborted. Otherwise, the JSON document resulting from the preceding processing and verification steps, herein referred to as the "Processed SD-JWT Payload", can be made available to the application to be used for its intended purpose.

          Note that these processing steps do not yield any guarantees to the Holder about having received a complete set of Disclosures. That is, for some digest values in the Issuer-signed JWT (which are not decoy digests), there may be no corresponding Disclosures, for example, if the message from the Issuer was truncated.
It is up to the Holder how to maintain the mapping between the Disclosures and the plaintext claim values to be able to display them to the user when needed.


### 7.2. Processing by the Holder
The Issuer provides the Holder with an SD-JWT, not an SD-JWT+KB.  If the Holder
receives an SD-JWT+KB, it MUST be rejected.
When receiving an SD-JWT, the Holder MUST do the following:

- Process the SD-JWT as defined in [Section 7.1](https://www.rfc-editor.org/rfc/rfc9901.html#sd_jwt_verification) to validate it and extract the payload.

          - Ensure that the contents of claims in the payload are acceptable (depending on the application; for example, check that any values the Holder can check are correct).

        
For presentation to a Verifier, the Holder MUST perform the following (or equivalent) steps (in addition to the checks described in [Section 7.1](https://www.rfc-editor.org/rfc/rfc9901.html#sd_jwt_verification) performed after receiving the SD-JWT):

- Decide which Disclosures to release to the Verifier, obtaining consent if necessary (note that if and how consent is attained is out of scope for this document).

          - 
            Verify that each selected Disclosure satisfies one of the two following conditions:

- The hash of the Disclosure is contained in the Issuer-signed JWT claims.

              - The hash of the Disclosure is contained in the claim value of another selected Disclosure.

            

          - Assemble the SD-JWT, including the Issuer-signed JWT and the selected Disclosures (see [Section 4](https://www.rfc-editor.org/rfc/rfc9901.html#data_formats) for the format).

          - 
            If Key Binding is not required:

- Send the SD-JWT to the Verifier.

            

          - 
            If Key Binding is required:

- Create a Key Binding JWT tied to the SD-JWT.

              - Assemble the SD-JWT+KB by concatenating the SD-JWT and the Key Binding JWT.

              - Send the SD-JWT+KB to the Verifier.

            

        


### 7.3. Verification by the Verifier
Upon receiving a presentation from a Holder, in the form of either an SD-JWT or
an SD-JWT+KB, in addition to the checks described in [Section 7.1](https://www.rfc-editor.org/rfc/rfc9901.html#sd_jwt_verification), Verifiers need to ensure that

- if Key Binding is required, then the Holder has provided an SD-JWT+KB, and

          - the Key Binding JWT is signed by the Holder and valid.

        
To this end, Verifiers MUST follow the following steps (or equivalent):

- Determine if Key Binding is to be checked according to the Verifier's policy
for the use case at hand. This decision MUST NOT be based on whether
or not a Key Binding JWT is provided by the Holder. Refer to [Section 9.5](https://www.rfc-editor.org/rfc/rfc9901.html#key_binding_security) for
details.

          - If Key Binding is required and the Holder has provided an SD-JWT (without Key Binding), the Verifier MUST reject the presentation.

          - If the Holder has provided an SD-JWT+KB, parse it into an SD-JWT and a Key Binding JWT.

          - Process the SD-JWT as defined in [Section 7.1](https://www.rfc-editor.org/rfc/rfc9901.html#sd_jwt_verification) to validate the presentation and extract the payload.

          - 
            If Key Binding is required:

- Determine the public key for the Holder from the SD-JWT (see [Section 4.1.2](https://www.rfc-editor.org/rfc/rfc9901.html#key_binding)).

              - Ensure that a signing algorithm was used that was deemed secure for the application. Refer to [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)], Sections [3.1](https://rfc-editor.org/rfc/rfc8725#section-3.1) and [3.2](https://rfc-editor.org/rfc/rfc8725#section-3.2) for details. The "none" algorithm MUST NOT be accepted.

              - Validate the signature over the Key Binding JWT per [Section 5.2](https://rfc-editor.org/rfc/rfc7515#section-5.2) of [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)].

              - Check that the `typ` of the Key Binding JWT is `kb+jwt` (see [Section 4.3](https://www.rfc-editor.org/rfc/rfc9901.html#kb-jwt)).

              - Check that the creation time of the Key Binding JWT, as determined by the `iat` claim, is within an acceptable window.

              - Determine that the Key Binding JWT is bound to the current transaction and was created for this Verifier (replay detection) by validating `nonce` and `aud` claims.

              - Calculate the digest over the Issuer-signed JWT and Disclosures as defined in [Section 4.3.1](https://www.rfc-editor.org/rfc/rfc9901.html#integrity-protection-of-the-presentation) and verify that it matches the value of the `sd_hash` claim in the Key Binding JWT.

              - Check that the Key Binding JWT is a valid JWT in all other respects, per [[RFC7519](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7519)] and [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)].

            

        
If any step fails, the presentation is not valid and processing MUST be aborted.
Otherwise, the Processed SD-JWT Payload can be passed to the application to be used for the intended purpose.

---

## 8. JWS JSON Serialization
This section describes an alternative format for SD-JWTs and SD-JWT+KBs using the JWS JSON
Serialization from [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)]. Supporting this format is OPTIONAL.


### 8.1. New Unprotected Header Parameters
For both the General and Flattened JSON Serialization, the SD-JWT or SD-JWT+KB is represented
as a JSON object according to [Section 7.2](https://rfc-editor.org/rfc/rfc7515#section-7.2) of [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)]. The following new
unprotected header parameters are defined:

          
`disclosures`:
          An array of strings where each element is an individual
Disclosure as described in [Section 4.2](https://www.rfc-editor.org/rfc/rfc9901.html#creating_disclosures).

          

`kb_jwt`:
          Present only in an SD-JWT+KB, the Key Binding JWT as described in [Section 4.3](https://www.rfc-editor.org/rfc/rfc9901.html#kb-jwt).

        

In an SD-JWT+KB, `kb_jwt` MUST be present when using the JWS JSON Serialization,
and the digest in the `sd_hash` claim MUST be computed over the SD-JWT as described
in [Section 4.3.1](https://www.rfc-editor.org/rfc/rfc9901.html#integrity-protection-of-the-presentation). This means that even when using
the JWS JSON Serialization, the representation as a regular SD-JWT Compact Serialization MUST be
created temporarily to calculate the digest. In detail, the SD-JWT Compact Serialization part is built
by concatenating the protected header, the payload, and the signature of the JWS
JSON serialized SD-JWT using a `.` character as a separator, and using the
Disclosures from the `disclosures` member of the unprotected header.
Unprotected headers other than `disclosures` are not covered by the digest, and
therefore, as usual, are not protected against tampering.


### 8.2. Flattened JSON Serialization
In the case of Flattened JSON Serialization, there is only one unprotected
header.
The following is a non-normative example of a JWS JSON serialized SD-JWT as
issued using the Flattened JSON Serialization:

```
{
  "header": {
    "disclosures": [
      "WyIyR0xDNDJzS1F2ZUNmR2ZyeU5STjl3IiwgInN1YiIsICJqb2huX2RvZV80M
        iJd",
      "WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImdpdmVuX25hbWUiLCAiSm9ob
        iJd",
      "WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgImZhbWlseV9uYW1lIiwgIkRvZ
        SJd",
      "WyJlSThaV205UW5LUHBOUGVOZW5IZGhRIiwgImJpcnRoZGF0ZSIsICIxOTQwL
        TAxLTAxIl0"
    ]
  },
  "payload": "eyJfc2QiOiBbIjRIQm42YUlZM1d0dUdHV1R4LXFVajZjZGs2V0JwWn
    lnbHRkRmF2UGE3TFkiLCAiOHNtMVFDZjAyMXBObkhBQ0k1c1A0bTRLWmd5Tk9PQV
    ljVGo5SE5hQzF3WSIsICJjZ0ZkaHFQbzgzeFlObEpmYWNhQ2FhN3VQOVJDUjUwVk
    U1UjRMQVE5aXFVIiwgImpNQ1hWei0tOWI4eDM3WWNvRGZYUWluencxd1pjY2NmRl
    JCQ0ZHcWRHMm8iXSwgImlzcyI6ICJodHRwczovL2lzc3Vlci5leGFtcGxlLmNvbS
    IsICJpYXQiOiAxNjgzMDAwMDAwLCAiZXhwIjogMTg4MzAwMDAwMCwgIl9zZF9hbG
    ciOiAic2hhLTI1NiIsICJjbmYiOiB7Imp3ayI6IHsia3R5IjogIkVDIiwgImNydi
    I6ICJQLTI1NiIsICJ4IjogIlRDQUVSMTladnUzT0hGNGo0VzR2ZlNWb0hJUDFJTG
    lsRGxzN3ZDZUdlbWMiLCAieSI6ICJaeGppV1diWk1RR0hWV0tWUTRoYlNJaXJzVm
    Z1ZWNDRTZ0NGpUOUYySFpRIn19fQ",
  "protected":
    "eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0In0",
  "signature": "3oOtvPxU3QdDWUmfGexVB5rWyON2f1atg5rL825bvvD1g7ywjKDK
    y2UHqHoH2QS4FA99JbG5qnlqFaGXFChfjQ"
}
```

The following is an SD-JWT+KB with two Disclosures:

```
{
  "header": {
    "disclosures": [
      "WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgImZhbWlseV9uYW1lIiwgIkRvZ
        SJd",
      "WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImdpdmVuX25hbWUiLCAiSm9ob
        iJd"
    ],
    "kb_jwt": "eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImtiK2p3dCJ9.eyJub25j
      ZSI6ICIxMjM0NTY3ODkwIiwgImF1ZCI6ICJodHRwczovL3ZlcmlmaWVyLmV4YW
      1wbGUub3JnIiwgImlhdCI6IDE3NDg1MzcyNDQsICJzZF9oYXNoIjogIlZqdFBz
      Z1pwUVRSeEtKdkRwU0otblhsWktFOVo5TGdENEZ5Q3d3b05NUncifQ.GrDvJ2j
      hYNmUvqdwVEIrxeTFEuI5qKSM7I6P95JmA6Wko-FBB5vPGQn0wvmdgjLCE2iDR
      h1r82zchjmABQ3V8w"
  },
  "payload": "eyJfc2QiOiBbIjRIQm42YUlZM1d0dUdHV1R4LXFVajZjZGs2V0JwWn
    lnbHRkRmF2UGE3TFkiLCAiOHNtMVFDZjAyMXBObkhBQ0k1c1A0bTRLWmd5Tk9PQV
    ljVGo5SE5hQzF3WSIsICJjZ0ZkaHFQbzgzeFlObEpmYWNhQ2FhN3VQOVJDUjUwVk
    U1UjRMQVE5aXFVIiwgImpNQ1hWei0tOWI4eDM3WWNvRGZYUWluencxd1pjY2NmRl
    JCQ0ZHcWRHMm8iXSwgImlzcyI6ICJodHRwczovL2lzc3Vlci5leGFtcGxlLmNvbS
    IsICJpYXQiOiAxNjgzMDAwMDAwLCAiZXhwIjogMTg4MzAwMDAwMCwgIl9zZF9hbG
    ciOiAic2hhLTI1NiIsICJjbmYiOiB7Imp3ayI6IHsia3R5IjogIkVDIiwgImNydi
    I6ICJQLTI1NiIsICJ4IjogIlRDQUVSMTladnUzT0hGNGo0VzR2ZlNWb0hJUDFJTG
    lsRGxzN3ZDZUdlbWMiLCAieSI6ICJaeGppV1diWk1RR0hWV0tWUTRoYlNJaXJzVm
    Z1ZWNDRTZ0NGpUOUYySFpRIn19fQ",
  "protected":
    "eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0In0",
  "signature": "3oOtvPxU3QdDWUmfGexVB5rWyON2f1atg5rL825bvvD1g7ywjKDK
    y2UHqHoH2QS4FA99JbG5qnlqFaGXFChfjQ"
}
```


### 8.3. General JSON Serialization
In the case of General JSON Serialization, there are multiple unprotected
headers (one per signature). If present, `disclosures` and `kb_jwt` MUST be
included in the first unprotected header and MUST NOT be present in any
following unprotected headers.
The following is a non-normative example of a presentation of a JWS JSON
serialized SD-JWT, including a Key Binding JWT using the General JSON
Serialization:

```
{
  "payload": "eyJfc2QiOiBbIjRIQm42YUlZM1d0dUdHV1R4LXFVajZjZGs2V0JwWn
    lnbHRkRmF2UGE3TFkiLCAiOHNtMVFDZjAyMXBObkhBQ0k1c1A0bTRLWmd5Tk9PQV
    ljVGo5SE5hQzF3WSIsICJjZ0ZkaHFQbzgzeFlObEpmYWNhQ2FhN3VQOVJDUjUwVk
    U1UjRMQVE5aXFVIiwgImpNQ1hWei0tOWI4eDM3WWNvRGZYUWluencxd1pjY2NmRl
    JCQ0ZHcWRHMm8iXSwgImlzcyI6ICJodHRwczovL2lzc3Vlci5leGFtcGxlLmNvbS
    IsICJpYXQiOiAxNjgzMDAwMDAwLCAiZXhwIjogMTg4MzAwMDAwMCwgIl9zZF9hbG
    ciOiAic2hhLTI1NiIsICJjbmYiOiB7Imp3ayI6IHsia3R5IjogIkVDIiwgImNydi
    I6ICJQLTI1NiIsICJ4IjogIlRDQUVSMTladnUzT0hGNGo0VzR2ZlNWb0hJUDFJTG
    lsRGxzN3ZDZUdlbWMiLCAieSI6ICJaeGppV1diWk1RR0hWV0tWUTRoYlNJaXJzVm
    Z1ZWNDRTZ0NGpUOUYySFpRIn19fQ",
  "signatures": [
    {
      "header": {
        "disclosures": [
          "WyI2SWo3dE0tYTVpVlBHYm9TNXRtdlZBIiwgImZhbWlseV9uYW1lIiwgI
            kRvZSJd",
          "WyJlbHVWNU9nM2dTTklJOEVZbnN4QV9BIiwgImdpdmVuX25hbWUiLCAiS
            m9obiJd"
        ],
        "kid": "issuer-key-1",
        "kb_jwt": "eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImtiK2p3dCJ9.eyJu
          b25jZSI6ICIxMjM0NTY3ODkwIiwgImF1ZCI6ICJodHRwczovL3ZlcmlmaW
          VyLmV4YW1wbGUub3JnIiwgImlhdCI6IDE3NDg1MzcyNDQsICJzZF9oYXNo
          IjogInFieUlXUDNwaFZneEVzRFJpd2R3OVc2QkozZHhpUEx1bWNZcFBidT
          RFYjgifQ.VyZqxaVHh1XE6M-kuax_7Laq42uFDrx17lLG2jluyKgy_PqC8
          5z4DVpISdMZDdSANGs-0zN2N7xnM-E1Pg0sOw"
      },
      "protected":
        "eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0In0",
      "signature": "dz1N3uvhVHJjldyXwppmBLieTj0vuBMbzL06rnrLIuxEQb9B
        HoIOwGrWh-UadW4orRpEiEtjf7xyHDONMJ6tBw"
    },
    {
      "header": {
        "kid": "issuer-key-2"
      },
      "protected":
        "eyJhbGciOiAiRVMyNTYiLCAidHlwIjogImV4YW1wbGUrc2Qtand0In0",
      "signature": "kuXio_U88RH_-fihAPET4AFUjj0BpxsT6yddMFIr6pfHKtAe
        0FOJNWQxU42rfnORuNQNTgGsf2A8LjEba5inNg"
    }
  ]
}
```


### 8.4. Verification of the JWS JSON Serialized SD-JWT
Verification of the JWS JSON serialized SD-JWT follows the rules defined in
[Section 3.4](https://www.rfc-editor.org/rfc/rfc9901.html#verification), except for the following aspects:

- The SD-JWT or SD-JWT+KB does not need to be split into component parts and the Disclosures
can be found in the `disclosures` member of the unprotected header.

          - To verify the digest in `sd_hash` in the Key Binding JWT of an SD-JWT+KB, the Verifier MUST
assemble the string to be hashed as described in
[Section 8.1](https://www.rfc-editor.org/rfc/rfc9901.html#json_serialization_unprotected_headers).
