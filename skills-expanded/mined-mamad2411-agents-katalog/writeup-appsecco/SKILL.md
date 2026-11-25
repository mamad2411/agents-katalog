<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-appsecco
description: CTF writeups and security challenges by appsecco.
---

# Writeups by appsecco

Source repository: `/repos/appsecco`

## Repository Index

- c0c0n-2019-ctf-writeups/README.md
- c0c0n-2019-ctf-writeups/domectf/algeria.md
- c0c0n-2019-ctf-writeups/domectf/australia.md
- c0c0n-2019-ctf-writeups/domectf/botswana.md
- c0c0n-2019-ctf-writeups/domectf/usa.md
- c0c0n-2019-ctf-writeups/redteam-village/README.md

## Writeup Content


### File: c0c0n-2019-ctf-writeups/README.md

# c0c0n 2019 CTF Write-ups
CTF write-ups from c0c0n 2019 CTF challenges that we participated

## CTF

1. [Redteam Village](https://ctf.redteamvillage.org)
2. [Dome CTF](https://domectf.in)

### Redteam Village

* [Redteam Village Writeup](redteam-village/README.md)

### Dome CTF

* [Australia - The Secret Message](domectf/australia.md)
* [China - The Dark Room](domectf/china.md)
* [Brazil - Digital Fragments](domectf/brazil.md)
* [United States - Play Store](domectf/usa.md)
* [Algeria - Evil Conference](domectf/algeria.md)
* [Botswana - The Rules](domectf/botswana.md)



### File: c0c0n-2019-ctf-writeups/redteam-village/README.md

# RedTeam Village CTF Write-up

## CTF Portal

https://ctf.redteamvillage.org/

## Attack

* The CTF portal gave 1 target IP - 34.89.165.167
* We found an SSH, RDP and web server running on the target
* Using the provided clue `victimcorporation`, we were able to browse to `http://34.89.165.167/victimcorporation/`
* We ran `dirb` against the URL `http://34.89.165.167/victimcorporation/` and found a directory `config`
* On subsequent bruteforce for filenames on `http://34.89.165.167/victimcorporation/config` we found `config.zip` which we were able to download
* An XML file inside gave us the credentials for `guestuser`
* We were able to SSH in to `34.89.165.167` using `guestuser` credential
* Navigating the filesystem, we were able to find another file revealing the credential of `appuser` who has `Local Administrator` privilege
* We also found another system in the LAN with IP `<IP>`
* We were able to laterally move to this system using `appuser` credential and login over RDP
* This new system was part of a domain controller
* We identified the `SQL Server` by resolving `MSSQL-SERVER` hostname from this domain joined machine

At this point, we were not able to connect to the SQL Server since there was no TCP/IP listener for it.

## Result

We ended up being #1 in the Red Team category for this event, with maximum points in the category. Since we were not able to reach the final objective of compromising the domain controller, the 1st prize for the event went to the highest scorer in the Blue Team category.


### File: c0c0n-2019-ctf-writeups/domectf/algeria.md

# Algeria - Evil Conference

## Solution

* The `Server` header in HTTP response of `http://evil-conference.domectf.in` revealed that there is a `Docker Registry`
* Ran `nmap` to scan for Top 1000 open ports and found TCP port 5000 running a Docker registry
* A comment in `http://evil-conference.domectf.in/js/main.js` revealed username for the docker registry
* Bruteforced the docker registry endpoint `http://evil-conference.domectf.in:5000/v2/catalog` for the password
* Found `domectf/iloveyou` as the credentials for the docker registry
* Enumerated the repositories using the URL `http://evil-conference.domectf.in:5000/v2/catalog`
* Pulled the private docker image and ran a local container to find a password protected zip file in `/home/domectf`
* Bruteforced the zip file to find the password `tetra` and extracted a list of files with hashes
* Each hash was MD5 with 1 junk character
* Fixed all the MD5 hashes by removing the junk character
* Each hash gave us a plain text character
* Stringing all this characters gave a base64 string which when decoded is the flag




### File: c0c0n-2019-ctf-writeups/domectf/australia.md

# Australia - The Secret Message

## Solution

- A zip file containing a `message.txt` was given. The zip file contained an encoded string starting with `revrs`.
- The string ended with `srver` which was the reverse of `revrs`, so we understood that `revrs` at the beginning meant to reverse the string.
- When we reverse the code leaving back `revrs` at the start, we again have a `revrs` which meant to reverse it again. And then we saw `bas64` at the beginning of the string.
- We understood it should be decoded with `base64` and once we did that, we also observed we got a `rot13`.
- For the uninitiated, `rot13` is simple letter substitution cipher that replaces a letter with the 13th letter after it. All this can be done with any online decoder website.
- As we decode in recursion, the string gets smaller and smaller until we get the flag.
- If we observe, all the operations are mentioned in 5 characters making it easier to write a program to decode this.
- We will have to iterate till we do not find `revrs` or `bas64` or `rot13` and do the operation in the first 5 characters in the string. The end result would be the flag


### File: c0c0n-2019-ctf-writeups/domectf/botswana.md

# Botswana - The rules!!

## Solution

* The challenge says "Make sure you follow the rules. The rules tell a different story."
* Looking at the rules sheet provided by the organisers, we noticed that there is a QR code
* The QR code points to a text file as Github gist `https://gist.githubusercontent.com/anees264/90af6d6e6b80c65b18a15e7c0dd769bd/raw/eb0bdcbf19368d9dc4ed66450816ca4314e88dd4/the_rules.txt`
* The contents of the text file looks like a RegEx pattern
* Upon further inspection we identified that it is a code snippet written in an esoteric programming language called Malbolge
* We used an online Malbolge interpreter to execute the code and the output is the flag 


### File: c0c0n-2019-ctf-writeups/domectf/usa.md

# Unlockme.apk

## Solution

1. Install Unlockme.apk in a rooted Android device
2. Scan a human face successfully in order view the login page
3. Decode APK file using `apktool` to find the hardcoded, base64 encoded, password
4. Do a source code analysis to understand the login process
   1. `register()` function was probably not being called, even though the code did exist
   2. `registerUser()` function was being invoked from within the `register()` function, based on a certain condition
   3. The app was trying to read user details from a shared preferences file named as `ctf.xml`.
5. Next obvious things to do was
   1. Update the shared preferences file `ctf.xml` to include following missing details `keyusername`, `true`, and `keyemail`
   2. Call the `registerUser()` function directly using Frida tool
   3. If all goes well, the `Internal` activity would be displayed
6. Analyse the `Internal.class` source code to understand what is happening
   * `startTimer()` function in class `Internal` is instantiating the class `Internal$1`
   * The source code in `Internal$1.class` file has a reference to a native method called `stringFromJNI()`
   * The source code in `Internal.class` file is loading a library named as `hello-jni`.
7. Using Frida, call the `startTimer()` function of `Internal` class.
8. Print the string value returned when `stringFromJNI()` function is called, in order to read the flag.
