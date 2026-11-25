# TypeScript Rules

## Type Definitions

- Always use strict TypeScript mode
- Prefer interfaces over types for object shapes
- Use type guards for runtime type checking
- Always define return types for functions
- Use proper generic constraints

## Type Patterns

### Interface vs Type

```typescript
// ✅ Prefer interfaces for object shapes
interface UserProps {
  id: string;
  name: string;
  email: string;
}

// ✅ Use types for unions, primitives, computed types
type Status = 'loading' | 'success' | 'error';
type UserKeys = keyof UserProps;
```

### Generic Constraints

```typescript
// ✅ Use proper generic constraints
interface ApiResponse<T extends Record<string, any>> {
  data: T;
  status: number;
  message: string;
}
```

### Type Guards

```typescript
// ✅ Implement type guards for runtime validation
function isUser(obj: any): obj is User {
  return obj && typeof obj.id === 'string' && typeof obj.name === 'string';
}
```

### Function Return Types

```typescript
// ✅ Always define return types
function calculateTotal(items: Item[]): number {
  return items.reduce((sum, item) => sum + item.price, 0);
}

// ✅ Use void for functions that don't return
function logMessage(message: string): void {
  console.log(message);
}
```

## Project-Specific Types

### LangType

```typescript
// Use the established LangType
import type { LangType } from '@/lib/types/LangType';

function handleLanguageChange(lang: LangType): void {
  // implementation
}
```

### TechIconKey

```typescript
// Use the established TechIconKey type
import type { TechIconKey } from '@/lib/types/TechIconKey';

function renderTechIcon(iconKey: TechIconKey): JSX.Element {
  // implementation
}
```

## Error Handling Types

```typescript
// Use custom error types from lib/errors
import { CustomError } from '@/lib/errors/CustomError';
import { PayloadValidationError } from '@/lib/errors/PayloadValidationError';
import { StorageError } from '@/lib/errors/StorageError';
```

## Database Types

```typescript
// Use Prisma generated types
import type { Hero, HeroTranslation, Language } from '@prisma/client';

// Create proper type combinations
type HeroWithTranslations = Hero & {
  translations: HeroTranslation[];
};
```

## Component Props Types

```typescript
// Follow the established pattern
interface ComponentProps {
  // Required props first
  id: string;
  title: string;

  // Optional props with default values
  isActive?: boolean;
  className?: string;

  // Event handlers
  onClick?: () => void;
  onChange?: (value: string) => void;
}
```

## API Types

```typescript
// Use proper API response types
interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
  errors?: string[];
}

// Use proper request types
interface CreateHeroRequest {
  heroVersion: string;
  heroPhoto: string;
  translations: {
    languageId: string;
    heroName: string;
    heroDescription: string;
  }[];
}
```

## Validation Types

```typescript
// Use Yup schema types
import * as yup from 'yup';

const heroSchema = yup.object({
  heroVersion: yup.string().required(),
  heroPhoto: yup.string().required(),
});

type HeroFormData = yup.InferType<typeof heroSchema>;
```

## Utility Types

```typescript
// Use built-in utility types effectively
type PartialHero = Partial<Hero>;
type RequiredHero = Required<Hero>;
type HeroKeys = keyof Hero;
type HeroValues = Hero[HeroKeys];

// Create custom utility types
type NonNullable<T> = T extends null | undefined ? never : T;
type DeepPartial<T> = {
  [P in keyof T]?: T[P] extends object ? DeepPartial<T[P]> : T[P];
};
```

## Const Assertions

```typescript
// ✅ Use const assertions for immutable data
const LANGUAGES = ['en', 'ua'] as const;
type Language = (typeof LANGUAGES)[number];

const CONFIG = {
  apiUrl: 'https://api.example.com',
  timeout: 5000,
} as const;
```

## Module Augmentation

```typescript
// Extend existing types when needed
declare module 'next-intl' {
  interface IntlMessages {
    // Add custom message types
  }
}
```

## Best Practices

- Use `type` for unions, primitives, and computed types
- Use `interface` for object shapes and extensibility
- Always use proper generic constraints
- Implement type guards for runtime validation
- Use const assertions for immutable data
- Prefer type inference where possible
- Use proper error types from the project's error system
- Follow the established naming conventions
- Use proper return types for all functions
- Implement proper prop types for components

