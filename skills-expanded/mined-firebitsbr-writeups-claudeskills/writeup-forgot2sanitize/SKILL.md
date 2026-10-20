<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-forgot2sanitize
description: CTF writeups and security challenges by forgot2sanitize.
---

# Writeups by forgot2sanitize

Source repository: `/repos/forgot2sanitize`

## Repository Index

- pentest_portfolio/README.md
- pentest_portfolio/templates/bug_bounty_template.md
- pentest_portfolio/templates/enterprise_template.md
- pentest_portfolio/templates/machine_labs_template.md
- pentest_portfolio/templates/web_labs_template.md
- pentest_portfolio/web_vulnerabilities/portswigger/path_traversal/file_path_traversal_traversal_sequences_stripped_non-recursively/README.md
- pentest_portfolio/web_vulnerabilities/portswigger/path_traversal/file_path_traversal_validation_of_start_of_path/README.md
- pentest_portfolio/web_vulnerabilities/portswigger/command_injection/Blind_command_injection_with_output_redirection/README.md
- pentest_portfolio/web_vulnerabilities/portswigger/authentication/username_enumeration_via_subtly_different_responses/README.md
- pentest_portfolio/web_vulnerabilities/portswigger/access_control_vulnerabilities/idor/README.md
- pentest_portfolio/web_vulnerabilities/portswigger/access_control_vulnerabilities/user_id_controlled_by_request_parameter/README.md

## Writeup Content


### File: pentest_portfolio/README.md

# Security Research & Pentest Portfolio

Welcome to my technical security showcase. This repository documents my journey through web application security, infrastructure testing, and professional reporting.

> **My Philosophy:** I don't just find bugs. I identify the **Root Cause**, evaluate the **Impact**, and provide **Actionable Mitigations** that bridge the gap between security and development.

---

## 🛠 Technical Stack & Toolkit

* **Web Security:** Burp Suite.
* **Network:** Nmap, Netcat, Wireshark.
* **Scripting:** Bash (Automation).
* **Standards:** OWASP Top 10, CVSS v3.1 Scoring.

---

## 📁 Repository Structure

* [**web_vulnerabilities/**](./web_vulnerabilities/) - Detailed writeups of web-based attacks (SQLi, XSS, IDOR) categorized by platform.
* [**machine_writeups/**](./machine_writeups/) - Full "Root-to-Shell" walkthroughs for machines from HackTheBox, VulnHub and TryHackMe.
* [**templates/**](./templates/) - My standardized professional vulnerability reporting templates
---

## 🤝 Let's Connect

I am currently seeking **Junior Security Researcher** or **AppSec Engineer** roles. If you are looking for a security-minded professional who understands the balance between "breaking" and "fixing," let's talk.

- **[LinkedIn](https://www.linkedin.com/in/serhiichornobai/)**
- **Email:** serhii.chornobai123@gmail.com

---

*Disclaimer: All testing performed here was conducted in authorized, controlled lab environments for educational purposes only.*


### File: pentest_portfolio/web_vulnerabilities/portswigger/access_control_vulnerabilities/idor/README.md

# Vulnerability Report: IDOR

## 1. Environment

* **Platform:** PortSwigger Academy
* **Category:** Access Control Vulnerabilities
* **Lab / Target Name:** Insecure direct object references
* **Difficulty / Scope:** Apprentice

---

## 2. Summary

A vulnerability was identified in the "View transcript" button functionality that allows an attacker to access arbitrary chat transcripts by manipulating the `id` parameter in the URL. This issue can be exploited to complete account takeover within the context of the lab environment.

---

## 3. Vulnerability Details

* **Vulnerability Type:** IDOR
* **OWASP Top 10:** A01:2025 Broken Access Control

---

## 4. Affected Component

* **Feature / Functionality:** Transcription download
* **Endpoint:** `/download-transcript/{id}.txt`
* **HTTP Method:** GET
* **Parameter(s):** `id` 

---

## 5. Preconditions

* Attacker must know target account username (e.g `carlos`)
* Availability of targeted function

---

## 6. Technical Description

The application fails to perform adequate server-side authorization checks. It relies solely on the user-provided `id` parameter to fetch data, allowing an attacker to access resources belonging to other users by simply changing the identifier.

---

## 7. Steps to Reproduce

1. Navigate to live chat page
2. Click on "View transcript" button.
3. Intercept the request using Burp Suite.
4. Identify the integer `id` parameter of transcription file in URL.
5. Modify the requested `id` from `2` to `1`.
6. Send the request to the server.
7. Observe that we have access to chat transcript of another user.
8. Observe that in successful intercepted transcript user `carlos` disclosed a password `i41v77ve0hfv5aq7zs8h`. 
9. Login to target account with breached credentials
---

## 8. Proof of Concept

### Normal Behavior:

![Normal Behavior](./assets/normal_behavior.png)

### Modified request:

![Modified Request](./assets/modified_request.png)

### Successful login into the target account:

![Successful Login Into The Target Account](./assets/login_into_target.png)

---

## 9. Root Cause Analysis

The root cause is a lack of access control enforcement at the object level. The application trusts user-supplied input to retrieve sensitive files without verifying if the requesting user has the necessary permissions.

---

## 10. Mitigation

* Implement proper server-side validation and authorization checks.
* Replace predictable integer IDs with randomized, non-guessable identifiers (e.g., UUIDs)
* Ensure that sensitive data aren't stored in plaintext transcription 

---

## 11. Severity Assessment

* **Severity Rating:** High
* **Justification:** The vulnerability allows for unauthenticated access to sensitive data. Given that the attack is easily scalable and leads to complete compromise of user accounts, it is classified as High severity.

*Disclaimer: Assessment based on an educational/lab environment*


### File: pentest_portfolio/web_vulnerabilities/portswigger/access_control_vulnerabilities/user_id_controlled_by_request_parameter/README.md

# Vulnerability Report: User ID controlled by request parameter

## 1. Environment

* **Platform:** PortSwigger Academy
* **Category:** Access Control Vulnerabilities
* **Lab / Target Name:** User ID controlled by request parameter
* **Difficulty / Scope:** Apprentice

---

## 2. Summary

A vulnerability was identified in the URL parameter controlled by user that allows an attacker to perform horizontal privilege escalation by manipulating the `id` URL parameter. This issue can be exploited to complete account takeover within the context of the lab environment.

---

## 3. Vulnerability Details

* **Vulnerability Type:** IDOR
* **OWASP Top 10:** A01:2025 Broken Access Control

---

## 4. Affected Component

* **Feature / Functionality:** My account page
* **Endpoint:** `/my-account?id={username}`
* **HTTP Method:** GET
* **Parameter(s):** `id`

---

## 5. Preconditions

* Attacker must be authenticated as low level user (e.g. `wiener:peter`)
* Availability of targeted function

---

## 6. Technical Description

The application fails to perform adequate server-side authorization checks. It relies solely on the user-provided `id` parameter to fetch data, allowing an attacker to access resources belonging to other users by simply changing the identifier.

---

## 7. Steps to Reproduce

1. Login as low privileged user `wiener:peter`.
2. Go to My account page.
3. Intercept the request using Burp Suite.
4. Identify the parameter with username in URL.
5. Modify the parameter in request to victim's username `carlos`.
6. Send the request to the server.
7. Observe unauthorized access to `carlos` account page.

---

## 8. Proof of Concept

### Expected Behavior:

![Expected Behavior](./assets/expected_behavior.png)

### Modified request and unauthorized access into victim's account:

![Modified Request](./assets/modified_request.png)

---

## 9. Root Cause Analysis

The root cause is a lack of access control enforcement at the object level. The application trusts user-supplied input to retrieve sensitive files without verifying if the requesting user has the necessary permissions.

---

## 10. Mitigation

* Implement proper server-side validation and authorization checks.
* Replace predictable identifiers (such as usernames) for accessing sensitive resources. Use randomized, non-guessable UUIDs instead.

---

## 11. Severity Assessment

* **Severity Rating:** High
* **Justification:** The severity is rated as High because the application allows for horizontal privilege escalation. Since the attack is easily scalable (by iterating through a list of known usernames) and leads to a complete account takeover of any user, the impact on data confidentiality is critical.

*Disclaimer: Assessment based on an educational/lab environment*


### File: pentest_portfolio/web_vulnerabilities/portswigger/authentication/username_enumeration_via_subtly_different_responses/README.md

# Vulnerability Report: Username enumeration via subtly different responses

## 1. Environment

* **Platform:** PortSwigger Academy
* **Category:** Authentication
* **Lab / Target Name:** Username enumeration via subtly different responses
* **Difficulty / Scope:** Practitioner

---

## 2. Summary

A vulnerability was identified in the login page that allows an attacker to enumerate valid usernames. After successful username enumeration the lack of rate limiting or account lockout mechanisms allows for a credential brute-force attack. This issue can be exploited to complete account takeover within the context of the lab environment.

---

## 3. Vulnerability Details

* **Vulnerability Type:** Authentication Flaw
* **OWASP Top 10:** A07:2025 Authentication Failures

---

## 4. Affected Component

* **Feature / Functionality:** User authentication
* **Endpoint:** `/login`
* **HTTP Method:** `POST`
* **Parameters:** `username`,  `password`

---

## 5. Preconditions

* Availability of targeted function
* Lack of attack prevention methods (brute-force protection, rate limiting, account lockout)

---

## 6. Technical Description

The application's authentication response varies subtly based on the validity of the username. Specifically, a trailing period is omitted in the error message when a valid username is provided. This side-channel allows an attacker to distinguish between valid and invalid users.

---

## 7. Steps to Reproduce

1. Navigate to login page.
2. Try to login with test credentials (e.g `testusername` and `testpassword`)
3. Intercept the request using Burp Suite.
4. Send intercepted request to Burp Intruder.
5. Configure the payload for `username` parameter.
6. Start brute-force attack.
7. Observe that error messages have difference in period. When username is invalid error message is `Invalid username or password.`, however when username is valid error message is `Invalid username or password`.
8. By difference in error messages enumerated username is `appserver`.
9. Set enumerated username to the `username` parameter.
10. Configure the payload for `password` parameter.`
11. Start brute-force attack.
12. One of the response has `302` redirection code.
13. Brute-forced password is `ginger`.

---

## 8. Proof of Concept

### Difference between error messages:

![Error Message Difference](./assets/error_messages_difference.png)

### Successful username enumeration:

![Successful Username Enumeration](./assets/username_enum.png)

### Successful password brute-force:

![Successful Password Brute-force](./assets/password_brute-force.png)

### Access to account:

![Access to Account](./assets/access_to_account.png)
---

## 9. Root Cause Analysis

The root cause is improper error handling that results in message inconsistency, leading to information disclosure.

---

## 10. Mitigation

* Ensure the application returns a generic, identical error message (e.g., "Invalid username or password") regardless of which credential was incorrect.
* Implement account lockout policies or CAPTCHA after a certain number of failed attempts.
* Implement strong password policy (minimum length of 12 characters, combining uppercase, lowercase, numbers, and symbols).

---

## 11. Severity Assessment

* **Severity Rating:** High
* **Justification:** The vulnerability presents a high risk because it allows an attacker to systematically enumerate valid usernames with minimal effort. Combined with the absence of rate limiting, this flaw serves as a direct stepping stone to a full account takeover. Since no prior authentication or user interaction is required, the complexity of the attack is Low, while the impact on user data confidentiality is High.

*Disclaimer: Assessment based on an educational/lab environment*


### File: pentest_portfolio/web_vulnerabilities/portswigger/command_injection/Blind_command_injection_with_output_redirection/README.md

# Vulnerability Report: Blind OS command injection with output redirection

## 1. Environment

* **Platform:** PortSwigger Academy
* **Category:** OS Command Injection
* **Lab / Target Name:** Blind OS command injection with output redirection
* **Difficulty / Scope:** Practitioner

---

## 2. Summary

A blind OS command injection vulnerability was identified in the feedback submission functionality. An attacker can inject and execute arbitrary OS commands by manipulating user-controlled input, leading to command execution on the underlying server within the lab environment.

---

## 3. Vulnerability Details

* **Vulnerability Type:** OS Command Injection
* **OWASP Top 10:** A05:2025 Injection

---

## 4. Affected Component

* **Feature / Functionality:** Submit feedback function
* **Endpoint:** `/feedback/submit`
* **HTTP Method:** POST
* **Parameter(s):** `name`, `email`, `subject`, `message`

---

## 5. Preconditions

* The feedback submission functionality is accessible to the user.

---

## 6. Technical Description

The application incorporates user-supplied input into an operating system command without proper validation or sanitization. As a result, an attacker can inject shell metacharacters and execute arbitrary commands. Because command output is not directly returned in the HTTP response, this vulnerability is classified as **blind** command injection. However, output redirection can be used to write command results to a web-accessible location, allowing the attacker to retrieve and verify execution.

---

## 7. Steps to Reproduce

1. Navigate to `/feedback` page
2. Fill in all input fields with arbitrary values (e.g. `test`) and submit the form.
3. Intercept the request using Burp Suite.
4. Modify one of the parameters (all are vulnerable) to the following payload: 
	```
	||whoami>/var/www/images/test.txt||
	```
5. Send the modified request to the server.
6. Navigate to the home page.
7. Intercept the image loading request and access the generated file:
	```
	/image?filename=test.txt
	```

---

## 8. Proof of Concept

### Modified request

```
POST /feedback/submit HTTP/2
Host: 0a5500370394df1d81af1beb00540028.web-security-academy.net
Content-Type: application/x-www-form-urlencoded

csrf=90CutsfrV9QOH9JHCeZMxqxcjSLabjzT&
name=||whoami>/var/www/images/test.txt||&
email=test@gmail.com&
subject=test&
message=test
```

### Command output retrieval

```
GET /image?filename=test.txt HTTP/2  
Host: 0a5500370394df1d81af1beb00540028.web-security-academy.net
```

### Observed behavior

The response contains the output of the `whoami` command, confirming successful command execution on the server.

---

## 9. Root Cause Analysis

The vulnerability exists due to insufficient input validation and unsafe handling of user-supplied data. User input is directly passed to OS-level commands, allowing shell command injection through metacharacters.

---

## 10. Mitigation

* Apply strict server-side input validation and sanitization.
* Implement allowlists where command execution is unavoidable.
* Use safe APIs that do not invoke a system shell.

---

## 11. Severity Assessment

* **Severity Rating:** High
* **Justification:** The vulnerability is easy to exploit and allows arbitrary command execution, which may lead to full system compromise within the affected context.

*Disclaimer: Assessment based on an educational/lab environment*


### File: pentest_portfolio/web_vulnerabilities/portswigger/path_traversal/file_path_traversal_traversal_sequences_stripped_non-recursively/README.md

# Vulnerability Report: File path traversal, traversal sequences stripped non-recursively

## 1. Environment

* **Platform:** PortSwigger Academy
* **Category:** Path Traversal
* **Lab / Target Name:** File path traversal, traversal sequences stripped non-recursively
* **Difficulty / Scope:** Practitioner

---

## 2. Summary

A vulnerability was identified in the image inclusion functionality that allows an attacker to access sensitive internal data (e.g. `/etc/passwd` file) by manipulating the `filename` parameter in the URL. This issue can be exploited to complete system compromise within the context of the lab environment.

---

## 3. Vulnerability Details

* **Vulnerability Type:** Path Traversal
* **OWASP Top 10:** A01:2025 Broken Access Control

---

## 4. Affected Component

* **Feature / Functionality:** image inclusion
* **Endpoint:** `/image?filename={id}.png`
* **HTTP Method:** GET
* **Parameter(s):** `filename`

---

## 5. Preconditions

* Availability of targeted function

---

## 6. Technical Description

The application fails to perform adequate server-side input sanitization. It relies solely on the user-provided `filename` parameter to fetch data, allowing an attacker to access arbitrary files on the server's filesystem by using nested traversal sequences.

---

## 7. Steps to Reproduce

1. View details of arbitrary product on website.
2. Intercept the request using Burp Suite.
3. Identify the `filename` parameter in URL.
4. Modify the requested parameter to `....//....//....//....//....//etc/passwd`.
5. Send the request to the server.
6. Observe content of `/etc/passwd` file in response.

---

## 8. Proof of Concept

### Expected behavior

![Expected Bevaior](./assets/expected_bevaior.png)

### Modified request with content of `/etc/passwd` file in response:

![Modified request](./assets/modified_request.png)

---

## 9. Root Cause Analysis

The root cause is insufficient input sanitization. The application attempts to strip traversal sequences but fails to do so recursively, allowing an attacker to bypass the filter by nesting the sequences (e.g., `....//`).

---

## 10. Mitigation

* Implement a strict allowlist of permitted file names.
* Validate the user input against a predefined set of expected values.
* Use filesystem APIs that resolve paths and verify they stay within the intended base directory (e.g., using `realpath` in PHP or `Path.getCanonicalPath` in Java).

---

## 11. Severity Assessment

* **Severity Rating:** High
* **Justification:** The severity is rated as High because the vulnerability allows for unauthenticated arbitrary file read. An attacker can retrieve sensitive system files (e.g., `/etc/passwd`), which may contain user information or configuration details, leading to a critical breach of confidentiality.

*Disclaimer: Assessment based on an educational/lab environment*


### File: pentest_portfolio/web_vulnerabilities/portswigger/path_traversal/file_path_traversal_validation_of_start_of_path/README.md

# Vulnerability Report: File path traversal, validation of start of path

## 1. Environment

* **Platform:** PortSwigger Academy
* **Category:** Path Traversal
* **Lab / Target Name:** File path traversal, validation of start of path
* **Difficulty / Scope:** Practitioner

---

## 2. Summary

A vulnerability was identified in the image inclusion functionality that allows an attacker to access sensitive internal data (e.g. `/etc/passwd` file) by manipulating the `filename` parameter in the URL. This issue can be exploited to complete system compromise within the context of the lab environment.

---

## 3. Vulnerability Details

* **Vulnerability Type:** Path Traversal
* **OWASP Top 10:** A01:2025 Broken Access Control

---

## 4. Affected Component

* **Feature / Functionality:** image inclusion
* **Endpoint:** `/image?filename=var/www/images/{id}.jpg`
* **HTTP Method:** GET
* **Parameter(s):** `filename`

---

## 5. Preconditions

* Availability of targeted function

---

## 6. Technical Description

The application validates that the `filename` parameter begins with a specific expected directory (e.g., `/var/www/images/`). However, it fails to sanitize the rest of the path, allowing an attacker to use directory traversal sequences (`../`) after the required prefix to escape the intended directory and access sensitive system files.

---

## 7. Steps to Reproduce

1. View details of arbitrary product on website.
2. Intercept the request using Burp Suite.
3. Identify the `filename` parameter in URL.
4. Modify the requested parameter to `var/www/images/../../../etc/passwd`.
5. Send the request to the server.
6. Observe content of `/etc/passwd` file in response.

---

## 8. Proof of Concept

### Expected behavior

![Expected Bevaior](./assets/expected_behavior.png)

### Modified request with content of `/etc/passwd` file in response:

![Modified request](./assets/modified_request.png)

---

## 9. Root Cause Analysis

The root cause is incomplete path validation. While the application enforces a "starts with" check on the file path, it does not prevent path normalization issues. An attacker can satisfy the initial check and then use `../` to navigate to arbitrary locations on the filesystem.

---

## 10. Mitigation

* Do not allow directory traversal sequences (`../`) even if the required prefix is present.
* Use path canonicalization to resolve the final path before reading the file and verify that the resolved path still resides within the allowed directory.

---

## 11. Severity Assessment

* **Severity Rating:** High
* **Justification:** The severity is rated as High because the vulnerability allows for unauthenticated arbitrary file read. An attacker can retrieve sensitive system files (e.g., `/etc/passwd`), which may contain user information or configuration details, leading to a critical breach of confidentiality.

*Disclaimer: Assessment based on an educational/lab environment*


### File: pentest_portfolio/templates/bug_bounty_template.md

# Vulnerability Report: <Short Vulnerability Title>

## 1. Summary

A vulnerability was identified in the <affected functionality> that allows an attacker to <primary attacker action>. By exploiting this issue, it is possible to <clear, concrete impact>.

---

## 2. Vulnerability Details

* **Vulnerability Type:** <e.g., IDOR / XSS / SQL Injection / Auth Bypass>
* **Weakness Category:** <Broken Access Control / Injection / Authentication>

---

## 3. Affected Component

* **Feature / Functionality:** <Feature name>
* **Endpoint:** <Endpoint or URL>
* **HTTP Method:** <GET / POST / etc.>
* **Parameter(s):** <Relevant parameters>

---

## 4. Preconditions

* <Authentication state (if any)>
* <Required user role or permissions>

---

## 5. Steps to Reproduce

1. Navigate to <relevant page or endpoint>.
2. Perform <required initial action>.
3. Intercept the request using a web proxy (e.g., Burp Suite).
4. Identify the <vulnerable parameter / object>.
5. Modify <parameter> from <original value> to <malicious value>.
6. Send the modified request.
7. Observe that <unauthorized behavior or data exposure> occurs.

---

## 6. Proof of Concept

### Request

Modified request demonstrating exploitation:

```
<HTTP request here>
```

### Response

```
<Relevant response snippet showing impact>
```

---

## 7. Impact

* Unauthorized access to <type of data / functionality>.
* Potential for <account takeover / data leakage / privilege escalation>.

---

## 8. Root Cause

The issue occurs because the application does not properly validate <authorization / input / ownership>. User-controlled input is directly used to access internal resources without sufficient security checks.

---

## 9. Mitigation

* Implement proper server-side authorization checks.
* Avoid exposing direct object references.
* Validate all user-controlled input before processing.

---

## 10. Severity Assessment

* **Suggested Severity:** <Low / Medium / High / Critical>
* **Attack Scenario:** <One-sentence realistic abuse case>

---

### Notes for Triagers

* The issue is fully reproducible.
* The impact is demonstrated in the Proof of Concept.


### File: pentest_portfolio/templates/enterprise_template.md

# Vulnerability Report: <Vulnerability Name>

## 1. Executive Summary

A security vulnerability was identified in the <affected component>. The issue allows an attacker to <attacker capability> due to <high-level root cause>. If exploited, this vulnerability may lead to <business-relevant impact> and poses a significant risk to the organization.

---

## 2. Vulnerability Details

* **Vulnerability Type:** <e.g., Broken Access Control / Injection / Authentication Failure>
* **OWASP Top 10:** <e.g., A01:2025 - Broken Access Control>

---

## 3. Affected Component

* **Application / System:** <Application name>
* **Feature / Functionality:** <Feature name>
* **Endpoint:** <Endpoint / URL>
* **HTTP Method:** <GET / POST / etc.>
* **Parameter(s):** <Relevant parameters>

---

## 4. Preconditions

* <Authentication state required>
* <User role or access level>
* <Environmental or configuration prerequisites>

---

## 5. Technical Description

The application processes user requests to <describe functionality>. However, it fails to properly <missing security control>. As a result, an attacker can <technical exploitation path>, which allows <direct technical impact>.

---

## 6. Steps to Reproduce

1. Access <relevant application functionality>.
2. Authenticate as <user role> (if applicable).
3. Intercept the request using a web proxy (e.g., Burp Suite).
4. Identify the <parameter / object / logic flaw>.
5. Modify the request to <malicious change>.
6. Send the request to the server.
7. Confirm that <unauthorized behavior occurs>.

---

## 7. Proof of Concept

### Exploitation Evidence

Evidence demonstrating successful exploitation and impact:

```
<request / response excerpts or logs>
```

Supporting screenshots or artifacts:

![PoC Evidence](./assets/poc_example.png)

---

## 8. Impact Analysis

* **Confidentiality:** <Impact description>
* **Integrity:** <Impact description>
* **Availability:** <Impact description or None>

**Business Impact:**
Successful exploitation may result in <financial loss / regulatory exposure / reputational damage / operational disruption>.

---

## 9. Root Cause Analysis

The root cause of this vulnerability is <design / implementation / configuration flaw>. The application lacks <specific control>, which results in insufficient enforcement of security boundaries and allows unauthorized access to protected resources.

---

## 10. Mitigation Recommendations

To remediate this vulnerability, the following actions are recommended:

* **Primary Remediation:** <Specific technical fix>
* **Compensating Controls:** <Additional short-term mitigations>
* **Preventive Measures:** <Long-term architectural or process improvements>

---

## 11. Severity Assessment

* **Severity Rating:** <Low / Medium / High / Critical>
* **CVSS v3.1 Score:** <Score>
* **CVSS v3.1 Vector:** `CVSS:3.1/AV:?/AC:?/PR:?/UI:?/S:?/C:?/I:?/A:?`

**Risk Justification:**
The severity is based on the ease of exploitation, lack of required privileges, and the potential impact on sensitive data and business operations.

---

### Reporting Notes

* This finding was identified during authorized security testing.
* No production data was altered or destroyed during testing.
* All evidence has been preserved for validation and remediation efforts.


### File: pentest_portfolio/templates/machine_labs_template.md

# Machine Exploitation Report: <Machine Name>

## 1. Environment

* **Platform:** Hack The Box / Proving Grounds / TryHackMe
* **Target / Machine Name:** <Machine name>
* **Difficulty:** <Easy / Medium / Hard>
* **IP Address:** <Target IP>

---

## 2. Executive Summary

The target machine was successfully compromised by exploiting multiple security weaknesses. Initial access was obtained via <initial attack vector>, followed by <privilege escalation technique>, resulting in full system compromise.

---

## 3. Attack Overview

* **Initial Access Vector:** <e.g., Web Service Exploit / Weak Credentials / SMB Misconfiguration>
* **Privilege Escalation Method:** <e.g., SUID binary / Kernel exploit / Misconfigured sudo>
* **Final Access Level:** <User / Root / Administrator>

---

## 4. Reconnaissance & Enumeration

* **Open Ports and Services:**

  * `<port>/<protocol>` - <service> (<version>)

* **Enumeration Techniques:**

  * Nmap scanning
  * Service-specific enumeration (<SMB / FTP / HTTP / etc.>)

---

## 5. Initial Compromise

### Vulnerable Service

* **Service:** <Service name>
* **Port:** <Port>
* **Issue:** <Misconfiguration / Vulnerability description>

### Exploitation

Description of how the vulnerability was exploited to gain initial access.

```
<commands / payloads / responses>
```

---

## 6. Post-Exploitation

* **Obtained Access:** <shell type / user>
* **Credential Discovery:** <files, hashes, keys, if any>
* **Lateral Movement:** <if applicable>

---

## 7. Privilege Escalation

### Privilege Escalation Vector

* **Technique:** <SUID / sudo / cron / kernel / path hijacking>
* **Misconfiguration:** <Exact reason it worked>

```
<commands demonstrating privilege escalation>
```

---

## 8. Proof of Compromise

* **User Flag:** `<flag>`
* **Root / Administrator Flag:** `<flag>`

Screenshots:

![Root Access](./assets/root.png)

---

## 9. Root Cause Analysis

The system suffered from multiple security weaknesses, including <primary root cause> and <secondary issues>. Insufficient hardening and outdated configurations allowed an attacker to escalate privileges and gain full control of the system.

---

## 10. Mitigation Recommendations

* Patch and update vulnerable services.
* Enforce principle of least privilege.
* Remove unnecessary SUID binaries and insecure sudo rules.
* Harden system configurations and restrict service exposure.

---

## 11. Severity Assessment

* **Severity Rating:** High
* **Justification:** Full system compromise was achieved with minimal attack complexity.

*Disclaimer: Assessment based on an educational/lab environment*


### File: pentest_portfolio/templates/web_labs_template.md

# Vulnerability Report: <Vulnerability Name>

## 1. Environment

* **Platform:** <Lab platform (e.g., PortSwigger Academy)>
* **Category:** <Vulnerability category>
* **Lab / Target Name:** <Lab name>
* **Difficulty / Scope:** <Apprentice / Practitioner / Expert>

---

## 2. Summary

A vulnerability was identified in the <affected functionality> that allows an attacker to <attacker capability>. This issue can be exploited to <technical impact> within the context of the lab environment.

---

## 3. Vulnerability Details

* **Vulnerability Type:** <e.g., IDOR / SQL Injection / Authentication Flaw>
* **OWASP Top 10:** <Relevant category>

---

## 4. Affected Component

* **Feature / Functionality:** <Feature name>
* **Endpoint:** <Endpoint path>
* **HTTP Method:** <GET / POST / etc.>
* **Parameter(s):** <Relevant parameters>

---

## 5. Preconditions

* <Authentication state, if required>
* <Any lab-specific conditions>

---

## 6. Technical Description

The application handles <describe normal behavior>. However, it does not properly <missing control or validation>. As a result, an attacker can <describe exploitation logic>.

---

## 7. Steps to Reproduce

1. Navigate to <relevant application page>.
2. Perform <initial setup action>.
3. Intercept the request using Burp Suite.
4. Identify the <vulnerable parameter / object>.
5. Modify the request to <malicious change>.
6. Send the request to the server.
7. Observe that <expected lab success condition> occurs.

---

## 8. Proof of Concept

### Exploitation Evidence

```
<Request / response snippets>
```

Supporting screenshots:

![PoC Screenshot](./assets/poc.png)

---

## 9. Root Cause Analysis

The root cause of this vulnerability is the absence of <specific security control>. The application exposes <internal object or logic> directly to user input, enabling unauthorized actions.

---

## 10. Mitigation

* Implement proper server-side validation and authorization checks.
* Avoid predictable identifiers or insecure logic.
* Follow secure design principles relevant to this vulnerability class.

---

## 11. Severity Assessment

* **Severity Rating:** <Low / Medium / High>
* **Justification:** Severity is based on ease of exploitation and the impact demonstrated in the lab scenario.

*Disclaimer: Assessment based on an educational/lab environment*
