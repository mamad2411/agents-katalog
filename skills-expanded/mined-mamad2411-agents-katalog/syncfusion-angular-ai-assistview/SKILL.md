---
name: syncfusion-angular-ai-assistview
description: Implement the Syncfusion Angular AI AssistView component. Use this skill when you need to create conversational AI interfaces, integrate AI services, add chat-like UI, or create intelligent assistant applications. Includes setup, configuration, event handling, AI integrations (OpenAI, Gemini, Ollama), speech features, and customization. Use this skill for all AI AssistView component implementation needs.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Angular AI AssistView Component

## Component Overview

The **Syncfusion AI AssistView** is a powerful Angular component that provides a ready-to-use interface for building conversational AI applications.

**Key Capabilities:**
- **Conversation Management** - Manage prompt-response pairs with history, persistence, and markdown rendering
- **AI Service Integration** - Connect to OpenAI, Gemini, Ollama, Lite-LLM, and MCP providers with streaming support
- **Speech Features** - Built-in speech-to-text with 11 configurable properties and 4 events
- **Toolbar System** - Four toolbar types (header, prompt, response, footer) with custom actions and tag directives
- **View Management** - Multiple views with programmatic `activeView` control and dynamic switching
- **Events & Interactions** - Typed event arguments (PromptRequestEventArgs, PromptChangedEventArgs, StopRespondingEventArgs)
- **File Attachments** - Support for file uploads with type/size restrictions and attachment click events
- **Templates** - Customize prompts, responses, suggestions, and banners with flexible templates
- **Methods** - Programmatically add/update responses, execute prompts, and control component behavior
- **Globalization** - Full RTL support and localization for 12+ languages with locale-based formatting
- **Customizable UI** - Height, width, CSS classes, HTML attributes, and theme customization

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and dependency setup
- Angular environment configuration
- Basic component initialization
- CSS imports and theme configuration
- First working example

### Core Features & Conversation Management
📄 **Read:** [references/assist-view-basics.md](references/assist-view-basics.md)
- Setting prompt text and placeholders
- Managing prompt-response collections
- Markdown response rendering
- Configuring prompt suggestions
- Customizing user and assistant avatars
- UI controls (clear button, scroll-to-bottom)
- Component configuration (height, width, showHeader, cssClass, htmlAttributes)
- State persistence with `enablePersistence`
- Globalization and localization (locale property with 12+ languages)
- RTL support with `enableRtl` for Arabic, Hebrew, Persian, Urdu

### Appearance & Styling
📄 **Read:** [references/appearance-customization.md](references/appearance-customization.md)
- Setting component width and height
- Applying custom CSS classes
- Theme customization
- Responsive design patterns

### Multiple Views & Custom Content
📄 **Read:** [references/custom-views.md](references/custom-views.md)
- Adding custom view models
- View types (Assist and Custom)
- View configuration and naming
- Managing multiple views within one component
- Programmatic view switching with `activeView` property
- Dynamic view navigation patterns
- View history and breadcrumb navigation
- Workflow-based view switching
- Conditional view display based on user roles

### Programmatic Control & Methods
📄 **Read:** [references/methods-and-actions.md](references/methods-and-actions.md)
- Adding prompt responses (string and object
- Complete event arguments reference section
- PromptRequestEventArgs with 6 properties (prompt, attachedFiles, promptSuggestions, cancel, etc.)
- PromptChangedEventArgs with 5 properties (value, previousValue, element, event)
- StopRespondingEventArgs for canceling responses
- AttachmentClickEventArgs with FileInfo interface
- Production-ready examples with all event types formats)
- Executing prompts dynamically
- Response handling patterns
- Programmatic interaction

## Complete documentation for all 4 toolbar types
- Header Toolbar (`toolbarSettings`) - Global actions and navigation
- Prompt Toolbar (`promptToolbarSettings`) - Actions on user prompts
- Response Toolbar (`responseToolbarSettings`) - Actions on AI responses
- Footer Toolbar (`footerToolbarSettings`) - Input area customization
- ToolbarItemModel interface with 10 properties
- ToolbarItemClickedEventArgs with dataIndex handling
- Tag directive approach: `<e-toolbarsettings>`, `<e-toolbaritem>`
- Property binding approach for dynamic toolbar items
- Common patterns, best practices, and troubleshootingest, promptChanged)
- File upload events (beforeAttachmentUpload, attachmentUploadSuccess)
- Event handling patterns and best practices

### File Attachments
📄 **Read:** [references/file-attachments.md](references/file-attachments.md)
- File attachment configuration
- Upload handling and validation
- File size and type restrictions
- Attachment display and management

### Toolbar Configuration
📄 **Read:** [references/toolbar-items.md](references/toolbar-items.md)
- Toolbar customization
- Built-in speech-to-text with `speechToTextSettings` (recommended approach)
- SpeechToTextSettingsModel with 11 configurable properties
- ButtonSettingsModel and TooltipSettingsModel interfaces
- 4 speech events: onStart, onStop, transcriptChanged, onError
- Event arguments: StartListeningEventArgs, StopListeningEventArgs, TranscriptChangedEventArgs, ErrorEventArgs
- Language support with 10+ language codes (en-US, es-ES, fr-FR, de-DE, ja-JP, etc.)
- Interim results handling with `allowInterimResults`
- Custom Web Speech API implementation (alternative approach)
- Text-to-speech setup and configuration
- Browser compatibility and error handling
### Templates & Custom Rendering
📄 **Read:** [references/templates.md](references/templates.md)
- Template system overview
- Prompt templates
- Response templates
- Custom template creation

### AI Service Integration
📄 **Read:** [references/ai-integrations.md](references/ai-integrations.md)
- Azure OpenAI integration setup
- Gemini integration
- Lite-LLM integration
- Model Context Protocol (MCP) integration
- Ollama integration
- Security best practices and API management

### Speech Features
📄 **Read:** [references/speech-features.md](references/speech-features.md)
- Speech-to-text setup and configuration
- Text-to-speech setup and configuration
- Audio handling
- Browser compatibility considerations

---

## Quick Start Example

Here's a minimal working example to get started:

```typescript
import { Component } from '@angular/core';
import { AIAssistViewModule } from '@syncfusion/ej2-angular-interactive-chat';

@Component({
  imports: [AIAssistViewModule],
  standalone: true,
  selector: 'app-root',
  template: `
    <div ejs-aiassistview 
      id='aiAssistView'
      [promptSuggestions]="suggestions"
      (promptRequest)="onPromptRequest($event)">
    </div>
  `,
  styles: [`
    :host ::ng-deep #aiAssistView {
      height: 100vh;
    }
  `]
})
export class AppComponent {
  suggestions = [
    'What is Angular?',
    'How to create components?',
    'Explain dependency injection'
  ];

  onPromptRequest(args: any) {
    // Handle prompt and provide response
    setTimeout(() => {
      const response = 'This is a sample response from your AI service.';
      // Add response using component method
    }, 1000);
  }
}
```

---

## Common Patterns

### Pattern 1: Basic Conversation Flow
1. Initialize component with suggestions
2. User enters prompt
3. `promptRequest` event fires
4. Call your AI service
5. Use `addPromptResponse()` to display result
6. Conversation history maintained automatically

### Pattern 2: AI Service Integration with Streaming
1. Enable streaming with `[enableStreaming]="true"`
2. Configure AI provider credentials (OpenAI, Gemini, etc.)
3. In `promptRequest` event, call provider API with streaming
4. Use `ReadableStream` for chunked responses
5. Handle `stopRespondingClick` event for cancellation
6. Update UI with `addPromptResponse()` incrementally

### Pattern 3: Custom View Management with activeView
1. Define multiple view types (Assist, Custom)
2. Use `[activeView]="currentIndex"` to control display
3. Switch between views programmatically based on user action
4. Track view history for back/forward navigation
5. Each view can have different configuration
6. Maintain separate state per view

### Pattern 4: Complete Toolbar Configuration
1. Configure header toolbar for global actions (new chat, export, settings)
2. Set up prompt toolbar for user prompt actions (edit, copy, retry)
3. Add response toolbar for AI response actions (copy, regenerate, like/dislike)
4. Configure footer toolbar for input actions (formatting, attachments)
5. Use tag directive or property binding approach
6. Handle `itemClicked` events with `dataIndex` for context

### Pattern 5: Speech-Enabled Interface
1. Configure `speechToTextSettings` with language and options
2. Enable `allowInterimResults` for real-time transcription
3. Handle speech events: `onStart`, `onStop`, `transcriptChanged`, `onError`
4. Automatically submit recognized text as prompts
5. Provide visual feedback during listening state

### Pattern 6: Event-Driven Actions with Typed Arguments
1. Use `PromptRequestEventArgs` to access prompt, attachedFiles, and cancel flag
2. Use `PromptChangedEventArgs` for real-time input validation
3. Handle `StopRespondingEventArgs` to cancel long-running requests
4. Use `beforeAttachmentUpload` for file validation
5
## Common Patterns

### Pattern 1: Basic Conversation Flowstreaming responses, multi-language support, and toolbar actions
2. **Code Assistant:** Create coding helpers with syntax highlighting, code regeneration, and like/dislike feedback
3. **Voice-Enabled Assistant:** Implement hands-free interfaces with built-in speech-to-text in 10+ languages
4. **Content Writer Assistant:** Implement writing tools with grammar checking, real-time suggestions, and response streaming
5. **Data Analysis Tool:** Create interfaces with multiple views (query, results, visualization) and view switching
6. **Learning Platform:** Build educational assistants with RTL support for Arabic/Hebrew learners and persistent conversation history
7. **Multi-language Support:** Implement interfaces with locale configuration for 12+ languages and RTL text direction
8. **Accessibility Assistant:** Provide reading aid with speech features, keyboard navigation, and ARIA attributes
9. **Workflow Applications:** Build step-by-step wizards with programmatic view control and conditional navigation
10. **Real-time AI Services:** Integrate streaming AI providers with abort functionality and visual streaming indicatorser input |
| `promptSuggestions` | string[] | `[]` | Provide quick starting prompts |
| `prompts` | object[] | `[]` | Initialize conversation history |
| `showClearButton` | boolean | `false` | Show button to clear input |
| `enableScrollToBottom` | boolean | `true` | Show scroll-to-bottom indicator |

### Layout & Appearance
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `width` | string \| number | `'100%'` | Set container width |
| `height` | string \| number | `'100%'` | Set container height |
| `cssClass` | string | `''` | Apply custom CSS styling and themes |
| `showHeader` | boolean | `true` | Control header visibility |
| `htmlAttributes` | object | `{}` | Add custom HTML attributes (aria-*, data-*, etc.) |

### Streaming & Features
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `enableStreaming` | boolean | `false` | Enable real-time streaming responses |
| `speechToTextSettings` | SpeechToTextSettingsModel | `null` | Configure built-in speech recognition |
| `activeView` | number | `0` | Programmatically switch between views |

### Globalization
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `locale` | string | `'en-US'` | Set language/culture (en-US, es-ES, fr-FR, de-DE, ja-JP, ar-SA, etc.) |
| `enableRtl` | boolean | `false` | Enable right-to-left text direction (Arabic, Hebrew, Persian, Urdu) |
| `enablePersistence` | boolean | `false` | Save component state between page reloads |

### Toolbar Configuration
| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `toolbarSettings` | ToolbarSettingsModel | `null` | Configure header toolbar (global actions) |
| `promptToolbarSettings` | PromptToolbarSettingsModel | `null` | Configure prompt toolbar (edit, copy, retry) |
| `responseToolbarSettings` | ResponseToolbarSettingsModel | `null` | Configure response toolbar (copy, regenerate, like/dislike) |
| `footerToolbarSettings` | FooterToolbarSettingsModel | `null` | Configure footer toolbar (formatting, attachments)

### Pattern 3: Custom View Management
1. Define multiple view types (Assist, Custom)
2. Switch between views based on user action
3. Each view can have different configuration
4. Maintain separate state per view

### Pattern 4: Event-Driven Actions
1. Listen to `promptChanged` for input validation
2. Handle `beforeAttachmentUpload` for file validation
3. Use `attachmentUploadSuccess` for post-upload actions
4. Leverage `created` event for initialization

---

## Key Properties

| Property | Type | Default | When to Use |
|----------|------|---------|------------|
| `prompt` | string | `''` | Pre-fill prompt text |
| `promptPlaceholder` | string | `'Type prompt for assistance...'` | Guide user input |
| `promptSuggestions` | string[] | `[]` | Provide quick starting prompts |
| `prompts` | object[] | `[]` | Initialize conversation history |
| `width` | string | `'100%'` | Set container width |
| `height` | string | `'100%'` | Set container height |
| `cssClass` | string | `''` | Apply custom CSS styling |
| `showClearButton` | boolean | `false` | Show button to clear input |
| `enableScrollToBottom` | boolean | `true` | Show scroll-to-bottom indicator |

---

## Common Use Cases

1. **Customer Support Chatbot:** Build customer service interfaces with knowledge base integration
2. **Code Assistant:** Create coding helpers with AI that can review and suggest code
3. **Content Writer Assistant:** Implement writing tools with grammar and style suggestions
4. **Data Analysis Tool:** Create interfaces for users to query and analyze data through natural language
5. **Learning Platform:** Build educational assistants that answer student questions
6. **Internal Knowledge Bot:** Create enterprise assistants for company documentation and FAQs
7. **Multi-language Support:** Implement translation and localization features
8. **Accessibility Assistant:** Provide reading aid or instruction assistance

---
