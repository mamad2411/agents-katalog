---
description:
globs:
alwaysApply: true
---
# Project Structure and Organization Rules

## File Organization
- Use consistent directory structure
- Group related files logically
- Separate source code from configuration
- Keep tests close to source code
- Use meaningful file and folder names
- Implement proper module/package structure

## Configuration Management
- Keep configuration separate from code
- Use environment-specific config files
- Never commit sensitive configuration
- Use configuration schemas/validation
- Document configuration options
- Use consistent naming conventions

## Documentation Structure
```
/docs
  /api           # API documentation
  /architecture  # System design docs
  /deployment    # Deployment guides
  /development   # Development setup
  /user          # User guides
  README.md      # Project overview
```

## Source Code Structure
```
/src
  /components    # Reusable components
  /services      # Business logic
  /utils         # Utility functions
  /types         # Type definitions
  /constants     # Application constants
  /config        # Configuration files
```

## Testing Structure
```
/tests
  /unit          # Unit tests
  /integration   # Integration tests
  /e2e           # End-to-end tests
  /fixtures      # Test data
  /mocks         # Mock objects
```

## Build and Deployment
```
/build         # Build outputs
/scripts       # Build/deployment scripts
/docker        # Docker configurations
/ci            # CI/CD configurations
```


├── docs/                   # Project documentation
├── src/                    # Source code
│   ├── main/               # Electron main process code
│   ├── modules/            # Application modules
│   ├── preload/            # Electron preload scripts
│   ├── renderer/           # Electron renderer process (UI)
│   │   ├── hooks/          # React hooks
│   │   └── views/          # React views/components
│   └── types/              # TypeScript type definitions
└── [Configuration Files]   # Various configuration files in the root
```

## Key Components

### 1. Main Process (`src/main/`)

**Purpose:** Contains the Electron main process code that runs in a Node.js environment.

**Responsibilities:**
- Application lifecycle management
- Native API access
- Window management
- IPC (Inter-Process Communication) handling
- System integration (shortcuts, notifications, etc.)
- Database operations
- Module loading and management
- Security features (encryption, authentication)

**Placement:** Place all main process code here, organized into logical modules based on functionality.

### 2. Preload Scripts (`src/preload/`)

**Purpose:** Bridge between main process and renderer process, exposing safe APIs to the renderer.

**Responsibilities:**
- Creating secure bridges between Node.js and browser environments
- Exposing selected APIs from the main process to the renderer process
- Handling IPC communication

**Placement:** Keep preload scripts minimal and focused on creating safe bridges.


### 3. Renderer Process (`src/renderer/`)

**Purpose:** Contains the application UI code that runs in the Chromium browser environment.

**Responsibilities:**
- User interface components and logic
- Frontend state management
- UI event handling
- Communication with the main process via IPC

**Structure:**
- `hooks/` - React hooks for state management and logic
- `views/` - React components organized by application views/screens

**Placement:** All UI-related code should go here, following React best practices.

### 4. Modules (`src/modules/`)

**Purpose:** Pluggable functionality modules that can be loaded by the application.

**Responsibilities:**
- Self-contained features or integrations
- Providing specific functionality to the main application
- Following a consistent API for integration

**Placement:** Each module should have its own directory with a clear entry point and necessary components.

### 5. Types (`src/types/`)

**Purpose:** TypeScript type definitions shared across different parts of the application.

**Responsibilities:**
- Defining interfaces, types, and enums used throughout the codebase
- Ensuring type safety across process boundaries

**Placement:** Place shared types here; component-specific types can be co-located with their components.

### 6. Documentation (`docs/`)

**Purpose:** Project documentation for developers and users.

**Content:**
- Architecture overviews
- API documentation
- Development guides
- User documentation
- Security information

**Placement:** Organize by topic with clear, descriptive filenames.

### 1. Core Application Features

For features that extend the core application:

- **Main Process Logic:** Add to `src/main/` in an appropriate module
- **UI Components:** Add to `src/renderer/views/` or create a new view directory
- **Shared Types:** Add to `src/types/` if used across processes
- **Configuration:** Update relevant config files if needed

### 2. Pluggable Modules

For features that should be pluggable or independently loadable:

- Create a new directory in `src/modules/[module-name]/`
- Include a clear entry point (e.g., `index.js` or `index.ts`)
- Follow the module interface pattern used by existing modules
- Document the module in `docs/`



## Best Practices
- Keep root directory clean
- Use consistent naming conventions
- Implement proper .gitignore
- Include necessary metadata files
- Organize by feature when appropriate
- Maintain clear separation of concerns
- Use standard conventions for the ecosystem
- Document structure decisions

## Best Practices

1. **Process Separation:** Respect the separation between main and renderer processes
   - Main process: Node.js APIs, system access, heavy computation
   - Renderer process: UI rendering, user interaction
2. **IPC Communication:** Use the established IPC patterns for cross-process communication
   - Keep IPC messages well-defined and typed
   - Document IPC channels in comments

3. **Security First:**
   - Never expose unnecessary Node.js APIs to the renderer
   - Validate all inputs, especially from IPC calls
   - Follow the principle of least privilege

4. **Modularity:**
   - Keep modules self-contained
   - Use clear interfaces between components
   - Avoid tight coupling between unrelated features

5. **TypeScript Usage:**
   - Use proper typing for all components
   - Avoid `any` types where possible
   - Leverage interfaces for better code documentation

6. **Documentation:**
   - Document new features in the `docs/` directory
   - Include JSDoc comments for public APIs and interfaces
   - Update this structure document when making significant architectural changes

## Configuration Files

Several important configuration files exist in the root directory:

- `forge.config.ts` - Electron Forge build configuration
- `vite.main.config.ts` - Vite configuration for the main process
- `vite.preload.config.ts` - Vite configuration for preload scripts
- `vite.renderer.config.ts` - Vite configuration for the renderer process
- `tsconfig.json` - TypeScript compiler configuration
- `package.json` - Project dependencies and scripts

Make sure to update these files appropriately when adding new features or dependencies.

## Visual Directory Map

- Maintain an up-to-date visual directory tree in `docs/PROJECT_STRUCTURE_TREE.md`.
- Regenerate this file after major refactors or when adding/removing top-level folders or features.
- Use the command:
  ```
  tree -L 3 -I 'node_modules|.git|.next|coverage|test-results|__mocks__' > docs/PROJECT_STRUCTURE_TREE.md
  ```
  (Or update manually if the `tree` command is unavailable.)
- This file serves as the canonical map for both AI agents and human contributors to locate and import files.
- Reference this file in onboarding and contribution documentation (e.g., README.md, CONTRIBUTING.md).

---

description: Enforces that docs/PROJECT_STRUCTURE_TREE.md is always up to date and checked in CI

globs: docs/PROJECT_STRUCTURE_TREE.md, scripts/update-project-structure-tree.sh, scripts/check-project-structure-tree.sh, .github/workflows/ci.yml

alwaysApply: true

- **docs/PROJECT_STRUCTURE_TREE.md must always reflect the current project structure**
  - Regenerate with `scripts/update-project-structure-tree.sh` (or `npm run update-structure-tree`)
  - Check with `scripts/check-project-structure-tree.sh` (or `npm run check-structure-tree`)
  - CI will fail if the file is out of date
  - PRs must not be merged if this file is not current
  - Reference this file in onboarding and contribution docs
