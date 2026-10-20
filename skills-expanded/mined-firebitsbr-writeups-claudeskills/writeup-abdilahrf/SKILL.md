<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-abdilahrf
description: CTF writeups and security challenges by abdilahrf.
---

# Writeups by abdilahrf

Source repository: `/repos/abdilahrf`

## Repository Index

- CTFWriteupScrapper/README.md

## Writeup Content


### File: CTFWriteupScrapper/README.md

## CTFWriteupScrapper

Scrap all writeup from http://ctftime.org/ and organize which to read first.

Initialize SQLite DB:

```
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

Start : `python runserver.py`

Open from browser `127.0.0.1:31337`

Update your database with latest writeup from ctftime : `127.0.0.1:31337/feed/`

## Requirements

- Flask
- BeautifulSoup
- urllib2
- mechanize

## Todo

Empty

## Screenshot

![Screen Shoot](screenshot.png)

## License

MIT @abdilahrf

