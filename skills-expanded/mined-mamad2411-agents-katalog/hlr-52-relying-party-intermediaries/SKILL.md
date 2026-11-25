---
name: "hlr-52-relying-party-intermediaries"
description: "Use when working with EUDI high-level requirements for 'Relying Party intermediaries'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.30 Topic 52 - Relying Party intermediaries"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~1843 -->

#### A.2.3.30 Topic 52 - Relying Party intermediaries

<div class="eudi-hlr" id="RPI_01" markdown>
<div class="eudi-hlr__id">RPI_01<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An intermediary SHALL register as a Relying Party, in accordance with all requirements in [Topic 27][topic-27], while indicating it intends to act as an intermediary.

*Note: a) This implies that an intermediary obtains an access certificate containing its own trade name and unique Relying Party identifier, and Service trade name and identifier. b) An intermediary may also obtain a registration certificate according to [Topic 44][topic-44], but this certificate will not be used for intermediated transactions. c) An entity that registered as an intermediary may also register as a Relying Party in its own capacity. In such a case, it will receive one or more registration certificates for its Services and intended use(s), (see RPRC_09), and will use one of these certificates when interacting with a Wallet Unit.*

</div>
</div>

<div class="eudi-hlr" id="RPI_02" markdown>
<div class="eudi-hlr__id">RPI_02</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPI_03" markdown>
<div class="eudi-hlr__id">RPI_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

An intermediary SHALL ensure that each intermediated Relying Party that will use its services to interact with Wallet Units, is registered at a Registrar in the Member State where the intermediated Relying Party is established, according all requirements in [Topic 44][topic-44]. The intermediary SHALL also ensure that it receives the necessary registration certificates for the intermediated Relying Party, as specified in RPRC_09. Each of these registration certificates SHALL show that the intermediated Relying Party uses the services of the intermediary. 

*Note: A Registrar is free to design a suitable process to achieve these goals. For example, it may decide an intermediary can register the intermediated Relying Parties at the Registrar, and receive the registration certificates in return. Alternatively, the Registrar could request the intermediated Relying Parties ro register themselves and indicate the intermediary they will be using, in which case they will receive the registration certificates and must send them to the intermediary. Alternative processes can be used as well.*

</div>
</div>

<div class="eudi-hlr" id="RPI_04" markdown>
<div class="eudi-hlr__id">RPI_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before registering the relationship between an intermediary and an intermediated Relying Party and issuing a registration certificate showing that the intermediated Relying Party uses the services of the intermediary, a Registrar SHALL ensure it obtains legally valid evidence that this Relying Party will indeed use the services of this intermediary to interact with Wallet Units. 

*Note: A Registrar is free to decide which evidence it needs and how it obtains this evidence. For example, the Registrar may require either the intermediary or the intermediated Relying Party to provide a signed copy of the contract between both parties. Alternatively, the Registrar could ask an authorised representative of the Relying Party to sign off on a registration that was done by the intermediary, or could ask for a mandate from the intermediated Relying Party to the intermediary to register the Relying Party.*

</div>
</div>

<div class="eudi-hlr" id="RPI_05" markdown>
<div class="eudi-hlr__id">RPI_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When an intermediated Relying Party asks its intermediary to request some attributes from a Wallet Unit, it SHALL indicate which single registration certificate the intermediary must include in the presentation request.

</div>
</div>

<div class="eudi-hlr" id="RPI_06" markdown>
<div class="eudi-hlr__id">RPI_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When requested by an intermediated Relying Party, an intermediary SHALL request a presentation of attributes from a specific Wallet Unit. In the request, the intermediary SHALL include the applicable intermediary's access certificate meant in requirement RPI_01 and the registration certificate of the Relying Party, indicated per RPI_05.

*Note: The applicable access certificate contains the association to this specific intermediated Relying Party, see Reg_34a. *

</div>
</div>

<div class="eudi-hlr" id="RPI_06a" markdown>
<div class="eudi-hlr__id">RPI_06a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPI_07" markdown>
<div class="eudi-hlr__id">RPI_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

In case a Wallet Unit receives a presentation request from an intermediary on behalf of an intermediated Relying Party, it SHALL NOT display the trade names of the intermediary and the intermediary Service to the User when asking for User approval, as described in RPA_07.

</div>
</div>

<div class="eudi-hlr" id="RPI_07a" markdown>
<div class="eudi-hlr__id">RPI_07a</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPI_07b" markdown>
<div class="eudi-hlr__id">RPI_07b</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="RPI_08" markdown>
<div class="eudi-hlr__id">RPI_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When a Wallet Unit presents to an intermediary any User attributes from a PID or attestation, the intermediary SHALL, after successfully carrying out the verifications in RPI_09, forward these attributes only to the Relying Party on behalf of which the presentation request was made. If any of the verifications in RPI_09 fail, the intermediary SHALL NOT forward any attributes to the Relying Party, nor to any other entity.

</div>
</div>

<div class="eudi-hlr" id="RPI_09" markdown>
<div class="eudi-hlr__id">RPI_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

When a Wallet Unit presents to an intermediary any attributes from a PID or attestation, the intermediary SHALL verify the authenticity of the PID or attestation, its revocation status, device binding and User binding, as well as any combined presentation of attributes, if applicable, as specified in this ARF and if agreed with the Relying Party.

*Note: The ARF does not mandate that a Relying Party must carry out all of these verifications. Therefore, the intermediary and any Relying Party using its services must agree on what verifications the intermediary will carry out.*

</div>
</div>

<div class="eudi-hlr" id="RPI_10" markdown>
<div class="eudi-hlr__id">RPI_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The intermediary SHALL delete any PIDs or attestations it obtained from the Wallet Unit, including any User attributes, completely and immediately after it has sent the User attributes to the intermediated Relying Party. If the intermediary does not send any User attributes to the intermediated Relying Party, for example because one of the verifications in RPI_09 failed, the intermediary SHALL delete the PIDs or attestations completely and immediately as soon as it has completed all necessary verifications.

</div>
</div>


[](){ #topic-53 }
