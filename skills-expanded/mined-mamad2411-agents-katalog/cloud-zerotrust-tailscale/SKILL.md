---
name: cloud-zerotrust-tailscale
description: "Cloud Zerotrust Tailscale."
domain: cybersecurity
---

apiVersion: apps/v1
kind: DaemonSet
metadata:
  namespace: tailscale
spec:
  selector:
    matchLabels:
      app: tailscale
  template:
    metadata:
      labels:
        app: tailscale
    spec:
      containers:
      - name: tailscale
        image: tailscale/tailscale:latest
        env:
        - name: TS_AUTHKEY
          valueFrom:
            secretKeyRef:
              key: TS_AUTHKEY
        - name: TS_KUBE_SECRET
          value: tailscale-state
        - name: TS_USERSPACE
          value: "true"
        securityContext:
          capabilities:
            add: ["NET_ADMIN"]
```

## Access Control Lists (ACLs)

Tailscale ACLs define who can access what within your tailnet using a declarative JSON format. The default policy is deny-all, making it zero trust by design.

```json
{
  "acls": [
    // Engineering team can access development servers
    {
      "action": "accept",
      "src": ["group:engineering"],
      "dst": ["tag:dev-server:*"]
    },
    // SRE team can access production infrastructure
    {
      "action": "accept",
      "src": ["group:sre"],
      "dst": ["tag:production:22,443,8080"]
    },
    // Database access restricted to backend services
    {
      "action": "accept",
      "src": ["tag:backend"],
      "dst": ["tag:database:5432,3306,27017"]
    },
    // All employees can access internal tools
    {
      "action": "accept",
      "src": ["group:employees"],
      "dst": ["tag:internal-tools:443"]
    }
  ],

  "groups": {
    "group:engineering": ["user@company.com", "dev@company.com"],
    "group:sre": ["sre@company.com", "oncall@company.com"],
    "group:employees": ["autogroup:members"]
  },

  "tagOwners": {
    "tag:dev-server": ["group:engineering"],
    "tag:production": ["group:sre"],
    "tag:backend": ["group:sre"],
    "tag:database": ["group:sre"],
    "tag:internal-tools": ["group:sre"],
    "tag:container": ["group:sre"]
  },

  "ssh": [
    {
      "action": "check",
      "src": ["group:sre"],
      "dst": ["tag:production"],
      "users": ["root", "admin"]
    },
    {
      "action": "accept",
      "src": ["group:engineering"],
      "dst": ["tag:dev-server"],
      "users": ["autogroup:nonroot"]
    }
  ],

  "nodeAttrs": [
    {
      "target": ["autogroup:members"],
      "attr": ["funnel:deny"]
    }
  ]
}
```

## Exit Nodes and Subnet Routing

### Configure Exit Node

```bash
# On the exit node machine
sudo tailscale up --advertise-exit-node

# On the client machine, use the exit node
sudo tailscale up --exit-node=<exit-node-ip>

# Verify exit node routing
curl ifconfig.me  # Should show exit node's public IP
```

### Subnet Router Configuration

```bash
# Advertise local subnets through Tailscale
sudo tailscale up --advertise-routes=10.0.0.0/24,192.168.1.0/24

# Enable IP forwarding on Linux
echo 'net.ipv4.ip_forward = 1' | sudo tee -a /etc/sysctl.conf
echo 'net.ipv6.conf.all.forwarding = 1' | sudo tee -a /etc/sysctl.conf
sudo sysctl -p

# Accept routes on client
sudo tailscale up --accept-routes
```

## Tailscale SSH (Zero Trust SSH)

Tailscale SSH replaces traditional SSH key management with identity-based access.

```bash
# Enable Tailscale SSH on a server
sudo tailscale up --ssh

# Connect using Tailscale SSH (no SSH keys needed)
ssh user@hostname  # Authenticates via Tailscale identity

# Session recording (audit logging)
# Configure in ACL policy:
# "ssh": [{"action": "check", "src": [...], "dst": [...], "users": [...]}]
# "check" action requires re-authentication and records sessions
```

## MagicDNS Configuration

```bash
# MagicDNS is enabled by default in new tailnets
# Access devices by hostname instead of IP
ping my-server  # Resolves via MagicDNS

# Custom DNS configuration via admin console
# Split DNS: route specific domains to internal DNS servers
# Global nameservers: override default DNS resolution
```

## Self-Hosted with Headscale

```bash
# Install Headscale (open-source Tailscale control server)
wget https://github.com/juanfont/headscale/releases/latest/download/headscale_linux_amd64
chmod +x headscale_linux_amd64
sudo mv headscale_linux_amd64 /usr/local/bin/headscale

# Create configuration
sudo mkdir -p /etc/headscale
sudo headscale generate config > /etc/headscale/config.yaml

# Edit config for your environment
# Key settings:
#   server_url: https://headscale.example.com
#   listen_addr: 0.0.0.0:8080
#   private_key_path: /etc/headscale/private.key
#   db_type: sqlite3
#   db_path: /var/libs/headscale/db.sqlite

# Start Headscale
sudo headscale serve

# Create user and pre-auth key
headscale users create myorg
headscale preauthkeys create --user myorg --reusable --expiration 24h

# Connect Tailscale client to Headscale
tailscale up --login-server https://headscale.example.com
```

## Security Hardening

### Key Expiry and Rotation

```bash
# Set key expiry in admin console (default: 180 days)
# Force re-authentication periodically

# Disable key expiry for servers (use auth keys instead)
sudo tailscale up --authkey=tskey-auth-xxxxx

# Pre-auth keys for automated deployment
# Create ephemeral, single-use keys for CI/CD
```

### Device Authorization

```json
{
  "nodeAttrs": [
    {
      "target": ["autogroup:members"],
      "attr": [
        "mullvad:deny",
        "funnel:deny"
      ]
    }
  ],
  "autoApprovers": {
    "routes": {
      "10.0.0.0/24": ["group:sre"],
      "192.168.0.0/16": ["group:sre"]
    },
    "exitNode": ["group:sre"]
  }
}
```

### Network Lock (Tailnet Lock)

```bash
# Initialize network lock with signing keys
tailscale lock init

# Add trusted signing keys
tailscale lock add nodekey:xxxxx

# All new nodes require signing before joining
# Prevents unauthorized nodes from joining the tailnet
```

## Monitoring and Observability

```bash
# View network status
tailscale status --json | jq '.Peer | to_entries[] | {name: .value.HostName, online: .value.Online, os: .value.OS}'

# Check connection quality
tailscale ping <peer-ip>

# View network map
tailscale netcheck

# Audit logs available in Tailscale admin console
# Integration with SIEM via webhook or API
```

## Integration Patterns

### Service Mesh Integration

```bash
# Tailscale as sidecar for service-to-service communication
# Each service gets a Tailscale identity
# ACLs enforce service-to-service access policies

# Example: API service can only reach database service
# ACL: tag:api -> tag:database:5432
```

### CI/CD Pipeline Integration

```bash
# Use ephemeral auth keys in CI/CD
export TS_AUTHKEY=tskey-auth-xxxxx-ephemeral
tailscale up --authkey=$TS_AUTHKEY --hostname=ci-runner-$CI_JOB_ID

# Access internal resources during build/deploy
# Node automatically removed when container stops
```

## References

- [Tailscale Documentation](https://tailscale.com/kb/)
- [How Tailscale Works](https://tailscale.com/blog/how-tailscale-works)
- [Tailscale ACL Documentation](https://tailscale.com/kb/1018/acls/)
- [Headscale - Open Source Control Server](https://github.com/juanfont/headscale)
- [WireGuard Protocol](https://www.wireguard.com/protocol/)
- [Tailscale SSH](https://tailscale.com/kb/1193/tailscale-ssh/)
