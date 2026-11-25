---
name: hermes-swift-mac-app
description: Build and configure the native macOS desktop app wrapper for Hermes Web UI with Swift and WKWebView
triggers:
  - how do I install the Hermes macOS app
  - set up Hermes Agent on my Mac
  - connect Hermes Swift app to remote server
  - configure SSH tunnel for Hermes macOS
  - build Hermes Agent from source
  - troubleshoot Hermes Mac app connection
  - customize Hermes Swift wrapper settings
  - release new version of Hermes macOS app
---

# Hermes Swift Mac App Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection

## Overview

Hermes Agent is a native macOS desktop wrapper for [Hermes Web UI](https://github.com/nesquena/hermes-webui). Built with Swift and WKWebView, it provides a standalone Mac app experience with no Electron or heavy dependencies. The app supports both local Hermes instances and remote servers via SSH tunneling.

**Key features:**
- Native macOS app using WKWebView (requires macOS 12+)
- Direct connection mode for local Hermes Web UI
- SSH tunnel mode for remote servers
- Clipboard integration (text and images)
- System notifications for AI responses
- Auto-update via Sparkle framework
- Signed and notarized for Gatekeeper

## Installation

### For End Users

Download the latest DMG from releases:

```bash
# Visit https://github.com/hermes-webui/hermes-swift-mac/releases
# Download Hermes-Agent-vX.X.X.dmg
# Open DMG and drag to Applications folder
```

### For Developers - Build from Source

```bash
# Install Xcode Command Line Tools if needed
xcode-select --install

# Clone and build
git clone https://github.com/hermes-webui/hermes-swift-mac.git
cd hermes-swift-mac
./build.sh
```

The `build.sh` script:
1. Compiles the Swift code via `swift build -c release`
2. Creates the `.app` bundle structure
3. Converts `icon.png` to `AppIcon.icns`
4. Copies binaries and resources
5. Installs to `/Applications/Hermes Agent.app`

## Project Structure

```
Sources/HermesAgent/
├── main.swift                        # Entry point, signal handling
├── AppDelegate.swift                 # App lifecycle, menu bar, Sparkle updater
├── BrowserWindowController.swift     # WKWebView window, clipboard, notifications
├── TunnelManager.swift               # SSH tunnel management
├── PreferencesWindowController.swift # Settings UI
└── SplashWindowController.swift      # Launch splash screen

Package.swift                         # SPM manifest
build.sh                              # Build and install script
scripts/release.sh                    # Release automation
```

## Configuration Modes

### Direct Mode (Local Hermes)

For Hermes Web UI running on the same Mac:

**Default settings:**
- Target URL: `http://localhost:8787`
- Connection Mode: Direct

```swift
// In PreferencesWindowController.swift
// Default URL stored in UserDefaults
UserDefaults.standard.string(forKey: "targetURL") ?? "http://localhost:8787"
```

### SSH Tunnel Mode (Remote Hermes)

For Hermes Web UI on a remote server:

**Required settings:**
- Connection Mode: SSH Tunnel
- Username: SSH user on remote server
- Host: Server hostname or IP
- Local Port: Port on Mac (default 8787)
- Remote Port: Port where Hermes runs on server (default 8787)

**SSH requirements:**
- Key-based authentication must work (`ssh user@host` without password)
- `~/.ssh/known_hosts` file accessible
- No password authentication support

```swift
// TunnelManager.swift constructs SSH command:
ssh -o StrictHostKeyChecking=accept-new \
    -o ExitOnForwardFailure=yes \
    -N -L \(localPort):localhost:\(remotePort) \
    \(username)@\(host)
```

## Code Examples

### Reading User Preferences

```swift
// From PreferencesWindowController.swift
let defaults = UserDefaults.standard

// Get connection mode
let mode = defaults.string(forKey: "connectionMode") ?? "direct"

// Get target URL
let targetURL = defaults.string(forKey: "targetURL") ?? "http://localhost:8787"

// Get SSH settings (tunnel mode)
let sshUsername = defaults.string(forKey: "sshUsername") ?? ""
let sshHost = defaults.string(forKey: "sshHost") ?? ""
let localPort = defaults.integer(forKey: "localPort")
let remotePort = defaults.integer(forKey: "remotePort")
```

### Starting SSH Tunnel

```swift
// From TunnelManager.swift
class TunnelManager {
    private var sshProcess: Process?
    
    func startTunnel(username: String, host: String, 
                     localPort: Int, remotePort: Int) {
        let process = Process()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/ssh")
        process.arguments = [
            "-o", "StrictHostKeyChecking=accept-new",
            "-o", "ExitOnForwardFailure=yes",
            "-N",
            "-L", "\(localPort):localhost:\(remotePort)",
            "\(username)@\(host)"
        ]
        
        try? process.run()
        self.sshProcess = process
        
        // Monitor tunnel health
        monitorTunnel()
    }
    
    func stopTunnel() {
        sshProcess?.terminate()
        sshProcess = nil
    }
}
```

### Testing Connection

```swift
// From PreferencesWindowController.swift
func testConnection(url: String, completion: @escaping (Bool) -> Void) {
    guard let testURL = URL(string: url) else {
        completion(false)
        return
    }
    
    var request = URLRequest(url: testURL)
    request.timeoutInterval = 5.0
    
    URLSession.shared.dataTask(with: request) { data, response, error in
        DispatchQueue.main.async {
            if let httpResponse = response as? HTTPURLResponse,
               httpResponse.statusCode == 200 {
                completion(true)
            } else {
                completion(false)
            }
        }
    }.resume()
}
```

### Clipboard Integration

```swift
// From BrowserWindowController.swift
// Paste handler for text and images
@objc func handlePaste(_ sender: Any?) {
    let pasteboard = NSPasteboard.general
    
    if let image = pasteboard.readObjects(forClasses: [NSImage.self])?.first as? NSImage,
       let data = image.tiffRepresentation,
       let bitmap = NSBitmapImageRep(data: data),
       let pngData = bitmap.representation(using: .png, properties: [:]) {
        let base64 = pngData.base64EncodedString()
        let js = "window.pasteImage('data:image/png;base64,\(base64)');"
        webView.evaluateJavaScript(js)
    } else if let string = pasteboard.string(forType: .string) {
        let js = "window.pasteText(\(jsonEscape(string)));"
        webView.evaluateJavaScript(js)
    }
}
```

### System Notifications

```swift
// From BrowserWindowController.swift
// Show notification when AI response completes
func showNotification(title: String, body: String) {
    let content = UNMutableNotificationContent()
    content.title = title
    content.body = body
    content.sound = .default
    
    let request = UNNotificationRequest(
        identifier: UUID().uuidString,
        content: content,
        trigger: nil
    )
    
    UNUserNotificationCenter.current().add(request)
}
```

### Auto-Update with Sparkle

```swift
// From AppDelegate.swift
import Sparkle

class AppDelegate: NSObject, NSApplicationDelegate {
    private var updaterController: SPUStandardUpdaterController?
    
    func applicationDidFinishLaunching(_ notification: Notification) {
        // Initialize Sparkle updater
        updaterController = SPUStandardUpdaterController(
            startingUpdater: true,
            updaterDelegate: nil,
            userDriverDelegate: nil
        )
        
        // Check for updates on launch
        updaterController?.updater.checkForUpdatesInBackground()
    }
    
    @objc func checkForUpdates(_ sender: Any?) {
        updaterController?.updater.checkForUpdates()
    }
}
```

## Building and Running

### Development Build

```bash
# Build in debug mode
swift build

# Run directly
swift run

# Run tests
swift test
```

### Release Build

```bash
# Build release binary
swift build -c release

# Or use build script (compiles + installs)
./build.sh
```

The build script handles:
- Release compilation
- App bundle creation at `HermesAgent.app/`
- Icon conversion (PNG → ICNS)
- Binary signing (if configured)
- Installation to `/Applications/`

### Icon Generation

```bash
# Convert PNG to ICNS (done by build.sh)
sips -s format icns icon.png --out AppIcon.icns

# Or manually with iconutil
mkdir icon.iconset
sips -z 16 16     icon.png --out icon.iconset/icon_16x16.png
sips -z 32 32     icon.png --out icon.iconset/icon_16x16@2x.png
sips -z 32 32     icon.png --out icon.iconset/icon_32x32.png
sips -z 64 64     icon.png --out icon.iconset/icon_32x32@2x.png
sips -z 128 128   icon.png --out icon.iconset/icon_128x128.png
sips -z 256 256   icon.png --out icon.iconset/icon_128x128@2x.png
sips -z 256 256   icon.png --out icon.iconset/icon_256x256.png
sips -z 512 512   icon.png --out icon.iconset/icon_256x256@2x.png
sips -z 512 512   icon.png --out icon.iconset/icon_512x512.png
sips -z 1024 1024 icon.png --out icon.iconset/icon_512x512@2x.png
iconutil -c icns icon.iconset
```

## Releasing

### Create a Release

```bash
# Use release script (pushes main, then tag separately)
scripts/release.sh v1.0.9
```

**Why separate pushes?** GitHub sometimes drops workflow triggers when commit and tag are pushed together. The script:
1. Pushes `main` branch
2. Waits briefly
3. Pushes the tag separately

This ensures the GitHub Actions workflow fires reliably.

### Manual Release Process

```bash
# Tag the release
git tag v1.0.9
git push origin main
git push origin v1.0.9

# If workflow doesn't trigger, run manually:
# Actions → Build and Release macOS App → Run workflow → enter tag
```

### GitHub Actions Workflow

The `.github/workflows/build-release.yml` (not shown in README but typical) would:
1. Build the app on `macos-latest`
2. Sign with Developer ID certificate (from secrets)
3. Notarize with Apple (requires Apple ID credentials)
4. Create DMG with `create-dmg` or `hdiutil`
5. Upload DMG as release asset

## Common Patterns

### Checking Tunnel Status

```swift
// From TunnelManager.swift
func isTunnelRunning() -> Bool {
    guard let process = sshProcess else { return false }
    return process.isRunning
}

func monitorTunnel() {
    // Check if local port is accessible
    let socket = CFSocketCreate(kCFAllocatorDefault, 
                                PF_INET, 
                                SOCK_STREAM, 
                                IPPROTO_TCP, 
                                0, nil, nil)
    // ... probe localhost:localPort
}
```

### Handling WebView Navigation

```swift
// From BrowserWindowController.swift
extension BrowserWindowController: WKNavigationDelegate {
    func webView(_ webView: WKWebView, 
                 decidePolicyFor navigationAction: WKNavigationAction,
                 decisionHandler: @escaping (WKNavigationActionPolicy) -> Void) {
        
        // Open external links in Safari
        if let url = navigationAction.request.url,
           navigationAction.navigationType == .linkActivated {
            NSWorkspace.shared.open(url)
            decisionHandler(.cancel)
            return
        }
        
        decisionHandler(.allow)
    }
}
```

### Global Keyboard Shortcut

```swift
// From AppDelegate.swift
func applicationDidFinishLaunching(_ notification: Notification) {
    // Register ⌘⇧H to bring app forward
    NSEvent.addGlobalMonitorForEvents(matching: .keyDown) { event in
        if event.modifierFlags.contains([.command, .shift]),
           event.charactersIgnoringModifiers == "h" {
            NSApp.activate(ignoringOtherApps: true)
        }
    }
}
```

## Troubleshooting

### Connection Error on Launch

**Symptom:** Blank page or "Unable to connect" error

**Solutions:**
1. Ensure Hermes Web UI is running:
   ```bash
   cd ~/hermes-webui-public
   bash start.sh
   ```
2. Check Target URL in Preferences (⌘,)
3. Use Test Connection button to verify
4. Check Console.app for errors from "Hermes Agent"

### SSH Tunnel Fails Immediately

**Symptom:** Status shows "Disconnected" right after connecting

**Solutions:**
1. Test SSH key auth works:
   ```bash
   ssh user@your-server
   # Should connect without password
   ```
2. Set up SSH keys if needed:
   ```bash
   ssh-keygen -t ed25519
   ssh-copy-id user@your-server
   ```
3. Verify remote port is correct (where Hermes actually runs)
4. Check `~/.ssh/known_hosts` isn't corrupted

### Voice Input Not Working

**Symptom:** Microphone button doesn't respond

**Solutions:**
1. Grant microphone permission:
   - System Settings → Privacy & Security → Microphone
   - Enable "Hermes Agent"
2. Restart app after granting permission
3. Check Info.plist includes `NSMicrophoneUsageDescription`

### Gatekeeper Blocks App

**Symptom:** "App can't be opened because it is from an unidentified developer"

**Solutions:**
1. Download latest release (v1.0.4+) — these are signed and notarized
2. If building from source without signing:
   ```bash
   xattr -cr /Applications/Hermes\ Agent.app
   ```
3. Right-click app → Open (first time only)

### Blurry App Icon

**Symptom:** Icon looks pixelated in Dock after building

**Solution:**
```bash
# Refresh icon cache
killall Dock
```

### Port Already in Use

**Symptom:** "Port forwarding failed" when starting tunnel

**Solutions:**
```bash
# Find what's using the port
lsof -i :8787

# Kill the process or change Local Port in Preferences
```

## Environment Variables

The app doesn't use environment variables directly, but for development:

```bash
# Enable WebKit debug logging
export WEBKIT_DEBUG=1

# Sparkle update feed (set in Info.plist normally)
export SPARKLE_APPCAST_URL=https://example.com/appcast.xml
```

## Testing

```bash
# Run all tests
swift test

# Run specific test
swift test --filter TunnelManagerTests

# Run with verbose output
swift test --verbose
```

### Example Test

```swift
// From Tests/HermesAgentTests/TunnelManagerTests.swift
import XCTest
@testable import HermesAgent

final class TunnelManagerTests: XCTestCase {
    func testTunnelCreation() {
        let manager = TunnelManager()
        XCTAssertFalse(manager.isTunnelRunning())
        
        manager.startTunnel(
            username: "test",
            host: "localhost",
            localPort: 8787,
            remotePort: 8787
        )
        
        // Wait briefly for process to start
        sleep(1)
        XCTAssertTrue(manager.isTunnelRunning())
        
        manager.stopTunnel()
        XCTAssertFalse(manager.isTunnelRunning())
    }
}
```

## Dependencies

Managed via Swift Package Manager in `Package.swift`:

```swift
// Package.swift
dependencies: [
    .package(url: "https://github.com/sparkle-project/Sparkle", from: "2.3.0")
],
targets: [
    .executableTarget(
        name: "HermesAgent",
        dependencies: [
            .product(name: "Sparkle", package: "Sparkle")
        ]
    )
]
```

**Runtime dependencies:**
- macOS 12 (Monterey) or later
- Xcode Command Line Tools (for building)
- SSH (provided by macOS)

**No external dependencies** for users — fully self-contained app.
