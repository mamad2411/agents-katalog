---
name: cr-code-style
description: Coding style guide for all application code. Use when writing, editing, refactoring, or reviewing any code, components, UI, backend handlers, API routes, database queries, or tests.
---

# Code Style

Use these defaults unless the user or project conventions say otherwise.

## Core Principles

- Prefer existing project patterns over introducing new ones.
- Prefer straightforward, readable code over cleverness.
- Keep feature code boring and easy to scan.
- Keep code easy to scan top-to-bottom.
- Optimize for local clarity first.
- Use descriptive, literal names for files, functions, variables, and components.
- Use explicit names and unsurprising APIs.
- Keep folder structure shallow and obvious.
- Keep code close to the feature unless it is clearly shared.

### Structure

- Put feature-specific code near the route or feature that owns it.
- Promote code to shared locations only when it is genuinely reusable.
- Prefer clear top-level buckets such as `components`, `helpers`, `server`, `lib`, or route-local files.
- Do not create extra files or layers unless separation improves comprehension.

### Abstraction Rules

- Avoid speculative abstractions.
- Do not introduce helpers, hooks, wrappers, or config layers just because code looks slightly repetitive.
- When duplication is real, refactor early if the resulting abstraction makes the code easier to skim.
- Prefer partial abstraction over forcing unrelated cases through one generic helper.
- If the abstraction makes the code harder to scan, keep the logic local even if that means some duplication.
- Extract only when one of these is true:
  - the logic is reused,
  - the concept is clearly distinct,
  - the main flow becomes easier to understand.
- Prefer a little duplication over indirection that hurts readability.
- Do not hide simple business logic behind generic utilities.

### Helper and Component Style

- Helpers should be small and single-purpose.
- Prefer inline logic over a tiny helper when the helper does not improve readability.
- Components should have clear responsibilities.
- Prefer sensible defaults and explicit props.
- Avoid giant catch-all utility files unless the functions are truly generic.
- Keep simple component logic local; extract only when complexity or reuse justifies it.
- Do not create custom hooks only as a cosmetic reorganization. Keep local component state in place unless the logic is truly reusable or the component has become large and logic-heavy.
- For large or complicated React logic, extracting a hook or using context is good when it meaningfully simplifies the component.

## Refactor Boundaries

### Default Scope

- Keep diffs scoped to the request unless broader cleanup is explicitly needed.
- Keep changes focused on the requested task.
- Touch nearby code only when it directly improves readability, correctness, or maintainability of the requested change.
- Prefer targeted edits over broad cleanup passes.

### What Is Usually OK

- Small cleanup in the same file while implementing the requested change.
- Tightening names or structure when it makes the modified code easier to understand.
- Removing obviously dead local code discovered in the touched area.
- Fixing small inconsistencies that are directly adjacent to the change.

### What To Avoid By Default

- Do not refactor unrelated files just because they could be improved.
- Do not introduce new abstractions during feature work unless they are clearly justified by the change.
- Do not perform sweeping renames, file moves, or architecture cleanup unless asked.
- Do not convert existing patterns to a new style across the codebase as part of a small task.
- Do not expand scope from implementation into design-system or infrastructure work unless the task actually calls for it.

### Abstraction Guardrails

- A little duplication is often better than introducing a premature shared helper.
- If an abstraction only helps the current change a little, keep the logic local.
- Extract only when reuse is real, the concept is clearly distinct, or the main code becomes meaningfully easier to follow.

### Existing Code Quality

- Respect local conventions unless they are actively blocking a clean implementation.
- Improve messy code incrementally, not ideologically.
- Preserve public APIs and established behavior unless a change is required.

### When To Escalate

Pause and ask before doing broader refactors such as:

- moving code across feature boundaries,
- redesigning component APIs,
- changing shared helpers used in many places,
- renaming public exports,
- replacing existing patterns project-wide.

## Component System Style

Use these rules when building shared components such as buttons, inputs, modals, tooltips, selects, and other repeated UI primitives. If the project does not use React or does not have a shared component layer, skip this section.

### Philosophy

- Prefer composable foundations over rigid UI kits.
- It is fine to start from headless or primitive libraries such as Radix, Base UI, shadcn-style building blocks, or similar tools.
- Do not expose raw primitive verbosity to product code if a wrapper can provide a better API.
- Shared primitives should optimize for teammate developer experience.

### What to Build

- Wrap high-frequency primitives behind ergonomic shared components.
- Wrap frequent primitive patterns behind ergonomic, product-ready components.
- Standardize common concerns inside the component:
  - structure,
  - accessibility glue,
  - common styling,
  - repeated state wiring,
  - common slots and adornments,
  - sensible defaults.
- Expose the common use case through a small, intuitive, somewhat opinionated prop API.
- Keep escape hatches for advanced cases without making the default usage verbose.

### Abstraction Boundary

- In app or feature code, avoid premature abstraction.
- In shared component primitives, abstraction is good when it removes repeated ceremony and improves consistency.
- Do not mirror a primitive library's low-level API unless that low-level API is actually what the team needs.
- Prefer product-grade wrappers over raw primitive composition in day-to-day feature code.

### API Design

- Design components around how teammates actually use them.
- Prefer clear prop names and obvious defaults.
- Support common cases directly instead of forcing every consumer to compose many subparts.
- Reduce boilerplate for labels, descriptions, errors, icons, prefixes, suffixes, headers, actions, and common layout patterns when those needs are frequent.
- Wrap primitives all the way when the component is a common app building block and the project benefits from a more opinionated DX.

### Styling and Customization

- Favor Tailwind-friendly or customization-friendly foundations.
- Avoid systems that become hard to style or override in modern workflows.
- Keep the component easy to customize without making the base API noisy.

## Tailwind Style

Use these defaults when writing or refactoring UI with Tailwind. If the project uses a different styling system (e.g., Mantine, styled-components, CSS Modules), follow that system instead.

### Principles

- Keep Tailwind classes inline when they describe component-local structure and positioning.
- Keep styling isolated to the component by default.
- Keep class lists lean.
- Default to simple, readable utility classes over style cleverness.
- Prefer practical, readable utility usage over class soup.
- Prefer canonical Tailwind utilities over arbitrary values.
- Prefer semantic tokens over repeated magic numbers.
- Keep typography styling simple unless the design system truly requires more.
- Do not override size, tracking, leading, color, and weight all at once without a strong reason.
- Do not customize every typography and spacing property by default.

### Layout and Spacing

- Prefer `flex` or `grid` for layout.
- Prefer `flex`/`grid` + `gap-*` over spacing hacks.
- Prefer `gap-*` for spacing between children.
- Avoid `space-x-*` and `space-y-*` by default.
- Use width, alignment, padding, and responsive utilities directly where the layout is defined.

### Styling Boundaries

- Keep structural styling in the JSX for the component that owns it.
- Do not extract style abstractions for simple one-off cases.
- Prefer inline conditional classes over variant systems such as `cva` unless the complexity is clearly justified.
- If reuse is real, prefer extracting a component over extracting detached class maps.
- Avoid building a style system on top of Tailwind unless the complexity is justified.
- If a design token or semantic utility should exist globally, prefer adding it once instead of repeating arbitrary values across components.

### Variants and Responsiveness

- Keep responsive, dark-mode, and print classes inline at the point of use.
- Make responsive behavior obvious in the component.
- Do not hide simple variant logic behind unnecessary helpers.

### Visual Design Defaults

- Add only the classes needed to express layout, hierarchy, and the intended UI.
- Do not add decorative polish by default unless the request or surrounding code calls for it.
- Favor clean, restrained styling over over-designed utility stacks.
- Default to plain, functional UI. Less is more.
- When typography components or sensible defaults already exist, rely on them instead of overriding font size, tracking, leading, color, and weight in every usage.
- If no typography component exists, prefer simple canonical classes like `text-4xl`, `font-semibold`, or no extra typography classes at all unless they are clearly needed.
- Avoid arbitrary values like `text-[16px]`, `tracking-[-0.02em]`, `leading-[1.05]`, custom rgba values, or one-off border colors unless there is a strong design-system reason.
- Prefer semantic tokens like `border-stroke`, `z-max`, or standard Tailwind scales over duplicated magic numbers.

## Backend Style: T3 + tRPC

Use these defaults when creating or refactoring routers, procedures, Zod schemas, and router-local backend utilities. If the project uses a different backend stack (e.g., Hono, Express, Fastify), follow its patterns instead.

### Philosophy

- Favor the simple, practical structure common in create-t3-app projects.
- Keep router boundaries aligned with domains, entities, or clear backend features.
- Treat tRPC routers as domain boundaries.
- Use routers to keep entity or feature separation clear.
- Keep backend code boring, explicit, and easy to navigate.
- Prefer small files with clear responsibilities over dumping everything into one router file.

### Router File Structure

For non-trivial routers, prefer this structure:

- `index.ts` — compose and export the router
- `queries.ts` — read procedures
- `mutations.ts` — write procedures
- `schemas.ts` — zod schemas and shared input/output validators
- `utils.ts` — router-specific backend helpers when needed

Keep these files colocated in a router directory.

### Responsibilities

#### `index.ts`

- Keep it tiny.
- Import `queries` and `mutations`.
- Export a router composed from those modules.
- Do not place business logic here.

#### `queries.ts`

- Put read-only procedures here.
- Keep query handlers direct and easy to scan.
- Validate inputs with schemas imported from `schemas.ts`.
- Throw explicit `TRPCError`s for expected failure cases.

#### `mutations.ts`

- Put write procedures here.
- Keep mutation handlers explicit about validation, authorization, persistence, and returned data.
- Use router-local utils when they remove meaningful complexity.
- Avoid hiding the main mutation flow behind too much indirection.

#### `schemas.ts`

- Keep zod schemas separate from server logic.
- Put input and shared validation schemas here.
- This file should be safe to import on the frontend when client-side validation is useful.
- Do not leak server-only logic into schemas.
- Prefer named schemas for common inputs such as IDs, filters, payloads, and enums.

#### `utils.ts`

- Use for router-specific helper logic only.
- Good candidates:
  - authorization helpers tied to the router domain,
  - entity-specific validation,
  - persistence helpers used by multiple procedures,
  - path or key builders tied to the router domain.
- Do not turn `utils.ts` into a generic dumping ground.
- If logic is used outside the router domain, move it to a more appropriate shared backend location.

### Procedure Style

- Prefer explicit `protectedProcedure`, `adminProcedure`, or other project-standard procedure wrappers.
- Validate inputs early and fail clearly.
- Keep procedure names literal, such as `getFile`, `listFiles`, `getUploadUrl`, `confirmFileUpload`, `deleteFileById`.
- Keep the happy path readable top-to-bottom.
- Destructure input near the top when it improves readability.
- Validate early.
- Throw clear `TRPCError`s for expected failures.
- Return plain, unsurprising shapes.

### Domain Separation

- Group procedures by domain, entity, or feature rather than by HTTP-style thinking.
- It is fine for a router to represent an entity-like boundary, but routers can also represent other clear backend domains.
- Keep related schemas, procedures, and helpers together so the domain is easy to understand.

### Abstraction Rules

- Avoid over-abstracting simple queries and mutations.
- Extract utils when logic is reused or meaningfully simplifies the procedure.
- Keep business flow visible in procedures unless the extracted helper clearly improves readability.
- Prefer router-local helpers over cross-backend abstractions when the logic is domain-specific.

## Examples

### Prefer direct feature code

```ts
export const InvoiceRow = ({ invoice }: { invoice: Invoice }) => {
  const isPaid = invoice.receipts.length > 0;

  return <span>{isPaid ? 'Paid' : 'Pending'}</span>;
};
```

### Avoid unnecessary helper extraction

```ts
const getInvoicePaymentStatus = (invoice: Invoice) =>
  invoice.receipts.length > 0 ? 'Paid' : 'Pending';

export const InvoiceRow = ({ invoice }: { invoice: Invoice }) => {
  return <span>{getInvoicePaymentStatus(invoice)}</span>;
};
```

### Prefer meaningful abstraction when duplication is real

```ts
const hasExpiredState = (status: string, deletedAt: Date | null) =>
  status === 'inactive' || deletedAt != null;

const isExpiredUser = hasExpiredState(user.status, user.deletedAt);
const isExpiredAdmin = hasExpiredState(admin.status, admin.deletedAt);
```

### Avoid generic abstraction that hurts skimming

```ts
const isExpired = (entity: { status: string; deletedAt: Date | null }) =>
  entity.status === 'inactive' || entity.deletedAt != null;
```

Use only if it really reads better in context.

### Prefer ergonomic wrapper APIs for common primitives

```tsx
<Modal
  open={open}
  setOpen={setOpen}
  title="Invite member"
  actionTrayItems={<SubmitButton />}
>
  <InviteForm />
</Modal>
```

### Avoid exposing primitive ceremony in feature code

```tsx
<Dialog.Root open={open} onOpenChange={setOpen}>
  <Dialog.Trigger asChild>
    <button>Open</button>
  </Dialog.Trigger>
  <Dialog.Portal>
    <Dialog.Overlay />
    <Dialog.Content>
      <Dialog.Title>Invite member</Dialog.Title>
      <InviteForm />
    </Dialog.Content>
  </Dialog.Portal>
</Dialog.Root>
```

### Prefer shared field components that absorb common wiring

```tsx
<InputField
  label="Email"
  description="Used for account notifications"
  error={errors.email}
  leftIcon={<MailIcon />}
  {...register('email')}
/>
```

### Avoid making every consumer rebuild the same field shell

```tsx
<Label htmlFor="email" />
<div className="relative">
  <MailIcon />
  <Input id="email" aria-invalid={!!errors.email} />
</div>
{errors.email && <FieldError>{errors.email}</FieldError>}
```

### Prefer `gap` for spacing

```tsx
<div className="flex flex-col gap-4">
  <Label />
  <Input />
  <Hint />
</div>
```

### Avoid `space-*` by default

```tsx
<div className="flex flex-col space-y-4">
  <Label />
  <Input />
  <Hint />
</div>
```

### Prefer small router composition in `index.ts`

```ts
import { createTRPCRouter } from '../../trpc';
import * as mutations from './mutations';
import * as queries from './queries';

export const filesRouter = createTRPCRouter({
  ...queries,
  ...mutations,
});
```

### Prefer schemas in a separate shared file

```ts
export const FileIdSchema = z.object({
  id: z.string(),
});

export const ListFilesSchema = z.object({
  userId: z.string().optional(),
  artistPageId: z.string().optional(),
  postId: z.string().optional(),
  purpose: FilePurposeSchema.optional(),
});
```

### Prefer direct procedures with visible flow

```ts
export const getFile = adminProcedure.input(FileIdSchema).query(async ({ ctx, input }) => {
  const file = await ctx.db.file.findUnique({
    where: { id: input.id },
  });

  if (!file) {
    throw new TRPCError({
      code: 'NOT_FOUND',
      message: 'File not found',
    });
  }

  return file;
});
```

### Prefer router-local utils for domain-specific logic

```ts
export const deleteFile = async ({ ctx, file }: { ctx: ProtectedTRPCContextType; file: File }) => {
  const authorizedToDelete =
    ctx.session.roles.includes('admin') || file.uploadedById === ctx.session.user_id;

  if (!authorizedToDelete) {
    throw new TRPCError({
      code: 'UNAUTHORIZED',
      message: '[FILES] You do not have permission to delete this file',
    });
  }

  await ctx.s3.deleteFile(file.path);
  return ctx.db.file.delete({ where: { id: file.id } });
};
```

### Usually OK: small adjacent cleanup

```ts
export const formatUsd = (amount: number) => {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
  }).format(amount);
};
```

If touching this file already, simplifying an obvious local implementation is fine.

### Usually avoid: unrelated abstraction during feature work

```ts
// Asked: add a status badge to invoices page
// Avoid: extracting a new cross-app status helpers module
// unless the task actually justifies it.
```

### Usually avoid: broad cleanup from a narrow request

```ts
// Asked: fix one modal action
// Avoid: renaming modal props across the whole app,
// moving files, and rewriting related hooks in the same task.
```

### Escalate first when scope expands

```ts
// This change now requires redesigning a shared component API.
// Pause and ask before continuing with the broader refactor.
```

## Output Checklist

Before finishing, check:

- Is the code easy to follow top-to-bottom?
- Are names literal and unsurprising?
- Did I avoid unnecessary abstractions while still refactoring meaningful duplication?
- Is feature code kept near its owner?
- Did I avoid creating extra files or layers without a strong reason?
- Did I stay focused on the requested task?
- Did I avoid broad cleanup unrelated to the change?
- Would the diff feel appropriately scoped to the request?
- Did I preserve behavior and public surfaces unless change was necessary?
- Did I improve developer experience compared with using primitives directly (for shared components)?
- Did I absorb repeated wiring into shared components where applicable?
- Did I use `gap` instead of `space-*` (when using Tailwind)?
- Are Tailwind classes mostly local, structural, and readable (when applicable)?
- Did I avoid arbitrary values when canonical utilities or semantic tokens would work (when using Tailwind)?
- Is the router split by responsibility when it is non-trivial (when using tRPC)?
- Are schemas separated from server-only logic (when using tRPC)?
- Are queries and mutations easy to find (when using tRPC)?
- Is domain-specific logic kept close to the router (when using tRPC)?
- Is the procedure flow explicit and easy to scan (when using tRPC)?
