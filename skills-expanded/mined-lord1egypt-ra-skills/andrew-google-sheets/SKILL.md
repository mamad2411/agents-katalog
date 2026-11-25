---
name: andrew-google-sheets
description: Google Sheets API   기/기, , 맷 리. OAuth 2.0  .  구  를 조고   .
---

# Google Sheets

## Overview

Google Sheets API 를   를 조, ,    . OAuth 2.0    Google Sheets  근.

## Setup

### 1. OAuth   

미 구 린    :

```bash
#   미  면 
ls ~/.google-credentials.json
```

### 2. 존 

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3.  

```bash
cd /Users/andrew/.openclaw/workspace/skills/google-sheets
python3 scripts/oauth_setup.py
```

첫   리고 Google  그    .

## Capabilities

###  기

** 조:**
```
"  '무'  근 10  보"
"A1  D10   "
```

**  조:**
```
"'2026  4 '  모  보"
```

###  기

** :**
```
"무   목 : 'OpenClaw ',  '2026-04-21',  '2026-04-21',  '100%'"
```

** :**
```
"무 6 째   '100%'  "
```

###  리

**  :**
```
"  ' 리' "
```

** 목 :**
```
" 구  목 보"
```

## Usage Examples

###  1:  목 조

```python
from scripts.sheets_ops import list_spreadsheets

#  모  목
sheets = list_spreadsheets()
for sheet in sheets:
    print(f"{sheet['name']} - {sheet['spreadsheetId']}")
```

###  2:   기

```python
from scripts.sheets_ops import read_range

#    기
data = read_range('SPREADSHEET_ID', 'Sheet1!A1:D10')
for row in data:
    print(row)
```

###  3:  기

```python
from scripts.sheets_ops import write_range

#    기
write_range(
    spreadsheet_id='SPREADSHEET_ID',
    range_name='Sheet1!A1:D1',
    values=[['', '', '', '']]
)
```

###  4:   (Append)

```python
from scripts.sheets_ops import append_rows

#   
append_rows(
    spreadsheet_id='SPREADSHEET_ID',
    range_name='Sheet1!A:D',
    values=[[' ', '2026-04-21', '', '0%']]
)
```

###  5:   

```python
from scripts.sheets_ops import create_spreadsheet

#   
new_sheet = create_spreadsheet('무')
print(f" : {new_sheet['spreadsheetId']}")
```

## Files Structure

```
google-sheets/
 SKILL.md
 scripts/
     oauth_setup.py      # OAuth 2.0    리
     sheets_ops.py       # Sheets API  
```

## Security Notes

- OAuth  `~/.google-sheets-token.pickle`  
-   `~/.google-credentials.json`   (린 공)
-   `.gitignore`   
-  : `https://www.googleapis.com/auth/spreadsheets` ( 체 근)

## Troubleshooting

**"OAuth    " :**
- `~/.google-credentials.json`   
- 구 린    미   

** :**
-   고 : `rm ~/.google-sheets-token.pickle`

** :**
-    : `rm ~/.google-sheets-token.pickle && python3 scripts/oauth_setup.py`

## Integration with Other Google Skills

Same OAuth credentials (`~/.google-credentials.json`) are shared with `google-calendar` and `google-tasks` skills, so you only need to authenticate once!
