# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Claude Suite is a comprehensive desktop GUI application for Claude CLI, built specifically for Windows with Tauri (Rust backend) and React TypeScript frontend. It provides an intuitive interface for AI-powered development workflows, project management, session handling, and MCP (Model Context Protocol) server management.

The application focuses on core Claude CLI integration optimized for Windows users, providing a streamlined experience for developers working with AI assistance on Windows platforms.

## Core Architecture

### Frontend (React/TypeScript)
- **Main App**: Multi-view application managing projects, sessions, agents, and settings
- **Core Components**: 
  - `FloatingPromptInput`: Central input interface with clipboard image support and thinking modes
  - `ClaudeCodeSession`: Real-time Claude interaction interface with session resumption and checkpoint management
  - `CCAgents`: Agent creation and management system with GitHub integration
  - `MCPManager`: MCP server configuration, testing, and project-specific management
  - `Settings`: Multi-tab configuration UI with theme switching, hooks, storage, and advanced settings
  - `HooksEditor`: Advanced shell command hooks for tool events with regex matching and templates
  - `StorageTab`: SQLite database viewer/editor for agent data and session history
  - `LanguageSelector`: Multi-language support with Chinese-first localization
  - `ClaudeStatusIndicator`: Real-time status monitoring for Claude processes
  - `ProviderManager`: Provider configuration and management system for API switching
  - `SlashCommandsManager`: Custom slash command system with autocomplete
  - `UsageDashboard`: Usage statistics and metrics tracking interface

### Frontend Architecture
- **Context Management**: 
  - `ThemeContext`: OKLCH color space-based theme system with localStorage persistence
- **Custom Hooks**: 
  - `useTranslation`: Chinese-first internationalization with fallback support
- **State Management**: React Context providers for theme, output caching, and i18n
- **API Layer**: Type-safe Tauri invoke-based communication (`src/lib/api.ts`) with comprehensive error handling

### Backend (Rust/Tauri)
- **Commands Architecture**: Modular command handlers in `src-tauri/src/commands/`
  - `claude.rs`: Core Claude CLI integration with process lifecycle management and project hiding/restoration
  - `agents.rs`: Agent execution with GitHub integration and process monitoring
  - `mcp.rs`: MCP server lifecycle, configuration, and health monitoring
  - `clipboard.rs`: Clipboard image handling with temporary file management
  - `storage.rs`: SQLite database operations with query optimization
  - `slash_commands.rs`: Custom slash command system with autocomplete
  - `usage.rs`: Usage statistics and metrics tracking
  - `provider.rs`: Provider configuration management for API switching
- **Additional Modules**:
  - `checkpoint/`: Session checkpoint management system with state persistence
  - `process/`: Process registry and lifecycle management
  - `claude_binary.rs`: Claude CLI binary detection and management

## Data Flow Architecture

1. **Frontend → Backend**: Type-safe Tauri `invoke()` with comprehensive error handling
2. **Backend → CLI**: Process spawning with streaming output capture and health monitoring
3. **Database**: SQLite with automatic migrations and query optimization
4. **File System**: Scoped access with security policies (`$HOME/**`, `$TEMP/**`, `$TMP/**`)
5. **Image Pipeline**: Clipboard → Base64 → Temp files → Claude CLI paths with UNC path handling
6. **Project Management**: Hidden projects list stored in `~/.claude/hidden_projects.json`

## Development Commands

### Frontend Development
```bash
# Start development server (Vite)
bun run dev        # Preferred
npm run dev        # Alternative

# Build frontend only
bun run build      # Preferred
npm run build      # Alternative

# Type checking
npx tsc --noEmit

# Preview built frontend
npm run preview
```

### Tauri Development
```bash
# Start Tauri development (includes frontend auto-rebuild)
npm run tauri dev

# Build complete release application (REQUIRED for cross-device compatibility)
npm run tauri build

# Build Rust backend only (debug)
cd src-tauri && cargo build

# Build Rust backend only (release with optimizations)
cd src-tauri && cargo build --release --features custom-protocol

# Run Rust tests
cd src-tauri && cargo test

# Check Rust code formatting
cd src-tauri && cargo fmt --check

# Run Rust linter
cd src-tauri && cargo clippy
```

### Critical Build Requirements
- **ALWAYS use `npm run tauri build` for production/testing** - ensures cross-device compatibility
- **Bun is required for release builds** - npm builds may cause compatibility issues on other devices
- **Release builds use aggressive optimizations** - opt-level="z", LTO, strip symbols

### Key Build Outputs
- Executable: `src-tauri/target/release/claude-suite.exe`
- MSI Installer: `src-tauri/target/release/bundle/msi/Claude Suite_1.0.0_x64_en-US.msi`
- NSIS Installer: `src-tauri/target/release/bundle/nsis/Claude Suite_1.0.0_x64-setup.exe`

## Architecture Patterns

### Frontend-Backend Communication
All communication uses Tauri's type-safe `invoke()` pattern:
```typescript
// Frontend with error handling
const result = await invoke<ReturnType>('command_name', { param: value });

// Backend with Result pattern
#[command]
async fn command_name(param: Type) -> Result<ReturnType, String>
```

### State Management
- **Global State**: React Context providers with TypeScript integration
- **Local State**: Component-specific state with hooks
- **Persistent State**: SQLite database with automatic migrations
- **Theme State**: OKLCH color space with localStorage persistence

### Error Handling Strategy
- **Rust Backend**: Comprehensive `Result<T, String>` pattern with detailed error messages
- **Frontend**: Type-safe error handling with user-friendly alerts
- **Process Management**: Graceful cleanup and recovery mechanisms

### Project Management System
- **Project Listing**: Dynamic scanning of `~/.claude/projects` directory
- **Project Hiding**: Non-destructive removal from project list using `hidden_projects.json`
- **Project Restoration**: Ability to restore hidden projects back to the list
- **File Preservation**: All project files and sessions are preserved when "deleting" projects

## Theme System

### OKLCH Color Space Implementation
```css
/* Enhanced theme with OKLCH color space for better perception */
:root, .dark {
  --color-background: oklch(0.12 0.01 240);
  --color-foreground: oklch(0.98 0.01 240);
  --color-muted-foreground: oklch(0.68 0.01 240);
}

.light {
  --color-background: oklch(0.99 0.005 240);
  --color-foreground: oklch(0.08 0.01 240);
  --color-muted-foreground: oklch(0.45 0.01 240);
}
```

### Theme Features
- **Dual Theme Support**: Light and dark themes with instant switching
- **Enhanced Contrast**: Improved readability in light theme with optimized contrast ratios
- **Backdrop Effects**: Advanced backdrop-blur with proper transparency handling
- **Chinese Font Support**: Comprehensive Chinese font stack with fallbacks
- **Accessibility**: WCAG-compliant contrast ratios (4.5:1 minimum)

## Internationalization

### Chinese-First Strategy
- **Primary Language**: Chinese (zh) with comprehensive UI translation
- **Fallback Strategy**: Chinese → English for all missing translations
- **Detection Order**: localStorage → navigator → htmlTag
- **Implementation**: Direct Chinese text in components for better performance
- **Resources**: Comprehensive translation files in `src/i18n/locales/`

### Localization Implementation
```typescript
// i18n configuration
fallbackLng: 'zh',
lng: 'zh',
detection: {
  order: ['localStorage', 'navigator', 'htmlTag'],
  caches: ['localStorage'],
}
```

## Dependencies and Technology Stack

### Frontend Stack
- **React 18.3.1**: Latest React with concurrent features
- **TypeScript 5.6.2**: Enhanced type safety and modern features
- **Tailwind CSS 4.1.8**: Latest utility-first CSS framework with Vite plugin
- **Tauri 2.1.1**: Modern Rust-based desktop framework
- **Framer Motion 12.0.0-alpha.1**: Smooth animations and transitions
- **Radix UI**: Accessible component primitives for dialogs, dropdowns, selects, tabs, tooltips
- **i18next 25.3.2**: Comprehensive internationalization with browser language detection
- **React Hook Form 7.54.2**: Form handling with Zod validation
- **@uiw/react-md-editor**: Markdown editing capabilities
- **React Syntax Highlighter**: Code syntax highlighting support

### Backend Stack
- **Rust 2021 Edition**: Modern Rust with async/await throughout
- **Tauri 2.x**: Desktop framework with comprehensive plugin system (shell, dialog, fs, process, updater, notification, clipboard-manager, global-shortcut, http)
- **SQLite (Rusqlite 0.32)**: Embedded database with bundled support
- **Tokio**: Async runtime for concurrent operations
- **Serde**: JSON serialization/deserialization with derive macros
- **Reqwest 0.12**: HTTP client for API communications
- **Chrono 0.4**: Date and time handling with serialization
- **Regex**: Pattern matching for hooks and content processing
- **Anyhow**: Error handling and context management
- **Base64 0.22**: Encoding for image clipboard operations
- **UUID 1.6**: Unique identifier generation with v4 and serde features
- **Tempfile**: Temporary file management for clipboard images
- **Zstd 0.13**: Compression for data storage optimization

### Build and Development
- **Bun**: Primary package manager (REQUIRED for cross-device compatibility)
- **Vite 6.0.3**: Fast development server and build tool with code splitting
- **Cargo**: Rust package manager with release optimizations
- **TypeScript Compiler**: Strict type checking and compilation

## Security Configuration

### Tauri Security Policies
```json
{
  "security": {
    "csp": "default-src 'self'; img-src 'self' asset: https://asset.localhost blob: data:; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-eval'",
    "assetProtocol": {
      "enable": true,
      "scope": ["**"]
    }
  }
}
```

### Filesystem Access
- **Allowed Scopes**: `$HOME/**`, `$TEMP/**`, `$TMP/**`
- **Permitted Operations**: readFile, writeFile, readDir, copyFile, createDir, removeDir, removeFile, renameFile, exists
- **Image Handling**: Temporary file storage with automatic cleanup

## Performance Optimizations

### Memory Management
- **Frontend Circular Buffering**: Prevents memory leaks in streaming operations
- **Backend Resource Cleanup**: Automatic cleanup of processes and temporary files
- **Database Optimization**: Efficient queries with proper indexing
- **Image Processing**: Optimized clipboard handling with temporary storage

### Build Optimizations
- **Code Splitting**: Manual chunks for vendor libraries and features (react-vendor, ui-vendor, editor-vendor, syntax-vendor, tauri, utils)
- **Rust Release Optimization**: Aggressive size optimization with LTO and symbol stripping (opt-level="z", lto=true, strip=true, panic="abort")
- **Chunk Size Management**: 2MB warning limit with strategic code splitting
- **Bundle Analysis**: ESBuild minification with CSS minification and ES2020 target

## Testing Strategy

### UI Testing Framework
Comprehensive testing strategy documented in `TESTING_GUIDE.md`:

1. **Theme Testing**: Both light and dark themes across all components
2. **Layout Testing**: Responsive design across desktop, tablet, and mobile
3. **Interaction Testing**: All user interactions and edge cases
4. **Performance Testing**: Memory usage, scrolling performance, and response times
5. **Cross-browser Testing**: Chrome 88+, Firefox 113+, Safari 15.4+, Edge 88+

## Development Workflow

### Critical Development Practices
1. **Always use `npm run tauri build` for testing** - Development mode can mask compatibility issues
2. **Bun is required for release builds** - Ensures cross-device compatibility
3. **Test in both themes** - Light and dark theme compatibility is essential
4. **Memory leak prevention** - Monitor frontend memory usage during development

### File Structure Patterns
- **Commands**: Each feature has its own command module in `src-tauri/src/commands/`
- **Components**: Organized by feature with comprehensive TypeScript types
- **Contexts**: Global state management with React Context
- **Hooks**: Custom hooks for complex state logic
- **Types**: Comprehensive type definitions for all interfaces

## Important Notes

### Recent Major Changes
- **Session Pool Removal**: All session pool functionality has been completely removed as it was deemed redundant
- **WSL Support Removal**: WSL integration has been completely removed to simplify the codebase
- **Project Management**: "Delete" project now means hiding from list while preserving all files
- **Application Rebranding**: Renamed from "Claudia" to "Claude Suite"

### Cross-Platform Compatibility
- **Windows-specific optimizations**: Process handling and file path management
- **Path Handling**: Proper handling of different OS path separators
- **UNC Path Support**: Automatic stripping of Windows UNC prefixes

### Deployment Considerations
- **Installer Generation**: Both MSI and NSIS installers are generated
- **Security Scanning**: CSP policies and filesystem restrictions
- **Version Management**: Automatic version handling in build process

### Known Limitations
- **OKLCH Color Space**: Requires modern browser support (Chrome 88+, Firefox 113+)
- **Backdrop Filter**: Browser support required for advanced transparency effects

## Troubleshooting

### Common Issues
1. **Build Compatibility Issues**: Always use `npm run tauri build` with bun for cross-device compatibility
2. **Theme Switching Problems**: Verify ThemeContext is properly wrapped around components
3. **Font Rendering**: Ensure Chinese fonts are properly loaded in CSS
4. **Multiline Content Send Failures**: Fixed in `claude.rs` with proper command line escaping

### Debug Commands
```bash
# Check compilation
cd src-tauri && cargo check

# Monitor memory usage in development
# Check for memory leaks in browser dev tools

# Theme debugging
# Verify CSS custom properties are applied correctly in browser inspector
```

Document Read
when you read document，if the lines < 500 you'd better read the full file

This documentation reflects the current simplified state of the project with recent major cleanups including session pool removal, WSL removal, and project management improvements. The application now focuses on core Claude CLI integration with a streamlined, maintainable architecture.