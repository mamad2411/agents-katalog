---
name: ctf-awd-watchbird
description: Use when pi needs the local Watchbird AWD PHP WAF package for installation, configuration, response inspection, flag masking, UI control, or AWD traffic logging on a PHP Web directory. Trigger on mentions of watchbird, PHP AWD WAF, `watchbird.php`, or `waf.so` deployment.
---

# Local Assets

- Tool root: wherever the watchbird package is unpacked (deploy into the target Web root).
- Files: `watchbird.php`, `waf.so`, `doc.md`

# Workflow

- Only use this on authorized AWD/lab targets and respect the event rules.
- Confirm the target Web root and whether the current user can write there.
- Prefer install/uninstall commands over manual file surgery.
- Note the control panel path and config persistence location after install.

# Common Commands

```bash
php watchbird.php --install /var/www/html
php watchbird.php --uninstall /var/www/html
```

# Notes

- The UI is opened with `?watchbird=ui` on an installed page.
- `watchbird.php` must be readable by `www-data` and the target directory must be writable during installation.
- Read `doc.md` before enabling deeper protections such as reverse proxying or fake-flag responses.
