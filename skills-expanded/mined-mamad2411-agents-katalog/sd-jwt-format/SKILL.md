---
name: "sd-jwt-format"
description: "Use when working with SD-JWT data formats. Covers: SD-JWT and SD-JWT+KB structure, disclosures, salt/hash mechanisms, and decoy digests."
sections:
  - "3. Concepts"
  - "3.1. SD-JWT and Disclosures"
  - "3.2. Disclosing to a Verifier"
  - "3.3. Optional Key Binding"
  - "3.4. Verification"
  - "4. SD-JWT and SD-JWT+KB Data Formats"
  - "4.1. Issuer-Signed JWT"
  - "4.2. Disclosures"
  - "4.3. Key Binding JWT"
---

<!-- ARF version: RFC-9901 -->
<!-- Tokens: ~7710 -->

## 3. Concepts
This section describes SD-JWTs with their respective Disclosures and Key Binding at a
conceptual level, abstracting from the data formats described in [Section 4](https://www.rfc-editor.org/rfc/rfc9901.html#data_formats).


### 3.1. SD-JWT and Disclosures
An SD-JWT, at its core, is a digitally signed JSON document containing digests over the selectively disclosable claims with the Disclosures outside the document. Disclosures can be omitted without breaking the signature, and modifications to them can be detected. Selectively disclosable claims can be individual object properties (name/value pairs) or array elements.
Each digest value ensures the integrity of, and maps to, the respective Disclosure.  Digest values are calculated using a hash function over the Disclosures, each of which contains a cryptographically secure random salt, the claim name (only when the claim is an object property), and the claim value. The Disclosures are sent to the Holder with the SD-JWT in the format defined in [Section 4](https://www.rfc-editor.org/rfc/rfc9901.html#data_formats).
When presenting an SD-JWT to a Verifier, the Holder only includes the Disclosures for the claims that it wants to reveal to that Verifier.
An SD-JWT MAY also contain cleartext claims that are always disclosed to the Verifier.


### 3.2. Disclosing to a Verifier
To disclose to a Verifier a subset of the SD-JWT claim values, a Holder sends only the Disclosures of those selectively released claims to the Verifier as part of the SD-JWT.


### 3.3. Optional Key Binding
Key Binding is an optional feature. When Key Binding is required by the use case, the SD-JWT MUST contain information about the key material controlled by the Holder.

          Note: How the public key is included in SD-JWT is described in [Section 4.1.2](https://www.rfc-editor.org/rfc/rfc9901.html#key_binding).

When a Verifier requires Key Binding, the Holder presents an SD-JWT+KB, consisting of an SD-JWT as well as a Key Binding JWT tied to that SD-JWT.
The Key Binding JWT encodes a signature by the Holder's private key over

- a hash of the SD-JWT,

          - a nonce to ensure the freshness of the signature, and

          - an audience value to indicate the intended Verifier for the document.

        
Details of the format of Key Binding JWTs are described in [Section 4.3](https://www.rfc-editor.org/rfc/rfc9901.html#kb-jwt).


### 3.4. Verification
At a high level, the Verifier

- receives either an SD-JWT or an SD-JWT+KB from the Holder,

          - verifies the signature on the SD-JWT (or the SD-JWT inside the SD-JWT+KB) using the Issuer's public key,

          - verifies the signature on the KB-JWT using the public key included (or referenced) in the SD-JWT, if the Verifier's policy requires Key Binding, and

          - calculates the digests over the Holder-Selected Disclosures and verifies that each digest is contained in the SD-JWT.

        
The detailed algorithm is described in [Section 7.3](https://www.rfc-editor.org/rfc/rfc9901.html#verifier_verification).

---

## 4. SD-JWT and SD-JWT+KB Data Formats
An SD-JWT is composed of

- an Issuer-signed JWT, and

        - zero or more Disclosures.

      
An SD-JWT+KB is composed of

- an SD-JWT (i.e., an Issuer-signed JWT and zero or more Disclosures), and

        - a Key Binding JWT.

      
The Issuer-signed JWT, Disclosures, and Key Binding JWT are explained in Sections
[4.1](https://www.rfc-editor.org/rfc/rfc9901.html#iss-signed-jwt), [4.2](https://www.rfc-editor.org/rfc/rfc9901.html#creating_disclosures), and [4.3](https://www.rfc-editor.org/rfc/rfc9901.html#kb-jwt), respectively.
The compact serialized format for the SD-JWT is the concatenation of each part delineated with a single tilde ('~') character as follows, where "D.1" to "D.N" represent the respective Disclosures:

```
<Issuer-signed JWT>~<D.1>~<D.2>~...~<D.N>~
```

The order of the concatenated parts MUST be the Issuer-signed JWT,
a tilde character, zero or more Disclosures each followed by a tilde character,
and lastly the optional Key Binding JWT.
In the case that there is no Key Binding JWT, the last element MUST be an empty
string and the last separating tilde character MUST NOT be omitted.
The serialized format for an SD-JWT+KB extends the SD-JWT format by concatenating a Key Binding JWT.

```
<Issuer-signed JWT>~<D.1>~<D.2>~...~<D.N>~<KB-JWT>
```

The two formats can be distinguished by the final `~` character that is present
on an SD-JWT.  A Verifier that expects an SD-JWT MUST verify that the final
tilde-separated component is empty.  A Verifier that expects an SD-JWT+KB MUST verify
that its final tilde-separated component is a valid KB-JWT.
The Disclosures are linked to the Issuer-signed JWT through the
digest values included therein.
When issuing to a Holder, the Issuer includes all the relevant Disclosures in the SD-JWT.
When presenting to a Verifier, the Holder sends only the selected set of the Disclosures in the SD-JWT.
The Holder MAY send any subset of the Disclosures to the Verifier, i.e.,
none, some, or all Disclosures. For data that the Holder does not want to reveal
to the Verifier, the Holder MUST NOT send Disclosures or reveal the salt values in any
other way. A Holder MUST NOT send a Disclosure that was not included in the issued
SD-JWT or send a Disclosure more than once.
To further illustrate the SD-JWT format, the following examples show a few different
SD-JWT permutations, both with and without various constituent parts.
An SD-JWT without Disclosures:

```
<Issuer-signed JWT>~
```

An SD-JWT with Disclosures:

```
<Issuer-signed JWT>~<Disclosure 1>~<Disclosure N>~
```

An SD-JWT+KB without Disclosures:

```
<Issuer-signed JWT>~<KB-JWT>
```

An SD-JWT+KB with Disclosures:

```
<Issuer-signed JWT>~<Disclosure 1>~<Disclosure N>~<KB-JWT>
```

As an alternative illustration of the SD-JWT format, ABNF [[RFC5234](https://www.rfc-editor.org/rfc/rfc9901.html#RFC5234)] for the
SD-JWT, SD-JWT+KB, and various constituent parts is provided here (for those who celebrate):

```
ALPHA = %x41-5A / %x61-7A ; A-Z / a-z
DIGIT = %x30-39 ; 0-9
BASE64URL = 1*(ALPHA / DIGIT / "-" / "_")
JWT = BASE64URL "." BASE64URL "." BASE64URL
DISCLOSURE = BASE64URL
SD-JWT = JWT "~" *(DISCLOSURE "~")
KB-JWT = JWT
SD-JWT-KB = SD-JWT KB-JWT
```


### 4.1. Issuer-Signed JWT
An SD-JWT has a JWT component that MUST be signed using the Issuer's private
key. It MUST NOT use the `none` algorithm.
The payload of an SD-JWT is a JSON object according to the following rules:

- The payload MAY contain the `_sd_alg` key described in [Section 4.1.1](https://www.rfc-editor.org/rfc/rfc9901.html#hash_function_claim).

          - The payload MAY contain one or more digests of Disclosures to enable selective disclosure of the respective claims, created and formatted as described in [Section 4.2](https://www.rfc-editor.org/rfc/rfc9901.html#creating_disclosures).

          - The payload MAY contain one or more decoy digests to obscure the actual number of claims in the SD-JWT, created and formatted as described in [Section 4.2.5](https://www.rfc-editor.org/rfc/rfc9901.html#decoy_digests).

          - The payload MAY contain one or more permanently disclosed claims.

          - The payload MAY contain the Holder's public key(s) or reference(s) thereto, as explained in [Section 4.1.2](https://www.rfc-editor.org/rfc/rfc9901.html#key_binding).

          - The payload MAY contain further claims such as `iss`, `iat`, etc. as defined or required by the application using SD-JWTs.

          - The payload MUST NOT contain the claims `_sd` or `...` except for the purpose of conveying digests as described in Sections [4.2.4.1](https://www.rfc-editor.org/rfc/rfc9901.html#embedding_object_properties) and [4.2.4.2](https://www.rfc-editor.org/rfc/rfc9901.html#embedding_array_elements), respectively.

        
The same digest value MUST NOT appear more than once in the SD-JWT.
Application and profiles of SD-JWT SHOULD be explicitly typed. See [Section 9.11](https://www.rfc-editor.org/rfc/rfc9901.html#explicit_typing) for more details.
It is the Issuer who decides which claims are selectively disclosable by the Holder and which are not. Claims MAY be included as plaintext as well, e.g., if hiding the particular claims from the Verifier is not required in the intended use case. See [Section 9.7](https://www.rfc-editor.org/rfc/rfc9901.html#sd-validity-claims) for considerations on making validity-controlling claims such as `exp` selectively disclosable.
Claims that are not selectively disclosable are included in the SD-JWT in plaintext just as they would be in any other JSON structure.


#### 4.1.1. Hash Function Claim
The claim `_sd_alg` indicates the hash algorithm used by the Issuer to generate
the digests as described in [Section 4.2](https://www.rfc-editor.org/rfc/rfc9901.html#creating_disclosures). When used, this claim MUST
appear at the top level of the SD-JWT payload. It
MUST NOT be used in any object nested within the payload. If the  `_sd_alg`
claim is not present at the top level, a default value of `sha-256` MUST be used.
This claim value is a case-sensitive string with the hash algorithm identifier.
The hash algorithm identifier MUST be a hash algorithm value from the "Hash Name
String" column in the "Named Information Hash Algorithm Registry"
[[Hash.Algs](https://www.rfc-editor.org/rfc/rfc9901.html#Hash.Algs)] or a value defined in another specification and/or
profile of this specification.
To promote interoperability, implementations MUST support the `sha-256` hash
algorithm.
See [Section 9](https://www.rfc-editor.org/rfc/rfc9901.html#security_considerations) for requirements regarding entropy of the salt,
minimum length of the salt, and choice of a hash algorithm.


#### 4.1.2. Key Binding
If the Issuer wants to enable Key Binding, it includes a public key
associated with the Holder, or a reference thereto, using the `cnf` claim as defined in [[RFC7800](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7800)].
The `jwk` confirmation method, as defined in [Section 3.2](https://rfc-editor.org/rfc/rfc7800#section-3.2) of [[RFC7800](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7800)], is
suggested for doing so, however, other confirmation methods can be used.

            Note that, as was stated in [[RFC7800](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7800)],
if an application needs to represent multiple proof-of-possession
keys in the same SD-JWT, one way to achieve this is to use other
claim names, in addition to `cnf`, to hold the additional proof-of-possession key information.

It is outside the scope of this document to describe how the Holder key pair is
established. For example, the Holder MAY create a key pair and provide a public key to the Issuer,
the Issuer MAY create the key pair for the Holder, or
Holder and Issuer MAY use pre-established key material.

            Note: The examples throughout this document use the `cnf` claim with the `jwk` member to include
the raw public key by value in SD-JWT.


### 4.2. Disclosures
Disclosures are created differently depending on whether a claim is an object property (name/value pair) or an array element.

- For a claim that is an object property, the Issuer creates a Disclosure as described in [Section 4.2.1](https://www.rfc-editor.org/rfc/rfc9901.html#disclosures_for_object_properties).

          - For a claim that is an array element, the Issuer creates a Disclosure as described in [Section 4.2.2](https://www.rfc-editor.org/rfc/rfc9901.html#disclosures_for_array_elements).

        


#### 4.2.1. Disclosures for Object Properties
For each claim that is an object property and that is to be made selectively disclosable, the Issuer MUST create a Disclosure as follows:

- 
              Create a JSON array of three elements in the following order:

- A salt value. MUST be a string. See [Section 9.3](https://www.rfc-editor.org/rfc/rfc9901.html#salt-entropy) for security considerations. To achieve the recommended entropy of the salt, the Issuer can base64url-encode 128 bits of cryptographically secure random data, producing a string. The salt value MUST be unique for each claim that is to be selectively disclosed. The Issuer MUST NOT reveal the salt value to any party other than the Holder.

                - The claim name, or key, as it would be used in a regular JWT payload. It MUST be a string and MUST NOT be `_sd`, `...`, or a claim name existing in the object as a permanently disclosed claim.

                - The claim value, as it would be used in a regular JWT payload. The value can be of any type that is allowed in JSON, including numbers, strings, booleans, arrays, null, and objects.

              

            - base64url-encode the UTF-8 byte sequence of the JSON array. This string is the Disclosure.

          

            Note: The order was decided based on readability considerations: Salts have a
constant length within the SD-JWT, claim names would be around the same length
all the time, and claim values would vary in size, potentially being large
objects.

The following example illustrates the steps described above.
The array is created as follows:

```
["_26bc4LT-ac6q2KI6cBW5es", "family_name", "Möbius"]
```

The resultant Disclosure is:
`WyJfMjZiYzRMVC1hYzZxMktJNmNCVzVlcyIsICJmYW1pbHlfbmFtZSIsICJNw7ZiaXVzIl0`
Note that variations in whitespace, encoding of Unicode characters, ordering of object properties, etc., are allowed
in the JSON representation and no canonicalization needs to be performed before base64url encoding because the digest is calculated over the base64url-encoded value itself.
For example, the following strings are all valid and encode the
same claim value "Möbius":

- 
              A different way to encode the Unicode umlaut:
`WyJfMjZiYzRMVC1hYzZxMktJNmNCVzVlcyIsICJmYW1pbHlfbmFtZSIsICJNXHUwMGY2Yml1cyJd`

            - 
              No white space:
`WyJfMjZiYzRMVC1hYzZxMktJNmNCVzVlcyIsImZhbWlseV9uYW1lIiwiTcO2Yml1cyJd`

            - 
              Newline characters between elements:
`WwoiXzI2YmM0TFQtYWM2cTJLSTZjQlc1ZXMiLAoiZmFtaWx5X25hbWUiLAoiTcO2Yml1cyIKXQ`

          
However, the digest is calculated over the respective base64url-encoded value itself, which effectively signs the variation chosen by the Issuer and makes it immutable in the context of the particular SD-JWT.
See [Appendix B](https://www.rfc-editor.org/rfc/rfc9901.html#disclosure_format_considerations) for some further considerations on the Disclosure format approach.


#### 4.2.2. Disclosures for Array Elements
For each claim that is an array element and that is to be made selectively disclosable, the Issuer MUST create a Disclosure as follows:

- 
              The array MUST contain two elements in this order:

- The salt value as described in [Section 4.2.1](https://www.rfc-editor.org/rfc/rfc9901.html#disclosures_for_object_properties).

                - The array element that is to be hidden. This value can be of any type that is allowed in JSON, including numbers, strings, booleans, arrays, and objects.

              

          
The Disclosure string is created by base64url-encoding the UTF-8 byte sequence of the resultant JSON array as described in [Section 4.2.1](https://www.rfc-editor.org/rfc/rfc9901.html#disclosures_for_object_properties). The same considerations regarding
variations in the result of the JSON encoding apply.
For example, a Disclosure for the second element of the `nationalities` array in the following JWT Claims Set:

```
{
  "nationalities": ["DE", "FR", "US"]
}
```

could be created by first creating the following array:

```
["lklxF5jMYlGTPUovMNIvCA", "FR"]
```

The resultant Disclosure would be:
`WyJsa2x4RjVqTVlsR1RQVW92TU5JdkNBIiwgIkZSIl0`

            Note that the size of an array alone can potentially reveal unintended information.
The use of decoys, as described in [Section 4.2.5](https://www.rfc-editor.org/rfc/rfc9901.html#decoy_digests), to consistently pad the size of an array can help obscure
the actual number of elements present in any particular instance.


#### 4.2.3. Hashing Disclosures
For embedding references to the Disclosures in the SD-JWT, each Disclosure is hashed using the hash algorithm specified in the `_sd_alg` claim described in [Section 4.1.1](https://www.rfc-editor.org/rfc/rfc9901.html#hash_function_claim), or SHA-256 if no algorithm is specified. The resultant digest is then included in the SD-JWT payload instead of the original claim value, as described next.
The digest MUST be computed over the US-ASCII bytes of the base64url-encoded value that is the Disclosure. This follows the convention in JWS [[RFC7515](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7515)] and JWE [[RFC7516](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7516)]. The bytes of the digest MUST then be base64url encoded.
It is important to note that:

- The input to the hash function MUST be the base64url-encoded Disclosure, not the bytes encoded by the base64url string.

            - The bytes of the output of the hash function MUST be base64url encoded, and are not the bytes making up the (sometimes used) hex representation of the bytes of the digest.

          
For example, the base64url-encoded SHA-256 digest of the Disclosure
`WyJfMjZiYzRMVC1hYzZxMktJNmNCVzVlcyIsICJmYW1pbHlfbmFtZSIsICJNw7ZiaXVzIl0`
for the `family_name` claim from [Section 4.2.1](https://www.rfc-editor.org/rfc/rfc9901.html#disclosures_for_object_properties) above is
`X9yH0Ajrdm1Oij4tWso9UzzKJvPoDxwmuEcO3XAdRC0`.


#### 4.2.4. Embedding Disclosure Digests in SD-JWTs
For selectively disclosable claims, the digests of the Disclosures are embedded into the Issuer-signed JWT instead of the claims themselves. The precise way of embedding depends on whether a claim is an object property (name/value pair) or an array element.

- For a claim that is an object property, the Issuer embeds a Disclosure digest as described in [Section 4.2.4.1](https://www.rfc-editor.org/rfc/rfc9901.html#embedding_object_properties).

            - For a claim that is an array element, the Issuer creates a Disclosure digest as described in [Section 4.2.4.2](https://www.rfc-editor.org/rfc/rfc9901.html#embedding_array_elements).

          


##### 4.2.4.1. Object Properties
Digests of Disclosures for object properties are added to an array under the new
key `_sd` in the object. The `_sd` key MUST refer to an array of strings, each
string being a digest of a Disclosure or a decoy digest as described in [Section 4.2.5](https://www.rfc-editor.org/rfc/rfc9901.html#decoy_digests).
An `_sd` key can be present at any level of the JSON object hierarchy, including at the top-level,
nested deeper as described in [Section 6](https://www.rfc-editor.org/rfc/rfc9901.html#nested_data), or in recursive Disclosures as described in [Section 4.2.6](https://www.rfc-editor.org/rfc/rfc9901.html#recursive_disclosures).
The array MAY be empty in case the Issuer decided not to selectively disclose
any of the claims at that level. However, it is RECOMMENDED to omit the `_sd`
key in this case to save space.
The Issuer MUST hide the original order of the claims in the array. To ensure
this, it is RECOMMENDED to shuffle the array of hashes, e.g., by sorting it
alphanumerically or randomly, after potentially adding
decoy digests as described in [Section 4.2.5](https://www.rfc-editor.org/rfc/rfc9901.html#decoy_digests). The precise method does not matter as long as it
does not depend on the original order of elements.
For example, using the digest of the Disclosure from [Section 4.2.3](https://www.rfc-editor.org/rfc/rfc9901.html#hashing_disclosures),
the Issuer could create the following SD-JWT payload to make `family_name`
selectively disclosable:

```
{
  "given_name": "Alice",
  "_sd": ["X9yH0Ajrdm1Oij4tWso9UzzKJvPoDxwmuEcO3XAdRC0"]
}
```


##### 4.2.4.2. Array Elements
Digests of Disclosures for array elements are added to the array in the same
position as the original claim value in the array. For each digest, an object
of the form `{"...": "<digest>"}` is added to the array. The key MUST always be the
string `...` (three dots). The value MUST be the digest of the Disclosure created as
described in [Section 4.2.3](https://www.rfc-editor.org/rfc/rfc9901.html#hashing_disclosures). There MUST NOT be any other keys in the
object. Note that the string `...` was chosen because the ellipsis character, typically entered as three period characters, is commonly used in places where content is omitted from the present context.
For example, using the digest of the array element Disclosure created in [Section 4.2.2](https://www.rfc-editor.org/rfc/rfc9901.html#disclosures_for_array_elements),
the Issuer could create the following SD-JWT payload to make the second element
of the `nationalities` array selectively disclosable:

```
{
  "nationalities":
    ["DE", {"...":"w0I8EKcdCtUPkGCNUrfwVp2xEgNjtoIDlOxc9-PlOhs"},
     "US"]
}
```

As described in [Section 7.3](https://www.rfc-editor.org/rfc/rfc9901.html#verifier_verification), Verifiers ignore all selectively
disclosable array elements for which they did not receive a Disclosure. In the
example above, the verification process would output an array with only two
elements, `["DE", "US"]`, unless the matching Disclosure for the second element is received,
in which case the output would be a three-element array, `["DE", "FR", "US"]`.


#### 4.2.5. Decoy Digests
An Issuer MAY add additional digests to the SD-JWT payload that are not associated with
any claim.  The purpose of such "decoy" digests is to make it more difficult for
an adversarial Verifier to see the original number of claims or array elements contained in the SD-JWT. Decoy
digests MAY be added both to the `_sd` array for objects as well as in arrays.
It is RECOMMENDED to create the decoy digests by hashing over a
cryptographically secure random number. The bytes of the digest MUST then be
base64url encoded as above. The same digest function as for the Disclosures MUST
be used.
For decoy digests, no Disclosure is sent to the Holder, i.e., the Holder will
see digests that do not correspond to any Disclosure. See
[Section 10.4](https://www.rfc-editor.org/rfc/rfc9901.html#decoy_digests_privacy) for additional privacy considerations.
To ensure readability and replicability, the examples in this specification do
not contain decoy digests unless explicitly stated. For an example
with decoy digests, see [Appendix A.1](https://www.rfc-editor.org/rfc/rfc9901.html#example-simple_structured).


#### 4.2.6. Recursive Disclosures
The algorithms above are compatible with "recursive Disclosures", in which one
selectively disclosed field reveals the existence of more selectively
disclosable fields.  For example, consider the following JSON structure:

```
{
    "family_name": "Möbius",
    "nationalities": ["DE", "FR", "UK"]
}
```

When the Holder has multiple nationalities, the Issuer may wish to conceal
the presence of any statement regarding nationalities while also allowing the
Holder to reveal each of those nationalities individually.
This can be accomplished by first making the entries within the "nationalities"
array selectively disclosable, and then making the whole "nationalities" field
selectively disclosable.
The following shows each of the entries within the "nationalities" array being made selectively disclosable:

```
{
    "family_name": "Möbius",
    "nationalities": [
        { "...": "PmnlrRjhLcwf8zTDdK15HVGwHtPYjddvD362WjBLwro" }
        { "...": "r823HFN6Ba_lpSANYtXqqCBAH-TsQlIzfOK0lRAFLCM" },
        { "...": "nP5GYjwhFm6ESlAeC4NCaIliW4tz0hTrUeoJB3lb5TA" }
    ]
}
```

Content of Disclosures:

```
PmnlrRj... = ["16_mAd0GiwaZokU26_0i0h","DE"]
r823HFN... = ["fn9fN0rD-fFs2n303ZI-0c","FR"]
nP5GYjw... = ["YIKesqOkXXNzMQtsX_-_lw","UK"]
```

Followed by making the whole "nationalities" array selectively disclosable:

```
{
    "family_name": "Möbius",
    "_sd": [ "5G1srw3RG5W4pVTwSsYxeOWosRBbzd18ZoWKkC-hBL4" ]
}
```

Content of Disclosures:

```
PmnlrRj... = ["16_mAd0GiwaZokU26_0i0h","DE"]
r823HFN... = ["fn9fN0rD-fFs2n303ZI-0c","FR"]
nP5GYjw... = ["YIKesqOkXXNzMQtsX_-_lw","UK"]
5G1srw3... = ["4drfeTtSUK3aY_-PF12gcX","nationalities",
    [
        { "...": "PmnlrRjhLcwf8zTDdK15HVGwHtPYjddvD362WjBLwro" },
        { "...": "r823HFN6Ba_lpSANYtXqqCBAH-TsQlIzfOK0lRAFLCM" },
        { "...": "nP5GYjwhFm6ESlAeC4NCaIliW4tz0hTrUeoJB3lb5TA" }
    ]
]
```

With this set of Disclosures, the Holder could include the Disclosure with hash
`PmnlrRj...` to disclose only the "DE" nationality, or include both `PmnlrRj...`
and `r823HFN...` to disclose both the "DE" and "FR" nationalities, but hide the
"UK" nationality. In either case, the Holder would also need to include the
Disclosure with hash `5G1srw3...` to disclose the `nationalities` field that
contains the respective elements.
Note that making recursive redactions introduces dependencies between the
Disclosure objects in an SD-JWT.  The `r823HFN...` Disclosure cannot be used
without the `5G1srw3...` Disclosure; since a Verifier would not have a matching
hash that would tell it where the content of the `r823HFN...` Disclosure should
be inserted.  If a Disclosure object is included in an SD-JWT, then the SD-JWT
MUST include any other Disclosure objects necessary to process the first
Disclosure object.  In other words, any Disclosure object in an SD-JWT must
"connect" to the claims in the issuer-signed JWT, possibly via an intermediate
Disclosure object.  In the above example, it would be illegal to include any one
of the `PmnlrRj...`, `r823HFN...`, `nP5GYjw...` Disclosure objects without also
including the `5G1srw3...` Disclosure object.


### 4.3. Key Binding JWT
This section defines the Key Binding JWT, which encodes a
signature over an SD-JWT by the Holder's private key.
The Key Binding JWT MUST be a JWT according to [[RFC7519](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7519)], and it MUST contain the following elements:

- 
            in the JOSE header,

- 
                `typ`: REQUIRED. MUST be `kb+jwt`, which explicitly types the Key Binding JWT as recommended in [Section 3.11](https://rfc-editor.org/rfc/rfc8725#section-3.11) of [[RFC8725](https://www.rfc-editor.org/rfc/rfc9901.html#RFC8725)].

              - 
                `alg`: REQUIRED. A digital signature algorithm identifier such as per the IANA "JSON Web Signature and Encryption Algorithms" registry. It MUST NOT be "none".

            

          - 
            in the JWT payload,

- 
                `iat`: REQUIRED. The value of this claim MUST be the time at which the Key Binding JWT was issued using the syntax defined in [[RFC7519](https://www.rfc-editor.org/rfc/rfc9901.html#RFC7519)].

              - 
                `aud`: REQUIRED. The value MUST be a single string that identifies the intended receiver of the Key Binding JWT. How the value is represented is up to the protocol used and is out of scope for this specification.

              - "nonce": REQUIRED. Ensures the freshness of the signature or its binding to the given transaction. The value type of this claim MUST be a string. How this value is obtained is up to the protocol used and is out of scope for this specification.

              - 
                `sd_hash`: REQUIRED. The base64url-encoded hash value over the Issuer-signed JWT and the selected Disclosures as defined below.

            

        
The general extensibility model of JWT means that additional claims and header parameters can be added to the Key Binding JWT.
However, unless there is a compelling reason, this SHOULD be avoided, as it may harm interoperability and burden conceptual integrity.


#### 4.3.1. Binding to an SD-JWT
The hash value in the `sd_hash` claim binds the KB-JWT to the specific SD-JWT.
The `sd_hash` value MUST be computed over the US-ASCII bytes of the
encoded SD-JWT, i.e.,
the Issuer-signed JWT, a tilde character, and zero or more Disclosures selected
for presentation to the Verifier, each followed by a tilde character:

```
<Issuer-signed JWT>~<Disclosure 1>~<Disclosure 2>~...~<Disclosure N>~
```

The bytes of the digest MUST then be base64url encoded.
The same hash algorithm as for the Disclosures MUST be used (defined by
the `_sd_alg` element in the Issuer-signed JWT or the default value, as defined
in [Section 4.1.1](https://www.rfc-editor.org/rfc/rfc9901.html#hash_function_claim)).


#### 4.3.2. Validating the Key Binding JWT
Whether to require Key Binding is up to the Verifier's policy, based on the set
of trust requirements (such as trust frameworks) it belongs to. See
[Section 9.5](https://www.rfc-editor.org/rfc/rfc9901.html#key_binding_security) for security considerations.
If the Verifier requires Key Binding, the Verifier MUST ensure that the key with which it validates the signature on
the Key Binding JWT is the key specified in the SD-JWT as the Holder's public
key.  For example, if the SD-JWT contains a `cnf` value with a `jwk` member, the
Verifier would parse the provided JWK and use it to verify the Key Binding JWT.
Details of the validation process are defined in [Section 7.3](https://www.rfc-editor.org/rfc/rfc9901.html#verifier_verification).
