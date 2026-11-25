# Noted - iOS Piano Learning App Background Instructions

## Project Overview
You are helping to develop "Noted", an iOS app designed to help users learn piano by providing real-time MIDI input visualization and automatic song recording capabilities. The app should be intuitive, educational, and engaging for piano learners of all levels.

## Core Features & Requirements

### 1. MIDI Input Integration
- **Real-time MIDI input detection**: Connect to external MIDI keyboards via USB, Bluetooth, or Lightning adapter
- **Note visualization**: Display played notes in real-time with note names, octaves, and timing
- **Multiple input sources**: Support for various MIDI keyboard brands and models
- **Input configuration**: Allow users to configure MIDI channel, velocity sensitivity, and input preferences

### 2. Visual Note Display
- **Piano keyboard view**: Show a virtual piano with highlighted keys as they're played
- **Note notation**: Display notes in both standard music notation and simplified note names (C4, D#5, etc.)
- **Real-time feedback**: Provide immediate visual feedback when notes are played
- **Customizable display**: Allow users to choose between different visualization modes (keyboard, staff notation, note names)

### 3. Recording & Playback
- **Automatic recording**: Start recording when MIDI input is detected
- **Manual recording control**: Allow users to start/stop recordings manually
- **Playback functionality**: Play back recorded sessions with note visualization
- **Session management**: Save, organize, and manage multiple recording sessions
- **Export options**: Export recordings as MIDI files or audio files

### 4. Learning Features
- **Practice modes**: Include different modes for learning (free play, guided practice, etc.)
- **Progress tracking**: Track playing time, notes played, and improvement over time
- **Metronome**: Built-in metronome with adjustable tempo and time signatures
- **Scale practice**: Provide scale exercises and chord progression practice

### 5. User Interface
- **Clean, intuitive design**: Focus on clarity and ease of use
- **Responsive layout**: Optimize for different iPad and iPhone screen sizes
- **Dark/light mode support**: Provide theme options for different lighting conditions
- **Accessibility**: Support VoiceOver and other accessibility features

## Technical Architecture

### Core Technologies
- **SwiftUI**: Primary UI framework for modern, reactive interfaces
- **Core MIDI**: Handle MIDI input/output and device management
- **AVFoundation**: Audio processing, recording, and playback
- **Core Data**: Local storage for recordings and user preferences
- **Combine**: Reactive programming for MIDI data streams

### Key Components
1. **MIDIManager**: Handle MIDI device connection and data processing
2. **NoteVisualizationView**: Real-time note display and piano keyboard
3. **RecordingEngine**: Manage recording sessions and file I/O
4. **PlaybackEngine**: Handle playback of recorded sessions
5. **SettingsManager**: User preferences and app configuration

### Data Models
```swift
// Key data structures to implement
struct MIDINote {
    let note: UInt8
    let velocity: UInt8
    let timestamp: TimeInterval
    let channel: UInt8
}

struct RecordingSession {
    let id: UUID
    let name: String
    let timestamp: Date
    let notes: [MIDINote]
    let duration: TimeInterval
}
```

## Development Guidelines

### Code Quality
- Follow Swift best practices and naming conventions
- Use dependency injection for testability
- Implement proper error handling and logging
- Write comprehensive unit tests for core functionality

### Performance
- Optimize for real-time MIDI processing (low latency)
- Efficient memory management for long recording sessions
- Smooth animations and responsive UI interactions
- Battery life optimization

### User Experience
- Immediate visual feedback for all user actions
- Intuitive gesture controls (tap, swipe, pinch)
- Clear visual hierarchy and typography
- Helpful onboarding for first-time users

## Implementation Priorities

### Phase 1: Core MIDI Integration
1. Set up Core MIDI framework integration
2. Implement MIDI device discovery and connection
3. Create basic note detection and processing
4. Build simple piano keyboard visualization

### Phase 2: Recording System
1. Implement automatic recording trigger
2. Create recording session management
3. Add playback functionality
4. Build session organization UI

### Phase 3: Enhanced Visualization
1. Add staff notation display option
2. Implement note name overlays
3. Create customizable visualization settings
4. Add real-time note history display

### Phase 4: Learning Features
1. Add built-in metronome
2. Implement practice modes
3. Create progress tracking system
4. Add scale and chord exercise features

## File Structure
```
apps/ios/
├── Sources/
│   ├── App/
│   │   ├── NotedApp.swift
│   │   └── ContentView.swift
│   ├── Features/
│   │   ├── MIDI/
│   │   │   ├── MIDIManager.swift
│   │   │   └── MIDINote.swift
│   │   ├── Recording/
│   │   │   ├── RecordingEngine.swift
│   │   │   └── RecordingSession.swift
│   │   ├── Visualization/
│   │   │   ├── PianoKeyboardView.swift
│   │   │   └── NoteDisplayView.swift
│   │   └── Playback/
│   │       └── PlaybackEngine.swift
│   ├── Services/
│   │   ├── AudioService.swift
│   │   └── DataManager.swift
│   └── Views/
│       ├── MainView.swift
│       ├── RecordingView.swift
│       └── SettingsView.swift
├── Resources/
│   ├── Info.plist
│   └── Assets.xcassets
└── Tests/
    ├── NotedTests/
    └── NotedUITests/
```

## Testing Strategy
- Unit tests for MIDI processing logic
- Integration tests for recording/playback
- UI tests for key user interactions
- Performance tests for real-time processing
- Accessibility testing with VoiceOver

## Success Metrics
- Responsive MIDI input (< 10ms latency)
- Stable recording for 30+ minute sessions
- Smooth UI performance at 60fps
- Successful MIDI device compatibility
- Positive user feedback on learning effectiveness

## Resources for Reference
- Apple's Core MIDI Programming Guide
- MIDI specification documentation
- Piano learning app UX patterns (Midiano, GridNotes)
- Music notation standards and conventions
- iOS Audio Programming best practices

Remember to prioritize user experience and educational value while maintaining technical excellence and performance standards.