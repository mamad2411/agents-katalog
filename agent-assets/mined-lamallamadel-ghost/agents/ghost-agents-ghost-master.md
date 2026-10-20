# Ghost CLI - Agent Guide

## Setup & Commands

**Initial Setup:** `npm install` (root), `cd desktop && npm install` (desktop app)

**Build:** `npm run build` (desktop only, creates production build)

**Lint:** `npm run lint` (desktop only, runs ESLint on TypeScript/React files)

**Test:** `npm test` (root runs test.js + integration tests in test/)

**Dev Server:** `cd desktop && npm run desktop:dev` (Electron app with Vite HMR on :5173)

## Tech Stack

- **Root:** Pure Node.js CLI (no deps), zero-install design for global NPM package
- **Desktop:** Electron + React 18 + TypeScript + Vite + TailwindCSS + Zustand (state)
- **Testing:** Node assert (root), Vitest (desktop)
- **Extension SDK:** @ghost/extension-sdk package (CommonJS + TypeScript defs)

## Architecture

- `ghost.js`: Main CLI entry with AI-powered Git assistant (Groq/Anthropic/Gemini)
- `core/`: Gateway, runtime, pipeline layers (intercept→auth→audit→execute)
- `extensions/`: Bundled extensions (ghost-git-extension)
- `packages/extension-sdk/`: NPM package for building extensions
- `desktop/`: Electron monitoring console (React SPA) - dev-only, not published to NPM
- `test/`: Integration tests for version hooks, merge resolution, and audit features
- `docs/`: Complete extension development documentation

## Code Style

- Root: Node.js CommonJS, minimal comments, ANSI color output
- Desktop: ESLint flat config, React hooks, TypeScript strict mode, functional components
- SDK: CommonJS modules with TypeScript definitions

## Extension Developer Toolkit

New commands and SDK for building extensions:

**CLI Commands:**
- `ghost extension init` - Interactive template wizard with gallery
- `ghost extension validate [path]` - Validate manifest and permissions

**Template Gallery:** `core/templates/` - Production-ready templates:
- **API Integration** - REST/GraphQL client with auth (Bearer, API Key, OAuth)
- **File Processor** - Batch operations with progress tracking and transformations
- **Git Workflow** - Commit hooks with validation (pre-commit, commit-msg, conventional commits)
- **Testing** - Vitest/Jest setup with mocking, coverage, and E2E support

**SDK Package:** `packages/extension-sdk/` - @ghost/extension-sdk NPM package with:
- `ExtensionSDK` class - High-level API (requestFileRead, requestNetworkCall, requestGitExec)
- `IntentBuilder` - Build JSON-RPC intents
- `RPCClient` - Communication with Ghost pipeline
- TypeScript definitions included

**Documentation:** `docs/` directory:
- `extension-api.md` - Complete I/O intent schema with examples
- `extension-examples.md` - Working examples (file processor, API integration, git helper)
- `DEVELOPER_TOOLKIT.md` - Complete toolkit guide
- `QUICK_REFERENCE.md` - Quick reference card
- `TEMPLATE_GALLERY.md` - Template gallery guide
