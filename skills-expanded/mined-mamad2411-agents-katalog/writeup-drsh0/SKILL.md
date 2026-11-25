<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-drsh0
description: CTF writeups and security challenges by drsh0.
---

# Writeups by drsh0

Source repository: `/repos/drsh0`

## Repository Index

- CySCA2018/Keep-it-hidden-writeup.md
- CySCA2018/README.md
- CySCA2018/Miscellaneous/network_basic[24pts].md
- CySCA2018/corp-pentest/zoned6v-writeup.md
- CySCA2018/web-app-pentest/Thinking_outside_the_box[109pts].md
- CySCA2018/web-app-pentest/double_agent[36pts].md
- CySCA2018/web-app-pentest/easy_money[24pts].md
- CySCA2018/web-app-pentest/keep_it_secret[244pts].md
- CySCA2018/Resources/CTFs-and-Boxes/README.md
- CySCA2018/Resources/Web/README.md

## Writeup Content


### File: CySCA2018/README.md

# CySCA 2018

A collection of notes and solutions for CySCA 2018 from team UTS and [UTS Cyber Security Society](http://facebook.com/utscsec). This project encourages all pull requests. 



### File: CySCA2018/Resources/CTFs-and-Boxes/README.md

# CTFs and Boxes

## Hack the box

[Hack the box](https://www.hackthebox.eu/) is a great site that contains vulnerable boxes as well as challenges that cover various areas such as Web, Steganography, Cryptography, etc. The boxes that they host are great for beginners and advanced users that are really challenging and provides a great environment to test your knowledge.


### File: CySCA2018/Resources/Web/README.md

# Web Application Penetration Testing Resources

## Root-me

[Root-me](https://www.root-me.org/?lang=en) is an online platform that contains challenges for a vast majority of different areas in security, it has a huge amount of various web application challenges both for web servers and web clients and caters to both beginners and advanced hackers.


### File: CySCA2018/Keep-it-hidden-writeup.md

CySCA 2018 | Keep it Hidden writeup

Looking at the webpage we are provided we can see an under construction page, which appears to be a sql table.

If we have our user agent set to *BOBDev/1.4* the webpage shows us the paramter *formatted=true*

Changing that to false we see a webpage that has the same table witht he value for flags changed to 1 (this means we are on the right track)

After a while of throwing everything at this webpage another parameter was discovered *debug=*

Looking around on the internet for vulnerabilities in php we found **PHP TEMPLATE INJECTION** where special characters, such as { are used to make the webpage execute arbitrary code or disclose information

making *debug={{self}}* threw an error that said *Template reference not found*

making *debug={{flag}}* caused the page to print the flag


### File: CySCA2018/Miscellaneous/network_basic[24pts].md

# Network Basic

Goal: Analyse a PCAP containing a brute force attempt to find the password that was successful in logging into an admin account.

- Brief tells use that the PCAP contains traffic capturing a brute force attempt against the admin login of a website.
- Download the PCAP file, and open it in wireshark.
- Since this capture involves brute forcing a web login, start filtering by http in wireshark.
- Sort the returned list of http packets by the status code and look for a status code of 200, which indicated that a login was successful.
- After highlighting the correct packet, sort the list by time each packet was sent.
- The request send in the packet before the 200 status code packet should contain the login details for admin.
- Found the credentials, which should be admin:Mellon.



### File: CySCA2018/corp-pentest/zoned6v-writeup.md

Corporate Pentest 1 writeup *Zonedv6*

___
We were initially given the domain bob.cysca

If we do *host -t mx bob.cysca* we see that it's DNS is managed by ns.bob.cysca and ns6.bob.cysca

Attempting a zone transfer with *nslookup -type=axfr bob.cysca ns6.bob.cysca* contained these two lines in the output
___

flag.udp.bob.cysca    service = 10 10 34532 axfr6flag.bob.cysca.

___
From this we can see axfr6flag.bob.cysca has a service running on port 34532

using openbsd-nc we can connect to it by executing

*nc -6v axfr6flag.bob.cysca* 

and it will print the flag



### File: CySCA2018/web-app-pentest/Thinking_outside_the_box[109pts].md

## Challenge 23: Thinking outside the box [109 pts]
> I hope all these login pages are done securely.

### Write-up

- looking at chat with Henry;
- he’s having an error logging into the org. site as a **member**
- so lets logout and then force an error. Cool, so we get a return error of `Invalid option selected for parameter 'user'` 
- we see that the sign on integration is running through `user=individual` and we decide to change it to `user=organisation`;
- we are prompted with an org. login form
- we know that the user name is henry and that the server is running SQL
- push username as `henry` and password as `' or 1=1--` 
- profit



### File: CySCA2018/web-app-pentest/double_agent[36pts].md

## Double Agent [36 pts]
> On the Internet, nobody knows you're a dog.

**Write-up**

- challenge name insinuates that you have to impersonate someone, or something;
- reading through the chat with John reveals that you can only view certain sections of the website with the browser `BOBDev` that isn’t version `1.3`;
- this hint is emphasised by visiting `/config` where is displays the error that the page “is incompatible with your browser”;
- configure your `user-agent` and manually verbose the browser `BOBDev/1.4`;
- profit



### File: CySCA2018/web-app-pentest/easy_money[24pts].md

## Easy Money [24 pts]
> Sigh, old (bad) habits die hard.
- view source
      <!-- I've learned my lesson, no more cleartext passwords in comments -->
                    <!-- Luckily hashes aren't reversible so only I can tell what the password is :D -->
                    <!-- guest:40be4e59b9a2a2b5dffb918c0e86b3d7 -->
- Crack Md5 using https://crackstation.net/
- **user:** `guest`
- **pwd:** `welcome`

### Write-up

- Visit URL to find a login form;
- Inspect by viewing source code;
- Hint from previous write-up with MD5 hash password
- Crack MD5 hash with https://crackstation.net/ or hashcat
- Profit



### File: CySCA2018/web-app-pentest/keep_it_secret[244pts].md

## Challenge 27: Keep it secret [244 pts]
> Leaving these dev sites around is just reckless!
> **HINT:** Your answer to "Double Agent" may help you here

### Write-up

- after navigating into the `dev_page?`, our team started digging around;
- using the hint from the `Double Agent` challenge, we were able to force the website into development mode with an appended string `formatting=false`;
- from here we found that there was a new un-formatted table and noticed that the “flags” stock was set to `1` whereas it was set to `0` on the `BOBDev/1.4` browser.
- we also notice a `debug =` string, so we start playing around and doing some research and attempt to append system print commands into the URL payload using Server-Side Template Injection with Flask. This is because Flask allows for the creation of templates using strings of HTML in the Python source code or laid out in static files in a templates directory local to `webpentest.cysca`
- input was sanitised and so we started testing with single strings
- forcing `http://webpentest.cysca:8000/dev_page?formatting=false&flags=1&debug={{config}}` printed out the config
- and so since there is `1` flag in stock, we would need to print `{{flag}}` in the appended parameter
- profit

config gives you:

    ```debug = <Config {'JSONIFY_PRETTYPRINT_REGULAR': False, 'SERVER_NAME': None, 'JSON_AS_ASCII': True, 'SESSION_REFRESH_EACH_REQUEST': True, 'SESSION_COOKIE_PATH': None, 'ENV': 'production', 'SECRET_KEY': 'secret', 'MAX_CONTENT_LENGTH': None, 'SESSION_COOKIE_DOMAIN': False, 'PREFERRED_URL_SCHEME': 'http', 'USE_X_SENDFILE': False, 'TRAP_HTTP_EXCEPTIONS': False, 'SESSION_COOKIE_NAME': 'session', 'BASE_DIR': '/opt/cysca-web', 'DEBUG': True, 'PROPAGATE_EXCEPTIONS': None, 'SQLALCHEMY_DATABASE_URI': 'sqlite:////opt/cysca-web/app.db', 'SESSION_COOKIE_SECURE': False, 'PRESERVE_CONTEXT_ON_EXCEPTION': None, 'SESSION_COOKIE_HTTPONLY': True, 'CSRF_SESSION_KEY': 'secret', 'TRAP_BAD_REQUEST_ERRORS': None, 'EXPLAIN_TEMPLATE_LOADING': False, 'APPLICATION_ROOT': '/', 'JSONIFY_MIMETYPE': 'application/json', 'THREADS_PER_PAGE': 2, 'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 'TESTING': False, 'SESSION_COOKIE_SAMESITE': None, 'DATABASE_CONNECT_OPTIONS': {}, 'JSON_SORT_KEYS': True, 'CSRF_ENABLED': True, 'TEMPLATES_AUTO_RELOAD': None, 'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200), 'MAX_COOKIE_SIZE': 4093}>```

