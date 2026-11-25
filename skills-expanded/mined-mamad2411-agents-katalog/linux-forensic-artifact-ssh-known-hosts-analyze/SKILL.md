---
name: linux-forensic-artifact-ssh-known-hosts-analyze
description: "subdomain: forensic-analysis tags: - linux - ssh - known-hosts - lateral-movement - forensics nist_csf: - DE."
domain: cybersecurity
---

subdomain: forensic-analysis
tags:
- linux
- ssh
- known-hosts
- lateral-movement
- forensics
nist_csf:
- DE.AE-02
- RS.AN-01
tools: [Read, Bash, Glob, Grep]
mitre_attack:
- T1021.004
- T1078
capec: []
