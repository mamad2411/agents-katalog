---
name: "hlr-27-registration-of-pid-providers-providers-"
description: "Use when working with EUDI high-level requirements for 'Registration of PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.16 Topic 27 - Registration of PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties"
  - "A. General requirements for Member State registration processes <!-- omit from toc -->"
  - "B. General requirements for the issuance of access certificates <!-- omit from toc -->"
  - "C. Requirements for the registration of PID Providers <!-- omit from toc -->"
  - "D. Requirements for the registration of Attestation Providers <!-- omit from toc -->"
  - "E. Requirements for the registration of Relying Parties <!-- omit from toc -->"
  - "F. Requirements for the contents of access certificates <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~5419 -->

#### A.2.3.16 Topic 27 - Registration of PID Providers, Providers of QEAAs, PuB-EAAs, and non-qualified EAAs, and Relying Parties

##### A. General requirements for Member State registration processes <!-- omit from toc -->

<div class="eudi-hlr" id="Reg_01" markdown>
<div class="eudi-hlr__id">Reg_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL provide processes and mechanisms for PID Providers, QEAA Providers, PuB-EAA Providers, non-qualified EAA Providers, and Relying Parties to register in a registry.

*Note: Member States may choose to implement a single registry for all these roles, or a separate registry for each of these roles.*

</div>
</div>

<div class="eudi-hlr" id="Reg_01a" markdown>
<div class="eudi-hlr__id">Reg_01a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL register a common set of data about a) PID Providers, b) QEAA Providers, c) PuB-EAA Providers, d) non-qualified EAA Providers. and e) Relying Parties, according to the relevant requirements in [Technical Specification 6](../../technical-specifications/ts6-common-set-of-rp-information-to-be-registered.md).

*Note: For PID Providers, QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers, the common set of data specified in [Technical Specification 6][ts6] include the attestation type(s) that the provider intends to issue to Wallet Units.*

</div>
</div>

<div class="eudi-hlr" id="Reg_01b" markdown>
<div class="eudi-hlr__id">Reg_01b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL collect the following information only for the purpose of transparency and SHALL NOT apply any pre-authorisation process on it: i) Contact information of the registering entity, ii) description of its services, iii) Attributes registered for each intended use (for Relying Parties), or types of attestation registered (for PID Providers and Attestation Providers), iv) Description of each intended use (for Relying Parties).

</div>
</div>

<div class="eudi-hlr" id="Reg_02" markdown>
<div class="eudi-hlr__id">Reg_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL make publicly available all necessary details and documentation about the registration processes for their registry.

</div>
</div>

<div class="eudi-hlr" id="Reg_03" markdown>
<div class="eudi-hlr__id">Reg_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL publish the registry entries online, in a sealed or signed machine-readable common format suitable for automated processing, according to the relevant requirements in [Technical Specification 5](../../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md), for the purpose of transparency to Users and other stakeholders.

</div>
</div>

<div class="eudi-hlr" id="Reg_04" markdown>
<div class="eudi-hlr__id">Reg_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL make the registry entries available online, in a human-readable format. The website used for this purpose SHALL use a secure channel protecting the authenticity and integrity of the information in the registry during transport. Member States SHALL NOT require authentication or prior registration and authorisation of any person wishing to retrieve the information in the registry.

</div>
</div>

<div class="eudi-hlr" id="Reg_05" markdown>
<div class="eudi-hlr__id">Reg_05</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Reg_06" markdown>
<div class="eudi-hlr__id">Reg_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL support the common API specified in [Technical Specification 5](../../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md) to enable automated retrieval of registry entries from the Member States' registries.

*Note: [Technical Specification 5][ts5] specifies the use of a secure channel protecting the authenticity and integrity of the information in the registry during transport, and does not require authentication or prior registration and authorisation of any entity wishing to retrieve the information in the registry.*

</div>
</div>

<div class="eudi-hlr" id="Reg_07" markdown>
<div class="eudi-hlr__id">Reg_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL enable a registered PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party to update the information registered on it, using a process comparable to the original registration process. For Relying Parties, this SHALL be possible using the API or user interface mentioned in Reg_24.

</div>
</div>

<div class="eudi-hlr" id="Reg_08" markdown>
<div class="eudi-hlr__id">Reg_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A registered PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party SHALL make any updates necessary to ensure the continued correctness of the registered information without undue delay.

</div>
</div>

<div class="eudi-hlr" id="Reg_09" markdown>
<div class="eudi-hlr__id">Reg_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL log all changes made on the information registered regarding a PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party, including at least initial registration, updates, deletion of information, and suspension or cancellation.

</div>
</div>


##### B. General requirements for the issuance of access certificates <!-- omit from toc -->

<div class="eudi-hlr" id="Reg_10" markdown>
<div class="eudi-hlr__id">Reg_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL ensure that an Access Certificate Authority notified according to [Topic 31][topic-31]] issues one or more access certificates to all PID Providers, QEAA Providers, PuB-EAA Providers, non-qualified EAA Providers and Relying Parties registered in one of the Member State's registries.

*Note: To be able to authenticate towards Wallet Units, each Relying Party Instance of a Relying Party and each service supply point of a PID Provider or Attestation Provider needs a separate access certificate, where the private key corresponding to the public key in the certificate is managed in the hardware and software of the Relying Party Instance or service supply point.*

</div>
</div>

<div class="eudi-hlr" id="Reg_10a" markdown>
<div class="eudi-hlr__id">Reg_10a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A registering entity SHALL register one or more Services, and SHALL receive at least one access certificate for each registered Service, complying with Reg_33 and Reg_34.

*Note: a) If the registering entity registers only one Service, all of its access certificates will contain an identical Service identifier and Service trade name. b) A single Relying Party Instance or service supply point may receive multiple access certificates, corresponding to multiple Services of the same Relying Party or Attestation Provider. This would enable the entity to use the same Relying Party Instance or supply point for multiple Services.*

</div>
</div>

<div class="eudi-hlr" id="Reg_10b" markdown>
<div class="eudi-hlr__id">Reg_10b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When issuing an access certificate to a PID Provider, Attestation Provider, or Relying Party, an Access Certificate Authority SHALL also send the signing certificate and, if present, any intermediate certificate(s) leading up to the corresponding trust anchor of the Access CA in the respective LoTE published by the Commission.

</div>
</div>

<div class="eudi-hlr" id="Reg_10c" markdown>
<div class="eudi-hlr__id">Reg_10c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The registering entity SHALL receive at least one registration certificate for each registered Service, complying with RPRC_07a.

*Note: If the registering entity registers only one Service, all of its registration certificates will contain an identical Service identifier and Service trade name.*

</div>
</div>

<div class="eudi-hlr" id="Reg_10d" markdown>
<div class="eudi-hlr__id">Reg_10d<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Relying Party SHALL register which of its registered intended uses are applicable to each of its registered Services.

*Note: Another way to phrase this is to say that the Relying Party must register the intended use(s) of each of it registered Services separately.*

</div>
</div>

<div class="eudi-hlr" id="Reg_10e" markdown>
<div class="eudi-hlr__id">Reg_10e<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A PID Provider or Attestation Provider SHALL register which type(s) of attestation each of its registered Services intends to issue to Wallet Units.

</div>
</div>

<div class="eudi-hlr" id="Reg_11" markdown>
<div class="eudi-hlr__id">Reg_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL ensure that the issuance process of access certificates by their notified Access Certificate Authority(s) complies with [ETSI TS 119 411-8]. An Access Certificate Authority SHALL have a policy governing all aspects of access certificate issuance and management complying with this standard. 

</div>
</div>

<div class="eudi-hlr" id="Reg_12" markdown>
<div class="eudi-hlr__id">Reg_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Access CA SHALL be able to revoke an access certificate, if it has a validity period of longer than 24 hours

</div>
</div>

<div class="eudi-hlr" id="Reg_13" markdown>
<div class="eudi-hlr__id">Reg_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Access CA SHALL have a policy specifying under which conditions an access certificate it issued will be revoked.

</div>
</div>

<div class="eudi-hlr" id="Reg_14" markdown>
<div class="eudi-hlr__id">Reg_14</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Reg_15" markdown>
<div class="eudi-hlr__id">Reg_15</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Reg_16" markdown>
<div class="eudi-hlr__id">Reg_16</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Reg_17" markdown>
<div class="eudi-hlr__id">Reg_17</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Reg_18" markdown>
<div class="eudi-hlr__id">Reg_18</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


##### C. Requirements for the registration of PID Providers <!-- omit from toc -->

<div class="eudi-hlr" id="Reg_19" markdown>
<div class="eudi-hlr__id">Reg_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL approve a PID Provider according to a well-defined policy before including it in its PID Provider Registry. To that end, a Member State SHALL define specific vetting processes and rules of acceptance for inclusion of PID Providers in its Registry.

</div>
</div>

<div class="eudi-hlr" id="Reg_20" markdown>
<div class="eudi-hlr__id">Reg_20<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL identify PID Providers at a level of confidence proportionate to the risk arising from the potential harm a fraudulent PID Provider could cause to Users and other stakeholders in the EUDI Wallet ecosystem.

</div>
</div>

<div class="eudi-hlr" id="Reg_20a" markdown>
<div class="eudi-hlr__id">Reg_20a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Registrar SHALL provide a method to suspend or cancel a registered PID Provider.

</div>
</div>

<div class="eudi-hlr" id="Reg_20b" markdown>
<div class="eudi-hlr__id">Reg_20b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Registrar SHALL have a policy for the suspension or cancellation of a registered PID Provider, which SHALL specify that a PID Provider is suspended or cancelled at least on request of the PID Provider or of a competent national authority.

</div>
</div>


##### D. Requirements for the registration of Attestation Providers <!-- omit from toc -->

<div class="eudi-hlr" id="Reg_21" markdown>
<div class="eudi-hlr__id">Reg_21<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL approve an Attestation Provider according to a well-defined policy before including it in its Attestation Provider Registry. To that end, a Member State SHALL define specific vetting processes and rules of acceptance for inclusion of Attestation Providers in its Registry. These processes and rules SHOULD consider any relevant differences between QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers.

</div>
</div>

<div class="eudi-hlr" id="Reg_22" markdown>
<div class="eudi-hlr__id">Reg_22<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL identify Attestation Providers (i.e., QEAA Providers, PuB-EAA Providers and non-qualified EAA Providers) at a level of confidence proportionate to the risk arising from the potential harm a fraudulent Attestation Provider could cause to Users and other stakeholders in the EUDI Wallet ecosystem.

</div>
</div>

<div class="eudi-hlr" id="Reg_22a" markdown>
<div class="eudi-hlr__id">Reg_22a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Registrar SHALL provide a method to suspend or cancel a registered Attestation Provider.

</div>
</div>

<div class="eudi-hlr" id="Reg_22b" markdown>
<div class="eudi-hlr__id">Reg_22b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Registrar SHALL have a policy for the suspension or cancellation of a registered Attestation Provider, which SHALL specify that an Attestation Provider is suspended or cancelled at least on request of the Attestation Provider or of a competent national authority.

</div>
</div>


##### E. Requirements for the registration of Relying Parties <!-- omit from toc -->

<div class="eudi-hlr" id="Reg_23" markdown>
<div class="eudi-hlr__id">Reg_23</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Reg_24" markdown>
<div class="eudi-hlr__id">Reg_24<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL enable a Relying Party to register remotely, using an API or user interface.

</div>
</div>

<div class="eudi-hlr" id="Reg_25" markdown>
<div class="eudi-hlr__id">Reg_25<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL identify a Relying Party at a level of confidence proportionate to the risk arising from the potential harm a fraudulent Relying Party could cause to Users and other stakeholders in the EUDI Wallet ecosystem.

</div>
</div>

<div class="eudi-hlr" id="Reg_26" markdown>
<div class="eudi-hlr__id">Reg_26<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

With respect to Reg_25, a Member State SHALL consider whether a registering entity intends to act as an intermediary.

*Note: According to the [European Digital Identity Regulation], an intermediary is a Relying Party.*

</div>
</div>

<div class="eudi-hlr" id="Reg_27" markdown>
<div class="eudi-hlr__id">Reg_27</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Reg_28" markdown>
<div class="eudi-hlr__id">Reg_28</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="Reg_29" markdown>
<div class="eudi-hlr__id">Reg_29<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Member State SHALL have a policy for the cancellation of a registered Relying Party, which SHALL specify that a Relying Party is cancelled at least on request of the Relying Party or of a competent national authority.

</div>
</div>

<div class="eudi-hlr" id="Reg_30" markdown>
<div class="eudi-hlr__id">Reg_30</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


##### F. Requirements for the contents of access certificates <!-- omit from toc -->

<div class="eudi-hlr" id="Reg_31" markdown>
<div class="eudi-hlr__id">Reg_31<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An access certificate SHALL contain a trade name for the entity (i.e., the PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party), in a format suitable for presenting to a User. This name SHALL be identical to the name for the entity registered according to [Technical Specification 6][ts6] and included in the entity's registration certificate(s) according to RPRC_06.

</div>
</div>

<div class="eudi-hlr" id="Reg_32" markdown>
<div class="eudi-hlr__id">Reg_32<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An access certificate SHALL contain an EU-wide unique identifier for the entity (i.e., the PID Provider, QEAA Provider, PuB-EAA Provider, non-qualified EAA Provider, or Relying Party), which SHALL be identical to the identifier for the entity registered according to [Technical Specification 6](../../technical-specifications/ts6-common-set-of-rp-information-to-be-registered.md) and included in the entity's registration certificate(s) according to RPRC_07.

</div>
</div>

<div class="eudi-hlr" id="Reg_32a" markdown>
<div class="eudi-hlr__id">Reg_32a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The trade name meant in Reg_31 and the identifier meant in Reg_32 SHALL be the same in all access certificates issued to a given entity.

</div>
</div>

<div class="eudi-hlr" id="Reg_33" markdown>
<div class="eudi-hlr__id">Reg_33<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An access certificate SHALL contain a Relying Party Service identifier, which SHALL be provided by the registering entity according to [Technical Specification 5](../../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md) and [Technical Specification 6](../../technical-specifications/ts6-common-set-of-rp-information-to-be-registered.md), and SHALL be unique within the scope of that entity. Moreover, it SHALL be included in the entity's registration certificate according to RPRC_07a.

</div>
</div>

<div class="eudi-hlr" id="Reg_34" markdown>
<div class="eudi-hlr__id">Reg_34<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An access certificate SHALL contain a trade name for the Relying Party Service, which SHALL be provided by the registering entity according to [Technical Specification 5](../../technical-specifications/ts5-common-formats-and-api-for-rp-registration-information.md) and [Technical Specification 6](../../technical-specifications/ts6-common-set-of-rp-information-to-be-registered.md), and SHALL be suitable for presenting to a User.

</div>
</div>

<div class="eudi-hlr" id="Reg_34a" markdown>
<div class="eudi-hlr__id">Reg_34a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the subject of the access certificate is an intermediary (see [Topic 52][topic-52]), the 'association to the wallet-relying party that is relying upon the intermediary ' mentioned in Annex I (16) of [CIR 2025/848] (and referenced in Annex IV, point 3(k) of that CIR) SHALL consist of the unique identifier of this Relying Party as meant in requirement Reg_32 and its Relying Party Service identifier as meant in Reg_33.

*Note: a) This implies that an intermediary receives a separate set of access certificates for each of its intermediated Relying Parties. b) The association is also included in the registration certificates of the intermediated Relying Parties, see RPRC_04.*

</div>
</div>

<div class="eudi-hlr" id="Reg_35" markdown>
<div class="eudi-hlr__id">Reg_35<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The access certificate format SHALL provide for the data elements to carry the elements mentioned in Reg_31 - Reg_34a.

*Note: The generic X.509 certificate structure has multiple suitable data elements which could be designated for these elements. *

</div>
</div>


[](){ #topic-28 }
