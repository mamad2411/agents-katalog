<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ensarhamza123
description: CTF writeups and security challenges by ensarhamza123.
---

# Writeups by ensarhamza123

Source repository: `/repos/ensarhamza123`

## Repository Index

- pentesting-portfolio/README.md
- pentesting-portfolio/Business logic vulnerabilities/business-logic-vulnerabilities-lab-01-excessive-trust-in-client-side-controls.md
- pentesting-portfolio/Information disclosure/lab-01-information-disclosure-in-error-messages.md
- pentesting-portfolio/SQL Injecion/lab-01-where-clause-retrieve-hidden-data.md

## Writeup Content


### File: pentesting-portfolio/README.md

# pentesting-portfolio
A collection of penetration testing lab reports from PortSwigger Web Security Academy, documented in a professional pentest report style.



### File: pentesting-portfolio/Business logic vulnerabilities/business-logic-vulnerabilities-lab-01-excessive-trust-in-client-side-controls.md

# Excessive Trust in Client-Side Controls

**Lab:** PortSwigger Web Security Academy – Excessive Trust in Client-Side Controls  
**Difficulty:** Apprentice  
**Date Completed:** 10 August 2025  
**Tools Used:** Burp Suite Community Edition (Proxy, Intercept), PortSwigger-provided browser

---

## Executive Summary
This lab demonstrated a business logic vulnerability caused by excessive trust in client-side controls. The price of an item was set on the client side and was not validated on the server, allowing an attacker to manipulate the price before completing a purchase.

---

## Steps Taken

1. **Login**
   - Logged into the provided lab account with a starting balance of **$100**.

2. **Product Selection**
   - Selected a high-value item: *Leather Jacket* priced at **$1300**.

3. **Intercepting the Request**
   - Added the item to the shopping cart.
   - Enabled **Burp Suite Intercept** to capture the HTTP request.

4. **Modifying the Price**
   - Located the `price` parameter in the intercepted request.
   - Changed the value from:
     ```
     price=1300
     ```
     to:
     ```
     price=0.01
     ```

5. **Completing the Purchase**
   - Forwarded the modified request.
   - Successfully purchased the jacket for **$0.01**.

6. **Post-Purchase Verification**
   - Account balance decreased from **$100** to **$99.99**.
   - Jacket appeared in the account's order history.

---

## Impact
This vulnerability allowed the purchase of any item at an arbitrary price, potentially leading to:
- Loss of revenue
- Inventory theft
- Abuse of promotional offers

---

## Remediation
- Perform **server-side validation** for all critical values such as prices, discounts, and quantities.
- Reject or ignore values received from the client that should be calculated or verified on the server.
- Implement integrity checks (e.g., hash/signature) for client-sent data.

---




### File: pentesting-portfolio/Information disclosure/lab-01-information-disclosure-in-error-messages.md

# Information Disclosure in Error Messages

**Lab:** PortSwigger Web Security Academy – Information Disclosure in Error Messages  
**Difficulty:** Apprentice  
**Date Completed:** 10 August 2025  
**Tools Used:** Burp Suite Community Edition (Proxy, HTTP History, Repeater), Google Chrome

---

## Executive Summary
This lab demonstrated a vulnerability where verbose error messages revealed sensitive details about the underlying web application framework. By manipulating a product ID parameter, I triggered an error that disclosed the exact version of the Apache Struts framework used by the server. Such information can be exploited by attackers to identify and target known vulnerabilities.

---

## Steps Taken

1. **Browsing Products**
   - Accessed the lab environment via Burp Suite's integrated browser (Google Chrome).
   - Clicked on multiple products while monitoring HTTP requests in the **Proxy → HTTP history** tab.

2. **Identifying Parameters**
   - Noticed product pages making requests with a `productId` parameter, for example:
     ```
     GET /product?productId=2
     ```

3. **Testing for Information Disclosure**
   - Sent a request to **Repeater** in Burp Suite for further testing.
   - Modified the `productId` value from:
     ```
     productId=2
     ```
     to:
     ```
     productId=test
     ```

4. **Error Message Analysis**
   - The server responded with a detailed error message containing:
     ```
     Apache Struts 2.3.31
     ```
   - This revealed both the framework name and version in use.

5. **Lab Completion**
   - Entered the disclosed version into the lab’s answer box, successfully completing the challenge.

---

## Impact
An attacker could use disclosed framework and version information to:
- Identify publicly known vulnerabilities affecting that version.
- Develop targeted exploits against the application.
- Gain deeper insights into the technology stack for further attacks.

---

## Remediation
- Disable verbose error messages in production environments.
- Implement generic error handling that hides technical details from users.
- Log full technical errors server-side for internal review only.
- Regularly patch and update frameworks to the latest secure versions.

---




### File: pentesting-portfolio/SQL Injecion/lab-01-where-clause-retrieve-hidden-data.md

# SQL Injection Vulnerability in WHERE Clause Allowing Retrieval of Hidden Data

**Lab:** PortSwigger Web Security Academy – SQL Injection Vulnerability in WHERE Clause Allowing Retrieval of Hidden Data  
**Difficulty:** Apprentice  
**Date Completed:** 10 August 2025  
**Tools Used:** Web Browser (Google Chrome)

---

## Executive Summary
This lab demonstrated a SQL Injection vulnerability in a product category filter. The application failed to properly sanitize user input in the `category` parameter, allowing the injection of SQL code into the WHERE clause. This enabled retrieval of hidden products from the database that were not meant to be displayed to the user.

---

## Steps Taken

1. **Navigating to the Category**
   - Accessed the **Gifts** category from the store navigation menu.
   - Observed the URL format:
     ```
     https://<lab-url>/filter?category=Gifts
     ```

2. **Testing for SQL Injection**
   - Modified the URL to append a single quote (`'`) to test for possible SQL errors:
     ```
     category=Gifts'
     ```
   - Received an error, confirming possible SQL Injection.

3. **Injecting a Boolean Condition**
   - Changed the `category` parameter to:
     ```
     category=Gifts'+OR+1=1--
     ```
   - This injected a tautology into the SQL query, forcing it to return all rows.

4. **Results**
   - Hidden products from the Gifts category were revealed in the product listing.
   - Successfully completed the lab.

---

## Impact
This vulnerability allowed bypassing intended restrictions to access hidden products or data. In a real-world scenario, attackers could:
- Access restricted or premium products without authorization.
- Enumerate all database records for a given table.
- Potentially chain this attack with other SQL Injection exploits for further compromise.

---

## Remediation
- Use parameterized queries (prepared statements) to handle user input safely.
- Validate and sanitize all incoming parameters.
- Implement least privilege for database accounts to limit the impact of injection attacks.

---

