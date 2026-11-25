---
name: "w3c-dc-api-interface"
description: "Use when implementing the W3C Digital Credentials API surface: the DigitalCredential interface, CredentialRequestOptions and CredentialCreationOptions extensions, the digital member, protocol registry, Credential Management Level 1 integration, and Permissions Policy integration."
sections:
  - "5. Protocols"
  - "5.1 Convert request protocol"
  - "7. The Digital Credentials API"
  - "7.1 Extensions to CredentialRequestOptions dictionary"
  - "7.2 The DigitalCredentialRequestOptions dictionary"
  - "7.3 The DigitalCredentialGetRequest dictionary"
  - "7.4 Extensions to CredentialCreationOptions dictionary"
  - "7.5 The DigitalCredentialCreationOptions dictionary"
  - "7.6 The DigitalCredentialCreateRequest dictionary"
  - "7.7 The DigitalCredential interface"
  - "7.8 Supporting Data Structures"
  - "8. Integration with [Credential Management Level 1](https://www.w3.org/TR/credential-management-1/)"
  - "8.1 [[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors) internal method"
  - "8.2 [[Store]](credential, sameOriginWithAncestors) internal method"
  - "8.3 [[Create]](origin, options, sameOriginWithAncestors) internal method"
  - "8.4 [[type]] internal slot"
  - "8.5 [[discovery]] internal slot"
  - "8.6 User permission*This section is non-normative.*"
  - "9. Permissions Policy integration"
---

<!-- ARF version: draft-2025 -->
<!-- Tokens: ~7939 -->

## 5. Protocols
    
      Use of the following [presentation protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) is
      defined by this specification.
    
    [Issue 439](https://github.com/w3c-fedid/digital-credentials/issues/439): What protocols should a user agent implement? [spec](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22spec%22)[substantive](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22substantive%22)In [#401](https://github.com/w3c-fedid/digital-credentials/pull/401), I suggested we add the following:
```
<p>
       A [=user agent=] MUST implement at least one of the [=digital credential/exchange protocol=] listed in the [=table of exchange protocols=].
       It is RECOMMENDED that user agent to implement all the [=digital credential/exchange protocols=] listed in the [=table of exchange protocols=]. 
    </p>
    <aside class="note" title="Checking which exchange protocols a user agent allows">
      <p>Developers can check which [=digital credential/exchange protocols=]
      a user agent allows by calling the `DigitalCredential.`{{DigitalCredential.userAgentAllowsProtocol()}} static method.
      See [[[#checking-if-protocol-is-allowed]]] for a usage example.
      </p>
    </aside>
```
As:

- It forces user agents to support at least one - so at least developers know what they are going to get.
- It strongly encourages implementing all, but it doesn't force it (we can't force it regardless because of 3 below or because of platform limitations).
- It keeps existing and "legacy" user agents as compliant, specially in the case we add new exchange protocols in the future. For example, might be impossible to implement some protocol on a particular platform, but feasible to implement other protocols.

    
      
        Table of supported [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and [issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) protocols
      
      
        
          
            [Identifier](https://w3c-fedid.github.io/digital-credentials/#dfn-protocol-identifier)
          
          
            Specification
          
        
      
      
        
          
            [Presentation protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol)
          
        
        
          
            `openid4vp-v1-unsigned`
          
          
            [OpenID for Verifiable Presentations 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) § [A.3.1.
            Unsigned Request](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#name-unsigned-request)
          
        
        
          
            `openid4vp-v1-signed`
          
          
            [OpenID for Verifiable Presentations 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) § [A.3.2. Signed
            Request](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#name-signed-request)
          
        
        
          
            `openid4vp-v1-multisigned`
          
          
            [OpenID for Verifiable Presentations 1.0](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html) § [A.3.2.2.
            JWS JSON Serialization](https://openid.net/specs/openid-4-verifiable-presentations-1_0.html#name-jws-json-serialization) (Multi-signed requests)
          
        
        
          
            `org-iso-mdoc`
          
          
            [ISO/IEC 18013-7:2025 ISO-compliant driving licence, Part 7: Mobile driving licence (mDL) add-on functions](https://www.iso.org/standard/91154.html) § Annex C
          
        
      
      
        
          
            [Issuance protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol)
          
        
        
          
            `openid4vci-v1`
          
          
            [OpenID for Verifiable Credential Issuance 1.0](https://openid.net/specs/openid-4-verifiable-credential-issuance-1_0.html) § Coming Soon
            Issue: API Integration
              The OpenID Foundation is working on integration with Digital
              Credentials API. You can track progress at [OpenID4VCI#410](https://github.com/openid/OpenID4VCI/issues/410).
            
          
        
      
    
### 5.1 Convert request protocol
    
      To convert request protocol given a
      [DigitalCredentialGetRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest) or [DigitalCredentialCreateRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest)
      request:
    
    
      - If request is:
        
          
            A [DigitalCredentialGetRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest):
          
          
            
              - Let protocolString be request's
              [protocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest-protocol).
              
              - If protocolString does not equal any [enumeration value](https://webidl.spec.whatwg.org/#dfn-enumeration-value)
              in [DigitalCredentialPresentationProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialpresentationprotocol), return failure.
              
              - Return the [DigitalCredentialPresentationProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialpresentationprotocol)
              [enumeration value](https://webidl.spec.whatwg.org/#dfn-enumeration-value) whose value is protocolString.
              
            
          
          
            A [DigitalCredentialCreateRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest):
          
          
            
              - Let protocolString be request's
              [protocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest-protocol).
              
              - If protocolString does not equal any [enumeration value](https://webidl.spec.whatwg.org/#dfn-enumeration-value)
              in [DigitalCredentialIssuanceProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialissuanceprotocol), return failure.
              
              - Return the [DigitalCredentialIssuanceProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialissuanceprotocol)
              [enumeration value](https://webidl.spec.whatwg.org/#dfn-enumeration-value) whose value is protocolString.

---

## 7. The Digital Credentials API
    
      The [Digital Credentials API](https://w3c-fedid.github.io/digital-credentials/#DC-API) leverages the
      [Credential Management Level 1](https://www.w3.org/TR/credential-management-1/) specification, allowing [user agents](https://infra.spec.whatwg.org/#user-agent) to
      mediate the [issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) and [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) of [digital credentials](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
    
    
      The API allows [requesting](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) a
      [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) from the user agent, which in turn presents a
      [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser) to the user, allowing them to select a
      [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) that can fulfill the request. This is done by the
      website calling the
      `navigator.credentials.`[get](https://www.w3.org/TR/credential-management-1/#dom-credentialscontainer-get)`()` method, which runs
      the [request a Credential](https://www.w3.org/TR/credential-management-1/#abstract-opdef-request-a-credential) algorithm of [Credential Management Level 1](https://www.w3.org/TR/credential-management-1/).
      That algorithm then calls back into this specification's
      [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential) interface's
      [[[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors)](https://w3c-fedid.github.io/digital-credentials/#dfn-discoverfromexternalsource-origin-options-sameoriginwithancestors) internal method.
    
    
      Additionally, the API also allows [requesting issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) of a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential), which
      initiates a mediated issuance flow between the user agent and/or a
      [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders). This is done by calling the
      `navigator.credentials.`[create](https://www.w3.org/TR/credential-management-1/#dom-credentialscontainer-create)`()` method, which
      runs the [create a credential](https://www.w3.org/TR/credential-management-1/#abstract-opdef-create-a-credential) algorithm of
      [Credential Management Level 1](https://www.w3.org/TR/credential-management-1/). That algorithm then calls back into this
      specification's [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential) interface's
      [[[Create]](origin, options, sameOriginWithAncestors)](https://www.w3.org/TR/credential-management-1/#dom-credential-create-slot)
      internal method.
    
    
      Please see [Credential Management
      Integration](https://w3c-fedid.github.io/digital-credentials/#credential-management-integration) for complete details of how to integrate with the
      [Credential Management Level 1](https://www.w3.org/TR/credential-management-1/) specification.
    
### 7.1 Extensions to CredentialRequestOptions dictionary
    ```
WebIDLpartial dictionary CredentialRequestOptions {
  DigitalCredentialRequestOptions digital;
};
```
#### 7.1.1 The digital member
    
      The `digital` member
      allows for options to configure the request for a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
    
### 7.2 The DigitalCredentialRequestOptions dictionary
    ```
WebIDLdictionary DigitalCredentialRequestOptions {
  required sequence<DigitalCredentialGetRequest> requests;
};
```
#### 7.2.1 The requests member
    
      The `requests`
      specify an [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and [presentation request data](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request-data), which the user agent MAY match
      against a [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager), such as a digital wallet.
    
### 7.3 The DigitalCredentialGetRequest dictionary
    
      The [DigitalCredentialGetRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest) dictionary represents a [presentation request](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request). It is used to specify an [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and some [presentation request data](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request-data), which the user agent MAY match
      against a [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager), such as a digital wallet.
    
    ```
WebIDLdictionary DigitalCredentialGetRequest {
  required DOMString protocol;
  required object data;
};
```
#### 7.3.1 The protocol member
    
      The `protocol` member
      denotes the [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol).
    
    
      The [protocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest-protocol) member's value is one of the
      [protocol identifiers](https://w3c-fedid.github.io/digital-credentials/#dfn-protocol-identifier) defined in
      [DigitalCredentialPresentationProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialpresentationprotocol).
    
#### 7.3.2 The data member
    
      The `data` member is
      the [presentation request data](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request-data) to be handled by the
      [holder's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager), such as a digital identity wallet.
    
### 7.4 Extensions to CredentialCreationOptions dictionary
    ```
WebIDLpartial dictionary CredentialCreationOptions {
  DigitalCredentialCreationOptions digital;
};
```
#### 7.4.1 The digital member
    
      The `digital` member
      allows for options to configure the issuance of a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
    
### 7.5 The DigitalCredentialCreationOptions dictionary
    ```
WebIDLdictionary DigitalCredentialCreationOptions {
  required sequence<DigitalCredentialCreateRequest> requests;
};
```
#### 7.5.1 The requests member
    
      The `requests`
      specify an [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) and [issuance request data](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request-data), which the user agent MAY forward to a
      [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
    
### 7.6 The DigitalCredentialCreateRequest dictionary
    
      The [DigitalCredentialCreateRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest) dictionary represents an [issuance request](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request). It is used to specify an [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) and some [issuance request data](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request-data), to communicate the issuance request between the
      [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) and the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
    
    ```
WebIDLdictionary DigitalCredentialCreateRequest {
  required DOMString protocol;
  required object data;
};
```
#### 7.6.1 The protocol member
    
      The `protocol`
      member denotes the [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol).
    
    
      The [protocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest-protocol) member's value is one of
      the [protocol identifiers](https://w3c-fedid.github.io/digital-credentials/#dfn-protocol-identifier) defined in
      [DigitalCredentialIssuanceProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialissuanceprotocol).
    
#### 7.6.2 The data member
    
      The `data` member
      is the [issuance request data](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request-data) to be handled by the
      [holder's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager), such as a digital identity wallet.
    
### 7.7 The DigitalCredential interface
    
      The `DigitalCredential` interface represents a conceptual
      [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
    
    
      The [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential) interface mandates [user mediation](https://www.w3.org/TR/credential-management-1/#user-mediated) for all
      operations to ensure user control and consent.
    
    
      To simplify the developer experience of [get](https://www.w3.org/TR/credential-management-1/#dom-credentialscontainer-get)`()`
      calls involving a [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential), [user agents](https://infra.spec.whatwg.org/#user-agent) MUST NOT throw
      an error if the [mediation](https://www.w3.org/TR/credential-management-1/#dom-credentialrequestoptions-mediation) member is absent
      or has a value other than "[required](https://www.w3.org/TR/credential-management-1/#dom-credentialmediationrequirement-required)".
      Similarly, in [create](https://www.w3.org/TR/credential-management-1/#dom-credentialscontainer-create)`()` calls involving a
      [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential), [user agents](https://infra.spec.whatwg.org/#user-agent) MUST NOT throw an error if the
      [mediation](https://www.w3.org/TR/credential-management-1/#dom-credentialcreationoptions-mediation) member is absent or has a value
      other than "[required](https://www.w3.org/TR/credential-management-1/#dom-credentialmediationrequirement-required)". This makes
      "[required](https://www.w3.org/TR/credential-management-1/#dom-credentialmediationrequirement-required)" mediation an implicit and
      non-overridable behavior of the [API](https://w3c-fedid.github.io/digital-credentials/#DC-API).
    
    ```
WebIDLtypedef (DigitalCredentialPresentationProtocol or DigitalCredentialIssuanceProtocol) DigitalCredentialProtocol;

[Exposed=Window, SecureContext]
interface DigitalCredential : Credential {
  [Default] object toJSON();
  readonly attribute DigitalCredentialProtocol protocol;
  [SameObject] readonly attribute object data;
  static boolean userAgentAllowsProtocol(DOMString protocol);
};
```
#### 7.7.1 The protocol member
    
      The `protocol` member is the
      [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) that was used to request the
      [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential), or the [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol)
      that was used to issue the [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
    
#### 7.7.2 The data member
    
      The `data` member is the
      credential's response data. It contains the subset of JSON-parseable
      object types.
    
#### 7.7.3 The userAgentAllowsProtocol() method
    
      The [userAgentAllowsProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential-useragentallowsprotocol)`()` method allows digital
      credential [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) to determine which [presentation protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and [issuance protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) the user agent allows.
    
    Note
      This method does not convey [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol)
      or [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) support in the underlying
      OS/platform.
    
    
      User agents MUST NOT vary the response value based on any information
      about availability of hardware, presence or configuration of software,
      [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager), or digital credentials, or user configuration or
      preferences. If the response value varied, the user agent would introduce
      risks both of fingerprinting and of silently revealing other details
      about user behavior or configuration. The response value SHOULD vary only
      by user agent major version and indicate whether the browser supports
      distributing requests with that protocol to underlying platform or
      provider.
    
    
      To check whether a user agent allows protocol given a
      [DOMString](https://webidl.spec.whatwg.org/#idl-DOMString) protocol, take the following steps:
    
    
      - If protocol is not an [enumeration value](https://webidl.spec.whatwg.org/#dfn-enumeration-value) of
      [DigitalCredentialProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialprotocol), return `false`.
      
      - Return `true` if the user agent allows protocol, otherwise return
      `false`.
      
    
    
      When this method is invoked, the user agent MUST return the result of
      [user agent allows protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-user-agent-allows-protocol) given protocol.
    
### 7.8 Supporting Data Structures
    
      Data structures, such as enumerations, which support
      [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential) in this specification.
    
#### 7.8.1 The request context struct
    
      A request context is a [struct](https://infra.spec.whatwg.org/#struct) with the following
      [items](https://infra.spec.whatwg.org/#struct-item):
    
    
      
        requests
      
      
        A [list](https://infra.spec.whatwg.org/#list) of validated [credential requests](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request).
      
      
        top-level origin
      
      
        An [environment settings object](https://html.spec.whatwg.org/multipage/webappapis.html#environment-settings-object)'s [origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-origin).
      
    
#### 7.8.2 The [DigitalCredentialPresentationProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialpresentationprotocol) enumeration
    
      This enumeration's values correspond to the supported [presentation protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) listed in [5. 
      Protocols](https://w3c-fedid.github.io/digital-credentials/#protocols).
    
    ```
WebIDLenum DigitalCredentialPresentationProtocol {
  "openid4vp-v1-unsigned",
  "openid4vp-v1-signed",
  "openid4vp-v1-multisigned",
  "org-iso-mdoc"
};
```
#### 7.8.3 The [DigitalCredentialIssuanceProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialissuanceprotocol) enumeration
    
      This enumeration's values correspond to the supported [issuance protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) listed in [5. 
      Protocols](https://w3c-fedid.github.io/digital-credentials/#protocols).
    
    ```
WebIDLenum DigitalCredentialIssuanceProtocol {
  "openid4vci-v1",
};
```

---

## 8. Integration with [Credential Management Level 1](https://www.w3.org/TR/credential-management-1/)
### 8.1 [[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors) internal method
    
      When invoked, the [[DiscoverFromExternalSource]](origin, options,
      sameOriginWithAncestors) internal method, if the user agent doesn't
      support [presentation requests](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) (e.g., the platform
      cannot provide a [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser)), call the default
      implementation of [Credential](https://www.w3.org/TR/credential-management-1/#credential)'s
      [[[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors)](https://www.w3.org/TR/credential-management-1/#dom-credential-discoverfromexternalsource-slot) internal method with the same arguments.
      Otherwise:
    
    
      - Let signal be options's [signal](https://www.w3.org/TR/credential-management-1/#dom-credentialrequestoptions-signal), if
      present.
      
      - If origin is an [opaque origin](https://html.spec.whatwg.org/multipage/browsers.html#concept-origin-opaque), return [a promise rejected with](https://webidl.spec.whatwg.org/#a-promise-rejected-with) a "[SecurityError](https://webidl.spec.whatwg.org/#securityerror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
      
      - Let global be [this](https://webidl.spec.whatwg.org/#this)'s [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global).
      
      - Let document be global's [associated Document](https://html.spec.whatwg.org/multipage/nav-history-apis.html#concept-document-window).
      
      - If document is not a [fully active descendant of a top-level traversable with user attention](https://html.spec.whatwg.org/multipage/interaction.html#fully-active-descendant-of-a-top-level-traversable-with-user-attention), return [a promise rejected with](https://webidl.spec.whatwg.org/#a-promise-rejected-with) a "[NotAllowedError](https://webidl.spec.whatwg.org/#notallowederror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
      
      - Let requests be options's [digital](https://w3c-fedid.github.io/digital-credentials/#dom-credentialrequestoptions-digital)'s
      [requests](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialrequestoptions-requests) member.
      
      - If global does not have [transient activation](https://html.spec.whatwg.org/multipage/interaction.html#transient-activation), return [a promise rejected with](https://webidl.spec.whatwg.org/#a-promise-rejected-with) a "[NotAllowedError](https://webidl.spec.whatwg.org/#notallowederror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
      
      - [Consume user activation](https://html.spec.whatwg.org/multipage/interaction.html#consume-user-activation) of global.
      
      - Let promise be [a new promise](https://webidl.spec.whatwg.org/#a-new-promise) in [this](https://webidl.spec.whatwg.org/#this)'s [relevant realm](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-realm).
      
      - [Prepare credential requests](https://w3c-fedid.github.io/digital-credentials/#dfn-prepare-credential-requests) with
      document, requests, promise, and signal.
      
      - Return promise.
      
    
### 8.2 [[Store]](credential, sameOriginWithAncestors) internal method
    
      When invoked, the [[Store]](credential, sameOriginWithAncestors)
      MUST call the default implementation of [Credential](https://www.w3.org/TR/credential-management-1/#credential)'s
      [[[Store]](credential, sameOriginWithAncestors)](https://www.w3.org/TR/credential-management-1/#dom-credential-store-slot) internal
      method with the same arguments.
    
### 8.3 [[Create]](origin, options, sameOriginWithAncestors) internal method
    
      When invoked, the [[Create]](origin, options,
      sameOriginWithAncestors) internal method, if the user agent doesn't
      support [issuance requests](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request), call the default
      implementation of [Credential](https://www.w3.org/TR/credential-management-1/#credential)'s [[[Create]](origin, options, sameOriginWithAncestors)](https://www.w3.org/TR/credential-management-1/#dom-credential-create-slot) internal method with the same
      arguments. Otherwise:
    
    
      - Let signal be options's [signal](https://www.w3.org/TR/credential-management-1/#dom-credentialcreationoptions-signal), if
      present.
      
      - If signal is [aborted](https://dom.spec.whatwg.org/#abortsignal-aborted), return [a promise rejected with](https://webidl.spec.whatwg.org/#a-promise-rejected-with) signal's [abort reason](https://dom.spec.whatwg.org/#abortsignal-abort-reason).
      
      - If origin is an [opaque origin](https://html.spec.whatwg.org/multipage/browsers.html#concept-origin-opaque), return [a promise rejected with](https://webidl.spec.whatwg.org/#a-promise-rejected-with) a "[SecurityError](https://webidl.spec.whatwg.org/#securityerror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
      
      - Let global be [this](https://webidl.spec.whatwg.org/#this)'s [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global).
      
      - Let document be global's [associated Document](https://html.spec.whatwg.org/multipage/nav-history-apis.html#concept-document-window).
      
      - If document is not a [fully active descendant of a top-level traversable with user attention](https://html.spec.whatwg.org/multipage/interaction.html#fully-active-descendant-of-a-top-level-traversable-with-user-attention), return [a promise rejected with](https://webidl.spec.whatwg.org/#a-promise-rejected-with) a "[NotAllowedError](https://webidl.spec.whatwg.org/#notallowederror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
      
      - Let requests be options's [digital](https://w3c-fedid.github.io/digital-credentials/#dom-credentialcreationoptions-digital)'s
      [requests](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreationoptions-requests) member.
      
      - If global does not have [transient activation](https://html.spec.whatwg.org/multipage/interaction.html#transient-activation), return [a promise rejected with](https://webidl.spec.whatwg.org/#a-promise-rejected-with) a "[NotAllowedError](https://webidl.spec.whatwg.org/#notallowederror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
      
      - [Consume user activation](https://html.spec.whatwg.org/multipage/interaction.html#consume-user-activation) of global.
      
      - Let promise be [a new promise](https://webidl.spec.whatwg.org/#a-new-promise) in the [relevant realm](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-realm) of [this](https://webidl.spec.whatwg.org/#this).
      
      - [Prepare credential requests](https://w3c-fedid.github.io/digital-credentials/#dfn-prepare-credential-requests) with
      document, requests, promise, and signal.
      
      - Return promise.
      
    
### 8.4 [[type]] internal slot
    
      The [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential) [interface object](https://webidl.spec.whatwg.org/#dfn-interface-object) has an internal slot named
      [[type]]
      whose value is "digital".
    
### 8.5 [[discovery]] internal slot
    
      The [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential) [interface object](https://webidl.spec.whatwg.org/#dfn-interface-object) has an internal slot named
      [[discovery]]
      whose value is "remote".
    
### 8.6 User permission*This section is non-normative.*
    
      The [Digital Credentials API](https://w3c-fedid.github.io/digital-credentials/#DC-API) is a [powerful feature](https://www.w3.org/TR/permissions/#dfn-powerful-feature) that
      requires [express permission](https://www.w3.org/TR/permissions/#dfn-express-permission) from an end-user. This requirement is
      normatively enforced when calling [CredentialsContainer](https://www.w3.org/TR/credential-management-1/#credentialscontainer)'s
      [get](https://www.w3.org/TR/credential-management-1/#dom-credentialscontainer-get)`()` method.

---

## 9. Permissions Policy integration
      
      
      
        This specification defines two [policy-controlled features](https://www.w3.org/TR/permissions-policy-1/#policy-controlled-feature):
      
      
        
          "digital-credentials-get"
        
        
          A [policy-controlled feature](https://www.w3.org/TR/permissions-policy-1/#policy-controlled-feature) that allows a [document](https://dom.spec.whatwg.org/#concept-document) to
          [request](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) digital
          credentials. Its [default allowlists](https://www.w3.org/TR/permissions-policy-1/#policy-controlled-feature-default-allowlist) is
          ['self'](https://www.w3.org/TR/permissions-policy-1/#default-allowlist-self). The [request a Credential](https://www.w3.org/TR/credential-management-1/#abstract-opdef-request-a-credential)
          algorithm serves as the policy enforcement point.
        
        
          "digital-credentials-create"
        
        
          A [policy-controlled feature](https://www.w3.org/TR/permissions-policy-1/#policy-controlled-feature) that allows a [document](https://dom.spec.whatwg.org/#concept-document) to
          [issue](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) digital credentials.
          Its [default allowlists](https://www.w3.org/TR/permissions-policy-1/#policy-controlled-feature-default-allowlist) is ['self'](https://www.w3.org/TR/permissions-policy-1/#default-allowlist-self). The [create a Credential](https://www.w3.org/TR/credential-management-1/#abstract-opdef-create-a-credential) algorithm serves as
          the policy enforcement point.
