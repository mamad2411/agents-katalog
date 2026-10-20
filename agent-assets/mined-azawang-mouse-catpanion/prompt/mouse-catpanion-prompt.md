You are helping me scaffold a macOS desktop MVP called "Mouse Companion".

Goal:
Build the initial project skeleton for a macOS desktop companion app that detects mouse hover, reads nearby text, falls back to OCR if direct text is unavailable, and shows a lightweight popup near the cursor with at most 3 short sentences. The app should feel low-interruption, playful, and ambient.

Product summary:
- Target users: macOS desktop users.
- Main interaction: when the cursor hovers in one place for 30–60 seconds, trigger content recognition and generate a short response.
- Response types: translation, fun fact / knowledge snippet, cold joke, light companion-like message.
- Popup appears near the cursor.
- If the cursor hovers over the popup, show 👍 and 👎 buttons.
- Allow low-frequency proactive “heartbeat” popup, but suppress it during high activity.
- Settings page should include:
  - language
  - start / pause
  - add API
  - API usage visualization (ring/progress style)
- Output must never exceed 3 sentences.
- First version is macOS only.
- Recognition priority: direct text if available, OCR fallback.
- First version should be architected to support one LLM provider first, but keep provider abstraction for future expansion.

Technical constraints:
- macOS only.
- Desktop app, not web-only.
- Must support floating overlay / popup behavior.
- Must request and handle macOS permissions cleanly, especially screen recording and possibly accessibility if needed for implementation on macOS.
- Avoid full-screen continuous capture. Only use minimal local region capture when needed.
- Store settings and lightweight usage/feedback data locally.
- Keep the architecture simple and modular for an MVP.
- Do not implement long conversations, cloud accounts, voice, or complex personality systems.

Important implementation preference:
- I care more about a clean project structure and clear module boundaries than feature completeness.
- Please scaffold first, with mock data / mock LLM response where appropriate.
- Do not try to fully implement every feature in one pass.
- The first working milestone should be:
  1. app launches,
  2. hover timer logic works,
  3. a popup can appear near cursor,
  4. popup shows a mock short response,
  5. settings window exists.

What I want you to produce:
1. Recommend the best tech stack for this macOS MVP and briefly justify it.
2. Create the project folder structure.
3. Create the initial files with minimal runnable code.
4. Add clear TODO markers for unimplemented parts.
5. Add a provider abstraction layer for future LLM integration.
6. Add a service boundary for text capture / OCR.
7. Add a simple local settings store.
8. Add a simple usage tracker model.
9. Add a README with setup, run instructions, and next milestones.

Architecture requirements:
- Organize primarily by feature/module, not by generic layers.
- Suggested modules may include:
  - app-shell
  - hover-monitor
  - text-capture
  - ocr
  - llm
  - popup-overlay
  - feedback
  - heartbeat
  - settings
  - usage-tracking
- Keep code easy to extend.
- Prefer a structure where each feature owns its UI + logic as much as possible.

Done when:
- The project compiles or runs locally.
- There is a visible app shell.
- There is a mock popup near cursor or simulated popup.
- There is a settings window/page with placeholder controls.
- The codebase is scaffolded for the next vertical slices.
- README explains what is implemented vs placeholder.

Process:
- First inspect the repo and propose the stack + folder structure.
- Then scaffold only the minimum viable architecture and files.
- Use mock implementations where real macOS integrations are not yet built.
- Do not overbuild.
- Do not add unnecessary dependencies.
- Keep the MVP narrow and reviewable.

Before writing large amounts of code:
- Show the proposed stack and folder tree first.
- Then proceed with implementation.