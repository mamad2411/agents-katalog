---
name: ctf-windows-tools
description: Use when pi needs the local Windows exploit helper bundle for Jenkins-related tooling such as ysoserial, jenkins-cli, or included CVE executables. Trigger on mentions of `ysoserial`, `jenkins-cli`, Jenkins exploit helpers, or the `windows_tools` directory.
---

# Local Assets

- Tool root: wherever the `windows_tools` bundle is unpacked.
- Files: `ysoserial-all.jar`, `jenkins-cli.jar`, `CVE_2015_8103.exe`, `CVE_2017_1000353.exe`, `CVE_2019_1003000.exe`, `CVE_2019_1003005.exe`

# Workflow

- Identify the exact Jenkins or Java exploitation task first.
- Prefer the least invasive validation path before launching a bundled CVE binary.
- Use `java -jar` with the JAR tools and only run the EXEs when the user explicitly wants that path.

# Common Commands

```bash
# java is required on PATH (check: command -v java)
cd ./windows_tools   # or wherever the jars live
java -jar ./ysoserial-all.jar
java -jar ./jenkins-cli.jar -s http://target/ help
```

# Notes

- Treat the CVE executables as high-risk helpers.
- Keep scope narrow and record exact target/version assumptions before use.
