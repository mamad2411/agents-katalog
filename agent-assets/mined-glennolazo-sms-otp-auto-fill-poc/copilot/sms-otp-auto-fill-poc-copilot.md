# POC-OTP Angular Project - AI Coding Assistant Instructions

## Project Architecture

This is an Angular 20.1 standalone application using **modern Angular patterns**:
- **Standalone components** without NgModules - see `src/app/app.ts`
- **Signals** for reactive state management - `protected readonly title = signal('POC-OTP')`
- **Application bootstrap** via `bootstrapApplication()` in `src/main.ts`
- **Provider-based configuration** in `src/app/app.config.ts`

## File Structure Conventions

- **Component naming**: Use class name `App` (not `AppComponent`) - see `src/app/app.ts`
- **Template separation**: Components use separate `.html` files via `templateUrl`
- **Style separation**: Components use separate `.css` files via `styleUrl` (not `styleUrls`)
- **Protected members**: Use `protected readonly` for template-accessible properties

## Development Workflow

### Available Scripts
```bash
npm start          # Development server (ng serve)
npm run build      # Production build
npm run watch      # Development build with file watching
npm test           # Run Karma unit tests
```

### Build Configuration
- **Development**: Source maps enabled, no optimization
- **Production**: Bundle budgets enforced (500kB initial, 4kB component styles)
- **Assets**: Served from `public/` directory (not `src/assets/`)

## TypeScript Configuration

Strict TypeScript settings enabled:
- `strict: true`
- `noImplicitReturns: true`
- `noFallthroughCasesInSwitch: true`
- `noPropertyAccessFromIndexSignature: true`

Angular-specific strict settings:
- `strictInjectionParameters: true`
- `strictInputAccessModifiers: true`
- `strictTemplates: true`

## Code Patterns

### Component Structure
```typescript
import { Component, signal } from '@angular/core';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet],  // Direct imports, no NgModule
  templateUrl: './app.html',
  styleUrl: './app.css'     // Note: styleUrl not styleUrls
})
export class App {
  protected readonly title = signal('POC-OTP');
}
```

### Application Bootstrap
```typescript
// main.ts
import { bootstrapApplication } from '@angular/platform-browser';
import { appConfig } from './app/app.config';
import { App } from './app/app';

bootstrapApplication(App, appConfig)
  .catch((err) => console.error(err));
```

### Configuration Pattern
```typescript
// app.config.ts
export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideZoneChangeDetection({ eventCoalescing: true }),
    provideRouter(routes)
  ]
};
```

## Code Formatting

- **Prettier configured** for Angular HTML templates: `"parser": "angular"`
- Follow existing patterns in `src/app/app.ts` for component structure

## Key Dependencies

- **Angular 20.1**: Latest version with new control flow syntax support
- **RxJS 7.8**: For reactive programming
- **Zone.js 0.15**: For change detection
- **Karma + Jasmine**: For unit testing

## When Adding Features

1. Create **standalone components** without NgModules
2. Use **signals** for reactive state instead of observables where appropriate
3. Import dependencies directly in component `imports` array
4. Place new routes in `src/app/app.routes.ts`
5. Add providers to `src/app/app.config.ts`