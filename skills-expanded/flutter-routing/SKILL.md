---
name: "flutter-routing"
description: "Declarative routing and navigation for Flutter using GoRouter and AutoRoute. Use when implementing navigation guards, nested routes, type-safe routing, or deep link handling."
metadata:
  last_modified: "2026-03-12 11:18:17 (GMT+8)"
---

# Flutter Routing & Navigation Architecture

## Goal
Establish a robust, scalable, and declarative navigation system for Flutter applications. This skill ensures developers can correctly choose and implement industry-standard routing solutions—GoRouter for official declarative support or AutoRoute for type-safe code generation—while maintaining clean URL handling, deep-link support, and complex nested navigation architectures.

## Process

### 🚀 High-Level Workflow
Navigating routing decisions requires understanding the project's scale and requirements for type safety versus boilerplate.

### Phase 1: Choosing Your Framework
Determine the best fit for your team's workflow:
- **GoRouter**: The official, widely-supported declarative solution. Best for standard web-compatible routing and ease of external tool integration (like Sentry).
- **AutoRoute**: Compile-time type-safe routing. Best for massive apps where manual URL string management becomes a liability and strong type guarantees are prioritized.

### Phase 2: Implementation Details
Consume these specialized architectural reference resources for deep implementation guidance:
- [GoRouter & Persistent Navigation](./references/routing-and-go-router.md) - Official declarative patterns, `StatefulShellRoute` for tabs, and redirection guards.
- [AutoRoute & Type-Safe Navigation](./references/auto-route.md) - Code generation patterns (`v11.x`), `@RoutePage` annotations, and global guards.

---

## 📚 Documentation Library
Refer to these detailed guides to implement specific routing features:

- [🔗 GoRouter Implementation Guide](./references/routing-and-go-router.md)
- [📦 AutoRoute Best Practices](./references/auto-route.md)

## Constraints
* **Declarative First**: Prohibit legacy imperative `Navigator.push` patterns in new architectures. All navigation should be addressable via URLs or generated Route objects.
* **Architecture Consistency**: Never mix GoRouter and AutoRoute in the same application module.
* **Web Compatibility**: Ensure all routing logic maintains browser URL bar synchronization and back-button behavior integrity.
* **Safe Parameters**: Never pass massive Object instances directly through URL parameters; pass unique identifiers and fetch data at the target destination.
