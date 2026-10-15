---
name: syncfusion-javascript-ai-assistview
description: "Implement the Syncfusion JavaScript AI AssistView control. Use this skill when users mention AI assistant interfaces, AI chat UI, conversational AI components, prompt-response interfaces, AI integration (OpenAI, Gemini, Ollama, LiteLLM, MCP), chat toolbars, file attachments in chat, speech-to-text, text-to-speech, custom AI views, prompt suggestions, markdown responses, or implementing any interactive AI assistant interface. Use this skill immediately for AIAssistView, AI chat control, interactive chat, ej2-interactive-chat package, AI conversation UI, or AI assistance components."
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion JavaScript AI AssistView Component

## Overview

The AI AssistView is an interactive chat component designed for building AI-powered conversational interfaces with support for prompts, responses, suggestions, custom toolbars, file attachments, speech features, and AI service integrations.

The AI AssistView component provides:

- **Prompt-Response System**: Display conversations with user prompts and AI responses
- **AI Service Integration**: Built-in support for major AI providers (OpenAI, Gemini, Ollama, etc.)
- **Toolbar Customization**: Header, footer, prompt, and response toolbars with custom items
- **File Attachments**: Upload and attach files to prompts
- **Speech Features**: Speech-to-text input and text-to-speech output
- **Custom Views**: Multiple view modes (Assist, Custom) with templates
- **Templates**: Customize banner, prompt items, response items, suggestions, and footer
- **Markdown Support**: Automatic markdown-to-HTML conversion for responses
- **Streaming Responses**: Real-time response streaming for AI outputs
- **Accessibility**: WCAG compliance with keyboard navigation and ARIA support

---

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation and dependencies (`@syncfusion/ej2-interactive-chat`)
- CSS imports and theme configuration
- Basic AI AssistView initialization
- First render with prompts and responses
- `promptRequest` event handling for AI integration
- Width, height, locale, and persistence configuration

### Assist View Configuration
📄 **Read:** [references/assist-view-configuration.md](references/assist-view-configuration.md)
- Setting prompt text and placeholder (`prompt`, `promptPlaceholder`)
- Prompt and response icon customization (`promptIconCss`, `responseIconCss`)
- Prompt-response collection (`prompts` property with `PromptModel[]`)
- Adding prompt suggestions (`promptSuggestions`, `promptSuggestionsHeader`)
- Show/hide clear button and header (`showClearButton`, `showHeader`)
- Enable scroll to bottom functionality (`enableScrollToBottom`)
- Markdown response rendering with built-in converter
- Response streaming (`enableStreaming`)

### AI Service Integrations
📄 **Read:** [references/ai-integrations.md](references/ai-integrations.md)
- OpenAI and Azure OpenAI integration with API setup
- Google Gemini integration and configuration
- Ollama LLM local model integration
- LiteLLM proxy service integration
- MCP Server integration for Model Context Protocol
- Custom AI service integration patterns
- `promptRequest` event best practices
- Error handling and response formatting

### Toolbar Configuration
📄 **Read:** [references/toolbar-configuration.md](references/toolbar-configuration.md)
- Header toolbar configuration (`toolbarSettings`)
- Footer toolbar setup (`footerToolbarSettings`, toolbar positioning: Inline/Bottom)
- Response toolbar items (`responseToolbarSettings`, like/dislike/copy/refresh)
- Prompt toolbar items (`promptToolbarSettings`)
- Custom toolbar items (text, icons, tooltips, alignment, templates)
- Toolbar item click events (`ToolbarItemClickedEventArgs`)
- Built-in toolbar items (send, attachment)

### Custom Views
📄 **Read:** [references/custom-views.md](references/custom-views.md)
- Adding custom views (`views` property with `AssistViewModel[]`)
- View types: Assist vs Custom (`AssistViewType` enum)
- Setting view name and icon (`name`, `iconCss`)
- View templates (`viewTemplate` for custom content)
- Active view management (`activeView` property)
- Switching between views programmatically

### Templates
📄 **Read:** [references/templates.md](references/templates.md)
- Banner template for welcome messages (`bannerTemplate`)
- Prompt item template customization (`promptItemTemplate`)
- Response item template formatting (`responseItemTemplate`)
- Prompt suggestion item template (`promptSuggestionItemTemplate`)
- Footer template for custom input areas (`footerTemplate`)
- Template context and data binding
- Template customization examples

### File Attachments
📄 **Read:** [references/file-attachments.md](references/file-attachments.md)
- Enabling attachments (`enableAttachments`)
- Attachment settings (`attachmentSettings` with allowed types, size limits, max count)
- Upload configuration (saveUrl, removeUrl)
- Attached files in prompts (`PromptModel.attachedFiles`)
- Attachment events (beforeUpload, success, failure, removed)
- File preview and click handling

### Speech to Text
📄 **Read:** [references/speech-to-text.md](references/speech-to-text.md)
- Speech-to-text configuration (`speechToTextSettings`)
- Browser speech recognition setup
- Language and locale settings
- Button and tooltip customization
- Interim results and transcript handling
- Microphone permissions and error handling

### Appearance Customization
📄 **Read:** [references/appearance.md](references/appearance.md)
- CSS class customization (`cssClass`)
- Width and height configuration
- RTL support (`enableRtl`)
- Theme customization with Syncfusion themes
- Custom styling examples
- Responsive design patterns

### Methods and Events
📄 **Read:** [references/methods-and-events.md](references/methods-and-events.md)
- Methods: `addPromptResponse()`, `executePrompt()`, `scrollToBottom()`, `refresh()`
- Events: `created`, `promptRequest`, `promptChanged`, `stopRespondingClick`
- Attachment events: `beforeAttachmentUpload`, `attachmentUploadSuccess`, etc.
- Event args interfaces and usage patterns
- Method usage examples

---

## Quick Start

### Basic AI AssistView

```typescript
import { AIAssistView, PromptRequestEventArgs } from '@syncfusion/ej2-interactive-chat';
import { enableRipple } from '@syncfusion/ej2-base';

enableRipple(true);

// Initialize AI AssistView
const aiAssistView: AIAssistView = new AIAssistView({
    promptSuggestions: [
        'How do I get started?',
        'What are the key features?'
    ],
    promptRequest: (args: PromptRequestEventArgs) => {
        // Handle prompt request - integrate with AI service here
        setTimeout(() => {
            const response = 'This is the AI response to: ' + args.prompt;
            aiAssistView.addPromptResponse(response);
        }, 1000);
    }
});

// Render to DOM
aiAssistView.appendTo('#aiAssistView');
```

### HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <title>AI AssistView</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    
    <!-- Syncfusion CSS -->
    <link href="https://cdn.syncfusion.com/ej2/32.1.19/tailwind3.css" rel="stylesheet" />
</head>
<body>
    <div id='container' style="height: 400px; width: 700px;">
        <div id="aiAssistView"></div>
    </div>
</body>
</html>
```

### CSS Imports

```css
@import '../node_modules/@syncfusion/ej2-base/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-inputs/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-buttons/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-navigations/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-notifications/styles/tailwind3.css';
@import '../node_modules/@syncfusion/ej2-interactive-chat/styles/tailwind3.css';
```

---

## Common Patterns

### Pattern 1: OpenAI Integration

```typescript
const aiAssistView: AIAssistView = new AIAssistView({
    promptSuggestions: ['Explain AI', 'Code example', 'Best practices'],
    promptRequest: async (args: PromptRequestEventArgs) => {
        try {
            const response = await fetch('https://api.openai.com/v1/chat/completions', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${OPENAI_API_KEY}`
                },
                body: JSON.stringify({
                    model: 'gpt-4',
                    messages: [{ role: 'user', content: args.prompt }]
                })
            });
            
            const data = await response.json();
            const aiResponse = data.choices[0].message.content;
            aiAssistView.addPromptResponse(aiResponse);
        } catch (error) {
            aiAssistView.addPromptResponse('Error: ' + error.message);
        }
    }
});
```

### Pattern 2: Markdown Responses with Streaming

```typescript
const aiAssistView: AIAssistView = new AIAssistView({
    enableStreaming: true,
    promptRequest: (args: PromptRequestEventArgs) => {
        // Simulate streaming response
        const markdownResponse = `# Response\n\nThis is **bold** and *italic* text.\n\n- Item 1\n- Item 2\n\`\`\`javascript\nconst x = 10;\n\`\`\``;
        
        let index = 0;
        const interval = setInterval(() => {
            if (index < markdownResponse.length) {
                const chunk = markdownResponse.slice(0, index + 5);
                aiAssistView.addPromptResponse(chunk, false);
                index += 5;
            } else {
                clearInterval(interval);
                aiAssistView.addPromptResponse(markdownResponse, true);
            }
        }, 50);
    }
});
```

### Pattern 3: Custom Toolbar with Actions

```typescript
const aiAssistView: AIAssistView = new AIAssistView({
    responseToolbarSettings: {
        items: [
            { type: 'Button', iconCss: 'e-icons e-copy', tooltip: 'Copy' },
            { type: 'Button', iconCss: 'e-icons e-assist-like', tooltip: 'Like' },
            { type: 'Button', iconCss: 'e-icons e-assist-dislike', tooltip: 'Dislike' }
        ],
        itemClicked: (args: ToolbarItemClickedEventArgs) => {
            if (args.item.iconCss.includes('copy')) {
                // Copy response to clipboard
                const responseText = aiAssistView.prompts[args.dataIndex].response;
                navigator.clipboard.writeText(responseText);
            } else if (args.item.iconCss.includes('like')) {
                console.log('User liked the response');
            }
        }
    }
});
```

### Pattern 4: File Attachments

```typescript
const aiAssistView: AIAssistView = new AIAssistView({
    enableAttachments: true,
    attachmentSettings: {
        allowedFileTypes: '.pdf,.docx,.txt,.jpg,.png',
        maxFileSize: 5242880, // 5MB
        maximumCount: 3,
        saveUrl: 'https://your-api.com/upload',
        removeUrl: 'https://your-api.com/remove'
    },
    promptRequest: (args: PromptRequestEventArgs) => {
        console.log('Attached files:', args.attachedFiles);
        // Process prompt with attached files
        aiAssistView.addPromptResponse('Received your prompt with attachments');
    }
});
```

---

## Key Properties Quick Reference

| Property | Type | Description |
|----------|------|-------------|
| `prompts` | `PromptModel[]` | Collection of prompt-response pairs |
| `promptSuggestions` | `string[]` | Array of suggested prompts |
| `promptRequest` | `Event` | Event triggered when user submits a prompt |
| `enableStreaming` | `boolean` | Enable response streaming |
| `enableAttachments` | `boolean` | Enable file attachment functionality |
| `views` | `AssistViewModel[]` | Custom view configurations |
| `toolbarSettings` | `ToolbarSettingsModel` | Header toolbar configuration |
| `footerToolbarSettings` | `FooterToolbarSettingsModel` | Footer toolbar configuration |
| `responseToolbarSettings` | `ResponseToolbarSettingsModel` | Response toolbar configuration |
| `promptToolbarSettings` | `PromptToolbarSettingsModel` | Prompt toolbar configuration |
| `bannerTemplate` | `string \| Function` | Custom banner template |
| `promptItemTemplate` | `string \| Function` | Custom prompt item template |
| `responseItemTemplate` | `string \| Function` | Custom response item template |
| `speechToTextSettings` | `SpeechToTextSettingsModel` | Speech-to-text configuration |
