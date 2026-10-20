---
name: "arf-topic-c-wallet-unit-attestation-part-1"
description: "Use when implementing Wallet Unit Attestation (WUA) or Wallet Instance Attestation (WIA). Covers WUA lifecycle, formats, key attestation, and WSCD binding. Part 1: covers 1 Introduction, 3 Purpose of the WUA, 4 Relation to Other Topics."
sections:
  - "C - Wallet Unit Attestation (WUA) and Key Attestation"
  - "1 Introduction"
  - "3 Purpose of the WUA"
  - "4 Relation to Other Topics"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~6793 -->

Version 0.4, updated 14 March 2025

# C - Wallet Unit Attestation (WUA) and Key Attestation

## 1 Introduction

### 1.1 Discussion Paper Topic Description

This document is the Discussion Paper for the European Digital Identity Cooperation Group regarding Topic C: Wallet Unit Attestation (WUA) and key attestation.
The ARF Development Plan [ARF_DevPlan] describes this Topic as follows:

*Define high-level requirements for WUA as defined in the IAs of article 5a, and for the key attestation.*

### 1.2 Key Words

This document uses the capitalised key words 'SHALL', 'SHOULD' and 'MAY' as specified in RFC 2119, i.e., to indicate requirements, recommendations and options specified in this document.
In addition, 'must' (non-capitalised) is used to indicate an external constraint, for instance a self-evident necessity or a requirement that is mandated by an external document. The word 'can' indicates a capability, whereas other words, such as 'will', 'is' or 'are' are intended as statements of fact.

### 1.3 Document Structure

The document is structured as follows:

- Chapter 2 presents the legal requirements for functionality related to the Wallet Unit Attestation and key attestation.

- Chapter 3 discusses the high-level purpose of the Wallet Unit Attestation and introduces the two use cases for WUA.

- Chapter 4 relates the topic to other topics being discussed, and to previously identified risks.

- Chapter 5 presents the additions and changes that will be made to the ARF as a result of discussing this topic with Member States.

### Change log

- Changes for Version 0.3:
  - Added Chapter 3.1, describing the use cases WUA should support.
  - Updated revocation discussion in Chapter 3
  - Restructured the HLRs
  - Added, removed and changed HLR.
- Changes for Version 0.2:
  - Updated discussions on revocation and cryptographic binding
  - Changes to HLRs

Multiple legal texts impose direct requirements on the Wallet Unit Attestation, and impose requirements that are solved by using Wallet Unit Attestations: [CIR 2024/2977], [CIR 2024/2979], [CIR 2024/2982], and the [European Digital Identity Regulation]. This section recaps the respective legal requirements from these sources.

### 2.1 [European Digital Identity Regulation] about the Wallet Unit Attestation

 The [European Digital Identity Regulation] does not directly address the need for Wallet Unit Attestations. Rather, it requires that it should be possible to verify the authenticity and validity of a Wallet Unit.

Below are the actual excerpts from the Regulation, including the recitals and the Articles that establish these requirements.

**Recital (34)**

*The use of European Digital Identity Wallets as well as the discontinuation of their use should be the exclusive right and choice of users. Member States should develop simple and secure procedures for the users to request immediate revocation of validity of European Digital Identity Wallets, including in the case of loss or theft. Upon the death of the user or the cessation of activity by a legal person, a mechanism should be established to enable the authority responsible for settling the succession of the natural person or assets of the legal person to request the immediate revocation of European Digital Identity Wallets.*

**Article 5a European Digital Identity Wallets**

*... 4. European Digital Identity Wallets shall, in particular:\
...\
(a) support common protocols and interfaces:\
...\
(viii) for relying parties to verify the authenticity and validity of European Digital Identity Wallets;\
...\
... 8. Member States shall provide validation mechanisms free-of-charge, in order to:\
(a) ensure that the authenticity and validity of European Digital Identity Wallets can be verified;\
...\
...9. Member States shall ensure that the validity of the European Digital Identity Wallet can be revoked in the following circumstances:\
...*

### 2.2 [CIR 2024/2977] about the Wallet Unit Attestation

[CIR 2024/2977] specifies three main requirements related to the Wallet Unit Attestation:

1. PID issuers must ensure their data is cryptographically bound to the Wallet Unit during issuance.
2. PID issuers must verify that the Wallet Unit belongs to a trusted Wallet Solution.
3. Wallet Unit Attestations must support revocation.

Below are the actual excerpts from the CIR, including the recitals and the Articles that establish these requirements.

**Recital (10)**

*To protect the data of wallet users and to ensure the authenticity of electronic attestations of attributes, mechanisms
for the authentication of providers of electronic attestations of attributes, and for the verification of the authenticity
and validity of wallet units by that provider should apply prior to the issuance of the attestations to wallet units.*

**Article 3**

*5. Providers of person identification data shall ensure that person identification data that they issue is cryptographically bound to the wallet unit to which it is issued.*

*9. Before issuing person identification data to a wallet unit, providers of person identification data shall authenticate and validate the wallet unit attestation of the wallet unit and verify that the wallet unit belongs to a wallet solution the provider of person identification data accepts or use another authentication mechanism in accordance with an electronic identity scheme notified at assurance level high.*

**Article 5**

*4. Where providers of person identification data revoke person identification data issued to wallet units, they shall do so in each of the following circumstances:\
...\
(b) where the wallet unit attestation to which the person identification data was issued to has been revoked;*

### 2.3 [CIR 2024/2979] about the Wallet Unit Attestation

[CIR 2024/2979] specifies six main requirements related to the Wallet Unit Attestation:

1. Wallet Providers must ensure the Wallet Unit contains a Wallet Unit Attestation.
2. The WUA must contain a public key, where the corresponding private key is protected by a WSCD.
3. The WUA must be revocable only by the Wallet Provider that provided the WUA.
4. The Wallet Provider must have certain responsibilities in relation to the revocation of the WUA.
5. The WUA must contain information as to where revocation information can be found. This information must be made available in a privacy preserving manner.
6. In case a Wallet Unit requests the presentation of attributes from another Wallet Unit, relevant information contained in the WUA of the requesting Wallet Unit may be logged by the requested Wallet Unit.

Below are the actual excerpts from the CIR, including the recitals and the Articles that establish these requirements.

**Recital (7)**

*Wallet units are to enable providers of person identification data or electronic attestations of attributes to verify that
they are issuing this data or attestations to genuine wallet units of the wallet user.*

**Recital (8)**

*To ensure data protection by design and by default, the wallets should be provided with available state-of-the-art
privacy enhancing techniques. These features should provide the possibility that wallets can be used without the
wallet user being trackable across different wallet-relying parties, if applicable in the usage scenario. For instance,
wallet providers should consider state-of-the-art privacy mitigating measures in relation to wallet unit attestations,
such as using ephemeral wallet unit attestations or batch issuance. In addition, embedded disclosure policies should
warn the wallet users against inappropriate or illegal disclosure of attributes from electronic attestations of
attributes.*

**Recital (9)**

*Wallet unit attestations should make it possible for wallet-relying parties which request attributes from wallet units,
to verify the validity status of the wallet unit that they are communicating with, as wallet unit attestations are to be
revoked when a wallet unit is no longer considered valid. The information regarding the validity status of the wallet
units should be made available in an interoperable manner, to ensure that it can be used by all wallet-relying parties.
Moreover, for cases where wallet users lost their wallet units or no longer have control over it, wallet providers
should enable wallet users to request the revocation of their wallet unit. To ensure the privacy and unlinkability,
Member States should employ privacy preserving techniques also for the wallet unit attestation. This may include
the usage of multiple wallet unit attestations for different purposes, disclosing only the minimally relevant
information about the wallet necessary for a transaction, or to limit the lifetime of the wallet unit attestation as an
alternative to the use of revocation identifiers.*

**Article 6**

*1. Wallet providers shall ensure that each wallet unit contains wallet unit attestations.\
2. Wallet providers shall ensure that the wallet unit attestations referred to in paragraph 1 contain public keys and that the corresponding private keys are protected by a wallet secure cryptographic device.\
3. Wallet providers shall:\
( c ) ensure wallet users have the right to request revocation of their wallet unit attestations, using the authentication mechanisms referred to in point (b).*

**Article 7**

*1. Wallet providers shall be the only entities capable of revoking wallet unit attestations for wallet units that they have provided.\
2. Wallet providers shall establish a publicly available policy specifying the conditions and the timeframe for the revocation of wallet unit attestations.\
3. Where wallet providers have revoked wallet unit attestations, they shall inform affected wallet users within 24 hours of the revocation of their wallet units, including the reason for the revocation and the consequences for the wallet user. This information shall be provided in a manner that is concise, easily accessible and using clear and plain language.\
4. Where wallet providers have revoked wallet unit attestations, they shall make publicly available the validity status of the wallet unit attestation in a privacy preserving manner and describe the location of that information in the wallet unit attestation.*

**Article 9**

*2. The logged information shall at least contain:\
…\
(b) the name, contact details, and the unique identifier of the corresponding wallet-relying party and the Member State in which that wallet-relying party is established, or in case of other wallet units, relevant information from the wallet unit attestation;*

### 2.3 [CIR 2024/2982] about the Wallet Unit Attestation

[CIR 2024/2982] specifies four main requirements related to Wallet Unit Attestations:

1. Wallet Units must validate a WUA when interacting with other Wallet Units.
2. WUA information must be displayed to Users in certain cases.
3. Wallet Units must provide WUA to wallet-relying parties or Wallet Units upon request.
4. Wallet Units must provide a WUA to PID Providers or Attestation Providers upon request.

Below are the actual excerpts from the CIR, including the recitals and the Articles that establish these requirements.

**Recital (5)**

*In order to ensure transparency and trustworthiness of wallet-relying parties towards wallet users, the protocols and
interfaces used by the wallet solutions should provide wallet users with a reliable mechanism to authenticate wallet-
relying parties and other wallet units. Inversely, wallet providers should provide a mechanism to authenticate and
validate wallet units so that relying parties can receive assurances with respect to trustworthiness and authenticity
of the wallet units. Further, the technical infrastructure of the wallets should also be designed to ensure that only the
minimal necessary amount of data is transferred only to the authorised relying parties, while keeping unlinkability
between the different transactions. In order to facilitate the issuance of person identification data and electronic
attestations of attributes, all wallet solutions should support a minimum set of protocols and interfaces.*

**Article 3**

*Regarding the protocols and interfaces referred to in Articles 4 and 5, wallet providers shall ensure that wallet units:\
(2) authenticate and validate the wallet unit attestations of other wallet units where interacting with other wallet units;\
(3) authenticate and validate requests made using wallet-relying party access certificates or wallet unit attestations from other wallet units, where applicable;\
(5) display to wallet users information contained in the wallet-relying party access certificates or in the wallet unit attestations;\
(8) present wallet unit attestations of the wallet unit to wallet-relying parties or wallet units that request it;*

**Article 4**

*3. In relation to the issuance of person identification data and electronic attestations of attributes to a wallet unit, wallet
providers shall ensure that the following requirements are complied with:\
...\
(b) where wallet users use their wallet unit to interact with providers of person identification data or electronic attestations of attributes, wallet units shall enable authentication and validation of the wallet unit components by presenting the wallet unit attestations to those providers upon their request;*

## 3 Purpose of the WUA

The legal requirements quoted in Chapter 2 address different aspects related to the Wallet Unit Attestation. The aspects cover interaction with the User (i.e., requirements in relation to the User interface), interaction with other parties (i.e., what a WUA should be used for) and requirements on the WUA itself (i.e., essential information that should be contained in the WUA). This document will not go into requirements on the User interface, but will focus on how WUAs may be used in connection with other parties. The detailed information to be contained in the WUA will be described in a technical specification of the WUA.

**This document is ONLY intended to specify the high-level requirements related to the WUA. The technical specifications related to the WUA is to be developed by the Commission at a later point in time.**

The legal requirements in relation to the functional requirements of the WUA can be summarised as the following functional requirements:

1. Information contained in the WUA must allow Relying Parties, PID Providers and Attestation Providers, and other Wallet Units to validate the authenticity and revocation status of a Wallet Unit.
2. Wallet Providers must be able to revoke a Wallet Unit, by revoking the corresponding WUA(s).
3. Only the Wallet Provider of a Wallet Unit must be able to revoke that Wallet Unit.
4. It is the Wallets Provider's responsibility to create the WUA.
5. During issuance, PID Providers and Attestation Providers must be able to ensure their PIDs and attestations are cryptographically bound to the Wallet Unit.
6. The WUA must consider the privacy of the User, i.e., techniques from Topic A should be used.
7. Relying Parties on the one hand and PID Provider and Attestation Providers on the other hand require different information from the WUA.
8. The Wallet Unit must handle presentation of the WUA automatically, without the involvement of the User. 
9. The WUA must provide PID Providers and Attestation Providers assurance, that the private PID or attestation key is bound to the same WSCD as the WUA private key.

Based on these functional requirements, the following requirements with regard to the WUA itself can be derived:

1. The WUA must contain a public key, where the corresponding private key is protected by a WSCD.
2. The WUA must contain information allowing parties to check if a Wallet Unit has been revoked.
3. The WUA must contain information allowing parties to verify the validity of the Wallet Unit, i.e., the WUA must contain a signature from the Wallet Provider.
4. The WUA must support both long and short validity terms.

### 3.1 Use cases

The functional requirements described above can be summarised in two use cases related to the WUA:

- Use case 1 - Authenticity of the Wallet Unit: Many different entities in the EUDI Wallet ecosystem will need to verify the authenticity of a Wallet Unit, including its revocation status. These entities include PID Providers, Attestation Providers, and Relying Parties and other Wallet Units (for Wallet-to-Wallet interaction). This use case can be supported by basic meta information in the WUA, i.e. a revocation handle and a signature from the Wallet Provider.
- Use case 2 - Capabilities and keys of the Wallet Unit: Certain entities in the EUDI Wallet ecosystem (i.e. PID Providers and Attestation Providers) will need additional information on top of what is provided by use case 1. This information includes descriptions of the capabilities of the individual Wallet Unit, i.e. information on the WSCA/WSCD used.

Privacy is an issue in relation to WUA and entities should be restricted to Use case 1, unless they have an actual need for Use case 2. In practice, this means Relying Parties and other Wallet Units must not be allowed access to the information in the WUA suitable for Use case 2. Furthermore, the WUA should be treated as any other attestation with regard to privacy, i.e., the discussions and solutions of [Topic A - Privacy Risks and Mitigations] also apply for WUA.

Use case 2 can be achieved by implementing the WUA as a revocable signature on a public key, issued by the Wallet Provider. Additionally the WUA should contain relevant information on the Wallet Unit capabilities, including the properties of the WSCD/WSCA. These attributes must also be signed by the Wallet Provider and may be used to provide additional trust in the Wallet Unit. The signed attributes and public key (i.e. the WUA), may be seen as an attestation and can utilise other attestation specific requirements from the ARF if beneficial.

Use case 1 can be achieved similarly to Use case 2, except the WUA would not contain additional information/attributes on the Wallet Unit capabilities.

The WUA should use a format the entities of the EUDI Wallet ecosystem would expect, i.e. be compatible with the interfaces defined in the ARF.

This paper identifies two requirements in relation to WUA that warrant further discussion: cryptographic binding and revocation. These are discussed in the two next subsections.

### Cryptographic binding

[CIR 2024/2977], Article 3, states that:

*5. Providers of person identification data shall ensure that person identification data that they issue is cryptographically bound to the wallet unit to which it is issued.*

The meaning of 'cryptographically bound' is discussed in ARF section 6.6.3.8. The WUA is intended to support this functionality by providing a base of trust, i.e. an attestation on a public key and the capabilities of the Wallet Unit. This approach will provide a trusted foundation on which the Wallet Provider may choose to implement more advanced features. At the same time, this approach allows the WUA to be treated as "any other attestation".

### Revocation

[CIR 2024/2977], Article 5, states that:

*4. Where providers of person identification data revoke person identification data issued to wallet units, they shall do so in each of the following circumstances:\
...\
(b) where the wallet unit attestation to which the person identification data was issued to has been revoked;*

As the WUA is used to revoke Wallet Units, it plays an important role in relation to PID providers. The Wallet Provider is responsibly for providing the revocation functionality; however, how it is to be used is described in Topic 38, Wallet Unit Revocation and Topic 7, Attestation Revocation and revocation checking. In order to fulfil the requirement in [CIR 2024/2977], the PID providers must keep track of all Wallet Units (i.e. all WUAs they received from Wallet Units during PID issuance) to which PID has been issued and periodically (e.g. daily) monitor this list to check if a WUA has been revoked. For this to function, several properties are required:

- The validity period of the WUA used in connection with issuance (Use case 2) should be long, preferably as long as the expected lifetime of the Wallet Unit. In practice this may be hard to achieve, as the Wallet Provider would need to guess the expected lifetime of the Wallet Units.
- To mitigate the privacy risk of the long validity period of the WUA, the WUA should be a once-only attestation as specified in [Topic A].

These requirements are discussed in [Topic A], which discusses privacy risks related to the usage of attestations in general. These discussions also apply to the WUA. Note that the validity period of the WUA used in connection with Relying Parties can be shorter than in the issuance use case. This may make revocation easier to handle, however it will require more frequent interactions with the Wallet Provider, which could also raise privacy concerns.

## 4 Relation to Other Topics

Below we discuss how Wallet Unit Attestations relate to the other topics being discussed.

### 4.1 Privacy Risks and Mitigations

[Topic A - Privacy Risks and Mitigations](./a-privacy-risks-and-mitigations.md) highlight that a WUA functions like any other attestation and therefore the risks and mitigations are the same:

- PID Providers and Attestation providers may assume the role of Relying Party with regard to RP-linkability: When presenting a WUA to a PID Provider or Attestation Provider, the Provider may record fixed values (hashes etc.) in all WUAs it receives and use these to track the User.
- The Wallet Provider may assume the role of Attestation Provider with regard to AP-linkability: If the Wallet Provider colludes with Relying Parties (including PID Providers and Attestation providers), User behaviour may be tracked.
- Using one of the one-time, limited-time, rotating batch or per-relying part attestations will all work with WUA. Note that the use pattern of WUA (it is only intended for PID and Attestation providers during issuance), it will most likely only be used a few times with a few Relying Parties (i.e. PID and attestation providers).

### 4.2 Relation to Risk Register

The purpose of WUA is to allow parties interacting with the Wallet Unit to ensure they are interacting with a legitimate Wallet Unit. Therefore the WUA has
impact on several of the risks listed in the risk register for European Digital Identity Wallets [RiskRegister]:

<table>
<colgroup>
<col style="width: 31%" />
<col style="width: 14%" />
<col style="width: 53%" />
</colgroup>
<thead>
<tr>
<th><strong>Risk type </strong></th>
<th><strong>Risk ID </strong></th>
<th><strong>Related risk titles </strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R1</td>
<td>Creation or use of an existing electronic identity</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R2</td>
<td>Creation or use of a fake electronic identity</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R3</td>
<td>Creation or use of fake attributes</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R4</td>
<td>Identify theft</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R6</td>
<td>Data disclosure</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R7</td>
<td>Data manipulation</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R9</td>
<td>Unauthorised transaction</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R14</td>
<td>Surveillance</td>
</tr>
</tbody>
</table>

The use of WUA is a mitigating mechanism with regard to some of the Technical Threats from the [Risk Register] (threats labelled TTX.Y in
its section III). This is primarily TT2. Errors and misconfigurations, TT3. Use of unreliable resources and TT5.Malicious actions. In relation to these
threats, the WUA is used to ensure that the Wallet Unit is not compromised.

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R1. Creation or use of an existing electronic identity</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Creation or use of an existing electronic identity is defined as the creation of an electronic identity in a wallet that exists in the real world and is assigned to another user. By essence, this risk leads to the risks of Identity theft (R4), and Unauthorised transactions (R9).</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R2. Creation or use of a fake electronic identity</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Creation or use of a fake electronic identity is defined as the creation of an electronic identity in a wallet that does not exist
in the real world.</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R3. Creation or use of fake attributes</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Creation or use of fake attributes is defined as the creation or use of attributes that cannot be validated to be issued by the claimed provider and cannot be trusted.</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R4. Identity theft</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Identity theft is defined as the unauthorised acquisition of the wallet unit or loss of authentication factors enabling to
impersonate a person.</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R6. Data disclosure</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Data disclosure is defined as the unauthorised exposure of personal
data including special categories of personal data. The privacy breach risk
is very similar when considered from a privacy rather than security viewpoint.</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R7. Data manipulation</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Data manipulation is defined as the unauthorised alteration of data.</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R9. Unauthorised transaction</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Unauthorised transactions are defined as operational activities conducted without the permission or knowledge of the
wallet user. In many cases, an unauthorised transaction can lead to Identity theft (R4) or Data disclosure (R6). It is also
related to unauthorised transactions, such as the misuse of cryptographic keys.</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R14. Surveillance</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Surveillance, or monitoring, is defined as the unauthorised tracking
or observation of a wallet user's activities, communication, or data.
Surveillance is often related to inference, which is defined as the
deduction of sensitive or personal information from seemingly innocuous
data.</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>SR1. Wholesale surveillance</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Wholesale surveillance is defined as the tracking or observation of
the activities of many users through their wallet's communication or
data. Wholesale surveillance is often associated with surveillance (R14)
and inference at a global scale, where information about many users is
combined to deduce sensitive or personal data about users or to identify
statistical trends that can be used to design further attacks.</td>
</tr>
</tbody>
</table>

More specifically, [RiskRegister] describes the following threats in relation to wallet unit attestations:

<table style="width:100%;">
<colgroup>
<col style="width: 13%" />
<col style="width: 51%" />
<col style="width: 35%" />
</colgroup>
<thead>
<tr>
<th><strong>ID<br />
</strong><em>Identifier</em></th>
<th><strong>Threat description<br />
</strong><em>Description of the identified threat</em> (*)</th>
<th><strong>Risk title<br />
</strong><em>Related risks</em></th>
</tr>
</thead>
<tbody>
<tr>
<td>TR10</td>
<td>An attacker can activate a new wallet on an invalid WSCD.</td>
<td>Creation or use of an existing electronic identity (R1) / Creation or use of a fake electronic identity (R2)
</td>
</tr>
<tr>
<td>TR12</td>
<td>An attacker can circumvent the verification by the PID provider that the wallet is controlled by the user and have a PID issued into a compromised wallet under the attacker’s control.</td>
<td>Creation or use of an existing electronic identity (R1) / Identify theft (R4) / Unauthorised transaction (R9)</td>
</tr>
<tr>
<td>TR13</td>
<td>
An attacker can get a valid PID into an invalid Wallet Unit</td>
<td>
Creation or use of an existing electronic identity (R1) / Identify theft (R4) / Unauthorised transaction (R9)</td>
</tr>
<td>TR22</td>
<td>An attacker can circumvent the verification by the (Q)EAA provider that the wallet is in control of the user and have a (Q)EAA issued into a compromised wallet under the attacker’s control.</td>
<td>Creation or use of fake attributes (R3)</td>
</tr>
<td>TR39</td>
<td>An attacker can unlawfully trace wallet users using unique/traceable identifiers.
</td>
<td>Data disclosure (R6) / Surveillance (R14)</td>
</tr>
<tr>
<td>TR46</td>
<td>An attacker can bypass or subvert the performance of checks by the wallet that verify whether the PID has been revoked by the PID provider to always return success.</td>
<td>Data manipulation (R7)</td>
</tr>
<tr>
<td>TR56</td>
<td>An attacker can propose an application that mimics a specific legitimate wallet to users.</td>
<td>Identity theft (R4)</td>
</tr>
<tr>
<td>TR84</td>
<td>A group of colluding relying parties or PID providers can derive the user’s identity data beyond data known to them.</td>
<td>Surveillance (R14)</td>
<tr>
<td>TR85</td>
<td>An attacker can track and trace a user by using person
identification data of the user where identification of the user
is not required.</td>
<td>Surveillance (R14)</td>
</tr>
<tr>
<td>TR107</td>
<td>An attacker can steal information from a user by spoofing a wallet.</td>
<td>
Effect on various risks</td>
</tr>
<tr>
<td>TR112</td>
<td>An attacker can modify a legitimate wallet instance and propose it to users as a legitimate one.</td>
<td>Effect on various risks</td>
</tr>
</tbody>
</table>
