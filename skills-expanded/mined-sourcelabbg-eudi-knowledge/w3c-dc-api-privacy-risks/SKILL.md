---
name: "w3c-dc-api-privacy-risks"
description: "Use when assessing W3C Digital Credentials API privacy risks: unnecessary requests for credentials, fingerprinting and data leakage, and user permission and transparency."
sections:
  - "11.4 Unnecessary Requests for Credentials"
  - "11.4.1 Government-issued credentials"
  - "11.4.2 Non-government-issued credentials"
  - "11.5 Fingerprinting and Data Leakage"
  - "11.5.1 Browser fingerprinting"
  - "11.5.2 Leaking incidental data with credential presentations"
  - "11.5.3 Revealing device properties through protocol availability"
  - "11.5.4 Avoiding leaks of credential availability"
  - "11.6 User Permission and Transparency"
  - "11.6.1 Handling multiple credential requests"
  - "11.6.2 Integrating Multiple User Agents"
  - "11.6.3 Permission Prior to Credential Manager Selection"
  - "11.6.4 Permission vs. Consent"
---

<!-- ARF version: draft-2025 -->
<!-- Tokens: ~6516 -->

### 11.4 Unnecessary Requests for Credentials
        
        
        
          Unnecessary credential requests are a key privacy risk to the entire
          digital credentials ecosystem. They could manifest in different ways
          and from different motivations:
        
        
          - Intentional abuse of the API to learn sensitive information about
          the user for the purpose of fraud, tracking, or sale of the data. For
          example, a site could trick a user into sharing their passport
          information through misleading content. This can lead to identity
          theft and financial loss, and severe loss of control and/or leakage
          of personal information.
          
          - Unnecessary requests for credentials without the explicit intent
          of user harm, such as an online store requesting users to sign up
          with their driver's license instead of generic email & passkey or
          federated credentials. This can lead to
          [exclusion](https://www.w3.org/reports/identity-web-impact#opportunities-and-threats) of
          users without the ability or willingness to share such a credential
          with the site, a deterioration of the prompt experience on the web,
          and an increase in the risk of accidental data leakage.
          
          - Requests for an excessive amount of information for valid
          purposes against the principle of data minimization. A common example
          is collection of a user's entire national identity document for age
          verification instead of relying on selective disclosure and age
          predicates.
          
        
        
          One challenge here is determining what constitutes "valid" purposes
          and which requests are therefore "unnecessary", and requires
          participation from all parties involved in the credential exchange.
        
        
          - Ideally, [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) would self-regulate their requests for
          credentials. However, from a [user agent](https://infra.spec.whatwg.org/#user-agent)'s perspective,
          [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) are potential attackers, and might not consider the
          user's best interest in their designs. The Digital Credentials API
          operates from an assumption that all [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) might have
          incentives that motivate unnecessary requests and abuse, and protect
          users accordingly.
          
          - [User agents](https://infra.spec.whatwg.org/#user-agent) are responsible for protecting their users
          against dangerous content and permission requests on the Web and
          could intervene on their behalf, proactively rejecting requests or
          requiring pre-authorization. To support this, this specification
          requires credential requests to be readable by the [user agent](https://infra.spec.whatwg.org/#user-agent)
          (i.e., not end-to-end encrypted to the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), see
          [5. 
      Protocols](https://w3c-fedid.github.io/digital-credentials/#protocols) and [6.2 
      Prepare credential requests](https://w3c-fedid.github.io/digital-credentials/#prepare-credential-requests)).
          
          - [Issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and lawmakers might decide to restrict use of
          (particularly government-issued) credentials to specific
          [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) with purpose attestations. [Credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager)
          might be expected to enforce these restrictions by law or policy.
          
          - The ultimate decision of whether or not to share their personal
          information lies with the user, which is why the API [requires](https://w3c-fedid.github.io/digital-credentials/#dfn-initiate-the-credential-request) the
          [user agent](https://infra.spec.whatwg.org/#user-agent) to present a credential picker to the user, and other
          parties might additionally require confirmation or consent.
          
        
        
          For a more detailed exploration of how to determine and address
          unnecessary usage, it makes sense to consider government-issued
          credentials and other credentials separately, as they potentially
          differ in the sensitivity of their data and the potential harms from
          misuse as well as legal & regulatory considerations.
        
        
          A key component of risk mitigation and ensuring user control that
          applies to both types of credentials is the [user agent](https://infra.spec.whatwg.org/#user-agent)'s ability
          to inspect the credential request metadata and make decisions or UI
          presentation based on it. This specification ensures this [user agent](https://infra.spec.whatwg.org/#user-agent) access through protocol requirements to transmit requests
          unencrypted and include relevant information (see [5. 
      Protocols](https://w3c-fedid.github.io/digital-credentials/#protocols)
          and [6.2 
      Prepare credential requests](https://w3c-fedid.github.io/digital-credentials/#prepare-credential-requests)).
        
#### 11.4.1 Government-issued credentials
        
          [Government-issued
          digital credentials](https://www.w3.org/reports/identity-web-impact#pure-digital-credentials) include travel documents, personal licenses,
          proof of welfare and public health programs, vehicle registrations,
          and other documents issued by government authorities, or other
          documents representing this information. These documents are highly
          sensitive, as they can contain permanent, irrevocable, unique
          identifiers that are central to a person's individual identity and
          ability to interact with vital public services.
        
##### 11.4.1.1 Risk of theft and leakage of government credentials
        
          The high value of these credentials to users and attackers means
          there is a significant risk of theft, and significant potential harm
          from leakage to unauthorized third parties. This includes the request
          of government identity for the purpose of tracking and
          personalization.
        
##### 11.4.1.2 Risk of proliferation of requests for government credentials
        
          A major concern with increased availability of government credentials
          online is [Jevon's Paradox](https://en.wikipedia.org/wiki/Jevons_paradox),
          i.e., the chance of increasing demand for credentials through lower
          friction of access. This effect is not inherently caused by the
          Digital Credentials API, but rather the overall increasing adoption
          of digital credentials across the ecosystem, which, however, would
          likely see additional momentum from [user agent](https://infra.spec.whatwg.org/#user-agent) implementation of
          the Digital Credentials API. As such, the effect needs to be
          considered by [user agents](https://infra.spec.whatwg.org/#user-agent) implementing the API, as it might
          result in harmful outcomes for users:
        
        
          - Increased risk of information leakage, and ultimately a less
          trusted user experience on the Web. When a large number of services
          access and store government-issued credentials in an insecure manner
          (i.e. not maintaining encryption or failing to safeguard private
          keys), the chance of data leaks and unauthorized access increases as
          well. Even seemingly non-identifying information like birthdates and
          postal codes, when combined, can statistically identify an
          individual.
          
          - Prompt fatigue and a loss in trust by users when they are
          prompted by a large number of websites to share personal information.
          
          - Increased potential for [surveillance](https://www.rfc-editor.org/info/rfc6973/#section-5.1.1)
          and restrictions on pseudonymous use of online services. Collusion
          between [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) and [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), or other parties, might result
          in the ability to closely monitor a user's activity on the Web and
          take adverse action against this individual. Even when no action is
          taken, the possibility of surveillance alone can cause anxiety,
          discomfort, and behavioral changes such as inhibition and
          self-censorship, impacting individual autonomy and freedom of
          expression.
          
          - 
          [Exclusion
          and discrimination](https://github.com/w3c/credential-considerations/blob/main/credentials-considerations.md#restrictions-of-free-expression) of individuals who cannot, or do not want to,
          provide these credentials, prohibiting them from participation in
          services that would previously not require government-issued
          credentials, such as forums and social media platforms on the Web.
          
        
##### 11.4.1.3 Mitigating unnecessary requests for government credentials
        
          The outlined risks of government-issued digital credentials present a
          challenge that cannot be solved by a single participant in the
          ecosystem, and will require a broader policy discussion within
          individual sovereign nations about the risks and benefits of
          accessing online services through real-world credentials.
        
        
          It is desirable that a government that issues digital credentials
          also enact laws and regulations that clearly define how and for what
          purposes those credentials are able to be used. All parties involved
          in the exchange, whether they are legally obliged to do so or not,
          are advised to support any government [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) authentication
          schemes, if they exist. The support for (and integration of)
          [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) authentication schemes such as [EUDI access and registration certificates](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/main/docs/annexes/annex-2/annex-2-high-level-requirements.md#a2327-topic-27---registration-of-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties) can mitigate risks of
          proliferation of unnecessary credential requests. However, the
          presence of such schemes is not guaranteed, which significantly
          increases the risk in a credential exchange.
        
        
          There are other practical steps that [user agents](https://infra.spec.whatwg.org/#user-agent) implementing the
          Digital Credentials API can take to reduce risk, increase user
          understanding, and prevent certain types of harm:
        
        
          - Only supporting protocols that enable selective disclosure and
          other techniques of data minimization can reduce the impact and
          likelihood of information leakage, and provide better context to
          users in permission and consent flows.
          
          - Support for protocols that allow unlinkability mechanisms such as
          [Zero-Knowledge Proofs](https://www.w3.org/TR/vc-data-model-2.0/#zero-knowledge-proofs) can
          prevent [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)-based surveillance and potential discrimination,
          by hiding the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers).
          
          - Offering useful context and a clearly understandable permission
          flow will help users make better decisions on whether or not to
          accept a credential exchange, which can reduce the viability of
          exchange requests that are made without a concrete user need.
          
        
        
          It is further critical that [user agents](https://infra.spec.whatwg.org/#user-agent) design a permission
          experience that accounts for the lack of these mitigations, e.g., the
          exchange of personal information from government credentials without
          any [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) authentication scheme. It is recommended that a
          higher level of friction and clear user messaging that highlights the
          involved risk be applied to these types of exchanges.
        
#### 11.4.2 Non-government-issued credentials
        
          Non-government-issued credentials include all other digital
          documents, certificates, and attestations that are not
          government-issued and don't represent government-issued documents.
          This could include proof of employment, (non-government) education
          credentials, or cinema tickets. Notably, their exchange is likely
          less restricted by laws and regulations. While these documents often
          don't exhibit the same risks as government-issued credentials, they
          could also contain identifiable or sensitive information.
        
##### 11.4.2.1 Risk of theft and leakage of non-government credentials
        
          The impact and viability of credential theft and leakage of
          non-government credentials is largely based on the content of each
          individual credential type. In general, it could lead to loss of
          control and exposure of sensitive private information, as well as
          impersonation and data theft, which can increase the likelihood of
          further attacks on the affected individual.
        
##### 11.4.2.2 Risk of proliferation of requests for non-government credentials
        
          The flexibility and lack of regulation of non-government credentials
          carries potential for abuse for the purpose of cross-site tracking
          and linking identities through long-lived identifiers, such as email
          address or phone number. [Verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) participating in a tracking
          scheme based on digital credentials could create user incentives to
          accept sharing identifier credentials across many sites ("loyalty
          cards" for the Web), without fully understanding the implications on
          their privacy.
        
        
          Even users unwilling to share their information in such a scheme
          could be affected by prompt fatigue and potentially risk exclusion
          from using these services.
        
##### 11.4.2.3 Mitigating unnecessary requests for non-government credentials
        
          For non-government-issued credentials, it is recommended that the
          [user agent](https://infra.spec.whatwg.org/#user-agent) understand the requested credential format and its
          privacy attributes, and build a risk framework that informs the
          context that is shown to the user, as well as the amount of friction
          that is appropriate for each credential type. Protocols and formats
          involved in the exchange of these credentials are generally expected
          to support features such as selective disclosure and unlinkability,
          but these features might not always be appropriate or necessary in
          the exchange of information, especially when it concerns low-risk
          credentials such as cinema tickets.
        
        
          A [user agent](https://infra.spec.whatwg.org/#user-agent) that recognizes the type of credential being
          requested is encouraged to customize its permission experience to
          best suit the requested credential and help users understand the
          consequences of sharing it.
        
        
          [User agents](https://infra.spec.whatwg.org/#user-agent) cannot be expected to understand all credential
          requests. A [user agent](https://infra.spec.whatwg.org/#user-agent) that does not recognize the type of
          credential being requested is advised to significantly increase user
          friction in their permission experience, and clearly communicate the
          risks of sharing unknown credentials with websites to the user. Note
          that this could require integration between
          [different user agents](https://w3c-fedid.github.io/digital-credentials/#multiple-user-agents) to apply
          appropriate levels of friction and transparency. For example, a
          browser might delegate knowledge about credential requests to the
          operating system, which might require [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager) to
          register known credential types and reject an exchange request for an
          unknown credential type.
        
        [Issue 100](https://github.com/w3c-fedid/digital-credentials/issues/100): Consider applying the robustness principle with regard to user agent request validation [discussion](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22discussion%22)[privacy-considerations](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-considerations%22)
          The need to provide users with appropriate transparency conflicts
          with the desire to enable the ecosystem to develop new credential
          formats without explicit [user agent](https://infra.spec.whatwg.org/#user-agent) buy-in.
        
##### 11.4.2.4 Reporting abuse
        [Issue 267](https://github.com/w3c-fedid/digital-credentials/issues/267): reporting abuse of credential requests [privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)[privacy-considerations](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-considerations%22)
          Consider an interoperable abuse reporting system for [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
          making unnecessary and abusive requests.

---

### 11.5 Fingerprinting and Data Leakage
        
        
#### 11.5.1 Browser fingerprinting
        
          While the API ensures that no user data is ever shared without a
          permission prompt (see the [[[#user-permission-and-transparency|User
          Permission and Transparency]] section), the longevity and uniqueness
          of real-world identifiers that are likely to be returned by the
          Digital Credentials API make it a potential target for trackers and
          fingerprinters.
        
        
          Even with selective disclosure, attackers might combine data from a
          digital credential (such as the user's age, or the credential
          [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), timestamps; see the [[[#leaking-incidental-data|Leaking
          Incidental Data]] section) to reidentify and/or fingerprint users.
        
        
          This attack might be harder for third-party attackers (such as
          scripts embedded on the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)'s pages but not actively
          collaborating with them for the purpose of tracking) because response
          encryption is mandatory and responses should be decrypted on the
          [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)'s server. The [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) could thus ensure not to
          reflect back decrypted information to client-side JavaScript. Not all
          [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) will choose to do so, however.
        
#### 11.5.2 Leaking incidental data with credential presentations
        
          To ensure authenticity of a credential, its presentation to
          [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) generally includes more information than the content
          the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) is requesting access to. It will usually contain at
          least a signature of the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and the [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager),
          and potentially other metadata.
        
        
          This additional information could be used to reidentify and
          fingerprint users, which is especially relevant when an otherwise
          unlinkable presentation is made.
        
        
          While the Digital Credentials API does not control the content of a
          credential response, [user agents](https://infra.spec.whatwg.org/#user-agent) can help protect users against
          this type of tracking through clearly highlighting which information
          likely gets shared with the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) beyond what was requested,
          and, more broadly, by identifying and blocking fingerprinting through
          the API by [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
        
#### 11.5.3 Revealing device properties through protocol availability
        
          The Digital Credentials API exposes information about which [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and [issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) protocols are supported by
          the [user agent](https://infra.spec.whatwg.org/#user-agent) through
          [userAgentAllowsProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential-useragentallowsprotocol)`()`. It mitigates browser
          fingerprinting and revealing information about the user's device
          configuration by not customizing its response based on, for example,
          which [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager) applications are installed on a user's
          device. The returned information is thus, at best, equivalent to a
          [user agent](https://infra.spec.whatwg.org/#user-agent) version.
        
#### 11.5.4 Avoiding leaks of credential availability
        
          The Digital Credentials API does not enable sites to learn whether a
          credential is available without first going through a
          [user permission flow](https://w3c-fedid.github.io/digital-credentials/#user-permission-and-transparency).
          Revealing the presence of credentials would be a risk to user
          privacy, as the presence of a credential is personal information that
          the user might not have preferred to share with the site, and, in
          combination with other signals, could be used to identify the user
          without their permission. It is also a risk to free expression, as
          websites might increasingly start to demand the presentation of these
          credentials from the user in order to access services, excluding
          individuals who are unwilling to present credentials.

---

### 11.6 User Permission and Transparency
        
        
        Issue: Work in progress
        
          The Digital Credentials API enables the sharing of highly personal,
          sensitive, and at-risk user information with websites via
          credentials, potentially granting the ability to track users online
          and offline, through permanent, unique, irrevocable, cross-context
          identifiers. It also reveals parts of the user's browsing activity as
          well as their intent to identify to specific websites and/or
          [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager). One crucial responsibility of the [user agent](https://infra.spec.whatwg.org/#user-agent) in a credential request is to gather permission from the user
          to proceed with the exchange of information.
        
        
          Important context details that are needed for a user to make an
          informed decision about proceeding with a credential exchange include
          the following:
        
        
          - The origin of the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) that requests the credential.
          
          - The information that is being requested, or that would be
          revealed by responding to the request.
          
          - Whether presenting this information will enable tracking.
          
          - Which [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager) can be used to fulfill the
          credential request.
          
          - Which credential would be used to share the requested
          information.
          
        
        
          It is advised that [user agents](https://infra.spec.whatwg.org/#user-agent) in their implementation ensure
          that the details listed are fully disclosed to the user before an
          exchange of any user-related information occurs.
        
        [Issue 252](https://github.com/w3c-fedid/digital-credentials/issues/252): Should we normatively define elements of a permission prompt? [privacy-considerations](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-considerations%22)
          Should these be normative in the spec?
        
        [Issue 44](https://github.com/w3c-fedid/digital-credentials/issues/44): API requests should provide the site with what they need to explain why and how requested credential information will be used [enhancement](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22enhancement%22)[pending closure](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22pending+closure%22)[privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)
          Should the API be designed so the site can provide in-context
          explanations?
        
#### 11.6.1 Handling multiple credential requests
        [Issue 286](https://github.com/w3c-fedid/digital-credentials/issues/286): Privacy Considerations for multiple presentation requests (and responses) [privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)[privacy-considerations](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-considerations%22)[v2](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22v2%22)
          We need to describe concerns, tradeoffs and possible mitigations of
          handling multiple requests and responses for credential presentation.
        
#### 11.6.2 Integrating Multiple User Agents
        
          Depending on the technical architecture of a user's system, it is
          likely that the definition of a "[user agent](https://infra.spec.whatwg.org/#user-agent)" will include
          multiple cooperating layers of the software stack, such as a browser
          and the operating system. The greatest priority for these layers has
          to be a safe and well-informed user permission experience. As such,
          integration can be vital for user safety. Some layers may hold
          information that is inaccessible by other layers, such as the
          availability of a user's credentials. Overprompting or prompting
          without sufficient context could lead to (exploitable) confusion and
          prompt blindness.
        
        
          For this reason, [user agents](https://infra.spec.whatwg.org/#user-agent) prompting for permission are
          encouraged to integrate software layers for an ideal user experience,
          if they consider it safe to do so. This could happen, for example, if
          a browser trusts the API contract of an operating system to show an
          appropriate prompt, and thus does not show a prompt itself.
        
#### 11.6.3 Permission Prior to Credential Manager Selection
        
          As part of the user permission flow, the [user agent](https://infra.spec.whatwg.org/#user-agent) needs to
          ensure that users retain the power to choose whether to forward a
          credential request to a [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager), and which credential
          manager to select. This is due to the information disclosure that
          happens as part of the request, and the ability of credential
          managers to retain or share this information at the time of the
          request.
        
#### 11.6.4 Permission vs. Consent
        
          The permission mediated by the [user agent](https://infra.spec.whatwg.org/#user-agent) is not consent, which
          has specific legal definitions that can vary among different legal
          and regulatory environments and may need to be collected by the
          [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager) before sharing information with the
          [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), or by the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) itself before initiating the
          request. With frameworks and regulations for obtaining consent still
          being developed, this API aims to enable the exchange of the
          necessary information, which could include the following:
        
        
          - The privacy policy of the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) receiving the credential.
          
          - The purpose for which the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) is requesting the
          information.
          
          - What the information will be used for.
          
          - How the information will be shared or retained.
          
          - Any evaluations and attestations of this information, if
          available.
          
          - Assertions of the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)'s legitimacy and registration for
          accessing the credential, such as [EUDI access and registration certificates](https://github.com/eu-digital-identity-wallet/eudi-doc-architecture-and-reference-framework/blob/main/docs/annexes/annex-2/annex-2-high-level-requirements.md#a2327-topic-27---registration-of-pid-providers-providers-of-qeaas-pub-eaas-and-non-qualified-eaas-and-relying-parties).
          
        
        
          As more of this information becomes available in a structured format,
          we expect [user agents](https://infra.spec.whatwg.org/#user-agent) and this specification to leverage it to
          improve the user permission experience as well.
