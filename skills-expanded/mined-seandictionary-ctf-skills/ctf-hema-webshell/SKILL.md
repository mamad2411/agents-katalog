---
name: ctf-hema-webshell
description: Use when pi needs the 河马 WebShell scanner package for Windows or Linux webshell scanning and cleanup planning on a Web root. Trigger on mentions of 河马WebShell, webshell查杀, backdoor scan, or malicious PHP/ASPX file hunting in a site directory.
---

# Local Assets

- Tool root: wherever the 河马 package is unpacked.
- Windows package: `HmSetup.zip` (Windows only).
- Linux package: `hm-linux-amd64.tgz` (use this on this Linux host).
- Docs: `doc_win.md`, `doc_linux.md`

# Workflow

- Choose the package that matches the target OS.
- Use this for scanning and triage, not blind deletion.
- Preserve suspicious samples or hashes when the user is doing incident review.

# Notes

- Read `doc_win.md` for Windows usage.
- Read `doc_linux.md` for Linux usage.
- Favor reporting and quarantine plans before destructive cleanup.
