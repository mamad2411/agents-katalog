---
name: "arf-rp-verification"
description: "Use when implementing RP-side verification during attestation presentation: authenticity checks, revocation verification, device binding, user binding, combined presentation, and suspicious request reporting."
sections:
  - "6.6.3.6 Relying Party Instance verifies the authenticity of the PID or attestation"
  - "6.6.3.7 Relying Party verifies that the PID or attestation is not revoked"
  - "6.6.3.8 Relying Party Instance verifies device binding"
  - "6.6.3.9 Relying Party Instance verifies or trusts User binding"
  - "6.6.3.10 Relying Party Instance verifies combined presentation of attributes"
  - "6.6.3.10.1 Introduction"
  - "6.6.3.10.2 Cryptographic binding between attestations"
  - "6.6.3.11 Relying Party Instance trusts issuer to have authenticated the Wallet Unit and the Wallet Provider"
  - "6.6.3.12 Relying Party optionally trusts issuer to regularly verify that Wallet Unit is not revoked"
  - "6.6.3.13 Wallet Unit enables the User to report suspicious requests by a Relying Party and to request a Relying Party to erase personal data"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~5653 -->

##### 6.6.3.6 Relying Party Instance verifies the authenticity of the PID or attestation

The Relying Party Instance receives a PID or attestation, including some
attributes, from the Wallet Unit. Subsequently, it verifies the signature over
the PID or attestation. To do this for PIDs, QEAAs, and PuB-EAAs, the Relying Party
Instance uses a trust anchor of the Provider obtained from a LoTE or Trusted List. Note
that the Provider may use an intermediate signing
certificate to sign the PID or attestation, and use the trust anchor to sign the
signing certificate, instead of signing the PID or attestation directly with the
trust anchor.

For non-qualified EAAs, the applicable Rulebook may describe how the
Relying Party Instance obtains the relevant trust anchor.

The above implies that a Relying Party Instance is aware whether the attestation
it is requesting from a Wallet Instance is a PID, a QEAA, a PuB-EAA, or a
non-qualified EAA. Also, the Relying Party Instance stores trust anchors in such
a way that, at the time of verification, it is able to distinguish between trust
anchors usable either for PIDs, for QEAAs, for PuB-EAAs, or for non-qualified
EAAs.

A Relying Party performs regular trust anchor management. It downloads the latest version of all applicable Trusted Lists and LoTEs. If if finds that new trusted entities have been added, or that new trust anchors have been added for existing trusted entities, it ensures that these trust anchors are properly stored in all relevant Relying Party Instances. Conversely, if the Relying Party finds that an existing trusted entity has been invalidated in the Trusted List or LoTE, or that some of the trust anchors of existing trusted entities have expired, been revoked, or otherwise been invalidated, it ensures that these trust anchors are removed from all Relying Party Instances. 

The technical implementation of the signature verification process depends on
which of the standards mentioned in [Topic 12][topic-12]
is supported by the Wallet Unit. Each of these standards specifies in detail
how to carry out signature verification.

In addition, the Relying Party may want to verify that the Attestation Provider
is registered to issue the type of attestation in question, as described in
[Section 6.3.2.3][6323-pid-provider-or-attestation-provider-receives-access-certificates-and-registration-certificates].

Notes:

- All PIDs and attestations in the EUDI Wallet ecosystem are digitally signed by
the respective PID Provider or Attestation Provider. All attributes in a PID will be included in that signature; these are called issuer-signed attributes. In addition, Attestation Providers can enable the WSCA/WSCD or a keystore in the Wallet Unit to sign attributes itself, using the private key associated with the public key in an attestation. Such attributes are called device-signed or self-issued attributes. This possibility is used primarily by SUA attestations for signing transactional data; see [Section 2.6.4][264-strong-user-authentication-for-electronic-payments]. The Attestation Rulebook for a specific type of attestation specifies the device-signed (self-issued) attributes that may be present in that attestation, if any. PIDs are not allowed to contain device-signed attributes; this implies that PIDs cannot be used to sign transactional data.

##### 6.6.3.7 Relying Party verifies that the PID or attestation is not revoked

To allow revocation checking of a PID or attestation, the PID Provider or
Attestation Provider includes revocation information in the PID or attestation,
if it is valid for longer than 24 hours. This revocation information includes a
URL indicating the location where a Relying Party can obtain a status list or
revocation list, and an identifier or index for this specific certificate or
attestation within that list.

Notes:

- For attestations with a validity period of less than 24 hours, including
revocation information is not necessary.
- A status list is a bit string or byte string in which each bit or group of
bits denotes the current revocation status (valid or revoked) of one
attestation. To get the status of the attestation it has received from the
Wallet Unit, the Relying Party obtains the status list from the URL specified in
the attestation and verifies the value encoded at the bit position given by the
index value in the attestation. For more information, see [Token Status List].
- A revocation list is a list of PID identifiers or attestation identifiers
revoked by the PID Provider or Attestation Provider. To get the status of the
PID or attestation it has received from the Wallet Unit, the Relying Party
obtains the revocation list from the URL specified in the attestation and
verifies whether the identifier included in the attestation is on the list or
not. For more information, see the (draft) second edition of [ISO/IEC 18013-5], available on [the GitHub repository of the responsible ISO Working Group](https://github.com/ISOWG10/ISO-18013/tree/main/Working%20Documents).
- In some cases, no reliable information regarding the revocation status of a
PID or attestation will be available, for example in case a Relying Party
Instance is offline and does not have access to a cached status list or
revocation list, or if the requested attestation is non-qualified and the
responsible Attestation Provider choose to not have a revocation service for the
attestation. In such a case, a Relying Party performs a risk analysis
considering all relevant factors for the use case, before taking a decision to
accept or refuse the PID or attestation.
- It is recommended but not mandatory for a Relying Party Instance to verify the
revocation status of a PID or attestation.

For more details and requirements on revocation, see [Topic 7][topic-7]. See also [Section 6.6.6.4][6664-pid-or-attestation-revocation].

##### 6.6.3.8 Relying Party Instance verifies device binding

Device binding is the cryptographic link that ensures a PID or attestation
belongs exclusively to the WSCD or to a keystore in the
User's Wallet Unit. This key property prevents copying or cloning,
significantly boosting the attestation's security. Device binding is also a
prerequisite for User binding, allowing the Relying Party to trust the Wallet
Unit's internal User authentication mechanisms to verify the presenter is the
rightful User.

Within the EUDI Wallet ecosystem, implementing device binding is mandatory for
PIDs, since PIDs must be managed at Level of Assurance High, which is impossible
without device binding to a WSCA/WSCD. It is also mandatory for attestations complying with
[ISO/IEC 18013-5], due to the fact that this is required in that standard. For
[SD-JWT VC]-compliant attestations, implementing device binding is recommended
but not mandatory. However, note that [OpenID4VP] enables the Relying Party to
indicate if it wants to receive a proof of device binding for a requested
attestations, via the ``require_cryptographic_holder_binding`` parameter in the
request. It also stipulates that a Wallet Unit cannot return a non-device-bound
attestation in case the Relying Party requests such a proof.

A PID Provider or an Attestation Provider can implement device binding by including
a cryptographic public key in the PID or attestation and signing it. The
corresponding private key is protected by the WSCA/WSCD or keystore in the Wallet Unit.

A WSCA/WSCD or keystore generates a public-private key pair for each PID and
device-bound attestation upon request of the Wallet Unit. The Wallet Unit sends
the public key to the PID Provider or Attestation Provider.

After receiving a presentation response, the Relying Party Instance may verify
that a PID or device-bound attestation it received from a Wallet Unit is indeed
bound to the WSCA/WSCD or keystore included in the Wallet Unit. The Relying
Party Instance does so by requesting the Wallet Unit to sign some
(pseudo-)random data provided by the Relying Party, using the private key
corresponding to the public key in the PID or attestation. For this reason,
device binding is also called 'proof of possession'. In [ISO/IEC 18013-5] it is
called 'mdoc authentication'. In [SD-JWT VC] it is called 'key binding'. Note
that it is recommended but not mandatory for a Relying Party Instance to verify
the device binding signature in the presentation response, if present.

The technical implementation of this verification depends on which of the
standards mentioned in [Topic 12][topic-12]
is supported by the Wallet Unit. Each of these standards specifies in detail how
to carry out this verification.

The data signed by the Wallet Unit may include (a representation of) some
transactional data which the Relying Party included in the presentation request,
see [Section 5.7.5][575-transactional-data-using-isoiec-18013-5-and-openid4vp].
Note that neither [ISO/IEC 18013-5] nor [OpenID4VP] or [SD-JWT VC] specify the
full syntax and semantics of the transactional data. Nor do these standards specify
how a Wallet Unit processes this data, or how it is presented to the
User prior to being signed. All of these aspects will need to be specified in
the Attestation Rulebook or Technical Specification for the type of attestation
that is being requested in the presentation request.

##### 6.6.3.9 Relying Party Instance verifies or trusts User binding

User binding (sometimes also called 'holder binding') is the property that the
person that presents the PID or attestation to the Relying Party is in fact the
User to whom the PID or the attestation was issued. User binding prevents an
attacker from successfully presenting a PID or an attestation that they are not
legally allowed to use.

The mechanism(s) available for User binding depend on the presentation flow type
(proximity or remote, supervised or unsupervised, see also [Section
4.4][44-data-presentation-flows]), and on the attributes issued to the User by
the PID Provider or Attestation Provider:

1. In the first place, for PIDs and device-bound attestations the Relying Party
can always decide to trust the User authentication mechanisms implemented by the
Wallet Unit (see [Section 6.5.3.3][6533-wallet-unit-requests-user-to-set-up-two-user-authentication-mechanisms]).
This means that the Relying Party trusts that the User device or the WSCA/WSCD
has properly authenticated the User before allowing the User to present the
attributes. Note that:

    - This trust is not based on the outcome of any verification by the Relying
    Party itself, but on a a-priori trust in the certified Wallet Unit and (for PIDs and
    attestations with a security level High) the certified WSCA/WSCD.
    - Using this method implies that Relying Parties must verify device binding,
    as described in [Section 6.6.3.8][6638-relying-party-instance-verifies-device-binding].
    The Relying Party Instance in fact first verifies that the PID or
    attestation is bound to the Wallet Unit (i.e., to a WSCA/WSCD or keystore attested in a KA), and then trusts that the Wallet Unit has authenticated the User.
    - As a matter of fact, this User binding method will always be carried out,
    since the Wallet Unit (and for PIDs additionally the WSCA/WSCD) must
    authenticate the User before it can present a PID or attestation, see
    [Section 6.5.3.3][6533-wallet-unit-requests-user-to-set-up-two-user-authentication-mechanisms].

1. In addition, in some cases, if a Relying Party does not want to only trust
the User authentication mechanisms of the Wallet Unit, it may be able to use
User attributes to carry out an additional User binding process. For example, if
the PID or attestation contains a User portrait, the Relying Party may be able
to visually compare that portrait to the face of the person
presenting the attestation, or do a biometrical matching to a photo taken of that face by an automated machine or
as a "selfie". This will generally be possible in supervised proximity
presentations by human inspection, or in an unsupervised proximity flow if
equipped with the appropriate equipment. It may also be possible to do this in
unsupervised remote presentations by using face recognition technology, possibly
even remotely. However, to generate trustworthy outcomes in such situations,
special conditions and dedicated security measures are required, such as good
lighting, clear instructions for the User for positioning their face and an
approved liveness detection mechanism supporting Presentation Attacks Detection
([PAD](https://www.enisa.europa.eu/publications/remote-identity-proofing-attacks-countermeasures)),
as well as mechanisms for injection attack detection, in particular deepfake
detection.
1. Lastly, if the person presenting the PID or attestation is able to present an
identity document, the Relying Party may be able to verify User binding by
comparing attributes from the PID or attestation, such as first and last name,
to those in the identity document. However, this requires that the Relying Party
can verify that the identity document is authentic and really belongs to the
person presenting it. In practice this will often mean that the identity
document is a photo ID, and the presentation must consequently be done in
proximity and be supervised, or done remotely and supported by PAD.

##### 6.6.3.10 Relying Party Instance verifies combined presentation of attributes

###### 6.6.3.10.1 Introduction

According to the [European Digital Identity Regulation], a combined presentation
of attributes is a request for attributes from two or more attestations in the
same action. Scenarios where a User is asked to present different attributes
from various physical documents are common in the real world, and are also
relevant in the digital domain. Several examples, including university
admissions, professional licencing, and rental or loan applications, are
discussed in the [Discussion Paper for Topic K](../discussion-topics/k-combined-presentation-of-attestations.md).
These scenarios can be addressed more efficiently through combined presentation,
allowing a Relying Party to receive a consolidated set of attributes from
different attestations.

In such cases, the Relying Party will need to verify that these attestations
belong to the same User. This can be done in different ways, including (but not
necessarily limited to):

- **Presentation-Based Binding**: A Relying Party may assume that attributes
presented in a single presentation response belong to the same User.
However, this means that the Relying Party trusts that the Wallet Instance that created the response is not
hacked or fraudulent. In some high-security use cases, such trust may not be
warranted.
- **Attribute-Based Binding**: Multiple attestations may include a shared unique
identifier (e.g., a PID number), which can then serve as a binding reference
across different attestations. Another possibility is the use of the same
identifying data, such as full name and date of birth, in multiple attestations,
which can be used to relate attestations to each other and to a User. This is
analogous to many present-day processes using paper documents, which may be seen
as an advantage. However, this method implies that identifying data of the User
must be presented even in use cases where this is not necessary for the purposes
of the use case itself. Moreover, this method may not be conclusive, for
instance if multiple people share the same name.
- **Cryptographic Binding**: The WSCA/WSCD or a keystore in the Wallet Unit may
generate a cryptographic proof demonstrating that it manages the private keys
associated with all of the involved PIDs and device-bound attestations. Since
the WSCA/WSCD or keystore complies with (much) higher security requirements than the device OS does, such a solution is more secure than presentation-based binding. To a lesser
extent, this also applies for keystores. Cryptographic binding is more
privacy-preserving than attribute-based binding, since no attributes other than
those strictly necessary for the use case have to be presented.

Cryptographic binding of attestations is discussed in the next section.

###### 6.6.3.10.2 Cryptographic binding between attestations

Cryptographic binding between attestations is an envisioned cryptographic
mechanism that enables a WSCA/WSCD or keystore to prove that it manages the
private keys corresponding to two (or more) public keys. A proof of
cryptographic binding between attestations can be used during attestation
presentation, e.g., to prove that the public keys associated with two (or more)
device-bound attestations are managed by the same WSCA/WSCD or keystore and
that, therefore, these attestations belong to the same User.

When designed with privacy in mind, cryptographic binding between attestations
becomes a powerful tool for protecting individuals from unnecessary exposure.
Rather than relying on full User identification for each presented attestation,
for instance by requesting the User's name from each of them, a Relying Party
can instead implement solutions that enable Users to prove only what is strictly
necessary — without revealing who they are. This aligns directly with the
commitments laid out in the [European Digital Identity Regulation]: access to
digital services must be privacy-protective by design (recital 4), supported by
privacy-enhancing technologies (recital 14), and uphold the principle of
unobservability (recital 32).

In this light, Article 5a(16)(b) provides a clear obligation: when attributes
are presented together, this must be done in a way that avoids unnecessary
identification of the User. Instead, a privacy-preserving cryptographic binding
between attestations opens the door to new possibilities. It enables the
transition of many real-world processes — currently performed under full User
identification — into more private digital equivalents.

Consider, for example, eligibility checks for educational programs. A student
should be able to prove they reside in a particular city (as attested in their
PID) and have qualifying grades (from a diploma) without revealing their name,
gender, or exact address. With the right cryptographic mechanisms in place, we
can minimize data exposure while maintaining trust in the combination of
presented attributes.

Note that:

- By definition, cryptographic binding between attestations can only be used for
PIDs and device-bound attestations.
- This version of the ARF does not specify or reference a specific cryptographic
mechanism to implement cryptographic binding between attestations. However,
[Topic 18][topic-18]
specifies high-level requirements for a cryptographic binding between
attestations scheme.
- This ARF assumes that each Wallet Unit (and therefore
each WSCA/WSCD and keystore) contains attestations for only one User (see also
[Section 3.2][32-users-of-wallet-units]). Therefore, a proof of cryptographic
binding between two attestations proves that these attestations belong to the
same User. However, some additional actions must be done to use such a mechanism
in practice:
    - During attestation issuance, an Attestation Provider must request the
    Wallet Unit to bind the new attestation to an existing PID or attestation.
    For this, the Attestation Provider must verify that the existing PID or
    attestation refers to the same User to whom the new attestation refers. How
    the Attestation Provider does this is out of scope of the ARF. For example,
    the Attestation Provider could request the User name and birth date from a
    PID on the Wallet Unit, verify that this information matches a record in its
    database, issue an attestation corresponding to the information in that
    record, and then request the Wallet Unit to bind the public key in that
    attestation to the public key in the PID.
    - A Relying Party that has verified a proof of cryptographic binding between
    two attestations needs to verify that these attestations belong to the User
    presenting them. This is User binding, as discussed in [Section 6.6.3.9][6639-relying-party-instance-verifies-or-trusts-user-binding].
    Note that, if User binding is proven for one of the bound attestations, it is
    proven for all of them.

##### 6.6.3.11 Relying Party Instance trusts issuer to have authenticated the Wallet Unit and the Wallet Provider

The Relying Party Instance does not have a way to directly verify the
authenticity of the Wallet Unit and the Wallet Provider. Rather, the Relying
Party trusts the PID Provider or the Attestation Provider to have done this
during issuance of the PID or attestation.

##### 6.6.3.12 Relying Party optionally trusts issuer to regularly verify that Wallet Unit is not revoked

[Section 6.6.2.5][6625-pid-provider-or-attestation-provider-verifies-that-wallet-unit-is-not-revoked]
explained how a PID Provider or an Attestation Provider can verify that a Wallet
Unit is not revoked, using the revocation information in the WIA and KA. That section also noted that the [CIR
2024/2977] requires PID Providers to verify regularly, during the entire
lifetime of the PID, whether the Wallet Unit on which that PID is residing is
revoked by the Wallet Provider. If that happens, the PID Provider must revoke
the PID. Therefore, by verifying the revocation status of the PID, the Relying
Party Instance can also trust the revocation status of the Wallet Unit.
Consequently, there is no need for a separate mechanism that would allow the
Relying Party to verify the revocation status of a Wallet Unit directly with the
Wallet Provider.

Attestation Providers can use the same mechanism to provide the same assurance
to Relying Parties, although this is not required by the CIR. If an Attestation
Provider does not support this, a Relying Party obtaining an attestation issued
by that Attestation Provider has no way of knowing whether the Wallet Unit is
revoked. It is up to a Relying Party to check, before requesting a particular
type of attestation from Wallet Units to fulfil a particular use case, if the
Attestation Provider provides this assurance. If not, the Relying Party must
decide whether the associated risk is acceptable.

##### 6.6.3.13 Wallet Unit enables the User to report suspicious requests by a Relying Party and to request a Relying Party to erase personal data

A Wallet Unit enables the User to report unlawful or suspicious requests for
personal data by a Relying Party to a Data Protection Authority (DPA). To allow
this, a Wallet Unit provides a dashboard displaying a log of all attestation
presentation transactions (as well as all other types of transaction) performed
by the Wallet Unit. For presentation transactions, this log includes the
identifiers of the attributes that were requested and presented, but not their
values. For high-level requirements on this transaction log, see [Topic 19][topic-19].

The Wallet Unit enables the User to easily report a suspicious presentation
request in the transaction log to a DPA. By default, this is the DPA that
supervises the Relying Party, but if the Wallet Unit does not know which DPA
this is (because this information was not available during the transaction), it
will present the User with the contact details of at least the DPA of the region
in which the Wallet Provider resides. The User can make such a report regardless
of whether any attributes were actually presented to the Relying Party. Even if
the Wallet Instance prevented the presentation of any attributes, for instance
because Relying Party authentication failed, or if the User did not approve the
presentation of any attributes, the User can still report the request to a Data
Protection Authority.

For more information and requirements on reporting presentation requests to a DPA,
see [Topic 50][topic-50].

The dashboard and the transaction log kept by the Wallet Unit also enable the
User to request a Relying Party to delete personal data in accordance with
Regulation (EU) 2016/679 (the GDPR). In the context of EUDI Wallet, this
personal data consists of attributes that were presented to the Relying Party by
the User, using their Wallet Unit. Relying parties, which act as data processors
or controllers, already have procedures, protocols, and interfaces in place to
handle data deletion requests in accordance with the GDPR. Wallet Units re-use
these already existing interfaces. As there are no standardised protocols and
interfaces for this purpose, this implies that a Wallet Unit can either

- open a specific URL with an external browser to ask for the deletion of data
in a web form provided by the Relying Party,
- open an external mail client with a suitable template text, or
- open an external phone client to enable the User to call the Relying Party.
  
The registration certificate of the Relying Party (see [Section 6.4.2][642-relying-party-registration])
contains the necessary contact information, including the URL of a web form for
privacy-related enquiries, an e-mail address, and/or a phone number.

A Relying Party may use the services of an intermediary to request data
from a Wallet Unit, see [Topic 52][topic-52].
However, such intermediaries are required to delete any data they obtain from a
Wallet Unit immediately after sending it to the Relying Party. Data deletion
requests are therefore always sent to the Relying Party, not the intermediary.

For more information and requirements on requesting a Relying Party to delete
personal data, see [Topic 48][topic-48].
