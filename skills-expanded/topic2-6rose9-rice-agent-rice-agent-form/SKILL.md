---
name: rice-agent-form
description: All forms use react-hook-form + zod with useForm and zodResolver; never use plain form elements or inline validation
---

# Rice Agent Form Conventions

All forms in this project use **react-hook-form** + **zod** for validation.

## Pattern

```tsx
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"

const formSchema = z.object({ ... })
type FormValues = z.infer<typeof formSchema>

function MyForm() {
  const form = useForm<FormValues>({
    resolver: zodResolver(formSchema),
    defaultValues: { ... },
  })

  const onSubmit = (data: FormValues) => { ... }

  return (
    <form onSubmit={form.handleSubmit(onSubmit)}>
      ...
    </form>
  )
}
```

## Components

Use `@/components/ui/form` (shadcn Form) for field wrapping:
- `<FormField>` — wraps each field with `control`, `name`, `render`
- `<FormItem>`, `<FormLabel>`, `<FormControl>`, `<FormMessage>` — layout

## shadcn Setup

```bash
npx shadcn-ui@latest add form input textarea
```

## Validation Rules

- Schemas defined at top of each form file (or in `@/lib/schemas/` if shared)
- Error messages in Myanmar where user-facing
- Phone fields: `/^(09\d{7,9}|\+?959\d{7,8})$/`
