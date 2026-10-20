# SAP-041: React Form Validation - Form Patterns & Complexity Decision Tree

**SAP**: SAP-041 (react-form-validation)
**Domain**: Form Patterns
**Version**: 1.0.0
**Last Updated**: 2025-11-10

---

## Overview

This file contains the **Form Complexity Decision Tree** for choosing the right form validation pattern based on complexity.

**4 Tiers**:
1. **Tier 1**: Simple Forms (1-3 fields, basic validation) - 5 min setup
2. **Tier 2**: Medium Forms (4-8 fields, cross-field validation) - 15 min setup
3. **Tier 3**: Complex Forms (9+ fields, dynamic fields) - 30 min setup
4. **Tier 4**: Wizard Forms (multi-step, state persistence) - 45 min setup

**For implementation workflows**, see [../workflows/AGENTS.md](../workflows/AGENTS.md)

**For accessibility patterns**, see [../accessibility/AGENTS.md](../accessibility/AGENTS.md)

**For troubleshooting**, see [../troubleshooting/AGENTS.md](../troubleshooting/AGENTS.md)

---

## Form Complexity Decision Tree

### Tier 1 - Simple Forms (1-3 fields, basic validation)

**Examples**:
- Login (email + password)
- Newsletter signup (email only)
- Contact form (name + email + message)
- Search bar (single input)

**Pattern**: Client-side validation only, no Server Actions

**Setup Time**: 5 minutes

**Technologies**:
- React Hook Form (`useForm`)
- Zod (`zodResolver`)
- Client validation only

**When to use**:
- ✅ Simple authentication forms
- ✅ Newsletter signups
- ✅ Search functionality
- ✅ Contact forms without sensitive data

**When NOT to use**:
- ❌ Forms that create user accounts (need server validation - use Tier 2)
- ❌ Forms with payment information (need server validation + compliance)
- ❌ Forms with file uploads (use Tier 3)

**Code Example**:

```typescript
const loginSchema = z.object({
  email: z.string().email("Invalid email"),
  password: z.string().min(1, "Password required")
})

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(loginSchema)
})

<form onSubmit={handleSubmit(onSubmit)}>
  <input {...register("email")} type="email" />
  {errors.email && <p role="alert">{errors.email.message}</p>}

  <input {...register("password")} type="password" />
  {errors.password && <p role="alert">{errors.password.message}</p>}

  <button type="submit">Login</button>
</form>
```

**Key Features**:
- Uncontrolled components (no re-renders on keystroke)
- Client-side validation only
- No Server Actions
- `onSubmit` validation mode (default)

**Performance**:
- 5x faster than controlled components (Formik)
- Minimal bundle size (12KB React Hook Form + 12KB Zod = 24KB gzipped)

**See implementation**: [../workflows/AGENTS.md#workflow-1-create-simple-login-form-5-min](../workflows/AGENTS.md#workflow-1-create-simple-login-form-5-min)

---

### Tier 2 - Medium Forms (4-8 fields, cross-field validation)

**Examples**:
- User registration (email, password, confirm password, name, phone)
- Profile update (conditional fields based on user type)
- Address form (zip code validation, state/country dependency)
- Feedback form (rating, category, comments, email)

**Pattern**: Client + Server validation, Server Actions

**Setup Time**: 15 minutes

**Technologies**:
- React Hook Form + Zod (client)
- Server Actions with `useActionState` (server)
- Cross-field validation with `.refine()`

**When to use**:
- ✅ User account creation (security requirement)
- ✅ Forms that modify database (need server validation)
- ✅ Forms with cross-field validation (password confirmation, etc.)
- ✅ Forms with conditional fields

**When NOT to use**:
- ❌ Simple read-only forms (use Tier 1)
- ❌ Forms with file uploads or dynamic field arrays (use Tier 3)

**Code Example**:

```typescript
const signupSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
  confirmPassword: z.string()
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ["confirmPassword"]
})

// Server Action
"use server"
export async function signup(prevState: any, formData: FormData) {
  const validated = signupSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password"),
    confirmPassword: formData.get("confirmPassword")
  })

  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }

  // Create user...
}

// Form Component
const [state, formAction, isPending] = useActionState(signup, null)

<form action={formAction}>
  {/* fields */}
  {state?.errors?.email && <p role="alert">{state.errors.email}</p>}
</form>
```

**Key Features**:
- Client + server validation (security)
- Cross-field validation with `.refine()`
- Server Actions with `useActionState`
- Progressive enhancement (works without JavaScript)

**Security Benefits**:
- Client validation cannot be bypassed
- Server validation enforces business rules
- Same Zod schema reused client + server (DRY)

**See implementation**: [../workflows/AGENTS.md#workflow-2-add-server-validation-to-existing-form-10-min](../workflows/AGENTS.md#workflow-2-add-server-validation-to-existing-form-10-min)

---

### Tier 3 - Complex Forms (9+ fields, dynamic fields)

**Examples**:
- Multi-entity forms (user + company + payment info)
- Forms with file uploads (profile picture, resume, documents)
- Forms with dynamic field arrays (add/remove team members, line items)
- Forms with conditional logic (show fields based on selections)

**Pattern**: Full RHF + Zod + Server Actions + Optimistic UI

**Setup Time**: 30 minutes

**Technologies**:
- React Hook Form (`useForm`, `useFieldArray`, `Controller`)
- Zod with nested schemas
- Server Actions
- Optimistic UI with `useOptimistic` (React 19+)

**When to use**:
- ✅ Forms with file uploads (profile pictures, documents)
- ✅ Forms with dynamic field arrays (add/remove items)
- ✅ Forms with nested objects (user.address.street, user.company.name)
- ✅ Forms with third-party UI components (date pickers, rich text editors)

**When NOT to use**:
- ❌ Simple forms (overkill - use Tier 1 or 2)
- ❌ Multi-step forms (use Tier 4 for better UX)

**Code Example**:

```typescript
const profileSchema = z.object({
  name: z.string().min(1),
  email: z.string().email(),
  avatar: z.instanceof(File)
    .refine(file => file.size <= 5 * 1024 * 1024, "File must be < 5MB")
    .refine(file => ["image/jpeg", "image/png"].includes(file.type), "Only JPEG/PNG"),
  company: z.object({
    name: z.string(),
    size: z.enum(["1-10", "11-50", "51-200", "201+"])
  }),
  teamMembers: z.array(z.object({
    name: z.string(),
    email: z.string().email()
  }))
})

const { register, control, handleSubmit } = useForm({
  resolver: zodResolver(profileSchema)
})

const { fields, append, remove } = useFieldArray({
  control,
  name: "teamMembers"
})

<form onSubmit={handleSubmit(onSubmit)}>
  {/* Dynamic field array */}
  {fields.map((field, index) => (
    <div key={field.id}>
      <input {...register(`teamMembers.${index}.name`)} />
      <input {...register(`teamMembers.${index}.email`)} />
      <button type="button" onClick={() => remove(index)}>Remove</button>
    </div>
  ))}
  <button type="button" onClick={() => append({ name: "", email: "" })}>
    Add Team Member
  </button>

  <button type="submit">Save</button>
</form>
```

**Key Features**:
- Dynamic field arrays with `useFieldArray`
- File upload validation
- Nested object validation
- Controlled components with `Controller` (for third-party UI)

**useFieldArray API**:
- `fields`: Array of field objects with unique `id`
- `append(data)`: Add new field to end
- `prepend(data)`: Add new field to beginning
- `remove(index)`: Remove field at index
- `insert(index, data)`: Insert field at index
- `move(from, to)`: Reorder fields

**File Upload Validation**:
- `z.instanceof(File)`: Check if value is File object
- `.refine(file => file.size <= max)`: Validate file size
- `.refine(file => types.includes(file.type))`: Validate MIME type

**See protocol-spec.md** for complete file upload patterns and integration with SAP-035 (react-file-upload).

---

### Tier 4 - Wizard Forms (multi-step, state persistence)

**Examples**:
- Onboarding flows (3+ steps: account → profile → preferences → completion)
- Checkout process (cart → shipping → payment → review → confirmation)
- Survey forms (conditional branching based on answers)
- Application forms (personal → education → work history → documents)

**Pattern**: Multi-step state management, URL-based persistence

**Setup Time**: 45 minutes

**Technologies**:
- React Hook Form (separate form per step)
- Zod (separate schema per step)
- Next.js routing (`useSearchParams`, `useRouter`)
- React state for cross-step persistence

**When to use**:
- ✅ Onboarding flows with 3+ distinct steps
- ✅ Checkout processes
- ✅ Long forms that benefit from chunking (better UX)
- ✅ Forms with conditional branching (show Step 3 only if Step 2 = X)

**When NOT to use**:
- ❌ Forms with <3 steps (single form is simpler)
- ❌ Forms where user needs to see all fields at once (use Tier 3)

**Code Example**:

```typescript
const step1Schema = z.object({ name: z.string(), email: z.string().email() })
const step2Schema = z.object({ company: z.string(), role: z.string() })
const step3Schema = z.object({ preferences: z.array(z.string()) })

const searchParams = useSearchParams()
const router = useRouter()
const step = parseInt(searchParams.get("step") || "1")
const [formData, setFormData] = useState({})

const schema = step === 1 ? step1Schema : step === 2 ? step2Schema : step3Schema
const { register, handleSubmit } = useForm({ resolver: zodResolver(schema) })

function nextStep(data: any) {
  setFormData({ ...formData, ...data })
  router.push(`?step=${step + 1}`)
}

function prevStep() {
  router.push(`?step=${step - 1}`)
}

<div>
  {/* Progress indicator */}
  <div>Step {step} of 3</div>
  <div className="w-full bg-gray-200 h-2">
    <div className="bg-blue-600 h-2" style={{ width: `${(step / 3) * 100}%` }} />
  </div>

  {/* Form for current step */}
  <form onSubmit={handleSubmit(step === 3 ? onFinalSubmit : nextStep)}>
    {step === 1 && (
      <>
        <input {...register("name")} />
        <input {...register("email")} />
      </>
    )}
    {step === 2 && (
      <>
        <input {...register("company")} />
        <input {...register("role")} />
      </>
    )}
    {step === 3 && (
      <>
        {/* Preferences */}
      </>
    )}

    {/* Navigation */}
    {step > 1 && <button type="button" onClick={prevStep}>Back</button>}
    <button type="submit">{step === 3 ? "Submit" : "Next"}</button>
  </form>
</div>
```

**Key Features**:
- URL-based step persistence (`?step=2`)
- Browser back/forward buttons work
- Progress indicator
- Per-step validation (only validates current step)
- Cross-step data persistence in React state

**URL-based Benefits**:
- Shareable URLs (can bookmark specific step)
- Browser back/forward navigation works
- Progressive enhancement (URL reflects state)
- No session storage needed

**Integration with SAP-023 (react-state-management)**:
- Use TanStack Query for server state (wizard draft persistence)
- Use Zustand for complex wizard state logic
- Use URL state for simple step tracking (recommended)

**See implementation**: [../workflows/AGENTS.md#workflow-3-build-multi-step-wizard-30-min](../workflows/AGENTS.md#workflow-3-build-multi-step-wizard-30-min)

---

## Decision Tree: Which Tier Should I Use?

```
START: How many fields does your form have?

├─ 1-3 fields
│  ├─ Does it create user accounts or modify data?
│  │  ├─ YES → Tier 2 (need server validation)
│  │  └─ NO → Tier 1 (client-only validation)
│
├─ 4-8 fields
│  ├─ Does it have file uploads or dynamic fields?
│  │  ├─ YES → Tier 3 (useFieldArray, file validation)
│  │  └─ NO → Tier 2 (standard form)
│
├─ 9+ fields
│  ├─ Can it be split into logical steps?
│  │  ├─ YES → Tier 4 (wizard, better UX)
│  │  └─ NO → Tier 3 (single complex form)
```

---

## Tier Comparison Table

| Feature | Tier 1 | Tier 2 | Tier 3 | Tier 4 |
|---------|--------|--------|--------|--------|
| **Field Count** | 1-3 | 4-8 | 9+ | 9+ (multi-step) |
| **Setup Time** | 5 min | 15 min | 30 min | 45 min |
| **Client Validation** | ✅ | ✅ | ✅ | ✅ |
| **Server Validation** | ❌ | ✅ | ✅ | ✅ |
| **Cross-Field Validation** | ❌ | ✅ | ✅ | ✅ |
| **File Uploads** | ❌ | ❌ | ✅ | ✅ |
| **Dynamic Fields** | ❌ | ❌ | ✅ | ✅ |
| **Multi-Step** | ❌ | ❌ | ❌ | ✅ |
| **URL State** | ❌ | ❌ | ❌ | ✅ |
| **Progressive Enhancement** | ❌ | ✅ | ✅ | ✅ |
| **React Hook Form API** | `useForm` | `useForm` | `useForm` + `useFieldArray` | `useForm` |
| **Example Use Cases** | Login, Newsletter | Signup, Profile | Company Form, Invoice | Onboarding, Checkout |

---

## Migration Path: Upgrading Between Tiers

### From Tier 1 to Tier 2 (Add Server Validation)

**Scenario**: You built a login form (Tier 1) and now want to add user registration (needs server validation).

**Steps**:
1. Keep existing Zod schema
2. Add Server Action (see [../workflows/AGENTS.md#workflow-2](../workflows/AGENTS.md#workflow-2))
3. Replace `handleSubmit` with `useActionState`
4. Update form to use native `action` instead of `onSubmit`

**Time**: 10 minutes

---

### From Tier 2 to Tier 3 (Add Dynamic Fields)

**Scenario**: You have a profile form (Tier 2) and need to add dynamic team members array.

**Steps**:
1. Update schema with `z.array()` for dynamic fields
2. Add `useFieldArray` to form
3. Implement add/remove buttons
4. Update Server Action to handle array data

**Time**: 20 minutes

---

### From Tier 3 to Tier 4 (Convert to Wizard)

**Scenario**: Your complex form (Tier 3) is overwhelming users, want to split into steps.

**Steps**:
1. Split single schema into per-step schemas
2. Add URL state with `useSearchParams`
3. Conditional rendering per step
4. Add progress indicator
5. Persist cross-step data in React state

**Time**: 30 minutes

---

## Anti-Patterns: Common Mistakes

### ❌ Anti-Pattern 1: Using Tier 3 for Simple Forms

**Problem**: `useFieldArray` for a form with 2 fields

**Solution**: Use Tier 1 or 2 (simpler patterns)

---

### ❌ Anti-Pattern 2: Client-Only Validation for User Creation

**Problem**: User registration form with only client validation (Tier 1)

**Solution**: Always use Tier 2 (server validation) for security

---

### ❌ Anti-Pattern 3: Single Form with 20+ Fields

**Problem**: Overwhelming UX, high abandonment rate

**Solution**: Use Tier 4 (wizard) to chunk into logical steps

---

### ❌ Anti-Pattern 4: Session Storage for Wizard State

**Problem**: Wizard state persisted in `localStorage`/`sessionStorage`

**Solution**: Use URL state (`?step=2`) for better UX and progressive enhancement

---

## Version History

**1.0.0 (2025-11-10)** - Initial form patterns extraction from awareness-guide.md
- Form Complexity Decision Tree (Tier 1-4)
- Decision flowchart
- Tier comparison table
- Migration paths between tiers
- Anti-patterns
