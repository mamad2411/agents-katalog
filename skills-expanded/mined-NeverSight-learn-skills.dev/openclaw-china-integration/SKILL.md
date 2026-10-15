---
name: openclaw-china-integration
description: Expert in integrating OpenClaw AI with Chinese IM platforms (DingTalk, Feishu, QQ, WeChat Work, WeChat Official Account)
triggers:
  - how do I connect OpenClaw to DingTalk
  - integrate OpenClaw with WeChat Work
  - set up OpenClaw China plugin
  - configure QQ bot with OpenClaw
  - add Feishu channel to OpenClaw
  - deploy OpenClaw to Chinese IM platforms
  - troubleshoot OpenClaw China connection
  - what Chinese messaging platforms does OpenClaw support
---

# OpenClaw China Integration Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

OpenClaw China is a comprehensive plugin collection that extends OpenClaw to support major Chinese instant messaging platforms including DingTalk (钉钉), Feishu (飞书), QQ, WeChat Work (企业微信), WeChat Official Account (微信公众号), and WeChat Customer Service (微信客服).

## What OpenClaw China Does

- **Multi-Platform Support**: Connects OpenClaw AI agents to 6+ Chinese IM platforms
- **Unified Interface**: Provides consistent message handling across different platforms
- **Rich Features**: Supports text, Markdown, images, files, voice messages, and streaming responses
- **Enterprise Ready**: Handles both internal (WeChat Work) and external (WeChat Customer Service) users
- **Low Configuration**: Simplified setup process with guided installation

## Installation

### Quick Setup (Recommended)

```bash
npx @openclaw-china/setup
```

This interactive installer will:
1. Check your OpenClaw installation
2. Guide you through platform selection
3. Generate configuration files
4. Install required dependencies

### Manual Installation

```bash
# Install OpenClaw China packages
npm install @openclaw-china/dingtalk @openclaw-china/qqbot @openclaw-china/wecom @openclaw-china/wecom-app @openclaw-china/wecom-kf @openclaw-china/wechat-mp

# Or install specific channels
npm install @openclaw-china/dingtalk  # DingTalk only
npm install @openclaw-china/qqbot     # QQ Bot only
npm install @openclaw-china/wecom     # WeChat Work Robot only
```

## Platform Selection Guide

| Platform | Complexity | Public IP Required | Use Case |
|----------|------------|-------------------|----------|
| **DingTalk** | Simple | No | Enterprise internal |
| **QQ Bot** | Simple | No | Public bot service |
| **WeChat Work Robot** | Simple | No | Enterprise internal (recommended) |
| **WeChat Work App** | Medium | Yes | Connect to personal WeChat |
| **WeChat Customer Service** | Medium | Yes | External customer support |
| **WeChat Official Account** | Medium | Yes | Public followers |

## Configuration

### DingTalk Configuration

```typescript
// config/channels.dingtalk.ts
export default {
  channels: {
    dingtalk: {
      enabled: true,
      clientId: process.env.DINGTALK_CLIENT_ID,
      clientSecret: process.env.DINGTALK_CLIENT_SECRET,
      // Optional: Enable multiple accounts
      accounts: [
        {
          clientId: process.env.DINGTALK_CLIENT_ID_1,
          clientSecret: process.env.DINGTALK_CLIENT_SECRET_1
        }
      ]
    }
  }
}
```

Environment variables:
```bash
DINGTALK_CLIENT_ID=your_client_id
DINGTALK_CLIENT_SECRET=your_client_secret
```

### QQ Bot Configuration

```typescript
// config/channels.qqbot-china.ts
export default {
  channels: {
    'qqbot-china': {
      enabled: true,
      appId: process.env.QQ_APP_ID,
      token: process.env.QQ_BOT_TOKEN,
      // Enable streaming for C2C (private chat)
      streaming: true,
      // Optional: Enable multiple bots
      accounts: [
        {
          appId: process.env.QQ_APP_ID_1,
          token: process.env.QQ_BOT_TOKEN_1,
          secret: process.env.QQ_BOT_SECRET_1
        }
      ]
    }
  }
}
```

### WeChat Work Robot (Long Connection)

```typescript
// config/channels.wecom.ts
export default {
  channels: {
    wecom: {
      enabled: true,
      corpId: process.env.WECOM_CORP_ID,
      corpSecret: process.env.WECOM_CORP_SECRET,
      // Connection mode: 'ws' (WebSocket) or 'webhook'
      mode: 'ws',
      // Optional: Robot token for webhook mode
      token: process.env.WECOM_ROBOT_TOKEN,
      encodingAESKey: process.env.WECOM_ENCODING_AES_KEY
    }
  }
}
```

### WeChat Work Self-Built App (Can Connect to Personal WeChat)

```typescript
// config/channels.wecom-app.ts
export default {
  channels: {
    'wecom-app': {
      enabled: true,
      corpId: process.env.WECOM_APP_CORP_ID,
      agentId: process.env.WECOM_APP_AGENT_ID,
      secret: process.env.WECOM_APP_SECRET,
      token: process.env.WECOM_APP_TOKEN,
      encodingAESKey: process.env.WECOM_APP_ENCODING_AES_KEY,
      // Public URL for callbacks
      callbackUrl: process.env.WECOM_APP_CALLBACK_URL
    }
  }
}
```

### WeChat Customer Service (External Users)

```typescript
// config/channels.wecom-kf.ts
export default {
  channels: {
    'wecom-kf': {
      enabled: true,
      corpId: process.env.WECOM_KF_CORP_ID,
      secret: process.env.WECOM_KF_SECRET,
      token: process.env.WECOM_KF_TOKEN,
      encodingAESKey: process.env.WECOM_KF_ENCODING_AES_KEY,
      // Welcome message when user enters session
      welcomeMessage: '您好！我是AI助手，有什么可以帮您？'
    }
  }
}
```

### WeChat Official Account

```typescript
// config/channels.wechat-mp.ts
export default {
  channels: {
    'wechat-mp': {
      enabled: true,
      appId: process.env.WECHAT_MP_APP_ID,
      appSecret: process.env.WECHAT_MP_APP_SECRET,
      token: process.env.WECHAT_MP_TOKEN,
      encodingAESKey: process.env.WECHAT_MP_ENCODING_AES_KEY,
      // Render Markdown to plain text for WeChat compatibility
      renderMarkdown: true,
      // Active delivery mode: 'split' (multiple messages) or 'merged' (single message)
      activeDeliveryMode: 'split',
      // ASR (Automatic Speech Recognition) for voice messages
      asrConfig: {
        enabled: true,
        secretId: process.env.TENCENT_CLOUD_SECRET_ID,
        secretKey: process.env.TENCENT_CLOUD_SECRET_KEY,
        engineType: '16k_zh' // 16kHz Chinese
      }
    }
  }
}
```

## Real Code Examples

### Handling Incoming Messages

```typescript
// Custom message handler for DingTalk
import { DingTalkChannel } from '@openclaw-china/dingtalk';

const channel = new DingTalkChannel({
  clientId: process.env.DINGTALK_CLIENT_ID,
  clientSecret: process.env.DINGTALK_CLIENT_SECRET
});

// Listen for messages
channel.on('message', async (message) => {
  console.log('Received:', message.content);
  
  // Process with OpenClaw
  const response = await openclawAgent.chat(message.content);
  
  // Send response
  await channel.sendMessage({
    conversationId: message.conversationId,
    content: response.text,
    messageType: 'markdown' // or 'text'
  });
});
```

### Sending Proactive Messages (Scheduled Tasks)

```typescript
// Send scheduled message via QQ Bot
import { QQBotChannel } from '@openclaw-china/qqbot';

const qqBot = new QQBotChannel({
  appId: process.env.QQ_APP_ID,
  token: process.env.QQ_BOT_TOKEN
});

async function sendDailyReport() {
  const report = await generateReport();
  
  await qqBot.sendMessage({
    userId: 'user_openid',
    content: report,
    messageType: 'markdown'
  });
}

// Schedule daily at 9 AM
cron.schedule('0 9 * * *', sendDailyReport);
```

### Handling File Uploads

```typescript
// Process file from WeChat Work
import { WeComAppChannel } from '@openclaw-china/wecom-app';

const wecomApp = new WeComAppChannel({
  corpId: process.env.WECOM_APP_CORP_ID,
  agentId: process.env.WECOM_APP_AGENT_ID,
  secret: process.env.WECOM_APP_SECRET
});

wecomApp.on('file', async (fileMessage) => {
  // Download file
  const fileBuffer = await wecomApp.downloadMedia(fileMessage.mediaId);
  
  // Process with OpenClaw
  const analysis = await openclawAgent.analyzeFile(fileBuffer);
  
  // Send response
  await wecomApp.sendMessage({
    userId: fileMessage.fromUserId,
    content: `文件分析结果：\n${analysis}`
  });
});
```

### Streaming Response (QQ Bot C2C)

```typescript
// Enable streaming for real-time chat experience
import { QQBotChannel } from '@openclaw-china/qqbot';

const qqBot = new QQBotChannel({
  appId: process.env.QQ_APP_ID,
  token: process.env.QQ_BOT_TOKEN,
  streaming: true // Enable streaming for private chat
});

qqBot.on('message', async (message) => {
  // Streaming only works for C2C (private chat)
  if (message.messageType === 'C2C') {
    const stream = await openclawAgent.chatStream(message.content);
    
    for await (const chunk of stream) {
      await qqBot.updateStreamMessage({
        messageId: message.id,
        content: chunk.text
      });
    }
  } else {
    // Group chat falls back to regular message
    const response = await openclawAgent.chat(message.content);
    await qqBot.sendMessage({
      groupId: message.groupId,
      content: response.text
    });
  }
});
```

### Voice Message with ASR (WeChat Official Account)

```typescript
// Automatic voice-to-text conversion
import { WeChatMPChannel } from '@openclaw-china/wechat-mp';

const wechatMP = new WeChatMPChannel({
  appId: process.env.WECHAT_MP_APP_ID,
  appSecret: process.env.WECHAT_MP_APP_SECRET,
  asrConfig: {
    enabled: true,
    secretId: process.env.TENCENT_CLOUD_SECRET_ID,
    secretKey: process.env.TENCENT_CLOUD_SECRET_KEY,
    engineType: '16k_zh'
  }
});

wechatMP.on('voice', async (voiceMessage) => {
  // ASR automatically converts voice to text
  const text = voiceMessage.recognizedText;
  
  console.log('Voice recognized:', text);
  
  // Process with OpenClaw
  const response = await openclawAgent.chat(text);
  
  await wechatMP.sendMessage({
    userId: voiceMessage.fromUserId,
    content: response.text
  });
});
```

## Common Patterns

### Multi-Account Setup

```typescript
// config/channels.dingtalk.ts
export default {
  channels: {
    dingtalk: {
      enabled: true,
      accounts: [
        {
          name: 'team-a',
          clientId: process.env.DINGTALK_TEAM_A_CLIENT_ID,
          clientSecret: process.env.DINGTALK_TEAM_A_CLIENT_SECRET
        },
        {
          name: 'team-b',
          clientId: process.env.DINGTALK_TEAM_B_CLIENT_ID,
          clientSecret: process.env.DINGTALK_TEAM_B_CLIENT_SECRET
        }
      ]
    }
  }
}
```

### Group Chat Management

```typescript
// Handle @mentions in WeChat Work group
import { WeComChannel } from '@openclaw-china/wecom';

const wecom = new WeComChannel({
  corpId: process.env.WECOM_CORP_ID,
  corpSecret: process.env.WECOM_CORP_SECRET,
  mode: 'ws'
});

wecom.on('message', async (message) => {
  // Check if bot is mentioned in group
  if (message.isGroupChat && message.isMentioned) {
    const cleanContent = message.content.replace(/@\w+/g, '').trim();
    
    const response = await openclawAgent.chat(cleanContent, {
      context: {
        groupId: message.groupId,
        userId: message.fromUserId
      }
    });
    
    await wecom.sendMessage({
      groupId: message.groupId,
      content: response.text,
      mentionedUsers: [message.fromUserId] // @user in response
    });
  }
});
```

### Message Formatting

```typescript
// Convert Markdown to platform-specific format
function formatMessage(text: string, platform: string): string {
  switch (platform) {
    case 'dingtalk':
    case 'wecom':
    case 'qqbot':
      // These support Markdown
      return text;
      
    case 'wechat-mp':
      // Convert Markdown to plain text
      return text
        .replace(/\*\*(.+?)\*\*/g, '$1')  // Bold
        .replace(/\*(.+?)\*/g, '$1')      // Italic
        .replace(/`(.+?)`/g, '$1')        // Code
        .replace(/^#+\s+(.+)$/gm, '$1');  // Headers
      
    default:
      return text;
  }
}
```

## Troubleshooting

### Connection Issues

**Problem**: WebSocket connection fails for WeChat Work Robot

```typescript
// Solution: Check network and enable debug logging
const wecom = new WeComChannel({
  corpId: process.env.WECOM_CORP_ID,
  corpSecret: process.env.WECOM_CORP_SECRET,
  mode: 'ws',
  debug: true // Enable debug logs
});

wecom.on('error', (error) => {
  console.error('WeChat Work error:', error);
  // Implement retry logic
});

wecom.on('disconnect', () => {
  console.log('Disconnected, reconnecting...');
  setTimeout(() => wecom.connect(), 5000);
});
```

**Problem**: Callback URL not receiving messages

```bash
# Verify your public URL is accessible
curl https://your-domain.com/webhook/wecom-app

# Check nginx/reverse proxy configuration
# Ensure SSL certificate is valid
# Verify firewall allows incoming connections
```

### Message Delivery Issues

**Problem**: Messages not sending on WeChat Official Account

```typescript
// Check 48-hour interaction window
import { WeChatMPChannel } from '@openclaw-china/wechat-mp';

const wechatMP = new WeChatMPChannel({
  appId: process.env.WECHAT_MP_APP_ID,
  appSecret: process.env.WECHAT_MP_APP_SECRET
});

try {
  await wechatMP.sendMessage({
    userId: 'user_openid',
    content: 'Hello'
  });
} catch (error) {
  if (error.code === 45015) {
    console.error('Outside 48-hour window, use template message instead');
    await wechatMP.sendTemplateMessage({
      userId: 'user_openid',
      templateId: process.env.TEMPLATE_ID,
      data: { message: 'Hello' }
    });
  }
}
```

**Problem**: Messages truncated or not displaying

```typescript
// Enable automatic message splitting for long content
const wechatMP = new WeChatMPChannel({
  appId: process.env.WECHAT_MP_APP_ID,
  appSecret: process.env.WECHAT_MP_APP_SECRET,
  activeDeliveryMode: 'split', // Split long messages automatically
  renderMarkdown: true // Convert Markdown to plain text
});
```

### Platform-Specific Issues

**QQ Bot**: Streaming not working in groups

```typescript
// Streaming only supports C2C (private chat)
const qqBot = new QQBotChannel({
  appId: process.env.QQ_APP_ID,
  token: process.env.QQ_BOT_TOKEN,
  streaming: true // Only applies to private chat
});

// For groups, use regular messages
qqBot.on('message', async (message) => {
  if (message.messageType === 'GROUP') {
    // No streaming in groups, send complete message
    const response = await openclawAgent.chat(message.content);
    await qqBot.sendMessage({
      groupId: message.groupId,
      content: response.text
    });
  }
});
```

**DingTalk**: Rate limiting

```typescript
// Implement rate limiting
import { RateLimiter } from 'limiter';

const limiter = new RateLimiter({
  tokensPerInterval: 20,
  interval: 'minute'
});

async function sendDingTalkMessage(message) {
  await limiter.removeTokens(1);
  return dingtalk.sendMessage(message);
}
```

### Debug Mode

```typescript
// Enable verbose logging for troubleshooting
export default {
  channels: {
    'qqbot-china': {
      enabled: true,
      debug: true, // Enable debug logs
      appId: process.env.QQ_APP_ID,
      token: process.env.QQ_BOT_TOKEN
    }
  },
  logging: {
    level: 'debug', // Set global log level
    channels: ['qqbot-china'] // Log specific channels
  }
}
```

## Feature Support Matrix

| Feature | DingTalk | QQ Bot | WeChat Work Robot | WeChat Work App | WeChat Customer Service | WeChat Official Account |
|---------|:--------:|:------:|:----------------:|:---------------:|:----------------------:|:----------------------:|
| Text Messages | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Markdown | ✅ | ✅ | ✅ | ✅ | ❌ | ✅ (converted) |
| Streaming | ✅ | ✅ (C2C only) | ✅ | ❌ | ❌ | ❌ |
| Images/Files | ✅ | ✅ | ✅ | ✅ | 🚧 | ✅ (images only) |
| Voice | ✅ | ✅ | ✅ | ✅ | 🚧 | ✅ (with ASR) |
| Group Chat | ✅ | ✅ | ✅ | ❌ | ❌ | ❌ |
| Multi-Account | ✅ | ✅ | ✅ | ✅ | 🚧 | 🚧 |
| Proactive Send | ✅ | ✅ | ✅ | ✅ | 🚧 | 🚧 |

Legend: ✅ Supported | ❌ Not Supported | 🚧 In Development
