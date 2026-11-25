---
name: shadcn-testing
description: Use when writing or reviewing tests for shadcn/ui components — covering Radix portal handling, keyboard interaction, async Dialog/Sheet assertions, Combobox/Command filtering, and Storybook story contracts.
---

# shadcn/ui Testing

## Specialization

Provide expert-level guidance for testing shadcn/ui components with Vitest + Testing Library, Playwright, and Storybook — covering Radix portal rendering, async state assertions, keyboard interaction sequences, `forceMount` patterns for animated components, and screen reader query strategies.

This skill covers testing authoring. Component design and CVA variants are handled by `shadcn-component-design`. Form composition and validation UX are handled by `shadcn-forms`. Quality gate pre-merge review is handled by `shadcn-quality-gate`.

## Trigger Conditions

- Writing unit or integration tests for shadcn/ui components (Button, Dialog, Sheet, Select, Combobox, Command, Popover, Tooltip, etc.).
- Radix portals (`Dialog`, `AlertDialog`, `Sheet`, `Tooltip`, `Popover`) are breaking standard `getByRole` or `getByText` queries.
- Tests need to simulate keyboard navigation across Radix-managed focus traps and roving tabindex patterns.
- `AnimatePresence` or `tailwindcss-animate` exit animations are preventing assertions on unmounted elements.
- Designing Storybook stories that serve as living component contracts with accessibility metadata.
- Writing Playwright E2E tests for multi-component flows involving dialogs, command palettes, or multi-select comboboxes.
- Auditing existing component tests for `fireEvent` misuse, missing `waitFor`, or missing ARIA query strategies.

## When Not to Use

- Quality gate evidence review before promotion (use `shadcn-quality-gate`).
- CI pipeline integration for test runs (use `shadcn-ci-integration`).
- Component authoring guidance without a test focus (use `shadcn-component-design`).
- xUnit or backend testing patterns (use `xunit-test-design`).

## Inputs

- Component name and its Radix primitive base.
- Test framework in use: Vitest + Testing Library, Jest + Testing Library, Playwright, or Storybook.
- Animation library in use: `tailwindcss-animate`, Framer Motion, or none.
- RSC/SSR context: Next.js App Router, Vite + React, or SvelteKit.
- Specific interaction to verify: open/close, keyboard nav, async filter, form submission, etc.
- Evaluation date in ISO format (`YYYY-MM-DD`).

## Required Outputs

| Output | Description |
|---|---|
| Test file(s) | Vitest/Jest + Testing Library tests with named `describe` blocks and explicit `it` intent strings |
| Portal query strategy | Confirmed approach for finding Radix portal content (`within(document.body)`, `screen.getByRole` with `hidden: false`, etc.) |
| Keyboard interaction map | Key sequence table for each interactive component under test |
| `waitFor` / `findBy` contract | All async assertions using `findBy*` or `waitFor(() => expect(...))` — no bare `getBy*` after triggers |
| `forceMount` pattern (if animated) | `AnimatePresence` or `data-state` handling so exit content can be asserted |
| Storybook stories (if applicable) | `argTypes`, `play` function with `@storybook/test` interactions, and `a11y` addon metadata |
| Playwright test (if applicable) | Page object or inline flow test for E2E scenario with explicit assertion on ARIA role and visible state |
| Coverage gaps record | Interactions that are deferred and explicit rationale |

## Depth Modes

| Level | Intent | Exit Rule |
|---|---|---|
| L1 Orientation | One component, one interaction (open/close or click) | Test passes; portal content found; no flakiness |
| L2 Practical Delivery | Full unit suite for one component family (Dialog + trigger + content) | All interactions covered; keyboard nav tested; async assertions stable |
| L3 Advanced Patterns | Multi-component flow, animated exit assertions, `forceMount` | Exit animations do not block assertions; Combobox async filter tested; form submit + dialog close asserted together |
| L4 Expert Standardization | Reusable test utilities and Storybook `play` function library | Shared `renderWithProviders`, `openDialog`, `selectComboboxOption` helpers; Storybook stories double as accessibility contracts |

## Core Testing Patterns

### 1. Setup

```bash
npm install -D vitest @testing-library/react @testing-library/user-event jsdom
npm install -D @storybook/test @storybook/addon-a11y          # Storybook optional
npm install -D @playwright/test                                # Playwright optional
```

`vitest.config.ts`:
```ts
import { defineConfig } from "vitest/config"
import react from "@vitejs/plugin-react"

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    setupFiles: ["./src/test/setup.ts"],
    globals: true,
  },
})
```

`src/test/setup.ts`:
```ts
import "@testing-library/jest-dom"
```

### 2. Radix Portal Query Pattern

Radix renders `Dialog`, `AlertDialog`, `Sheet`, `Tooltip`, `Popover`, and `DropdownMenu` content into a portal appended to `document.body`, outside the component tree. Standard queries scoped to a render container will not find portal content.

**Correct approach:**

```tsx
import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { Dialog, DialogTrigger, DialogContent, DialogTitle } from "@/components/ui/dialog"

describe("Dialog", () => {
  it("opens on trigger click and closes on Escape", async () => {
    const user = userEvent.setup()

    render(
      <Dialog>
        <DialogTrigger>Open</DialogTrigger>
        <DialogContent>
          <DialogTitle>Confirm action</DialogTitle>
          <p>Are you sure?</p>
        </DialogContent>
      </Dialog>
    )

    // Dialog content is NOT in the render container — query from screen (document.body)
    await user.click(screen.getByRole("button", { name: "Open" }))
    expect(screen.getByRole("dialog")).toBeInTheDocument()
    expect(screen.getByText("Confirm action")).toBeVisible()

    await user.keyboard("{Escape}")
    await waitFor(() => {
      expect(screen.queryByRole("dialog")).not.toBeInTheDocument()
    })
  })
})
```

**Rules:**
- Always use `screen.*` (not `within(container).*`) for Radix portal content.
- Always use `@testing-library/user-event` (`userEvent.setup()`) over `fireEvent` — Radix relies on pointer events.
- Use `waitFor` for close assertions — Radix unmounts asynchronously after exit animation.
- `getByRole("dialog")` works because Radix sets `role="dialog"` on the content element.

### 3. Keyboard Interaction Maps

| Component | Key Sequence | Expected Behavior |
|---|---|---|
| Dialog | `Tab` (trigger focused) → `Enter` | Dialog opens; focus moves to first focusable element inside |
| Dialog | `Escape` (dialog open) | Dialog closes; focus returns to trigger |
| Select | `Space`/`Enter` on trigger | Listbox opens |
| Select | `Arrow Down/Up` | Cycles options |
| Select | `Enter` on option | Selects and closes |
| DropdownMenu | `Enter`/`Space` on trigger | Menu opens |
| DropdownMenu | `Arrow Down/Up` | Moves focus between items |
| DropdownMenu | `Escape` | Closes; focus returns to trigger |
| Combobox (Command) | Type characters | Filters list asynchronously |
| Combobox | `Arrow Down/Up` | Navigates filtered results |
| Combobox | `Enter` | Selects item |
| Tabs | `Arrow Right/Left` | Moves between tabs (automatic activation) |
| RadioGroup | `Arrow Down/Up` | Moves between radio buttons |

```tsx
it("navigates Select with keyboard", async () => {
  const user = userEvent.setup()
  render(<SelectDemo />)

  const trigger = screen.getByRole("combobox")
  await user.click(trigger) // open
  await user.keyboard("{ArrowDown}")
  await user.keyboard("{Enter}")

  expect(trigger).toHaveTextContent("Option 2") // or whatever option 2 is
})
```

### 4. Animated Component: `forceMount` + `waitFor`

When using `tailwindcss-animate` or Framer Motion, Radix exit animations delay unmount. Without `forceMount`, testing close state requires `waitFor`.

**Option A — `waitFor` (no `forceMount`, tests animation path):**
```tsx
await user.keyboard("{Escape}")
await waitFor(() => expect(screen.queryByRole("dialog")).not.toBeInTheDocument(), {
  timeout: 500,
})
```

**Option B — `forceMount` (disables animation in test, tests content presence):**
```tsx
// Only use in tests; do not ship forceMount to production unless intentional
render(
  <Dialog open={false}>
    <DialogContent forceMount>
      <DialogTitle>Hidden but mounted</DialogTitle>
    </DialogContent>
  </Dialog>
)
// Content is in DOM but hidden; assert on data-state
expect(screen.getByRole("dialog", { hidden: true })).toHaveAttribute("data-state", "closed")
```

**Decision rule:** Use `waitFor` for standard tests. Use `forceMount` only when testing hidden state presence (e.g., asserting correct ARIA attributes on a closed dialog).

### 5. Combobox / Command Async Filter

```tsx
import { render, screen, waitFor } from "@testing-library/react"
import userEvent from "@testing-library/user-event"

it("filters options by input and selects result", async () => {
  const user = userEvent.setup()
  render(<ComboboxDemo />)

  await user.click(screen.getByRole("combobox"))
  // Command input appears in portal
  const input = screen.getByPlaceholderText("Search framework...")
  await user.type(input, "next")

  // Wait for filtered results — Command uses internal async filter
  await waitFor(() => {
    expect(screen.getByRole("option", { name: /next\.js/i })).toBeInTheDocument()
  })

  await user.click(screen.getByRole("option", { name: /next\.js/i }))
  expect(screen.getByRole("combobox")).toHaveTextContent(/next\.js/i)
})
```

### 6. Form Integration Test

```tsx
it("shows field errors on submit with empty required fields", async () => {
  const user = userEvent.setup()
  render(<ProfileForm />)

  await user.click(screen.getByRole("button", { name: /submit/i }))

  // react-hook-form sets aria-invalid and aria-describedby
  await waitFor(() => {
    expect(screen.getByRole("textbox", { name: /username/i })).toHaveAttribute(
      "aria-invalid",
      "true"
    )
    expect(screen.getByText(/username must be at least 2 characters/i)).toBeInTheDocument()
  })
})
```

### 7. Storybook `play` Functions

```tsx
// Button.stories.tsx
import type { Meta, StoryObj } from "@storybook/react"
import { expect, userEvent, within } from "@storybook/test"
import { Button } from "@/components/ui/button"

const meta: Meta<typeof Button> = {
  title: "ui/Button",
  component: Button,
  tags: ["autodocs"],
}
export default meta

type Story = StoryObj<typeof Button>

export const ClickInteraction: Story = {
  args: { children: "Click me" },
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement)
    const button = canvas.getByRole("button", { name: "Click me" })
    await userEvent.click(button)
    await expect(button).toBeVisible()
  },
}
```

**Storybook a11y addon metadata:**
```tsx
export const Default: Story = {
  parameters: {
    a11y: {
      config: {
        rules: [{ id: "color-contrast", enabled: true }],
      },
    },
  },
}
```

## Pragmatic Stop Rule

Stop and deliver when:
1. All interaction paths (open, close, keyboard, submit, error) have passing tests.
2. All async assertions use `findBy*` or `waitFor` — no synchronous queries after async triggers.
3. Portal content is queried from `screen`, not a scoped container.
4. Animated exit assertions either use `waitFor` (production path) or explicit `forceMount` (state testing).
5. Coverage gaps are documented with rationale.
