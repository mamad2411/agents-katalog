<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-01cyberwarehouse
description: CTF writeups and security challenges by 01cyberwarehouse.
---

# Writeups by 01cyberwarehouse

Source repository: `/repos/01cyberwarehouse`

## Repository Index

- Portia/README.md

## Writeup Content


### File: Portia/README.md

# Portia 0.0.1 alpha
Portia is a manual web scanner tool made with nodejs for pentesting and bug bounty supported by linux operating system. Have any problems and bugs? please report to us!
portia inspired by real life spider name which mean intelligent at hunting behaviour. project will be continue untill 2027.

# Installation
## For debian and ubuntu based distro
```
sudo apt install nodejs && sudo apt install git
git clone https://github.com/01cyberwarehouse/Portia
```
## For arch based distro
```
sudo pacman -S nodejs git
git clone https://github.com/01cyberwarehouse/Portia
```
## For fedora based
```
sudo dnf install nodejs && sudo dnf install git
git clone https://github.com/01cyberwarehouse/Portia
```
# Usage
```
# For first time
machineryman01@machine01:~/Documents/project/hacking_tools/Portia$ chmod +x portia 

machineryman01@machine01:~/Documents/project/hacking_tools/Portia$ ./portia -t
http://testhtml5.vulnweb.com/#/popular

[T] Scan report on Wed Nov 12 2025 20:02:14 GMT+0800 (Malaysia Time)
[>] TARGET URL: "http://testhtml5.vulnweb.com/#/popular"
[i] IP: "44.228.249.3" Protocol family: IPv4

Raw Headers [!]:
Server,nginx/1.19.0,Date,Wed, 12 Nov 2025 12:02:14 GMT,Content-Type,text/html; charset=utf-8,Content-Length,6940,Connection,close,Access-Control-Allow-Origin,*

Headers [!]:
 {
  server: 'nginx/1.19.0',
  date: 'Wed, 12 Nov 2025 12:02:14 GMT',
  'content-type': 'text/html; charset=utf-8',
  'content-length': '6940',
  connection: 'close',
  'access-control-allow-origin': '*'
}

Additional information [i]:
Protocol: "http:"
Path location: "/"
Host: testhtml5.vulnweb.com
Status code: 200
Content-Type: text/html; charset=utf-8
Do you want to scan the directories of http://testhtml5.vulnweb.com/#/popular (y/n): y
[!] HOST: testhtml5.vulnweb.com Path: /admin.js STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /index.htm STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /phpmyadmin/sql.php STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /ApacheGUI/jsp/GUISettings.jsp STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /main.js STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /style.css STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /admin.php STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /index.php STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /main.php STATUS: Not Found 404
[!] HOST: testhtml5.vulnweb.com Path: /index.html STATUS: Not Found 404

```
# Video example
https://github.com/user-attachments/assets/d4f8b56e-59d0-4ba2-88a0-8cb6036334f0

# Warning!
I do not responsible for any misuse of this tool please use it for ethical reason.

