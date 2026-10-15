---
name: syncfusion-javascript-chat-ui
description: "Implement the Syncfusion Javascript Chat UI control using Javascript (ej2-interactive-chat). Use this skill when the user mentions chat UI, chat interface, conversational UI, messaging interface, chat applications, messaging systems, customer support chat, AI chatbots, or any real-time conversation features. Provides comprehensive guidance on messages, typing indicators, file attachments, @mentions, suggestions, header/footer customization, templates, load-on-demand, message toolbars, RTL support, localization, accessibility features, and complete chat interface implementations with working code examples."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Implementing Syncfusion TypeScript Chat UI

## Overview

The Chat UI component provides a modern, feature-rich interface for building conversational applications including customer support chat, AI chatbots, messaging systems, and collaborative communication tools.

The Syncfusion Chat UI (`ChatUI`) control is from the `@syncfusion/ej2-interactive-chat` package that provides:

- **Message Management** - Display, send, and manage chat messages with rich content
- **User Differentiation** - Visual distinction between current user and other participants
- **Real-time Indicators** - Typing indicators for active participants
- **File Attachments** - Upload and display files, images, and documents in messages
- **Smart Features** - @mentions, quick reply suggestions, message replies
- **Customization** - Templates for messages, empty states, headers, footers
- **Accessibility** - Keyboard navigation, ARIA support, RTL layout
- **Message Toolbar** - Per-message actions (Copy, Reply, Pin, Delete)
- **Load on Demand** - Lazy loading for large conversation histories

**Package:** `@syncfusion/ej2-interactive-chat`

**Dependencies:** ej2-base, ej2-navigations, ej2-inputs, ej2-buttons, ej2-dropdowns, ej2-popups

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation
- CSS imports for themes (material, bootstrap, fabric, etc.)
- Basic Chat UI initialization
- UserModel configuration (current user and participants)
- MessageModel structure for initial messages
- Component dimensions (width, height)
- created event and component lifecycle

### Messages Configuration
📄 **Read:** [references/messages.md](references/messages.md)
- MessageModel properties (id, text, author, timestamp, status)
- messages property - initial message collection
- Message status indicators (sent, received, read)
- Message replies (replyTo, MessageReplyModel)
- Message flags (isForwarded, isPinned)
- Auto-scroll behavior (autoScrollToBottom)
- Message grouping by sender
- Mentions in messages (mentionUsers array)
- Attached files in messages

### Header & Footer Configuration
📄 **Read:** [references/header-footer.md](references/header-footer.md)
- Show/hide header and footer (showHeader, showFooter)
- Header text and icon (headerText, headerIconCss)
- Header toolbar configuration (headerToolbar, ToolbarSettingsModel)
- Toolbar items setup (ToolbarItemModel with text, icon, alignment, tooltip)
- Toolbar item click events (itemClicked)
- Footer placeholder text customization
- Footer template for custom layouts

### Typing Indicator
📄 **Read:** [references/typing-indicator.md](references/typing-indicator.md)
- Show/hide typing indicator (typingUsers property)
- Dynamic typing user updates (UserModel array)
- Multiple users typing scenarios
- Custom typing indicator template (typingUsersTemplate)
- userTyping event (isTyping, message, user)

### Templates & Customization
📄 **Read:** [references/templates.md](references/templates.md)
- Empty chat template (emptyChatTemplate)
- Message template (messageTemplate) with context
- Typing users template (typingUsersTemplate)
- Time break template (timeBreakTemplate)
- Suggestion template (suggestionTemplate)
- Footer template (footerTemplate)
- Template context and data binding patterns

### Timebreak & Timestamp
📄 **Read:** [references/timebreak-timestamp.md](references/timebreak-timestamp.md)
- Show time breaks (showTimeBreak) for date-based grouping
- Time break template customization
- Show timestamps (showTimeStamp) per message
- Global timestamp format (timeStampFormat)
- Per-message timestamp format override
- Date/time formatting patterns
- Culture-based formatting

### File Attachments
📄 **Read:** [references/file-attachments.md](references/file-attachments.md)
- Enable attachments (enableAttachments)
- Attachment settings (attachmentSettings, FileAttachmentSettingsModel)
- Server upload configuration (saveUrl, removeUrl)
- Save format options (Base64 vs Blob)
- File type restrictions (allowedFileTypes)
- File size limits (maxFileSize)
- Maximum attachment count (maximumCount)
- Drag and drop support (enableDragAndDrop)
- Custom attachment templates (attachmentTemplate, previewTemplate)
- Attachment events (click, upload, success, failure, removed)

### @Mention Integration
📄 **Read:** [references/mention.md](references/mention.md)
- Mention trigger character (mentionTriggerChar, default '@')
- Mention user list (mentionUsers property)
- UserModel configuration for mentions
- Mention popup filtering
- mentionSelect event and cancellation
- Mention data in messages
- Custom mention handling

### Suggestions
📄 **Read:** [references/suggestions.md](references/suggestions.md)
- Quick reply suggestions (suggestions property)
- Suggestion template customization (suggestionTemplate)
- Displaying suggestions above input
- Suggestion click behavior
- Dynamic suggestion updates

### Load on Demand
📄 **Read:** [references/load-on-demand.md](references/load-on-demand.md)
- Enable lazy loading (loadOnDemand property)
- Scroll-triggered message loading
- Performance optimization for large conversations
- Pagination patterns
- Adding older messages programmatically

### Methods
📄 **Read:** [references/methods.md](references/methods.md)
- addMessage() - add string or MessageModel
- updateMessage() - modify existing messages
- scrollToBottom() - scroll to latest message
- scrollToMessage() - scroll to specific message by ID
- focus() - set focus on input textarea
- refresh() and dataBind() for updates
- Other component methods

### Events
📄 **Read:** [references/events.md](references/events.md)
- created - component initialization
- messageSend - before sending message (with cancellation)
- userTyping - typing status updates
- mentionSelect - mention selection handling
- itemClicked - toolbar item clicks (header and message toolbars)
- Attachment events (click, beforeUpload, uploadSuccess, uploadFailure, removed)
- Event handling patterns

### Message Toolbar & Appearance
📄 **Read:** [references/message-toolbar-appearance.md](references/message-toolbar-appearance.md)
- Message toolbar settings (messageToolbarSettings)
- Per-message toolbar items (Copy, Reply, Pin, Delete)
- Custom toolbar items
- Message toolbar click events
- Compact mode (enableCompactMode) - left-align all messages
- CSS customization (cssClass)
- Theme integration
- RTL support (enableRtl)
- Localization (locale)
- Persistence (enablePersistence)
- Accessibility features

---

## Quick Start

### Basic Chat UI Setup

```typescript
import { ChatUI, UserModel, MessageModel } from '@syncfusion/ej2-interactive-chat';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

// Define current user
let currentUser: UserModel = {
    id: "user1",
    user: "Albert",
    avatarUrl: "https://example.com/avatar1.png"
};

// Define other participant
let participantUser: UserModel = {
    id: "user2",
    user: "Michale Suyama",
    avatarUrl: "https://example.com/avatar2.png"
};

// Initial messages
let chatMessages: MessageModel[] = [
    {
        author: currentUser,
        text: "Hi Michale, are we on track for the deadline?"
    },
    {
        author: participantUser,
        text: "Yes, the design phase is complete."
    },
    {
        author: currentUser,
        text: "Great! I'll review it and send feedback by today."
    }
];

// Initialize Chat UI
let chatUI: ChatUI = new ChatUI({
    user: currentUser,
    messages: chatMessages,
    headerText: 'Michale Suyama',
    showTimeStamp: true,
    autoScrollToBottom: true
});

// Render
chatUI.appendTo('#chatUI');
```

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>Chat UI Example</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <!-- CSS imports -->
    <link href="https://cdn.syncfusion.com/ej2/32.1.19/tailwind3.css" rel="stylesheet" />
</head>
<body>
    <div class="chatui-container" style="height: 500px; width: 400px;">
        <div id="chatUI"></div>
    </div>
</body>
</html>
```

### CSS Imports (via npm)

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-interactive-chat/styles/tailwind3.css';
```

---

## Common Patterns

### Add a New Message Programmatically

```typescript
// Add as string (uses current user)
chatUI.addMessage("This is a new message");

// Add as MessageModel (any user)
chatUI.addMessage({
    text: "Response from bot",
    author: botUser,
    timestamp: new Date()
});
```

### Handle Message Send Event

```typescript
let chatUI: ChatUI = new ChatUI({
    user: currentUser,
    messageSend: (args: MessageSendEventArgs) => {
        console.log("Message being sent:", args.message.text);
        
        // Cancel send if needed
        if (args.message.text.trim() === '') {
            args.cancel = true;
        }
        
        // Send to server/API
        sendToServer(args.message);
    }
});
```

### Show Typing Indicator

```typescript
// Show user is typing
chatUI.typingUsers = [participantUser];

// Hide typing indicator (after message received)
chatUI.typingUsers = [];
```

### Enable File Attachments with Upload

```typescript
let chatUI: ChatUI = new ChatUI({
    user: currentUser,
    enableAttachments: true,
    attachmentSettings: {
        saveUrl: 'https://your-server.com/api/upload',
        removeUrl: 'https://your-server.com/api/remove',
        allowedFileTypes: '.jpg,.png,.pdf,.docx',
        maxFileSize: 5242880, // 5MB in bytes
        maximumCount: 3
    },
    attachmentUploadSuccess: (args) => {
        console.log("File uploaded successfully:", args.file.name);
    }
});
```

### Add @Mention Support

```typescript
let mentionableUsers: UserModel[] = [
    { id: "user1", user: "Albert" },
    { id: "user2", user: "Michale" },
    { id: "user3", user: "Janet" }
];

let chatUI: ChatUI = new ChatUI({
    user: currentUser,
    mentionTriggerChar: '@',
    mentionUsers: mentionableUsers,
    mentionSelect: (args: MentionSelectEventArgs) => {
        console.log("Mentioned user:", args.itemData);
    }
});
```

### Update Existing Message

```typescript
// Update message content
chatUI.updateMessage({
    text: "Updated message content",
    author: currentUser
}, "message-id-123");
```

### Scroll to Specific Message

```typescript
// Scroll to bottom (latest message)
chatUI.scrollToBottom();

// Scroll to specific message by ID
chatUI.scrollToMessage("message-id-456");
```

---

## Key Properties Summary

| Property | Type | Description |
|----------|------|-------------|
| `user` | UserModel | Current user interacting with the chat |
| `messages` | MessageModel[] | Collection of chat messages |
| `showHeader` | boolean | Show/hide header (default: true) |
| `showFooter` | boolean | Show/hide footer (default: true) |
| `headerText` | string | Text displayed in header |
| `placeholder` | string | Input placeholder text |
| `typingUsers` | UserModel[] | Users currently typing |
| `showTimeStamp` | boolean | Show message timestamps (default: true) |
| `showTimeBreak` | boolean | Group messages by date (default: false) |
| `autoScrollToBottom` | boolean | Auto-scroll on new message (default: false) |
| `enableAttachments` | boolean | Enable file attachments (default: false) |
| `attachmentSettings` | FileAttachmentSettingsModel | File upload configuration |
| `mentionTriggerChar` | string | Character to trigger mentions (default: '@') |
| `mentionUsers` | UserModel[] | Users available for @mention |
| `suggestions` | string[] | Quick reply suggestions |
| `loadOnDemand` | boolean | Lazy load messages (default: false) |
| `enableCompactMode` | boolean | Left-align all messages (default: false) |
| `messageToolbarSettings` | MessageToolbarSettingsModel | Per-message toolbar config |
| `headerToolbar` | ToolbarSettingsModel | Header toolbar config |
| `width` | string \| number | Component width (default: '100%') |
| `height` | string \| number | Component height (default: '100%') |
| `cssClass` | string | Custom CSS classes |
| `enableRtl` | boolean | Right-to-left layout (default: false) |
| `locale` | string | Localization culture |

---

## Common Use Cases

### Customer Support Chat
- Real-time agent-customer conversations
- Typing indicators for agent availability
- File attachments for screenshots/documents
- Message status (sent, delivered, read)
- Quick reply suggestions for common responses

### AI Chatbot Interface
- User-bot message differentiation
- Typing indicator during AI processing
- Suggested responses and quick actions
- Message templates for rich responses
- Empty state with welcome message

### Team Collaboration Tool
- @mention team members
- Message replies and threading
- Pin important messages
- File sharing with preview
- Load on demand for long conversations

### Live Help Widget
- Compact mode for embedded widget
- Custom header with agent info
- Footer with typing status
- Auto-scroll to latest message
- Minimize/maximize functionality

### Documentation Q&A
- Question-answer format with clear user distinction
- Code snippet attachments
- Time breaks for conversation sessions
- Message toolbar with copy functionality
- Search and scroll to specific messages
