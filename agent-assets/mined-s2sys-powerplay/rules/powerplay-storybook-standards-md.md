---
name: storybook-standards
description: Storybook component documentation — story structure, accessibility testing, Chromatic integration, versioning
globs: ["**/*.stories.tsx", "**/*.stories.jsx", "**/*.stories.ts", "**/*.stories.js", "**/storybook/**"]
alwaysApply: false
---

# Storybook Standards

Storybook is a component development environment. Use it to document, test, and showcase UI components in isolation.

---

## Story Structure

**ALWAYS**:
- One story file per component
- Export default with title and component
- Use decorators for layout/theming
- Provide ArgsTable (auto-generated prop documentation)
- Create variants for each state (default, hover, disabled, loading)
- Write descriptive titles and descriptions

**NEVER**:
- Skip stories for public components
- Leave stories without examples
- Forget accessibility annotations
- Hardcode data (use args)

### ✅ GOOD Story Structure

```typescript
// Button.stories.tsx
import { Meta, StoryObj } from '@storybook/react';
import { Button, ButtonProps } from './Button';

/**
 * Primary action button component.
 * Supports multiple variants, sizes, and states.
 */
const meta: Meta<typeof Button> = {
  title: 'Components/Button',
  component: Button,
  tags: ['autodocs'],
  
  // Global decorators
  decorators: [
    (Story) => (
      <div style={{ padding: '20px' }}>
        <Story />
      </div>
    ),
  ],

  // Prop documentation
  argTypes: {
    variant: {
      control: 'select',
      options: ['primary', 'secondary', 'danger', 'ghost'],
      description: 'Button color variant',
    },
    size: {
      control: 'select',
      options: ['sm', 'md', 'lg'],
      description: 'Button size preset',
    },
    disabled: {
      control: 'boolean',
      description: 'Disable button interactions',
    },
    isLoading: {
      control: 'boolean',
      description: 'Show loading spinner',
    },
    children: {
      control: 'text',
      description: 'Button label text',
    },
  },

  // Default args
  args: {
    variant: 'primary',
    size: 'md',
    disabled: false,
    isLoading: false,
    children: 'Click me',
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Primary button variant (blue background).
 */
export const Primary: Story = {
  args: {
    variant: 'primary',
    children: 'Primary Action',
  },
};

/**
 * Secondary button variant (gray background).
 */
export const Secondary: Story = {
  args: {
    variant: 'secondary',
    children: 'Secondary Action',
  },
};

/**
 * Danger button variant (red background).
 */
export const Danger: Story = {
  args: {
    variant: 'danger',
    children: 'Delete',
  },
};

/**
 * Disabled button state.
 */
export const Disabled: Story = {
  args: {
    disabled: true,
    children: 'Disabled',
  },
};

/**
 * Loading state with spinner.
 */
export const Loading: Story = {
  args: {
    isLoading: true,
    children: 'Loading...',
  },
};

/**
 * Large button with icon.
 */
export const LargeWithIcon: Story = {
  args: {
    size: 'lg',
    children: '🚀 Launch',
  },
};

/**
 * All button variants side-by-side.
 */
export const AllVariants: Story = {
  render: (args) => (
    <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
      <Button {...args} variant="primary">
        Primary
      </Button>
      <Button {...args} variant="secondary">
        Secondary
      </Button>
      <Button {...args} variant="danger">
        Danger
      </Button>
      <Button {...args} variant="ghost">
        Ghost
      </Button>
    </div>
  ),
};

/**
 * All sizes with primary variant.
 */
export const AllSizes: Story = {
  render: (args) => (
    <div style={{ display: 'flex', gap: '10px', alignItems: 'center' }}>
      <Button {...args} size="sm">
        Small
      </Button>
      <Button {...args} size="md">
        Medium
      </Button>
      <Button {...args} size="lg">
        Large
      </Button>
    </div>
  ),
};
```

---

## Accessibility Testing in Storybook

**ALWAYS**:
- Add accessibility (a11y) testing addon
- Run automated checks on every story
- Verify color contrast (WCAG AA)
- Check keyboard navigation
- Verify ARIA labels and roles
- Test with screen reader simulation

**NEVER**:
- Ignore accessibility violations
- Skip testing disabled/focus states
- Use inaccessible color combinations

### ✅ GOOD Accessibility Story

```typescript
// Input.stories.tsx with accessibility addon
import { Meta, StoryObj } from '@storybook/react';
import { Input, InputProps } from './Input';

const meta: Meta<typeof Input> = {
  title: 'Components/Input',
  component: Input,
  tags: ['autodocs'],
  
  parameters: {
    // a11y addon configuration
    a11y: {
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true,
          },
          {
            id: 'label-title-only',
            enabled: false, // Labels preferred over titles
          },
        ],
      },
    },
  },

  argTypes: {
    label: {
      control: 'text',
      description: 'Associated label text',
    },
    placeholder: {
      control: 'text',
      description: 'Placeholder text (not substitute for label)',
    },
    error: {
      control: 'text',
      description: 'Error message shown below input',
    },
    disabled: {
      control: 'boolean',
      description: 'Disabled state',
    },
  },

  args: {
    label: 'Email address',
    placeholder: 'your@email.com',
    error: '',
    disabled: false,
  },
};

export default meta;
type Story = StoryObj<typeof meta>;

/**
 * Standard input field with label.
 * WCAG: Label associated via htmlFor/id.
 */
export const Default: Story = {
  args: {
    label: 'Full name',
  },
};

/**
 * Input with error message.
 * WCAG: Error announced via aria-describedby.
 */
export const WithError: Story = {
  args: {
    label: 'Email',
    error: 'Invalid email format',
  },
  parameters: {
    a11y: {
      // Story-specific a11y config
      config: {
        rules: [
          {
            id: 'color-contrast',
            enabled: true,
          },
        ],
      },
    },
  },
};

/**
 * Disabled input field.
 * WCAG: Visual indication + aria-disabled.
 */
export const Disabled: Story = {
  args: {
    disabled: true,
    label: 'Contact (unavailable)',
  },
};

/**
 * Focus state visible (keyboard navigation).
 * WCAG: 2px outline on focus-visible.
 */
export const Focused: Story = {
  render: (args) => {
    const inputRef = React.useRef<HTMLInputElement>(null);
    
    React.useEffect(() => {
      inputRef.current?.focus();
    }, []);

    return <Input {...args} ref={inputRef} />;
  },
};
```

---

## Chromatic Integration

**ALWAYS**:
- Set up Chromatic for visual regression testing
- Take snapshots of every story variant
- Review visual changes before merging
- Set interaction testing for complex components
- Configure baselines for expected appearance

**NEVER**:
- Deploy without visual review
- Ignore Chromatic warnings
- Skip baseline approval

### ✅ GOOD Chromatic Setup

```typescript
// .storybook/main.ts
import type { StorybookConfig } from '@storybook/react-webpack5';

const config: StorybookConfig = {
  stories: ['../src/**/*.stories.{js,jsx,ts,tsx}'],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-a11y',
    '@storybook/addon-interactions',
    '@storybook/addon-coverage',
    // Chromatic addon
    'chromatic',
  ],
  framework: {
    name: '@storybook/react-webpack5',
    options: {},
  },
  docs: {
    autodocs: 'tag',
  },
};

export default config;

// .storybook/.chromatic (environment config)
# .env or Chromatic token
CHROMATIC_PROJECT_TOKEN=your_chromatic_token
CHROMATIC_BRANCH_TOKEN=your_branch_token

// package.json script
{
  "scripts": {
    "storybook": "storybook dev -p 6006",
    "build-storybook": "storybook build",
    "chromatic": "chromatic --project-token=$CHROMATIC_PROJECT_TOKEN"
  }
}
```

---

## Component Documentation

**ALWAYS**:
- Write DocBlock comments above stories
- Document component purpose
- List all props with descriptions
- Provide usage examples
- Link to design guidelines
- Show error states and edge cases

**NEVER**:
- Leave prop documentation blank
- Create stories without context
- Skip error state examples

### ✅ GOOD Documentation

```typescript
/**
 * # Card Component
 * 
 * A reusable container for grouping related content.
 * 
 * ## Usage
 * ```tsx
 * <Card>
 *   <Card.Header>
 *     <h2>Title</h2>
 *   </Card.Header>
 *   <Card.Body>
 *     Content here
 *   </Card.Body>
 *   <Card.Footer>
 *     <Button>Action</Button>
 *   </Card.Footer>
 * </Card>
 * ```
 * 
 * ## Variants
 * - **Elevated**: Subtle shadow, used for grouped content
 * - **Outlined**: Minimal styling, used in data lists
 * 
 * ## Accessibility
 * - Uses semantic HTML (`<article>` or `<section>`)
 * - Heading hierarchy preserved
 * - Color contrast WCAG AA
 * 
 * ## Related
 * - [Design System](https://figma.com/...)
 * - [Spacing Guide](https://docs.example.com/spacing)
 */
const meta: Meta<typeof Card> = {
  title: 'Components/Card',
  component: Card,
  tags: ['autodocs'],
  
  parameters: {
    docs: {
      description: {
        component: 'A flexible card component for grouping related content with optional header, body, and footer.',
      },
    },
  },
};
```

---

## Interaction Testing

**ALWAYS**:
- Use play() function to simulate user interactions
- Test clicks, form submissions, keyboard navigation
- Verify visual changes after interactions
- Test with userEvent (more realistic than fireEvent)
- Check accessibility after interactions

**NEVER**:
- Skip interaction testing for interactive components
- Use fireEvent (unrealistic user behavior)
- Forget to check focus states

### ✅ GOOD Interaction Story

```typescript
import { expect, within } from '@storybook/test';
import { userEvent } from '@storybook/test';

export const Modal: Story = {
  args: {
    isOpen: true,
    title: 'Confirm Action',
    children: 'Are you sure?',
  },
  
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const confirmButton = canvas.getByRole('button', { name: /confirm/i });
    
    // Test: button is visible
    await expect(confirmButton).toBeVisible();
    
    // Test: click button
    await userEvent.click(confirmButton);
    
    // Test: focus visible on cancel after confirm
    const cancelButton = canvas.getByRole('button', { name: /cancel/i });
    await expect(cancelButton).toHaveFocus();
  },
};
```

---

## Story File Organization

**ALWAYS**:
- Group stories by feature (Buttons, Forms, Layouts)
- Use consistent file naming: `ComponentName.stories.tsx`
- Co-locate stories with components
- Create index story for category overview

**NEVER**:
- Scatter stories randomly
- Use unclear naming (story_1, test_1)
- Mix multiple components in one story file

### ✅ GOOD File Structure

```
src/
├── components/
│   ├── Button/
│   │   ├── Button.tsx
│   │   ├── Button.stories.tsx
│   │   ├── Button.test.tsx
│   │   └── Button.module.css
│   ├── Form/
│   │   ├── Input/
│   │   │   ├── Input.tsx
│   │   │   └── Input.stories.tsx
│   │   ├── Checkbox/
│   │   │   ├── Checkbox.tsx
│   │   │   └── Checkbox.stories.tsx
│   │   └── Form.stories.tsx (overview)
│   └── Card/
│       ├── Card.tsx
│       └── Card.stories.tsx
└── .storybook/
    ├── main.ts
    └── preview.ts
```

---

## Storybook Best Practices

**ALWAYS**:
- Enable autodocs (automatic prop documentation)
- Use tags for component filtering (@storybook/blocks)
- Set up visual regression testing (Chromatic)
- Organize by feature/page
- Keep stories focused and isolated
- Test all states: default, hover, focus, active, disabled, loading, error

**NEVER**:
- Create stories that depend on other stories
- Use global state in stories
- Hardcode data (use args)
- Forget to test keyboard navigation

---

## Storybook Checklist

- [ ] Story file created for each component
- [ ] Default export with title and component
- [ ] ArgTypes documented for all props
- [ ] Default args provided
- [ ] All variants shown (primary, secondary, etc.)
- [ ] All states shown (default, hover, disabled, loading, error)
- [ ] Accessibility (a11y) addon configured
- [ ] No accessibility violations
- [ ] Chromatic integration set up
- [ ] Visual regression testing enabled
- [ ] Interaction tests (play function) added
- [ ] DocBlock comments written
- [ ] Component purpose documented
- [ ] Usage examples provided
- [ ] Design system links included

---

## Summary

Good Storybook setup:
1. **Documented** — Clear purpose and usage examples
2. **Comprehensive** — All variants and states shown
3. **Accessible** — a11y testing enabled, no violations
4. **Tested** — Interaction tests + visual regression
5. **Organized** — Logical grouping and naming
6. **Automated** — Chromatic visual review on every PR

Storybook is your component documentation system.
