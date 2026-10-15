---
name: syncfusion-angular-chat-ui
description: Implement the Syncfusion Angular Chat UI component. Use this skill whenever users need to implement messaging, real-time conversations, file attachments, typing indicators, user mentions, or bot integrations (Dialogflow, Microsoft Bot Framework) in Angular applications. Essential for customer support chatbots, team messaging apps, AI-powered assistants, and collaborative communication interfaces.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Angular Chat UI Component

## Component Overview

The Syncfusion Angular Chat UI component provides a complete, feature-rich solution for building conversational interfaces in Angular applications. It enables real-time messaging, user presence indicators, file attachments, typing indicators, and seamless integration with bot frameworks and AI services.

**Key Capabilities:**
- **Message Management** - Configure messages with text, rich templates, media, replies, pinning, and forwarding
- **User System** - Define current user, presence status, avatars with custom styling and mentions
- **Appearance Control** - Customize width, height, placeholder, CSS classes, compact mode, and suggestions
- **Header & Footer** - Control visibility, titles, icons, custom templates, and header toolbar with actions
- **Events & Interactions** - Handle message send, typing indicators, toolbar actions (copy, reply, pin, delete)
- **Templates** - Customize empty chat, messages, time breaks, typing indicators, and suggestion items
- **File Attachments** - Enable uploads with type/size restrictions, drag-and-drop, custom paths, attachment click events
- **Methods** - Programmatically add/update messages, scroll to bottom, scroll to specific message, focus input
- **Globalization** - Support multiple languages (i18n), RTL text direction, and locale-based formatting
- **Advanced Features** - Load on demand, state persistence, mentions, message status, time breaks, bot integrations

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup (Ivy vs ngcc)
- Setup Angular environment with Angular CLI
- Basic component initialization
- Configuring messages and users
- CSS imports and theme configuration
- Running the application

### Messages and Users
📄 **Read:** [references/messages-and-users.md](references/messages-and-users.md)
- Message configuration and properties (text, id, author, timestamp)
- User models and avatars
- Defining current user with unique identifier
- Avatar URLs and custom background colors
- User presence status (online, offline, away, busy)
- Message pinning for important messages
- **Enhanced MessageReplyModel** with complete interface documentation
- **Reply with attachments** and timestamp formatting
- **Dynamic reply creation** patterns
- Message forwarding
- Compact mode for group conversations
- Markdown message support

### Appearance and Layout
📄 **Read:** [references/appearance-and-layout.md](references/appearance-and-layout.md)
- Placeholder text customization
- Width and height properties
- CSS class customization for styling
- Compact mode configuration
- Auto-scroll to bottom behavior
- Suggestions display for quick replies

### Header and Footer
📄 **Read:** [references/header-and-footer.md](references/header-and-footer.md)
- Header visibility control
- Header text (title) configuration
- Header icon customization with CSS classes
- **Header toolbar with custom actions** (call, video, settings, profile)
- **ToolbarSettingsModel configuration** with items and itemClicked event
- Footer visibility and control
- Footer template for custom layouts

### Events and Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- Component lifecycle events (created)
- Message send event handling
- User typing event and typing indicators
- Message toolbar configuration
- **Complete ToolbarItemModel properties** (align, cssClass, disabled, iconCss, tabIndex, template, text, tooltip, type, visible)
- Toolbar items customization (copy, reply, pin, delete, forward)
- Item click event handling
- Toolbar width configuration
- Before/after attachment events
- **Header toolbar vs message toolbar differences**

### Templates and Content
📄 **Read:** [references/templates-and-content.md](references/templates-and-content.md)
- Message template customization
- Empty chat template for initial state
- Time break template for date separators
- Message status and delivery icons
- Timestamp display and visibility
- Timestamp format customization (dd/MM/yyyy hh:mm a)
- **Suggestion template customization** with context variables (index, suggestion)
- **Advanced suggestion examples** (category-based, search-highlighted, icon-based)
- Typing indicator template

### Attachments and File Handling
📄 **Read:** [references/attachments-and-file-handling.md](references/attachments-and-file-handling.md)
- Enable file attachment support
- Attachment settings configuration
- Server endpoints (saveUrl, removeUrl)
- File type restrictions and filters
- File size limits (default 30MB)
- **SaveFormat enum** (Blob vs Base64) with advantages and use cases
- **Custom storage paths** with path property for CDN/cloud storage
- Drag-and-drop file upload
- Maximum file count restrictions
- File preview templates
- Attachment templates
- **attachmentClick event** for custom file interactions (preview, download, metadata)
- **attachedFile property** for pre-populating messages with files
- Upload event handling (success, failure)

### Methods and Programmatic Control
📄 **Read:** [references/methods-and-programmatic-control.md](references/methods-and-programmatic-control.md)
- addMessage() - Add new messages programmatically
- updateMessage() - Edit existing messages
- scrollToBottom() - Scroll to latest messages
- **scrollToMessage(messageId)** - Navigate to specific message (pinned messages, search results, deep linking)
- **focus()** - Set focus to chat input programmatically (auto-focus, modal close, command execution)
- ViewChild component access
- Accessing chat instance for direct control

### Globalization and Localization
📄 **Read:** [references/globalization-and-localization.md](references/globalization-and-localization.md)
- Localization (L10n) and i18n support
- Typing indicator translations
- Multiple language support
- Right-to-Left (RTL) layout for Arabic, Hebrew, Persian
- Locale configuration
- Language-specific string customization

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- **State persistence** with enablePersistence (localStorage, cross-tab sync, browser refresh protection)
- **Custom persistence implementations** for sensitive data
- Load on demand for large message histories (1000+ messages)
- Mention integration with @character
- Trigger character customization
- Predefined mentions in messages
- mentionSelect event handling
- Message status tracking (sent, delivered, read)
- Time breaks between messages for date organization

### Bot Integrations
📄 **Read:** [references/bot-integrations.md](references/bot-integrations.md)
- Google Dialogflow integration for AI conversations
- Microsoft Bot Framework integration with Azure
- Direct Line API configuration
- Token server setup for security
- Backend API configuration
- Secure credential handling
- Bot response message handling
- Session management

---

## Quick Start Example

Here's a minimal example to get started:

```typescript
import { Component } from '@angular/core';
import { ChatUIModule } from '@syncfusion/ej2-angular-interactive-chat';
import { UserModel } from '@syncfusion/ej2-interactive-chat';

@Component({
  imports: [ChatUIModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div id="chatui" ejs-chatui 
         [user]="currentUserModel" 
         headerText="TeamSync Professionals">
      <e-messages>
        <e-message text="Hi, how are you?" [author]="currentUserModel"></e-message>
        <e-message text="Great! How can I help?" [author]="michaleUserModel"></e-message>
      </e-messages>
    </div>
  `,
  styles: [`
    #chatui {
      height: 500px;
      width: 100%;
    }
  `]
})
export class AppComponent {
  public currentUserModel: UserModel = { user: 'Albert', id: 'user1' };
  public michaleUserModel: UserModel = { user: 'Michale', id: 'user2' };
}
```

**Installation:**
```bash
npm install @syncfusion/ej2-angular-interactive-chat
```

**CSS Import (src/styles.css):**
```css
@import "../node_modules/@syncfusion/ej2-base/styles/material3.css";
@import '../node_modules/@syncfusion/ej2-inputs/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-popups/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-dropdowns/styles/material3.css';
@import '../node_modules/@syncfusion/ej2-angular-interactive-chat/styles/material3.css';
```

---

## Key Components and Props

**Core Component:**
- `<ejs-chatui>` - Main chat container
  - `[user]` - Current user model (UserModel)
  - `[messages]` - Message collection
  - `headerText` - Header title
  - `[headerToolbar]` - Header toolbar with custom actions
  - `[height]` / `[width]` - Dimensions
  - `[enableAttachments]` - File upload support
  - `[enablePersistence]` - State persistence across sessions
  - `[enableRtl]` - Right-to-left layout
  - `[attachmentSettings]` - File upload configuration
  - `[messageToolbarSettings]` - Message-level toolbar
  - `[suggestions]` - Quick reply suggestions
  - `[suggestionTemplate]` - Custom suggestion rendering

**Message Element:**
- `<e-message>` - Individual message
  - `text` - Message content
  - `[author]` - User who sent message
  - `[timeStamp]` - Message timestamp
  - `[timeStampFormat]` - Custom timestamp format
  - `[isPinned]` - Pin importance
  - `[replyTo]` - Thread context (MessageReplyModel)
  - `[isForwarded]` - Forwarded indicator
  - `[attachedFile]` - Pre-populated file attachments (FileInfo)
  - `[status]` - Message delivery status (MessageStatusModel)
  - `[mentionUsers]` - Users mentioned in message

**User Model Properties:**
- `id` - Unique user identifier
- `user` - Display name
- `avatarUrl` - Avatar image
- `avatarBgColor` - Avatar background color
- `statusIconCss` - Presence status icon

---

## Common Use Cases

**1. Customer Support Chat**
- Configure header with support team name
- Enable file attachments for screenshots/documents
- Use message status for delivery tracking
- Integrate with Dialogflow for AI-powered responses

**2. Team Messaging App**
- Multiple users with presence status
- Mention teammates with @mentions
- Pin important decisions/announcements
- Use timestamp format for timezone support

**3. AI Assistant**
- Integrate with Microsoft Bot Framework or Dialogflow
- Show typing indicator while bot responds
- Suggest quick replies with suggestions array
- Handle bot-specific message formatting

**4. Load Performance**
- Enable load on demand for 1000+ message conversations
- Implement auto-scroll for smooth scrolling
- Use compact mode to reduce vertical space
- Lazy load attachments and media

**5. Internationalization (i18n)**
- Provide localized typing indicators ("X is typing")
- Enable RTL for Arabic/Hebrew/Persian users
- Customize date/time format per locale
- Translate button labels and placeholders

---
