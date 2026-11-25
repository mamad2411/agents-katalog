---
name: react-preferences-persistence-pattern
description: |
  Fix React user preferences not persisting after page reload when loaded from database.
  Use when: (1) Settings load into state but don't appear in UI after reload, (2) User
  preferences exist in database but UI shows defaults, (3) Accessibility settings or
  theme preferences not applied despite being saved, (4) E2E tests fail expecting
  persisted settings. Covers React useEffect patterns for loading async data and
  applying DOM changes separately, preventing application during loading state.
author: Claude Code
version: 1.0.0
date: 2026-01-25
---

# React Preferences Persistence Pattern

## Problem

User preferences are successfully saved to the database and loaded into React state,
but they're not applied to the UI after page reload. Settings appear correct in the
database but the UI shows default values or doesn't reflect the saved preferences.

Common symptoms:
- Accessibility settings (high contrast, font size) not applied on page load
- Theme preferences revert to default despite being saved
- Language/locale settings don't persist across page reloads
- E2E tests fail when verifying settings persistence

## Context / Trigger Conditions

**When this occurs:**
- After implementing user preferences with database persistence
- Settings save successfully but don't apply after page refresh
- React state shows correct values but DOM doesn't reflect them
- useEffect loads data but UI remains unchanged

**Typical scenario:**
```typescript
// ❌ BROKEN: Loads settings but never applies them to DOM
useEffect(() => {
  loadSettings(); // Updates state but DOM stays default
}, [loadSettings]);
```

**Error manifestations:**
- E2E test failures: "Expected element to have class 'high-contrast' but received ''"
- Visual regression: UI always shows defaults despite database containing preferences
- User complaints: "My settings don't save"

## Solution

### Pattern: Separate Loading and Application Effects

Use two distinct useEffect hooks:
1. **Loading Effect**: Fetch data from database/API and update state
2. **Application Effect**: Apply state changes to DOM, triggered by state changes

```typescript
const [settings, setSettings] = useState({
  highContrast: false,
  fontSize: "base",
  reduceMotion: false,
});
const [loading, setLoading] = useState(true);

// Effect 1: Load settings from database
useEffect(() => {
  const loadSettings = async () => {
    setLoading(true);
    try {
      const result = await getAccessibilitySettings();
      if (result.success) {
        setSettings(result.settings);
      }
    } finally {
      setLoading(false);
    }
  };
  loadSettings();
}, []);

// Effect 2: Apply settings to DOM whenever they change
useEffect(() => {
  if (!loading) {
    applyAccessibilitySettings(settings);
  }
}, [settings, loading]);
```

### Why This Works

1. **Initial Load**: First effect fetches from database, updates state
2. **State Change Trigger**: When `setSettings()` updates state, second effect runs
3. **Loading Guard**: `if (!loading)` prevents applying default values before load completes
4. **Save Trigger**: When user clicks save, state updates trigger application automatically

### Complete Implementation

```typescript
"use client";

import { useState, useEffect, useCallback } from "react";

export function AccessibilitySettings() {
  const [settings, setSettings] = useState({
    highContrast: false,
    fontSize: "base" as "sm" | "base" | "lg" | "xl",
    reduceMotion: false,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  // Load settings from database
  const loadSettings = useCallback(async () => {
    setLoading(true);
    try {
      const result = await getAccessibilitySettings();
      if (result.success) {
        setSettings(result.settings);
      }
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadSettings();
  }, [loadSettings]);

  // Apply settings to DOM whenever they change (after load or after save)
  useEffect(() => {
    if (!loading) {
      applyAccessibilitySettings(settings);
    }
  }, [settings, loading]);

  const handleSave = async () => {
    setSaving(true);
    try {
      const result = await updateAccessibilitySettings(settings);
      if (result.success) {
        // Settings already in state, application effect will trigger automatically
        toast.success("Settings updated");
      }
    } finally {
      setSaving(false);
    }
  };

  const applyAccessibilitySettings = (settings: typeof settings) => {
    const root = document.documentElement;

    // High contrast
    if (settings.highContrast) {
      root.classList.add("high-contrast");
    } else {
      root.classList.remove("high-contrast");
    }

    // Font size
    root.classList.remove("font-size-sm", "font-size-base", "font-size-lg", "font-size-xl");
    if (settings.fontSize !== "base") {
      root.classList.add(`font-size-${settings.fontSize}`);
    }

    // Reduce motion
    if (settings.reduceMotion) {
      root.classList.add("reduce-motion");
    } else {
      root.classList.remove("reduce-motion");
    }
  };

  if (loading) {
    return <LoadingSpinner />;
  }

  return (
    <div>
      {/* Settings UI */}
      <Button onClick={handleSave} disabled={saving}>
        Save
      </Button>
    </div>
  );
}
```

## Verification

### Manual Testing
1. Change a setting and save
2. Refresh the page
3. Setting should be applied immediately (not defaults)
4. Check browser DevTools: `document.documentElement.className` should show applied classes

### E2E Test Pattern
```typescript
test('should preserve accessibility settings after page reload', async ({ page }) => {
  // Enable high contrast
  const highContrastSwitch = page.locator('button[role="switch"]#highContrast');
  await highContrastSwitch.click();

  // Save
  const saveButton = page.locator('button').filter({ hasText: /save/i });
  await saveButton.click();

  // Wait for save to complete
  await page.waitForTimeout(1000);

  // Reload page
  await page.reload();
  await page.waitForLoadState('networkidle');

  // Verify setting persisted
  const html = page.locator('html');
  await expect(html).toHaveClass(/high-contrast/);

  // Verify switch state
  const reloadedSwitch = page.locator('button[role="switch"]#highContrast');
  await expect(reloadedSwitch).toHaveAttribute('aria-checked', 'true');
});
```

## Example: Language/Locale Switching

For preferences that require page navigation (like language/locale changes):

```typescript
const handleSave = async () => {
  setSaving(true);
  try {
    const result = await updateLanguage({ locale: selectedLocale });
    if (result.success) {
      toast.success("Language updated");
      // Navigate to new locale URL with full page reload
      const segments = window.location.pathname.split('/');
      segments[1] = selectedLocale; // Replace locale (first segment after /)
      const newPath = segments.join('/');
      window.location.href = newPath; // Full reload ensures all i18n updates
    }
  } catch (error) {
    toast.error("Failed to update language");
    setSaving(false);
  }
};
```

**Why `window.location.href`?**
- next-intl router's `push()` with `{ locale }` parameter doesn't reliably trigger navigation
- Full page reload ensures all i18n contexts update properly
- Server components re-render with new locale
- Middleware applies correct locale prefix

## Notes

### Best Practices from React Docs

1. **You Might Not Need an Effect**: If you can calculate something during render, you don't need an Effect. Use Effects only for synchronizing with external systems (database, DOM, browser APIs).

2. **Loading State Guards**: Always check loading state before applying DOM changes to prevent flicker from default → loaded values.

3. **Cleanup Functions**: For event listeners or subscriptions, return cleanup functions from useEffect to prevent memory leaks.

4. **Dependencies**: Include all reactive values used inside the effect in the dependency array (or use `useCallback` for functions).

### Common Mistakes

❌ **Applying settings only on save** (missing the load → apply path):
```typescript
const handleSave = async () => {
  await updateSettings(settings);
  applySettings(settings); // ❌ Only applies when user clicks save
};
```

❌ **Single effect for load + apply** (race condition with async load):
```typescript
useEffect(() => {
  loadSettings(); // async
  applySettings(settings); // ❌ Runs before load completes, uses defaults
}, []);
```

✅ **Separate effects with loading guard**:
```typescript
useEffect(() => {
  loadSettings();
}, []);

useEffect(() => {
  if (!loading) applySettings(settings); // ✅ Waits for load
}, [settings, loading]);
```

### When to Use This Pattern

- **User preferences**: Theme, accessibility, language, timezone
- **Persisted UI state**: Sidebar collapsed, view mode, filters
- **Feature flags**: User-specific feature toggles
- **Session restoration**: Restoring scroll position, form data

### When NOT to Use This Pattern

- **Computed values**: Derive from props/state instead
- **Event handlers**: Use callbacks, not effects
- **Static data**: Load once at app initialization, not per component

## References

- [React's useEffect: Best Practices](https://dev.to/hkp22/reacts-useeffect-best-practices-pitfalls-and-modern-javascript-insights-g2f)
- [You Might Not Need an Effect – React](https://react.dev/learn/you-might-not-need-an-effect)
- [useEffect – React Official Docs](https://react.dev/reference/react/useEffect)
- [Navigation APIs – next-intl](https://next-intl.dev/docs/routing/navigation)
- [Next.js Internationalization Guide](https://nextjs.org/docs/pages/guides/internationalization)
