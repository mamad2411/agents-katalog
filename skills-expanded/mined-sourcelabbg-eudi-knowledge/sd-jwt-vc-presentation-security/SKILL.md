---
name: "sd-jwt-vc-presentation-security"
description: "Use when presenting or verifying SD-JWT VCs. Covers: presentation in OpenID4VP, JWT claims, security considerations, and privacy considerations."
sections:
  - "6. SD-JWT VC Type Metadata"
  - "6.1. Type Metadata Example"
  - "6.2. Type Metadata Format"
  - "6.3. Retrieving Type Metadata"
  - "6.4. Extending Type Metadata"
  - "6.5. Schema Type Metadata"
  - "7. Document Integrity"
  - "8. Display Metadata"
  - "8.1. Rendering Metadata"
  - "9. Claim Metadata"
  - "9.1. Claim Path"
  - "9.2. Claim Display Metadata"
  - "9.3. Claim Selective Disclosure Metadata"
  - "10. Security Considerations"
  - "10.1. Server-Side Request Forgery"
  - "10.2. Ecosystem-specific Public Key Verification Methods"
  - "10.3. Circular \"extends\" Dependencies of Types"
  - "10.4. Robust Retrieval of Type Metadata"
---

<!-- ARF version: draft-08 -->
<!-- Tokens: ~7762 -->

## 6. SD-JWT VC Type Metadata
An SD-JWT VC type, i.e., the `vct` value, is associated with Type Metadata defining, for example, information about the type or a schema defining (see [Section 6.5.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#schema-definition)) which claims MAY or MUST appear in the SD-JWT VC, and how credentials are displayed.
This section defines Type Metadata that can be associated with a type of an SD-JWT VC, as well as a method for retrieving the Type Metadata and processing rules. This Type Metadata is intended to be used, among other things, for the following purposes:

- Developers of Issuers and Verifiers can use the Type Metadata to understand the
semantics of the type and the associated rules. While in some cases,
Issuers are the parties that define types, this is
not always the case. For example, a type can be defined by a
standardization body or a community.

        - Verifiers can use the Type Metadata to determine whether a credential is valid
according to the rules of the type. For example, a Verifier can check
whether a credential contains all required claims and whether the claims
are selectively disclosable.

        - Wallets can use the metadata to display the credential in a way that is
consistent with the intent of the provider of the Type Metadata.

      
Type Metadata can be retrieved as described in [Section 6.3](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#retrieving-type-metadata).


### 6.1. Type Metadata Example
All examples in this section are non-normative.
The following is an example of an SD-JWT VC payload, containing a `vct` claim
with the value `https://betelgeuse.example.com/education_credential`:

```
{
  "vct": "https://betelgeuse.example.com/education_credential",
  "vct#integrity": "sha256-WRL5ca_xGgX3c1VLmXfh-9cLlJNXN-TsMk-PmKjZ5t0",
  ...
}
```

Type Metadata for the type `https://betelgeuse.example.com/education_credential`
can be retrieved using various mechanisms as described in
[Section 6.3](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#retrieving-type-metadata). For this example, the `vct` value is a URL as defined in
[Section 6.3.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#retrieval-from-vct-claim) and the following Type Metadata Document is
retrieved from it:

```
{
  "vct":"https://betelgeuse.example.com/education_credential",
  "name":"Betelgeuse Education Credential - Preliminary Version",
  "description":"This is our development version of the education credential. Don't panic.",
  "extends":"https://galaxy.example.com/galactic-education-credential-0.9",
  "extends#integrity":"sha256-9cLlJNXN-TsMk-PmKjZ5t0WRL5ca_xGgX3c1VLmXfh-WRL5",
  "schema_uri":"https://exampleuniversity.com/public/credential-schema-0.9",
  "schema_uri#integrity":"sha256-o984vn819a48ui1llkwPmKjZ5t0WRL5ca_xGgX3c1VLmXfh"
}
```

This example is shortened for presentation, a full Type Metadata example can be found in [Appendix B.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#ExampleTypeMetadata).
Note: The hash of the Type Metadata document shown in the second example must be equal
to the one in the `vct#integrity` claim in the SD-JWT VC payload,
`WRL5ca_xGgX3c1VLmXfh-9cLlJNXN-TsMk-PmKjZ5t0`.


### 6.2. Type Metadata Format
The Type Metadata document MUST be a JSON object. The following properties are
defined:

- 
            `name`

- OPTIONAL. A human-readable name for the type, intended for developers reading
the JSON document.

            

          - 
            `description`

- OPTIONAL. A human-readable description for the type, intended for
developers reading the JSON document.

            

          - 
            `extends`

- OPTIONAL. A URI of another type that this type extends, as described in
[Section 6.4](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#extending-type-metadata).

            

          - 
            `display`: An array of objects containing display information for the type, as described
in [Section 8](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#display-metadata). This property is OPTIONAL.

          - 
            `claims`: An array of objects containing claim information for the type, as described in
[Section 9](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#claim-metadata). This property is OPTIONAL.

          - 
            `schema`

- OPTIONAL. An embedded JSON Schema document describing the structure of
the Verifiable Credential as described in [Section 6.5.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#schema-definition). `schema` MUST NOT be used
if `schema_uri` is present.

            

          - 
            `schema_uri`

- OPTIONAL. A URL pointing to a JSON Schema document describing the structure
of the Verifiable Credential as described in [Section 6.5.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#schema-definition). `schema_uri` MUST NOT
be used if `schema` is present.

            

        
An example of a Type Metadata document is shown in [Appendix B.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#ExampleTypeMetadata).


### 6.3. Retrieving Type Metadata


#### 6.3.1. From a URL in the vct Claim
A URI in the `vct` claim can be used to express a type. If the
type is a URL using the HTTPS scheme, Type Metadata MAY be retrieved from it.
The Type Metadata is retrieved using the HTTP GET method. The response MUST be a JSON
object as defined in [Section 6.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#type-metadata-format).
If the claim `vct#integrity` is present in the SD-JWT VC, its value
`vct#integrity` MUST be an "integrity metadata" string as defined in Section [Section 7](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#document-integrity).


#### 6.3.2. From a Registry
A Consumer MAY use a registry to retrieve Type Metadata for a SD-JWT VC type,
e.g., if the type is not an HTTPS URL or if the Consumer does not have
access to the URL. The registry MUST be a trusted registry, i.e., the Consumer MUST trust the registry to provide correct Type Metadata for the type.
The registry MUST provide the Type Metadata in the same format as described in
[Section 6.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#type-metadata-format).


#### 6.3.3. Using a Defined Retrieval Method
Ecosystems MAY define additional methods for retrieving Type Metadata. For example, a
standardization body or a community MAY define a service which has to be used to
retrieve Type Metadata based on a URN in the `vct` claim.


#### 6.3.4. From a Local Cache
A Consumer MAY cache Type Metadata for a SD-JWT VC type. If a hash for integrity
protection is present in the Type Metadata as defined in [Section 7](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#document-integrity), the Consumer MAY assume that the Type Metadata is static and can be cached
indefinitely. Otherwise, the Consumer MUST use the `Cache-Control`
header of the HTTP response to determine how long the metadata can be cached.


#### 6.3.5. From Type Metadata Glue Documents
Credentials MAY encode Type Metadata directly, providing it as "glue
information" to the Consumer.
For JSON-serialized JWS-based credentials, such Type Metadata documents MAY be
included in the unprotected header of the JWS. In this case, the key `vctm` MUST
be used in the unprotected header and its value MUST be an array of
base64url-encoded Type Metadata documents as defined in this specification.
Multiple documents MAY be included for providing a whole chain of types to the
Consumer (see [Section 6.4](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#extending-type-metadata)).
A Consumer of a credential MAY use the documents in the `vctm`
array instead of retrieving the respective Type Metadata elsewhere as follows:

- When resolving a `vct` in a credential, the Consumer MUST ensure
that the `vct` claim in the credential matches the one in the Type Metadata
document, and it MUST verify the integrity of the Type Metadata document as
defined in [Section 7](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#document-integrity). The Consumer MUST NOT use the Type Metadata if no hash for integrity protection was provided in `vct#integrity`.

            - When resolving an `extends` property in a Type Metadata document, the Consumer MUST ensure that the value of the `extends` property in the
Type Metadata document matches that of the `vct` in the Type Metadata document, and it MUST verify the integrity of the Type Metadata document as defined in
[Section 7](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#document-integrity). The Consumer MUST NOT use the Type Metadata if no hash for integrity protection was provided.

          


### 6.4. Extending Type Metadata
An SD-JWT VC type can extend another type. The extended type is identified by the URI in
the `extends` property. Consumers MUST retrieve and process
Type Metadata for the extended type before processing the Type Metadata for the extending
type.
The extended type MAY itself extend another type. This can be used to create a
chain or hierarchy of types. The security considerations described in
[Section 10.3](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#circular-extends) apply in order to avoid problems with circular dependencies.


### 6.5. Schema Type Metadata


#### 6.5.1. Schema Definition
Schemas for Verifiable Credentials are contained in the `schema` or retrieved via the `schema_uri` Type Metadata parameters (as defined in [Section 6.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#type-metadata-format)).
A schema MUST be represented by a JSON Schema document according to draft version 2020-12 [[JSON.SCHEMA.2020-12](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#JSON.SCHEMA.2020-12)] or above.
The schema of a Verifiable Credential MUST include all properties that are required by this specification and MUST NOT override their cardinality, JSON data type, or semantic intent.
The following is a non-normative example of a JSON Schema document for the example in [Section 3.3](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#vc-sd-jwt-example) requiring the presence of the `cnf` claim in an SD-JWT VC presentation:

```
{
  "$schema":"https://json-schema.org/draft/2020-12/schema",
  "type":"object",
  "properties":{
    "vct":{
      "type":"string"
    },
    "iss":{
      "type":"string"
    },
    "nbf":{
      "type":"number"
    },
    "exp":{
      "type":"number"
    },
    "cnf":{
      "type":"object"
    },
    "status":{
      "type":"object"
    },
    "given_name":{
      "type":"string"
    },
    "family_name":{
      "type":"string"
    },
    "email":{
      "type":"string"
    },
    "phone_number":{
      "type":"string"
    },
    "address":{
      "type":"object",
      "properties":{
        "street_address":{
          "type":"string"
        },
        "locality":{
          "type":"string"
        },
        "region":{
          "type":"string"
        },
        "country":{
          "type":"string"
        }
      }
    },
    "birthdate":{
      "type":"string"
    },
    "is_over_18":{
      "type":"boolean"
    },
    "is_over_21":{
      "type":"boolean"
    },
    "is_over_65":{
      "type":"boolean"
    }
  },
  "required":[
    "iss",
    "vct",
    "cnf"
  ]
}
```

Note that `iss` and `vct` are always required by this specification.


#### 6.5.2. Schema Validation
If a `schema` or `schema_uri` property is present, a Consumer MUST validate the JSON document resulting from the SD-JWT verification algorithm
(as defined in Section 7 of [[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)]) against the JSON Schema document provided by the `schema` or `schema_uri` property.
If an `extends` property is present, the schema of the extended type MUST also be validated in the same manner. This process includes
validating all subsequent extended types recursively until a type is encountered that does not contain an `extends` property in its Type Metadata.
Each schema in this chain MUST be evaluated for a specific Verifiable Credential.
If the schema validation fails for any of the types in the chain, the Consumer MUST reject the Verifiable Credential.
The following is a non-normative example of a result JSON document after executing the SD-JWT verification algorithm that is validated against the JSON Schema document in the example provided in [Section 6.5.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#schema-definition):

```
{
  "vct":"https://credentials.example.com/identity_credential",
  "iss":"https://example.com/issuer",
  "iat":1683000000,
  "exp":1883000000,
  "sub":"6c5c0a49-b589-431d-bae7-219122a9ec2c",
  "address":{
    "country":"DE"
  },
  "cnf":{
    "jwk":{
      "kty":"EC",
      "crv":"P-256",
      "x":"TCAER19Zvu3OHF4j4W4vfSVoHIP1ILilDls7vCeGemc",
      "y":"ZxjiWWbZMQGHVWKVQ4hbSIirsVfuecCE6t4jT9F2HZQ"
    }
  }
}
```

Note, the example above does not contain any `_sd_alg`, `_sd`, or `...` claims.

---

## 7. Document Integrity
Both the `vct` claim in the SD-JWT VC and the various URIs in the Type Metadata MAY be accompanied by a respective claim suffixed with `#integrity`, in particular:

- 
          `vct` as defined in [Section 3.2.2.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#claims),

        - 
          `extends` as defined in [Section 6.4](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#extending-type-metadata)

        - 
          `uri` as used in two places in [Section 8.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#rendering-metadata)

        - 
          `schema_uri` as defined in [Section 6.5](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#schema-type-metadata)

      
The value MUST be an "integrity metadata" string as defined in Section 3 of
[[W3C.SRI](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#W3C.SRI)]. A Consumer of the respective documents MUST verify the
integrity of the retrieved document as defined in Section 3.3.5 of [[W3C.SRI](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#W3C.SRI)].

---

## 8. Display Metadata
The `display` property is an array containing display information for the type.
The array MUST contain an object for each language that is supported by the
type. The consuming application MUST use the language tag it considers most
appropriate for the user.
The objects in the array have the following properties:

- 
          `lang`: A language tag as defined in Section 2 of [[RFC5646](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC5646)]. This property is REQUIRED.

        - 
          `name`: A human-readable name for the type, intended for end users. This
property is REQUIRED.

        - 
          `description`: A human-readable description for the type, intended for end
users. This property is OPTIONAL.

        - 
          `rendering`: An object containing rendering information for the type, as
described in [Section 8.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#rendering-metadata). This property is OPTIONAL.

      


### 8.1. Rendering Metadata
The `rendering` property is an object containing rendering information for the
type. The object MUST contain a property for each rendering method that is
supported by the type. The property name MUST be a rendering method identifier
and the property value MUST be an object containing the properties defined for
the rendering method.


#### 8.1.1. Rendering Method "simple"
The `simple` rendering method is intended for use in applications that do not
support SVG rendering. The object contains the following properties:

- 
              `logo`: An object containing information about the logo to be displayed for
the type, as described in [Section 8.1.1.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#logo-metadata). This property is OPTIONAL.

            - 
              `background_color`: An RGB color value as defined in [[W3C.CSS-COLOR](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#W3C.CSS-COLOR)] for the background of the credential.
This property is OPTIONAL.

            - 
              `text_color`: An RGB color value as defined in [[W3C.CSS-COLOR](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#W3C.CSS-COLOR)] value for the text of the credential. This property
is OPTIONAL.

          


##### 8.1.1.1. Logo Metadata
The `logo` property is an object containing information about the logo to be
displayed for the type. The object contains the following properties:

- 
                `uri`: A URI pointing to the logo image. This property is REQUIRED.

              - 
                `uri#integrity`: An "integrity metadata" string as described in
[Section 7](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#document-integrity). This property is OPTIONAL.

              - 
                `alt_text`: A string containing alternative text for the logo image. This
property is OPTIONAL.

            


#### 8.1.2. Rendering Method "svg_template"
The `svg_template` rendering method is intended for use in applications that
support SVG rendering. The object MUST contain an array of objects containing
information about the SVG templates available for the type. Each object contains
the following properties:

- 
              `uri`: A URI pointing to the SVG template. This property is REQUIRED.

            - 
              `uri#integrity`: An "integrity metadata" string as described in
[Section 7](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#document-integrity). This property is OPTIONAL.

            - 
              `properties`: An object containing properties for the SVG template, as
described in [Section 8.1.2.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#svg-template-properties). This property is REQUIRED if more than
one SVG template is present, otherwise it is OPTIONAL.

          


##### 8.1.2.1. SVG Template Properties
The `properties` property is an object containing properties for the SVG
template. Consuming applications MUST use these properties to find the best SVG
template available for display to the user based on the display properties
(landscape/portrait) and user preferences (color scheme, contrast). The object
MUST contain at least one of the following properties:

- 
                `orientation`: The orientation for which the SVG template is optimized, with
valid values being `portrait` and `landscape`. This property is OPTIONAL.

              - 
                `color_scheme`: The color scheme for which the SVG template is optimized, with
valid values being `light` and `dark`. This property is OPTIONAL.

              - 
                `contrast`: The contrast for which the SVG template is optimized, with valid
values being `normal` and `high`. This property is OPTIONAL.

            


##### 8.1.2.2. SVG Rendering
Consuming application MUST preprocess the SVG template by replacing placeholders
in the SVG template with properly escaped values of the claims in the credential. The
placeholders MUST be defined in the SVG template using the syntax
`{{svg_id}}`, where `svg_id` is an identifier defined in the claim metadata as
described in [Section 9](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#claim-metadata).
Placeholders MUST only be used in the text content of the SVG template and MUST NOT
be used in any other part of the SVG template, e.g., in attributes or comments.
A consuming application MUST ensure that all special characters in the claim
values are properly escaped before inserting them into the SVG template. At
least the following characters MUST be escaped:

- 
                `&` as `&amp;`

              - 
                `<` as `&lt;`

              - 
                `>` as `&gt;`

              - 
                `"` as `&quot;`

              - 
                `'` as `&apos;`

            
If the `svg_id` is not present in the claim metadata, the consuming application
SHOULD reject not render the SVG template. If the `svg_id` is present in the
claim metadata, but the claim is not present in the credential, the placeholder
MUST be replaced with an empty string or a string appropriate to indicate that
the value is absent.
The following non-normative example shows a minimal SVG with one placeholder
using the `svg_id` value `address_street_address` which is defined in the
example in [Appendix B.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#ExampleTypeMetadata):

```
<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100">
  <text x="10" y="20">Street address: {{address_street_address}}</text>
</svg>
```

When rendering the SVG template, the consuming application MUST ensure that
malicious schema providers or issuers cannot inject executable code into the SVG
template and thereby compromise the security of the consuming application. The
consuming application MUST NOT execute any code in the SVG template. If code
execution cannot be prevented reliably, the SVG display MUST be sandboxed.

---

## 9. Claim Metadata
The `claims` property is an array of objects containing information about
particular claims for displaying and validating the claims.
The array MAY contain an object for each claim that is supported by the type.
Each object contains the following properties:

- 
          `path`: An array indicating the claim or claims that are being addressed, as
described below. This property is REQUIRED.

        - 
          `display`: An object containing display information for the claim, as
described in [Section 9.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#claim-display-metadata). This property is OPTIONAL.

        - 
          `sd`: A string indicating whether the claim is selectively disclosable, as
described in [Section 9.3](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#claim-selective-disclosure-metadata). This property is OPTIONAL.

        - 
          `svg_id`: A string defining the ID of the claim for reference in the SVG
template, as described in [Section 8.1.2.2](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#svg-rendering). The ID MUST be unique within the
type metadata. It MUST consist of only alphanumeric characters and underscores
and MUST NOT start with a digit. This property is OPTIONAL.

      


### 9.1. Claim Path
The `path` property MUST be a non-empty array of strings, `null` values, or
non-negative integers. It is used to select a particular claim in the credential
or a set of claims. A string indicates that the respective key is to be
selected, a `null` value indicates that all elements of the currently selected
array(s) are to be selected, and a non-negative integer indicates that the
respective index in an array is to be selected.
The following shows a non-normative, reduced example of a credential:

```
{
  "vct": "https://betelgeuse.example.com/education_credential",
  "name": "Arthur Dent",
  "address": {
    "street_address": "42 Market Street",
    "city": "Milliways",
    "postal_code": "12345"
  },
  "degrees": [
    {
      "type": "Bachelor of Science",
      "university": "University of Betelgeuse"
    },
    {
      "type": "Master of Science",
      "university": "University of Betelgeuse"
    }
  ],
  "nationalities": ["British", "Betelgeusian"]
}
```

The following shows examples of `path` values and the respective selected
claims in the credential above:

- 
            `["name"]`: The claim `name` with the value `Arthur Dent` is selected.

          - 
            `["address"]`: The claim `address` with its sub-claims as the value is selected.

          - 
            `["address", "street_address"]`: The claim `street_address` with the value
`42 Market Street` is selected.

          - 
            `["degrees", null, "type"]`: All `type` claims in the `degrees` array are
selected.

        
In detail, the array is processed from left to right as follows:

- Select the root element of the credential, i.e., the top-level JSON object.

          - 
            Process the `path` components from left to right:

- If the `path` component is a string, select the element in the respective
key in the currently selected element(s). If any of the currently
selected element(s) is not an object, abort processing and return an
error. If the key does not exist in any element currently selected,
remove that element from the selection.

              - If the `path` component is `null`, select all elements of the currently
selected array(s). If any of the currently selected element(s) is not an
array, abort processing and return an error.

              - If the `path` component is a non-negative integer, select the element at
the respective index in the currently selected array(s). If any of the
currently selected element(s) is not an array, abort processing and
return an error. If the index does not exist in a selected array, remove
that array from the selection.

              - If the set of elements currently selected is empty, abort processing and
return an error.

            

        
The result of the processing is the set of elements to which the respective
claim metadata applies.
The `path` property MUST point to the respective claim as if all
selectively disclosable claims were disclosed to a Verifier. That means that a
consuming application which does not have access to all disclosures may not be
able to identify the claim which is being addressed.


### 9.2. Claim Display Metadata
The `display` property is an array containing display information for the
claim. The array MUST contain an object for each language that is supported by
the type. The consuming application MUST use the language tag it considers most
appropriate for the user.
The objects in the array have the following properties:

- 
            `lang`: A language tag as defined in Section 2 of [[RFC5646](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#RFC5646)]. This property is REQUIRED.

          - 
            `label`: A human-readable label for the claim, intended for end users. This
property is REQUIRED.

          - 
            `description`: A human-readable description for the claim, intended for end
users. This property is OPTIONAL.

        


### 9.3. Claim Selective Disclosure Metadata
The `sd` property is a string indicating whether the claim is selectively
disclosable. The following values are defined:

- 
            `always`: The Issuer MUST make the claim selectively disclosable.

          - 
            `allowed`: The Issuer MAY make the claim selectively disclosable.

          - 
            `never`: The Issuer MUST NOT make the claim selectively disclosable.

        
If omitted, the default value is `allowed`.

---

## 10. Security Considerations
The Security Considerations in the SD-JWT specification
[[I-D.ietf-oauth-selective-disclosure-jwt](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#I-D.ietf-oauth-selective-disclosure-jwt)] apply to this specification.
Additionally, the following security considerations need to be taken into
account when using SD-JWT VCs:


### 10.1. Server-Side Request Forgery
The JWT VC Issuer Metadata configuration is retrieved from the JWT VC Issuer by the
Holder or Verifier. Similar to other metadata endpoints, the URL for the
retrieval MUST be considered an untrusted value and could be a vector for
Server-Side Request Forgery (SSRF) attacks.
Before making a request to the JWT VC Issuer Metadata endpoint, the Holder or
Verifier MUST validate the URL to ensure that it is a valid HTTPS URL and that
it does not point to internal resources. This requires, in particular, ensuring
that the host part of the URL does not address an internal service (by IP
address or an internal host name) and that, if an external DNS name is used, the
resolved DNS name does not point to an internal IPv4 or IPv6 address.
When retrieving the metadata, the Holder or Verifier MUST ensure that the
request is made in a time-bound and size-bound manner to prevent denial of
service attacks. The Holder or Verifier MUST also ensure that the response is a
valid JWT VC Issuer Metadata configuration document before processing it.
Additional considerations can be found in [[OWASP_SSRF](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#OWASP_SSRF)].


### 10.2. Ecosystem-specific Public Key Verification Methods
When defining ecosystem-specific rules for the verification of the public key,
as outlined in [Section 3.5](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#issuer-signed-jwt-verification-key-validation), it is critical
that those rules maintain the integrity of the relationship between the `iss` value
within the Issuer-signed JWT and the public keys of the Issuer.
It MUST be ensured that for any given `iss` value, an attacker cannot influence
the type of verification process used. Otherwise, an attacker could attempt to make
the Verifier use a verification process not intended by the Issuer, allowing the
attacker to potentially manipulate the verification result to their advantage.


### 10.3. Circular "extends" Dependencies of Types
A type MUST NOT extend another type that extends (either directly or with steps
in-between) the first type. This would result in a circular dependency that
could lead to infinite recursion when retrieving and processing the metadata.
Consumers MUST detect such circular dependencies and reject the
credential.


### 10.4. Robust Retrieval of Type Metadata
In [Section 6.3](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#retrieving-type-metadata), various methods for distributing and retrieving
metadata are described. Methods relying on a network connection may fail due to
network issues or unavailability of a network connection due to offline usage of
credentials, temporary server outages, or denial of service attacks on the
metadata server.
Consumers SHOULD therefore implement a local cache as described in
[Section 6.3.4](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#retrieval-from-local-cache) if possible. Such a cache MAY be populated with metadata before
the credential is used.
Issuers MAY provide glue documents as described in [Section 6.3.5](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#glue-documents) to provide
metadata directly with the credential and avoid the need for network requests.
These measures allow the Consumers to continue to function even if
the metadata server is temporarily unavailable and avoid privacy issues as
described in [Section 12.1](https://www.ietf.org/archive/id/draft-ietf-oauth-sd-jwt-vc-08.html#privacy-preserving-retrieval-of-type-metadata).
