# SAP-041: React Form Validation - Accessibility Patterns (WCAG 2.2 Level AA)

**SAP**: SAP-041 (react-form-validation)
**Domain**: Accessibility
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains **WCAG 2.2 Level AA accessibility patterns** for React Hook Form + Zod validation forms.

**Compliance Target**: WCAG 2.2 Level AA (0 axe-core violations)

**Supported Screen Readers**:
- NVDA (Windows)
- VoiceOver (macOS, iOS)
- JAWS (Windows)

**Checklist Coverage**:
1. Error Identification (3.3.1, Level A)
2. Labels or Instructions (3.3.2, Level A)
3. Error Suggestion (3.3.3, Level AA)
4. Error Prevention (3.3.4, Level AA)
5. Focus Order (2.4.3, Level A)
6. Status Messages (4.1.3, Level AA)

**For implementation workflows**, see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For form patterns**, see [../form-patterns/AGENTS.md](../form-patterns/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

---

## Accessibility Checklist (WCAG 2.2 Level AA)

### 3.3.1 Error Identification (Level A)

**Requirement**: Errors identified programmatically and described to user

**Pattern**:
```typescript
<input
  aria-invalid={errors.email ? "true" : "false"}
  aria-describedby={errors.email ? "email-error" : undefined}
/>
{errors.email && (
  <p id="email-error" role="alert" aria-live="assertive">
    {errors.email.message}
  </p>
)}
```

**Checklist**:
- [ ] All error fields have `aria-invalid="true"`
- [ ] All errors have `aria-describedby` linking to error message
- [ ] All error messages have `role="alert"` for screen reader announcements

**Why this matters**:
- Screen readers announce errors immediately when validation fails
- Users know which field has an error and what the error is
- Programmatic error identification allows assistive tech to parse errors

**Testing**:
```bash
# Install axe DevTools Chrome extension
# Run accessibility scan on form with errors
# Should show 0 violations for error identification
```

---

### 3.3.2 Labels or Instructions (Level A)

**Requirement**: All form fields have labels or instructions

**Pattern**:
```typescript
<label htmlFor="email" className="block text-sm font-medium">
  Email Address <span aria-label="required">*</span>
</label>
<input
  id="email"
  {...register("email")}
  aria-required="true"
/>
```

**Checklist**:
- [ ] All form fields have `<label>` elements
- [ ] All labels have `htmlFor` matching input `id`
- [ ] Required fields indicated visually (*, "required" text, etc.)
- [ ] Required fields have `aria-required="true"`

**Why this matters**:
- Screen readers announce label when field receives focus
- Visual labels help all users understand field purpose
- Required field indicators prevent submission errors

**Anti-Pattern** (DON'T DO THIS):
```typescript
// ❌ Bad: No label association
<label>Email Address</label>
<input {...register("email")} />

// ✅ Good: Label associated with input
<label htmlFor="email">Email Address</label>
<input id="email" {...register("email")} />
```

---

### 3.3.3 Error Suggestion (Level AA)

**Requirement**: Error messages provide correction suggestions

**Pattern**:
```typescript
// ❌ Bad: Vague error
z.string().min(8) // Error: "String must contain at least 8 character(s)"

// ✅ Good: Specific suggestion
z.string().min(8, "Password must be at least 8 characters. Please add more characters.")
```

**Checklist**:
- [ ] Error messages explain what went wrong
- [ ] Error messages suggest how to fix
- [ ] Error messages use plain language (avoid technical jargon)

**Examples**:
- Email: "Invalid email address. Please use format: name@example.com"
- Password: "Password must be at least 8 characters. Please add more characters."
- Date: "Date must be in the future. Please select a date after today."
- Phone: "Phone number must be 10 digits. Please remove spaces and dashes."
- URL: "URL must start with https://. Please add the protocol."

**Zod Schema Examples**:
```typescript
const schema = z.object({
  email: z.string()
    .email("Invalid email address. Please use format: name@example.com"),

  password: z.string()
    .min(8, "Password must be at least 8 characters. Please add more characters.")
    .regex(/[A-Z]/, "Password must include at least one uppercase letter.")
    .regex(/[0-9]/, "Password must include at least one number."),

  birthdate: z.string()
    .refine(date => new Date(date) < new Date(), {
      message: "Birthdate must be in the past. Please select an earlier date."
    }),

  url: z.string()
    .url("Invalid URL. Please start with https:// or http://")
})
```

---

### 3.3.4 Error Prevention (Level AA)

**Requirement**: Critical actions require confirmation, review, or reversal

**Pattern**:
```typescript
// Confirmation step for account deletion
<form onSubmit={handleSubmit(onDelete)}>
  <p className="text-red-600 font-medium">
    This action cannot be undone. Are you sure you want to delete your account?
  </p>

  <label>
    <input {...register("confirm")} type="checkbox" required />
    I understand this action is permanent
  </label>

  <button type="submit" className="bg-red-600 text-white">
    Delete Account
  </button>
</form>
```

**Checklist**:
- [ ] Critical actions (delete, payment, etc.) have confirmation step
- [ ] Multi-step forms allow review before final submission
- [ ] Users can edit previous steps in wizard forms

**Critical actions requiring confirmation**:
- Account deletion
- Payment processing
- Data deletion (bulk delete, permanent delete)
- Irreversible state changes
- Subscription cancellations

**Multi-Step Form Review Pattern**:
```typescript
// Step 4: Review all data before submission
{step === 4 && (
  <>
    <h2>Review Your Information</h2>

    <div>
      <h3>Account</h3>
      <p>Email: {formData.email}</p>
      <button onClick={() => router.push("?step=1")}>Edit</button>
    </div>

    <div>
      <h3>Profile</h3>
      <p>Name: {formData.name}</p>
      <p>Company: {formData.company}</p>
      <button onClick={() => router.push("?step=2")}>Edit</button>
    </div>

    <button type="submit">Confirm and Submit</button>
  </>
)}
```

---

### 2.4.3 Focus Order (Level A)

**Requirement**: Logical tab order through form fields

**Pattern**:
```typescript
// Natural tab order (top to bottom)
<form>
  <input {...register("name")} />     {/* Tab index 1 */}
  <input {...register("email")} />    {/* Tab index 2 */}
  <input {...register("phone")} />    {/* Tab index 3 */}
  <button type="submit">Submit</button> {/* Tab index 4 */}
</form>

// Focus first error after failed submission
useEffect(() => {
  if (Object.keys(errors).length > 0) {
    const firstError = Object.keys(errors)[0]
    const element = document.getElementById(firstError)
    element?.focus()
  }
}, [errors])
```

**Checklist**:
- [ ] Tab order matches visual order (top to bottom, left to right)
- [ ] No unexpected tab jumps
- [ ] After failed submission, focus moves to first error
- [ ] Submit button is last in tab order

**Focus Management for Multi-Column Forms**:
```typescript
// ✅ Good: Natural tab order
<div className="grid grid-cols-2 gap-4">
  <input {...register("firstName")} />  {/* Tab 1 */}
  <input {...register("lastName")} />   {/* Tab 2 */}
  <input {...register("email")} />      {/* Tab 3 */}
  <input {...register("phone")} />      {/* Tab 4 */}
</div>

// ❌ Bad: Manual tabIndex (avoid unless necessary)
<input {...register("field1")} tabIndex={3} />
<input {...register("field2")} tabIndex={1} />
<input {...register("field3")} tabIndex={2} />
```

**Auto-Focus First Error**:
```typescript
import { useEffect } from "react"

const {
  register,
  handleSubmit,
  formState: { errors },
  setFocus
} = useForm()

useEffect(() => {
  if (Object.keys(errors).length > 0) {
    const firstErrorField = Object.keys(errors)[0] as any
    setFocus(firstErrorField)
  }
}, [errors, setFocus])
```

---

### 4.1.3 Status Messages (Level AA)

**Requirement**: Status messages announced to screen readers

**Pattern**:
```typescript
{/* Loading state */}
{isPending && (
  <div role="status" aria-live="polite">
    Submitting form...
  </div>
)}

{/* Success message */}
{state?.success && (
  <div role="status" aria-live="polite" className="text-green-600">
    Form submitted successfully!
  </div>
)}

{/* Error message */}
{state?.message && (
  <div role="alert" aria-live="assertive" className="text-red-600">
    {state.message}
  </div>
)}
```

**Checklist**:
- [ ] Loading states have `role="status"` and `aria-live="polite"`
- [ ] Success messages have `role="status"` and `aria-live="polite"`
- [ ] Error messages have `role="alert"` and `aria-live="assertive"`

**ARIA Live Regions**:
- `aria-live="polite"`: Announces when screen reader is idle (success, info)
- `aria-live="assertive"`: Announces immediately, interrupting current speech (errors, warnings)

**Status Message Types**:
```typescript
// Polite (background updates)
<div role="status" aria-live="polite">
  Draft saved at 2:34 PM
</div>

// Assertive (urgent alerts)
<div role="alert" aria-live="assertive">
  Connection lost. Please check your internet.
</div>

// Progress indicator
<div role="status" aria-live="polite" aria-busy="true">
  Uploading file... 45%
</div>
```

---

## Complete Accessible Form Example

```typescript
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { useEffect } from "react"
import { signupSchema, type SignupFormData } from "@/lib/validations/auth"

export function AccessibleSignupForm() {
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting, isSubmitSuccessful }
  } = useForm<SignupFormData>({
    resolver: zodResolver(signupSchema)
  })

  // Focus first error after failed submission
  useEffect(() => {
    if (Object.keys(errors).length > 0) {
      const firstError = Object.keys(errors)[0]
      const element = document.getElementById(firstError)
      element?.focus()
    }
  }, [errors])

  async function onSubmit(data: SignupFormData) {
    // Submit form...
  }

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="space-y-6" noValidate>
      {/* Email field */}
      <div>
        <label
          htmlFor="email"
          className={`block text-sm font-medium ${errors.email ? "text-red-600" : ""}`}
        >
          Email Address <span aria-label="required">*</span>
        </label>
        <input
          id="email"
          {...register("email")}
          type="email"
          autoComplete="email"
          aria-invalid={errors.email ? "true" : "false"}
          aria-describedby={errors.email ? "email-error" : "email-description"}
          aria-required="true"
          className={`mt-1 block w-full px-3 py-2 border rounded-md ${
            errors.email ? "border-red-600" : "border-gray-300"
          }`}
        />
        <p id="email-description" className="mt-1 text-sm text-gray-600">
          We'll never share your email with anyone else.
        </p>
        {errors.email && (
          <p id="email-error" role="alert" aria-live="assertive" className="mt-1 text-sm text-red-600">
            {errors.email.message}
          </p>
        )}
      </div>

      {/* Password field */}
      <div>
        <label
          htmlFor="password"
          className={`block text-sm font-medium ${errors.password ? "text-red-600" : ""}`}
        >
          Password <span aria-label="required">*</span>
        </label>
        <input
          id="password"
          {...register("password")}
          type="password"
          autoComplete="new-password"
          aria-invalid={errors.password ? "true" : "false"}
          aria-describedby={errors.password ? "password-error" : "password-description"}
          aria-required="true"
          className={`mt-1 block w-full px-3 py-2 border rounded-md ${
            errors.password ? "border-red-600" : "border-gray-300"
          }`}
        />
        <p id="password-description" className="mt-1 text-sm text-gray-600">
          Must be at least 8 characters with uppercase, lowercase, and numbers.
        </p>
        {errors.password && (
          <p id="password-error" role="alert" aria-live="assertive" className="mt-1 text-sm text-red-600">
            {errors.password.message}
          </p>
        )}
      </div>

      {/* Loading state */}
      {isSubmitting && (
        <div role="status" aria-live="polite" className="text-blue-600">
          Submitting form...
        </div>
      )}

      {/* Success message */}
      {isSubmitSuccessful && (
        <div role="status" aria-live="polite" className="p-3 bg-green-50 text-green-800 rounded-md">
          Account created successfully!
        </div>
      )}

      {/* Submit button */}
      <button
        type="submit"
        disabled={isSubmitting}
        className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
      >
        {isSubmitting ? "Creating account..." : "Create Account"}
      </button>
    </form>
  )
}
```

**Key Accessibility Features**:
1. ✅ Label association (`htmlFor` + `id`)
2. ✅ Required field indicators (`aria-required="true"`, `*` with `aria-label`)
3. ✅ Error identification (`aria-invalid`, `aria-describedby`, `role="alert"`)
4. ✅ Error suggestions (descriptive Zod messages)
5. ✅ Focus management (auto-focus first error)
6. ✅ Status announcements (`role="status"`, `aria-live`)
7. ✅ Keyboard navigation (natural tab order)
8. ✅ Visual feedback (error border, disabled state)

---

## Testing Accessibility

### Automated Testing with axe-core

```bash
# Install dependencies
npm install -D @axe-core/react

# Create test file
# tests/accessibility.test.tsx
import { render } from "@testing-library/react"
import { axe, toHaveNoViolations } from "jest-axe"
import { SignupForm } from "@/components/forms/SignupForm"

expect.extend(toHaveNoViolations)

test("SignupForm has no accessibility violations", async () => {
  const { container } = render(<SignupForm />)
  const results = await axe(container)
  expect(results).toHaveNoViolations()
})
```

**Run tests**:
```bash
npm run test
```

---

### Manual Testing with Screen Readers

**Testing Checklist**:

**1. NVDA (Windows)**:
- [ ] Navigate form with Tab key
- [ ] Verify labels are announced when field receives focus
- [ ] Submit form with errors, verify errors are announced
- [ ] Verify error location (field name + error message)

**2. VoiceOver (macOS)**:
- [ ] Enable VoiceOver (Cmd + F5)
- [ ] Navigate form with VO + Right Arrow
- [ ] Verify required field indicators announced
- [ ] Submit form, verify error announcements

**3. JAWS (Windows)**:
- [ ] Navigate form with Tab key
- [ ] Verify field labels and descriptions announced
- [ ] Test form submission error flow
- [ ] Verify status messages announced

---

### Browser DevTools Accessibility Audit

**Chrome DevTools**:
1. Open DevTools (F12)
2. Go to Lighthouse tab
3. Select "Accessibility" category
4. Run audit
5. Fix any reported issues

**Target Score**: 100/100

---

## Integration with SAP-026 (react-accessibility)

**Cross-Reference**: SAP-026 provides comprehensive accessibility patterns beyond forms.

**SAP-026 Features**:
- Skip links and landmark regions
- Keyboard navigation patterns
- Focus visible styles
- Color contrast validation
- ARIA patterns for interactive components

**Integration Pattern**:
```typescript
// Use SAP-026 for page-level accessibility
import { SkipLink } from "@/components/accessibility/SkipLink"
import { A11yProvider } from "@/components/accessibility/A11yProvider"

// Use SAP-041 for form-specific accessibility
import { AccessibleSignupForm } from "@/components/forms/SignupForm"

export default function SignupPage() {
  return (
    <A11yProvider>
      <SkipLink href="#signup-form">Skip to signup form</SkipLink>

      <main id="signup-form">
        <h1>Create Account</h1>
        <AccessibleSignupForm />
      </main>
    </A11yProvider>
  )
}
```

---

## Version History

**1.0.0 (2025-11-10)** - Initial accessibility patterns extraction from awareness-guide.md
- WCAG 2.2 Level AA checklist (6 criteria)
- Complete accessible form example
- Automated testing with axe-core
- Manual testing guidelines
- Integration with SAP-026
