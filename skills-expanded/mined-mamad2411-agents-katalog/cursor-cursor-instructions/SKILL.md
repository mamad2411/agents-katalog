# Cursor Project Instructions

## Project Overview

Cursor is an AI-first coding environment built on Electron. It provides advanced AI-assisted coding features including code generation, diff editing, chat interface, and more.

## Technology Stack

- **Framework**: Electron with React
- **Editor**: CodeMirror 6
- **Language**: TypeScript
- **State Management**: Redux with Redux Toolkit
- **Build System**: Electron Forge with Webpack
- **Styling**: Tailwind CSS
- **Package Manager**: npm

## Project Structure

```
cursor/
├── src/
│   ├── main/           # Electron main process
│   ├── renderer/       # React renderer process
│   ├── util/           # Shared utilities
│   └── features/       # Feature-specific modules
├── .webpack/           # Webpack configuration
├── config/             # Additional configuration
├── assets/             # Static assets
└── resources/          # Build resources
```

## Development Workflow

### Initial Setup
```bash
npm i
./setup.sh  # Mac/Linux
./setup.ps1  # Windows
```

### Running the Application
```bash
npm start
```

### Building
```bash
npm run make      # Create distributable
npm run package   # Package without making distributable
```

### Code Quality
```bash
npm run lint      # ESLint
npm run format    # Prettier
npm run fix       # Auto-fix linting issues
npm test          # Run tests
```

## Key Architecture Points

### Electron Processes
- **Main Process**: Handles OS interactions, window management, file operations
- **Renderer Process**: React-based UI, CodeMirror editor integration
- **IPC**: Use `@electron/remote` carefully, prefer secure IPC patterns

### CodeMirror Integration
- Uses CodeMirror 6 as the text editor
- Language support via @codemirror/lang-* packages
- Custom extensions for Cursor-specific features
- Vim mode support via custom adapter

### State Management
- Redux Toolkit for global state
- Feature-based slice organization
- Async operations with createAsyncThunk
- Reselect for memoized selectors

### Build Configuration
- Webpack for bundling (main and renderer separate)
- Electron Forge for packaging
- Custom loaders for TypeScript, CSS, etc.

## Important Notes

- This is the Cursor editor's own source code
- The project uses Electron Forge for packaging
- CodeMirror is heavily customized for Cursor's needs
- Security is important - validate all IPC communications
- Performance matters - optimize re-renders and state updates
- The editor supports multiple programming languages

## Git Workflow

- Use conventional commit messages
- Husky pre-commit hooks run pretty-quick for formatting
- Branch protection may be enabled
- PRs are welcome for bug fixes and features

## Testing

- Jest is configured for testing
- Test files use .test.ts or .test.tsx suffix
- Focus on critical paths and business logic
- Mock external dependencies appropriately

## Common Tasks

When working on this codebase:
1. Understand the Electron architecture (main vs renderer)
2. Follow existing patterns for similar features
3. Use TypeScript strictly - no `any` types
4. Test editor changes thoroughly
5. Consider performance implications
6. Follow the established code style (ESLint + Prettier)
