---
name: linux-container-namespace-user-privesc-detect
description: "subdomain: container-security tags: - linux - namespace - user-namespace - privesc - container nist_csf: - DE."
domain: cybersecurity
---

subdomain: container-security
tags:
- linux
- namespace
- user-namespace
- privesc
- container
nist_csf:
- DE.CM-01
- DE.AE-02
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1611
- T1068
capec: []
