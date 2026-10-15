---
name: syncfusion-aspnetcore-ai-assistview
description: Implement the Syncfusion ASP.NET Core AI AssistView control for interactive AI-powered assistance interfaces. Use this skill when implementing AI assistants, prompt suggestions, custom views, file attachments, markdown responses, customizable templates, assistance features, file uploads, or customizing AI conversation UI in ASP.NET Core applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core AI AssistView Control

## Overview

The Syncfusion AI AssistView is a comprehensive component for building AI-powered assistance interfaces in ASP.NET Core applications. It provides support for:
- Configurable prompt suggestions with custom headers
- Prompt-response collections with markdown rendering
- File attachments with validation and size restrictions
- Custom views and templates for complete UI control
- Event-driven architecture for real-time interaction
- Toolbar customization for both header and footer areas
- Icon customization for prompts and responses

## Key Features

- **Prompt Suggestions**: Guide users with predefined suggestions
- **Markdown Support**: Render formatted content with built-in markdown converter
- **Custom Templates**: Customize banners, prompts, responses, and suggestions
- **File Attachments**: Enable users to attach files with the prompt
- **Multiple Views**: Support for Assist and Custom view types
- **Toolbar Customization**: Customize header and footer toolbar items
- **Icon Customization**: Personalize prompt and response avatars
- **Stop Responding**: Cancel in-progress AI responses with the stop responding button
- **Header Visibility**: Show or hide the header bar via `showHeader`
- **Helpful Feedback**: Mark responses as helpful using `PromptModel.isResponseHelpful`
- **Event Driven**: Full event lifecycle for complete control
- **Methods**: Dynamic prompt execution and response management

## Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and NuGet package setup
- TagHelper registration and configuration
- CSS/script resource linking
- Basic control initialization
- Prompt suggestions and responses configuration

### Configuring Prompts and Responses
📄 **Read:** [references/assist-view-configuration.md](references/assist-view-configuration.md)
- Setting prompt text and placeholders
- Prompt-response collection initialization
- Markdown response rendering
- Prompt suggestions with headers
- Avatar customization (prompt and response icons)
- Clear button and scroll-to-bottom features
- Show or hide the header bar (`showHeader`)
- Marking a response as helpful (`PromptModel.isResponseHelpful`)

### Appearance and Styling
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Width and height configuration
- CSS class customization
- Custom styling and theming
- Component container styling

### Handling Events
📄 **Read:** [references/events-handling.md](references/events-handling.md)
- Created event for initialization
- PromptRequest event for handling prompts (with `cancel`, `attachedFiles`, `promptSuggestions`)
- PromptChanged event for text changes (with `value`, `previousValue`)
- StopRespondingClick event for cancelling in-progress responses
- Attachment events (upload, success, failure, removed, click)

### Using Methods and APIs
📄 **Read:** [references/methods-and-apis.md](references/methods-and-apis.md)
- addPromptResponse() method for string and object responses
- executePrompt() method for dynamic prompt execution
- Public method signatures and usage patterns

### Templates and Custom Views
📄 **Read:** [references/templates-and-views.md](references/templates-and-views.md)
- Banner templates for welcome messages
- Prompt item templates for custom prompt rendering
- Response item templates for response customization
- Suggestion item templates
- Footer templates for custom actions
- Custom view types and active view configuration

### Toolbar Configuration
📄 **Read:** [references/toolbar-and-items.md](references/toolbar-and-items.md)
- Footer toolbar items and positioning
- Header toolbar configuration with icons
- Item types (Button, Separator, Input)
- Item alignment, visibility, and disabled states
- Tooltip text and CSS classes
- Built-in toolbar items for prompts and responses
- Custom toolbar items with templates and events
- `ToolbarItemClickedEventArgs` — item, dataIndex, cancel, event, name
- `itemClicked` event for prompt and response toolbar items

### File Attachments
📄 **Read:** [references/file-attachments.md](references/file-attachments.md)
- Enabling file attachments
- Setting save and remove URLs
- File type restrictions (`allowedFileTypes`)
- Maximum file size configuration
- Maximum attachment count limits
- Pre-loading attached files in prompts (`PromptModel.attachedFiles`)

## Quick Start

```razor
@using Syncfusion.EJ2.InteractiveChat;

<div class="aiassist-container" style="height: 350px; width: 650px;">
    <ejs-aiassistview id="aiAssistView" promptRequest="onPromptRequest" created="onCreated"></ejs-aiassistview>
</div>

<script>
    var assistObj;
    function onCreated() {
        assistObj = this;
    }
    function onPromptRequest(args) {
        setTimeout(() => {
            let defaultResponse = 'For real-time prompt processing, connect the AI AssistView control to your preferred AI service, such as OpenAI or Azure Cognitive Services. Ensure you obtain the necessary API credentials to authenticate and enable seamless integration.';
            assistObj.addPromptResponse(defaultResponse);
        }, 2000);
    }
</script>
```

## Common Patterns

### Pattern 1: Adding Prompt Suggestions
```razor
@using Syncfusion.EJ2.InteractiveChat;

@{
    var suggestions = new string[] { "How do I prioritize my tasks?", "How can I improve my time management skills?" };
}

<div class="aiassist-container" style="height: 350px; width: 650px;">
    <ejs-aiassistview id="aiAssistView" 
        promptSuggestions="@suggestions" 
        promptRequest="onPromptRequest" 
        created="onCreated">
    </ejs-aiassistview>
</div>

<script>
    var assistObj;
    function onCreated() {
        assistObj = this;
    }
    function onPromptRequest(args) {
        setTimeout(() => {
            assistObj.addPromptResponse('Response for: ' + args.prompt);
        }, 2000);
    }
</script>
```

### Pattern 2: Markdown Response Rendering
```razor
@using Syncfusion.EJ2.InteractiveChat;
@using System.Text.Json;

@{
   var markdownData = new[]
    {
        new {
            prompt = "What is Markdown?",
            response = "# Markdown Guide\n\nMarkdown is a lightweight markup language:\n\n- **Headers:** Use `#`, `##`, `###`\n- **Bold:** `**text**` for bold\n- **Lists:** Use `-` for bullet points",
            suggestions = new string[] {"How do I use bold?"}
        }
    };
    var promptsJson = JsonSerializer.Serialize(markdownData);
}

<div class="aiassist-container" style="height: 350px; width: 650px;">
    <ejs-aiassistview id="aiAssistView" 
        prompts="@markdownData" 
        promptRequest="onPromptRequest" 
        created="onCreated">
    </ejs-aiassistview>
</div>

<script>
    var assistObj;
    var prompts = @Html.Raw(promptsJson);
    function onCreated() {
        assistObj = this;
    }
    function onPromptRequest(args) {
        setTimeout(() => {
            var foundPrompt = prompts.find(prompt => prompt.prompt == args.prompt);
            if (foundPrompt) {
                assistObj.addPromptResponse(foundPrompt.response);
            }
        }, 2000);
    }
</script>
```

### Pattern 3: File Attachments
```razor
@using Syncfusion.EJ2.InteractiveChat;

<div class="aiassist-container" style="height: 350px; width: 650px;">
    <ejs-aiassistview id="aiAssistView" 
        enableAttachments="true" 
        promptRequest="onPromptRequest" 
        created="onCreated">
        <e-aiassistview-attachmentsettings 
            saveUrl=@Url.Content("https://services.syncfusion.com/aspnet/production/api/FileUploader/Save") 
            removeUrl=@Url.Content("https://services.syncfusion.com/aspnet/production/api/FileUploader/Remove")>
        </e-aiassistview-attachmentsettings>
    </ejs-aiassistview>
</div>

<script>
    var assistObj;
    function onCreated() {
        assistObj = this;
    }
    function onPromptRequest(args) {
        setTimeout(() => {
            assistObj.addPromptResponse('Processing your prompt with attachments');
        }, 2000);
    }
</script>
```
