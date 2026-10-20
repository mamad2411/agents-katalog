---
name: "arf-presentation-reqs"
description: "Use when implementing wallet-side presentation trust: Relying Party authentication, attribute request verification, embedded disclosure policy evaluation, and user approval flows."
sections:
  - "6.6.3.1 Required trust relationships"
  - "6.6.3.2 Wallet Unit authenticates the Relying Party Instance"
  - "6.6.3.3 Wallet Unit verifies that Relying Party does not request more attributes than it registered"
  - "6.6.3.4 Wallet Unit evaluates embedded disclosure policy, if present"
  - "6.6.3.5 Wallet Unit obtains User approval for presenting selected attributes"
  - "6.6.3.5.1 Introduction"
  - "6.6.3.5.2 Wallet Unit authenticates the User"
  - "6.6.3.5.3 Wallet Unit informs the User about the identity of the Relying Party"
  - "6.6.3.5.4 Wallet Unit informs the User about the attributes the Relying Party requested"
  - "6.6.3.5.5 Wallet Unit informs the User about the Relying Party's intended use and privacy policy"
  - "6.6.3.5.6 Wallet Unit informs the User about the outcome of the evaluation of the requested attributes"
  - "6.6.3.5.7 Wallet Unit informs the User about the outcome of the evaluation of the embedded disclosure policy"
  - "6.6.3.5.8 Wallet Unit enables the User to approve or deny the requested attributes"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~6119 -->

##### 6.6.3.1 Required trust relationships

A Relying Party can request a User to present some attributes from a PID or from
an attestation in their Wallet Unit. [Figure 12][61-scope] shows that a Relying
Party uses a Relying Party Instance to interact with the Wallet Unit of the
User. The relationship between the Relying Party and their Relying Party
Instance is similar to the relationship between the User and their Wallet Unit.

When processing the request, the following trust relationships are established:

1. The Wallet Unit authenticates the Relying Party Instance, ensuring the User
about the Relying Party's identity. [Section
6.6.3.2][6632-wallet-unit-authenticates-the-relying-party-instance] explains
how this will be done.
2. The Wallet Unit verifies that the Relying Party does not request more
attributes than it has registered for, and informs the User about the outcome of
this verification. See [Section 6.6.3.3][6633-wallet-unit-verifies-that-relying-party-does-not-request-more-attributes-than-it-registered]
for more information.
3. The Attestation Provider, during issuance, may optionally embedded a
disclosure policy in the attestation. If such a policy is present for the
requested attestation, the Wallet Unit evaluates the disclosure policy and
informs the User about the outcome of this evaluation. See [Section 6.6.3.4][6634-wallet-unit-evaluates-embedded-disclosure-policy-if-present].
4. The User approves or rejects the presentation of the requested attributes.
User approval and selective disclosure are described in [Section 6.6.3.5][6635-wallet-unit-obtains-user-approval-for-presenting-selected-attributes].
Subsequently, after the Wallet Unit presents the selected attributes from the
PID or attestation to the Relying Party Instance by sending a response to the
request, the Relying Party validates the response. The following trust
relationships are established:
5. The Relying Party Instance verifies the signature of the PID or attestation.
This ensures that the Relying Party can trust that the PID or attestation it
receives is issued by an authentic Provider and has not been changed. This is
described in [Section 6.6.3.6][6636-relying-party-instance-verifies-the-authenticity-of-the-pid-or-attestation].
6. The Relying Party verifies that the PID Provider or Attestation Provider did
not revoke the PID or attestation. This is described in [Section 6.6.3.7][6637-relying-party-verifies-that-the-pid-or-attestation-is-not-revoked].
7. For PIDs and device-bound attestations, the Relying Party verifies that the
PID Provider or Attestation Provider issued this PID or attestation to the same
Wallet Unit that presented it to the Relying Party. In other words, it checks
that the PID or attestation was not copied or replayed. This is generally called
device binding, and it is discussed in [Section 6.6.3.8][6638-relying-party-instance-verifies-device-binding].
8. In some use cases, the Relying Party verifies that the person presenting the
PID or attestation is the User to whom the PID or the attestation was issued.
This is called User binding. In other use cases, the Relying Party trusts that
the Wallet Unit and/or the WSCA/WSCD have done this check. User binding is
discussed in [Section 6.6.3.9][6639-relying-party-instance-verifies-or-trusts-user-binding].
9. The Relying Party can request attributes from two or more attestations in the
same interaction. This is called a **combined presentation of attributes**. If
so, the Relying Party verifies that these attestations belong to the same User.
This is discussed in [Section 6.6.3.10][66310-relying-party-instance-verifies-combined-presentation-of-attributes].
10. Finally, after the interaction with the Relying Party Instance is over, the
Wallet Unit enables the User to report unlawful or suspicious requests for
personal data by a Relying Party, based on information logged by the Wallet
Unit. In addition, the Wallet Unit enables the User to send a request to a
Relying Party to delete personal data (i.e., User attributes) obtained from the
Wallet Unit. This is discussed in [Section 6.6.3.13][66313-wallet-unit-enables-the-user-to-report-suspicious-requests-by-a-relying-party-and-to-request-a-relying-party-to-erase-personal-data].

##### 6.6.3.2 Wallet Unit authenticates the Relying Party Instance

Relying Party authentication is a process whereby a Relying Party proves its
identity to a Wallet Unit, in the context of an interaction in which the Relying
Party requests the Wallet Unit to present some attributes.

Relying Party authentication is included in the protocol used by a Wallet Unit
and a Relying Party Instance to communicate. As documented in [Topic 12][topic-12],
at least two different protocols can be used within the EUDI Wallet ecosystem,
namely the ones specified in [ISO/IEC 18013-5] and [OpenID4VP]. Both protocols
include functionality allowing the Wallet Unit to authenticate the Relying Party
Instance. Although these protocols differ in the details, on a high level, they
both implement Relying Party authentication as shown in Figure 13 below.

![Figure 13](https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/media/Figure_13_Relying_Party_Authentication.png)

```mermaid
sequenceDiagram
  participant U as User
  participant WI as Wallet Instance
  participant RPI as Relying Party Instance
  participant AC as Access CA
  participant RP as Relying Party
  participant L as LoTE
  participant R as Registrar
  RP->R: A.1 Register
  WI-->L: B. Obtain Access CA trust anchor
  RPI->RPI: 1. Prepare presentationrequest including accesscertificate&nbsp;and trust chain
  RPI->RPI: 2. Sign request using&nbsp;access certificate's&nbsp;private key
  RPI->WI: 3. Presentation request
  WI->WI: 4. Verify signature using publickey from access&nbsp;certificate
  WI->WI: 5. Verify access&nbsp;certificate and&nbsp;trust chain using&nbsp;trust anchor
  WI->AC: 6. Validate that access&nbsp;certificateand trust&nbsp;chain are not revoked
  WI->RPI: 9. Send response with approvedattributes
  RPI->AC: A.2 Obtain access&nbsp;certificate
```

Figure 13 High-level overview of Relying Party authentication process

The figure shows the following:

First, there are two preconditions that need to be fulfilled before the Relying
Party authentication process can begin. Note that these actions are not carried
out for every presentation, but only once (excluding possible updates):

A) The Relying Party registered itself with a Registrar in its Member State, as described in
[Section 6.4.2][642-relying-party-registration],
and obtained one or more access certificate for each of its Relying Party Instances from an Access Certificate Authority (See [Section 3.18][318-access-certificate-authorities]) associated with the Registrar.

B) The Wallet Unit obtained the trust anchor of the Access Certificate Authority from the respective List of Trusted Entities (LoTE, see [Section 3.5][35-trusted-list-provider-or-lote-provider]).

Subsequently, during each presentation of attributes:

1. The Relying Party Instance prepares a request for some attributes to the
Wallet Unit and includes its access certificate in the
request, plus all intermediate certificates up to (but excluding) the trust anchor.
1. The Relying Party Instance signs some data in the attribute request using its
private key.
1. The Relying Party Instance sends the request to the Wallet Unit.
1. The Wallet Unit checks the authenticity of the request by verifying the
signature over the request using the public key in the access certificate.
1. The Wallet Unit checks the authenticity of the Relying Party by validating
the access certificate and all intermediate certificates
included in the request. For validating the last intermediate certificate, the
Wallet Unit uses the trust anchor it obtained from the LoTE in step B above.
1. The Wallet Unit validates that none of the certificates in the trust chain
have been revoked. This includes the access certificate
as well as all other certificates in the trust chain, including the trust anchor
itself if applicable. For revocation checking, the Wallet Unit uses the standard CRL or OCSP mechanisms, as specified in [RFC 5280], [ETSI TS 119 411-8], and in the Certification Practices Statement of the Access CA. For offline revocation checking, a Wallet Unit caches the CRLs of all Access Certificate Authorities.
1. The Wallet Unit continues by requesting the User for approval.
1. The User approves the attributes that will be presented.
1. The Wallet Unit sends a response containing only the approved attributes to
the Relying Party Instance.

If Relying Party authentication fails for any reason (in steps 4. - 6.), the Wallet Unit notifies the User. In addition, the Wallet Unit either does not present the requested attributes to the Relying Party, or gives the User the choice to present the requested attributes or not. It is up to the Wallet Provider to make a choice for one of these two options, considering the precise reason for which authentication failed. To give some examples:

- If the signature over the request is not valid, the Wallet Unit will likely stop the transaction, since this may point to a man-in-the-middle attack or another serious security issue.
- Similarly, if the access certificate chain cannot be verified using a trust anchor from the Access Certificate Authority LoTE, the Wallet Unit will stop the transaction, because the Relying Party may be using a fake access certificate.
- If the Wallet Unit cannot verify the revocation status of the access certificate or another certificate because no sufficiently fresh revocation information is available, it is up to the Wallet Provider to decide to continue the transaction (by asking for User approval) or to stop it, perhaps taking into account the sensitivity of the requested attributes.
- If there is some minor error in the format of the (properly signed) access certificate, the Wallet Unit will continue the transaction, if there are no associated security risks.  

For more information on Relying Party authentication, please refer to [Topic 6][topic-6].

##### 6.6.3.3 Wallet Unit verifies that Relying Party does not request more attributes than it registered

Figure 14 shows how a Wallet Unit verifies that the Relying Party properly registered all attributes it request in the presentation request.

![Figure 14](https://raw.githubusercontent.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/main/docs/media/Figure_14_Verifying_Relying_Party_Registration.png)

```mermaid
sequenceDiagram
  participant U as User
  participant WI as Wallet Instance
  participant RP as Relying Party
  participant PORC as Provider of registration certificates&nbsp;
  participant R as Registrar
  participant L as LoTE
  participant RP1 as Relying PartyInstance
  RP-->R: A.1 Register Relying Party
  WI-->L: B. Obtain trust anchor&nbsp;of Provider of registrationcertificates
  RP1->RP1: 1. Prepare presentation requestInclude&nbsp;registration certificate&nbsp;plus&nbsp;trust chain
  RP1->WI: 2. Presentation request
  WI->WI: 3. Verify registration&nbsp;certificateand&nbsp;trust chain using&nbsp;<br/>trust anchor
  WI->WI: 5. Verify that all requestedattributes were registered&nbsp;
  WI->PORC: 4. Validate that registrationcertificate&nbsp;and trust&nbsp;chain arenot revoked
  WI->RP1: 8. Send response with approvedattributes
  RP-->PORC: A.2 Obtain registration certificate(s)
  RP1-->RP: A.3 Distribute registrationcertificates to relevant&nbsp;Relying Party Instances
```

Figure 14 High-level overview of registration certificate verification process

First, there are two preconditions that need to be fulfilled before the verification process can begin. Note that these actions are not carried
out for every presentation, but only once (excluding possible updates):

A) During registration, the Relying Party registered which attributes it intends to
request from Wallet Units for each of the services (intended uses) it has; see [Section 6.4.2][642-relying-party-registration]. The Registrar ensured that an associated Provider of registration certificates listed these
attributes in a separate registration certificate for each intended use and sent it to the
Relying Party. Subsequently, the Relying Party distributed the registration certificates it received to its
Relying Party Instances. Note that it is up to the Relying Party to determine if all of its Relying Party Instances need all of the registration certificates, or that some Relying Party Instances are used only for a subset of the Relying Party's intended uses, and consequently only need the registration certificates describing those intended uses. 

B) The Wallet Unit obtained the trust anchor of the Provider of registration certificates from the respective List of Trusted Entities (LoTE, see [Section 3.5][35-trusted-list-provider-or-lote-provider]).

Subsequently, during each presentation of attributes:

1. The Relying Party Instance prepares a presentation request and includes a single
registration certificate pertaining to the intended use of the request. Note that a single intended use may cover multiple attributes from multiple
attestations. For example, a Relying Party selling alcoholic beverages online
may register that for this intended use they will request an age verification
attribute from the PID and a User address from some other attestation. However,
if a Relying Party really has multiple intended uses for interacting with a
Wallet Unit, it needs to send multiple presentation requests, each including the
relevant registration certificate.
to the Wallet Unit
1. The Relying Party Instance sends the request to the Wallet Unit.
1. The Wallet Unit verifies the registration certificate. The Wallet Unit verifies that:

    - the registration certificate is present and well-formed,
    - the signature over the registration certificate can be verified using a trust anchor from the LoTE of Providers of registration certificates,
    - the registration certificate contains the same Relying Party identifier and Service identifier as the access certificate contained in the same presentation request. If that is not the case, a fraudulent Relying Party could be using a registration certificate that was issued to another Relying Party. Note that there two different ways in which this condition can be fulfilled:
      - Either the access certificate and the registration certificate were issued to the same Relying Party, in which the subject fields of both certificates contain the same set of identifiers,
      - Or the access certificate was issued to an intermediary (see [Section 6.6.5][665-pid-or-attestation-presentation-to-an-intermediary]), and the registration certificate indicates that the intermediated Relying Party uses the services of this intermediary, by including the Relying Party identifier and Service identifier of the intermediary in a `usesIntermediary` field according to [Technical Specification 5](../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md).
1. The Wallet Unit verifies that the registration certificate has not expired and is not revoked.  

    In case any of the checks in point 3. and 4. fail, the Wallet Unit warns the User, when asking the User for approval, see [Section 6.6.3.5][6635-wallet-unit-obtains-user-approval-for-presenting-selected-attributes], that it could not obtain or validate the information registered about the Relying Party. In addition, it is up to the Wallet Provider to determine, based on its risk analysis and security policy, whether and under which conditions the User may approve (or reject) the presentation of attributes despite specific failed validation checks. Moreover, any User approval must be explicit; silence or pre-ticked boxes do not suffice.

1. If all of the above checks pass, the Wallet Unit retrieves from the registration certificate the list of attributes registered by the Relying Party. The Wallet Unit compares this list to the attributes that the Relying Party requests in the presentation request. In case the Relying Party requested some attributes that are not included in the registration certificate, the Wallet Unit warns the User that the Relying Party is requesting more information than it has registered. The Wallet Unit does so when asking the User for approval, see step 6. and [Section 6.6.3.5][6635-wallet-unit-obtains-user-approval-for-presenting-selected-attributes]. In addition, it is up to the Wallet Provider to determine, based on its risk analysis, security policy, and applicable law, whether the Wallet Unit must 

    - enable the User to approve (or reject) the presentation of all requested attributes, including the non-registered ones,
    - enable the User to approve (or reject) the presentation of the registered attributes only, or 
    - reject the presentation of all requested attributes.

    Moreover, any User approval must be explicit; silence or pre-ticked boxes do not suffice.
1. The Wallet Unit informs the User about the outcome of the above verifications and requests approval for presenting the requested attributes.
1. The User approves the attributes that will be presented.
1. The Wallet Unit sends a response containing only the approved attributes to
the Relying Party Instance.

> Notes: 
> - The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].
> - The process and verifications describe above ensure that Wallet Providers comply with the 'general access policy' described in [CIR 2025/848].

For
more information, see [Topic 44][topic-44].

##### 6.6.3.4 Wallet Unit evaluates embedded disclosure policy, if present

During attestation issuance, an Attestation Provider optionally created an embedded
disclosure policy for the attestation, see [Section 6.6.2.8][6628-provisioning-embedded-disclosure-policies].
If such a policy is present for the requested attestation, the Wallet Unit
evaluates the policy, together with information in the registration certificate, to
determine whether the Attestation Provider allows this Relying Party to receive
the requested attestation. Note that the Wallet Unit verifies the authenticity
of the registration certificate before using any data contained in it.

The Wallet Unit presents the outcome of the disclosure policy evaluation to the
User when requesting User approval, see [Section 6.6.3.5.7][66357-wallet-unit-informs-the-user-about-the-outcome-of-the-evaluation-of-the-embedded-disclosure-policy].

For more details on the embedded disclosure policy, see [Topic 43][topic-43].

##### 6.6.3.5 Wallet Unit obtains User approval for presenting selected attributes

###### 6.6.3.5.1 Introduction

**Note: In this document the term 'User approval' exclusively refers to a User's
decision to present an attribute to a Relying Party. Under no circumstances
User approval to present data from their Wallet Unit should be construed as
lawful grounds for the processing of personal data by the Relying Party or any
other entity. A Relying Party requesting or processing personal data from a
Wallet Unit must ensure that it has grounds for lawful processing of that data,
according to Article 6 of Regulation (EU) 2016/679 (the GDPR).**

Before presenting any attribute to a Relying Party, the Wallet Unit requests the
User for their approval. This is critical for ensuring that the User remains in
control of their attributes.

A Wallet Unit requests User approval in all use cases, both in proximity flow
and remote flow, and including:

- Use cases where the Relying Party could be assumed to be trusted, for example,
when the Relying Party is part of law enforcement or another government agency.
- Use cases where the requested attributes are critical for the Relying Party to
grant access to the User or deliver the requested services.
- Use cases where there is, according to the GDPR or other legislation, no legal
need to ask for the User's approval because another legal basis exists for
requesting the attributes.

A number of conditions must be fulfilled for effective User approval:

1. The Wallet Unit authenticated the User; see [Section 6.6.3.5.2][66352-wallet-unit-authenticates-the-user],
1. The Wallet Unit informed the User about the identity of the Relying Party and
about the identity of the intermediary, if applicable; see [Section 6.6.3.5.3][66353-wallet-unit-informs-the-user-about-the-identity-of-the-relying-party],
1. The Wallet Unit informed the User about the attributes the Relying Party requested; see [Section 6.6.3.5.4][66354-wallet-unit-informs-the-user-about-the-attributes-the-relying-party-requested],
1. The Wallet Unit informed the User about the Relying Party's intended use and
privacy policy for these attributes; see [Section 6.6.3.5.5][66355-wallet-unit-informs-the-user-about-the-relying-partys-intended-use-and-privacy-policy],
1. The Wallet Unit informed the User about the outcome of the evaluation of the
requested attributes; see [Section 6.6.3.5.6][66356-wallet-unit-informs-the-user-about-the-outcome-of-the-evaluation-of-the-requested-attributes],
1. The Wallet Unit informed the User about the outcome of the evaluation of the
embedded disclosure policy, if any; see [Section 6.6.3.5.7][66357-wallet-unit-informs-the-user-about-the-outcome-of-the-evaluation-of-the-embedded-disclosure-policy],
1. The Wallet Unit enables the User to approve or deny the requested attributes; see [Section 6.6.3.5.8][66358-wallet-unit-enables-the-user-to-approve-or-deny-the-requested-attributes].

These conditions are further discussed in the next subsections. After the User
gives their approval, the Wallet Unit will present the approved User attributes
to the Relying Party Instance.

High-level requirements regarding User approval can be found in [Topic 6][topic-6]

###### 6.6.3.5.2 Wallet Unit authenticates the User

A prerequisite for requesting User approval is that the Wallet Unit is sure that
the person using the Wallet Unit (and giving the approval) is in fact the User.
Therefore, the Wallet Unit authenticates the User prior to or during requesting
User approval, on request of the Wallet Unit. To do so, the Wallet Unit uses one
of the User authentication mechanisms set up during Wallet Unit activation, see
[Section 6.5.3.3][6533-wallet-unit-requests-user-to-set-up-two-user-authentication-mechanisms].

###### 6.6.3.5.3 Wallet Unit informs the User about the identity of the Relying Party

In order to be able to give approval, a User needs to be informed about the
identity of the Relying Party. The Wallet Unit displays to the User the
User-friendly Relying Party trade name and Service trade name. The Wallet Unit obtains this information from the registration certificate presented by the Relying Party Instance.

If the Relying Party uses an intermediary,
the Wallet Unit does not inform the User about the trade names of the intermediary and its Service during the transaction; see [Section 6.6.5][665-pid-or-attestation-presentation-to-an-intermediary]. However, it does log the intermediary's trade names in the transaction log. The Wallet Unit finds the trade names of the intermediary
in the access certificate presented by the Relying Party Instance,
whereas it obtains the trade names of the intermediated Relying Party from the registration certificate.

###### 6.6.3.5.4 Wallet Unit informs the User about the attributes the Relying Party requested

In order to be able to give approval, a User also needs to know which attributes
the Relying Party wishes to receive. Note that a Relying Party may request
attributes from multiple attestations in a single request; for example
information from a diploma and from a PID.

In case a Relying Party requests the presentation of the portrait in a PID, the Wallet Unit warns the User that the request involves the presentation of biometric data. The Wallet Unit then ensures that User approval for presenting the portrait is explicit; silence or a pre-ticked box do not suffice.

###### 6.6.3.5.5 Wallet Unit informs the User about the Relying Party's intended use and privacy policy

According to the GDPR, a User must be informed about the Relying Party's
intended use for the requested attributes. For each presentation request, the
Relying Party can have only one intended use. If the Relying Party has multiple
intended uses for requesting attributes from a Wallet Unit, it needs to send
multiple presentation requests. In such a case, the Wallet Unit will request the
User for their approval multiple times.

The registration certificate sent by the Relying Party Instance to the Wallet
Unit contains a User-friendly
description of the Relying Party's intended use, as well as a URL to the
applicable privacy policy of the Relying Party. The Wallet Unit displays this
information to the User.

###### 6.6.3.5.6 Wallet Unit informs the User about the outcome of the evaluation of the requested attributes

[Section 6.6.3.3][6633-wallet-unit-verifies-that-relying-party-does-not-request-more-attributes-than-it-registered]
above described how the Wallet Unit can verify the attributes requested by the
Relying Party against the attributes that the Relying Party registered for the
given intended use. If the
outcome is negative, the Wallet Unit will inform the User that this is the case.
For example, "\<Relying Party name\> requested \<attribute1\>, but it did not
register this attribute. Do you want to continue?" Note that it is up to the Wallet Provider to decide if the User can
overrule a negative outcome of this verification and decide to approve the
request.

###### 6.6.3.5.7 Wallet Unit informs the User about the outcome of the evaluation of the embedded disclosure policy

[Section 6.6.3.4][6634-wallet-unit-evaluates-embedded-disclosure-policy-if-present]
above described that an Attestation Provider can add an embedded disclosure
policy for an attestation. It also described how a Wallet Unit can evaluate such
a policy. The Wallet Unit presents the outcome of the disclosure policy
evaluation to the User when asking for User approval. For example, "The issuer
of your \<attestation name\> does not want you to present data to \<Relying
Party name\>. Do you want to continue?" Note that the User can overrule a
negative outcome of the disclosure policy evaluation and decide to approve the
request.

###### 6.6.3.5.8 Wallet Unit enables the User to approve or deny the requested attributes

After presenting all of the above information to the User, the Wallet Unit
enables the User to approve or deny the requested attributes. Preferably, the
User gives approval either to present all attributes requested, or none of them.
This is because partial approval would mean that the Relying Party cannot
deliver the service, but nevertheless receives some User attributes. This would
be a violation of the User's privacy. Note that a Relying Party is not allowed
to request more data than is justified for the intended use. Therefore, if the
User feels that the Relying Party is actually requesting more data than needed,
that implies that the Relying Party is not trustworthy. The User will probably not
approve the presentation of any data in that case.

The Wallet Unit will present all approved User attributes, and only these,
to the Relying Party Instance.
