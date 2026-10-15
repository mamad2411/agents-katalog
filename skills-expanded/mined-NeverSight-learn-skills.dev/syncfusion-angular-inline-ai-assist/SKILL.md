---
name: syncfusion-angular-inline-ai-assist
description: Implement the Syncfusion Angular Inline AI Assist component for AI-powered text processing and editing. Use this skill when user needs to add AI-powered suggestions, create prompt/response workflows, customize toolbars and commands, handle AI responses, configure templates, implement event handling, or add localization to Angular applications with intelligent inline text editing capabilities. Covers installation, configuration, response modes, command settings, toolbar customization, template usage, event handling, methods, and RTL/localization support.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Angular Inline AI Assist Component

## Component Overview

The **Inline AI Assist** component provides intelligent text processing capabilities that enhance user productivity. It leverages advanced natural language processing to enable AI-powered text suggestions, content generation, and editing features directly within Angular applications.

**Key Capabilities:**
- **Response Modes** - Popup (floating) or Inline (in-place) response display with configurable dimensions
- **Command System** - Predefined AI operations with icons, grouping, and custom command items
- **Response Actions** - Custom response toolbar items for accept/reject workflows
- **Template System** - Flexible editor and response templates for custom layouts
- **Events & Interactions** - Comprehensive events for lifecycle (created, open, close) and user interactions
- **Toolbar Configuration** - Inline toolbar with custom items, positioning, and alignment
- **Methods** - Programmatically add prompts, update responses, open/close popups, and control behavior
- **Globalization** - Multi-language support with RTL capabilities and locale-based formatting
- **Customizable UI** - CSS classes, z-index control, popup dimensions, and theme integration

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation and package setup
- Angular environment configuration
- Basic component implementation
- CSS imports and theme setup
- Initial configuration with relateTo and target properties

### Core Configuration
📄 **Read:** [references/core-configuration.md](references/core-configuration.md)
- Prompt text and placeholder configuration
- Prompt/response collection management
- Response display modes (Popup vs Inline)
- Popup dimensions (width, height, z-index)
- CSS customization and styling

### Commands and Responses
📄 **Read:** [references/commands-and-responses.md](references/commands-and-responses.md)
- Command settings and command items
- Adding preset AI operations with grouping
- Response settings and response items
- Built-in accept/reject actions
- Custom response toolbar items and event handling

### Templates and Toolbars
📄 **Read:** [references/templates-and-toolbars.md](references/templates-and-toolbars.md)
- Editor template customization
- Response template layout
- Inline toolbar configuration and items
- Toolbar positioning, alignment, and styling
- Tab key navigation in toolbars

### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Lifecycle events (created, open, close)
- Prompt request event handling
- Component methods (addResponse, executePrompt, showPopup, hidePopup)
- Event arguments and callback patterns

### Localization and Styling
📄 **Read:** [references/localization-and-styling.md](references/localization-and-styling.md)
- Localization and multi-language support
- Right-to-left (RTL) text direction
- Custom CSS class styling
- Theme integration
- Text content customization

## Quick Start Example

```typescript
import { Component, ViewChild } from '@angular/core';
import { InlineAIAssistModule, InlineAIAssistComponent, InlinePromptRequestEventArgs, ResponseSettingsModel, ResponseItemSelectEventArgs } from '@syncfusion/ej2-angular-interactive-chat';

@Component({
    imports: [InlineAIAssistModule],
    standalone: true,
    selector: 'app-root',
    template: `
        <div id="container" style="height: 350px; width: 650px;">
            <button id="summarizeBtn" class="e-btn e-primary" (click)="onClick()">Content Summarize</button>
            <div id="editableText" contenteditable="true">
                <p>Inline AI Assist component provides intelligent text processing capabilities that enhance user productivity.</p>
            </div>
            <ejs-inlineaiassist id="inlineAssist" #inlineAssistComponent
                [relateTo]="'#summarizeBtn'"
                [responseSettings]="responseSetting"
                popupWidth="500px"
                (promptRequest)="onPromptRequest($event)">
            </ejs-inlineaiassist>
        </div>
    `,
    styles: [`#editableText { width: 100%; min-height: 120px; padding: 12px; border: 1px solid; }`]
})
export class AppComponent {
    @ViewChild('inlineAssistComponent')
    public inlineAssistComponent!: InlineAIAssistComponent;

    public itemSelect = (args: ResponseItemSelectEventArgs) => {
        if (args.command.label === 'Accept') {
            const editable = document.getElementById('editableText') as HTMLElement;
            if (editable && this.inlineAssistComponent.prompts.length > 0) {
                const lastResponse = this.inlineAssistComponent.prompts[this.inlineAssistComponent.prompts.length - 1].response;
                editable.innerHTML = '<p>' + lastResponse + '</p>';
            }
            this.inlineAssistComponent.hidePopup();
        }
    }

    public responseSetting: ResponseSettingsModel = {
        itemSelect: this.itemSelect
    }

    onClick(): void {
        this.inlineAssistComponent.showPopup();
    }

    public onPromptRequest = (args: InlinePromptRequestEventArgs) => {
        setTimeout(() => {
            let response = 'Connect this component to OpenAI or Azure AI services for real-time prompt processing.';
            this.inlineAssistComponent.addResponse(response);
        }, 1000);
    };
}
```

## Common Patterns

### Pattern 1: Response Handling with Item Selection
```typescript
// Handle accept/reject responses
public itemSelect = (args: ResponseItemSelectEventArgs) => {
    if (args.command.label === 'Accept') {
        // Apply the AI response to your content
        const content = this.inlineAssistComponent.prompts[this.inlineAssistComponent.prompts.length - 1].response;
        this.applyResponse(content);
        this.inlineAssistComponent.hidePopup();
    } else if (args.command.label === 'Discard') {
        this.inlineAssistComponent.hidePopup();
    }
}
```

### Pattern 2: Executing Predefined Prompts
```typescript
// Execute a specific prompt with custom command
public executeCommand(prompt: string) => {
    this.inlineAssistComponent.showPopup();
    this.inlineAssistComponent.executePrompt(prompt);
}

// Example usage: Summarize, Translate, or Make Professional
this.executeCommand('Summarize the content');
```

### Pattern 3: Command Groups for Organization
```typescript
// Organize commands into logical groups
public commandSetting: CommandSettingsModel = {
    commands: [
        { label: 'Summarize', prompt: 'Summarize...', groupBy: 'Improve content' },
        { label: 'Shorten', prompt: 'Shorten...', groupBy: 'Improve content' },
        { label: 'Translate', prompt: 'Translate...', groupBy: 'Edit content' },
    ]
}
```

### Pattern 4: Inline vs Popup Modes
```typescript
// Toggle between response display modes
public responseMode: string = 'Popup'; // or 'Inline'

// Use Inline for seamless in-place editing
// Use Popup for review-based workflows
```

## Key Properties and Configuration

| Property | Purpose | Example |
|----------|---------|---------|
| `relateTo` | Position relative to DOM element | `[relateTo]="'#button'"` |
| `target` | Append location in DOM | `[target]="'#container'"` |
| `responseMode` | Display mode (Popup/Inline) | `[responseMode]="'Popup'"` |
| `popupWidth` / `popupHeight` | Popup dimensions | `popupWidth="500px"` |
| `placeholder` | Prompt textarea placeholder | `[placeholder]="'Ask AI...'"` |
| `cssClass` | Custom CSS styling | `[cssClass]="'custom'"` |
| `enableStreaming` | Real-time streaming responses | `[enableStreaming]="true"` |
| `enablePersistence` | Preserve state across reloads | `[enablePersistence]="true"` |
| `commandSettings` | Predefined AI commands | `[commandSettings]="cmdSettings"` |
| `responseSettings` | Response action items | `[responseSettings]="respSettings"` |
| `inlineToolbarSettings` | Inline toolbar items | `[inlineToolbarSettings]="toolbar"` |
| `editorTemplate` | Custom prompt input template | `[editorTemplate]="template"` |
| `responseTemplate` | Custom response display template | `[responseTemplate]="template"` |
| `locale` | Language/localization | `[locale]="'de'"` |
| `enableRtl` | Right-to-left text direction | `[enableRtl]="true"` |

## Common Use Cases

1. **Text Summarization**: Create a button that triggers content summarization via AI
2. **Grammar & Style**: Help users improve writing with grammar and style suggestions
3. **Content Translation**: Add quick translation options for multiple languages
4. **Code Generation**: Assist users in generating code snippets based on descriptions
5. **Email Composition**: Enhance email writing with AI suggestions and rephrasing
6. **Document Enhancement**: Improve document quality with AI-powered editing
7. **Accessibility Support**: Provide AI assistance for users with accessibility needs
8. **Multilingual Support**: Enable global applications with localized AI assistance
