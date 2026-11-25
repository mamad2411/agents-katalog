---
name: ctf-sqlmap
description: Use when pi needs the local sqlmap setup for authorized SQL injection detection, parameter testing, raw HTTP request replay, tamper-assisted payload shaping, database enumeration, or controlled extraction in CTF and lab targets. Trigger on mentions of sqlmap, SQL injection automation, raw request files, tamper scripts, or sqlmap API usage.
---

# Local Assets

- Tool root: wherever `sqlmap` is installed (put it on PATH, or `cd` into its directory).
- Entrypoint: `sqlmap` (CLI on PATH) or `python3 ./sqlmap.py`.
- API entrypoint: `sqlmap-api` or `python3 ./sqlmapapi.py`.
- Request templates: `GET.txt`, `POST.txt`.
- Config: `sqlmap.conf`.
- Read `README.md` and the `doc/` dir when you need option details.

# Workflow

- Confirm authorization and target scope before using automated SQLi testing.
- Start from one reproducible request and pin the suspected parameter with `-p` before widening coverage.
- Prefer `-r` with a raw request file for authenticated, cookie-heavy, JSON, or custom-header targets.
- Escalate gradually: detection and fingerprinting first, then enumeration, then focused extraction.
- Reach for `--level`, `--risk`, `--tamper`, or extra threads only after a baseline probe shows they are needed.
- Avoid broad crawling or whole-site automation when a single proof request is enough.

# Common Commands

```bash
# sqlmap should be on PATH (or run: python3 ./sqlmap.py ...)
sqlmap -h
sqlmap -u "http://target/item.php?id=1" -p id --batch
sqlmap -u "http://target/item.php?id=1" -p id --dbs
sqlmap -r ./POST.txt -p username --batch --current-user
sqlmap -r ./GET.txt --level 3 --risk 2 --threads 4
sqlmap -r request.txt --cookie="PHPSESSID=xxxx" --tamper=space2comment --dump
sqlmap-api -s -H 127.0.0.1 -p 8775
```

# Notes

- `-r` is usually the most reliable path when the original request comes from Burp or a browser session.
- Use `-p` to keep probes bounded and reduce noise on multi-parameter requests.
- Save durable output when the user needs a reusable trail; sqlmap will also keep session data under its output directory.
- Treat `--os-shell`, file write, and similar post-exploitation features as higher-risk actions that need a stronger proof bar.
