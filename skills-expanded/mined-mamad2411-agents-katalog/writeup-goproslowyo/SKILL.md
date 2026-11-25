<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-goproslowyo
description: CTF writeups and security challenges by goproslowyo.
---

# Writeups by goproslowyo

Source repository: `/repos/goproslowyo`

## Repository Index

- docsthebox/README.md
- docsthebox/USAGE.md

## Writeup Content


### File: docsthebox/README.md

# docsthebox

![screenshot of notion database](.img/notebook.png)

## whats this?

docsthebox hits the hack the box api and gets all api data on the machines.

machines are stored in specified the notion database if they don't exist yet.

each page has basic templates attached to help document your exploitation.

## how do i use this?

glad you asked -- please check out the [usage instructions](USAGE.md).

you *will* need to set some things up so please read it.

easiest is to run the docker container if you have docker, otherwise run the python code.

sorry windows users, you might have to changes some paths. or just run the docker container.

## what else is needed?

maybe use notionx library over raw json + requests

code cleanup and commenting

## known bugs

hack the box has an incredibly aggresive cloudflare configuration and notion can
sometimes not fetch the images from hack the box without receiving a 403 denied.
this may cause images to not load sometimes. sorry, blame htb for their CF config.

## creds

- [ritchies](https://github.com/ritchies)

- [goproslowyo](https://github.com/goproslowyo)

- thomas frank for inspiration

![screenshot of notion notebook page](.img/page1.png)
![another screenshot of notion notebook page](.img/page2.png)



### File: docsthebox/USAGE.md

# How To Use

- Create a Notion Developer Integration

  - [Notion Integrations](https://www.notion.so/my-integrations)

  ![Create a Notion Integration](.img/notion-api-key.png)

  - Get a Notion Internal Integration Secret

  ![Get an Internal Integration Secret](.img/notion-api-key2.png)

- Duplicate the Notion template

  - [Notion Template](https://infosecinfo.notion.site/fd6bd562b7644ac7a69d254a555ef5c3?v=da10fc398b3b468091fe8e933e16cfb0&pvs=4)

  ![Duplicate the Template](.img/clone-notion-database.png)

  - Choose workspace to duplicate to

  ![Duplicate template to Workspace](.img/clone-notion-database2.png)

- Get the Notion DB ID from the URL (yours will be unique from the screenshot)

  ![Get the Notion DB ID from the URL](.img/notion-db-id.png)

- Authorize the Notion Integration to access your new Notion database

  ![Authorized the Notion Integration to Access your DB](.img/authorized-notion-integration1.png)

  ![Authorized the Notion Integration to Access your DB #2](.img/authorized-notion-integration2.png)

- Get a Hack The Box app token from your profile settings page

  - [Profile Settings](https://app.hackthebox.com/profile/settings)

  ![Get Hack The Box App Token](.img/htb-app-token.png)

---

By now you should have three things:

  1. A Notion Internal Integration Secret

  1. The database ID of your Notion DB

  1. Your Hack The Box App Token

If don't have these items please review the above steps again.

- Install Poetry (you don't need poetry really, just requests, but poetry makes it easier if the project grows)

  - `pip install --user poetry`

  - `oetry run python box-to-docs.py --help`

  or

  - `pip install --user requests`

  - `python box-to-docs.py`

  or

  - `docker run -v /tmp:/tmp ghcr.io/goproslowyo/docsthebox:latest --help`

NOTE: Please adjust the paths accordingly if you're on windows.

