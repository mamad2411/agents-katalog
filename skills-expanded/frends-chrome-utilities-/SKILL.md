# Frends Chrome Utilities - AI Rules

You are an advanced AI assistant developing new features for the `frends-chrome-utilities` Chrome Extension.

## Core Rules
1. **Read `ARCHITECTURE.md` Priority**: Before writing any new extension feature, you MUST read the `ARCHITECTURE.md` file in the root directory. It contains critical information about the SPA navigation structure and DOM extraction rules specific to the Frends UI.
2. **Vanilla JS Only**: Do not introduce NPM loops, Webpack configurations, or third-party React libraries. All files run natively as V3 Content Scripts `(chrome.storage.local)`, Service Workers `(chrome.runtime.onMessage)`, and vanilla CSS.
3. **No Automatic Browser Testing**: Do not attempt to use headless browser testing sub-agents to "validate" the unpacked Chrome Extension. E2E browser automation will fail to load local unpacked extensions correctly. After finishing your implementation, you must provide full manual testing steps in a markdown artifact for the user to complete manually.
4. **Z-Index Portal Strategy**: When creating floating UI panels or overlays that sit in front of the process editor canvas, you MUST inject them dynamically into `document.body` and calculate positioning bounds via `#your-trigger-button.getBoundingClientRect()`. NEVER inject them natively as children of the top navigation bar, because Frends' z-index stacking layers will trap the child element underneath the `<canvas>` viewport.
5. **Namespaced CSS**: Always aggressively prefix custom HTML IDs and Classes (e.g. `.frends-custom-feature-wrapper`) so you do not break the actual application's native selectors.
