# SAP-041: React Form Validation - Claude Agent Awareness

**SAP**: SAP-041 (react-form-validation)
**Version**: 1.0.0
**Claude Compatibility**: Sonnet 4.5+
**Last Updated**: 2025-11-09

---

## 📖 Quick Reference

**New to SAP-041?** → Read **[README.md](README.md)** first (10-min read)

The README provides:
- 🚀 **Quick Start** - Quick setup with production-ready configuration
- 📚 **Time Savings** - 50% reduction
- 🎯 **Feature 1** - Core feature 1
- 🔧 **Feature 2** - Core feature 2
- 📊 **Feature 3** - Core feature 3
- 🔗 **Integration** - Works with SAP-020 (Foundation)

This CLAUDE.md provides: Claude Code-specific workflows for implementing SAP-041.
s.

---

## Quick Start for Claude

### When User Says...

| User Request | Read This | Priority |
|--------------|-----------|----------|
| "Create a signup form" | awareness-guide.md (Workflow 1: Simple Form) | Phase 1 |
| "Add validation to my form" | adoption-blueprint.md (Option A or B) | Phase 2 |
| "Make form accessible" | awareness-guide.md (Accessibility Checklist) | Phase 1 |
| "Build multi-step form" | protocol-spec.md (Tutorial: Multi-step wizard) | Phase 2 |
| "Add server validation" | awareness-guide.md (Workflow 2: Server Validation) | Phase 1 |
| "Fix form not working" | awareness-guide.md (Troubleshooting Guide) | Phase 1 |
| "Why React Hook Form?" | capability-charter.md (Problem Statement) | Phase 3 |
| "How do I do X?" | protocol-spec.md (How-to guides) | Phase 2 |

### Progressive Context Loading

**Phase 1** (Quick reference, 5-10 min):
- Read **awareness-guide.md** only (~68KB, 10k tokens)
- Use for: Quick questions, decision trees, workflows, troubleshooting

**Phase 2** (Implementation, 15-30 min):
- Read **adoption-blueprint.md** (~38KB, 6k tokens)
- Read **protocol-spec.md** (~65KB, 10k tokens)
- Use for: Step-by-step setup, complete API reference, how-to guides

**Phase 3** (Deep understanding, 30+ min):
- Read **capability-charter.md** (~30KB, 5k tokens)
- Read **ledger.md** (~20KB, 3k tokens)
- Use for: Design rationale, evidence, metrics, adoption history

**Total token budget**:
- Phase 1: ~10k tokens
- Phase 2: ~26k tokens (cumulative)
- Phase 3: ~34k tokens (cumulative)

---

## Progressive Context Loading Strategy

### Phase 1: Orientation (awareness-guide.md)

**Read when**:
- User asks "how do I validate forms in React?"
- User wants quick reference or decision tree
- User needs workflow example (copy-paste code)
- User reports issue (troubleshooting)

**Key sections**:
- **Quick Reference**: 30-second overview
- **Form Complexity Decision Tree**: Tier 1-4 (simple to wizard)
- **Common Workflows**: 3 copy-paste examples
  - Workflow 1: Simple login form (5 min)
  - Workflow 2: Add server validation (10 min)
  - Workflow 3: Multi-step wizard (30 min)
- **Accessibility Checklist**: WCAG 2.2 Level AA requirements
- **Troubleshooting Guide**: Common issues and fixes

**Token cost**: ~10k tokens

**Output**: Quick understanding, working code examples

---

### Phase 2: Implementation (adoption-blueprint.md + protocol-spec.md)

**Read adoption-blueprint.md when**:
- User says "set up React Hook Form in my project"
- User wants step-by-step installation guide
- User needs working code example (full form component)

**Key sections**:
- **Prerequisites**: Next.js 15+, React 19+, TypeScript
- **Installation**: npm install, directory setup
- **Quick Start**: Option A (client-only) or Option B (full-stack)
- **Validation Checklist**: Functional, accessibility, performance

**Token cost**: ~6k tokens

---

**Read protocol-spec.md when**:
- User needs complete API reference
- User asks "how do I do X with React Hook Form?"
- User building complex form (Tier 3-4)
- User needs advanced patterns (file upload, async validation, etc.)

**Key sections**:
- **Reference**: Complete API documentation
  - React Hook Form hooks (useForm, useFieldArray, etc.)
  - Zod validation methods (.string(), .refine(), etc.)
  - Server Action patterns
- **How-to Guides**: 12 task-oriented guides
  - Set up React Hook Form with Zod
  - Add server-side validation
  - Handle file uploads
  - Create multi-step wizards
  - etc.
- **Tutorials**: 3 learning-oriented tutorials
  - Build simple signup form (15 min)
  - Build complex multi-entity form (45 min)
  - Build multi-step wizard (60 min)

**Token cost**: ~10k tokens

---

### Phase 3: Deep Understanding (capability-charter.md + ledger.md)

**Read capability-charter.md when**:
- User asks "why React Hook Form over Formik?"
- User needs design rationale (why this approach?)
- User wants evidence for business value

**Key sections**:
- **Problem Statement**: Current challenges with form validation
- **Solution Design**: Why React Hook Form + Zod
- **Success Criteria**: Metrics, benchmarks
- **Business Value**: Time savings, cost savings

**Token cost**: ~5k tokens

---

**Read ledger.md when**:
- User asks "how much time will this save?"
- User wants evidence (npm downloads, production usage)
- User needs adoption metrics (bundle size, performance)
- User wants to know validation status (pilot vs production)

**Key sections**:
- **Metrics**: Time savings (88.9%), bundle size (24KB), performance
- **Evidence Base**: npm downloads, State of JS, production companies
- **Dogfooding History**: Validation status, success criteria
- **Version History**: Changelog, planned features

**Token cost**: ~3k tokens

---

## Claude Code Workflows

### Workflow 1: Generate Simple Form (5 min)

**User**: "Create a login form with email and password"

**Claude Steps**:

1. **Read awareness-guide.md** (Workflow 1: Simple Form pattern)

2. **Generate Zod schema**:
   ```typescript
   // lib/validations/auth.ts
   import { z } from "zod"

   export const loginSchema = z.object({
     email: z.string()
       .min(1, "Email is required")
       .email("Invalid email address"),
     password: z.string()
       .min(1, "Password is required")
   })

   export type LoginFormData = z.infer<typeof loginSchema>
   ```

3. **Generate form component**:
   ```typescript
   // components/forms/LoginForm.tsx
   "use client"

   import { useForm } from "react-hook-form"
   import { zodResolver } from "@hookform/resolvers/zod"
   import { loginSchema, type LoginFormData } from "@/lib/validations/auth"

   export function LoginForm() {
     const {
       register,
       handleSubmit,
       formState: { errors, isSubmitting }
     } = useForm<LoginFormData>({
       resolver: zodResolver(loginSchema)
     })

     async function onSubmit(data: LoginFormData) {
       console.log("Login data:", data)
       // TODO: Send to server
     }

     return (
       <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
         {/* Email field */}
         <div>
           <label htmlFor="email" className="block text-sm font-medium">
             Email Address <span className="text-red-600">*</span>
           </label>
           <input
             id="email"
             {...register("email")}
             type="email"
             aria-invalid={errors.email ? "true" : "false"}
             aria-describedby={errors.email ? "email-error" : undefined}
             className="mt-1 block w-full px-3 py-2 border rounded-md"
           />
           {errors.email && (
             <p id="email-error" role="alert" className="mt-1 text-sm text-red-600">
               {errors.email.message}
             </p>
           )}
         </div>

         {/* Password field */}
         <div>
           <label htmlFor="password" className="block text-sm font-medium">
             Password <span className="text-red-600">*</span>
           </label>
           <input
             id="password"
             {...register("password")}
             type="password"
             aria-invalid={errors.password ? "true" : "false"}
             aria-describedby={errors.password ? "password-error" : undefined}
             className="mt-1 block w-full px-3 py-2 border rounded-md"
           />
           {errors.password && (
             <p id="password-error" role="alert" className="mt-1 text-sm text-red-600">
               {errors.password.message}
             </p>
           )}
         </div>

         {/* Submit button */}
         <button
           type="submit"
           disabled={isSubmitting}
           className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 disabled:opacity-50"
         >
           {isSubmitting ? "Logging in..." : "Login"}
         </button>
       </form>
     )
   }
   ```

4. **Verify**:
   - TypeScript types inferred from schema (no manual types)
   - Accessibility attributes included (aria-invalid, aria-describedby, role="alert")
   - Error messages displayed correctly
   - Loading state shown (isSubmitting)

**Token usage**: ~10k (read awareness-guide.md)

**Time**: 5 minutes

---

### Workflow 2: Add Server Validation to Existing Form (10 min)

**User**: "Add server-side validation to my signup form"

**Claude Steps**:

1. **Read awareness-guide.md** (Workflow 2: Server Validation pattern)

2. **Check if Zod schema exists**:
   - If yes: Reuse schema
   - If no: Create schema first (see Workflow 1)

3. **Create Server Action**:
   ```typescript
   // actions/auth.ts
   "use server"

   import { signupSchema } from "@/lib/validations/auth"
   import { redirect } from "next/navigation"

   export async function signup(prevState: any, formData: FormData) {
     // Extract form data
     const rawData = {
       email: formData.get("email"),
       password: formData.get("password")
     }

     // Validate with Zod
     const validatedFields = signupSchema.safeParse(rawData)

     if (!validatedFields.success) {
       return {
         errors: validatedFields.error.flatten().fieldErrors,
         message: "Validation failed"
       }
     }

     // TODO: Create user in database
     // const user = await prisma.user.create({ ... })

     redirect("/dashboard")
   }
   ```

4. **Update form component to use useActionState**:
   ```typescript
   "use client"

   import { useActionState } from "react"
   import { signup } from "@/actions/auth"

   export function SignupForm() {
     const [state, formAction, isPending] = useActionState(signup, null)

     return (
       <form action={formAction} className="space-y-4">
         {/* Email field */}
         <div>
           <label htmlFor="email">Email Address *</label>
           <input
             id="email"
             name="email"
             type="email"
             required
             aria-invalid={state?.errors?.email ? "true" : "false"}
             aria-describedby={state?.errors?.email ? "email-error" : undefined}
           />
           {state?.errors?.email && (
             <p id="email-error" role="alert">
               {state.errors.email[0]}
             </p>
           )}
         </div>

         {/* Password field */}
         <div>
           <label htmlFor="password">Password *</label>
           <input
             id="password"
             name="password"
             type="password"
             required
             aria-invalid={state?.errors?.password ? "true" : "false"}
             aria-describedby={state?.errors?.password ? "password-error" : undefined}
           />
           {state?.errors?.password && (
             <p id="password-error" role="alert">
               {state.errors.password[0]}
             </p>
           )}
         </div>

         {/* Global error */}
         {state?.message && (
           <div role="alert" className="p-3 bg-red-50 text-red-800">
             {state.message}
           </div>
         )}

         {/* Submit button */}
         <button type="submit" disabled={isPending}>
           {isPending ? "Creating account..." : "Sign Up"}
         </button>
       </form>
     )
   }
   ```

5. **Verify**:
   - Server Action has `"use server"` directive
   - Form uses `action={formAction}` (not `onSubmit`)
   - Error state from server displayed correctly
   - Loading state shown (`isPending`)
   - Progressive enhancement (works without JavaScript)

**Token usage**: ~10k (read awareness-guide.md)

**Time**: 10 minutes

---

### Workflow 3: Build Multi-Step Wizard (30 min)

**User**: "Create a 3-step onboarding form: Account → Profile → Preferences"

**Claude Steps**:

1. **Read protocol-spec.md** (Tutorial: Multi-step wizard)

2. **Define schemas for each step**:
   ```typescript
   // lib/validations/onboarding.ts
   import { z } from "zod"

   export const step1Schema = z.object({
     email: z.string().email("Invalid email"),
     password: z.string().min(8, "Password must be at least 8 characters")
   })

   export const step2Schema = z.object({
     name: z.string().min(1, "Name is required"),
     company: z.string().min(1, "Company is required"),
     role: z.string().min(1, "Role is required")
   })

   export const step3Schema = z.object({
     newsletter: z.boolean(),
     notifications: z.boolean(),
     theme: z.enum(["light", "dark", "system"])
   })

   export type OnboardingStep1 = z.infer<typeof step1Schema>
   export type OnboardingStep2 = z.infer<typeof step2Schema>
   export type OnboardingStep3 = z.infer<typeof step3Schema>
   ```

3. **Create wizard state management**:
   ```typescript
   // components/forms/OnboardingWizard.tsx
   "use client"

   import { useState } from "react"
   import { useForm } from "react-hook-form"
   import { zodResolver } from "@hookform/resolvers/zod"
   import { useRouter, useSearchParams } from "next/navigation"
   import { step1Schema, step2Schema, step3Schema } from "@/lib/validations/onboarding"

   export function OnboardingWizard() {
     const router = useRouter()
     const searchParams = useSearchParams()
     const step = parseInt(searchParams.get("step") || "1")
     const [formData, setFormData] = useState({})

     // Select schema based on current step
     const schema = step === 1 ? step1Schema : step === 2 ? step2Schema : step3Schema

     const { register, handleSubmit, formState: { errors } } = useForm({
       resolver: zodResolver(schema),
       defaultValues: formData
     })

     function nextStep(data: any) {
       setFormData({ ...formData, ...data })
       router.push(`?step=${step + 1}`)
     }

     function prevStep() {
       router.push(`?step=${step - 1}`)
     }

     async function onFinalSubmit(data: any) {
       const finalData = { ...formData, ...data }
       console.log("Final data:", finalData)
       // TODO: Send to server
       router.push("/dashboard")
     }

     return (
       <div className="max-w-2xl mx-auto p-6">
         {/* Progress indicator */}
         <div className="mb-8">
           <div className="flex justify-between mb-2">
             <span>Step {step} of 3</span>
             <span>{step === 1 ? "Account" : step === 2 ? "Profile" : "Preferences"}</span>
           </div>
           <div className="w-full bg-gray-200 h-2 rounded">
             <div
               className="bg-blue-600 h-2 rounded transition-all"
               style={{ width: `${(step / 3) * 100}%` }}
             />
           </div>
         </div>

         {/* Form */}
         <form onSubmit={handleSubmit(step === 3 ? onFinalSubmit : nextStep)}>
           {/* Step 1: Account */}
           {step === 1 && (
             <>
               <h2>Create your account</h2>
               {/* Email, Password fields */}
             </>
           )}

           {/* Step 2: Profile */}
           {step === 2 && (
             <>
               <h2>Tell us about yourself</h2>
               {/* Name, Company, Role fields */}
             </>
           )}

           {/* Step 3: Preferences */}
           {step === 3 && (
             <>
               <h2>Set your preferences</h2>
               {/* Newsletter, Notifications, Theme fields */}
             </>
           )}

           {/* Navigation */}
           <div className="flex justify-between pt-4">
             {step > 1 && (
               <button type="button" onClick={prevStep}>Back</button>
             )}
             <button type="submit" className="ml-auto">
               {step === 3 ? "Complete Setup" : "Next"}
             </button>
           </div>
         </form>
       </div>
     )
   }
   ```

4. **Create wizard page**:
   ```typescript
   // app/onboarding/page.tsx
   import { OnboardingWizard } from "@/components/forms/OnboardingWizard"

   export default function OnboardingPage() {
     return <OnboardingWizard />
   }
   ```

5. **Verify**:
   - URL reflects current step (progressive enhancement)
   - Form data persisted across steps
   - Back button works (browser navigation)
   - Each step validated independently
   - Final step submits all data

**Token usage**: ~10k (read protocol-spec.md Tutorial section)

**Time**: 30 minutes

---

### Workflow 4: Make Form Accessible (15 min)

**User**: "Make my signup form WCAG 2.2 Level AA compliant"

**Claude Steps**:

1. **Read awareness-guide.md** (Accessibility Checklist)

2. **Audit existing form** (check these items):
   - [ ] All fields have labels
   - [ ] Labels associated (htmlFor + id)
   - [ ] Errors identified (aria-invalid)
   - [ ] Errors associated (aria-describedby)
   - [ ] Errors announced (role="alert")
   - [ ] Required fields indicated
   - [ ] Keyboard navigation works

3. **Add missing accessibility attributes**:
   ```typescript
   <div>
     <label htmlFor="email" className={errors.email ? "text-red-600" : ""}>
       Email Address <span aria-label="required">*</span>
     </label>
     <input
       id="email"
       {...register("email")}
       type="email"
       aria-invalid={errors.email ? "true" : "false"}
       aria-describedby={errors.email ? "email-error" : undefined}
       aria-required="true"
       className={errors.email ? "border-red-600" : "border-gray-300"}
     />
     {errors.email && (
       <p id="email-error" role="alert" aria-live="assertive" className="text-red-600">
         {errors.email.message}
       </p>
     )}
   </div>
   ```

4. **Suggest axe DevTools testing**:
   ```bash
   npm install -D @axe-core/react
   ```

5. **Suggest manual testing**:
   - Tab through fields (check focus order)
   - Press Enter on submit button
   - Use screen reader (NVDA, VoiceOver)

6. **Verify**:
   - 0 axe-core violations
   - Lighthouse accessibility score 100
   - Screen reader announces errors
   - Tab order logical
   - Focus visible

**Token usage**: ~10k (read awareness-guide.md Accessibility section)

**Time**: 15 minutes

---

## Form Complexity Decision Prompts

### When User Says...

**"Create a simple form"** → Use **Tier 1** pattern (client-side only, 5 min)
- 1-3 fields
- Basic validation (required, email, min length)
- No server validation needed
- Example: Login, newsletter signup, search bar

**"Create a signup form"** → Use **Tier 2** pattern (client + server, 15 min)
- 4-8 fields
- Cross-field validation (password confirmation)
- Server validation required (security)
- Example: User registration, profile update, address form

**"Create a checkout form"** → Use **Tier 3** pattern (complex validation, 30 min)
- 9+ fields
- Dynamic fields (add/remove items)
- File uploads
- Conditional logic
- Example: Multi-entity forms, forms with file uploads

**"Create an onboarding flow"** → Use **Tier 4** pattern (wizard, 45 min)
- Multi-step (3+ steps)
- State persistence across steps
- URL-based navigation
- Progress indicator
- Example: Onboarding, checkout, survey, application

---

## Decision Tree

```
User request → Form complexity?
├─ 1-3 fields, basic validation → Tier 1 (Simple, 5 min)
│  └─ Client-side only, no Server Actions
│  └─ Read: awareness-guide.md (Workflow 1)
│
├─ 4-8 fields, cross-field validation → Tier 2 (Medium, 15 min)
│  └─ Client + Server validation, Server Actions
│  └─ Read: awareness-guide.md (Workflow 2) + adoption-blueprint.md (Option B)
│
├─ 9+ fields, dynamic fields, file uploads → Tier 3 (Complex, 30 min)
│  └─ Full RHF + Zod + Server Actions + Optimistic UI
│  └─ Read: protocol-spec.md (How-to guides)
│
└─ Multi-step, conditional branching → Tier 4 (Wizard, 45 min)
   └─ Multi-step state, URL persistence, progress indicator
   └─ Read: protocol-spec.md (Tutorial: Multi-step wizard)
```

---

## Code Generation Patterns

### Pattern 1: Schema-First Generation

**Always start with Zod schema**, then generate:

1. **Schema** (single source of truth):
   ```typescript
   const schema = z.object({
     email: z.string().email("Invalid email"),
     password: z.string().min(8, "Password must be at least 8 characters")
   })
   ```

2. **Type** (inferred, no manual definition):
   ```typescript
   type FormData = z.infer<typeof schema>
   ```

3. **Form component** (uses schema):
   ```typescript
   const { register, handleSubmit } = useForm<FormData>({
     resolver: zodResolver(schema)
   })
   ```

4. **Server Action** (uses same schema):
   ```typescript
   "use server"
   export async function submit(formData: FormData) {
     const validated = schema.safeParse({ email: formData.get("email"), ... })
     if (!validated.success) {
       return { errors: validated.error.flatten().fieldErrors }
     }
     // Process...
   }
   ```

**Benefits**:
- Single source of truth (schema)
- Zero manual TypeScript types
- Client + server use same validation logic
- No type drift

---

### Pattern 2: Accessibility-First Generation

**Always include accessibility attributes** when generating forms:

**Required attributes**:
```typescript
<div>
  <label htmlFor="field-id">
    Label <span aria-label="required">*</span>
  </label>
  <input
    id="field-id"
    name="field"
    aria-invalid={errors.field ? "true" : "false"}
    aria-describedby={errors.field ? "field-error" : undefined}
    aria-required="true"
  />
  {errors.field && (
    <p id="field-error" role="alert" aria-live="assertive">
      {errors.field.message}
    </p>
  )}
</div>
```

**Don't generate** (missing accessibility):
```typescript
// ❌ Bad: Missing ARIA attributes
<input {...register("email")} />
{errors.email && <p>{errors.email.message}</p>}
```

---

### Pattern 3: Progressive Enhancement

**Always use Server Actions for form submission** (not client-side fetch):

**Generate**:
```typescript
// ✅ Good: Works without JavaScript
<form action={formAction}>
  <input name="email" required />
  <button type="submit">Submit</button>
</form>
```

**Don't generate**:
```typescript
// ❌ Bad: Requires JavaScript
<form onSubmit={handleSubmit(async (data) => {
  await fetch("/api/submit", { body: JSON.stringify(data) })
})}>
```

**Why**: Forms should work without JavaScript (progressive enhancement)

---

## Integration Patterns with Other SAPs

### SAP-020 (react-foundation)

**When generating Server Actions**:

1. Always add `"use server"` directive
2. Use React 19 hooks (useActionState, not deprecated useFormState)
3. Return structured errors:
   ```typescript
   return { errors: validated.error.flatten().fieldErrors }
   ```

**Example**:
```typescript
"use server"

import { signupSchema } from "@/lib/validations/auth"

export async function signup(prevState: any, formData: FormData) {
  const validated = signupSchema.safeParse({
    email: formData.get("email"),
    password: formData.get("password")
  })

  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }

  // Process signup...
}
```

---

### SAP-033 (react-authentication)

**When generating protected forms**:

1. Check authentication in Server Action:
   ```typescript
   "use server"
   import { auth } from "@/auth"

   export async function updateProfile(formData: FormData) {
     const session = await auth()
     if (!session) throw new Error("Unauthorized")

     // Validate and update...
   }
   ```

2. Include user context in validation:
   ```typescript
   const schema = z.object({
     email: z.string().email(),
     userId: z.string().uuid() // From session
   })
   ```

---

### SAP-034 (react-database-integration)

**When generating forms that persist to database**:

1. Match Zod schema to Prisma/Drizzle schema:
   ```typescript
   import { Prisma } from "@prisma/client"

   const userSchema = z.object({
     email: z.string().email(),
     name: z.string()
   }) satisfies z.ZodType<Prisma.UserCreateInput>
   ```

2. Handle database errors in Server Action:
   ```typescript
   try {
     await prisma.user.create({ data: validated.data })
   } catch (error: any) {
     if (error.code === "P2002") { // Unique constraint
       return { errors: { email: ["Email already exists"] } }
     }
     throw error
   }
   ```

---

### SAP-026 (react-accessibility)

**When generating accessible forms**:

1. Always include WCAG 2.2 Level AA attributes (see Pattern 2 above)
2. Suggest axe-core testing:
   ```bash
   npm install -D @axe-core/react
   ```
3. Mention screen reader testing (NVDA, VoiceOver, JAWS)

---

### SAP-023 (react-state-management)

**When generating wizard forms**:

1. Use URL state for step persistence:
   ```typescript
   import { useSearchParams, useRouter } from "next/navigation"

   const searchParams = useSearchParams()
   const router = useRouter()
   const step = parseInt(searchParams.get("step") || "1")

   function nextStep() {
     router.push(`?step=${step + 1}`)
   }
   ```

2. Benefits:
   - URL reflects application state
   - Browser back/forward works
   - Shareable URLs (bookmark specific step)
   - Progressive enhancement

---

## Common Claude Pitfalls

### Pitfall 1: Generating Controlled Components

**Problem**: Claude generates `<input value={watch("field")} />` (causes re-renders)

**Fix**: Always use uncontrolled with `register()`:
```typescript
// ✅ Correct
<input {...register("email")} />

// ❌ Avoid
<input value={watch("email")} onChange={e => setValue("email", e.target.value)} />
```

**Exception**: Use controlled for third-party components (date pickers, rich text editors):
```typescript
<Controller
  name="birthdate"
  control={control}
  render={({ field }) => <DatePicker {...field} />}
/>
```

---

### Pitfall 2: Missing Server Validation

**Problem**: Claude generates client-side validation only

**Fix**: Always generate Server Action with validation:
```typescript
"use server"
export async function submit(formData: FormData) {
  const validated = schema.safeParse({ /* data */ })
  if (!validated.success) {
    return { errors: validated.error.flatten().fieldErrors }
  }
  // Process...
}
```

**Why**: Client validation can be bypassed via DevTools

---

### Pitfall 3: Inaccessible Error Messages

**Problem**: Claude generates `{errors.email && <p>{errors.email.message}</p>}` without ARIA

**Fix**: Always include accessibility attributes:
```typescript
{errors.email && (
  <p id="email-error" role="alert" aria-live="assertive">
    {errors.email.message}
  </p>
)}
<input aria-describedby={errors.email ? "email-error" : undefined} />
```

---

### Pitfall 4: Manual TypeScript Types

**Problem**: Claude generates manual types alongside Zod schemas (drift risk)

**Fix**: Always infer types from schemas:
```typescript
// ✅ Correct: Infer from schema
const schema = z.object({ email: z.string().email() })
type FormData = z.infer<typeof schema>

// ❌ Avoid: Manual types (can drift)
interface FormData { email: string }
const schema = z.object({ email: z.string().email() })
```

---

### Pitfall 5: Incorrect Error Format

**Problem**: Server Action returns errors as strings instead of arrays

**Fix**: Use Zod's `flatten().fieldErrors`:
```typescript
// ✅ Correct: Returns { email: ["Error message"] }
return { errors: validated.error.flatten().fieldErrors }

// ❌ Wrong: Returns { email: "Error message" }
return { errors: { email: validated.error.errors[0].message } }
```

**Why**: Form expects `string[]` format for consistency

---

## Troubleshooting for Claude

### When User Reports...

**"Form validation not working"**:
- Check `resolver: zodResolver(schema)` in `useForm()`
- Check schema imported correctly
- Check `formState: { errors }` destructured

**"TypeScript errors"**:
- Check Zod version (need 3.20+ for `z.infer`)
- Check types inferred from schema (not manual types)
- Check schema matches form fields

**"Server Action not working"**:
- Check `"use server"` directive at top of file
- Check function is exported
- Check return format: `{ errors: { field: ["message"] } }`

**"Errors not displaying"**:
- Check `formState.errors` destructured
- Check error format (array vs string)
- Check conditional rendering: `{errors.field && ...}`

**"Form not accessible"**:
- Run axe DevTools scan
- Check Accessibility Checklist in awareness-guide.md
- Verify ARIA attributes present

---

## Next Steps for Claude

After generating form:

1. **Suggest testing**:
   - Functional: Submit form, verify validation
   - Accessibility: Run axe DevTools, Lighthouse
   - TypeScript: Verify no type errors
   - Performance: Check bundle size, re-renders

2. **Suggest integration**:
   - SAP-033: Add authentication check
   - SAP-034: Persist to database
   - SAP-026: Full accessibility audit

3. **Suggest improvements**:
   - Add loading indicators
   - Add optimistic updates (useOptimistic)
   - Add progressive enhancement test (disable JS)
   - Add real-time validation (mode: "onChange")

---

## Progressive Loading Summary

| Phase | Files | Tokens | Use Case |
|-------|-------|--------|----------|
| **Phase 1** | awareness-guide.md | ~10k | Quick tasks, workflows, troubleshooting |
| **Phase 2** | + adoption-blueprint.md<br>+ protocol-spec.md | ~26k | Implementation, setup, API reference |
| **Phase 3** | + capability-charter.md<br>+ ledger.md | ~34k | Design rationale, evidence, metrics |

**Recommendation**:
- 90% of tasks: Phase 1 only (awareness-guide.md)
- 9% of tasks: Phase 2 (add adoption-blueprint.md or protocol-spec.md)
- 1% of tasks: Phase 3 (add capability-charter.md or ledger.md)

---

## Version History

**1.0.0 (2025-11-09)** - Initial Release
- Progressive context loading strategy (3 phases)
- 4 Claude Code workflows (simple form, server validation, wizard, accessibility)
- Form complexity decision tree (Tier 1-4)
- 3 code generation patterns (schema-first, accessibility-first, progressive enhancement)
- Integration patterns for 5 SAPs (SAP-020, SAP-033, SAP-034, SAP-026, SAP-023)
- 5 common pitfalls and fixes
- Troubleshooting guide for Claude
- Next steps suggestions

---

**Related Artifacts**:
- [Awareness Guide](awareness-guide.md) - Quick reference, workflows, decision trees
- [Adoption Blueprint](adoption-blueprint.md) - 20-minute installation guide
- [Protocol Spec](protocol-spec.md) - Complete technical documentation
- [Capability Charter](capability-charter.md) - Problem/solution design
- [Ledger](ledger.md) - Metrics, evidence, adoption tracking
- [README](README.md) - One-page overview
