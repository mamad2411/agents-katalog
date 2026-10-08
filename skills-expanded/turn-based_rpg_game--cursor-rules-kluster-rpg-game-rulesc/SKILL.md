---
description: Kluster.ai custom code review rules for Turn-Based RPG Game - Validation rules for game mechanics, data integrity, security, and performance
globs: **/*.ts,**/*.tsx,**/*.js,**/*.jsx
---

# Turn-Based RPG Game - Kluster.ai Code Review Rules

## 1. GAME MECHANICS INTEGRITY

### Battle System Rules
- **Critical**: Battle damage calculations MUST be deterministic and server-side only. Never trust client-provided damage values.
- **Critical**: Ability cooldowns and mana costs MUST be validated on the server before execution.
- **High**: Battle state transitions MUST follow the correct sequence: player turn → ability execution → DoT/buff application → enemy turn → victory check.
- **High**: Health values MUST never exceed max health except during explicit healing that allows overheal.
- **Medium**: Damage over time (DoT) effects MUST track duration and tick count correctly.
- **Medium**: Buff/debuff stacking MUST be handled correctly (e.g., multiple shields should stack, not overwrite).
- **Low**: Battle log messages should accurately reflect all actions taken.

### Character Class Balance
- **High**: Class-specific abilities (Priest healing, Mage damage, Warrior defense) MUST scale appropriately with player level.
- **High**: Base stats for each class (Priest: spirit focus, Mage: intellect focus, Warrior: strength/stamina focus) MUST remain balanced.
- **Medium**: Ability power scaling formulas should be consistent across all classes.
- **Low**: Class descriptions should match actual gameplay mechanics.

### Progression System
- **Critical**: Experience gain MUST be calculated server-side only to prevent cheating.
- **Critical**: Level calculations MUST use the formula: `Math.floor(Math.sqrt(experience / 100)) + 1` consistently.
- **High**: Daily experience resets MUST be atomic operations to prevent race conditions.
- **Medium**: Level-ups should trigger proper stat recalculations immediately.
- **Medium**: Experience requirements should increase reasonably with level to maintain engagement.

### Equipment & Items
- **Critical**: Item stat bonuses MUST be validated on the server before applying to player stats.
- **Critical**: Item rarity (common, uncommon, rare, epic, legendary) MUST affect stat ranges appropriately.
- **High**: Equipment slots (weapon, helmet, chest, legs, boots, accessory) MUST be mutually exclusive per slot.
- **High**: Item generation algorithms MUST produce balanced items that don't break game economy.
- **Medium**: Item quality should visibly affect player power without creating pay-to-win scenarios.
- **Medium**: Equipment changes should immediately update player stats in active battles.

## 2. CONVEX BACKEND PATTERNS

### Query Safety
- **Critical**: Queries MUST never modify database state. Use mutations for any data changes.
- **Critical**: User authentication checks MUST occur at the start of every authenticated query/mutation.
- **High**: Queries that filter data MUST use `withIndex()` instead of `.filter()` for performance.
- **High**: Paginated queries MUST use `paginationOptsValidator` and return `{page, isDone, continueCursor}`.
- **Medium**: Query results should limit data exposure (don't return sensitive fields unnecessarily).
- **Low**: Query names should clearly indicate what data they retrieve.

### Mutation Safety
- **Critical**: Mutations that modify player resources (health, mana, gold, items) MUST validate the player owns those resources.
- **Critical**: Race condition-prone operations (concurrent battles, item trades) MUST be handled atomically.
- **High**: Mutations MUST validate all input arguments using Convex validators before processing.
- **High**: Error messages from mutations should be user-friendly and not expose internal details.
- **Medium**: Mutations should return meaningful data to the client for UI updates.
- **Medium**: Complex mutations should break down into helper functions for testability.

### Function Registration
- **Critical**: Sensitive game logic (damage calculation, reward distribution) MUST use `internalMutation` or `internalAction`, NOT public functions.
- **High**: All Convex functions MUST include both `args` and `returns` validators.
- **High**: Public API functions MUST sanitize inputs to prevent injection attacks.
- **Medium**: Function names should follow camelCase and be descriptive of their action.
- **Low**: Group related functions in the same file (e.g., all battle logic in `battles.ts`).

### Database Schema Integrity
- **Critical**: Schema changes MUST maintain backward compatibility with existing data.
- **Critical**: Index names MUST include all indexed fields (e.g., `by_player_and_level` for `["playerId", "level"]`).
- **High**: Foreign key relationships (e.g., `playerId: v.id("players")`) MUST be enforced in mutations.
- **High**: Required fields should use non-optional validators; optional fields must use `v.optional()`.
- **Medium**: Schema should minimize data duplication (normalize when appropriate).
- **Medium**: Add indexes for all common query patterns to avoid table scans.

## 3. FRONTEND REACT PATTERNS

### Component Structure
- **High**: Components MUST handle loading states when using `useQuery` (check for `undefined`).
- **High**: Error handling MUST be implemented for all `useMutation` calls with user-friendly toast messages.
- **Medium**: Complex components should break down into smaller, reusable sub-components.
- **Medium**: Props interfaces should be explicitly typed and documented.
- **Low**: Component files should export one primary component per file.

### State Management
- **High**: Game state MUST be derived from Convex queries, not duplicated in local React state.
- **High**: Optimistic updates should be avoided for critical game state (battles, inventory) to prevent desync.
- **Medium**: Form state should use controlled components with proper validation.
- **Medium**: Client-side caching should respect real-time updates from Convex.
- **Low**: useState should be minimized in favor of server state from useQuery.

### User Experience
- **High**: Loading indicators MUST be shown for async operations (attacks, equipment changes).
- **High**: Error messages MUST be displayed to users via toast notifications, not silent failures.
- **Medium**: Disabled buttons should indicate why they're disabled (e.g., "Not enough mana").
- **Medium**: Success feedback should be immediate for player actions.
- **Low**: UI should follow consistent styling patterns using Tailwind classes.

## 4. TYPESCRIPT SAFETY

### Type Strictness
- **Critical**: NEVER use `any` type for function parameters or return values in game logic.
- **High**: Use specific `Id<"tableName">` types instead of generic `string` for document IDs.
- **High**: Discriminated unions MUST use `as const` for literal types.
- **Medium**: Convex-generated types from `_generated/dataModel` should be used for document shapes.
- **Medium**: Utility types should be defined in a shared location for reuse.
- **Low**: Type imports should be separated from value imports for clarity.

### Null Safety
- **High**: ALWAYS check for null/undefined before accessing nested properties.
- **High**: Use optional chaining (`?.`) and nullish coalescing (`??`) appropriately.
- **Medium**: Function return types should explicitly indicate nullability with `| null` or `v.optional()`.
- **Medium**: Database queries that might not find data should handle the null case gracefully.

### Validator Alignment
- **Critical**: TypeScript types MUST match Convex validators exactly (e.g., `v.number()` → `number`).
- **High**: Record validators `v.record(keyType, valueType)` MUST have matching TypeScript `Record<KeyType, ValueType>`.
- **High**: Array validators `v.array(elementType)` should use `Array<T>` type annotations when declared.
- **Medium**: Return validators should match the actual return type of the handler function.

## 5. SECURITY & ANTI-CHEAT

### Authentication & Authorization
- **Critical**: ALL player-modifying mutations MUST verify the user is authenticated via `getAuthUserId()`.
- **Critical**: Players MUST only be able to modify their own data (check `player.userId === currentUserId`).
- **High**: Admin functions (if added) MUST use internal functions, never public API.
- **High**: Session validation should happen on every request, not cached client-side.
- **Medium**: Anonymous users should have limited capabilities (view leaderboard only).

### Data Validation
- **Critical**: Resource changes (health, mana, items) MUST be server-validated before persistence.
- **Critical**: Battle outcomes MUST be calculated server-side; never trust client-provided win/loss states.
- **High**: Input sanitization MUST occur for all user-provided strings (player names, guild names).
- **High**: Rate limiting should be implemented for expensive operations (battle creation, item generation).
- **Medium**: Client timestamps should be treated as untrusted; use server `Date.now()` for authoritative time.

### Exploit Prevention
- **Critical**: Check for integer overflow in experience/gold calculations (use safe number ranges).
- **Critical**: Prevent duplicate item generation by validating unique constraints.
- **High**: Validate battle state before allowing actions (player's turn, ability available, alive).
- **High**: Prevent race conditions in item trading/transfers with atomic operations.
- **Medium**: Log suspicious activities (rapid experience gain, impossible damage values) for monitoring.

## 6. PERFORMANCE OPTIMIZATION

### Query Efficiency
- **Critical**: NEVER use `.filter()` on large tables; create indexes and use `withIndex()`.
- **High**: Limit query results with `.take(n)` or pagination to prevent loading entire tables.
- **High**: Avoid N+1 query patterns; batch related data fetches when possible.
- **Medium**: Use `.unique()` instead of `.first()` when expecting exactly one result.
- **Medium**: Order queries using indexes to avoid in-memory sorting.
- **Low**: Consider caching frequently accessed static data (class definitions, item templates).

### Real-Time Updates
- **High**: Minimize the number of documents watched by queries (use specific filters).
- **Medium**: Avoid subscribing to high-frequency updates in background tabs.
- **Medium**: Debounce rapid user actions (button mashing) to prevent excessive mutations.
- **Low**: Use React.memo for components that don't need frequent re-renders.

### Database Design
- **High**: Denormalize frequently accessed data to reduce query complexity (e.g., store player total stats).
- **Medium**: Archive completed battles instead of keeping them in active `battles` table.
- **Medium**: Use background actions for heavy computations (leaderboard recalculations).
- **Low**: Monitor table sizes and implement cleanup for old/unused data.

## 7. DATA INTEGRITY & CONSISTENCY

### Transaction Boundaries
- **Critical**: Multi-step operations (battle resolution, item trade) MUST complete atomically or rollback.
- **High**: Inventory changes MUST validate item existence before and after modifications.
- **High**: Player stat calculations MUST be consistent across all code paths.
- **Medium**: Guild membership changes should update both guild and player records together.
- **Low**: Use helper functions to ensure consistency in repeated operations.

### State Machine Validation
- **Critical**: Battle state transitions MUST validate current state before advancing (can't attack when dead).
- **High**: Challenge states (pending, active, completed) MUST follow valid state transitions.
- **Medium**: Player status (active, inactive, banned) should have proper state guards.
- **Low**: Document state machines in comments for complex workflows.

### Data Consistency
- **Critical**: Calculated fields (total stats from equipment) MUST recalculate when dependencies change.
- **High**: Aggregate data (leaderboard rankings) should update in near real-time or on schedule.
- **High**: Foreign key references MUST be validated before deletion (don't delete player with active battles).
- **Medium**: Timestamps should use consistent sources (all server-side `Date.now()` or `_creationTime`).

## 8. SOCIAL FEATURES & MULTIPLAYER

### Guild System
- **High**: Guild membership MUST be validated before allowing guild-specific actions.
- **High**: Guild creation should enforce uniqueness on guild names.
- **Medium**: Guild roles (leader, member) should be checked for privileged operations.
- **Medium**: Guild invitations should prevent duplicate invites to the same player.
- **Low**: Guild disbanding should clean up all related data (members, challenges).

### Player Challenges
- **Critical**: Challenge outcomes MUST be determined by actual battle results, not player claims.
- **High**: Challenge state MUST prevent duplicate acceptances or invalid state transitions.
- **High**: Both players in a challenge MUST exist and be active.
- **Medium**: Challenge rewards should be distributed atomically (winner gets reward, loser gets nothing).
- **Low**: Challenge history should be preserved for player stats.

### Leaderboard
- **High**: Leaderboard rankings MUST be calculated from authoritative server data only.
- **Medium**: Leaderboard updates should be efficient (incremental, not full recalculation).
- **Medium**: Pagination should be implemented for leaderboards with many players.
- **Low**: Leaderboard should handle ties gracefully (consistent ordering).

### Farcaster Integration
- **High**: Farcaster profile data MUST be validated before associating with player accounts.
- **Medium**: Shared battle frames should generate valid, non-expiring URLs.
- **Medium**: Social features should degrade gracefully if Farcaster is unavailable.
- **Low**: Battle share data should include relevant context (winner, battle stats).

## 9. ERROR HANDLING & DEBUGGING

### Error Messages
- **High**: User-facing errors MUST be clear and actionable (e.g., "Not enough mana" instead of "Invalid state").
- **High**: Internal errors should be logged with sufficient context for debugging.
- **Medium**: Error responses should include error codes for client-side handling.
- **Low**: Stack traces should not be exposed to end users in production.

### Logging
- **Medium**: Log critical game events (level-ups, rare item drops, challenge completions) for analytics.
- **Medium**: Log authentication failures and suspicious activities for security monitoring.
- **Low**: Debug logs should be removable in production builds.
- **Low**: Log messages should include relevant IDs (playerId, battleId) for tracing.

### Graceful Degradation
- **High**: Frontend MUST handle backend errors without crashing the UI.
- **Medium**: Missing optional data (Farcaster profiles) should not break core features.
- **Medium**: Retry logic should be implemented for transient failures.
- **Low**: Offline state should be communicated clearly to users.

## 10. CODE QUALITY & MAINTAINABILITY

### Code Organization
- **Medium**: Related functions should be grouped in the same file (battles, players, items, social).
- **Medium**: Complex algorithms should be extracted into pure helper functions with tests.
- **Medium**: Magic numbers should be extracted into named constants.
- **Low**: Files should have clear single responsibilities.
- **Low**: Imports should be organized (external libraries, then internal modules).

### Documentation
- **Medium**: Complex game mechanics should have explanatory comments.
- **Medium**: Public API functions should have JSDoc comments describing purpose and parameters.
- **Low**: Non-obvious business logic should be documented inline.
- **Low**: Schema changes should be documented with migration notes.

### Testing Considerations
- **High**: Game logic functions should be pure when possible for easier testing.
- **Medium**: Edge cases (zero health, max level, empty inventory) should be handled explicitly.
- **Medium**: Validation functions should be testable in isolation.
- **Low**: Mock data should be available for development/testing.

### Dependency Management
- **Medium**: Third-party dependencies should be minimized to reduce bundle size.
- **Medium**: Security vulnerabilities in dependencies should be addressed promptly.
- **Low**: Unused dependencies should be removed from package.json.

## 11. GAME-SPECIFIC BUSINESS RULES

### Balancing Constraints
- **High**: Experience gain per battle MUST be capped to prevent exploits (e.g., max 100 XP per battle).
- **High**: Daily resets MUST occur at consistent times to ensure fairness.
- **Medium**: Item drop rates should follow configured rarity distributions.
- **Medium**: Ability power scaling should not create one-shot scenarios at low levels.
- **Low**: Class balance should be monitored and adjusted based on player data.

### Economy Rules
- **High**: Currency/resource generation MUST have server-side validation and limits.
- **Medium**: Item marketplace prices should prevent economic exploits (negative prices, overflow).
- **Medium**: Trading between players should be logged for audit trails.
- **Low**: Resource sinks should exist to prevent infinite accumulation.

### Progression Gates
- **Medium**: Level requirements for content should be enforced server-side.
- **Medium**: Tutorial or onboarding state should guide new players appropriately.
- **Low**: Achievement systems should track progress accurately.

## 12. CONVEX-SPECIFIC BEST PRACTICES

### File Storage
- **High**: Use `ctx.storage` for binary assets (images, files), not database fields.
- **Medium**: Validate file types and sizes before storage.
- **Medium**: Clean up orphaned storage files when associated records are deleted.
- **Low**: Generate signed URLs for secure file access.

### Scheduled Jobs
- **High**: Cron jobs MUST be idempotent (safe to run multiple times).
- **Medium**: Daily resets should use `crons.interval` with proper timing.
- **Medium**: Background cleanup jobs should batch operations to avoid timeouts.
- **Low**: Scheduled job failures should be logged and monitored.

### HTTP Endpoints
- **High**: HTTP endpoints MUST validate authentication tokens manually (no automatic auth).
- **Medium**: REST endpoints should follow RESTful conventions for consistency.
- **Medium**: CORS headers should be configured appropriately for allowed origins.
- **Low**: HTTP actions should set appropriate status codes and headers.

## VALIDATION CHECKLIST FOR CODE REVIEWS

When reviewing code, Kluster.ai should verify:

1. **Security**: ✓ Authentication checks present? ✓ Input validation? ✓ Authorization verified?
2. **Data Integrity**: ✓ Server-side calculations? ✓ Atomic operations? ✓ Consistent state transitions?
3. **Performance**: ✓ Indexed queries? ✓ Limited result sets? ✓ No N+1 patterns?
4. **Type Safety**: ✓ No `any` types? ✓ Validators match types? ✓ Null checks present?
5. **Game Logic**: ✓ Balanced mechanics? ✓ Anti-cheat measures? ✓ Deterministic results?
6. **User Experience**: ✓ Error handling? ✓ Loading states? ✓ Clear feedback?
7. **Code Quality**: ✓ Clear naming? ✓ Documented complexity? ✓ DRY principle followed?

## SEVERITY GUIDELINES

- **Critical (P0-P1)**: Security vulnerabilities, data corruption risks, game-breaking exploits
- **High (P2)**: Performance issues, poor user experience, anti-pattern usage
- **Medium (P3)**: Code quality issues, maintainability concerns, minor bugs
- **Low (P4-P5)**: Style inconsistencies, documentation gaps, optimization opportunities
