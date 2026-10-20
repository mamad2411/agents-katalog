---
name: "mdoc-standards-tech"
description: "Use when understanding the standards and technologies behind mDocs. Covers: ISO/IEC 18013-5, 18013-7, 23220 standards overview, CBOR encoding, COSE signing, salted hashed claims, and X.509 certificate chains (IACA, DSC)."
sections:
  - "Standards and technology"
  - "[Underlying standards](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#underlying-standards)"
  - "[Foundational technologies](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#foundational-technologies)"
---

<!-- ARF version: MATTR-Learn-2025 -->
<!-- Tokens: ~1629 -->

# Standards and technology

This page details the following mDocs concepts:

- [Underlying standards](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#underlying-standards): This will help you understand where mDocs are
positioned in relation to existing standards.
- [Foundational technologies](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#foundational-technologies): This will help you understand what
technologies are being used to enable the core concepts of mDocs, and how they might interface
with your existing ecosystem.

## [Underlying standards](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#underlying-standards)
The [ISO/IEC 18013-5:2021](https://www.iso.org/standard/69084.html) standard was created to
standardize certain aspects in a Mobile Driver Licenses (mDLs) ecosystem. It defines the interface
for a mobile device to present an mDL to a verifier using a digital wallet in a close proximity
scenario. This includes data structure and important security features enabling the verifier to
validate the mDL.
The [ISO/IEC 18013-7:2025](https://www.iso.org/standard/91154.html) technical specification was
created to augment capabilities defined in the
[ISO/IEC 18013-5](https://www.iso.org/standard/69084.html) standard by enabling using a browser to
present an mDL to a verifier remotely (online). This standard specifies two protocols to support
online presentation of mDLs - RestAPI and
[OpenID for Verifiable Presentations (OID4VP)](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html).
MATTR mDocs implement the latter, which defines a mechanism on top of
[OAuth 2.0](https://www.rfc-editor.org/info/rfc6749) to enable online verification of verifiable
credentials, including mDLs.
The [ISO/IEC TS 23220 standard series](https://www.iso.org/standard/74910.html) (currently under
development) aims to generalize applications of this technology for more use cases, broadly referred
to as Mobile Documents or mDocs. ISO/IEC TS 23220-4 is compatible with ISO/IEC 18013-5 and ISO/IEC
18013-7 while introducing additional capabilities such as holder authentication.
MATTR mDocs have a generic format that can be presented with any claims and can be used in many
scenarios - purchasing age-restricted items, opening bank accounts, renting or sharing cars, going
through airport security, accessing secure locations and more.
## [Foundational technologies](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#foundational-technologies)
### [Object representation](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#object-representation)
mDocs verification workflows require compact data structures. Therefore, Concise Binary Object
Representation (CBOR) is the main format used to encode mDocs data structures.
CBOR is a binary data format designed to be interoperable with JSON while supporting more complex
data types. Being binary, it offers more compact messages, and allows encoding data directly without
converting it to a base64-encoded string first. In the context of mDocs, this is a big advantage
over JSON, which is a less space efficient data encoding method.
Refer to [CBOR.io](https://cbor.io/) to go deeper into CBOR.
### [Object signing](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#object-signing)
Personal information included in mDocs must be signed to be tamper proof. CBOR Object Signing and
Encryption (COSE) allows signing CBOR data structures in the same way JSON data structures can be
signed by JavaScript Object Signing and Encryption (JOSE).
mDocs use COSE to sign CBOR data structures, verifying the validity of the signed credential by
authenticating both the issuer and the device.
### [Hashed salted claims](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#hashed-salted-claims)
A hash is a cryptographic function that takes in data of any length, and creates a fixed length
unique output, referred to as a Hash (also known as a Digest). The algorithm type indicates the
fixed output length. For example, the SHA-256 algorithm generates 256 bits / 32 byte long hashes:

Valid hash functions must meet the following requirements:

- Collision resistant: Two distinct inputs must never result in the same hash.
- One-way: A Hash cannot be used to decipher the original input.
- Repeatable: The same data input should always generate the same output hash.

A salted hash value is the result of combining a unique random salt with a piece of data (e.g., a
claim) and applying a hash function, making it more secure by preventing attackers from easily
reversing or guessing the original data.
In the context of mDocs, salted hashed claim are used to enhance privacy by allowing holders to
reveal only specific information to relying parties, without disclosing unnecessary personal data.
This is referred to as selective disclosure. Each claim in the mDoc (e.g., date of birth or address)
is hashed with a unique salt and signed by the issuer, making it impossible to reverse-engineer the
original data unless the holder explicitly discloses it—even if the relying party receives a
credential that contains salted hashes of other undisclosed claims. This enables holders to reveal
only the necessary claim, such as their birthdate, without disclosing other claims like their
address.
For example, if an mDoc contains both a holder's birthdate and address, the credential will contain
salted hashes of each. When the holder needs to prove their age, they disclose only the birthdate.
The relying party receives the disclosed birthdate, along with its corresponding hash and salt from
the credential and can confirm the holder meets the age requirement without accessing other
information, such as the address, thereby preserving the holder’s privacy.
### [X.509 certificates](https://learn.mattr.global/docs/concepts/mdocs/standards-and-technologies#x509-certificates)
mDocs are high assurance identity credentials. Verifiers must be able to authenticate their issuers
to enable digital trust workflows within the ecosystem.
X.509 certificates are a standardized format for digital certificates, fundamental to Public Key
Infrastructure (PKI). Each certificate includes a public key and details about the certificate
itself, binding this information to a specific entity. Public key validation and verification
processes guarantee that the information in the certificate aligns with the claimed entity,
maintaining the overall security and trustworthiness of the PKI infrastructure.
X.509 certificates commonly use certificate chains which encompass multiple layers of digital
certificates to establish a chain of trust. The PKI hierarchy begins with a root certificate, acting
as the highest authority that issues intermediate certificates, creating a chain of trust leading to
end-entity certificates (such as mDocs). Certificate chain validation ensures the integrity of this
hierarchy, confirming that each certificate in the chain is legitimate, signed by its issuer and has
not been revoked.
In the context of mDocs, an
[Issuing Authority Certificate Authority (IACA)](/docs/issuance/certificates/overview#issuing-authority-certificate-authority-iaca)
and a [Document Signer Certificates (DSC)](/docs/issuance/certificates/overview#document-signer-certificate-dsc) are
both X.509 certificates.
