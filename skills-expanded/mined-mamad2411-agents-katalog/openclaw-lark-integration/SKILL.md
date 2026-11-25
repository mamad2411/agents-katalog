---
name: openclaw-lark-integration
description: Official Lark/Feishu plugin for OpenClaw that enables AI agents to interact with Lark workspaces including messages, docs, bases, calendars, and tasks
triggers:
  - "integrate OpenClaw with Lark"
  - "set up Feishu plugin for OpenClaw"
  - "connect my AI agent to Lark workspace"
  - "configure OpenClaw Lark permissions"
  - "create a Lark bot with OpenClaw"
  - "troubleshoot OpenClaw Lark integration"
  - "manage OpenClaw Lark group settings"
  - "use OpenClaw with Feishu documents"
---

# OpenClaw Lark Integration

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Official Lark/Feishu plugin for OpenClaw that seamlessly connects AI agents to Lark workspaces. Enables reading and writing messages, managing docs, bases, sheets, calendars, and tasks with built-in security controls and interactive cards.

## What It Does

The OpenClaw Lark plugin allows AI agents to:

- **Messaging**: Read message history (groups/DMs/threads), send/reply to messages, search, download attachments
- **Documents**: Create, update, and read Lark docs
- **Base**: Full CRUD operations on bases, tables, fields, records with advanced filtering
- **Sheets**: Create, edit, and view spreadsheets
- **Calendar**: Manage calendars, events, attendees, and check free/busy status
- **Tasks**: Create, query, update, complete tasks and manage subtasks/comments
- **Interactive Cards**: Real-time status updates with streaming responses
- **Security**: Built-in permission policies and per-group configuration

## Installation

### Prerequisites

- Node.js v22 or higher
- OpenClaw version 2026.2.26 or higher

Check OpenClaw version:
```bash
openclaw -v
```

If below required version, upgrade:
```bash
npm install -g openclaw
```

### Install Plugin

```bash
npm install -g @larksuite/openclaw-lark
```

Or with pnpm:
```bash
pnpm add -g @larksuite/openclaw-lark
```

## Configuration

### 1. Create Lark/Feishu App

1. Go to [Lark Open Platform](https://open.larksuite.com/) or [Feishu Open Platform](https://open.feishu.cn/)
2. Create a new custom app
3. Configure bot capabilities and permissions
4. Obtain App ID and App Secret

### 2. Required Permissions

The app needs these permission scopes:

**Messaging**:
- `im:message` - Send messages
- `im:message:read_as_user` - Read messages as user
- `im:chat` - Access chat information

**Documents**:
- `docx:document` - Manage docs
- `drive:drive` - Access drive files

**Base**:
- `bitable:app` - Manage base apps
- `bitable:record` - Manage records

**Sheets**:
- `sheets:spreadsheet` - Manage spreadsheets

**Calendar**:
- `calendar:calendar` - Manage calendars
- `calendar:event` - Manage events

**Tasks**:
- `task:task` - Manage tasks

### 3. Configure Environment Variables

Create or update your OpenClaw config file with Lark credentials:

```typescript
// openclaw.config.ts
export default {
  channels: {
    lark: {
      appId: process.env.LARK_APP_ID,
      appSecret: process.env.LARK_APP_SECRET,
      verificationToken: process.env.LARK_VERIFICATION_TOKEN,
      encryptKey: process.env.LARK_ENCRYPT_KEY,
      
      // Optional: Security policies
      policies: {
        allowPrivateChat: true,
        allowGroupChat: false, // Disable by default for security
        groupAllowlist: [], // Whitelist specific groups
      },
      
      // Optional: Default settings
      enableInteractiveCards: true,
      enableStreamingResponse: true,
    }
  }
}
```

Set environment variables:
```bash
export LARK_APP_ID="your_app_id"
export LARK_APP_SECRET="your_app_secret"
export LARK_VERIFICATION_TOKEN="your_verification_token"
export LARK_ENCRYPT_KEY="your_encrypt_key"
```

### 4. Start OpenClaw with Lark Channel

```bash
openclaw start --channel lark
```

Or specify config file:
```bash
openclaw start --config openclaw.config.ts
```

## Key Commands

### OpenClaw CLI Commands

```bash
# Start with Lark channel
openclaw start --channel lark

# Check version
openclaw -v

# View help
openclaw --help

# Stop OpenClaw
openclaw stop
```

### Managing the Bot

Once running, interact with your bot in Lark/Feishu by:
- Sending direct messages
- @mentioning in allowed groups
- Using configured skills and prompts

## API Usage Patterns

### Sending Messages

The plugin automatically handles message sending through OpenClaw's unified interface:

```typescript
// Example skill that sends a Lark message
import { SkillContext } from 'openclaw';

export async function sendLarkMessage(context: SkillContext, message: string) {
  // OpenClaw automatically routes to Lark channel
  await context.channel.sendMessage({
    text: message,
    chatId: context.chatId
  });
}
```

### Reading Messages

```typescript
export async function getRecentMessages(context: SkillContext, limit: number = 10) {
  const messages = await context.channel.getMessages({
    chatId: context.chatId,
    limit: limit
  });
  
  return messages.map(msg => ({
    sender: msg.sender,
    content: msg.content,
    timestamp: msg.timestamp
  }));
}
```

### Working with Documents

```typescript
export async function createDocument(
  context: SkillContext, 
  title: string, 
  content: string
) {
  const doc = await context.channel.lark.createDoc({
    title: title,
    content: content,
    folderToken: context.workspace.defaultFolder
  });
  
  return {
    docId: doc.docToken,
    url: doc.url
  };
}
```

### Managing Base Records

```typescript
export async function addBaseRecord(
  context: SkillContext,
  baseId: string,
  tableId: string,
  fields: Record<string, any>
) {
  const record = await context.channel.lark.base.createRecord({
    appToken: baseId,
    tableId: tableId,
    fields: fields
  });
  
  return record;
}

export async function queryBaseRecords(
  context: SkillContext,
  baseId: string,
  tableId: string,
  filter?: string
) {
  const records = await context.channel.lark.base.listRecords({
    appToken: baseId,
    tableId: tableId,
    filter: filter, // e.g., "AND(CurrentValue.[Status] = 'Active')"
    pageSize: 100
  });
  
  return records.items;
}
```

### Calendar Operations

```typescript
export async function createCalendarEvent(
  context: SkillContext,
  summary: string,
  startTime: string,
  endTime: string,
  attendees?: string[]
) {
  const event = await context.channel.lark.calendar.createEvent({
    summary: summary,
    startTime: { timestamp: startTime },
    endTime: { timestamp: endTime },
    attendees: attendees?.map(email => ({ email }))
  });
  
  return {
    eventId: event.eventId,
    htmlLink: event.htmlLink
  };
}
```

### Task Management

```typescript
export async function createTask(
  context: SkillContext,
  summary: string,
  description: string,
  dueDate?: string
) {
  const task = await context.channel.lark.task.createTask({
    summary: summary,
    description: description,
    due: dueDate ? { date: dueDate } : undefined
  });
  
  return task;
}
```

## Security Configuration

### Permission Policies

Configure access control in your config file:

```typescript
export default {
  channels: {
    lark: {
      // ... credentials
      
      policies: {
        // Allow private chats (default: true)
        allowPrivateChat: true,
        
        // Disable all group chats (recommended for security)
        allowGroupChat: false,
        
        // Or allow specific groups only
        allowGroupChat: true,
        groupAllowlist: [
          'oc_xxxxxxxxxxxxx', // Group chat ID
          'oc_yyyyyyyyyyyyy'
        ],
        
        // Require confirmation for sensitive operations
        requireConfirmation: {
          deleteDocument: true,
          deleteBaseRecord: true,
          sendMessageToGroup: true
        }
      }
    }
  }
}
```

### Per-Group Configuration

```typescript
export default {
  channels: {
    lark: {
      // ... credentials
      
      groupSettings: {
        'oc_xxxxxxxxxxxxx': {
          enabled: true,
          allowedSkills: ['search', 'summarize'], // Restrict skills
          customSystemPrompt: 'You are a helpful assistant for the engineering team.',
          maxTokens: 4000
        }
      }
    }
  }
}
```

## Interactive Cards and Streaming

### Enable Streaming Responses

```typescript
export default {
  channels: {
    lark: {
      // ... credentials
      enableStreamingResponse: true,
      enableInteractiveCards: true
    }
  }
}
```

Streaming automatically shows:
- 🤔 Thinking indicator
- 📝 Generating status with live text
- ✅ Complete notification

### Custom Interactive Cards

```typescript
export async function sendCardWithActions(context: SkillContext) {
  await context.channel.sendCard({
    header: {
      title: 'Confirm Action',
      template: 'blue'
    },
    elements: [
      {
        tag: 'div',
        text: {
          tag: 'plain_text',
          content: 'Do you want to proceed with this operation?'
        }
      },
      {
        tag: 'action',
        actions: [
          {
            tag: 'button',
            text: { tag: 'plain_text', content: 'Confirm' },
            type: 'primary',
            value: { action: 'confirm' }
          },
          {
            tag: 'button',
            text: { tag: 'plain_text', content: 'Cancel' },
            type: 'default',
            value: { action: 'cancel' }
          }
        ]
      }
    ]
  });
}
```

## Common Patterns

### Message Handler Skill

```typescript
import { Skill } from 'openclaw';

export const messageHandlerSkill: Skill = {
  name: 'lark-message-handler',
  description: 'Handle incoming Lark messages',
  
  async execute(context) {
    const { message, sender } = context;
    
    // Process message
    if (message.includes('help')) {
      return await context.reply('How can I assist you?');
    }
    
    // Search message history
    if (message.startsWith('search:')) {
      const query = message.substring(7);
      const results = await context.channel.searchMessages({ query });
      return results;
    }
    
    // Default response
    return await context.reply('Message received');
  }
};
```

### Document Automation

```typescript
export async function createWeeklyReport(context: SkillContext) {
  const today = new Date();
  const title = `Weekly Report - ${today.toISOString().split('T')[0]}`;
  
  // Gather data from Base
  const tasks = await context.channel.lark.base.listRecords({
    appToken: process.env.LARK_TASK_BASE_ID!,
    tableId: 'tblxxxxxxxx',
    filter: "AND(CurrentValue.[CompletedAt] >= DATE_SUB(TODAY(), 7))"
  });
  
  // Create formatted document
  const content = `
# ${title}

## Completed Tasks
${tasks.items.map(t => `- ${t.fields.Name}`).join('\n')}

## Summary
Total tasks completed: ${tasks.items.length}
`;
  
  const doc = await context.channel.lark.createDoc({
    title,
    content
  });
  
  return doc.url;
}
```

### Batch Operations

```typescript
export async function batchUpdateRecords(
  context: SkillContext,
  baseId: string,
  tableId: string,
  updates: Array<{ recordId: string; fields: Record<string, any> }>
) {
  // Lark API supports batch operations
  const result = await context.channel.lark.base.batchUpdateRecords({
    appToken: baseId,
    tableId: tableId,
    records: updates
  });
  
  return {
    updated: result.records.length,
    records: result.records
  };
}
```

## Troubleshooting

### Bot Not Responding

**Issue**: Bot doesn't reply to messages

**Solutions**:
1. Verify OpenClaw is running: `openclaw status`
2. Check credentials are set correctly
3. Ensure bot has required permissions in Lark admin console
4. Verify group is in allowlist if `allowGroupChat` is true
5. Check logs: `openclaw logs --channel lark`

### Permission Errors

**Issue**: "Permission denied" errors

**Solutions**:
1. Review required scopes in Lark app settings
2. Re-authorize the app after adding permissions
3. Check if user has necessary workspace permissions
4. Verify app is published (not in development mode)

### Message Not Sent

**Issue**: Messages fail to send

**Solutions**:
1. Check if chat ID is valid
2. Verify bot is added to the group chat
3. Ensure `im:message` permission is granted
4. Check message format and size limits

### Configuration Not Loading

**Issue**: Config changes not taking effect

**Solutions**:
1. Restart OpenClaw after config changes
2. Verify config file path: `openclaw start --config ./path/to/config.ts`
3. Check for TypeScript/JSON syntax errors
4. Ensure environment variables are exported

### Streaming Not Working

**Issue**: Streaming responses not appearing

**Solutions**:
1. Verify `enableStreamingResponse: true` in config
2. Check Lark client version supports interactive cards
3. Test with simple message first
4. Review network/firewall settings

### Rate Limiting

**Issue**: "Rate limit exceeded" errors

**Solutions**:
1. Implement exponential backoff in custom skills
2. Cache frequently accessed data
3. Use batch operations where possible
4. Monitor API quota in Lark admin console

## Best Practices

1. **Security First**: Never disable default security policies without understanding risks
2. **Use Private Chats**: Recommended for personal assistants to avoid permission abuse
3. **Whitelist Groups**: If using in groups, explicitly whitelist trusted chats only
4. **Environment Variables**: Always use env vars for credentials, never hardcode
5. **Error Handling**: Wrap API calls in try-catch blocks
6. **Confirmation Dialogs**: Use interactive cards for destructive operations
7. **Rate Limiting**: Respect API limits, implement backoff strategies
8. **Logging**: Enable detailed logs during development for debugging
9. **Skill Restrictions**: Limit available skills per group to reduce attack surface
10. **Regular Updates**: Keep OpenClaw and plugin updated for security patches

## Additional Resources

- [Official Documentation](https://bytedance.larkoffice.com/docx/MFK7dDFLFoVlOGxWCv5cTXKmnMh)
- [Lark Open Platform](https://open.larksuite.com/)
- [Feishu Open Platform](https://open.feishu.cn/)
- [OpenClaw Official Website](https://openclaw.ai)
- [GitHub Repository](https://github.com/larksuite/openclaw-larksuite)
