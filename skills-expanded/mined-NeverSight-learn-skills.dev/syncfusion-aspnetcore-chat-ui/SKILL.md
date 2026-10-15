---
name: syncfusion-aspnetcore-chat-ui
description: Implement the Syncfusion ASP.NET Core Chat-UI control for interactive, real-time messaging components. Use this skill when implementing chat interfaces, message management, file uploads and attachments, appearance customization with templates, message events, typing indicators, or internationalization and RTL layouts in ASP.NET Core applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core Chat-UI Control

## Overview

The Chat-UI component provides a complete conversational interface with real-time messaging, file attachments, user presence, and extensive customization options. This skill guides you through implementing chat interfaces for customer support, team collaboration, and interactive applications using ASP.NET Core tag helpers and Razor pages.

The Chat-UI component is an interactive messaging interface featuring:
- **Rich Message Support:** Text content, pinned messages, threaded replies, message forwarding
- **User Management:** Multi-user conversations, presence status, user configuration
- **File Attachments:** Upload, preview, download with file type/size restrictions
- **Event System:** Created, message send, user typing, attachment events
- **Templates:** Customizable UI for empty chat, messages, typing indicator, suggestions, footer
- **Appearance:** Configurable placeholder, width, height, CSS classes
- **Timestamps:** Show/hide timestamps with customizable format
- **Advanced Features:** Compact mode, globalization, RTL support, speech-to-text

## Quick Start Example

```razor
@using Syncfusion.EJ2.InteractiveChat;

<div style="height:400px; width:450px">
    <ejs-chatui id="chatUI">
        <e-chatui-user id="user1" user="Albert"></e-chatui-user>
        <e-chatui-messages>
            @foreach (var message in ViewBag.ChatMessagesData)
            {
                <e-chatui-message text="@message.Text" author="@message.Author"></e-chatui-message>
            }
        </e-chatui-messages>
    </ejs-chatui>
</div>
```

**Corresponding C# Controller:**
```csharp
using Syncfusion.EJ2.InteractiveChat;

public ActionResult Default()
{
    var currentUser = new ChatUIUser() { Id = "user1", User = "Albert" };
    var otherUser = new ChatUIUser() { Id = "user2", User = "Michale Suyama" };
    
    var messages = new List<ChatUIMessage>()
    {
        new ChatUIMessage() { Text = "Hi Michale, are we on track?", Author = currentUser },
        new ChatUIMessage() { Text = "Yes, all set!", Author = otherUser }
    };
    
    ViewBag.ChatMessagesData = messages;
    return View();
}
```

## Documentation Navigation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- NuGet package installation and dependencies
- ASP.NET Core project setup with Razor pages
- Tag helper registration and configuration
- CDN stylesheet and script setup
- Script manager registration
- Basic Chat-UI implementation
- Initial user and message configuration

### Message Configuration
📄 **Read:** [references/messages-configuration.md](references/messages-configuration.md)
- Message model setup and properties
- Adding and managing text messages
- Message configuration (ID, text, author, timestamp)
- Pinned messages for important conversations
- Reply-to for threaded conversations
- Forwarded messages and message tracking
- Compact mode for streamlined layouts

### User Configuration
📄 **Read:** [references/user-configuration.md](references/user-configuration.md)
- ChatUIUser model setup and properties
- User identity configuration
- Setting current user context
- Multi-user support and management
- User presence and status indicators
- Avatar configuration and styling

### Appearance & Styling
📄 **Read:** [references/appearance-styling.md](references/appearance-styling.md)
- Placeholder text customization
- Width and height configuration
- CSS class application and customization
- Component-level styling
- Theme customization approaches
- Responsive design patterns

### Events & Interactions
📄 **Read:** [references/events-interactions.md](references/events-interactions.md)
- Created event for initialization
- Message send event handling
- User typing event detection
- Attachment upload events (before, success, failure)
- Attachment removal and click events
- Event binding patterns and best practices

### Methods & API
📄 **Read:** [references/methods-api.md](references/methods-api.md)
- addMessage method for programmatic message addition
- updateMessage method for editing existing messages
- scrollToBottom method for view navigation
- Real-time integration with SignalR
- Best practices for performance and error handling

### Templates & Customization
📄 **Read:** [references/templates-customization.md](references/templates-customization.md)
- Empty chat template for initial states
- Message custom templates with jsrender
- Time break template for message organization
- Typing indicator template customization
- Suggestion template for auto-complete
- Footer template for custom input areas
- Advanced template patterns and styling

### File Attachments
📄 **Read:** [references/file-attachments.md](references/file-attachments.md)
- Enable attachment support with enableAttachments
- Configure attachment settings
- Save and remove URL endpoints
- File type restrictions (allowedFileTypes)
- File size limits (maxFileSize)
- Save format options (Blob vs Base64)
- Drag-and-drop support configuration
- Server path and upload handling

### Header & Footer
📄 **Read:** [references/header-footer.md](references/header-footer.md)
- Show/hide header with showHeader property
- Header text configuration and display
- Header icon styling with headerIconCss
- Show/hide footer with showFooter property
- Footer template customization
- Input area configuration

### Timestamps & Time Breaks
📄 **Read:** [references/timestamps-timebreaks.md](references/timestamps-timebreaks.md)
- Show/hide timestamps with showTimeStamp
- Timestamp format customization (timeStampFormat)
- Time break separators for message organization
- Date-wise message grouping
- Timestamp template patterns

### Typing Indicators
📄 **Read:** [references/typing-indicator.md](references/typing-indicator.md)
- Show/hide typing indicator
- Multi-user typing display
- Typing indicator template customization
- User presence detection
- Styling typing indicator UI

### Mentions & User References
📄 **Read:** [references/mentions-integration.md](references/mentions-integration.md)
- Configure mentionable users
- Mention trigger character customization
- Predefined mentions in messages
- Mention selection and events
- Mention item template and styling

### Globalization & RTL
📄 **Read:** [references/globalization-rtl.md](references/globalization-rtl.md)
- Localization and multi-language support
- Setting culture and locale
- RTL (Right-to-Left) layout support
- Language-specific templates
- Speech-to-text localization

### Toolbar Configuration
📄 **Read:** [references/toolbar-configuration.md](references/toolbar-configuration.md)
- Header toolbar configuration and items
- Message toolbar settings and customization
- Toolbar item configuration and events
- Custom toolbar actions and handlers
- Toolbar visibility and styling

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Load on demand with scroll handling
- Auto-scroll to bottom behavior
- Enable persistence for state management
- Performance optimization techniques
- Server-side data loading strategies

### Suggestions Feature
📄 **Read:** [references/suggestions-feature.md](references/suggestions-feature.md)
- Enable suggestions with suggestions property
- Suggestion template customization
- Context-based suggestion filtering
- Suggestion selection and handling
- Custom suggestion UI and styling

## Common Patterns

### Create a Basic Chat Interface
```razor
<div style="height:400px; width:500px">
    <ejs-chatui id="chatUI" 
                 placeholder="Type a message..."
                 showHeader="true"
                 headerText="Support Chat">
        <e-chatui-user id="user1" user="Support Agent"></e-chatui-user>
    </ejs-chatui>
</div>
```

### Add Messages with Events
```razor
<ejs-chatui id="chatUI" messageSend="onMessageSend">
    <e-chatui-user id="user1" user="Albert"></e-chatui-user>
    <e-chatui-messages>
        @foreach (var message in ViewBag.ChatMessagesData)
        {
            <e-chatui-message text="@message.Text" 
                            author="@message.Author"
                            timeStamp="@message.TimeStamp"></e-chatui-message>
        }
    </e-chatui-messages>
</ejs-chatui>

<script>
    function onMessageSend(args) {
        // Handle message send event
        console.log("Message sent:", args);
    }
</script>
```

### Enable File Attachments
```razor
<ejs-chatui id="chatUI" enableAttachments="true">
    <e-chatui-user id="user1" user="Albert"></e-chatui-user>
    <e-chatui-attachmentsettings 
        saveUrl=@Url.Content("https://services.syncfusion.com/aspnet/production/api/FileUploader/Save")
        removeUrl=@Url.Content("https://services.syncfusion.com/aspnet/production/api/FileUploader/Remove")
        maxFileSize="5000000"
        allowedFileTypes=".pdf,.docx,.xlsx">
    </e-chatui-attachmentsettings>
</ejs-chatui>
```

## Key Properties

| Property | Type | Purpose |
|----------|------|---------|
| `id` | string | Unique identifier for the ChatUI component |
| `placeholder` | string | Input field hint text (default: "Type your message…") |
| `width` | string | Chat UI width (default: 100%) |
| `height` | string | Chat UI height (default: 100%) |
| `showHeader` | boolean | Display header section (default: true) |
| `headerText` | string | Header title/name display |
| `headerToolbar` | object | Configure toolbar items in header |
| `showFooter` | boolean | Display input footer (default: true) |
| `showTimeStamp` | boolean | Display message timestamps (default: true) |
| `timeStampFormat` | string | Timestamp format pattern (default: "dd/MM/yyyy hh:mm a") |
| `cssClass` | string | CSS classes for styling |
| `enableAttachments` | boolean | Enable file upload support (default: false) |
| `enableCompactMode` | boolean | Align all messages left (default: false) |
| `loadOnDemand` | boolean | Enable lazy loading of messages (default: false) |
| `autoScrollToBottom` | boolean | Automatically scroll to latest message (default: true) |
| `enablePersistence` | boolean | Persist chat state across sessions (default: false) |
| `suggestions` | array | Quick reply suggestions for users |
| `messageToolbarSettings` | object | Configure message-level toolbar actions |

## Common Use Cases

**Use Case 1: Customer Support Chat**
- Multiple support agents handling customer queries
- File attachment for screenshots/documents
- Message history with timestamps
- Typing indicators to show agent engagement
- Header with support agent name and status

**Use Case 2: Team Collaboration**
- Mention team members with @ mentions
- Pin important discussion points
- Forward messages for reference
- Message editing and deletion
- Multi-user presence indicators

**Use Case 3: Multilingual Support**
- RTL support for Arabic/Hebrew languages
- Localized UI strings via globalization
- Culture-specific timestamp formats
- Support for multiple character sets
