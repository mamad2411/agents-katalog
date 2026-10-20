---
name: "mdoc-structure-function"
description: "Use when working with mDoc/ISO 18013-5 data structures. Covers: MSO (Mobile Security Object) structure, COSE_sign1, namespaces, element digests, presentation construction, selective disclosure mechanics, device auth methods (signature vs ECDH MAC), issuer auth, offline verification, and signed mDoc payload examples with decoded JSON."
sections:
  - "Structure to Function"
  - "[Data structure](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#data-structure)"
  - "[Function](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#function)"
  - "[Signed mDoc payload](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#signed-mdoc-payload)"
  - "[Branded mDoc](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#branded-mdoc)"
---

<!-- ARF version: MATTR-Learn-2025 -->
<!-- Tokens: ~3805 -->

# Structure to Function

To properly use mDocs in a digital trust ecosystem, one must gain a good understanding of their
structure, and how it relates to their function.
## [Data structure](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#data-structure)
### [From claims to an mDoc](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#from-claims-to-an-mdoc)
mDocs issuers ascertain verifiable information about holders they issue credentials to. This
information is referred to as *claims* and is stored in systems which are referred to as *claims
sources*. When these claims are issued in an mDoc they are grouped into *namespaces* to prevent
collision between claim names.
When creating a presentation from an mDoc and sharing it with a verifier, it only includes a subset
of the raw claims from the mDoc. These are the elements required by the verifier that the holder had
consented to disclose. By comparing these elements to the corresponding salted hashes in the Mobile
Security Object (MSO), the verifier can ascertain the claims' integrity.
The following diagram depicts the mDoc and Presentation architecture which includes the
aforementioned elements:

- MSO: A COSE_sign1 structure (CBOR standard for presenting digital signatures) comprising several
components:

- `Header` : Details the algorithm being used.

- `DSC` : The Document Signer Certificate (DSC) is included in the MSO and can be used
alongside the IACA certificate to verify the MSO signature.


- `Issuer Signature` : The signature of the mDoc’s issuer.
- Payload: The element signed by the DSC. It includes the following components:

- Device public key.
- Credential validity period.
- Metadata (key type, authorizations, etc.).
- Element Digest/Hash: An array that includes all the salted hashes of issuer signed
claims.


- `All Elements` : Includes the raw claims grouped by namespaces. Each element within a namespace
includes the claim name, claim value and salt value.

### [From an mDoc to a presentation](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#from-an-mdoc-to-a-presentation)
The following diagram depicts what elements are carried through when we creating a presentation from
an mDoc and sharing it with a verifier:

- `DSC` : Required to verify the MSO signature.
- `Selected Elements` : The subset of raw claims from the mDoc. These are the elements required by
the verifier and agreed to be shared by the holder. Comparing these elements to the
corresponding hashes in the MSO, the verifier can ascertain their integrity.
- `Device Auth` : A signature produced using the private key associated with the device public key
in the MSO over the unique session data.

## [Function](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#function)
The structure described above serves the following capabilities:
### [Salted hashed claims enable selective disclosure](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#salted-hashed-claims-enable-selective-disclosure)
The MSO is always included in an mDoc presentation to enable validating the issuer signature.
Selective disclosure would not be possible if all claims in the MSO were signed then revealed to
every verifier. The salted hashing of claims into the MSO ensures that it provides no data and only
proves that what is disclosed and presented by the holder was indeed signed by the issuer.
When a verifier is validating an mDoc presentation, they re-compute the hash/digest for each
revealed claim and its salt, and try to match it to the one referenced in the MSO. If the match is
successful then the integrity of the claim back to the issuer is proven. If they don’t match, the
value is rejected and the presentation is invalid. This structure enables the holder to selectively
disclose a subset of their credential claims, and the verifier to verify this subset of claims.
### [Salt values support unwanted disclosures protection](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#salt-values-support-unwanted-disclosures-protection)
Since hash functions are repeatable, brute forcing might enable verifiers to guess unrevealed claims
when their enumeration is very limited (for example nationality can only be a two letter country
code defined in [ISO 3166-1](https://www.iso.org/iso-3166-country-codes.html)).
To solve this, the issuer adds a unique random massive number (commonly referred to as *nonce* or
*salt*) to each claim value for every hash that is created. This means you can only reconstruct the
hashed claim if you have both the salt and the claim value:

### [Device Auth provides anti-cloning and replay protection](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#device-auth-provides-anti-cloning-and-replay-protection)
The `Device Auth` element authenticates that the device presenting the credential is the same one
that the credential was issued to.
When an issuer issues an mDoc, the device generates a private key that is locked to its hardware.
That same private key must be used whenever the credential is presented to a verifier, both
in-person and remotely (online). Assuming the private key is exclusively bound to a device, it
prevents anti-cloning, and the relying party can trust that the credential is both valid and is
presented by the intended device.
Device authentication can be implemented in one of two methods, both supported by the ISO/IEC
18013-5:2021 specification:

- **Signature authentication**: The holder uses the device key to produce a digital signature that
is included in the device’s response, authenticating the holder’s possession of the device key
to the verifier. This is considered a non-repudiable method.
- **ECDH-agreed Mac based authentication**: The holder and the verifier use their own private key
and the other parties public key to generate a mutually agreed key using ECDH (Elliptic Curve
Diffie Helman). This prevents scenarios where a verifier may attempt to share the response with
a 3rd party without the holder’s consent. Since both parties (the holder and the verifier) could
generate the same MAC, the verifier cannot prove to a 3rd party that it was the holder who
generated the MAC. This method is considered to be non-repudiable to the verifier, but it is
repudiable to a 3rd party as it can’t tell whether the MAC was produced by the holder or the
verifier.

Replay protection is achieved using the same mechanism by signing over the session transcript,
acting as a fingerprint of the current session between the verifier and the holder.
### [Issuer Auth enables offline verification](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#issuer-auth-enables-offline-verification)
The mDoc is constructed in a way that the verifier only needs the IACA’s certificate of the issuer
to verify a presented credential. Everything else (DSC, MSO) exists within the mDoc itself, enabling
offline verification as no internet access is required to retrieve any information.
### [Status field enables revocation checking](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#status-field-enables-revocation-checking)
[Revocable](/docs/issuance/revocation/overview#mdocs) mDocs include a status reference in their MSO payload. The standardized field name is `status`, though legacy credentials issued before adoption of Draft 14 of the Token Status List specification use `_status`. Both field names contain identical information and serve the same purpose. For more details, see [mDocs revocation](/docs/issuance/revocation/overview#mdocs).
## [Signed mDoc payload](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#signed-mdoc-payload)
Let's look into the structure of a signed mDoc issued by a MATTR VII tenant:
Signed mDoc example```
{
  "id": "8669f836-b3b2-43f3-aecd-d92187cb1cac",
  "encoded": "omppc3N1ZXJBdXRohEOhASahGCFZApcwggKTMIICOKADAgECAgpSc4u6ewLWeF9jMAoGCCqGSM49BAMCMC4xCzAJBgNVBAYTAkFVMR8wHQYDVQQDDBZsYWJzLm1hdHRybGFicy5jbyBJQUNBMB4XDTI0MDcyOTEwMTMwMVoXDTI1MTAyNzEwMTMwMVowOTELMAkGA1UE... [truncated]",
  "decoded": {
    "namespaces": {
      "org.iso.18013.5.1": [
        {
          "digestID": 1,
          "random": "XYGwWHUk5ugOnrIrivXZdQ==",
          "elementIdentifier": "sex",
          "elementValue": {
            "type": "string",
            "value": "1"
          }
        },
        {
          "digestID": 15,
          "random": "VHu6WoNegd/NwwUmKLfU6g==",
          "elementIdentifier": "portrait",
          "elementValue": {
            "type": "binary",
            "value": "iVBORw0KGgoAAAANSUhEUgAAAG8AAACPCAMAAADDX3XQAAAABGdBTUEAALGPC/xhBQAAAAFzUkdCAK7OHOkAAAAJcEhZcwAACxMAAAsTAQCanBgAAABIUExURa+uqbmMda6Ca6J2YAwIBhwTD5ZsVqqqpaOinpyblpSSjtGlkT0rIi0fGIpiTX1XQ8eZgkw3LF5CM4qJ... [truncated]"
          }
        },
        {
          "digestID": 4,
          "random": "5levHsGtTQiVO30tX/fSmg==",
          "elementIdentifier": "birth_date",
          "elementValue": {
            "type": "date",
            "value": "1990-04-30"
          }
        },
        {
          "digestID": 17,
          "random": "+gM3eo9JfRiiI5O8rcULrw==",
          "elementIdentifier": "given_name",
          "elementValue": {
            "type": "string",
            "value": "Connor Justin"
          }
        },
        {
          "digestID": 3,
          "random": "5wACvuuwC6fo3TXf/fb3bQ==",
          "elementIdentifier": "issue_date",
          "elementValue": {
            "type": "date",
            "value": "2024-01-01"
          }
        },
        {
          "digestID": 10,
          "random": "73TwdasU4qKtNarutPNAJw==",
          "elementIdentifier": "age_over_18",
          "elementValue": {
            "type": "string",
            "value": "true"
          }
        },
        {
          "digestID": 5,
          "random": "wa9hWf6bIkpRHSGyEvdqQw==",
          "elementIdentifier": "age_over_21",
          "elementValue": {
            "type": "string",
            "value": "true"
          }
        },
        {
          "digestID": 13,
          "random": "+UqiYYLdKafjOiK3u7CcGw==",
          "elementIdentifier": "expiry_date",
          "elementValue": {
            "type": "date",
            "value": "2035-12-30"
          }
        },
        {
          "digestID": 14,
          "random": "5NLYphEy1GcFbe0Bd4PKkg==",
          "elementIdentifier": "family_name",
          "elementValue": {
            "type": "string",
            "value": "Jackman"
          }
        },
        {
          "digestID": 0,
          "random": "9dioUYwBh5JD/6OsXWvi1Q==",
          "elementIdentifier": "resident_city",
          "elementValue": {
            "type": "string",
            "value": "Capitol"
          }
        },
        {
          "digestID": 9,
          "random": "1CuwU/Pz98Q1tKswtKTVRQ==",
          "elementIdentifier": "resident_state",
          "elementValue": {
            "type": "string",
            "value": "Montcliff"
          }
        },
        {
          "digestID": 2,
          "random": "ESTI7ty3CWJWJHF4S7c+UA==",
          "elementIdentifier": "document_number",
          "elementValue": {
            "type": "string",
            "value": "DL245198"
          }
        },
        {
          "digestID": 8,
          "random": "3QF6v9KTgB+ZvPPb217X/g==",
          "elementIdentifier": "issuing_country",
          "elementValue": {
            "type": "string",
            "value": "AU"
          }
        },
        {
          "digestID": 12,
          "random": "iVuyMlADYeONkhySnLS2Qg==",
          "elementIdentifier": "resident_address",
          "elementValue": {
            "type": "string",
            "value": "243B Main Street"
          }
        },
        {
          "digestID": 6,
          "random": "+QkFpEozov7qzBAmKPsyzQ==",
          "elementIdentifier": "resident_country",
          "elementValue": {
            "type": "string",
            "value": "AU"
          }
        },
        {
          "digestID": 16,
          "random": "o6qXfzgTvHsXBFLqQ5aUQA==",
          "elementIdentifier": "issuing_authority",
          "elementValue": {
            "type": "string",
            "value": "Montcliff DMV"
          }
        },
        {
          "digestID": 11,
          "random": "Jhh+KbsegrYbNMZWTLnP3A==",
          "elementIdentifier": "driving_priviledges",
          "elementValue": {
            "type": "string",
            "value": "[   {     \"vehicle_category_code\": \"B\",     \"issue_date\": \"2022-10-10\",     \"expiry_date\": \"2032-10-10\"   } ]"
          }
        },
        {
          "digestID": 7,
          "random": "jx38q9nJPTYXwRBzzKsvdg==",
          "elementIdentifier": "un_distinguishing_sign",
          "elementValue": {
            "type": "string",
            "value": "AU"
          }
        }
      ]
    },
    "issuerAuth": "hEOhASahGCFZApcwggKTMIICOKADAgECAgpSc4u6ewLWeF9jMAoGCCqGSM49BAMCMC4xCzAJBgNVBAYTAkFVMR8wHQYDVQQDDBZsYWJzLm1hdHRybGFicy5jbyBJQUNBMB4XDTI0MDcyOTEwMTMwMVoXDTI1MTAyNzEwMTMwMVowOTELMAkGA1UEBhMCQVUxKjAoBgNV... [truncated]"
  }
}
```

- `id` : Unique identifier of this credential.
- `encoded` : Encoded version of the credential, represented as a base64 string.
- `decoded` : Decoded version of the credential:

- `namespaces` : Each namespace corresponds to a group of claims included in the credential.
These can be claims that are part of a specific standard, jurisdiction or any other
reference.

- `org.iso.18013.5.1` : This namespace includes claims that comply with the
[ISO/IEC 18013-5 standard](https://www.iso.org/standard/69084.html). Each element in
this object represents a claim and includes the following fields:

- `digestID` : Serial number identifying the claim within this namespace.
- `random` : This is the random value (nonce/salt) added to each claim when it is
encoded. This enables
[unwanted disclosures protection](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#salt-values-support-unwanted-disclosures-protection).
- `elementIdentifier` : The identifier of this claim as per
[ISO/IEC 18013-5 standard](https://www.iso.org/standard/69084.html).
- `elementValue` :

- `type` : Claim data type.
- `value` : Claim value.


- `issuerAuth` : This is the digital signature represented as a COSE_sign1 structure. It
includes different details regarding the encrypton algorithm, certificates and public
keys.


## [Branded mDoc](https://learn.mattr.global/docs/concepts/mdocs/structure-to-function#branded-mdoc)
The following image depicts how the credential above would look like in the holder's digital wallet:
