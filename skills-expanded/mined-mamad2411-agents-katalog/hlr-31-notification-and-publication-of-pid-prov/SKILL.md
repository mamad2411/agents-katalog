---
name: "hlr-31-notification-and-publication-of-pid-prov"
description: "Use when working with EUDI high-level requirements for 'Notification and publication of PID Provider, Wallet Provider, Attestation Provider, Access Certificate Authority, and Provider of registration certificates'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.20 Topic 31 - Notification and publication of PID Provider, Wallet Provider, Attestation Provider, Access Certificate Authority, and Provider of registration certificates"
  - "A. Generic requirements for notification <!-- omit from toc -->"
  - "B. Requirements for the notification of PID Providers <!-- omit from toc -->"
  - "C. Requirements for the notification of Wallet Providers <!-- omit from toc -->"
  - "D. Requirements for the notification of PuB-EAA Providers <!-- omit from toc -->"
  - "E. Requirements for the notification of Access Certificate Authorities and Providers of registration certificates <!-- omit from toc -->"
  - "F. Requirements for the publication of LoTEs compiled by the Commission <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~6311 -->

#### A.2.3.20 Topic 31 - Notification and publication of PID Provider, Wallet Provider, Attestation Provider, Access Certificate Authority, and Provider of registration certificates

##### A. Generic requirements for notification <!-- omit from toc -->

<div class="eudi-hlr" id="GenNot_01" markdown>
<div class="eudi-hlr__id">GenNot_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Member States SHALL notify all PID Providers, PuB-EAA Providers, Wallet Providers, Access Certificate Authorities, and Providers of registration certificates to the European Commission, using a common system provided by the Commission, complying with all relevant requirements in[Technical Specification 2](../../technical-specifications/ts2-notification-publication-provider-information.md).

</div>
</div>

<div class="eudi-hlr" id="GenNot_02" markdown>
<div class="eudi-hlr__id">GenNot_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In addition to [Technical Specification 2][ts2] referred to in GenNot_01, the European Commission SHALL establish standard operating procedures for the notification of a PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authority, or Provider of registration certificates to the Commission.

*Note: The outcome of the notification procedure is the publication of the information notified by the Member State according to [Article 5a](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e1347-1-1) (18) in a machine and human readable manner using the common system mentioned in Section H, TLPub_01.*

</div>
</div>

<div class="eudi-hlr" id="GenNot_03" markdown>
<div class="eudi-hlr__id">GenNot_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The common system mentioned in GenNot_01 SHALL enable: - A secure notification channel between Member States and the Commission for all notifications. - A notification, verification, and publication process and associated validation steps (with follow-up and monitoring) at the Commission side. - Collected data to be processed, consolidated, signed or sealed, and published in both a machine-processable LoTE and in a human-readable format, manually and/or automatically using e.g. a web service and/or API.

</div>
</div>

<div class="eudi-hlr" id="GenNot_04" markdown>
<div class="eudi-hlr__id">GenNot_04</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="GenNot_05" markdown>
<div class="eudi-hlr__id">GenNot_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In addition to [Technical Specification 2][ts2] referred to in GenNot_01, the European Commission SHALL establish standard operating procedures for the suspension or cancellation of a PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authority, or Provider of registration certificates. These operating procedures SHALL include unambiguous conditions for suspension or cancellation. As an outcome of the suspension or cancellation procedure, the Commission SHALL change the status of the suspended or cancelled PID Provider, PuB-EAA Provider, Wallet Provider, Access Certificate Authority or Provider of registration certificates in the respective LoTE to Invalid.

</div>
</div>


##### B. Requirements for the notification of PID Providers <!-- omit from toc -->

<div class="eudi-hlr" id="PPNot_01" markdown>
<div class="eudi-hlr__id">PPNot_01</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="PPNot_02" markdown>
<div class="eudi-hlr__id">PPNot_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The common set of information to be notified about a PID Provider SHALL include at least: 1. Identification data: i. MS/Country of establishment, ii. Name as registered in an official record, iii. Where applicable: a. A business registration number from an official record, b. Identification data from that official record. 2. PID Provider trust anchors, i.e., public keys and name as per point 1) ii) above, supporting the authentication of PIDs issued by the PID Provider, 3. If applicable, trust anchors for PID revocation lists, i.e., public keys and name supporting the authentication of any Attestation Status Lists or Attestation Revocation Lists used to revoke PIDs issued by the PID Provider. 4. Trust anchors of Access Certificate Authorities for PID Providers, i.e., public keys and CA name, supporting the authentication of the PID Provider by Wallet Units at the service supply point(s) listed per point  5. below. 5. Service supply point(s), i.e., the URL(s) at which a Wallet Unit can start the process of requesting and obtaining a PID. 6. If applicable, the URL at which Relying Parties and other entities can retrieve the relevant Attestation Status Lists or Attestation Revocation Lists.

*Note: a) Regarding point 3 above, see section 6.3.2.4 of the ARF main document. b) Relating to point 4: PID Provider Access Certificate Authority trust anchors are notified separately from the Access Certificate Authority for Relying Parties (see Section G below), since PID Providers are -legally speaking- not Relying Parties. b) For the concept of an Access Certificate Authority, see also [Topic 27][topic-27]] and [Section 6.3.2 of the ARF main document][632-pid-provider-or-attestation-provider-registration-and-notification]. c) Regarding point 6: This could be the domain name only, as the full URL containing the ASL or ARL relevant for an individual PID will anyway be included in that PID.*

</div>
</div>

<div class="eudi-hlr" id="PPNot_03" markdown>
<div class="eudi-hlr__id">PPNot_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers SHALL ensure that all PIDs they issue can be authenticated using the PID Provider trust anchors notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="PPNot_03a" markdown>
<div class="eudi-hlr__id">PPNot_03a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers SHALL ensure that all Attestation Status Lists or Attestation Revocation Lists used to revoke their PIDs can be authenticated using the trust anchors for PID revocation lists notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="PPNot_04" markdown>
<div class="eudi-hlr__id">PPNot_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers SHALL ensure that their access certificates can be authenticated using the applicable Access Certificate Authority trust anchors notified to the Commission.

*Note: [Topic 6][topic-6]] describes how access certificates will be used.*

</div>
</div>

<div class="eudi-hlr" id="PPNot_05" markdown>
<div class="eudi-hlr__id">PPNot_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Units, Relying Parties, and other relevant actors SHALL accept PID Provider trust anchors and the trust anchors for PID revocation lists because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled PID Provider LoTE, which is sealed by the Commission.

</div>
</div>

<div class="eudi-hlr" id="PPNot_06" markdown>
<div class="eudi-hlr__id">PPNot_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Units and other relevant actors SHALL accept Access Certificate Authority trust anchors because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled LoTE, which is signed or sealed by the Commission.

</div>
</div>

<div class="eudi-hlr" id="PPNot_07" markdown>
<div class="eudi-hlr__id">PPNot_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The format of a PID Provider LoTE SHALL comply with [ETSI TS 119 602], including Annex D.

</div>
</div>


##### C. Requirements for the notification of Wallet Providers <!-- omit from toc -->

<div class="eudi-hlr" id="WPNot_01" markdown>
<div class="eudi-hlr__id">WPNot_01</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WPNot_02" markdown>
<div class="eudi-hlr__id">WPNot_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The common set of information to be notified about a Wallet Provider SHALL include: 1. Identification data: i. MS/Country of establishment, ii. Name as registered in an official record, iii. Where applicable: a. Business registration number from an official record, and b. Identification data from the official record. 2. Wallet Provider trust anchors, i.e., public keys and name as per point 1. b. above, supporting the authentication of Key Attestations and Wallet Instance Attestations issued by the Wallet Provider. 3. Trust anchors for WIA and KA revocation lists, i.e., public keys and name supporting the authentication of any Attestation Status Lists used to revoke WIAs and KAs issued by the Wallet Provider. 4. Name and reference number of the certified Wallet Solution(s) provided by the Wallet Provider. 5. The URL at which PID Providers, Attestation Providers, and other entities can retrieve the relevant Attestation Status Lists for WIAs and KAs. 

*Note: a) See [Topic 9][topic-9]] and [Topic 38][topic-38]] for the definition of the KA and WIA. b) A Wallet Provider does not need an access certificate to interact with Wallet Units. c) Regarding point 3, see section 6.3.2.4 of the ARF main document. d) Regarding point 5: This could be the domain name only, as the full URL containing the ASL relevant for an individual WIA or KA will anyway be included in that WIA or KA.*

</div>
</div>

<div class="eudi-hlr" id="WPNot_03" markdown>
<div class="eudi-hlr__id">WPNot_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that all WIAs and KAs they issue can be authenticated using the trust anchors notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="WPNot_03a" markdown>
<div class="eudi-hlr__id">WPNot_03a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that all Attestation Status Lists used to revoke their WIAs and KAs can be authenticated using the trust anchors for WIA and KA revocation lists notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="WPNot_04" markdown>
<div class="eudi-hlr__id">WPNot_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PID Providers, Attestation Providers, and other relevant actors SHALL accept Wallet Provider trust anchors and the trust anchors for WIA and KA revocation lists because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled Wallet Provider LoTE, which is sealed by the Commission.

</div>
</div>

<div class="eudi-hlr" id="WPNot_05" markdown>
<div class="eudi-hlr__id">WPNot_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The format of a Wallet Provider LoTE SHALL comply with [ETSI TS 119 602], including Annex E.

</div>
</div>

<div class="eudi-hlr" id="WPNot_06" markdown>
<div class="eudi-hlr__id">WPNot_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Wallet Provider is cancelled (see requirement GenNot_05 above), that Wallet Provider SHALL immediately revoke all of its Wallet Instances and all associated WSCDs and keystores, in accordance with the requirements in [Topic 38][topic-38]. If a Wallet Provider is suspended, that Wallet Provider and the Member State SHALL agree on the necessary precautionary measures that need to be taken, which MAY include the immediate revocation of the Wallet Instances and WSCDs or keystores for all or some of its valid Wallet Units.

</div>
</div>


##### D. Requirements for the notification of PuB-EAA Providers <!-- omit from toc -->

<div class="eudi-hlr" id="PuBPNot_01" markdown>
<div class="eudi-hlr__id">PuBPNot_01</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="PuBPNot_02" markdown>
<div class="eudi-hlr__id">PuBPNot_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The common set of information to be notified by Member States about PuB-EAA Providers SHALL include at least: 1. Identification data: i. MS/Country of establishment, ii. Name as registered in an official record, iii. Where applicable: a. Registration number as in official record, and b. Official record identification data. iv. Identification data of the Union or national law under which a. Either the PuB-EAA Provider is established as the responsible body for the Authentic Source based on which the electronic attestation of attributes is issued, or b. The PuB-EAA Provider is the body designated to act on behalf of the responsible body referred to in point 1. iv. a. v.The conformity assessment report issued by a conformity assessment body, confirming that the requirements set out in paragraphs 1, 2 and 6 of [Article 45f](https://eur-lex.europa.eu/legal-content/EN/ALL/?uri=CELEX:32024R1183#d1e3902-1-1) are met. 2. PuB-EAA Provider trust anchors, i.e., public keys and name as per point 1) ii) above, supporting the authentication of PuB-EAAs issued by the PuB-EAA Provider, 3. If applicable, trust anchors for PuB-EAA revocation lists, i.e., public keys and name supporting the authentication of any Attestation Status Lists or Attestation Revocation Lists used to revoke PuB-EAAs issued by the PuB-EAA Provider. 4. Service supply point(s), i.e., the URL(s) at which a Wallet Unit can start the process of requesting and obtaining a PuB-EAA from the PuB-EAA Provider. 5. If applicable, the URL at which Relying Parties and other entities can retrieve the relevant Attestation Status Lists or Attestation Revocation Lists.

*Note: c) Regarding point 3, see section 6.3.2.4 of the ARF main document. d) Regarding point 5: This could be the domain name only, as the full URL containing the ASL or ARL relevant for an individual PuB-EAA will anyway be included in that PuB-EAA.*

</div>
</div>

<div class="eudi-hlr" id="PuBPNot_03" markdown>
<div class="eudi-hlr__id">PuBPNot_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The format of the PuB-EAA Provider LoTE SHALL comply with [ETSI TS 119 602], including Annex H.

</div>
</div>

<div class="eudi-hlr" id="PuBPNot_04" markdown>
<div class="eudi-hlr__id">PuBPNot_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PuB-EAA Providers SHALL ensure that all PuB-EAAs they issue can be authenticated using the trust anchors notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="PuBPNot_05" markdown>
<div class="eudi-hlr__id">PuBPNot_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

PuB-EAA Providers SHALL ensure that all Attestation Status Lists and Attestation Revocation Lists used to revoke their PuB-EAAs can be authenticated using the trust anchors for PuB-EAA revocation lists notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="PuBPNot_06" markdown>
<div class="eudi-hlr__id">PuBPNot_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Relying Parties and other relevant actors SHALL accept PuB-EAA Provider trust anchors and the trust anchors for PuB-EAA Provider revocation lists because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled PuB-EAA Provider LoTE, which is sealed by the Commission.

</div>
</div>


##### E. Requirements for the notification of Access Certificate Authorities and Providers of registration certificates <!-- omit from toc -->

<div class="eudi-hlr" id="RPACANot_01" markdown>
<div class="eudi-hlr__id">RPACANot_01</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPACANot_02" markdown>
<div class="eudi-hlr__id">RPACANot_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The common set of information to be notified about an Access Certificate Authority or a Provider of registration certificates SHALL include: 1. Identification data: i) Member State or country of establishment, ii) Name as registered in an official record, iii) Where applicable: - A business registration number from an official record, - Identification data from that official record. 2. Trust anchors of the Access Certificate Authority or Provider of registration certificates, i.e., public keys and name as per point 1) ii), supporting the authentication of access certificates and registration certificates by Wallet Units. 3.Trust anchors for access certificate or registration certificate revocation lists, i.e., public keys and name supporting the authentication of any lists used to revoke access certificates or registration certificates issued by the Access Certificate Authority or Provider of registration certificates. 4. If applicable, the URL at which Relying Parties and other entities can retrieve the relevant CRL.

*Note: Regarding point 4: This could be the domain name only, as the full URL containing the CRL relevant for an individual certificate will anyway be included in that certificate.*

</div>
</div>

<div class="eudi-hlr" id="RPACANot_03" markdown>
<div class="eudi-hlr__id">RPACANot_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An Access Certificate Authority SHALL ensure that the access certificates it issues to Relying Parties, PID Providers, QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers can be authenticated using the trust anchors notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="RPACANot_03a" markdown>
<div class="eudi-hlr__id">RPACANot_03a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Provider of registration certificates SHALL ensure that the registration certificates it issues to Relying Parties, PID Providers, QEAA Providers, PuB-EAA Providers, and non-qualified EAA Providers can be authenticated using the trust anchors notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="RPACANot_03b" markdown>
<div class="eudi-hlr__id">RPACANot_03b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Access Certificate Authorities or Providers of registration certificates SHALL ensure that all lists used to revoke their access certificates and registration certificates can be authenticated using the trust anchors for revocation lists notified to the Commission.

</div>
</div>

<div class="eudi-hlr" id="RPACANot_04" markdown>
<div class="eudi-hlr__id">RPACANot_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The trust anchors of Access Certificate Authorities and Providers of registration certificates, as well as their CRL trust anchors, SHALL be accepted because of their secure notification by the Member States to the Commission and by their publication in the corresponding Commission-compiled LoTEs, which are signed or sealed by the Commission.

</div>
</div>

<div class="eudi-hlr" id="RPACANot_05" markdown>
<div class="eudi-hlr__id">RPACANot_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The format of a LoTE for Access Certificate Authorities SHALL comply with [ETSI TS 119 602], including Annex F.

</div>
</div>

<div class="eudi-hlr" id="RPACANot_05a" markdown>
<div class="eudi-hlr__id">RPACANot_05a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The format of a LoTE for Providers of registration certificates SHALL comply with [ETSI TS 119 602], including Annex G.

</div>
</div>

<div class="eudi-hlr" id="RPACANot_06" markdown>
<div class="eudi-hlr__id">RPACANot_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If an Access Certificate Authority is suspended or cancelled (see requirement GenNot_05 above), that Access Certificate Authority SHALL immediately revoke all of its temporally valid access certificates.

*Note: This implies that if an intermediary obtained its access certificates from an Access Certificate Authority that is suspended or cancelled, any intermediated Relying Party depending on that intermediary will not be able to request attributes from Wallet Units, even though its registration is still valid. Such an intermediated Relying Party will either have to transit to another intermediary (which has access certificates issued by an active Access Certification Authority) or wait until the original intermediary obtains new access certificates either from another Access CA or from the original one, once that CA can continue its operations.*

</div>
</div>

<div class="eudi-hlr" id="RPACANot_07" markdown>
<div class="eudi-hlr__id">RPACANot_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Provider of registration certificates is suspended or cancelled (see requirement GenNot_05 above), that Provider SHALL immediately revoke all of its valid registration certificates (if any). Moreover, the corresponding Registrar SHALL prohibit all access to the registry entries published online per Reg_03 and Reg_04.

</div>
</div>


##### F. Requirements for the publication of LoTEs compiled by the Commission <!-- omit from toc -->

<div class="eudi-hlr" id="TLPub_01" markdown>
<div class="eudi-hlr__id">TLPub_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The European Commission SHALL establish technical specifications for the system enabling the publication by the Commission of the information notified by the Member States regarding PID Providers, Wallet Providers, PuB-EAA Providers, Access Certificate Authorities, and Providers of registration certificates.

</div>
</div>

<div class="eudi-hlr" id="TLPub_02" markdown>
<div class="eudi-hlr__id">TLPub_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The European Commission SHALL establish technical specifications for the set of information to be published about PID Providers, Wallet Providers, PuB-EAA Providers, Access Certificate Authorities and Providers of registration certificates, based on the information notified by the Member States.

*Note: The information to be published MAY be different from the information to be notified for each of these entities.*

</div>
</div>

<div class="eudi-hlr" id="TLPub_03" markdown>
<div class="eudi-hlr__id">TLPub_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The publication of the information referred to in TLPub_01 SHALL take place over a secure channel protecting the authenticity and integrity of the published information.

</div>
</div>

<div class="eudi-hlr" id="TLPub_04" markdown>
<div class="eudi-hlr__id">TLPub_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The technical system mentioned in TLPub_01 SHALL NOT require authentication or prior registration and authorisation of any entity wishing to retrieve the published information.

</div>
</div>

<div class="eudi-hlr" id="TLPub_05" markdown>
<div class="eudi-hlr__id">TLPub_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The information referred to in TLPub_01 SHALL be published in an electronically signed or sealed form that is suitable for automated processing, and in a human-readable format, e.g., through introspection and display facilities, over an authenticated channel.

</div>
</div>

<div class="eudi-hlr" id="TLPub_06" markdown>
<div class="eudi-hlr__id">TLPub_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Commission SHALL publish in the OJEU the locations of the LoTEs for PID Providers, PuB-EAA Providers, Wallet Providers, Access Certificate Authorities, and Providers of registration certificates.

</div>
</div>

<div class="eudi-hlr" id="TLPub_07" markdown>
<div class="eudi-hlr__id">TLPub_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Commission SHALL publish in the OJEU the trust anchors to be used for verifying the signature or seal mentioned in TLPub_05.

</div>
</div>

<div class="eudi-hlr" id="TLPub_08" markdown>
<div class="eudi-hlr__id">TLPub_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

As part of the specifications referred to in TLPub_01, the European Commission SHALL establish technical specifications for ensuring the availability and authenticity of the full history regarding the information notified about PID Providers, Wallet Providers, PuB-EAA Providers, Access Certificate Authorities, and Providers of registration certificates.

</div>
</div>


[](){ #topic-34 }
