---
description: Run Next.js Architecture and App Router Conventions Check
globs: ['src/app/**/*.tsx', 'src/app/**/*.ts', 'app/**/*.tsx', 'app/**/*.ts']
---

# Next.js: App Router Architecture & Conventions

<audit_rules>

- You MUST verify Server/Client component boundaries. Default to Server Components. `use client` MUST only be used when necessary (e.g., hooks, browser APIs, event handlers) and pushed as far down the component tree as possible.
- You MUST NEVER import a Server Component directly into a Client Component. Pass them as `children` or props instead.
- You MUST enforce App Router file conventions. Ensure correct usage of route groups `(folder)`, parallel routes `@folder`, and intercepting routes `(.)`.
- You MUST verify all route folder names use `kebab-case` and do NOT contain spaces or underscores.
- You MUST ensure `error.tsx` and `global-error.tsx` include the `'use client'` directive.
- You MUST ensure Data Fetching in Server Components uses standard `fetch` with appropriate caching strategies (`force-cache` or `no-store`).
  </audit_rules>

<example_good>

```tsx
// src/app/components/interactive-button.tsx
'use client'
import { useState } from 'react'

export function InteractiveButton({ children }: { children: React.ReactNode }) {
  const [count, setCount] = useState(0)
  return (
    <button onClick={() => setCount((c) => c + 1)}>
      {children} - {count}
    </button>
  )
}

// src/app/page.tsx
// Server component passing children to client component
import { InteractiveButton } from './components/interactive-button'
import { ServerData } from './components/server-data'

export default function Page() {
  return (
    <InteractiveButton>
      <ServerData />
    </InteractiveButton>
  )
}
```

</example_good>

<example_bad>

```tsx
// src/app/components/bad-client.tsx
'use client'
// BAD: Importing server component directly into client component
import { ServerData } from './server-data'

export function BadClient() {
  return <ServerData /> // This will fail or bloat the client bundle
}
```

</example_bad>
