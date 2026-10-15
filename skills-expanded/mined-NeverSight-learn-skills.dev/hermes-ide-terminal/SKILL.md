---
name: hermes-ide-terminal
description: AI-native terminal emulator & IDE built with Tauri, React, and Rust
triggers:
  - "set up hermes ide"
  - "how do I use hermes terminal"
  - "configure hermes ide with claude"
  - "hermes ide git integration"
  - "build hermes from source"
  - "hermes ide agent mode"
  - "troubleshoot hermes terminal"
  - "hermes ide project scanning"
---

# Hermes IDE Terminal Skill

> Skill by [ara.so](https://ara.so) — Hermes Skills collection.

## Overview

Hermes IDE is an AI-native terminal emulator built with Tauri 2, React 18, and Rust. It provides:

- **Agent mode for Claude** with rich chat interface, image support, and persistent conversations
- **Multi-session terminal management** with split panes and WebGL rendering
- **Git integration** with built-in panel for staging, commits, and inline diffs
- **AI intelligence** including ghost-text suggestions, prompt composer, and error pattern matching
- **Project awareness** that scans your codebase to build context for AI agents
- **Cross-platform** support for macOS, Windows, and Linux

## Installation

### Pre-built Binaries

Download from the official website:
```bash
# Visit https://www.hermes-ide.com/download
# Choose your platform: macOS (Intel/Apple Silicon), Windows, Linux (.deb/.AppImage/.rpm)
```

### Build from Source

**Prerequisites:**
```bash
# Check versions
node --version  # 18+
rustc --version # 1.70+
```

**Platform-specific dependencies:**

```bash
# Linux (Debian/Ubuntu)
sudo apt install libwebkit2gtk-4.1-dev libappindicator3-dev librsvg2-dev patchelf

# macOS
xcode-select --install

# Windows
# Install Visual Studio Build Tools with "Desktop development with C++"
# Install WebView2 Runtime from Microsoft
```

**Clone and build:**
```bash
git clone https://github.com/hermes-hq/hermes-ide.git
cd hermes-ide
npm install
npm run tauri dev    # Development mode with hot-reload
npm run tauri build  # Production build
```

## Architecture

Hermes IDE uses a layered architecture:

```
React Frontend (TypeScript) ← Tauri IPC Bridge → Rust Backend
     UI & State                                   PTY, DB, Scanner
```

**Key directories:**
- `src/` - React/TypeScript frontend (components, hooks, state, terminal)
- `src-tauri/` - Rust backend (PTY management, SQLite, project scanning)
- `src/api/` - Tauri IPC command wrappers
- `src/terminal/` - Terminal pool & AI intelligence engine

## Configuration

### Claude Agent Setup

Hermes uses your existing `claude` CLI authentication:

```bash
# Install Claude CLI first
npm install -g @anthropic-ai/claude-cli

# Authenticate (choose one method)
claude auth login              # Pro/Max account
claude auth api-key $ANTHROPIC_API_KEY  # API key
```

**In Hermes IDE:**
1. Open Command Palette (Cmd/Ctrl+K)
2. Type "Claude"
3. Select "Start Claude Agent Session"
4. Conversations persist across restarts

### Project Scanning

Hermes automatically scans projects to build AI context:

```typescript
// Project scanning happens automatically when you:
// 1. Open a terminal in a directory
// 2. Attach a project via sidebar
// 3. Use Cmd/Ctrl+Shift+P → "Scan Project"

// Detected information includes:
// - Languages and frameworks
// - Project structure
// - Dependencies
// - Git repository info
```

### Terminal Configuration

Configure shell and environment in settings:

```json
{
  "shell": {
    "program": "/bin/zsh",
    "args": ["-l"]
  },
  "environment": {
    "TERM": "xterm-256color",
    "COLORTERM": "truecolor"
  },
  "fontSize": 14,
  "fontFamily": "JetBrains Mono, monospace"
}
```

## Key Features & Usage

### Terminal Sessions

```typescript
// Create new session
// Cmd/Ctrl+T

// Switch sessions
// Cmd/Ctrl+1-9 (first 9 sessions)
// Or use sidebar

// Split panes
// Cmd/Ctrl+D (horizontal)
// Cmd/Ctrl+Shift+D (vertical)

// Close session
// Cmd/Ctrl+W
```

### Git Integration

Access via sidebar panel:

```bash
# All git operations available via UI
# - View staged/unstaged/untracked files
# - Click files to see inline diffs
# - Stage/unstage with checkboxes
# - Commit with message input
# - Push/Pull buttons

# Or use git commands directly in terminal
git add .
git commit -m "feat: add new feature"
git push origin main
```

### AI Ghost-Text Suggestions

Hermes provides real-time command suggestions:

```bash
# Start typing and ghost text appears
git com█
# Suggestion: git commit -m "message"

# Accept with Tab or Right Arrow
# Reject with Esc or continue typing
```

### Prompt Composer

Use natural language for autonomous execution:

```bash
# Open Prompt Composer: Cmd/Ctrl+Shift+P
# Type natural language instructions:

"Create a new React component called UserProfile with TypeScript"
"Fix all eslint errors in src/"
"Run tests and commit if they pass"

# Hermes executes commands and tracks progress
```

### Command Palette

Access all features quickly:

```bash
# Open: Cmd/Ctrl+K
# Fuzzy search for:
# - Commands
# - Settings
# - Projects
# - Sessions
# - Git operations
```

## Development Workflow

### Frontend Development

```typescript
// src/components/Terminal.tsx
import React, { useEffect, useRef } from 'react';
import { Terminal } from 'xterm';
import { FitAddon } from 'xterm-addon-fit';

export const TerminalComponent: React.FC = () => {
  const terminalRef = useRef<HTMLDivElement>(null);
  const xtermRef = useRef<Terminal | null>(null);

  useEffect(() => {
    if (!terminalRef.current) return;

    const term = new Terminal({
      fontFamily: 'JetBrains Mono, monospace',
      fontSize: 14,
      theme: {
        background: '#1e1e1e',
        foreground: '#d4d4d4',
      },
    });

    const fitAddon = new FitAddon();
    term.loadAddon(fitAddon);
    term.open(terminalRef.current);
    fitAddon.fit();

    xtermRef.current = term;

    return () => {
      term.dispose();
    };
  }, []);

  return <div ref={terminalRef} className="terminal-container" />;
};
```

### Backend Development

```rust
// src-tauri/src/pty/mod.rs
use portable_pty::{native_pty_system, CommandBuilder, PtySize};
use std::sync::Arc;
use tokio::sync::Mutex;

pub struct PtySession {
    pub id: String,
    pty: Arc<Mutex<Box<dyn portable_pty::MasterPty + Send>>>,
    writer: Arc<Mutex<Box<dyn std::io::Write + Send>>>,
}

impl PtySession {
    pub fn new(shell: &str, cwd: &str) -> Result<Self, Box<dyn std::error::Error>> {
        let pty_system = native_pty_system();
        let pair = pty_system.openpty(PtySize {
            rows: 24,
            cols: 80,
            pixel_width: 0,
            pixel_height: 0,
        })?;

        let mut cmd = CommandBuilder::new(shell);
        cmd.cwd(cwd);
        
        let _child = pair.slave.spawn_command(cmd)?;
        let writer = pair.master.take_writer()?;

        Ok(Self {
            id: uuid::Uuid::new_v4().to_string(),
            pty: Arc::new(Mutex::new(pair.master)),
            writer: Arc::new(Mutex::new(writer)),
        })
    }

    pub async fn write(&self, data: &[u8]) -> Result<(), Box<dyn std::error::Error>> {
        let mut writer = self.writer.lock().await;
        writer.write_all(data)?;
        writer.flush()?;
        Ok(())
    }
}
```

### Tauri IPC Commands

```rust
// src-tauri/src/commands.rs
use tauri::command;

#[command]
pub async fn create_terminal_session(
    shell: String,
    cwd: String,
) -> Result<String, String> {
    let session = PtySession::new(&shell, &cwd)
        .map_err(|e| e.to_string())?;
    
    let session_id = session.id.clone();
    
    // Store session in global state
    // ...
    
    Ok(session_id)
}

#[command]
pub async fn write_to_terminal(
    session_id: String,
    data: String,
) -> Result<(), String> {
    // Get session from global state
    // ...
    
    session.write(data.as_bytes())
        .await
        .map_err(|e| e.to_string())?;
    
    Ok(())
}
```

### Frontend API Wrappers

```typescript
// src/api/terminal.ts
import { invoke } from '@tauri-apps/api/tauri';

export interface TerminalSession {
  id: string;
  cwd: string;
  shell: string;
}

export async function createTerminalSession(
  shell: string,
  cwd: string
): Promise<string> {
  return await invoke<string>('create_terminal_session', {
    shell,
    cwd,
  });
}

export async function writeToTerminal(
  sessionId: string,
  data: string
): Promise<void> {
  await invoke('write_to_terminal', {
    sessionId,
    data,
  });
}

export async function resizeTerminal(
  sessionId: string,
  rows: number,
  cols: number
): Promise<void> {
  await invoke('resize_terminal', {
    sessionId,
    rows,
    cols,
  });
}
```

## Common Patterns

### State Management

Hermes uses React Context + useReducer:

```typescript
// src/state/AppContext.tsx
import React, { createContext, useReducer } from 'react';

interface AppState {
  sessions: TerminalSession[];
  activeSessionId: string | null;
  projects: Project[];
}

type AppAction =
  | { type: 'ADD_SESSION'; session: TerminalSession }
  | { type: 'REMOVE_SESSION'; sessionId: string }
  | { type: 'SET_ACTIVE_SESSION'; sessionId: string };

const appReducer = (state: AppState, action: AppAction): AppState => {
  switch (action.type) {
    case 'ADD_SESSION':
      return {
        ...state,
        sessions: [...state.sessions, action.session],
      };
    case 'REMOVE_SESSION':
      return {
        ...state,
        sessions: state.sessions.filter(s => s.id !== action.sessionId),
      };
    case 'SET_ACTIVE_SESSION':
      return {
        ...state,
        activeSessionId: action.sessionId,
      };
    default:
      return state;
  }
};

export const AppContext = createContext<{
  state: AppState;
  dispatch: React.Dispatch<AppAction>;
} | null>(null);

export const AppProvider: React.FC = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, {
    sessions: [],
    activeSessionId: null,
    projects: [],
  });

  return (
    <AppContext.Provider value={{ state, dispatch }}>
      {children}
    </AppContext.Provider>
  );
};
```

### Custom Hooks

```typescript
// src/hooks/useTerminal.ts
import { useContext, useCallback } from 'react';
import { AppContext } from '../state/AppContext';
import { createTerminalSession, writeToTerminal } from '../api/terminal';

export const useTerminal = () => {
  const context = useContext(AppContext);
  if (!context) throw new Error('useTerminal must be used within AppProvider');

  const { state, dispatch } = context;

  const createSession = useCallback(async (shell: string, cwd: string) => {
    const sessionId = await createTerminalSession(shell, cwd);
    dispatch({
      type: 'ADD_SESSION',
      session: { id: sessionId, shell, cwd },
    });
    dispatch({ type: 'SET_ACTIVE_SESSION', sessionId });
    return sessionId;
  }, [dispatch]);

  const write = useCallback(async (data: string) => {
    if (!state.activeSessionId) return;
    await writeToTerminal(state.activeSessionId, data);
  }, [state.activeSessionId]);

  return {
    sessions: state.sessions,
    activeSessionId: state.activeSessionId,
    createSession,
    write,
  };
};
```

### Project Scanning

```rust
// src-tauri/src/project/scanner.rs
use std::path::Path;
use walkdir::WalkDir;
use serde::{Serialize, Deserialize};

#[derive(Serialize, Deserialize)]
pub struct ProjectContext {
    pub languages: Vec<String>,
    pub frameworks: Vec<String>,
    pub dependencies: Vec<String>,
    pub structure: String,
}

pub fn scan_project(path: &Path) -> Result<ProjectContext, Box<dyn std::error::Error>> {
    let mut languages = Vec::new();
    let mut frameworks = Vec::new();
    let mut dependencies = Vec::new();

    // Detect package.json (Node.js)
    if path.join("package.json").exists() {
        languages.push("JavaScript".to_string());
        let package_json = std::fs::read_to_string(path.join("package.json"))?;
        let package: serde_json::Value = serde_json::from_str(&package_json)?;
        
        if let Some(deps) = package.get("dependencies") {
            if deps.get("react").is_some() {
                frameworks.push("React".to_string());
            }
            if deps.get("vue").is_some() {
                frameworks.push("Vue".to_string());
            }
        }
    }

    // Detect Cargo.toml (Rust)
    if path.join("Cargo.toml").exists() {
        languages.push("Rust".to_string());
    }

    // Count files by type for structure summary
    let mut file_counts = std::collections::HashMap::new();
    for entry in WalkDir::new(path).max_depth(3) {
        if let Ok(entry) = entry {
            if let Some(ext) = entry.path().extension() {
                *file_counts.entry(ext.to_string_lossy().to_string()).or_insert(0) += 1;
            }
        }
    }

    Ok(ProjectContext {
        languages,
        frameworks,
        dependencies,
        structure: format!("{:?}", file_counts),
    })
}
```

## Testing

### Frontend Tests

```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Watch mode
npm run test:watch
```

```typescript
// src/components/__tests__/Terminal.test.tsx
import { render, screen } from '@testing-library/react';
import { TerminalComponent } from '../Terminal';

describe('TerminalComponent', () => {
  it('renders terminal container', () => {
    render(<TerminalComponent />);
    const container = screen.getByClassName('terminal-container');
    expect(container).toBeInTheDocument();
  });
});
```

### Backend Tests

```bash
cd src-tauri
cargo test
cargo test -- --nocapture  # Show output
```

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_pty_session_creation() {
        let session = PtySession::new("/bin/bash", "/tmp");
        assert!(session.is_ok());
        let session = session.unwrap();
        assert!(!session.id.is_empty());
    }

    #[tokio::test]
    async fn test_write_to_pty() {
        let session = PtySession::new("/bin/bash", "/tmp").unwrap();
        let result = session.write(b"echo test\n").await;
        assert!(result.is_ok());
    }
}
```

## Troubleshooting

### Build Issues

**Error: `webkit2gtk not found`**
```bash
# Linux
sudo apt install libwebkit2gtk-4.1-dev

# If still failing, check pkg-config
pkg-config --modversion webkit2gtk-4.1
```

**Error: `Rust toolchain not found`**
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

**Error: `node-gyp` failures on Windows**
```bash
npm install --global windows-build-tools
npm config set msvs_version 2019
```

### Runtime Issues

**Terminal not rendering**
```typescript
// Check terminal element is mounted
useEffect(() => {
  console.log('Terminal ref:', terminalRef.current);
  if (!terminalRef.current) {
    console.error('Terminal container not found');
    return;
  }
  // ...
}, []);
```

**PTY session hangs**
```rust
// Add timeout to PTY operations
use tokio::time::{timeout, Duration};

let result = timeout(
    Duration::from_secs(5),
    session.write(data)
).await;

if result.is_err() {
    eprintln!("PTY write timed out");
}
```

**Git authentication fails**
```bash
# Check SSH agent
ssh-add -l

# Or use Git Credential Manager
git config --global credential.helper manager

# Set environment variable in Hermes settings
# GIT_SSH_COMMAND="ssh -i ~/.ssh/id_rsa"
```

### Performance Issues

**High CPU usage**
```bash
# Check terminal rendering settings
# Reduce font size or disable ligatures
# Limit scrollback buffer size in settings
```

**Memory leaks**
```typescript
// Ensure proper cleanup in useEffect
useEffect(() => {
  const term = new Terminal();
  // ...
  
  return () => {
    term.dispose();  // Critical!
  };
}, []);
```

## Environment Variables

```bash
# Claude API configuration
export ANTHROPIC_API_KEY=sk-ant-...

# Custom shell
export HERMES_SHELL=/bin/zsh

# Debug logging
export RUST_LOG=debug
export HERMES_DEBUG=1

# Custom config directory
export HERMES_CONFIG_DIR=$HOME/.config/hermes
```

## Contributing

```bash
# Fork and clone
git clone https://github.com/YOUR_USERNAME/hermes-ide.git
cd hermes-ide

# Create feature branch
git checkout -b feature/my-feature

# Make changes and test
npm run tauri dev
npm run test
cd src-tauri && cargo test

# Type check
npx tsc --noEmit

# Commit (follows conventional commits)
git commit -m "feat: add new terminal feature"

# Push and open PR
git push origin feature/my-feature

# Sign CLA when prompted
```

Read [CONTRIBUTING.md](https://github.com/hermes-hq/hermes-ide/blob/main/CONTRIBUTING.md) and [DESIGN_PRINCIPLES.md](https://github.com/hermes-hq/hermes-ide/blob/main/DESIGN_PRINCIPLES.md) before contributing.

## Resources

- **Documentation**: https://github.com/hermes-hq/hermes-ide#readme
- **Architecture**: https://github.com/hermes-hq/hermes-ide/blob/main/ARCHITECTURE.md
- **Discord**: https://discord.gg/vMQXSTY6BM
- **Discussions**: https://github.com/hermes-hq/hermes-ide/discussions
- **Changelog**: https://hermes-ide.com/changelog
