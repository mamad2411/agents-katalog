---
name: proto-smtp
description: SMTP mail service and anti-spoofing review for scoped domains — banner and capability enumeration, open-relay detection, STARTTLS/DANE encryption audit, SPF/DKIM/DMARC validation, VRFY/EXPN user enumeration exposure, and MTA-STS/BIMI configuration review. No credential brute force, email spoofing test, phishing simulation, or bulk mail relay.
disable-model-invocation: true
risk: safe-active
allowed-modes: [auto, bug-bounty, red-team, ctf, blue-team, offensive, grey-hat, forensic, reverse-engineering, mobile-pentest]
authorization-required: yes
evidence-outputs: [command-log, redacted-evidence, finding-draft]
---

# SMTP assessment — safe mail service and anti-spoofing review

Use this skill to review authorized SMTP mail services for open-relay risk, STARTTLS encryption posture, user enumeration exposure (VRFY/EXPN), SPF/DKIM/DMARC anti-spoofing controls, and MTA-STS/DANE/BIMI configuration — without brute force, credential theft, email spoofing, phishing, or bulk mail relay. All checks are read-only banner, DNS, and connection-handshake review. Never send test messages to external recipients, attempt credential guessing, or inject SMTP headers.

## Required inputs

- Written scope naming authorized mail servers (MX hosts, SMTP submission hosts), ports (25 SMTP, 465 SMTPS, 587 submission), domains for SPF/DKIM/DMARC review, allowed check types (banner grab, STARTTLS check, VRFY/EXPN test, open-relay test), rate limits, and testing window.
- Explicit permission for VRFY/EXPN user enumeration attempt. Without this, only banner, STARTTLS, and open-relay checks are allowed.
- Explicit permission for open-relay test (a test SMTP transaction targeting a project-controlled external test address). This is required to confirm open relay — without it, only banner-based relay detection is possible.
- Valid authorization cache for each mail server and domain.
- List of prohibited recipient domains for open-relay testing. Only project-controlled or explicitly authorized test recipient addresses may be used.
- Separate disabled-default approval before any credential brute force, phishing simulation, email spoofing (sending with forged `MAIL FROM`), bulk mail, or SMTP header injection.

## Required gates

1. `pentest_agent_load_config` → `pentest_agent_validate_policy` before planning.
2. `pentest_agent_parse_scope` → `pentest_agent_validate_target` for each mail server and domain.
3. `pentest_agent_check_authorization` before any active SMTP connection.
4. `pentest_agent_build_command` for dry-run argv preview when catalog tools (nmap, swaks, dig, openssl) are used.
5. `pentest_agent_execute_tool` for all execution.
6. `pentest_agent_append_evidence` → `pentest_agent_record_finding` → report.

## Workflow

### Phase 1 — mail server discovery and service fingerprinting

1. Identify MX hosts for authorized domains:
   - DNS query: `dig +short <domain> MX` — returns the mail exchanger hostnames and priorities.
   - Record all MX hosts, priorities, and resolved IPs.
2. Port scan authorized mail servers:
   - `nmap -p 25,465,587 --open <mail-server-ip>` through `pentest_agent_execute_tool`.
3. SMTP banner and capability enumeration:
   - `nmap -sV -p 25 --script smtp-commands <mail-server>` — reports SMTP banner (mail server software, version, hostname) and supported commands.
   - Or manual: `nc <mail-server> 25` and send `EHLO test.local`. Parse the response for supported extensions: STARTTLS, AUTH (PLAIN, LOGIN, CRAM-MD5, DIGEST-MD5, GSSAPI), PIPELINING, 8BITMIME, SIZE, DSN, CHUNKING, SMTPUTF8.
   - Record: banner text, supported commands and extensions, server software and version.
   - Flag: banner reveals internal hostname, server version, or software details → low/medium finding (information disclosure).
   - Flag: PLAIN/LOGIN AUTH offered without STARTTLS → high finding (cleartext credential transmission).

### Phase 2 — STARTTLS and encryption posture

1. Check STARTTLS availability:
   - `nmap -p 25 --script smtp-commands <mail-server>` reports if STARTTLS is in the EHLO response.
   - If STARTTLS is not offered → critical finding for any mail server handling sensitive email. Credentials (AUTH) and email content transmitted in cleartext.
2. STARTTLS certificate audit:
   - `openssl s_client -starttls smtp -connect <mail-server>:25 -servername <mail-server>` through executor.
   - If port 465 (SMTPS) is open: `openssl s_client -connect <mail-server>:465 -servername <mail-server>`.
   - Record: TLS version (minimum 1.2), cipher suite, certificate chain, validity, hostname match, issuer.
   - Flag: TLS 1.0/1.1 support → medium finding. TLS 1.2 minimum required. TLS 1.3 preferred.
   - Flag: weak ciphers (RC4, 3DES, EXPORT, NULL, anonymous key exchange) → medium/high finding.
   - Flag: self-signed certificate → low/medium finding. Expired certificate → medium finding.
   - Flag: hostname mismatch (certificate CN does not match the MX hostname) → medium finding (opportunistic TLS with mismatched cert enables MITM downgrade).
3. Check for MTA-STS policy (Mail Transfer Agent Strict Transport Security):
   - DNS query: `dig +short _mta-sts.<domain> TXT` — should return `v=STSv1; id=<timestamp>`.
   - If MTA-STS is configured, also fetch: `https://mta-sts.<domain>/.well-known/mta-sts.txt` — the policy file specifies `mode: enforce` (strict) or `mode: testing` (reporting only).
   - MTA-STS `mode: enforce` → positive control (forces TLS for inbound mail from compliant senders).
   - MTA-STS `mode: testing` or missing → medium finding (no forced TLS for inbound mail).
4. Check for DANE/TLSA (DNS-based Authentication of Named Entities):
   - DNS query: `dig +short _25._tcp.<mx-hostname> TLSA` — checks if the MX host has a TLSA record binding its TLS certificate.
   - DANE is stronger than traditional CA-based TLS because it pins the certificate in DNS (signed by DNSSEC). If DNSSEC is enabled and TLSA records exist → positive control.
   - Missing DANE with DNSSEC → recommendation only (not a finding — DANE adoption is low).

### Phase 3 — open relay detection

Only if scope explicitly permits open-relay testing with controlled recipient addresses:

1. Banner-based check:
   - `nmap -p 25 --script smtp-open-relay <mail-server>` — tests relay by attempting to send to a non-local domain.
   - This is a safe automated check that completes a minimal SMTP transaction. It is detection-only.
2. Manual open-relay test (only with explicit per-test approval):
   - Connect to the mail server, send `EHLO`, then attempt to relay an email to a project-controlled external test address:
     ```
     MAIL FROM:<test@authorized-domain.com>
     RCPT TO:<test-recipient@controlled-test-address.com>
     ```
   - If the server accepts `RCPT TO` for a non-local domain → critical finding (open relay). Open relays are abused for spam and phishing and should be immediately closed.
   - If the server rejects with `Relaying denied` or `550 5.7.1` → positive control.
   - Do NOT complete the transaction with `DATA`. Stop after `RCPT TO` rejection.
   - Use ONLY a project-controlled test recipient address. Never send to real external addresses.

### Phase 4 — user enumeration (VRFY/EXPN)

Only if scope explicitly permits user enumeration testing:

1. Test VRFY command for user enumeration:
   - `nmap -p 25 --script smtp-enum-users <mail-server>` — tests common usernames (root, admin, postmaster, webmaster, etc.) with VRFY.
   - Manual test: connect to mail server, send `VRFY root`, `VRFY admin`, `VRFY postmaster`.
   - If the server returns `252` with the user's mailbox → user enumeration is possible (medium finding). If the server returns `550` or `252 2.1.5 Cannot VRFY user` → VRFY is disabled (positive).
2. Test EXPN command for mailing list expansion:
   - Similarly send `EXPN root`, `EXPN admin`.
   - EXPN expands mailing lists and aliases, revealing internal recipients. If enabled → medium finding.
3. Test RCPT TO enumeration:
   - `for user in root admin postmaster webmaster info support; do echo -e "EHLO test\nMAIL FROM:<test@test.local>\nRCPT TO:<$user@<domain>>\nQUIT" | nc <mail-server> 25 2>/dev/null | grep "250\|550"; done`
   - Different responses for valid vs invalid users (250 vs 550) reveal user existence. If distinguishable → medium finding.
   - Limit enumeration to the common-names list explicitly allowed in scope (maximum 20 addresses). Do NOT brute-force large username lists.
4. Do NOT enumerate beyond the authorized list. Do NOT build or export a user list from the results (use only for finding confirmation).

### Phase 5 — anti-spoofing controls (SPF / DKIM / DMARC)

DNS-based email authentication protects the domain from spoofing:

1. **SPF** (Sender Policy Framework):
   - `dig +short <domain> TXT | grep "v=spf1"`
   - Parse the SPF record: mechanisms (`mx`, `a`, `include`, `ip4`, `ip6`, `ptr`, `exists`, `redirect`), qualifiers (`+` pass, `?` neutral, `~` softfail, `-` hardfail), and the `all` mechanism.
   - `-all` (hard fail) → strictest, rejects unauthorized senders. Positive.
   - `~all` (soft fail) → marks as suspicious but doesn't reject. Medium finding (weak enforcement).
   - `?all` (neutral) or `+all` (allow all) → critical finding — no SPF enforcement at all.
   - Missing SPF record → critical finding.
   - Check SPF lookup count: each `include`, `a`, `mx`, `ptr`, `exists` counts toward the 10-lookup limit. Exceeding 10 causes `PermError` and invalidates SPF. Use `dig` to count and validate.
   - Check that included domains resolve valid SPF records and are not overly permissive.
2. **DKIM** (DomainKeys Identified Mail):
   - Common selectors: `default`, `google`, `selector1`, `selector2`, `dkim`, `mail`, `s1`, `s2`, `k1`, `mandrill`, `sendgrid`, `mailgun`.
   - For each selector: `dig +short <selector>._domainkey.<domain> TXT`
   - Parse: key type (`k=rsa` preferred), key, testing mode (`t=y` or `t=s` — if set, DKIM failures are not enforced → medium finding), granularity (`g=*` uses the key for all local-parts).
   - Check key length: RSA 1024-bit minimum, 2048-bit recommended. RSA 512-bit → high finding (crackable).
   - Missing DKIM for a domain that sends email → high finding (emails cannot be cryptographically verified).
3. **DMARC** (Domain-based Message Authentication, Reporting, and Conformance):
   - `dig +short _dmarc.<domain> TXT`
   - Parse: `v=DMARC1`, `p=` (policy: `none`, `quarantine`, `reject`), `sp=` (subdomain policy), `rua=` (aggregate report address), `ruf=` (forensic report address), `pct=` (percentage applied), `adkim=` (DKIM alignment: `s` strict, `r` relaxed), `aspf=` (SPF alignment).
   - `p=reject` → strictest, rejects unauthorized mail. Positive.
   - `p=quarantine` → sends to spam. Medium finding (partial enforcement).
   - `p=none` → monitoring only, no enforcement. High finding (the domain has the technical controls but doesn't enforce them — spoofed emails reach inboxes).
   - Missing DMARC → critical finding.
   - `ruf=` with an external address → forensic reports contain email content. Flag if reports go to an unapproved third party.
   - `pct=100` → full enforcement. `pct<100` → partial rollout (medium finding if policy is reject/quarantine but percentage is low).
4. **BIMI** (Brand Indicators for Message Identification):
   - `dig +short default._bimi.<domain> TXT`
   - BIMI requires DMARC `p=quarantine` or `p=reject` to be effective. Presence indicates mature email security posture. Missing is not a finding — informational only.
5. **SMTP TLS Reporting (TLS-RPT)**:
   - `dig +short _smtp._tls.<domain> TXT` — reports TLS failures from external MTAs.
   - Presence indicates monitoring of STARTTLS adoption. Informational.

### Phase 6 — hardening assessment

1. **STARTTLS everywhere**: all SMTP endpoints (25, 587, 465) should offer STARTTLS or SMTPS. Missing STARTTLS on port 25 is common (MTA-to-MTA traffic has lagged TLS adoption) but should be flagged. Port 587 (submission) must have STARTTLS.
2. **AUTH mechanisms**: `PLAIN` and `LOGIN` should only be offered under TLS. `CRAM-MD5` and `DIGEST-MD5` without TLS → medium finding (challenge-response without channel encryption can be cracked offline).
3. **Open relay**: must be disabled. Critical finding otherwise.
4. **VRFY/EXPN**: should be disabled on Internet-facing MTAs. Enabled on internal mail servers is acceptable but should be restricted.
5. **Banner information**: should not reveal software version, internal hostname, or OS. Use `smtpd_banner` (Postfix) or equivalent to customize.
6. **Rate limiting**: recommend configuring connection rate limits to slow brute force (Postfix: `smtpd_client_connection_rate_limit`, `anvil_rate_time_unit`).
7. **DNSSEC for email domains**: DNSSEC signs DNS responses including MX, SPF, DKIM, DMARC records. Without DNSSEC, these records can be spoofed. Missing DNSSEC → medium finding for domains handling sensitive email.

## Decision points

- **Open relay detected**: critical finding — immediate remediation required. Server can be used to send spam and phishing emails.
- **SPF missing or `+all`**: critical finding — domain can be trivially spoofed.
- **DMARC `p=none`**: high finding — spoofing protection is technically deployed but not enforced.
- **STARTTLS missing on port 587**: critical finding — user credentials and email content in cleartext on the submission port.
- **PLAIN AUTH without STARTTLS**: critical finding — credentials transmitted in cleartext.
- **VRFY/EXPN enabled and returning valid responses**: medium finding — user enumeration enables targeted brute force and social engineering.
- **DKIM RSA 512-bit key**: high finding — the key can be factored and DKIM signatures forged.
- **Proceed to authenticated SMTP testing**: only if scope provides test credentials and explicitly authorizes authenticated SMTP. This is a separate workflow — SMTP AUTH testing is credential-testing, not reconnaissance.
- **Downgrade to banner/DNS only**: when STARTTLS is required and no test credentials are available. Record what was discovered and stop.

## Prohibited behavior

- Credential brute force against SMTP AUTH (`hydra smtp`, `medusa smtp`) — disabled-default.
- Email spoofing (sending email with forged `MAIL FROM` to test SPF/DKIM/DMARC efficacy) — phishing-class, disabled-default.
- Sending test messages to external/real recipients — prohibited unless scope explicitly authorizes a specific test recipient.
- SMTP header injection (CRLF injection in web forms that feed into SMTP) — exploitation, prohibited unless scope explicitly permits `smtp-injection-validation`.
- Open-relay testing to real external domains — only project-controlled test addresses.
- Bulk mail sending (even to controlled addresses) — DoS/spam-class, prohibited.
- Mailbox enumeration beyond the authorized username list (maximum 20 names) — prohibited.
- AUTH LOGIN or AUTH PLAIN without TLS — prohibited even for the test account. Do not transmit credentials in cleartext.

## Stop conditions

- Server returns `530 5.7.0 Authentication required` for any command → stop, do not attempt to authenticate unless test credentials are provided.
- Open relay test returns `250` for RCPT TO to external domain → record as critical finding, stop relay testing immediately, do NOT complete the DATA transaction.
- VRFY/EXPN returns user mailbox addresses → stop user enumeration, record the exposure, do not expand the test list.
- STARTTLS handshake fails → record the failure, do not retry aggressively.
- Evidence would include email addresses, mailbox names, or user identities → redact and stop that enumeration path.

## Evidence — SMTP service record

For each authorized domain and mail server:

```text
Domain: example.com
MX hosts: [mx1.example.com (10), mx2.example.com (20)]

Mail server: mx1.example.com (10.0.0.10)
Ports: [25 (SMTP), 587 (submission) — both open]
Banner: 220 mx1.example.com ESMTP Postfix (Debian)
  Supported extensions: STARTTLS, PIPELINING, 8BITMIME, SIZE 26214400, DSN, SMTPUTF8
  AUTH: PLAIN LOGIN (only advertised after STARTTLS — positive)

STARTTLS: supported on port 25 and 587
  TLS version: 1.3 (port 25), 1.3 (port 587)
  Cipher: TLS_AES_256_GCM_SHA384
  Certificate: valid (Let's Encrypt), CN=mx1.example.com, expires 2025-08-01
  Weak ciphers: none

Open relay: not an open relay (Relaying denied — 554 5.7.1)

VRFY/EXPN: VRFY disabled (252 2.1.5 Cannot VRFY user — positive)
              EXPN disabled (550 5.7.1 — positive)

SPF: v=spf1 mx -all (hard fail — positive)
DKIM: selector=default, k=rsa, 2048-bit (positive)
      selector=google, k=rsa, 2048-bit (positive)
DMARC: v=DMARC1; p=reject; rua=mailto:dmarc@example.com; pct=100 (positive)
MTA-STS: mode: enforce (positive)
BIMI: not configured (informational)
DNSSEC: enabled on example.com (positive)

Email security grade:
  SPF: A (hard fail, no lookup overflow)
  DKIM: A (2048-bit RSA)
  DMARC: A (p=reject, full enforcement)
  TLS: A (1.3, strong cipher)
  Overall: A

Findings:
  [INFO] All anti-spoofing controls in place and enforced — positive
  [INFO] STARTTLS with TLS 1.3 — positive
```

For a weaker configuration, the findings would list specific gaps with severity.

Aggregate into a domain email security posture summary. Include: MX inventory, STARTTLS posture, open-relay status, user-enumeration exposure, SPF/DKIM/DMARC grades, MTA-STS status, and DNSSEC status.

Never store: VRFY/EXPN results with valid user mailboxes, SMTP session logs with AUTH credentials, email addresses from enumeration (hash or count only), actual DKIM private keys, or open-relay test transaction data with real recipient addresses.

## Report handoff

1. `pentest_agent_record_finding` for each confirmed weakness: open relay, missing SPF/DKIM/DMARC, DMARC `p=none`, STARTTLS missing, PLAIN AUTH without TLS, weak DKIM key, VRFY/EXPN enabled, banner information disclosure.
2. Package findings with the domain's overall email security grade: anti-spoofing score, encryption posture, and relay/enumeration exposure.
3. Recommend: implement SPF with `-all`, deploy DKIM with RSA 2048-bit keys (rotate keys periodically), implement DMARC with `p=reject` and 100% enforcement, enable STARTTLS on all ports with TLS 1.2+, enforce MTA-STS, implement DNSSEC for the domain, disable VRFY/EXPN, monitor DMARC aggregate reports for unauthorized senders, configure BIMI for brand protection, and implement DANE/TLSA for certificate pinning.
4. Explicitly note that no credential brute force, email spoofing, phishing simulation, bulk relay, SMTP header injection, or authenticated mailbox access was performed — only safe banner, DNS, and connection-handshake review.
