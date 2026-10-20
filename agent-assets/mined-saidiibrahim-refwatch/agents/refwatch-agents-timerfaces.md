# AGENTS.md

## Scope
Timer Faces subsystem for the watch app. Applies to `RefWatchWatchOS/Core/Components/TimerFaces/`.

## Key Types
- `TimerFaceModel` protocols expose read‑only state (`matchTime`, `periodTimeRemaining`, etc.) and minimal actions (`pauseMatch`, `resumeMatch`, `startHalfTimeManually`).
- `TimerFaceStyle` enumerates available faces; default is `standard`. Persist selection via `@AppStorage("timer_face_style")`.
- `TimerFaceFactory` returns a SwiftUI view for a given style and model.
- `StandardTimerFace` mirrors the previous inline timer UI; `ProStoppageFace` provides an alternate layout.

## Adding a New Face
1) Add a new case to `TimerFaceStyle` and provide a display name/icon if applicable.
2) Implement a SwiftUI view for the face. Views must accept a `TimerFaceModel` (or minimal protocol) and read state only; actions call the model’s methods.
3) Register the new face in `TimerFaceFactory`.
4) Ensure `TimerFaceSettingsView` can select it (no hard‑coded assumptions).

## Guidelines
- No timers or state machines in the face view; the model owns timekeeping.
- Keep layout performant and glanceable; prefer concise typography.
- Use haptics sparingly and via adapters (not directly in the face view).
- Maintain accessibility (Dynamic Type where possible; avoid tiny tap targets).

## Testing
- Unit test face‑specific formatting/helpers. For visuals, rely on SwiftUI previews or snapshot tests (if present) rather than logic in the view.

