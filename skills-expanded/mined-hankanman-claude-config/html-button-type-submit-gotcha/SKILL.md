---
name: html-button-type-submit-gotcha
description: |
  Fix buttons unintentionally submitting forms due to HTML's default type="submit" behavior.
  Use when: (1) Dismiss/cancel/close buttons trigger form submissions, (2) Modal/dialog buttons
  cause unexpected form submits, (3) Dropdown/toggle buttons submit parent forms, (4) Any
  interactive button inside a form triggers submission when it shouldn't. Solves the common
  gotcha where buttons without explicit type attributes default to type="submit" inside forms,
  causing confusing behavior. Covers HTML button elements, React components, and all web
  frameworks with form handling.
author: Claude Code
version: 1.0.0
date: 2026-02-02
---

# HTML Button Type Submit Gotcha

## Problem

Buttons without an explicit `type` attribute default to `type="submit"` when inside a `<form>` element. This causes UI buttons (dismiss, cancel, close, toggle, etc.) to unintentionally submit forms when clicked, leading to confusing and buggy behavior.

**Common Scenario**: A dismiss button on an alert/modal inside a form triggers form submission instead of just closing the alert.

## Context / Trigger Conditions

Use this pattern when you encounter:

1. **Unexpected Form Submissions**:
   - Clicking dismiss/close buttons submits forms
   - Cancel buttons trigger form submission
   - Modal close buttons submit parent forms
   - Dropdown/toggle buttons cause form submits

2. **Symptoms**:
   - Forms submit when clicking non-submit UI buttons
   - Page reloads or navigates unexpectedly
   - Data gets saved/sent when just trying to close UI elements
   - Event handlers on buttons fire but also trigger form submission

3. **Context Markers**:
   - Button is inside a `<form>` element (even nested deeply)
   - Button doesn't have explicit `type` attribute
   - Button is for UI interaction (not form submission)
   - Problem only appears when button is within form boundaries

4. **Code Patterns That Fail**:
   ```html
   <!-- ❌ Defaults to type="submit" inside forms -->
   <form>
     <button onClick={handleDismiss}>Close</button>
   </form>

   <!-- ❌ React component without type -->
   <form>
     <button className="..." onClick={onClose}>
       <X />
     </button>
   </form>
   ```

## Solution

Always explicitly set `type="button"` on buttons that should not submit forms.

### HTML/JSX

```html
<!-- ✅ Explicit type prevents form submission -->
<form>
  <button type="button" onClick={handleDismiss}>Close</button>
</form>
```

### React Component

```tsx
// ✅ Dismiss button in Alert component
function Alert({ onDismiss }) {
  return (
    <div role="alert">
      {children}
      <button
        type="button"  // Critical: prevents form submission
        onClick={onDismiss}
        aria-label="Dismiss alert"
      >
        <X className="h-4 w-4" />
      </button>
    </div>
  );
}
```

### Common Button Types Requiring `type="button"`

```tsx
// Dismiss buttons
<button type="button" onClick={handleDismiss}>✕</button>

// Cancel buttons
<button type="button" onClick={handleCancel}>Cancel</button>

// Modal close buttons
<button type="button" onClick={closeModal}>Close</button>

// Dropdown toggles
<button type="button" onClick={toggleDropdown}>Menu</button>

// Tab switches
<button type="button" onClick={() => setTab('profile')}>Profile</button>

// Increment/decrement
<button type="button" onClick={() => setCount(c => c + 1)}>+</button>

// Delete/remove (non-form action)
<button type="button" onClick={handleDelete}>Delete</button>
```

## The Three Button Types

**Understanding the options**:

1. **`type="submit"`** (DEFAULT in forms):
   ```html
   <button type="submit">Submit Form</button>
   <!-- Submits the parent form -->
   ```

2. **`type="button"`** (Interactive UI):
   ```html
   <button type="button">Click Me</button>
   <!-- Does nothing by default, only runs onClick handler -->
   ```

3. **`type="reset"`** (Avoid):
   ```html
   <button type="reset">Reset</button>
   <!-- Clears form fields - usually annoying to users -->
   ```

## Verification

### Test the fix:

1. **Manual Testing**:
   - Place button inside a form
   - Click the button
   - Verify form does NOT submit
   - Verify onClick handler still fires

2. **Developer Tools**:
   ```javascript
   // Check button type in console
   document.querySelector('button').type
   // Should be: "button" for UI buttons
   // Should be: "submit" for submit buttons
   ```

3. **React DevTools**:
   - Inspect button element
   - Verify `type` prop is set to `"button"`

## Complete Examples

### Example 1: Alert Component

```tsx
interface AlertProps {
  dismissible?: boolean;
  onDismiss?: () => void;
  children: React.ReactNode;
}

function Alert({ dismissible, onDismiss, children }: AlertProps) {
  return (
    <div role="alert">
      {children}
      {dismissible && onDismiss && (
        <button
          type="button"  // ✅ Prevents form submission
          onClick={onDismiss}
          className="absolute top-3 right-3"
          aria-label="Dismiss alert"
        >
          <X className="h-4 w-4" />
        </button>
      )}
    </div>
  );
}
```

### Example 2: Modal Component

```tsx
function Modal({ isOpen, onClose, children }) {
  if (!isOpen) return null;

  return (
    <div className="modal-overlay">
      <div className="modal-content">
        <button
          type="button"  // ✅ Won't submit parent form
          onClick={onClose}
          className="modal-close"
          aria-label="Close modal"
        >
          ✕
        </button>
        {children}
      </div>
    </div>
  );
}
```

### Example 3: Form with Mixed Buttons

```tsx
function UserForm() {
  const handleCancel = () => {
    // Cancel logic
  };

  return (
    <form onSubmit={handleSubmit}>
      <input name="username" />
      <input name="email" />

      <div className="button-group">
        {/* ✅ Cancel should NOT submit */}
        <button type="button" onClick={handleCancel}>
          Cancel
        </button>

        {/* ✅ Submit SHOULD submit (explicit is better) */}
        <button type="submit">
          Save Changes
        </button>
      </div>
    </form>
  );
}
```

## Why This Happens

### HTML Specification

From the HTML specification:
- When a button's `type` attribute is in the "Submit Button" state (or not specified), the button is a submit button
- Submit buttons are the default way to submit form data
- This default exists for backward compatibility and simplicity in basic forms

### Developer Expectations vs Reality

```html
<!-- What developers expect: -->
<form>
  <button>Click Me</button>  <!-- Expect: just onClick -->
</form>

<!-- What actually happens: -->
<form>
  <button type="submit">Click Me</button>  <!-- Reality: submits form -->
</form>
```

## Best Practices

### 1. Always Specify Type Explicitly

```tsx
// ❌ Bad: Implicit type (defaults to submit in forms)
<button onClick={handleClick}>Click</button>

// ✅ Good: Explicit type
<button type="button" onClick={handleClick}>Click</button>
<button type="submit">Submit Form</button>
```

### 2. Create Type-Safe Button Components

```tsx
interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'danger';
  children: React.ReactNode;
}

// Force explicit type or default to "button" for safety
function Button({
  type = 'button',  // Safe default
  variant = 'primary',
  children,
  ...props
}: ButtonProps) {
  return (
    <button type={type} className={getVariantClass(variant)} {...props}>
      {children}
    </button>
  );
}

// Usage:
<Button onClick={handleClick}>Cancel</Button>  // type="button" by default
<Button type="submit">Save</Button>  // Explicit submit
```

### 3. ESLint Rule

Add to `.eslintrc`:

```json
{
  "rules": {
    "react/button-has-type": ["error", {
      "button": true,
      "submit": true,
      "reset": true
    }]
  }
}
```

This rule enforces explicit `type` attribute on all buttons.

### 4. Component Library Pattern

```tsx
// Base button with safe defaults
export const Button = React.forwardRef<
  HTMLButtonElement,
  React.ButtonHTMLAttributes<HTMLButtonElement>
>(({ type = 'button', ...props }, ref) => {
  return <button ref={ref} type={type} {...props} />;
});

// Specialized button components
export const SubmitButton = (props: Omit<ButtonProps, 'type'>) => (
  <Button type="submit" {...props} />
);

export const CancelButton = (props: Omit<ButtonProps, 'type'>) => (
  <Button type="button" {...props} />
);
```

## Common Pitfalls

### 1. Forgetting Type in Complex Components

```tsx
// ❌ Easy to forget when component gets complex
function ComplexButton({ icon, label, onClick, loading, disabled }) {
  return (
    <button  // Missing type!
      onClick={onClick}
      disabled={disabled || loading}
      className="complex-button"
    >
      {loading ? <Spinner /> : icon}
      {label}
    </button>
  );
}

// ✅ Always include type
function ComplexButton({ type = 'button', icon, label, onClick, loading, disabled }) {
  return (
    <button
      type={type}  // Explicit type with safe default
      onClick={onClick}
      disabled={disabled || loading}
      className="complex-button"
    >
      {loading ? <Spinner /> : icon}
      {label}
    </button>
  );
}
```

### 2. Third-Party Component Libraries

```tsx
// Some UI libraries don't set type="button" by default
// Check their documentation and override if needed

// ❌ Potential issue
<ThirdPartyButton onClick={handleClick}>Click</ThirdPartyButton>

// ✅ Safer
<ThirdPartyButton type="button" onClick={handleClick}>Click</ThirdPartyButton>
```

### 3. Event Handler Confusion

```tsx
// ❌ Button submits AND runs onClick
<form onSubmit={handleFormSubmit}>
  <button onClick={handleButtonClick}>  {/* Missing type! */}
    Delete
  </button>
</form>
// Result: Both handleButtonClick AND handleFormSubmit fire

// ✅ Button only runs onClick
<form onSubmit={handleFormSubmit}>
  <button type="button" onClick={handleButtonClick}>
    Delete
  </button>
</form>
// Result: Only handleButtonClick fires
```

## Framework-Specific Notes

### React

```tsx
// TypeScript provides no warning for missing type
// Use ESLint rule: react/button-has-type

interface Props {
  onClick: () => void;
}

function MyButton({ onClick }: Props) {
  return (
    <button type="button" onClick={onClick}>  // Always explicit
      Click
    </button>
  );
}
```

### Vue

```vue
<!-- Same issue exists in Vue -->
<template>
  <form @submit="handleSubmit">
    <!-- ❌ Will submit form -->
    <button @click="handleClick">Click</button>

    <!-- ✅ Won't submit form -->
    <button type="button" @click="handleClick">Click</button>
  </form>
</template>
```

### Angular

```typescript
// Same principle applies
@Component({
  template: `
    <form (ngSubmit)="onSubmit()">
      <!-- Wrong: submits form -->
      <button (click)="onClick()">Click</button>

      <!-- Correct: only runs onClick -->
      <button type="button" (click)="onClick()">Click</button>
    </form>
  `
})
```

## References

- [MDN: &lt;button&gt; Element](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/button) - Official HTML button documentation
- [HTML button type Attribute - W3Schools](https://www.w3schools.com/tags/att_button_type.asp) - Button type attribute reference
- [Forms and buttons in HTML - MDN](https://developer.mozilla.org/en-US/docs/Learn_web_development/Core/Structuring_content/HTML_forms) - HTML forms best practices
- [3 Default Behaviours When Submitting HTML Forms - Medium](https://medium.com/programming-essentials/3-default-behaviours-when-submitting-html-forms-adaf45c7bf23) - Form submission behavior explained
