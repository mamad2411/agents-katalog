---
name: openclaw-wechat-integration
description: Connect OpenClaw AI agents to personal WeChat accounts for messaging, group chats, and automation
triggers:
  - how do I connect OpenClaw to WeChat
  - set up WeChat channel for OpenClaw
  - configure openclaw-wechat plugin
  - integrate WeChat with my AI bot
  - troubleshoot OpenClaw WeChat connection
  - handle WeChat messages in OpenClaw
  - deploy OpenClaw WeChat on cloud server
  - manage multiple WeChat accounts in OpenClaw
---

# openclaw-wechat-integration

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

This skill provides expertise in using the openclaw-wechat plugin to connect OpenClaw AI agents to personal WeChat accounts, enabling automated messaging, group chat interactions, and multi-account management.

## What It Does

openclaw-wechat is a WeChat channel plugin for OpenClaw that enables:
- Direct messages and group chat support
- Text and image message handling
- QR code login authentication
- Multi-account WeChat bot management
- Webhook-based message receiving
- Cloud server deployment compatibility

## Installation

### Install the Plugin

```bash
openclaw plugins install @canghe/openclaw-wechat
```

### Update Existing Installation

```bash
openclaw plugins update wechat
```

## Core Configuration

### Required Configuration Steps

1. **Set API Key** (obtain from project community):
```bash
openclaw config set channels.wechat.apiKey "wc_live_xxxxxxxxxxxxxxxx"
```

2. **Set Proxy URL** (required for WeChat protocol handling):
```bash
openclaw config set channels.wechat.proxyUrl "http://your-proxy-server:3000"
```

3. **Set Webhook Host** (required for cloud deployment):
```bash
openclaw config set channels.wechat.webhookHost "your-server-ip"
```

4. **Enable the Channel**:
```bash
openclaw config set channels.wechat.enabled true
```

### Configuration File Structure

The configuration is stored in `~/.openclaw/openclaw.json`:

```json
{
  "channels": {
    "wechat": {
      "enabled": true,
      "apiKey": "wc_live_xxxxxxxxxxxxxxxx",
      "proxyUrl": "http://your-proxy:3000",
      "webhookHost": "1.2.3.4",
      "webhookPort": 18790,
      "webhookPath": "/webhook/wechat",
      "deviceType": "ipad"
    }
  }
}
```

### Configuration Options Reference

| Option | Required | Default | Description |
|--------|----------|---------|-------------|
| `enabled` | Yes | `false` | Enable/disable the WeChat channel |
| `apiKey` | Yes | - | API key from service provider |
| `proxyUrl` | Yes | - | Proxy service URL for WeChat protocol |
| `webhookHost` | Cloud only | - | Public IP or domain for webhooks |
| `webhookPort` | No | `18790` | Port for webhook listener |
| `webhookPath` | No | `/webhook/wechat` | Webhook endpoint path |
| `deviceType` | No | `"ipad"` | Device type: `"ipad"` or `"mac"` |

## First-Time Login

### QR Code Authentication

Start the gateway to initiate login:

```bash
openclaw gateway start
```

The terminal will display a QR code. Scan it with your WeChat mobile app to authenticate.

### Verify Connection

```bash
openclaw gateway status
```

Check logs for connection status:

```bash
openclaw gateway logs
```

## Multi-Account Configuration

### Managing Multiple WeChat Accounts

Configure multiple accounts with distinct API keys:

```json
{
  "channels": {
    "wechat": {
      "accounts": {
        "work": {
          "apiKey": "wc_live_work_xxx",
          "webhookHost": "1.2.3.4",
          "webhookPort": 18790,
          "deviceType": "ipad"
        },
        "personal": {
          "apiKey": "wc_live_personal_xxx",
          "webhookHost": "1.2.3.4",
          "webhookPort": 18791,
          "deviceType": "mac"
        }
      }
    }
  }
}
```

**Important**: Each account must use a unique `webhookPort` to avoid conflicts.

## Message Handling Patterns

### Receiving Messages

The plugin automatically receives messages via webhooks. Ensure your webhook endpoint is accessible:

```typescript
// OpenClaw automatically handles incoming messages
// Configure message handlers in your OpenClaw skills

// Example skill handler (conceptual)
export async function onMessage(context: MessageContext) {
  const { message, channel } = context;
  
  if (channel === 'wechat') {
    console.log('WeChat message:', message.text);
    console.log('From:', message.sender);
    console.log('Chat type:', message.isGroup ? 'group' : 'private');
  }
}
```

### Sending Messages

When building OpenClaw skills that send WeChat messages:

```typescript
// Example: Sending a text message
await context.send({
  channel: 'wechat',
  to: 'wxid_xxxxxxxxxx',
  text: 'Hello from OpenClaw!'
});

// Example: Sending to a group
await context.send({
  channel: 'wechat',
  to: 'group_id',
  text: 'Message to group',
  isGroup: true
});
```

### Image Message Handling

```typescript
// Receiving images
export async function onMessage(context: MessageContext) {
  if (context.message.type === 'image') {
    const imageUrl = context.message.imageUrl;
    // Process image
  }
}

// Sending images
await context.send({
  channel: 'wechat',
  to: 'wxid_xxxxxxxxxx',
  type: 'image',
  imageUrl: 'https://example.com/image.png'
});
```

## Cloud Server Deployment

### Network Requirements

1. **Open Webhook Port**: Ensure firewall allows incoming connections:
```bash
# Example: UFW on Ubuntu
sudo ufw allow 18790/tcp
```

2. **Verify Public Accessibility**:
```bash
# Test from external machine
curl http://YOUR_SERVER_IP:18790/webhook/wechat
```

### Systemd Service Setup

Create `/etc/systemd/system/openclaw-gateway.service`:

```ini
[Unit]
Description=OpenClaw Gateway Service
After=network.target

[Service]
Type=simple
User=YOUR_USER
WorkingDirectory=/home/YOUR_USER
ExecStart=/usr/local/bin/openclaw gateway start
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable openclaw-gateway
sudo systemctl start openclaw-gateway
sudo systemctl status openclaw-gateway
```

### Docker Deployment

```dockerfile
FROM node:18-alpine

WORKDIR /app

# Install OpenClaw
RUN npm install -g openclaw

# Install plugin
RUN openclaw plugins install @canghe/openclaw-wechat

# Expose webhook port
EXPOSE 18790

# Configure via environment
ENV OPENCLAW_CONFIG_PATH=/app/config/openclaw.json

CMD ["openclaw", "gateway", "start"]
```

## Troubleshooting

### Bot Cannot Receive Messages

**Symptoms**: Gateway starts but no messages arrive.

**Solutions**:

1. **Verify webhook host configuration**:
```bash
openclaw config get channels.wechat.webhookHost
# Should return your public IP
```

2. **Check port accessibility**:
```bash
# From external network
telnet YOUR_SERVER_IP 18790
```

3. **Verify gateway is running**:
```bash
openclaw gateway status
```

4. **Check webhook logs**:
```bash
openclaw gateway logs --tail 100
```

5. **Test webhook endpoint**:
```bash
curl -X POST http://YOUR_SERVER_IP:18790/webhook/wechat \
  -H "Content-Type: application/json" \
  -d '{"test": true}'
```

### QR Code Not Displaying

**Symptoms**: Gateway starts but no QR code appears.

**Solutions**:

1. **Check proxy URL connectivity**:
```bash
curl http://your-proxy-server:3000/health
```

2. **Verify API key is valid**:
```bash
openclaw config get channels.wechat.apiKey
```

3. **Clear session cache**:
```bash
rm -rf ~/.openclaw/sessions/wechat
openclaw gateway restart
```

### Login Expired

**Symptoms**: Bot stops responding, shows login errors.

**Solutions**:

1. **Restart gateway to get new QR code**:
```bash
openclaw gateway restart
```

2. **Scan QR code again with WeChat**

3. **Check WeChat account status** (ensure not blocked)

### Multiple Accounts Port Conflict

**Symptoms**: Second account fails to start.

**Solution**: Ensure each account has a unique `webhookPort`:

```json
{
  "channels": {
    "wechat": {
      "accounts": {
        "account1": {
          "webhookPort": 18790
        },
        "account2": {
          "webhookPort": 18791
        }
      }
    }
  }
}
```

### Proxy Connection Issues

**Symptoms**: Cannot connect to proxy server.

**Solutions**:

1. **Verify proxy is running**:
```bash
curl http://your-proxy-server:3000
```

2. **Check network connectivity**:
```bash
ping your-proxy-server
```

3. **Update proxy URL**:
```bash
openclaw config set channels.wechat.proxyUrl "http://new-proxy:3000"
```

## Common Commands

```bash
# View current configuration
openclaw config list

# Start gateway in foreground
openclaw gateway start

# Start gateway in background
openclaw gateway start --daemon

# Stop gateway
openclaw gateway stop

# Restart gateway
openclaw gateway restart

# View logs
openclaw gateway logs

# View real-time logs
openclaw gateway logs --follow

# Check gateway status
openclaw gateway status

# Uninstall plugin
openclaw plugins uninstall wechat
```

## Best Practices

1. **Security**: Store API keys in environment variables:
```bash
export WECHAT_API_KEY="wc_live_xxxxxxxxxxxxxxxx"
openclaw config set channels.wechat.apiKey "$WECHAT_API_KEY"
```

2. **Monitoring**: Set up log rotation for production:
```bash
openclaw config set logging.rotation.enabled true
openclaw config set logging.rotation.maxSize "100M"
```

3. **Backup**: Regularly backup session data:
```bash
tar -czf openclaw-backup-$(date +%Y%m%d).tar.gz ~/.openclaw/sessions
```

4. **Firewall**: Only expose webhook port, not entire server:
```bash
sudo ufw default deny incoming
sudo ufw allow 18790/tcp
sudo ufw enable
```

5. **Health Checks**: Implement automated restarts on failure when using systemd (see service configuration above).
