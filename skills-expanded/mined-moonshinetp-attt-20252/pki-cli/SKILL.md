---
name: pki-cli
description: Manage X.509 certificates via PKI Manager CLI. Use this skill for creating CAs, issuing certificates, revoking, renewing, downloading certs in various formats (PEM, DER, PKCS12, JKS), and managing CRLs. Triggered by mentions of PKI CLI, certificate management commands, or CA operations.
---

# PKI Manager CLI

## Overview

PKI Manager CLI is a command-line tool for managing X.509 certificates via the PKI Manager API. Use the `pki` CLI tool via `uvx` for all operations.

## Quick Start

### Prerequisites

Create a `.env` file with your PKI Manager credentials:

```bash
# Create config directory
mkdir -p ~/.config/pki-cli

# Create .env file
cat > ~/.config/pki-cli/.env << 'EOF'
PKI_API_URL=https://your-pki-server.example.com/api/v1
PKI_OIDC_URL=https://your-iam-server.example.com/realms/realm/protocol/openid-connect/token
PKI_CLIENT_ID=your-client-id
PKI_CLIENT_SECRET=your-client-secret
EOF
```

> **Important:** The API URL must include `/v1` at the end (e.g., `https://pki.example.com/api/v1`). Using just `/api` will cause parsing errors.

### Running the CLI

Use `uvx` to run the CLI directly from the GitHub repository:

```bash
# Run any pki command
uvx --from "git+https://github.com/oriolrius/pki-manager-cli.git" pki <command>

# Create an alias for convenience
alias pki='uvx --from "git+https://github.com/oriolrius/pki-manager-cli.git" pki'
```

## CLI Commands

### Configuration & Auth

```bash
# Show current configuration
pki config

# Test authentication
pki login

# Clear cached token
pki logout

# Check API health
pki health
```

### Certificate Authorities

```bash
# List all CAs
pki ca list
pki ca list --status active
pki ca list -o json

# Get CA details
pki ca get <CA_ID>
pki ca get <CA_ID> -o json

# Create a new CA
pki ca create --cn "My Root CA" --org "My Organization" --country ES
pki ca create --cn "My CA" --org "Org" --country ES --algorithm RSA-4096 --validity 3650

# Revoke a CA
pki ca revoke <CA_ID> --reason cessationOfOperation
pki ca revoke <CA_ID> -f  # Skip confirmation

# Delete a CA
pki ca delete <CA_ID> -f
```

**Key Algorithms:** `RSA-2048`, `RSA-4096`, `ECDSA-P256`, `ECDSA-P384`

### Certificates

```bash
# List certificates
pki cert list
pki cert list --ca <CA_ID>
pki cert list --status active --type server
pki cert list -o json

# Get certificate details
pki cert get <CERT_ID>
pki cert get <CERT_ID> -o json

# Issue a new certificate
pki cert issue --ca <CA_ID> --cn "myserver.example.com" --type server
pki cert issue --ca <CA_ID> --cn "myserver.example.com" --type server \
    --dns "www.example.com" --dns "api.example.com" \
    --ip "192.168.1.100" \
    --validity 365 --algorithm RSA-2048

# Issue client certificate
pki cert issue --ca <CA_ID> --cn "user@example.com" --type client

# Issue email certificate (requires email SANs via API)
pki cert issue --ca <CA_ID> --cn "user@example.com" --type email

# Renew a certificate
pki cert renew <CERT_ID>
pki cert renew <CERT_ID> --validity 365

# Revoke a certificate
pki cert revoke <CERT_ID> --reason keyCompromise
pki cert revoke <CERT_ID> -f  # Skip confirmation

# Delete a certificate
pki cert delete <CERT_ID> -f

# Download certificate
pki cert download <CERT_ID>                      # PEM format
pki cert download <CERT_ID> -f pkcs12 -p secret  # PKCS12 with password
pki cert download <CERT_ID> -f jks -p secret     # Java KeyStore
pki cert download <CERT_ID> -o mycert.pem        # Custom output file
```

**Certificate Types:** `server`, `client`, `dual`, `email`, `code_signing`
**Download Formats:** `pem`, `der`, `pkcs12`, `jks`

### Dashboard & Search

```bash
# Show statistics
pki stats
pki stats -o json

# List expiring certificates
pki expiring
pki expiring --limit 10

# Search CAs and certificates
pki search "example.com"
pki search "myserver" -o json
```

## Output Formats

All commands support `-o json` for JSON output, useful for scripting:

```bash
# Get CA ID from JSON output
CA_ID=$(pki ca list -o json | jq -r '.items[0].id')

# Process certificates
pki cert list -o json | jq '.items[] | {id, subject, status}'
```

## CLI Options (Global)

Override configuration via CLI options:

```bash
pki --api-url "https://pki.example.com/api/v1" \
    --oidc-url "https://iam.example.com/realms/pki/protocol/openid-connect/token" \
    --client-id "my-client" \
    --client-secret "my-secret" \
    ca list
```

Or via environment variables:

```bash
export PKI_API_URL="https://pki.example.com/api/v1"
export PKI_OIDC_URL="https://iam.example.com/realms/pki/protocol/openid-connect/token"
export PKI_CLIENT_ID="my-client"
export PKI_CLIENT_SECRET="my-secret"
pki ca list
```

## Examples

### Create CA and Issue Certificate

```bash
# Create a CA
CA_ID=$(pki ca create --cn "Internal CA" --org "MyOrg" --country ES -o json | jq -r '.id')
echo "Created CA: $CA_ID"

# Issue a server certificate
pki cert issue --ca "$CA_ID" --cn "web.internal" --type server \
    --dns "www.internal" --dns "api.internal"
```

### Renew Expiring Certificates

```bash
# Renew all certificates expiring soon
for id in $(pki expiring -o json | jq -r '.[].id'); do
    echo "Renewing certificate: $id"
    pki cert renew "$id"
done
```

### Export Certificate for Nginx

```bash
# Download as PEM (includes cert, key, and chain)
pki cert download <CERT_ID> -o /etc/nginx/ssl/mysite.pem
```

### Export Certificate for Java Application

```bash
# Download as JKS
pki cert download <CERT_ID> -f jks -p changeit -o /opt/app/keystore.jks
```

## Public Endpoints (No Auth Required)

These endpoints don't require authentication:

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /api/docs` | Swagger UI |
| `GET /api/v1/openapi.json` | OpenAPI spec (JSON) |
| `GET /api/v1/openapi.yaml` | OpenAPI spec (YAML) |
| `GET /cas/{caId}.pem` | Download CA certificate |
| `GET /crl/{caId}.crl` | Download CRL |

```bash
# Download CA certificate (no auth)
curl -s "https://pki.example.com/cas/{caId}.pem" -o ca.pem

# Download CRL
curl -s "https://pki.example.com/crl/{caId}.crl" -o crl.der
```

## Revocation Reasons

Valid reasons for `--reason` option:
- `unspecified`
- `keyCompromise`
- `caCompromise`
- `affiliationChanged`
- `superseded`
- `cessationOfOperation`
- `certificateHold`
- `removeFromCRL`
- `privilegeWithdrawn`
- `aaCompromise`

## Quick Reference

| Operation | Command |
|-----------|---------|
| List CAs | `pki ca list` |
| Create CA | `pki ca create --cn "Name" --org "Org" --country XX` |
| Get CA | `pki ca get <id>` |
| Revoke CA | `pki ca revoke <id> --reason <reason>` |
| Delete CA | `pki ca delete <id> -f` |
| List Certs | `pki cert list` |
| Issue Cert | `pki cert issue --ca <id> --cn "name" --type server` |
| Get Cert | `pki cert get <id>` |
| Download | `pki cert download <id> -f pem` |
| Renew | `pki cert renew <id>` |
| Revoke Cert | `pki cert revoke <id> --reason <reason>` |
| Delete Cert | `pki cert delete <id> -f` |
| Stats | `pki stats` |
| Expiring | `pki expiring` |
| Search | `pki search "query"` |
