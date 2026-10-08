---
alwaysApply: true
---
# Pond0x Issues Dashboard - Project Instructions

## Project Overview

This is a **Next.js 15** application that creates a beautiful GitHub issues dashboard for the Pond0x project. It features a glassmorphic design, real-time issue fetching, advanced filtering, and an interactive tutorial system for new GitHub users.

### Tech Stack
- **Framework**: Next.js 15 with App Router
- **React**: v19.1.0 
- **TypeScript**: v5 with strict mode
- **Styling**: Tailwind CSS with custom design system
- **State Management**: TanStack Query for server state, React hooks for local state
- **Icons**: Lucide React
- **Data Fetching**: GitHub REST API v3

## Project Status & Development Philosophy

⚠️ **IMPORTANT**: This is an **ongoing, actively developed project** with continuous refinement and improvement cycles.

### Continuous Development Approach
- **Iterative Enhancement**: Features and components are continuously refined based on user feedback and evolving requirements
- **Code Quality Evolution**: Regular refactoring and optimization passes to improve maintainability and performance
- **Design System Refinement**: UI/UX components are regularly updated to enhance user experience
- **Feature Expansion**: New functionality is added incrementally while maintaining existing feature stability
- **Best Practices Updates**: Development patterns and guidelines evolve as the project matures

### Expectations for Contributors
- **Incremental Improvements**: Always look for opportunities to enhance existing code during any modifications
- **Future-Proofing**: Write code with extensibility in mind, anticipating future feature additions
- **Documentation Updates**: Keep documentation current with any changes made to the codebase
- **Backward Compatibility**: Maintain compatibility when possible, but don't hesitate to evolve APIs when necessary
- **Quality Gates**: Each change should meet or exceed current quality standards

### Development Lifecycle
1. **Feature Implementation**: Initial development following current best practices
2. **Feedback Integration**: Incorporating user feedback and usage patterns
3. **Performance Optimization**: Regular performance audits and improvements
4. **Code Refinement**: Ongoing refactoring for better maintainability
5. **Feature Enhancement**: Expanding capabilities based on evolving needs

This ongoing development philosophy ensures the project remains modern, maintainable, and continues to provide value to its users.

---

## Architecture & File Organization

### Directory Structure
```
src/
├── app/                    # Next.js App Router
│   ├── layout.tsx         # Root layout with providers
│   ├── page.tsx           # Homepage
│   └── globals.css        # Global styles & design system
├── components/            # Reusable UI components
│   ├── ui/               # Base UI components
│   └── tutorial/         # Tutorial-specific components
├── hooks/                # Custom React hooks
├── lib/                  # Utilities and external services
├── types/                # TypeScript type definitions
```

### Key Files
- `src/lib/github.ts` - GitHub API service class
- `src/hooks/useIssues.ts` - Main data fetching hook
- `src/types/github.ts` - TypeScript interfaces
- `src/lib/utils.ts` - Utility functions
- `tailwind.config.js` - Custom design tokens

---

## Design System & Styling

### Color Palette
```css
/* Primary (Green) */
primary-50: #ecfdf5
primary-500: #10b981
primary-600: #059669

/* Secondary (Purple) */
secondary-500: #8b5cf6
secondary-600: #7c3aed

/* Accent Colors */
accent-yellow: #f59e0b
accent-pink: #ec4899
accent-cyan: #06b6d4
accent-orange: #f97316
```

### Key Design Components

#### Glass Cards
```css
.glass-card {
  @apply bg-glass border border-white/20 backdrop-blur-glass rounded-2xl shadow-2xl;
}
```

#### Background
- Uses `bg-gradient-pond` for main background
- Overlay with `bg-black/30` for depth
- All content in relative positioned containers

#### Typography
- **Primary Font**: Inter (Google Fonts)
- **Mono Font**: JetBrains Mono
- Use `gradient-text` class for hero text

---

## Component Patterns

### Component Structure
```tsx
'use client'; // Only for client components

import { ComponentProps } from '@/types/component';
import { cn } from '@/lib/utils';

interface ComponentNameProps {
  // Props with descriptive types
  variant?: 'primary' | 'secondary';
  children: React.ReactNode;
}

export function ComponentName({ variant = 'primary', children }: ComponentNameProps) {
  return (
    <div className={cn(
      'base-classes',
      variant === 'primary' && 'primary-classes',
      variant === 'secondary' && 'secondary-classes'
    )}>
      {children}
    </div>
  );
}
```

### Custom Hooks Pattern
```tsx
export function useFeatureName() {
  const [state, setState] = useState(initialState);
  
  // TanStack Query for server state
  const { data, isLoading, error } = useQuery({
    queryKey: ['feature', dependency],
    queryFn: () => apiCall(),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });

  // Computed values with useMemo
  const computedValue = useMemo(() => {
    return heavyComputation(data);
  }, [data]);

  return {
    // Return object with descriptive names
    data: computedValue,
    isLoading,
    error,
    actions: { setState }
  };
}
```

---

## Data Management

### GitHub API Integration
- **Service Class**: `GitHubService` in `src/lib/github.ts`
- **Authentication**: Uses `NEXT_PUBLIC_GITHUB_TOKEN` env var
- **Error Handling**: Throws descriptive errors for API failures
- **Type Safety**: All responses typed with GitHub interfaces

### Query Configuration
```tsx
useQuery({
  queryKey: ['issues', filters.state, filters.sort],
  queryFn: () => githubService.fetchIssues(params),
  staleTime: 5 * 60 * 1000, // 5 minutes
  retry: 2,
})
```

### State Management Strategy
- **Server State**: TanStack Query
- **Local UI State**: React hooks (`useState`, `useReducer`)
- **Global State**: Context providers (ErrorBoundary, QueryProvider)
- **URL State**: Next.js searchParams for filters

---

## Development Guidelines

### TypeScript Standards
```tsx
// Use strict interfaces
interface GitHubIssue {
  id: number;
  title: string;
  state: 'open' | 'closed'; // Literal types
  user: {
    login: string;
    avatar_url: string;
  };
}

// Generic types for reusable components
interface FilterProps<T> {
  items: T[];
  onFilter: (items: T[]) => void;
}
```

### Code Quality
- **ESLint**: Next.js recommended + TypeScript
- **Formatting**: Prettier with ignore patterns
- **Type Checking**: `npm run type-check` before commits
- **Naming**: Use descriptive, intention-revealing names

### Performance Best Practices
- Use `useMemo` for expensive computations
- Implement proper loading states
- Optimize images with Next.js `Image` component
- Use Tailwind's purge for smaller CSS bundles

---

## Component Guidelines

### UI Components (`src/components/ui/`)
- Single responsibility
- Highly reusable
- Accept `className` prop for extensibility
- Use `cn()` utility for conditional classes

### Feature Components (`src/components/`)
- Business logic components
- Use custom hooks for data fetching
- Handle loading and error states
- Follow naming convention: PascalCase

### Example Component Structure
```tsx
export function IssueCard({ issue, compact = false }: IssueCardProps) {
  return (
    <article className="glass-card p-6 hover:bg-white/10 transition-all duration-300">
      {/* Header section */}
      <div className="flex items-start gap-4">
        <StatusIcon status={issue.state} />
        
        <div className="flex-1 min-w-0">
          {/* Title with truncation */}
          <h3 className="text-lg font-semibold text-white mb-2">
            <a href={issue.html_url} target="_blank" rel="noopener noreferrer">
              {truncateText(issue.title, 80)}
            </a>
          </h3>
          
          {/* Metadata */}
          <div className="flex items-center gap-2 text-sm text-gray-400">
            <span className="font-mono text-primary-400">#{issue.number}</span>
            <Calendar className="w-4 h-4" />
            {formatRelativeTime(issue.created_at)}
          </div>
        </div>
      </div>
    </article>
  );
}
```

---

## API Integration

### GitHub Service Pattern
```tsx
export class GitHubService {
  private baseUrl: string;
  private token?: string;

  constructor() {
    this.baseUrl = `${GITHUB_API_BASE}/repos/${REPO_OWNER}/${REPO_NAME}`;
    this.token = process.env.NEXT_PUBLIC_GITHUB_TOKEN;
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Accept': 'application/vnd.github.v3+json',
      'Content-Type': 'application/json',
    };

    if (this.token) {
      headers.Authorization = `token ${this.token}`;
    }

    return headers;
  }

  async fetchIssues(params?: IssueParams): Promise<GitHubIssue[]> {
    // Implementation with proper error handling
  }
}
```

### Error Handling
- Use descriptive error messages
- Implement retry logic for network requests
- Show user-friendly error states in UI
- Log errors for debugging

---

## Styling Guidelines

### Tailwind Usage
```css
/* Prefer utility classes */
<div className="flex items-center gap-4 p-6 bg-white/10 backdrop-blur-sm rounded-xl">

/* Use custom components for repeated patterns */
<div className="glass-card">

/* Responsive design */
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
```

### Custom CSS Classes
```css
/* Base layer - CSS reset and defaults */
@layer base {
  html {
    font-family: 'Inter', system-ui, sans-serif;
    scroll-behavior: smooth;
  }
}

/* Components layer - reusable patterns */
@layer components {
  .glass-card {
    @apply bg-glass border border-white/20 backdrop-blur-glass rounded-2xl shadow-2xl;
  }
  
  .gradient-text {
    @apply bg-gradient-to-r from-primary-500 to-secondary-500 bg-clip-text text-transparent;
  }
}
```

### Animation Guidelines
- Use Tailwind's built-in animations
- Custom keyframes in `tailwind.config.js`
- Prefer `transition-all duration-300` for hover states
- Use `animate-slide-up` for modals/cards

---

## Environment Setup

### Required Environment Variables
```bash
NEXT_PUBLIC_GITHUB_TOKEN=ghp_your_token_here  # Optional but recommended for higher rate limits
```

### Development Commands
```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run start        # Start production server
npm run lint         # Run ESLint
npm run type-check   # TypeScript validation
npm run format       # Format with Prettier
```

### Dependencies Management
- Keep dependencies updated
- Use exact versions for critical packages
- Prefer React 19+ compatible packages
- Test thoroughly before updating major versions

---

## Tutorial System

### Tutorial Architecture
- **State Management**: `useTutorial` hook
- **Step Data**: Defined in `src/lib/tutorial-data.tsx`
- **Modal Component**: `TutorialModal` with step navigation
- **Persistence**: Browser localStorage (disabled in artifacts)

### Adding Tutorial Steps
```tsx
export const tutorialSteps: TutorialStep[] = [
  {
    id: 'step-id',
    title: 'Step Title',
    description: 'Brief description',
    content: (
      <div className="space-y-4">
        {/* JSX content */}
      </div>
    ),
    action: {
      type: 'link',
      url: 'https://example.com',
      text: 'Action Button Text'
    }
  }
];
```

---

## Best Practices Summary

### Code Organization
- ✅ Use barrel exports in index files
- ✅ Group related functionality in folders
- ✅ Keep components focused and single-purpose
- ✅ Use TypeScript interfaces over types when possible

### Performance
- ✅ Implement proper loading states
- ✅ Use React.memo for expensive components
- ✅ Optimize images and assets
- ✅ Implement proper error boundaries

### Accessibility
- ✅ Use semantic HTML elements
- ✅ Provide proper ARIA labels
- ✅ Ensure keyboard navigation
- ✅ Maintain color contrast ratios

### Security
- ✅ Sanitize user inputs
- ✅ Use environment variables for secrets
- ✅ Implement proper CORS settings
- ✅ Validate API responses

### Testing Strategy
- Unit tests for utility functions
- Integration tests for API services
- Component testing with React Testing Library
- E2E testing for critical user flows

---

## Common Patterns

### Conditional Rendering
```tsx
{isLoading && <LoadingSpinner />}
{error && <ErrorMessage error={error} />}
{data?.length === 0 && <EmptyState />}
{data?.map(item => <ItemComponent key={item.id} item={item} />)}
```

### Form Handling
```tsx
const [filters, setFilters] = useState<IssueFilters>(defaultFilters);

const updateFilter = (key: keyof IssueFilters, value: any) => {
  setFilters(prev => ({ ...prev, [key]: value }));
};
```

### API Error Handling
```tsx
if (!response.ok) {
  throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
}
```

## Conclusion

This comprehensive guide serves as the foundation for maintaining consistency and quality throughout the **ongoing development** of the Pond0x Issues Dashboard. 

### Remember:
- 🔄 **Continuous Improvement**: Every interaction with this codebase is an opportunity for enhancement
- 📈 **Quality Evolution**: Standards and practices will evolve as the project matures
- 🚀 **Future-Ready**: Build with tomorrow's features in mind while delivering today's requirements
- 🤝 **Collaborative Growth**: This documentation and the project itself will grow through collective contributions

**The project is never "complete" - it's always evolving, always improving, always adapting to new requirements and opportunities.**