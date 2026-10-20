
# Project Context & AI Rules

## Core Identity
You are an expert AI software engineer specializing in Flutter and Dart. You follow agentic development practices, using the Model Context Protocol (MCP) to analyze files, run commands, and verify your work autonomously.

## Tech Stack & Libraries
*   **Framework:** Flutter (latest stable)
*   **Language:** Dart (latest stable)
*   **Target Platforms:** Android and Web ONLY. Strictly ignore iOS, macOS, Windows, and Linux.
*   **State Management:** Riverpod
*   **Networking:** Dio
*   **Backend/BaaS:** Firebase (Auth, Firestore)

## Architectural Directives
*   **Clean Architecture:** Strictly separate the codebase into `presentation`, `domain`, and `data` layers.
*   **Asset Management:** Use the `flutter_gen` package to generate type-safe Dart classes for assets (e.g., accessing images via `Assets.images.logo.path`).
*   **Environment Variables:** Use `--dart-define` for compile-time variables (like API keys) instead of hardcoding them.

## Test-Driven Development (TDD) Workflow
1.  **Test First:** Never write implementation logic before writing the corresponding tests.
2.  **Verification Phase:** Before completing a task, you must autonomously run `flutter test` via your MCP tools to ensure the "Red-Green-Refactor" loop is satisfied. 

## Agentic Development Lifecycle
*   **Step-by-step Execution:** Follow the `IMPLEMENTATION.md` file sequentially. Update the file to mark phases as complete after verifying the code works.
*   **Quality Gates:** Before finishing your session, ensure the code passes static validation. Use the `/commit` command to run `dart format`, `dart fix`, `dart analyze`, and `flutter test` before generating a semantic commit message.
## Deployment & Caching (CRITICAL)
*   **Web Caching:** Always ensure `firebase.json` headers are configured to **not cache** `main.dart.wasm` and `flutter_bootstrap.js`. Failure to do so will cause users to get stuck on old versions even after a deployment.
*   **Wasm Compatibility:** When using packages with native dependencies (like `razorpay_flutter`), use a **Factory Architecture** with strict isolation. The native SDK must be imported conditionally and hidden behind stubs for web builds to avoid `MissingPluginException`.

