---
name: follow-create-mobile-cross-with-capacitor
description: Guide to building Capacitor 8 cross-platform mobile apps with web technologies
argument-hint: "[scope]"
related:
  - use-bun-native-api
  - deep-review-codebase
  - follow-tool-vite
  - learn
  - follow-deploy
  - follow-create-mobile

---
## Goal

Build cross-platform mobile applications with Capacitor 8 using web technologies that run on iOS, Android, and PWA from a single codebase

## Scope

Use for developing and maintaining Capacitor 8 mobile apps in a monorepo, covering setup, configuration, plugins, build, deployment, and security

- Packages: `@capacitor/core`, `@capacitor/cli`, `@capacitor/android`, `@capacitor/ios` (always the same version) — always confirm the latest versions with `/deep-research` + `/follow-best-practice` (no pinning in this file — per `/update-devin-global-skills`)

## Execute

### 1. Environment Setup

> Goal: check and prepare the environment before starting development

1. Run `/deep-research` + `/follow-best-practice` to confirm the latest versions and requirements of the current Capacitor major, then run `/review-dependencies` to summarize the tech stack
2. Verify Node.js >= 22 (Capacitor 8 requirement)
3. Verify the latest Android Studio version supported by Capacitor (check with `/deep-research`)
4. Verify Xcode >= 26.0 for iOS development (Capacitor 8 requirement — the toolchain always bundles Swift)
5. Verify JDK 21 or newer
6. Set environment variables if needed: `CAPACITOR_ANDROID_STUDIO_PATH`, `CAPACITOR_COCOAPODS_PATH`
7. Run `/use-bun-native-api` for the Bun runtime and package manager
8. Run `/deep-review-codebase` for configuration files

### 2. Project Configuration

> Goal: configure `capacitor.config.ts` correctly per best practices

1. Create `capacitor.config.ts` with the `CapacitorConfig` type from `@capacitor/cli`
2. Set `appId` in reverse domain name notation (e.g. `com.company.appname`)
3. Set `appName` to a user-friendly app name
4. Point `webDir` at the compiled web assets containing `index.html`
5. Set `server.androidScheme` to `https` (default)
6. Set `server.iosScheme` to `https` or `capacitor` (default)
7. Set `server.cleartext` to `false` in production
8. Set `loggingBehavior` to `debug` for dev and `none` for production
9. Define plugin configurations in the `plugins` object keyed by plugin class name
10. Use platform-specific overrides in the `android` and `ios` properties when needed

### 3. SPA Integration

> Goal: connect the web app to the Capacitor native container correctly

1. Run `/follow-tool-vite` for SPA build configuration
2. Create a separate SPA build config (e.g. `vite.config.spa.ts`) with `ssr: false`
3. Build the SPA into the directory `webDir` points to (e.g. `dist-spa`)
4. Verify `index.html` is at the root of `webDir`
5. Use `bun --filter website build:spa` to build the SPA
6. Set the `cap:sync` script to `bun run build && cap sync`
7. Set the `cap:copy` script to `bun run build && cap copy`

### 4. Plugin Management

> Goal: manage Capacitor plugins systematically and compatible with version 8

1. Install plugins with `bun add @capacitor/<plugin-name>`
2. Install third-party plugins with `bun add @<vendor>/capacitor-<plugin-name>`
3. Run `cap sync` after every plugin install or update
4. Define plugin configuration under the `plugins` object in `capacitor.config.ts`
5. Use `includePlugins` to allowlist plugins in `cap sync`
6. Keep plugin versions compatible with the Capacitor major version
7. Use Capacitor 8 compatible plugins only
8. Pick official plugins from the `## Official Plugins Catalog` below — it covers everything the Capacitor team maintains
9. Run `/learn-from-web` when you need additional community/third-party plugins

### 5. Platform Development

> Goal: develop and test on native platforms correctly
Develop and test on native platforms

1. Add a platform with `cap add ios` or `cap add android`
2. `cap add ios` uses the SPM template (default in Capacitor 8)
3. Use `cap add ios --packagemanager CocoaPods` if you want the CocoaPods template
4. Open the native IDE with `cap open ios` (Xcode) or `cap open android` (Android Studio)
5. Run on a device/emulator with `cap run ios` or `cap run android`
6. Run `cap sync` before every run to copy web assets and update dependencies
7. Set up live reload for development with `server.url`
8. Test on real devices before a production release

### 6. Platform-Specific Code

> Goal: handle platform-specific code correctly with feature detection

1. Use `Capacitor.platform` to detect the platform (`ios`, `android`, `web`)
2. Use `Capacitor.isNativePlatform()` to detect a native environment
3. Split platform-specific code with dynamic imports
4. Use `@capacitor/core` APIs for cross-platform access
5. Avoid browser-specific APIs that the WebView doesn't support
6. Prefer feature detection over platform detection when possible
7. Handle per-platform edge cases (e.g. WKWebView process termination on iOS)

### 7. Build And Deployment

> Goal: build and deploy to the app stores securely

1. Run `/follow-deploy` for the deployment strategy
2. Run `cap sync` before every build
3. Build iOS through Xcode or `cap run ios --configuration Release`
4. Build Android through Android Studio or Gradle
5. Configure iOS signing in `ios.buildOptions`: `signingStyle`, `exportMethod`, `signingCertificate`, `provisioningProfile`
6. Configure Android signing in `android.buildOptions`: `keystorePath`, `keystorePassword`, `keystoreAlias`, `keystoreAliasPassword`, `releaseType`, `signingType`
7. Use Fastlane to automate deployment: `fastlane supply` (Android), `fastlane deliver` (iOS)
8. Use OTA updates via `@capgo/capacitor-updater` for hot fixes
9. If you need to manage system bar insets, use `@capacitor/system-bars` (the new core plugin in Capacitor 8, replacing the removed `adjustMarginsForEdgeToEdge`)

### 8. OTA Updates

> Goal: manage over-the-air updates for the web bundle safely

1. Install `@capgo/capacitor-updater` for OTA update support
2. Define the `CapacitorUpdater` config in `capacitor.config.ts`: `appId`, `autoUpdateUrl`, `notifyUpdate`, `resetWhenUpdate`
3. Use channels for staged rollouts (`production`, `staging`, `dev`)
4. Test OTA updates on real devices before production
5. Have a rollback strategy in case an update goes wrong

### 9. Security

> Goal: follow security best practices for Capacitor apps

1. Never embed secrets in app code; keep sensitive operations server-side
2. Use PKCE for OAuth2 authentication flows
3. Use Universal Links instead of Custom URL Schemes for deep links
4. Never send sensitive data through Custom URL scheme deep links
5. Set a Content Security Policy (CSP) in a `<meta>` tag
6. Use SSL/TLS for network requests
7. Set `server.cleartext` to `false` in production
8. Use the iOS Keychain or Android Keystore to store sensitive values
9. Use `@capgo/capacitor-native-biometric` for biometric authentication
10. Set `webContentsDebuggingEnabled: false` in production

### 10. Migration And Testing

> Goal: migrate between major versions and test thoroughly

1. Migrate a major version: `bun add -D @capacitor/cli@latest` then run `npx cap migrate` — review breaking changes of every plugin and update SDK targets per Rules §1
2. Don't use `cap migrate` in a monorepo — migrate manually (see Rules §6)
3. Check the new major's platform gotchas (e.g. Capacitor 8: `@capacitor/system-bars` replaces `adjustMarginsForEdgeToEdge`, iOS `appendUserAgent` whitespace fix)
4. Test on many real devices + emulators — plugin functionality, offline/network transitions, push/local notifications, deep links, OTA flow + rollback, biometrics, app lifecycle, WebView edge cases (process termination, memory pressure)

## Rules

### 1. Version Requirements

Capacitor 8 requirements:

- Node.js >= 22 (latest LTS recommended)
- Xcode >= 26.0, iOS deployment target >= 15
- Android minSdkVersion >= 24, compileSdkVersion >= 36, targetSdkVersion >= 36
- JDK >= 21
- Android Studio >= Otter 2025.2.1 (check the latest stable with `/deep-research`)
- Kotlin >= 2.2.20
- Gradle plugin >= 8.13.0, wrapper >= 8.14.3 (AGP 9.x requires Gradle 9.x + JDK 21)

### 2. Configuration Rules

Rules for `capacitor.config.ts`:

- Use `capacitor.config.ts` (TypeScript), not `.json`
- Use the `CapacitorConfig` type from `@capacitor/cli`
- `appId` is always reverse domain name notation
- `webDir` must point to a directory containing `index.html`
- `server.cleartext` is `false` in production
- `loggingBehavior` is `none` in production
- Use platform-specific overrides in the `android` and `ios` properties
- Define plugin config in the `plugins` object keyed by class name

### 3. Plugin Rules

Rules for plugin management:

- Use Capacitor 8 compatible plugins only
- Run `cap sync` after every plugin install/update
- Use `includePlugins` for allowlisting in a monorepo
- Check plugin breaking changes before upgrading
- Use SPM (default) for iOS plugins in Capacitor 8
- Use CocoaPods with `--packagemanager CocoaPods` when required
- Don't use Cordova plugins when a Capacitor equivalent exists

### 4. SPA Build Rules

Rules for SPA integration:

- Use a separate Vite config for the SPA build (`vite.config.spa.ts`)
- Set `ssr: false` in the SPA build config
- Build into the `webDir` directory (e.g. `dist-spa`)
- Verify `index.html` is at the root of `webDir`
- Use the `cap:sync` script that builds first, then syncs
- Don't use server-side rendering in the SPA build

### 5. Security Rules

Security rules:

- Never embed secrets in app code
- Use PKCE for OAuth2
- Use Universal Links instead of Custom URL Schemes
- Set a CSP in a `<meta>` tag
- Use SSL/TLS for network requests
- `server.cleartext` is `false` in production
- Use Keychain/Keystore for sensitive values
- `webContentsDebuggingEnabled: false` in production

### 6. Monorepo Rules

Rules for monorepo integration:

- Use `bun --filter <workspace>` to run scripts in a specific workspace
- `webDir` uses a relative path from the mobile workspace (e.g. `../website/dist-spa`)
- The `cap:sync` script builds the SPA first, then syncs
- Don't use `cap migrate` in a monorepo; migrate manually
- Use `includePlugins` for allowlisting plugins in the monorepo
- Keep website and mobile workspace dependencies separate

### 7. CLI Commands

Frequently used Capacitor CLI commands:

- `cap init` - initialize Capacitor config
- `cap add [platform]` - add a native platform
- `cap sync [platform]` - copy web assets and update dependencies
- `cap copy [platform]` - copy web assets only
- `cap update [platform]` - update native dependencies only
- `cap open [platform]` - open the native IDE
- `cap run [platform]` - build and deploy to a device/emulator
- `cap migrate` - migrate to a new major version

## Expected Outcome

- The Capacitor 8 app runs on iOS, Android, and PWA
- Configuration follows best practices
- Plugins are managed systematically
- SPA integration works smoothly with the monorepo
- Security best practices are met
- Build and deployment succeed
- Conforms to the Capacitor 8 official documentation
