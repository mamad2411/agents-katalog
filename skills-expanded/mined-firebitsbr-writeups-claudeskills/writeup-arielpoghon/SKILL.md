<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-arielpoghon
description: CTF writeups and security challenges by Arielpoghon.
---

# Writeups by Arielpoghon

Source repository: `/repos/Arielpoghon`

## Repository Index

- -My_first_bug-/README.md

## Writeup Content


### File: -My_first_bug-/README.md

# pentest-portfolio
#https://legendary-queijadas-e0916f.netlify.app/

pentesting writeups,tools and mini pentest reports -Ariel M.Poghon
#My first payout 
##Expired TLS Certificate on a3desk.thetradedesk.com - Enables MITM
#ID
26bffe43-eb8a-42af-92ce-6ebd24d149e6
#Submitted
08 Nov 2025 12:50:32 UTC
#Target Location
*.thetradedesk.com
#Target category
#Web App
#VRT
#Cryptographic Weakness > Use of Expired Cryptographic Key (or Certificate)
#Priority
P4
#Description
Cryptography is used to ensure secure storage and transmission of data. However, there are a number of best practices that must be followed to ensure the cryptography in use remains secure and does not result in the exposure of sensitive data. The application uses broken, weak, or otherwise flawed cryptography which can allow an attacker to decrypt sensitive information.

#Business Impact

This vulnerability can lead to reputational damage of the company through the impact to customers’ trust, and the ability of an attacker to view data. The severity of the impact to the business is dependent on the sensitivity of the accessible data being transmitted by the application.

#Breaks secure access for employees/partners.
Facilitates phishing (spoof site with valid cert).
Violates PCI/GDPR if any PII transmitted. -An attacker can set up a transparent MITM proxy. -When victim visits https://a3desk.thetradedesk.com and clicks "Proceed", all cookies, form data, API calls are fully decrypted and modifiable.
Steps to Reproduce

Visit https://a3desk.thetradedesk.com/ → Chrome/Firefox: "Your connection is not private" (NET::ERR_CERT_DATE_INVALID).
Run: openssl s_client -connect a3desk.thetradedesk.com:443 -servername a3desk.thetradedesk.com < /dev/null
Output:
verify error:num=10:certificate has expired
notAfter=Jun 11 23:59:59 2025 GMT
subject=CN=a3desk.thetradedesk.com
issuer=C=US, O=Amazon, CN=Amazon RSA 2048 M03
Verify return code: 10 (certificate has expired)

#Proof of Concept (PoC)
Verify certificate expiry
1.Run on terminal for full verification ,you can refer on attached screenshot.
openssl s_client -connect a3desk.thetradedesk.com:443 -servername a3desk.thetradedesk.com < /dev/null 2>&1 | grep -E "subject|issuer|notBefore|notAfter|expired"

#References
CWE-299: Improper Certificate Validation
CWE-327: Use of a Broken or Risky Cryptographic Algorithm
OWASP A02:2021 – Cryptographic Failures
NIST SP 800-52r2 §3.3: Certificates must be valid
PCI DSS 4.0 Requirement 4.2.1: Valid certificates required

#Guidance
The application uses broken, weak, or otherwise flawed cryptography which can allow an attacker to decrypt sensitive information. This includes:
Support for TLS 1.0/1.1 with weak CBC-SHA ciphers (vulnerable to BEAST, POODLE, Lucky13) on 25+ subdomains – forces downgrades and breaks confidentiality.
Fully expired TLS certificate on internal A3Desk tool (expired June 11, 2025) – enables seamless MITM after user bypasses warning.
Outdated nginx 1.29.0 performing TLS termination (misses crypto patches, e.g., CVE-2025-53859).

The following screenshot(s) demonstrate(s) this vulnerability:
<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/cf4e7f25-daf5-44f8-892e-6a5b6d803fab" />

