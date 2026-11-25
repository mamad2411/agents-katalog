---
description: 
globs: *.ts,*tsx
alwaysApply: false
---
# Development Rules for HomeHarmony

## 🎯 Core Development Principles

### 1. Code Quality Standards
- **TypeScript First**: All new code must be written in TypeScript with proper type definitions
- **Functional Components**: Use React functional components with hooks, avoid class components
- **ESLint Compliance**: All code must pass ESLint checks without warnings
- **Consistent Formatting**: Follow existing code style and formatting patterns

### 2. Component Architecture
- **Single Responsibility**: Each component should have one clear purpose
- **Composition over Inheritance**: Prefer component composition patterns
- **Props Interface**: Always define TypeScript interfaces for component props
- **Default Props**: Use default parameters instead of defaultProps

```typescript
// ✅ Good
interface ComponentProps {
  title: string;
  isVisible?: boolean;
}

const Component = ({ title, isVisible = true }: ComponentProps) => {
  // component logic
};

// ❌ Avoid
const Component = (props: any) => {
  // component logic
};
```

## 🏗️ File Structure Rules

### 1. Import Organization
Organize imports in this order:
1. React and React-related imports
2. Third-party libraries
3. Internal components (using `@/` alias)
4. Relative imports
5. Type-only imports last

```typescript
// ✅ Good
import React, { useState, useEffect } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import type { Member } from '../types';
```

### 2. Component File Structure
```typescript
// 1. Imports
import React from 'react';
import { Button } from '@/components/ui/button';

// 2. Type definitions
interface ComponentProps {
  // props definition
}

// 3. Component implementation
export const Component: React.FC<ComponentProps> = ({ prop1, prop2 }) => {
  // 4. State declarations
  const [state, setState] = useState();
  
  // 5. Effect hooks
  useEffect(() => {
    // effect logic
  }, []);
  
  // 6. Event handlers
  const handleClick = () => {
    // handler logic
  };
  
  // 7. Render logic
  return (
    <div>
      {/* JSX */}
    </div>
  );
};
```

## 🎨 UI/UX Development Rules

### 1. shadcn/ui Component Usage
- **Prefer shadcn/ui**: Always use existing shadcn/ui components before creating custom ones
- **Consistent Styling**: Use the established design system and color scheme
- **Accessibility**: Ensure all interactive elements are keyboard accessible
- **Responsive Design**: All components must work on mobile, tablet, and desktop

### 2. Tailwind CSS Guidelines
- **Utility Classes**: Use Tailwind utility classes instead of custom CSS when possible
- **Responsive Modifiers**: Always consider mobile-first responsive design
- **Consistent Spacing**: Use the established spacing scale (p-4, m-6, etc.)
- **Color Usage**: Stick to the defined color palette

```tsx
// ✅ Good - Responsive, semantic, consistent
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 p-6">
  <Card className="bg-white shadow-sm hover:shadow-md transition-shadow">
    {content}
  </Card>
</div>

// ❌ Avoid - Not responsive, custom styles
<div style={{ display: 'flex', padding: '20px' }}>
  <div className="custom-card">
    {content}
  </div>
</div>
```

### 3. Visual Consistency
- **Icon Usage**: Use Lucide React icons consistently throughout the app
- **Color Coding**: Maintain the established color scheme for different states
  - Blue: Primary actions and branding
  - Green: Success states and completed items
  - Orange: Warnings and low stock alerts
  - Red: Errors and overdue items
- **Typography**: Use consistent font weights and sizes

## 📊 State Management Rules

### 1. Local State Management
- **useState**: Use for component-level state
- **useEffect**: Use for side effects and lifecycle events
- **State Lifting**: Lift state up to the nearest common ancestor when sharing between components
- **Immutable Updates**: Always create new objects/arrays instead of mutating existing ones

```typescript
// ✅ Good - Immutable update
setTasks(prev => prev.map(task => 
  task.id === taskId ? { ...task, completed: true } : task
));

// ❌ Avoid - Mutation
tasks[index].completed = true;
setTasks(tasks);
```

### 2. Data Persistence
- **localStorage Keys**: Use the established naming convention (`homeharmony-*`)
- **JSON Serialization**: Ensure all stored data is properly serializable
- **Error Handling**: Wrap localStorage operations in try-catch blocks
- **Data Migration**: Consider backward compatibility when changing data structures

### 3. Form State
- **React Hook Form**: Use for all form implementations
- **Zod Validation**: Define schemas for form validation
- **Error Handling**: Display user-friendly error messages
- **Loading States**: Show loading indicators during form submission

## 🔧 Performance Rules

### 1. Optimization Techniques
- **Avoid Unnecessary Re-renders**: Use React.memo() for expensive components
- **Callback Optimization**: Use useCallback() for event handlers passed to child components
- **Effect Dependencies**: Always include all dependencies in useEffect dependency arrays
- **Lazy Loading**: Consider lazy loading for routes and heavy components

### 2. Bundle Size Management
- **Tree Shaking**: Import only what you need from libraries
- **Dynamic Imports**: Use dynamic imports for optional functionality
- **Image Optimization**: Optimize images and use appropriate formats

```typescript
// ✅ Good - Tree shaking friendly
import { Button } from '@/components/ui/button';
import { format } from 'date-fns';

// ❌ Avoid - Imports entire library
import * as dateFns from 'date-fns';
import { components } from '@/components/ui';
```

## 🧪 Testing Guidelines

### 1. Component Testing
- **Unit Tests**: Write tests for complex business logic
- **Integration Tests**: Test component interactions
- **Accessibility Tests**: Ensure components meet accessibility standards
- **Responsive Tests**: Test layouts on different screen sizes

### 2. Test Structure
- **Descriptive Names**: Use clear, descriptive test names
- **Arrange-Act-Assert**: Follow the AAA pattern for test structure
- **Mock External Dependencies**: Mock API calls and external services
- **Test User Interactions**: Focus on testing user workflows

## 🔒 Security Rules

### 1. Data Handling
- **Input Validation**: Validate all user inputs on the client side
- **XSS Prevention**: Sanitize any dynamic content
- **Local Storage**: Don't store sensitive information in localStorage
- **Type Safety**: Use TypeScript to prevent runtime errors

### 2. Component Security
- **Props Validation**: Always validate component props
- **Safe Rendering**: Be careful with dangerouslySetInnerHTML
- **Event Handling**: Validate event data before processing

## 🚀 Deployment & Build Rules

### 1. Build Configuration
- **Environment Variables**: Use Vite environment variables for configuration
- **Build Optimization**: Ensure production builds are optimized
- **Asset Optimization**: Optimize images, fonts, and other assets
- **Bundle Analysis**: Regularly analyze bundle size

### 2. Code Organization
- **Feature Folders**: Organize related components together
- **Shared Utilities**: Keep utility functions in the lib folder
- **Type Definitions**: Maintain type definitions in appropriate files
- **Documentation**: Keep README and documentation up to date

## 📝 Code Review Checklist

Before submitting code, ensure:

- [ ] TypeScript types are properly defined
- [ ] Components are responsive and accessible
- [ ] ESLint passes without warnings
- [ ] Code follows established patterns
- [ ] Performance considerations are addressed
- [ ] Error handling is implemented
- [ ] Documentation is updated if needed
- [ ] Tests are written for new functionality

## 🛠️ Development Commands

```bash
# Development
bun run dev          # Start development server
bun run build        # Build for production
bun run build:dev    # Build for development
bun run preview      # Preview production build
bun run lint         # Run ESLint

# Package Management
bun install          # Install dependencies
bun add <package>    # Add new dependency
bun add -d <package> # Add dev dependency
```

## 📚 Learning Resources

### Documentation
- [React Documentation](https://react.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Vite Documentation](https://vitejs.dev)

### Best Practices
- Follow React best practices and patterns
- Maintain consistent code style across the project
- Write self-documenting code with clear variable names
- Use meaningful commit messages following conventional commits

These rules ensure consistency, maintainability, and scalability of the HomeHarmony application while providing a great developer experience.

