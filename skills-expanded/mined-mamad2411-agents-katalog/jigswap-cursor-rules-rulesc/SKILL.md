---
alwaysApply: true
---
# Component Organization Rules

This document defines the standard component organization rules that all agents must follow when working with this codebase.

## Core Principles

### 1. Forms Should Be Their Own Components
- Forms must be organized as separate, reusable components
- Each form should have its own directory under `apps/web/src/components/forms/`
- Forms should be compound components that can be used in both dialogs and pages

### 2. Forms Should Be Compound Components
- Main form component should be in `/<form-name>/index.tsx`
- Break down large forms into smaller, focused sub-components
- Sub-components should be in `/<form-name>/<sub-component-name>.tsx`
- Each sub-component should have a single responsibility

### 3. Component Naming Convention
- Main components: `/<component-name>/index.tsx`
- Sub-components: `/<component-name>/<sub-component-name>.tsx`
- Use kebab-case for file names
- Use PascalCase for component names

### 4. Details Components Organization
- Details components should be stored in `/<workspace>/src/components/details/<component-name>/index.tsx`
- Follow the same sub-component pattern as forms
- Details components should be compound components for flexibility

## Directory Structure Standards

### Forms Structure
```
apps/web/src/components/forms/
├── index.ts (exports)
├── <form-name>/
│   ├── index.tsx (main component)
│   ├── <form-name>-schema.ts (validation schema)
│   ├── <form-name>-<section>.tsx (sub-components)
│   ├── <form-name>-actions.tsx (form actions)
│   ├── <form-name>-modal.tsx (modal wrapper)
│   └── README.md (documentation)
```

### Details Structure
```
apps/web/src/components/details/
├── index.ts (exports)
├── <detail-name>/
│   ├── index.tsx (main component)
│   ├── <detail-name>-header.tsx
│   ├── <detail-name>-info.tsx
│   ├── <detail-name>-actions.tsx
│   └── README.md (documentation)
```

## Component Design Patterns

### Form Components
- Use `showActions?: boolean` prop to control action visibility
- Support both page and dialog usage patterns
- Include proper TypeScript interfaces for all props
- Use react-hook-form with Zod validation
- Provide `onSuccess`, `onCancel` callbacks

### Detail Components
- Use `showActions?: boolean` prop to control action visibility
- Support both page and dialog usage patterns
- Include proper TypeScript interfaces for all props
- Handle loading states gracefully
- Provide action callbacks (onEdit, onDelete, etc.)

## Implementation Guidelines

### When Creating New Forms
1. Create directory: `apps/web/src/components/forms/<form-name>/`
2. Create main component: `index.tsx`
3. Create schema: `<form-name>-schema.ts`
4. Break down into logical sub-components
5. Create modal wrapper if needed
6. Update exports in `apps/web/src/components/forms/index.ts`
7. Add README.md with usage examples
8. **Ensure all text content is internationalized** using `useTranslations`

### When Creating New Details
1. Create directory: `apps/web/src/components/details/<detail-name>/`
2. Create main component: `index.tsx`
3. Break down into logical sub-components (header, info, actions)
4. Update exports in `apps/web/src/components/details/index.ts`
5. Add README.md with usage examples
6. **Ensure all text content is internationalized** using `useTranslations`

### Sub-Component Guidelines
- Each sub-component should have a single responsibility
- Use descriptive names that indicate the component's purpose
- Include proper TypeScript interfaces
- Make components flexible with optional props
- Document complex logic with comments

## Code Quality Standards

### TypeScript
- Use proper type definitions for all props
- Avoid `any` types - use specific interfaces
- Import types from generated Convex files when applicable
- Use generic types for reusable components

### React Patterns
- Use compound component pattern for flexibility
- Implement proper prop drilling or context as needed
- Use React hooks appropriately
- Handle loading and error states

### Accessibility
- Include proper ARIA labels
- Use semantic HTML elements
- Ensure keyboard navigation works
- Provide proper focus management

### Internationalization (i18n)
- **ALL text content must be internationalized** - no hardcoded English text
- Use `useTranslations` hook from `next-intl` for all text content
- Translation keys should be descriptive and organized by feature/component
- Follow the existing translation structure in `apps/web/locales/en.json` and `apps/web/locales/nl.json`
- Translation files are managed through Crowdin - do not modify them directly unless necessary
- Use proper translation namespacing (e.g., `t("puzzles.title")`, `t("common.loading")`)
- Support both English and Dutch languages
- Ensure all user-facing text, including:
  - Component labels and placeholders
  - Error messages and notifications
  - Button text and actions
  - Form field labels and descriptions
  - Modal titles and content
  - Navigation items
  - Status messages and loading states

## Migration Guidelines

### When Refactoring Existing Components
1. Identify the component's responsibilities
2. Break down into logical sub-components
3. Create the new directory structure
4. Move code to appropriate sub-components
5. Update imports throughout the codebase
6. Remove old files
7. Update documentation

### When Adding New Features
1. Follow the established patterns
2. Create reusable components
3. Update exports appropriately
4. Add proper documentation
5. Include usage examples
6. **Internationalize all new text content** - add translation keys to Crowdin-managed files if needed

## Examples

### Form Component Usage
```tsx
// In a page
<FormComponent
  id="form-id"
  onSuccess={() => router.push("/success")}
  onCancel={() => router.back()}
/>

// In a dialog
<FormComponentModal
  open={open}
  onOpenChange={setOpen}
  onSuccess={() => setOpen(false)}
/>

// With internationalization
import { useTranslations } from "next-intl";

function MyComponent() {
  const t = useTranslations("puzzles");
  
  return (
    <div>
      <h1>{t("title")}</h1>
      <p>{t("description")}</p>
      <button>{t("addPuzzle")}</button>
    </div>
  );
}
```

### Detail Component Usage
```tsx
// In a page
<DetailComponent
  itemId={id}
  showActions={true}
  onEdit={(id) => router.push(`/edit/${id}`)}
/>

// In a dialog
<DetailComponent
  itemId={id}
  showActions={false}
/>
```

## Enforcement

All agents working on this codebase must:
1. Follow these component organization rules
2. Use the established patterns for new components
3. Refactor existing components to match these standards
4. Maintain consistency across the codebase
5. Document any deviations with clear reasoning
6. **Internationalize ALL text content** - no hardcoded English text allowed
7. Use proper translation namespacing and follow existing translation structure
8. Consider both English and Dutch translations when adding new content

## File Naming Conventions

- Components: PascalCase (e.g., `PuzzleForm`)
- Files: kebab-case (e.g., `puzzle-form.tsx`)
- Directories: kebab-case (e.g., `puzzle-form/`)
- Interfaces: PascalCase with descriptive names (e.g., `PuzzleFormProps`)
- Types: PascalCase with descriptive names (e.g., `PuzzleFormData`)

## Translation Key Conventions

- Use descriptive, hierarchical keys (e.g., `puzzles.addPuzzle`, `common.loading`)
- Group related translations under common namespaces
- Use camelCase for translation keys
- Follow existing patterns in `apps/web/locales/en.json` and `apps/web/locales/nl.json`
- Translation files are managed through Crowdin - coordinate with translation team

This ensures consistency and maintainability across the entire codebase. # Component Organization Rules

This document defines the standard component organization rules that all agents must follow when working with this codebase.

## Core Principles

### 1. Forms Should Be Their Own Components
- Forms must be organized as separate, reusable components
- Each form should have its own directory under `apps/web/src/components/forms/`
- Forms should be compound components that can be used in both dialogs and pages

### 2. Forms Should Be Compound Components
- Main form component should be in `/<form-name>/index.tsx`
- Break down large forms into smaller, focused sub-components
- Sub-components should be in `/<form-name>/<sub-component-name>.tsx`
- Each sub-component should have a single responsibility

### 3. Component Naming Convention
- Main components: `/<component-name>/index.tsx`
- Sub-components: `/<component-name>/<sub-component-name>.tsx`
- Use kebab-case for file names
- Use PascalCase for component names

### 4. Details Components Organization
- Details components should be stored in `/<workspace>/src/components/details/<component-name>/index.tsx`
- Follow the same sub-component pattern as forms
- Details components should be compound components for flexibility

## Directory Structure Standards

### Forms Structure
```
apps/web/src/components/forms/
├── index.ts (exports)
├── <form-name>/
│   ├── index.tsx (main component)
│   ├── <form-name>-schema.ts (validation schema)
│   ├── <form-name>-<section>.tsx (sub-components)
│   ├── <form-name>-actions.tsx (form actions)
│   ├── <form-name>-modal.tsx (modal wrapper)
│   └── README.md (documentation)
```

### Details Structure
```
apps/web/src/components/details/
├── index.ts (exports)
├── <detail-name>/
│   ├── index.tsx (main component)
│   ├── <detail-name>-header.tsx
│   ├── <detail-name>-info.tsx
│   ├── <detail-name>-actions.tsx
│   └── README.md (documentation)
```

## Component Design Patterns

### Form Components
- Use `showActions?: boolean` prop to control action visibility
- Support both page and dialog usage patterns
- Include proper TypeScript interfaces for all props
- Use react-hook-form with Zod validation
- Provide `onSuccess`, `onCancel` callbacks

### Detail Components
- Use `showActions?: boolean` prop to control action visibility
- Support both page and dialog usage patterns
- Include proper TypeScript interfaces for all props
- Handle loading states gracefully
- Provide action callbacks (onEdit, onDelete, etc.)

## Implementation Guidelines

### When Creating New Forms
1. Create directory: `apps/web/src/components/forms/<form-name>/`
2. Create main component: `index.tsx`
3. Create schema: `<form-name>-schema.ts`
4. Break down into logical sub-components
5. Create modal wrapper if needed
6. Update exports in `apps/web/src/components/forms/index.ts`
7. Add README.md with usage examples
8. **Ensure all text content is internationalized** using `useTranslations`

### When Creating New Details
1. Create directory: `apps/web/src/components/details/<detail-name>/`
2. Create main component: `index.tsx`
3. Break down into logical sub-components (header, info, actions)
4. Update exports in `apps/web/src/components/details/index.ts`
5. Add README.md with usage examples
6. **Ensure all text content is internationalized** using `useTranslations`

### Sub-Component Guidelines
- Each sub-component should have a single responsibility
- Use descriptive names that indicate the component's purpose
- Include proper TypeScript interfaces
- Make components flexible with optional props
- Document complex logic with comments

## Code Quality Standards

### TypeScript
- Use proper type definitions for all props
- Avoid `any` types - use specific interfaces
- Import types from generated Convex files when applicable
- Use generic types for reusable components

### React Patterns
- Use compound component pattern for flexibility
- Implement proper prop drilling or context as needed
- Use React hooks appropriately
- Handle loading and error states

### Accessibility
- Include proper ARIA labels
- Use semantic HTML elements
- Ensure keyboard navigation works
- Provide proper focus management

### Internationalization (i18n)
- **ALL text content must be internationalized** - no hardcoded English text
- Use `useTranslations` hook from `next-intl` for all text content
- Translation keys should be descriptive and organized by feature/component
- The source strings are defined in `apps/web/locales/source.json` and should be containing the source strings
- Follow the existing translation structure in `apps/web/locales/en.json` and `apps/web/locales/nl.json`
- Translation files are managed through Crowdin - do not modify them directly unless necessary
- Use proper translation namespacing (e.g., `t("puzzles.title")`, `t("common.loading")`)
- Support both English and Dutch languages
- Ensure all user-facing text, including:
  - Component labels and placeholders
  - Error messages and notifications
  - Button text and actions
  - Form field labels and descriptions
  - Modal titles and content
  - Navigation items
  - Status messages and loading states

## Migration Guidelines

### When Refactoring Existing Components
1. Identify the component's responsibilities
2. Break down into logical sub-components
3. Create the new directory structure
4. Move code to appropriate sub-components
5. Update imports throughout the codebase
6. Remove old files
7. Update documentation

### When Adding New Features
1. Follow the established patterns
2. Create reusable components
3. Update exports appropriately
4. Add proper documentation
5. Include usage examples
6. **Internationalize all new text content** - add translation keys to Crowdin-managed files if needed

## Examples

### Form Component Usage
```tsx
// In a page
<FormComponent
  id="form-id"
  onSuccess={() => router.push("/success")}
  onCancel={() => router.back()}
/>

// In a dialog
<FormComponentModal
  open={open}
  onOpenChange={setOpen}
  onSuccess={() => setOpen(false)}
/>

// With internationalization
import { useTranslations } from "next-intl";

function MyComponent() {
  const t = useTranslations("puzzles");
  
  return (
    <div>
      <h1>{t("title")}</h1>
      <p>{t("description")}</p>
      <button>{t("addPuzzle")}</button>
    </div>
  );
}
```

### Detail Component Usage
```tsx
// In a page
<DetailComponent
  itemId={id}
  showActions={true}
  onEdit={(id) => router.push(`/edit/${id}`)}
/>

// In a dialog
<DetailComponent
  itemId={id}
  showActions={false}
/>
```

## Enforcement

All agents working on this codebase must:
1. Follow these component organization rules
2. Use the established patterns for new components
3. Refactor existing components to match these standards
4. Maintain consistency across the codebase
5. Document any deviations with clear reasoning
6. **Internationalize ALL text content** - no hardcoded English text allowed
7. Use proper translation namespacing and follow existing translation structure
8. Consider both English and Dutch translations when adding new content

## File Naming Conventions

- Components: PascalCase (e.g., `PuzzleForm`)
- Files: kebab-case (e.g., `puzzle-form.tsx`)
- Directories: kebab-case (e.g., `puzzle-form/`)
- Interfaces: PascalCase with descriptive names (e.g., `PuzzleFormProps`)
- Types: PascalCase with descriptive names (e.g., `PuzzleFormData`)

## Translation Key Conventions

- Use descriptive, hierarchical keys (e.g., `puzzles.addPuzzle`, `common.loading`)
- Group related translations under common namespaces
- Use camelCase for translation keys
- Follow existing patterns in `apps/web/locales/en.json` and `apps/web/locales/nl.json`
- Translation files are managed through Crowdin - coordinate with translation team

This ensures consistency and maintainability across the entire codebase. 