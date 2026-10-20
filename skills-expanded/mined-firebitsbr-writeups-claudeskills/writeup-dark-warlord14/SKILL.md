<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dark-warlord14
description: CTF writeups and security challenges by dark-warlord14.
---

# Writeups by dark-warlord14

Source repository: `/repos/dark-warlord14`

## Repository Index

- ffufplus/README.md
- JSScanner/README.md

## Writeup Content


### File: JSScanner/README.md

# JSScanner

You can find the article related to this script here 
https://securityjunky.com/scanning-js-files-for-endpoint-and-secrets/

To install the required tools use
```
bash install.sh
```

Change the alive.txt with the domains you need to test. These should be in below format
```
http://example.com
https://example2.com
```

To run the tool use 
```
jsscanner path_to_alive.txt

Eg. jsscanner alive.txt
```


Thanks to [@amiralkizaru](https://github.com/amiralkizaru), [@LifeHack3r](https://github.com/LifeHack3r) and [@g33kyshivam](https://github.com/g33kyshivam) for the contribution.



### File: ffufplus/README.md

# ffufplus - ffuf on Steroids

[![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/dark-warlord14/ffufplus/issues)

ffufplus - ffuf on Steroids

<img src="https://securityjunky.com/wp-content/uploads/2020/04/carbon-17-1024x497.png" alt="ffufplus" width="750">

---

### Installation

```
bash install.sh
```

### Usage

To run the tool, just use the following command.
```
bash script.sh
```


### Thanks

- [@joohoi](https://twitter.com/joohoi) - for the great ffuf

