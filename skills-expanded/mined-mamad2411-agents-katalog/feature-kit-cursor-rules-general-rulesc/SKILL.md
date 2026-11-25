# Cursor Rules for Feature Kit

## General Principles

1. **Simplicity First**: Always prioritize simple, straightforward implementations. Avoid overcomplicating solutions. If a simple approach works, use it.

2. **No Emojis**: Do not use emojis anywhere in the codebase, documentation, commit messages, or any project files.

## Library and Dependency Management

3. **Check Existing Libraries First**: Before creating any custom implementation, check if a library already exists that solves the problem. Search npm, check package.json, and verify if the functionality is available in already installed packages.

4. **Use @uidotdev/usehooks**: Always check and use hooks from `@uidotdev/usehooks` before creating custom React hooks. Available hooks include:

   - useBattery, useClickAway, useCopyToClipboard, useCounter, useDebounce, useDefault, useDocumentTitle, useFavicon, useGeolocation, useHistoryState, useHover, useIdle, useIntersectionObserver, useIsClient, useIsFirstRender, useList, useLocalStorage, useLockBodyScroll, useLongPress, useMap, useMeasure, useMediaQuery, useMouse, useNetworkState, useObjectState, useOrientation, usePreferredLanguage, usePrevious, useQueue, useRenderCount, useRenderInfo, useScript, useSessionStorage, useSet, useThrottle, useToggle, useVisibilityChange, useWindowScroll, useWindowSize

5. **Read package.json**: Always read the package.json file to understand what libraries are already available before implementing new functionality.

## Documentation

6. **Minimal Documentation**: Only create documentation when explicitly requested by the user. Do not proactively create README files, documentation files, or extensive comments unless asked.

## Commit Messages

7. **Conventional Commits**: When asked to create commit messages, always follow the Conventional Commits specification:
   - Format: `<type>(<scope>): <subject>`
   - Types: feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert
   - Keep subject line under 72 characters
   - Use imperative mood ("add" not "added" or "adds")

## Code Quality

8. **Business Logic Only**: The codebase should only contain business logic and standard React/JavaScript patterns. All common functionality should use established npm libraries.

9. **Feature-Based Structure**: Follow the feature-based folder structure. App features (not content features) should be organized in `/features` directory with their own components, hooks, and utilities.

10. **TypeScript**: Use TypeScript strictly. Avoid `any` types when possible. Use proper type definitions.

## Implementation Guidelines

11. **Keep It Simple**: Do not overcomplicate implementations. Prefer straightforward, readable code over clever but complex solutions.

12. **Consistency**: Follow existing patterns in the codebase. Maintain consistency with naming conventions, file structure, and code style.
