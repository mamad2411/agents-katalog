---
name: "arf-issuance-reqs"
description: "Use when implementing PID or attestation issuance, including lifecycle states, batch issuance, key binding, and trust requirements between issuers and wallet units."
sections:
  - "6.6.1 PID or attestation lifecycle"
  - "6.6.2 PID or attestation issuance"
  - "6.6.2.1 Required trust relationships"
  - "6.6.2.2 Wallet Unit authenticates the PID Provider or Attestation Provider"
  - "6.6.2.3 Wallet Unit verifies Provider's entitlements and registered attestation types"
  - "6.6.2.4 PID Provider or Attestation Provider validates the Wallet Unit"
  - "6.6.2.5 PID Provider or Attestation Provider verifies that Wallet Unit is not revoked"
  - "6.6.2.6 Wallet Unit verifies PID or attestation"
  - "6.6.2.7 User activates the PID"
  - "6.6.2.8 Provisioning embedded disclosure policies"
  - "6.6.2.8.1 Introduction"
  - "6.6.2.9 Batch issuance"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~6180 -->

#### 6.6.1 PID or attestation lifecycle

[Section 4.6.6][466-pid-or-attestation] above presented the lifecycle of a PID
or attestation within a Wallet Unit:

1. Using their Wallet Unit, the User requests the **issuance** of a logical PID or attestation from a PID Provider or an Attestation Provider. This results in the Wallet Unit requesting one or multiple technical PIDs or attestations from that Provider. The required trust
relationships for issuance are discussed in [Section 6.6.2][662-pid-or-attestation-issuance]
below.
1. Once one or more technical PIDs or attestations are issued into the Wallet Unit, the User can
**present** attributes from it to the following entities: 
    - First of all, to a Relying Party Instance. Presentation happens according to the User's
decision and depending on successful authentication of the Relying Party. The
required trust relationships for presenting PIDs and attestations, including
User approval and Relying Party authentication, are discussed in [Section 6.6.3][663-pid-or-attestation-presentation-to-a-relying-party].
    - Instead of presenting attributes to a Relying Party, a User can also present
them to another User, meaning that their Wallet Unit is interacting with another
Wallet Unit. This is discussed in [Section 6.6.4][664-pid-or-attestation-presentation-to-another-wallet-unit].
    - Finally, the User can also present attributes to an intermediary, who interacts with the Wallet Unit on behalf of a Relying Party. [Section 6.6.5][665-pid-or-attestation-presentation-to-an-intermediary] discusses how presentation to an intermediary is different from presentation to a 'normal' Relying Party.
1. The PID Provider or the Attestation Provider remains responsible for **management** of
the logical PID or attestation over its lifetime. Management may include re-issuing the corresponding technical PIDs or attestations with the same or different attribute values. The
Provider can also revoke the PID or the attestation, possibly based on a request
of the User. The management of PIDs and attestations is discussed in [Section 6.6.6][666-pid-or-attestation-management].
1. Finally, [Section 6.6.7][667-pid-or-attestation-deletion] discusses what
happens if a User decides to **delete** a logical PID or attestation from their Wallet
Unit.

#### 6.6.2 PID or attestation issuance

##### 6.6.2.1 Required trust relationships

The lifecycle of a PID or an attestation starts when a User, using their Wallet
Unit, requests a PID Provider or an Attestation Provider to issue the PID or an
attestation to their Wallet Unit. The following trust relationships are
established during issuance:

1. The Wallet Unit authenticates the PID Provider or Attestation Provider using
the access certificate referred to in [Section 6.3][63-trust-throughout-a-pid-provider-or-an-attestation-provider-lifecycle].
This ensures that the User can trust that the PID or attestation they are about
to receive, is issued by an authenticated PID Provider or Attestation Provider
respectively. See [Section 6.6.2.2][6622-wallet-unit-authenticates-the-pid-provider-or-attestation-provider]
below describing how this will be done.
1. The Wallet Unit verifies the PID Provider's or Attestation Provider's entitlements and registered attestation types. This ensure that the Provider has registered itself as either a PID Provider, a QEAA Provider, a PuB-EAA Provider, or a non-qualified EAA Provider, and has also registered the type(s) of attestations it issues. See [Section 6.6.2.3][6623-wallet-unit-verifies-providers-entitlements-and-registered-attestation-types] for more information.
1. If the above verifications pass, the Wallet Units sends an authorization request to the PID Provider or Attestation Provider. Subsequently, the PID Provider or Attestation Provider authenticates the
Wallet Unit, see [Section 6.6.2.4][6624-pid-provider-or-attestation-provider-validates-the-wallet-unit]
below.
1. The PID Provider or Attestation Provider verifies that the Wallet Provider
did not revoke the Wallet Unit. This is described in [Section 6.6.2.5][6625-pid-provider-or-attestation-provider-verifies-that-wallet-unit-is-not-revoked].
1. If necessary, the PID Provider or Attestation Provider authenticates the User, meaning that the Provider is sure about the identity of the User. In most use cases, this is necessary to enable determination of the values of the attributes that the Provider will attest to. For instance, a PID Provider needs to authenticate the User to ensure it provides a PID containing the correct family name and date of birth. In some use cases User authentication is not necessary; for example, when a shop owner issues a voucher or a receipt to a customer, the shop owner does not need to know who the customer is. The method
by which the PID Provider or Attestation Provider performs User identification
and authentication is out of scope of the ARF, as these processes are specific
to each PID Provider or Attestation Provider. However, for a PID, these
processes will satisfy the requirements for Level of Assurance High in
[Commission Implementing Regulation (EU) 2015/1502](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32015R1502).
For a QEAA, the User identification process will satisfy the reference standards laid down in [CIR 2025/1566] on verification of the identity and attributes of the person to whom a qualified certificate or qualified electronic attestation of attributes is to be issued.
For other attestations, user authentication is performed on a security level
commensurate with the required level of security for the attestation issued.
1. After the PID or attestation is issued to the Wallet Unit, the Wallet Unit
verifies the authenticity of the PID or attestation; see [Section 6.6.2.6][6626-wallet-unit-verifies-pid-or-attestation].
1. The User will activate a PID before they can use it; see [Section 6.6.2.7][6627-user-activates-the-pid].
1. If the [OpenID4VCI] Credential Issuer metadata for an attestation contains an
embedded disclosure policy, the Wallet Unit
retrieves the policy and stores it locally, so that it can apply the policy in
case a Relying Party requests attributes from the attestation. See [Section 6.6.2.8][6628-provisioning-embedded-disclosure-policies].

More detailed requirements for the issuance process of PIDs and attestations,
for instance regarding the issuance protocol, are included in [Topic 10][topic-10].

##### 6.6.2.2 Wallet Unit authenticates the PID Provider or Attestation Provider

To start the process of requesting a PID or an attestation, the User directs the
Wallet Unit to contact the PID Provider or Attestation Provider at a service supply point. A service supply point is a system at which a Wallet Unit can start the process of requesting and obtaining a PID or attestation. The User may
for example use the Wallet Unit to scan a QR code or tap an NFC tag to do so, or the Wallet Provider may configure each Wallet Unit with a pre-defined list of PID Providers and Attestation Providers, including the URLs of their service supply points and associated attestation type(s). Note that no centralised service discovery mechanism for PID or attestation issuance is foreseen.

Before requesting the issuance of a PID or an attestation, the Wallet Unit
authenticates the PID Provider or the Attestation Provider. To do so, the Wallet
Unit follows the same process as for authenticating a Relying Party, see [Section 6.6.3.2][6632-wallet-unit-authenticates-the-relying-party-instance], with the following differences:

- A PID Provider or Attestation Provider does not send it access certificate to the Wallet Unit in a request, but makes it available in its Credential Issuer metadata according to [OpenID4VCI] and [ETSI TS 119 472-3].
- The PID Provider or Attestation Provider does not sign a request, but rather its Credential Issuer metadata.

The Wallet Unit verifies that the access certificate of the PID Provider or Attestation Provider is valid and authentic, and the signature over the metadata is valid. If this is not the case, the Wallet Unit warns the User that it could not verify the identity of the PID Provider or Attestation Provider, and does not request the issuance of a PID or attestation.

##### 6.6.2.3 Wallet Unit verifies Provider's entitlements and registered attestation types

During registration, the PID Provider or Attestation Provider registered its entitlements, meaning whether it is a PID Provider, QEAA Provider, PuB-EAA Provider, or non-qualified EAA Provider; see [Section 6.3.2][632-pid-provider-or-attestation-provider-registration-and-notification]. It also registered the type(s) of PID or attestation it intends to issue to Wallet Units. A Provider of registration certificates listed this information in one or more registration certificate(s) and sent these to the
PID Provider or Attestation Provider. Subsequently, the PID Provider or Attestation Provider distributed the registration certificate(s) to its
service supply points.  Note that it is up to the PID Provider or Attestation Provider to determine if all of its supply points need all of the registration certificates, or that some supply points are used only for a subset of the attestation type(s) that this Provider issues, and consequently only need the registration certificates describing those attestation type(s). Each service supply point includes it registration certificate in its Credential Issuer metadata, similar to its access certificate; see the previous section.

The Wallet Unit obtains the registration certificate from the Credential Issuer metadata and verifies it. The Wallet Unit verifies that:

- the registration certificate is present and well-formed,
- the signature over the registration certificate can be verified using a trust anchor from the LoTE of Providers of registration certificates,
- the registration certificate has not expired and is not revoked,
- the registration certificate contains the same PID Provider or Attestation Provider identifier and the same Service identifier as the access certificate contained in the same Credential Issuer metadata. If that is not the case, a fraudulent entity could be using a registration certificate that was issued to a genuine PID Provider or Attestation Provider. 
  
If any of these checks fail, the Wallet Unit warns the User that it could not obtain or validate the information registered about the PID Provider or Attestation Provider, and does not request the issuance of a PID or attestation.

If all of the above checks pass, the Wallet Unit retrieves from the registration certificate the entitlements and the list of attestations registered by the PID Provider or Attestation Provider. The Wallet Unit verifies that the entitlement (i.e.,  PID Provider, QEAA Provider, PuB-EAA Provider, or non-qualified EAA Provider) matches with its expectations, for example based on the the type of PID or attestation it wants to receive. Next, the Wallet Unit verifies that the type of attestation it wants to receive is included in the list of attestation types in the registration certificate. If one of these verifications comes out negative, the Wallet Unit warns the User and does not request the issuance of a PID or attestation.

> Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].

For more information, see [Topic 44][topic-44].

##### 6.6.2.4 PID Provider or Attestation Provider validates the Wallet Unit

###### 6.6.2.4.1 Verifies the authenticity of the Wallet Unit

As shown in [Figure 12][61-scope], a PID Provider or an Attestation Provider
downloads the Wallet Provider LoTE from the location published by the Commission. Note that for PID Providers it is not mandatory to possess the trust anchors of all Wallet Providers in the ecosystem. This is because it is not mandatory for a
PID Provider to accept all certified Wallet Solutions. Each PID Provider will choose which trust anchors they need to
trust. This is different for Attestation Providers: they must accept all
Wallet Solutions and hence must possess all Wallet Provider trust anchors.

[Section 6.5.3][653-wallet-unit-activation] above described that a Wallet
Provider issues KAs and WIAs to the Wallet Unit. When the Wallet Unit requests the issuance of a PID or an attestation, it sends a WIA, and in most cases also a KA, to the PID Provider or the Attestation Provider. The PID Provider or Attestation Provider verifies the signature
over the WIA and the KA, using the Wallet Provider trust anchor obtained from the Trusted
List. This proves that the Wallet Unit is authentic and is provided by a trusted Wallet
Provider. For more details see [Topic 9][topic-9] and [Technical Specification 3](../technical-specifications/ts3-wallet-unit-attestation.md).

###### 6.6.2.4.2 Optionally, validates the properties of the WSCA/WSCD or the keystore

A key attestation (KA)  describes the certifications and the other relevant properties of the
WSCA/WSCD or a keystore. Because the WSCA/WSCD contains the private keys of the PID, the security level of the WSCA/WSCD is a key determinant for reaching
the overall Level of Assurance (LoA) High, as required for the PID in the Wallet
Unit. PID Providers therefore may want to validate a KA describing the WSCA/WSCD to verify that the WSCA/WSCD indeed complies with the requirements for Level of Assurance High.

For other device-bound attestations, the security of the attestation private keys is similarly important for guaranteeing the overall security of the attestation. The Attestation Provider decides on the
required level of security for the keystore and indicates this in the Credential Issuer metadata specified in [OpenID4VCI]. The Wallet Unit selects the WSCA/WSCD or a keystore that complies with the required level of security, and sends a KA describing this WSCA/WSCD or keystore to the Attestation Provider. The Attestation Provider can validate the KA to verify that the WSCA/WSCD or keystore indeed complies with its security requirements.

For non-device-bound attestations, the Wallet Unit does not send a key attestation to the Attestation Provider.

###### 6.6.2.4.3 Verifies that key for new PID or device-bound attestation is protected by the WSCD or keystore

Knowing the properties of the WSCA/WSCD or keystore is not very useful if the PID Provider or
Attestation Provider cannot be sure that the private key for their new PID or device-bound
attestation is indeed protected by that WSCA/WSCD or keystore. To enable this, each KA contains one or more public keys. By including these keys into a KA, the Wallet Provider attests that all of the associated private keys are indeed generated by and stored in the WSCA/WSCD or keystore described in the KA. The PID Provider or Attestation Provider can use each of these keys to bind a new PID or attestation to.

Apart from verifying the authenticity of the KA, the PID Provider or Attestation Provider also verifies that the KA is bound to the context of the PID or attestation issuance process. In other words, that it was not copied and replayed by an attacker. [OpenID4VCI] and [Technical Specification 3](../technical-specifications/ts3-wallet-unit-attestation.md) describe two methods for doing so. In both methods, during the issuance process, the PID Provider or Attestation Provider sends a nonce to the Wallet Unit. Subsequently it verifies that either

- The key attestation contains this nonce, meaning that the Wallet Provider signed it during the issuance process, or
- The Wallet Unit signed this nonce using the private key corresponding to one of the public keys in the key attestation, thereby proving possession of that key.

##### 6.6.2.5 PID Provider or Attestation Provider verifies that Wallet Unit is not revoked

[Section 6.5.3.4][6534-wallet-provider-issues-one-or-more-key-attestations-to-the-wallet-unit]
and [Section 6.5.3.5][6535-wallet-provider-issues-one-or-more-wias-to-the-wallet-unit]
above described that a Wallet Provider issues Key Attestations (KA) and Wallet
Instance Attestations (WIA) to the Wallet Unit. Both a KA and a WIA contain
revocation information. During the lifetime of the Wallet Unit, the Wallet
Provider regularly verifies that the security of the Wallet Unit is not breached
or compromised. If the Wallet Unit is no longer secure, the Wallet Provider
revokes the Wallet Instance and, if the breach involves a WSCA/WSCD or
keystore, revokes the corresponding KAs. The WIA and KA thus
allow PID Providers and Attestation Providers to verify that the Wallet Unit is
not revoked.

[CIR 2024/2977] requires that PID Providers must verify regularly, during the
entire lifetime of the PID, whether the Wallet Instance has been revoked (using
the revocation information in the WIA received during PID issuance) and whether
the WSCD or keystore has been revoked (using the revocation information in the
KA received during PID issuance). If either the Wallet Instance or the WSCD or
keystore has been revoked, the PID Provider must revoke the PID. This is
possible because both the WIA and the KA have a revocation maintenance period, which
is at least as long as the validity period of the PID. PID Providers 
also verify regularly whether the Wallet Provider has been suspended or
cancelled in the associated LoTE. If any of these events happens, the PID
Provider revokes the PID. Therefore, by verifying the revocation status of
the PID, the Relying Party Instance implicitly verifies the revocation status of
the Wallet Unit. See
[Technical Specification 3](../technical-specifications/ts3-wallet-unit-attestation.md)
for more information.

Attestation Providers can use the same mechanism as well, to provide the same
assurance to Relying Parties, although this is not required by the CIR. See also
[Section 6.6.3.12][66312-relying-party-optionally-trusts-issuer-to-regularly-verify-that-wallet-unit-is-not-revoked].

[Topic 38][topic-38]
describes Wallet Unit revocation in more detail.

Once it has done all verifications, the PID Provider or Attestation Provider
will issue the PID or attestation to the Wallet Unit.

##### 6.6.2.6 Wallet Unit verifies PID or attestation

After the Wallet Unit receives the PID or attestation, it will

- verify that the PID or attestation it received matches the request.
- verify the signature of the PID or attestation, using the appropriate trust
anchor if available, in the same way as described for a Relying Party Instance in [Section 6.6.3.6][6636-relying-party-instance-verifies-the-authenticity-of-the-pid-or-attestation]. Note that for a non-qualified attestation, the Wallet Unit may not be in possession of the necessary trust anchor.
- display the contents (i.e., attribute values) of the new PID or attestation to
the User and request the User's approval for storing the new PID or attestation.
When requesting approval, the Wallet Unit displays the contents of the PID or
attestation to the User. The Wallet Unit also informs the User about the
identity of the PID Provider or Attestation Provider, using the subject
information from the PID Provider's or Attestation Provider's access certificate.

If any of these verifications fail, the Wallet Unit will delete the PID or
attestation, and will inform the User that issuance was not successful.
Otherwise, the Wallet Unit will store the PID or attestation and will inform the
User that issuance was successful. The Wallet Unit
will also disclose the fact that it contains the new PID or attestation to the [W3C Digital Credentials API] framework, see [Section 4.4.3][443-remote-presentation-transaction-flows], unless the User has disabled such disclosure.

##### 6.6.2.7 User activates the PID

[Commission Implementing Regulation (EU) 2015/1502](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32015R1502)
requires that for an eID means on Level of Assurance High, an activation process
is implemented to verify that the eID means was delivered only into the
possession of the person to whom it belongs. In the context of the EUDI Wallet,
this means that it must be verified that a PID is issued into the Wallet Unit of
the PID subject. Note that activation is required only for PIDs, since the
[European Digital Identity Regulation] only requires PIDs to be issued at LoA
High.

PID Providers, in combination with Wallet Providers, have to ensure that the PID
issuing process complies with this requirement, see also requirement ISSU_05 in
Annex 2. During certification the responsible CAB decides whether the
implemented process is indeed compliant.

The ARF does not specify a process or mechanism for PID activation. PID
Providers and Wallet Providers are free to specify a suitable mechanism. Several
options have been suggested, but others may be used as well:

1. Wallet Providers, PID Providers, and CABs could decide that no additional
mechanism for PID activation is needed, if they conclude that existing
mechanisms are sufficient to ensure that the new PID can only end up on the
device used by the subject of the PID:
    - User authentication to the Wallet Unit that starts the request for PID issuance,
    - Mutual authentication and secure communication between the Wallet Unit and
    the PID Provider (as specified in [OpenID4VCI]), and
    - User authentication to the PID Provider as part of the PID issuance process, using an eID means on LoA High (or an eID means on LoA Substantial in conjunction with additional remote onboarding procedures, in accordance with article 5a.24 of the [European Digital Identity Regulation]).
2. Another option is to let the WSCA/WSCD perform identity matching during PID
issuance. This would require that the Wallet Provider identifies the Wallet
User and puts some identifying data, for instance User first and last name, in
the WSCA/WSCD. Then, during PID issuance, the WSCA verifies that the data in the
new PID match the data stored in the WSCA/WSCD.
3. A third option is to perform activation by using an activation code shared
via a trusted channel. In this setup, the Wallet Provider would identify the
Wallet User and store a random activation code in the WSCA/WSCD. The Wallet
Provider would share the activation code with the relevant PID Provider,
indicating the Wallet User's identity. During PID issuance, the PID Provider
would retrieve the correct activation code and send the code to the PID
subject's known address. To activate the PID, the PID subject (who is also the
Wallet User) enters the code in the Wallet Instance.

Note that options 2 and 3 introduce a need for the Wallet Provider to identify
the Wallet User. As explained in [Section 6.5.3.6][6536-wallet-provider-sets-up-a-user-account-for-user],
this is not needed for any other purpose, and any implications for the privacy
of the User need to be assessed. Also, these options require additional
functionality of the Wallet Instance and the WSCA/WSCD, which would probably
mean that PID activation can be done only for specific combinations of a Wallet
Provider and a PID Provider. However, as pointed out in [Section 6.5.2.3][6523-user-validates-that-wallet-solution-is-usable-with-relevant-pid],
this is allowed.

##### 6.6.2.8 Provisioning embedded disclosure policies

##### 6.6.2.8.1 Introduction

During attestation issuance, an Attestation Provider can optionally create an
embedded disclosure policy for the attestation. If so, the Attestation Provider
will provide it to Wallet Units during attestation issuance, by including it in
the Credential Issuer metadata (defined in [OpenID4VCI]) for that attestation. Such an
embedded disclosure policy contains rules determining which (types of) Relying
Parties are allowed by the Attestation Provider to receive the attestation.

Note that the [European Digital Identity Regulation] does not contain a requirement
for PIDs to be able to contain an embedded disclosure policy, but only for QEAAs
and PuB-EAAs.

For more information regarding embedded disclosure policies, please refer to the
[Discussion Paper for Topic D](../discussion-topics/d-embedded-disclosure-policies.md).

###### 6.6.2.8.2 Types of embedded disclosure policies

Annex III of [CIR 2024/2979] defines the following common embedded
disclosure policies that must be supported:

1. 'No policy' indicating that no policy applies to the electronic attestations
of attributes.
2. 'Authorised relying parties only policy', indicating that wallet users may only
disclose electronic attestations of attributes to authenticated relying parties
which are explicitly listed in the disclosure policies.
3. 'Specific root of trust' indicating that wallet users should only disclose
the specific electronic attestation of attributes to authenticated wallet-relying
parties with wallet-relying party access certificates derived from a specific
root (or list of specific roots) or intermediate certificate(s).

The first of these policies is the default and will be applied if the
Attestation Provider does not provide an embedded disclosure policy for an
attestation.

For expressing conditions on Relying Parties, an embedded disclosure policy will
refer to information included in the registration certificate provided to the Wallet
Unit by the Relying Party. Note that registration certificates are signed and hence
the information they contain is authenticated. Moreover, each registration certificate is bound to the access certificate used by the Relying Party to authenticate itself towards the Wallet Unit. Therefore, the Wallet Unit can trust that the information in the registration certificate applies to the Relying Party that sends the presentation request.

Wallet Units will provide support for at least policies 2. and 3. above. Note that these policies apply on the level of attestations, not individual attributes.

###### 6.6.2.8.3 Distributing embedded disclosure policies

An Attestation Provider will provide an embedded disclosure policy, if any, in
the Credential Issuer metadata specified in [OpenID4VCI]. This does not require
modifications to the attestation format. Embedded disclosure policies will be
integrated directly into the metadata, rather than being "linked" using a URL
and stored by the Attestation Provider. [ETSI TS 119 472-3] specifies how these policies are expressed and how an Attestation Provider includes them in the Credential Issuer metadata.

The approach ensures that the Wallet
Unit is not required to communicate with the Attestation Provider in order to be
able to obtain and evaluate a policy for an attestation requested by a Relying
Party. Instead, during issuance of an attestation, the Wallet Unit retrieves any
relevant disclosure policy from the Credential Issuer metadata and stores it
locally. A consequence of this approach is that an Attestation Provider will
revoke an attestation if a relevant embedded disclosure policy is updated.

##### 6.6.2.9 Batch issuance

Batch issuance means that instead of issuing a single technical PID or attestation to a
Wallet Unit, a PID Provider or Attestation Provider issues a batch of them. All
PIDs or attestations in a batch represent the same logical PID or attestation and have the same attestation type, attribute values
and technical validity period. Apart from that, all of the descriptions in this section
6.6.2 apply regardless of the number of attestations issued (single or batch).

Batch issuance is discussed in more detail in the [Discussion Paper for Topic B](../discussion-topics/b-re-issuance-and-batch-issuance-of-pids-and-attestations.md).
