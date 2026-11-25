---
name: "arf-architecture"
description: "Use when designing wallet components, understanding EUDI design principles (user-centricity, interoperability, privacy/security by design), or working with the reference architecture, its components, and interfaces."
sections:
  - "4.1 Introduction"
  - "4.2 Design principles"
  - "4.2.1 User-centricity"
  - "4.2.2 Accessibility"
  - "4.2.3 Interoperability"
  - "4.2.4 Privacy by design"
  - "4.2.5 Security by design"
  - "4.3 Reference architecture"
  - "4.3.1 Overview"
  - "4.3.2 Components of a Wallet Unit"
  - "4.3.3 Wallet Unit interfaces and protocols"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~5491 -->

### 4.1 Introduction

This chapter provides a broad overview of the EUDI Wallet ecosystem's core
components, their interfaces, and the overall design principles. This chapter is
structured as follows:

- [Section 4.2][42-design-principles] discusses the design principles that
guided the design of the EUDI Wallet ecosystem, as described in this ARF.
- [Section 4.3][43-reference-architecture] presents an overview of the
ecosystem's architecture, focussing on the components that make up a Wallet Unit
and on the interfaces between a Wallet Unit and other entities, as well as the
protocols used on these interfaces.
- [Section 4.4][44-data-presentation-flows] discusses the different attestation
presentation flows enabled by this architecture, and in particular the
mechanisms foreseen to enable and secure remote presentation flows in which the
Wallet Unit and the Relying Party interact over the internet.
- [Section 4.5][45-wscd-architecture-types] briefly discusses the different
architecture types a Wallet Providers may use for implementing a Wallet
Secure Cryptographic Device into their Wallet Solutions.
- [Section 4.6][46-state-diagrams] presents state diagrams for all of the main
entities and components in the EUDI Wallet ecosystem, discussing all of the
states a particular component can be in, as well as the conditions triggering
state transitions.
- [Section 4.7][47-possible-implementations-of-pseudonyms] discusses how pseudonyms can be implemented and used within a Wallet Unit.

### 4.2 Design principles

To effectively translate the [European Digital Identity Regulation] into a
User-friendly, privacy-focused, and secure technical architecture, establishing
design principles is crucial. These principles, rooted in the regulatory
framework and enriched by industry best practices, will serve as fundamental
guidelines. This approach ensures compliance with requirements emphasising
User-centricity, accessibility, privacy, security, and cross-border
interoperability. It demonstrates a commitment to both regulatory alignment and
excellence in the EUDI Wallet architecture's design.

#### 4.2.1 User-centricity

The EUDI Wallet ecosystem prioritises User-centricity as a core design
principle. This means placing User needs and experience at the forefront of
every design decision. The Wallet Unit should be intuitive and easy to use, with
seamless integration into existing use cases. Wallet Units make it easy for
Users to exercise their legal rights to full control over their attributes and
privacy, with transparent information about what attributes are being presented
and to whom. Additionally, the Wallet Unit should be accessible and inclusive,
catering to Users with varying technical backgrounds and abilities. By
prioritising User-centricity, the EUDI Wallet ecosystem fosters trust and
encourages widespread adoption, ultimately achieving its goal of empowering
Users with secure and convenient digital identity management.

#### 4.2.2 Accessibility

Regarding the accessibility of Wallet Units for Users, it is essential to ensure
that Wallet Units are inclusive by design and fully aligned with the
applicable European legal and technical frameworks on accessibility. The same
applies to any other User-facing component of the EUDI Wallet ecosystem, such as
websites and User authentication methods of PID Providers and Attestation
Providers, registries (see [Section 3.17][317-registrars]), et cetera. This is
not only a matter of legal compliance but also a fundamental component of
ensuring equal access, User trust, and widespread adoption across all segments
of the population, including persons with disabilities.

For more information, please refer to [Chapter 8][8-accessibility].

#### 4.2.3 Interoperability

The EUDI Wallet ecosystem prioritises interoperability as a core design
principle. This ensures a Wallet Unit functions seamlessly across borders within
the EU. Users can travel freely and confidently utilise their digital identity
wallets for various services, from e-government platforms to private online
interactions. Interoperability fosters secure data exchange through standardised
protocols, allowing trusted entities to verify credentials effortlessly. This
not only simplifies the User experience but also strengthens overall security
within the system. Moreover, interoperability prevents market fragmentation by
creating a level playing field for different Wallet Solutions. It fosters
competition and collaboration, ultimately driving innovation in the EUDI Wallet
ecosystem. By prioritising interoperability, the EUDI Wallet architecture lays
the foundation for a trusted and universally accepted EUDI Wallet ecosystem
across the EU.

#### 4.2.4 Privacy by design

The EUDI Wallet architecture embodies the principle of privacy by design. This
means that the protection of User data is a fundamental pillar of the
architecture's design. The principle of data minimisation guides the collection
of personal information, ensuring that Relying Parties gather only the
attributes they need and have registered for. By enabling selective disclosure
of attributes, the Wallet Unit empowers Users with granular control over what
data is presented and to whom. Transparency is built into the system, with clear
explanations of how data is used and protected. By making privacy a cornerstone
from the beginning, the EUDI Wallet ecosystem aims to foster trust and protect
the fundamental rights of its Users. Finally, measures are taken to prevent
Users from being tracked by Relying Parties, PID Providers, or Attestation
Providers.

For more information, please refer to [Sections 7.4.3.4][7434-risks-and-mitigation-measures-related-to-authorisation]
and [7.4.3.5][7435-risks-and-mitigation-measures-related-to-user-privacy].

#### 4.2.5 Security by design

The EUDI Wallet architecture embraces the principle of security by design. This
means security considerations are woven into the very fabric of the
architecture's design. Throughout the design process, potential vulnerabilities
are identified and mitigated. Secure coding practices are mandated, and the
architecture itself minimises attack surfaces by compartmentalising sensitive
data and access controls. By prioritising security from the outset, the EUDI
Wallet architecture aims to be inherently resistant to cyberattacks and data
breaches, fostering trust and User confidence in this EUDI Wallet ecosystem.

For more information, please refer to [Sections 7.4.3.2][7432-risks-and-mitigation-measures-related-to-confidentiality-integrity-and-authenticity]
and [7.4.3.3][7433-risks-and-mitigation-measures-related-to-tampering-of-cryptographic-keys-and-sensitive-data].

### 4.3 Reference architecture

#### 4.3.1 Overview

The figure below gives an overview of the architecture of the EUDI Wallet
ecosystem and its components. In comparison to [Figure 1][roles-introduction],
this figure presents more detail on the composition of a Wallet Unit and its
interfaces to other entities. The depicted components of a Wallet Unit are
described in [Section 4.3.2][432-components-of-a-wallet-unit],
while the interfaces are described in [Section 4.3.3][433-wallet-unit-interfaces-and-protocols].
The other entities shown in the figure were already described in [Chapter 3][3-roles-within-the-eudi-wallet-ecosystem].

![Figure 2](https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/media/Figure_2_High-Level_Architecture.png)

```mermaid
classDiagram
  class WalletUnit {
  }
  class UserDevice {
  }
  class WalletSecurenbspCryptographicApplicationWSCA {
  }
  class WalletInstance {
  }
  class RelyingPartyInstancenbsporVerifierWalletUnit {
  }
  class PIDProviders {
  }
  class UserInterface {
  }
  class User {
  }
  class WalletUnitService {
  }
  class AttestationProviders {
  }
  class QESRCProviders {
  }
  class AuthenticSources {
  }
  class TrustedServiceApp {
  }
  class JavaCardApplet {
  }
  class JavaCardApplet {
  }
  class OS {
  }
  class WalletSecurenbspCryptographicDeviceWSCD {
  }
  class Remote {
  }
  class Localexternal {
  }
  class Localinternal {
  }
  class Localnative {
  }
  class Keystore {
  }
  class QSCD {
  }
  class Optionalcomponent {
  }
  class Mandatorycomponent {
  }
  class WalletProviderBackend {
  }
  _2 ..> UserInterface : &nbsp; UI&nbsp;&nbsp;
  _20 ..|> WalletUnit : Issue KAs & WIAs. <br/>Support & Maintenance.
  WalletInstance --|> RelyingPartyInstancenbsporVerifierWalletUnit : Presentation<br/>(ISO/IEC 18013-5,<br/>OpenID4VP,<br/>ISO/IEC 18013-7)
  AuthenticSources ..|> AttestationProviders : Verification
  AttestationProviders --|> WalletInstance : (Q)EAA<br/>Issuance<br/>Interface<br/>(OpenID4VCI)
  PIDProviders --|> WalletInstance : PID<br/>Issuance<br/> Interface<br/>(OpenID4VCI)
  QESRCProviders --|> WalletInstance : QES <br/>Remote<br/>Signing<br/>Interface
  TrustedServiceApp ..|> Remote
  WalletUnit --> WalletUnit
  WalletUnit ..|> WalletUnit : Secure Cryptographic Interface
  JavaCardApplet ..|> Localexternal
  JavaCardApplet ..|> Localinternal
  OS ..|> Localnative
  WalletInstance ..|> WalletUnit
  WalletUnit ..|> QSCD
  WalletUnitService ..|> WalletUnit
```
*Figure 2: EUDI Wallet ecosystem reference architecture*

Figure 2 shows the high-level components and interfaces of the EUDI Wallet
ecosystem. The **Wallet Unit** is shown interacting with external entities through standardized
protocols for its entire lifecycle. The components of the Wallet Unit are
detailed in [Section 4.3.2][432-components-of-a-wallet-unit].

#### 4.3.2 Components of a Wallet Unit

The following have been identified as the core components of a Wallet Unit:

- **User device**: A User Device comprises the hardware, operating system,
and software environment required to host and execute the Wallet Instance. The
minimum hardware and software requirements for the User device will be
determined by the Wallet Provider.

- **Wallet Instance**: The app or application installed on a User device,
which is an instance of the corresponding software that is part of the Wallet Solution and belongs to and is controlled by a
User. This component implements the core business logic and interfaces as
depicted in Figure 2. It directly interacts with the WSCA (which is interacting
with the WSCD, see bullets hereafter) to securely manage critical assets and
execute cryptographic functions. It optionally interfaces with one or more keystores for
the management of non-critical cryptographic assets. Regarding the possible implementations of a Wallet Instance, please note the following:

    - The wordings used above and in the remainder of this and the following sections assume that a Wallet Instance is an app installed on a User device. However, a Wallet Instance can also be a web application. If this is the case, instead of opening the app, the User would log in to their web wallet using the browser on their User device. In such an architecture, typically no data is stored locally. Apart from UI aspects and short-range interfaces, all functions of the Wallet Unit are executed by the Wallet Unit Service running on the Wallet Provider backend depicted in Figure 2 and briefly discussed in the next section. Also, this implies that the WSCD will be a remote HSM, as discussed in [Section 4.5.2][452-remote-wscd]. All requirements in the ARF are applicable regardless of whether the Wallet Instance is a mobile app or a web app, except where explicitly indicated.
    - Similarly, the [European Digital Identity Regulation] does not exclude the possibility that a Wallet Instance may be installed on a non-mobile device, for example a server. The requirements in this ARF also apply for the installation of a Wallet Unit on a User device that is not a mobile device.
    - A User device can host more than one Wallet Instance, either provided by multiple Wallet Providers or by the same one, if supported by that Wallet Provider. If a User device hosts multiple Wallet Instances, it is part of multiple Wallet Units. In such a case, all requirements in this ARF for a single Wallet Unit and its components apply to each one independently.
    - The exact functionalities of the Wallet Instance depend on whether the Wallet Provider chooses to use a Wallet Unit Service (running on the Wallet Provider backend) as part of the Wallet Unit, see below. If a Wallet Unit Service is present, some tasks and responsibilities will be divided between the Wallet Instance and the Wallet Unit Service.

- **Wallet Secure Cryptographic Device (WSCD)**: A tamper-resistant device that
provides an environment that is linked to and used by the Wallet Secure
Cryptographic Application (WSCA) to protect critical assets and to securely
execute cryptographic functions. This includes a hardware-backed repository for storing and managing cryptographic keys and other critical assets, but also the
environment where related security-critical functions are executed. The WSCD is
tamper-proof and duplication-proof. In fact, [CIR 2024/2981], Annex IV, section
2 (3) states "As a prerequisite to the certification under national
certification schemes, the WSCD shall be assessed against the requirements of
assurance level high as set out in Implementing Regulation (EU) 2015/1502".
Therefore, a WSCD by legal definition complies with requirements of LoA High.
One WSCD may be a part of multiple Wallet Units, e.g. in case of a remote HSM.
The WSCD consists of two parts: the WSCD hardware covers the hardware issued by
the WSCD vendor and the WSCD firmware covers security-related software, such as
an operating system and cryptographic libraries provided by the WSCD vendor.
Figure 2 shows four different possible security architectures for the WSCD (for
more details see [Section 4.5][45-wscd-architecture-types]):
    - a remote WSCD, which is a remote device, such as a Hardware Security
    Module (HSM), accessed over a network.
    - a local external WSCD, which is an external device, such as a smart card issued
    to the User specifically for this purpose,
    - a local internal WSCD, which is a component within the User device, such
    as a SIM, e-SIM, or embedded Secure Element,
    - a local native WSCD, which is a component embedded in the User device and
    accessed via an API provided by the operating system.

- **Wallet Secure Cryptographic Application (WSCA)**: an application that
manages critical assets by being linked to and using the cryptographic and
non-cryptographic functions provided by the Wallet Secure Cryptographic Device.
Different types of WSCD generally use different types of WSCA. For example, if
the WSCD is a remote HSM, the WSCA may be (but does not have to be) a dedicated
firmware module. If the WSCD is a external smartcard or an internal e-SIM or
embedded Secure Element, the WSCA takes the form of a dedicated Java Card applet
running on the smart card, e-SIM, or SE. If the WSCD is a local native WSCD, the
WSCA is integrated into the OS of the User device. In all cases, the WSCA
interfaces directly with the Wallet Instance. For more details see [Section 4.5][45-wscd-architecture-types]. Note that the WSCA is dedicated firmware and/or software implementing specific functions needed within the EUDI Wallet ecosystem. A WSCD may offer additional functionalities through native firmware or software, for generic purposes. A good example of this is that some WSCDs will offer functionalities for synchronising (backing up and restoring) private keys, for instance to enable the creation of fallback or load balancing systems. However, within the scope of the EUDI Wallet ecosystem, private key export is not necessary and therefore it is not supported by a WSCA.

- **Keystore**: In addition to a WSCA/WSCD, a Wallet Unit may also have
available one or more other keystores. A keystore is a hardware-backed
repository and service in which non-critical cryptographic assets are generated,
stored, and used exclusively inside a dedicated hardware security boundary.
Examples of a keystore include a Secure Element, a TPM, TEE, or secure enclave,
or a remote HSM. Depending on its implementation, a keystore is associated with
a certain level of security, classified, for example, according to [ISO/IEC 18045]; see also [OpenID4VCI] Appendix D.2.
A keystore cannot be used for PID private keys, since these must be managed on
Level of Assurance High, which can only be done using a WSCA/WSCD. See [Section 2.2][22-identification-and-authentication]
for the distinction between 'Level of Assurance' and 'level of security'.

- **Local QSCD**: The Wallet Unit may contain a local QSCD. In principle, a
local QSCD can be the same component as the WSCD. Or, to put it differently,
a single component can implement both the QSCD and the WSCD functionality.
However, in such case that component must be certified both as QSCD and as WSCD.
Alternatively, a local QSCD can also be a separate component, for example a
dedicated smart card, that is connected to the Wallet Unit. If a local QSCD is
available to the Wallet Unit, it is provided by the Wallet Provider, and the
Wallet Provider is responsible for ensuring the correct functioning of the
Wallet Instance and the local QSCD when creating a signature.

- **Wallet Provider backend**: The Wallet Provider backend offers Users support
with their Wallet Units, performs essential maintenance, and issues Wallet Unit
Attestations and Wallet Instance Attestations to the Wallet Unit. Maintenance provided by the
Wallet Provider is discussed in more detail in the [discussion paper for Topic
T](../discussion-topics/t-support-and-maintenance-by-the-wallet-provider.md) and
in [Section
6.5.3.2][6532-wallet-provider-requests-data-about-the-users-device-from-the-wallet-instance].
High-level requirements are in included in [Topic
56](../annexes/annex-2/annex-2.02-high-level-requirements-by-topic.md#a2334-topic-56-wallet-provider-support-and-maintenance)
in Annex 2.

- **Wallet Unit Service**: Depending on the implementation chosen by the Wallet Provider, some parts of a Wallet Unit may run on the Wallet Provider backend rather than being part of the Wallet Instance. These parts are called the Wallet Unit Service. If a Wallet Unit Service is present, some tasks and responsibilities will be divided between the Wallet Instance and the Wallet Unit Service.

#### 4.3.3 Wallet Unit interfaces and protocols

Figure 2 shows the following interfaces between components of a Wallet Unit, or
between the Wallet Unit and other entities in the EUDI Wallet ecosystem:

- The **Wallet Provider Interface** is used by the Wallet Instance to
communicate with the Wallet Provider to request and issue Wallet Unit
Attestations and Wallet Instance Attestations, as well as to provide support to the User and collect aggregated
and User-consented information in a privacy-preserving manner to provision the
Wallet Unit, in compliance with applicable legislation. Because the Wallet
Provider is responsible for both sides of this interface, it will not be
standardised in the scope of the EUDI Wallet ecosystem. Moreover, the exact location of this interface may depend on the implementation of the Wallet Unit. If management of KAs and WIAs by the Wallet Unit is implemented within a Wallet Unit Service, then part of the Wallet Provider Interface will be internal to the Wallet Provider backend. This is depicted in Figure 2.

- The **User Interface** is the point of interaction and communication
between the User and the Wallet Instance. This interface will not be
standardised in the scope of the EUDI Wallet ecosystem.

- The **Presentation Interface** enables Relying Party Instances to securely
request and receive PIDs, QEAAs, PuB-EAAs, and EAAs from Wallet Units. This
interface accommodates both remote and proximity interactions.  

  For proximity presentation flows to a Relying Party Instance, the Wallet Instance implements the the protocol specified in [ISO/IEC 18013-5], see [Section 5.7.2][572-proximity-attestation-presentation-using-isoiec-18013-5]. This interface can, with some extensions, also be used by a Wallet Unit to request User attributes from another Wallet Unit, see [Section 6.6.4][664-pid-or-attestation-presentation-to-another-wallet-unit].

  For remote presentation flows to a Relying Party Instance, the Wallet Instance implements the following (see [Sections 5.7.3][573-remote-attestation-presentation-using-isoiec-18013-7] and [5.7.4][574-remote-attestation-presentation-using-openid4vp-and-haip]):

    - the protocol specified in [OpenID4VP] in combination with a custom URI scheme,
    - the [OpenID4VP] protocol in combination with the [W3C Digital Credentials API],
    - the protocol specified in [ISO/IEC 18013-7], in combination with the [W3C Digital Credentials API],
    - optionally, the [ISO/IEC 18013-7] protocol in combination with a custom URI scheme.
  
  Proximity presentation flows are discussed in [Section 4.4.2][442-proximity-presentation-flows]. Remote presentation flows, including the role of URI schemes and the [W3C Digital Credentials API], are discussed in [Section 4.4.3][443-remote-presentation-transaction-flows].

- The **Secure Cryptographic Interface** enables the Wallet Unit to
communicate with the Wallet Secure Cryptographic Application (WSCA). This
interface is specifically designed for managing cryptographic assets and
executing cryptographic functions. In case the WSCA is delivered by the Wallet
Provider, the Wallet Provider is responsible for both sides of this interface,
and hence standardisation is not needed within the scope of the EUDI Wallet
ecosystem. In case the WSCA is delivered by the provider of the WSCD, this
interface will comply with an existing specification that is not specifically
designed for the EUDI Wallet ecosystem. Rather, each type of WSCA/WSCD will
expose a provider-defined interface to the Wallet Units. For example, in case
the WSCD is a secure element, [CIR 2024/2979] requires support for the [GP
OMAPI] interface specification (or an equivalent one). To be able to support
different types of WSCA/WSCD, Wallet Units may therefore need to be able to
handle multiple flavours of this interface.

- The **WSCA - WSCD Interface** enables the WSCA to communicate with the
WSCD. This interface is not specifically designed for the EUDI Wallet ecosystem.
Rather, each type of WSCD will expose a manufacturer-defined interface to the
WSCA making use of it, for example syscalls of the operating system. In case the
WSCA is delivered by the Wallet Provider, the Wallet Provider is responsible for
correctly implementing this interface.

- The **PID Issuance Interface** complies with the [OpenID4VCI] standard (see [Section 5.8][58-protocols-and-transmission-mechanisms-for-attestation-issuance])
and is used when the Wallet Unit communicates with a PID Provider to request and
receive PIDs to be stored within the Wallet Unit. 
  > Note: In addition to supporting [OpenID4VCI], PID Providers are allowed to support other protocols for issuing PIDs to (national) Wallet Units, provided these protocols comply with all relevant requirements in the Implementing Acts and the standards referenced therein. In many Member States, the PID Provider and the Wallet Provider are closely related, and can therefore bilaterally agree to support a different protocol for PID issuance. 

- The **Attestation Issuance Interface** also complies with the
[OpenID4VCI] standard and is used by the Wallet Unit to request various
attestations that the User wants to include in their Wallet Unit.

- The **Remote Signing or Sealing Interface** facilitates communication
between the Wallet Unit and a Qualified Electronic Signature Remote
Creation (QESRC) Provider. This interface is used by the Wallet Unit to generate
a qualified electronic signature or seal.

*Note that the "Attribute Deletion Request to Relying Party Interface" and the
"Reporting Relying Party to DPA Interface", which are mentioned in the
Regulation, are not depicted as interfaces in Figure 2. Functionality enabling a
User to request a Relying Party to delete personal data (i.e., User attributes)
obtained from the User's Wallet Unit is seen as a feature of the Wallet
Solution. The same applies to functionalities enabling the User to report a
Relying Party to a Data Protection Authority.*
