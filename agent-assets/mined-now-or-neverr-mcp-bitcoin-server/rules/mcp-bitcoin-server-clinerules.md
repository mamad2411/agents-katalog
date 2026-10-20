# Project Intelligence: Bitcoin Wallet MCP Server

This file captures important patterns, preferences, and project intelligence for the Bitcoin wallet MCP server project.

## Project Patterns

### Directory Structure
- `memory-bank/`: Documentation and context for the project
- Future directories should follow Node.js/TypeScript best practices:
  - `src/`: Source code
  - `dist/`: Compiled output
  - `tests/`: Test files
  - `config/`: Configuration files

### Coding Standards
- TypeScript for all new code
- Follow Node.js and TypeScript best practices
- Async/await preferred over callbacks or raw promises
- Strong typing for all interfaces
- Security-first approach for all cryptocurrency operations

### Bitcoin-Specific Patterns
- Always validate Bitcoin addresses before operations
- Treat private keys with highest security measures
- Consider both testnet and mainnet compatibility
- Handle Bitcoin value amounts as satoshis in code (1 BTC = 100,000,000 satoshis)
- Include proper error handling for network operations

### MCP Server Patterns
- Use the MCP SDK for all client-facing interfaces
- Define clear input and output schemas for tools
- Follow the MCP protocol for resource URI templates
- Properly validate all incoming requests

### Security Practices
- Never log sensitive information (private keys, mnemonics)
- Encrypt all sensitive data at rest
- Apply proper access controls for wallet operations
- Use secure random number generation for cryptographic operations
- Apply the principle of least privilege

## Development Workflow

### Package Management
- **Strictly use `pnpm` for all package management tasks.**
- **NEVER edit `package.json` directly.** Use `pnpm add`, `pnpm remove`, or `pnpm pkg set` commands to manage dependencies and scripts.

### Setting Up Development Environment
1. Install Node.js and `pnpm` globally (`npm install -g pnpm` or follow official pnpm install guide).
2. Run `pnpm install` to install project dependencies.
3. Configure editor for TypeScript, ESLint, Prettier (if used).
4. Set up testing framework (TBD).

### Implementation Flow
1. Start with basic MCP server implementation
2. Add Bitcoin library integration
3. Implement wallet management functionality
4. Add transaction handling capabilities
5. Implement security measures
6. Create comprehensive tests

### Testing Approach
- Unit tests for all core functionality
- Integration tests for Bitcoin operations
- Use testnet for live transaction testing
- Implement security-focused tests
- **Verification**: ALWAYS run `pnpm test` after installing dependencies, updating configurations (tsconfig, jest config), or implementing features. Do NOT consider a task complete until all tests pass. Configuration interactions can be complex and require validation.

### Jest/ESM Configuration Notes (Learned July 4, 2025)
- **Context**: Project uses TypeScript, `type: "module"`, `module: NodeNext`, `isolatedModules: true`.
- **Requirement**: Running Jest requires the `NODE_OPTIONS=--experimental-vm-modules` flag in the `test` script (`package.json`).
- **Requirement**: Jest globals (`jest`, `describe`, `it`, etc.) must be explicitly imported from `@jest/globals` in both test files (`*.test.ts`) and manual mock files (`__mocks__/*.ts`) when using ESM configuration. Install `@jest/globals` as a dev dependency (`pnpm add -D @jest/globals`).
- **Requirement**: When mocking modules with native bindings (like `keytar`), explicitly map the module to its mock file using `moduleNameMapper` in `jest.config.cjs` (e.g., `'^keytar$': '<rootDir>/tests/__mocks__/keytar.ts'`).
- **Configuration**: Use the `ts-jest/presets/default-esm` preset in `jest.config.cjs`. Avoid conflicting `moduleNameMapper` rules (like removing `.js` extensions) if they interfere with `ts-jest`'s ESM handling.

## Project Evolution

The project will likely evolve through these phases:
1. Basic wallet functionality (create wallet, check balance)
2. Transaction capabilities (send, receive)
3. Advanced wallet features (HD wallets, multisig)
4. Enhanced security measures
5. Performance optimizations
6. Additional cryptocurrency support (potential future extension)

## User Preferences / Project Rules

- **Package Manager**: `pnpm` is the required package manager.
- **Dependency Management**: All dependencies MUST be added/removed using `pnpm` commands (`pnpm add`, `pnpm remove`). Direct editing of `package.json` for dependencies is forbidden.
- **Script Management**: Scripts in `package.json` should preferably be managed using `pnpm pkg set scripts.<script_name>="<command>"`. (Note: Adding `NODE_OPTIONS` required manual edit for clarity).
- **Test Verification**: **CRITICAL:** Always run `pnpm test` after changes. Do not assume success based on code/config edits alone. Confirm with passing tests before proceeding or completing a task.

## Critical Implementation Paths

### Wallet Creation
- Key generation
- Address derivation
- Secure storage

### Transaction Handling
- UTXO selection
- Transaction construction
- Fee calculation
- Transaction signing
- Network broadcasting

### Security Implementation
- Key encryption
- Secure storage
- Access control
- Input validation

## Tool Usage Patterns

### MCP Tool Design
- Keep tools focused on single responsibilities
- Use clear and consistent naming
- Provide detailed descriptions
- Use comprehensive input validation
- Return consistent error formats

### Resource Design
- Use intuitive URI patterns
- Provide consistent data formats
- Include pagination for large data sets
- Return appropriate error codes

## Known Challenges

- Bitcoin network reliability and confirmation times
- Fee estimation accuracy
- Security of key storage
- Testing cryptocurrency transactions safely
- Maintaining compatibility with Bitcoin protocol updates

This document will be updated as project work progresses and new patterns and insights emerge.
