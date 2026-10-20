---
description: Run Input Validation and Sanitization Check
globs:
  [
    '**/api/**/*.ts',
    '**/actions/**/*.ts',
    '**/lib/validation/**/*.ts',
    '**/components/forms/**/*.tsx',
  ]
---

# Security: Input Validation & Sanitization

<audit_rules>

- You MUST validate ALL user inputs using a schema validation library like Zod BEFORE processing or storing data.
- You MUST sanitize string inputs to prevent XSS: escape HTML characters in user-generated content and strip dangerous tags from HTML inputs.
- You MUST validate and sanitize file uploads: check file types using magic numbers (not extensions), scan for malware, and limit file sizes.
- You MUST prevent prototype pollution by validating object keys and rejecting `__proto__`, `constructor`, or `prototype` properties.
- You MUST enforce length limits on string inputs and numeric ranges on number inputs to prevent DoS attacks.
- You MUST verify that validation errors are user-friendly and do NOT leak internal implementation details or stack traces.
  </audit_rules>

**How to check**: Ensure all user-facing inputs pass through a schema (e.g. Zod); search for unsanitized HTML or raw query construction; confirm file uploads use type and size checks.

<example_good>

```typescript
import { z } from 'zod'
import DOMPurify from 'dompurify'

const CreatePostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10).max(10000),
  tags: z.array(z.string().max(20)).max(5),
})

export async function createPost(formData: FormData) {
  try {
    const data = {
      title: formData.get('title'),
      content: formData.get('content'),
      tags: formData.getAll('tags'),
    }

    // Validate with Zod
    const validated = CreatePostSchema.parse(data)

    // Sanitize HTML content
    const sanitizedContent = DOMPurify.sanitize(validated.content)

    // Store sanitized data
    const post = await db.post.create({
      data: {
        ...validated,
        content: sanitizedContent,
      },
    })

    return { success: true, post }
  } catch (error) {
    if (error instanceof z.ZodError) {
      return { success: false, errors: error.flatten() }
    }
    throw error
  }
}
```

</example_good>

<example_bad>

```typescript
// BAD: No validation, direct use of user input
export async function createPost(formData: FormData) {
  const title = formData.get('title') as string
  const content = formData.get('content') as string

  // BAD: Directly storing user input without sanitization
  const post = await db.post.create({
    data: { title, content },
  })

  return { success: true, post }
}
```

</example_bad>

**Related rules**: auth-standards, api-security, security-headers, upload-security.
