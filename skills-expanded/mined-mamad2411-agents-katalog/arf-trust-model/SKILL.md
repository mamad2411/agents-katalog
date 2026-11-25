---
name: "arf-trust-model"
description: "Use when understanding the EUDI trust framework, provider registration, and lifecycle management for Wallet Providers, PID Providers, Attestation Providers, and Relying Parties."
sections:
  - "6.1 Scope"
  - "6.2 Trust throughout a Wallet Provider lifecycle"
  - "6.2.1 Wallet Provider lifecycle"
  - "6.2.2 Wallet Provider notification"
  - "6.2.3 Wallet Provider invalidation"
  - "6.3 Trust throughout a PID Provider or an Attestation Provider lifecycle"
  - "6.3.1 PID Provider or Attestation Provider lifecycle"
  - "6.3.2 PID Provider or Attestation Provider registration and notification"
  - "6.3.3 Suspension or cancellation of the registration of a PID Provider or Attestation Provider"
  - "6.4 Trust throughout a Relying Party lifecycle"
  - "6.4.1 Relying Party lifecycle"
  - "6.4.2 Relying Party registration"
  - "6.4.3 Relying Party suspension or cancellation"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~7760 -->

### 6.1 Scope

This chapter explains how trust works in the EUDI Wallet system, how it is established,
maintained, validated, and managed. It describes the rules and assumptions that decide
whether different parts of the system, like a wallet app, a user's device, or a
service provider, can be trusted.

![Figure 12](https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/media/Figure_12_Trust_Model.png)

```mermaid
flowchart TD
n0tklJ06Eg1gI686ZZUtUN_59["Relying Party Instance"]
n0tklJ06Eg1gI686ZZUtUN_58["Wallet Provider"]
n0tklJ06Eg1gI686ZZUtUN_57["Relying Party"]
n0tklJ06Eg1gI686ZZUtUN_56[" "]
n0tklJ06Eg1gI686ZZUtUN_53[" "]
n02((" "))
n03["Relying Party"]
n020["Wallet Unit"]
n019["Wallet Provider"]
n011["Relying Party Instance"]
n05["Common trust infrastructure(Metadata + URLs of the Trusted Lists and LoTEs)EU Commisson"]
n06["- PID Provider<br/>- Attestation Provider&nbsp; (QEAA/EAA/Pub-EAA"]
n014["RegistrarMember States"]
n0OqG462VzuzaBs0EC9eQU_37[" "]
n0tklJ06Eg1gI686ZZUtUN_42["WIAs KAs"]
n0tklJ06Eg1gI686ZZUtUN_44(("AccessCA"))
n0tklJ06Eg1gI686ZZUtUN_47(("Provider of registrationcertificates"))
n0tklJ06Eg1gI686ZZUtUN_60[" "]
n0tklJ06Eg1gI686ZZUtUN_61["RegistrarMember States"]
n0tklJ06Eg1gI686ZZUtUN_62(("AccessCA"))
n0tklJ06Eg1gI686ZZUtUN_63(("Provider of registrationcertificates"))
n0tklJ06Eg1gI686ZZUtUN_67[" "]
n0tklJ06Eg1gI686ZZUtUN_68["Member States"]
n0tklJ06Eg1gI686ZZUtUN_71["User"]
n0I7to5rTce0LnQP7jjDGX_36["API"]
n0I7to5rTce0LnQP7jjDGX_37["API"]
n019 -->|Issues<br/>WIAs and KAs| n020
n02 -->|AuthN| n020
n019 -->|AuthN| n020
n020 -->|AuthN & AuthZ<br/>Request PIDs,<br/>attestations| n011
n011 -->|Send registration<br/>certificate(s)<br/>(if available)| n03
n011 -->|Issue access<br/>certificate| n0tklJ06Eg1gI686ZZUtUN_44
n03 -->|Issue access<br/>certificate| n0tklJ06Eg1gI686ZZUtUN_44
n03 -->|Issue registration<br/>certificates(s)<br/>(optional)| n0tklJ06Eg1gI686ZZUtUN_47
n05 -->|Notifies<br/>1 - Access CAs<br/>2 - Providers of registration certificates| n014
n011 -->|Get the Trusted Lists<br/>and LoTEs of<br/>1 - PID / Attestation Providers<br/>2 - Wallet Providers| n05
n020 -->|Get the Trusted Lists<br/>and LoTEs of<br/>1 - Access CAs<br/>2 - Providers of registration certificates<br/>3 - PID / Attestation Providers| n05
n06 -->|AuthN & AuthZ<br/>Request PIDs,<br/>attestations| n020
n06 -->|Get the LoTEs of<br/>1 - Wallet Providers| n05
n06 -->|Issue access<br/>certificate(s)| n0tklJ06Eg1gI686ZZUtUN_62
n06 -->|Issue<br/>registration<br/>certificate(s)<br/>(optional)| n0tklJ06Eg1gI686ZZUtUN_63
n05 -->|Notifies<br/>1 - PID / Attestation Providers<br/>2 - Access CAs<br/>3 - Providers of registration certificates| n0tklJ06Eg1gI686ZZUtUN_61
n05 -->|Notifies<br/>1 - Wallet Providers| n0tklJ06Eg1gI686ZZUtUN_68
n019 -->|Designated as<br/>Wallet Provider| n0tklJ06Eg1gI686ZZUtUN_68
style n0tklJ06Eg1gI686ZZUtUN_59 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_58 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_57 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_56 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_53 stroke: #d6b656,color: #000000,fill: #fff2cc
style n02 stroke: none,color: #000000,fill: #A0C0FF
style n03 stroke: #d6b656,color: #000000,fill: #fff2cc
style n020 stroke: #9673a6,color: #000000,fill: #e1d5e7
style n019 stroke: #d6b656,color: #000000,fill: #fff2cc
style n011 stroke: #d6b656,color: #000000,fill: #fff2cc
style n05 stroke: #b85450,color: #000000,fill: #f8cecc
style n06 stroke: #d6b656,color: #000000,fill: #fff2cc
style n014 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_42 stroke: #b85450,color: #000000,fill: #f8cecc
style n0tklJ06Eg1gI686ZZUtUN_44 stroke: #b85450,color: #000000,fill: #f8cecc
style n0tklJ06Eg1gI686ZZUtUN_47 stroke: #b85450,color: #000000,stroke-dasharray: 1, 5,fill: #f8cecc
style n0tklJ06Eg1gI686ZZUtUN_60 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_61 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_62 stroke: #b85450,color: #000000,fill: #f8cecc
style n0tklJ06Eg1gI686ZZUtUN_63 stroke: #b85450,color: #000000,stroke-dasharray: 1, 5,fill: #f8cecc
style n0tklJ06Eg1gI686ZZUtUN_67 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_68 stroke: #d6b656,color: #000000,fill: #fff2cc
style n0tklJ06Eg1gI686ZZUtUN_71 stroke: none,color: #000000,fill: none
style n0I7to5rTce0LnQP7jjDGX_36 stroke: #d6b656,color: #000000,fill: #ffdb70
style n0I7to5rTce0LnQP7jjDGX_37 stroke: #d6b656,color: #000000,fill: #ffdb70
linkStyle 0 stroke: #7a7a7a,color: #000000
linkStyle 1 stroke: #7a7a7a
linkStyle 2 stroke: #7a7a7a,color: #000000
linkStyle 3 stroke: #7a7a7a,color: #000000
linkStyle 4 stroke: #7a7a7a,color: #000000
linkStyle 5 stroke: #7a7a7a,color: #000000
linkStyle 6 stroke: #7a7a7a,color: #000000
linkStyle 7 stroke: #7a7a7a,color: #000000,stroke-dasharray: 1, 5
linkStyle 8 stroke: #7a7a7a,color: #000000
linkStyle 9 stroke: #7a7a7a,color: #000000
linkStyle 10 stroke: #7a7a7a,color: #000000
linkStyle 11 stroke: #7a7a7a,color: #000000
linkStyle 12 stroke: #7a7a7a,color: #000000
linkStyle 13 stroke: #7a7a7a,color: #000000
linkStyle 14 stroke: #7a7a7a,color: #000000,stroke-dasharray: 1, 5
linkStyle 15 stroke: #7a7a7a,color: #000000
linkStyle 16 stroke: #7a7a7a,color: #000000
linkStyle 17 stroke: #7a7a7a,color: #000000
```

Figure 12 illustrates the main entities and their relationships in the trust model
of the EUDI Wallet ecosystem.

At its core is the **Wallet Unit** (top middle, blue), which interacts with
various entities throughout its lifecycle. The Wallet Unit lifecycle is described
in [Section 6.5][65-trust-throughout-a-wallet-unit-lifecycle] and consists of
installation, activation, management, and uninstallation. Each Wallet Unit is a
configuration of a **Wallet Solution**, comprising a
**Wallet Instance**, a **WSCA/WSCD**, and one or more **keystores**, provided by
a **Wallet
Provider** or by the **User's device**. The User installs a Wallet Instance on their device, which leads to the activation of the Wallet Unit by the Wallet Provider. The Wallet Provider manages a Wallet Unit until it is uninstalled by the User.
The Wallet Provider ensures that a valid Wallet Unit is in possession of at
least one **Key Attestation (KA)** for each WSCA/WSCD or keystore, and at least one **Wallet Instance Attestation (WIA)**. A KA attests the properties of a WSCA/WSCD or keystore and contains public keys for cryptographic binding. A WIA attests the integrity and revocation status of the Wallet Instance and describes the associated Wallet Solution. The Wallet Provider can revoke the Wallet Instance via the WIA revocation status to revoke the Wallet Unit. The Wallet Provider can revoke a WSCA/WSCD or keystore via the KA revocation status. See [Section 6.5][65-trust-throughout-a-wallet-unit-lifecycle].

The Wallet Unit handles User **PIDs** and **attestations** (QEAAs, PuB-EAAs, and
non-qualified EAAs). PIDs are issued by **PID Providers** and attestations by
**Attestation Providers**, both positioned to the left of the Wallet Unit in
[Figure 12][61-scope]. Before interacting with a Wallet Unit, these Providers
must be registered by a **Registrar**. Upon registration, they receive one or more
**access certificates** from an
**Access Certificate Authority** associated with the Registrar. They also obtain one or more **registration certificates** from an associated
**Provider of registration certificates**.
See [Section 6.3][63-trust-throughout-a-pid-provider-or-an-attestation-provider-lifecycle].

After a Wallet Unit has received a PID or attestation, it can present **User
attributes** to **Relying Party Instances** (right side of [Figure
12][61-scope]). These instances are hardware/software setups enabling
**Relying Parties** to interact with Wallet Units. Like a PID Provider or
Attestation Providers, Relying Parties register with a
**Registrar** in their Member State, and receive one or more **access certificates** for
each of their Relying Party Instances.
In addition, a Relying Party obtains one or more
**registration certificates** from a Provider of registration certificates
associated with the Registrar. This is discussed in [Section 6.4][64-trust-throughout-a-relying-party-lifecycle].

Notes:

- This conceptual trust model may be implemented with slight variations across
Member States, such as adopting one or multiple Certification Authorities or
leveraging existing entities that already fulfil this role.
- For PIDs, qualified EAAs, and PuB-EAAs, interoperability is essential ([Section
4.2.3][423-interoperability]). Interoperability is achieved by using a PKI
following X.509 certificate standards
([RFC 5280](https://datatracker.ietf.org/doc/html/rfc5280),
[RFC 3647](https://datatracker.ietf.org/doc/html/rfc3647)) for signing PIDs, QEAAs, and PuB-EAAs. Non-qualified EAAs
may adopt alternative trust models and verification mechanisms.
- The model supports both remote (see [Section 4.4.2][442-proximity-presentation-flows]) and proximity (see [Section 4.4.3][443-remote-presentation-transaction-flows] use cases.
- This version of the ARF does not yet include trust interactions for
qualified electronic signatures or seals; see [Topic 16][topic-16].
- Besides the trust relationships described in this chapter, other trust
relations are established as well. For instance, Users, PID Providers,
Attestation Providers, and Relying Parties trust Conformity Assessment Bodies and
Trusted List Providers (i.e., Member States) or LoTE Providers (i.e., the Commission). This trust is primarily rooted in authority and in
procedural measures, such as public oversight, published security and
operational policies, and audits, rather than in technical measures. To verify
that entities are indeed interacting with a trusted authority, standard
technical measures suitable for the context will be used.

### 6.2 Trust throughout a Wallet Provider lifecycle

#### 6.2.1 Wallet Provider lifecycle

[Section 4.6.2][462-wallet-provider] presented the lifecycle of a Wallet Provider:

1. The Wallet Provider is notified to the
Commission by a Member State. This is discussed in [Section 6.2.2][622-wallet-provider-notification].
1. Under specific conditions, a Member State may decide to change the status of a
registered Wallet Provider to Invalid. This is discussed in [Section 6.2.3][623-wallet-provider-invalidation].

#### 6.2.2 Wallet Provider notification

[Figure 12][61-scope] depicts the Wallet Provider to the top of the Wallet
Unit. To the left and below of this, the figure also shows that a Member State notifies the Wallet Provider and its (certified) Wallet Solution(s) to the European Commission. Note that Wallet Providers are not registered according to [CIR 2025/848], like Relying Parties, PID Providers, and Attestation Providers are. Wallet Providers consequently do not receive access certificates or registration certificates. This is because there is no need for interoperability between Wallet Providers and Wallet Units; each Wallet Provider only needs to communicate with its own Wallet Units.

Instead, the Wallet Solution provided by the Wallet Provider is certified as described in
[Chapter 7][7-wallet-solution-certification-and-risk-management], and then registered in accordance with [CIR 2024/2980]. In that process, information about the corresponding Wallet Provider, including its trust anchors, is notified by the Member State. If the notification process is successful, the Commission includes the trust anchors
of the Wallet Provider in the Wallet Provider LoTE. 

During issuance of a PID or attestation, a PID Provider or Attestation Provider can use these trust anchors for two purposes:

- to verify the authenticity of WIAs and KAs they obtain from Wallet Units, so they can be sure they are dealing with an authentic Wallet Unit from a trusted Wallet Provider.
- to verify the authenticity of Attestation Status Lists they use to verify the revocation status of received WIAs and KAs.

Note that the trust anchors for these two purposes may be the same. However, they also may be different, because a Wallet Provider can outsource the responsibility of providing revocation lists to a third party. However, if so, the Wallet Provider ensures that the relevant trust anchors are included in the Wallet Provider LoTE.

See [Section 6.6.2.4][6624-pid-provider-or-attestation-provider-validates-the-wallet-unit] and [Topic 9][topic-9].

More details on the Wallet Provider notification process can be found in [Topic 31][topic-31].

#### 6.2.3 Wallet Provider invalidation

The Member State may decide to notify the Commission that the Wallet Provider's status in the
corresponding LoTE should be changed to Invalid. As a result of this status
change, PID Providers and Attestation Providers will no longer
trust the trust anchors of the Wallet Provider, which they need to verify the KAs and WIAs they receive from Wallet Units. They will therefore refuse to issue PIDs and attestations to any Wallet Unit provided by that Wallet Provider. The Member State can subsequently notify the Commission that the Wallet Provider's status should be changed to Valid again. The notification of the status change and its reflection in the Wallet Provider LoTE follow the procedures laid down in [CIR 2024/2980].

As a result of being invalidated, the Wallet Provider will revoke its valid Wallet Units, see [Section 6.5.4.2][6542-wallet-unit-revocation]. 

>Note that independently of the status of the Wallet Provider, its Wallet Solution may be suspended or withdrawn, see [Section 4.6.3][463-wallet-solution]. In that case, the Wallet Provider revokes all associated Wallet Units if necessary, see [Section 6.5.4.2][6542-wallet-unit-revocation]. The result is the same: PID Providers and Attestation Providers will stop issuing PIDs and attestations to these Wallet Units.

### 6.3 Trust throughout a PID Provider or an Attestation Provider lifecycle

#### 6.3.1 PID Provider or Attestation Provider lifecycle

[Section 4.6.5][465-pid-provider-or-attestation-provider] presented the
lifecycle of a PID Provider or Attestation Provider:

1. A PID Provider or an Attestation Provider is registered by a Registrar in its Member State. This is discussed in [Section 6.3.2][632-pid-provider-or-attestation-provider-registration-and-notification].
2. Under specific conditions, the Registrar may decide to suspend or
cancel registration of a registered PID Provider or Attestation Provider. This
is discussed in [Section 6.3.3][633-suspension-or-cancellation-of-the-registration-of-a-pid-provider-or-attestation-provider].

#### 6.3.2 PID Provider or Attestation Provider registration and notification

##### 6.3.2.1 Introduction

[Figure 12][61-scope] depicts the PID Providers and Attestation Providers to
the left of the Wallet Unit. To the left and below of this, the figure also
shows that each PID Provider and Attestation Provider will register itself with
a Registrar in its Member
State. The Member State conditionally notifies a PID Provider or Attestation Provider to the
European Commission:

- **PID Providers** are notified to the Commission.
- **QEAA Providers** are not notified to the Commission, except for establishing the [Art. 22](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=uriserv%3AOJ.L_.2014.257.01.0073.01.ENG#d1e2162-73-1) Trusted List once a qualified status is granted.
- **PuB-EAA Providers** are notified to the Commission.
- **Non-qualified EAA Providers** are not notified to the Commission.

If the registration and notification processes are successful, at least the
following happens:

- Data about the PID Provider or Attestation Provider is included in the
registry of the relevant Registrar.
- The PID Provider or Attestation Provider receives one or more access certificates and
one or more registration certificates.
- The trust anchors of the PID Provider or Attestation Provider are conditionally included in
a Trusted List or LoTE.

These processes are discussed in the next subsections.

##### 6.3.2.2 Data about the PID Provider or Attestation Provider is included in the registry

When a PID Provider or Attestation Provider is registered, the Registrar
registers a set of data about the PID Provider or Attestation Provider in its
register. The Registrar makes the contents of the register available to the
general public, both in machine-readable and human-readable format. High-level
requirements on the registration process can be found in [Topic 27][topic-27].

The data to be registered about a PID Provider, QEAA Provider, PuB-EAA Provider,
or EAA Provider includes the PID or attestation type(s) that the Provider intends to
issue to Wallet Units. This enables Wallet Units and Relying Parties to verify
that a given PID Provider or Attestation Provider registered its intent to issue
a specific PID or attestation type. For example, a PuB-EAA Provider may have registered
for issuing mDLs, but not to issue diplomas.

Regarding PID Providers or QEAA Providers, it may be argued that Wallet Units do
not have to do this verification, since these are trusted parties. Nevertheless,
it is beneficial if a Wallet Unit verifies if a PID Provider or QEAA Provider is
registered for issuing a PID or a particular type of QEAA, prior to requesting
the issuance of such a PID or QEAA. Doing this helps to prevent attempts to
issue a PID or attestation while not being entitled to do so, either
fraudulently or as a result of an error.

Note that the Registrar collects the following information only for the purpose of transparency and does not apply any pre-authorisation process on it:

- Contact information of the registering PID Provider or Attestation Provider, 
- Description of the services of the PID Provider or Attestation Provider, 
- Types of attestation registered.

In particular, registration of a specific attestation type for a specific PID Provider or Attestation Provider does not imply that the Registrar (or any other entity in the EUDI Wallet ecosystem) authorises the Provider to issue attestations of that type. If authorisation is necessary for issuing a specific attestation type, it takes place out of scope of the EUDI Wallet ecosystem.

##### 6.3.2.3 PID Provider or Attestation Provider receives access certificate(s) and registration certificate(s)

When a PID Provider or Attestation Provider is registered by a Member State, an
Access Certificate Authority (see [Section 3.18][318-access-certificate-authorities])
issues one or more access certificates to the PID Provider or to the Attestation
Provider. A PID Provider or an Attestation Provider needs such a certificate to
authenticate itself towards a Wallet Unit when issuing a PID or an attestation
to it, as described in [Section 6.6.2.2][6622-wallet-unit-authenticates-the-pid-provider-or-attestation-provider].

A PID Provider access certificate does not indicate that its subject is a PID
Provider. Similarly, an Attestation Provider access certificate does not
indicate that its subject is a QEAA Provider, a PuB-EAA Provider, or a
non-qualified EAA Provider. Furthermore, the access certificate of a PID
Provider or Attestation Provider does not contain the Provider's registration to
issue attestations of a specific type, for instance an mDL or diploma. Such
information is instead included in registration certificates. Upon registration, the PID Provider or Attestation Provider receives one or more registration certificates from a Provider of registration certificates, see [Section 3.19][319-providers-of-registration-certificates].

A Wallet Unit can use the information in the registration
certificate to verify that an Attestation Provider it is contacting to issue a specific type of attestation is
in fact registered for that type of attestation.  The information in a registration certificate is also available in human-readable and machine-readable format via the Registrar's online service. The API and interfaces for that are specified in [Technical Specification 5](../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md). 

The PID Provider or Attestation Provider includes an access certificate and a registration certificate in its Credential Issuer metadata, specified per [OpenID4VCI] and [ETSI TS 119 472-3], to make them available to Wallet Units. 

Note that an Attestation Provider may simultaneously be a Relying Party, for
instance in case it intends to request data from the User's PID during issuance
of an attestation. Such an Attestation Provider would then register both as a
Relying Party (which is called a Service Provider in [Technical Specification 5](../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md))
and as a QEAA Provider, PuB-EAA Provider, or non-qualified EAA Provider. In that
case, the registration certificate(s) issued to the Attestation Provider will include both roles. Registration certificates for Relying Parties are
discussed in [Section 6.4.2][642-relying-party-registration].

See [Sections 6.6.2.2][6622-wallet-unit-authenticates-the-pid-provider-or-attestation-provider] and [6.6.2.3][6623-wallet-unit-verifies-providers-entitlements-and-registered-attestation-types] to learn more about how Wallet Units use a PID Provider's or Attestation Provider's access certificates and registration certificates. 

##### 6.3.2.4 PID Provider or Attestation Provider trust anchors are conditionally included in a Trusted List or LoTE

For a PID Provider or a PuB-EAA Provider, successful
registration and notification also means that the Provider is notified to the
European Commission and that its trust anchors are included in the respective LoTE by the Commission. The trust anchors of a QEAA Provider are included in a Trusted List once it gets the qualified status.

Relying Parties can use these trust anchors for two purposes:

- to verify the authenticity of PIDs, QEAAs, and PuB-EAAs they obtain from Wallet Units.
- to verify the authenticity of Attestation Status Lists or Attestation Revocation Lists they use to verify the revocation status of received PIDs, QEAAs, and PuB-EAAs, if any.

Note that the trust anchors for these two purposes may be the same. However, they also may be different, because a PID Provider or Attestation Provider can outsource the responsibility of providing revocation lists to a third party. However, if so, the PID Provider or Attestation Provider ensures that the relevant trust anchors are included in the relevant Trusted List or LoTE.

Non-qualified EAA Providers are not notified by a Member State and their trust anchors are not
included in a LoTE by the Commission. However, if a Relying Party
requests a non-qualified EAA from a Wallet Instance, it must know how to obtain
the trust anchor it needs to verify the signature over that EAA.
To help with this, [Topic 12][topic-12]
recommends that the applicable Rulebook specifies the mechanisms enabling this.
This mechanism may be a LoTE complying with [ETSI TS 119 602]. However, other methods may be used as well, and even
if such a LoTE exists, it does not have to comply with the requirements
in [Topic 31][topic-31].

High-level requirements on the PID Provider or Attestation Provider notification
process, as well as on the information registered and published in the respective Trusted List or LoTE, can be found in
[Topic 31][topic-31].

#### 6.3.3 Suspension or cancellation of the registration of a PID Provider or Attestation Provider

Under specific conditions, a Registrar may decide to suspend or cancel the
registration of a PID Provider or Attestation Provider. The conditions for this
will be specified by each Registrar.

Suspension or cancellation implies that the PID Provider's or Attestation Provider's
access certificates are revoked. As a result, the PID Provider or Attestation
Provider will no longer be able to issue PIDs or attestations to Wallet Units.

For a PID Provider, QEAA Provider, or PuB-EAA Provider, suspension or
cancellation also implies that its status in the respective Trusted List or LoTE will be
changed to Invalid. As a result, Relying Parties will no longer trust PIDs or
attestations issued by that Provider. For non-qualified EAA Providers, the
applicable Rulebook (see [Topic 12][topic-12])
may define similar mechanisms ensuring that Relying Parties will no longer
trust the trust anchors of EAA Providers of which the registration was suspended
or cancelled.

When a Registrar suspends or cancels the registration of a PID Provider or Attestation
Provider, the PID Provider or Attestation Provider revokes all of their PIDs or
attestations as described in [Section 6.6.6.4][6664-pid-or-attestation-revocation].

### 6.4 Trust throughout a Relying Party lifecycle

#### 6.4.1 Relying Party lifecycle

[Section 4.6.7][467-relying-party] presented the lifecycle of a Relying Party:

1. A Relying Party is registered by a Registrar in the Member State where it
resides. Relying Party registration is discussed in [Section 6.4.2][642-relying-party-registration].
2. Under specific conditions, a Registrar may decide to suspend or cancel the
registration of a Relying Party. This is discussed in [Section 6.4.3][643-relying-party-suspension-or-cancellation].

#### 6.4.2 Relying Party registration

[Figure 12][61-scope] depicts the Relying Party Instance to the right of the
Wallet Unit. A Relying Party Instance is a combination of hardware and software
used by a Relying Party to interact with a Wallet Unit. A Relying Party can operate
multiple Relying Party Instances. This will happen especially in case the
interactions with the Wallet Unit take place in proximity; for instance, a
border control agency at an airport employing multiple lines (each operated by
an agency employee) where arriving passengers can present their PID. However, a
single Relying Party operating multiple Relying Party Instances can also happen
in a remote context, for example if there is an operational system (including a
remote Relying Party Instance) next to a fallback system used for business
continuity purposes. A Relying Party may also use multiple remote Relying Party
Instances for load distribution.

[Figure 12][61-scope] also shows the Relying Party. Below that, it shows that
each Relying Party will register itself with a Registrar in its Member State.
If the registration process is successful, the Registrar includes the Relying
Party in its public registry.

A Relying Party may register in the context of several services, having different
intended uses. Each intended use will require a different set of attributes to be
obtained from a Wallet Unit. As a result, a single Relying Party may register
multiple times and may be issued more than one registration certificate.

Note that the Registrar collects the following information only for the purpose of transparency and does not apply any pre-authorisation process on it:

- Contact information of the registering Relying Party, 
- Description of the services of the Relying Party, 
- Attributes registered for each intended use,
- Description of each intended use.

In particular, registration of a specific set of attributes for a specific intended use of a specific Relying Party does not imply that the Registrar (or any other entity in the EUDI Wallet ecosystem) authorises the Provider to request those attributes for that intended use. If authorisation is necessary for requesting specific attributes, it takes place out of scope of the EUDI Wallet ecosystem.

As a result of successful registration,

- a Provider of registration certificates (see [Section 3.19][319-providers-of-registration-certificates])
associated with the Registrar issues one or more registration certificates
to the Relying Party. The purpose of the registration certificate is described in
[Section 6.6.3.3][6633-wallet-unit-verifies-that-relying-party-does-not-request-more-attributes-than-it-registered]. The Provider of registration certificates complies with the requirements in [CIR 2025/848], including those for the associated policy and practice statement in Annex V. Issuance of registration certificates takes places in an automated manner and without undue delay.
- an Access Certificate Authority (see [Section 3.18][318-access-certificate-authorities])
associated with the Registrar issues an access certificate to each Relying Party
Instance of the Relying Party. A Relying Party Instance needs such a certificate
to authenticate itself towards Wallet Units when requesting the presentation of
attributes, as described in [Section 6.6.3.2][6632-wallet-unit-authenticates-the-relying-party-instance].
Issuing access certificates to a registered Relying Party is mandatory.

See [Sections 6.6.3.2][6632-wallet-unit-authenticates-the-relying-party-instance] and [6.6.3.3][6633-wallet-unit-verifies-that-relying-party-does-not-request-more-attributes-than-it-registered] to learn more about how Wallet Units use a Relying Party's access certificates and registration certificates. 

High-level requirements on the Relying Party registration process can be found
in [Topic 27][topic-27].

#### 6.4.3 Relying Party suspension or cancellation

Under specific conditions, a Registrar may decide to suspend or cancel the
registration of a registered Relying Party. The conditions for this will be
specified by each Registrar.

Suspension or cancellation involves revocation of all valid access certificates of the Relying Party by the relevant Access CA, such that the Relying Party is no longer able to interact with Wallet Units. It also implies that all of the Relying Party's registration certificates are revoked. The Provider of registration certificates publishes revocation information (in the form of a status list) in accordance with [ETSI TS 119 475].
