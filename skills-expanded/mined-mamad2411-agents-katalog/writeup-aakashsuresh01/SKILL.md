<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-aakashsuresh01
description: CTF writeups and security challenges by aakashsuresh01.
---

# Writeups by aakashsuresh01

Source repository: `/repos/aakashsuresh01`

## Repository Index

- Bug_skeleton/README.md

## Writeup Content


### File: Bug_skeleton/README.md

# Bug_skeleton
BugSight is a modular, open-source bug bounty toolkit designed for security researchers and pentesters to automate recon, triage,, BugSight streamlines every step of the bounty workflow from asset discovery to vulnerability reporting.
```
       .-.
      (o o)
      | O \
       \   \
        `~~~'
      BUGSIGHT

```

# BugSight

A modular bug bounty toolkit for fast recon and triage on large scopes.

## Goal

- Recon + Fast triage for large scopes, with automated aggregation and reporting.

## Tech Stack

- **Python CLI**: [Typer](https://github.com/tiangolo/typer)
- **External binaries**: Managed via `scripts/install_tools.sh`

## Features

- **Recon**: Automated with subfinder, dnsx, httpx, naabu, mapcidr, ASN expansion
- **Web**: Katana crawling (headless), history (gau/waybackurls), ffuf/feroxbuster brute, tech fingerprinting
- **Vuln**: Nuclei scan with curated tags; JSON + Markdown output; auto-updating templates
- **Secrets**: trufflehog & gitleaks on targets and scoped repos
- **Evidence**: gowitness screenshots for live hosts and paths
- **Report**: Aggregates all results into `/reports/{timestamp}/report.md` and HTML, with severity summary

## Requirements

- Follows `src/bugskeleton/modules/*.py` interfaces and `src/bugskeleton/core/pipeline.py`
- Configurable via `config/config.yaml` (scope, rate limits, exclusions, nuclei tags)
- Includes dry-run and schema-validation tests in `/tests`
- Ships with:
  - Moderate rate by default
  - Configurable user-agent
  - robots.txt off by default for crawling

## Example CLI Usage

```bash
# Run all pipeline modules
bugskeleton run all -t targets.txt -o reports

# Run web discovery with headless crawling
bugskeleton run web --headless

# Build aggregated report
bugskeleton report build
```

## Installation

```bash
# Install external tools
bash scripts/install_tools.sh

# Install Python dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config/config.yaml` to define your scope, exclusions, rate limits, and nuclei tags.

