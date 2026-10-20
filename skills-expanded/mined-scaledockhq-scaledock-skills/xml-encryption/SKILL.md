---
name: xml-encryption
description: >-
  XML Encryption: This document specifies a process for encrypting data and representing the result in XML. Covers XML Encryption Syntax and Processing Version 1.1. Use when encrypting XML. Triggers: XML Encryption.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# XML Encryption

This document specifies a process for encrypting data and representing the result in XML. The data may be in a variety of formats, including octet streams and other unstructured data, or structured data formats such as XML documents, an XML element, or XML element content. The result of encrypting data is an XML Encryption element that contains or references the cipher data.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when encrypting XML.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: XML Encryption Syntax and Processing Version 1.1 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 3.2.** "The presence of any child element under EncryptionMethod that is not permitted by the algorithm or the presence of a KeySize child inconsistent with the algorithm MUST be treated as an error."
2. **§ 4.3.** "If the cleartext is of type element or content, the data MUST be serialized in UTF-8 as specified in [XML10], using Normal Form C [NFC]."
3. **§ 5.2.4.** "For the purposes of this specification, AES-GCM shall be used with a 96 bit Initialization Vector (IV) and a 128 bit Authentication Tag (T)."
4. **§ 5.5.2.** "Implementations MUST implement RSA-OAEP for the transport of all key types and sizes that are mandatory to implement for symmetric encryption."
5. **§ 6.1.3.** "Implementations SHOULD restrict algorithm usage to algorithms known to be secure in the face of chosen-ciphertext attacks (RSA-OAEP, AES-GCM)."
6. **§ 6.1.3.** "In that case, documents containing RSA-PKCS#1 v1.5 [XMLENC-PKCS15-ATTACK] and AES-CBC [XMLENC-CBC-ATTACK] ciphertexts SHOULD be rejected without decryption."
7. **§ 6.2.** "While the signature secures plaintext it only covers that which is signed, recipients of encrypted messages must not infer integrity or authenticity of other unsigned information (e.g., headers) within the encrypted envelope, see [XMLDSIG-CORE1], section 8.1.1 Only What is Signed is Secure]."
8. **§ 6.4.** "For the Galois/Counter Mode (GCM) used by this specification, the IV must not be reused for any key and should be random, but it need not be secret."
9. **§ 6.7.** "Implementations SHOULD NOT provide detailed error responses related to security algorithm processing."
10. **§ 6.8.** "Implementers SHOULD ensure that distinct errors detected during security algorithm processing do not consume systematically different amounts of processing time from each other."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [XML Encryption Syntax and Processing Version 1.1](https://www.w3.org/TR/xmlenc-core1/): Recommendation, xmlenc-core1 REC-xmlenc-core1-20130411 (Recommendation, 2013-04-11), checked 2026-10-06.
