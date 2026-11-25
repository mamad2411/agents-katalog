---
name: "arf-topic-x-relying-party-registration-part-3"
description: "Use when implementing RP registration and access certificate management. Covers registration workflows, certificate issuance, attribute disclosure policies, and RP trust framework. Part 3: covers 4 Current HLRs and Proposals of Changes, 5 Relation to Other Topics."
sections:
  - "4 Current HLRs and Proposals of Changes"
  - "4.1 Topic 27 - Registration of PID Providers, Providers of QEAAs, PuB-EAAs, and (non-qualified) EAAs, and Relying Parties"
  - "4.2 Topic 44 - Relying Party Registration Certificates"
  - "4.3 Topic 52 - Relying Party Intermediaries"
  - "5 Relation to Other Topics"
  - "5.1 Topic 6 - Relying Party authentication and User approval"
  - "5.2 Topic 31 - PID Provider, Wallet Provider, Attestation Provider, and Access Certificate Authority notification and publication"
  - "5.3 Use of Certificate Transparency"
  - "5.4 User requesting data deletion to relying parties"
  - "5.5 User reporting unlawful or suspicious request of data to DPAs"
  - "5.6 Relation to Risk Register"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~7341 -->

## 4 Current HLRs and Proposals of Changes


The ARF, Annex 2, Topic 27, Topic 44 and Topic 52, contains a number of High-Level Requirements related to the topic.

The Topic 27 requirements cover general requirements for Member State registration processes and specific requirements for the registration of Relying Parties, whereas Topic 44 covers issuance of Relying Party registration certificates. Topic 52 focuses on the intermediaries.

The existing HLRs are listed in the tables below, along with a proposal to keep, change, add, or remove the HLR.

### 4.1 Topic 27 - Registration of PID Providers, Providers of QEAAs, PuB-EAAs, and (non-qualified) EAAs, and Relying Parties

A.  General requirements for Member State registration processes

| **Index** | **Requirement specification** | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_01    | Member States SHALL provide processes and mechanisms for PID Providers, QEAA Providers, PuB-EAA Providers, (non-qualified) EAA Providers, and other Relying Parties to register in a registry. *Note: Member States may choose to implement a single registry for all these roles, or a separate registry for each of these roles, or organise registries e.g. per applicable sector.* |       Keep with proposed change       |
| Reg_02    | Member States SHALL make publicly available all necessary details and documentation about the registration processes for their registry. |        Keep      |
| Reg_03    | Member States SHALL publish the registry entries online, in a sealed or signed machine-readable common format suitable for automated processing, according to the [European Digital Identity Regulation] Article 5b 5, for the purpose of transparency to Users and other stakeholders. |      Keep        |
| Reg_04    | Member States SHALL make the registry available online, in a common human-readable format. |      Keep        |
| Reg_05    | The Commission SHALL establish a technical specification for the common formats mentioned in Reg_03 and Reg_04. |          Keep    |
| Reg_06    | The Commission SHALL provide specifications for a common API for retrieving registry entries from the Member States registries per Reg_03, defining the minimum requirements for interoperability. *Note: Requirements for this API are defined in Reg_08 and Reg_09.* |      Keep     |
| Reg_07    | The Commission SHALL provide specifications for a common user interface for accessing the Member State registries per Reg_04. *Note: Requirements for this user interface are defined in Reg_08 and Reg_09.* |      Keep        |
| Reg_08    | The API mentioned in Reg_06 and the user interface mentioned in Reg_07 SHALL use a secure channel protecting the authenticity and integrity of the information in the registry during transport. |    Keep      |
| Reg_09    | The API mentioned in Reg_06 and the user interface mentioned in Reg_07 SHALL NOT require authentication or prior registration and authorisation of any entity wishing to retrieve the information in the registry. |      Keep    | 

B. *General requirements for the issuance of access certificates*

| **Index** | **Requirement specification**                                | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_10    | A Member State SHALL ensure that an Access Certificate Authority notified according to [[Topic 31][topic-31]] issues access certificates on request to Relying Parties, including the PID Providers, QEAA Providers, PuB-EAA Providers and (non-qualified) EAA Providers registered in one of the Member State's registries.| Keep with proposed changes |
| Reg_11    | A Member State SHALL ensure that the issuance process of access certificates by their notified Access Certificate Authority(s) complies with a common Certificate Policy for Access Certificate Authority. |  Keep    |
| Reg_12    | The Commission SHALL provide technical specifications establishing the common Access Certificate Authority Certificate Policy mentioned in Reg_11. |    Keep   |
| Reg_13    | The common Certificate Policy mentioned in Reg_12 SHALL require that an Access Certificate Authority logs all issued certificates for Certificate Transparency (CT). *Note: This requirement is still under discussion and might be changed or removed in a future version of this ARF.*| Keep  |
| Reg_14    | The common Certificate Policy mentioned in Reg_12 SHALL require that an Access Certificate Authority provides one or more method(s) to revoke the access certificates it issued. | Keep  |
| Reg_15    | The common Certificate Policy mentioned in Reg_12 SHALL include a policy for revocation, which SHALL require that an Access Certificate Authority revokes all access certificates of the certificate subject at least when: - the certificate subject which is a Relying Party is cancelled by the respective Registrar,  - on request of the certificate subject, or - on request of a national supervisory body.| Keep with proposed changes |
| Reg_15b   | The common Certificate Policy mentioned in Reg_12 SHALL include a policy for Relying Party Instance-specific revocation, which SHALL require that an Access Certificate Authority revokes one or more of the access certificates of the certificate subject at least when: - the corresponding Relying Party Instance is cancelled by the respective Registrar, - on request of the certificate subject, or - on request of a national supervisory body. *Note: This policy is required for needs of executing partial revocation of access certificates, e.g. for situations when a Relying Party has issues not reaching to all of its instances.*|  New  |
| Reg_16    | The common Certificate Policy mentioned in Reg_12 SHALL specify the profile of access certificates in detail. |  Keep  |
|Reg_17	    | The common Certificate Policy mentioned in Reg_12 SHALL require that an access certificate indicates whether its subject is a PID Provider, a QEAA Provider, a PuB-EAA Provider, a (non-qualified) EAA Provider, or a Relying Party Instance. | Delete |
| Reg_18    | The common Certificate Policy mentioned in Reg_12 SHALL define the minimum change history information to be stored for resolving possible disputes regarding registration. | Keep |


C. *Requirements for the registration of PID Providers*

| **Index** | **Requirement specification**                                | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_19  | A Member State SHALL approve a PID Provider according to a well-defined policy before including it in its PID Provider Registry. To that end, a Member State SHALL define specific vetting processes and rules of acceptance for inclusion of PID Providers in its Registry. |  Delete   |
| Reg_20  | A Member State SHALL identify PID Providers at a level of confidence proportionate to the risk arising from the potential harm a fraudulent PID Provider could cause to Users and other stakeholders in the EUDI Wallet ecosystem. |  Delete   |
| Reg_20a | A Registrar SHALL provide a method to suspend or cancel a registered PID Provider. |  Delete  |
| Reg_20b | A Registrar SHALL have a policy for the suspension or cancellation of a registered PID Provider, which SHALL specify that a PID Provider is suspended or cancelled at least on request of the PID Provider or of a national supervisory body. |   Delete  |

D. *Requirements for the registration of Attestation Providers*

| **Index** | **Requirement specification**                                | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_21 | A Member State SHALL approve an Attestation Provider according to a well-defined policy before including it in its Attestation Provider Registry. To that end, a Member State SHALL define specific vetting processes and rules of acceptance for inclusion of Attestation Providers in its Registry. These processes and rules SHOULD consider any relevant differences between QEAA Providers, PuB-EAA Providers and (non-qualified) EAA Providers. |     Delete         |
| Reg_22 | A Member State SHALL identify Attestation Providers (i.e., QEAA Providers, PuB-EAA Providers and non-qualified EAA Providers) at a level of confidence proportionate to the risk arising from the potential harm a fraudulent Attestation Provider could cause to Users and other stakeholders in the EUDI Wallet ecosystem. |     Delete         |
| Reg_22a | A Registrar SHALL provide a method to suspend or cancel a registered Attestation Provider. | Delete  |
| Reg_22b | A Registrar SHALL have a policy for the suspension or cancellation of a registered Attestation Provider, which SHALL specify that an Attestation Provider is suspended or cancelled at least on request of the PID Provider or of a national supervisory body. |  Delete  |

E. Requirements for the registration of Relying Parties

| **Index** | **Requirement specification** | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_23    | The Commission SHALL establish a technical specification for a common set of Relying Party information to be registered in Member State registries. This set SHALL include at least the information defined in [European Digital Identity Regulation] article 5b 2 (c). |     Keep         |
| Reg_24    | A Member State SHALL enable a Relying Party to register remotely, using an API or user interface. |       Keep       |
| Reg_25    | A Member State SHALL identify a Relying Party at a level of confidence proportionate to the risk arising from the potential harm a fraudulent Relying Party could cause to Users and other stakeholders in the EUDI Wallet ecosystem. |      Delete        |
| Reg_26    | A Member State SHALL enable a Relying Party to update the information registered on it using a process comparable to the original registration process, and using the API or user interface mentioned in Reg_24. |       Keep       |
| Reg_27    | Relying Parties SHALL make any updates necessary to ensure the continued correctness of the registered information without undue delay. |      Keep    |
| Reg_28    | A Member State's Registry SHALL log all changes made on the information regarding a Relying Party, including at least initial registration, updates, deletion of information, and suspension or cancellation. |     Keep with proposed changes       |
| Reg_29    | A Registrar SHALL have a policy for the cancellation of a registered Relying Party, which SHALL specify that a Relying Party is cancelled at least on request of the Relying Party or of a national supervisory body. |      Keep with proposed changes       |
| Reg_30    | During registration, the Relying Party SHALL be provided both JWT and CWT format registration certificates by the Registrar. *Note: This gives the Relying Party freedom to provide their intended use for both remote and proximity use cases, as necessary - without requesting use case implementation approach upon the registration event.* |    New    | 

F.  *Requirements for the issuance of Relying Party Instance access certificates*

| **Index** | **Requirement specification**                                | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_31	| The common Relying Party Registration Certificate Policy SHALL require that a Relying Party registration certificate contains a name for the Relying Party, in a format suitable for presenting to a User. *Note: A Wallet Unit needs such a name when requesting User approval according to [Topic 6][topic-6].*| Move modified HLR text under Topic 44 (**new RPRC_03a**) |
| Reg_32	| The common Relying Party Registration Certificate Policy SHALL require that a Relying Party registration certificate contains an EU-wide unique identifier for the Relying Party, and SHALL specify a method for deriving such identifiers. *Note: - The Wallet Instance needs such an identifier at least to lodge a complaint of suspicious Relying Party presentation requests to a data protection authority according to Topic 50. - The EU-wide unique identifier could, for example, be a concatenated list of one or more registered official wallet-relying party identifiers listed in Annex I(3) of the \[Draft of the CIR for RP-Registration\], expressed in semantic form defined in \[ETSI EN319 412-1\] Sections 5.1.4 or 5.1.5 and used as the Distinguished Name (DN) of the Certificate subject in both access and registration certificates of the Relying Party*   | Move modified HLR text under Topic 44 (**new RPRC_03b**). |
| Reg_33    | All Relying Party Instance access certificates of a Relying Party SHALL include the user-friendly (common) name of Relying Party service and unique identifier identical to the ones defined in requirements RPRC_03a and RPRC_03b, respectively. | New |


### 4.2 Topic 44 - Relying Party Registration Certificates

A. Issuance of Relying Party registration certificates

| **Index** | **Requirement specification** | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| RPRC_01	| During the registration process for Relying Parties, as specified in Topic 27, the Member State Registrar SHALL create and sign or seal a registration certificate and issue it to the Relying Party for each intended use requested to be registered by the Relying Party. The registration certificate SHALL comply with the applicable requirements in the technical specification mentioned in RPRC_02. *Note: See Topic 52.* | Keep with proposed changes |
| RPRC_02   | The Commission SHALL ensure that a technical specification is created, describing at least 1. the contents and format of registration certificates, 2. the signing method(s) used to ensure the authenticity of the registration certificates. 3. the trust infrastructure necessary for signing registration certificates and for verifying these signatures, including, if necessary, the use of Trusted Lists to establish trust in Member States Registrars and to distribute their trust anchors to Wallet Units. 4. the method used for binding each registration certificate to the Relying Party Instance access certificate that will be used during the same transaction. This binding method SHALL enable a Wallet Unit to verify that the registration certificate is bound to the Relying Party that authenticated itself using the access certificate. The binding method SHALL consider situations in which the Relying Party uses the services of an intermediary (see Topic 52) to connect to the Wallet Unit. 5. whether or not a registration certificate must have a validity period. 6. the method to be used for revocation of registration certificates. Moreover, the technical specification SHALL describe the impact of revocation, especially compared to the impact of revocation of the Relying Party Instance access certificates. |     Keep with proposed changes    |
| RPRC_03    | The contents of a registration certificate issued per registered intended use of the Relying Party SHALL include at least information required in Annex V of the CIR for Relying Party Registration. If the Relying Party uses the services of an intermediary (see Topic 52): the fact that this is the case, plus the user-friendly (common) name and unique identifier (as meant in RPRC_03a and RPRC_03b) of this intermediary. |      Keep with proposed changes        |
| RPRC_03a	| The common Relying Party Registration Certificate Policy SHALL require that a Relying Party registration instance certificate contains a common name for the Relying Party instance, in a format suitable for presenting to a User. *Notes: - A Wallet Unit needs such a name when requesting User approval according to [Topic 6][topic-6], - If Relying Party uses an Intermediary, both Intermediary and End-Relying Party common names need to be shown when requesting User approval and the User should be informed that the Intermediary is representing/acting on behalf of the End-Relying Party*.  |  New  |
| RPRC_03b	| The common Relying Party Registration Certificate Policy SHALL require that a Relying Party registration certificate contains an EU-wide unique identifier for the Relying Party, and SHALL specify a method for deriving such identifiers. *Notes: - The Wallet Instance needs such an identifier at least to lodge a complaint of suspicious Relying Party presentation requests to a data protection authority according to Topic 50. - The EU-wide unique identifier could, for example, be a concatenated list of one or more registered official wallet-relying party identifiers listed in Annex I(3) of the \[Draft of the CIR for RP-Registration\], expressed in semantic form defined in \[ETSI EN319 412-1\] Sections 5.1.4 or 5.1.5 and used as the Distinguished Name (DN) of the certificate subject in both access and registration certificates of the Relying Party. Exact specification is left for the technical specifications to be developed by the European Commission.* |  New  |
| RPRC_04   | In both proximity and remote presentation flows, the Relying Party Instance SHALL transfer a Relying Party registration certificate to the Wallet Unit in the presentation request, according to the applicable standard's extension mentioned in RPRC_05. The registration certificate SHALL be included in the request by value, not by reference. *Note: This ensures that no external requests are necessary to validate the request, and that transactions are atomic and self-contained.* | Keep |
| RPRC_05   | The Commission SHALL ensure that extensions are specified for [ISO/IEC 18013-5] and for \[OpenID4VP\], allowing a Relying Party to transfer a Relying Party registration certificate to a Wallet Unit. These extensions SHALL comply with applicable requirements in these standards. | Keep  |
| RPRC_06   | The Wallet Unit SHALL verify the authenticity and validity of the registration certificate according to the technical specification meant in RPRC_02. If the outcome of the verification is negative, the Wallet Unit SHALL, when asking for User approval according to RPA_07 and subject to the User preference set according to RPRC_08, notify the User that it could not verify whether the Relying Party registered the requested attributes with the competent authorities. |  Keep |
| RPRC_07   | The Wallet Unit SHALL verify that all attributes requested in the presentation request are included in the list of attributes in the registration certificate. If the outcome of the verification is negative, the Wallet Unit SHALL, when asking for User approval according to RPA_07 and subject to the User preference set according to RPRC_08, notify the User about the requested attributes that the Relying Party did not register. | Keep |
| RPRC_08   | A Wallet Unit SHOULD enable its User to set their preference for showing or hiding the notifications meant in RPRC_06 and RPRC_07. By default, the Wallet Unit SHALL show the notifications. |  Keep  |
| RPRC_09   | The EU-wide unique identifier SHALL be identical in all registration certificates issued for a given Relying Party. *Note: In case the registration certificates issued to an End-Relying Party are held and presented by an Intermediary (Relying Party), the given Relying Party meant in the text is the End-Relying Party. An Intermediary will obtain and hold registration certificates with non-identical unique identifiers.* |  New  |
| RPRC_10   | The Commission SHALL provide technical specifications establishing common Certificate Policy for registration certificates, covering at least management and selection of signing keys, revocation and lifecycle management of RPRCs on individual intended use level. *Note: The TS could set the provider of RPRCs to follow applicable parts of technical standards such as EN 319 401 (for General Policy Requirements for TSPs) and TS 119 461 (for identity proofing of Relying Party representatives).* |  New  |
| RPRC_11   | There SHALL be only one valid registration certificate present in a presentation request for given intended use of a Relying Party. An error SHALL be reported (logged and shown for the User) by the Wallet Unit if it receives multiple registration certificates for the same intended use within same presentation request. |  New  |


### 4.3 Topic 52 - Relying Party Intermediaries

| **Index** | **Requirement specification** | **Proposal** |
|-----------|-------------------------------|--------------|
| RPI_01 | An intermediary SHALL register as a Relying Party, in accordance with all requirements in [Topic 27][topic-27]. *Note: This implies that an intermediary obtains an access certificate containing its own name and unique Relying Party identifier.* |       Keep        |
| RPI_02 | An intermediary is acting only as an intermediary for other (End-) Relying Parties, but from the Registrar and the regulation's point of view is considered as a Relying Party and obtains a registration certificate according to [Topic 44][topic-44], containing Intermediary name and Relying Party identifier. |  Keep with proposed changes     |
| RPI_03 | For each of the End-Relying Parties that uses its services, an intermediary SHALL be the holder of the registration certificate for each registered intended use of the said End-Relying Party, according to the requirements in [Topic 44][topic-44]. This registration certificate SHALL contain that End-Relying Party's name and unique identifier, as well as the list of attributes registered for that Relying Party's intended use. |   Keep with proposed changes      |
| RPI_04 | When issuing a registration certificate for a Relying Party to an intermediary, the Registrar SHALL verify, in a manner to be decided by a Member State, that the Relying Party will indeed use the services of the intermediary to interact with Wallet Units. |    Keep        |
| RPI_05 | When issuing a registration certificate for an intermediary, the Registrar SHALL include in the registration certificate the attributes meant in RPRC_03a and RPRC_03b containing the name and unique identifier of the intermediated End-Relying Party. |         Keep with proposed changes    |
| RPI_06 | When requested for an intended use by an intermediated End-Relying Party, an intermediary SHALL request the presentation of attributes from a specific Wallet Unit, using the intermediary's access certificate meant in requirement RPI_01, and the registration certificate accessible to the intermediary in relation to the intermediated End-Relying Party and the intended use, as meant in RPI_03. |  Keep with proposed changes       |
| RPI_07 | In case a Wallet Unit receives a presentation request from an intermediary, on behalf of a Relying Party, it SHALL verify the name of the intermediary during Relying Party authentication and display this name to the User when asking for User approval, as described in requirement RPA_06a. |       Keep        |
| RPI_08 | When a Wallet Unit presents any User attributes to an intermediary, the intermediary SHALL forward these attributes only to the Relying Party that requested the intermediary to request these attributes from the Wallet Unit. |         Keep      |

## 5 Relation to Other Topics

Below we discuss how Relying Party registration relates to the other topics being discussed.

As indicated in the chapter 3, several changes are proposed in the context of the Relying Party registration. The changes introduced in the respective HLRs are to be also reflected in the remaining topics/HLRs, at least in reference to Topic 6 and Topic 31. Note that term **Registration Certificate Authority** has been introduced, aside the formerly used Access Certificate Authority.

In result, the following modification are therefore proposed:

> Note: only affected HLRs are listed, not exhaustive lists as in Section 4.

### 5.1 Topic 6 - Relying Party authentication and User approval

| **Index** | **Requirement specification** | **Proposal** |
|-----------|-------------------------------|--------------|
| RPA_06a | If the registration certificate indicates that an intermediary, as described in [Topic 52][topic-52], the Wallet Unit SHALL verify that the name and the unique identifier of the intermediary included in the registration certificate are identical to the name and unique identifier included in the Relying Party Instance access certificate. If this verification fails, the Wallet Unit SHALL treat this as a Relying Party authentication failure. If this verification succeeds, the Wallet Instance SHALL display to the User the names of the intermediary and the intermediated End-Relying Party. |     Keep with proposed changes      |

### 5.2 Topic 31 - PID Provider, Wallet Provider, Attestation Provider, and Access Certificate Authority notification and publication

| **Index** | **Requirement specification** | **Proposal** |
|-----------|-------------------------------|--------------|
| GenNot_01 | The European Commission SHALL establish technical specifications for a common system enabling the notification of PID Providers, PuB-EAA Providers, Wallet Providers, Access Certificate Authorities and Registrars of Registration Certificates by Member States to the Commission. *Note: Notification does not apply to QEAA Providers and (non-qualified) EAA Providers, as explained in Sections D and F below, respectively.*  |  Keep with proposed changes   |
| GenNot_02 |  As part of the specifications referred to in GenNot_01, the European Commission SHALL establish standard operating procedures for the notification of a PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authorities or Registration Certificate Authorities to the Commission. *Note: The outcome of the notification procedure is the publication of the information notified by the Member State according to [Article 5a](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e1347-1-1) (18) in a machine and human readable manner using the common system mentioned in Section H, TLPub_01.* |   Keep with proposed changes   |
| GenNot_05 |  As part of the specifications referred to in GenNot_01, the European Commission SHALL establish standard operating procedures for the suspension or cancellation of a PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authority or Registration Certificate Authority. These operating procedures SHALL include unambiguous conditions for suspension or cancellation. As an outcome of the suspension or cancellation procedure, the status of the suspended or cancelled PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authority or Registration Certificate Authority in the Trusted List SHALL be changed to Invalid. | Keep with proposed changes    |
| PPNot_02 |  The common set of information to be notified about a PID Provider SHALL include at least: 1. Identification data: i. MS/Country of establishment, ii. Name as registered in an official record, iii. Where applicable: a. A business registration number from an official record, b. Identification data from that official record. 2. PID Provider trust anchors, i.e., public keys and name as per point 1) ii) above, supporting the authentication of PIDs issued by the PID Provider, 3. PID Provider Access Certificate Authority trust anchors, i.e., public keys and CA name, supporting the authentication of the PID Provider by Wallet Units at the service supply point(s) listed per point 4. below. 4. Service supply point(s), i.e., the URL(s) at which a Wallet Unit can start the process of requesting and obtaining a PID. *Notes: - Relating to point 3. above: PID Provider Access Certificate Authority trust anchors are notified separately from the ~~Relying Party~~ Access Certificate Authority (see Section G below), since PID Providers are -legally speaking- not Relying Parties. - For the concept of an  Access Certificate Authority, see also [[Topic 27][topic-27]] and [Section 6.3.2 of the ARF main document][632-pid-provider-or-attestation-provider-registration-and-notification].*  |  Keep with proposed changes   |
| RPACANot_01  |  The European Commission SHALL establish technical specifications for the common set of information to be notified about Access Certificate Authorities and Registrars of Registration Certificates. |   Keep with proposed changes   |
| RPACANot_02  | The common set of information to be notified about an Access Certificate Authority and Registrars of Registration Certificates SHALL include: 1. Identification data: i) MS/Country of establishment, ii) Name as registered in an official record, iii) Where applicable: - A business registration number from an official record, - Identification data from that official record. 2. Access Certificate Authority or Registration Certificate Authority trust anchors, i.e., public keys and name as per point 1) ii), supporting the authentication of Relying Parties by Wallet Units. |   Keep with proposed changes  |
| RPACANot_04 | Access Certificate Authority and Registration Certificate Authority trust anchors SHALL be accepted because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled Access Certificate Authority and Registration Certificate Authority Trusted Lists which are signed or sealed by the Commission. *Note: The adopted version of the CIR for Relying Party registration will clarify how the Trusted List for Registrars of Registration Certificates are to be arranged, the certificates not being PKI/X.509 certificates as is the case with standard EU Trusted Lists. It is also to be clarified in the related technical specification if Access Certificate Authorities can sign other certificates than access certificates.* |  Keep with proposed changes  |
| RPACANot_06 | If an Access Certificate Authority is suspended or cancelled (see requirement GenNot_05 above), that Access Certificate Authority SHALL immediately revoke all of its valid access certificates. *Note: When the access certificates of an Intermediary that has its RPACs issued by said suspended or cancelled Access Certificate Authority are revoked, the End-Relying Parties depending on said Intermediary, while having valid registration certificates from a Registrar will have no access to transact with EUDI Wallet Users until the End-Relying Parties a) transit to another Intermediary that has RPAC issued by an active Access Certification Authority or b)the original Access Certificate Authority can continue its operations and re-issue earlier revoked certificates for the original Intermediary.* |   New   |
| RPACANot_07 | If a Registrar of Relying Party Registration Certificates is suspended or cancelled (see requirement GenNot_05 above), that Registrar of Relying Party Registration Certificates SHALL immediately revoke all of its valid registration certificates.  |   New   |
| TLPub_01 | The European Commission SHALL establish technical specifications for the system enabling the publication by the Commission of the information notified by the Member States regarding PID Providers, Wallet Providers, PuB-EAA Providers, Access Certificate Authorities and Registrars of Registration Certificates. |  Keep with proposed changes  |
| TLPub_02 | The European Commission SHALL establish technical specifications for the set of information to be published about: PID Providers, Wallet Providers,PuB-EAA Providers, Access Certificate Authorities and Registrars of Registration Certificates based on the information notified by the Member States. *Note: The information to be published MAY be different from the information to be notified per requirements PPNot_01, WPNot_01, PuBPNot_01, and RPACANot_01 above, respectively.* |  Keep with proposed changes  |
| TLPub_08  | As part of the specifications referred to in TLPub_01, the European Commission SHALL establish technical specifications for ensuring the availability and authenticity of the full history regarding the information notified about PID Providers, Wallet Providers, PuB-EAA Providers, Access  Certificate Authorities and Registrars of Registration Certificates.  |   New   |

### 5.3 Use of Certificate Transparency

[Topic S] refers to use of Certificate Transparencey (CT) in the context of access certificates. There is no decision yet whether CT will be used at all, as the initial intention of CT use was the context of browsers/QWACs. Regulation has no requirement for use of Certificate Transparency with registration certificates.


### 5.4 User requesting data deletion to relying parties

[Topic L] will discuss requirements related to the EUDI Wallet User's means to request data deletion from any Relying Parties that they've provided with attestation data. This will be using the contact details which are required to be registered as part of the registration data set.


### 5.5 User reporting unlawful or suspicious request of data to DPAs

[Topic M] will cover requirements on EUDI Wallet Users means to report evidently or potentially unlawful presentation requests by a Relying Party to relevant data protection authority/-ies (DPAs). This reporting would be actuated if a Relying Party is trying to ask attestations or attributes beyond its reported Intended Use -specific data set that is present in the related Registration Certificate. 

If found in breach and not corrected promptly by the Relying Party, the DPA and national authorities are allowed to request revocation of the access and registration certificates of the Relying Party in breach of their registration data.


### 5.6 Relation to Risk Register

The risk register for European Digital Identity Wallets \[RiskRegister\]
contains the following risks that are related to the Relying Party registration:

|Risk type | Risk id | Related risk titles|
|-------------|-------|-------------------|
|High-level risks to the wallets | R6 | Data disclosure|
|High-level risks to the wallets |R9 | Unauthorised transaction|

| R6 Data disclosure |
|---|
|Data disclosure is defined as the unauthorised exposure of personal data including special categories of personal data. The privacy breach risk is very similar when considered from a privacy rather than security viewpoint. |

| R9 Unauthorised transaction |
|---|
|Unauthorised transactions are defined as operational activities conducted without the permission or knowledge of the wallet user. In many cases, an unauthorised transaction can lead to Identity theft (R4) or Data disclosure (R6). It is also related to unauthorised transactions, such as the misuse of cryptographic keys. |

More specifically, \[RiskRegister\] describes the following threats to a Wallet:

|ID | Threat description | Related risks |
|---------|-------|-------------------|
|TR25 | The wallet can present attributes to a relying party without the approval of a user. | Data disclosure (R6) |
|TR29 | An attacker can leak attributes from the wallet and identify the wallet user where identification is not required/allowed. | Data disclosure (R6) |
|TR38 | Not being able to prove user’s consent for shared attributes, relying parties can affect the integrity of logs. | Data disclosure (R6) |
|TR40 | A relying party that consists of multiple units/entities that each have a different scope of what they are allowed to request/process, can request and process data for which they do not have lawful grounds for. | Data disclosure (R6) / Unauthorised transaction (R9) |
