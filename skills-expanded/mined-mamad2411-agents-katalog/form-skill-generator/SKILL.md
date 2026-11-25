---
name: form-skill-generator
description: "Generate a project-specific form patterns skill. Use for frontend apps to document form handling. Triggers on: generate form skill, create form patterns, form-skill-generator."
type: meta
generates: form-patterns
trigger:
  condition: has frontend app
---

# Form Skill Generator

Generate a project-specific `form-patterns` skill that documents exactly how forms are built in THIS project.

---

## The Job

1. Read project context (`docs/project.json`)
2. Analyze existing form implementations
3. Ask clarifying questions about form patterns
4. Generate `docs/skills/form-patterns/SKILL.md`
5. Update `project.json` to record the generated skill

---

## Step 1: Read Project Context

```bash
cat docs/project.json
```

Look for:
- `apps[].type` — includes "frontend" or "fullstack"
- `stack.framework` — React, Vue, etc.
- `security.inputValidation` — zod, yup, etc.

---

## Step 2: Analyze Existing Form Implementations

```bash
# Find form components
find . -type f -name "*Form*.tsx" | grep -v node_modules | head -20

# Find form libraries
grep -E "react-hook-form|formik|useForm" package.json 2>/dev/null

# Find validation schemas
find . -type f -name "*schema*" | grep -v node_modules | head -10

# Look at existing form
cat $(find . -type f -name "*Form*.tsx" | grep -v node_modules | head -1) 2>/dev/null | head -50
```

---

## Step 3: Clarifying Questions

```
I found the following form patterns:

Form Library: [detected]
Validation: [detected]
UI Components: [detected]

Please confirm or correct:

1. What form library do you use?
   A. react-hook-form
   B. Formik
   C. Native form handling
   D. Server Actions with useFormState
   E. Other: [specify]

2. What validation library?
   A. Zod
   B. Yup
   C. Joi
   D. Built into form library
   E. Custom

3. What UI components for form fields?
   A. Custom components
   B. shadcn/ui
   C. Radix UI
   D. Chakra UI
   E. MUI
   F. Other: [specify]

4. How are forms submitted?
   A. API call (fetch/axios)
   B. Server Actions
   C. GraphQL mutation
   D. Form action to API route
```

---

## Step 4: Generate the Skill

Create `docs/skills/form-patterns/SKILL.md`:

```markdown
---
name: form-patterns
description: "Build forms with validation and submission in [PROJECT_NAME]"
project-specific: true
generated-by: form-skill-generator
generated-at: [DATE]
---

# Form Patterns Skill

How to build forms in this project.

---

## Quick Reference

| Task | Pattern |
|------|---------|
| Create form | Use `useForm` + Zod resolver |
| Add field | Use `FormField` component |
| Submit | Call server action or API |
| Show errors | Use `FormMessage` component |

---

## Architecture

- **Form Library:** [FORM_LIBRARY] (e.g., react-hook-form)
- **Validation:** [VALIDATION_LIB] (e.g., Zod)
- **UI Components:** [UI_LIB] (e.g., shadcn/ui)
- **Submission:** [SUBMISSION_PATTERN] (e.g., Server Actions)

---

## Basic Form Template

\`\`\`typescript
// components/[Entity]Form.tsx
'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import { Button } from '@/components/ui/button'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { createEntity } from '@/actions/entity'
import { toast } from 'sonner'

// Schema
const formSchema = z.object({
  name: z.string().min(1, 'Name is required').max(100),
  email: z.string().email('Invalid email'),
  description: z.string().optional(),
})

type FormValues = z.infer<typeof formSchema>

interface EntityFormProps {
  onSuccess?: () => void
  defaultValues?: Partial<FormValues>
}

export function EntityForm({ onSuccess, defaultValues }: EntityFormProps) {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: '',
      email: '',
      description: '',
      ...defaultValues,
    },
  })

  const onSubmit = async (data: FormValues) => {
    try {
      await createEntity(data)
      toast.success('Entity created successfully')
      form.reset()
      onSuccess?.()
    } catch (error) {
      toast.error('Failed to create entity')
    }
  }

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="name"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Name</FormLabel>
              <FormControl>
                <Input placeholder="Enter name" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Email</FormLabel>
              <FormControl>
                <Input type="email" placeholder="email@example.com" {...field} />
              </FormControl>
              <FormDescription>
                We'll never share your email.
              </FormDescription>
              <FormMessage />
            </FormItem>
          )}
        />

        <FormField
          control={form.control}
          name="description"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Description (optional)</FormLabel>
              <FormControl>
                <Textarea placeholder="Enter description" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />

        <Button type="submit" disabled={form.formState.isSubmitting}>
          {form.formState.isSubmitting ? 'Creating...' : 'Create'}
        </Button>
      </form>
    </Form>
  )
}
\`\`\`

---

## Field Types

### Text Input

\`\`\`typescript
<FormField
  control={form.control}
  name="name"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Name</FormLabel>
      <FormControl>
        <Input {...field} />
      </FormControl>
      <FormMessage />
    </FormItem>
  )}
/>
\`\`\`

### Select

\`\`\`typescript
<FormField
  control={form.control}
  name="status"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Status</FormLabel>
      <Select onValueChange={field.onChange} defaultValue={field.value}>
        <FormControl>
          <SelectTrigger>
            <SelectValue placeholder="Select status" />
          </SelectTrigger>
        </FormControl>
        <SelectContent>
          <SelectItem value="pending">Pending</SelectItem>
          <SelectItem value="active">Active</SelectItem>
          <SelectItem value="completed">Completed</SelectItem>
        </SelectContent>
      </Select>
      <FormMessage />
    </FormItem>
  )}
/>
\`\`\`

### Checkbox

\`\`\`typescript
<FormField
  control={form.control}
  name="terms"
  render={({ field }) => (
    <FormItem className="flex items-start space-x-3 space-y-0">
      <FormControl>
        <Checkbox
          checked={field.value}
          onCheckedChange={field.onChange}
        />
      </FormControl>
      <div className="space-y-1 leading-none">
        <FormLabel>Accept terms</FormLabel>
        <FormDescription>
          You agree to our Terms of Service.
        </FormDescription>
      </div>
      <FormMessage />
    </FormItem>
  )}
/>
\`\`\`

### Date Picker

\`\`\`typescript
<FormField
  control={form.control}
  name="dueDate"
  render={({ field }) => (
    <FormItem>
      <FormLabel>Due Date</FormLabel>
      <Popover>
        <PopoverTrigger asChild>
          <FormControl>
            <Button variant="outline" className="w-full justify-start">
              <CalendarIcon className="mr-2 h-4 w-4" />
              {field.value ? format(field.value, 'PPP') : 'Pick a date'}
            </Button>
          </FormControl>
        </PopoverTrigger>
        <PopoverContent>
          <Calendar
            mode="single"
            selected={field.value}
            onSelect={field.onChange}
          />
        </PopoverContent>
      </Popover>
      <FormMessage />
    </FormItem>
  )}
/>
\`\`\`

---

## Validation Patterns

### Schema Examples

\`\`\`typescript
import { z } from 'zod'

const schema = z.object({
  // Required string
  name: z.string().min(1, 'Required'),
  
  // Email
  email: z.string().email('Invalid email'),
  
  // Optional
  nickname: z.string().optional(),
  
  // With transform
  amount: z.string().transform(Number).pipe(z.number().positive()),
  
  // Enum
  status: z.enum(['draft', 'published']),
  
  // Array
  tags: z.array(z.string()).min(1, 'At least one tag'),
  
  // Conditional
  role: z.enum(['user', 'admin']),
  adminCode: z.string().optional(),
}).refine(data => {
  if (data.role === 'admin' && !data.adminCode) {
    return false
  }
  return true
}, {
  message: 'Admin code required for admin role',
  path: ['adminCode'],
})
\`\`\`

---

## Form Submission

### With Server Action

\`\`\`typescript
const onSubmit = async (data: FormValues) => {
  try {
    await createEntity(data)
    toast.success('Created!')
    form.reset()
  } catch (error) {
    toast.error('Failed to create')
  }
}
\`\`\`

### With API Route

\`\`\`typescript
const onSubmit = async (data: FormValues) => {
  const response = await fetch('/api/entities', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  
  if (!response.ok) {
    const error = await response.json()
    throw new Error(error.message)
  }
  
  toast.success('Created!')
}
\`\`\`

---

## Edit Forms

### Loading Existing Data

\`\`\`typescript
interface EditFormProps {
  entity: Entity
}

export function EditEntityForm({ entity }: EditFormProps) {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      name: entity.name,
      email: entity.email,
      description: entity.description ?? '',
    },
  })

  const onSubmit = async (data: FormValues) => {
    await updateEntity(entity.id, data)
    toast.success('Updated!')
  }
  
  // ...
}
\`\`\`

---

## Checklist

When creating a form:

- [ ] Define Zod schema with validation messages
- [ ] Use react-hook-form with zodResolver
- [ ] Use FormField for each input
- [ ] Handle loading state on submit button
- [ ] Show success/error toasts
- [ ] Reset form on success (if appropriate)
- [ ] Test validation errors display
- [ ] Test submission flow
```

---

## Step 5: Update project.json

Add to `skills.generated[]`:

```json
{
  "name": "form-patterns",
  "generatedFrom": "form-skill-generator",
  "generatedAt": "2026-02-20"
}
```
