# Frontend Rules

> **Scope:** `apps/web`  
> **Last updated:** 2025-06-25

## Tech Stack

| Concern | Technology |
| ------- | ---------- |
| Framework | Next.js (App Router) |
| Language | TypeScript |
| Styling | Tailwind CSS |
| UI Components | shadcn/ui |
| Forms | React Hook Form |
| Validation | Zod |
| State Management | Zustand |
| Icons | Lucide React |

---

## Architecture

Use feature-based architecture.

**Structure:**

```
src/
├── app/
├── components/
├── features/
├── hooks/
├── services/
├── store/
├── types/
├── lib/
└── providers/
```

Do not place all code inside `app/`.

---

## Page Rules

Each page should:

- Be responsive
- Follow accessibility standards
- Handle loading states
- Handle empty states
- Handle error states

---

## Component Rules

Components must:

- Be reusable
- Be typed
- Have a single responsibility

Avoid large components.

**Maximum recommended size:** 300 lines

Split large components into smaller ones.

---

## Naming Conventions

### Components

PascalCase

**Examples:**

```
JobCard.tsx
ProfileForm.tsx
ResumeUploader.tsx
```

### Hooks

```
useAuth.ts
useJobs.ts
useProfile.ts
```

### Services

```
auth.service.ts
job.service.ts
profile.service.ts
```

---

## State Management Rules

Use Zustand.

Do not use Context API for global state unless necessary.

**Examples:**

```
auth.store.ts
profile.store.ts
job.store.ts
```

---

## API Rules

Frontend must never directly access database logic.

All communication goes through API services.

**Examples:**

```
services/auth.service.ts
services/job.service.ts
services/profile.service.ts
```

---

## Form Rules

**Use:**

- React Hook Form
- Zod Validation

Every form must have:

- Validation
- Error messages
- Loading state
- Success state

---

## UI Design Principles

1. Clean
2. Professional
3. Minimal
4. Fast
5. Mobile friendly

**Avoid:**

- Unnecessary animations
- Overly complex UI
- Excessive colors

---

## Dashboard Layout

Every authenticated page must use `DashboardLayout`.

**Includes:**

- Sidebar
- Header
- Main content area

---

## Job Pages

Jobs must display:

- Job title
- Company
- Location
- Match score
- Quality score
- Apply button
- Save button

---

## Profile Pages

Profile should include:

- Personal information
- Skills
- Education
- Experience
- Projects

---

## Resume Pages

Resume section should support:

- Upload resume
- View resume
- Download resume
- Delete resume

---

## Loading States

Every async page must include:

- Skeleton loading
- Error state
- Empty state

Never leave blank screens.

---

## Type Safety

Do **not** use `any`.

Always create proper types.

Use shared types whenever possible.

---

## Mock Data

During frontend-first development:

- Use mock data
- Do not create fake backend logic
- Keep mock data inside feature modules

**Example:**

```
features/jobs/mock/jobs.ts
```

---

## Performance Rules

**Use:**

- Server Components when possible
- Client Components only when necessary

Avoid unnecessary re-renders.

---

## Definition of Done

Frontend feature is complete only when:

- Responsive
- Typed
- Validated
- Loading state added
- Error state added
- Empty state added
- Reusable components extracted
