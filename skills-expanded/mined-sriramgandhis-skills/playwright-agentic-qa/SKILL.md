# 🎭 PLAYWRIGHT AGENTIC QA: AUTONOMOUS E2E VERIFICATION

This skill connects the **SUPERPOWERS** controller to reality. It allows the Antigravity Engine to autonomously open browsers, click buttons, and verify visual/interaction states using Playwright.

## ⚖️ CORE PHILOSOPHY
- **No Manual Testing:** If a human has to click it to verify it works, the verification loop failed.
- **Agentic Eyes:** Use the Playwright CLI or MCP server to navigate the accessibility tree deterministically.
- **TDD Parity:** E2E tests are written *before* the UI is finalized, guaranteeing the logic behaves as expected across Chromium, Firefox, and Safari.

## 🛠️ OPERATING RULES
1. **CLI Verification:** When tasked with testing a flow, use `playwright-cli open <url>` and subsequent commands (`type`, `press`, `screenshot`) to autonomously verify the UI.
2. **SUPERPOWERS Integration:** The `SUPERPOWERS` controller MUST use Playwright for the `GREEN` phase of UI development.
3. **Session Monitoring:** In complex flows, utilize `playwright-cli show` to spawn the visual dashboard for real-time tracking.
4. **Locators:** Always use resilient web-first assertions (e.g., `getByRole`, `getByPlaceholder`) instead of brittle CSS selectors.

## 🚀 USAGE EXAMPLES
- `playwright-cli open http://localhost:3000`
- `playwright-cli screenshot`
- `playwright-cli click "Add to Cart"`
