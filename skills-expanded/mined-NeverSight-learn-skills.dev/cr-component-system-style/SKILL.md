---
name: cr-component-system-style
description: Shared component system preferences. Use when building reusable UI primitives, wrapping headless libraries, or designing teammate-friendly component APIs.
---

# Component System Style

Use these rules when building shared components such as buttons, inputs, modals, tooltips, selects, and other repeated UI primitives.

## Philosophy

- Prefer composable foundations over rigid UI kits.
- It is fine to start from headless or primitive libraries such as Radix, Base UI, shadcn-style building blocks, or similar tools.
- Do not expose raw primitive verbosity to product code if a wrapper can provide a better API.
- Shared primitives should optimize for teammate developer experience.

## What to Build

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

## Abstraction Boundary

- In app or feature code, avoid premature abstraction.
- In shared component primitives, abstraction is good when it removes repeated ceremony and improves consistency.
- Do not mirror a primitive library's low-level API unless that low-level API is actually what the team needs.
- Prefer product-grade wrappers over raw primitive composition in day-to-day feature code.

## API Design

- Design components around how teammates actually use them.
- Prefer clear prop names and obvious defaults.
- Support common cases directly instead of forcing every consumer to compose many subparts.
- Reduce boilerplate for labels, descriptions, errors, icons, prefixes, suffixes, headers, actions, and common layout patterns when those needs are frequent.
- Wrap primitives all the way when the component is a common app building block and the project benefits from a more opinionated DX.

## Styling and Customization

- Favor Tailwind-friendly or customization-friendly foundations.
- Avoid systems that become hard to style or override in modern workflows.
- Keep the component easy to customize without making the base API noisy.

## Examples

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

## Output Checklist

Before finishing, check:

- Did I improve developer experience compared with using the primitive directly?
- Is the default API compact and easy to consume?
- Did I absorb repeated wiring into the shared component?
- Are advanced escape hatches still possible?
- Would a teammate prefer using this wrapper over the raw primitive?
