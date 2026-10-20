<!--
LICENSE UPL
Author: Mauro Risonho de Paula Assumpção
Data Create: 2026-03-16
Data Update: 2026-03-16
-->

---
name: writeup-hackgiver
description: CTF writeups and security challenges by hackgiver.
---

# Writeups by hackgiver

Source repository: `/repos/hackgiver`

## Repository Index

- Headers-Checker/README.md

## Writeup Content


### File: Headers-Checker/README.md

# Security Headers Checker

A Python script for pentesting that checks whether key security response headers are present on a given URL, and whether they are securely configured. Outputs a color-coded report with current values, configuration analysis, and recommended fixes.

---

## Headers checked

| Header | Secure configuration expected |
|---|---|
| Strict-Transport-Security | max-age >= 31536000; includeSubDomains |
| Content-Security-Policy | default-src defined; no unsafe-inline, unsafe-eval or wildcard |
| X-XSS-Protection | 1 or 1; mode=block |
| X-Frame-Options | DENY (preferred) or SAMEORIGIN |
| X-Content-Type-Options | nosniff |
| Cache-Control | must contain no-store |
| Referrer-Policy | no-referrer or same-origin (strict values) |
| Permissions-Policy | at least one feature explicitly denied with =() |

---

## Requirements

Python 3.6 or higher is required. Install the dependency with:

```bash
pip install requests
```

---

## Usage

```bash
python3 header_checker.py <url> [--no-verify]
```

### Arguments

| Argument | Description |
|---|---|
| `url` | Target URL. If no scheme is provided, `https://` is added automatically. |
| `--no-verify` | Optional. Skips SSL certificate verification. Useful in lab environments or when testing self-signed certificates. |

### Examples

```bash
# Basic usage
python3 header_checker.py https://example.com

# Without explicit scheme
python3 header_checker.py example.com

# Skip SSL verification
python3 header_checker.py https://example.com --no-verify
```

---

## Output

Each header is evaluated and assigned one of three statuses:

- PRESENT & SECURE: the header is present and meets the expected secure configuration.
- PRESENT BUT INSECURE: the header is present but misconfigured. The detected issue and a recommended fix are shown.
- MISSING: the header is not present. A recommended value is shown.

At the end of the report a summary is displayed with the count of secure, insecure, and missing headers, along with a percentage score color-coded as follows:

- 75% or above: green
- 50% to 74%: yellow
- Below 50%: red

The full list of response headers received from the server is also printed, which can be useful when writing a pentest report.

---

## Validation logic

- **Strict-Transport-Security**: verifies that max-age is at least 31536000 (one year) and that the includeSubDomains directive is present.
- **Content-Security-Policy**: checks that default-src is defined and that no unsafe directives such as unsafe-inline, unsafe-eval, or a bare wildcard are present.
- **X-XSS-Protection**: must start with 1. A value of 0 (disabled) is flagged as insecure.
- **X-Frame-Options**: accepts DENY or SAMEORIGIN. ALLOW-FROM is flagged as deprecated and insecure.
- **X-Content-Type-Options**: must be exactly nosniff.
- **Cache-Control**: must contain the no-store directive.
- **Referrer-Policy**: accepts no-referrer, same-origin, strict-origin, and strict-origin-when-cross-origin. Permissive values such as unsafe-url are flagged.
- **Permissions-Policy**: checks that at least one feature is explicitly denied using =() and that not all features use a wildcard.

---

## Disclaimer

This tool is intended for use on systems you own or have explicit permission to test. Unauthorized use against third-party systems may be illegal.

