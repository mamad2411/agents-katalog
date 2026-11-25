---
name: "mdoc-core-capabilities"
description: "Use when understanding mDoc/ISO 18013-5 core capabilities. Covers: issuer data authentication, device authentication, holder authentication, session encryption, remote and in-person verification workflows, selective disclosure, and revocation."
sections:
  - "Core Capabilities"
  - "[Security features](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#security-features)"
  - "[User experience](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#user-experience)"
  - "[Revocation](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#revocation)"
---

<!-- ARF version: MATTR-Learn-2025 -->
<!-- Tokens: ~1183 -->

# Core Capabilities

The core capabilities enabled by mDocs can be split into two main categories - enhanced security and
improved user experience.
## [Security features](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#security-features)
### [Issuer data authentication](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#issuer-data-authentication)
Relying parties need to be able to know what entity issued a presented credential, as that
information can affect their decision to trust information included in the credential. mDocs adhere
to a very specific and well-defined suite of data structures, procedures and cryptographic
algorithms defined in the ISO 18013-5 standard. This enables relying parties to verify the origin
and the issuer of a credential through a chain of linked certificates all the way to its root
Certificate Authority (CA).
Refer to the [Chain of trust](/docs/concepts/chain-of-trust) sub-section for more information.
### [Device authentication](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#device-authentication)
Relying parties must be confident that a presented credential was in fact issued to the device it is
presented from. To protect against malicious cloning, mDocs are bound to a mobile device and enable
verifying the binding between a credential and the mobile device used to present it. We refer to
this concept as device authentication. When a credential is issued to a mobile device, the latter
generates a private key that is locked to its tamper resistant key store. The issuer then includes
the corresponding public key in the credential to establish the device binding. That same private
key must be used whenever the credential is presented to a relying party.
### [Holder authentication](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#holder-authentication)
Relying parties must also be able to validate that the person presenting the credential is the same
person the credential was issued to. For this purpose, mDocs can include a portrait picture of their
holder, enabling the verifier to compare it with the person presenting them in person. This
comparison can be performed either manually or using facial recognition technologies.
While the ISO/IEC 18013-5 standard explicitly requires a portrait picture as part of a valid mDL
certificate, our current issuance and verification capabilities do not enforce it. That is because
mDocs were built to meet wider use cases, some of which may not require a portrait picture. Advanced
techniques enable confirming the authorized person is presenting the credential without sharing
their biometric data as part of the verification workflow.
### [Session encryption](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#session-encryption)
mDocs communication protocols establish an end-to-end encrypted channel to ensure the credentials
remain hidden and confidential from any possible eavesdroppers. This security feature applies to
both in-person and remote (online) verification workflows.
Refer to the [Verification](/docs/verification) section for more information.
## [User experience](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#user-experience)
### [Multiple verification workflows](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#multiple-verification-workflows)
mDocs offer tremendous value as a single credential can be used across different digital
interactions and workflows:
#### [Remote interactions](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#remote-interactions)
mDocs can be used in online interactions via either same-device or cross-device workflows as per
ISO/IEC 18013-7. In same-device workflow, the user completes the entire interaction on their mobile
device, whereas in cross-device workflows they begin an interaction on a different device and are
then redirected to the mobile device that holds the mDoc to complete the interaction.
#### [In-person interactions](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#in-person-interactions)
mDocs are constructed in a way that enables real time offline verification, with no reliance on
internet-based technologies. The two devices (holder’s and verifier’s) communicate via BLE and have
all the information required to complete a verification workflow using non-internet technologies and
communication protocols. This means that in-person verification workflows can be completed anywhere,
regardless of location and internet coverage.
Refer to the [Verification](/docs/verification) section for more information.
### [Selective disclosure](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#selective-disclosure)
mDocs allow relying parties to specifically request only the information they need from the holders
of these credentials. The holders, in turn, can consent to sharing selected information contained in
the credential while fully understanding what, with whom, and for what purpose they are sharing it.
This concept is known as *Selective Disclosure*.
Refer to the
[Structure to function](/docs/concepts/mdocs/structure-to-function#salt-values-support-unwanted-disclosures-protection)
sub-section for more information on how mDocs enable this capability.
## [Revocation](https://learn.mattr.global/docs/concepts/mdocs/core-capabilities#revocation)
mDocs issued using MATTR VII have the capability to be set with a status that can be checked by
Verifiers while preserving the privacy of the holder. This status can then be updated by Issuers to
indicate if the credential is permanently revoked, temporarily revoked, or still valid. The holder
can use their digital wallet to see the latest status of their mDocs at any time.
Refer to [Revocation](/docs/issuance/revocation/overview) to learn more about this capability.
