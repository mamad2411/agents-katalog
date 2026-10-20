---
name: "token-status-list-aggregation-x509"
description: "Use when implementing Token Status List aggregation and PKI integration. Covers: status list aggregation behavior and X.509 extensions."
sections:
  - "9. Status List Aggregation"
  - "9.1. Issuer Metadata"
  - "9.2. Status List Parameter"
  - "9.3. Status List Aggregation in JSON Format"
  - "10. X.509 Certificate Extensions"
  - "10.1. Extended Key Usage Extension"
---

<!-- ARF version: draft-10 -->
<!-- Tokens: ~1122 -->

## 9. Status List Aggregation
Status List Aggregation is an optional mechanism to retrieve a list of URIs to all Status List Tokens, allowing a Relying Party to fetch all relevant Status Lists for a specific type of Referenced Token or Issuer. This mechanism is intended to support fetching and caching mechanisms and allow offline validation of the status of a reference token for a period of time.
If a Relying Party encounters an invalid Status List referenced in the response from the Status List Aggregation endpoint, it SHOULD continue processing the other valid Status Lists referenced in the response.
There are two options for a Relying Party to retrieve the Status List Aggregation.
An Issuer MAY support any of these mechanisms:

- 
          Issuer metadata: The Issuer of the Referenced Token publishes an URI which links to Status List Aggregation, e.g. in publicly available metadata of an issuance protocol

        - 
          Status List Parameter: The Status Issuer includes an additional claim in the Status List Token that contains the Status List Aggregation URI.

      

```
┌─────────────────┐
                                      │                 │
                                      │ Issuer Metadata │
                                      │                 │
                                      └───┬─────────────┘
                                          │
  ┌───────────────────┐                   │ link within metadata
 ┌───────────────────┐│  link all         ▼
┌───────────────────┐││◄───────┐  ┌─────────────────────────┐
│                   ││◄────────┤  │                         │
│ Status List Token │◄┴────────┴──┤ Status List Aggregation │
│                   │┘            │                         │
└───────┬───────────┘             └─────────────────────────┘
        │                                 ▲
        │   link by aggregation_uri       │
        └─────────────────────────────────┘
```


### 9.1. Issuer Metadata
The Issuer MAY link to the Status List Aggregation URI in metadata that can be provided by different means like .well-known metadata as is used commonly in OAuth and OpenID or via a VICAL extension for ISO mDoc / mDL. If the Issuer is an OAuth Authorization Server according to [[RFC6749](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC6749)], it is RECOMMENDED to use `status_list_aggregation_endpoint` for its metadata defined by [[RFC8414](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC8414)].
The concrete specification on how this is implemented depends on the specific ecosystem and is out of scope of this specification.


### 9.2. Status List Parameter
The URI to the Status List Aggregation MAY be provided as the optional parameter `aggregation_uri` in the Status List itself as explained in [Section 4.3](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-cbor) and [Section 4.2](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#status-list-json) respectively. A Relying Party may use this URI to retrieve an up-to-date list of relevant Status Lists.


### 9.3. Status List Aggregation in JSON Format
This section defines the structure for a JSON-encoded Status List Aggregation:

- 
            `status_lists`: REQUIRED. JSON array of strings that contains URIs linking to Status List Tokens.

        
The Status List Aggregation URI provides a list of Status List URIs. This aggregation in JSON and the media type return SHOULD be `application/json`. A Relying Party can iterate through this list and fetch all Status List Tokens before encountering the specific URI in a Referenced Token.
The following is a non-normative example for media type `application/json`:

```
{
   "status_lists" : [
      "https://example.com/statuslists/1",
      "https://example.com/statuslists/2",
      "https://example.com/statuslists/3"
   ]
}
```

---

## 10. X.509 Certificate Extensions


### 10.1. Extended Key Usage Extension
[[RFC5280](https://www.ietf.org/archive/id/draft-ietf-oauth-status-list-10.html#RFC5280)] specifies the Extended Key Usage (EKU) X.509 certificate extension for use on end entity certificates. The extension indicates one or more purposes for which the certified public key is valid. The EKU extension can be used in conjunction with the Key Usage (KU) extension, which indicates the set of basic cryptographic operations for which the certified key may be used. A certificate's issuer explicitly delegates Status List Token signing authority by issuing a X.509 certificate containing the KeyPurposeId defined below in the extended key usage extension.
The following OID is defined for usage in the EKU extension
```
   id-kp  OBJECT IDENTIFIER  ::=
       { iso(1) identified-organization(3) dod(6) internet(1)
         security(5) mechanisms(5) pkix(7) 3 }
id-kp-oauthStatusListSigning             OBJECT IDENTIFIER ::= { id-kp TBD }
```
