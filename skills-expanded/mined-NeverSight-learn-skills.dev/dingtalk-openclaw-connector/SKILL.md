---
name: dingtalk-openclaw-connector
description: Connect OpenClaw AI agents to DingTalk with message handling, document operations, calendar, todos, and AI cards
triggers:
  - how do I integrate OpenClaw with DingTalk
  - set up DingTalk connector for OpenClaw
  - create a DingTalk bot with OpenClaw
  - how to handle DingTalk messages in OpenClaw
  - send DingTalk notifications from OpenClaw agent
  - configure DingTalk AI card streaming
  - troubleshoot DingTalk OpenClaw connector
  - route multiple DingTalk bots to different agents
---

# DingTalk OpenClaw Connector Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Official DingTalk channel plugin for OpenClaw, enabling AI agents to receive/send messages, manage documents, calendars, todos, and more within DingTalk enterprise workspace.

## What It Does

This TypeScript connector bridges OpenClaw agents with DingTalk's ecosystem:

- **Messaging**: Receive/send private/group messages, @mentions, rich media (text/Markdown/images)
- **Documents**: Create, append, search, list DingTalk documents
- **DING Notifications**: Send priority alerts to users/groups
- **Todos**: Create personal todos, check status, set deadlines
- **AI Tables**: Create tables, read/write rows, query data
- **Calendar**: Manage calendars, events (CRUD + search), attendees, availability
- **Journal**: Submit daily/weekly reports, query history
- **AI Cards**: Streaming responses with typewriter effect, interactive buttons
- **Multi-Agent Routing**: Connect multiple bots to different OpenClaw agents
- **Access Control**: Flexible permission policies for private/group chats

## Prerequisites

- **OpenClaw** ≥ 2026.4.9 (check: `openclaw -v`, upgrade: `npm install -g openclaw`)
- **Node.js** (for installation)
- **DingTalk App** (mobile, for QR authorization)

## Installation

### Quick Install with Auto-Authorization

```bash
npx -y @dingtalk-real-ai/dingtalk-connector install
```

Scan the QR code displayed in terminal with DingTalk mobile app. After seeing "Success! Bot configured.", restart gateway:

```bash
openclaw gateway restart
```

### Manual Installation (if auto-auth fails)

```bash
npm install -g @dingtalk-real-ai/dingtalk-connector
```

Then follow [manual setup guide](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/docs/DINGTALK_MANUAL_SETUP.md) to configure credentials.

## Configuration

Plugin config is stored in OpenClaw's channel settings. Key environment variables:

```bash
# DingTalk bot credentials (obtained during authorization)
DINGTALK_CLIENT_ID=your_client_id
DINGTALK_CLIENT_SECRET=your_client_secret
DINGTALK_ROBOT_CODE=your_robot_code

# Optional: Multi-agent routing
DINGTALK_AGENT_MAPPING='{"bot_code_1":"agent_1","bot_code_2":"agent_2"}'

# Optional: Access control
DINGTALK_PRIVATE_CHAT_POLICY=whitelist  # whitelist|blacklist|all
DINGTALK_GROUP_CHAT_POLICY=all          # whitelist|blacklist|all
DINGTALK_WHITELIST=user_id_1,user_id_2
```

### Access Control Policies

Configure who can interact with your bot:

```typescript
// In OpenClaw channel config
{
  "privateChatPolicy": "whitelist",  // Only whitelisted users
  "groupChatPolicy": "all",          // All groups
  "whitelist": ["user_123", "user_456"],
  "blacklist": []
}
```

Options: `all`, `whitelist`, `blacklist`

## Key Capabilities

### 1. Message Handling

The connector automatically receives and routes DingTalk messages to your OpenClaw agent:

```typescript
// Agent receives message context
interface MessageContext {
  conversationId: string;
  senderId: string;
  senderName: string;
  content: {
    text?: string;
    images?: Array<{ downloadCode: string; url: string }>;
    files?: Array<{ fileName: string; downloadCode: string }>;
  };
  isGroupChat: boolean;
  atUsers?: string[];
}
```

### 2. Sending Messages

**Text Message:**
```typescript
// Agent action
{
  "action": "sendMessage",
  "params": {
    "conversationId": "cid_xxx",
    "content": "Hello from OpenClaw!"
  }
}
```

**Markdown with @mention:**
```typescript
{
  "action": "sendMessage",
  "params": {
    "conversationId": "cid_xxx",
    "content": "## Report\n@user_123 please review",
    "format": "markdown",
    "atUsers": ["user_123"]
  }
}
```

**Image Message:**
```typescript
{
  "action": "sendMessage",
  "params": {
    "conversationId": "cid_xxx",
    "imageUrl": "https://example.com/image.png"
    // Or local path: "imagePath": "/path/to/image.png"
  }
}
```

### 3. AI Card Streaming

Show real-time thinking/generation progress:

```typescript
// Enable in channel config
{
  "enableAICard": true,
  "streamingMode": "typewriter"  // typewriter effect
}
```

The connector automatically wraps agent responses in interactive cards with states:
- 🤔 Thinking...
- ✍️ Generating...
- ✅ Complete

### 4. Document Operations

**Create Document:**
```typescript
{
  "action": "createDocument",
  "params": {
    "title": "Meeting Notes",
    "content": "# Agenda\n- Item 1\n- Item 2",
    "spaceId": "space_xxx"  // optional
  }
}
```

**Append to Document:**
```typescript
{
  "action": "appendDocument",
  "params": {
    "documentId": "doc_xxx",
    "content": "\n## New Section\nAdditional notes..."
  }
}
```

**Search Documents:**
```typescript
{
  "action": "searchDocuments",
  "params": {
    "keyword": "meeting",
    "maxResults": 10
  }
}
```

### 5. DING Notifications

Send high-priority alerts:

```typescript
{
  "action": "sendDing",
  "params": {
    "receiverUserIds": ["user_123", "user_456"],
    "content": "Urgent: Server down!",
    "remindType": "DING_SMS"  // DING_NOTICE or DING_SMS
  }
}
```

### 6. Todo Management

**Create Todo:**
```typescript
{
  "action": "createTodo",
  "params": {
    "subject": "Review PR #123",
    "description": "Check code quality",
    "dueTime": "2026-05-20T17:00:00Z",
    "executorIds": ["user_123"]
  }
}
```

**Query Todos:**
```typescript
{
  "action": "getTodos",
  "params": {
    "status": "PENDING",  // PENDING|DONE
    "startDate": "2026-05-01",
    "endDate": "2026-05-31"
  }
}
```

### 7. Calendar & Events

**Create Calendar Event:**
```typescript
{
  "action": "createCalendarEvent",
  "params": {
    "calendarId": "cal_xxx",
    "summary": "Team Sync",
    "startTime": "2026-05-20T14:00:00+08:00",
    "endTime": "2026-05-20T15:00:00+08:00",
    "location": "Conference Room A",
    "attendees": [
      { "userId": "user_123" },
      { "userId": "user_456" }
    ]
  }
}
```

**Query Events:**
```typescript
{
  "action": "searchCalendarEvents",
  "params": {
    "calendarId": "cal_xxx",
    "startTime": "2026-05-20T00:00:00+08:00",
    "endTime": "2026-05-21T00:00:00+08:00"
  }
}
```

**Check Availability:**
```typescript
{
  "action": "checkAvailability",
  "params": {
    "userIds": ["user_123", "user_456"],
    "startTime": "2026-05-20T14:00:00+08:00",
    "endTime": "2026-05-20T15:00:00+08:00"
  }
}
```

### 8. AI Tables

**Create Table:**
```typescript
{
  "action": "createAITable",
  "params": {
    "name": "Customer Database",
    "fields": [
      { "name": "Name", "type": "TEXT" },
      { "name": "Email", "type": "TEXT" },
      { "name": "Status", "type": "SINGLE_SELECT", "options": ["Active", "Inactive"] }
    ]
  }
}
```

**Insert Row:**
```typescript
{
  "action": "insertTableRow",
  "params": {
    "tableId": "tbl_xxx",
    "fields": {
      "Name": "John Doe",
      "Email": "john@example.com",
      "Status": "Active"
    }
  }
}
```

**Query Rows:**
```typescript
{
  "action": "queryTableRows",
  "params": {
    "tableId": "tbl_xxx",
    "filter": {
      "Status": "Active"
    },
    "maxResults": 50
  }
}
```

### 9. Journal (Reports)

**Submit Daily Report:**
```typescript
{
  "action": "submitJournal",
  "params": {
    "type": "daily",
    "date": "2026-05-20",
    "content": "## Completed\n- Feature A\n- Bug fix B\n\n## Tomorrow\n- Feature C"
  }
}
```

**Query Reports:**
```typescript
{
  "action": "getJournals",
  "params": {
    "type": "weekly",
    "startDate": "2026-05-01",
    "endDate": "2026-05-15"
  }
}
```

## Multi-Agent Routing

Connect multiple DingTalk bots to different OpenClaw agents for specialized tasks:

### Configuration

```bash
# In .env or OpenClaw config
DINGTALK_AGENT_MAPPING='{
  "robot_code_hr": "hr_agent",
  "robot_code_it": "it_support_agent",
  "robot_code_sales": "sales_agent"
}'
```

### Agent Definitions

```yaml
# openclaw.config.yaml
agents:
  hr_agent:
    name: HR Assistant
    model: gpt-4
    systemPrompt: You are an HR assistant handling employee queries
    
  it_support_agent:
    name: IT Support
    model: gpt-4
    systemPrompt: You provide IT technical support
    
  sales_agent:
    name: Sales Helper
    model: gpt-4
    systemPrompt: You assist with sales inquiries and CRM
```

Each bot routes to its designated agent automatically. See [Multi-Agent Setup Guide](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/docs/MULTI_AGENT_SETUP.md).

## Common Patterns

### Pattern 1: Auto-Reply Bot

```typescript
// Agent receives all group messages where bot is @mentioned
// Auto-respond with context-aware answers
async function handleMessage(context: MessageContext) {
  const { content, isGroupChat, atUsers } = context;
  
  if (isGroupChat && !atUsers?.includes(botUserId)) {
    return; // Ignore if not @mentioned
  }
  
  const response = await generateResponse(content.text);
  
  return {
    action: "sendMessage",
    params: {
      conversationId: context.conversationId,
      content: response
    }
  };
}
```

### Pattern 2: Document Search Assistant

```typescript
// Search docs and create summary
async function searchAndSummarize(query: string) {
  // 1. Search documents
  const docs = await executeAction({
    action: "searchDocuments",
    params: { keyword: query, maxResults: 5 }
  });
  
  // 2. Generate summary
  const summary = await summarize(docs);
  
  // 3. Create new doc with results
  return executeAction({
    action: "createDocument",
    params: {
      title: `Search Results: ${query}`,
      content: summary
    }
  });
}
```

### Pattern 3: Meeting Scheduler

```typescript
// Find available slot and create event
async function scheduleMeeting(attendeeIds: string[], duration: number) {
  const now = new Date();
  const nextWeek = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000);
  
  // 1. Check availability
  const availability = await executeAction({
    action: "checkAvailability",
    params: {
      userIds: attendeeIds,
      startTime: now.toISOString(),
      endTime: nextWeek.toISOString()
    }
  });
  
  // 2. Find first free slot
  const freeSlot = findFreeSlot(availability, duration);
  
  // 3. Create event
  return executeAction({
    action: "createCalendarEvent",
    params: {
      summary: "Team Meeting",
      startTime: freeSlot.start,
      endTime: freeSlot.end,
      attendees: attendeeIds.map(id => ({ userId: id }))
    }
  });
}
```

### Pattern 4: Task Tracker Bot

```typescript
// Create todo from message command
async function createTaskFromMessage(message: string, conversationId: string) {
  // Parse: "todo: Review PR #123 by Friday"
  const match = message.match(/todo:\s*(.+?)\s+by\s+(.+)/i);
  if (!match) return;
  
  const [, task, deadline] = match;
  
  // Create todo
  const todo = await executeAction({
    action: "createTodo",
    params: {
      subject: task,
      dueTime: parseDeadline(deadline)
    }
  });
  
  // Confirm in chat
  return executeAction({
    action: "sendMessage",
    params: {
      conversationId,
      content: `✅ Task created: ${task}\n📅 Due: ${deadline}`
    }
  });
}
```

## Troubleshooting

### Bot Not Responding

1. **Check gateway status:**
   ```bash
   openclaw gateway status
   ```

2. **Restart gateway:**
   ```bash
   openclaw gateway restart
   ```

3. **Verify credentials:**
   ```bash
   # Check if config exists
   openclaw config list
   ```

4. **Check logs:**
   ```bash
   openclaw gateway logs
   ```

### Authorization Failed

- Ensure you're using **DingTalk mobile app** (not desktop) to scan QR
- Check if QR code expired (timeout ~5 min), restart installation
- Verify network access to DingTalk API endpoints

### Message Not Received

- Confirm bot is in the conversation (group chat: must add bot; private: user initiated)
- Check access control policies (whitelist/blacklist)
- Verify bot has required permissions in DingTalk admin console

### Streaming AI Card Not Working

```typescript
// Ensure enabled in config
{
  "enableAICard": true,
  "streamingMode": "typewriter"
}
```

- Feature requires OpenClaw ≥ 2026.4.9
- Check browser console for WebSocket errors

### Multi-Agent Routing Issues

- Verify `DINGTALK_AGENT_MAPPING` JSON syntax
- Ensure agent names match those in `openclaw.config.yaml`
- Check robot codes are correct (not client IDs)

### Image Upload Fails

- Ensure image file exists and is readable
- Check file size (DingTalk limit: 20MB for images)
- Verify image format (JPEG, PNG, GIF supported)
- For URLs, ensure publicly accessible

### Calendar Events Not Creating

- Verify user has calendar permissions in DingTalk
- Check time format (ISO 8601 with timezone)
- Ensure `calendarId` is valid (create calendar first if needed)

### Common Error Codes

- `40014`: Invalid access token → Re-authorize bot
- `60020`: Permission denied → Check DingTalk app permissions
- `90002`: Message frequency limit → Rate limiting, slow down
- `71006`: Robot not in conversation → Add bot to group/chat

## Testing

Quick test after installation:

```bash
# Send test message to bot in DingTalk
# Expected: Bot responds with AI-generated reply in card format
```

**Verify specific features:**

```typescript
// Test document creation
// In DingTalk: @bot create a document titled "Test"

// Test todo
// In DingTalk: @bot remind me to review code tomorrow

// Test search
// In DingTalk: @bot search for meeting notes from last week
```

## Security Notes

- **Model Risks**: AI may hallucinate or execute unintended actions
- **Authorization Scope**: Bot operates with user permissions granted during setup
- **Data Privacy**: Follow company security policies if using corporate account
- **Default Protections**: Do NOT disable default security configs without understanding risks
- **Recommended Use**: Personal assistant, not production enterprise deployment

## Additional Resources

- [Manual Setup Guide](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/docs/DINGTALK_MANUAL_SETUP.md)
- [DEAP Agent Integration](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/docs/DEAP_AGENT_GUIDE.md) (local device operations)
- [Multi-Agent Routing Examples](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/docs/MULTI_AGENT_SETUP.md)
- [Troubleshooting Guide](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/docs/TROUBLESHOOTING.md)
- [GitHub Issues](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/issues)
- [CHANGELOG](https://github.com/DingTalk-Real-AI/dingtalk-openclaw-connector/blob/main/CHANGELOG.md)
