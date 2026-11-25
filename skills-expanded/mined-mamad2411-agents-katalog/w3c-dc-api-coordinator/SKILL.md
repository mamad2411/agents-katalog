---
name: "w3c-dc-api-coordinator"
description: "Use when implementing user-agent behaviour for the W3C Digital Credentials API: the Credential Request Coordinator, its interaction states, and the algorithms to prepare, validate, initiate, abort, and reject a credential request."
sections:
  - "6. Credential Request Coordinator"
  - "6.1 Interaction states"
  - "6.2 Prepare credential requests"
  - "6.3 Validate credential requests"
  - "6.4 Abort the credential request"
  - "6.5 Reject the credential request"
  - "6.6 Initiate the credential request"
---

<!-- ARF version: draft-2025 -->
<!-- Tokens: ~7485 -->

## 6. Credential Request Coordinator
    
      The credential request coordinator
      is a user-agent-defined component that mediates [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential)
      interactions through the [top-level traversable](https://html.spec.whatwg.org/multipage/document-sequences.html#top-level-traversable). Each [top-level traversable](https://html.spec.whatwg.org/multipage/document-sequences.html#top-level-traversable) has exactly one associated coordinator. The coordinator
      ensures that at most one interaction is active across all [child navigables](https://html.spec.whatwg.org/multipage/document-sequences.html#child-navigable), orchestrates the end-to-end flow of presentation or
      issuance, and manages transitions between [interaction states](https://w3c-fedid.github.io/digital-credentials/#dfn-interaction-states).
    
    
      The [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) maintains an active promise, which the user
      agent initializes as `null`. Through this [Promise](https://webidl.spec.whatwg.org/#idl-promise), the
      [coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) reflects the state of the asynchronous [credential request](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request) workflow to script and either
      [resolves](https://webidl.spec.whatwg.org/#resolve) with a [credential response](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-response) when the
      interaction completes successfully, or [rejects](https://webidl.spec.whatwg.org/#reject) when processing fails,
      when the user cancels the request via the UI, or when script aborts the
      operation via an [AbortSignal](https://dom.spec.whatwg.org/#abortsignal).
    
    
      The [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) maintains an abort signal, which the user agent
      initializes as `null`.
    
    
      The [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) maintains an abort algorithm, which the user
      agent initializes as `null`.
    
    
      The [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator):
    
    
      - Validates and transforms presentation or issuance inputs and outputs.
      
      - Requests the platform to display, for user selection, the credentials
      that are available for the current request and/or the [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) that
      can handle the current request. The availability of credentials and
      [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) is determined by matching the request parameters, user
      consent, and platform policy.
      
      - Manages [resolution](https://webidl.spec.whatwg.org/#resolve) or [rejection](https://webidl.spec.whatwg.org/#reject) of the
      [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) based on the
      interaction outcome.
      
    
    
      A user agent MAY delegate some or all coordinator responsibilities to
      external [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager), platform components, or other trusted
      entities according to user or platform policy.
    
    Note
      
        Although the coordinator handles input/output coordination, it is the
        responsibility of the platform together with available [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager), to present the UI that allows the user to choose a
        [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) and/or a [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager).
      
    
### 6.1 Interaction states
    
      The [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) has a finite set of
      interaction
      states, which are used to manage the lifecycle of a [credential request](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request):
    
    
      
        "idle":
      
      
        No [credential request](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request) is currently in progress.
      
      
        "requesting":
      
      
        A [credential request](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request) is in progress and the user
        interface is presented.
      
      
        "aborting":
      
      
        The active interaction is being canceled due to an error, a user
        action, or a [signal abort](https://dom.spec.whatwg.org/#abortcontroller-signal-abort); the coordinator is
        cleaning up before returning to "[idle](https://w3c-fedid.github.io/digital-credentials/#dfn-idle)".
      
    
    
      The coordinator is initialized in the [idle](https://w3c-fedid.github.io/digital-credentials/#dfn-idle) [interaction state](https://w3c-fedid.github.io/digital-credentials/#dfn-interaction-states).
    
### 6.2 Prepare credential requests
    
      To prepare credential
      requests given a [Document](https://dom.spec.whatwg.org/#concept-document) document, a [sequence](https://webidl.spec.whatwg.org/#idl-sequence)
      of [DigitalCredentialGetRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest) values or a [sequence](https://webidl.spec.whatwg.org/#idl-sequence) of
      [DigitalCredentialCreateRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest) values requests, a [Promise](https://webidl.spec.whatwg.org/#idl-promise)
      promise, and an optional [AbortSignal](https://dom.spec.whatwg.org/#abortsignal) signal:
    
    
      - Let global be document's [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global).
      
      - If the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) is not in the "[idle](https://w3c-fedid.github.io/digital-credentials/#dfn-idle)" [interaction state](https://w3c-fedid.github.io/digital-credentials/#dfn-interaction-states):
        
          - [Queue a global task](https://html.spec.whatwg.org/multipage/webappapis.html#queue-a-global-task) on the [DOM manipulation task source](https://html.spec.whatwg.org/multipage/webappapis.html#dom-manipulation-task-source)
          given global to [reject](https://webidl.spec.whatwg.org/#reject) promise with a "[NotAllowedError](https://webidl.spec.whatwg.org/#notallowederror)"
          [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
          
          - Return.
          
        
      
      - [Assert](https://infra.spec.whatwg.org/#assert): the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) is `null`.
      
      - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) [interaction state](https://w3c-fedid.github.io/digital-credentials/#dfn-interaction-states) to "[requesting](https://w3c-fedid.github.io/digital-credentials/#dfn-requesting)".
      
      - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) to promise.
      
      - Let validatedRequests be the result of [validate credential requests](https://w3c-fedid.github.io/digital-credentials/#dfn-validate-credential-requests) given requests. If that
      [throws](https://webidl.spec.whatwg.org/#dfn-throw) an [exception](https://webidl.spec.whatwg.org/#dfn-exception) error, then:
        
          - [Reject the credential request with](https://w3c-fedid.github.io/digital-credentials/#dfn-reject-the-credential-request-with) error and promise.
          
          - Return.
          
        
      
      - If validatedRequests [is empty](https://infra.spec.whatwg.org/#list-is-empty), then:
        
          - [Reject the credential request with](https://w3c-fedid.github.io/digital-credentials/#dfn-reject-the-credential-request-with) a newly created [TypeError](https://webidl.spec.whatwg.org/#exceptiondef-typeerror) and promise.
          
          - Return.
          
        
      
      - If signal was passed, then:
        
          - [Assert](https://infra.spec.whatwg.org/#assert): signal is not [aborted](https://dom.spec.whatwg.org/#abortsignal-aborted).
            Note
              [Pre-aborted](https://dom.spec.whatwg.org/#abortsignal-aborted) [signals](https://dom.spec.whatwg.org/#abortcontroller-signal)
              are handled by [request a Credential](https://www.w3.org/TR/credential-management-1/#abstract-opdef-request-a-credential) and [create a Credential](https://www.w3.org/TR/credential-management-1/#abstract-opdef-create-a-credential) before this algorithm is invoked.
            
          
          - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [abort signal](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-signal) to signal.
          
          - Let abortAlgorithm be the following algorithm, closing over
          promise and signal:
            
              - If the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) is not promise, return.
              
              - [Abort the credential request](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-the-credential-request) given signal's [abort reason](https://dom.spec.whatwg.org/#abortsignal-abort-reason).
              
            
          
          - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [abort algorithm](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-algorithm) to abortAlgorithm.
          
          - [Add](https://dom.spec.whatwg.org/#abortsignal-add) abortAlgorithm to signal.
          
        
      
      - If document stops being [fully active](https://html.spec.whatwg.org/multipage/document-sequences.html#fully-active), [abort the credential request](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-the-credential-request) with an
      "[AbortError](https://webidl.spec.whatwg.org/#aborterror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
      
      - Let handled be the result of running [handle virtual wallet behavior](https://w3c-fedid.github.io/digital-credentials/#dfn-handle-virtual-wallet-behavior) given promise and global.
      
      - If handled is `true`, return.
      
      - [Initiate the credential request](https://w3c-fedid.github.io/digital-credentials/#dfn-initiate-the-credential-request)
      with document, validatedRequests, promise, and signal.
      
    
### 6.3 Validate credential requests
    
      To validate credential
      requests given a sequence of [DigitalCredentialGetRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest) or
      [DigitalCredentialCreateRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest) objects requests:
    
    
      - Let validatedRequests be a new empty [list](https://infra.spec.whatwg.org/#list).
      
      - [For each](https://infra.spec.whatwg.org/#list-iterate) request of requests:
        
          - Let protocol be the result of running [convert request protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-convert-request-protocol) given request.
          
          - If protocol is failure, [continue](https://infra.spec.whatwg.org/#iteration-continue).
          
          - If [user agent allows protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-user-agent-allows-protocol) given protocol returns
          `false`, [continue](https://infra.spec.whatwg.org/#iteration-continue).
          
          - Let data be request's [data](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest-data),
          if request is a [DigitalCredentialGetRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialgetrequest), or request's
          [data](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest-data), if request is a
          [DigitalCredentialCreateRequest](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialcreaterequest).
          
          - [Serialize](https://infra.spec.whatwg.org/#serialize-a-javascript-value-to-a-json-string)
          data to a JSON string.
          
          - If serialization results in an [exception](https://webidl.spec.whatwg.org/#dfn-exception), [throw](https://webidl.spec.whatwg.org/#dfn-throw)
          that [exception](https://webidl.spec.whatwg.org/#dfn-exception).
          
          - Validate request's [presentation request data](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request-data) or [issuance request data](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request-data) according to
          request's [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) or [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) or other criteria. Validation
          requirements are protocol-specific and are outside the scope of this
          specification:
            Note: Validation details outside scope
              
                Validation includes verifying request's [presentation request data](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request-data) or [issuance request data](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request-data) conforms to the requirements
                of the specified [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol)
                or [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol). Please refer to
                the specification of the specific [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) or [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) for details, including potential
                reasons for validation failure, and any security and privacy
                considerations that need to be considered by implementers
                during validation.
              
            
            [Issue 472](https://github.com/w3c-fedid/digital-credentials/issues/472): User agent request validation and errors [spec](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22spec%22)[substantive](https://github.com/w3c-fedid/digital-credentials/issues/?q=is%3Aissue+is%3Aopen+label%3A%22substantive%22)The prepare steps originally stated that:

In addition to protocol-defined requirements, a [=user agent=] might apply additional validation criteria based on local policy, configuration, or evolving security considerations. For example, a [=user agent=] might reject a request that (a) seeks particular credential attributes, (b) uses or requires cryptographic algorithms the [=user agent=] is configured not to accept (e.g., as part of algorithm agility or a transition to post-quantum schemes), or (c) relies on certificates or trust anchors that are not accepted by the [=user agent=]'s configured trust decisions.

It would be good to expand on these.
            
              - If validation fails, [throw](https://webidl.spec.whatwg.org/#dfn-throw) an appropriate
              [exception](https://webidl.spec.whatwg.org/#dfn-exception).
              
              - Otherwise, [append](https://infra.spec.whatwg.org/#list-append) request to validatedRequests.
              
            
          
        
      
      - Return validatedRequests.
      
    
### 6.4 Abort the credential request
    
      To abort the
      credential request given a JavaScript value error:
    
    
      - If the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) is `null`, return.
      
      - Let activePromise be the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s
      [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise).
      
      - If the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) is in the "[requesting](https://w3c-fedid.github.io/digital-credentials/#dfn-requesting)" [interaction state](https://w3c-fedid.github.io/digital-credentials/#dfn-interaction-states):
        
          - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) [interaction state](https://w3c-fedid.github.io/digital-credentials/#dfn-interaction-states) to "[aborting](https://w3c-fedid.github.io/digital-credentials/#dfn-aborting)".
          
          - Dismiss the [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser).
            Note
              Dismissal can fail (e.g., if the [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser)
              was destroyed due to memory pressure), but the [coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)
              proceeds to complete the credential request regardless.
            
          
        
      
      - [Reject the credential request with](https://w3c-fedid.github.io/digital-credentials/#dfn-reject-the-credential-request-with)
      error and activePromise.
      
    
### 6.5 Reject the credential request
    
      To reject the
      credential request with a (JavaScript Value) error and a
      [Promise](https://webidl.spec.whatwg.org/#idl-promise) promise:
    
    
      - [Assert](https://infra.spec.whatwg.org/#assert): the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) is promise.
      
      - [Queue a global task](https://html.spec.whatwg.org/multipage/webappapis.html#queue-a-global-task) on the [DOM manipulation task source](https://html.spec.whatwg.org/multipage/webappapis.html#dom-manipulation-task-source) given
      promise's [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global) to perform the following steps:
        
          - If the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) is not promise, then return.
          
          - Let signal be the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s
          [abort signal](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-signal).
          
          - Let abortAlgorithm be the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s
          [abort algorithm](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-algorithm).
          
          - If signal is not `null` and abortAlgorithm is not `null`:
            
              - [Remove](https://dom.spec.whatwg.org/#abortsignal-remove) abortAlgorithm from signal.
              
            
          
          - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [abort signal](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-signal) to `null`.
          
          - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [abort algorithm](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-algorithm) to `null`.
          
          - [Reject](https://webidl.spec.whatwg.org/#reject) promise with error.
          
          - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) to `null`.
          
          - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) [interaction state](https://w3c-fedid.github.io/digital-credentials/#dfn-interaction-states) to "[idle](https://w3c-fedid.github.io/digital-credentials/#dfn-idle)".
          
        
      
    
### 6.6 Initiate the credential request
    
      To initiate the
      credential request given a [Document](https://dom.spec.whatwg.org/#concept-document) document, a [list](https://infra.spec.whatwg.org/#list) of
      validated credential requests validatedRequests, a [Promise](https://webidl.spec.whatwg.org/#idl-promise)
      promise, and an optional [AbortSignal](https://dom.spec.whatwg.org/#abortsignal) signal:
    
    
      - Let topLevelOrigin be document's [top-level traversable](https://html.spec.whatwg.org/multipage/document-sequences.html#top-level-traversable)'s
      [active document](https://html.spec.whatwg.org/multipage/document-sequences.html#nav-document)'s [relevant settings object](https://html.spec.whatwg.org/multipage/webappapis.html#relevant-settings-object)'s
      [origin](https://html.spec.whatwg.org/multipage/webappapis.html#concept-settings-object-origin).
      
      - Let requestData be a new [request context](https://w3c-fedid.github.io/digital-credentials/#dfn-request-context) whose [requests](https://w3c-fedid.github.io/digital-credentials/#dfn-requests) is validatedRequests and [top-level origin](https://w3c-fedid.github.io/digital-credentials/#dfn-top-level-origin) is topLevelOrigin.
      
      - [In parallel](https://html.spec.whatwg.org/multipage/infrastructure.html#in-parallel):
        
          - Display a [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser) with requestData and
          wait for one of the following outcomes:
            
              - The user selects a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) or [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) that
              can fulfill the request.
              
              - The user cancels the operation.
              
              - The platform encounters an error.
              
            
            
              When a [user agent](https://infra.spec.whatwg.org/#user-agent) communicates with a [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager)
              located on a different device, it is RECOMMENDED that the [user agent](https://infra.spec.whatwg.org/#user-agent) use [Client to Authenticator Protocol (CTAP)](https://fidoalliance.org/specs/fido-v2.3-ps-20260226/fido-client-to-authenticator-protocol-v2.3-ps-20260226.html).
            
          
          - If signal is not null and signal is [aborted](https://dom.spec.whatwg.org/#abortsignal-aborted):
            
              - Return.
                Note: Abort already handled
                  The abort algorithm [added](https://dom.spec.whatwg.org/#abortsignal-add) to signal by
                  the [prepare credential requests](https://w3c-fedid.github.io/digital-credentials/#dfn-prepare-credential-requests) steps handles tearing down the [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser).
                
              
            
          
          - If the user cancels the operation or no credential was selected:
            
              - Let error be a newly created "[NotAllowedError](https://webidl.spec.whatwg.org/#notallowederror)"
              [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
              
              - [Reject the credential request with](https://w3c-fedid.github.io/digital-credentials/#dfn-reject-the-credential-request-with) error and promise.
              
              - Return.
              
            
          
          - If the platform returns a platform-specific error:
            
              - Let error be determined as follows:
                
                  
                    The user agent or platform does not permit the operation:
                  
                  
                    A newly created "[NotAllowedError](https://webidl.spec.whatwg.org/#notallowederror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
                  
                  
                    The request data is malformed or invalid:
                  
                  
                    A newly created [TypeError](https://webidl.spec.whatwg.org/#exceptiondef-typeerror).
                  
                  
                    A credential request is already in progress:
                  
                  
                    A newly created "[InvalidStateError](https://webidl.spec.whatwg.org/#invalidstateerror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
                  
                  
                    Otherwise:
                  
                  
                    A newly created "[OperationError](https://webidl.spec.whatwg.org/#operationerror)" [DOMException](https://webidl.spec.whatwg.org/#idl-DOMException).
                  
                
              
              - [Reject the credential request with](https://w3c-fedid.github.io/digital-credentials/#dfn-reject-the-credential-request-with) error and promise.
              
              - Return.
              
            
          
          - If a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) was selected by the user:
            
              - Let protocol be the [protocol identifier](https://w3c-fedid.github.io/digital-credentials/#dfn-protocol-identifier) returned by the [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser) for
              this exchange.
                Note: Protocol is determined by the platform
                  The [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser) or underlying platform
                  determines which item in validatedRequests to forward to a
                  [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and returns the [protocol identifier](https://w3c-fedid.github.io/digital-credentials/#dfn-protocol-identifier) for that exchange. The user agent does not
                  necessarily know which specific item was selected.
                
              
              - Let responseData be a [string](https://infra.spec.whatwg.org/#string) [presentation response](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-response) or [string](https://infra.spec.whatwg.org/#string) [issuance response](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-response) returned by the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
                Note: Why the response is a string
                  The response is a string because the user agent is
                  responsible for parsing it into a JavaScript object in the
                  correct realm, verifying it is valid JSON, and confirming the
                  parsed value is an object, as required by the
                  [data](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential-data) attribute.
                
              
              - [Queue a global task](https://html.spec.whatwg.org/multipage/webappapis.html#queue-a-global-task) on the [DOM manipulation task source](https://html.spec.whatwg.org/multipage/webappapis.html#dom-manipulation-task-source) given document's [relevant global object](https://html.spec.whatwg.org/multipage/webappapis.html#concept-relevant-global) to perform
              the following steps:
                
                  - If the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) is not promise, then
                  return.
                  
                  - Let parsedResponseDataOrError be the result of [parse a JSON string to a JavaScript value](https://infra.spec.whatwg.org/#parse-a-json-string-to-a-javascript-value) given responseData.
                  
                  - Let abortSignal be the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [abort signal](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-signal).
                  
                  - Let abortAlgorithm be the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [abort algorithm](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-algorithm).
                  
                  - If abortSignal is not `null` and abortAlgorithm is
                  not `null`, [Remove](https://dom.spec.whatwg.org/#abortsignal-remove) abortAlgorithm from
                  abortSignal.
                  
                  - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [abort signal](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-signal) to `null`.
                  
                  - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [abort algorithm](https://w3c-fedid.github.io/digital-credentials/#dfn-abort-algorithm) to `null`.
                  
                  - If parsedResponseDataOrError is an [exception](https://webidl.spec.whatwg.org/#dfn-exception):
                    
                      - [Reject](https://webidl.spec.whatwg.org/#reject) promise with
                      parsedResponseDataOrError.
                      
                    
                  
                  - Otherwise, if parsedResponseDataOrError is not an
                  [object](https://html.spec.whatwg.org/multipage/iframe-embed-object.html#the-object-element):
                    
                      - [Reject](https://webidl.spec.whatwg.org/#reject) promise with a newly created
                      [TypeError](https://webidl.spec.whatwg.org/#exceptiondef-typeerror).
                      
                    
                  
                  - Otherwise:
                    
                      - Let credential be a newly created
                      [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential) instance with its
                      [data](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential-data) initialized to
                      parsedResponseDataOrError and its
                      [protocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential-protocol) initialized to protocol.
                      
                      - [Resolve](https://webidl.spec.whatwg.org/#resolve) promise with credential.
                      
                    
                  
                  - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator)'s [active promise](https://w3c-fedid.github.io/digital-credentials/#dfn-active-promise) to `null`.
                  
                  - Set the [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator) [interaction state](https://w3c-fedid.github.io/digital-credentials/#dfn-interaction-states) to "[idle](https://w3c-fedid.github.io/digital-credentials/#dfn-idle)".
