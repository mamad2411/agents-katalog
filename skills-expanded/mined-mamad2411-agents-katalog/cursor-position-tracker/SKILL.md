---
name: "Cursor Position Tracker"
version: "1.0.0"
description: "Tracks and manages cursor position across text inputs, rich text editors, and custom selection interfaces. Handles IME composition and RTL text."
author: "workspace"
activated: false
---

# Cursor Position Tracker

Tracks and manages cursor position across text inputs, rich text editors, and custom selection interfaces. Handles IME composition and RTL text.

## Decision Framework

### When to Apply
Use when: Rich text editors, custom input components, IME support needed, collaborative editing

### When NOT to Apply
Don't use when: Simple form inputs with standard behavior

## Anti-Patterns

### 1. Breaking IME Composition
```javascript
// BAD: Prevents character composition
input.addEventListener('input', (e) => { formatText(); });

// GOOD: Wait for composition end
let composing = false;
input.addEventListener('compositionstart', () => composing = true);
input.addEventListener('compositionend', () => { composing = false; formatText(); });
input.addEventListener('input', (e) => { if (!composing) formatText(); });
```


## Trigger Phrases

- "Cursor position"
- "Text selection"
- "Rich text editor"
- "IME support"
- "Text input handling"

## Patterns

### Selection Manager
```javascript
class SelectionManager {
  saveSelection() {
    const sel = window.getSelection();
    if (sel.rangeCount > 0) return sel.getRangeAt(0).cloneRange();
    return null;
  }
  restoreSelection(range) {
    if (!range) return;
    const sel = window.getSelection();
    sel.removeAllRanges();
    sel.addRange(range);
  }
}
```

## Integration
- Works with: real-time-collaboration-engine, form-pattern-engine

