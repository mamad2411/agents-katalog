---
name: ssl-cert-check
description: Check SSL certificate validity and expiration for a domain
---

# SSL Certificate Check

Check SSL certificate validity and expiration for a domain

## When to Use

- User wants to check ssl
- User wants to ssl check
- Keywords: ssl, certificate, security, https

## Required Parameters

- **domain** (string): Domain to check SSL certificate

## Output

- **valid** (boolean): Certificate is valid
- **issuer** (string): Certificate issuer
- **expires** (string): Expiration date
- **days_left** (number): Days until expiration

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: ssl-checker.io
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `fetch` -> 5 steps -> Exit: `ret_ok`, `ret_fail`
