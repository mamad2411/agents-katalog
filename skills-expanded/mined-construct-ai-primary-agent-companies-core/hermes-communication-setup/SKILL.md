---
name: hermes-communication-setup
description: >
  Use this skill when the task involves setting up Hermes agent communication channels, configuring HERMES_MODE=both
  for dual CLI/gateway operation, establishing secure API connections between desktop and cloud deployments,
  or troubleshooting Hermes agent integration issues.
  
  Use when: Hermes agent needs to be configured for desktop communication; HERMES_MODE=both setup is required;
  API server crashes silently on startup; webhook endpoints need configuration; secure communication channels
  between desktop and cloud need establishment.
  
  Don't use when: The task is about general environment variable access (use environment-variable-access instead);
  the task requires network tunneling without Hermes (use network-tunneling-configuration instead).
agent: render-deployment-specialist
company: infraforge-ai
category: infrastructure
---

# Hermes Communication Setup Skill

## Overview

The Hermes Communication Setup skill enables the Render Deployment Specialist agent to effectively configure and troubleshoot Hermes agent communication channels, particularly for desktop-to-cloud integration. This skill covers HERMES_MODE=both configuration, API server setup, webhook integration, and secure communication protocols.

## Capabilities

### Hermes Mode Configuration
- **CLI Mode Setup**: Configure Hermes for command-line interface operation
- **Gateway Mode Setup**: Configure Hermes for multi-platform messaging integration
- **Both Mode Setup**: Configure dual CLI and gateway functionality (HERMES_MODE=both)
- **Mode Switching**: Switch between different Hermes operational modes

### API Server Configuration
- **Server Startup**: Configure hermes serve command with proper parameters
- **Port Configuration**: Set up correct host and port bindings (0.0.0.0:8000)
- **Health Endpoints**: Configure /health endpoint for monitoring
- **Error Handling**: Set up proper error responses and logging

### Webhook Integration
- **Webhook Endpoints**: Configure webhook URLs for external integrations
- **Authentication**: Set up webhook authentication and security
- **Event Handling**: Configure webhook event types and processing
- **Retry Logic**: Implement webhook retry and failure handling

### Desktop Communication
- **Secure Channels**: Establish encrypted communication between desktop and cloud
- **Authentication**: Configure API key authentication for desktop access
- **Session Management**: Manage persistent communication sessions
- **Real-time Updates**: Set up real-time communication protocols

## Common Patterns

### HERMES_MODE=both Configuration
```bash
# Environment variables for dual mode operation
HERMES_MODE=both
HERMES_PUBLIC_URL=https://your-app.onrender.com
HERMES_WEBHOOK_SECRET=whsec_secure_random_key
HERMES_API_KEY=pk_hermes_secure_key

# API server configuration
API_HOST=0.0.0.0
API_PORT=8000
HEALTH_CHECK_URL=http://localhost:8000/health
```

### API Server Startup Script
```bash
#!/bin/bash
set -euo pipefail

# Configuration
API_PORT="${API_PORT:-8000}"
API_HOST="${API_HOST:-0.0.0.0}"
HERMES_MODE="${HERMES_MODE:-both}"

# Log helper
log() {
  echo "[$(date -Iseconds)] [API] $1"
}

# Validate environment
if [[ -z "${OPENROUTER_API_KEY:-}" ]]; then
  log "ERROR: OPENROUTER_API_KEY is required"
  exit 1
fi

if [[ -z "${GITHUB_TOKEN:-}" ]]; then
  log "ERROR: GITHUB_TOKEN is required"
  exit 1
fi

log "Starting Hermes API server on ${API_HOST}:${API_PORT} with mode=${HERMES_MODE}"

# Start the server
exec hermes serve \
  --host "$API_HOST" \
  --port "$API_PORT" \
  --mode "$HERMES_MODE" \
  --log-level INFO \
  --enable-health-check
```

### Webhook Configuration
```json
{
  "webhooks": {
    "paperclip_integration": {
      "url": "https://your-app.onrender.com/api/webhooks/hermes",
      "events": ["deployment_success", "deployment_failure", "health_check"],
      "secret": "whsec_hermes_shared_secret",
      "headers": {
        "X-Hermes-Signature": "v1,g0hM9SsE+OTPJTGt/tmIKtSyZlE3uFJELVlNIOLJ1OE=",
        "Content-Type": "application/json"
      },
      "retry": {
        "max_attempts": 5,
        "backoff_multiplier": 2,
        "initial_delay": 1
      }
    }
  }
}
```

### Desktop Authentication Setup
```bash
# Generate secure API key for desktop access
DESKTOP_API_KEY=$(openssl rand -hex 32)
echo "Desktop API Key: pcak_desktop_${DESKTOP_API_KEY}"

# Configure desktop environment
export PAPERCLIP_API_URL=https://your-app.onrender.com
export PAPERCLIP_API_KEY=pcak_desktop_${DESKTOP_API_KEY}
export HERMES_DESKTOP_MODE=true
```

## Troubleshooting Common Issues

### API Server Silent Crash
When the API server starts but crashes immediately with no logs:

1. **Check Required Environment Variables**
   ```bash
   # Verify all required vars are set
   env | grep -E '^(OPENROUTER_API_KEY|GITHUB_TOKEN|HERMES_MODE)'
   ```

2. **Test Server Command Manually**
   ```bash
   # Run the server command directly to see errors
   hermes serve --host 0.0.0.0 --port 8000 --mode both
   ```

3. **Check Port Availability**
   ```bash
   # Ensure port 8000 is not already in use
   netstat -tlnp | grep :8000 || echo "Port 8000 is available"
   ```

4. **Validate Hermes Installation**
   ```bash
   # Check if hermes command is available
   which hermes && hermes --version
   ```

### Webhook Delivery Failures
When webhooks are not being delivered to endpoints:

1. **Verify Webhook URLs**
   ```bash
   # Test webhook endpoint accessibility
   curl -X POST https://your-app.onrender.com/api/webhooks/hermes \
     -H "Content-Type: application/json" \
     -d '{"test": "webhook"}'
   ```

2. **Check Authentication**
   ```bash
   # Verify webhook secret is correct
   echo -n "webhook_payload" | openssl sha256 -hmac "your_webhook_secret"
   ```

3. **Review Network Policies**
   ```bash
   # Check if Render allows outbound webhook calls
   curl -I https://webhook.site/test
   ```

### Desktop Connection Issues
When desktop cannot connect to cloud deployment:

1. **Verify API Keys**
   ```bash
   # Test API key authentication
   curl https://your-app.onrender.com/api/health \
     -H "Authorization: Bearer pcak_desktop_your_key"
   ```

2. **Check Network Connectivity**
   ```bash
   # Test basic connectivity
   ping your-app.onrender.com
   ```

3. **Validate TLS/SSL**
   ```bash
   # Check SSL certificate
   openssl s_client -connect your-app.onrender.com:443 -servername your-app.onrender.com
   ```

## Security Configuration

### API Key Management
- **Key Generation**: Use cryptographically secure random generation
- **Key Storage**: Store keys securely in environment variables
- **Key Rotation**: Implement regular key rotation procedures
- **Access Logging**: Log all API key usage for audit purposes

### Communication Encryption
- **TLS Configuration**: Ensure all communication uses HTTPS/TLS
- **Certificate Validation**: Verify SSL certificates are valid and current
- **Encryption at Rest**: Encrypt sensitive data stored in databases
- **Secure Headers**: Implement security headers (HSTS, CSP, etc.)

### Authentication Protocols
- **Token-based Auth**: Use JWT or similar token-based authentication
- **Session Management**: Implement secure session handling
- **Rate Limiting**: Apply rate limiting to prevent abuse
- **IP Whitelisting**: Restrict access to known IP ranges when possible

## Integration Points

### Internal InfraForge AI
- **Database Agent**: Coordinates database connection configuration
- **Security Agent**: Works with authentication and encryption setup
- **Monitoring Agent**: Integrates with communication monitoring systems

### Cross-Company Integration
- **DevForge AI**: Collaborates on application communication requirements
- **PaperclipForge AI**: Works with project management for communication setup
- **QualityForge AI**: Partners on communication testing and validation

## Success Metrics

- **Connection Success**: ≥99% successful Hermes API server startups
- **Webhook Reliability**: ≥95% webhook delivery success rate
- **Authentication Security**: 100% secure API key implementation
- **Communication Uptime**: ≥99.5% communication channel availability

---

**Skill Level**: Expert
**Last Updated**: 2026-04-23
**Version**: 1.0
