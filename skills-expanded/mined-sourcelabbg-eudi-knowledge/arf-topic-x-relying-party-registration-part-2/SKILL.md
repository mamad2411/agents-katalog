---
name: "arf-topic-x-relying-party-registration-part-2"
description: "Use when implementing RP registration and access certificate management. Covers registration workflows, certificate issuance, attribute disclosure policies, and RP trust framework. Part 2: covers 3 Discussion."
sections:
  - "3 Discussion"
  - "3.1 Proximity use case support"
  - "3.2 Access certificates with multiple Relying Party instances"
  - "3.3 Registration certificate per intended use"
  - "3.4 Addressing the PID Providers and Attestation Providers on RPRCs"
  - "3.5 Registration certificate for intermediaries"
  - "3.6 Registration and Registration Certificate life cycles"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~5415 -->

## 3 Discussion 

The Relying Party registration covers from functional perspective of the ARF and the European Digital Identity ecosystem the following aspects: 


1) the **Registrar function** for which the Member States are responsible to organise this function, register and a publicly accessible API at a national level (based on the future technical specifications and the CIR provided by the European Commission),
2) the registration process mandated to be be followed by all Relying Parties resulting in issuance of one or more **Wallet-Relying Party Access Certificates** (RPAC) and as many **Wallet-Relying Party Registration Certificates** (RPRC) as the Relying Party has dedicated intended uses (use cases, services provided to the EUDI Wallet Users),
3) the **operational use of aforementioned certificates** in Relying Party transactions with the EUDI Wallet Units and their Users,
4) **handling the functional revocation of Relying Party certificates** as necessitated by the legal requirements, 
5) how the registration and operational use of the RP registration certificates shall be done when **the Relying Party relies upon another Relying Party that is acting on its behalf (an intermediary)** to provide its intended use towards the Wallet Units.

Having analysed the combined legal requirements, the current ARF (release 1.8), as well as recent German architecture concept proposals (\[German non-paper on RP Authn\], \[German non-paper on WRP with attestations\], that together contain considerable amount of technical detail and that were discussed indirectly in the context of topic D already), this section raises the following topics for discussion at level of High-Level Requirements relevant for the ARF:

+ Requirements needed to support registrar issuance of RP registration certificates for proximity use cases, not just remote (specifically, support of both JWT and CWT formats of the RP registration certificates, support of both JOSE and COSE signature)
+ Requirements impacted from the fact that the Relying Party has an access certificate per Relying Party Instance (either in remote or proximity scenarios)
+ Requirements impacted from the fact that registration certificates are issued per each registered intended use of the Relying Party
+ Changes needed in the ARF due to earlier assumption that PID or Attestation Providers did not need a Relying Party registration certificate
+ Identified HLR changes due to clarification of the role of intermediaries (adaptation of the certificate usage to the role  of intermediaries and the related processes, e.g. registration process and RP registration certificate content if issued to an intermediary, and binding association between the access certificate of the intermediary and the registration certificates of its End-Relying Parties)  
+ Modification related to distinguishing between lifecycle of the RP registration and the lifecycle of RPRC itself, as well as the relation between them (e.g. adapt the HLRs to the fact that certificates can only be revoked (no suspension), while the registration can be cancelled or suspended)  
+ Other terminology mismatches that need alignment between the draft IA and the ARF (eg. registration 'withdrawal' to be replaced with 'cancellation').
+ Necessary adaptation of registration policy, certification policy and certification policy statement requirements in line with conclusions on the above issues
+ Impacts on the HLRs under other Topics of ARF Annex 2 (Topic 6 & Topic 31, at least)

This document is ONLY intended to clarify the high-level requirements related to the Relying Party registration topic. The necessary technical specifications (including any policy documents) will be developed by the European Commission after agreement over the requirements has been reached.

### 3.1 Proximity use case support

The Annex IV and V of the \[Draft CIR on Relying Party registration\] will bind legally what certificate standards are applicable for the RPAC and RPRC to be issued by the registrar. Use of the RPRC in context of proximity use case is mentioned in the ARF indirectly in (6.6.3.5), but necessary technical requirements for RPRC issuance are pointing at use of JOSE for signing/sealing the certificate, and the data format of the certificate contents being JSON (Annex V of the draft CIR). Requirement for the Registrar to support provisioning of registration certificates in both JWT and CWT format was agreed to be added to the requirements.

A new HLR is proposed to extend the scope of registration to apply over both online and proximity use cases:

| **Index** | **Requirement specification** | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_30    | During registration, the Relying Party SHALL be provided both JWT and CWT format registration certificates by the Registrar. *Note: This gives the Relying Party freedom to provide their intended use for both remote and proximity use cases, as necessary - without requesting use case implementation approach upon the registration event.* | New | 

### 3.2 Access certificates with multiple Relying Party instances
When addressing the RPACs, the Regulation does not recognise the need for multiple instances of Relying Party services in modern IT architectures (replication of RP servers and common dependence on multiple geographical cloud provider regions to ensure availability and continuity of RP services). Multi-instance Relying Parties will also be commonplace in proximity use cases with handheld or mounted verification devices interacting with the Wallet Units. The fact that multiple access certificates with individual private keys can be requested and issued by the Access Certificate Authorities should be clarified in the ARF requirements on registering access certificates, and in the policy documents to be created based on the ARF high-level requirements.

The HLR Reg_15 on policy for revocation is revised to mention multiple RPACs (_all_ RPACS of a Relying Party), and a new HLR Reg_15b is brought to clarify the need for controlled revocation of individual instance RPACs (when the Relying Party still has at least one or more valid RPACs after revoking one or more RPACs assigned to its Relying Party Instances). Related to the existing HLRs on relying party access certificates Reg_31 and Reg_32, the requirements with their contextual notes should be moved under Topic 44 with rewording to mean RPRCs. To ensure binding of the RPAC and RPRC with the unique identifier of the Relying Party, a new HLR Reg_33 is introduced.

| **Index** | **Requirement specification**                                | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_15    | The common Certificate Policy mentioned in Reg_12 SHALL include a policy for revocation, which SHALL require that an Access Certificate Authority revokes all access certificates of the certificate subject at least when: - the certificate subject which is a Relying Party is cancelled or suspended by the respective Registrar,  - on request of the certificate subject, or - on request of a national supervisory body.| Keep with proposed changes |
| Reg_15b   | The common Certificate Policy mentioned in Reg_12 SHALL include a policy for Relying Party Instance-specific revocation, which SHALL require that an Access Certificate Authority revokes one or more of the access certificates of the certificate subject at least when: - the corresponding Relying Party Instance is cancelled by the respective Registrar, - on request of the certificate subject. or - on request of a a national supervisory body. *Note: This policy is required for needs of executing partial revocation of access certificates, e.g. for situations when a Relying Party has issues not reaching to all of its instances.*|  New  |
| Reg_31	| The common Relying Party Registration Certificate Policy SHALL require that a Relying Party registration certificate contains a name for the Relying Party, in a format suitable for presenting to a User. *Note: A Wallet Unit needs such a name when requesting User approval according to [Topic 6][topic-6].* | Move modified HLR text under Topic 44 (new RPRC_03a) |
| Reg_32	| The common Relying Party Registration Certificate Policy SHALL require that a Relying Party registration certificate contains an EU-wide unique identifier for the Relying Party, and SHALL specify a method for deriving such identifiers. *Note: - The Wallet Instance needs such an identifier at least to lodge a complaint of suspicious Relying Party presentation requests to a data protection authority according to Topic 50. - The EU-wide unique identifier could, for example, be a concatenated list of one or more registered official wallet-relying party identifiers listed in Annex I(3) of the \[Draft of the CIR for RP-Registration\], expressed in semantic form defined in \[ETSI EN319 412-1\] Sections 5.1.4 or 5.1.5 and used as the Distinguished Name (DN) of the Certificate subject in both access and registration certificates of the Relying Party*   | Move modified HLR text under Topic 44 (new RPRC_03b). *Note: Identicality is covered in new HLR RPRC_09 - see Section 3.3*|
| Reg_33    | All Relying Party Instance access certificates of a Relying Party SHALL include the user-friendly (common) name of Relying Party service and unique identifier identical to the ones defined in requirements RPRC_03a and RPRC_03b, respectively. |  New  |


### 3.3 Registration certificate per intended use

The Relying Party registration requires Relying Parties to provide information necessary for authentication, their contact details, and the intended use of the European Digital Identity Wallets, including the specific data they will request from users. The RPAC (wallet Relying Party Access Certificate) authenticates who the Relying Party is, while the RPRC (wallet-Relying Party Registration Certificate) specifies what data that authenticated the Relying Party is entitled to request for a particular registered purpose (intended use). Crucially, Relying Parties are explicitly prohibited from requesting any data beyond what is indicated in their registration. This is a key mechanism for enforcing data minimisation and purpose limitation.

According to the \[Draft CIR on Relying Party registration\] a Relying Party will get issued a unique RPRC for each of its registered intended uses, and these registration certificates may be revoked independent of each other or of the associated RPAC. The access certificates are the Relying Party's 'master switches' to the EUDI ecosystem, whilst registration certificates are used to register and document the use case/s provided to the Wallet User. The registration certificate will not be a X.509 certificate, and thus the required certificate policies for RPRCs should be clarified both in the IA draft and the ARF. 

Current RPRC_2 and RPC_3 in the ARF should be updated to reflect the text of the draft CIR on RPR, a new requirement on use of unique RP identifier across the RPRCs, and a new HLR on creating applicable certificate policies is suggested for Topic 44 as follows:

| **Index** | **Requirement specification** | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| RPRC_01	| During the registration process for Relying Parties, as specified in [Topic 27][topic-27], the Member State Registrar SHALL create and sign or seal a registration certificate and issue it to the Relying Party for each intended use requested to be registered by the Relying Party. The registration certificate SHALL comply with the applicable requirements in the technical specification mentioned in RPRC_02. Note: See [Topic 52][topic-52]. | Keep with proposed changes |
| RPRC_02   | The Commission SHALL ensure that a technical specification is created, describing at least 1. the contents and format of registration certificates, 2. the signing method(s) used to ensure the authenticity of the registration certificates. 3. the trust infrastructure necessary for signing registration certificates and for verifying these signatures, including, if necessary, the use of Trusted Lists to establish trust in Member States Registrars and to distribute their trust anchors to Wallet Units. 4. the method used for binding each registration certificate to the Relying Party Instance access certificate that will be used during the same transaction. This binding method SHALL enable a Wallet Unit to verify that the registration certificate was in fact issued to the Relying Party that authenticated itself using the access certificate. The binding method SHALL consider situations in which the Relying Party uses the services of an intermediary (see [Topic 52][topic-52]) to connect to the Wallet Unit. 5. whether or not a registration certificate must have a validity period. 6. the method to be used for revocation of registration certificates. Moreover, the technical specification SHALL describe the impact of revocation, especially compared to the impact of revocation of the Relying Party Instance access certificates. |     Keep with proposed changes    |
| RPRC_03    | The contents of a registration certificate issued per registered intended use of the Relying Party SHALL include at least information required in Annex V of the CIR for Relying Party Registration. If the Relying Party uses the services of an intermediary (see [Topic 52][topic-52]): the fact that this is the case, plus the user-friendly (common) name and unique identifier (as meant in RPRC_03a and RPRC_03b) of this intermediary. |      Keep with proposed changes        |
| RPRC_09    | The EU-wide unique identifier SHALL be identical in all registration certificates issued for a given Relying Party.|  New  |
| RPRC_10    | The Commission SHALL provide technical specifications establishing common Certificate Policy for registration certificates, covering at least management and selection of signing keys, revocation and lifecycle maganagement of RPRCs on individual intended use level. *Note: The TS could set the provider of RPRCs to follow applicable parts of technical standards such as EN 319 401 (for General Policy Requirements for TSPs) and TS 119 461 (for identity proofing of Relying Party representatives).* |  New  |
 |RPRC_11 | There SHALL be only one valid registration certificate present in a presentation request for given intended use of a Relying Party. An error SHALL be reported by the Wallet Unit if it receives multiple registration certificates for the same intended use. |  New  |

> Note: The modifications suggested for RPRC_01 and RPRC_03 above include also the changes required from discussion on intermediaries at Section 3.5.


### 3.4 Addressing the PID Providers and Attestation Providers on RPRCs

The \[Draft of the CIR for RP-Registration\] implies that among all other roles defined in the ARF also the PID Providers and Attestation Providers will receive registration certificates, with the role registered as part of the registration and reflected in the certificate information (the specific entitlement being one or more of the set PID_Provider, QEAA_Provider, Non_Q_EAA_Provider or PUB_EAA_Provider). This needs to be reflected in the ARF, which so far has separated these roles from the Relying Parties (per definition of the ARF).

 Section 6.3.2.2 of the ARF says that "_A PID Provider access certificate indicates that its subject is a PID Provider. Similarly, an Attestation Provider access certificate indicates that its subject is a QEAA Provider, a PuB-EAA Provider or a non-qualified EAA Provider._"

This is not the case per the draft CIR, the entitlements indicating the registered role are only present in the Relying Party registration certificate.

Therefore, the definition set in the ARF needs to be adapted or extended accordingly, and Reg_17 on list of HLRs for the issuance of access certificates should be removed (entitlements not being present in access certificates):

| **Index** | **Requirement specification** | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
|Reg_17	| The common Certificate Policy mentioned in Reg_12 SHALL require that an access certificate indicates whether its subject is a PID Provider, a QEAA Provider, a PuB-EAA Provider, a (non-qualified) EAA Provider, or a Relying Party Instance. | Delete |

### 3.5 Registration certificate for intermediaries

#### 3.5.1 Registration on-behalf of the End-Relying Parties
The intention reflected in the \[Draft of the CIR for RP-Registration\] is that the intermediaries are to receive the RPRC of their End-Relying Parties. If an End-Relying Party uses an intermediary, it (the End-RP) will not need to itself apply or receive its Wallet-Relying Party certificate from the Registrar, if the intermediary (as part of their service towards the End-Relying Parties) registers for it and possesses the RPRCs for all of its customers. This will simplify the process of End-Relying Parties, who can This model is not mandated by the ARF, the processes how registration will be organised in Member States is left for national discretion.

> Note: The means to indicate to the national registry/ies that an entity is registering as an Intermediary is left for national discretion (see RPI_04), there is no such role/entitlement recognised in the Regulation.

A pure intermediary will upon its registration receive only RPACs listing its own unique Relying Party identifier and (common) name. The intermediated End-Relying Parties are not provided RPACs, and their set of issued RPRCs are hosted by their intermediary. It is not in the scope of the ARF to cover how the intended use specific RPRCs are to be managed between the End-Relying Party and the Intermediary.

As the intermediaries are acting on behalf of the End-Relying Parties, and will remain liable towards the Registrar on accuracy of the information to be registered, they must carry same identity proofing and data verification checks for their customers as the Registrar would do for the End-Relying Party in case of direct registration path. The Registrar shall also not trust blindly the Intermediary but execute the identity verification of both the Intermediary and the End-Relying Parties to be registered.

> Note: Attention must be paid towards compliance of principles such as lawfulness, fairness, transparency, storage limitation or accountability, and of requirements such as those related to data subject rights when using an Intermediary. The compliance against requirements of RPI_10 are therefore essential to be audited when defining the national registration and security policies for Intermediaries. There is no such intention from the Commission, as this (no EU-level policy setting) is already the case for the proxying TSPs since enforcement of (EU) 2014/910.


#### 3.5.2 Use of certificates upon on-behalf operation towards Wallet Units
When operating on behalf of its End-Relying Parties, the intermediary will possess as many RPRCs as number of its intermediated End-RPs entities (multiplied by the number of services/intended uses for each entity possibly). The ARF describes already how the certificates are to be used by the Intermediary and the Wallet Unit in RPI_06 to RPI_10. For clarity, the process of presenting the Intermediary RPAC and the End-Relying Party RPRC with necessary technical level binding is illustrated in Figure 1 below.

![Intermediary-certificate-presentation-to-wu](./img/intermediary-certificate-presentation-to-wu.png)

Figure 1 - Validation of identifiers between Intermediary RPAC and End-Relying Party RPRC.

The ARF (1.8) contains requirement RPI_02, assuming the intermediary does not receive registration certificates of its own, and this assumption remains valid unless the Relying Party acting as an intermediary has other wallet-relying party services with intended uses that invoke the duty to register an RPRC. 

As summary, the ARF needs to be adapted to the intended role of the intermediaries as per the \[Draft of the CIR for RP-Registration\], which implies modifications of multiple HLRs. Below are the proposed changes to the key HRLs in this respect (other HLRs might need to be updated accordingly). 


| **Index** | **Requirement specification** | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| RPI_02 | An intermediary is acting only as an intermediary for other (End-) Relying Parties, but from the Registrar point of view is considered as a Relying Party and obtains a registration certificate according to [Topic 44][topic-44], containing Intermediary name and Relying Party identifier. |  Keep with proposed changes     |
| RPI_03 | For each of the End-Relying Parties that uses its services, an intermediary SHALL possess a registration certificate for each registered intended use of the said End-Relying Party, according to the requirements in [Topic 44][topic-44]. This registration certificate SHALL contain that End-Relying Party's name and unique identifier, as well as the list of attributes registered for that Relying Party's intended use. |   Keep with proposed changes      |
| RPI_05 | When issuing a registration certificate for an intermediary, the Registrar SHALL include in the registration certificate the attributes meant in RPRC_03a and RPRC_03b containing the name and unique identifier of the intermediated End-Relying Party. |         Keep with proposed changes    |
| RPI_06 | When requested for an intended use by an intermediated End-Relying Party, an intermediary SHALL request the presentation of attributes from a specific Wallet Unit, using the intermediary's access certificate meant in requirement RPI_01, and the registration certificate possessed by the intermediary in relation to the intermediated End-Relying Party and the intended use, as meant in RPI_03. |  Keep with proposed changes       |
| RPRC_01	| During the registration process for Relying Parties, as specified in [Topic 27][topic-27], the Member State Registrar SHALL create and sign or seal a registration certificate and issue it to the Relying Party for each intended use requested to be registered by the Relying Party. The registration certificate SHALL comply with the applicable requirements in the technical specification mentioned in RPRC_02. *Note: See Topic 52.* | Keep with proposed changes | 

### 3.6 Registration and Registration Certificate life cycles 

The Article 9 of \[Draft of the CIR for RP-Registration\]  envisions 'suspension' and 'cancellation' of the registration (apart from the non-specified "active" state after the registration). 
At the same time the RP registration certificate has its own life cycle, which envisions only 'revocation' (apart from the "valid" state after issuance).

In addition, the IA draft text lists the following reasons of suspension/cancellation:
+ the registration contains information which is inaccurate, out of date or misleading;
+ the wallet-relying party is not complying with the registration policy;
+ the wallet-relying party is requesting more attributes than they have registered; 
+ the wallet-relying party is otherwise acting in breach of Union or national law in a manner related to their role as wallet-relying party;
+ by a supervisory body European Digital Identity Wallet Framework in the case of illegal or fraudulent use of the European Digital Identity Wallet.

The technical specifications and policy documents that base their requirements on the ARF must specify the RPRC specific policies on lifecycle management (e.g., updates for and revocation of the existing RPRCs as intended uses and their data requirements change over time) and policies for eventual multi-registration (per intended use, per Member State) and cross-border registration. 

Defined policies should also address how to execute post-registration analysis and audits against the registered intended uses, unless the audits are to be left entirely for the EUDI Wallet Unit level functions - such as already introduced in the ARF [Section 6.6.3.13][66313-wallet-unit-enables-the-user-to-report-suspicious-requests-by-a-relying-party-and-to-request-a-relying-party-to-erase-personal-data], and the functionalities to be defined via Topic M - User reporting unlawful or suspicious request of data to DPAs.


| **Index** | **Requirement specification** | **Proposal** |
|-----------|--------------------------------------------------------------|--------------|
| Reg_15 | The common Certificate Policy mentioned in Reg_12 SHALL include a policy for revocation, which SHALL require that an Access Certificate Authority revokes an access certificate at least when: the certificate subject's registration is cancelled by the respective Registrar, on request of the certificate subject, or on request of a national supervisory body. | Keep with proposed changes |
| Reg_22a | A Registrar SHALL provide a method to suspend or cancel the registration of a registered Attestation Provider. | Keep with proposed changes |
| Reg_22b | A Registrar SHALL have a policy for the suspension or cancellation of a registered Attestation Provider, which SHALL specify that an Attestation Provider's registration is suspended or cancelled at least on request of the PID Provider,Registrar or of a national supervisory body. | Keep with proposed changes |
| REG_28 | A Member State's Registry SHALL log all changes made on the information regarding a Relying Party, including at least initial registration, updates, deletion of information, and suspension or cancellation. | Keep with proposed changes |
| REG_29 | A Registrar SHALL have a policy for the cancellation and suspension of the registration of a registered Relying Party, which SHALL specify that the Relying Party's registration is cancelled or suspended at least on request of the Relying Party, Registrar or a national supervisory body. | Keep with proposed changes |
