---
name: "w3c-dc-api-privacy"
description: "Use when reviewing W3C Digital Credentials API privacy design: design considerations and alternatives, the spectrum of privacy, and privacy properties of the presentation protocol and credential format."
sections:
  - "11.1 Design Considerations and Alternatives"
  - "11.2 Spectrum of Privacy"
  - "11.3 Presentation Protocol and Credential Format"
  - "11.3.1 Presentation Protocol Considerations for User Privacy"
---

<!-- ARF version: draft-2025 -->
<!-- Tokens: ~4400 -->

### 11.1 Design Considerations and Alternatives
        
        
        
          The Digital Credentials API is designed to mediate requests for
          digital credentials from websites, being agnostic to the credential
          format and the information contained in it, as well as the protocol
          used to exchange it. This and other key design choices are derived
          from the goal of providing a more secure and private credential
          exchange experience for users than the existing alternatives (e.g.,
          [[custom-schemes](https://w3c-fedid.github.io/digital-credentials/#bib-custom-schemes)]), that is still compatible with common exchange
          protocols for ease of adoption.
        
        
          The API provides the connection interface between [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) and
          [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders), i.e. the means by which a [credential presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol)
          is initiated and the user switches to the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) application to
          select a credential. Solutions that have been used for this purpose
          in the past include QR codes and custom URL schemes. As documented in
          [Presenting Credentials on the Web](https://docs.google.com/document/d/1Ppaz_EnhzHqPOz5UusRJvbSunh-RXPWgJ3Np_TM2EE0/) and [Concerns with custom schemes for identity presentment](https://github.com/w3c-fedid/digital-credentials/blob/main/custom-schemes.md),
          those solutions have security, privacy, and accessibility concerns.
        
        
          With adoption of digital credential technology being driven by
          ecosystem demand and regulatory mandates, the Web platform offers an
          alternative to the aforementioned less-desirable technologies that is
          easy to use for developers, is compatible with existing credential
          [presentation protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and, most importantly,
          has better user privacy, security, and accessibility properties for
          users than the aforementioned alternatives.
        
        
          The Digital Credentials API offers the [user agent](https://infra.spec.whatwg.org/#user-agent) the ability to
          intermediate on behalf of the user (e.g. in the form of a [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser)) to contextualize requests and
          [prevent
          immediate exposure to holder applications](https://w3c-fedid.github.io/digital-credentials/#permission-prior-to-credential-manager-selection). It also enforces
          certain minimum requirements on supported protocols, such as
          [response encryption](https://w3c-fedid.github.io/digital-credentials/#encrypting-credential-responses).
        
        Note
          The Digital Credentials API is not intended to inhibit the
          development of other standardized solutions that enhance user
          privacy. For example, an API could be standardized that more strictly
          enforces unlinkability for specific purposes such as age
          verification. Higher-level, designed-for-purpose APIs often enable
          [purpose limitation](https://www.w3.org/TR/privacy-principles/#purpose-limitation), ease
          of explanation to the user, and privacy and security protections from
          [user agents](https://infra.spec.whatwg.org/#user-agent).

---

### 11.2 Spectrum of Privacy
        
        
        
          The Digital Credentials API serves a variety of use cases with
          different grades of data disclosure and individual users with
          different preferences depending on the context that they are in.
          Notably, the privacy properties of a credential exchange mediated by
          this API could be mandated by the legal and regulatory environment of
          an individual user.
        
        
          This means that some users might not want, or be allowed, to use the
          most privacy-preserving means of exchanging credential information.
          Nonetheless, [user agents](https://infra.spec.whatwg.org/#user-agent) need to serve users with an experience
          that is private by default and protect them from harm.
        
        
          Because of this spectrum of preferences and use cases, it can be
          difficult for a [user agent](https://infra.spec.whatwg.org/#user-agent) to discern whether a user means to
          expose their personal information or is being tricked into doing so.
          It is thus the [user agent](https://infra.spec.whatwg.org/#user-agent)'s responsibility to ensure that every
          user understands what data they are sharing and who will participate
          in the exchange of information, before the exchange begins.

---

### 11.3 Presentation Protocol and Credential Format
        
        
        
          Because the Digital Credentials API sits at the center of an exchange
          that involves multiple independent parties, the [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and credential format used by
          these parties for exchanging user information are crucial to the
          [user agent](https://infra.spec.whatwg.org/#user-agent)'s goal of protecting user privacy.
        
#### 11.3.1 Presentation Protocol Considerations for User Privacy
        [Issue 255](https://github.com/w3c-fedid/digital-credentials/issues/255): Define concrete privacy and security requirements for the supported protocols [privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)[security-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22security-tracker%22)[registry](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22registry%22)[privacy-considerations](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-considerations%22)[security-considerations](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22security-considerations%22)There are two requirements for protocols that I think need further elaboration:

MUST have undergone privacy review [...]

And

MUST have undergone security review [...]

Technically, a review saying "this protocol is awful in every way" satisfies these criteria.
It would be more useful if there were a set of concrete privacy and security requirements that a protocol needed to satisfy, such a review would be able to say whether a standard was achieved or not.  It might be the case that there are subjective elements to a review, but there should also be a minimum bar that each protocol needs to clear.
This goes beyond the present set of requirements in the current [inclusion criteria](https://w3c-fedid.github.io/digital-credentials/#general-inclusion-criteria).  I don't have a comprehensive list to hand, but one should be possible to develop.  And once developed, that list should be in the spec.  For instance, does the protocol depend on [phoning home](https://nophonehome.com/)?  Does the protocol (or the formats it conveys) guarantee unlinkability of presentations?  Or - given that unlinkability doesn't make sense for some use cases - under what conditions does the API require the protocol provide unlinkability?  What sort of transparency affordances does the protocol include?  What sorts of covert channels are acceptable?
##### 11.3.1.1 Selective disclosure
        
          [Selective
          disclosure](https://github.com/w3c/credential-considerations/blob/main/credentials-considerations.md#selective-disclosure) is a fundamental technique for
          [data minimization](https://www.w3.org/TR/privacy-principles/#data-minimization) that
          allows [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to share the minimum required information that is
          requested by a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). Protocols are expected to facilitate
          selective disclosure by allowing the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to specify the
          exact claims needed.
        
##### 11.3.1.2 Unlinkable presentations
        
          [Unlinkability](https://github.com/w3c/credential-considerations/blob/main/credentials-considerations.md#unlinkable-presentations)
          is a property that ensures that, if a user presents attributes from a
          credential multiple times, [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) cannot link these separate
          presentations to conclude they concern the same user
          (verifier-verifier linkability), or that [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) cannot collude
          with [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) to report the exchange of a credential from a
          [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager) to the [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) (verifier-issuer
          linkability). The former is a property that can be maintained by the
          [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), e.g. through issuing fresh credentials for
          individual [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
        
        
          While the latter is achievable, e.g. through
          [zero-knowledge proofs](https://www.w3.org/TR/vc-data-model-2.0/#zero-knowledge-proofs),
          design choices of the API such as encrypted responses make it
          impossible for a [user agent](https://infra.spec.whatwg.org/#user-agent) to prove that verifier-issuer
          unlinkability was achieved in practice. Nonetheless, protocols are
          requested to limit linkability wherever possible.
        
        
          Note that unlinkability is exclusively a consideration for attributes
          that cannot be linked to a specific user identity. Inherently
          linkable attributes such as names, driver's license numbers, or phone
          numbers do not benefit from unlinkability.
        
        
          Through the Digital Credentials API, the [user agent](https://infra.spec.whatwg.org/#user-agent) can help
          [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) and [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager) exchange unlinkable
          attributes, but, because of response encryption, it cannot guarantee
          that no linkable information is passed between [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) and
          [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager). It is recommended that [user agents](https://infra.spec.whatwg.org/#user-agent)
          account for this fact in their user permission experience.
        
        [Issue 279](https://github.com/w3c-fedid/digital-credentials/issues/279): Linkability and issuer involvement as a protocol requirement [privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)
          Which level of unlinkability is the goal for this API? Can we
          normatively enforce support for any particular unlinkability
          features?
        
##### 11.3.1.3 "Phone home" mechanisms
        
          ["Phoning home"](https://github.com/w3c/credential-considerations/blob/main/credentials-considerations.md#no-phoning-home) refers
          to scenarios where the presentation or verification of a digital
          credential causes a notification or communication back to the
          [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) or another central entity, which can lead to tracking and
          profiling of individuals.
        
        
          Similar to unlinkability, it is impossible for [user agents](https://infra.spec.whatwg.org/#user-agent) to
          ensure that an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) isn't actively involved in the creation or
          validation of credential presentations after a user has given
          permission to proceed with a credential request. From that point on,
          the [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager) owns this decision. While some credential
          managers can be considered [user agents](https://infra.spec.whatwg.org/#user-agent), it is generally
          recommended that the [user agent](https://infra.spec.whatwg.org/#user-agent) implementing the
          [Digital Credentials API](https://w3c-fedid.github.io/digital-credentials/#DC-API) designs its permission
          experience to prevent
          [exposure of a
          request to the credential manager](https://w3c-fedid.github.io/digital-credentials/#permission-prior-to-credential-manager-selection) before user confirmation
          (keeping in mind [considerations for
          integrating multiple cooperating user agents](https://w3c-fedid.github.io/digital-credentials/#multiple-user-agents)).
        
        
          Protocols are required to support mechanisms that allow [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers),
          [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager), and [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to avoid or reduce the
          dependence on "phone home" mechanisms.
        
        [Issue 279](https://github.com/w3c-fedid/digital-credentials/issues/279): Linkability and issuer involvement as a protocol requirement [privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)
          Which level of unlinkability is the goal for this API? To what degree
          can the spec mandate restrictions to [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) involvement?
        
##### 11.3.1.4 Unlinkable revocation
        
          A common instance of [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) involvement in a credential exchange
          is for credential revocation checks. This is particularly challenging
          when presentations are intended to be verifier-issuer unlinkable.
          When credential presentations are made unlinkable through the use of
          e.g. [zero-knowledge proofs](https://www.w3.org/TR/vc-data-model-2.0/#zero-knowledge-proofs),
          the credential formats used in protocols are expected to support
          offline revocation methods such as [Cryptographic
          Accumulators](https://eprint.iacr.org/2024/657.pdf). It is further expected that protocol design and
          specification discourages the involvement of [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) for the
          purpose of revocation where possible.
        
        [Issue 280](https://github.com/w3c-fedid/digital-credentials/issues/280): Can we require protocols to support unlinkable revocation? [privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)[registry](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22registry%22)
          We should discuss whether unlinkable revocation techniques are
          practical enough to be required normatively.
        
##### 11.3.1.5 Support for user transparency, permission and consent
        
          User understanding and participation are non-negotiable properties of
          a credential presentation. The protocol is expected to help all
          involved parties enable user participation by providing the
          information vital for informed permission and/or consent.
        
##### 11.3.1.6 Support for verifier authorization
        
          Verifier authorization refers to the process by which a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
          proves its identity and demonstrates that it is legitimately entitled
          to request specific attributes or credentials. This is particularly
          useful when exchanging sensitive data, such as from government-issued
          credentials. Verifier authorization can limit unnecessary or abusive
          credential requests, and ensure that a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)'s access is
          restricted to the specific credential attributes it registered for.
        
        
          Checking verifier authorization is usually handled by the
          [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager), but [user agents](https://infra.spec.whatwg.org/#user-agent) could find the presence
          of such a scheme helpful in preventing API abuse and designing a
          well-informed user permission experience.
        
        [Issue 281](https://github.com/w3c-fedid/digital-credentials/issues/281): User agents that only support authorized verifiers (for government credentials) [privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)
          Should we require protocols to include provisions that allow [user agents](https://infra.spec.whatwg.org/#user-agent) to understand verifier authorization?
        
##### 11.3.1.7 Encrypting credential responses
        
          To prevent exposure of user information to other parties in
          "transit", for example browser extensions loaded on [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier)
          pages, and to encourage secure storage of user credentials by the
          [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), protocols are required to support and mandate encrypted
          responses in a credential exchange.
        
        [Issue 109](https://github.com/w3c-fedid/digital-credentials/issues/109): Should response encryption be required [discussion](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22discussion%22)[pending closure](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22pending+closure%22)[privacy-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22privacy-tracker%22)[security-tracker](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22security-tracker%22)Related to [#49](https://github.com/w3c-fedid/digital-credentials/issues/49) and several other discussions we've had: do we want to say that the response must always be encrypted (and if so, by which algorithms), or are we OK leaving that as optional?
