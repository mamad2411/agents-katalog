---
name: headscale-network
description: "Deploy and manage a self-hosted Tailscale control server (Headscale) for zero-trust private networking and secure access to your stack."
metadata:
  openclaw:
    emoji: "🌐"
---

# Headscale Network

Headscale provides a self-hosted, open-source alternative to the Tailscale control server. This skill allows you to run your own private, encrypted mesh network without relying on external services or opening ports to the public internet.

## Why use Headscale?

- **Zero-Trust Access**: Connect your devices securely without exposing services directly to the internet.
- **Data Privacy**: Keep all traffic internal and within your control.
- **Seamless Integration**: Use the standard Tailscale clients on Windows, macOS, Linux, iOS, and Android to connect to your custom Headscale server.
- **Self-Hosted Control**: Retain full ownership of your network routing and authentication policies.

## Integration with OpenClaw

When using this skill with other services:
- **Tailscale Nodes**: Other services in your stack can connect to Headscale using the \`tailscale\` service container sidecars.
- **Secure Proxies**: You can route traffic to internal services securely.
- **Admin Management**: You can manage users and preauth keys from within the Headscale CLI or via a connected web UI.

## Getting Started

To connect a Tailscale client to your self-hosted Headscale instance:
1. Generate a preauth key or namespace on the Headscale server.
2. Run your Tailscale client with the \`--login-server\` flag pointing to your OpenClaw Headscale URL (e.g., \`tailscale up --login-server=https://headscale.yourdomain.com\`).
3. Follow the authentication link provided to register your machine.
