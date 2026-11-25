---
name: andrew-google-tasks
description: Google Tasks API   (Task) 리. OAuth 2.0  .    목 조, , ,  리  .
---

# Google Tasks

## Overview

Google Tasks API 를     (Tasks)  조, , ,  리   . OAuth 2.0    Tasks  근.

## Setup

### 1. OAuth   

미 구 린,  과    :

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
cd /Users/andrew/.openclaw/workspace/google-tasks
python3 scripts/tasks_ops.py
```

첫   리고 Google  그    .

## Capabilities

###  목 조

**  목 :**
```
"   목 보"
"     ?"
```

###   

**   :**
```
" 미   ,    2 "
" 보고를  , 모: 5  "
```

###   리

** :**
```
" 미   "
```

###  

**  경:**
```
" 보고   주  "
```

###  

** 취:**
```
"  "
```

## Usage Examples

###  1:  목 조

```python
from scripts.tasks_ops import list_tasks, format_task

# 기본 목  조
tasks = list_tasks('@default')
for task in tasks:
    print(format_task(task))
```

###  2:   

```python
from scripts.tasks_ops import create_task

#   
task = create_task(
    tasklist_id='@default',
    title=' 보고 ',
    notes='5  , ',
    due='2026-04-20T17:00:00+09:00'
)
print(f"  : {task['title']}")
```

###  3:   리

```python
from scripts.tasks_ops import complete_task

#  
task_id = '_ID_기'
complete_task('@default', task_id)
print("  리!")
```

###  4:  목 목 조

```python
from scripts.tasks_ops import list_tasklists

tasklists = list_tasklists()
for tl in tasklists:
    print(f"{tl['title']} - {tl['id']}")
```

## Files Structure

```
google-tasks/
 SKILL.md
 scripts/
     tasks_ops.py      # Tasks API  
```

## Security Notes

- OAuth  `~/.google-tasks-token.pickle`  
-   `~/.google-credentials.json`   (린,  과 공)
-   `.gitignore`   
-  : `https://www.googleapis.com/auth/tasks` (Tasks 체 근)

## Troubleshooting

**"OAuth    " :**
- `~/.google-credentials.json`   
- 구 린    미   

** :**
-   고 : `rm ~/.google-tasks-token.pickle`

** :**
-    : `rm ~/.google-tasks-token.pickle && python3 scripts/tasks_ops.py`

## Integration with Other Google Skills

Same OAuth credentials (`~/.google-credentials.json`) are shared with `google-calendar` and `google-sheets` skills, so you only need to authenticate once!
