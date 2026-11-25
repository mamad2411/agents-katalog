---
name: phishing-email-analysis
description: Guides triaging a reported phish (.eml/.msg) by reading the Received chain and Authentication-Results (SPF/DKIM/DMARC/ARC/compauth), spotting Reply-To/Return-Path mismatches, extracting and safely handling URLs and attachments, recognizing AiTM/device-code/consent phishing kits, and scoping who else got or clicked it. Use when the user shares a suspicious email or headers, asks whether a message is phishing, or needs to analyze a reported phish.
license: Apache-2.0
metadata:
  verified: "2026-11-17"
---

# Phishing email analysis

Goal: a verdict (malicious, spam, benign, or simulation) plus **scope** (who received
it, who clicked, whether creds were entered), fast. Credentials entered or a payment
reply means an incident, so go to `load_skill bec-email-investigation`. The
reporter/culture side is `load_skill social-engineering-defense`.

## Intake: the original, not a forward

- An inline forward strips the headers. Get the message **as an attachment**:
  - `.eml` from Gmail "Download message" or OWA/new Outlook "Download"
  - `.msg` from classic Outlook
  - the admin copy (Defender submissions/Threat Explorer, Workspace security
    investigation tool)
- `.msg` is an OLE file with no parser in the image. Convert it off-box
  (`extract-msg`, `msgconvert`) or ask for `.eml`.
- Stage it under `/work` and record its **sha256** first (`sha256sum` in
  your own shell). Work on a copy.
- **Handling rules**: never open it in a mail client, because remote images beacon.
  Never click. Defang what you write (`hxxps://evil[.]tld`). **Never submit a URL or
  file to a public scanner or sandbox without authorization.** urlscan submissions
  default to public, so search first (`load_skill security-apis`).

## Headers: bottom-up, trust only your own stamps

`read_file` the `.eml`. The headers are plain text above the first blank line.

- **Received chain**: only hops added by **your** MTA/SEG are trustworthy, and anything
  below your boundary can be forged. At the boundary hop, take the connecting **IP +
  HELO** and run `whois_lookup`, `asnmap`, `shodan_host`. A VPS or residential IP for
  a "bank" is suspicious. Large timestamp gaps suggest queued or replayed mail.
- **Authentication-Results** (RFC 8601): trust only the header with your receiver's
  authserv-id. Attackers plant fake `pass` headers lower down. Read `spf=
smtp.mailfrom=`, `dkim= header.d=` and `dmarc= header.from=`. On M365 also check:
  - `compauth=` with its `reason=` (Microsoft's composite verdict)
  - `X-MS-Exchange-Organization-AuthAs` (Anonymous vs Internal)
  - `X-Forefront-Antispam-Report` (`SCL`, `SFV`, `CAT:PHSH/SPOOF/BULK`)
- **ARC** (`ARC-Seal cv=`, `ARC-Authentication-Results i=n`) explains DKIM broken by a
  list or forwarder. It counts only if you trust the sealer, because anyone can add ARC headers.
- **Traps**:
  - `dmarc=pass` is not legitimacy. Attacker-owned lookalikes authenticate perfectly.
  - A compromised vendor mailbox passes everything.
  - Abused platforms pass as themselves: e-sign/invoice services, SharePoint/OneDrive
    shares, Google Forms, ESPs.
  - `dmarc=fail action=none` means the sender's `p=none` let a spoof in. Tell them
    (`load_skill email-security`).
- **Mismatches**:
  - display name vs address
  - **Reply-To ≠ From**, often to free webmail (the BEC reply hijack)
  - Return-Path domain unrelated to From
  - Message-ID domain inconsistent with the sending platform
  - cousin or homoglyph domains (`rn`/`m`, punycode `xn--`)

  Run `whois_lookup` on the From and Reply-To domains, since a domain days old is a
  strong signal. Check `ct_search` (crt.sh) for certificates issued just before the
  send, `dnstwist` for registered lookalike or cousin domains of the impersonated
  brand (background job), and `dns_lookup` MX to see whether the domain can even
  receive replies. `ioc_lookup` enriches the domains and IPs from URLs and the
  hashes of attachments.

## URLs: find the real destination

- Compare each `href` with its link text. Unwrap rewriters (Safe Links `?url=`,
  `urldefense.com/v3/__...__`, Mimecast). The wrapper is not the IOC.
- Walk redirect chains **passively** first, using urlscan search and
  `load_skill indicator-enrichment`. Expect open redirects on trusted domains,
  shorteners, and **CAPTCHA/Turnstile gates** that hide the kit from scanners. Only
  detonate with authorization, in an isolated browser or sandbox.
- Strip the victim's **base64 email from the path or `#fragment`** before any lookup.
  It personalizes the kit and leaks who was targeted.
- **QR codes** in images or PDFs evade text-link scanners, so decode them offline.
  **SVG/HTML attachments** can carry JS, HTML smuggling, or a local fake login page,
  so treat them as code. SVGs were 65% of CAPTCHA-gated phishing in Aug 2026 and the leading delivery method at the end of Q3.
  verify: https://www.microsoft.com/en-us/security/blog/2026/11/05/email-threat-landscape-q3-2026-trends-and-insights/

## Which credential-theft pattern?

- **AiTM reverse proxy** (Evilginx-class, Tycoon2FA, EvilProxy, Sneaky2FA and
  successors): it proxies the real IdP, so the page shows **your real tenant branding**
  and steals the session cookie, beating non-phishing-resistant MFA. Tells: a fresh
  domain or certificate, IdP paths on a foreign host, anti-bot JS, and a bounce to a
  benign site when it detects a sandbox. Tycoon2FA was disrupted in Mar 2026, but kits
  rebrand, so pivot on infrastructure, not the kit name.
  verify: https://www.microsoft.com/en-us/security/blog/2026/03/04/inside-tycoon2fa-how-a-leading-aitm-phishing-kit-operated-at-scale/
- **Device-code phishing**: there is no fake page. The lure (often a QR code or a
  meeting/Teams pretext) has the victim enter a code at the real
  `microsoft.com/devicelogin`. The IOC is in the sign-in logs (protocol `deviceCode`).
- **OAuth consent phishing**: a real `login.microsoftonline.com/.../authorize` or Google
  OAuth link carrying an attacker `client_id`. The IOC is the **app ID, publisher and
  scopes** (`Mail.Read`, `offline_access`), not the domain.
- **ClickFix / fake CAPTCHA**: the page tells the user to paste a command into Run or
  a terminal. That is malware, so go to EDR and `load_skill incident-response`.

## Attachments

- Decode the MIME parts and hash each one. With raw shell: `python3 -I -c` plus the
  stdlib `email` module. Watch for nested `.eml` and archives. Check CIRCL hashlookup
  first (`ioc_lookup` on the hash), since a known-good hit clears the file.
- Route by type:
  - Office → `olevba` from oletools (`load_skill malware-maldoc`)
  - PDFs, images, Office docs → `exif_metadata` (author, creating tool, internal paths;
    lure templates repeat)
  - executables and scripts → `load_skill malware-triage` (capa, rabin2, YARA, in your own sandbox)
  - LNK/ISO/OneNote → `malware-maldoc`

## Scope and close

- **Who else got it?** Search by sender, subject, URL domain and hash: M365 Threat
  Explorer, `EmailEvents`, message trace; Workspace investigation tool (Gmail log
  events). Purge from every mailbox once a copy is saved.
- **Who clicked or entered creds?** Proxy/DNS logs for the kit domain, `UrlClickEvents`,
  and sign-ins from new IPs/ASNs just after the click. Any hit means reset plus revoke
  sessions, then `load_skill bec-email-investigation`.
- Block the sender, domains, URLs and hashes. Pivot to sibling infrastructure
  (`load_skill ioc-pivoting`). Tell the reporter the outcome.
- `write_file` a triage table (IOC, type, source, verdict, confidence).
  `report_finding` confirmed-malicious items with defanged evidence and the proving
  header excerpt.
