# Booking Tool - Cursor Rules

## Project Overview

This is a Next.js 16 booking tool for a venue with form-based reservations, calendar integration, and email notifications.

## Tech Stack

- **Framework**: Next.js 16 (App Router) with React 19
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS 4 with shadcn/ui components (New York style)
- **State Management**: React Query (@tanstack/react-query) for server state
- **Date Handling**: date-fns
- **Database**: Supabase (PostgreSQL)
- **Integrations**: Google Calendar API, Gmail API
- **Icons**: lucide-react

## Code Style & Conventions

### TypeScript

- Use strict TypeScript with proper types for all functions and components
- Prefer `interface` over `type` for object shapes
- Use `type` for unions, intersections, and utility types
- Always define return types for functions
- Use `async/await` over promises chains
- Handle errors explicitly with try-catch blocks

### React & Next.js

- Use Server Components by default, only use Client Components when necessary ('use client')
- Use React Query for all server state management
- Prefer Server Actions for mutations (form submissions)
- Use Next.js App Router conventions (route.ts, layout.tsx, page.tsx)
- Use proper Next.js metadata exports for SEO
- Implement proper loading and error states

### Component Structure

- Use shadcn/ui components from `@/components/ui`
- Follow shadcn/ui patterns and conventions
- Create reusable components in `@/components`
- Use the `cn()` utility from `@/lib/utils` for className merging
- Keep components focused and single-purpose
- Extract complex logic into custom hooks in `@/hooks`

### Styling

- Use Tailwind CSS utility classes
- Follow mobile-first responsive design
- Use CSS variables for theming (already configured)
- Maintain consistent spacing using Tailwind's spacing scale
- Use semantic color names (primary, secondary, destructive, etc.)

### File Organization

```
app/
  ├── (routes)/
  ├── api/          # API routes
  ├── components/   # Shared components
  ├── lib/          # Utilities and helpers
  ├── hooks/        # Custom React hooks
  └── types/        # TypeScript type definitions
```

## Database & API Patterns

### Supabase

- Use Supabase client-side SDK for queries
- Create Server Actions for mutations (better security)
- Use Row Level Security (RLS) policies
- Type database tables with TypeScript interfaces
- Store Supabase client creation in `@/lib/supabase`

### Google Calendar Integration

- Use Google Calendar API v3
- Store OAuth tokens securely (Supabase Vault or environment variables)
- Implement token refresh logic
- Sync bookings bidirectionally (create events, read existing events)
- Handle API rate limits gracefully

### Email Service

- Use Gmail API or a service like Resend/SendGrid
- Create email templates for confirmation emails
- Use Server Actions for sending emails
- Include booking details in confirmation emails

## Form Handling

- Use React Hook Form for form state management
- Implement proper validation with Zod schemas using `@hookform/resolvers/zod`
- Use `useForm` hook with `zodResolver` for form validation
- Show validation errors inline using form state
- Disable submit button during submission
- Show loading states during async operations
- Reset form after successful submission using `reset()` method
- Example pattern:

  ```typescript
  import { useForm } from "react-hook-form";
  import { zodResolver } from "@hookform/resolvers/zod";
  import { z } from "zod";

  const schema = z.object({
    /* ... */
  });
  const form = useForm({ resolver: zodResolver(schema) });
  ```

## Date & Time Handling

- Use date-fns for all date operations
- Store dates in UTC in database
- Display dates in user's local timezone
- Use date-fns format functions for display
- Handle timezone conversions explicitly

## Error Handling

- Use React Query's error handling for API calls
- Display user-friendly error messages
- Log errors server-side for debugging
- Implement retry logic for transient failures
- Use error boundaries for React errors

## Performance

- Use React Query caching effectively
- Implement optimistic updates for better UX
- Use Next.js Image component for images
- Lazy load heavy components
- Minimize client-side JavaScript bundle

## Security

- Never expose API keys or secrets in client code
- Use environment variables for sensitive data
- Validate all user inputs server-side
- Implement CSRF protection for forms
- Use Supabase RLS for database security

## Testing Considerations

- Write type-safe code (TypeScript is your first test)
- Test critical user flows manually
- Use React Query DevTools in development

## Common Patterns

### API Route Pattern

```typescript
// app/api/example/route.ts
import { NextRequest, NextResponse } from "next/server";

export async function GET(request: NextRequest) {
  try {
    // Implementation
    return NextResponse.json({ data });
  } catch (error) {
    return NextResponse.json({ error: "Message" }, { status: 500 });
  }
}
```

### Server Action Pattern

```typescript
"use server";

import { revalidatePath } from "next/cache";

export async function createBooking(formData: FormData) {
  // Validation
  // Database operation
  // Integration calls
  revalidatePath("/");
  return { success: true };
}
```

### React Query Hook Pattern

```typescript
// hooks/use-bookings.ts
import { useQuery } from "@tanstack/react-query";

export function useBookings() {
  return useQuery({
    queryKey: ["bookings"],
    queryFn: async () => {
      // Fetch logic
    },
  });
}
```

## UI/UX Guidelines

- Left side: Booking form (fixed width, scrollable if needed)
- Right side: Tabs for Calendar, Options/Pricing, General Info
- Use responsive design: stack vertically on mobile
- Show loading skeletons for async data
- Provide clear feedback for all user actions
- Use consistent spacing and typography

## Integration Priorities

1. Supabase setup and schema design
2. Basic booking form and validation
3. Calendar view with reserved dates
4. Google Calendar sync
5. Email confirmation system

## Package Management

- **Always use Yarn** for all package-related actions (install, add, remove, etc.)
- Use `yarn add` instead of `npm install`
- Use `yarn add -D` for dev dependencies
- Use `yarn` instead of `npm install` for installing dependencies from package.json

## Notes

- This is a Dutch project (Beheerraad/oud-zwembad) - consider i18n if needed
- Venue booking tool - prioritize reliability and user experience
- Multiple reservation types (kitchen, rooms, etc.) - make it flexible
