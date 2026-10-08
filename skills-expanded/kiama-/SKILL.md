# KIAMA Cursor Rules

## Project Overview
KIAMA is a decentralized chat application similar to Discord, built with Electron, React, and Node.js.

## Code Style
- **TypeScript**: Strict mode, explicit types
- **React**: Functional components with hooks
- **Naming**: PascalCase for components, camelCase for variables
- **Imports**: Relative imports within modules, absolute from src root
- **Styling**: SCSS modules, BEM-like class naming

## Architecture
- **Client**: Electron main process + React renderer
- **Server**: Node.js with Express + Socket.IO
- **Plugins**: Extensible system for both client and server
- **Build**: All outputs go to root `dist/` directory

## Key Patterns

### Component Structure
```typescript
interface ComponentProps {
  // Define props interface
}

const ComponentName: React.FC<ComponentProps> = ({ prop }) => {
  // Component logic
  return (
    <div className="component-name">
      {/* JSX content */}
    </div>
  );
};
```

### Plugin Creation
```typescript
const myPlugin: ClientPlugin = {
  name: 'My Plugin',
  version: '1.0.0',
  init: (api) => {
    // Plugin initialization
  }
};
```

### Server Method
```typescript
private setupSocket() {
  // Socket.IO setup
}
```

## Development Workflow
1. `npm run install:all` - Install dependencies
2. `npm run build` - Build all components
3. `npm run start:server` & `npm run start:client` - Run application
4. Use `npm run dev:*` for development with hot reload

## Common Issues
- Path resolution problems (use absolute paths in configs)
- Module not found (check dist/ directory)
- Socket connection issues (verify server is running)
- Plugin loading failures (check plugin interface compliance)

## File Locations
- Client main: `src/client/main/main.ts`
- React app: `src/client/renderer/src/App.tsx`
- Server main: `src/server/src/server.ts`
- CLI entry: `src/server/src/index.ts`
- Built files: `dist/` directory

## Testing
Currently manual testing. Key areas:
- Server startup and CLI functionality
- Client connection and messaging
- Plugin loading and execution
- Build process completion