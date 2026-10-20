---
name: "arf-topic-x-relying-party-registration-part-1"
description: "Use when implementing RP registration and access certificate management. Covers registration workflows, certificate issuance, attribute disclosure policies, and RP trust framework. Part 1: covers Legal notice: All legal information and excerpts documented in Section 2 is based on the European Digital Identity Regulation (EU) 2024/1183 and the current public consultation draft of the Commission Implementing Regulation for Relying Party registration. The latter is undergoing changes due to consultation process, and thus this document may need modification after the publication and approval of the final CIR., 1 Introduction, 2 Legal Requirements for Relying Party registration."
sections:
  - "Topic X - Relying Party Registration"
  - "Legal notice: All legal information and excerpts documented in Section 2 is based on the European Digital Identity Regulation (EU) 2024/1183 and the current public consultation draft of the Commission Implementing Regulation for Relying Party registration. The latter is undergoing changes due to consultation process, and thus this document may need modification after the publication and approval of the final CIR."
  - "1 Introduction"
  - "2 Legal Requirements for Relying Party registration"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~6037 -->

Version 0.4, updated 25 April 2025

[Link to GitHub discussion](https://www.github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/discussions/431)

# Topic X - Relying Party Registration

## Legal notice: All legal information and excerpts documented in Section 2 is based on the European Digital Identity Regulation (EU) 2024/1183 and the current public consultation draft of the Commission Implementing Regulation for Relying Party registration. The latter is undergoing changes due to consultation process, and thus this document may need modification after the publication and approval of the final CIR.

## 1 Introduction

### 1.1 Discussion Paper Topic Description

This document is the Discussion Paper for the European Digital Identity Cooperation Group regarding Topic X: Relying Party registration.
The ARF Development Plan [ARF_DevPlan] describes this Topic as follows:

_This topic is to gather High level Requirements (HLR) for Relying Party registration. The HLR relate to information necessary for authentication to access European Digital Identity Wallets, and to relying parties’ contact details and their intended use of wallets, including what data relying parties may ask users for_.

### 1.2 Key Words

This document uses the capitalised key words 'SHALL', 'SHOULD' and 'MAY' as specified in RFC 2119, i.e., to indicate requirements, recommendations and options specified in this document.
In addition, 'must' (non-capitalised) is used to indicate an external constraint, for instance a self-evident necessity or a requirement that is mandated by an external document. The word 'can' indicates a capability, whereas other words, such as 'will', 'is' or 'are' are intended as statements of fact.

### 1.3 Document Structure

The document is structured as follows:

- Chapter 2 presents the legal requirements for functionality related to the Relying Party registration.

- Chapter 3 presents and discusses a list of identified issues, with suggested changes and/or new High-Level Requirements related to this topic.

- Chapter 4 presents a log of the additions and changes that will be made to High Level Requirements in the ARF as a result of discussing this topic with Member States.

- Chapter 5 refers to other topics related to Relying Party registration.

- Chapter 6 presents the additions and changes that will be made to the ARF main document as a result of discussions.

## 2 Legal Requirements for Relying Party registration

Two legal texts impose direct requirements on the Relying Party registration: The evolving [Draft of the CIR for RP-Registration](https://tinyurl.com/IA-5b-draft) and the [European Digital Identity Regulation]. This section recaps the respective legal requirements from these sources.

### 2.1 [European Digital Identity Regulation] about Relying Party registration

The [European Digital Identity Regulation] requires the Relying Parties to be registered. It specifies the following requirements related to Relying Party registration:

1. Setting up national registers of registered wallet-relying parties in each Member State
2. Registering Relying Party needs to provide at minimum, a definite set of information necessary to authenticate to EUDI Wallets including the intended use and indication of data requested for this use from the user
3. Relying Parties shall only request data that is registered for the intended use
4. Member States shall make the Relying Party register information available to the public in a manner that is both human and machine-readable
5. Member States shall provide a common mechanism for authenticating the Relying Parties in the European Digital Identity ecosystem
6. An Intermediary that is acting on behalf of relying parties is deemed to be a Relying Party, but shall not store data exchanged between the EUDI Wallet user and intermediated Relying Party
7. The European Commission shall establish technical specifications and procedures to support the registration process, publication of the registries, updates of registration information by means of implementing acts.

Below are the actual excerpts from the Regulation, including the recitals and the Articles that establish these requirements.

**Recital (17)**

_For the purposes of registration, relying parties should provide the information necessary to allow for their electronic identification and authentication towards European Digital Identity Wallets. When declaring their intended use of the European Digital Identity Wallet, relying parties should provide information regarding the data that they will request, if any, in order to provide their services and the reason for the request.
Relying party registration facilitates the verification by Member States with regard to the lawfulness of the activities of the relying parties in accordance with Union law. The obligation to register provided for in this Regulation should be without prejudice to obligations laid down in other Union or national law, such as the information to be provided to the data subjects pursuant to the Regulation (EU) 2016/679. Relying parties should comply with the safeguards offered by Articles 35 and 36 of that Regulation, in particular by performing data protection impact assessments and by consulting the competent data protection authorities prior to data processing where data protection impact assessments indicate that the processing would result in a high risk. Such safeguards should support the lawful processing of personal data by relying parties, in particular with regard to special categories of data, such as health data. The registration of relying parties is intended to enhance transparency and trust in the use of European Digital Identity Wallets.
Registration should be cost-effective and proportionate to the related risks in order to ensure uptake by service providers. In that context, registration should provide for the use of automated procedures, including the reliance on and the use of existing registers by Member States, and should not entail a pre-authorisation process.
The registration process should enable a variety of use-cases that can differ in terms of mode of operation, whether online or in offline mode, or in terms of the requirement to authenticate devices for the purposes of interfacing with the European Digital Identity Wallet.
Registration should apply exclusively to relying parties providing services by means of digital interaction._

**Recital (18)**

_Safeguarding Union citizens and residents in the Union against the unauthorised or fraudulent use of European Digital Identity Wallets is of high importance for ensuring trust in and for the wide uptake of European Digital Identity Wallets. Users should be provided with effective protection against such misuse. In particular, when facts that form the basis for fraudulent or otherwise illegal use of a European Digital Identity Wallet are established by a national judicial authority in the context of another procedure, supervisory bodies that are responsible for European Digital Identity Wallet issuers should, upon notification, take the necessary measures to ensure that the registration of the relying party and the inclusion of relying parties in the authentication mechanism are withdrawn or suspended until the notifying authority confirms that the irregularities identified have been remedied._

**Article 3**

Definitions

_‘relying party’ means a natural or legal person that relies upon electronic identification, European Digital Identity Wallets or other electronic identification means, or upon a trust service;_

**Article 5b - European Digital Identity Wallet-Relying Parties**

1. _Where a relying party intends to rely upon European Digital Identity Wallets_
_for the provision of public or private services by means of digital_
_interaction, the relying party shall register in the Member State where it is_
_established._
2. _The registration process shall be cost-effective and proportionate-to-risk._
_The relying party shall provide at least:_
_(a) the information necessary to authenticate to European Digital Identity Wallets, which as a minimum includes:_
_(i) the Member State in which the relying party is established; and_
_(ii) the name of the relying party and, where applicable, its registration number as stated in an official record together with identification data of that official record;_
_(b) the contact details of the relying party;_
_(c) the intended use of European Digital Identity Wallets, including a indication of the data to be requested by the relying party from users._
3. _Relying parties shall not request users to provide any data other than that_
_indicated pursuant to paragraph 2, point (c)._
4. _Paragraphs 1 and 2 shall be without prejudice to Union or national law that_
_is applicable to the provision of specific services._
5. _Member States shall make the information referred to in paragraph 2_
_publicly available online in electronically signed or sealed form suitable for_
_automated processing._
6. _Relying parties registered in accordance with this Article shall inform_
_Member States without delay about any changes to the information provided_
_in the registration pursuant to paragraph 2._
7. _Member States shall provide a common mechanism for allowing the_
_identification and authentication of relying parties, as referred to in Article_
_5a(5), point (c)._
_…_
8. _Intermediaries acting on behalf of relying parties shall be deemed to be_
_relying parties and shall not store data about the content of the transaction._
9. _By ... [6 months from the date of entry into force of this amending_
_Regulation], the Commission shall establish technical specifications and_
_procedures for the requirements referred to in paragraphs 2, 5 and 6 to 9 of this_
_Article by means of implementing acts on the implementation of European_
_Digital Identity Wallets as referred to in Article 5a(23). Those implementing_
_acts shall be adopted in accordance with the examination procedure referred_
_to in Article 48(2)._
_..._

### 2.2 Draft CIR on Relying Party registration

The public consultation version of the \[Draft of the CIR for RP-Registration\] specifies the following requirements related to Relying Party registration:


1. The roles:

- wallet-relying party - a type of the relying party; includes: service providers, PID providers, attestation providers, trust service providers and intermediaries;
- registrar

1. Setting up at each Member State one or more national registers of registered wallet-relying parties.
2. Make this information available to the public in a manner that is both human and machine-readable - via an API and website. The information made available shall be signed or sealed.
3. Member States should set out and publish one or more registration policies applicable to national registers set up in their territory
4. Wallet-relying parties should provide the necessary information (during registration process), including their entitlement(s), for inclusion in the national registers
5. Registrars should set up online and, where applicable, automated registration processes and shall verify registration information provided by the wallet-relying party in an automated manner where possible.
6. The registrant receives:

- one or more ‘Wallet-Relying Party Access Certificates’, and
- one or more 'Wallet-Relying Party Registration Certificates'

7. Wallets authenticate wallet-relying parties with use of the Wallet-Relying Party Access Certificates.
8. In a transaction, a wallet solution shall inform the wallet user whenever the wallet-relying party is asking for more information than what they have registered as intended use and the user will have possibility to reject the transaction (as well as to make a claim or report the case to a competent authority).
9. The registrar may suspend or cancel the registration with or without prior notice to the affected wallet-relying party based on proportionality assessment, taking into account the impact on the fundamental rights, privacy, security and confidentiality of the users in the eco-system, as well as the severity of the disruption caused by the suspension or cancellation and the associated costs, both for the wallet-relying party and the user.


The list of information to be provided by a wallet-relying party during registration (as per Annex I):

- official name of the wallet-relying party
- one or more official identifiers of the wallet-relying party (EORI, LEI, VAT number...)
- physical address and member state if not present in official identifier
- URL belonging to the wallet-relying party where applicable
- Detailed contact information
- description of the type of services provided
- a list of the attributes that the relying party intends to request
- a description of intended use of the data
- indication whether the wallet-relying party is a public sector body
- applicable entitlement(s) of the wallet-relying party


The list of possible entitlements (as per Annex I):

- Service_Provider
- QEAA_Provider
- Non_Q_EAA_Provider
- PUB_EAA_Provider
- PID_Provider
- QCert_for_ESeal_Provider
- QCert_for_ESig_Provider
- rQSigCDs_Provider
- rQSealCDs_Provider
- ESig_ESeal_Creation_Provider
- WAC_Provider

Requirements for electronic signatures or seals applied to the information made available on registered wallet-relying parties (as per Annex II):

- shall be JSON advanced electronic signatures at conformance level B-B, B-T or B-LT, and comply with ETSI TS 119 182-1 (JAdES baseline signatures)

Requirements on the API for the register (as per Annex II):

- be a REST API, supporting JSON as format with JAdES or ASIC signature format
- allow any requestor, without prior authentication, to make (search/read) requests to the register, for information about a wallet-relying party
- be published and documented using OpenAPI version 3 

Requirements for wallet-relying party access certificates (as per Annex IV):

- issued under certificate policy and certificate practice statement compliant with IETF RFC 3647
- certificate to include: a clear description of the public key infrastructure hierarchy and certification
paths from the end-entity wallet-relying party access certificates up to the top of the hierarchy used for issuing them, while indicating the expected trust anchor(s) in such hierarchy and paths; - a machine processable reference to the applicable certificate policy and certificate practice statement; and - the information referred to in Annex I, points 1, 2, 3, 5(b) and 5(d)

Requirements for wallet-relying party registration certificates (as per ANNEX V):

- issued under certificate policy and certificate practice statement compliant with IETF RFC 3647 and
IETF RFC 5755
- certificate to include: - the location where the certificate supporting the advanced
electronic signature or advanced electronic seal on that certificate is
available, for the entire certification path to be built up to the expected
trust anchor in the public key infrastructure hierarchy used by the
provider; - machine processable reference to the applicable certificate policy and certificate practice statement; - registration information referred to in Annex I (points 1, 2 and 8; and - to comply with IETF RFC 5755 to express attributes in relation to wallet-relying party registration certificates

Below are selected excerpts from the public consultation \[Draft of the CIR for RP-Registration\], including the recitals and the Articles that establish these requirements.

**Recital (1)**

_Member States should establish and maintain registers of registered wallet-relying parties established in their territory._

**Recital (4)**

_In order to facilitate the consultation of the information on registered wallet-relying parties across the Union, Member States should make this information available to the public in a manner that is both human and machine-readable._

**Recital (6)**

_As registration policies are a useful tool for providing clear guidance to the wallet-relying parties on the registration process, Member States should set out and publish the registration policies applicable to registers set up in their territory._

**Recital (7)**

_[...] another objective of the relying party registration is to facilitate the verification by Member States of the lawfulness of the activities of the wallet-relying parties. Therefore, wallet-relying parties should provide, for inclusion in the registers the necessary information, including their entitlement(s)._

**Recital (8)**

_In order to ensure that the registration process is cost-effective and proportionate-to risk, and to strike an appropriate balance between meeting a high level of transparency and safety on the one hand and ensuring uptake by service providers on the other hand, registrars should set up online and, where applicable, automated registration processes for wallet-relying parties that are easy to use and they should verify applications for registration without undue delay._

**Recital (10)**

_[...] wallet-relying parties should use wallet-relying party access certificates when they identify themselves to wallet units. To guarantee interoperability of those certificates across all wallets provided within the Union, wallet-relying parties access certificates should adhere to common requirements set-out in the Annex to this Regulation_

**Recital (11)**

_[...] wallet-relying parties are not to request users to provide any data other than those indicated for the intended use of wallets during the registration process. Wallet users should be enabled to verify the registration data of wallet-relying parties. To enable wallet users to verify that the attributes being requested by the wallet-relying party are within the scope of their registered attributes, Member States may require the issuance of wallet-relying party registration certificates to registered wallet-relying parties. To ensure the interoperability of the wallet-relying party registration certificates, Member States should ensure that those certificates meet the requirements and standards set out in the Annex of this Implementing Regulation._

**Recital (12)**
_[...] registrars should be able to suspend or cancel the registration of any wallet-relying party without prior notice where the registrars have reason to believe that the registration contains information which is not accurate, not up to date or misleading, the wallet-relying party is not compliant with the registration policy or the wallet-relying party is otherwise acting in breach of Union or national law in a way that relates to their role as a wallet-relying party. In order to safeguard the stability of the wallet ecosystem, the decision to suspend or cancel a registration should be proportionate to the service disruption caused by the suspension or cancellation and the associated cost and inconvenience for the service provider and the user. For the same reason, supervisory bodies are to be enabled to suspend and cancel the registration required pursuant to Article 46a(4), point (f) of Regulation (EU) No 910/2014._

**Article 2**

Key definitions

_‘wallet-relying party’ means a relying party that intends to rely upon wallet units for the provision of public or private services by means of digital interaction;_

_‘register of wallet-relying parties’ means an electronic register used by a Member State to make information on wallet-relying parties registered in that Member State publicly available as set out in Article 5b(5) of Regulation (EU) No 910/2014;_

_‘provider of wallet-relying party access certificates’ means a natural or legal person mandated by a Member State to issue wallet-relying party access certificates to wallet-relying parties registered in that Member State;_

_‘wallet-relying party access certificate’ means a certificate for electronic seals or signatures authenticating and validating the wallet-relying party issued by a provider of wallet-relying party access certificates;_

_‘registrar of wallet-relying parties’ means a body responsible for establishing and maintaining a list of registered wallet-relying parties established in their territory who has been designated by a Member State;_

_‘wallet-relying party registration certificate’ means a data object that indicates the attributes the relying party has registered to intend to request from users;_

_‘provider of wallet-relying party registration certificates’ means a natural or legal person mandated by a Member State to issue wallet-relying party registration certificates to wallet-relying parties registered in that Member State._

**Article 3**

National registers

_2 Member States shall make the information set out in Annex I on registered wallet-relying parties from all national registers publicly available online, both in human readable form and in a form suitable for automated processing_

_3. The information shall be available through a single national application programming interface (‘API’) and through a national website. It shall be electronically signed or sealed by or on behalf of the registrar, in accordance with the requirements set out in Section 1 of Annex II._

**Article 4**

Registration policies

_1. Member States shall lay down and publish one or more national registration policies applicable to national registers._

_3. The registration policy shall cover at least the following points:_

 _(a) the identification and authentication procedures applicable to wallet-relying parties during the registration process;_

 _(b) the supporting documentation to be provided by the wallet-relying party to establish their identity, business registration, any applicable entitlement(s), and other relevant information that is required under the registration policy;_

 _(c) where applicable, the description of the authentic sources or other official electronic records in the Member State where the register is set up, that can be relied upon to provide accurate data, information or other evidence required as part of the registration process;_

 _(d) where applicable, the automated means supported to enable wallet-relying parties to register or to update an existing registration;_

 _(e) the means of redress available to wallet-relying parties under the law of the Member State where the register is set up;_

 _(f) the rules and procedures for the verification of the identity of the registered wallet-relying party and of any other relevant information provided by that party._

**Article 6**

The registration process

_3. Registrars shall verify, where applicable, in an automated manner:_

 _(a) the accuracy and validity of the information required under Article 5;_

 _(b) where applicable, the power of attorney of a representative of the wallet-relying party in accordance with the laws and procedures of the Member State where the register is set up;_

 _(c) the type of entitlement(s) of the wallet-relying party as set out in **Annex I.**_

_4. The verification of the information referred to in paragraph 3 shall include an authenticity and validity assessment of the provided information against the supporting documentation provided by the wallet-relying parties and against any authentic sources or other official electronic records in the Member State where the register is set up and to which the registrars have access in accordance with national law. The verification of entitlements of wallet-relying parties shall be carried out in accordance with **Annex III**._

_5. When a wallet-relying party no longer intends to rely upon wallet units for the provision of public or private services under a specific registration, it shall notify the relevant registrar without undue delay and request the cancellation of that registration._

**Article 7**

Wallet-relying party access certificates

_1. Member States shall ensure that providers of wallet-relying party access certificates issue wallet-relying party access certificates to wallet-relying parties registered in accordance with the requirements set out in Article 4 to Article 6 of this Regulation._

_2. Member States shall set up dedicated certificate policies and certificate practice statements in accordance with the requirements set out in Annex IV. Member States shall ensure that wallet-relying party access certificates meet the requirements set out in **Annex IV**._

**Article 8**

Wallet-relying party registration certificates

_1. Member States may require providers of wallet-relying party registration certificates to issue wallet-relying party registration certificates to wallet-relying parties registered in accordance with the requirements set out in Article 4 to Article 6 of this Regulation._

_2. Where Member States require the provision of wallet-relying party registration certificates, Member States shall ensure that these certificates meet the requirements set out in **Annex V**._

**Article 9**
Suspension and cancellation

_1. Registrars may suspend or cancel a registration of a wallet-relying party where such a suspension or cancellation is requested by a supervisory body pursuant to Article 46a(4), point (f) of Regulation (EU) No 910/2014 or where the registrars have reasons to believe that:_
_(a) the registration contains information which is not accurate, not up to date or misleading;_
_(b) the wallet-relying party is not compliant with the registration policy;_
_(c) the wallet-relying party is requesting more attributes than what they have registered in accordance with Article 5 and Article 6 of this Regulation;_
_(d) the wallet-relying party is otherwise acting in breach of Union or law of that Member State in a way that relates to their role as a wallet-relying party;_

_4. When considering the suspension or cancellation in accordance with Article 9 paragraph 2, the registrar shall conduct a proportionality assessment, taking into account the impact on the fundamental rights privacy, security and confidentiality of the users in the eco-system, as well as the severity of the disruption caused by the suspension or cancellation and the associated costs, both for the wallet-relying party and the user. Based on the result of this assessment, the registrar may suspend or cancel the registration with or without prior notice to the affected wallet-relying party._

**ANNEX I**

(summary)

Information regarding wallet-relying parties

- name of the wallet-relying party as stated in official record
- one or more identifiers of the wallet-relying party (EORI, LEI, VAT number...)
- physical address
- Detailed contact information
- a description of the type of services provided
- a list of the attributes, that the relying party intends to request
- description of intended use of the attributes
- indication whether the wallet-relying party is a public sector body
- applicable entitlement(s) of the wallet-relying party

The possible entitlements of the wallet-relying party:

- Service_Provider
- QEAA_Provider
- Non_Q_EAA_Provider
- PUB_EAA_Provider
- PID_Provider
- QCert_for_ESeal_Provider
- QCert_for_ESig_Provider
- rQSigCDs_Provider
- rQSealCDs_Provider
- ESig_ESeal_Creation_Provider
- WAC_Provider

_5. Detailed contact information of the wallet-relying party, one or more, including:_
_(a) a website for providing helpdesk and support;_
_(b) a phone number where the wallet-relying party can be contacted for matters pertaining to its registration and intended use of the wallet units;_
_(c) a digital address where the wallet-relying party can be contacted for matters pertaining to its registration and intended use of the wallet units;_
_(d) an e-mail address where the wallet-relying party can be contacted for matters pertaining to its registration and intended use of the wallet units;_

_7. A list of the attributes that the relying party intends to request, expressed as a friendly name and a technical name including the namespace that the attributes are grouped under in a machine-readable format for automated processing, with an indication if they are mandatory or optional._

**ANNEX II**

(summary)

_1. REQUIREMENTS ON ELECTRONIC SIGNATURES OR SEALS APPLIED TO THE INFORMATION MADE AVAILABLE ON REGISTERED WALLET-RELYING PARTIES_

- The file format used by the API: be JavaScript Object Notation (JSON)
- electronic signatures and electronic seals - JSON advanced electronic signatures at conformance level B-B, B-T or B-LT, comply with ETSI TS 119 182-1 V1.2.1 (JAdES baseline signatures)

_2. REQUIREMENTS ON THE SINGLE API_

- REST API, supporting JSON data format
- published as OpenAPI version 3
- allow any requestor, without prior authentication, to make (search/read) requests to the register
- provide security functions in order to ensure the availability and integrity of the API and the information available through it. The API shall be secure by default and by design.


**ANNEX III**

(summary)

_Source of documentary evidence for the verification of entitlements of wallet-relying parties_

- verification of qualified trust service providers - shall be based on the national trusted lists
- verification of non-qualified trust service providers - shall be based on the national trusted lists or on national MS verification procedures (set out in their registration policies)
- verification of providers of person identification data - shall be based on the list of providers of person identification data published by the Commission in accordance with Article 5a(18) of Regulation (EU) No 910/2014
- verification of providers of electronic attestations of attributes issued by or on behalf of a public sector body responsible for an authentic source - shall be based on the list published by the Commission in accordance with Article 45f(3) of Regulation (EU) No 910/2014

**ANNEX IV**

(summary)

_Requirements for wallet-relying party access certificates_

- X.509 certificate with certificate policy and certificate practice statement
- shall comply with IETF RFC 3647
- plus additional requirements set out in the Annex IV

**ANNEX V**

(summary)

_Requirements for wallet-relying party registration certificates_

- certificate policy and certificate practice statement shall comply with IETF RFC 3647 and IETF RFC 5755
- includes the information referred to in Annex I, points 1, 2 and 8;
- expresses attributes in way compliant with IETF RFC 5755;
- plus additional requirements set out in the Annex V.
