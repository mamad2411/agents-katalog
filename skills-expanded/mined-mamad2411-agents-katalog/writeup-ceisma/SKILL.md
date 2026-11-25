<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-ceisma
description: CTF writeups and security challenges by ceisma.
---

# Writeups by ceisma

Source repository: `/repos/ceisma`

## Repository Index

- HacklabWriteups/README.md
- HacklabWriteups/CyberLens/README.md
- HacklabWriteups/MD2PDF/README.md

## Writeup Content


### File: HacklabWriteups/CyberLens/README.md

# CyberLens

This TryHackMe room provides a solid foundation for applying various concepts to complete the challenge. In this challenge, we'll exploit web applications using Metasploit and Windows hacking techniques.

Before starting, it's important to add the domain `cyberlens.thm` to `/etc/hosts`. This is also mentioned in the CyberLens room: 

![](images/cyberl-1.png)  
*In my case it's* `sudo echo '10.10.174.127 cyberlens.thm' >> /etc/hosts`  


### Reconnaissance

Once the domain is added to `/etc/hosts`, we can begin with an Nmap scan:

![](images/cyberl-2.png)

![](images/cyberl-3.png)

Port **80** shows that the server is hosting a website. Upon visiting, we see a simple page with some basic information. One of the URLs  is called **'CyberLens Image Extractor'** and leads to a page where you can upload an image and view its metadata:

![](images/cyberl-4.png)

Inspecting the page's source code reveals that a piece of JavaScript extracts the metadata from the image. What stands out is the `fetch()` request, which calls itself on port **61777**, the same HTTP port we found in the Nmap scan. 

![](images/cyberl-5.png)

Visiting `http://10.10.174.127:61777` shows that it's an **Apache Tika Server**, version **1.17**. Now that we know this, we can search for vulnerabilities for this version and see if there is an available exploit. We'll do this using the tool `searchsploit`:

![](images/cyberl-7.png)
`searchsploit apache tika`  


### Exploitation

Now that we've found a potential exploit to gain a foothold, we will execute it using `metasploit`. After launching Metasploit via the command `msfconsole -q`, we search for the exploit with `search apache tika`. Then, select the exploit using `use 0`. 

![](images/cyberl-9.png)

It's important to configure the exploit properly. The required settings are: **RHOST**, **RPORT**, **TARGETURI**. Below is an image of my settings: 

![](images/cyberl-8.png)

Run the exploit with `run`. If successful, you'll see the following: 

![](images/cyberl-10.png)

We've successfully gained a foothold and now have a `meterpreter` shell. Navigate to `C:\Users\CyberLens\Desktop` to find the first flag. If you want to use Linux commands, you can spawn a shell by typing `shell`.

![](images/cyberl-11.png)  


### Privilege Escalation

For privilege escalation, we'll background the current `meterpreter` session by pressing `CTRL+Z` and confirming with `y`. Back in Metasploit, we'll use the `local_exploit_suggester` module with the command `use multi/recon/local_exploit_suggester`. Set the session number of your meterpreter session (`set SESSION 1`) and run it.

![](images/cyberl-12.png)

The exploit suggester provides several options for privilege escalation. We'll choose the first option, `always_install_elevated`. Set the `SESSION` and `LHOST` options for this module and run it with `run` (or `exploit`).

If successful, we'll return to the `meterpreter` session. Open a `shell` and use `whoami` to check if you have Administrator privileges. If the image below matches your output, you now have Administrator privileges.

![](images/cyberl-13.png)

Navigate to `C:\Users\Administrator\Desktop` to find the admin flag.

![](images/cyberl-14.png)



### File: HacklabWriteups/MD2PDF/README.md

# MD2PDF

The MD2PDF room on TryHackMe offers an excellent opportunity to practice and explore XSS (Cross-site Scripting) and SSRF (Server-Side Request Forgery) vulnerabilities.

### Reconnaissance

Since this challenge provides little information and lacks a clear description of the objective, a good starting point is to conduct an Nmap scan: 

![Nmap Scan](images/md2-1.png)  
`nmap 10.10.3.145 -sV -p- -vv -T4 -oN tcp_all`
  
  
We see that three ports are open: port **22** for **SSH**, and ports **80** and **5000**, which are not recognized as any specific services. Since port **80** is typically used for **HTTP**, we assume this is the case here as well. We can easily confirm this by visiting the target's IP address in a web browser: 

![Web page for port 80](images/md2-2.png)  
`http://10.10.3.145 (default port 80)`
  
  
Port **5000** also displays a web page, which looks very similar to the one on port **80** but has no additional functionality:

![Web page for port 5000](images/md2-3.png)  
`http://10.10.3.145:5000`
  
  
To discover whether the web server has other pages or files available, we perform a web scan on the IP address using a fuzzing tool called `feroxbuster`:

![Feroxbuster scan](images/md2-4.png)
`feroxbuster -u http://10.10.3.145 -x txt,php`
  
  
Meanwhile, we inspect the text field on the main page, which, as the room's title suggests, converts markdown (MD) text into a PDF file.

When entering a simple HTML syntax (in our example:  
`<a href="http://malicious-site.com">Click me!</a>`) we see that it gets executed, making the website vulnerable to **XSS**.

![XSS payload example with anchor link](images/md2-5.png)
  
  
With `feroxbuster`, we discover a directory called `/admin`. Upon visiting this directory, we are greeted by the following page: 

![Admin page discovery](images/md2-6.png)

### Exploitation

If an XSS or SSRF vulnerability exists in the PDF generator, we could potentially exploit it to access private server files or make requests on behalf of the server. The error message displayed on the page suggests that this might be possible.

Since we know the PDF generator's text field accepts HTML markup, we attempt to use an `<iframe>` as a payload to view the contents of `/admin` through port 5000. As `/admin` only allows internal requests, we try to submit a request using **SSRF** via the server.

![Attempted SSRF payload](images/md2-7.png)
  
  
The generated PDF should now reveal the `/admin` directory since the request was made through the server, rather than from our IP address.

![Generated PDF showing /admin directory contents](images/md2-8.png)

The `/admin` directory contains the flag for this challenge.




### File: HacklabWriteups/README.md

# HacklabWriteups
Write-ups to refine my pentest reporting abilities.

