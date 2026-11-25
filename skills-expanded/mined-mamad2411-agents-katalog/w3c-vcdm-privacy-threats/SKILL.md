---
name: "w3c-vcdm-privacy-threats"
description: "Use when assessing advanced W3C VCDM privacy threats and residual risks. Covers: late-section privacy threats, issuer/verifier cooperation impacts, and ecosystem risk considerations."
sections:
  - "8.15 Legal Processes*This section is non-normative.*"
  - "8.16 Sharing Information with the Wrong Party*This section is non-normative.*"
  - "8.17 Data Theft*This section is non-normative.*"
  - "8.18 Frequency of Claim Issuance*This section is non-normative.*"
  - "8.19 Prefer Single-Use Credentials*This section is non-normative.*"
  - "8.20 Private Browsing*This section is non-normative.*"
  - "8.21 Issuer Cooperation Impacts on Privacy*This section is non-normative.*"
---

<!-- ARF version: 2.0-2024-12-04 -->
<!-- Tokens: ~4602 -->

### 8.15 Legal Processes*This section is non-normative.*
        

        
Legal processes can compel [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders), and [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to
disclose private information to authorities, such as law enforcement. It is
also possible for the same private information to be accidentally disclosed
to an unauthorized party through a software bug or security failure. Authors
of legal processes and compliance regimes are advised to draft guidelines that
require notifying the [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) involved when their private information is
intentionally or accidentally disclosed to a third party. Providers of software
services are advised to be transparent about known circumstances that might
cause such private information to be shared with a third party, as well as the
identity of any such third party.

---

### 8.16 Sharing Information with the Wrong Party*This section is non-normative.*
        

        
When a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) chooses to share information with a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), it
might be the case that the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) is acting in bad faith and requests
information that could harm the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders). For example, a
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might ask for a bank account number, which could then be used
with other information to defraud the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) or the bank.
        

        
[Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) ought to strive to tokenize as much information as possible so
that if a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) accidentally transmits [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) to the wrong
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), the situation is not catastrophic.
        

        
For example, instead of including a bank account number to check
an individual's bank balance, provide a token that enables the
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to check if the balance is above a certain amount. In this
case, the bank could issue a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) containing a balance
checking token to a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders). The [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) would then include the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) in a [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) and bind the
token to a credit checking agency using a digital signature. The
[verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) could then wrap the [verifiable presentation](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) in their
digital signature and hand it back to the issuer to check the
account balance dynamically.
        

        
Using this approach, even if a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) shares the account balance token
with the wrong party, an attacker cannot discover the bank account number or
the exact value of the account. Also, given the validity period of the
counter-signature, the attacker gains access to the token for only a
few minutes.

---

### 8.17 Data Theft*This section is non-normative.*
        

        
The data expressed in [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) and
[verifiable presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-presentation) are valuable since they contain authentic
statements made by trusted third parties (such as [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers)) or
individuals (such as [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) or [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects)). The storage and
accessibility of this data can inadvertently create honeypots of
sensitive data for malicious actors. These adversaries often seek to
exploit such reservoirs of sensitive information, aiming to
acquire and exchange that data for financial gain.
        
        
[Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) are advised to retain the minimum amount of data
necessary to issue [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) to [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and
to manage the status and revocation of those credentials. Similarly,
[issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) are advised to avoid creating publicly
accessible credentials that include personally identifiable information
(PII) or other sensitive data. Software implementers are advised
to safeguard [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) using robust consent
and access control measures, ensuring that they remain
inaccessible to unauthorized entities.
        
        
[Holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) are advised to use implementations that appropriately
encrypt their data in transit and at rest and protect sensitive
material (such as cryptographic secrets) in ways that cannot be easily
extracted from hardware or other devices. It is further suggested that
[holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) store and manipulate their data only on devices they
control, away from centralized systems, to reduce the likelihood of
an attack on their data or inclusion in a large-scale theft if an attack is
successful. Furthermore, [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) are encouraged to rigorously control
access to their credentials and presentations, allowing access only to those
with explicit authorization.
        
        
[Verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) are advised to ask only for data necessary for a particular
transaction and to retain no data beyond the needs of any particular
transaction.
        
        
Regulators are advised to reconsider existing audit requirements such that
mechanisms that better preserve privacy can be used to achieve similar
enforcement and audit capabilities. For example, audit-focused regulations
that insist on the collection and long-term retention of personally
identifiable information can cause harm to individuals and organizations
if that same information is later compromised and accessed by an attacker.
The technologies described by this specification enable [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to
prove properties about themselves and others more readily, reducing the
need for long-term data retention by [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). Alternatives include
keeping logs that the information was collected and checked, as well as
random tests to ensure that compliance regimes are operating as expected.

---

### 8.18 Frequency of Claim Issuance*This section is non-normative.*
        

        
As detailed in Section [8.14 Patterns of Use](https://www.w3.org/TR/vc-data-model-2.0/#patterns-of-use), patterns of use can be
correlated with certain types of behavior. This correlation is partially
mitigated when a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) uses a [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) without the
knowledge of the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers). [Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) can defeat this protection
however, by making their [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) short lived and renewal
automatic.
        

        
For example, an `ageOver` [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is helpful in
gaining access to a bar. If an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) issues such a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) with a very short validity period and an automatic
renewal mechanism, then the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) could correlate the [holder's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
behavior in a way that negatively impacts the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
        

        
Organizations providing software to [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) ought to warn them if they
repeatedly use [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) with short lifespans, which could result in
behavior correlation. [Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) ought to avoid issuing [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) that
enable them to correlate patterns of use.

---

### 8.19 Prefer Single-Use Credentials*This section is non-normative.*
        

        
An ideal privacy-respecting system would require only the information necessary
for interaction with the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to be disclosed by the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
The [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) then records that the disclosure requirement has been met
and discards any sensitive information disclosed. In many cases,
competing priorities, such as regulatory burden, prevent this ideal system from
being employed. In other instances, long-lived identifiers prevent single use.
The designer of any [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) ecosystem ought to strive
to make it as privacy-respecting as possible by preferring single-use
[verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) whenever possible.
        

        
Using single-use [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) provides several benefits. The
first benefit is to [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) who can be sure that the data in a
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) is fresh. The second benefit is to [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders),
who know that if there are no long-lived identifiers in the
[verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential), the [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) itself cannot be
used to track or correlate them online. Finally, there is nothing for attackers
to steal, making the entire ecosystem safer to operate within.

---

### 8.20 Private Browsing*This section is non-normative.*
        

        
In an ideal private browsing scenario, no PII will be revealed. Because many
[credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) include PII, organizations providing software to
[holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) ought to warn them about the possibility of this information
being revealed if they use [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) and [presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) while in
private browsing mode. As each browser vendor handles private browsing
differently, and some browsers might not have this feature, it is
important that implementers not depend on private browsing mode to provide
any privacy protections. Instead, implementers are advised to rely on
tooling that directly usable by their software to provide privacy guarantees.

---

### 8.21 Issuer Cooperation Impacts on Privacy*This section is non-normative.*
        

        
[Verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) rely on a high degree of trust in [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers).
The degree to which a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) might take advantage of possible privacy
protections often depends strongly on the support an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) provides for
such features. In many cases, privacy protections which make use of
zero-knowledge proofs, data minimization techniques, bearer credentials,
abstract claims, and protections against signature-based correlation require
active support by the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), who need to incorporate those capabilities
into the [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) they issue.
        
        
It is crucial to note that [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) not only depend on [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers)
participation to provide [verifiable credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) capabilities that help
preserve [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) privacy, but also rely on [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to
not deliberately subvert these privacy protections. For example, an
[issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) might sign [verifiable credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifiable-credential) using a signature scheme
that protects against signature-based correlation. This would protect the
[holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) from being correlated by the signature value as it is shared among
[verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). However, if the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) creates a unique key for each
issued [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), it might be possible for the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to track
[presentations](https://www.w3.org/TR/vc-data-model-2.0/#dfn-presentation) of the [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential), regardless of a [verifier's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
inability to do so.
        
        
In addition to previously described privacy protections an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) might
offer, [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) need to be aware of data they leak that is associated with
identifiers and claim types they use when issuing [credentials](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential). One
example of this would be an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) issuing driver's licenses which reveal
both the location(s) in which they have jurisdiction and the location of the
[subject's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) residence. [Verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might take advantage of this by
requesting a [credential](https://www.w3.org/TR/vc-data-model-2.0/#dfn-credential) to check that the [subject](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) is licensed to
drive when, in fact, they are interested in metadata *about* the
credential, such as which [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) issued the credential, and tangential
information that might have been leaked by the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), such as the
[subject's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects) home address. To mitigate such leakage, [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) might
use common identifiers to mask specific location information or other sensitive
metadata; for example, a shared [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) identifier at a state or national
level instead of at the level of a county, city, town, or other smaller
municipality. Further, [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) can use [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) attestation mechanisms
to preserve privacy, by providing proof that an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) exists in a set of
trusted entities without needing to disclose the exact [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers).
