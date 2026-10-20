---
name: ctf-dirsearch
description: Use when pi needs the local dirsearch setup for Web path brute forcing, hidden directory discovery, backup-file hunting, recursive content discovery, or authenticated directory fuzzing. Trigger on mentions of dirsearch, directory brute force, backup file search, or hidden path enumeration.
---

# Local Assets

- Tool root: wherever `dirsearch` is installed (put it on PATH, or `cd` into its directory).
- Recommended entrypoint: `dirsearch` (CLI on PATH) or `python3 ./dirsearch.py`.
- Read `doc.md` for local defaults and `config.ini` behavior.

# Workflow

- Prefer the `dirsearch` CLI on PATH.
- Choose extensions based on the target stack.
- Add filters early if the site returns fake `200` or uniform `403` pages.
- Use `--cookie` or `--raw` for authenticated targets.

# Common Commands

```bash
# dirsearch should be on PATH (or run: python3 ./dirsearch.py ...)
dirsearch -u http://target -e php,html,js
dirsearch -u http://target -e php,zip,bak,old,txt -f
dirsearch -u http://target -e php,html,js -r -R 2
dirsearch -u http://target --cookie "PHPSESSID=xxxx" -e php,html,js
```

# Notes

- If the wordlist is not `%EXT%` based, remember `-f`.
- Use `--exclude-response`, `--exclude-text`, or `--exclude-sizes` when noise is high.
- Save reports with `--format` and `-o` when the user wants reusable output.
