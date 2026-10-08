# Repository Guidelines

## Canonical Agent Guide
- `AGENTS.md` is the source of truth for GPT-5.4/Codex work in this repo.
- `CLAUDE.md` and `GEMINI.md` are thin compatibility wrappers. Update them only when agent-specific behavior changes.
- When architecture, workflow, or validation guidance changes, update `AGENTS.md` first, then adjust wrappers if needed.

## Project Structure & Module Ownership
- `PungentRoots/`: SwiftUI app sources.
  - `PungentRootsApp.swift`: boots the live `AppEnvironment` and injects it into the root scene.
  - `ContentView.swift`: thin navigation shell; owns `@State private var flowModel = ScanFlowModel()`.
  - `Camera/`:
    - `CaptureTypes.swift`: shared `CapturePayload`, `CaptureState`, and `CaptureReadiness` used across capture and UI layers.
    - `AutoCaptureController.swift`: orchestration layer that selects VisionKit `DataScannerViewController` when available and falls back to the legacy AVFoundation/Vision path.
    - `LiveCaptureController.swift`: legacy capture implementation with readiness and zoom heuristics. Keep this behind shared capture-domain types.
  - `OCR/`: OCR configuration and document camera helpers.
  - `Services/`:
    - `AppEnvironment.swift`: shared dependency container. It owns services and returns typed `ScanAnalysis` values from analysis entrypoints.
    - `ScanFlowModel.swift`: `@MainActor @Observable` screen-level orchestration for capture, analysis, cancellation, UI-test preview state, and rescan flow.
    - `TextAcquisitionService.swift`: converts capture payloads into normalized text inputs for detection.
    - `MetricReporter.swift`: MetricKit subscriber for performance telemetry.
  - `Detection/`: bundled dictionary loading, rule-based matching, and scoring thresholds.
  - `Models/`:
    - `Scan.swift`: core detection result, match, verdict, and persistence-facing model types.
    - `ScanAnalysis.swift`: shared analysis payload passed between services, views, previews, and tests.
  - `Utilities/`: normalization and regex helpers.
  - `Views/`:
    - `ScanCameraModuleView.swift`: capture surface, status badge, and capture error presentation.
    - `ScanResultSectionView.swift`: processing/result container.
    - `DetectionResultView.swift`: verdict card, transcript disclosure, and rescan affordance.
    - `AdaptiveGlass.swift`: iOS 26 Liquid Glass helpers with pre-iOS 26 material fallbacks.
    - Supporting overlays, empty states, and shared badges.
  - `Resources/`: localization strings and the bundled detection dictionary.
- `PungentRootsTests/`: unit coverage using Apple’s `Testing` framework.
- `PungentRootsUITests/`: scenario-based UI coverage, including settings, transcript disclosure, rescan flow, and accessibility-size checks.
- `Scripts/run-tests.sh`: canonical local/CI test wrapper.

## Non-Negotiables
- Minimum deployment target stays `iOS 18.5`.
- iOS 26 APIs are additive only. Guard all Liquid Glass and newer UI behavior with availability checks and ship functional fallbacks below iOS 26.
- Keep all OCR and detection processing on-device. Do not add network calls without explicit approval.
- Do not leak `LiveCaptureController`-specific types into SwiftUI. Shared UI state must flow through `CapturePayload`, `CaptureState`, and `CaptureReadiness`.
- `ContentView` stays thin. Put screen orchestration in `ScanFlowModel`, not in view bodies.
- `AppEnvironment` is a service container and analysis entrypoint, not a screen view model.
- Use `ScanAnalysis` instead of ad hoc tuples for analysis results.
- Cancel stale analysis work before starting rescans or stopping the screen.

## Build, Test, and Validation Commands
- `xed .` or `open PungentRoots.xcodeproj`: open the project in Xcode.
- `xcodebuild -scheme PungentRoots -destination "platform=iOS Simulator,OS=18.6,name=iPhone 16 Pro" build`: deterministic simulator build.
- `xcodebuild test -scheme PungentRoots -destination "platform=iOS Simulator,OS=18.6,name=iPhone 16 Pro"`: full test run.
- `Scripts/run-tests.sh`: preferred wrapper for local and CI validation.

## iOS Workflow Expectations
- Inspect the full scan path before editing behavior: `ContentView` -> `ScanFlowModel` -> `AutoCaptureController`/`CaptureTypes` -> `TextAcquisitionService` -> `AppEnvironment.analyzeAsync` -> result views.
- Prefer small dedicated SwiftUI views with stable trees and explicit state boundaries.
- Keep async work and side effects out of view bodies. Start and cancel work from `ScanFlowModel`.
- When updating capture behavior, validate both VisionKit-supported and forced-legacy paths.
- When touching glass styling, keep it focused on high-value chrome: badges, compact controls, settings header, and primary actions. Avoid placing dense transcript content or the live camera preview inside heavy glass treatments.

## Preferred Tools & References
- Use the Apple docs MCP/context7 tooling for current SwiftUI, VisionKit, AVFoundation, Observation, and Liquid Glass guidance.
- Codex users should prefer the Build iOS Apps skills when relevant:
  - `build-ios-apps:swiftui-view-refactor`
  - `build-ios-apps:swiftui-ui-patterns`
  - `build-ios-apps:swiftui-liquid-glass`
  - `build-ios-apps:swiftui-performance-audit`
  - `build-ios-apps:ios-debugger-agent`
- Capture citation links in PR notes when behavior depends on recent Apple API guidance.

## Coding Style
- Swift source uses 4-space indentation, no trailing whitespace, and `guard` for early exits.
- Keep functions under roughly 80 lines. Extract helpers or subviews when bodies grow.
- Types use UpperCamelCase; methods and properties use lowerCamelCase.
- Prefer `@MainActor` or `MainActor.run` when mutating observable UI state from async work.
- Add `///` comments only where logic is not obvious from the code.

## Testing Guidelines
- Default to the `Testing` framework with behavior-focused `@Test` names.
- Add or update tests when changing:
  - detection scoring or dictionary behavior
  - normalization or OCR heuristics
  - `ScanFlowModel` state transitions
  - capture-state mapping or overlay severity behavior
- Maintain scenario-oriented UI tests for settings presentation, transcript disclosure, rescan behavior, and accessibility sizing.
- Keep UI-test launch hooks working:
  - `--ui-test-disable-capture`
  - `--ui-test-preview-result`
- If a camera/OCR change cannot be covered automatically, document the manual runbook in `PLAN.md`.

## Documentation & Process
- Update `README.md` when architecture entry points, developer workflow, or platform strategy changes.
- Update `PLAN.md` when manual validation steps or device coverage expectations change.
- Bump the detection dictionary `version` string and record the rationale in commit/PR text whenever the JSON changes.
- Before merging structural work, confirm `AGENTS.md`, `README.md`, and `PLAN.md` match the implementation.

## Commit & Pull Request Guidelines
- Use imperative, present-tense commit summaries with optional scopes, e.g. `[Camera] Unify capture state types`.
- Keep the first commit line at or below 72 characters.
- PRs should include:
  - purpose summary
  - validation evidence (`Scripts/run-tests.sh`, targeted simulator checks, screenshots if relevant)
  - targeted devices or simulator configurations
  - accessibility notes
  - dictionary version rationale when applicable

## Security & Privacy
- Strip sensitive ingredient text from debug logs.
- Dispose of intermediate scan images after they are no longer needed.
- Keep privacy copy accurate: OCR and detection stay on-device, with no network dependency.
