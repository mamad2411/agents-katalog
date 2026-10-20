# Project: Passwd to Dict Exercise

## IMPORTANT

This CLAUDE.md file is within a subdirectory of the main project. Please see the CLAUDE.md file in the source root directory for overarching context about this Python project.

The relative path of the source root directory is: ../.. (the directory is called python_workout).

## Exercise requirements
- Write a function - passwd_to_dict() - that reads from a Unix-style password file (e.g. /etc/passwd) and returns a dict based on it.
- Example file contents:
```
nobody:*:-2:-2::0:0:Unprivileged User:/var/empty:/usr/bin/false
root:*:0:0::0:0:System Administrator:/var/root:/bin/sh
daemon:*:1:1::0:0:System Services:/var/root:/usr/bin/false
```
- Each line is one user record, divided into colon-separated fields.
- Two fields are of interest; others can be ignored:
  - Field 0: username
  - Field 2: user's unique ID (uid).
- The function should return a dict where the usernames are keys and the user IDs are values.
- Lines beginning with a '#' (commented-out) should be ignored.
- Use Pythonic conventions.

## Exercise notes
- Consider using str.startswith(), str.endswith() and str.strip() (and its variants).
- str.split() is also likely to be useful.