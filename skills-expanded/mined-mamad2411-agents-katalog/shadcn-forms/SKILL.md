---
name: shadcn-forms
description: Use when implementing forms with shadcn/ui — covering react-hook-form integration, zod schema design, FormField composition, validation UX, server action wiring, and multi-step form patterns.
---

# shadcn/ui Forms

## Specialization

Provide expert-level guidance for building production-quality forms using shadcn/ui Form components, `react-hook-form`, and `zod` — covering schema design, `FormField` composition, validation UX, server action integration, multi-step forms, and accessibility.

This skill covers form implementation patterns. Component design and CVA variants are handled by `shadcn-component-design`. Theming and design tokens are handled by `shadcn-theming`.

## Trigger Conditions

- Building a form that uses shadcn `Form`, `FormField`, `FormItem`, `FormLabel`, `FormControl`, `FormDescription`, and `FormMessage` components.
- Designing a `zod` schema for a form and wiring it to `react-hook-form` via `zodResolver`.
- Implementing validation UX: inline field errors, form-level errors, submission loading states, and success feedback.
- Wiring a form to a Next.js Server Action or a REST/tRPC endpoint.
- Building a multi-step or wizard form with shared `zod` schema and step-level validation.
- Auditing an existing form for accessibility gaps, uncontrolled state leakage, or missing error handling.

## When Not to Use

- Non-form component design (use `shadcn-component-design`).
- Project installation and wiring (use `shadcn-setup`).
- Quality gate review of a completed implementation (use `shadcn-quality-gate`).

## Inputs

- Form purpose and field inventory.
- Validation rules per field (required, min/max, regex, async, cross-field).
- Submission target: Server Action, REST endpoint, tRPC mutation, or GraphQL mutation.
- Multi-step requirements if applicable.
- Framework in use and RSC constraints.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| `zod` schema | Typed schema with all field validations, cross-field refinements, and transform rules |
| `useForm` setup | `react-hook-form` `useForm` configured with `zodResolver`, default values, and mode |
| `FormField` composition | Each field wrapped in `FormField` → `FormItem` → `FormLabel` + `FormControl` + `FormDescription` + `FormMessage` |
| Submission handler | `handleSubmit` wired to the submission target; loading and error states handled |
| Validation UX record | Inline field errors, form-level error, optimistic feedback, and empty/success states defined |
| Accessibility annotation | All labels associated with controls; error messages linked via `aria-describedby`; focus management on submission |
| Multi-step contract (if applicable) | Step schema slices, navigation state, and partial validation gates defined |
| Readiness summary | Open items, deferred fields, and known edge cases |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | Build one form with a single field and submit | Field renders, validates on submit, and error message appears |
| L2 Practical Delivery | Full production form with all field types and validation | All fields typed, all validations active, submission handler wired |
| L3 Advanced Patterns | Multi-step, async validation, or server-error mapping | Step transitions clean, async validation debounced, server errors surface correctly |
| L4 Expert Standardization | Reusable cross-project form patterns | Typed form hook factory, shared field component library, and validation pattern library documented |

## Core Form Pattern

### 1. Install Dependencies

```bash
npx shadcn add form
npm install react-hook-form zod @hookform/resolvers
```

### 2. Define the Zod Schema

```ts
import { z } from "zod"

export const profileSchema = z.object({
  username: z
    .string()
    .min(2, { message: "Username must be at least 2 characters." })
    .max(32, { message: "Username must be 32 characters or fewer." }),
  email: z.string().email({ message: "Please enter a valid email address." }),
  role: z.enum(["admin", "editor", "viewer"], {
    required_error: "Please select a role.",
  }),
  bio: z.string().max(500).optional(),
})

export type ProfileFormValues = z.infer<typeof profileSchema>
```

**Schema design rules:**

- Define error messages inside the schema, not in the component.
- Use `z.infer<typeof schema>` to derive the TypeScript type — never duplicate manually.
- Cross-field validation uses `.refine()` or `.superRefine()` at the schema root.
- Async validation (uniqueness checks) uses `z.string().refine(async (val) => ...)` — debounce at the hook level.

### 3. Configure `useForm`

```tsx
"use client"

import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { profileSchema, type ProfileFormValues } from "./profile-schema"

const form = useForm<ProfileFormValues>({
  resolver: zodResolver(profileSchema),
  defaultValues: {
    username: "",
    email: "",
    bio: "",
  },
  mode: "onBlur", // validate on field blur; use "onSubmit" for minimal UX friction
})
```

**Mode selection:**

| Mode | UX Behavior | When to Use |
|---|---|---|
| `onSubmit` | Errors appear only after submit | Minimal friction; new user flows |
| `onBlur` | Errors appear when field loses focus | Balanced; default recommendation |
| `onChange` | Errors appear on every keystroke | High guidance; complex or critical forms |
| `all` | Errors appear on blur and change after first submit | Progressive disclosure |

### 4. Compose FormField

```tsx
import {
  Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage,
} from "@/components/ui/form"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"

export function ProfileForm() {
  const form = useForm<ProfileFormValues>({ /* ... */ })

  async function onSubmit(values: ProfileFormValues) {
    // Call server action or API
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="username"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Username</FormLabel>
              <FormControl>
                <Input placeholder="shadcn" {...field} />
              </FormControl>
              <FormDescription>This is your public display name.</FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? "Saving…" : "Save changes"}
        </Button>
      </form>
    </Form>
  )
}
```

**`FormField` rules:**

- Always use `FormField` with `control` and `name` — never use uncontrolled inputs.
- `FormMessage` renders the zod error message automatically when present; do not duplicate.
- `FormDescription` is optional — use for helper text only, not validation guidance.
- Spread `{...field}` onto the control component; never manually wire `value` and `onChange`.

## Submission Patterns

### Next.js Server Action

```tsx
import { profileAction } from "@/app/actions/profile"

async function onSubmit(values: ProfileFormValues) {
  const result = await profileAction(values)
  if (result.error) {
    form.setError("root", { message: result.error })
  }
}
```

- Use `form.setError("root", ...)` for form-level server errors.
- Validate the submitted values server-side independently — never trust client zod validation alone.
- Return typed error objects from server actions, not thrown exceptions.

### REST / tRPC

```tsx
async function onSubmit(values: ProfileFormValues) {
  try {
    await api.profile.update.mutate(values)
    toast.success("Profile updated.")
  } catch (err) {
    form.setError("root", { message: "Update failed. Please try again." })
  }
}
```

## Multi-Step Forms

```ts
// Define schema slices per step
const step1Schema = profileSchema.pick({ username: true, email: true })
const step2Schema = profileSchema.pick({ role: true, bio: true })

// Validate only the current step's slice
const isStep1Valid = await form.trigger(["username", "email"])
if (!isStep1Valid) return
setCurrentStep(2)
```

**Multi-step rules:**

- One `useForm` instance owns all steps; do not split into separate form instances.
- Use `form.trigger([...fieldNames])` to validate a step's fields before advancing.
- Track `currentStep` in component state; do not encode it in the zod schema.
- Submit the full schema only on the final step.

## Accessibility Requirements

- Every `<Input>`, `<Select>`, `<Checkbox>`, `<Textarea>` must have an associated `<FormLabel>` rendered by the shadcn Form primitive — this wires `htmlFor`/`id` automatically via `useFormField`.
- `<FormMessage>` renders with `role="alert"` internally — do not add a redundant `aria-live` wrapper.
- On submission failure, focus the first errored field: `form.setFocus(firstErrorField)`.
- Disabled submit button during `isSubmitting` prevents double-submission; ensure it is re-enabled on error.

## Pragmatic Stop Rule

Stop when the zod schema is complete, all `FormField` compositions render errors correctly, the submission handler is wired and handles both success and error paths, and accessibility requirements are met. Open items must be in the readiness summary.
