---
name: syncfusion-aspnetcore-inline-ai-assist
description: Implement Syncfusion ASP.NET Core Inline AI Assist control for real-time text processing and AI-powered features. Use this skill when users need intelligent prompt suggestions, AI-assisted content generation, command popups, response actions, or positioning AI assist popups in ASP.NET Core applications.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core Inline AI Assist Control

## Overview

The Inline AI Assist is a Syncfusion ASP.NET Core control that provides intelligent text processing capabilities with:
- **Real-time prompt processing** connected to AI services (OpenAI, Azure Cognitive Services)
- **Multiple response modes**: Inline (in-place updates) or Popup (floating dialog)
- **Command popups** with built-in and custom command items
- **Response action items** for user feedback and content acceptance
- **Event lifecycle**: created, promptRequest, open, close
- **Public methods**: addResponse, executePrompt, showPopup, hidePopup, showCommandPopup, hideCommandPopup
- **Template support**: Custom editor templates and response templates
- **Globalization**: Localization (L10n) and RTL support

## Documentation Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Prerequisites and system requirements
- ASP.NET Core project setup with Razor pages
- NuGet package installation (Syncfusion.EJ2.AspNet.Core)
- Tag helper configuration in _ViewImports.cshtml
- Script and stylesheet resources setup
- Basic control rendering and first run

### Positioning and Response Modes
📄 **Read:** [references/positioning-and-modes.md](references/positioning-and-modes.md)
- Configure relateTo property (position relative to elements)
- Configure target property (where control appends)
- ResponseMode property: Inline vs Popup modes
- Dynamic mode switching
- Complete positioning examples with use cases

### Command Configuration
📄 **Read:** [references/command-configuration.md](references/command-configuration.md)
- CommandSettings and command items
- Command properties (id, label, prompt, iconCss, disabled, groupBy, tooltip)
- PopupWidth and PopupHeight configuration
- Command grouping and organization
- ItemSelect event handling
- Advanced command scenarios

### Events and Handlers
📄 **Read:** [references/events-and-handlers.md](references/events-and-handlers.md)
- created event (control rendering completion)
- promptRequest event (with async handling)
- open event (popup opened)
- close event (popup closed)
- Event flow and lifecycle
- Best practices for event handlers

### Public Methods and APIs
📄 **Read:** [references/methods-and-apis.md](references/methods-and-apis.md)
- addResponse() - Add response programmatically
- executePrompt() - Execute prompt dynamically
- showPopup() - Open popup with optional positioning
- hidePopup() - Close popup
- showCommandPopup() - Show command menu
- hideCommandPopup() - Hide command menu

### Inline Assist Features
📄 **Read:** [references/inline-assist-features.md](references/inline-assist-features.md)
- Prompt property configuration
- Prompts collection (history management)
- Placeholder text customization
- Z-index property
- Popup width and height configuration
- CssClass for custom styling
- Managing prompt-response collections

### Response Settings and Templates
📄 **Read:** [references/response-settings-templates.md](references/response-settings-templates.md)
- ResponseSettings configuration
- Built-in response items (accept/reject)
- Custom response items and grouping
- EditorTemplate for footer customization
- ResponseTemplate for response items
- Template syntax and context variables
- ItemSelect event handling

### Advanced Features
📄 **Read:** [references/advanced-features.md](references/advanced-features.md)
- Public methods (addResponse, executePrompt, showPopup, hidePopup, showCommandPopup, hideCommandPopup)
- Inline toolbar settings and positioning
- Toolbar items (type, text, iconCss, alignment, tooltip)
- TabIndex for keyboard navigation
- Globalization: L10n and localization
- RTL (enableRtl property)
- Accessibility features

## Quick Start Example

```razor
@using Syncfusion.EJ2.InteractiveChat;

<style>
    #editableText {
        width: 100%;
        min-height: 120px;
        max-height: 300px;
        overflow-y: auto;
        font-size: 16px;
        padding: 12px;
        border-radius: 4px;
        border: 1px solid;
    }
</style>

<div class="container" style="height: 350px; width: 650px;">
    <button id="summarizeBtn" class="e-btn e-primary" onclick="onSummarizeClick()">Summarize</button>
    <div id="editableText" contenteditable="true">
        <p>Add your content here for AI processing...</p>
    </div>
    
    <ejs-inlineaiassist id="defaultInlineAssist" 
        relateTo="#summarizeBtn" 
        created="onCreated" 
        promptRequest="onPromptRequest">
        <e-inlineaiassist-responsesettings itemSelect="onItemSelect"></e-inlineaiassist-responsesettings>
    </ejs-inlineaiassist>
</div>

<script>
    var inlineAssist;
    
    function onCreated() {
        inlineAssist = this;
    }
    
    function onPromptRequest(args) {
        setTimeout(function () {
            var response = 'Connect to your AI service for real processing...';
            inlineAssist.addResponse(response);
        }, 1000);
    }
    
    function onItemSelect(args) {
        if (args.command.label === 'Accept') {
            document.getElementById('editableText').innerHTML = 
                '<p>' + inlineAssist.prompts[inlineAssist.prompts.length - 1].response + '</p>';
            inlineAssist.hidePopup();
        }
    }
    
    function onSummarizeClick() {
        if (inlineAssist) {
            inlineAssist.showPopup();
        }
    }
</script>
```

## Common Patterns

### 1. Setup Inline vs Popup Modes
```razor
<!-- Popup mode (default) -->
<ejs-inlineaiassist id="assist1" responseMode="Popup" relateTo="#btn"></ejs-inlineaiassist>

<!-- Inline mode (updates content in-place) -->
<ejs-inlineaiassist id="assist2" responseMode="Inline" relateTo="#btn"></ejs-inlineaiassist>
```

### 2. Add Command Popups
```razor
<ejs-inlineaiassist id="assist3" relateTo="#btn">
    <e-inlineaiassist-commandsettings 
        commands="commandsData" 
        popupWidth="250px" 
        popupHeight="200px"
        itemSelect="onCommandSelect">
    </e-inlineaiassist-commandsettings>
</ejs-inlineaiassist>
```

### 3. Handle Events
```razor
<ejs-inlineaiassist id="assist4" 
    created="onCreated"
    promptRequest="onPromptRequest" 
    open="onOpen" 
    close="onClose">
</ejs-inlineaiassist>
```

### 4. Use Public Methods
```javascript
// Show popup at current position
inlineAssist.showPopup();

// Execute prompt dynamically
inlineAssist.executePrompt('Your prompt text');

// Add response programmatically
inlineAssist.addResponse('Response text');

// Hide popup
inlineAssist.hidePopup();
```

## Key Props

| Property | Purpose | Example |
|----------|---------|---------|
| `relateTo` | Position control relative to DOM element | `relateTo="#btn"` or `relateTo=".container"` |
| `target` | Specify where control appends in DOM | `target="#container"` |
| `responseMode` | Display mode for responses | `responseMode="Popup"` or `"Inline"` |
| `prompt` | Default prompt text | `prompt="What are benefits?"` |
| `popupWidth` | Control width | `popupWidth="400px"` |
| `popupHeight` | Control height | `popupHeight="auto"` |
| `placeholder` | Textarea placeholder text | `placeholder="Type prompt here..."` |
| `zIndex` | Stacking context | `zIndex="4000"` |
| `enableRtl` | Right-to-left layout | `enableRtl="true"` |
| `locale` | Localization language | `locale="de"` |
| `cssClass` | Custom CSS class | `cssClass="custom-class"` |

## Common Use Cases

1. **Content Summarization Tool**
   - Place button near text editor
   - Use Popup mode for full interface
   - Add Accept/Reject response items
   - Connect promptRequest to summarization API

2. **Inline Text Suggestions**
   - Use Inline mode for in-place updates
   - Minimal UI footprint
   - Quick acceptance workflow
   - Stream responses for real-time feedback

3. **Multi-Command Workflow**
   - Show command popup for quick actions
   - Group commands by category (Improve, Edit)
   - Handle each command's promptRequest differently
   - Dynamic response handling per command

4. **Accessibility-Focused Implementation**
   - Enable RTL for Arabic/Hebrew content
   - Use localization for multiple languages
   - Configure tab navigation with tabIndex
   - Use semantic templates

---
