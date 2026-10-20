---
name: "hlr-16-signing-documents-with-a-wallet-unit"
description: "Use when working with EUDI high-level requirements for 'Signing documents with a Wallet Unit'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.10 Topic 16 - Signing documents with a Wallet Unit"
  - "A. Requirement for Wallet Providers <!-- omit from toc -->"
  - "B. Requirements for QTSPs <!-- omit from toc -->"
  - "C. Requirements for Relying Parties <!-- omit from toc -->"
  - "D. Requirements for the Commission <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~3201 -->

#### A.2.3.10 Topic 16 - Signing documents with a Wallet Unit

##### A. Requirement for Wallet Providers <!-- omit from toc -->

<div class="eudi-hlr" id="QES_01" markdown>
<div class="eudi-hlr__id">QES_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that each User has the possibility to receive a qualified certificate for Qualified Electronic Signatures, bound to a QSCD, that is either local, external, or remotely managed in relation to the Wallet Instance.

</div>
</div>

<div class="eudi-hlr" id="QES_02" markdown>
<div class="eudi-hlr__id">QES_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that each User who is a natural person has, at least for non-professional purposes, free-of-charge access to a Signature Creation Application which allows the creation of free-of-charge Qualified Electronic Signatures using the certificates referred to in QES_01. Wallet Providers SHALL ensure that: - The Signature Creation Application SHALL, as a minimum, be capable of signing or sealing User-provided data and Relying Party-provided data. - The Signature Creation Application SHALL be implemented as part of a Wallet Solution or external to it (by providers of trust services or by Relying Parties). - The Signature Creation Application SHALL be able to generate signatures or seals in formats compliant with at least the mandatory formats referred to in QES_08.

*Note: a) Signature Creation Application (SCA): see definition in [ETSI TS 119 432]. 2) If the SCA is external to the Wallet Solution, it may be for example a separate mobile application, or be hosted remotely, for instance by the QTSP or by a Relying Party.*

</div>
</div>

<div class="eudi-hlr" id="QES_03" markdown>
<div class="eudi-hlr__id">QES_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the use of the qualified certificate referred to in QES_01, Wallet Providers SHALL ensure that a Wallet Unit implements secure authentication of the User, as well as signature or seal invocation capabilities, as a part of a local, external or remote QSCD.

</div>
</div>

<div class="eudi-hlr" id="QES_04" markdown>
<div class="eudi-hlr__id">QES_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL enable their Wallet Units to interface with QSCDs using protocols and interfaces necessary for the implementation of secure User authentication and signature or seal functionality.

*Note: In a Relying Party-centric flow, the remote QTSP will likely be selected by the Relying Party, which implies the QSCD is managed by the remote QTSP. In a Wallet Unit-driven flow, the User should be able to choose the QSCD.*

</div>
</div>

<div class="eudi-hlr" id="QES_05" markdown>
<div class="eudi-hlr__id">QES_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL enable their Wallet Units to be used for User enrolment to a remote QES Provider (i.e., a QTSP offering remote QES), except where the Wallet Unit interfaces with local or external QSCDs.

</div>
</div>

<div class="eudi-hlr" id="QES_06" markdown>
<div class="eudi-hlr__id">QES_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that their Wallet Solution supports at least one of the following options for remote QES signature creation: - remote QES creation through secure authentication to a QTSP signature web portal, - remote QES creation channelled by the Wallet Unit, - remote QES creation channelled by a Relying Party.

</div>
</div>

<div class="eudi-hlr" id="QES_07" markdown>
<div class="eudi-hlr__id">QES_07</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="QES_08" markdown>
<div class="eudi-hlr__id">QES_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that their Wallet Units are able to create signatures or seals in accordance with the mandatory PAdES format as specified in [ETSI EN 319 142-1] V1.2.1 (2024-01). In addition, Wallet Providers SHOULD ensure that their Wallet Units are able to create signatures or seals in accordance with the following formats: - XAdES as specified in [ETSI EN 319 132-1] V1.3.1 (2024-07), - JAdES as specified in [ETSI TS 119 182-1] V1.2.1 (2024-07), - CAdES as specified in [ETSI EN 319 122-1] V1.3.1 (2023-06), and - ASiC as specified in [ETSI EN 319 162-1] V1.1.1 (2016-04) and [ETSI EN 319 162-2] V1.1.1 (2016-04).

</div>
</div>

<div class="eudi-hlr" id="QES_09" markdown>
<div class="eudi-hlr__id">QES_09</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="QES_10" markdown>
<div class="eudi-hlr__id">QES_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that, where the Signature Creation Application is implemented as part of the Wallet Unit and is used to generate signatures or seals of the representation of the document or data to be signed or sealed, the Wallet Unit presents the representation of the document or data to be signed or sealed to the User.

</div>
</div>

<div class="eudi-hlr" id="QES_11" markdown>
<div class="eudi-hlr__id">QES_11<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Where the Signature Creation Application is implemented as part of the Wallet Unit, a Wallet Unit SHALL compute the hash or digest of the document or data to be signed through its Signature Create Application component.

</div>
</div>

<div class="eudi-hlr" id="QES_12" markdown>
<div class="eudi-hlr__id">QES_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL be able to create a signature over a document or data to be signed, either by using a local QSCD or by interfacing with a remote QES Provider.

*Note: a local signing application is on-device. It may either be embedded in the Wallet Unit or be an external application.*

</div>
</div>

<div class="eudi-hlr" id="QES_13" markdown>
<div class="eudi-hlr__id">QES_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL provide a log of transactions related to qualified electronic signatures or seals generated by or through the Wallet Unit, allowing the User to view the history of previously signed data or documents, according to requirement DASH_04 in [Topic 19][topic-19].

*Note: If the signature is generated by a remote Signature Creation Application, the Wallet is at minimum used to authenticate the User to the remote QTSP and to obtain the User's consent for the usage of the private signing key. The logs then record information about these processes.*

</div>
</div>

<div class="eudi-hlr" id="QES_14" markdown>
<div class="eudi-hlr__id">QES_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL enable the User to explicitly authorise the creation of a qualified electronic signature or seal through their Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="QES_15" markdown>
<div class="eudi-hlr__id">QES_15<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In remote signature creation scenarios, a Wallet Unit SHALL verify that the qualified electronic signature or seal creation device is part of a qualified service, which is carried out by a qualified trust service provider.

</div>
</div>

<div class="eudi-hlr" id="QES_16" markdown>
<div class="eudi-hlr__id">QES_16<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHOULD support multiple-signing scenarios, where multiple signatories are required to sign the same document or data.

</div>
</div>

<div class="eudi-hlr" id="QES_17" markdown>
<div class="eudi-hlr__id">QES_17<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL provide a signature creation confirmation upon the creation of a qualified electronic signature, informing the User about the outcome of the signature creation process.

*Note: See also QES_17a.*

</div>
</div>

<div class="eudi-hlr" id="QES_17a" markdown>
<div class="eudi-hlr__id">QES_17a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the Signature Creation Application is external to the Wallet Unit, after the User authorises the usage of the private signing key, the Signature Creation Application SHALL return the outcome of the signature creation process to the Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="QES_18" markdown>
<div class="eudi-hlr__id">QES_18<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL configure at least one default qualified signing service in the Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="QES_19" markdown>
<div class="eudi-hlr__id">QES_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Wallet Providers SHALL ensure that, where the Signature Creation Application is implemented as part of the Wallet Unit, a Wallet Unit supports [ETSI TS 119 101] when using signing keys managed by the QSCD, whether locally, externally, or remotely in relation to the Wallet Instance.

</div>
</div>

<div class="eudi-hlr" id="QES_20" markdown>
<div class="eudi-hlr__id">QES_20</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="QES_21" markdown>
<div class="eudi-hlr__id">QES_21</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="QES_22" markdown>
<div class="eudi-hlr__id">QES_22</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


##### B. Requirements for QTSPs <!-- omit from toc -->

<div class="eudi-hlr" id="QES_23" markdown>
<div class="eudi-hlr__id">QES_23<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

QTSPs providing the remote QES part of a Wallet Solution SHALL support: 1. [ETSI TS 119 431-1] , 2. [ETSI TS 119 431-2] , 3. [ETSI TS 119 432]. Wallet Providers and QTSPs providing the remote QES part of a Wallet Solution SHALL comply with Sole Control Assurance Level (SCAL) 2 as defined in [CEN EN 419 241-1] .

</div>
</div>

<div class="eudi-hlr" id="QES_24" markdown>
<div class="eudi-hlr__id">QES_24<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

QTSPs providing the Signature Creation Application as part of the remote QES part of a Wallet Solution SHALL support [ETSI TS 119 101].

</div>
</div>


##### C. Requirements for Relying Parties <!-- omit from toc -->

<div class="eudi-hlr" id="QES_24a" markdown>
<div class="eudi-hlr__id">QES_24a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Relying Parties providing the Signature Creation Application in a Relying Party-centric flow SHALL support [ETSI TS 119 101].

</div>
</div>


##### D. Requirements for the Commission <!-- omit from toc -->

<div class="eudi-hlr" id="QES_25" markdown>
<div class="eudi-hlr__id">QES_25</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="QES_26" markdown>
<div class="eudi-hlr__id">QES_26</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>


[](){ #topic-18 }
