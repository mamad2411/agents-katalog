---
name: hermes-desktop-os1-native-macos-client
description: Native macOS interface for AI agents running on Orgo cloud computers with built-in terminal, sessions, kanban, and voice mode
triggers:
  - "set up Hermes Desktop OS1 on macOS"
  - "connect to an Orgo cloud computer"
  - "install the Hermes agent on a VM"
  - "configure OS1 for SSH connections"
  - "use OS1 voice mode with OpenAI Realtime"
  - "build OS1 from source"
  - "troubleshoot Orgo connection issues"
  - "manage OS1 workspace sessions"
---

# Hermes Desktop OS1 Native macOS Client

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

Hermes Desktop - OS1 Edition is a native macOS application that provides a unified workspace for AI agents running on Orgo cloud computers or SSH hosts. It offers direct VM provisioning, automatic agent installation, a real-time websocket terminal, session management, kanban boards, file editing, and WebRTC voice mode powered by OpenAI Realtime.

## What OS1 Does

- **Direct cloud computer integration**: Connects to Orgo VMs via HTTP API and websocket terminal without SSH
- **One-click agent install**: Automatically installs Hermes Agent on fresh cloud computers
- **Native workspace**: Sessions browser, kanban board, file editor, skills viewer, cron manager
- **Real terminal**: Interactive shell over websocket with full resize and reflow support
- **Voice mode**: WebRTC voice interface using OpenAI Realtime with Orgo MCP tool integration
- **SSH fallback**: Traditional SSH connections for existing hosts

## Installation

### Download Pre-built

1. Download `OS1.app.zip` from the GitHub releases page
2. Unzip and move `OS1.app` to `/Applications`
3. Right-click → Open (first launch only to bypass macOS Gatekeeper)

### Build from Source

```sh
git clone https://github.com/nickvasilescu/hermes-desktop-os1.git
cd hermes-desktop-os1
./scripts/build-macos-app.sh
```

The app bundle will be at `dist/OS1.app`.

### Run Tests

```swift
swift test
```

For live integration tests against a real Orgo computer:

```sh
ORGO_LIVE_TESTS=1 \
ORGO_API_KEY="sk_live_..." \
ORGO_DEFAULT_COMPUTER_ID="<uuid>" \
swift test --filter OrgoTransportLiveTests
```

## Configuration

### Setting Up an Orgo Cloud Computer

1. **Get API Key**: Visit [orgo.ai/settings/api-keys](https://www.orgo.ai/settings/api-keys)
2. **Open Connections Tab** → Click **Add Host**
3. **Select Orgo VM** transport
4. **Paste API Key** → Click **Verify & Save**
   - Key is stored in macOS Keychain for reuse
5. **Pick Workspace** from dropdown
6. **Pick or Create Computer**:
   - Select existing computer, OR
   - Click **Create new computer…** (defaults: Linux, 8GB RAM, 4 CPU, 50GB disk)
7. **Save** connection
8. **Install Agent**: If agent isn't installed, Overview screen shows install banner
   - Click to run official Hermes Agent installer (~60-90 seconds)

### Setting Up SSH Connection

1. **Add Host** → Select **SSH** transport
2. **Enter Details**:
   - Host alias or address
   - Optional: user, port, Hermes profile
3. **Prerequisites**:
   - SSH accessible from your Mac without interactive prompts
   - `python3` on non-interactive SSH PATH
   - Hermes Agent already installed

## API and Transport Architecture

### Orgo Transport Routing

The transport intelligently routes requests:

```swift
// HTTP operations try platform proxy first
// https://www.orgo.ai/api/computers/{id}/...
// Falls back to direct VM URL on 5xx routing failures
// https://<fly_instance_id>.orgo.dev/...

// Terminal websocket connects directly
// wss://<fly_instance_id>.orgo.dev/terminal?token=<vncPassword>
```

### Key HTTP Endpoints

```
POST /bash           - Execute bash command
POST /exec           - Execute arbitrary command
GET  /files          - List files
PUT  /files          - Write file
GET  /sessions       - List agent sessions
GET  /tasks          - Get kanban tasks
GET  /skills         - List available skills
GET  /cron           - List cron jobs
```

### Connection Configuration Example

```swift
// Orgo connection persists API key in Keychain
// Access pattern in Swift:
import Security

func saveOrgoAPIKey(_ key: String) {
    let query: [String: Any] = [
        kSecClass as String: kSecClassGenericPassword,
        kSecAttrService as String: "com.elementsoftware.os1.orgo",
        kSecAttrAccount as String: "api-key",
        kSecValueData as String: key.data(using: .utf8)!
    ]
    SecItemAdd(query as CFDictionary, nil)
}
```

## Voice Mode Configuration

OS1 includes WebRTC voice mode using OpenAI Realtime API.

### Setting Up Voice Mode

1. **Configure OpenAI Key**:
   - Open **Providers** tab → Save OpenAI API key to Keychain, OR
   - Set environment variable for runtime

2. **Environment Variables**:

```sh
# Required: OpenAI API key
OPENAI_API_KEY="sk-..."

# Optional: Orgo MCP configuration
OS1_ORGO_MCP_JS_PATH="/absolute/path/to/dist/index.js"
OS1_ORGO_MCP_PACKAGE="@orgo-ai/mcp"
OS1_REALTIME_ORGO_TOOLSETS="core,screen,files"
OS1_REALTIME_ORGO_DISABLED_TOOLS="orgo_upload_file"
OS1_REALTIME_ORGO_READ_ONLY="true"
```

3. **Running with Voice Mode**:

```sh
# From source
OPENAI_API_KEY="sk-..." swift run OS1

# Packaged app
./scripts/build-macos-app.sh
OPENAI_API_KEY="sk-..." ./dist/OS1.app/Contents/MacOS/OS1
```

### Voice Mode Architecture

The voice system:
- Starts a loopback WebRTC session endpoint after boot animation
- Sends SDP to `POST /session` endpoint
- Swift backend forwards to `https://api.openai.com/v1/realtime/calls`
- Exposes Orgo MCP tools to the voice model as Realtime function tools
- Runs local MCP server (`npx -y @orgo-ai/mcp`)
- Forwards tool calls between model and Orgo

### Orgo Toolsets

Default toolsets: `core,screen,files`

Opt-in toolsets (use with caution): `shell,admin`

```sh
# Enable shell and admin toolsets (WARNING: gives voice model system access)
OS1_REALTIME_ORGO_TOOLSETS="core,screen,files,shell,admin"
```

## Building and Packaging

### Basic Build

```sh
./scripts/build-macos-app.sh
```

Creates universal binary (Apple Silicon + Intel) at `dist/OS1.app`.

### Code Signing

The default build is ad-hoc signed with designated requirement for `com.elementsoftware.os1`.

**Custom Signing Identity**:

```sh
# Use specific identity
OS1_CODESIGN_IDENTITY="Developer ID Application: Your Name (TEAM123)" \
./scripts/build-macos-app.sh

# Or use first available Apple Development identity
OS1_AUTO_CODESIGN=1 ./scripts/build-macos-app.sh
```

### Environment Variables for Build

```sh
# Legacy name (also supported)
HERMES_CODESIGN_IDENTITY="Developer ID Application: Your Name"

# Custom identity
OS1_CODESIGN_IDENTITY="Developer ID Application: Your Name"

# Auto-select first Apple Development cert
OS1_AUTO_CODESIGN=1
```

## Common Usage Patterns

### Installing Agent on Fresh VM

```swift
// After connecting to a VM without agent
// 1. Overview screen detects missing agent
// 2. Shows "Install Hermes Agent" button
// 3. Installation handles:
//    - VM clock drift synchronization
//    - System git installation
//    - Stale apt lock cleanup
//    - Hermes agent installation (~60-90s)
```

### Working with Sessions

Sessions are AI agent task sessions stored on the VM.

```swift
// Sessions view provides:
// - Full-text search across all sessions
// - Session browser with metadata
// - Direct navigation to session details
// - Export/archive capabilities
```

### Managing Files

```swift
// File editor includes:
// - Syntax highlighting
// - Conflict detection (checks mtime before save)
// - Profile-aware path resolution
// - Direct VM filesystem access via HTTP API
```

### Using the Terminal

```swift
// Terminal features:
// - Real-time websocket connection
// - Full TTY resize support
// - Output reflow on window resize
// - History persistence
// - Direct byte streaming (no SSH overhead)
```

## Troubleshooting

### Connection Issues

**Problem**: Can't connect to Orgo VM

```
Solutions:
1. Verify API key at orgo.ai/settings/api-keys
2. Check workspace has active computers
3. Ensure computer is running (not stopped/suspended)
4. Check Connections tab shows green status indicator
```

**Problem**: 5xx errors from platform proxy

```
Behavior: Transport automatically falls back to direct VM URL
Check: Look for fallback message in logs
Note: Long-running ops (installer) skip proxy to avoid 30s timeout
```

### Agent Installation Failures

**Problem**: Install hangs or times out

```
Common causes:
- VM clock drift (installer syncs automatically)
- Missing system git (installer apt-gets it)
- Stale apt locks (installer cleans them)

Solution: Let installer run full course (~90s)
Manual check: Use terminal tab to inspect /tmp/hermes-install.log
```

### SSH Connection Problems

**Problem**: SSH connection fails

```
Checklist:
- Can you `ssh user@host` from terminal without password prompt?
- Is python3 in non-interactive PATH? (ssh user@host 'which python3')
- Is Hermes already installed on remote host?
- Does ~/.ssh/config have correct settings for host?
```

### Voice Mode Issues

**Problem**: Microphone not accessible

```
1. Check System Settings → Privacy & Security → Microphone
2. Grant OS1.app microphone access
3. Restart app after granting permission
```

**Problem**: Voice mode not starting

```
Check:
1. OPENAI_API_KEY is set (env or Providers tab)
2. No firewall blocking WebRTC
3. Console.app for OS1 logs
4. Look for "oai-events data channel ready" in logs
```

**Problem**: MCP tools not available in voice

```
Check:
1. ORGO_API_KEY is set or saved in OS1
2. ORGO_DEFAULT_COMPUTER_ID matches active connection
3. OS1_REALTIME_ORGO_TOOLSETS includes desired toolsets
4. MCP server can start: npx -y @orgo-ai/mcp --version
```

## Development Workflow

### Local Development Loop

```sh
# 1. Make code changes

# 2. Run tests
swift test

# 3. Run from source
swift run OS1

# 4. Build and test packaged app
./scripts/build-macos-app.sh
open dist/OS1.app
```

### Debugging Transport Layer

```swift
// Enable verbose logging in OrgoTransport.swift
print("[OrgoTransport] Attempting proxy: \(proxyURL)")
print("[OrgoTransport] Fallback to direct: \(directURL)")

// Check websocket handshake
print("[Terminal] WebSocket connecting to: \(wsURL)")
print("[Terminal] WebSocket state: \(webSocket.readyState)")
```

### Testing Against Live Orgo

```sh
# Get computer ID from Orgo dashboard or API
ORGO_DEFAULT_COMPUTER_ID=$(curl -H "Authorization: Bearer $ORGO_API_KEY" \
  https://www.orgo.ai/api/computers | jq -r '.[0].id')

# Run live tests
ORGO_LIVE_TESTS=1 \
ORGO_API_KEY="sk_live_..." \
ORGO_DEFAULT_COMPUTER_ID="$ORGO_DEFAULT_COMPUTER_ID" \
swift test --filter OrgoTransportLiveTests
```

## Real Code Examples

### Creating a Connection Programmatically

```swift
import Foundation

struct OrgoConnection {
    let apiKey: String
    let workspaceId: String
    let computerId: String
    
    func saveToKeychain() {
        let query: [String: Any] = [
            kSecClass as String: kSecClassGenericPassword,
            kSecAttrService as String: "com.elementsoftware.os1.orgo",
            kSecAttrAccount as String: "api-key",
            kSecValueData as String: apiKey.data(using: .utf8)!,
            kSecAttrAccessible as String: kSecAttrAccessibleAfterFirstUnlock
        ]
        
        SecItemDelete(query as CFDictionary) // Remove old
        SecItemAdd(query as CFDictionary, nil)
    }
}

// Usage
let connection = OrgoConnection(
    apiKey: ProcessInfo.processInfo.environment["ORGO_API_KEY"] ?? "",
    workspaceId: "workspace-uuid",
    computerId: "computer-uuid"
)
connection.saveToKeychain()
```

### Executing Commands on VM

```swift
import Foundation

func executeBashCommand(
    computerId: String,
    command: String,
    apiKey: String
) async throws -> String {
    let url = URL(string: "https://www.orgo.ai/api/computers/\(computerId)/bash")!
    var request = URLRequest(url: url)
    request.httpMethod = "POST"
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    request.setValue("application/json", forHTTPHeaderField: "Content-Type")
    
    let body = ["command": command]
    request.httpBody = try JSONSerialization.data(withJSONObject: body)
    
    let (data, _) = try await URLSession.shared.data(for: request)
    
    struct Response: Codable {
        let stdout: String
        let stderr: String
        let exitCode: Int
    }
    
    let response = try JSONDecoder().decode(Response.self, from: data)
    return response.stdout
}

// Usage
Task {
    let output = try await executeBashCommand(
        computerId: "abc-123",
        command: "ls -la /home/agent",
        apiKey: ProcessInfo.processInfo.environment["ORGO_API_KEY"]!
    )
    print(output)
}
```

### Reading Sessions from Agent

```swift
import Foundation

struct HermesSession: Codable {
    let id: String
    let title: String
    let createdAt: String
    let messages: [Message]
    
    struct Message: Codable {
        let role: String
        let content: String
        let timestamp: String
    }
}

func fetchSessions(
    computerId: String,
    apiKey: String
) async throws -> [HermesSession] {
    let url = URL(string: "https://www.orgo.ai/api/computers/\(computerId)/sessions")!
    var request = URLRequest(url: url)
    request.setValue("Bearer \(apiKey)", forHTTPHeaderField: "Authorization")
    
    let (data, _) = try await URLSession.shared.data(for: request)
    return try JSONDecoder().decode([HermesSession].self, from: data)
}

// Usage with search
Task {
    let sessions = try await fetchSessions(
        computerId: "abc-123",
        apiKey: ProcessInfo.processInfo.environment["ORGO_API_KEY"]!
    )
    
    // Full-text search
    let searchTerm = "deployment"
    let matching = sessions.filter { session in
        session.messages.contains { message in
            message.content.localizedCaseInsensitiveContains(searchTerm)
        }
    }
    
    print("Found \(matching.count) sessions mentioning '\(searchTerm)'")
}
```

## Requirements

- **macOS 14+** (Sonoma or newer)
- **Universal Binary**: Apple Silicon or Intel
- **Orgo Account**: For cloud computer features (get API key at orgo.ai)
- **OR SSH Access**: For traditional SSH connections

## Architecture Notes

- **Swift + SwiftUI**: Native macOS app, no Electron
- **Keychain Integration**: Secure credential storage
- **WebSocket Terminal**: Direct VM connection via SwiftTerm
- **HTTP API Client**: First-class Orgo platform integration
- **MCP Integration**: Voice mode exposes Orgo tools to OpenAI Realtime
- **Localization Ready**: English, Simplified Chinese, Russian scaffolding

## Project Links

- **GitHub**: https://github.com/nickvasilescu/hermes-desktop-os1
- **Upstream**: https://github.com/dodo-reach/hermes-desktop (SSH-first original)
- **Orgo Platform**: https://www.orgo.ai
- **Design System**: https://github.com/nickvasilescu/OS-1 (Element Software theme)
- **License**: MIT
