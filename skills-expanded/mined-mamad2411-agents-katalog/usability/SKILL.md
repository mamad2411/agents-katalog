---
name: usability
description: "Design psychology - affordances, feedback, mental models"
---

# Don Norman - Design Psychology

Apply cognitive psychology to interface design. Users don't read manuals - the interface must teach itself.

## Core Concepts

### Affordances
What an object suggests it can do. A button affords pressing. A slider affords dragging.

**Rules:**
- Buttons must look pressable (raised, colored, bounded)
- Links must look clickable (underlined or colored)
- Draggable items need grab handles or visual cues
- Text fields must look editable (bordered, lighter background)

### Signifiers
Visual indicators that reveal affordances.

**Rules:**
- Hover states show what's interactive
- Cursor changes (pointer, grab, text) signal interaction type
- Icons with labels > icons alone
- Placeholder text shows expected input format

### Feedback
Every action needs a visible response.

**Rules:**
- Button press: visual depression or color change (<100ms)
- Form submit: loading state, then success/error
- Async operations: progress indicator
- Errors: specific, actionable message at the point of failure

### Mapping
Controls should relate spatially to what they affect.

**Rules:**
- Left arrow goes left, right arrow goes right
- Volume up is up, volume down is down
- Related controls are grouped together
- Scroll direction matches content movement

### Constraints
Prevent errors by making them impossible.

**Rules:**
- Disable buttons until form is valid
- Date pickers prevent invalid dates
- Number inputs prevent letters
- Destructive actions require confirmation

### Mental Models
Users have expectations from past experience.

**Rules:**
- Logo in top-left goes home
- X closes things
- Shopping cart icon shows cart
- Save icon is still a floppy disk (unfortunately)
- Don't fight convention without good reason

## Prescriptive Rules

### Interactive Elements

```css
/* Buttons */
.button {
  min-height: 44px;        /* Touch target */
  min-width: 44px;
  padding: 12px 24px;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.1s;    /* Instant feedback */
}

.button:hover {
  transform: translateY(-1px);  /* Subtle lift */
}

.button:active {
  transform: translateY(1px);   /* Press down */
}

/* Disabled state */
.button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
```

### Form Fields

```css
/* Text inputs */
.input {
  min-height: 44px;
  padding: 12px 16px;
  border: 1px solid #d1d5db;
  border-radius: 4px;
  background: #ffffff;
}

.input:focus {
  border-color: #3b82f6;
  outline: none;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Error state */
.input.error {
  border-color: #ef4444;
}

.error-message {
  color: #ef4444;
  font-size: 14px;
  margin-top: 4px;
}
```

### Feedback Timing

| Action | Feedback Timing | Type |
|--------|-----------------|------|
| Button click | < 100ms | Visual state change |
| Form validation | On blur or submit | Inline error |
| API call start | Immediate | Loading indicator |
| API call success | When complete | Success message (auto-dismiss) |
| API call failure | When complete | Error message (persist until dismissed) |
| Navigation | < 300ms | Page transition |

### Error Messages

**Bad:**
- "Error"
- "Invalid input"
- "Something went wrong"

**Good:**
- "Email must include @ symbol"
- "Password must be at least 8 characters"
- "Could not save. Check your internet connection and try again."

**Rules:**
- Say what went wrong
- Say how to fix it
- Place the message near the problem
- Use red but also an icon (for colorblind users)

## Review Checklist

- [ ] Every clickable element has hover/active states
- [ ] All form fields have focus states
- [ ] Errors appear at point of failure with fix instructions
- [ ] Loading states exist for all async operations
- [ ] Touch targets are at least 44x44px
- [ ] Related controls are visually grouped
- [ ] Dangerous actions have confirmation

## The Gulf of Execution

The gap between what users want to do and how to do it.

**Narrow this gulf:**
1. Make actions visible (don't hide in menus)
2. Use familiar patterns (don't innovate on basics)
3. Provide shortcuts for experts
4. Show current system state

## The Gulf of Evaluation

The gap between system state and user understanding.

**Narrow this gulf:**
1. Show what just happened
2. Show what can happen next
3. Show current state clearly
4. Provide undo for mistakes

## Norman Score

| Score | Meaning |
|-------|---------|
| 10 | Zero learning required, errors impossible |
| 7-9 | Minor confusion points, mostly intuitive |
| 4-6 | Requires exploration to understand |
| 0-3 | Users give up, needs redesign |

## Integration

Combine with:
- `/design` - Philosophy behind why this matters
- `/mobile` - Mobile-specific psychology (thumb zones)
- `/interaction` - Input/interaction fundamentals
