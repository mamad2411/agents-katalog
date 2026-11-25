---
name: web-bot-auth
description: "Web Bot Auth: sign and verify bot and AI agent HTTP requests with RFC 9421 HTTP Message Signatures, following draft-ietf-webbotauth-00 (build posture), with upgrades from the draft-meunier individual drafts. Use when a crawler, AI agent or other automated client must prove its identity to websites, or when a website, CDN or reverse proxy must verify such requests: Signature, Signature-Input and the Signature-Agent header, tag=web-bot-auth, created, expires and keyid (JWK SHA-256 thumbprint), covered components such as @authority, the key directory at /.well-known/http-message-signatures-directory (application/http-message-signatures-directory+json, a JWKS), jwks_uri and cimd discovery types, key rotation, directory response signatures, verifier outcomes, replay and SSRF limits. Triggers: web bot auth, webbotauth, bot authentication, signed agents, verified bots, crawler identity, HTTP message signatures, RFC 9421, draft-ietf-webbotauth-httpsig-protocol, draft-meunier-webbotauth-httpsig-protocol."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.2"
  kind: standard
---

# Web Bot Auth

Web Bot Auth is the IETF Web Bot Auth (webbotauth) working group's protocol for automated HTTP clients to sign their requests with RFC 9421 HTTP Message Signatures, and for websites to verify them. The signer names an HTTPS URL in a `Signature-Agent` header where its public keys are published; the verifier resolves that URL and checks the signature. With this skill the agent implements the signer role, the verifier role, or a key directory.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites (§ numbers refer to `draft-ietf-webbotauth-httpsig-protocol-00` unless they say RFC 9421). When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Draft posture: **build**, pinned to `draft-ietf-webbotauth-httpsig-protocol-00` (1 September 2026), the working group draft that replaced `draft-meunier-webbotauth-httpsig-protocol-02` and absorbed the separate directory draft. RFC 9421 underneath is stable.

## Inputs (fill in, or ask before starting)

- Role: signer (Agent), verifier (Origin or a fronting proxy), directory operator, or several.
- Discovery type the signer publishes: `directory` (default, well-known URI on an origin), `jwks_uri` or `cimd` (§ 5.5).
- Algorithms: which RFC 9421 algorithms to sign with or accept, for example `ed25519` (RFC 9421 § 3.3, § 6.2.2).
- Target version: draft-ietf-webbotauth-00 (default, posture build: implement it). The draft-meunier individual drafts are legacy: read them and upgrade from them, never build new signers on them; verifiers may still accept the legacy bare-String `Signature-Agent` (§ 5.2.1). No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned draft in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the datatracker page of the working group draft for a newer revision or a replacement, check the webbotauth working group page for new documents, and update the pins.

## Invariants

1. **Signers cover `@authority` or `@target-uri`** and set `created`, `expires`, `keyid` and `tag="web-bot-auth"` (§ 5.2). `keyid` is the base64url JWK SHA-256 thumbprint of the key (§ 5.2). Expiry of no more than 24 hours is recommended (§ 5.2).
2. **Every signed request carries `Signature-Agent`** in dictionary form, with an `https` URI per signature label, and the signature covers its own member, for example `"signature-agent";key="sig1"` (§ 5.2.1, § 4.3).
3. **No shared secrets.** HMAC (`hmac-sha256`) must not be used; each client should use its own asymmetric key pair (§ 6.4).
4. **Verifiers follow RFC 9421 § 3.2** and fail verification on unknown or untrusted keys and on algorithms outside their allowed set (RFC 9421 § 3.2 steps 5 and 6).
5. **Key lookup is keyed on the (URL, key) pair**, never on `keyid` alone (§ 5.4).
6. **A `Signature-Agent` value is a claim until resolved.** Verifiers must not attach policy to it or attribute a request to it until they have fetched that URL, or hold proof per § 5.5.3, and found the key (§ 4.1, § 4.4).
7. **Discovery fetches must return 200 and must not follow redirects automatically** (§ 5.5). Directories are served over HTTPS; at the well-known URI with `application/http-message-signatures-directory+json` (§ 5.5.1).
8. **A failed fetch never evicts a cached directory**; a successful fetch that lacks the key does (§ 6.10).
9. **A valid signature identifies the signer, nothing more.** It does not authenticate a human user, and does not express authorization, delegation or consent (§ 4.1, § 4.6, § 5.2.2).

## Workflow

1. **Pick the version.** Use draft-ietf-webbotauth-00. If an existing signer or verifier cites a `draft-meunier-*` draft, sends a bare-String or `data:` `Signature-Agent`, or looks keys up by `keyid` alone, plan the upgrade (step 7).
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded as `draft-ietf-webbotauth-httpsig-protocol-00`.
2. **Signer: generate and publish keys.** Create an asymmetric key pair per agent, publish the public key as a JWKS at the chosen discovery URL, and plan rotation.
   -> [`references/signer-and-directory.md`](references/signer-and-directory.md)
   ✓ The directory answers 200 over HTTPS with a JWKS whose `kid` values, if present, equal the thumbprints (§ 5.5), and with the directory media type at the well-known URI.
3. **Signer: sign each request.** Build the covered components and parameters, compute the RFC 9421 signature base, sign, and send `Signature`, `Signature-Input` and `Signature-Agent`.
   -> [`references/signer-and-directory.md`](references/signer-and-directory.md), [`references/http-message-signatures.md`](references/http-message-signatures.md)
   ✓ The request verifies against the published key with the RFC 9421 algorithm, and the signature is generated per request with bounded `created` and `expires` (§ 6.9).
4. **Verifier: parse and select signatures.** Parse the three fields, select signatures with `tag="web-bot-auth"`, and check covered components and freshness.
   -> [`references/verifier.md`](references/verifier.md)
   ✓ Malformed fields get 400 or are ignored by policy (§ 5.4); signatures without the tag can be discarded.
5. **Verifier: resolve keys.** Resolve the `Signature-Agent` member covered by the signature with bounded, cached, SSRF-safe fetches.
   -> [`references/verifier.md`](references/verifier.md)
   ✓ Fetches have size, key count, timeout and address limits (§ 6.7); cache respects HTTP caching (Appendix C.4).
6. **Verifier: decide.** Verify, classify as verified, invalid or unverified, and apply local policy.
   -> [`references/verifier.md`](references/verifier.md)
   ✓ Unverified requests stay in the existing bot-management path and never become trusted (Appendix C.1, C.9).
7. **Upgrade** (only when asked). Follow the checklist from the individual drafts: dictionary `Signature-Agent` on every request with `https` values, typed discovery, (URL, key) lookup, no redirects.
   -> [`references/versions.md`](references/versions.md)
   ✓ Requests verify against the current draft's rules with the same keys and directory URL as before.

## Verify before done

- [ ] `Signature-Input` has `created`, `expires`, `keyid` and `tag="web-bot-auth"`, and covers `@authority` (or `@target-uri`) and the `signature-agent` member for its label.
- [ ] `keyid` equals the RFC 7638 thumbprint of the public key (RFC 8037 Appendix A.3 for Ed25519), computed, not chosen.
- [ ] `Signature-Agent` uses the dictionary form with an `https` URL; `directory` values are bare origins (§ 5.5).
- [ ] The verifier indexes keys by (URL, key) and attributes a request only to a URL it resolved.
- [ ] Discovery fetches reject non-200 responses, do not auto-follow redirects, and block private, loopback and link-local addresses.
- [ ] No HMAC keys, no test keys from RFC 9421 in production (§ 6.4, § 6.8), and no long-lived static signatures (§ 6.9).
- [ ] Requests over plain HTTP with `Signature` headers are refused or ignored (§ 6.1).

## Reference index

- **`references/versions.md`**: the working group draft and the individual drafts it replaced, what changed, and the upgrade checklist. Load for steps 1 and 7.
- **`references/http-message-signatures.md`**: RFC 9421 essentials: components, signature parameters, the signature base, the verification algorithm, algorithms, `Accept-Signature`, replay. Load for steps 3 to 6.
- **`references/signer-and-directory.md`**: the Web Bot Auth signing profile, `Signature-Agent`, multiple signatures, the directory format, discovery types, rotation and directory response signatures. Load for steps 2 and 3.
- **`references/verifier.md`**: the verification profile, key resolution, trust model, caching, SSRF limits, outcomes, proxies and privacy. Load for steps 4 to 6.

## Related skills

- `jwt` for JOSE key formats (JWK, JWKS, thumbprints) and token validation that often sits next to request signatures: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`.
- `owasp-agentic` for reviewing agent identity and privilege as a whole: `npx skills add ScaleDockHQ/scaledock-skills --skill owasp-agentic`.
- `http-message-signatures` for the full RFC 9421 signing and verification rules this profile builds on: `npx skills add ScaleDockHQ/scaledock-skills --skill http-message-signatures`.
- `aipref` for publishing and reading AI usage preferences with Content-Usage: `npx skills add ScaleDockHQ/scaledock-skills --skill aipref`.
- `robots-txt` for robots.txt rules that crawlers and AI agents follow: `npx skills add ScaleDockHQ/scaledock-skills --skill robots-txt`.
- `privacy-pass`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill privacy-pass`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9421: HTTP Message Signatures](https://www.rfc-editor.org/rfc/rfc9421): RFC (Standards Track), RFC 9421 (February 2024), checked 2026-10-02.
- [draft-ietf-webbotauth-httpsig-protocol-00: HTTP Message Signatures for automated traffic](https://www.ietf.org/archive/id/draft-ietf-webbotauth-httpsig-protocol-00.txt): WG draft (IETF webbotauth WG), revision -00 (1 September 2026), checked 2026-10-05. Draft posture: build.
- [draft-ietf-webbotauth-httpsig-protocol datatracker page](https://datatracker.ietf.org/doc/draft-ietf-webbotauth-httpsig-protocol/): WG Document, latest revision -00, checked 2026-10-05.
- [draft-meunier-webbotauth-httpsig-protocol](https://datatracker.ietf.org/doc/draft-meunier-webbotauth-httpsig-protocol/): Replaced individual draft (replaced by the WG draft), last revision -02 (2026-08-18), checked 2026-10-05. Draft posture: track.
- [draft-meunier-http-message-signatures-directory](https://datatracker.ietf.org/doc/draft-meunier-http-message-signatures-directory/): Replaced individual draft (merged into the protocol draft), last revision -05 (2026-03-02), checked 2026-10-05. Draft posture: track.
- [draft-meunier-webbotauth-httpsig-protocol-02](https://www.ietf.org/archive/id/draft-meunier-webbotauth-httpsig-protocol-02.txt): Replaced individual draft, -02 (2026-08-18), checked 2026-10-05.
- [draft-meunier-web-bot-auth-architecture-05](https://www.ietf.org/archive/id/draft-meunier-web-bot-auth-architecture-05.txt): Replaced individual draft (renamed to draft-meunier-webbotauth-httpsig-protocol), -05 (2026-03-02), checked 2026-10-05.
- [draft-meunier-http-message-signatures-directory-05](https://www.ietf.org/archive/id/draft-meunier-http-message-signatures-directory-05.txt): Replaced individual draft, -05 (2026-03-02), checked 2026-10-05.
- [Web Bot Auth (webbotauth) working group charter](https://datatracker.ietf.org/wg/webbotauth/about/): Active IETF working group, charter as published, checked 2026-10-02.
- [RFC 7638: JSON Web Key (JWK) Thumbprint](https://www.rfc-editor.org/rfc/rfc7638): RFC (Standards Track), RFC 7638 (September 2015), checked 2026-10-02.
- [RFC 8037: CFRG ECDH and Signatures in JOSE](https://www.rfc-editor.org/rfc/rfc8037): RFC (Standards Track), RFC 8037 (January 2017), checked 2026-10-02.
