---
name: "hlr-40-wallet-instance-installation-and-wallet-"
description: "Use when working with EUDI high-level requirements for 'Wallet Instance installation and Wallet Unit activation and management'. Contains normative SHALL/SHOULD/MAY requirements from ARF Annex 2."
sections:
  - "A.2.3.23 Topic 40 - Wallet Instance installation and Wallet Unit activation and management"
  - "A. HLRs for Wallet Instance installation <!-- omit from toc -->"
  - "B. HLRs for Wallet Unit activation <!-- omit from toc -->"
  - "C. HLRs for Wallet Unit management <!-- omit from toc -->"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~5889 -->

#### A.2.3.23 Topic 40 - Wallet Instance installation and Wallet Unit activation and management

##### A. HLRs for Wallet Instance installation <!-- omit from toc -->

<div class="eudi-hlr" id="WIAM_01" markdown>
<div class="eudi-hlr__id">WIAM_01<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

To ensure that the User can trust the Wallet Solution, a Wallet Provider SHOULD make its certified Wallet Solution available for installation only via the official app store of the relevant operating system (e.g., Android, iOS).

*Note: This allows the operating system of the device to perform relevant checks regarding the authenticity of the Wallet Unit.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_02" markdown>
<div class="eudi-hlr__id">WIAM_02<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Wallet Provider makes its certified Wallet Solution available for installation through other means than the official OS app store, it SHALL implement a mechanism allowing the User to verify the authenticity of the Wallet Unit. Moreover, it SHALL provide clear instructions to the User on how to install the Wallet Instance, including at least: - instructions on the verification of the authenticity of the Wallet Instance to be installed, - instructions on bypassing of any operating system limitations on side-loading of apps, if applicable, and ensuring that these limitations are restored after the Wallet Instance has been installed.

*Note: This requirement also applies for the installation of a Wallet Instance on a User device that is not a mobile device, and for which no official operating system app store may exist.*

</div>
</div>


##### B. HLRs for Wallet Unit activation <!-- omit from toc -->

<div class="eudi-hlr" id="WIAM_03" markdown>
<div class="eudi-hlr__id">WIAM_03<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL ensure that a Wallet Instance starts a process to activate the new Wallet Unit with the Wallet Provider immediately after installation or when the User first opens the Wallet Instance. The Wallet Provider SHALL ensure that the Wallet Instance starts this process only with a secure backend of the Wallet Provider.

</div>
</div>

<div class="eudi-hlr" id="WIAM_04" markdown>
<div class="eudi-hlr__id">WIAM_04<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During the activation process of a new Wallet Unit, the Wallet Provider SHALL verify that the new Wallet Instance is a genuine instance of its Wallet Solution.

</div>
</div>

<div class="eudi-hlr" id="WIAM_05" markdown>
<div class="eudi-hlr__id">WIAM_05<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During the activation process of a new Wallet Unit, the Wallet Provider SHALL process information about the User device and the available WSCA/WSCD and keystore(s), as far as necessary to issue Key Attestations and Wallet Instance Attestations to the Wallet Unit conform all requirements in [Topic 9][topic-9]. The Wallet Provider MAY process additional information necessary for managing the Wallet Unit, but it SHALL NOT process more information than it reasonably needs for legitimate purposes. The Wallet Provider SHALL request User consent (through the Wallet Instance) for all information and data it will process, both during activation and throughout the lifetime of the Wallet Unit. The Wallet Provider SHALL inform the User about the purposes of data processing, in accordance with the General Data Protection Regulation.

</div>
</div>

<div class="eudi-hlr" id="WIAM_06" markdown>
<div class="eudi-hlr__id">WIAM_06<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Provider SHALL request the User, through the new Wallet Instance, to log in to an existing account at the Wallet Provider, or to set up a new User account if the User does not have an account yet. If a new account must be set up, the Wallet Provider SHALL explain to the User that setting up an account is necessary to enable the User to request revocation of the Wallet Unit in case of theft or loss. The Wallet Provider SHALL register one or more User authentication methods that the Wallet Provider will use to authenticate the User in the future. These methods SHALL be independent of the Wallet Unit and the User device. The Wallet Provider SHALL allow the User to register using an alias instead of true identity data. The Wallet Provider SHALL NOT use any registered User data for purposes other than User authentication, unless the User gives explicit consent to do so. The Wallet Provider SHALL register the relationship between the Wallet Unit and the corresponding User account.

*Note: The User may already have an account at the Wallet Provider, for example because they use a Wallet Unit of this Wallet Provider already on another device, or if they are migrating to a new device.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_07" markdown>
<div class="eudi-hlr__id">WIAM_07<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL activate a new Wallet Unit before a User can use it to have issued an PID or attestation.

</div>
</div>

<div class="eudi-hlr" id="WIAM_08" markdown>
<div class="eudi-hlr__id">WIAM_08<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL only activate a new Wallet Unit if it has verified that the Wallet Unit includes a WSCA/WSCD that is certified to be compliant with applicable requirements for Level of Assurance High.

*Note: a) A WSCA/WSCD by definition complies with requirements for Level of Assurance High, see WIAM_14. b) In addition, the Wallet Unit can include one or more keystores.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_08a" markdown>
<div class="eudi-hlr__id">WIAM_08a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a Wallet Unit contains one or more keystores, the Wallet Provider SHALL assign a security level to every keystore, with the following possible values: `iso_18045_high`, `iso_18045_moderate`, `iso_18045_enhanced-basic`, `iso_18045_basic` or `none`, corresponding to the level of resistance for which the keystore was certified (respectively AVA_VAN.5, AVA_VAN.4, AVA_VAN.3, AVA_VAN.2 and no certification).

*Note: For the definition of these security levels, also see [OpenID4VCI] Annex D.2*

</div>
</div>

<div class="eudi-hlr" id="WIAM_09" markdown>
<div class="eudi-hlr__id">WIAM_09<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If a WSCA/WSCD or keystore contains cryptographic assets related to multiple Wallet Units, the Wallet Provider SHALL ensure that a Wallet Unit can only access assets that are related to that Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="WIAM_10" markdown>
<div class="eudi-hlr__id">WIAM_10<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During the activation process of a new Wallet Unit, a Wallet Provider SHALL create and sign at least one Key Attestation for the WSCA/WSCD, at least one Key Attestation for each keystore, and at least one Wallet Instance Attestation, and issue them to the Wallet Unit. The Wallet Provider SHALL verify that the private key(s) corresponding to the public key(s) in each KA are protected by the respective WSCA/WSCD or keystore, under control of the User. The Wallet Provider SHALL take measures to verify the integrity of the Wallet Instance before issuing a Wallet Instance Attestation.

</div>
</div>

<div class="eudi-hlr" id="WIAM_10a" markdown>
<div class="eudi-hlr__id">WIAM_10a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

During the activation process of a new Wallet Unit, the Wallet Provider SHALL offer the User a means to verify the formal certification information of their Wallet Solution.

</div>
</div>


##### C. HLRs for Wallet Unit management <!-- omit from toc -->

<div class="eudi-hlr" id="WIAM_11" markdown>
<div class="eudi-hlr__id">WIAM_11</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WIAM_12" markdown>
<div class="eudi-hlr__id">WIAM_12<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

All communication between the Wallet Provider and the Wallet Instance SHALL be mutually authenticated and SHOULD be encrypted.

</div>
</div>

<div class="eudi-hlr" id="WIAM_12a" markdown>
<div class="eudi-hlr__id">WIAM_12a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Provider SHALL NOT access the contents of a Wallet Instance, in particular to learn a) which attestations are present on the Wallet Unit, b) the status of these attestations, c) the value of attributes in these attestations, and d) the contents of the Wallet Unit log meant in DASH_02.

</div>
</div>

<div class="eudi-hlr" id="WIAM_12b" markdown>
<div class="eudi-hlr__id">WIAM_12b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the contents of a Wallet Unit specified in WIAM_12a are stored in a Wallet Instance on the User's device, the Wallet Instance SHALL ensure that the Wallet Provider cannot access the contents of the Wallet Unit.

</div>
</div>

<div class="eudi-hlr" id="WIAM_12c" markdown>
<div class="eudi-hlr__id">WIAM_12c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the contents of a Wallet Unit specified in WIAM_12a are stored in a Wallet Unit Service on the Wallet Provider backend, the Wallet Provider SHALL specify and implement strict controls to limit access by the Wallet Provider to the contents of the Wallet Unit.

*Note: In this situation, the Wallet Unit cannot fully prevent the Wallet Provider from accessing the Wallet Unit contents.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_13" markdown>
<div class="eudi-hlr__id">WIAM_13<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL enable the User to 'factory reset' the Wallet Unit, which SHALL cause the deletion of all attestations, the log, and all other personal data, settings, and configurations from the Wallet Unit. If the User resets the Wallet Unit, the Wallet Instance SHALL request the associated WSCA/WSCD and keystore(s) to delete all cryptographic assets related to the Wallet Unit and to all PIDs and device-bound attestations on the Wallet Unit, if the WSCA/WSCD and the keystore(s) are connected to the User device.

*Note:  a) The User can use this option, for instance, in preparation to the planned uninstallation of the Wallet Instance. b) Deletion of PID or KA cryptographic assets requires User authentication, as specified in requirement WIAM_14. c) The Wallet Unit does not necessarily inform the Wallet Provider about the factory reset. d) It may happen there is no connection to the WSCA/WSCD or to a keystore at the moment the User resets the Wallet Instance. For instance, in case the WSCA/WSCD is an external smart card and the User does not present that card to the User device. Another example occurs when the WSCA/WSCD is a remote HSM and the User device is offline at that moment. In such cases, the cryptographic assets will remain present on the WSCA/WSCD or on the keystore, even though they will never be used again. If needed, it is up to the Wallet Provider to define how the Wallet Unit should handle such situations. For example, an HSM manager could address such cases by deciding to delete cryptographic keys in the HSM that are too old or haven't been used for too long, while being aware of the risks in doing so.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_13a" markdown>
<div class="eudi-hlr__id">WIAM_13a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

If the User resets the Wallet Unit, the Wallet Unit SHALL disclose the fact that it no longer stores any previously disclosed PID(s) or attestation(s) to the Digital Credentials API framework.

</div>
</div>

<div class="eudi-hlr" id="WIAM_14" markdown>
<div class="eudi-hlr__id">WIAM_14<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A WSCA/WSCD managing the critical assets of a PID, such as private or secret cryptographic keys, SHALL authenticate the User at Level of Assurance High before performing any cryptographic operation involving any of these assets.

*Note: a) [CIR 2024/2981], Annex IV, section 2 (3) states "As a prerequisite to the certification under national certification schemes, the WSCD shall be assessed against the requirements of assurance level high as set out in Implementing Regulation (EU) 2015/1502." Therefore, a WSCA/WSCD by legal definition complies with requirements of LoA High. b) Note to WIAM_14 - WIAM_14b: Many actions of the Wallet Unit, such as processing a Relying Party presentation request and presenting an attestation, require multiple cryptographic operations, for example ephemeral key generation followed by key agreement and presentation signing and encryption. These requirements does not imply that a separate User authentication is necessary before each of these operations. Rather, a successful User authentication will be valid for all cryptographic operations necessary for a Wallet Unit action. It is up to the Wallet Provider to determine what constitutes a 'Wallet Unit action', finding a balance between security (more User authentications) and User convenience (fewer User authentications). During certification of the Wallet Solution, it will be verified that the solution provides an adequate level of security.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_14a" markdown>
<div class="eudi-hlr__id">WIAM_14a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A WSCA/WSCD managing the critical assets of a KA SHALL authenticate the User at Level of Assurance High before performing any cryptographic operation involving any of these assets.

*Note: The WSCA/WSCD manages the private key(s) corresponding to the public key(s) attested in the KA.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_14b" markdown>
<div class="eudi-hlr__id">WIAM_14b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A WSCA/WSCD managing the cryptographic assets of an attestation having a level of security High SHALL authenticate the User at level of security High before performing any cryptographic operation involving any of these assets.

*Note: a) The term 'Level of Assurance', as used in the European Digital Identity Regulation and in Implementing Regulation (EU) 2015/1502, is only applicable to electronic identity means, which in the context of the EUDI Wallet means only the PID. For that reason, this requirement uses the term 'level of security'. Levels of security are defined in standards or specifications different from CIR 2015/1502, for instance ISO/IEC 18045. b) During issuance of an attestation, the Attestation Provider in its Credential Issuer metadata indicates the level of security it requires for the key storage and user authentication for this type of attestation. See [OpenID4VCI] section 12.2.4 and Appendix D.2.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_14c" markdown>
<div class="eudi-hlr__id">WIAM_14c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A Wallet Unit SHALL use either the WSCA/WSCD or a keystore to manage any cryptographic assets that are not considered to be critical assets.

*Note: a) The ARF uses the term 'keystore' to refer to a hardware-backed repository and service in which non-critical cryptographic assets are generated, stored, and used exclusively inside a dedicated hardware security boundary. b) Examples of non-critical cryptographic assets are private and secret keys of attestations having a level of security lower than High. c) As mentioned in WIAM_14 and WIAM_14b, the private and secret keys of PIDs and KAs are critical assets and therefore are stored in a WSCA/WSCD.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_15" markdown>
<div class="eudi-hlr__id">WIAM_15<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

Before performing any operation, including allowing a User to view attestations and attribute values, a Wallet Instance SHALL securely authenticate the User using a multi-factor authentication mechanism provided by the User device.

*Note: a) One of the authentication factors is the possession of the User device.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_15a" markdown>
<div class="eudi-hlr__id">WIAM_15a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the purpose of WIAM_15, the Wallet Instance SHALL enforce the activation of an OS-level User authentication mechanism with adequate security policies.

*Note: Adequate' here means adequate for any operation excluding the issuance or presentation of PIDs, KAs, and potentially other attestations at level of security High. This includes but is not limited to generating pseudonyms, accessing the transaction log (dashboard), data export and migration, requesting the erasure of personal data by a Relying Party, and reporting a Relying Party to a DPA.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_15b" markdown>
<div class="eudi-hlr__id">WIAM_15b<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Unit SHALL enable the User to use a Wallet Unit-specific authentication method for User authentication, in addition to the User authentication mechanism provided by the User device per WIAM_15. The Wallet Provider SHALL either make the use of this additional authentication method mandatory for all Users, or leave it to each User to decide if they want to use it.

*Note: a) This authentication method may be implemented by the Wallet Instance, a (local) keystore, the WSCA/WSCD, or any other component of the Wallet Unit. b) As an optimisation to reduce the number of User authentication events, the Wallet Provider can choose to implement this additional authentication method in the WSCA/WSCD, in such a way that it complies with WIAM_14.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_15c" markdown>
<div class="eudi-hlr__id">WIAM_15c<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Instance SHALL also use the User authentication mechanism provided by the User device (WIAM_15) and possibly the Wallet Unit-specific authentication method (WIAM_15b) to unlock the keystore mentioned in WIAM_14c, where applicable.

*Note: Apart from using the same mechanism, the intent of this requirement is also to minimize the number of User authentications needed (after the initial authentication per WIAM_15a) to enable the issuance or presentation of (non-PID) attestations. However, see WIAM_16 and WIAM_16a: the Wallet Provider may request another authentication if this is necessary for security.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_16" markdown>
<div class="eudi-hlr__id">WIAM_16<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the User authentication mechanism provided by the User device (WIAM_15), the Wallet Instance SHALL force the User device to enable a time-based control (e.g., a session timeout or re-authentication interval), to ensure that access is automatically revoked after a defined period of inactivity.

*Note: It is assumed that re-authentication is required by the User device when the device is locked by the User.*

</div>
</div>

<div class="eudi-hlr" id="WIAM_16a" markdown>
<div class="eudi-hlr__id">WIAM_16a<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

For the Wallet Unit-specific User authentication method (WIAM_15b), the Wallet Provider SHALL define and implement conditions after which user authentication shall again be required, including at least an idle timeout. The Wallet Unit SHOULD provide the User with the option to set the idle timeout to a duration shorter than the default timeout set by the Wallet Provider. The Wallet Provider SHOULD also consider other factors, including the device being locked by the User and the Wallet Instance losing focus.

</div>
</div>

<div class="eudi-hlr" id="WIAM_17" markdown>
<div class="eudi-hlr__id">WIAM_17<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

The Wallet Provider SHALL ensure that the Wallet Unit requests the User, during activation of the Wallet Unit, to set up the authentication factors for the User authentication mechanism implemented by the WSCA/WSCD meant in WIAM_14, the authentication mechanism implemented by the User device meant in WIAM_15 and WIAM_15a, and, if used, the Wallet Unit-specific authentication method meant in WIAM_15b.

</div>
</div>

<div class="eudi-hlr" id="WIAM_18" markdown>
<div class="eudi-hlr__id">WIAM_18</div>
<div class="eudi-hlr__body" markdown>

Empty

</div>
</div>

<div class="eudi-hlr" id="WIAM_19" markdown>
<div class="eudi-hlr__id">WIAM_19<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A WSCA/WSCD and a keystore SHALL be able to prove possession of the private key corresponding to a public key on request of a Wallet Instance, for example by signing a challenge with that private key.

</div>
</div>

<div class="eudi-hlr" id="WIAM_20" markdown>
<div class="eudi-hlr__id">WIAM_20<span class="kw-shall">SHALL</span></div>
<div class="eudi-hlr__body" markdown>

A WSCA/WSCD SHALL protect a private key it generated during the entire lifetime of the key. This protection SHALL at least imply that the WSCA/WSCD prevents the private key from being extracted in the clear. If a WSCA/WSCD is able to export a private key in encrypted format, the resulting level of protection SHALL be equivalent to the protection level of the private key when stored in the WSCA/WSCD.

</div>
</div>

<div class="eudi-hlr" id="WIAM_21" markdown>
<div class="eudi-hlr__id">WIAM_21<span class="kw-should">SHOULD</span></div>
<div class="eudi-hlr__body" markdown>

Whenever the WSCA/WSCD successfully authenticated the User, the Wallet Unit SHOULD check if the WSCD contains cryptographic assets for technical PIDs or attestations that cannot be presented any longer to Relying Parties, for example because they have expired or because a once-only attestation (see [Topic 10][topic-10], section D, method A) was presented to a Relying Party already. The Wallet Unit SHOULD then request the WSCA/WSCD to destroy all cryptographic assets related to these technical PIDs or attestations. However, the Wallet Unit SHOULD NOT request the destruction of the private key belonging to the last technical PID or attestation corresponding to a logical PID or attestation.

*Note: a) The reason for this recommendation is that probably, Wallet Providers will want to prevent an accumulation of unused private keys in the WSCA/WSCD, given that such devices typically do not have much storage space. However, deletion of private keys (and potentially other cryptographic assets) is a cryptographic key operation and cannot be done without User authentication - see WIAM_14. At the same time, for usability reasons the User must not be involved in such 'cleaning up' processes, see also ISSU_42. The recommended solution is to take advantage of a User authentication event to also carry out any necessary cleaning operations. b) Method A (once-only attestations, see ISSU_ 37) includes a potential fallback to Method B (limited-time attestations) in case no unused technical PIDs or attestations are left. To ensure that falling back to Method B is always possible when needed, a Wallet Unit should ensure that for every logical PID or attestation it has, it is always in possession of at least one technical PID or attestation.*

</div>
</div>


[](){ #topic-42 }
