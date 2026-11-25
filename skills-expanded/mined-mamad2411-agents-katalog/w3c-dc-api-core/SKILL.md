---
name: "w3c-dc-api-core"
description: "Use when getting oriented in the W3C Digital Credentials API: what it is for, worked examples of requesting and issuing a credential (including cross-origin), scope, and terminology."
sections:
  - "1. Introduction*This section is non-normative.*"
  - "2. Examples of usage*This section is non-normative.*"
  - "2.1 Feature Detection"
  - "2.2 Checking if protocol is allowed"
  - "2.3 Requesting a digital credential"
  - "2.4 Issuing a digital credential"
  - "2.5 Requesting a digital credential across origins"
  - "2.6 Issuing a digital credential across origins"
  - "3. Scope*This section is non-normative.*"
  - "4. Terminology"
---

<!-- ARF version: draft-2025 -->
<!-- Tokens: ~6006 -->

## 1. Introduction*This section is non-normative.*
    
      This document defines an API enabling a website to request presentation
      and issuance of a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
    
    
      The API is agnostic to credential formats and is designed to be
      extensible to multiple [presentation protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and
      [issuance protocols](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol). See [5. 
      Protocols](https://w3c-fedid.github.io/digital-credentials/#protocols).
    
    
      The API is designed to support the following goals:
    
    
      - Keep the acts of [requesting](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) and [issuing](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) separate from the specific [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol) and [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol) respectively; thereby enabling the extensibility of such
      protocols and credential formats.
      
      - Require [presentation requests](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) and [issuance requests](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) to be unencrypted, enabling user-agent
      inspection for risk analysis.
      
      - Assume opaque (i.e., encrypted) [presentation responses](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-response) and [issuance responses](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-response), enabling
      [issuers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers), [verifiers](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier), and [holders](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) to control where potentially
      sensitive personally identifiable information is exposed.
      
      - Ensure that all credential interactions are user-mediated, giving
      users control and consent over the [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) and [issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) of their [digital credentials](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
      
      - Require [transient activation](https://html.spec.whatwg.org/multipage/interaction.html#transient-activation) to perform [presentation requests](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) or [issuance requests](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request), ensuring that sites cannot silently request or issue digital
      credentials without the user's active participation.
      
      - Enable platform-provided UX for credential and [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager)
      selection during requests for [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) or [issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request).
      
      - Enable platforms to provide secure cross-device [presentation requests](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) and [issuance requests](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) with proximity checks.
      
    
    
      [Digital credentials](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) of many types can be presented and issued using
      this API. Examples of these
      types include:
    
    
      - a driving license, passport, or other identity card issued by a
      government institution
      
      - a travel authorization document issued by an embassy or consulate
      
      - a proof of employment issued by a public or private organization
      
      - a proof of education or professional training issued by an
      institution
      
      - many other scenarios as described in [Verifiable Credentials Use Cases](https://www.w3.org/TR/vc-use-cases/)

---

## 2. Examples of usage*This section is non-normative.*
      
      
      
        The following examples illustrate how the [API](https://w3c-fedid.github.io/digital-credentials/#DC-API) can be used
        to request and issue digital credentials.
      
### 2.1 Feature Detection
      
        Before using the [API](https://w3c-fedid.github.io/digital-credentials/#DC-API), it's important to check if the user
        agent supports the necessary features. This can be done using the
        following code:
      
      
        
    [Example 1](https://w3c-fedid.github.io/digital-credentials/#example-checking-for-api-support): Checking for API support
   ```
if (typeof DigitalCredential !== "undefined") {
  // The API is supported
} else {
  // The API is not supported
}
```
      
### 2.2 Checking if protocol is allowed
      
        The [userAgentAllowsProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential-useragentallowsprotocol)`()` static method can
        be used to check if the user agent allows a specific protocol for
        digital credential issuance or presentation. This is useful for
        checking which protocols are allowed by the user's browsers prior to
        making an API call. On browsers that implement [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential)
        (detectable via the `typeof` check shown above), protocol identifiers
        are added to [DigitalCredentialProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialprotocol) progressively as [user agents](https://infra.spec.whatwg.org/#user-agent) adopt support for them, so calling this method with an unknown
        protocol identifier safely returns `false` without
        [throwing](https://webidl.spec.whatwg.org/#dfn-throw) an [exception](https://webidl.spec.whatwg.org/#dfn-exception). Note that calling this
        method on a browser where [DigitalCredential](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredential) is not defined will
        throw a [ReferenceError](https://webidl.spec.whatwg.org/#exceptiondef-referenceerror), so the `typeof DigitalCredential !==
        "undefined"` guard shown above is still required before using this
        method.
      
      
        
    [Example 2](https://w3c-fedid.github.io/digital-credentials/#example-using-the-useragentallowsprotocol-static-method): Using the userAgentAllowsProtocol() static method
   ```
if (DigitalCredential.userAgentAllowsProtocol("example-protocol")) {
  // DC API supported. Proceed with issuance or presentation.
} else {
  // DC API not supported. Fall back to, for example,
  // a traditional HTML form-based approach.
  showHTMLForm();
}
```
      
      
        Alternatively, one can check for support of multiple protocols,
        filtering out those that are not supported:
      
      
        
    [Example 3](https://w3c-fedid.github.io/digital-credentials/#example-checking-multiple-protocols-with-useragentallowsprotocol): Checking multiple protocols with userAgentAllowsProtocol()
   ```
const protocols = [
  "example-issuance-protocol",
  "another-issuance-protocol"
];
const supportedProtocols = protocols.filter(DigitalCredential.userAgentAllowsProtocol);
if (supportedProtocols.length > 0) {
  // At least one protocol is supported. Proceed with issuance.
} else {
  // No protocols are supported. Fall back to a different issuance method.
}
```
      
      
        Because protocol identifiers are added to [DigitalCredentialProtocol](https://w3c-fedid.github.io/digital-credentials/#dom-digitalcredentialprotocol)
        progressively, one can use this method to prefer a newer protocol while
        gracefully falling back to an older one on legacy browsers:
      
      
        
    [Example 4](https://w3c-fedid.github.io/digital-credentials/#example-preferring-a-newer-protocol-with-fallback-to-an-older-one): Preferring a newer protocol with fallback to an older one
   ```
// Ordered by preference; on browsers that implement DigitalCredential,
// unknown protocols return false rather than throwing.
const protocol = [
  "example-new-protocol",
  "example-legacy-protocol",
].find(DigitalCredential.userAgentAllowsProtocol);

if (protocol) {
  // Use the best protocol this browser supports.
} else {
  // No supported protocol found. Fall back to another approach.
}
```
      
### 2.3 Requesting a digital credential
      
        The following example shows how to request a digital credential using
        the [API](https://w3c-fedid.github.io/digital-credentials/#DC-API). The entry point for the API is the
        `navigator.credentials.`[get](https://www.w3.org/TR/credential-management-1/#dom-credentialscontainer-get)`()` method, which is
        used to request a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) from the user agent. If the
        user agent supports [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request), it allows the user to select a digital
        credential through a [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser):
      
      
        
    [Example 5](https://w3c-fedid.github.io/digital-credentials/#example-requesting-a-digital-credential): Requesting a digital credential
   ```
<button>Verify Identity</button>
<script>
  const button = document.querySelector("button");
  button.addEventListener("click", async () => {
    const protocol = "example-request-protocol";
    // Check for DC API and protocol support
    if (!DigitalCredential.userAgentAllowsProtocol(protocol)) {
      // The browser doesn't allow the use of this protocol.
      // Fall back to a different verification method.
      showTraditionalVerificationForm();
      return;
    }
    try {
      const credential = await navigator.credentials.get({
        digital: {
          requests: [{
            protocol,
            data: { /* presentation request data */ }
          }]
        }
      });

      // Post it back to the verifier server for decryption and verification
      const response = await fetch("/verify-credential", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(credential)
      });

      // Check response
      if (!response.ok) {
        throw new Error("Failed to verify credential");
      }

      // Render the verification result
      displayVerificationResult(await response.json());

    } catch (error) {
      console.error("Error requesting digital credential:", error);
    }
  });
</script>
```
      
      
        Similarly, when a site needs to [issue](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) a
        digital credential, the [Digital Credentials API](https://w3c-fedid.github.io/digital-credentials/#DC-API) mediates
        the issuance of a digital credential between the site, the user agent,
        and the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
      
### 2.4 Issuing a digital credential
      
        The following example shows how to request the issuance of a digital
        credential using the [Digital Credentials API](https://w3c-fedid.github.io/digital-credentials/#DC-API). To issue a
        digital credential, a site calls the
        `navigator.credentials.`[create](https://www.w3.org/TR/credential-management-1/#dom-credentialscontainer-create)`()` method,
        which, if the user agent supports issuance, would initiate the issuance
        flow:
      
      
        
    [Example 6](https://w3c-fedid.github.io/digital-credentials/#example-requesting-issuance-of-a-digital-credential): Requesting issuance of a digital credential
   ```
<button>Request Digital Credential Issuance</button>
<script>
  const button = document.querySelector("button");
  button.addEventListener("click", async () => {
    const protocol = "example-issuance-protocol";
    // Check for DC API and protocol support
    if (!DigitalCredential.userAgentAllowsProtocol(protocol)) {
      // The browser doesn't allow the use of this protocol.
      // Fall back to a different issuance method.
      showTraditionalIssuanceForm();
      return;
    }
    try {
      const credential = await navigator.credentials.create({
        digital: {
          requests: [{
            protocol,
            data: { /* issuance request data */ }
          }]
        }
      });
    } catch (error) {
      console.error("Error issuing digital credential:", error);
    }
  });
</script>
```
      
### 2.5 Requesting a digital credential across origins
      
        The specification allows usage of the API for presenting credentials
        from a remote/third-party origin via the
        ["digital-credentials-get"](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credentials-get) [policy-controlled feature](https://www.w3.org/TR/permissions-policy-1/#policy-controlled-feature). This is
        useful for scenarios where a website wants to request digital
        credentials from a verification service that is hosted on a different
        origin. The Permissions Policy can be set on an iframe that embeds the
        website that wants to use the API. Here is an example of how the
        Permissions Policy can be set on an iframe:
      
      
        
    [Example 7](https://w3c-fedid.github.io/digital-credentials/#example-requesting-a-digital-credential-across-origins): Requesting a digital credential across origins
   ```
<iframe src="https://verifier-service.example.com"
        allow="digital-credentials-get">
</iframe>
```
      
### 2.6 Issuing a digital credential across origins
      
        Similarly, the specification allows usage of the API for issuing
        credentials from a remote/third-party origin via the
        ["digital-credentials-create"](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credentials-create) [policy-controlled feature](https://www.w3.org/TR/permissions-policy-1/#policy-controlled-feature). This
        is useful for scenarios where a website wants to request issuance of a
        digital credential using an issuance service on a different origin. The
        Permissions Policy can be set on an iframe embedding the [issuer's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers)
        interface. Here is an example:
      
      
        
    [Example 8](https://w3c-fedid.github.io/digital-credentials/#example-issuing-a-digital-credential-across-origins): Issuing a digital credential across origins
   ```
<iframe src="https://issuer.example.com"
        allow="digital-credentials-create">
</iframe>
```

---

## 3. Scope*This section is non-normative.*
    
      The following items are within the scope of this specification:
    
    
      - [Presentation requests](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) including
      mechanisms for [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) of
      [digital credentials](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
      
      - [Issuance requests](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) for [digital credentials](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential).
      
      - Mechanisms ensuring that, when an API call is made, the website does
      not learn anything about the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) nor any [digital credentials](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential)
      they hold, without explicit user consent.
      
      - Ensuring that any installed application software will not learn
      anything about a given [issuance request](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) or
      [presentation request](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) unless the [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders)
      explicitly consents to use that software.
      
    
    
      The following items are out of scope:
    
    
      - UI/UX considerations, except for accessibility and privacy aspects,
      which are addressed to ensure access to and protection of user data
      during [presentation](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) and [issuance](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) processes.
      
      - Functionality outside the [user agent](https://infra.spec.whatwg.org/#user-agent) is out of scope, including
      platform-specific frameworks, native operating system APIs, standalone
      applications, and hardware components that store, manage, or process
      [digital credentials](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential). This includes the user interface and user
      interactions for selecting a specific credential and obtaining the user's
      permission to forward a request to the user-selected [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager).
      
      - Implementation of [credential managers](https://www.w3.org/TR/credential-management-1/#credential-manager), specifically in the role
      of [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) software (commonly known as "digital wallets"), including
      how they securely store or manage [digital credentials](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) or advertise
      capabilities to [present](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) or [issue](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) them to the [user agent](https://infra.spec.whatwg.org/#user-agent), is out of scope.
      The only exception is the transmission of [issuance request data](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request-data) and [presentation request data](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request-data) to
      and from such software.

---

## 4. Terminology
    Note: Definitions under discussion
      The goal of the definitions in this section is to reuse or establish
      terminology that is common across a variety of digital credential formats
      and protocols. These definitions are actively evolving.
    
    
        Credential request
      
      
        A [presentation request](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) or an [issuance request](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request).
      
      
        Credential response
      
      
        A [presentation response](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-response) or an [issuance response](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-response).
      
      
        Digital credential
      
      
        A cryptographically signed digital document containing one or more
        [claims](https://www.w3.org/TR/vc-data-model-2.0/#dfn-claims) made by an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) about one or more [subjects](https://www.w3.org/TR/vc-data-model-2.0/#dfn-subjects).
        Note: Focus on digital credentials about people
          This specification is currently focused on digital credentials
          pertaining to people.
        
      
      
        Digital credential chooser
      
      
        A platform-provided user interface that presents one or more [credential requests](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request) to the user, allowing them to select a
        [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) or [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) that can fulfill the request, or
        cancel the operation.
        Note: Relationship to credential chooser
          The [digital credential chooser](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential-chooser) may be invoked as part of a
          broader [credential chooser](https://www.w3.org/TR/credential-management-1/#credential-chooser), or as a separate platform-provided
          user interface. The exact relationship is implementation-defined.
        
      
        Issuance protocol
      
      
        A standardized protocol used for communication between an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers)
        and a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) during the issuance of a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential). The
        issuance protocol is identified by a [protocol identifier](https://w3c-fedid.github.io/digital-credentials/#dfn-protocol-identifier). See [5. 
      Protocols](https://w3c-fedid.github.io/digital-credentials/#protocols).
      
      
        Issuance request
      
      
        An issuance request is a request to issue a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential)
        composed of some [issuance request data](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request-data) and an
        [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol).
      
      
        Issuance request data
      
      
        A data structure that an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers) or a [user agent](https://infra.spec.whatwg.org/#user-agent), via an
        [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol), to request the issuance of a
        [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) by an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers).
      
      
        Issuance response
      
      
        A format that [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) uses, via an [issuance protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-protocol), to respond to an [issuance request](https://w3c-fedid.github.io/digital-credentials/#dfn-issuance-request) by
        an [issuer](https://www.w3.org/TR/vc-data-model-2.0/#dfn-issuers).
      
      
        Presentation protocol
      
      
        A standardized protocol used for presenting a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential)
        between a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) and a [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier). A protocol is identified by a
        [protocol identifier](https://w3c-fedid.github.io/digital-credentials/#dfn-protocol-identifier). See [5. 
      Protocols](https://w3c-fedid.github.io/digital-credentials/#protocols).
      
      
        Presentation request
      
      
        A presentation request is a request for a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential)
        composed of [presentation request data](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request-data) and a
        [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol).
      
      
        Presentation request data
      
      
        A format that [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier) software or a [user agent](https://infra.spec.whatwg.org/#user-agent) uses, via an
        [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol), to request a [digital credential](https://w3c-fedid.github.io/digital-credentials/#dfn-digital-credential) from a [holder](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders).
      
      
        Presentation response
      
      
        A format that a [holder's](https://www.w3.org/TR/vc-data-model-2.0/#dfn-holders) [credential manager](https://www.w3.org/TR/credential-management-1/#credential-manager), such as a digital
        wallet, uses, via an [presentation protocol](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-protocol), to
        respond to a [presentation request](https://w3c-fedid.github.io/digital-credentials/#dfn-presentation-request) by a
        [verifier](https://www.w3.org/TR/vc-data-model-2.0/#dfn-verifier).
      
      
        Protocol identifier
      
      
        A [string](https://infra.spec.whatwg.org/#string) composed of one or more [ASCII lower alpha](https://infra.spec.whatwg.org/#ascii-lower-alpha) [code points](https://infra.spec.whatwg.org/#code-point), zero or more U+002D HYPHEN-MINUS [code points](https://infra.spec.whatwg.org/#code-point), and zero or
        more [ASCII digit](https://infra.spec.whatwg.org/#ascii-digit) [code points](https://infra.spec.whatwg.org/#code-point) (in any order). For example,
        "123a-protocol", "abc", or simply "a".
      
      
        Request coordinator
      
      
        See [credential request coordinator](https://w3c-fedid.github.io/digital-credentials/#dfn-credential-request-coordinator).
