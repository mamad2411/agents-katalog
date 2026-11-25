---
name: syncfusion-angular-speech-to-text
description: Implement the Syncfusion Angular SpeechToText component. Use this skill for real-time speech-to-text conversion with text transcripts, custom button appearance and tooltips, recognition event handling, multiple language support with localization and RTL, error handling, and security best practices for microphone access and data transmission.
metadata:
  author: "Syncfusion Inc"
  version: "33.1.44"
---

# Syncfusion Angular SpeechToText Component

## Component Overview

The **Syncfusion Angular SpeechToText component** is a lightweight, accessible control that converts spoken words into text using the browser's native Speech Recognition API.

**Key Capabilities:**
- **Real-time Transcription** - Convert speech to text with interim and final results
- **Button Customization** - Configure icon, text, positioning, and styling for start/stop buttons
- **Tooltip Support** - Add tooltips with custom content and positioning for better UX
- **Events & Interactions** - Handle listening state changes, errors, and transcript updates
- **Methods** - Programmatic control via startListening() and stopListening() methods
- **Language Support** - Multi-language recognition with locale configuration
- **Globalization** - RTL support and localization for international applications
- **Styling Options** - CSS classes, HTML attributes, and theme integration
- **Security Features** - HTTPS enforcement and explicit microphone permissions
- **Browser Compatibility** - Chrome 25+, Edge 79+, Safari 12+, Opera 30+

## Documentation and Navigation Guide

### Getting Started
📄 **Read:** [references/getting-started.md](references/getting-started.md)
- Package installation (Ivy vs ngcc compatibility)
- Angular project setup and configuration
- CSS imports and theme management
- Module imports and basic component rendering
- Button content customization
- Complete working example with TextArea integration

### Button Customization
📄 **Read:** [references/button-customization.md](references/button-customization.md)
- ButtonSettingsModel configuration
- Start and stop button content labels
- Icon customization with CSS classes
- Icon positioning (top, bottom, left, right)
- Primary button styling for emphasis
- Visual style variations and best practices

### Tooltip Configuration
📄 **Read:** [references/tooltip-configuration.md](references/tooltip-configuration.md)
- TooltipSettingsModel setup
- Tooltip content for start and stop states
- Tooltip positioning relative to button
- Enabling and disabling tooltips
- Practical tooltip usage patterns

### Styling and Appearance
📄 **Read:** [references/styling-and-appearance.md](references/styling-and-appearance.md)
- CSS class system (e-primary, e-outline, e-info, e-success, e-warning, e-danger)
- Custom styling with cssClass property
- Theme configuration and integration
- HTML attributes customization
- Custom CSS examples and advanced styling

### Events and Methods
📄 **Read:** [references/events-and-methods.md](references/events-and-methods.md)
- Event types (created, onStart, onStop, onError, transcriptChanged)
- Event handler implementation and event arguments (including event, name properties)
- Programmatic control with startListening(), stopListening(), and destroy() methods
- Controlling component state with listeningState property (Inactive, Listening, Stopped)
- Canceling listening with the cancel property in onStart event
- Distinguishing user vs programmatic actions with isInteracted property
- Event handling patterns for different scenarios
- Managing listening lifecycle programmatically
- State transition management and workflow control
- Component cleanup and memory management

### Speech Recognition Features
📄 **Read:** [references/speech-recognition-features.md](references/speech-recognition-features.md)
- Retrieving transcript from speech input
- Setting recognition language (lang property)
- Interim results configuration (allowInterimResults)
- Listening state management (Inactive, Listening, Stopped)
- Tooltip visibility control (showTooltip)
- Disabled state configuration
- State persistence with enablePersistence property
- State monitoring and status management
- Custom state management with localStorage

### Internationalization
📄 **Read:** [references/internationalization.md](references/internationalization.md)
- Localization setup using L10n.load()
- Translation key mapping for error messages and labels
- Multi-language implementation examples
- RTL (Right-to-Left) support enablement
- Language-specific configuration best practices

### Security and Error Handling
📄 **Read:** [references/security-and-error-handling.md](references/security-and-error-handling.md)
- Security risks and mitigation strategies
- Data transmission and privacy concerns
- HTTPS enforcement and MITM prevention
- Microphone permission management
- Error type handling (no-speech, aborted, audio-capture, not-allowed, service-not-allowed, network, unsupported-browser, default)
- Browser support matrix and compatibility

## Quick Start Example

Here's a minimal working SpeechToText component with transcript output:

```typescript
import { Component, ViewChild } from '@angular/core';
import { SpeechToTextModule, TextAreaComponent, TextAreaModule, TranscriptChangedEventArgs } from '@syncfusion/ej2-angular-inputs';

@Component({
    imports: [SpeechToTextModule, TextAreaModule],
    standalone: true,
    selector: 'app-root',
    template: `
    <div class="speechText-container">
        <button ejs-speechtotext 
                (transcriptChanged)="onTranscriptChange($event)">
        </button>
        <ejs-textarea #outputTextarea 
                      id="textareaInst" 
                      value="" 
                      rows="5" 
                      cols="50" 
                      resizeMode="None" 
                      placeholder="Transcribed text will be shown here...">
        </ejs-textarea>
    </div>`
})
export class AppComponent {
    @ViewChild('outputTextarea') outputTextarea!: TextAreaComponent;
    
    onTranscriptChange(args: TranscriptChangedEventArgs): void {
        this.outputTextarea.value = args.transcript;
    }
}
```

## Common Patterns

### Pattern 1: Customized Button with Events
Implement a styled button with custom labels and event handlers:

```typescript
public buttonSettings: ButtonSettingsModel = {
    content: 'Start Listening',
    stopContent: 'Stop Listening',
    iconCss: 'e-icons e-play',
    stopIconCss: 'e-icons e-pause',
    isPrimary: true
};

onListeningStart(args: StartListeningEventArgs): void {
    console.log('Listening started');
}

onListeningStop(args: StopListeningEventArgs): void {
    console.log('Listening stopped');
}
```

### Pattern 2: Multi-Language Support
Configure localization for international applications:

```typescript
L10n.load({
    'de': {
        "speech-to-text": {
            "startAriaLabel": "Drücken Sie, um zu sprechen",
            "stopAriaLabel": "Drücken Sie, um zu stoppen",
            "noSpeechError": "Keine Sprache erkannt"
        }
    }
});
```

### Pattern 3: Programmatic Control
Manage listening state programmatically without user button clicks:

```typescript
@ViewChild('speechtotext') speechToText!: SpeechToTextComponent;

public startListening(): void {
    this.speechToText.startListening();
}

public stopListening(): void {
    this.speechToText.stopListening();
}
```

### Pattern 4: Error Handling
Handle speech recognition errors gracefully:

```typescript
onErrorHandler(args: ErrorEventArgs): void {
    if (args.error === 'no-speech') {
        console.log('No speech detected. Please try again.');
    } else if (args.error === 'not-allowed') {
        console.log('Microphone permission denied.');
    }
}
```

### Pattern 5: Conditional Listening with Cancel
Control when listening can start using the cancel property:

```typescript
onListeningStart(args: StartListeningEventArgs): void {
    // Cancel listening if conditions aren't met
    if (!this.hasPermission || !navigator.onLine) {
        args.cancel = true;
        alert('Cannot start listening. Check permissions and connection.');
        return;
    }
    
    // Track if user or system triggered the action
    if (args.isInteracted) {
        console.log('User clicked the button');
    } else {
        console.log('Started programmatically');
    }
}
```

### Pattern 6: Distinguishing Interim vs Final Results
Handle interim and final transcripts differently:

```typescript
onTranscriptChange(args: TranscriptChangedEventArgs): void {
    if (args.isInterimResult) {
        // Show interim results in real-time (lighter styling)
        this.interimText = args.transcript;
    } else {
        // Process final results (save, send to API, etc.)
        this.finalText = args.transcript;
        this.saveTranscript(args.transcript);
    }
}
```

### Pattern 7: Controlling Component State
Programmatically control the component's operational state:

```typescript
import { SpeechToTextState } from '@syncfusion/ej2-angular-inputs';

export class AppComponent {
    public currentState: SpeechToTextState = SpeechToTextState.Inactive;
    
    // Set component to listening state
    startListening(): void {
        this.currentState = SpeechToTextState.Listening;
    }
    
    // Set component to stopped state
    stopListening(): void {
        this.currentState = SpeechToTextState.Stopped;
    }
    
    // Reset to inactive state
    resetState(): void {
        this.currentState = SpeechToTextState.Inactive;
    }
}
```

### Pattern 8: Proper Component Cleanup
Ensure proper cleanup to prevent memory leaks:

```typescript
import { OnDestroy } from '@angular/core';

export class AppComponent implements OnDestroy {
    @ViewChild('speechtotext') speechToText!: SpeechToTextComponent;
    
    ngOnDestroy(): void {
        if (this.speechToText) {
            this.speechToText.stopListening();
            this.speechToText.destroy();
        }
    }
}
```

## Key Props

| Prop | Type | Default | Purpose |
|------|------|---------|---------|
| `buttonSettings` | ButtonSettingsModel | - | Configure button appearance and labels |
| `tooltipSettings` | TooltipSettingsModel | - | Customize tooltip content and position |
| `lang` | string | `'en-US'` | Set speech recognition language |
| `allowInterimResults` | boolean | `true` | Enable real-time interim transcription |
| `transcript` | string | `''` | Current recognized text (read-only) |
| `listeningState` | SpeechToTextState | `Inactive` | Monitor listening status (Inactive, Listening, Stopped) |
| `showTooltip` | boolean | `true` | Display tooltip on hover |
| `disabled` | boolean | `false` | Disable component interaction |
| `enablePersistence` | boolean | `false` | Persist component state across page reloads |
| `enableRtl` | boolean | `false` | Enable right-to-left text direction |
| `cssClass` | string | - | Apply custom CSS classes |
| `htmlAttributes` | object | - | Set custom HTML attributes on button |
| `locale` | string | `'en-US'` | Set UI localization language |

## Browser Requirements

The SpeechToText component requires:
- **Active internet connection** for speech recognition processing
- **Browser Speech Recognition API support**:
  - Chrome 25+
  - Edge 79+
  - Safari 12+
  - Opera 30+
  - Firefox: Not Supported
- **Microphone hardware** connected to the system
- **User microphone permission** granted in browser settings
- **HTTPS context** for secure microphone access (recommended)
