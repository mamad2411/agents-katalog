<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-dustinfant
description: CTF writeups and security challenges by dustinfant.
---

# Writeups by dustinfant

Source repository: `/repos/dustinfant`

## Repository Index

- ScopeLine/README.md
- ScopeLine/report.md

## Writeup Content


### File: ScopeLine/README.md

# ScopeLine

**ScopeLine** is a modular, scope-driven, identity-aware penetration testing framework for web applications and APIs.  
It focuses on authorization flaws, identity context, SSRF, IDOR, and attack path analysis, with clean Markdown reporting.

## Overview

ScopeLine provides a structured approach to API and web security testing:

- **Scope-driven**: Targets are defined explicitly in `scope.yaml`
- **Identity-aware**: Tests behavior across user roles and auth contexts
- **Modular**: Discovery, vulnerability scanning, analysis, and reporting are cleanly separated
- **Automation-friendly**: Designed for CI/CD and repeatable assessments

## Key Features

- HTTP service discovery and probing
- OpenAPI endpoint discovery
- Directory and endpoint enumeration
- JWT and authentication header analysis
- Privilege inference and role comparison
- IDOR and SSRF detection
- Attack path analysis
- Structured Markdown reporting

## Usage

```bash
# Ensure PYTHONPATH includes the project root
export PYTHONPATH=.

# Run full interactive scan
python3 run.py

# Run CI-style scan
python3 run.py --ci



### File: ScopeLine/report.md

# Pentest Report

No confirmed findings.

