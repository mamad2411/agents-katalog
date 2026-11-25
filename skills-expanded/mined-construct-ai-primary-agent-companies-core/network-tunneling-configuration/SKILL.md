---
name: network-tunneling-configuration
description: >
  Use this skill when the task involves setting up secure network tunnels for desktop-to-cloud communication,
  configuring ngrok, Tailscale, or Cloudflare Tunnel, or establishing secure connectivity between local
  and cloud environments.
  
  Use when: Desktop applications need secure access to cloud deployments; ngrok tunnels require setup;
  Tailscale mesh networking needs configuration; Cloudflare Tunnel needs establishment; secure remote
  access to cloud services is required.
  
  Don't use when: The task is about Hermes agent communication setup (use hermes-communication-setup instead);
  the task requires general environment variable access (use environment-variable-access instead).
agent: render-deployment-specialist
company: infraforge-ai
category: infrastructure
---

# Network Tunneling Configuration Skill

## Overview

The Network Tunneling Configuration skill enables the Render Deployment Specialist agent to set up and manage secure network tunnels for desktop-to-cloud communication. This skill covers ngrok, Tailscale, Cloudflare Tunnel, and other tunneling solutions to establish secure, reliable connectivity between local development environments and cloud deployments.

## Capabilities

### ngrok Configuration
- **Tunnel Setup**: Configure secure tunnels to local services
- **Authentication**: Set up ngrok authentication and access control
- **Custom Domains**: Configure custom domains and SSL certificates
- **Traffic Inspection**: Set up request/response inspection and logging

### Tailscale Integration
- **Mesh Networking**: Configure zero-trust mesh networking
- **Device Management**: Manage device registration and access control
- **Subnet Routing**: Set up subnet routers for network access
- **ACL Configuration**: Configure access control lists and policies

### Cloudflare Tunnel
- **Tunnel Creation**: Set up Cloudflare tunnels for secure access
- **DNS Configuration**: Configure DNS records for tunnel endpoints
- **Access Policies**: Set up access policies and authentication
- **Performance Optimization**: Optimize tunnel performance and reliability

### Alternative Tunneling Solutions
- **SSH Tunneling**: Configure SSH-based port forwarding
- **VPN Setup**: Establish VPN connections for secure access
- **WireGuard**: Configure WireGuard tunnels for peer-to-peer networking
- **LocalTunnel**: Set up localtunnel for development testing

## Common Patterns

### ngrok Tunnel Setup
```bash
#!/bin/bash
set -euo pipefail

# Configuration
LOCAL_PORT="${LOCAL_PORT:-8000}"
SUBDOMAIN="${SUBDOMAIN:-paperclip-dev}"
REGION="${REGION:-us}"

# Install ngrok if not present
if ! command -v ngrok &> /dev/null; then
  echo "Installing ngrok..."
  curl -s https://ngrok-agent.s3.amazonaws.com/ngrok.asc | sudo tee /etc/apt/trusted.gpg.d/ngrok.asc >/dev/null
  echo "deb https://ngrok-agent.s3.amazonaws.com buster main" | sudo tee /etc/apt/sources.list.d/ngrok.list
  sudo apt update && sudo apt install ngrok
fi

# Authenticate ngrok
if [[ -n "${NGROK_AUTH_TOKEN:-}" ]]; then
  ngrok config add-authtoken "$NGROK_AUTH_TOKEN"
fi

# Start tunnel
echo "Starting ngrok tunnel on port $LOCAL_PORT..."
ngrok http "$LOCAL_PORT" \
  --subdomain="$SUBDOMAIN" \
  --region="$REGION" \
  --log=stdout \
  --log-format=json &

NGROK_PID=$!

# Wait for tunnel to be ready
echo "Waiting for ngrok tunnel to be ready..."
sleep 5

# Get tunnel URL
TUNNEL_URL=$(curl -s http://localhost:4040/api/tunnels | jq -r '.tunnels[0].public_url')

if [[ -z "$TUNNEL_URL" ]]; then
  echo "ERROR: Failed to get tunnel URL"
  kill "$NGROK_PID" 2>/dev/null || true
  exit 1
fi

echo "Tunnel established: $TUNNEL_URL"
echo "Local service: http://localhost:$LOCAL_PORT"
echo "Press Ctrl+C to stop tunnel"

# Keep tunnel alive
wait "$NGROK_PID"
```

### Tailscale Mesh Network Setup
```bash
#!/bin/bash
set -euo pipefail

# Configuration
TAILSCALE_AUTH_KEY="${TAILSCALE_AUTH_KEY}"
TAILSCALE_HOSTNAME="${TAILSCALE_HOSTNAME:-paperclip-dev}"
TAILSCALE_ADVERTISE_ROUTES="${TAILSCALE_ADVERTISE_ROUTES:-192.168.1.0/24}"

# Install Tailscale
if ! command -v tailscale &> /dev/null; then
  echo "Installing Tailscale..."
  curl -fsSL https://tailscale.com/install.sh | sh
fi

# Start Tailscale
echo "Starting Tailscale..."
sudo tailscale up \
  --auth-key="$TAILSCALE_AUTH_KEY" \
  --hostname="$TAILSCALE_HOSTNAME" \
  --advertise-routes="$TAILSCALE_ADVERTISE_ROUTES" \
  --accept-dns=true \
  --accept-routes=true

# Wait for connection
echo "Waiting for Tailscale connection..."
sleep 10

# Get Tailscale IP
TAILSCALE_IP=$(tailscale ip -4)
echo "Tailscale IP: $TAILSCALE_IP"

# Configure firewall if needed
sudo ufw allow in on tailscale0
sudo ufw --force enable

echo "Tailscale mesh network configured"
echo "Access your services via: $TAILSCALE_IP"
```

### Cloudflare Tunnel Configuration
```bash
#!/bin/bash
set -euo pipefail

# Configuration
CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN}"
CLOUDFLARE_ZONE_ID="${CLOUDFLARE_ZONE_ID}"
TUNNEL_NAME="${TUNNEL_NAME:-paperclip-tunnel}"
DOMAIN="${DOMAIN:-paperclip-dev.yourdomain.com}"
LOCAL_SERVICE="${LOCAL_SERVICE:-http://localhost:8000}"

# Install cloudflared
if ! command -v cloudflared &> /dev/null; then
  echo "Installing cloudflared..."
  wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
  sudo dpkg -i cloudflared-linux-amd64.deb
  rm cloudflared-linux-amd64.deb
fi

# Login to Cloudflare
echo "Authenticating with Cloudflare..."
cloudflared tunnel login

# Create tunnel
echo "Creating Cloudflare tunnel..."
TUNNEL_ID=$(cloudflared tunnel create "$TUNNEL_NAME" | grep -oP 'Created tunnel \K.*(?= with id)')

if [[ -z "$TUNNEL_ID" ]]; then
  echo "ERROR: Failed to create tunnel"
  exit 1
fi

echo "Tunnel created with ID: $TUNNEL_ID"

# Create DNS record
echo "Creating DNS record..."
cloudflared tunnel route dns "$TUNNEL_NAME" "$DOMAIN"

# Configure tunnel
cat > /tmp/tunnel-config.yaml << EOF
tunnel: $TUNNEL_ID
credentials-file: /root/.cloudflared/$TUNNEL_ID.json

ingress:
  - hostname: $DOMAIN
    service: $LOCAL_SERVICE
  - service: http_status:404
EOF

# Start tunnel
echo "Starting Cloudflare tunnel..."
cloudflared tunnel --config /tmp/tunnel-config.yaml run "$TUNNEL_NAME" &

TUNNEL_PID=$!

# Wait for tunnel to be ready
echo "Waiting for tunnel to be ready..."
sleep 10

# Test tunnel
if curl -f "https://$DOMAIN" > /dev/null 2>&1; then
  echo "SUCCESS: Tunnel is working at https://$DOMAIN"
else
  echo "WARNING: Tunnel may not be ready yet"
fi

echo "Cloudflare tunnel configured"
echo "Access your service at: https://$DOMAIN"
echo "Press Ctrl+C to stop tunnel"

# Keep tunnel alive
wait "$TUNNEL_PID"
```

### SSH Tunnel Setup
```bash
#!/bin/bash
set -euo pipefail

# Configuration
REMOTE_HOST="${REMOTE_HOST:-your-server.com}"
REMOTE_USER="${REMOTE_USER:-ubuntu}"
LOCAL_PORT="${LOCAL_PORT:-8000}"
REMOTE_PORT="${REMOTE_PORT:-80}"
SSH_KEY_PATH="${SSH_KEY_PATH:-~/.ssh/id_rsa}"

# Establish SSH tunnel
echo "Establishing SSH tunnel..."
echo "Local port $LOCAL_PORT -> $REMOTE_HOST:$REMOTE_PORT via SSH"

ssh -i "$SSH_KEY_PATH" \
  -o StrictHostKeyChecking=no \
  -o UserKnownHostsFile=/dev/null \
  -o LogLevel=ERROR \
  -N \
  -L "$LOCAL_PORT:localhost:$REMOTE_PORT" \
  "$REMOTE_USER@$REMOTE_HOST"

echo "SSH tunnel established"
echo "Access remote service at: http://localhost:$LOCAL_PORT"
```

## Security Configuration

### Access Control
- **Authentication**: Configure proper authentication for tunnel access
- **IP Whitelisting**: Restrict access to specific IP ranges
- **Rate Limiting**: Implement rate limiting to prevent abuse
- **Audit Logging**: Log all tunnel access and usage

### Encryption
- **TLS Termination**: Ensure proper TLS termination at tunnel endpoints
- **Certificate Management**: Manage SSL certificates for custom domains
- **End-to-End Encryption**: Implement end-to-end encryption where possible
- **Key Management**: Securely manage encryption keys and credentials

### Network Security
- **Firewall Rules**: Configure firewall rules for tunnel traffic
- **Network Segmentation**: Isolate tunnel traffic from other network segments
- **Intrusion Detection**: Monitor for suspicious tunnel activity
- **Regular Updates**: Keep tunneling software updated with security patches

## Monitoring and Troubleshooting

### Tunnel Health Monitoring
```bash
#!/bin/bash
# Monitor tunnel connectivity and performance

TUNNEL_TYPE="${1:-ngrok}"
SERVICE_URL="${SERVICE_URL:-http://localhost:8000}"

case "$TUNNEL_TYPE" in
  "ngrok")
    # Check ngrok tunnel status
    TUNNEL_INFO=$(curl -s http://localhost:4040/api/tunnels)
    if [[ $? -eq 0 ]]; then
      PUBLIC_URL=$(echo "$TUNNEL_INFO" | jq -r '.tunnels[0].public_url')
      echo "ngrok tunnel active: $PUBLIC_URL"
    else
      echo "ERROR: ngrok tunnel not accessible"
      exit 1
    fi
    ;;

  "tailscale")
    # Check Tailscale status
    if tailscale status > /dev/null 2>&1; then
      TAILSCALE_IP=$(tailscale ip -4)
      echo "Tailscale active: $TAILSCALE_IP"
    else
      echo "ERROR: Tailscale not connected"
      exit 1
    fi
    ;;

  "cloudflare")
    # Check Cloudflare tunnel
    if pgrep -f cloudflared > /dev/null; then
      echo "Cloudflare tunnel process running"
    else
      echo "ERROR: Cloudflare tunnel not running"
      exit 1
    fi
    ;;
esac

# Test service connectivity
if curl -f --max-time 10 "$SERVICE_URL" > /dev/null 2>&1; then
  echo "Service is accessible"
else
  echo "ERROR: Service not accessible through tunnel"
  exit 1
fi

echo "Tunnel health check passed"
```

### Common Troubleshooting

#### ngrok Issues
1. **Authentication Problems**
   ```bash
   # Re-authenticate ngrok
   ngrok config add-authtoken "$NGROK_AUTH_TOKEN"
   ```

2. **Port Conflicts**
   ```bash
   # Check if port is already in use
   netstat -tlnp | grep ":$LOCAL_PORT"
   ```

3. **Rate Limiting**
   ```bash
   # Check ngrok account limits
   curl -H "Authorization: Bearer $NGROK_API_KEY" \
     https://api.ngrok.com/accounts/$NGROK_ACCOUNT_ID/requests
   ```

#### Tailscale Issues
1. **Connection Problems**
   ```bash
   # Check Tailscale status
   sudo tailscale status
   sudo tailscale ping "$TARGET_HOST"
   ```

2. **ACL Configuration**
   ```bash
   # Check ACL configuration
   sudo tailscale lock status
   ```

3. **Network Issues**
   ```bash
   # Restart Tailscale
   sudo systemctl restart tailscaled
   ```

#### Cloudflare Issues
1. **DNS Propagation**
   ```bash
   # Check DNS resolution
   dig "$DOMAIN"
   ```

2. **Certificate Issues**
   ```bash
   # Check certificate status
   openssl s_client -connect "$DOMAIN:443" -servername "$DOMAIN"
   ```

3. **Tunnel Connectivity**
   ```bash
   # Check tunnel logs
   journalctl -u cloudflared -f
   ```

## Performance Optimization

### Bandwidth Management
- **Compression**: Enable compression for tunnel traffic
- **Caching**: Implement caching to reduce tunnel traffic
- **Connection Pooling**: Use connection pooling for better performance
- **Load Balancing**: Distribute traffic across multiple tunnel instances

### Latency Reduction
- **Geographic Selection**: Choose tunnel endpoints closest to users
- **Protocol Optimization**: Use optimized protocols for low latency
- **Connection Reuse**: Reuse connections to reduce handshake overhead
- **Traffic Shaping**: Implement traffic shaping for consistent performance

## Integration Points

### Internal InfraForge AI
- **Security Agent**: Coordinates security configuration for tunnels
- **Monitoring Agent**: Integrates with tunnel monitoring systems
- **Network Agent**: Works with network configuration and optimization

### Cross-Company Integration
- **DevForge AI**: Collaborates on development environment tunneling
- **PaperclipForge AI**: Works with project access requirements
- **QualityForge AI**: Partners on tunnel testing and validation

## Success Metrics

- **Tunnel Uptime**: ≥99.5% tunnel availability
- **Connection Success**: ≥98% successful tunnel establishments
- **Security Compliance**: 100% secure tunnel configurations
- **Performance Standards**: <100ms average latency for tunnel traffic

---

**Skill Level**: Expert
**Last Updated**: 2026-04-23
**Version**: 1.0
