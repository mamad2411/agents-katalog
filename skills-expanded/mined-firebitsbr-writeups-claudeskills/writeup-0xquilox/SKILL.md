<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-0xquilox
description: CTF writeups and security challenges by 0xQuilox.
---

# Writeups by 0xQuilox

Source repository: `/repos/0xQuilox`

## Repository Index

- soft-verified/README.md
- soft-verified/Reference Proof-of-Concept (Off-Platform)/README.md
- soft-verified/exploit-server/README.md
- soft-verified/Reference Proof-of-Concept (Off-Platform)/src/README.md

## Writeup Content


### File: soft-verified/README.md

# Verified Wallet Bug Bounty
A bug bounty report for the Verified Wallet Network browser extension.

---

## 1. Verified Wallet Browser Extension – Security Vulnerability Report

### Summary

The **Verified Wallet** browser extension exposes a critical client-side attack surface due to **unrestricted message handling and insecure storage practices**.
Any arbitrary website can interact with the extension via `postMessage`, trigger privileged wallet methods, and read sensitive wallet metadata stored in web-accessible `localStorage`.

These issues **break core browser extension trust boundaries** and enable cross-site wallet interaction without origin validation.

---

## Affected Component

* **Product**: Verified Wallet Chrome Extension
* **Version**: 1.1.1
* **Manifest**: v3
* **Files**:

  * `scripts/injected.js`
  * `scripts/content.js`
  * `scripts/background.js`

---

### Vulnerability 1: Unrestricted `postMessage` Acceptance

**Severity: HIGH**

### Description

The extension accepts `postMessage` events with `type: "VW_REQ"` from **any webpage origin**.
Messages are sent using:

```js
window.postMessage(message, "*")
```

and no origin validation is enforced when processing incoming requests.

This allows **any website** to invoke wallet methods such as:

* `eth_requestAccounts`
* `eth_sendTransaction`
* recovery-related methods

### Impact

* Malicious websites can interact with wallet functionality
* No per-origin permission or trust enforcement
* Violates Chrome extension security model

### Proof of Concept

```js
window.postMessage({
  type: "VW_REQ",
  id: "exploit-1",
  params: {
    method: "eth_requestAccounts",
    params: []
  }
}, "*");
```

**Observed behavior**:
The extension processes the request and responds, confirming acceptance from an arbitrary origin.

### Security Impact

* Cross-site wallet interaction
* Phishing / transaction spoofing vectors
* Wallet logic abuse

---

### Vulnerability 2: Request / Response Confusion

**Severity: MEDIUM**

### Description

The extension does not strictly distinguish between request (`VW_REQ`) and response (`VW_RES`) message flows.
In testing, messages sent as requests were echoed or mishandled as responses.

### Impact

* Message flow desynchronization
* Potential replay or state confusion
* Weak message lifecycle enforcement

### Evidence

Captured message:

```json
{
  "type": "VW_REQ",
  "id": "exploit-2",
  "params": {
    "method": "eth_sendTransaction",
    "params": [{ "to": "...", "value": "0x1" }]
  }
}
```

Returned directly without strict response validation.

---

## Vulnerability 3: Wallet Metadata Stored in Web-Accessible `localStorage`

**Severity: HIGH**

### Description

The injected script stores wallet-related data in `localStorage` under the key `myVault`.

```js
localStorage.setItem("myVault", JSON.stringify(vaultData));
```

Because this runs in the **page context**, any JavaScript on the website can read this data.

### Impact

* Wallet metadata leakage
* Persistent exposure across sessions
* Readable by XSS or malicious scripts

### Proof of Concept

```js
console.log(localStorage.getItem("myVault"));
```

**Observed data includes**:

* Wallet address
* Chain ID
* Registration metadata

---

### Vulnerability 4: No Origin-Based Permission Model

**Severity: MEDIUM**

### Description

The extension does not associate wallet permissions with specific website origins.
Once installed, **all websites share the same trust level**.

### Impact

* No domain isolation
* No user-consent enforcement per site
* Enables cross-site wallet abuse

---

### Root Cause Analysis

| Issue             | Root Cause                                        |
| ----------------- | ------------------------------------------------- |
| Message injection | `postMessage("*")` with no origin checks          |
| Storage exposure  | Using `localStorage` instead of extension storage |
| Trust confusion   | Missing message schema & lifecycle validation     |
| Permission abuse  | No origin-scoped authorization                    |

---

### Recommended Remediations

#### 1. Enforce Origin Validation

```js
if (event.origin !== EXPECTED_ORIGIN) return;
```

#### 2. Move Wallet State Out of Page Context

* Use `chrome.storage.local`
* Never store wallet data in page `localStorage`

#### 3. Enforce Strict Message Schema

* Validate `type`, `method`, `params`
* Reject unknown or malformed messages

#### 4. Implement Per-Origin Permissions

* Explicit user approval per website
* Maintain origin allowlist

---

### CVSS (Estimated)

**Score**: 8.2 (High)

| Metric              | Value    |
| ------------------- | -------- |
| Attack Vector       | Network  |
| Attack Complexity   | Low      |
| Privileges Required | None     |
| User Interaction    | Required |
| Scope               | Changed  |
| Confidentiality     | High     |
| Integrity           | High     |

---

### Attachments

* ✔ Reproducible HTML PoC
* ✔ Console logs
* ✔ Architecture analysis
* ✔ Message traces


## 2. Vulnerability Title

**Client-Side Exposure of Privileged Backend Configuration in Verified Wallet Exteension

### Summary

The Verified Wallet browser extension bundles multiple **privileged backend configuration values** directly into client-side JavaScript, including:

* Azure Function endpoints
* Azure Function access key
* Firebase project identifiers
* WalletConnect project identifier
* Internal service URLs

While backend services correctly enforce authentication, origin checks, and access control, exposing these values in a browser extension increases the application’s attack surface and violates the principle of least privilege.

---

### Affected Assets

#### Exposed in Extension Bundle

* Azure Function endpoints:

  * `/api/smssender`
  * `/api/emailsender`
  * `/api/otpsender`
  * `/api/user`, `/api/wallet`, `/api/transaction`, etc.
* Azure Function key (`x-functions-key`)
* Firebase configuration (project ID, API key, VAPID key)
* WalletConnect project ID

All values are accessible via:

* Browser DevTools
* Static bundle inspection
* Any webpage interacting with the extension

---

### Proof of Exposure

Using a standalone HTML page and browser DevTools, the following were confirmed:

* Constants are embedded in compiled JavaScript
* Identifiers and service endpoints are readable without authentication
* Requests can be constructed directly using exposed values

---

### Security Controls Observed (Positive Findings)

Backend services correctly enforce:

* CORS origin validation

  ```
  400 The origin 'null' is not allowed
  ```
* Firebase access rules (`403`, `OPERATION_NOT_ALLOWED`)
* No unauthenticated data access observed

This confirms that **no immediate remote exploitation is possible** using browser-originated requests.

---

### Security Impact

Although no direct abuse was observed during testing, client-side exposure enables:

* Infrastructure enumeration
* Targeted backend probing from non-browser contexts
* Easier exploitation if server-side controls regress
* Increased risk during future feature changes or misconfigurations
* Leakage of internal architecture details to attackers

Browser extensions should be treated as **fully hostile clients**.

---

### Recommended Remediation

1. **Remove privileged secrets from client bundles**

   * Azure Function keys must never be shipped client-side
2. **Move privileged calls behind authenticated backend services**
3. **Use per-session, scoped tokens if client access is unavoidable**
4. **Audit build pipeline to prevent secret leakage**
5. **Rotate exposed keys as a precaution**

---

## 🧾 Severity Assessment

| Component                       | Severity      |
| ------------------------------- | ------------- |
| Azure Function key exposure     | **Medium**    |
| Internal API endpoints exposure | Medium        |
| Firebase config                 | Informational |
| WalletConnect project ID        | Informational |

---
Just tell me 👍




### File: soft-verified/Reference Proof-of-Concept (Off-Platform)/README.md





### File: soft-verified/Reference Proof-of-Concept (Off-Platform)/src/README.md





### File: soft-verified/exploit-server/README.md

### This is a local node server that can be run as a malicious website to trigger walllet connection and drainage
### Note
Run the two files as a basic frontend server in a folder using "node serve_poc.js"

