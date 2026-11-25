<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dlray89
description: CTF writeups and security challenges by Dlray89.
---

# Writeups by Dlray89

Source repository: `/repos/Dlray89`

## Repository Index

- Web-Pentesting-Assessment-Reports-HTB/file-upload-assessment-report.md

## Writeup Content


### File: Web-Pentesting-Assessment-Reports-HTB/file-upload-assessment-report.md

# E-Commerce Web Application Assessment Report

Company: HTB </br>
Author: David Ray Jr

</br>

I was assigned to perform a penetration test for a company's e-commerce web application. The web application is in its early stages, so I will only be testing any file upload forms you can find.


## Main Security issues

* Client side validation was easily bypassed by modifying front end code along with modifying the extention by:
    * Character injection
    * Reverse double extentions
    * Double Extentions

* Web application vulnerable to XXE exploitation by creating an SVG image with malicious XML code to leak source code of the upload.php file.
* Black-List was able to be bypassed by fuzzing for extentions for potential extentions that can be use in the attack.
* Uploading a basic webshell to take control over the web-server.

## Mitigation

### Extentions Validation:
</br>
Recommended to use both by whitelisting the allowed extensions and blacklisting dangerous extensions. This way, the blacklist list will prevent uploading malicious scripts if the whitelist is ever bypassed.

Also apply both back-end and front-end file validation. Even if front-end validation can be easily bypassed, it reduces the chances of users uploading unintended files, thus potentially triggering a defense mechanism and sending us a false alert.

### Content Validation:
</br>
 We cannot validate one without validating the other and you must always validate both the file extension and its content. you should also make sure that the file extension matches the file's content.

</br> 

### Upload Disclosure:
You should always avoid disclosing the uploads directory or providing direct access to the uploaded file. I recommended to hide the uploads directory from the end-users and only allow them to download the uploaded files through a download page.






