---
name: hermespet-macos-ai-companion
description: Build, configure, and extend HermesPet — a native macOS AI companion living in the Dynamic Island with multi-engine support, desktop pets, and advanced system integration
triggers:
  - how do I build HermesPet from source
  - configure HermesPet AI engines
  - add a new AI provider to HermesPet
  - customize HermesPet desktop pet animations
  - integrate voice recognition in HermesPet
  - troubleshoot HermesPet Dynamic Island display
  - extend HermesPet with new AI capabilities
  - debug HermesPet memory and context system
---

# HermesPet macOS AI Companion Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## What is HermesPet?

HermesPet is a native macOS application (macOS 14+) built with Swift 6 and SwiftUI that places an AI companion in your MacBook's Dynamic Island. It supports **5 parallel AI engines** (DeepSeek, Kimi, MiniMax, OpenAI, Claude Code, Codex, OpenClaw, custom gateways), **5 pixel desktop pets**, voice input, file drag-and-drop, multi-conversation context sharing, and local memory tracking.

**Key Architecture:**
- Pure native Swift 6 (no Electron/WebView)
- SwiftUI-based UI with Dynamic Island integration
- Local SQLite for conversation/memory storage
- SFSpeechRecognizer for offline voice recognition
- Multi-threaded AI engine orchestration (up to 8 simultaneous conversations)
- Embedded opencode runtime for cloud AI (zero external dependencies)
- Apache 2.0 licensed

## Project Structure

```
HermesPet/
├── HermesPet/              # Main app target
│   ├── Models/             # Data models (Conversation, Message, AIEngine)
│   ├── Views/              # SwiftUI views
│   │   ├── DynamicIslandView.swift
│   │   ├── ChatWindowView.swift
│   │   ├── DesktopPetView.swift
│   │   └── SettingsView.swift
│   ├── Managers/           # Core business logic
│   │   ├── AIEngineManager.swift
│   │   ├── ConversationManager.swift
│   │   ├── VoiceManager.swift
│   │   ├── MemoryManager.swift
│   │   └── UpdateManager.swift
│   ├── Services/           # AI provider integrations
│   │   ├── CloudAIService.swift
│   │   ├── ClaudeCodeService.swift
│   │   ├── CodexService.swift
│   │   ├── OpenClawService.swift
│   │   └── HermesGatewayService.swift
│   └── Utils/              # Helpers (FileDropHandler, MarkdownRenderer)
└── docs/                   # Assets and documentation
```

## Building from Source

### Prerequisites

```bash
# Requires Xcode 15.0+ (for Swift 6)
xcode-select --install

# Optional CLI tools (auto-detected by app)
# Claude Code
brew install anthropic-cli

# Codex (if available)
npm install -g @openai/codex-cli

# OpenClaw
npm install -g openclaw
```

### Build Steps

```bash
# Clone repository
git clone https://github.com/basionwang-bot/HermesPet.git
cd HermesPet

# Open in Xcode
open HermesPet.xcodeproj

# Or build from command line
xcodebuild -scheme HermesPet -configuration Release build

# Create DMG for distribution
# (Uses create-dmg script in scripts/)
./scripts/create-dmg.sh
```

**Code Signing Configuration:**

```swift
// HermesPet.xcodeproj settings
PRODUCT_BUNDLE_IDENTIFIER = "cc.hermespet.HermesPet"
DEVELOPMENT_TEAM = "R34KL4X4D9" // Official Team ID
CODE_SIGN_IDENTITY = "Apple Development"
ENABLE_HARDENED_RUNTIME = YES
MACOS_DEPLOYMENT_TARGET = 14.0
```

## Key Components & Extension Points

### 1. Adding a New AI Engine

Create a new service conforming to `AIServiceProtocol`:

```swift
// Services/CustomAIService.swift
import Foundation

protocol AIServiceProtocol {
    var engineType: AIEngineType { get }
    func sendMessage(_ message: String, context: [Message]) async throws -> String
    func streamMessage(_ message: String, context: [Message]) async throws -> AsyncThrowingStream<String, Error>
    func isAvailable() -> Bool
}

class CustomAIService: AIServiceProtocol {
    var engineType: AIEngineType { .custom }
    
    private let baseURL: String
    private let apiKey: String
    
    init(baseURL: String, apiKey: String) {
        self.baseURL = baseURL
        self.apiKey = apiKey
    }
    
    func isAvailable() -> Bool {
        // Check if API key is configured and endpoint is reachable
        return !apiKey.isEmpty && checkEndpointHealth()
    }
    
    func sendMessage(_ message: String, context: [Message]) async throws -> String {
        let request = buildRequest(message: message, context: context)
        let (data, response) = try await URLSession.shared.data(for: request)
        
        guard let httpResponse = response as? HTTPURLResponse,
              (200...299).contains(httpResponse.statusCode) else {
            throw AIServiceError.invalidResponse
        }
        
        let result = try JSONDecoder().decode(CustomAIResponse.self, from: data)
        return result.content
    }
    
    func streamMessage(_ message: String, context: [Message]) async throws -> AsyncThrowingStream<String, Error> {
        AsyncThrowingStream { continuation in
            Task {
                let request = buildStreamRequest(message: message, context: context)
                let (bytes, _) = try await URLSession.shared.bytes(for: request)
                
                for try await line in bytes.lines {
                    if line.hasPrefix("data: ") {
                        let json = String(line.dropFirst(6))
                        if let chunk = parseChunk(json) {
                            continuation.yield(chunk)
                        }
                    }
                }
                continuation.finish()
            }
        }
    }
    
    private func buildRequest(message: String, context: [Message]) -> URLRequest {
        var request = URLRequest(url: URL(string: "\(baseURL)/v1/chat/completions")!)
        request.httpMethod = "POST"
        request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
        request.setValue("application/json", forHTTPHeaderField: "Content-Type")
        
        let messages = context.map { ["role": $0.role, "content": $0.content] }
        let body: [String: Any] = [
            "model": "custom-model",
            "messages": messages + [["role": "user", "content": message]],
            "temperature": 0.7
        ]
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        return request
    }
    
    private func checkEndpointHealth() -> Bool {
        // Implement health check
        return true
    }
}
```

Register in `AIEngineManager`:

```swift
// Managers/AIEngineManager.swift
class AIEngineManager: ObservableObject {
    @Published var availableEngines: [AIEngineType] = []
    private var services: [AIEngineType: AIServiceProtocol] = [:]
    
    func detectAvailableEngines() {
        services = [:]
        
        // Cloud AI (always available with embedded runtime)
        if let cloudService = CloudAIService() {
            services[.cloudAI] = cloudService
            availableEngines.append(.cloudAI)
        }
        
        // Custom gateway
        if let customAPIKey = ProcessInfo.processInfo.environment["CUSTOM_AI_API_KEY"],
           let baseURL = ProcessInfo.processInfo.environment["CUSTOM_AI_BASE_URL"] {
            let customService = CustomAIService(baseURL: baseURL, apiKey: customAPIKey)
            if customService.isAvailable() {
                services[.custom] = customService
                availableEngines.append(.custom)
            }
        }
        
        // Claude Code (check CLI)
        if checkCLIAvailable("claude") {
            services[.claudeCode] = ClaudeCodeService()
            availableEngines.append(.claudeCode)
        }
        
        // ... other engines
    }
    
    private func checkCLIAvailable(_ command: String) -> Bool {
        let process = Process()
        process.launchPath = "/usr/bin/which"
        process.arguments = [command]
        process.launch()
        process.waitUntilExit()
        return process.terminationStatus == 0
    }
}
```

### 2. Creating Custom Desktop Pet Animations

Desktop pets are SwiftUI views with state-driven animations:

```swift
// Views/Pets/CustomPetView.swift
import SwiftUI

struct CustomPetView: View {
    @State private var position: CGPoint
    @State private var animationPhase: PetAnimationPhase = .idle
    @State private var isSniffing = false
    
    enum PetAnimationPhase {
        case idle, walking, sniffing, eating, celebrating
    }
    
    var body: some View {
        ZStack {
            // Base sprite (16x16 pixel art)
            Image(spriteName)
                .interpolation(.none)
                .resizable()
                .frame(width: 48, height: 48)
            
            // Overlay effects (sniff particles, etc.)
            if isSniffing {
                sniffParticles
            }
        }
        .position(position)
        .onAppear { startIdleAnimation() }
    }
    
    private var spriteName: String {
        switch animationPhase {
        case .idle: return "custom-pet-idle-\(idleFrame)"
        case .walking: return "custom-pet-walk-\(walkFrame)"
        case .sniffing: return "custom-pet-sniff"
        case .eating: return "custom-pet-eat-\(eatFrame)"
        case .celebrating: return "custom-pet-celebrate"
        }
    }
    
    private var sniffParticles: some View {
        ForEach(0..<3, id: \.self) { i in
            Circle()
                .fill(Color.white.opacity(0.6))
                .frame(width: 4, height: 4)
                .offset(x: CGFloat(i * 8) - 8, y: -10)
                .animation(
                    .easeInOut(duration: 0.8)
                    .repeatForever()
                    .delay(Double(i) * 0.2),
                    value: isSniffing
                )
        }
    }
    
    func sniff(at location: CGPoint) {
        withAnimation(.spring(response: 0.3)) {
            position = location
            animationPhase = .sniffing
            isSniffing = true
        }
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            withAnimation {
                isSniffing = false
                animationPhase = .idle
            }
        }
    }
    
    func eat(file: URL) {
        animationPhase = .eating
        // Trigger eating animation cycle
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) {
            animationPhase = .idle
        }
    }
    
    private func startIdleAnimation() {
        Timer.scheduledTimer(withTimeInterval: 0.5, repeats: true) { _ in
            if animationPhase == .idle {
                idleFrame = (idleFrame + 1) % 4
            }
        }
    }
    
    @State private var idleFrame = 0
    @State private var walkFrame = 0
    @State private var eatFrame = 0
}
```

Register pet in `DesktopPetManager`:

```swift
// Managers/DesktopPetManager.swift
class DesktopPetManager: ObservableObject {
    @Published var currentPet: AnyView?
    
    func setPet(for engine: AIEngineType) {
        switch engine {
        case .cloudAI:
            currentPet = AnyView(CloudPetView())
        case .claudeCode:
            currentPet = AnyView(ClawdPetView())
        case .custom:
            currentPet = AnyView(CustomPetView(position: initialPosition))
        // ... other pets
        default:
            currentPet = nil
        }
    }
}
```

### 3. Extending Memory System

The memory system tracks user interactions locally:

```swift
// Managers/MemoryManager.swift
import Foundation
import SQLite3

class MemoryManager {
    private var db: OpaquePointer?
    private let sensitiveKeywords = ["password", "salary", "contract", ".env", "secret"]
    
    init() {
        openDatabase()
        createTables()
    }
    
    private func openDatabase() {
        let fileURL = try! FileManager.default
            .url(for: .applicationSupportDirectory, in: .userDomainMask, appropriateFor: nil, create: true)
            .appendingPathComponent("HermesPet/memory.sqlite")
        
        if sqlite3_open(fileURL.path, &db) != SQLITE_OK {
            print("Failed to open database")
        }
    }
    
    private func createTables() {
        let createIntentTable = """
        CREATE TABLE IF NOT EXISTS user_intents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp INTEGER NOT NULL,
            app_name TEXT,
            file_path TEXT,
            query TEXT,
            ai_engine TEXT,
            response_summary TEXT
        )
        """
        executeSQL(createIntentTable)
    }
    
    func recordIntent(app: String?, filePath: String?, query: String, engine: AIEngineType, response: String) {
        // Blacklist check
        if let path = filePath, containsSensitiveKeyword(path) { return }
        if containsSensitiveKeyword(query) { return }
        
        let summary = summarizeResponse(response) // First 200 chars
        let sql = """
        INSERT INTO user_intents (timestamp, app_name, file_path, query, ai_engine, response_summary)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        
        var stmt: OpaquePointer?
        if sqlite3_prepare_v2(db, sql, -1, &stmt, nil) == SQLITE_OK {
            sqlite3_bind_int64(stmt, 1, Int64(Date().timeIntervalSince1970))
            sqlite3_bind_text(stmt, 2, app, -1, nil)
            sqlite3_bind_text(stmt, 3, filePath, -1, nil)
            sqlite3_bind_text(stmt, 4, query, -1, nil)
            sqlite3_bind_text(stmt, 5, engine.rawValue, -1, nil)
            sqlite3_bind_text(stmt, 6, summary, -1, nil)
            
            if sqlite3_step(stmt) != SQLITE_DONE {
                print("Failed to insert intent")
            }
        }
        sqlite3_finalize(stmt)
    }
    
    func getDailySummary(for date: Date) -> String {
        let startOfDay = Calendar.current.startOfDay(for: date)
        let endOfDay = startOfDay.addingTimeInterval(86400)
        
        let sql = """
        SELECT app_name, file_path, query, response_summary
        FROM user_intents
        WHERE timestamp >= ? AND timestamp < ?
        ORDER BY timestamp ASC
        """
        
        var intents: [(app: String?, file: String?, query: String, response: String)] = []
        var stmt: OpaquePointer?
        
        if sqlite3_prepare_v2(db, sql, -1, &stmt, nil) == SQLITE_OK {
            sqlite3_bind_int64(stmt, 1, Int64(startOfDay.timeIntervalSince1970))
            sqlite3_bind_int64(stmt, 2, Int64(endOfDay.timeIntervalSince1970))
            
            while sqlite3_step(stmt) == SQLITE_ROW {
                let app = sqlite3_column_text(stmt, 0).map { String(cString: $0) }
                let file = sqlite3_column_text(stmt, 1).map { String(cString: $0) }
                let query = String(cString: sqlite3_column_text(stmt, 2))
                let response = String(cString: sqlite3_column_text(stmt, 3))
                intents.append((app, file, query, response))
            }
        }
        sqlite3_finalize(stmt)
        
        return generateSummaryPrompt(from: intents)
    }
    
    private func containsSensitiveKeyword(_ text: String) -> Bool {
        let lowercase = text.lowercased()
        return sensitiveKeywords.contains { lowercase.contains($0) }
    }
    
    private func generateSummaryPrompt(from intents: [(app: String?, file: String?, query: String, response: String)]) -> String {
        var prompt = "Based on yesterday's activity:\n\n"
        for intent in intents {
            if let app = intent.app { prompt += "- Used \(app)\n" }
            if let file = intent.file { prompt += "- Worked on \(file)\n" }
            prompt += "- Asked: \(intent.query)\n"
        }
        prompt += "\nGenerate a brief daily summary in Markdown and suggest 1-2 follow-up actions."
        return prompt
    }
    
    func exportMemory() -> Data? {
        let sql = "SELECT * FROM user_intents"
        var intents: [[String: Any]] = []
        var stmt: OpaquePointer?
        
        if sqlite3_prepare_v2(db, sql, -1, &stmt, nil) == SQLITE_OK {
            while sqlite3_step(stmt) == SQLITE_ROW {
                var intent: [String: Any] = [:]
                for i in 0..<sqlite3_column_count(stmt) {
                    let name = String(cString: sqlite3_column_name(stmt, i))
                    if let text = sqlite3_column_text(stmt, i) {
                        intent[name] = String(cString: text)
                    }
                }
                intents.append(intent)
            }
        }
        sqlite3_finalize(stmt)
        
        return try? JSONSerialization.data(withJSONObject: intents, options: .prettyPrinted)
    }
}
```

### 4. Integrating Voice Recognition

Voice input uses SFSpeechRecognizer for offline Chinese/English:

```swift
// Managers/VoiceManager.swift
import Speech
import AVFoundation

class VoiceManager: NSObject, ObservableObject {
    @Published var isRecording = false
    @Published var transcription = ""
    @Published var permissionGranted = false
    
    private let speechRecognizer: SFSpeechRecognizer?
    private var recognitionRequest: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    
    override init() {
        // Auto-detect system language, fallback to Chinese
        let locale = Locale.current.language.languageCode?.identifier ?? "zh-CN"
        self.speechRecognizer = SFSpeechRecognizer(locale: Locale(identifier: locale))
        super.init()
        
        requestPermission()
    }
    
    func requestPermission() {
        SFSpeechRecognizer.requestAuthorization { status in
            DispatchQueue.main.async {
                self.permissionGranted = (status == .authorized)
            }
        }
    }
    
    func startRecording() throws {
        guard permissionGranted else {
            throw VoiceError.permissionDenied
        }
        
        // Cancel previous task
        recognitionTask?.cancel()
        recognitionTask = nil
        
        // Configure audio session
        let audioSession = AVAudioSession.sharedInstance()
        try audioSession.setCategory(.record, mode: .measurement, options: .duckOthers)
        try audioSession.setActive(true, options: .notifyOthersOnDeactivation)
        
        recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        guard let recognitionRequest = recognitionRequest else {
            throw VoiceError.recognitionUnavailable
        }
        
        recognitionRequest.shouldReportPartialResults = true
        
        let inputNode = audioEngine.inputNode
        recognitionTask = speechRecognizer?.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            if let result = result {
                DispatchQueue.main.async {
                    self?.transcription = result.bestTranscription.formattedString
                }
            }
            
            if error != nil || result?.isFinal == true {
                self?.stopRecording()
            }
        }
        
        let recordingFormat = inputNode.outputFormat(forBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: recordingFormat) { buffer, _ in
            recognitionRequest.append(buffer)
        }
        
        audioEngine.prepare()
        try audioEngine.start()
        
        DispatchQueue.main.async {
            self.isRecording = true
        }
    }
    
    func stopRecording() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        recognitionRequest?.endAudio()
        
        DispatchQueue.main.async {
            self.isRecording = false
        }
    }
}

enum VoiceError: Error {
    case permissionDenied
    case recognitionUnavailable
}
```

Trigger via global hotkey (⌘⇧V):

```swift
// AppDelegate.swift
import Carbon

class AppDelegate: NSObject, NSApplicationDelegate {
    var hotKeyRef: EventHotKeyRef?
    let voiceManager = VoiceManager()
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        registerPushToTalkHotkey()
    }
    
    private func registerPushToTalkHotkey() {
        var eventType = EventTypeSpec(eventClass: OSType(kEventClassKeyboard), eventKind: UInt32(kEventHotKeyPressed))
        InstallEventHandler(GetApplicationEventTarget(), { _, event, userData in
            let manager = Unmanaged<VoiceManager>.fromOpaque(userData!).takeUnretainedValue()
            try? manager.startRecording()
            return noErr
        }, 1, &eventType, Unmanaged.passUnretained(voiceManager).toOpaque(), nil)
        
        // ⌘⇧V = Command + Shift + V
        let hotKeyID = EventHotKeyID(signature: 0x48505054, id: 1) // 'HPPT'
        RegisterEventHotKey(UInt32(kVK_ANSI_V), UInt32(cmdKey | shiftKey), hotKeyID, GetApplicationEventTarget(), 0, &hotKeyRef)
    }
}
```

### 5. Dynamic Island Integration

The Dynamic Island view responds to app state:

```swift
// Views/DynamicIslandView.swift
import SwiftUI

struct DynamicIslandView: View {
    @ObservedObject var conversationManager: ConversationManager
    @ObservedObject var engineManager: AIEngineManager
    @State private var isExpanded = false
    @State private var showCompletionCheckmark = false
    
    var body: some View {
        HStack(spacing: 12) {
            // Left ear: Pet sprite
            currentPetSprite
                .frame(width: 24, height: 24)
            
            Spacer()
            
            // Right ear: Status indicator
            statusIndicator
                .frame(width: 24, height: 24)
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .background(
            Capsule()
                .fill(isExpanded ? Color.black.opacity(0.9) : Color.clear)
                .overlay(
                    Capsule()
                        .stroke(engineManager.currentEngine.accentColor, linewidth: isExpanded ? 2 : 0)
                )
        )
        .frame(width: isExpanded ? 300 : 100, height: 36)
        .position(x: NSScreen.main!.frame.width / 2, y: 32) // Below notch
        .animation(.spring(response: 0.3, dampingFraction: 0.7), value: isExpanded)
        .onHover { hovering in
            isExpanded = hovering
        }
        .onChange(of: conversationManager.isProcessing) { processing in
            if !processing {
                showCompletionAnimation()
            }
        }
    }
    
    private var currentPetSprite: some View {
        Image(engineManager.currentEngine.petSpriteName)
            .interpolation(.none)
            .resizable()
            .aspectRatio(contentMode: .fit)
    }
    
    private var statusIndicator: some View {
        ZStack {
            if conversationManager.isProcessing {
                // Rotating pulse
                Circle()
                    .trim(from: 0, to: 0.7)
                    .stroke(engineManager.currentEngine.accentColor, lineWidth: 3)
                    .rotationEffect(.degrees(rotationAngle))
                    .onAppear {
                        withAnimation(.linear(duration: 1).repeatForever(autoreverses: false)) {
                            rotationAngle = 360
                        }
                    }
            } else if showCompletionCheckmark {
                // Face ID style checkmark
                Path { path in
                    path.move(to: CGPoint(x: 6, y: 12))
                    path.addLine(to: CGPoint(x: 10, y: 16))
                    path.addLine(to: CGPoint(x: 18, y: 8))
                }
                .trim(from: 0, to: checkmarkProgress)
                .stroke(Color.green, style: StrokeStyle(lineWidth: 2, lineCap: .round, lineJoin: .round))
                .onAppear {
                    withAnimation(.easeInOut(duration: 0.4)) {
                        checkmarkProgress = 1.0
                    }
                }
            }
        }
    }
    
    @State private var rotationAngle: Double = 0
    @State private var checkmarkProgress: CGFloat = 0
    
    private func showCompletionAnimation() {
        showCompletionCheckmark = true
        checkmarkProgress = 0
        
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) {
            withAnimation {
                showCompletionCheckmark = false
            }
        }
    }
}
```

## Configuration

### Environment Variables

```bash
# Cloud AI providers (choose one or multiple)
export DEEPSEEK_API_KEY="sk-..."
export KIMI_API_KEY="sk-..."
export MINIMAX_API_KEY="..."
export OPENAI_API_KEY="sk-..."

# Custom OpenAI-compatible gateway
export HERMES_GATEWAY_BASE_URL="https://your-gateway.com/v1"
export HERMES_GATEWAY_API_KEY="..."

# OpenClaw (auto-detected if installed)
# npm install -g openclaw
# openclaw start

# Optional: Disable specific engines
export HERMESPET_DISABLE_CLAUDE_CODE=1
export HERMESPET_DISABLE_CODEX=1

# Privacy: Disable memory tracking
export HERMESPET_DISABLE_MEMORY=1
```

### App Settings (Settings.bundle)

```xml
<!-- Settings.bundle/Root.plist -->
<dict>
    <key>PreferenceSpecifiers</key>
    <array>
        <dict>
            <key>Type</key>
            <string>PSToggleSwitchSpecifier</string>
            <key>Title</key>
            <string>Enable Memory Tracking</string>
            <key>Key</key>
            <string>memory_enabled</string>
            <key>DefaultValue</key>
            <true/>
        </dict>
        <dict>
            <key>Type</key>
            <string>PSMultiValueSpecifier</string>
            <key>Title</key>
            <string>Default AI Engine</string>
            <key>Key</key>
            <string>default_engine</string>
            <key>Values</key>
            <array>
                <string>cloudAI</string>
                <string>claudeCode</string>
                <string>codex</string>
            </array>
            <key>DefaultValue</key>
            <string>cloudAI</string>
        </dict>
    </array>
</dict>
```

## Common Patterns

### Sending a Message with Context

```swift
let conversationManager = ConversationManager()
let conversation = conversationManager.createConversation(engine: .cloudAI)

Task {
    do {
        let response = try await conversationManager.sendMessage(
            "Explain Swift concurrency",
            to: conversation,
            attachments: [URL(fileURLWithPath: "/path/to/code.swift")]
        )
        print("AI Response: \(response)")
    } catch {
        print("Error: \(error)")
    }
}
```

### Streaming Response

```swift
Task {
    let stream = try await conversationManager.streamMessage(
        "Write a SwiftUI animation",
        to: conversation
    )
    
    for try await chunk in stream {
        print(chunk, terminator: "")
    }
}
```

### File Drop Handling

```swift
// Views/ChatWindowView.swift
.onDrop(of: [.fileURL], isTargeted: $isDropTargeted) { providers in
    providers.forEach { provider in
        _ = provider.loadObject(ofClass: URL.self) { url, error in
            guard let url = url else { return }
            DispatchQueue.main.async {
                conversationManager.addAttachment(url, to: currentConversation)
            }
        }
    }
    return true
}
```

### Tool Permission Confirmation

```swift
// Managers/ToolPermissionManager.swift
class ToolPermissionManager: ObservableObject {
    @Published var pendingRequest: ToolRequest?
    
    func requestPermission(for tool: ToolRequest, completion: @escaping (Bool) -> Void) {
        DispatchQueue.main.async {
            self.pendingRequest = tool
            self.permissionCallback = completion
        }
    }
