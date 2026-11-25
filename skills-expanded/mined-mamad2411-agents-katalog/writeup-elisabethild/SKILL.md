<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-elisabethild
description: CTF writeups and security challenges by ElisabethIld.
---

# Writeups by ElisabethIld

Source repository: `/repos/ElisabethIld`

## Repository Index

- Bug-Bounty-Journey/README.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/Path-Traversal.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/README.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/Step-1-How-the-Web-Works.md
- Bug-Bounty-Journey/Phase-2-Web-Attacks-and-Tools/README.md
- Bug-Bounty-Journey/Phase-3-Real-Targets-and-Practice/README.md
- Bug-Bounty-Journey/Phase-4-Reporting-and-Bug-Bounty-Platforms/README.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Essencials-Proxy.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Google-Dorking.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/OSINT-Techniques.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Scope-Discovery.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Tech-Stack-Fingerprinting.md
- Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Writing-Your-Own-Recon-Scripts.md

## Writeup Content


### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/README.md

# 🔍 PHASE 1: Basics + Start Finding Easy Bugs (0–2 months)

🎯 **My Goal:**  
Build a strong base.  
Start practicing with real bugs and super simple CTFs (Capture The Flag challenges).

📚 **I’m learning:**  
- How the web works: HTTP, HTML, forms, cookies, sessions.  
- The OWASP Top 10 (the 10 most common web bugs).  
- How to use important tools like:
  - Browsers with extensions (FoxyProxy, Wappalyzer)  
  - Burp Suite (Community version – free)

🛠 **I’m already practicing on:**  
- Hack The Box Academy  
- PortSwigger Web Security Academy  
- TryHackMe (I’m doing beginner rooms like “Intro to Pentesting” and “OWASP Top 10”)  
- Hacktivity (I read real bug reports to learn from others)

🧠 **My focus now:**  
I’m starting with **XSS (Cross-Site Scripting)** and **IDOR (Insecure Direct Object Reference)**.  
They’re common bugs and you don’t need to be a tech genius to find them. Just practice and observe carefully!



### File: Bug-Bounty-Journey/Phase-2-Web-Attacks-and-Tools/README.md

# 🧪 PHASE 2: Level Up Skills + First Real Bug (2–4 months)

🎯 **My Goal:**  
Get more confident.  
Start understanding more complex bugs and hopefully report my first real vulnerability.

📚 **I’m learning:**  
- Deeper web concepts (CORS, authentication, sessions, APIs)  
- More OWASP bugs: CSRF, Open Redirect, SSRF, SQLi  
- How bug bounty platforms work: HackerOne, Bugcrowd, Intigriti  
- How to write a good bug report

🛠 **I’m practicing on:**  
- More TryHackMe rooms (intermediate level)  
- PortSwigger Academy (labs on the new OWASP bugs)  
- Bug bounty platforms (starting to look for low-hanging bugs)  
- Doing CTFs

🧠 **My focus now:**  
Try to find and report my **first real bug**, even if it's a low severity one.  
Learn from others' reports, stay patient, and don’t be afraid to fail. It’s part of the process!



### File: Bug-Bounty-Journey/Phase-3-Real-Targets-and-Practice/README.md

# 🛡️ PHASE 3: Get Consistent + Build My Reputation (4–7 months)

🎯 **My Goal:**  
Find bugs more often.  
Become faster at testing, better at reporting, and start getting some real results and invites.

📚 **I’m learning:**  
- Recon (finding targets, subdomains, endpoints)  
- Automation with tools and scripts  
- Vulnerability chaining (combining small bugs into big impact)  
- Deep dives into fewer targets (quality over quantity)

🛠 **I’m practicing on:**  
- Public and private programs on HackerOne, Bugcrowd, Intigriti  
- Recon platforms like Assetnote, Chaos, ProjectDiscovery tools  
- Writing clean, professional reports  
- Creating content (write-ups, notes)

🧠 **My focus now:**  
Improve my **recon and reporting game**, be more efficient, and start building a real **name in the community**.  
One step closer to becoming a pro.



### File: Bug-Bounty-Journey/Phase-4-Reporting-and-Bug-Bounty-Platforms/README.md

# 🧠 PHASE 4: Mastery + Give Back (7–12 months and beyond)

🎯 **My Goal:**  
Become highly skilled, confident, and recognized in the bug bounty community.  
Give back by sharing knowledge and helping others grow too.

📚 **I’m learning:**  
- Advanced web attacks (prototype pollution, desync, race conditions)  
- Custom payload crafting and fuzzing  
- Advanced recon and automation  
- Creating personal tools or scripts

🛠 **I’m practicing on:**  
- High-tier private programs  
- My own lab environments to test edge cases  
- Collaborating with other hunters  
- Participating in CTFs and live hacking events

🧠 **My focus now:**  
Be a consistent and valuable contributor in the field.  
Build a strong portfolio (maybe even speak at conferences or write technical blogs).  
I’m no longer just learning — I’m **teaching**, **sharing**, and **leading**.



### File: Bug-Bounty-Journey/README.md

# Bug-Bounty-Journey
🕷️ A structured roadmap documenting my hands-on journey to become a Bug Bounty Hunter — from fundamentals to real-world reports.

---

🎯 Goal: Tracking my progress through a 4-phase plan to become a skilled Web Pentester and Ethical Hacker.

🧪 Focus: A learning and action-based repository focused on web security, pentesting, and vulnerability research.

---

## 📚 Table of Contents

- [Phase 1: Setup & Foundations](#phase-1-setup--foundations)
- [Phase 2: Web Attacks & Tools](#phase-2-web-attacks--tools)
- [Phase 3: Real Targets & Practice](#phase-3-real-targets--practice)
- [Phase 4: Reporting & Bug Bounty Platforms](#phase-4-reporting--bug-bounty-platforms)
- [Resources](#resources)

---

## ⚙️ Phase 1: Setup & Foundations

- [ ] Install and configure a local lab (Burp Suite, OWASP Juice Shop, DVWA, etc.)
- [ ] Complete Web Security Academy modules (Authentication, Access Control, etc.)
- [ ] Learn HTTP, HTML, and basics of JS relevant to web pentesting
- [ ] Study OWASP Top 10 (latest version)

---

## 🛠️ Phase 2: Web Attacks & Tools

- [ ] Practice XSS, SQLi, CSRF, IDOR, SSRF, etc.
- [ ] Learn to use tools: Burp Suite, ffuf, nuclei, etc.
- [ ] Set up automation with bash/python for recon
- [ ] Take notes on payloads, bypasses, and behaviors

---

## 🎯 Phase 3: Real Targets & Practice

- [ ] Register on HackerOne, Bugcrowd, and TryHackMe bug bounty rooms
- [ ] Hunt on public programs (Respect scope!)
- [ ] Practice on labs like PortSwigger, PentesterLab, HackTheBox
- [ ] Start a vulnerability database (personal notes)

---

## 📋 Phase 4: Reporting & Bug Bounty Platforms

- [ ] Learn how to write professional bug reports
- [ ] Understand disclosure rules and legal boundaries
- [ ] Report your first bug (even if out-of-scope)
- [ ] Build a report template (Markdown or PDF)

---

## 📎 Resources

- [Web Security Academy](https://portswigger.net/web-security)
- [OWASP Cheat Sheets](https://cheatsheetseries.owasp.org/)
- [Bug Bounty Radar](https://bugbountyguide.com/)
- [HackerOne Directory](https://hackerone.com/directory/programs)
- [PayloadAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings)

---



### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/Path-Traversal.md

BurpSuite Proxy -> Repeater

### 1

`GET /image?filename=51.jpg HTTP/2` =>
```
HTTP/2 200 OK
Content-Type: image/jpeg
X-Frame-Options: SAMEORIGIN
Content-Length: 177003

ÿØÿá!Exif ... etc ...
```

### 2

`GET /image?filename=/etc/passwd HTTP/2` =>
```
HTTP/2 400 Bad Request
Content-Type: application/json; charset=utf-8
X-Frame-Options: SAMEORIGIN
Content-Length: 14
```

`"No such file"`

### 3 Correct

`GET /image?filename=../../../etc/passwd HTTP/2` =>
```
HTTP/2 200 OK
Content-Type: image/jpeg
X-Frame-Options: SAMEORIGIN
Content-Length: 2316
```

```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync ... etc ...
```



### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/Step-1-How-the-Web-Works.md

# Step 1: How the Web Works

## 1. How the Web Works?
The web is like a huge toy store. When you want to buy a toy (visit a webpage), you ask the shopkeeper (the server) if they have the toy (the webpage you want to see). The shopkeeper responds by saying, "Yes, I have this toy!" and gives it to you (the webpage appears in your browser).

## 2. HTTP (Hypertext Transfer Protocol)
HTTP is like the language you and the shopkeeper use to talk. You say, “I want that toy,” and the shopkeeper says, “Here’s the toy you asked for.” When you open a webpage, your browser (like Google Chrome or Firefox) talks to the server using this language called HTTP. It lets things move back and forth, like a conversation.

**Example:**
- **You**: "Hello, I want to see my favorite page."
- **Server**: "Here you go, enjoy!"

## 3. HTML (HyperText Markup Language)
HTML is like the blueprint for building a house. When you go to a webpage, the page has different parts, like a roof, walls, windows, etc. HTML tells where to put everything: a title here, a paragraph there, an image over here. It makes the webpage look organized, not just a bunch of words and numbers.

**Example:**
- The **roof** of the house is the **title** of the webpage.
- The **walls** are the **texts** you see.
- The **windows** are the **images** or links you can click.

## 4. Forms
Forms are like when you write a letter or a list of things you want to ask for. When you want to send information to a server (like your name or a message), you use a form. This form is like a sheet with empty spaces where you can write things down.

**Example:**
- In the toy store, if you want to ask for a special toy, the shopkeeper gives you a form where you write your name and what you want.
- You fill out the form and hand it over so they know what toy to bring.

## 5. Cookies
Cookies are like the little notes your friends leave you when they visit, to remind you of something. When you visit a website, the site can leave you a note in your browser, saying something like “Let’s remember you like the color red for your background.” Next time you visit, the site remembers your preference because of that note (cookie).

**Example:**
- It’s like the toy store leaving you a small note saying, “You liked dinosaur toys” so that the next time you visit, they show you more dinosaur toys.

## 6. Sessions
Sessions are like when the shopkeeper gives you a wristband with a number. While you’re in the store, the shopkeeper knows who you are and keeps helping you, but when you leave the store, the wristband disappears. Sessions make the server remember who you are while you’re browsing, but once you close the browser or the page, that information is lost.

**Example:**
- When you enter a store, they give you a wristband with your number, and while you're inside, the shopkeeper remembers what things you want to buy.
- But when you leave, the wristband goes away and the shopkeeper won’t remember you the next time you come.

---

## Easy Summary:
- **HTTP** is the language used by you and the server to talk.
- **HTML** is the blueprint for the webpage (like building a house).
- **Forms** are like lists where you ask for something (like a letter).
- **Cookies** are notes that websites leave to remember things.
- **Sessions** are like a wristband that helps the server remember you while you're browsing.




### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Essencials-Proxy.md

**Proxy** - is software that sits between a client and a server.

Browser <--------------> Proxy <--------------> Server

A proxy will capture all messages before they travel to their intended recipient. 

Two proxies are particularly popular with bug bounty hunters: 
  - Burp Suite,
  - Zed Attack Proxy (ZAP). 


The **payloads** are the data that you want to insert into specific positions in the request. 

The **payload positions** specify which parts of the request will be replaced by the payloads you choose.



### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Google-Dorking.md

***Don’t recommend Google dorking on a corporate or shared network.***

- **site** 
to search for Python’s *print()* function - `print site:python.org`

- **inurl**
the existence of a page called
*/course/jumpto.php* on a website could indicate that it’s vulnerable - `inurl:"/course/jumpto.php" site:example.com`

- **intitle** - `intitle:"index of" site:example.com`

- **link** researching the uncommon *regular expression denial-of-service (ReDoS)* vulnerability - `link:"https://en.wikipedia.org/wiki/ReDoS"`

- **filetype** searches for pages with a specific file extension, the *.log* file extension - `filetype:log site:example.com`

- **Wildcard (*)** string that starts with *how to hack* and ends with *using Google* - `"how to hack * using Google"`

- **Quotes (" ")** exact match - *phrase* how to hack: `"how to hack"`

- **Or (|)** to search for one search term or the other, or both at the same time. Must be surrounded by spaces - `"how to hack" site:(reddit.com | stackoverflow.com)`

- **Minus (-)** excludes certain search results, *how to hack websites* but not *php* - `"how to hack websites" -php`

*Google search operators*

all of a company’s subdomains - `site:*.example.com`

Special endpoints that can lead to vulnerabilities. *Kibana* is a data visualization tool.
Many *Kibana* dashboards run under the path *app/kibana* - `site:example.com inurl:app/kibana`

Find company resources hosted by a third party online (like *Amazon S3 buckets*) - `site:s3.amazonaws.com COMPANY_NAME`

Look for special extensions. Often used for script files: *.log, .php, .cfm, .asp, .jsp, .pl* - `site:example.com ext:php` or `site:example.com ext:log`

This query searches the site *example.com* for text files that contain *password* - `site:example.com ext:txt password`

**Amazon S3:**
```
site:s3.amazonaws.com COMPANY_NAME
site:amazonaws.com COMPANY_NAME

amazonaws s3 COMPANY_NAME
amazonaws bucket COMPANY_NAME
amazonaws COMPANY_NAME
s3 COMPANY_NAME
```



### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/OSINT-Techniques.md


Check the company’s *job posts* for engineering positions. 

Often reveal the technologies the company uses.

- LinkedIn
- Stack Overflow
- Quora
- the employees’ *Google calendars* (notes, slides, and even login credentials)
- the organization or its employees *social media*
- the company’s *SlideShare* or *Pastebin* accounts

Discovered sets of valid credentials on *Post-it Notes* visible in the *background* of *office selfies*!

**Pastebin** (https://pastebin.com/) is a website for pasting and storing text online for a short time. Search for the target’s organization name.

**PasteHunter** (https://github.com/kevthehermit/PasteHunter/) to scan for publicly pasted data.

**Wayback Machine** (https://archive.org/web/), a digital record of internet content.

**Tomnomnom’s tool Waybackurls** (https://github.com/tomnomnom/waybackurls/) can automatically extract endpoints and URLs from the Wayback Machine.



### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Scope-Discovery.md

## WHOIS and Reverse WHOIS

`$ whois facebook.com` is not always available, as some organizations and individuals use a service called *domain privacy*.

Reverse WHOIS tool like **ViewDNS.info** - https://viewdns.info/reversewhois/

## IP Addresses

Find the IP address of a domain `$ nslookup facebook.com`

**Reverse IP** searches look for domains hosted on the same server, given an IP or domain. You can also use **ViewDNS.info** for this.

`NetRange` field. An *IP range* is a block of IP addresses that all belong to the same organization.

```
$ whois 157.240.2.35
NetRange: 157.240.0.0 - 157.240.255.255
CIDR: 157.240.0.0/16
NetName: THEFA-3 etc..
```

**Autonomous System Numbers (ASNs)** identify the owners of these networks. et. By checking if *two IP addresses* share *an ASN*, 
you can determine whether the IPs belong to the *same owner*.

We can deduce that any IP within the *157.240.2.21* to *157.240.2.34* range probably belongs to *Facebook*:

```
$ whois -h whois.cymru.com 157.240.2.20
AS | IP | AS Name
32934 | 157.240.2.20 | FACEBOOK, US

$ whois -h whois.cymru.com 157.240.2.27
AS | IP | AS Name
32934 | 157.240.2.27 | FACEBOOK, US

$ whois -h whois.cymru.com 157.240.2.35
AS | IP | AS Name
32934 | 157.240.2.35 | FACEBOOK, US
```

The `-h` flag in the `whois` command sets the **WHOIS server** to retrieve information from.

`whois.cymru.com` is a database that translates **IPs** to **ASNs**.

If the company has a dedicated IP range and doesn’t mark those addresses as out of scope, you could plan to attack every IP in that range.

## Certificate Parsing (SSL - Secure Sockets Layer)

Used to **encrypt** web traffic.

An **SSL** certificate’s *Subject Alternative Name* field.

Online databases like **crt.sh** - https://crt.sh/, **Censys**, and **Cert Spotter**.

The **crt.sh** website also has a useful utility that lets you retrieve the information in **JSON** format:
`https://crt.sh/?q=facebook.com&output=json`

<img width="558" height="661" alt="image" src="https://github.com/user-attachments/assets/cb2a0ba8-4e1f-4a9f-9799-fd2842ec1068" />

## Subdomain Enumeration

**Sublist3r**, **SubBrute**, **Amass**, and **Gobuster** can enumerate subdomains automatically.

Daniel Miessler’s *SecLists* at https://github.com/danielmiessler/SecLists/. 

**Commonspeak2** (https://github.com/assetnote/commonspeak2/) to generate wordlists based on the most current internet data.

Command to **remove duplicate** items from a set of two wordlists:
`sort -u wordlist1.txt wordlist2.txt`

`-u` - to return only **unique** items in the sorted list.

### Gobuster is a tool for brute-forcing.

 `-d` to specify the domain, `-w` to specify the wordlist

 ```gobuster dns -d target_domain -w wordlist```

**Altdns** (https://github.com/infosec-au/altdns/) - automating which discovers subdomains with names that are permutations of other subdomain names.

For example, if you’ve already learned that *example.com* uses **Jenkins**, you can check if *jenkins.example.com* is a valid subdomain.

Look for **subdomains** of **subdomains**: *dev.example.com*, you might find subdomains like *1.dev.example.com*.

Running enumeration tools recursively: **add the results** of your first run to your Known Domains list and **run the tool again**.


## Service Enumeration

- In *active scanning*, you **directly** engage with the *server*.

Tools like **Nmap** or **Masscan**

Reveals the **open ports** on *scanme.nmap.org* (target):

```$ nmap scanme.nmap.org```

- In *passive scanning*, you use third-party resources **without** interacting with the *server*.

 Is **stealthier** and helps attackers **avoid detection**.

**Censys**, **Project Sonar**, **Shodan** - a search engine that lets the user find machines connected to the internet.

If you run a **Shodan** search on *scanme.nmap.org*’s IP address, *45.33.32.156*, you get the result:

<img width="1890" height="711" alt="image" src="https://github.com/user-attachments/assets/a003c79d-fd6b-49e1-93db-e5275e8b6714" />

and provides *additional information* about the server.

## Directory Brute-Forcing

Directory brute-forcing can sometimes allow you to **directly take over a server**!

For example, a pathname that includes `phpmyadmin` usually means that the application is built with `PHP`.

**Dirsearch** or **Gobuster** use wordlists to construct URLs, and then request these URLs from a web server.

If the server responds with a **status code** in the `200` range, the directory or file **exists**. 

Examine `403` pages carefully to see if you can bypass the **protection to access** the content.

`-u` - specifies **the hostname** and `-e` - specifies **the file extension** to use when constructing URLs:

```$ ./dirsearch.py -u scanme.nmap.org -e php``` or

```$ dirsearch -u scanme.nmap.org -e php``` (for install `sudo apt install dirsearch`).

**Gobuster’s** `dir` mode is used to find additional content.

```gobuster dir -u target_url -w wordlist```

Manually visiting all the pages can be time-consuming. 

Instead, use a screenshot tool like:
- **EyeWitness** (https://github.com/FortyNorthSecurity/EyeWitness/) or
- **Snapper** (https://github.com/dxa4481/Snapper/) to automatically verify that a page is hosted on each location. 

*EyeWitness* accepts a list of URLs and takes screenshots of each page. In a photo gallery app, you can quickly skim these to find the interesting-looking
ones. Keep an eye out for hidden services, such as developer or admin panels, directory listing pages, analytics pages, and pages that look outdated and illmaintained. These are all **common places for vulnerabilities** to manifest.

## Spidering the Site

Identifies all the *URLs embedded* on the page and visits them.

**OWASP Zed Attack Proxy (ZAP)** at https://www.zaproxy.org/

Tools -> Spider -> [specifying the starting URL] -> Start Scan

*Burp Suite* has an equivalent tool called *the crawler*.

## Third-Party Hosting

**S3** - *Simple Storage Service*, is **Amazon’s** online storage.

- **Buckets** to serve in their *web applications*, or
- can use **S3 buckets** as a *backup* or *storage*.

URL format: 
`BUCKET.s3.amazonaws.com` or `s3.amazonaws.com/BUCKET`.

Google Dorking:

```
site:s3.amazonaws.com COMPANY_NAME
site:amazonaws.com COMPANY_NAME

amazonaws s3 COMPANY_NAME
amazonaws bucket COMPANY_NAME
amazonaws COMPANY_NAME
s3 COMPANY_NAME
```

**GrayhatWarfare** (https://buckets.grayhatwarfare.com/) is an online search to find publicly *exposed S3 buckets*.

**Lazys3** (https://github.com/nahamsec/lazys3/) try to *brute-force buckets* by using *keywords*.

**Bucket Stream** (https://github.com/eth0izzle/bucket-stream/)

### Buckets 

that belong to the target organization, use the AWS command line tool to see if you can access one.

`pip install awscli`

Configure it to work with AWS by following Amazon’s documentation at https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html.

Now able to access buckets directly from your terminal via the aws s3 command:

`aws s3 ls s3://BUCKET_NAME/`

If this works, can read the contents and copying files to your local machine:

`aws s3 cp s3://BUCKET_NAME/FILE_NAME/path/to/local/directory`

You can also try *to upload* new files to the bucket or *delete* files from it. 

For example, *will copy* your local file named TEST_FILE into the *target’s S3 bucket*:

`aws s3 cp TEST_FILE s3://BUCKET_NAME/`

And this command *will remove* the TEST_FILE that you just uploaded:

`aws s3 rm s3://BUCKET_NAME/TEST_FILE`

## GitHub Recon

Search an organization’s **GitHub** repositories for sensitive data.

- The **organization’s name** or
- **product names** via GitHub’s search bar, or
- the GitHub **accounts** of known **employees**.

Dive into the code. Special attention to the `Issues` and `Commits` sections.

`Code` section for potentially vulnerable code *snippets*. 

Check the `Blame` and `History` sections at the *top-right corner* of the file’s page to see.

<img width="350" height="160" alt="image" src="https://github.com/user-attachments/assets/839f9aaf-b902-4497-90b5-a586f2cab6b6" />


- API keys,
- encryption keys, and
- database passwords.

Terms like `key`, `secret`, `password`. 

After, you can use **KeyHacks** (https://github.com/streaak/keyhacks/) to check if the credentials are valid and learn how to use them to access the target’s services.

Automate the GitHub recon:
- **Gitrob** (https://github.com/michenriksen/gitrob/) locates potentially sensitive files pushed to public repositories on GitHub,
- **TruffleHog** (https://github.com/trufflesecurity/truffleHog/) specializes in finding secrets (by regex searches and scanning for high-entropy strings).



### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Tech-Stack-Fingerprinting.md

**Common Vulnerabilities and Exposures (CVEs)**

Gives each CVE a number for reference, database (https://cve.mitre.org/cve/search_cve_list.html).

`$ nmap scanme.nmap.org -sV`

Next, in *Burp*, send an **HTTP request** to the server: Send to Repeater -> Send (then see Response):

```
Server: Apache/2.0.6 (Ubuntu)
X-Powered-By: PHP/5.0.1
X-Generator: Drupal 8
X-Drupal-Dynamic-Cache: UNCACHEABLE
Set-Cookie: PHPSESSID=abcde;
```
Cookie named `PHPSESSID`, it’s probably developed using `PHP`.

Right-click a page, select *View Source Code*, and press **CTRL-F** to search for *phrases* like `powered by`, `built with`, and `running`. 
For instance, you might find `Powered by: WordPress 3.3.2` written in the source.

`phpmyadmin` at the root directory, like `https://example.com/phpmyadmin`, means the application runs `PHP`.

A directory named `jinja2` that contains templates, probably uses `Django` and `Jinja2`.

- **Wappalyzer** (https://www.wappalyzer.com/) a browser extension,
- **BuiltWith** (https://builtwith.com/) a website that shows you which web technologiesa site is built with,
- **StackShare** (https://stackshare.io/) is an online platform that allows developers to share the tech they use,
- **Retire.js** is a tool that detects *outdated* `JavaScript` libraries and `Node.js` packages.




### File: Bug-Bounty-Journey/Phase-1-Setup-and-Foundations/assests/Writing-Your-Own-Recon-Scripts.md

The first line of every shell script you write should be *the shebang line*.

It starts with `#!`

### Scan only `scanme.nmap.org`:
```
#!/bin/bash
nmap scanme.nmap.org
/PATH/TO/dirsearch.py -u scanme.nmap.org -e php
```

- `$1` the first argument passed in,
- `$2` is the second argument, and so on.
- `$@` represents all arguments passed in, while
- `$#` represents the total number of arguments.

### Scan for `whatever domain`:
```
#!/bin/bash
nmap $1
/PATH/TO/dirsearch.py -u $1 -e php
```

`PATH` variable, an environmental variable in *Unix systems* that specifies where executable binaries are found.

If you run this command to add `Dirsearch’s` directory to your `PATH`, you can run the tool *from anywhere* without needing to specify its absolute path:
```
export PATH="PATH_TO_DIRSEARCH:$PATH"
```

After executing this command, you should be able to use `Dirsearch` directly:
```
#!/bin/bash
nmap $1
dirsearch.py -u $1 -e php
```

Will have to run the `export` command again after you *restart* your terminal for your `PATH` to contain the path to `Dirsearch`. 

You can add the `export` command to your `~/.bash_profile` file, a file that stores *your bash preferences* and *configuration*. 

Opening `~/.bash_profile` with text editor and adding the `export` command *to the bottom* of the file. 

Save the script in your current directory with the filename `recon.sh`

- `.sh` extension for shell scripts.

Execute the script in the terminal: `$ ./recon.sh`

Adding executing rights for everyone by running in the terminal: `$ chmod +x recon.sh`

Or  for the owner of the script only: `$ chmod 700 recon.sh`

### Run the script, try passing in `scanme.nmap.org` as the first argument:
```
$ ./recon.sh scanme.nmap.org
```

## Saving Tool Output to a File

- *Input redirection* is using the content of a file, or the output of another program, as the input to your script.
- *Output redirection* is redirecting the output of a program to another location, such as to a file or another program.

### The most useful redirection operators:

- `PROGRAM > FILENAME` writes the program’s output *into the file* with that name (it *will clear* any content from the file first, also *create* the file if the file does not already exist);

- `PROGRAM >> FILENAME` appends the output of the program *to the end* of the file, *without clearing* the file’s original content;

- `PROGRAM < FILENAME` *reads* from the file and uses its content as the program input;

- `PROGRAM1 | PROGRAM2` uses the *output* of `PROGRAM1` as the *input* to `PROGRAM2`.

### Write the results of the `nmap` and `dirsearch` scans into different files:
```
#!/bin/bash
echo "Creating directory $1_recon."
mkdir $1_recon
nmap $1 > $1_recon/nmap
echo "The results of nmap scan are stored in $1_recon/nmap."
/PATH/TO/dirsearch.py -u $1 -e php --simple-report=$1_recon/dirsearch
echo "The results of dirsearch scan are stored in $1_recon/dirsearch."
```
- `echo` prints a message to the terminal.
- `mkdir` creates a directory with the name `DOMAIN_recon`
- store the results of `nmap` into a *file* named `nmap` in the newly created directory.
- dirsearch’s `simple-report` flag generates a report in the designated location. Store the results of `dirsearch` to a file named *dirsearch* in the new directory.

### Variables in *bash* can be assigned using the syntax (no spaces around the `=` sign):
```
VARIABLE_NAME=VARIABLE_VALUE
```
### The syntax for referencing variables:
```
$VARIABLE_NAME
```

```
#!/bin/bash
PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon
echo "Creating directory $DIRECTORY."
mkdir $DIRECTORY
nmap $DOMAIN > $DIRECTORY/nmap
echo "The results of nmap scan are stored in $DIRECTORY/nmap."
$PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php –simple-report=$DIRECTORY/dirsearch
echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
```
- use `${DOMAIN}_recon` instead of `$DOMAIN_recon` bash would recognize the entirety of `DOMAIN_recon` as the variable name (the `{}` tell).
- we also stored the `$PATH_TO_DIRSEARCH` in *a variable* (to make it easy to change in the future).

## Adding the `Date` of the Scan to the Output:

*Command substitution*, or operating on the output of a command. 

- `$()` tells Unix to execute the command surrounded by the parentheses and assign its output to the value of a variable.
```
#!/bin/bash
PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
TODAY=$(date)
echo "This scan was created on $TODAY"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon
echo "Creating directory $DIRECTORY."
mkdir $DIRECTORY
nmap $DOMAIN > $DIRECTORY/nmap
echo "The results of nmap scan are stored in $DIRECTORY/nmap."
$PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
```
- `TODAY=$(date)` assign the output of the `date` command to the variable `TODAY`
- `echo "This scan was created on $TODAY"` this lets us output a message indicating the *day* on which we performed the scan.

## Adding `Options` to Choose the Tools to Run:
### Conditionals in bash, the syntax of an `if` statement, the conditional statement ends with the `fi` keyword:
```
if [condition 1]
then
 # Do if condition 1 is satisfied
elif [condition 2]
then
 # Do if condition 2 is satisfied, and condition 1 is not satisfied
else
 # Do something else if neither condition is satisfied
fi
```

To be able to specify the scan `MODE`: `$ ./recon.sh scanmme.nmap.org MODE`.

```
#!/bin/bash
PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
TODAY=$(date)
echo "This scan was created on $TODAY"
DIRECTORY=${DOMAIN}_recon
echo "Creating directory $DIRECTORY."
mkdir $DIRECTORY
if [ $2 == "nmap-only" ]
then
 nmap $DOMAIN > $DIRECTORY/nmap
 echo "The results of nmap scan are stored in $DIRECTORY/nmap."
elif [ $2 == "dirsearch-only" ]
then
 $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php –simple-report=$DIRECTORY/dirsearch
 echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
else
 nmap $DOMAIN > $DIRECTORY/nmap
 echo "The results of nmap scan are stored in $DIRECTORY/nmap."
 $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
 echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
fi
```

- `"nmap-only"` run `nmap` only and store the results to a file named *nmap*.
- `"dirsearch-only"` execute and store the results of `dirsearch` only.
- if the user specifies neither - `else` - run both scans - `nmap $DOMAIN > $DIRECTORY/nmap`.

### Can make your tool run only the `nmap` or `dirsearch` commands by specifying one of these:
```
$ ./recon.sh scanme.nmap.org nmap-only
$ ./recon.sh scanme.nmap.org dirsearch-only
```

## Running Additional Tools
### For example, you want to switch between these three modes or run all three recon tools at once:
```
$ ./recon.sh scanme.nmap.org nmap-only
$ ./recon.sh scanme.nmap.org dirsearch-only
$ ./recon.sh scanme.nmap.org crt-only
```

The syntax of `case` statements (without a long list of `if-else`). Note that the statement ends with `esac` (`case` backward):
```
case $VARIABLE_NAME in
 case1)
  Do something
  ;;
 case2)
  Do something
  ;;
 caseN)
  Do something
  ;;
 *)
  Default case, this case is executed if no other case matches.
  ;;
esac
```

### Improve our script with `case` (instead of multiple `if-else`):
```
#!/bin/bash
PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
TODAY=$(date)
echo "This scan was created on $TODAY"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon
echo "Creating directory $DIRECTORY."
mkdir $DIRECTORY
case $2 in
 nmap-only)
  nmap $DOMAIN > $DIRECTORY/nmap
  echo "The results of nmap scan are stored in $DIRECTORY/nmap."
  ;;
 dirsearch-only)
  $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
  echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
  ;;
 crt-only)
  curl "https://crt.sh/?q=$DOMAIN&output=json" -o $DIRECTORY/crt
  echo "The results of cert parsing is stored in $DIRECTORY/crt."
  ;;
 *)
  nmap $DOMAIN > $DIRECTORY/nmap
  echo "The results of nmap scan are stored in $DIRECTORY/nmap."
  $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
  echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
  curl "https://crt.sh/?q=$DOMAIN&output=json" -o $DIRECTORY/crt
  echo "The results of cert parsing is stored in $DIRECTORY/crt."
  ;;
esac
```
- the `curl` command downloads the content of a page.
- `-o` option lets you specify an output file.

### The syntax of a bash `function`:
```
FUNCTION_NAME()
{
 DO_SOMETHING
}
```

Let’s add `functions` to the script:
```
#!/bin/bash
PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
TODAY=$(date)
echo "This scan was created on $TODAY"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon
echo "Creating directory $DIRECTORY."
mkdir $DIRECTORY
nmap_scan()
{
  nmap $DOMAIN > $DIRECTORY/nmap
  echo "The results of nmap scan are stored in $DIRECTORY/nmap."
}
dirsearch_scan()
{
  $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
  echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
}
crt_scan()
{
  curl "https://crt.sh/?q=$DOMAIN&output=json" -o $DIRECTORY/crt
  echo "The results of cert parsing is stored in $DIRECTORY/crt."
}
case $2 in
 nmap-only)
  nmap_scan
  ;;
 dirsearch-only)
  dirsearch_scan
  ;;
 crt-only)
  crt_scan
  ;;
 *)
  nmap_scan
  dirsearch_scan
  crt_scan
  ;;
esac
```

We created three functions:
- `nmap_scan`,
- `dirsearch_scan`, and
- `crt_scan`

We put the `scan` and `echo` commands in these functions so we can call them repeatedly without writing the same code over and over.

All bash variables are *GLOBAL except* for input parameters like `$1`, `$2`, and `$3`.

Values like `$1`, `$2`, and `$3` can refer only to the values the function is called with, so you can’t use a script’s input arguments within a function, like this:
```
nmap_scan()
{
  nmap $1 > $DIRECTORY/nmap
  echo "The results of nmap scan are stored in $DIRECTORY/nmap."
}
nmap_scan
```
Here:
- the `$1` in the function refers to the first argument that `nmap_scan` was called with, not the argument our `recon.sh` script was called with. Since
`nmap_scan` wasn’t called with any arguments, `$1` is blank.

## Parsing the Results

*Global Regular Expression Print (`grep`)* to search for a certain piece of information in the output files.
```
grep password file.txt
```
- to search for the string `password`
- in the file `file.txt`

Search the `nmap` output file to see if the target has `port 80` open:
```
$ grep 80 TARGET_DIRECTORY/nmap
80/tcp open http
```

###  A *regular expression*, or `regex`
Is a special string that describes a search pattern.

For example, the output of the `nmap` command looks like this:
```
Starting Nmap 7.60 ( https://nmap.org )
Nmap scan report for scanme.nmap.org (45.33.32.156)
Host is up (0.065s latency).
Other addresses for scanme.nmap.org (not scanned): 2600:3c01::f03c:91ff:fe18:bb2f
Not shown: 992 closed ports
PORT STATE SERVICE
22/tcp open ssh
25/tcp filtered smtp
80/tcp open http
135/tcp filtered msrpc
139/tcp filtered netbios-ssn
445/tcp filtered microsoft-ds
9929/tcp open nping-echo
31337/tcp open Elite
Nmap done: 1 IP address (1 host up) scanned in 2.43 seconds
```

You might want *to trim* the irrelevant messages from the file so it looks more like this:
```
PORT STATE SERVICE
22/tcp open ssh
25/tcp filtered smtp
80/tcp open http
135/tcp filtered msrpc
139/tcp filtered netbios-ssn
445/tcp filtered microsoft-ds
9929/tcp open nping-echo
31337/tcp open Elite
```
↑
Command *to filter out* the messages at the **start** and **end** of `nmap`’s output and keep only the essential part of the report:
```
grep -E "^\S+\s+\S+\s+\S+$" DIRECTORY/nmap > DIRECTORY/nmap_cleaned
```
- `-E` flag tells `grep` you’re using a regex,
- `\s+` would match any whitespace one or more characters long,
- `\S+` would match any non-whitespace one or more characters long,
- `"^\S+\s+\S+\s+\S+$"` specifies that we should extract lines that contain three strings separated by two whitespaces.

To account for *extra whitespaces* that might be in the command output, let’s *add two more* optional spaces around our search string:
```
"^\s*\S+\s+\S+\s+\S+\s*$"
```

A `regex` consists of two parts:
- *Constants* are sets of strings, while
- *Operators* are symbols that denote operations over these strings.

### `Regex` operators that represent *characters*:
- `\d` matches any digit,
- `\w` matches any character,
- `\s` matches any whitespace, and
- `\S` matches any non-whitespace,
- `.` matches with any single character,
- `\` escapes a special character,
- `^` matches the start of the string or line,
- `$` matches the end of the string or line.

Specify the *number* of characters to match:
- `*` matches the preceding character zero or more times,
- `+` matches the preceding character one or more times,
- `{3}` matches the preceding character three times,
- `{1, 3}` matches the preceding character one to three times,
- `{1, }` matches the preceding character one or more times,
- `[abc]` matches one of the characters within the brackets,
- `[a-z]` matches one of the characters within the range of *a* to *z*,
- `(a|b|c)` matches either *a* or *b* or *c*.

#### Regex syntax - RexEgg’s cheat sheet - https://www.rexegg.com/regex-quickstart.html

## Building a Master Report

- `jq` a command line utility that processes `JSON`.

If we examine the `JSON` output file from `crt.sh`, we need to extract the `name_value` field of each certificate item to extract domain names:
```
$ jq -r ".[] | .name_value" $DOMAIN/crt
```
- `-r` flag tells `jq` to write the output directly to standard output rather than format it as `JSON` strings,
- `.[]` iterates through the array within the `JSON` file, and
- `.name_value` extracts the `name_value` field of each item,
- `$DOMAIN/crt` is the input file to the `jq` command.

#### How `jq` works - https://stedolan.github.io/jq/manual/

To combine all output files into a master report:
```
#!/bin/bash
PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
DOMAIN=$1
DIRECTORY=${DOMAIN}_recon
echo "Creating directory $DIRECTORY."
mkdir $DIRECTORY
nmap_scan()
{
  nmap $DOMAIN > $DIRECTORY/nmap
  echo "The results of nmap scan are stored in $DIRECTORY/nmap."
}
dirsearch_scan()
{
  $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
  echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
}
crt_scan()
{
  curl "https://crt.sh/?q=$DOMAIN&output=json" -o $DIRECTORY/crt
  echo "The results of cert parsing is stored in $DIRECTORY/crt."
}
case $2 in
 nmap-only)
  nmap_scan
  ;;
 dirsearch-only)
  dirsearch_scan
  ;;
 crt-only)
  crt_scan
  ;;
 *)
  nmap_scan
  dirsearch_scan
  crt_scan
  ;;
esac
echo "Generating recon report from output files..."
TODAY=$(date)
echo "This scan was created on $TODAY" > $DIRECTORY/report
echo "Results for Nmap:" >> $DIRECTORY/report
grep -E "^\s*\S+\s+\S+\s+\S+\s*$" $DIRECTORY/nmap >> $DIRECTORY/report
echo "Results for Dirsearch:" >> $DIRECTORY/report
cat $DIRECTORY/dirsearch >> $DIRECTORY/report
echo "Results for crt.sh:" >> $DIRECTORY/report
jq -r ".[] | .name_value" $DIRECTORY/crt >> $DIRECTORY/report
```

- `$DIRECTORY/report` create a new file named `report` and write today’s date into it,
- `$DIRECTORY/nmap >> $DIRECTORY/report` append the results of the `nmap` and `dirsearch` commands into the `report` file,
- `cat $DIRECTORY/dirsearch >> $DIRECTORY/report`. The `cat` command prints the contents of a file to standard output, but we can also use it to redirect the content of the file into another file,
- `echo "Results for crt.sh:" >> $DIRECTORY/report` and `jq -r ".[] | .name_value" $DIRECTORY/crt >> $DIRECTORY/report` extract domain names from the `crt.sh` report and append it to the end of the `report` file.

## Scanning Multiple Domains

To write a tool that can scan *multiple domains* with a single command, like this:
```
./recon.sh facebook.com fbcdn.net nmap-only
```
The `getopts` tool parses options from the command line by using singlecharacter flags.

*OPTSTRING* specifies the option letters that `getopts` should recognize:
  -  if it should recognize the options `-m` and `-i`, you should specify `mi`,
  -  if you want an option to contain argument values, the letter should be followed by a colon, like `m:i`.

*NAME* argument specifies the variable name that stores the option letter. 
```
getopts OPTSTRING NAME
```

The `getopts` tool also automatically stores the value of any options into the `$OPTARG` variable. We can store that value into a variable named `MODE`:
```
getopts "m:" OPTION
MODE=$OPTARG
```
- `-m` flag to specify the scan mode and assume that all other arguments are domains.

#### `getopts` stops parsing arguments when it encounters an argument that doesn’t start with the - character.
So you’ll need to place the scan mode *before* the domain arguments:
```
./recon.sh -m nmap-only facebook.com fbcdn.net
```

### Loop

Bash has two types of loops:
- `for` - works better for our purposes, as we already know the number of values we are looping through (you already have a list of values to iterate through),
- `while` - when you’re not sure how many values to loop through but want to specify the condition in which the execution should stop.

Syntax of a `for`, for every item in *LIST_OF_VALUES*, bash will execute the code between `do` and `done` once:
```
for i in LIST_OF_VALUES
do
 DO SOMETHING
done
```

Now let’s implement our functionality:
```
for i in "${@:$OPTIND:$#}"
do
 # Do the scans for $i
done
```

- `"${@:$OPTIND:$#}"` that contains every command line argument, besides the ones that are already parsed by `getopts`, which stores the index of the first argument after the options it parses into a variable named `$OPTIND`,
- `"${@:OPTIND:}"` slices the array so that it removes the *MODE* argument (like `nmap-only`) making sure that we iterate through only the domains part of our input,
- `$@` represent the array containing all input arguments,
- `$#` is the number of command line arguments passed in,
- `$i` variable represents the current item in the argument array.

In bash, you can *slice arrays* by using this syntax:
```
"${INPUT_ARRAY:START_INDEX:END_INDEX}"
```

We can then wrap the loop around the code:
```
#!/bin/bash
PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
nmap_scan()
{
  nmap $DOMAIN > $DIRECTORY/nmap
  echo "The results of nmap scan are stored in $DIRECTORY/nmap."
}
dirsearch_scan()
{
  $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
  echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
}
crt_scan()
{
 curl "https://crt.sh/?q=$DOMAIN&output=json" -o $DIRECTORY/crt
 echo "The results of cert parsing is stored in $DIRECTORY/crt."
}
getopts "m:" OPTION
MODE=$OPTARG

for i in "${@:$OPTIND:$#}"
do

 DOMAIN=$i
 DIRECTORY=${DOMAIN}_recon
 echo "Creating directory $DIRECTORY."
 mkdir $DIRECTORY

 case $MODE in
  nmap-only)
   nmap_scan
   ;;
  dirsearch-only)
   dirsearch_scan
   ;;
  crt-only)
   crt_scan
   ;;
  *)
   nmap_scan
   dirsearch_scan
   crt_scan
   ;;
 esac
 echo "Generating recon report for $DOMAIN..."
 TODAY=$(date)
 echo "This scan was created on $TODAY" > $DIRECTORY/report
  if [ -f $DIRECTORY/nmap ];then
  echo "Results for Nmap:" >> $DIRECTORY/report
  grep -E "^\s*\S+\s+\S+\s+\S+\s*$" $DIRECTORY/nmap >> $DIRECTORY/report
 fi
  if [ -f $DIRECTORY/dirsearch ];then
  echo "Results for Dirsearch:" >> $DIRECTORY/report
  cat $DIRECTORY/dirsearch >> $DIRECTORY/report
 fi
  if [ -f $DIRECTORY/crt ];then
  echo "Results for crt.sh:" >> $DIRECTORY/report
  jq -r ".[] | .name_value" $DIRECTORY/crt >> $DIRECTORY/report
 fi
 done
```
- loop starts with the `for` keyword and ends with the `done` keyword,
- we check whether the output file of an `nmap` scan (`if [ -f $DIRECTORY/nmap ];then`), a `dirsearch` scan (`if [ -f $DIRECTORY/dirsearch ];then`), or a `crt.sh` scan (`if [ -f $DIRECTORY/crt ];then`) exist so we can determine if we need to generate a report for that scan type.

The brackets `[]` mean that we’re passing the contents into a test command: 
- `[ -f $DIRECTORY/nmap ]` is equivalent to `test -f $DIRECTORY/nmap`. The `test` command evaluates a conditional and outputs either `true` or `false`.
- `-f` flag tests whether a file exists.

Some useful test conditions:
- `-eq` and `-ne` flags test for *equality* and *inequality*, respectively.

This returns `true` if `$3` is *equal* to `1`:
```
if [ $3 -eq 1 ]
```

This returns `true` if `$3` is *not equal* to `1`:
```
if [ $3 -ne 1 ]
```
- `if [ $3 -gt 1 ]` - test for greater than,
- `if [ $3 -ge 1 ]` - test for greater than or equal to,
- `if [ $3 -lt 1 ]` - test for less than,
- `if [ $3 -le 1 ]` - test for less than or equal to,
- `if [ -z "" ]` and `if [ -n "abc" ]` - test whether a string is empty. These conditions are both true.

The `-d`, `-f`, `-r`, `-w`, and `-x` flags check for directory and file statuses. 

- `if [ -d /bin]` - returns `true` if `/bin` is a *directory* that exists,
- `if [ -f /bin/bash ]` - returns `true` if `/bin/bash` is a *file* that exists,
- `if [ -r /bin/bash ]` - returns `true` if `/bin/bash` is a *readable* file,
- `if [ -w /bin/bash ]` - or a *writable* file,
- `if [ -x /bin/bash ]` - or an *executable* file.

You can also use `&&` and `||` to combine test expressions. 
- `if [ $3 -gt 1 ] && [ $3 -lt 3 ]` - returns `true` if *both* expressions are `true`,
- `if [ $3 -gt 1 ] || [ $3 -lt 0 ]` - returns `true` if *at least one of them* is `true`.

Find more comparison flags in the `test` command’s manual by running `man test` (you can always enter `man` followed by the command name).

## Writing a Function Library

As your codebase gets larger, you should writing a *function library* to *reuse code*. 

We can store all the commonly used functions in a separate file `scan.lib`. 

We can call these functions as needed for future recon tasks:
```
#!/bin/bash
nmap_scan()
{
  nmap $DOMAIN > $DIRECTORY/nmap
  echo "The results of nmap scan are stored in $DIRECTORY/nmap."
}
dirsearch_scan()
{
  $PATH_TO_DIRSEARCH/dirsearch.py -u $DOMAIN -e php --simple-report=$DIRECTORY/dirsearch
  echo "The results of dirsearch scan are stored in $DIRECTORY/dirsearch."
}
crt_scan()
{
  curl "https://crt.sh/?q=$DOMAIN&output=json" -o $DIRECTORY/crt
  echo "The results of cert parsing is stored in $DIRECTORY/crt."
}
```

We source a script via the `source` command, followed by the path to the script:
```
#!/bin/bash
source ./scan.lib
PATH_TO_DIRSEARCH="/Users/vickieli/tools/dirsearch"
getopts "m:" OPTION
MODE=$OPTARG
for i in "${@:$OPTIND:$#}"
do
 DOMAIN=$i
 DIRECTORY=${DOMAIN}_recon
 echo "Creating directory $DIRECTORY."
 mkdir $DIRECTORY
 case $MODE in
  nmap-only)
   nmap_scan
   ;;
  dirsearch-only)
   dirsearch_scan
   ;;
  crt-only)
   crt_scan
   ;;
  *)
   nmap_scan
   dirsearch_scan
   crt_scan
   ;;
 esac
 echo "Generating recon report for $DOMAIN..."
 TODAY=$(date)
 echo "This scan was created on $TODAY" > $DIRECTORY/report
 if [ -f $DIRECTORY/nmap ];then
   echo "Results for Nmap:" >> $DIRECTORY/report
   grep -E "^\s*\S+\s+\S+\s+\S+\s*$" $DIRECTORY/nmap >> $DIRECTORY/report
 fi
 if [ -f $DIRECTORY/dirsearch ];then
   echo "Results for Dirsearch:" >> $DIRECTORY/report
   cat $DIRECTORY/dirsearch >> $DIRECTORY/report
 fi
 if [ -f $DIRECTORY/crt ];then
   echo "Results for crt.sh:" >> $DIRECTORY/report
   jq -r ".[] | .name_value" $DIRECTORY/crt >> $DIRECTORY/report
 fi
done
```

## Building Interactive Programs

Takes user input during execution; if users enter the command line option, `-i`, you want to enter an interactive mode that allows you to specify
domains to scan as you go:
```
./recon.sh -i -m nmap-only
```

For that, you can use `read`. This command reads user input and stores the input string into a variable:
```
echo "Please enter a domain!"
read $DOMAIN
```
These commands will prompt the user to enter a domain, then store the input inside a variable named `$DOMAIN`.

To prompt a user repeatedly, we need to use a `while` loop.
As long as the *CONDITION* is true, the `while` loop will execute the code between do and done *repeatedly*:
```
while CONDITION
do
 DO SOMETHING
done
```

We can use a `while` loop, until the user enters `quit`:
```
while [ $INPUT != "quit" ];do
 echo "Please enter a domain!"
 read INPUT
 if [ $INPUT != "quit" ];then
  scan_domain $INPUT
  report_domain $INPUT
 fi
done
```

We can use a `while` loop to parse options by using `getopts` repeatedly and invoke the `-i` option:
```
while getopts "m:i" OPTION; do
 case $OPTION in
  m)
    MODE=$OPTARG
    ;;
  i)
    INTERACTIVE=true
    ;;
 esac
done
```

Here, we specify a `while` loop that gets command line options repeatedly:
- If the option flag is `-m`, we set the `MODE` variable to the scan mode that the user has specified.
- If the option flag is `-i`, we set the `$INTERACTIVE` variable to *true*.

Then, later in the script, we can decide whether to invoke the interactive mode by checking the value of the `$INTERACTIVE` variable. 

Putting it all together, we get our final script:
```
#!/bin/bash
source ./scan.lib

while getopts "m:i" OPTION; do
 case $OPTION in
  m)
    MODE=$OPTARG
    ;;
  i)
    INTERACTIVE=true
    ;;
 esac
done

scan_domain(){
 DOMAIN=$1
 DIRECTORY=${DOMAIN}_recon
 echo "Creating directory $DIRECTORY."
 mkdir $DIRECTORY
 case $MODE in
  nmap-only)
   nmap_scan
   ;;
  dirsearch-only)
   dirsearch_scan
   ;;
  crt-only)
   crt_scan
   ;;
  *)
   nmap_scan
   dirsearch_scan
   crt_scan
   ;;
 esac
}
report_domain(){
  DOMAIN=$1
  DIRECTORY=${DOMAIN}_recon
  echo "Generating recon report for $DOMAIN..."
 TODAY=$(date)
  echo "This scan was created on $TODAY" > $DIRECTORY/report
  if [ -f $DIRECTORY/nmap ];then
   echo "Results for Nmap:" >> $DIRECTORY/report
   grep -E "^\s*\S+\s+\S+\s+\S+\s*$" $DIRECTORY/nmap >> $DIRECTORY/report
  fi
  if [ -f $DIRECTORY/dirsearch ];then
   echo "Results for Dirsearch:" >> $DIRECTORY/report
   cat $DIRECTORY/dirsearch >> $DIRECTORY/report
  fi
  if [ -f $DIRECTORY/crt ];then
   echo "Results for crt.sh:" >> $DIRECTORY/report
   jq -r ".[] | .name_value" $DIRECTORY/crt >> $DIRECTORY/report
  fi
}
if [ $INTERACTIVE ];then
  INPUT="BLANK"
  while [ $INPUT != "quit" ];do
   echo "Please enter a domain!"
   read INPUT
   if [ $INPUT != "quit" ];then
    scan_domain $INPUT
    report_domain $INPUT
   fi
  done
else
  for i in "${@:$OPTIND:$#}";do
   scan_domain $i
   report_domain $i

  done
fi
```
- `if [ $INTERACTIVE ];then` we first check if the user has selected the interactive mode by specifying the `-i` option,
- `while [ $INPUT != "quit" ];do` then repeatedly prompt the user for a domain by using a `while` loop,
- `if [ $INPUT != "quit" ];then` the `while` loop will continue to run and ask the user for domains until the user enters `quit`, which will cause the `while` loop
to exit and the program to terminate.

## Using Special Variables and Characters

In Unix, commands return `0` on *success* a `positive integer` on *failure*.

- `$?` contains the exit value of the last command executed.

```
#!/bin/sh
chmod 777 script.sh
if [ "$?" -ne "0" ]; then
 echo "Chmod failed. You might not have permissions to do that!"
fi
```

- `$$` which contains the current process’s ID (is useful when you need to create temporary files for the script).

You can create temporary files named `/tmp/script_name_$$` for every one of scripts.

If you want other programs to use the variable as well, you need to *export* the variable:
```
export VARIABLE_NAME=VARIABLE_VALUE
```

Let’s say that in one of your scripts you set the variable *VAR*:
```
VAR="Hello!"
```

If you export *VAR* in the first script and run that script *before* running a second script, the second script will be able to read *VAR’s* value.

- In Unix, the wildcard character `*` stands for *all*.

This command will print out *all the filenames* in the *current directory* that have the file extension `.txt`:
```
$ ls *.txt
```

- Backticks (`) indicate *command substitution*. You can use both backticks and the $() command substitution syntax mentioned earlier for the same purpose. 

This `echo` command will print the output of the `whoami` command:
```
echo `whoami`
```

- Most special characters, aren’t interpreted as special when they are placed in double quotes (" ").

Instead, they’re treated as part of a string:
```
$ echo "abc '*' 123"
```

- The backslash (\), the escape character in bash. It tells bash that a certain character should be interpreted *literally*, and not as a special character.

- Certain special characters, remain special even within double quotes (" "), so to treat them literally, using a backslash:
```
$ echo "\" is a double quote. \$ is a dollar sign. \` is a backtick. \\ is a backslash."
```
This command will `echo`:
```
" is a double quote. $ is a dollar sign. ` is a backtick. \ is a backslash.
```

You can also use a backslash before a newline to indicate that the line of code has not ended:
```
chmod 777 \
script.sh
```
is the same as this `chmod 777 script.sh`

#### Set up a directory of scripts and sort your scripts by their *functionality*.


## Scheduling Automatic Scans pag.128

