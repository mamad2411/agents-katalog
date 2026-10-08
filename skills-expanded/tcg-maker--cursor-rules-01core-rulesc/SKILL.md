---
description: A coding guide that makes you a great engineer, built into your soul, gene and blood. The rule MUST be applied to everything
globs: 
alwaysApply: true
---
# Core Programming Principles

## Goal

Create maintainable, reusable, and testable code by adhering to principles of separation of concerns, clear responsibilities, and manageable module size. Avoid overly complex "god objects" or files.

> **Note:** Examples below are illustrative only and not binding to any specific language or framework.

## Core Principles

1.  **Single Responsibility Principle (SRP):**
    *   Each module, class, or function should ideally have one primary responsibility or represent one distinct piece of logic or functionality.
    *   **Example:** Instead of one large `DataProcessor`, separate concerns into `DataLoader`, `DataTransformer`, `DataExporter`, etc.

2.  **Identify Logical Sections:**
    *   Break down complex systems into smaller, self-contained logical sections. Each section often becomes a candidate for its own module or class.
    *   **Example:** The input handler, the processing engine, and the output writer are all distinct sections that can be separated.

3.  **Extract Domain Logic/State:**
    *   When a module becomes responsible for managing a significant amount of state and logic related to a specific *domain* (like user management, data processing, or logging), extract that state and logic into a dedicated module or service.
    *   Modules related to that domain should then interact with the service instead of relying on a parent or global state.
    *   **Example:** `userSession` state/logic moved to `UserSessionService`; logging logic moved to `Logger`.

4.  **Shared Constants for API Communications:**
    *   Always use shared constants for API communications, and never use string literals to create coupling between client and server.
    *   Create centralized constant files that define error codes, API endpoints, status codes, and other shared values.
    *   Both client and server should reference the same logical constants to ensure consistency and maintainability.
    *   **Example:** Instead of `if (error.contains('Account is inactive'))`, use `if (ErrorCodes.shouldLogout(errorCode))` where `ErrorCodes.ACCOUNT_INACTIVE` is defined in a shared constants file.
    *   **Benefits:** Type safety, refactoring support, single source of truth, prevents typos, easier testing.

5.  **Limit Module Size:**
    *   Aim to keep files and modules reasonably sized. If a file grows much larger, it's often a sign it's doing too much and should be split further or have logic extracted to smaller units as described in [98.split-large-files.mdc](mdc:.cursor/rules/98.split-large-files.mdc)

6.  **Function/Component Search and Documentation:**
    *   Before creating any new function or component, you must check and update `readme/structure.md` as described in [01.search-codebase.mdc](mdc:.cursor/rules/01.search-codebase.mdc)
    *   This ensures no duplication and that all logic is discoverable and documented.
    *   If a function or component is deleted, you must also remove its entry from `readme/structure.md` to keep the documentation accurate.
