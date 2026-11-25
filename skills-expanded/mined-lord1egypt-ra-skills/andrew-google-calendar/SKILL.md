---
name: andrew-google-calendar
description: Google Calendar API   조, , ,  리. OAuth 2.0  .   린  고 리  .
---

# Google Calendar

## Overview

Google Calendar API 를    조, , ,    . OAuth 2.0     린 근.

## Setup

### 1. OAuth   

```bash
# Google Cloud Console  OAuth   
# https://console.cloud.google.com/apis/credentials

#    리 복
cp ~/Downloads/client_secret_*.json ~/.google-credentials.json
```

### 2. 존 

```bash
pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib
```

### 3.  

```bash
cd /Users/andrew/.openclaw/workspace/google-calendar
python3 scripts/oauth_setup.py
```

첫   리고 Google  그    .

## Capabilities

###  조

**  :**
```
" 7   보"
"  ?"
" 주  목 려"
```

** 기 조:**
```
"4  15  20   보"
```

###  

**  :**
```
"  2   미  , 1  , Zoom "
" 주  10  dentist , 30 "
```

###  

** 경:**
```
"  2  미  3  "
" 목 ' 미' '  미' 경"
```

###  

** 취:**
```
"  2  미 취"
```

## Usage Examples

###  1:   조

```python
from scripts.calendar_ops import list_events, format_event

#  7   조
events = list_events(max_results=10)
for event in events:
    print(format_event(event))
```

###  2:   

```python
from scripts.calendar_ops import create_event
from datetime import datetime, timedelta

#   2   
start = datetime.now() + timedelta(days=1, hours=14)
end = start + timedelta(hours=1)

event = create_event(
    summary=" 미",
    start_time=start.isoformat(),
    end_time=end.isoformat(),
    description="주  ",
    location="Zoom"
)
```

###  3: 린 목 

```python
from scripts.oauth_setup import list_calendars

calendars = list_calendars()
for cal in calendars:
    print(f"{cal['summary']} - {cal['accessRole']}")
```

## Files Structure

```
google-calendar/
 SKILL.md
 scripts/
    oauth_setup.py      # OAuth 2.0    리
    calendar_ops.py     # Calendar API  
 references/
```

## Security Notes

- OAuth  `~/.google-calendar-token.pickle`  
-   `~/.google-credentials.json`  
-   `.gitignore`   
-  : `https://www.googleapis.com/auth/calendar` (기/기 체 근)

## Troubleshooting

**"OAuth    " :**
- Google Cloud Console  OAuth 2.0  를  
- `client_secret_XXXXXX.json`  `~/.google-credentials.json`  복

** :**
-   고 : `rm ~/.google-calendar-token.pickle`
- Google Cloud Console  API  

** :**
- OAuth  면   
-    
