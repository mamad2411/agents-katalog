<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ashu1665
description: CTF writeups and security challenges by ashu1665.
---

# Writeups by ashu1665

Source repository: `/repos/ashu1665`

## Repository Index

- report1/README.md

## Writeup Content


### File: report1/README.md

# report1
Report of manual pentest vs automatic for http://zero.webappsecurity.com

#                                           Environment Details  
The Free Online Bank Web site is published by Micro Focus Fortify for the sole purpose of demonstrating the functionality and effectiveness of Micro Focus Fortify’s WebInspect products in detecting and reporting Web application vulnerabilities. This site is not a real banking site and any similarities to third party products and/or Web sites are purely coincidental. This site is provided "as is" without warranty of any kind, either express or implied. Micro Focus Fortify does not assume any risk in relation to your use of this Web site. Use of this Web site indicates that you have read and agree to Micro Focus Fortify’s Terms of Use  

#                                         Features of the Environment  
 1. Font Script : Font Awesome  
 2. Web Framework : Bootstrap  
 3. Programming Language : Java  
 4. JavaScript Libraries : jQuery1.8.2  
 5. Web Server : Apache Tomcat	1.1  
 6. HTML5, HTTPServer[Apache-Coyote/1.1]  
 7. IP [54.82.22.214]  
 8. host : zero.webappsecurity.com  

#                                     Pentesting For Following Bugs  
## a)  XSS (Cross-Site Scripting)  
#### Description:  
Cross-Site Scripting (XSS) attacks are a type of injection, in which malicious scripts are injected into otherwise benign and trusted websites. XSS attacks occur when an attacker uses a web application to send malicious code, generally in the form of a browser side script, to a different end user. Flaws that allow these attacks to succeed are quite widespread and occur anywhere a web application uses input from a user within the output it generates without validating or encoding it. 

### Manaual Test  
Steps to reproduce:  
1. Login in the website  
2. Submit the following paylaod http://zero.webappsecurity.com/bank/account-activity.html?accountId=18132);alert(1234);//992  

POC:-  
![man_xss](https://github.com/ashu1665/report1/blob/master/zero_man_xss.png)  

### Automatic Test  
Steps to reproduce:  
1.Run the following cmd:- python3 vuln_scan.py http://zero.webappsecurity.com/bank/account-summary.html "JSESSIONID=D437107A"  
2. Choose the 1 option as XSS  

POC:-  
![auto_xss1](https://github.com/ashu1665/report1/blob/master/zero_xss1.png)  
![auto_xss2](https://github.com/ashu1665/report1/blob/master/zero_xss2.png)  

## b) SQL Injection  
#### Description:-  
SQL injection is a web security vulnerability that allows an attacker to interfere with the queries that an application makes to its database. It generally allows an attacker to view data that they are not normally able to retrieve. This might include data belonging to other users, or any other data that the application itself is able to access. In many cases, an attacker can modify or delete this data, causing persistent changes to the application's content or behavior.

In some situations, an attacker can escalate an SQL injection attack to compromise the underlying server or other back-end infrastructure, or perform a denial-of-service attack.

### Manaual Test  
Steps to reproduce:  
1. Login the website  
2. Visit the url http://zero.webappsecurity.com/bank/pay-bills-saved-payee.html  
3. Use the payload payeeId=sprint' using POST request  

POC:-
![auto_sqli](https://github.com/ashu1665/report1/blob/master/zero-man_sql.png)  
![auto_sqli2](https://github.com/ashu1665/report1/blob/master/zero_sql_man1.png)  

### Automatic Test  
Steps to reproduce  
1. Run the command python3 vuln_scan.py http://zero.webappsecurity.com/bank/account-summary.html "JSESSIONID=D437107A"  
2. Choose the 2 option SQL 

POC:-  
![sql_injection](https://github.com/ashu1665/report1/blob/master/zero_sql.png)  

## c) XXE(XML External Entity)  
#### Description:-  
An XML External Entity attack is a type of attack against an application that parses XML input. This attack occurs when XML input containing a reference to an external entity is processed by a weakly configured XML parser. This attack may lead to the disclosure of confidential data, denial of service, server side request forgery, port scanning from the perspective of the machine where the parser is located, and other system impacts. 

### Manaual Test  
**Not Found**  

### Automatic Test  
Steps to Reproduce  
1. Run the command python3 vuln_scan.py http://zero.webappsecurity.com/bank/account-summary.html "JSESSIONID=D437107A"  
2. Choose the 3 option XXE  

POC:-  
![XXE](https://github.com/ashu1665/report1/blob/master/zero_xxe.png)  

## d) CORS(Cross-origin resource sharing)    
#### Description:-  
Cross-origin resource sharing (CORS) is a browser mechanism which enables controlled access to resources located outside of a given domain. It extends and adds flexibility to the same-origin policy (SOP). However, it also provides potential for cross-domain based attacks, if a website's CORS policy is poorly configured and implemented.  

### Manaual Test  
Steps to reproduce  
1. Login into the website  
2. Visit the url http://zero.webappsecurity.com/bank/account-summary.html and intercept the request using burp and send it to repeater  
3. Change the origin header to http://bing.com  

POC:-  
![CORS](https://github.com/ashu1665/report1/blob/master/zero_cors_man.png)    

### Automatic Test  
Steps to reproduce  
1. Run the command python3 vuln_scan.py http://zero.webappsecurity.com/bank/account-summary.html "JSESSIONID=D437107A"  
2. Choose the 5 option CORS  

POC:-  
![CORS1](https://github.com/ashu1665/report1/blob/master/zero_cors.png)  

## e) Sensitive Data Leak  
#### Description  
A possible sensitive file has been found. This file is not directly linked from the website. This check looks for common sensitive resources like password files, configuration files, log files, include files, statistics data, database dumps. Each one of these files could help an attacker to learn more about his target. 

### Manual Test  
**Not Found**  

### Automatic test  
Steps to reproduce  
1. Run the command python3 vuln_scan.py http://zero.webappsecurity.com/bank/account-summary.html "JSESSIONID=D437107A"  
2. Choose the option 8 Sensitive Data Leak  

POC:-  
![Sensitive1](https://github.com/ashu1665/report1/blob/master/zero_sensitive_1.png)  

![Sensitive2](https://github.com/ashu1665/report1/blob/master/zero_sensitive_2.png)  

## f) Missing Security Headers  
#### Description:-    
HTTP security headers are a fundamental part of website security. Upon implementation, they protect you against the types of attacks that your site is most likely to come across. These headers protect against XSS, code injection, clickjacking, etc.

### Manaual Test  
Steps to reproduce  
1. Visit https://securityheaders.com/ and in search box enter https://securityheaders.com/  

POC:-  
![Missing Secuity](https://github.com/ashu1665/report1/blob/master/zero_man_security_header.png)  

### Automatic Test  
Steps to reproduce  
1. Run the command python3 vuln_scan.py http://zero.webappsecurity.com/bank/account-summary.html "JSESSIONID=D437107A"  
2. Choose the option 6 missing security headers  

POC:-  
![Security_header](https://github.com/ashu1665/report1/blob/master/zero_security_header.png)

# Comparison Between Manual and Automatic Pentest  
## Number of bug types Found in Manual Test  
1. **XSS**  
2. **SQL Injection**  
3. **CORS**  
4. **Missing Security Headers**  

Total **4 bug types found using Manual test out of 9** tested for  

## Number of bug types Found in Automatic test  
1. **XSS**  
2. **SQL Injection**  
3. **XXE**
4. **CORS**  
5. **Missing Security Headers**  
6. **Sensitive Data Leak**  

Total **6 bug types Found using Automatic test out of 9** tested for  















