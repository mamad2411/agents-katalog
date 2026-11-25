---
name: "arf-topic-e-pseudonyms-and-user-authentica-part-2"
description: "Use when implementing pseudonyms or user authentication mechanisms. Covers verifiable pseudonyms, attested pseudonyms, scope-rate-limited pseudonyms, and ZKP-based approaches. Part 2: covers 6 Relation to Other Topics, 7 Changes to the ARF, 8 References ...."
sections:
  - "6 Relation to Other Topics"
  - "6.1 Topic A: Privacy Risks and Mitigations"
  - "6.2 Topic C: Wallet Unit Attestations"
  - "6.3 Topic F: Digital Credentials API"
  - "6.4 Relation to Risk Register"
  - "7 Changes to the ARF"
  - "7.1 Changes to Existing HLRs"
  - "8 References"
  - "Appendix A Questions Related to Use Cases A and B"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~6788 -->

## 6 Relation to Other Topics

This chapter discusses how pseudonyms relate to other topics being discussed.

### 6.1 Topic A: Privacy Risks and Mitigations

#### 6.1.1 Introduction

[Topic A - Privacy Risks and Mitigations](./a-privacy-risks-and-mitigations.md) discusses surveillance risks related to presenting PIDs and attestations. Similar concerns are relevant for the Pseudonym functionality defined by the [W3C WebAuthn] specification. In fact, from a linkability perspective, there are only minor differences between the attestations present in the registration flow of [WebAuthn] and other attestations such as PID and (Q)EAAs. [Section 6.4](#64-relation-to-risk-register) discusses how this relates to the risks and threats identified in the [RiskRegister].

The subsections below consider two different types of linkability concerns for the attestation types summarised in [Section 5.2.3](#523-pseudonym-attestation), namely Relying Party linkability and CA linkability. Note that the latter form of linkability is similar to what is dubbed Attestation Provider linkability in the discussion Paper for Topic A, but there is a mismatch between the use of the word "attestation" in the broader ARF framework and in [W3C WebAuthn] and to avoid confusion a different wording is used here.

#### 6.1.2 Relying Party Linkability

Relying Party linkability is the ability for Relying Parties to link together multiple authentications performed by a User using a Wallet Unit.
Note that it is inherent for the use cases that the **same** Relying Party shall be able to link together multiple presentations of a pseudonym, as it must be unique per Relying Party and per User. However, **different** Relying Parties should not be able to infer any information about whether they have interacted with one or multiple Users by comparing multiple authentications using pseudonyms.

To prevent Relying Party linkability, it is necessary to ensure that no unique (per Wallet Unit) value is presented to multiple different Relying Parties. Depending on the type of attestation used for registration (see [Section 5.2.3](#523-pseudonym-attestation), this may or may not be the case for [W3C WebAuthn].

If *Basic Attestations* are used, where each Wallet Unit holds only one attestation key pair and corresponding certificate, the public key of this attestation key pair may be such a unique value that is presented to multiple Relying Parties. [W3C WebAuthn] suggests to ensure that multiple different Authenticators hold the same attestation key pair, thereby no longer making it a unique value for correlation. However, please note that this implies letting several different Wallet Units share the same private key. This is against best security practices, as it implies private keys must be transferred to or from Wallet Units, which increases the risk of keys being compromised. It could however be deemed as a compromise to achieve better privacy properties – without necessarily ensuring it with high level of assurance. 

If an *Attestation CA* is used to issue certificates on multiple attestation keys, the degree to which Relying Parties can correlate the different certificates can be reduced. However, as long as an Authenticator uses a single attestation key more than once to sign a Pseudonym, the Relying Parties can still deduce some information by correlating attestation public keys. This mitigation is similar to the proposals of Method B and Method C (Limited-time Attestations and Rotating-batch Attestations) from the discussion paper on topic A.

If an *Anonymisation CA* is used to issue certificates on single-use-only attestation keys, Relying Parties are not able to correlate information about multiple presentations. This can be referred to as being *Relying Party-unlinkable*.

Neither *Self Attestation* nor *No Attestation* allows Relying Parties to correlate information about multiple presentations of pseudonyms, as no attestation public key is released to the Relying Party. That is, they are Relying Party-unlinkable.

#### 6.1.3 CA Linkability

Certificate Authority (CA) linkability is the ability for a CA to track a User's interactions at several different Relying Parties by combining the information from those Relying Parties with information hold by the CA.

Note that all attestation types that are Relying Party-linkable also are CA-linkable by definition, as the information available to CAs and Relying Parties is a superset of the information available only to multiple Relying Parties.

Both the types *Attestation CA* and *Anonymisation CA* are CA-linkable as CAs can store which public key they issue certificates to and share with which Wallet Unit. By correlating this with the information available at the Relying Parties, it is possible to track how a Wallet Unit uses the pseudonym functionality.

Neither *Self Attestation* nor *No Attestation* includes any information from a CA and Relying Parties are therefore not able to correlate information about multiple presentations of pseudonyms with this form of attestation type. That is, they are both also CA-unlinkable.

#### 6.1.4 Drawbacks of Different Attestation Types

The table below summarises information from the previous sections with regard to drawbacks of the different attestation types.

| Attestation Type | Drawbacks |
|--------------------|---------------------------------------|
| Basic Attestations | Relying Party-linkable and CA-linkable |
| Attestation CA     | CA-linkable and to some degree Relying Party-linkable |
| Anonymisation CA   | CA-linkable |
| Self Attestation   | No assurances for Relying Parties |
| No Attestation     | No assurances for Relying Parties |

### 6.2 Topic C: Wallet Unit Attestations

[Topic C - Wallet Unit Attestations (WUA) and Key Attestations](./c-wallet-unit-attestation.md) discusses how the Wallet Unit can document its functional and security capabilities, e.g., support for secure hardware, revocation status, etc. This is similar to the role of `attestations` in WebAuthn. 

Certain WUA attributes are somewhat sensitive, as they may allow for linkability, and are only intended for PID Providers and Attestation Providers when performing issuance. Other metadata in the WUA is used to prove that the Wallet Unit has not been revoked. This information is less sensitive.

When a Wallet Unit and a Relying Party perform registration of a pseudonym, key material will be stored on the Wallet Unit (in its role as Authenticator). During this registration, it may be possible to use the WUA similar to a pseudonym attestation (discussed in [Section 5.2.3](#523-pseudonym-attestation)). 

**Revocation / invalidation of pseudonyms:** Pseudonyms are local to each Relying Party, which makes revocation somewhat easy: The Relying Party can simply invalidate the pseudonym locally and the Wallet Unit will no longer be able to access that Relying Party. This revocation will not affect other functionality of the Wallet Unit, e.g., other Pseudonyms, PID and attestations will remain valid. In addition to local revocation, it was discussed at a Focus meeting, if it should be possible for a Relying Party to also revoke the entire Wallet Unit. The outcome of this discussion, was that it should not be possible for Relying Parties to request the revocation of a Wallet Unit.

### 6.3 Topic F: Digital Credentials API

As stated in [Chapter 5](#5-high-level-approach-to-pseudonyms-w3c-webauthn), [W3C WebAuthn] does not specify the interface between the Wallet Unit (i.e., Authenticator) and the Client used by the User to initiate the usage of the pseudonyms.

[Discussion Topic F](./f-digital-credential-api.md) must also take into account providing a seamless integration for the use of pseudonyms.

### 6.4 Relation to Risk Register

As pseudonyms may be used to provide authentication, a large number of the risks listed in the risk register for European Digital Identity Wallets [RiskRegister] are (at least indirectly) related to the use of pseudonyms:

<table>
<colgroup>
<col style="width: 31%" />
<col style="width: 14%" />
<col style="width: 53%" />
</colgroup>
<thead>
<tr>
<th><strong>Risk type </strong></th>
<th><strong>Risk ID </strong></th>
<th><strong>Related risk titles </strong></th>
</tr>
</thead>
<tbody>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R2</td>
<td>Creation or use of a fake electronic identity</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R4</td>
<td>Identify theft</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R5</td>
<td>Data theft</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R6</td>
<td>Data disclosure</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R9</td>
<td>Unauthorised transaction</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R10</td>
<td>Transaction manipulation</td>
</tr>
<tr>
<td><strong>High-level risks to the wallets</strong></td>
<td>R14</td>
<td>Surveillance</td>
</tr>
</tbody>
</table>

Some of the Technical Threats from the [Risk Register] (threats labelled TTX.Y in its section III) are also relevant threats to consider in the context of pseudonyms. This is primarily TT5. Malicious actions, in which threats, such as TT5.1 Interception of information or TT5.3 Replay of messages, may lead to the risks expressed in the table above.

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
<th><strong>R5. Data theft</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Data theft is defined as the unauthorised extraction of data. Data theft is also associated to threats, such as data interception
(unauthorised capture of data in transit) and data decryption (unauthorised decoding of encrypted data), which are likely to
lead in some cases to Data disclosure (R6).</td>
</tr>
</tbody>
</table>

<table>
<colgroup>
<col style="width: 100%" />
</colgroup>
<thead>
<tr>
<th><strong>R6. Data Disclosure</strong></th>
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
<th><strong>R10. Transaction manipulation</strong></th>
</tr>
</thead>
<tbody>
<tr>
<td>Transaction manipulation is defined as the unauthorised alteration of operations in the wallet. Transaction manipulation is
an attack on integrity, and it is related to a data integrity breach.</td>
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

More specifically, \[RiskRegister\] describes the following threats in relation to pseudonyms:

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
<td>TR1</td>
<td>An attacker can revoke pseudonyms without justified reason.</td>
<td>Creation or use of a fake electronic identity (R2)
</td>
</tr>
<tr>
<td>TR26</td>
<td>PID, (Q)EAAs or pseudonyms can be presented to a wrong relying party.</td>
<td>Data disclosure (R6)</td>
</tr>
<tr>
<td>TR39</td>
<td>An attacker can unlawfully trace wallet users using unique/traceable
identifiers.</td>
<td>Data disclosure (R6) and Surveillance (R14)</td>
</tr>
<td>TR51</td>
<td>An attacker can convince a user to share personal data (i.e. PID, EAA-s, pseudonyms, electronic signatures, logs and other data) with the attacker or with a third party that the user did not intend to do so.</td>
<td>Data theft (R5) / Data disclosure (R6)</td>
</tr>
<td>TR55</td>
<td>An attacker can bypass the user authentication method to use
a pseudonym generated by a wallet unit.
</td>
<td>Identity theft (R4)</td>
</tr>
<tr>
<td>TR84</td>
<td>A group of colluding relying parties or PID providers can derive the
user's identity data beyond data known to them.</td>
<td>Surveillance (R14)</td>
</tr>
<tr>
<td>TR85</td>
<td>An attacker can track and trace a user by using person
identification data of the user where identification of the user
is not required.</td>
<td>Surveillance (R14)</td>
</tr>
<tr>
<td>TR91</td>
<td>A relying party can replay elements from a previous session in
another session.</td>
<td>Transaction manipulation (R10)</td>
</tr>
<tr>
<td>TR102</td>
<td>An attacker can impersonate relying parties during the
connection to relying parties.</td>
<td>Unauthorised transaction (R9) / Data
disclosure (R6)</td>
</tr>
<tr>
<td>TR105</td>
<td>An attacker can perform man-in-the-middle attacks.</td>
<td>Unauthorised transaction (R9) / Data
disclosure (R6) / Surveillance (R14)</td>
</tr>
</tbody>
</table>

>Note that there is no threat corresponding to TR68-71 (Attacker can revoke without consent/reason) in relation to pseudonyms.

R14, SR1, TR39, and TR84 are particularly relevant to consider given the discussion in Chapter 5.1, namely linkability of attestations in [W3C WebAuthn].

TR26, TR102, and TR105 are particularly relevant for the challenge described in Chapter 4.3, namely that the Relying Party is only authenticated by the Client and not by the Wallet Unit.

## 7 Changes to the ARF

This chapter proposes changes and additions to the ARF, specifically to the  High Level Requirements (HLRs) for Annex 2 Topic 11 (Pseudonyms).

The existing HLRs in the ARF (version 2.5.0) were developed to support [Use Case A](#41-use-case-a-pseudonymous-authentication) and [Use Case B](#42-use-case-b-presentation-of-attributes-with-subsequent-authentication-using-pseudonyms). 

As previously noted, as it is possible to define custom types of (Q)EAAs in the ARF, [Use Case D](#44-use-case-d-linkable-pseudonymous-authentication) is already supported by the current functionality already included in the ARF. 

This discussion paper proposes changes in two categories: 
1. *Changes* to existing HLRs making it *optional* for Wallet Units to support the pseudonyms functionality required by the legislation by letting them be WebAuthn Authenticators rather than mandatory. These are presented in [Section 7.1](#71-changes-to-existing-hlrs).
2. *Additional* HLRs to guide future pseudonyms solutions to support also [Use Case C](#43-use-case-c-rate-limited-participation) in the context the EUDI Wallet ecosystem. These are presented in [Section 7.2](#72-new-guiding-hlrs-for-scope-rate-limited-pseudonyms). Note, however, that the EU Commission will not actively develop any such scheme fulfilling these HLRs. Instead, they are only meant as a guide for others to design and standardize protocols that may be included in a future version of the ARF.

### 7.1 Changes to Existing HLRs

The existing HLRs and [CIR.2024.2979] mandate that Wallet Units implement WebAuthn as an authenticator. However, as there already exists many WebAuthn authenticator implementations widely available to Users through their operating system, web browsers or specialized apps, we propose to weaken the requirements in the ARF and the CIR such that it becomes *optional* for a Wallet Unit to also be a WebAuthn authenticator and thereby free for Wallet Units to enable [Use Case A](#41-use-case-a-pseudonymous-authentication) and [Use Case B](#42-use-case-b-presentation-of-attributes-with-subsequent-authentication-using-pseudonyms) using alternative technologies. 

> Under Article 5a of the [European Digital Identity Regulation], EUDI Wallets must support the generation and storage of pseudonyms. This requirement remains intact. Our proposal only affects how this is achieved: implementing WebAuthn would remain one compliant approach, but not the only one. Wallet Units not following this path must use alternatives to live up to the legislation.

In the ARF v.2.5.0, there are 23 requirements related to pseudonyms. 
Of these, the first 20 requirements (PA\_01-PA\_19 and PA\_08a) are requirements to enable [Use Case A](#41-use-case-a-pseudonymous-authentication) and [Use Case B](#42-use-case-b-presentation-of-attributes-with-subsequent-authentication-using-pseudonyms) remains unaffected
The remaining three HLRs (PA\_20, PA\_21 and PA\_22) are specific to WebAuthn and we propose the following changes: 

| **Index** | **ARF v.2.5.0 specification**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            | **Proposed specification**                                                                                                                                                                                                                                                  |
|-----------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| PA_20     | The Wallet Unit SHALL verify the identity of a Relying Party when a User registers a Pseudonym or authenticates with a Pseudonym, provided the profile or extension of [W3C WebAuthn] meant in PA_21 enables the Wallet Unit to do this. In case the profile or extension does not enable this, the Wallet Unit SHALL trust the WebAuthn Client (i.e., the browser) to verify the Relying Party identity. *Notes: - [W3C WebAuthn] currently does not offer a way for an Authenticator (i.e., the Wallet Unit) to authenticate a Relying Party. Instead, the Client (i.e., the browser) will authenticate the Relying Party, using TLS.* | The Wallet Unit SHALL verify the identity of a Relying Party when a User registers a Pseudonym or authenticates with a Pseudonym. If the provided the profile or extension of [W3C WebAuthn] meant in PA_21 does not enable the Wallet Unit to do this, the Wallet Unit SHALL trust the WebAuthn Client (i.e., the browser) to verify the Relying Party identity. *Notes: - [W3C WebAuthn] currently does not offer a way for an Authenticator (i.e., the Wallet Unit) to authenticate a Relying Party. Instead, the Client (i.e., the browser) will authenticate the Relying Party, using TLS.*                                                                                                                                                                                                                                                                             |
| PA_21     | The Commission SHALL create or reference a technical specification containing a profile or extension of the [W3C WebAuthn] specification compliant with the HLRs specified in this Topic. This specification SHALL contain all details necessary for Wallet Units and Relying Parties to generate, register, and use Pseudonyms.                                                                                                                                                                                                                                                                                                         | No changes.                                                                                                                                                                                                                                                                 |
| PA_22     | Wallet Providers SHALL ensure that their Wallet Solution supports the [W3C WebAuthn] specification and the technical specification meant in requirement PA_21.                                                                                                                                                                                                                                                                                                                                                                                                                                                                           | Wallet Providers MAY ensure that their Wallet Solution supports the HLRs defined for this topic by letting their Wallet Units perform the role of a WebAuthn authenticator following the [W3C WebAuthn] specification and the technical specification referenced in referenced in PA\_21. |

#### 7.2 New Guiding HLRs for Scope Rate Limited Pseudonyms
The below HLRs will be added to the existing HLR in Annex 2, Topic 11 of the ARF v.2.5.0.

##### Requirement 1
The protocols and cryptography underlying the scope rate limited pseudonym functionality shall be standardized by a standardization organization recognized by the Commission or in a standard recognized by the Commission.

> Rationale: This is necessary to provide sufficient guarantees for the security of the functionality and to enable interoperability between different member states' implementations. 

##### Requirement 2
A protocol enabling scope rate limited pseudonyms SHALL enable a Wallet Unit to allow a User to generate a scope rate limited pseudonym, register this by a Relying Party, and prove that this is within the rate and scope restrictions determined by the Relying Party.

> Rationale: This is to support [Use Case C](#43-use-case-c-rate-limited-participation). 

##### Requirement 3
A protocol enabling scope rate limited pseudonyms SHALL allow a Relying Party to verify that the rate is not exceeded for a particular User when presented with a scope rate limited pseudonym.

> Rationale: This is to support [Use Case C](#43-use-case-c-rate-limited-participation). 

##### Requirement 4
A protocol enabling scope rate limited pseudonyms SHALL allow a Relying Party to choose the scope and rate when requesting a scope rate limited pseudonym from a User.

> Rationale: This is to support the widest possible range of use cases. 

##### Requirement 5
A protocol enabling scope rate limited pseudonyms SHALL NOT allow any entity or collusion of entities not including the User, to link scope rate limited pseudonyms of the same User when used across several different Relying Parties. This shall hold even if the scope and rate are identical across the different Relying Parties and both for registration and authentication of the scope rate limited pseudonym.

> Rationale: This is to protect the privacy of the user. In particular, this requirement also ensures that a Relying Party cannot choose the same scope as another Relying Party to break the unlinkability of the interactions between the Relying Parties. 

##### Requirement 6
A protocol enabling scope rate limited pseudonyms SHALL ensure that if the rate is larger than 1, then a User's different scope rate limited pseudonyms SHALL be unlinkable for the same scope. This SHALL hold against any entity or collusion of entities, not including the User. Further, such protocol SHALL ensure that during registration or authentication with such pseudonym it SHALL NOT be possible for the Relying Party to deduce any information about how many pseudonyms the particular User has already registered (except that it does not exceed the predetermined rate).

> Rationale: This is to protect the privacy of the user. 

##### Requirement 7
A protocol enabling scope rate limited pseudonyms SHALL ensure that no entity or collusion of entities, not including a User, is able to authenticate or register with a scope rate limited pseudonym of this User.

> Rationale: This is to ensure that no one can impersonate the User. 

##### Requirement 8
A Wallet Unit SHALL store cryptographic material necessary for authenticating as a scope rate limited pseudonyms in either a WSCD or in a keystore.

> Rationale: This is to ensure that the Wallet Unit takes measures to protect this material. It is however not given that it must be in a WSCD as it does not make sense to talk about LoA High for pseudonyms as these does not constitute an electronic means of identification.

##### Requirement 9
A User's scope rate limited pseudonyms for a particular scope and rate SHALL be persistent over time independently if whether they change Wallet Unit. 

> Rationale: This is to ensure that the rate for a given scope can really be trusted by RP. Note that this has the implications that some of the cryptographic material necessary for authenticating as a pseudonym must necessarily be backed up outside the User's physical device.

## 8 References

| Reference | Description |
|-----------------|-----------------|
| [W3C WebAuthn] | Web Authentication: An API for accessing Public Key Credentials Level 2 W3C Recommendation, 8 April 2021, <https://www.w3.org/TR/webauthn-2/> |
| [ARF_DevPlan] | Architecture and Reference Framework Development plan 2025, European Commission, v1.0.|
| [RiskRegister] | Annex 1 to the Commission Implementing Regulation laying down rules for the application of Regulation (EU) No 910/2014 of the European Parliament and of the Council as regards the certification of the European Digital Identity Wallets, European Commission, October 2024, draft |
| [European Digital Identity Regulation] | Regulation (EU) 2024/1183 of the European Parliament and of the Council of 11 April 2024 amending Regulation (EU) No 910/2014 as regards establishing the European Digital Identity Framework |
| [CIR.2024.2979] | Commission Implementing Regulation (EU) 2024/2979 of 28 November 2024 laying down rules for the application of Regulation (EU) No 910/2014 of the European Parliament and of the Council as regards the integrity and core functionalities of European Digital Identity Wallets |

## Appendix A Questions Related to Use Cases A and B
Below, we list questions that have been discussed at the focus meetings along with brief summaries of the conclusions.

**Question 1:** Should any other use cases be supported?

> It should be possible to register attributes to the pseudonym later than at registration. 

**Question 2:** For both use cases: Should both cross-device and same-device flows be supported?
I.e., should registration and authentication with pseudonyms be possible both when a user initiates the interactions with the Relying Party from the same device and with a device different from the one hosting the Wallet Unit? The answer to this question will impose requirements on the interfaces between the Wallet Unit and the client a user initiates the interaction with.

> Yes: Both cross-device and same-device flows should support pseudonyms

**Question 3:** For Use Case A: Should a single user be able to use their Wallet Unit to present several different pseudonyms to a single Relying Party? High-Level Requirements must be defined that enforces the answer to this question.

> Yes: It should be possible for a user to have several pseudonyms at the same Relying Party (see [PA_04](../annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a-hlrs-related-to-use-cases-a-and-b).

**Question 4:** For both use cases: What assurances must be given to the Relying Party? Such possible assurance exists on at least three levels:

1. No assurances are given to the Relying Party. I.e., the Relying Party is not even guaranteed that it is interacting with the Wallet Unit.
2. The Relying Party is assured that the private key corresponding to the pseudonym being stored/authenticated *was* originally stored in a Wallet Unit.
3. The Relying Party is assured that the private key corresponding to the pseudonym being stored/authenticated *is* currently stored in a non-revoked Wallet Unit.
4. For use case B: The Relying Party is assured that the private key corresponding to the pseudonym used to authenticate is stored on the same Wallet Unit as the originally presented PID or attestation.

> There should be some assurance that keys are stored securely and option 4.

Note that, because the technical implementation of pseudonyms must rely on [W3C WebAuthn], the possibility for achieving such assurances is to use attestations (for an explanation of this see  [Chapter 5](#5-high-level-approach-to-pseudonyms-w3c-webauthn)).
Therefore, higher assurances comes with a trade-off in terms of surveillance risks.
For a further discussion of these risks see [Chapter 6.1](#61-topic-a-privacy-risks-and-mitigations)).
