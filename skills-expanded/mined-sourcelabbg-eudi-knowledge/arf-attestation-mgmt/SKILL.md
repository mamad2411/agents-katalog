---
name: "arf-attestation-mgmt"
description: "Use when implementing attestation presentation to other Wallet Units or intermediaries, attestation management (refresh, status checks), and attestation deletion."
sections:
  - "6.6.4 PID or attestation presentation to another Wallet Unit"
  - "6.6.4.1 Introduction"
  - "6.6.4.2 General transaction flow"
  - "6.6.5 PID or attestation presentation to an intermediary"
  - "6.6.6 PID or attestation management"
  - "6.6.6.1 Overview"
  - "6.6.6.2 PID or attestation re-issuance"
  - "6.6.6.3 Deletion of unusable technical PIDs or attestations"
  - "6.6.6.4 PID or attestation revocation"
  - "6.6.7 PID or attestation deletion"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~7550 -->

#### 6.6.4 PID or attestation presentation to another Wallet Unit

##### 6.6.4.1 Introduction

[Section 6.6.3][663-pid-or-attestation-presentation-to-a-relying-party] discussed
the trust relationships necessary when a Wallet Unit receives a request from a
Relying Party Instance and presents attributes to that Relying Party Instance.
However, the [European Digital Identity Regulation] requires that a Wallet Unit
is also able to receive such a request from another Wallet Unit, and present
attributes to that requesting Wallet Unit. In this context, the ARF calls the
requesting Wallet Unit the Verifier Wallet Unit, and the presenting Wallet Unit
the Holder Wallet Unit. The User of a Holder Wallet Unit is called a Holder, and
the User of a Verifier Wallet Unit is called a Verifier.

Wallet-to-Wallet interactions cover use cases where a natural person, the
Holder, wishes to present a PID or attestation to another natural person, the
Verifier, where both are using their Wallet Units. As an example, the use case
could occur in a setting where one private person (the Verifier) wants to rent
out their car to another private person (the Holder), provided the Holder has a
valid driving licence.

Note that legal entities are not allowed to bypass the processes and rules
governing Relying Parties, in particular regarding the obligation to register, by
using Wallet-to-Wallet interactions. Therefore,

- **Wallet-to-Wallet interactions will only take place in proximity, not
remotely.** This ensures that both Users are aware of the device they are
connecting to, because they have to present and scan a QR code or NFC tag. Being
in proximity also allows for out-of-band communication and authentication
possibilities between Holder and Verifier.
- **Wallet Units will be restricted in the number of times they can act as a
Verifier per unit of time.** Since many Relying Parties will need to have
frequent interactions with multiple Wallet Units, this ensures that it will not
be feasible for a Relying Party to use a Wallet Unit for all of these
interactions.
- **A User will need to select a dedicated 'Holder Wallet Unit' mode to start
using Wallet-to-Wallet interactions.** If this mode is selected, a Holder Wallet
Unit will clearly indicate to its User that they are presenting attributes to
another natural person, and that they should not proceed if they are in fact
interacting with a legal entity.

For more information and high-level requirements, please refer to
[Technical Specification 9](../technical-specifications/ts9-wallet-to-wallet-interactions.md)
and [Topic 30][topic-30].
The next section describes a Wallet-to-Wallet transaction flow on a high level.

##### 6.6.4.2 General transaction flow

Figure 15 shows the transaction flow for Wallet-to-Wallet interactions.

![Figure 15](https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/media/Figure_15_W2W_presentation.png)

```mermaid
sequenceDiagram
  participant H as Holder
  participant HU as HolderWallet Unit
  participant VU as Verifier&nbsp;Wallet Unit
  participant V as Verifier
  H->V: 1. Agree (out of band) on attributes to be presented
  HU->VU: 4. Device engagement QR code,&nbsp;including presentation offer (if any)
  HU->Q_9wWjG8hOZr_bmCtn9E_31: 8. Request approval forpresenting attributes
  Q_9wWjG8hOZr_bmCtn9E_31->HU: 9. Approval
  HU->VU: 10. Send response with&nbsp;approved attributes
  VU->V: 2. Select Verifier mode
  HU->HU: 7.Check if requested attributes are&nbsp;subset of presentation offer (if any)
  HU->H: 2. Select Holder mode
  VU->V: 5a. Show presentation offer
  V->VU: Select attributes to be requestedfrom presentation offer
  VU->V: 5b. Show predefined list of attributes
  V->VU: Select attributes to be requested
  HU->VU: 6. Send presentation request over BLE
  VU->VU: 11. Verify response & attributes
  VU->V: 12. Show attributes
```

Figure 15 Wallet-to-Wallet transaction flow

The transaction flow can be described as follows:

1. The two EUDI Wallet Users meet in physical proximity and agree that one (the Holder) will present specific attributes from a PID or attestation to the other (the Verifier). This agreement takes place out of band of the EUDI Wallet ecosystem; typically, it will be done orally.
2. Both Users select a dedicated 'Wallet-to-Wallet mode' in their respective
Wallet Unit and are asked to specify their role (Holder or Verifier).
1. The Holder Wallet Unit gives the Holder an option to suggest to the Verifier
which PID or attestation, and which attributes, the Verifier should request. This suggestion is called a presentation offer.
1. A handshake protocol (called device engagement in [ISO/IEC 18013-5]) is
performed and a data connection is established between the two devices as
specified [ISO/IEC 18013-5]. This protocol also sends the presentation offer to
the Verifier, if the User specified such an offer.
1. The Verifier tells the Verifier Wallet Unit what attributes
should be included in the presentation request:
   - If the Holder specified a presentation offer in step 3, the Verifier Wallet
   Unit displays the offer to the Verifier. The Verifier selects all or a subset
   of the offered attributes, but is not allowed to add additional attributes.
   - If there is no presentation offer in the handshake, the Verifier Wallet
   Unit assists the Verifier in creating a presentation request from scratch, by
   allowing the Verifier to select attributes from a pre-defined list populated
   by the Wallet Provider.
1. The Verifier Wallet Unit sends the presentation request to the Holder Wallet Unit.
2. The Holder Wallet Unit checks if the presentation request matches the
presentation offer created in step 3 (if any), and aborts the transaction in
case the request contains attributes that were not present in the offer. The
Holder Wallet Unit informs the Holder about the reason for aborting. If no
presentation offer was sent in step 4, then this check is omitted.
8. The Holder Wallet Unit prompts the Holder for approval to present the
requested attributes to the Verifier.
9. The Holder approves the presentation.
10. The Holder Wallet Unit sends a presentation to the Verifier Wallet Unit.
11. The Verifier Wallet Unit verifies the received presentation.
12. The Verifier Wallet Unit presents the received attributes to the
Verifier.

Notes:

- Step 2 ensures that both parties actively accept that a local data connection
towards a natural-person Wallet Unit will be established. For the Holder this
is very important, because many (if not all) of the verifications usually done on
a presentation request from a Relying Party will not be performed when a Wallet
Unit acts as a Holder Wallet Unit; see the note to step 6 below. For the
Verifier, this is necessary as well, since the functionality offered by a
Verifier Wallet Unit is completely different then when acting a 'normal' Wallet
Unit.
- In step 3, if the Holder wishes to let the Verifier specify the requested
information, the presentation offer is left empty. However, the use of a
presentation offer is recommended, as this increases the chance of success of
the use case.
- Step 4 establishes a local data connection. [ISO/IEC 18013-5] requires that an
mdoc reader (i.e., a Verifier Wallet Unit) must support both a QR code and NFC for
device engagement, and both BLE and NFC for data retrieval. An mdoc (i.e., a Holder Wallet Unit) then chooses to use either a QR code or NFC for device engagement, and either BLE or
NFC for data retrieval. The requirements regarding supported technologies are
therefore more stringent for an mdoc than for an mdoc reader. Depending on the device it's installed on and the technologies chosen by
the Holder, this may mean that a Wallet Unit is not able to act as a Verifier Wallet Unit. For example, if
a Holder Wallet Unit uses only NFC for device engagement, then a Wallet Unit on
a device that does not have NFC will be not be able to act as a Verifier Wallet Unit towards
that Holder Wallet Unit. [Technical Specification 9](../technical-specifications/ts9-wallet-to-wallet-interactions.md) therefore limits the choice offered by [ISO/IEC 18013-5] and stipulates that in Wallet-to-Wallet interactions, device engagement always uses a QR code and data retrieval always uses BLE. 
- In step 5, if the offered attributes do not fulfil the needs of the Verifier
for the use case, the Verifier may decide to stop the transaction and return to
step 1 to communicate (out of band) to the Holder which attributes the Holder
should offer.
- In step 5, if there is no presentation offer, the Verifier Wallet Unit will
present the Verifier with a list of 'frequently used' attributes to include in
the presentation request. Conceivably, the Verifier Wallet Unit may limit the
number of attributes in the list by asking the Verifier a set of pre-defined
questions about the purpose of the use case. However, there is no guarantee that
the Holder Wallet Unit contains these attributes. For the success of the use case, the presence of a presentation offer is very helpful.
- A user-friendly User interface is important in steps 3 and 5 (when Users select what
attributes to offer cq. request).
- In step 6, a presentation request from a Verifier Wallet Unit does not contain
an access certificate (see [Section 6.6.3.2][6632-wallet-unit-authenticates-the-relying-party-instance])
or a registration certificate (see [Section 6.6.3.3][6633-wallet-unit-verifies-that-relying-party-does-not-request-more-attributes-than-it-registered]).
The Holder therefore cannot be certain about the Verifier's identity, nor is
there any check regarding the Verifier's reasonable need to request these User
attributes. This is because a Verifier is a User, and is not required to
register as a Relying Party. Additionally, because there is no registration certificate in the presentation request, the Holder Wallet Unit is
not able to evaluate an embedded disclosure policy, if existing, see [Section 6.6.3.4][6634-wallet-unit-evaluates-embedded-disclosure-policy-if-present].
- However, the presentation request in step 6 will include a cryptographic proof that the Verifier Wallet Unit is a genuine, non-revoked EUDI Wallet Unit operated by a recognised Wallet Provider, once a common method to provide such a proof will be available. ETSI is preparing a technical specification of such a common method, which will probably use a WIA of the Verifier Wallet Unit. If such a proof is available in the request, the Holder Wallet Unit will verify it.
- In step 11, the Verifier Wallet Unit verifies the authenticity of the presented
PID or attestation in the same way a Relying Party Instance does, as specified in [Section 6.6.3.6][6636-relying-party-instance-verifies-the-authenticity-of-the-pid-or-attestation].
This implies that the Verifier Wallet Unit needs to obtain the trust anchors of
the relevant PID Provider or Attestation Provider from the respective Trusted
List or LoTE. Additionally, the Verifier Wallet Unit optionally also verifies the revocation status
of the presented PID or attestation as specified in [Section 6.6.3.7][6637-relying-party-verifies-that-the-pid-or-attestation-is-not-revoked].

#### 6.6.5 PID or attestation presentation to an intermediary

[Section 3.11.4][3114-intermediaries] introduced intermediaries, which are a special category of Relying Party. An intermediary interacts with a Wallet Unit to request User attributes on behalf of another (intermediated) Relying Party. The current section explains the interactions between the intermediated Relying Party, the intermediary, and the Wallet Unit in the course of such an interaction.

1. The intermediary registers once as a Relying Party with a Registrar (see
[Section 3.17][317-registrars]) and obtains one or more access certificate(s) (see
[Section 3.18][318-access-certificate-authorities]) bearing its own Relying Party identifier and trade name and Relying Party Service identifier and trade name. These access certificates are not different from an
access certificate issued to a 'normal' Relying Party, since an intermediary is,
as a matter of legal fact, a Relying Party. As explained in [Section 3.11.3][3113-relying-party-instances], an intermediary needs a separate access certificate for each of its Relying Party Instances.

    Moreover, according to the (amended) [CIR 2025/848], Annex IV, point 3(k), an access certificate for an intermediary contains "an association to the wallet-relying party that is relying upon the intermediary to whom the wallet-relying party access certificate has been issued and that is acting on behalf of the relying party who intends to rely upon the wallet." This implies that an intermediary receives a separate set of access certificates for each of its intermediated Relying Parties. For example, if an intermediary has 100 Relying Party Instances and 1000 customers (intermediated Relying Parties), it will need to request and manage 100.000 access certificates.

 
    In addition, the intermediary
receives one or more registration certificate (see [Section 3.19][319-providers-of-registration-certificates]). However, these registration
certificates will not be used in intermediated transactions.
1. Next, the intermediary tries to find customers, meaning Relying Parties that want to use the intermediary's services to connect to Wallet Units and request User attributes on their behalf. If Relying Parties signs up with them, the intermediary ensures that they are registered in the Member State where they are established; as described in [Section 6.4.2][642-relying-party-registration]. The intermediary also ensures that it receives a registration certificate for each of the registered intended uses of the intermediated Relying Party. Finally, the intermedia also registers the new intermediated Relying Party with its own Registrar, see the (amended) [CIR 2025/848], Annex I, point 16.

    Note that it is up to each Registrar to design a suitable process to achieve these goals. For example, it may decide an intermediary can register the intermediated Relying Parties at the Registrar, and receive the registration certificates in return. Alternatively, the Registrar could request the intermediated Relying Parties register themselves and indicate the intermediary they will be using, in which case they will receive the registration certificates and must send them to the intermediary. Alternative processes can be used as well.

    The registration certificates of the intermediated Relying Party show that it uses the services of the intermediary; both entities are identified by their unique Relying Party identifier and Service identifier. Before registering this relationship between an intermediary and an intermediated Relying Party and issuing a registration certificate attesting to this, a Registrar ensures it obtains legally valid evidence that this particular Relying Party will indeed use the services of this particular intermediary to interact with Wallet Units. A Registrar is free to decide which evidence it needs and how it obtains this evidence. For example, the Registrar could require either the intermediary or the Relying Party to provide a signed copy of the contract between both parties. Alternatively, the Registrar could ask an authorised representative of the Relying Party to sign off on a registration that was done by the intermediary, or could ask for a legally valid mandate from the intermediated Relying Party to the intermediary to register the Relying Party.
1. When asked by an intermediated Relying Party, the intermediary will request a
presentation of attributes from a Wallet Unit, using one of the flows described
in [Section 4.4][44-data-presentation-flows]. For this, the intermediary will
use its own access certificate (containing the association to the intermediated Relying Party, see point 1. above) and the registration
certificate of the intermediated Relying Party (point 2. above).
1. If the Wallet Unit sees in the registration certificate that the Relying Party uses
the services of an intermediary, it verifies that the identifier and Service identifier of the intermediary listed in the `usesIntermediary` field of the
registration certificate are identical to the identifier and Service identifier listed in the access
certificate. If this verification is not
successful, the Wallet Unit informs the User and, depending on the Wallet Provider's security policy, may stop the transaction. If the verification is successful, the Wallet Unit displays only the trade name of the intermediated Relying Party, together with the trade names of its Service, to the User when asking for User approval to present the requested attributes.
    >Note: The Wallet Unit does not display the trade names of the intermediary and its Service to the User, because the intermediary operates on behalf of the intermediated Relying Party and is not a party in the use case taking place between the User and the Relying Party. The User would probably not expect or recognise the name of the intermediary or its Service, and may be confused if the Wallet Unit would show these names. However, the intermediary name and service are logged by the Wallet Unit, see [Section 6.6.3.13][66313-wallet-unit-enables-the-user-to-report-suspicious-requests-by-a-relying-party-and-to-request-a-relying-party-to-erase-personal-data], so the fact that an intermediary was used in the transaction is visible to the User.  
1. When a Wallet Unit presents a PID or attestation to the intermediary, the
intermediary carries out the verifications described in [Section 6.6.3][663-pid-or-attestation-presentation-to-a-relying-party], if the intermediary has agreed to do
so with the intermediated Relying Party. This means it may verify the authenticity of the PID or attestation, its revocation
status, device binding (if expected), and User binding, as well as any combined
presentation of attributes, if applicable. Note that a Relying
Party is not obliged to carry out all of these verifications. Therefore, the
intermediary and any Relying Party using its services must agree on what
verifications the intermediary will carry out.
1. If these verifications are successful, the intermediary forwards the User
attributes it obtained from the Wallet Unit to the intermediated Relying Party.
There must be an interface between an intermediary and a Relying Party, over
which the intermediated Relying Party can request the intermediary to request
some User attributes from a Wallet Unit and that the intermediary uses to send
back the attribute values presented by the Wallet Unit. However, specifying this
interface or the (security) requirements with which it needs to comply, is out
of scope of the ARF. In particular, it is not required that the User attributes
are end-to-end encrypted between the Wallet Unit and the intermediated Relying
Party, such that an intermediary would not be able to see them.
1. The intermediary deletes any PIDs or attestations it obtained from the Wallet
Unit, including any User attributes, immediately after it has sent the User
attributes to the Relying Party. If the intermediary does not send any User
attributes to the Relying Party, for example because one of the verifications in
the previous step failed, the intermediary deletes the PIDs or attestations
immediately after it has completed all necessary verifications.

Note that this approach implies that an intermediated Relying Party using the
services of an intermediary will not need an access certificate.

For high-level requirements on intermediaries, see [Topic 52][topic-52].

#### 6.6.6 PID or attestation management

##### 6.6.6.1 Overview

Starting from the issuance of a logical PID or attestation, the PID or attestation is
managed by the User and the PID Provider or Attestation Provider. Management is performed until the PID or attestation is deleted by the User (see [Section 6.6.7][667-pid-or-attestation-deletion]) or the Wallet Instance is uninstalled by the User (see [Section 6.5.5][655-wallet-instance-uninstallation]). Management includes at least the following processes:

1. Re-issuance of technical PIDs or attestations when necessary.
2. Deletion of an unusable technical PID or attestation, typically after it has been
replaced in a re-issuance process.
3. Revocation of the PID or attestation when necessary.

These processes are discussed in the next subsections.

##### 6.6.6.2 PID or attestation re-issuance

###### 6.6.6.2.1 Introduction

Re-issuance means the replacement of a technical PID or attestation that already exists in
a Wallet Unit by a technical PID or attestation having the same attestation type. Moreover, the existing and the new technical PID or attestation represent the same logical PID or attestation, see [Section 5.3][53-logical-versus-technical-pids-and-attestations].Re-issuance is therefore always performed by the same PID Provider or Attestation Provider
that issued the existing PID or attestation. Re-issuance is always initiated by the Wallet
Unit, although the User may prompt the Wallet Unit to start the process, and the PID Provider or Attestation Provider may tell the User that re-issuance is necessary.

The value of the attributes in the new PID or attestation will typically be the
same as in the original PID or attestation. However, this is not required; the PID
Provider or Attestation Provider may change one or more attribute values, and this may actually be the reason for re-issuance.

Note that, in general, if the logical PID or attestation was originally issued in the form of a batch of technical PIDs or attestations, then the PID Provider or Attestation Provider will re-issue a batch of technical PIDs or attestations as well.

Re-issuance is only applied within the administrative validity period of a logical PID or attestation, if applicable. As an example, a mobile driving licence (mDL) will be issued
in the form of technical attestations which typically have a technical validity period shorter than
the administrative validity period of the licence itself. Re-issuance is used
for obtaining fresh technical attestations as needed during the administrative validity
period, to ensure that the User can always present a valid mDL. When the
administrative validity period ends, there will be an administrative process for
obtaining a new driving licence, which is however out of scope of this document. Note that not all logical PIDs and attestations have an administrative validity period. For example, a diploma often has no expiry date, nor will a voucher (since it will typically be usable only once).

There may be different reasons for re-issuing a PID or attestation, for example:

- The current technical PID(s) or attestation(s) are near the end of their
 technical validity period, or the Wallet Unit is running out of once-only
 attestations. A short technical validity period or a requirement that an attestation can be presented only once are used to mitigate the risk of Relying Party linkability.
 For more information, see [Section 7.4.3.5][7435-risks-and-mitigation-measures-related-to-user-privacy].
- The value of one or more of the attributes in the logical PID or attestation
 has changed.
- The security architecture of the Wallet Solution uses PIDs and/or
 attestations that are issued just-in-time, at the moment that PID or
 attestation is being requested by a Relying Party. This is sometimes
 called synchronous issuing.

These reasons are discussed in the next subsections. Re-issuance is discussed in
more detail in the [Discussion Paper for Topic B](../discussion-topics/b-re-issuance-and-batch-issuance-of-pids-and-attestations.md).

###### 6.6.6.2.2 Re-issuance to limit Relying Party linkability

As specified in [ISO/IEC 18013-5] or [SD-JWT VC], each technical PID or
attestation contains metadata indicating its technical validity period.
Determining the length of the technical validity period is the responsibility of
the PID Provider or the Attestation Provider. The
technical validity period chosen by the PID Provider or Attestation Provider will
depend on several factors, primarily the security architecture of the
Wallet Solution and the strategy chosen to mitigate Relying Party
linkability, see [Section 7.4.3.5][7435-risks-and-mitigation-measures-related-to-user-privacy].

Given the above factors, it can generally be assumed that the technical validity
period of a PID or attestations will be much shorter than the lifetime of the corresponding logical PID or attestation,
meaning the period of time that a User wants to keep that PID or attestation in
their Wallet Unit. That implies that new technical PIDs and attestations will need to be
re-issued periodically, to replace the ones that are reaching end of their
technical validity.

A similar reason for re-issuing PIDs and attestations occurs when the
PID Provider or Attestation Provider uses once-only attestations (see [Section 7.4.3.5][7435-risks-and-mitigation-measures-related-to-user-privacy]),
which can be presented only once to a Relying Party. In that case, the Wallet
Unit, or rather the User, will regularly need new technical PIDs or attestations to avoid
running out and to remain able to use the logical PID or attestation.

Re-issuance of PIDs or attestations for these reasons is a purely technical
matter. To the maximum extent possible, the User does not notice that new technical
attestations have been issued for their logical PID or attestation, nor do they have to take any action to ensure
that re-issuance happens in time. These conditions are very different from a
first-time issuance of a PID or attestation, where the User must take the
initiative to request the PID or attestation, and is potentially involved in the
process in other ways as well.

This implies, among other, that no User authentication takes place during
re-issuance for an existing logical PID or attestation. Nevertheless, a Wallet Unit may offer
the User the option to receive a notification of re-issuance.

In the absence of User authentication, and to prevent that a re-issued technical PID or
attestation ends up at the wrong User, the PID Provider or Attestation Provider
ensures that a re-issued PID or attestation is issued to same Wallet
Unit as the technical PID or attestation it replaces. This can be done by
the use of device-bound refresh tokens, see [OpenID4VCI].

Finally, since the User is not involved, it is the Wallet Unit itself that triggers the
re-issuance of PIDs and attestations when necessary.

###### 6.6.6.2.3 Re-issuance because of a change of attribute values

During the lifetime of a logical PID or attestation, the value of some of the attributes
may change. For example, at the date of birth of the User, an age attestation
attribute (i.e., an attribute indicating whether the User has reached a certain
age) may have to be changed from value False to value True. In another example,
the User of a mobile driving licence may have passed the examination for a
different vehicle category. In this case, the PID Provider or Attestation
Provider re-issues technical PID(s) or attestation(s) with the correct attribute
values, and revokes the existing technical attestation(s).

Re-issuance of a PID or attestation for this reason will have an impact on the
User, because they will notice that their attribute values have been changed.
Therefore, in this case Users will be informed when re-issuance happens.
Additionally, an Attestation Provider may state in their terms of conditions
that re-issuance of an attestation may be used.

###### 6.6.6.2.4 Re-issuance when using synchronous issuing

A third reason for re-issuing a technical PID or attestation is where the PID Provider or
Attestation Provider uses synchronous issuing in their security architecture. In
such an architecture, the Wallet Unit requests the re-issuance of a new technical PID or
attestation **after** it has received a request for presentation of the corresponding logical PID or attestation from a
Relying Party. Such a technical PID or attestation is very short-lived and is used only
once.

The conditions on User awareness and authentication discussed in [Section 6.6.6.2.2][66622-re-issuance-to-limit-relying-party-linkability]
are also valid for a synchronous re-issuance process.

##### 6.6.6.3 Deletion of unusable technical PIDs or attestations

Some time after it is issued, a technical PID or attestation will become unusable, in the
sense that the User cannot present it any longer to a Relying Party. For
example, it expires, or a once-only PID or attestation (see
[Section 7.4.3.5][7435-risks-and-mitigation-measures-related-to-user-privacy])
has been presented to a Relying Party already. Typically (but not always), such a technical PID
or attestation will already have been replaced in a re-issuance process as
described in [Section 6.6.6.2.2][66622-re-issuance-to-limit-relying-party-linkability].

Wallet Providers need to decide what to do with unusable technical PIDs or attestations.
Non-device-bound attestation can be simply deleted, but for PIDs and
device-bound attestations this is more complicated, as the Wallet Provider needs
to manage the associated private keys in the WSCA/WSCD or keystore of the Wallet
Unit. Typically, the amount of storage space available in a WSCA/WSCD or
keystore is limited, and Wallet Providers will want to delete these keys to
prevent an accumulation of unused private keys. Deletion of cryptographic assets
in the WSCA/WSCD in particular is a cryptographic key operation and cannot be
done without User authentication by the WSCA/WSCD; see [Section 6.5.3.3][6533-wallet-unit-requests-user-to-set-up-two-user-authentication-mechanisms].
At the same time, for usability reasons the User should not be involved in such
'cleaning up' processes, just like the User does not have to take any action for
re-issuance processes ([Section 6.6.6.2.2][66622-re-issuance-to-limit-relying-party-linkability]).

The recommended solution for this challenge is to ensure that, whenever the
WSCA/WSCD successfully authenticates the User, the Wallet Unit checks if there
are any technical PIDs or device-bound attestations that cannot be presented any longer to
Relying Parties. The Wallet Unit then requests the WSCA/WSCD to destroy all
cryptographic key material in the WSCA/WSCD related to these PIDs or
attestations. Thus, the Wallet Unit takes advantage of the fact that the User
authenticates for another purpose, for example because they want to present a
PID, to also carry out any necessary key deletion operations. A last aspect of this to be mentioned here is that the Wallet Unit will not delete the last technical PID or attestation corresponding to a logical PID or attestation, even when it is no longer usable. This is because that would mean the corresponding logical PID or attestation is deleted from the Wallet Unit. Instead, the Wallet Unit keeps such a last technical PID or attestation and keeps trying to trigger the re-issuance of new ones. See also [Topic 40][topic-40]
in Annex 2.

##### 6.6.6.4 PID or attestation revocation

PID or attestation management includes ensuring that PIDs and attestations can
be revoked if necessary. The User can request the PID Provider or Attestation Provider to revoke the logical PID
or attestation at least in case of loss or theft. The PID Provider or
Attestation Provider can also decide itself to revoke a logical PID or attestation, for example
in case the Wallet Unit on which the associated technical PIDs or attestations are residing is revoked;
see [Section 6.5.3.4][6534-wallet-provider-issues-one-or-more-key-attestations-to-the-wallet-unit], or for any other valid reason outside the scope of the EUDI Wallet ecosystem.

Revoking a logical PID or attestation implies that all technical PIDs or attestations associated with that logical PID or attestation will be revoked if they are still valid for more than 24 hours. Revocation of technical PIDs and attestations is discussed in
[Topic 7][topic-7].

In addition to revoking a technical PID or attestation, a PID Provider or Attestation Provider can revoke the certificate that it used for signing that PID or attestation, or any intermediate certificate between that signing certificate and the corresponding trust anchor. In all of these cases, a Relying Party that performs revocation checking will not accept the technical PID or attestation.

#### 6.6.7 PID or attestation deletion

In case the User no longer wants to retain a specific logical PID or attestation in
their Wallet Unit, the User can delete it. If the PID Provider or Attestation
Provider issued a batch of multiple technical PIDs or attestations corresponding to the logical attestation, the Wallet Unit deletes them all. Deleting a technical PID or a
device-bound attestation also means that the WSCA/WSCD or keystore destroys the
cryptographic key material associated with that PID or attestation. Before
deleting critical assets of a PID, the WSCA/WSCD included in the Wallet Unit
will authenticate the User.

The Wallet Unit also discloses the fact that it no longer contains the PID or
attestation to the [W3C Digital Credentials API] framework, see [Section 4.4.3][443-remote-presentation-transaction-flows].

For high-level requirements on this topic, see [Topic 51][topic-51].
