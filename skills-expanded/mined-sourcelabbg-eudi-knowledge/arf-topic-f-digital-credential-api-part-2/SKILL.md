---
name: "arf-topic-f-digital-credential-api-part-2"
description: "Use when integrating EUDI Wallet with the W3C Digital Credentials API. Covers browser integration, DC API flow, CTAP-Hybrid, and security considerations. Part 2: covers 6 Frequently Asked Questions about the Digital Credentials API, 7 References."
sections:
  - "6 Frequently Asked Questions about the Digital Credentials API"
  - "A. What is the W3C Digital Credentials API?"
  - "B. What problem does it solve?"
  - "C. Is it a W3C Standard yet?"
  - "D. What about OpenID for Verifiable Presentations (OpenID4VP)?"
  - "E. Does it lock you into one protocol or format?"
  - "F. How is privacy handled?"
  - "G. Who are the main actors?"
  - "H. Does it also support issuing attestations and PID, not just presenting them?"
  - "I. What's the browser support today for Presentation?"
  - "J. What's the browser support today for Issuance?"
  - "K. Is it relevant for the EUDI Wallet ecosystem?"
  - "L. How does the API support cross-device (phone-to-desktop) flows, and where does CTAP 2.0/2.2 fit?"
  - "M. Can the company running the CTAP tunnel read my data?"
  - "N. What's the basic difference between using a DC API or custom scheme?"
  - "O. Wallet discovery and invocation, who's in control?"
  - "Q. Privacy implications?"
  - "R. Cross-device flows (phone <-> desktop)?"
  - "S. Maturity and portability?"
  - "T. If I must use custom schemes, what are the minimum mitigations?"
  - "Bottom line"
  - "7 References"
---

<!-- ARF version: v3.0.0 -->
<!-- Tokens: ~2615 -->

## 6 Frequently Asked Questions about the Digital Credentials API

This FAQ explains the W3C Digital Credentials API (DC API) in plain terms—what
it is, why it matters, and how it fits alongside existing open protocols and
profiles (e.g., OpenID4VP, ISO 18013-7, ETSI). It is written for policy,
product, and engineering audiences and aims to be neutral: it does not endorse
any vendor, protocol, or format.

### A. What is the W3C Digital Credentials API?

It's a Web API that lets wallets present and relying parties request and
(optionally) issue digital credentials (e.g., ID cards, driving licenses,
diplomas) via the browser (user agent). It's protocol- and format-agnostic and
builds on Credential Management Level 1.

### B. What problem does it solve?

It replaces ad-hoc deep links and custom schemes with a standard,
browser-mediated flow so sites can request credentials, users can choose a
wallet and consent, and results return in the same tab-consistently and with
stronger privacy.

- **Safer invocation**: The browser only opens a wallet after explicit user
confirmation, using clear context about who is asking and what is requested.
- **Phishing resistance**: The wallet receives the authenticated website origin
from the user agent, making origin spoofing harder.
- **Better UX**: The user never "falls out" into opaque app hops; the session
returns to the original tab whether fulfilled or aborted.
- **Cross-device hardening**: When a phone and desktop are involved, the OS can
enforce proximity-checked secure transport (e.g., CTAP 2.2 hybrid) under the
hood.
- **Lower integration drift**: A single web surface for sites and wallets
reduces bespoke glue code and privacy pitfalls of raw URL schemes.

### C. Is it a W3C Standard yet?

It's a **W3C Working Draft** (latest from 11 Oct 2025) on the Recommendation
track, work-in-progress and evolving.

### D. What about OpenID for Verifiable Presentations (OpenID4VP)?

They're complementary. **OpenID4VP** defines a protocol; the **Digital
Credentials API** can carry OpenID4VP messages instead of traditional HTTPS
redirects.

### E. Does it lock you into one protocol or format?

No. The spec is **protocol- and format-agnostic** and maintains a registry of
protocols so multiple ecosystems (e.g., ISO mDL flows, OpenID4VP, etc.) can work
through one browser interface.

### F. How is privacy handled?

The browser intermediates requests (e.g., a credential chooser), requires
readable requests (so it can protect users), and **mandates features like
response encryption**. The specification discusses **selective disclosure,
unlinkability, and verifier authorisation** considerations.

### G. Who are the main actors?

Same as EUDI ecosystem: **Attestation Provider -> EUDI Wallet -> Relying Party**.
The **user agent mediates** between the site (relying party/attestation
provider) and the wallet, enforcing UI/permission and transport requirements.

### H. Does it also support issuing attestations and PID, not just presenting them?

Yes. The API includes flows to request issuance, including cross-origin issuance
via Permissions Policy (digital-credentials-create).

### I. What's the browser support today for Presentation?

| | Chrome | Safari/Webkit | Edge | Firefox |
| --- | --- | --- | --- | ---|
| *Android* | Supported | - | Work in progress | - |
| *iOS* / *iPadOS* | Supported | Supported | Supported | Supported |
| *Windows* | Supported | - | - | -|
| *MacOS* | Supported | - | Supported | - |
| *Ubuntu* | Supported | - | - | - |

*Table for support on **Presentation** (expected rapid changes, as the draft evolves)*

### J. What's the browser support today for Issuance?

| | Chrome | Safari/Webkit | Edge | Firefox |
| --- | --- | --- | --- | ---|
| *Android* | Work in progress | - | Work in progress | - |
| *iOS* / *iPadOS* | - |- |- | - |
| *Windows* | Work in progress | - | - | -|
| *MacOS* | Work in progress | - | Work in progress | - |
| *Ubuntu* | Work in progress | - | - | - |

*Table for support on **Issuance** (expected rapid changes, as draft evolves)*

### K. Is it relevant for the EUDI Wallet ecosystem?

Yes, **some EUDI discussions profile the Digital Credentials API** alongside
OpenID4VP and ISO 18013-7 remote flows, treating it as a secure
transport/mediation layer (with strong verifier authentication expectations).

### L. How does the API support cross-device (phone-to-desktop) flows, and where does CTAP 2.0/2.2 fit?

In a cross-device flow, the desktop site invokes the Digital Credentials API and
shows a QR code. You scan it with your phone (where your wallet lives). The
browser/OS establishes a secure, phishing-resistant channel between desktop and
phone with a **proximity check**, on Chrome this uses the **FIDO CTAP protocol**
(Bluetooth for proximity), then the wallet asks for consent and returns an
**encrypted** credential response back to the site. CTAP's role here is the
**device-to-device pairing and proximity assurance**; it **does not carry your
personal data**, the credential payload itself travels via the chosen
presentation protocol (e.g., OpenID4VP/JWE or ISO 18013-7/HPKE). Apple documents
a similar cross-platform model and explicitly references **FIDO CTAP** for these
flows. The W3C spec stays **protocol-agnostic** and notes that the details of
cross-device transports are handled by platform implementations and underlying
*cross-device* protocols.

### M. Can the company running the CTAP tunnel read my data?

No, the CTAP hybrid (caBLE) tunnel is end-to-end encrypted between your
desktop/browser ("client platform") and your phone's authenticator/wallet. After
the WebSocket is established ```(wss://.../cable/connect/<routing-id>/<tunnel-id>```
or ```/cable/contact/<contact-id>)```, the two devices perform a Noise-based
cryptographic handshake (KNpsk0/NKpsk0 with P-256, SHA-256, AES-GCM) and then
exchange only encrypted CTAP frames. The tunnel service routes packets but
cannot decrypt CTAP contents.

Separately, in DC API deployments the credential response itself is additionally
encrypted end-to-end for the requesting website (e.g., JWE/HPKE in OpenID4VP or
ISO mDL profiles). That means neither the tunnel operator nor the browser can
read the returned attributes, only the verifier's backend holding the private
key can.

What the tunnel can still see is limited metadata (it terminates wss, knows the
tunnel/contact ID it's routing, and can observe timing/size), but not the CTAP
payload or your credential data.

### N. What's the basic difference between using a DC API or custom scheme?

- **DC API**: A browser-mediated Web API for requesting/presenting/issuing
credentials. The user agent parses the request, the platform/ wallet shows
consent UI, and returns results back to the site. It's format/protocol-agnostic
and designed with privacy & security considerations.
- **Custom scheme**: The site launches a wallet app via a URI like
```mywallet://...``` (or QR). Data returns via another app launch/redirect. No
standardized mediation by the browser.

### O. Wallet discovery and invocation, who's in control?

- **DC API**: The browser and the operating system controls wallet
discovery/selection and applies permissions and origin checks, yielding more
consistent UX and policy enforcement.
- **Custom scheme**: Any app can register the same scheme, so links can be
hijacked/mis-routed unless you move to verified mechanisms (iOS Universal Links,
Android App Links).

#### P. Security risks to watch out for?

- **DC API**: Benefits from the browser's security model (same-origin,
permissions, dedicated privacy section in the spec). Cross-device transports can
add phishing-resistance (handled by the platform), while the response is
encrypted for the verifier.
- **Custom scheme**: Documented risks include scheme hijacking, confusing
redirects, and easier relay/phishing in cross-device QR flows if you don't add
proximity or strong channel binding. Industry guidance recommends using the
browser (external user agent) instead of app-to-app redirects where possible.

### Q. Privacy implications?

- **DC API**: The request must be readable by the browser (to protect the user),
and specs emphasize data minimization and consent UI; returned attributes are
end-to-end encrypted to the verifier.
- **Custom scheme**: Requests often travel in URIs; careless designs can leak
data via logs or be intercepted by the wrong app. (Use verified links and keep
PII out of URLs.)

### R. Cross-device flows (phone <-> desktop)?

- **DC API**: Platforms can provide proximity-bound, phishing-resistant
cross-device channels under the hood while keeping the same API surface for
sites.
- **Custom scheme**: Pure QR/app-link flows need extra controls (proximity
checks, anti-relay measures). Otherwise, they're easier to phish/relay.

### S. Maturity and portability?

- **DC API**: A W3C Working Draft, evolving and being trialled; goal is one
portable browser surface across wallets/protocols.
- **Custom scheme**: Works everywhere today but tends toward per-wallet glue
code and platform-specific hardening. See [OWASP Mobile Application
Security](https://mas.owasp.org/MASTG-KNOW-0079/?utm_source=chatgpt.com).

### T. If I must use custom schemes, what are the minimum mitigations?

Use Universal Links (iOS) / App Links (Android) with domain verification, keep
secrets out of URLs, and follow OAuth for Native Apps (RFC 8252): prefer the
system browser (external user agent) and apply Security Considerations included
in OpenID4VP or OID4VCI (e.g., FAPI2) depending on the scenario.

### Bottom line

Choose DC API when you want browser-level mediation, stronger default
privacy/security posture, and a unified UX. Choose custom schemes only as
fallback mechanism with verified links + strict hardening, otherwise you inherit
real risks (hijacking, leakage, and weaker cross-device protection).

## 7 References

| Reference | Description |
| --- | --- |
| [RiskRegister] | Annex 1 to the Commission Implementing Regulation laying down rules for the application of Regulation (EU) No 910/2014 of the European Parliament and of the Council as regards the certification of the European Digital Identity Wallets, European Commission, October 2024, draft |
| [ARF_DevPlan] | Architecture and Reference Framework Development plan 2025, European Commission, v1.0, final |
| [Cred_API] | Digital Credentials, Draft Community Group Report, 20 February 2025, available at [https://w3c-fedid.github.io/digital-credentials/](https://w3c-fedid.github.io/digital-credentials/)|
| [Cred_Man] | Credential Management Level 1, 13 August 2024, available at [https://www.w3.org/TR/credential-management-1/](https://www.w3.org/TR/credential-management-1/)|
| [Ctap] | Client to Authenticator Protocol (CTAP) Review Draft, March 21, 2023, available at [https://fidoalliance.org/specs/fido-v2.2-rd-20230321/fido-client-to-authenticator-protocol-v2.2-rd-20230321.html](https://fidoalliance.org/specs/fido-v2.2-rd-20230321/fido-client-to-authenticator-protocol-v2.2-rd-20230321.html)|
