---
name: syncfusion-react-ai-assistview
description: Implement the Syncfusion React AI AssistView component. Use this skill to handle AI-powered conversational interfaces, AssistView setup, conversation flow, speech input or output, file attachments, UI customization, state management, chain of thoughts reasoning visualization, generative UI with dynamic tools, and AI service integration such as OpenAI or Azure AI in React applications.
metadata:
  author: "Syncfusion Inc"
  version: "34.1.29"
---

# Syncfusion React AI AssistView Component

## Component Overview

The **Syncfusion React AI AssistView** component is a comprehensive interactive chat component designed for building AI-powered conversational interfaces. It provides:

### Core Capabilities
- **Prompt-Response Management**: Manage conversation history with automatic data collection
- **Real-time Streaming**: Stream AI responses character-by-character for live typing effects
- **Chain of Thoughts**: Visualize AI reasoning process through thinking blocks with multi-stage workflow support
- **Template System**: Customize every UI element (banners, prompt items, responses, suggestions, footer)
- **Multi-View Support**: Switch between conversation assist view and custom content views
- **Voice Integration**: Built-in Speech-to-Text (voice input) and Text-to-Speech (voice output)
- **File Attachments**: Upload and include files with prompts
- **Advanced Toolbars**: Configurable toolbars for header, footer, responses, and prompts
- **AI Service Integration**: Direct integration with OpenAI, Azure OpenAI, and other AI services
- **Event-Driven Architecture**: Hooks for prompt submission, changes, and component lifecycle

### Key Features
- **Markdown Support**: Render AI responses as formatted HTML via markdown parsing
- **Conversation History**: Automatic tracking of all prompts and responses
- **Suggestion System**: Display helpful prompt suggestions to guide users
- **Avatar Customization**: Customize user and AI icons/avatars
- **Scroll Management**: Auto-scroll or manual scroll-to-bottom button
- **Clear Functionality**: Clear current prompt or entire conversation
- **Regenerate Responses**: Request alternative AI responses for existing prompts without resubmitting queries
- **Responsive Design**: Works on desktop and mobile with responsive layouts

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Install @syncfusion/ej2-react-interactive-chat package
- Add CSS theme imports
- Create basic component initialization
- Render component to DOM
- First working functional component example

### Configuration Essentials
📄 **Read:** [references/configuration-essentials.md](references/configuration-essentials.md)
- Set initial prompt text and placeholders
- Configure prompt suggestions and suggestion headers
- Customize user and AI avatar icons
- Control clear button visibility
- Enable/disable scroll-to-bottom functionality
- Manage component instance via refs
- **Set component dimensions (height and width)**
- **Apply custom CSS classes for styling**
- **Control header visibility**
- **Configure globalization (locale, RTL support)**
- **Enable state persistence across sessions**

### Conversation Management
📄 **Read:** [references/conversation-management.md](references/conversation-management.md)
- Initialize with pre-configured conversation data
- Add responses (string or object format)
- Access and manage conversation history
- Work with PromptModel data structure
- Render markdown in responses
- Persist and restore conversations

### Events and Interactions
📄 **Read:** [references/events-and-interactions.md](references/events-and-interactions.md)
- Handle component lifecycle (created event)
- Respond to prompt submissions (promptRequest event)
- Track prompt text changes (promptChanged event)
- **Access detailed event arguments (PromptChangedEventArgs, PromptRequestEventArgs)**
- **Cancel prompt submissions programmatically**
- **Handle stop responding events for long operations**
- **Modify suggestions and toolbar items dynamically**
- Implement event-driven workflows
- Integrate with AI services via event handlers

### Toolbar Customization
📄 **Read:** [references/toolbar-customization.md](references/toolbar-customization.md)
- Configure four toolbar types (header, footer, response, prompt)
- Add custom toolbar items
- Control toolbar positioning (Inline vs Bottom)
- Customize toolbar icons
- Handle item click events
- **Configure all ToolbarItemModel properties (align, cssClass, disabled, tabIndex, template, type, visible)**
- **Create custom toolbar item templates**
- **Control item visibility and enabled state dynamically**
- **Set tab order for keyboard navigation**
- Manage attachment button behavior
- **Enable regenerate responses functionality for multiple AI-generated responses**
- **Navigate between regenerated responses with previous/next buttons**

### File Attachments
📄 **Read:** [references/file-attachments.md](references/file-attachments.md)
- Enable file attachment support
- Configure upload endpoints (saveUrl, removeUrl)
- Restrict file types (allowedFileType)
- Set file size limits (maxFileSize)
- Limit number of attachments (maximumCount)
- **Access attached files via attachedFiles array (FileInfo interface)**
- **Handle attachment lifecycle events (beforeAttachmentUpload, attachmentUploadSuccess, attachmentUploadFailure, attachmentRemoved)**
- **Validate files before upload**
- **Initialize prompts with pre-attached files**
- Handle server-side file processing
- Custom attachment templates (attachmentTemplate)

### Custom Views
📄 **Read:** [references/custom-views.md](references/custom-views.md)
- Create multiple views (Assist and Custom types)
- Set view names and icons
- Define view-specific templates
- **Configure activeView property to set initial view**
- **Switch between views programmatically**
- **Persist active view across sessions**
- **Conditionally set initial view based on user role or state**
- Display side-by-side content panels
- Use cases for multi-view layouts

### Templating System
📄 **Read:** [references/templating-system.md](references/templating-system.md)
- Customize banner templates (welcome content)
- Create prompt item templates (user message display)
- Design response item templates (AI response display)
- Build suggestion item templates
- Create custom footer templates
- Access template context data

### AI Service Integration
📄 **Read:** [references/ai-integration-setup.md](references/ai-integration-setup.md)
- Integrate with Azure OpenAI, OpenAI, Gemini, Claude
- Configure API credentials and authentication
- Handle real-time prompt processing
- Stream responses for live typing effects
- Parse markdown responses with marked library
- Error handling and rate limiting
- Security considerations for API keys

### Generative UI
📄 **Read:** [references/generative-ui.md](references/generative-ui.md)
- **Register custom tools with registerToolUI() method**
- **Configure tool templates and handlers for rendering**
- **Add interactive elements (charts, cards, custom tools) via blocks property**
- **Render multiple tools within single AI response**
- **Configure AI system prompts for structured JSON generation**
- **AI service integration with generative UI blocks**

### Speech Capabilities
📄 **Read:** [references/speech-capabilities.md](references/speech-capabilities.md)
- Enable Speech-to-Text (voice input)
- Configure speech recognition language
- Handle interim transcripts while speaking
- Implement Text-to-Speech (voice output) via Web Speech API
- **Convert AI responses to spoken audio**
- **Customize TTS with textToSpeechSettings (language, speechPitch, speechRate, volume, voice)**
- Customize button labels and icons
- Handle speech events (start, stop, transcript, error)
- Browser compatibility notes

### Chain of Thoughts
📄 **Read:** [references/chain-of-thoughts.md](references/chain-of-thoughts.md)
- **Visualize AI reasoning process with thinking blocks**
- **Configure thinking blocks with stages and status updates**
- **Add multi-stage reasoning workflows (completed, inprogress, failed)**
- **Customize thinking block templates**
- **Add inline context items with badges and tooltips**
- **Handle editableContextClicked events for interactive context**
- **Configure stage-level item templates**
- Stream thinking blocks for real-time reasoning visualization

### Methods and APIs
📄 **Read:** [references/methods-and-apis.md](references/methods-and-apis.md)
- Use addPromptResponse() method
- Execute prompts dynamically with executePrompt()
- Scroll to bottom programmatically
- Access component instance via refs
- Manage component state
- Common patterns and gotchas

---

## Quick Start Example

```tsx
import { AIAssistViewComponent, PromptRequestEventArgs } from '@syncfusion/ej2-react-interactive-chat';
import * as React from 'react';
import * as ReactDOM from "react-dom";

function App() {
    const assistInstance = React.useRef<AIAssistViewComponent>(null);
    
    const onPromptRequest = (args: PromptRequestEventArgs) => {
        setTimeout(() => {
            let defaultResponse = 'For real-time AI processing, connect to your preferred service (OpenAI, Azure OpenAI, etc.).';
            assistInstance.current.addPromptResponse(defaultResponse);
        }, 1000);
    };
  
    return (
        <AIAssistViewComponent 
            id="aiAssistView" 
            ref={assistInstance} 
            promptRequest={onPromptRequest}
            prompt={'Welcome! How can I help?'}
            promptSuggestions={['Ask about features', 'Get started guide']}
        />
    );
}

ReactDOM.render(<App />, document.getElementById('container'));
```

---

## Common Patterns

### Pattern 1: Basic Chat with Suggestions
Create a simple conversational interface with predefined suggestions:
- Enable prompt suggestions to guide user interactions
- Handle promptRequest event with simple responses
- Display conversation history automatically

### Pattern 2: AI Service Integration
Connect to real AI services for intelligent responses:
- Use promptRequest event to capture user input
- Call AI API with prompt text
- Stream response character-by-character for live effect
- Parse markdown responses for formatted output

### Pattern 3: Multi-View Dashboard
Combine chat with supporting content:
- Create Assist view for conversation
- Add Custom view for settings/sidebar
- Switch activeView based on user interaction
- Share data between views

### Pattern 4: Voice-Enabled Chat
Enable hands-free interaction with speech:
- Enable speechToTextSettings to capture voice
- Configure Text-to-Speech for response audio
- Use toolbar for voice control buttons
- Handle speech events for status feedback

### Pattern 5: File-Attached Prompts
Support file uploads with prompts:
- Enable attachments with enableAttachments property
- Configure attachment endpoints and file restrictions
- Include file data in prompt context
- Send files to backend API

### Pattern 6: Chain of Thoughts Reasoning
Visualize AI's step-by-step reasoning process:
- Inject AssistThinking module for thinking block support
- Create thinking blocks with multiple reasoning stages
- Use status updates (completed, inprogress, failed) for real-time progress
- Stream thinking blocks alongside text responses
- Add context items to highlight referenced tools or files
- Customize block and stage templates for branded styling

---

## Key Props & Configuration

### Essential Props
- `promptRequest`: Event handler when user submits prompt
- `prompt`: Initial/default text in prompt input
- `promptPlaceholder`: Placeholder text for input area
- `promptSuggestions`: Array of suggested prompts
- `prompts`: Pre-configured conversation data

### Customization Props
- `promptIconCss`: CSS class for user avatar
- `responseIconCss`: CSS class for AI avatar
- `showClearButton`: Show/hide clear button (default: false)
- `showHeader`: Show/hide component header (default: true)
- `enableScrollToBottom`: Show scroll-to-bottom button (default: true)
- `height`: Component height (string | number, default: '100%')
- `width`: Component width (string | number, default: '100%')
- `cssClass`: Custom CSS classes for styling
- `activeView`: Currently displayed view index (number, default: 0)

### Template Props
- `bannerTemplate`: Welcome banner content
- `promptItemTemplate`: User message display
- `responseItemTemplate`: AI response display
- `promptSuggestionItemTemplate`: Suggestion styling
- `footerTemplate`: Custom prompt input area

### Advanced Props
- `enableAttachments`: Enable file uploads (default: false)
- `attachmentSettings`: File upload configuration
- `speechToTextSettings`: Voice input configuration
- `textToSpeechSettings`: Text-to-speech configuration
- `toolbarSettings`: Header toolbar configuration
- `footerToolbarSettings`: Footer toolbar configuration
- `responseToolbarSettings`: Response action toolbar
- `promptToolbarSettings`: Prompt toolbar configuration
- `blockTemplate`: Custom template for thinking blocks and other response blocks
- `itemTemplate`: Custom template for individual stages within thinking blocks
- `locale`: Localization/globalization setting (default: 'en-US')
- `enableRtl`: Enable right-to-left rendering (default: false)
- `enablePersistence`: Enable state persistence (default: false)

### Generative UI Props
- **`blocks`**: Array of response blocks (TextBlock, ToolBlock, ThinkingBlock) to render dynamic UI elements within responses
- **`registerToolUI()`**: Public method to register custom tool templates for rendering interactive components (charts, cards, custom tools) within AI responses

### Event Props
- `created`: Component lifecycle event
- `promptRequest`: Prompt submission event
- `promptChanged`: Prompt text change event
- `stopRespondingClick`: Stop button click event
- `beforeAttachmentUpload`: Before file upload event
- `attachmentUploadSuccess`: File upload success event
- `attachmentUploadFailure`: File upload failure event
- `attachmentRemoved`: File removal event
- `editableContextClicked`: Fires when user clicks an inline context item in thinking blocks

---

## Common Use Cases

### Chat Bot with AI Integration
Build a customer service chatbot connected to OpenAI or Azure services:
1. Set up component with suggestions
2. Handle promptRequest to send to AI API
3. Stream responses for real-time feedback
4. Use templates for branded appearance

### Voice-Enabled Assistant
Create hands-free voice interaction:
1. Enable speechToTextSettings
2. Configure Text-to-Speech toolbar button
3. Handle speech events for status
4. Provide visual feedback during voice capture

### File Analysis Chat
Allow users to upload and discuss files:
1. Enable attachments
2. Configure file restrictions (type, size, count)
3. Send files with prompts to backend
4. Display file information in conversation

### Multi-Feature Dashboard
Combine chat with settings and content:
1. Create multiple views (Assist + Custom)
2. Use templates for custom view content
3. Implement view switching logic
4. Share conversation state between views

### Thinking-Enabled Reasoning Assistant
Showcase AI's reasoning process for complex tasks:
1. Inject AssistThinking module for thinking block support
2. Configure thinking blocks with multiple stages
3. Stream blocks with status updates (inprogress → completed)
4. Add context items (tools, files, search results) within stages
5. Customize block templates for transparent reasoning display
6. Handle editableContextClicked for interactive exploration

### Generative UI with Dynamic Interactive Tools
Render dynamic interactive components and custom tools within AI responses:
1. Register custom tools (charts, cards, forms) using registerToolUI()
2. Configure tool templates for responsive UI rendering
3. Define blocks array with TextBlock and ToolBlock combinations
4. Configure AI system prompt for structured JSON generation
5. Send tool blocks within addPromptResponse() calls
6. Create rich, interactive experiences with AI-generated UI elements

---