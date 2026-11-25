---
name: syncfusion-aspnetcore-speech-to-text
description: Implement the Syncfusion ASP.NET Core SpeechToText control for converting spoken words to text using Web Speech API. Use this skill when implementing speech recognition with Razor Tag Helpers, converting voice to text in ASP.NET Core applications, handling microphone input, processing speech events, customizing button appearance, managing listening states, or building accessible voice-enabled forms. Covers setup, speech recognition features, Razor Tag Helper syntax, events, methods, globalization, and security.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion ASP.NET Core SpeechToText Control

## Overview

The SpeechToText control enables users to convert spoken words into text using the Web Speech API in ASP.NET Core applications. This skill helps you implement, customize, and troubleshoot speech recognition using Razor Tag Helpers.

The main Razor Tag Helper that captures audio and converts speech to text in real-time using browser APIs.

**Key Features:**
- Real-time speech recognition via Web Speech API
- Multiple language support
- Customizable button and tooltip via tag helper attributes
- Event-driven architecture
- Programmatic control via JavaScript methods
- Accessibility support (ARIA labels, keyboard navigation)
- Localization support
- Error handling and recovery
- ASP.NET Core binding

## Documentation

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Installation via NuGet
- ASP.NET Core project setup
- Razor Tag Helper registration
- Basic control implementation
- CSS imports and theme selection
- First working example
- Script manager configuration

### Speech Recognition Features
📄 **Read:** [references/speech-recognition-features.md](references/speech-recognition-features.md)
- Retrieving transcripts in real-time
- Setting language for recognition
- Managing interim results
- Listening state management
- Handling speech-to-text conversion
- Real-time vs final results
- Multi-language support

### Button and Tooltip Customization
📄 **Read:** [references/button-and-tooltip-customization.md](references/button-and-tooltip-customization.md)
- Button customization via tag helper attributes
- Icon customization using CSS classes
- Icon positioning
- Tooltip configuration
- Primary button styling
- CSS class styling (e-primary, e-success, etc.)
- Responsive design

### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Event binding in Razor (onStart, onStop, onError, transcriptChanged)
- Event handling in script tag
- Error types and error handling
- startListening() and stopListening() methods
- Programmatic control via JavaScript
- Getting component instance with ej.base.getComponent()
- Event workflows and patterns

### Globalization and Localization
📄 **Read:** [references/globalization-and-localization.md](references/globalization-and-localization.md)
- Localization with L10n.load()
- Available locale strings
- Language-specific error messages
- RTL support via enableRtl attribute
- Accessibility labels and ARIA attributes
- Multi-language interface examples

### Troubleshooting and Security
📄 **Read:** [references/troubleshooting-and-security.md](references/troubleshooting-and-security.md)
- Common issues and solutions
- Browser compatibility matrix
- Microphone permission handling
- Security considerations for ASP.NET Core
- Privacy and data transmission
- Performance optimization
- Offline fallback strategies

## Quick Start Example

```razor
@using Syncfusion.EJ2.Inputs

<div id='speechtotext-container'>
    <ejs-speechtotext id="speech-to-text" transcriptChanged="onTranscriptChanged"></ejs-speechtotext>
    <ejs-textarea id="output-textarea" rows="5" cols="50" value="" resizeMode="None" placeholder="Transcribed text will be shown here..."></ejs-textarea>
</div>

<script>
    function onTranscriptChanged(args) {
        var textareaObj = ej.base.getComponent(document.getElementById("output-textarea"), "textarea");
        textareaObj.value = args.transcript;
    }
</script>

<style>
    #speechtotext-container {
        gap: 20px;
        display: flex;
        flex-direction: column;
        align-items: center;
    }
</style>
```

## Common Patterns

### Pattern 1: Voice Form with Multiple Fields

```razor
@using Syncfusion.EJ2.Inputs

<div class="form-group">
    <label>Name (speak):</label>
    <ejs-speechtotext id="name-voice" transcriptChanged="onNameTranscript"></ejs-speechtotext>
    <ejs-textbox id="name-field"></ejs-textbox>
</div>

<div class="form-group">
    <label>Message (speak):</label>
    <ejs-speechtotext id="message-voice" transcriptChanged="onMessageTranscript"></ejs-speechtotext>
    <ejs-textarea id="message-field" rows="4"></ejs-textarea>
</div>

<script>
    function onNameTranscript(args) {
        var nameField = ej.base.getComponent(document.getElementById("name-field"), "textbox");
        nameField.value = args.transcript;
    }

    function onMessageTranscript(args) {
        var messageField = ej.base.getComponent(document.getElementById("message-field"), "textarea");
        messageField.value = args.transcript;
    }
</script>
```

### Pattern 2: Programmatic Control

```razor
@using Syncfusion.EJ2.Inputs

<ejs-speechtotext id="speech-control"></ejs-speechtotext>

<div>
    <button onclick="startVoiceInput()">Start Recording</button>
    <button onclick="stopVoiceInput()">Stop Recording</button>
</div>

<script>
    function startVoiceInput() {
        var speechComponent = ej.base.getComponent(
            document.getElementById("speech-control"), 
            "speechtotext"
        );
        speechComponent.startListening();
    }

    function stopVoiceInput() {
        var speechComponent = ej.base.getComponent(
            document.getElementById("speech-control"), 
            "speechtotext"
        );
        speechComponent.stopListening();
    }
</script>
```

### Pattern 3: Error Handling

```razor
@using Syncfusion.EJ2.Inputs

<ejs-speechtotext id="error-speech" 
    onError="handleError" 
    onStart="handleStart" 
    onStop="handleStop">
</ejs-speechtotext>

<div id="error-message" style="display:none; color: red; padding: 10px;"></div>

<script>
    function handleError(args) {
        var errorDiv = document.getElementById("error-message");
        errorDiv.style.display = "block";
        
        var errorMessages = {
            'no-speech': '🔇 No speech detected. Please try again.',
            'audio-capture': '🎙️ Microphone not found.',
            'not-allowed': '🔒 Microphone permission denied.',
            'network': '🌐 Network error occurred.'
        };
        
        errorDiv.textContent = errorMessages[args.error] || 'Error: ' + args.error;
        setTimeout(() => { errorDiv.style.display = "none"; }, 5000);
    }

    function handleStart() {
        console.log('🎤 Listening started');
    }

    function handleStop() {
        console.log('⏹️ Listening stopped');
    }
</script>
```

## Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `lang` | string | Language code (e.g., 'en-US', 'fr-FR') |
| `transcript` | string | Current transcribed text |
| `allowInterimResults` | boolean | Show real-time results (default: true) |
| `listeningState` | enum | Current state (Inactive, Listening, Stopped) |
| `cssClass` | string | CSS classes (e-primary, e-success, etc.) |
| `enableRtl` | boolean | Enable right-to-left layout |
| `locale` | string | Localization language code |

## Tag Helper Attributes

```razor
<ejs-speechtotext 
    id="speechId"
    lang="en-US"
    allowInterimResults="true"
    cssClass="e-primary"
    enableRtl="false"
    locale="en-US"
    transcriptChanged="onTranscriptChanged"
    onStart="onStartListening"
    onStop="onStopListening"
    onError="onError"
    created="onCreated">
    
    <e-speechtotext-buttonSettings 
        content="Start Listening" 
        stopContent="Stop Listening"
        iconCss="e-icons e-play"
        stopIconCss="e-icons e-pause"
        iconPosition="Right"
        isPrimary="true">
    </e-speechtotext-buttonSettings>
    
    <e-speechtotext-tooltipSettings 
        position="TopCenter"
        content="Click to start"
        stopContent="Click to stop">
    </e-speechtotext-tooltipSettings>
</ejs-speechtotext>
```

## Event Handlers

| Event | Args | Description |
|-------|------|-------------|
| `created` | - | Fired when control is initialized |
| `onStart` | StartListeningEventArgs | Fired when listening begins |
| `onStop` | StopListeningEventArgs | Fired when listening ends |
| `onError` | ErrorEventArgs | Fired when error occurs |
| `transcriptChanged` | TranscriptChangedEventArgs | Fired when transcript updates |

## Methods

| Method | Description |
|--------|-------------|
| `startListening()` | Begin speech recognition |
| `stopListening()` | Stop speech recognition |

## Troubleshooting

### Control not rendering
**Solution:** Check that `<ejs-scripts></ejs-scripts>` is in layout and CSS is imported

### Events not firing
**Solution:** Verify event handlers are valid JavaScript functions in global scope

### Microphone permission denied
**Solution:** Allow microphone access in browser settings

### Speech not recognized
**Solution:** Check microphone volume, speak clearly, verify language setting

