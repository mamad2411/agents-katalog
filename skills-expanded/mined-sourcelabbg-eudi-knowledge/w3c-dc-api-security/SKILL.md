---
name: "w3c-dc-api-security"
description: "Use when reviewing W3C Digital Credentials API security: credential protocol security, cross-device security, quishing, data integrity, XSS/CSRF protection, and session security. Also covers accessibility and internationalization."
sections:
  - "10. Security Considerations*This section is non-normative.*"
  - "10.1 Threat Model"
  - "10.2 Mitigations"
  - "10.3 Cross-Device Security and Proximity"
  - "12. Accessibility Considerations"
  - "13. Internationalization Considerations*This section is non-normative.*"
---

<!-- ARF version: draft-2025 -->
<!-- Tokens: ~5102 -->

## 10. Security Considerations*This section is non-normative.*
      
      
      
        The sections that follow describe the API's security properties, the
        threats in scope, the assumptions on which security depends, and
        residual threats that remain after the mitigations are applied. This
        specification defines requirements for the user agent's behavior only
        when mediating [credential responses](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-response).
      
      Note
        Other security considerations that depend on protocols, credential
        manager implementations, operating systems, or transport security are
        described as expectations or preconditions, but these are not
        normatively required by this specification unless already normatively
        specified.
      
### 10.1 Threat Model
      
        The threat model for this specification includes threats to this API
        and to adjacent standards of the ecosystem.
      
      
        For this specification, threats fall into two categories: [in-scope threats](https://w3c-fedid.github.io/digital-credentials/#dfn-in-scope-threats) and [out-of-scope threats](https://w3c-fedid.github.io/digital-credentials/#dfn-out-of-scope-threats).
      
#### 10.1.1 In-Scope Threats
      
        In-Scope Threats are introduced or addressed by the DC API
        itself. The following are [in-scope threats](https://w3c-fedid.github.io/digital-credentials/#dfn-in-scope-threats) for this specification:
      
      
        
          Request Tampering
        
        
          A network attacker that can inject or modify page content in an
          insecure context attempts to alter a [DigitalCredentialGetRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest)
          or [DigitalCredentialCreateRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest) before processing.
        
        
          API Flooding
        
        
          A malicious website attempts to overwhelm the API by making rapid,
          repeated requests to exhaust system resources, confuse the user,
          create unnecessary credential interactions, or cause prompt fatigue
          that degrades user experience. This includes making requests at
          inappropriate times, such as during page load or without meaningful
          user context.
        
        
          Unauthorized Cross-Origin Access
        
        
          A malicious website attempts to request or issue digital credentials
          through embedded third-party content, such as an `[iframe](https://html.spec.whatwg.org/multipage/iframe-embed-object.html#the-iframe-element)`, without
          explicit permission from the embedding site, potentially enabling
          credential harvesting or unauthorized access to sensitive user data.
        
      
#### 10.1.2 Out of Scope Threats
      
        Out-of-scope threats are those handled by protocols,
        [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager), OS platform security, or transport layers.
        Even if "out of scope", they are relevant because they influence the
        end-to-end security of credential presentation and issuance. The
        following defines the [out-of-scope threats](https://w3c-fedid.github.io/digital-credentials/#dfn-out-of-scope-threats) for this specification:
      
      
        - To be written...
        
      
### 10.2 Mitigations
      
        The following mitigations address [in-scope threats](https://w3c-fedid.github.io/digital-credentials/#dfn-in-scope-threats) through
        normative requirements in the specification.
      
      
        WebIDL [interfaces](https://webidl.spec.whatwg.org/#dfn-interface) of the Digital Credential API are only exposed in
        [secure contexts](https://html.spec.whatwg.org/multipage/webappapis.html#secure-context), reducing the risk of [tampering](https://w3c-fedid.github.io/digital-credentials/#dfn-request-tampering) through
        [insecure contexts](https://html.spec.whatwg.org/multipage/webappapis.html#secure-context) (e.g., a malicious script being
        injected through the network). Please refer to the
        [5 Security Considerations](https://www.w3.org/TR/secure-contexts/#security-considerations) section of the
        [Secure Contexts](https://www.w3.org/TR/secure-contexts/) specification for more information.
      
      
        Additionally, requests from an [opaque origin](https://html.spec.whatwg.org/multipage/browsers.html#concept-origin-opaque) are rejected. Calls to
        [[[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors)](https://w3c-fedid.github.io/digital-credentials/#dfn-discoverfromexternalsource-origin-options-sameoriginwithancestors) and [[[Create]](origin, options, sameOriginWithAncestors)](https://w3c-fedid.github.io/digital-credentials/#dfn-create-origin-options-sameoriginwithancestors) from an [opaque origin](https://html.spec.whatwg.org/multipage/browsers.html#concept-origin-opaque) (for
        example, a `data:` document, or a document sandboxed without
        `allow-same-origin`) are [rejected](https://webidl.spec.whatwg.org/#reject), reducing the risk of
        malicious extraction or spoofing from untrusted environments.
      
      
        The Digital Credentials API reduces [API flooding](https://w3c-fedid.github.io/digital-credentials/#dfn-api-flooding) through two
        mechanisms:
      
      
        - 
          **Transient activation:** Both
          [[[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors)](https://w3c-fedid.github.io/digital-credentials/#dfn-discoverfromexternalsource-origin-options-sameoriginwithancestors) and [[[Create]](origin, options, sameOriginWithAncestors)](https://w3c-fedid.github.io/digital-credentials/#dfn-create-origin-options-sameoriginwithancestors) methods [Consume user activation](https://html.spec.whatwg.org/multipage/interaction.html#consume-user-activation), preventing automated or repeated requests without user
          interaction.
        
        - 
          **Always required mediation:** The API makes [user mediation](https://www.w3.org/TR/credential-management-1/#user-mediated) implicitly "[required](https://www.w3.org/TR/credential-management-1/#dom-credentialmediationrequirement-required)"
          (see [the DigitalCredential
          interface](https://w3c-fedid.github.io/digital-credentials/#the-digitalcredential-interface)), ensuring that user permission is obtained through the
          platform's credential chooser interface for every credential
          operation.
        
      
      
        For additional guidance on preventing abuse of credential requests,
        please refer to the section
        [7 Privacy Considerations](https://www.w3.org/TR/credential-management-1/#privacy-considerations) of the
        [Credential Management Level 1](https://www.w3.org/TR/credential-management-1/) specification. Note, however, that these
        protections have limitations, as sites may still employ dark patterns
        to encourage unnecessary user interactions that trigger credential
        requests.
      
      
        The Digital Credentials API reduces [cross-origin abuse](https://w3c-fedid.github.io/digital-credentials/#dfn-unauthorized-cross-origin-access) through integration with
        [Permissions Policy](https://www.w3.org/TR/permissions-policy-1/) (see [Permissions Policy
        Integration](https://w3c-fedid.github.io/digital-credentials/#permissions-policy)). The [request a Credential](https://www.w3.org/TR/credential-management-1/#abstract-opdef-request-a-credential) and [create a Credential](https://www.w3.org/TR/credential-management-1/#abstract-opdef-create-a-credential) algorithms respectively serve as policy enforcement
        points for the ["digital-credentials-get"](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credentials-get) and
        ["digital-credentials-create"](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credentials-create) [policy-controlled features](https://www.w3.org/TR/permissions-policy-1/#policy-controlled-feature). The
        two features are intentionally separate: a site may enable
        ["digital-credentials-get"](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credentials-get) without enabling
        ["digital-credentials-create"](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credentials-create), and vice versa, limiting each
        embedded context to only the capability it requires. Please refer to
        section [Permissions Policy](https://www.w3.org/TR/permissions-policy-1/#privacy-and-security) of the
        [Permissions Policy](https://www.w3.org/TR/permissions-policy-1/) specification for additional security
        properties provided by this integration.
      
### 10.3 Cross-Device Security and Proximity
        
        
        
          The Digital Credentials API supports cross-device experiences where a
          user presents a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) from a secondary device, such
          as a smartphone acting as a [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager), to a primary
          device, such as a laptop. Although the specific data exchange
          protocols (e.g., cryptographic formats and transports) are out of
          scope for this API, such cross-device interactions typically rely on
          established protocols like the Client to Authenticator Protocol
          (CTAP) ([Client to Authenticator Protocol (CTAP)](https://fidoalliance.org/specs/fido-v2.3-ps-20260226/fido-client-to-authenticator-protocol-v2.3-ps-20260226.html)).
        
        
          These protocols ensure security by establishing cryptographically
          secure channels and enforcing physical proximity (e.g., via Bluetooth
          Low Energy) to mitigate remote relay attacks. Crucially, in a
          cross-device flow, the [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager) cannot inherently trust
          the [origin](https://html.spec.whatwg.org/multipage/browsers.html#concept-origin) string forwarded by the primary device, as the primary
          device or its browser might be compromised. Therefore, protocols that
          employ signed requests, where the [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) cryptographically
          proves its identity, provide significantly stronger security
          assurances than relying solely on the browser-asserted [origin](https://html.spec.whatwg.org/multipage/browsers.html#concept-origin).

---

## 12. Accessibility Considerations
      
      
      
        The user interface for selecting and authorizing a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) is provided by the platform and is largely outside the
        scope of this specification; however, the accessibility of that
        experience is within scope (see [3. 
      Scope](https://w3c-fedid.github.io/digital-credentials/#scope)). The following guidance
        applies to [user agents](https://infra.spec.whatwg.org/#user-agent) and platforms implementing the [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser) and the flows around it, and references the
        relevant success criteria of [[WCAG22](https://w3c-fedid.github.io/digital-credentials/#bib-wcag22)]. Where the chooser is a non-web
        user interface, those criteria apply as described in [[WCAG2ICT-22](https://w3c-fedid.github.io/digital-credentials/#bib-wcag2ict-22)].
      
      
        The content of modal dialogs presented during [issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) or [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request), which can include
        text, QR codes, and other visual media, SHOULD be labelled and exposed
        to assistive technologies with appropriate names, roles, and values
        (see [Success Criterion 4.1.2 Name, Role, Value](https://www.w3.org/TR/WCAG22/#name-role-value)), and SHOULD provide text
        alternatives for non-text content (see [Success Criterion 1.1.1 Non-text Content](https://www.w3.org/TR/WCAG22/#non-text-content)).
      
      
        Changes in the state of an interaction, such as waiting for another
        device, a successful response, an error, or a cancellation, SHOULD be
        programmatically determinable and conveyed to assistive technologies
        without requiring a change of focus (see [Success Criterion 4.1.3 Status Messages](https://www.w3.org/TR/WCAG22/#status-messages)).
      
      
        When an operation fails, the [user agent](https://infra.spec.whatwg.org/#user-agent) rejects with one of several
        distinct errors; for example, a "[NotAllowedError](https://webidl.spec.whatwg.org/#notallowederror)",
        "[InvalidStateError](https://webidl.spec.whatwg.org/#invalidstateerror)", or "[OperationError](https://webidl.spec.whatwg.org/#operationerror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException), or a
        [TypeError](https://webidl.spec.whatwg.org/#exceptiondef-typeerror). Where the platform surfaces such a failure to the user,
        it SHOULD identify in text what went wrong and, where applicable, how
        to recover, rather than only signalling that an error occurred (see
        [Success Criterion 3.3.1 Error Identification](https://www.w3.org/TR/WCAG22/#error-identification)).
      
      
        Interactive elements, particularly those that allow the user to
        continue or abort an [issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request)
        or [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) request,
        MUST be operable in a device-independent manner (for example, via the
        keyboard; see [Success Criterion 2.1.1 Keyboard](https://www.w3.org/TR/WCAG22/#keyboard)). In particular, activation MUST NOT require a multipoint or path-based gesture (see
        [Success Criterion 2.5.1 Pointer Gestures](https://www.w3.org/TR/WCAG22/#pointer-gestures)) or device motion (see
        [Success Criterion 2.5.4 Motion Actuation](https://www.w3.org/TR/WCAG22/#motion-actuation)) as the only means of operation. The
        [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser) SHOULD present its controls in a
        meaningful focus order (see [Success Criterion 2.4.3 Focus Order](https://www.w3.org/TR/WCAG22/#focus-order)), move focus into
        the chooser when it is opened; keep focus within it while it is shown;
        and restore focus to the previously focused element, or another
        appropriate location, when it is closed.
      
      
        Where releasing a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) requires the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to
        authenticate, an accessible authentication method SHOULD be available.
        Where a step relies on a cognitive function test, such as recalling a
        password, an alternative that does not require one SHOULD be offered
        (see [Success Criterion 3.3.8 Accessible Authentication (Minimum)](https://www.w3.org/TR/WCAG22/#accessible-authentication-minimum)); and
        authentication SHOULD NOT depend solely on a single physical
        characteristic, such as a biometric, that some users cannot provide.
        This step is typically performed by the platform or [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager) and is otherwise outside the scope of this specification.
      
      
        Some platforms fulfil [presentation requests](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request)
        across devices; for example, by displaying a QR code for the user to
        scan with a separate device. Because such flows can depend on vision, a
        camera, or the use of a second device, platforms SHOULD provide an
        equivalent and accessible means of completing the interaction that does
        not rely on a single sensory ability or input modality. A cross-device
        request conveyed only through a visual artifact such as a QR code, with
        no accessible alternative, excludes users who cannot use that modality.
      
      
        An interaction may be subject to time limits from more than one source.
        These SHOULD be handled so that users who need more time are not
        excluded (see [Success Criterion 2.2.1 Timing Adjustable](https://www.w3.org/TR/WCAG22/#timing-adjustable)):
      
      
        - A site can bound the interaction by passing an [AbortSignal](https://dom.spec.whatwg.org/#abortsignal) as
        [signal](https://www.w3.org/TR/credential-management-1/#dom-credentialrequestoptions-signal); for example, one created with
        `AbortSignal.timeout()`. Sites SHOULD allow sufficient time and SHOULD NOT impose a short limit that rushes the user.
        
        - A proximity check is a security-essential, real-time constraint
        that cannot be extended without defeating its purpose. In this case,
        the platform SHOULD make the remaining time programmatically
        determinable, and SHOULD allow the user to retry the interaction.
        
        - The validity window of a cross-device request SHOULD be extendable
        or able to be retried.
        
      
      
        The decision to review and disclose a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) SHOULD NOT
        be subject to a forcing countdown, including time pressure inherited
        from the surrounding site flow.
      
      
        Human-readable credential content shown during an interaction, together
        with any accessible alternatives for it such as text alternatives for
        images, is carried within the credential payload and is the
        responsibility of the relevant credential format and protocol. Those
        formats and protocols also determine the language and direction of that
        content.

---

## 13. Internationalization Considerations*This section is non-normative.*
      
      
      
        This API is agnostic to credential formats and exchange protocols, and
        treats the request payloads ([DigitalCredentialGetRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest)'s
        [data](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest-data) and
        [DigitalCredentialCreateRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest)'s
        [data](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest-data)) and the response payload
        ([DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential)'s [data](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential-data)) as opaque. As a
        result, the API defines no string-typed values that carry
        human-readable, natural language content:
      
      
        - The string-typed values it defines, most notably [protocol identifiers](https://w3c-fedid.github.io/digital-credentials/#dfn-protocol-identifier), are restricted
        to ASCII ([ASCII lower alpha](https://infra.spec.whatwg.org/#ascii-lower-alpha), U+002D HYPHEN-MINUS, and [ASCII digit](https://infra.spec.whatwg.org/#ascii-digit)) and compared by exact equality. They are machine identifiers,
        not human-readable text, so normalization, case folding, and language
        or direction metadata do not apply.
        
        - All payloads are exchanged as JSON text and JavaScript values. When
        a JSON string is encoded as bytes (for example, for transport), it is
        encoded using UTF-8. Request payloads are serialized using [serialize a JavaScript value to a JSON string](https://infra.spec.whatwg.org/#serialize-a-javascript-value-to-a-json-string), which calls the ECMAScript
        `JSON.stringify` operation, and responses are parsed using [parse a JSON string to a JavaScript value](https://infra.spec.whatwg.org/#parse-a-json-string-to-a-javascript-value). Because `JSON.stringify` emits
        lone (unpaired) surrogate code points as `\uXXXX` escape sequences, the
        serialized request is always well-formed, UTF-8-encodable JSON.
        
        - Human-readable, localizable credential content (for example, the
        values of credential claims such as a name or address, including their
        representation in different scripts and languages) is carried opaquely
        within the credential payload. Its internationalization is determined
        by the relevant credential format and [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) or [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) (for example,
        the formats defined in [ISO/IEC 18013-5:2021 ISO-compliant driving licence, Part 5: Mobile driving licence (mDL) application](https://www.iso.org/standard/69084.html), and protocols such as
        [OpenID for Verifiable Presentations 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html)), which this specification expects to provide language
        and direction metadata, and localized alternatives, where appropriate.
        
        - The one value the API routes to the platform that a [user agent](https://infra.spec.whatwg.org/#user-agent)
        may display is the requesting [top-level origin](https://w3c-fedid.github.io/digital-credentials/#dfn-top-level-origin).
        Rendering an origin's host to the user, including the handling of
        internationalized domain names and bidirectional text, follows the
        [host-rendering guidance in the URL
        Standard](https://url.spec.whatwg.org/#url-rendering-i18n) and is out of scope for this specification.
        
        - Any other text presented to the user during a credential
        interaction is rendered either by the website (using HTML, which
        provides language and direction support through the host language), or
        by the platform's [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser). The chooser is out of
        scope for this specification; where it displays credential content, the
        language and direction of that content, as provided by the credential
        format and protocol, govern its presentation.
        
      
      
        Consequently, this specification introduces no natural language text
        that requires language or direction metadata. Were a future revision to
        introduce site-authored human-readable text at the API layer,
        normatively defined permission prompt text, or a user-agent-drawn
        presentation element, that text would need to carry, or be associated
        with, appropriate language and direction metadata.
