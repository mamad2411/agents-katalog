# Cursor Rules for GameHub Project

## 🏗️ Project Structure & Architecture

### Core Architecture
- **Auto-Discovery Router System**: Use the smart router with auto-discovery for all new routes
- **Hierarchical Routing**: Follow the pattern `games.{game}.{module}.{action}` 
- **Export Default Pattern**: All handlers must use `export default` for auto-discovery
- **Folder Structure**: Each action should be a folder with `index.ts` containing the handler

### Directory Structure
```
src/
├── actions/                # 🎯 Actions & Business Logic
│   ├── games/             # Game actions (poker, etc.)
│   │   ├── index.ts       # Main games handler
│   │   └── {game}/        # Individual games
│   │       ├── index.ts   # Game-specific handler
│   │       └── {module}/  # Game modules (room, lobby, etc.)
│   │           └── {action}/ # Action folders
│   │               └── index.ts # Action handler (export default)
│   └── financial/         # Financial actions (wallet, etc.)
│       └── user-wallet/
├── modules/               # 🔧 Core Modules & Systems
│   ├── core/             # Router, handler, utilities
│   │   ├── smart-router.ts
│   │   ├── handler.ts
│   │   └── utils/
│   │       └── parseMessageKey.ts
│   └── global/           # Global configurations
├── utils/                # 🛠️ Utilities & Helpers
│   ├── types/            # Type definitions
│   ├── typeGuards.ts     # ID validation
│   └── demos/            # Demo files
├── archive/              # 📦 Archived/legacy code
│   └── games/            # Old games
└── scripts/              # 🔧 Build & deployment scripts
```

## 🔧 TypeScript Best Practices

### Type Safety Requirements
- **NO `any` types**: Use proper TypeScript types everywhere
- **NO `as` casting**: Use proper type guards and validation instead
- **Strict typing**: All functions, parameters, and return values must be typed
- **Interface over type**: Prefer interfaces for object shapes
- **Generic types**: Use generics for reusable components

### Custom ID System
```typescript
// Always use custom ID types, never raw strings for IDs
export type ID = string & {
  uuid: void;
};

type RoomId = ID & {
  Room: void;
};

type UserId = ID & {
  User: void;
};

type GameId = ID & {
  Game: void;
};

// Example usage:
export interface Room {
  id: RoomId;
  name: string;
  created_at: string;
  created_by: UserId;
  // ... other properties
}

// ❌ WRONG - Never use string for IDs
function getRoom(roomId: string) { }

// ✅ CORRECT - Use typed IDs
function getRoom(roomId: RoomId) { }
```

### Handler Pattern
```typescript
// All handlers must follow this pattern:
import { HandlerContext } from '@/modules/core/handler';

async function handleAction(context: HandlerContext, query: Record<string, string>): Promise<void> {
  // Implementation
}

export default handleAction;
```

## 🚀 Development Guidelines

### Router Usage
- Use `smart-router.ts` for all routing
- Register module handlers with `registerModule()`
- Let auto-discovery handle action routes
- Use pattern matching for dynamic routes: `games.:game.room.:action`

### File Naming & Organization
- **Action folders**: Use kebab-case for folder names (`create-room/`, `join-game/`)
- **Handler files**: Always `index.ts` inside action folders
- **Export pattern**: Always `export default` for handlers
- **Import pattern**: Use `@/` alias for imports from src

### Error Handling
- Use proper error types and interfaces
- Implement error boundaries in handlers
- Log errors with context information
- Return user-friendly error messages

### Testing Requirements
- Unit tests for all handlers
- Integration tests for router functionality
- Type checking tests for custom ID types
- Mock external dependencies properly

## 📝 Code Examples

### Creating New Game Action
```typescript
// src/actions/games/poker/room/bet/index.ts
import { HandlerContext } from '@/modules/core/handler';
import { RoomId } from '@/utils/types';

interface BetQuery {
  roomId: RoomId;
  amount: string;
}

async function handleBet(context: HandlerContext, query: Record<string, string>): Promise<void> {
  const { roomId, amount } = query as BetQuery;
  
  // Validate roomId is proper RoomId type
  if (!isValidRoomId(roomId)) {
    throw new Error('Invalid room ID');
  }
  
  // Implementation
}

export default handleBet;
```

### Type Guards for IDs
```typescript
// src/utils/typeGuards.ts
import { RoomId, UserId, GameId } from '@/utils/types';

export function isValidRoomId(id: string): id is RoomId {
  return /^room_[a-zA-Z0-9_]+$/.test(id);
}

export function isValidUserId(id: string): id is UserId {
  return /^\d+$/.test(id);
}

export function isValidGameId(id: string): id is GameId {
  return /^game_[a-zA-Z0-9_]+$/.test(id);
}
```

### Router Registration
```typescript
// src/actions/games/poker/index.ts
import { registerModule } from '@/modules/core/smart-router';
import { handlePokerMessage } from './pokerHandler';

// Register module handler
registerModule('games.poker', handlePokerMessage);
```

## 🔒 Security & Validation

### Input Validation
- Validate all query parameters
- Use type guards for ID validation
- Sanitize user inputs
- Implement rate limiting for actions

### Type Safety
- Never trust external data types
- Use runtime validation with type guards
- Implement proper error handling for type mismatches

## 📚 Documentation

### Code Comments
- Document complex business logic
- Explain type constraints and validations
- Add JSDoc for public functions
- Include usage examples for handlers

### Architecture Decisions
- Document router design decisions
- Explain auto-discovery benefits
- Document ID type system rationale
- Keep migration guides updated

## 🎯 Migration Guidelines

### From Old Structure
- Move handlers to action folders
- Convert to `export default` pattern
- Update ID types to use custom types
- Remove `any` types and `as` casting
- Update imports to use `@/` alias

### Testing Migration
- Update test imports for new structure
- Add type checking tests
- Verify auto-discovery works
- Test ID validation

## ⚠️ Common Pitfalls to Avoid

### Type Safety Issues
- ❌ Using `any` for unknown types
- ❌ Using `as` for type casting
- ❌ Using `string` for ID fields
- ❌ Ignoring TypeScript errors

### Architecture Issues
- ❌ Creating handlers without folders
- ❌ Using named exports instead of default
- ❌ Bypassing the router system
- ❌ Mixing old and new patterns

### Performance Issues
- ❌ Not caching auto-discovered handlers
- ❌ Re-importing modules unnecessarily
- ❌ Not using proper error boundaries

## 🔄 Continuous Improvement

### Code Review Checklist
- [ ] No `any` types used
- [ ] No `as` casting used
- [ ] Custom ID types used for all IDs
- [ ] Proper error handling implemented
- [ ] Auto-discovery pattern followed
- [ ] Type guards implemented where needed
- [ ] Tests cover type safety
- [ ] Documentation updated

### Future Enhancements
- Consider implementing dependency injection
- Add middleware support to router
- Implement plugin system for games
- Add real-time WebSocket support
- Consider GraphQL for complex queries 