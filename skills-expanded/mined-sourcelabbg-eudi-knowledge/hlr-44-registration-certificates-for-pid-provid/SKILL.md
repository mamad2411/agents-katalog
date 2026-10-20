---
name: "hlr-44-registration-certificates-for-pid-provid"
description: "Use when working with EUDI high-level requirements for 'Registration certificates for PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.26 Topic 44 - Registration certificates for PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties"
  - "A. Generic requirements on the specification and contents of registration certificates <!-- omit from toc -->"
  - "B Requirements on the issuance of registration certificates to Relying Parties <!-- omit from toc -->"
  - "C. Requirements on the issuance of registration certificates to PID Providers and Attestation Providers <!-- omit from toc -->"
  - "D. Requirements on the presentation and verification of registration certificates of Relying Parties <!-- omit from toc -->"
  - "E. Requirements on the presentation and verification of registration certificates of PID Providers and Attestation Providers <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~5426 -->

#### A.2.3.26 Topic 44 - Registration certificates for PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties

##### A. Generic requirements on the specification and contents of registration certificates <!-- omit from toc -->

<div class="eudi-hlr" id="RPRC_01" markdown>
<div class="eudi-hlr__id">RPRC_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Providers of registration certificates SHALL comply with all relevant requirements in [ETSI TS 119 475].

</div>
</div>

<div class="eudi-hlr" id="RPRC_01a" markdown>
<div class="eudi-hlr__id">RPRC_01a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Provider of registration certificates SHALL be able to revoke a registration certificate, if it has a validity period of longer than 24 hours, in accordance with the applicable requirements in [ETSI TS 119 475].

</div>
</div>

<div class="eudi-hlr" id="RPRC_01b" markdown>
<div class="eudi-hlr__id">RPRC_01b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Provider of registration certificates SHALL have a policy specifying under which conditions a registration certificate it issued will be revoked.

</div>
</div>

<div class="eudi-hlr" id="RPRC_02" markdown>
<div class="eudi-hlr__id">RPRC_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When signing a registration certificate, the Provider of registration certificates SHALL include the signing certificate and, if present, any intermediate certificate(s) leading up to the corresponding trust anchor of the Provider in the LoTE, in the `x5c` parameter in the JOSE header of the registration certificate.

</div>
</div>

<div class="eudi-hlr" id="RPRC_02a" markdown>
<div class="eudi-hlr__id">RPRC_02a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the verification of the registration certificates of Relying Parties, a Wallet Unit SHALL accept all trust anchors of Providers of registration certificates, as published by the Commission in the relevant LoTE, and only those.

</div>
</div>

<div class="eudi-hlr" id="RPRC_03" markdown>
<div class="eudi-hlr__id">RPRC_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The contents of a registration certificate SHALL include at least the information required in Annex V of the [CIR 2025/848](https://data.europa.eu/eli/reg_impl/2025/848/oj) regarding registration of wallet-relying parties.

</div>
</div>

<div class="eudi-hlr" id="RPRC_04" markdown>
<div class="eudi-hlr__id">RPRC_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the subject of the registration certificate uses the services of an intermediary (see [Topic 52][topic-52]), the 'association to the intermediary' mentioned in Annex I (15) of [CIR 2025/848] (and referenced in Annex V, point 3(j) of that CIR) SHALL consist of the unique identifier of this intermediary, as meant in requirement Reg_32 and the intermediary's Relying Party Service identifier as meant in Reg_33.

*Note: a) These identifiers are identical to those in the access certificate of the intermediary. b) The association is also included in the respective access certificate of the intermediary, see Reg_34a.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_04a" markdown>
<div class="eudi-hlr__id">RPRC_04a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The registration certificate format SHALL provide for the data elements to carry the Relying Party Service identifier mentioned in Reg_33 and the Relying Party Service trade name mentioned in Reg_34. 

</div>
</div>

<div class="eudi-hlr" id="RPRC_05" markdown>
<div class="eudi-hlr__id">RPRC_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the subject of the registration certificate is not a Relying Party (i.e. in the terms of CIR 2025/848, a Service Provider), the certificate SHALL NOT contain the intended use as meant in Annex I (9) and (10) of CIR 2025/848.

*Note: A PID Provider or Attestation Provider may request attributes from the Wallet Unit during issuance, for example to identify and authenticate the User. If so, it registers as both a Service Provider and an Attestation Provider, and consequently its registration certificate contains its intended use.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_06" markdown>
<div class="eudi-hlr__id">RPRC_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The contents of a registration certificate SHALL include a trade name for the subject of the certificate, in a format suitable for presenting to a User, which SHALL be identical to the trade name in the access certificates of the entity, see Reg_31.

</div>
</div>

<div class="eudi-hlr" id="RPRC_07" markdown>
<div class="eudi-hlr__id">RPRC_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The contents of a registration certificate SHALL include an EU-wide unique identifier for the subject of the certificate, which SHALL be identical to the identifier in the access certificates of that entity, see Reg_32.

*Note: a) A Wallet Unit needs an identifier for a Relying Party at least to allow the User to send a report of suspicious Relying Party presentation requests to a data protection authority according to [Topic 50][topic-50].*

</div>
</div>

<div class="eudi-hlr" id="RPRC_07a" markdown>
<div class="eudi-hlr__id">RPRC_07a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The contents of a registration certificate SHALL contain an identifier and a trade name for the Relying Party Service, which SHALL be identical to the Service identifier and trade name in one or more of the access certificates of that entity, see Reg_33 and Reg_34.

*Note: There must be at least one Relying Party Instance or service supply point that is able to use a given registration certificate.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_08" markdown>
<div class="eudi-hlr__id">RPRC_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The EU-wide unique identifier meant in RPRC_07 SHALL be identical in all registration certificates issued for a given entity.

*Note: In case the registration certificates issued to an intermediated Relying Party are held and presented by an intermediary, the entity meant in this requirement is the intermediated Relying Party. An intermediary may obtain and hold registration certificates with a different unique identifier for other intermediated Relying Parties.*

</div>
</div>


##### B Requirements on the issuance of registration certificates to Relying Parties <!-- omit from toc -->

<div class="eudi-hlr" id="RPRC_09" markdown>
<div class="eudi-hlr__id">RPRC_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During the registration process for Relying Parties, as specified in [Topic 27][topic-27], a Provider of registration certificates associated to the Member State Registrar SHALL create and sign or seal a separate registration certificate for each combination of intended use and Relying Party Service, as registered by the Relying Party per Reg_10d, and issue it to the Relying Party. The Provider of registration certificates SHALL do so in an automated manner and without undue delay. Each registration certificate SHALL comply with the requirements in the technical specification mentioned in RPRC_01. 

*Note: Example clarifying 'each combination of intended use and Relying Party Service': If a Relying Party registers Service A having intended use 1 and 2, Service B having intended uses 2, 3, 4 and 5, and Service C having intended use 4, it would receive seven registration certificates. *

</div>
</div>

<div class="eudi-hlr" id="RPRC_10" markdown>
<div class="eudi-hlr__id">RPRC_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Relying Party SHALL distribute the registration certificates it received during registration to its Relying Party Instances. The Relying Party SHALL ensure that the registration certificate(s) sent to a Relying Party Instance contain the same Service identifier as the access certificate of that Relying Party Instance.

*Note: It is up to the Relying Party to determine if all of its Relying Party Instances need all of the registration certificates, or that some Relying Party Instances are used only for a subset of the Relying Party's Services, and consequently only need the registration certificates containing the corresponding Service identifiers.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_11" markdown>
<div class="eudi-hlr__id">RPRC_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The contents of a registration certificate issued to a Relying Party SHALL contain at least one of the following: a) the URL of a web form provided by the Relying Party, which Users can use to send data deletion requests, b) an e-mail address of the Relying Party, on which the Relying Party is prepared to receive data deletion requests from Users, c) a telephone number of the Relying Party, on which the Relying Party is prepared to receive data deletion requests from Users.

*Note: See [Topic 48][topic-48] for more information about data deletion requests.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_12" markdown>
<div class="eudi-hlr__id">RPRC_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The contents of a registration certificate issued to a Relying Party SHALL contain the name and country of the Data Protection Authority supervising the Relying Party. In addition, the registration certificate SHALL contain at least one of the following: a) the URL of a web form provided by the DPA, which Users can use to report suspicious attribute presentation requests. b) an e-mail address of the DPA, on which the DPA is prepared to receive reports about suspicious attribute presentation requests from Users, c) a telephone number of the DPA, on which the DPA is prepared to receive reports about suspicious attribute presentation requests from Users.

*Note: See [Topic 50][topic-50] for more information about reporting suspicious attribute presentation requests.*

</div>
</div>


##### C. Requirements on the issuance of registration certificates to PID Providers and Attestation Providers <!-- omit from toc -->

<div class="eudi-hlr" id="RPRC_13" markdown>
<div class="eudi-hlr__id">RPRC_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During the registration process for PID Providers, QEAA Providers, PuB-EAA Provider, or non-qualified EAA Providers, as specified in [Topic 27][topic-27], a Provider of registration certificates associated to the Member State Registrar SHALL create and sign or seal a separate registration certificate for each of the registered Services of the registering entity, and issue it to the registering entity. Each registration certificate SHALL comply with the requirements in the technical specification mentioned in RPRC_01.

</div>
</div>

<div class="eudi-hlr" id="RPRC_14" markdown>
<div class="eudi-hlr__id">RPRC_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider, QEAA Provider, PuB-EAA Provider, or non-qualified EAA Provider SHALL distribute the registration certificates it received during registration to all service supply points having an access certificate containing the same Service identifier.

*Note: A service supply point is a system at which a Wallet Unit can start the process of requesting and obtaining a PID or attestation.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_15" markdown>
<div class="eudi-hlr__id">RPRC_15<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The contents of a registration certificate issued to a PID Provider, a QEAA Provider, a PuB-EAA Provider, or a non-qualified EAA Provider SHALL contain the type(s) of attestation that the applicable Service of this entity intends to issue to Wallet Units.

</div>
</div>


##### D. Requirements on the presentation and verification of registration certificates of Relying Parties <!-- omit from toc -->

<div class="eudi-hlr" id="RPRC_16" markdown>
<div class="eudi-hlr__id">RPRC_16</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPRC_17" markdown>
<div class="eudi-hlr__id">RPRC_17<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL verify the format, authenticity, and validity of the registration certificate it received from a Relying Party in a presentation request, according to the technical specification meant in RPRC_01. If the certificate is absent, malformed, inauthentic, or expired, the Wallet Unit SHALL, when asking for User approval according to RPA_07, warn the User that it could not obtain or validate the information registered about the Relying Party and its Service. In addition, the Wallet Provider SHALL determine, based on its risk analysis and security policy, whether and under which conditions the Wallet Unit will allow the User to approve the presentation of the requested attributes despite specific failed verifications.

*Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>

<div class="eudi-hlr" id="RPRC_17a" markdown>
<div class="eudi-hlr__id">RPRC_17a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL verify that the registration certificate contains the same unique Relying Party identifier and the same Service identifier as the access certificate in the presentation request. If this is not the case, the Wallet Unit SHALL, when asking for User approval according to RPA_07, warn the User that it could not validate the information registered about the Relying Party and its Service. In addition, the Wallet Provider SHALL determine, based on its risk analysis and security policy, whether and under which conditions the Wallet Unit will allow the User to approve the presentation of the requested attributes despite this failed verification.

*Note: a) There are two ways in which a registration certificate can comply with this requirement: either the access certificate and the registration certificate were issued to the same entity, or the access certificate was issued to an intermediary (see [Topic 52][topic-52]), and the registration certificate indicates that the intermediated Relying Party uses the services of this intermediary. b) If the registration certificate does not comply with this requirement, a fraudulent entity acting as a Relying Party may be trying to use a registration certificate that was issued to another Relying Party.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_18" markdown>
<div class="eudi-hlr__id">RPRC_18</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPRC_18a" markdown>
<div class="eudi-hlr__id">RPRC_18a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPRC_19" markdown>
<div class="eudi-hlr__id">RPRC_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Relying Party Instance SHALL include a single registration certificate applicable for its current Service and intended use in each presentation request to a Wallet Unit, according to the applicable standard's extension mentioned in RPRC_20. The registration certificate SHALL be included in the request by value, not by reference. The Relying Party Instance SHALL do so both in proximity and remote presentation flows.

*Note: a) This ensures that no external requests are necessary to validate the Relying Party. b) A Relying Party Instance may be used for multiple Relying Party Services, provided it has a separate access certificate for each of these Services, see RPA_06 and Reg_10b.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_19a" markdown>
<div class="eudi-hlr__id">RPRC_19a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPRC_20" markdown>
<div class="eudi-hlr__id">RPRC_20<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Relying Party Instances and Wallet Units SHALL support the extension for [ISO/IEC 18013-5] or the extension for [OpenID4VP], as applicable. as specified in [ETSI TS 119 472-2] and amended by Annex 2 of (the amended) [CIR 2024/2982], for transferring a single Relying Party registration certificate from a Relying Party Instance to a Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="RPRC_20a" markdown>
<div class="eudi-hlr__id">RPRC_20a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPRC_21" markdown>
<div class="eudi-hlr__id">RPRC_21<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

After receiving a presentation request from a Relying Party, a Wallet Unit SHALL verify that all attributes requested in the request are included in the list of attributes in the registration certificate included in the same request. If the outcome of the verification is negative, the Wallet Unit SHALL, when asking for User approval according to RPA_07, warn the User that the Relying Party is requesting more information than it has registered. In addition, the Wallet Provider SHALL determine, based on its risk analysis and security policy, whether the Wallet Unit must a) enable the User to approve (or reject) the presentation of all requested attributes, including the non-registered ones, b) enable the User to approve (or reject) the presentation of the registered attributes only, or c) reject the presentation of all requested attributes.

*Note: This ensures that Wallet Providers comply with the 'general access policy' described in [CIR 2025/848].*

</div>
</div>


##### E. Requirements on the presentation and verification of registration certificates of PID Providers and Attestation Providers <!-- omit from toc -->

<div class="eudi-hlr" id="RPRC_22" markdown>
<div class="eudi-hlr__id">RPRC_22<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider or Attestation Provider SHALL include the registration certificate of the applicable Service in its Credential Issuer metadata used in the common OpenID4VCI protocol referenced in ISSU_01 and the extension thereof in [ETSI TS 119 472-3]. The registration certificate SHALL be included in the metadata by value, not by reference.

*Note: This ensures that no external requests are necessary to validate the PID Provider or Attestation Provider, and that issuance transactions are atomic and self-contained.*

</div>
</div>

<div class="eudi-hlr" id="RPRC_22a" markdown>
<div class="eudi-hlr__id">RPRC_22a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before requesting the issuance of a PID or an attestation, a Wallet Unit SHALL verify the format, authenticity, and validity of the registration certificate it obtained from a PID Provider's or Attestation Provider's metadata, according to the technical specification meant in RPRC_01. If the certificate is absent, malformed, inauthentic, or expired, the Wallet Unit SHALL warn the User that it could not obtain or validate the information registered about the PID Provider or Attestation Provider, and SHALL NOT request the issuance of a PID or attestation.

*Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>

<div class="eudi-hlr" id="RPRC_22b" markdown>
<div class="eudi-hlr__id">RPRC_22b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before requesting the issuance of a PID or an attestation, a Wallet Unit SHALL verify that the registration certificate contains the same unique identifier as the access certificate in the PID Provider's or Attestation Provider's metadata. If this is not the case, the Wallet Unit SHALL warn the User that it could not validate the information registered about the PID Provider or Attestation Provider, and SHALL NOT request the issuance of a PID or attestation 

*Note: a) If the registration certificate does not comply with this requirement, a fraudulent entity acting as a PID Provider or Attestation Provider may be trying to use a registration certificate that was issued to another PID Provider or Attestation Provider. b) The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>

<div class="eudi-hlr" id="RPRC_23" markdown>
<div class="eudi-hlr__id">RPRC_23<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before requesting the issuance of a PID or an attestation, a Wallet Unit SHALL verify that the type of attestation it wants to request from a PID Provider or Attestation Provider is included in the registration certificate of that Provider. If that is not the case, the Wallet Unit SHALL warn the User that the PID Provider or Attestation Provider is not registered for issuing the desired attestation type, and SHALL NOT request the issuance of a PID or attestation.

*Note: The requirement for Wallet Units to verify and validate registration certificates only applies as of 24 months after entry into force of the Regulation amending [CIR 2024/2982].*

</div>
</div>


[](){ #topic-48 }
