---
name: openclaw-windows-companion
description: Windows companion suite for OpenClaw AI assistant - system tray app, node capabilities, WebSocket gateway client, and CLI tools
triggers:
  - how do I build the OpenClaw Windows tray app
  - set up OpenClaw Windows companion with node mode
  - connect Windows tray to OpenClaw gateway
  - enable OpenClaw node capabilities on Windows
  - troubleshoot OpenClaw Windows WebSocket connection
  - use OpenClaw CLI to test gateway
  - configure OpenClaw Windows notifications
  - debug OpenClaw tray pairing issues
---

# OpenClaw Windows Companion

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

The **OpenClaw Windows Hub** is a native Windows companion suite for [OpenClaw](https://openclaw.ai), an AI-powered personal assistant. It provides a WinUI 3 system tray app, shared gateway client library, and CLI tools for connecting Windows to your OpenClaw gateway via WebSocket.

## What It Does

- **System Tray App (Molty)**: Modern Windows 11-style tray icon with status monitoring, quick send hotkey, embedded WebView2 chat, toast notifications, and node capabilities
- **Node Mode**: Turns your Windows PC into a controllable node that the OpenClaw agent can use for system commands, screen capture, camera, canvas, speech-to-text, text-to-speech, and location
- **Shared Library**: `OpenClaw.Shared` - reusable WebSocket gateway client with message/event handling
- **CLI Validator**: `OpenClaw.Cli` - command-line tool for testing WebSocket connections, sending messages, and probing gateway APIs

## Prerequisites

- Windows 10 (20H2+) or Windows 11
- .NET 10.0 SDK: https://dotnet.microsoft.com/download/dotnet/10.0
- Windows 10 SDK (for WinUI build) - via Visual Studio or standalone
- WebView2 Runtime (pre-installed on modern Windows or download from https://developer.microsoft.com/microsoft-edge/webview2)

## Installation

### End User Installation

Download the installer for your architecture:

```powershell
# x64
Invoke-WebRequest -Uri "https://github.com/openclaw/openclaw/releases/latest/download/OpenClawCompanion-Setup-x64.exe" -OutFile "OpenClawCompanion-Setup-x64.exe"
.\OpenClawCompanion-Setup-x64.exe

# ARM64
Invoke-WebRequest -Uri "https://github.com/openclaw/openclaw/releases/latest/download/OpenClawCompanion-Setup-arm64.exe" -OutFile "OpenClawCompanion-Setup-arm64.exe"
.\OpenClawCompanion-Setup-arm64.exe
```

### Developer Build

```powershell
# Clone the repo
git clone https://github.com/openclaw/openclaw-windows-node.git
cd openclaw-windows-node

# Check prerequisites
.\build.ps1 -CheckOnly

# Build all projects
.\build.ps1

# Build specific project
.\build.ps1 -Project WinUI
```

Or build directly with dotnet:

```powershell
# Build all
dotnet build

# Build WinUI for specific architecture
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -r win-x64
dotnet build src/OpenClaw.Tray.WinUI/OpenClaw.Tray.WinUI.csproj -r win-arm64

# Build MSIX package (for camera/mic consent prompts)
dotnet build src/OpenClaw.Tray.WinUI -r win-x64 -p:PackageMsix=true
dotnet build src/OpenClaw.Tray.WinUI -r win-arm64 -p:PackageMsix=true
```

## Running the Tray App

```powershell
# Build and launch (unpackaged)
.\run-app-local.ps1

# Skip rebuild if already built
.\run-app-local.ps1 -NoBuild

# Run isolated from normal tray settings (multiple worktrees)
.\run-app-local.ps1 -Isolated

# Test alpha updates from Release build
.\run-app-local.ps1 -Configuration Release -Isolated -UpdateChannel alpha

# Launch through WinAppCLI with Package.appxmanifest
.\run-app-local.ps1 -UseWinApp -NoBuild
```

## CLI WebSocket Validator

The CLI tool validates gateway connectivity and sends test messages.

```powershell
# Show help
dotnet run --project src/OpenClaw.Cli -- --help

# Use tray settings from %APPDATA%\OpenClawTray\settings.json
dotnet run --project src/OpenClaw.Cli -- --message "test message"

# Loop sends with API probes
dotnet run --project src/OpenClaw.Cli -- --repeat 5 --delay-ms 1000 --probe-read --verbose

# Override gateway URL/token
dotnet run --project src/OpenClaw.Cli -- --url ws://127.0.0.1:18789 --token "$env:OPENCLAW_TOKEN" --message "override test"
```

## Configuration

### Gateway Connection

Settings are stored in `%APPDATA%\OpenClawTray\settings.json`:

```json
{
  "GatewayUrl": "ws://127.0.0.1:18789",
  "Token": "your-gateway-token",
  "NodeMode": true,
  "NotificationsEnabled": true,
  "AutoStart": true
}
```

### Node Mode Setup

1. **Enable Node Mode** in Settings (enabled by default)
2. **First connection** creates a pairing request
3. **Approve the device** on your OpenClaw gateway:

```bash
# List devices
openclaw devices list

# Approve your Windows device
openclaw devices approve <device-id>
```

4. **Configure allowed commands** in `~/.openclaw/openclaw.json`:

```json
{
  "gateway": {
    "nodes": {
      "allowCommands": [
        "system.notify",
        "system.run",
        "system.run.prepare",
        "system.which",
        "system.execApprovals.get",
        "system.execApprovals.set",
        "canvas.present",
        "canvas.hide",
        "canvas.navigate",
        "canvas.eval",
        "canvas.snapshot",
        "canvas.a2ui.push",
        "canvas.a2ui.pushJSONL",
        "canvas.a2ui.reset",
        "screen.snapshot",
        "screen.record",
        "camera.list",
        "camera.snap",
        "camera.clip",
        "stt.transcribe",
        "location.get",
        "device.info",
        "device.status",
        "tts.speak"
      ]
    }
  }
}
```

## Code Examples

### Using the Shared Gateway Client

```csharp
using OpenClaw.Shared;

// Create client from settings
var settingsPath = Path.Combine(
    Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData),
    "OpenClawTray",
    "settings.json"
);
var settings = await SettingsManager.LoadAsync(settingsPath);
var client = new GatewayClient(settings.GatewayUrl, settings.Token);

// Connect
await client.ConnectAsync();

// Send a message
var response = await client.SendMessageAsync(new
{
    method = "chat.send",
    @params = new
    {
        message = "Hello from Windows!"
    }
});

// Listen for events
client.OnMessage += (sender, message) =>
{
    Console.WriteLine($"Received: {message}");
};

// Disconnect
await client.DisconnectAsync();
```

### Sending System Commands from Agent

When Node Mode is enabled, the agent can control your Windows PC:

```javascript
// Show a Windows toast notification
await node.send("system.notify", {
  title: "Hello from OpenClaw",
  message: "Your task is complete!",
  sound: "Default"
});

// Execute a command (subject to execution policy)
await node.send("system.run", {
  command: "powershell",
  args: ["-Command", "Get-Process | Select-Object -First 5"]
});

// Take a screenshot
const screenshot = await node.send("screen.snapshot", {
  format: "png",
  quality: 90
});

// Capture from camera
const photo = await node.send("camera.snap", {
  deviceId: "default",
  format: "jpeg"
});

// Show a WebView2 canvas window
await node.send("canvas.present", {
  url: "https://example.com",
  width: 800,
  height: 600
});

// Text-to-speech (requires opt-in in Settings)
await node.send("tts.speak", {
  text: "Hello from OpenClaw",
  voice: "system" // or "elevenlabs" if configured
});

// Speech-to-text (requires opt-in in Settings)
const transcription = await node.send("stt.transcribe", {
  duration: 5, // seconds
  language: "en-US"
});
```

### Building a Custom Client

```csharp
using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

public class CustomGatewayClient
{
    private readonly ClientWebSocket _ws = new();
    private readonly string _url;
    private readonly string _token;

    public CustomGatewayClient(string url, string token)
    {
        _url = url;
        _token = token;
    }

    public async Task ConnectAsync()
    {
        var uri = new Uri(_url);
        _ws.Options.SetRequestHeader("Authorization", $"Bearer {_token}");
        await _ws.ConnectAsync(uri, CancellationToken.None);
    }

    public async Task<JsonDocument> SendAsync(string method, object parameters)
    {
        var message = new
        {
            jsonrpc = "2.0",
            id = Guid.NewGuid().ToString(),
            method,
            @params = parameters
        };

        var json = JsonSerializer.Serialize(message);
        var bytes = Encoding.UTF8.GetBytes(json);
        await _ws.SendAsync(
            new ArraySegment<byte>(bytes),
            WebSocketMessageType.Text,
            true,
            CancellationToken.None
        );

        var buffer = new byte[8192];
        var result = await _ws.ReceiveAsync(
            new ArraySegment<byte>(buffer),
            CancellationToken.None
        );

        var response = Encoding.UTF8.GetString(buffer, 0, result.Count);
        return JsonDocument.Parse(response);
    }
}

// Usage
var client = new CustomGatewayClient("ws://127.0.0.1:18789", Environment.GetEnvironmentVariable("OPENCLAW_TOKEN"));
await client.ConnectAsync();

var response = await client.SendAsync("chat.send", new
{
    message = "Custom client test"
});

Console.WriteLine(response.RootElement.GetProperty("result"));
```

## Common Patterns

### Quick Send Hotkey Integration

Quick Send uses `Ctrl+Alt+Shift+C` and requires `operator.write` scope:

```csharp
// Register global hotkey (WinUI)
private void RegisterHotkey()
{
    var modifiers = ModifierKeys.Control | ModifierKeys.Alt | ModifierKeys.Shift;
    var key = VirtualKey.C;
    
    HotkeyManager.Register(modifiers, key, async () =>
    {
        await ShowQuickSendDialog();
    });
}

// Send message
private async Task SendQuickMessage(string message)
{
    try
    {
        await _gatewayClient.SendMessageAsync(new
        {
            method = "chat.send",
            @params = new { message }
        });
    }
    catch (Exception ex) when (ex.Message.Contains("missing scope: operator.write"))
    {
        // Copy remediation to clipboard
        var info = $"Operator: {_clientId}\n" +
                   $"Device: {_deviceId}\n" +
                   $"Missing scope: operator.write\n\n" +
                   $"Update your token to include operator.write scope.";
        Clipboard.SetText(info);
        ShowNotification("Scope Error", "Remediation copied to clipboard");
    }
}
```

### Loading and Saving Settings

```csharp
public class SettingsManager
{
    private readonly string _settingsPath;

    public SettingsManager(string settingsPath)
    {
        _settingsPath = settingsPath;
    }

    public async Task<Settings> LoadAsync()
    {
        if (!File.Exists(_settingsPath))
        {
            return new Settings
            {
                GatewayUrl = "ws://127.0.0.1:18789",
                Token = "",
                NodeMode = true,
                NotificationsEnabled = true,
                AutoStart = false
            };
        }

        var json = await File.ReadAllTextAsync(_settingsPath);
        return JsonSerializer.Deserialize<Settings>(json);
    }

    public async Task SaveAsync(Settings settings)
    {
        var directory = Path.GetDirectoryName(_settingsPath);
        if (!Directory.Exists(directory))
        {
            Directory.CreateDirectory(directory);
        }

        var json = JsonSerializer.Serialize(settings, new JsonSerializerOptions
        {
            WriteIndented = true
        });

        await File.WriteAllTextAsync(_settingsPath, json);
    }
}

public class Settings
{
    public string GatewayUrl { get; set; }
    public string Token { get; set; }
    public bool NodeMode { get; set; }
    public bool NotificationsEnabled { get; set; }
    public bool AutoStart { get; set; }
}
```

### Handling WebSocket Events

```csharp
public class EventHandler
{
    private readonly GatewayClient _client;

    public EventHandler(GatewayClient client)
    {
        _client = client;
        _client.OnMessage += HandleMessage;
        _client.OnError += HandleError;
        _client.OnDisconnected += HandleDisconnect;
    }

    private void HandleMessage(object sender, JsonDocument message)
    {
        var root = message.RootElement;
        
        if (root.TryGetProperty("method", out var method))
        {
            // Handle notification/event
            var methodName = method.GetString();
            
            switch (methodName)
            {
                case "session.started":
                    HandleSessionStarted(root.GetProperty("params"));
                    break;
                case "usage.updated":
                    HandleUsageUpdated(root.GetProperty("params"));
                    break;
                case "notification":
                    HandleNotification(root.GetProperty("params"));
                    break;
            }
        }
        else if (root.TryGetProperty("result", out var result))
        {
            // Handle response
            var id = root.GetProperty("id").GetString();
            Console.WriteLine($"Response {id}: {result}");
        }
    }

    private void HandleError(object sender, Exception ex)
    {
        Console.WriteLine($"WebSocket error: {ex.Message}");
    }

    private void HandleDisconnect(object sender, EventArgs e)
    {
        Console.WriteLine("Disconnected from gateway");
    }
}
```

## Troubleshooting

### Quick Send Fails with "missing scope: operator.write"

This is a **token scope issue**. The token used by the tray app needs `operator.write` scope:

1. Check your token scopes on the gateway
2. Generate a new token with `operator.write` included
3. Update the token in Settings
4. Reconnect the tray app

### Quick Send Fails with "pairing required" / "NOT_PAIRED"

This is a **device approval issue**:

1. Open the tray app to trigger pairing request
2. Approve the device on your gateway:
   ```bash
   openclaw devices list
   openclaw devices approve <device-id>
   ```
3. Reconnect the tray app
4. Retry Quick Send

### WebSocket Connection Fails

```powershell
# Test connection with CLI
dotnet run --project src/OpenClaw.Cli -- --url ws://127.0.0.1:18789 --token "$env:OPENCLAW_TOKEN" --verbose

# Check gateway is running
netstat -an | Select-String "18789"

# Verify token
$env:OPENCLAW_TOKEN
```

### Node Commands Not Working

1. **Check Node Mode is enabled** in Settings
2. **Verify device is approved**:
   ```bash
   openclaw devices list
   ```
3. **Check gateway allowCommands** in `~/.openclaw/openclaw.json`
4. **Review logs** from Support & Debug menu

### Camera/Microphone Not Working

Packaged installs (MSIX) declare capabilities. Windows may ask for consent on first use:

1. Ensure you're running the packaged version (not unpackaged .exe)
2. Check Windows Settings → Privacy → Camera/Microphone
3. Grant permission to "OpenClaw Tray"

### Build Errors

```powershell
# Check prerequisites
.\build.ps1 -CheckOnly

# Clean and rebuild
dotnet clean
dotnet build

# Install missing Windows SDK
# Via Visual Studio Installer or standalone from:
# https://developer.microsoft.com/windows/downloads/windows-sdk/
```

### Tray Icon Not Appearing

1. Check if app is running in Task Manager
2. Restart Windows Explorer:
   ```powershell
   Stop-Process -Name explorer -Force
   ```
3. Check for crashes in Event Viewer (Application logs)
4. Review logs from tray Support & Debug menu

### Auto-Updates Not Working

```powershell
# Test alpha channel
.\run-app-local.ps1 -Configuration Release -Isolated -UpdateChannel alpha

# Check GitHub releases are accessible
Invoke-WebRequest -Uri "https://api.github.com/repos/openclaw/openclaw/releases/latest"
```
