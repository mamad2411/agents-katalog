---
name: "arf-topic-e-pseudonyms-and-user-authentica-part-1"
description: "Use when implementing pseudonyms or user authentication mechanisms. Covers verifiable pseudonyms, attested pseudonyms, scope-rate-limited pseudonyms, and ZKP-based approaches. Part 1: covers Versioning, 1 Introduction, 2 Types of Pseudonyms ...."
sections:
  - "E - Pseudonyms, including User authentication mechanism"
  - "Versioning"
  - "1 Introduction"
  - "2 Types of Pseudonyms"
  - "3 Legal Requirements for Pseudonyms"
  - "4 Use Cases"
  - "5 High-Level Approach to Pseudonyms: [W3C WebAuthn]"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~7031 -->

Version 1.0, updated 19 November 2025

[Link to GitHub discussion](https://www.github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/discussions/375)

# E - Pseudonyms, including User authentication mechanism

## Versioning

| Version                 | Date       | Description                                                               |
|-------------------------|------------|---------------------------------------------------------------------------|
| `0.7` (part of ARF 2.5) | 03.04.2025 | Initial version after first rounds of discussion.                         |
| `0.8`                   | 26.09.2025 | Restructuring, additional use cases added, and HLRs for future use cases. |
| `0.9`                   | 25.10.2025 | Optional to implement WebAuthn, revision of HLRs.                         |
| `1.0`                   | 19.11.2025 | Revision after comments by member states                                  |

## 1 Introduction

### 1.1 Discussion Paper Topic Description

This document is the Discussion Paper for the European Digital Identity Cooperation Group regarding Topic E: Pseudonyms, including User authentication mechanism.
The ARF Development Plan [ARF_DevPlan] describes this Topic as follows:

*High-level requirements for pseudonyms in the ARF need to be further detailed, including
specifying the use cases where pseudonyms should be applied.*

### 1.2 Key Words

This document uses the capitalised key words 'SHALL', 'SHALL NOT', 'SHOULD' and 'MAY' as specified in RFC 2119, i.e., to indicate requirements, prohibitions, recommendations and options specified in this document.
In addition, 'must' (non-capitalised) is used to indicate an external constraint, for instance a self-evident necessity or a requirement that is mandated by an external document. The word 'can' indicates a capability, whereas other words, such as 'will', 'is' or 'are' are intended as statements of fact.

### 1.3 Document Structure

The document is structured as follows:

- [Chapter 2](#2-types-of-pseudonyms) presents a basic distinction between different types of pseudonyms as well as introducing terminology for these different types. 

- [Chapter 3](#3-legal-requirements-for-pseudonyms) presents the legal requirements for functionality related to pseudonyms.

- [Chapter 4](#4-use-cases) explains envisioned use cases for pseudonyms and lists open questions related to these use cases.

- [Chapter 5](#5-high-level-approach-to-pseudonyms-w3c-webauthn) presents the current (as stated in [CIR.2024.2979] and version 0.7 of this paper) technical approach to pseudonyms and highlights its challenges.

- [Chapter 6](#6-relation-to-other-topics) relates the topic to other topics being discussed and previously identified risks.

- [Chapter 7](#7-changes-to-the-arf) presents the additions and changes that will be made to the ARF as a result of discussing this topic with Member States.

- [Chapter 8](#8-references) lists references used in this document. 

Finally, for completeness, in [Appendix A](#appendix-a-questions-related-to-use-cases-a-and-b), we include some of the previous questions that was discussed during the meetings for the basic use cases ([Use Case A](#41-use-case-a-pseudonymous-authentication) and [Use Case B](#42-use-case-b-presentation-of-attributes-with-subsequent-authentication-using-pseudonyms)).

## 2 Types of Pseudonyms
A pseudonym is an alternative name or identifier used by a person for a particular purpose.
Before examining the legal requirements for the Pseudonyms functionality, we introduce three different types of pseudonyms that can achieve different policy and technical goals and which we will use in this paper. 

- **Verifiable pseudonym:** A verifiable pseudonym is a pseudonym that allows a User to prove possession over the pseudonym and thereby authenticate as the pseudonym.
- **Attested pseudonym:** An attested pseudonym is a subtype of a verifiable pseudonym, allowing Relying Parties to verify that a third party has attested that a pseudonym is owned by a User. 
- **Scope rate limited pseudonym:** A scope rate limited pseudonym is a subtype of a verifiable pseudonym guaranteeing that the user is limited to control only a certain number of pseudonyms within the rate for a given scope. 

A special case of a *scope rate limited pseudonym* occurs when the rate is set to 1. In that case, each User is guaranteed to have at most one valid pseudonym within the relevant scope, for example, in an electronic voting system. This is often referred to as a *scope unique* or *scope exclusive pseudonym*.

Note also that the EUDI Wallet ecosystem already enables *attested pseudonyms* as there are no hindrances for an Attestation Provider to issue a (Q)EAA attesting to a particular pseudonym for a User. As such attestations are key-bound, a User could subsequently authenticate as such pseudonym by making a verifiable presentation to Relying Parties. There is however no EU-wide definition of such an attestation type. 
The concept of Cryptographic Binding of Attestations scheme as discussed in [Topic K - Combined Presentation of Attributes](k-combined-presentation-of-attestations.md) would allow such attested pseudonyms to be cryptographically bound to the same User during issuance.

## 3 Legal Requirements for Pseudonyms

There are two legal texts that impose direct requirements on the pseudonym functionality of the Wallet Units: the [European Digital Identity Regulation] and [CIR.2024.2979], the Implementing Act on PID and EAA.

Below we recap the respective legal requirements from these sources.

### 3.1 The [European Digital Identity Regulation] about Pseudonyms
There are two main requirements in the [European Digital Identity Regulation] about Pseudonyms in relation to Wallet Units:

1. Wallet Units must be able to generate pseudonyms and store them encrypted and locally within the Wallet Unit.
2. Relying Parties must accept identification via pseudonyms when there are no legal requirements for legal identification.

Below are the actual parts of the regulation that establish these requirements.

| Recitals/Articles                                                   | Text                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
|-------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Recital 19                                                  | ... Reliance on the legal identity should not hinder European Digital Identity Wallet users to access services under a pseudonym, where there is no legal requirement for legal identity for authentication. ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Recital 22                                                  | European Digital Identity Wallets should include a functionality to generate user-chosen and managed pseudonyms, to authenticate when accessing online services.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Recital 57                                                  | Where very large online platforms within the meaning of Article 33(1) of Regulation (EU) 2022/2065 of the European Parliament and of the Council require users to be authenticated in order to access online services, those platforms should be required to accept the use of European Digital Identity Wallets upon the voluntary request of the user. Users should be under no obligation to use a European Digital Identity Wallet to access private services and should not be restricted or hindered in their access to services on the grounds that they do not use a European Digital Identity Wallet. However, if users wish to do so, very large online platforms should accept them for that purpose, while respecting the principle of data minimisation and the right of the users to use freely chosen pseudonyms. ... |
| Recital 60                                                  | Unless specific rules of Union or national law require users to identify themselves, accessing services by using a pseudonym should not be prohibited.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| Article 5 Pseudonyms in electronic transaction              | Without prejudice to specific rules of Union or national law requiring users to identify themselves or to the legal effect given to pseudonyms under national law, the use of pseudonyms that are chosen by the user shall not be prohibited.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| Article 5a European Digital Identity Wallets                | ... 4. European Digital Identity Wallets shall enable the user, in a manner that is user-friendly, transparent, and traceable by the user, to: ... (b) generate pseudonyms and store them encrypted and locally within the European Digital Identity Wallet; ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| Article 5b European Digital Identity Wallet-Relying Parties | ... 9. ... Relying parties shall not refuse the use of pseudonyms, where the identification of the user is not required by Union or national law. ...                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

Note that the choice given to the User when choosing their pseudonym (as pr. Recital 22, 57, and Article 5) necessarily must be subject to restrictions. Alternatively, it will be impossible to prevent two Users from choosing the same pseudonym and thus authentication as such pseudonym would not provide any meaningful guarantee. Such restriction may be to ensure that a pseudonym must contain sufficient entropy to prevent collisions which will still enable the User to choose their pseudonyms by using different randomness. A User can be given such a choice for any of the different pseudonym types presented in [Chapter 2](#2-types-of-pseudonyms).
 
Additionally, pseudonyms are mentioned in Article 32 and Annex IV about the validation of qualified electronic signatures and certificates. However, the use of pseudonyms in this context is completely independent from the notion of pseudonyms used by the Wallet Unit for authentication, as discussed in this discussion paper.

### 3.2 [CIR.2024.2979] about Pseudonyms

[CIR.2024.2979] specifies three main requirements for pseudonyms:

1. [W3C WebAuthn] defines the technical specification for pseudonyms.
2. The pseudonyms the Wallet Unit generates must be unique for each Relying Party.
3. The pseudonyms can be used either stand-alone or in combination with other attested attributes.

Below are the actual excepts of the CIR that establish these requirements. 

| Recitals/Articles  | Text                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
|------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Recital 14 | The generation of wallet-relying party specific pseudonyms should enable wallet users to authenticate themselves without providing wallet-relying parties with unnecessary information. As set out in Regulation (EU) No 910/2014, wallet users are not to be hindered from accessing services under a pseudonym, where there is no legal requirement for legal identity for authentication. Therefore, the wallets are to include a functionality to generate user-chosen and managed pseudonyms, to authenticate when accessing online services. The implementation of the specifications set out in Annex V should enable these functionalities accordingly. Further, wallet-relying parties are not to request users to provide any data other than those indicated for the intended use of wallets in the relying party register. Wallet users should be enabled to verify the registration data of relying parties at any point in time. |
| Article 14 | 1. Wallet units shall support the generation of pseudonyms for wallet users in compliance with the technical specifications set out in Annex V. 2. Wallet units shall support the generation, upon the request of a wallet-relying party, of a pseudonym which is specific and unique to that wallet-relying party and provide this pseudonym to the wallet-relying party, either standalone or in combination with any person identification data or electronic attribute attestation requested by that wallet-relying party. |
| Annex V    | TECHNICAL SPECIFICATIONS FOR PSEUDONYM GENERATION REFERRED TO IN ARTICLE 14 Technical specifications: — WebAuthn Sch– W3C Recommendation, 8 April 2021, Level 2, <https://www.w3.org/TR/2021/REC-webauthn-2-20210408/>.|                                                                                        

Please note that Article 1 of [CIR.2024.2979] stipulates that it can be updated in the future "to keep in line with technology […] in particular the Architecture and Reference Framework". This means that the text of the CIR and the standards references therein serve as starting point of the further development of the ARF, but that the ARF is not per definition constrained by the current version of [CIR.2024.2979].

## 4 Use Cases

This chapter introduces and elaborates on several use cases for pseudonyms. Use cases A and B are inferred from the above legal requirements, and the distinction between these two use cases follows from Article 14 (2) in [CIR.2024.2979]. The use cases C and D are additional use cases envisioned to be useful to support in the EUDI Wallet ecosystem. 

The use cases all exists in both cross-device and same device flows.

### 4.1 Use Case A: Pseudonymous Authentication

Pseudonyms can be used to authenticate a User when it is not necessary for a Relying Party to learn the legal identity of a User.

Concretely, the use case is as follows:

1. A User registers a pseudonym at a Relying Party, using their Wallet Unit.
2. The User can afterwards do a series of interactions with this Relying Party.
3. If the User at a later point wishes to build upon previous interactions with this Relying Party, they should then be able to authenticate with the pseudonym used when registering. Thereby, the User "logs in" to the same account at the Relying Party. The User uses their Wallet Unit to perform this pseudonymous authentication.

The Relying Party should be guaranteed that only the same User who registered the pseudonym can subsequently authenticate as this pseudonym towards the Relying Party. This implies that pseudonyms across multiple Users must be collision free i.e., no two Users can have the same pseudonym. Additionally, note that no guarantee is given to the Relying Party about how many such pseudonyms a User may control. One User may Use this to control several different accounts at the same Relying Party. 

> To support this use case verifiable pseudonyms must be supported. Alternatively, if the Relying Parties can also act as an Attestation Provider, then attested pseudonyms can also support this use case. In that case, the flow would be that the Relying Party (now acting as an issuer) either picks or let the User pick a pseudonym and attests this into a verifiable credential that the User stores. Later on the User can do a verifiable presentation to the Relying Party to authenticate as the pseudonym. 

### 4.2 Use Case B: Presentation of Attributes with Subsequent Authentication using Pseudonyms

Similar to use case A above, a User wishes to create an account with an associated pseudonym that can be used for subsequent authentication at later sessions. However, in this scenario the User additionally would like to register verifiable attributes in the form of either Person Identification Data (PID), Qualified Electronic Attestation of Attributes (QEAAs), Electronic Attestation of Attributes issued by or on behalf of a public sector body responsible for an authentic source (PuB-EAA), or non-qualified Electronic Attestation of Attributes (EAAs) while registering.

Concretely, the use case goes as follows:

1. A User registers a pseudonym at a Relying Party, using their Wallet Unit.
2. In the same interaction, the User also presents attributes from a PID or attestation in their Wallet Unit to the Relying Party. This could for example be an "age over 18" attribute. 
3. The User can afterward do a series of interactions with this Relying Party.
4. If the User at a later point wishes to build upon previous interactions with this Relying Party, they should then be able to authenticate with the pseudonym used when registering. Thereby, the User "logs in" to the same account at the Relying Party. The User uses their Wallet Unit to perform this pseudonymous authentication.

Note that this is particularly useful when the disclosed attributes do not uniquely identify the User as this now allows the Relying Party to continue interactions with the same User at a later point (letting the User make a new presentation of attributes for subsequent interactions will not allow this because of the unlinkability requirements for presentations). Similar to use case A, there are no guarantees on how many different pseudonyms a User may use for the same Relying Party. 

In addition, to the basic guarantee that subsequent authentications can only be performed by the User registering the pseudonym and that presented attributes can be trusted to hold, ideally, the Relying Party should also be guaranteed that the registered pseudonym and the attributes are belonging (and controlled) by only one person (to prevent two person's collaborating to create an account and thereby circumvent for example restrictions on age). 

> This use case is supported by verifiable pseudonyms. However, if the additional guarantee about the pseudonym and the presentation being tied to the same User is required, then neither of the pseudonym types introduced in [Chapter 2](#2-types-of-pseudonyms) supports this by default, as it requires not only properties of the pseudonym, but rather a property of their combined presentation with the attested attributes. 

### 4.3 Use Case C: Rate Limited Participation

This use case builds on either use case A or B, adding an additional guarantee for the Relying Party: They are guaranteed that a particular person can only register a number of different pseudonyms (referred to as the rate) for a particular scope. The specific number and scope are determined by the Relying Party. 

Note that this rather abstract use case enables a wider range of concrete use cases. Notable examples include: 
+ It enables users to participate in online voting (guaranteeing that each individual can vote only once).
+ It enables Relying Parties to do reliable surveying (again ensuring users registers only once). 
+ It can be used to combat spam or bot accounts, for example to protect social media from so called "troll farms".

> Scope rate limited pseudonyms are the only of the pseudonyms types that will support this use case. 

### 4.4 Use Case D: Linkable Pseudonymous Authentication

This use case considers a case where a single pseudonym must be recognized and able to authenticate towards several different actors. That is, instead of having one or multiple pseudonyms pr. Relying Party, a user wishes to authenticate with the same pseudonym towards several different relying parties and allow these parties to exchange information based upon this pseudonym. I.e., a pseudonym that allow specific Relying Parties to *link* the authentications to provide integrated services in a collaborative way.

The use case goes as follows: 
1. A User interacts with a Relying Party "A", registers a pseudonym at this Relying Party and may do a series of interactions with this Relying Party.
2. If the User at a later point wishes to allow another Relying Party "B" to learn the pseudonym they used to interact with "A" to allow "A" and "B", then the User should be able to authenticate with the pseudonym used at "A" towards "B". 

This use case may be extended to let any number of Relying Parties (for example within a sector) link the User's pseudonym.
Examples of this use case include: 

- **e-Commerce:** A User can register a pseudonym when ordering goods online and subsequently authenticate with this pseudonym towards the carrier to be allowed to pickup the goods. Note that if this is combined with for example an age verification upon registration of the pseudonym as in use case B, this can ensure that the person picking up the goods in fact also fulfills said age verification. 
- **Health insurance:** A User can register and associate a pseudonym at their health insurance company. Upon visits to a healthcare provider, the User can then choose to authenticate as their pseudonym. The healthcare provider can then use that pseudonym to contact the insurance company and facilitate for example payments for the provided service. 

Note that even though linkability is useful in some contexts as described above, it is also poses a threat to the User's privacy. If they are authenticating with pseudonym also used elsewhere when not necessary this may be used to track the User. 

> These use cases can be supported by using just verifiable pseudonyms (by enabling the User to register the same verifiable pseudonym with multiple Relying Parties) or alternatively attested pseudonyms (by letting the Relying Party also take the role of an issuer and issue an Attested Pseudonym to the User's Wallet which the User can subsequently present to other Relying Parties).

## 5 High-Level Approach to Pseudonyms: [W3C WebAuthn]

### 5.1 Introduction to Passkeys

[CIR.2024.2979] and the standards referenced therein serve as starting point for the further development of the pseudonyms functionality, however, the ARF is not per definition contstrainted by the current version of [CIR.2024.2979]. 
Therefore, as specified in [CIR.2024.2979], [W3C WebAuthn] defines the current technical specification for pseudonyms. 

Passkeys are a widely used type of credential that can serve as a verifiable pseudonym. They are created and asserted using the [W3C WebAuthn] API.

Passkeys are to be seen as an alternative to passwords.
The idea is that a User, when registering a user account at a service, uses a secure device to generate a public-private key pair, registers the public key at the service, and can then subsequently use the private key to authenticate towards the service at later points in time.

In a bit more detail, the flow for using such passkeys follows the following blueprint:

**Registration:**

1. The User generates a public-private key pair and stores both the public and the private key at their secure device (referred to as an authenticator).
2. The User registers the public key at the desired Relying Party service.

**Authentication:**

1. When the User wishes to authenticate towards a service, the service will send them a challenge consisting of a random value.
2. The User uses the private key stored on their secure device to sign the challenge and sends this back to the service.
3. The service verifies that the signature on the challenge can be verified using the registered public key. If the signature verifies and the origin matches the expected origin, the User is considered authenticated and thereby granted access to the service.

### 5.2 Introduction to [W3C WebAuthn]

#### 5.2.1 Overview

[W3C WebAuthn] defines an API for the creation and use of Passkeys. Conceptually, in addition to the User, there are four different logical components in this specification:

- **Relying Party Server:** The Relying Party that wishes to offer a service based on authentication using Passkeys.
- **Relying Party Client:** The program provided by the Relying Party that runs in the Client of the User and communicates with the Relying Party Server. The Relying Party Client is typically some JavaScript code, provided by the Relying Party, that runs on the Client (i.e., browser).
- **Client:** The client that the User uses to interact with the Relying Party's server and with the User's authenticator. The Client can be thought of as the browser that the User uses to access the Relying Party's service.
- **Authenticator:** The device controlled by the User to create, store, and use the Passkeys. In the context of the EUDI Wallet ecosystem, the Wallet Unit will act as the Authenticator.

Note that the Relying Party Client and the Client are two programs that are executed on the same physical machine.

[W3C WebAuthn] defines a model dividing the responsibilities between these different entities and defines an interface between the Relying Party Client and the Client. Additionally, it defines a challenge/response protocol to authenticate with Passkeys. The interface is referred to as the *WebAuthn API*.

However, [W3C WebAuthn] does not specify how the Authenticator and the Client must communicate. In this context, [Chapter 6](#6-relation-to-other-topics) briefly discuss the relation to [Topic F (Digital Credential API)](./f-digital-credential-api.md) .

[W3C WebAuthn] relies on several different types of identifiers, including:

- **Relying Party ID:** An identifier unique to the Relying Party, which must be a valid domain string. This what the User will identify the Relying Party by and let the Authenticator learn which Relying Party is asking for registration/authentication.
- **Credential ID:** A unique identifier chosen by the Authenticator for each Passkey.
- **User ID:** An identifier unique to each User, which is assigned by the Relying Party. This will be provided to the Authenticator when registering a new Passkey. Subsequently, it will be provided by the Authenticator when authenticating towards the Relying Party. The Authenticator will keep track of which Passkeys are available for which User IDs and Relying Party IDs. The Relying Party keeps track of a User Name for each User ID.
- **User Name:** An alias that may be chosen by the User or the Relying Party and assigned to a specific Passkey on the Authenticator. This allows the User to easily distinguish and select which Passkey they want to authenticate with, if several are present in the Authenticator for the given Relying Party.

The next sections elaborate on how the different components work together to allow the registration and subsequent authentication using Passkeys.

#### 5.2.2 Registration

The flow for registering a Passkey in [W3C WebAuthn] is the following:

0. The User requests (out of band of WebAuthn) the Relying Party to create a new Pseudonym.
1. The Relying Party Server creates a challenge and sends this along with the User ID, the Relying Party ID, and the User Name to the Relying Party Client.
2. The Relying Party Client forwards the information to the Client using the WebAuthnAPI.
3. The Client checks that the Relying Party ID is consistent with the caller's origin and forwards the information to the Authenticator along with other contextual data.
4. The Authenticator authenticates the User (for example using a PIN or via biometrics). It then generates a new key pair with a new Credential ID and set the scope of this to the specific Relying Party ID and User ID. Finally, the Authenticator may generate an attestation (explained in [Section 5.2.3](#523-pseudonym-attestation)) and sends this, as well as the public key and its Credential ID, to the Client.
5. The Client then forwards the information to the Relying Party Client that again forwards it to the Relying Party Server.
6. The Relying Party Server verifies the attestation and registers the received public key for this User ID.

Note that the Authenticator stores the public key in a way such that it is scoped uniquely to a specific Relying Party, aligning with the requirements of [CIR.2024.2979], Article 14 (2), which states that the pseudonyms must be unique to each Relying Party.

#### 5.2.3 Pseudonym Attestation

The term 'attestation' is here used differently than elsewhere in the ARF.
In this context, the attestation is not about attributes of the User, but rather about attributes of the Authenticator. The attestation serves to ensure the Relying Party that they are talking with an Authenticator with certain properties. The attestation often takes the form of a signature on the challenge as well as some other contextual data.

In [W3C WebAuthn], five different types of attestations are mentioned:

- **Basic Attestation:** The Authenticator stores a single master public and private key. The private key is used to sign all attestations and a certificate on the public key is included in the attestation data to allow the Relying Party to verify the signature.

- **Attestation CA:** Similar to the above, in the sense that the Authenticator stores a single master public and private key stored. However, instead of using this to attest Passkeys, the Authenticator uses this to authenticate towards a Certificate Authority (CA), which is then configured to issue certificates to the Authenticator on multiple attestation key pairs.

- **Anonymisation CA:** Similar to the second bullet above, except that it is explicit that the Authenticator requests a certificate for a new attestation key pair per generated Passkey.

- **Self Attestation:** The attestation is signed with the private key of the newly generated key pair in the Passkey. Note that this does not give any guarantees for the Relying Party about the authenticator they are interacting with.

- **No Attestation Statement:** No attestation is given. Note that this does not give any guarantees for the Relying Party about the Authenticator they are interacting with.

[Section 6.1](#61-topic-a-privacy-risks-and-mitigations)) discusses how these three possibilities relate to previously identified privacy risks about user surveillance (see also [Topic A](./a-privacy-risks-and-mitigations.md)).

Note that in the EUDIW ecosystem Wallet Unit Attestations (WUAs) as defined in [TS3](https://github.com/eu-digital-identity-wallet/eudi-doc-standards-and-technical-specifications/blob/main/docs/technical-specifications/ts3-wallet-unit-attestation.md) serve a similar purpose to these types of attestations but in relation to issuance of PIDs or other attestations. 

#### 5.2.4 Authentication

The flow for authentication using a Passkey following [W3C WebAuthn] is:

1. The Relying Party Server creates a challenge and sends this along with its Relying Party ID to the Relying Party Client.
2. The Relying Party Client forwards the information to the Client using the WebAuthn API.
3. The Client checks that the Relying Party ID is consistent with the caller's origin and forwards the information to the Authenticator along with other contextual data.
4. The Authenticator authenticates the User (for example using a PIN or via biometrics). It then prompts the User to select one of the Passkeys scoped to this Relying Party ID, if there are multiple. For this step the User Name can be presented to the User. Finally, the Authenticator uses the private key of the chosen key pair (= Passkey) to sign the challenge as well as some contextual data including the User ID, Credential ID, and the Relying Party ID. The Authenticator then sends this to the Client.
5. The Client forwards the information to the Relying Party Client, which again forwards it to the Relying Party Server.
6. The Relying Party Server verifies the signature with the stored public key for this User ID and Credential ID, and, depending on the outcome of this verification, considers the User to be authenticated.

### 5.3 Challenges using [W3C WebAuthn] for Pseudonyms in the EUDI Wallet

This section list challenges related to the use of [W3C WebAuthn] as the technical specification for pseudonyms:

1. On its own, [W3C WebAuthn] does not support enable a Relying Party to obtain a strong guarantee ensuring that presentation of attributes as well as the registering of a pseudonym is performed by the same User (which is useful for [Use Case B](#42-use-case-b-presentation-of-attributes-with-subsequent-authentication-using-pseudonyms)). 
2. [W3C WebAuthn] does not support scope rate limited pseudonyms and in particular does not allow Relying parties to verify pseudonyms are limited to a particular scope and rate. Hence, [Use Case C](#43-use-case-c-rate-limited-participation) is not supported. 
3. For privacy reasons, [W3C WebAuthn] does not allow passkeys to be used for multiple different Relying Parties. Hence, it cannot be used for [Use Case D](#44-use-case-d-linkable-pseudonymous-authentication). 
4. Attestations may be linkable; see discussion in [Section 6.1](#61-topic-a-privacy-risks-and-mitigations) and also [Topic A](./a-privacy-risks-and-mitigations.md). This risk depends on the chosen type of attestation.
5. The information about the Relying Party is verified only by the Client and not by the Authenticator itself. This may be a problem, as in Article 5a (5) a) vii) of the [European Digital Identity Regulation] it is stated that "*European Digital Identity Wallets shall, in particular ... ensure that the relying parties can be authenticated and identified by implementing authentication mechanisms in accordance with Article 5b;...*".
