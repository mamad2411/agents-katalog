---
name: 1password-troubleshooting
description: "Guidelines for troubleshooting the 1Password Chrome Extension, covering autofill issues and biometric unlock."
---

# 1Password Chrome Extension Troubleshooting

The 1Password Chrome Extension is the primary bridge between the browser and the 1Password desktop app. 

## Common Issues & Resolutions

### 1. Autofill Failing
If the 1Password icon does not appear in login or credit card fields:
1. **Check Page Structure:** Ensure the `<input>` fields use standard attributes (e.g., `type="password"`, `autocomplete="current-password"`). 1Password's heuristic engine relies on standard HTML forms.
2. **Shadow DOM:** 1Password generally supports Shadow DOM, but heavily customized or nested web components can occasionally obscure fields from the extension.
3. **Right-Click Fallback:** If the inline menu fails, users can right-click the field and select "1Password" -> "Autofill" from the context menu.

### 2. Desktop App Integration
The browser extension relies on the "1Password Desktop App Integration" to enable biometric unlock (Touch ID, Windows Hello) and to sync the lock state.
*   **Symptom:** Extension asks for the Master Password instead of Touch ID, or refuses to unlock.
*   **Resolution:** 
    1. Ensure the 1Password Desktop app is running.
    2. Check Settings -> "Integrate with 1Password app" in the extension.
    3. If it hangs, completely restart the browser and the desktop app.
