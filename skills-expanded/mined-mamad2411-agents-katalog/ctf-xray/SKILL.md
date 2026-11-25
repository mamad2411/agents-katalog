---
name: ctf-xray
description: Use when pi needs the local xray binaries for passive proxy scanning, active crawler-based Web scanning, service scanning, or HTML/JSON vulnerability reporting. Trigger on mentions of xray, passive proxy audit, Web scanner proxy mode, or Chaitin xray.
---

# Local Assets

- Tool root: wherever `xray` is installed (put it on PATH, or `cd` into its directory).
- Windows binary: `xray_windows_amd64.exe`
- Linux binary: `xray_linux_amd64`
- Config files: `xray.yaml`, `module.xray.yaml`, `plugin.xray.yaml`, `config.yaml`
- Read `doc.md` for mode-specific guidance.

# Workflow

- Prefer passive proxy mode for authenticated/manual browsing.
- Use active crawling for quick coverage when login state is not required.
- Use service scan for host:port targets.
- Restrict targets in config or invocation to avoid accidental scope creep.

# Common Commands

```bash
# xray should be on PATH or run from its install dir (Linux amd64 build)
xray version
xray genca
xray webscan --listen 127.0.0.1:7777 --html-output xray-report.html
xray webscan --basic-crawler http://target/ --html-output crawler-report.html
xray servicescan --target 127.0.0.1:8009 --html-output service-report.html
```

# Notes

- Import `ca.crt` before HTTPS passive scanning.
- Use `--html-output` or `--json-output` for durable results.
- Review `hostname_allowed` style restrictions before passive proxy use.
