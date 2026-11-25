---
name: polaris-design-interaction-states
description: Design interaction states for Shopify UI that communicate element status, build confidence, and signal interactivity. Master feedback, signifiers, and accessibility for all input devices.
---

# Interaction States

Interaction states communicate the status of an element in the interface, establish confidence once an action is taken, and suggest the ability (or inability) to interact with the element.

## Principles

### Be Subtle, But Clear

Successful interaction feedback is informative, not decorative.

**Guidelines:**
- Avoid elaborate transitions
- Prevent visual noise
- Avoid intense color changes
- Prevent distraction and unpleasantness

**Do:**
- Make feedback informative
- Keep transitions smooth
- Focus on clarity

**Don't:**
- Create decorative feedback
- Use elaborate animations
- Make interface unpleasant

### Keep Things Consistent

Consistent treatments for interaction feedback create recognizable patterns.

**Consistency importance:**
- If interaction produces different feedback, it deteriorates pattern integrity
- Risks confusing merchants
- Reduces interface predictability

**Do:**
- Use consistent feedback across admin
- Maintain recognizable patterns
- Build predictable experience

**Don't:**
- Change feedback treatment inconsistently
- Create confusing patterns
- Make interactions unpredictable

## Designing Interaction States

Merchants interact with interfaces differently depending on input device.

### Input Devices to Consider

- Mouse
- Touch screen
- Keyboard
- Voice
- Game controller
- Refreshable braille display

**Design considerations:**
- Each device has different affordances
- Consider all input methods
- Test with multiple devices
- Ensure accessibility across all inputs

## Use Signifiers

Provide merchants with cues about what the interface will do.

**Benefits of signifiers:**
- Set clear expectations
- Create intuitive interface
- Make interface easier to use
- Reduce confusion

### Types of Signifiers

**Explicit signifiers:**
- Content directs merchants to intended action
- Examples: "Sort", "Save"
- Clear and obvious

**Hidden signifiers:**
- Clue revealed upon interaction
- Examples: Hover states, tab navigation
- Subtle but discoverable

**Negative signifiers:**
- Action appears inactive
- Grayed out elements
- No hover response
- Indicates unavailability

**Do:**
- Use clear signifiers
- Make interactive elements obvious
- Provide cues about capabilities

**Don't:**
- Leave interactive elements ambiguous
- Hide all signifiers
- Create confusing affordances

## Behavior and Feedback

### Provide Feedback Indicators

Let merchants know interface received their request.

**Use these components:**
- Progress bar component (shows progress)
- Spinner component (indicates loading)
- Provide information about what's happening
- Estimate time when appropriate

**Do:**
- Show that action was received
- Provide progress information
- Communicate timing estimates

**Don't:**
- Leave merchants waiting without feedback
- Disappear during processing
- Create uncertainty

### Non-Disruptive Feedback

For action outcomes that don't interrupt:

**Use:**
- App Bridge Toast component
- Non-modal notifications
- Subtle success messages
- Corner notifications

**Do:**
- Provide outcome feedback
- Use non-disruptive components
- Keep focus on task

**Don't:**
- Create disruptive feedback
- Modal heavy confirmations
- Interrupt workflow unnecessarily

### Unsuccessful Completion Feedback

For actions that fail requiring merchant action:

**Provide:**
- Information about what prevented action
- What merchant can do to fix
- Clear error messages

**Use:**
- Text field validation error state
- Form validation messages
- Clear next steps

**Do:**
- Explain what went wrong
- Tell merchants how to fix
- Guide toward solution

**Don't:**
- Create vague error messages
- Blame merchant
- Leave without guidance

## Common Interaction States

### Hover State
- Indicates interactivity
- Subtle visual change
- Shows element is clickable
- Should be obvious on all interactive elements

### Active/Pressed State
- Shows element is currently activated
- Different visual treatment
- Clear from default state
- Provides tactile feedback

### Focus State
- Essential for keyboard navigation
- Clear focus indicator
- Helps keyboard users navigate
- Must be visible

### Disabled State
- Indicates unavailability
- Clearly shows non-interactivity
- No hover response expected
- Grayed out or reduced opacity

### Loading State
- Shows processing in progress
- Uses spinner or progress indicators
- Communicates waiting time
- Prevents duplicate actions

### Error State
- Communicates problem
- Clear error messaging
- Often highlights affected field
- Shows how to fix

### Success State
- Confirms action completion
- Positive visual feedback
- May use color (green)
- Reassures merchant
