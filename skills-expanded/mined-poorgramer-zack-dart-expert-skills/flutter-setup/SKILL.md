---
name: "flutter-setup"
description: "Complete Flutter SDK installation, IDE configuration, and troubleshooting guide for Linux, macOS, and Windows. Use for installing Flutter SDK from scratch, configuring PATH environment variables across platforms, setting up VS Code/Android Studio/IntelliJ IDEA with Flutter plugins, resolving 'flutter command not found' errors, fixing flutter doctor warnings and errors, troubleshooting Android SDK/NDK installation issues, configuring Xcode and CocoaPods on macOS, installing Visual Studio C++ build tools on Windows, resolving PATH conflicts and SDK path issues, fixing network/proxy setup problems, debugging IDE plugin activation, configuring emulators and simulators, handling platform-specific build errors, resolving dependency conflicts, fixing certificate and signing issues, troubleshooting hot reload failures, and verifying successful installation with flutter doctor diagnostics."
metadata:
  last_modified: "2026-04-01 14:35:00 (GMT+8)"
---
# Flutter Environment Setup & Troubleshooting Guide

## Goal
Establish a reliable, optimized Flutter development environment across Linux, macOS, and Windows platforms. This guide covers initial SDK installation, PATH configuration, IDE setup, and comprehensive troubleshooting for common setup issues, dependency conflicts, and tooling misconfigurations.

## Prerequisites Checklist
Before starting Flutter installation, verify:
- **Disk Space**: Minimum 2.8 GB for SDK, plus additional space for IDEs and Android SDK
- **Network Access**: Stable internet connection for downloading SDK and dependencies
- **Administrative Access**: Ability to modify system PATH and install software
- **Git Installed**: Required for Flutter SDK management and updates

---

## 🚀 Installation Process

### Step 1: Download and Extract Flutter SDK
1. Download the latest stable Flutter SDK from flutter.dev for your platform
2. Extract to a permanent location (avoid temporary directories)
3. **Important**: Choose paths without spaces or special characters

**Recommended Installation Paths:**
- **Linux/macOS**: `~/development/flutter` or `/opt/flutter`
- **Windows**: `C:\develop\flutter` (NEVER use `C:\Program Files\`)

### Step 2: Configure PATH Environment Variable

#### Linux/macOS PATH Configuration
Add Flutter to your shell configuration file:

**For Bash** (`~/.bashrc` or `~/.bash_profile`):
```bash
export PATH="$PATH:$HOME/development/flutter/bin"
export PATH="$PATH:$HOME/development/flutter/.pub-cache/bin"
```

**For Zsh** (`~/.zshrc`):
```zsh
export PATH="$PATH:$HOME/development/flutter/bin"
export PATH="$PATH:$HOME/development/flutter/.pub-cache/bin"
```

**For Fish** (`~/.config/fish/config.fish`):
```fish
set -gx PATH $PATH $HOME/development/flutter/bin
set -gx PATH $PATH $HOME/development/flutter/.pub-cache/bin
```

**Apply changes immediately:**
```bash
source ~/.bashrc  # or ~/.zshrc or ~/.bash_profile
```

#### Windows PATH Configuration

**Method 1: PowerShell (Recommended)**
```powershell
$flutterPath = "C:\develop\flutter\bin"
$currentPath = [Environment]::GetEnvironmentVariable("Path", [EnvironmentVariableTarget]::User)
if ($currentPath -notmatch [regex]::Escape($flutterPath)) {
    [Environment]::SetEnvironmentVariable("Path", "$currentPath;$flutterPath", [EnvironmentVariableTarget]::User)
}
```

**Method 2: GUI**
1. Open System Properties → Advanced → Environment Variables
2. Under "User variables", select `Path` → Edit
3. Click "New" and add `C:\develop\flutter\bin`
4. Click OK and restart terminal

**Important**: Close and reopen all terminal windows after PATH changes.

### Step 3: Verify Installation
Run the Flutter doctor command to check installation status:
```bash
flutter doctor -v
```

This command checks for:
- Flutter SDK installation
- Android toolchain (Android SDK, NDK, Platform Tools)
- Chrome (for web development)
- Visual Studio / Xcode (platform-specific)
- Connected devices
- IDE plugins

---

## 🔧 Understanding Flutter Doctor Output

### Doctor Check Categories

**[✓] Flutter** - SDK properly installed and in PATH
**[✓] Android toolchain** - Android SDK, licenses, build tools configured
**[✓] Chrome** - Web development support available
**[✓] Visual Studio** (Windows) - C++ build tools for desktop apps
**[✓] Xcode** (macOS) - iOS/macOS development tools
**[✓] Android Studio** - IDE and Android SDK integration
**[✓] VS Code** - Lightweight IDE with Flutter extension
**[✓] Connected device** - Physical device or emulator detected

**[!]** Warning - Optional component missing or needs attention
**[✗]** Error - Critical component missing or misconfigured

---

## 💻 IDE Setup Best Practices

### Visual Studio Code Setup
1. Install VS Code from code.visualstudio.com
2. Install Flutter extension: `Ctrl+P` → `ext install Dart-Code.flutter`
3. Install Dart extension (auto-installed with Flutter)
4. Restart VS Code

**Recommended VS Code Settings:**
```json
{
  "dart.flutterSdkPath": "C:\\develop\\flutter",
  "dart.debugExternalPackageLibraries": true,
  "dart.debugSdkLibraries": false,
  "[dart]": {
    "editor.formatOnSave": true,
    "editor.selectionHighlight": false,
    "editor.suggest.snippetsPreventQuickSuggestions": false,
    "editor.suggestSelection": "first",
    "editor.tabCompletion": "onlySnippets",
    "editor.wordBasedSuggestions": false
  }
}
```

### Android Studio Setup
1. Download and install Android Studio
2. Open Plugins: `File → Settings → Plugins` (Windows/Linux) or `Android Studio → Preferences → Plugins` (macOS)
3. Search for "Flutter" and install
4. Search for "Dart" and install
5. Restart Android Studio
6. Configure Android SDK: `Tools → SDK Manager`
   - Install latest Android SDK Platform
   - Install Android SDK Command-line Tools
   - Install Android SDK Build-Tools
   - Install Android Emulator

### IntelliJ IDEA Setup
1. Open Plugins: `File → Settings → Plugins`
2. Install Flutter plugin (includes Dart)
3. Restart IntelliJ IDEA
4. Configure Flutter SDK path: `File → Settings → Languages & Frameworks → Flutter`

---

## 🛠️ Common Issues & Troubleshooting

### Issue 1: "flutter: command not found"
**Cause**: Flutter bin directory not in system PATH

**Solutions:**
1. Verify Flutter installation path exists
2. Re-add to PATH using platform-specific instructions above
3. Restart terminal/IDE completely
4. Check PATH with: `echo $PATH` (Linux/macOS) or `echo $env:Path` (PowerShell)
5. Ensure no typos in path (check forward/backward slashes)

### Issue 2: "cmdline-tools component is missing"
**Cause**: Android SDK Command-line Tools not installed

**Solution:**
1. Open Android Studio
2. Navigate to `Tools → SDK Manager → SDK Tools`
3. Check "Android SDK Command-line Tools (latest)"
4. Click "Apply" and wait for installation
5. Run `flutter doctor --android-licenses` and accept all

### Issue 3: Android License Status Unknown
**Cause**: Android SDK licenses not accepted

**Solution:**
```bash
flutter doctor --android-licenses
```
Press `y` to accept each license. If this fails:
1. Ensure Android SDK Command-line Tools installed
2. Set ANDROID_HOME environment variable:
   - **Linux/macOS**: `export ANDROID_HOME=$HOME/Android/Sdk`
   - **Windows**: `setx ANDROID_HOME "C:\Users\%USERNAME%\AppData\Local\Android\Sdk"`
3. Retry license acceptance

### Issue 4: Visual Studio Not Found (Windows)
**Cause**: Visual Studio not installed or missing C++ workload

**Solution:**
1. Install Visual Studio 2022 (Community edition works)
2. During installation, select "Desktop development with C++"
3. Include these individual components:
   - MSVC v142+ build tools
   - Windows 10/11 SDK
   - C++ CMake tools
4. Run `flutter doctor` to verify

### Issue 5: Xcode Not Configured (macOS)
**Cause**: Xcode not installed or command-line tools not configured

**Solution:**
```bash
# Install Xcode from Mac App Store, then:
sudo xcode-select --switch /Applications/Xcode.app/Contents/Developer
sudo xcodebuild -runFirstLaunch
sudo xcodebuild -license accept
```

### Issue 6: CocoaPods Not Installed (macOS)
**Cause**: CocoaPods required for iOS plugin dependencies

**Solution:**
```bash
sudo gem install cocoapods
pod setup
```

If gem installation fails, use Homebrew:
```bash
brew install cocoapods
```

### Issue 7: "Unable to find git in your PATH"
**Cause**: Git not installed or not in PATH

**Solution:**
- **Linux**: `sudo apt-get install git`
- **macOS**: `brew install git` or install Xcode Command Line Tools
- **Windows**: Download from git-scm.com and ensure "Git from command line" option selected

### Issue 8: Network/Proxy Issues
**Cause**: Corporate proxy or firewall blocking Flutter downloads

**Solution:**
Configure Flutter to use proxy:
```bash
export HTTP_PROXY=http://proxy.company.com:8080
export HTTPS_PROXY=http://proxy.company.com:8080
export NO_PROXY=localhost,127.0.0.1

flutter config --no-analytics  # Disable analytics if blocked
```

For persistent configuration, add to shell profile.

### Issue 9: Multiple Flutter Versions Conflict
**Cause**: Multiple Flutter installations or conflicting PATH entries

**Solution:**
1. Check which Flutter is active: `which flutter` (Linux/macOS) or `where flutter` (Windows)
2. Remove duplicate PATH entries
3. Uninstall unused Flutter installations
4. Clear Flutter cache: `flutter clean` in project directories

### Issue 10: IDE Plugin Not Detecting Flutter SDK
**Cause**: IDE cannot locate Flutter SDK

**Solution:**
1. **VS Code**: Add to settings.json:
   ```json
   {"dart.flutterSdkPath": "/path/to/flutter"}
   ```
2. **Android Studio/IntelliJ**: `Settings → Languages & Frameworks → Flutter → Flutter SDK path`
3. Verify path points to SDK root (contains `bin/`, `packages/`, etc.)

### Issue 11: Hot Reload Not Working
**Cause**: IDE not properly connected or outdated Flutter version

**Solution:**
1. Ensure app running in debug mode (not release)
2. Check IDE console for connection errors
3. Restart app with `r` in terminal or IDE restart button
4. Update Flutter: `flutter upgrade`
5. Clear build cache: `flutter clean`

### Issue 12: Build Failed - Gradle Issues (Android)
**Cause**: Gradle configuration or network issues

**Solution:**
1. Update Gradle wrapper: Edit `android/gradle/wrapper/gradle-wrapper.properties`
2. Clear Gradle cache:
   ```bash
   cd android
   ./gradlew clean
   cd ..
   flutter clean
   ```
3. Check `android/app/build.gradle` for correct `compileSdkVersion` and `minSdkVersion`

---

## ✅ Post-Installation Verification

After resolving all `flutter doctor` issues:

1. **Create test project:**
   ```bash
   flutter create test_app
   cd test_app
   ```

2. **Run on available device:**
   ```bash
   flutter devices  # List available devices
   flutter run      # Run on default device
   ```

3. **Test hot reload:** Make a change to `lib/main.dart` and press `r` in terminal

4. **Build release version:**
   ```bash
   flutter build apk        # Android
   flutter build ios        # iOS (macOS only)
   flutter build windows    # Windows desktop
   flutter build macos      # macOS desktop
   flutter build linux      # Linux desktop
   ```

---

## 📚 Platform-Specific Configuration Guides

For detailed platform-specific setup instructions:

- [🐧 Linux Development Setup](./references/environment-setup-linux.md)
- [🍎 macOS Development Setup](./references/environment-setup-macos.md)
- [🪟 Windows Development Setup](./references/environment-setup-windows.md)

---

## 🔍 Additional Diagnostic Commands

**Check Flutter version:**
```bash
flutter --version
```

**Update Flutter SDK:**
```bash
flutter upgrade
```

**Check Flutter channel (stable/beta/dev):**
```bash
flutter channel
```

**Switch to stable channel:**
```bash
flutter channel stable
flutter upgrade
```

**Clear Flutter cache:**
```bash
flutter clean
flutter pub cache repair
```

**Analyze project for issues:**
```bash
flutter analyze
```

**Check for dependency updates:**
```bash
flutter pub outdated
```

---

## 🎯 Success Criteria

Your Flutter environment is properly configured when:
- `flutter doctor -v` shows all green checkmarks (or acceptable warnings)
- `flutter --version` displays version information
- `flutter devices` lists at least one available device
- `flutter create test_project && cd test_project && flutter run` successfully launches app
- IDE recognizes Flutter SDK and provides code completion
- Hot reload works (press `r` during debug session)

If any issues persist after following this guide, consult platform-specific references or Flutter's official troubleshooting documentation.

## Version Requirements (verified)
- Flutter 3.44+ and Dart 3.12+ are required by the current major versions of `go_router` 18, `sign_in_with_apple` 8, `flutter_line_sdk` 3, `sentry_flutter` 10, and `serverpod` 4.
- `google_mobile_ads` 9.2 and `home_widget` 0.10 require Flutter 3.38.1+. `app_links` 7.2 requires Flutter 3.44+ (Dart 3.12+).
- Check the installed version with `flutter --version`. Local check on Flutter 3.47.9 stable: about 45 main packages resolve together and `flutter analyze` passes. Not every package in every skill was checked.
- **Android (Flutter 3.44+):** AGP 9 uses built-in Kotlin by default. Apps and plugins that still apply `kotlin-android` (KGP) must migrate, or temporarily set `android.builtInKotlin=false`. See the official `migrate-to-built-in-kotlin` guide.
- **iOS (Flutter 3.41+):** Xcode 27 requires the `UIScene` lifecycle. Unmodified `AppDelegate` projects are migrated automatically. Custom `AppDelegate` projects need the manual migration.
- **Upcoming (Flutter 3.50):** the in-framework `material` and `cupertino` libraries are deprecated. Standalone `material_ui` and `cupertino_ui` 1.x packages are available now, and `go_router` 18 already depends on them.
