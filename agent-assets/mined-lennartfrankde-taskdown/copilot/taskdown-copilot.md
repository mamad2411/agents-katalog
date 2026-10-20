# Copilot Instructions for Taskdown

## Project Overview

Taskdown is a modern task management application built with SvelteKit and TypeScript. It features both web and desktop capabilities through Tauri integration, uses PocketBase as its database, and includes comprehensive deployment automation through Docker and Coolify.

## Technology Stack

### Core Framework

- **SvelteKit**: Modern web framework with SSR/SSG capabilities
- **TypeScript**: For type safety and better developer experience
- **Svelte 5**: Latest version with new runes syntax ($props, $state, etc.)

### Styling & UI

- **Tailwind CSS 4.0**: Utility-first CSS framework with all features enabled
- **@tailwindcss/forms**: Form styling utilities
- **@tailwindcss/typography**: Typography utilities

### Desktop Integration

- **Tauri 2.0**: Cross-platform desktop application framework
- **@tauri-apps/api**: Tauri JavaScript/TypeScript API

### Database & Backend

- **PocketBase**: Backend-as-a-Service with real-time capabilities
- Available at `http://localhost:8090` in development

### Development Tools

- **Vite**: Build tool and development server
- **ESLint**: Linting with TypeScript and Svelte support
- **Prettier**: Code formatting with Svelte and Tailwind plugins
- **Vitest**: Unit testing framework
- **Playwright**: End-to-end testing

### Deployment & Infrastructure

- **Docker**: Containerization with multi-stage builds
- **Coolify**: Deployment platform with auto-provisioning
- **GitHub Actions**: CI/CD workflows (configurable)

## File Structure Patterns

```
src/
├── lib/                    # Reusable components and utilities
│   ├── components/         # Svelte components
│   ├── stores/            # Svelte stores for state management
│   ├── utils/             # Utility functions
│   └── assets/            # Static assets
├── routes/                 # SvelteKit file-based routing
│   ├── +layout.svelte     # Root layout
│   ├── +page.svelte       # Home page
│   └── api/               # API routes (+server.ts files)
└── app.html               # HTML template
```

## Code Style and Conventions

### Svelte Components

- Use Svelte 5 runes syntax: `$props()`, `$state()`, `$derived()`
- Component names in PascalCase
- Use TypeScript for all component scripts
- Prefer composition over inheritance

```svelte
<script lang="ts">
	interface Props {
		title: string;
		items: string[];
	}

	let { title, items }: Props = $props();
	let selectedItem = $state<string | null>(null);
</script>
```

### TypeScript

- Strict mode enabled
- Use explicit types for props and component interfaces
- Prefer `interface` over `type` for object shapes
- Use proper typing for Tauri API calls

### Styling

- Use Tailwind CSS classes exclusively
- Follow mobile-first responsive design
- Utilize Tailwind's design tokens for consistency
- Use `@apply` sparingly, prefer utility classes

### File Naming

- Routes: `+page.svelte`, `+layout.svelte`, `+server.ts`
- Components: `ComponentName.svelte`
- Utilities: `camelCase.ts`
- Types: `types.ts` or inline interfaces

## SvelteKit Patterns

### Routes

- Use `+page.svelte` for pages
- Use `+layout.svelte` for shared layouts
- Use `+server.ts` for API endpoints
- Use `+page.server.ts` for server-side data loading

### Data Loading

```typescript
// +page.server.ts
export async function load() {
	return {
		items: await fetchItems()
	};
}
```

### API Routes

```typescript
// +server.ts
import { json } from '@sveltejs/kit';

export async function GET() {
	return json({ status: 'ok' });
}
```

## Testing Conventions

### Unit Tests (Vitest)

- Place tests next to source files with `.test.ts` or `.spec.ts`
- Use `@testing-library/svelte` for component testing
- Mock external dependencies

### E2E Tests (Playwright)

- Place tests in `e2e/` directory
- Use page object pattern for complex interactions
- Test critical user workflows

## Development Workflow

### Local Development

```bash
npm install                 # Install dependencies
npm run services:start     # Start PocketBase and other services
npm run dev                # Start development server
```

### Code Quality

```bash
npm run lint               # ESLint + Prettier check
npm run format             # Fix formatting issues
npm run check              # Svelte type checking
```

### Testing

```bash
npm run test:unit          # Run unit tests
npm run test:e2e           # Run E2E tests
npm test                   # Run all tests
```

### Tauri Development

```bash
npm run tauri:dev          # Run desktop app in development
npm run tauri:build        # Build desktop app
```

## Tauri Integration Patterns

### Tauri Commands

- Define commands in Rust backend (`src-tauri/`)
- Import and use in frontend with proper typing

```typescript
import { invoke } from '@tauri-apps/api/core';

interface TaskData {
	id: string;
	title: string;
	completed: boolean;
}

async function createTask(task: TaskData): Promise<string> {
	return await invoke('create_task', { task });
}
```

### Window Management

```typescript
import { getCurrentWindow } from '@tauri-apps/api/window';

const appWindow = getCurrentWindow();
await appWindow.setTitle('Taskdown - Task Manager');
```

## PocketBase Integration

### Connection

- Development: `http://localhost:8090`
- Production: Configured via environment variables
- Use PocketBase JavaScript SDK for API calls

### Authentication

```typescript
import PocketBase from 'pocketbase';

const pb = new PocketBase('http://localhost:8090');
await pb.collection('users').authWithPassword(email, password);
```

## Best Practices

### Performance

- Use `$derived` for computed values
- Implement proper loading states
- Optimize bundle size with dynamic imports
- Use Svelte transitions sparingly

### Accessibility

- Use semantic HTML elements
- Implement proper ARIA attributes
- Ensure keyboard navigation works
- Test with screen readers

### Security

- Validate all user inputs
- Use proper CORS configuration
- Implement authentication checks
- Sanitize data before database operations

### Error Handling

- Use try-catch blocks for async operations
- Implement user-friendly error messages
- Log errors appropriately
- Handle network failures gracefully

## Common Patterns to Follow

### State Management

```typescript
// Use stores for global state
import { writable } from 'svelte/store';

export const tasks = writable<Task[]>([]);

// Use $state for component-local state
let isLoading = $state(false);
```

### Form Handling

```svelte
<script lang="ts">
	let formData = $state({ title: '', description: '' });

	async function handleSubmit() {
		// Validate and submit
	}
</script>

<form onsubmit={handleSubmit}>
	<input bind:value={formData.title} required />
	<textarea bind:value={formData.description}></textarea>
	<button type="submit">Submit</button>
</form>
```

### API Calls

```typescript
async function fetchTasks(): Promise<Task[]> {
	try {
		const response = await fetch('/api/tasks');
		if (!response.ok) throw new Error('Failed to fetch tasks');
		return await response.json();
	} catch (error) {
		console.error('Error fetching tasks:', error);
		throw error;
	}
}
```

## Environment Configuration

### Development

- Services available via `npm run services:start`
- Hot reloading enabled
- Source maps available

### Production

- Static site generation with fallback for SPA mode
- Docker containerization
- Health checks at `/health` endpoint

## Notes for AI Assistance

- Always use TypeScript for type safety
- Prefer Svelte 5 runes over legacy reactive syntax
- Follow the established file structure
- Use Tailwind utilities instead of custom CSS
- Consider both web and desktop contexts when suggesting features
- Test suggestions work with the current SvelteKit version
- Respect the existing code style and patterns
