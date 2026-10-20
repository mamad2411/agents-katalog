---
name: angular-perf
description: "Angular performance and optimization patterns"
allowed-tools: []
---

# Minko Gechev: Angular Performance

Minko Gechev's core belief: **Performance is a feature, not an afterthought.** Every millisecond of load time and every kilobyte of bundle size affects user experience.

## The Foundational Principle

> "The fastest code is code that doesn't run. The smallest bundle is the one you don't ship."

Performance optimization in Angular is about:
- Shipping less JavaScript
- Running less change detection
- Loading only what's needed
- Measuring before optimizing

## Core Principles

### 1. Lazy Loading Is Non-Negotiable

Every feature module should be lazy loaded unless proven otherwise.

**Not this:**
```typescript
// app.module.ts - everything loaded upfront
@NgModule({
  imports: [
    UsersModule,
    AdminModule,
    ReportsModule,
    SettingsModule  // User may never visit settings
  ]
})
class AppModule {}
```

**This:**
```typescript
// app-routing.module.ts - load on demand
const routes: Routes = [
  { path: 'users', loadChildren: () => import('./users/users.module').then(m => m.UsersModule) },
  { path: 'admin', loadChildren: () => import('./admin/admin.module').then(m => m.AdminModule) },
  { path: 'reports', loadChildren: () => import('./reports/reports.module').then(m => m.ReportsModule) },
  { path: 'settings', loadChildren: () => import('./settings/settings.module').then(m => m.SettingsModule) }
];
```

**With standalone components (Angular 14+):**
```typescript
const routes: Routes = [
  {
    path: 'dashboard',
    loadComponent: () => import('./dashboard.component').then(c => c.DashboardComponent)
  }
];
```

### 2. OnPush Change Detection Strategy

Default change detection checks every component on every event. OnPush checks only when inputs change.

**Not this:**
```typescript
@Component({
  // Default change detection - checks on every click anywhere
})
class ExpensiveListComponent {
  @Input() items: Item[];
}
```

**This:**
```typescript
@Component({
  changeDetection: ChangeDetectionStrategy.OnPush  // Only checks when items reference changes
})
class ExpensiveListComponent {
  @Input() items: Item[];
}
```

**Rules for OnPush:**
- All `@Input()` must be immutable (new reference on change)
- Use `async` pipe for observables (triggers change detection correctly)
- Call `ChangeDetectorRef.markForCheck()` only when truly needed

### 3. TrackBy for All ngFor

Without trackBy, Angular destroys and recreates DOM for every change.

**Not this:**
```html
<li *ngFor="let user of users">{{ user.name }}</li>
<!-- Entire list re-rendered when any user changes -->
```

**This:**
```html
<li *ngFor="let user of users; trackBy: trackByUserId">{{ user.name }}</li>
<!-- Only changed items re-rendered -->
```

```typescript
trackByUserId(index: number, user: User): string {
  return user.id;
}
```

### 4. Async Pipe Over Manual Subscriptions

Manual subscriptions leak memory. Async pipe handles cleanup.

**Not this:**
```typescript
class UserComponent implements OnInit, OnDestroy {
  user: User;
  private subscription: Subscription;

  ngOnInit() {
    this.subscription = this.userService.getUser().subscribe(u => this.user = u);
  }

  ngOnDestroy() {
    this.subscription.unsubscribe();  // Easy to forget
  }
}
```

**This:**
```typescript
class UserComponent {
  user$ = this.userService.getUser();

  constructor(private userService: UserService) {}
}
```
```html
<div *ngIf="user$ | async as user">{{ user.name }}</div>
```

### 5. Bundle Analysis and Budgets

Set budgets, enforce them, analyze violations.

**angular.json:**
```json
{
  "budgets": [
    {
      "type": "initial",
      "maximumWarning": "500kb",
      "maximumError": "1mb"
    },
    {
      "type": "anyComponentStyle",
      "maximumWarning": "2kb",
      "maximumError": "4kb"
    }
  ]
}
```

**Analyze bundles:**
```bash
ng build --stats-json
npx webpack-bundle-analyzer dist/stats.json
```

### 6. Preloading Strategies

Don't just lazy load—preload intelligently.

```typescript
// Preload all modules after initial load
@NgModule({
  imports: [RouterModule.forRoot(routes, {
    preloadingStrategy: PreloadAllModules
  })]
})

// Or custom strategy - preload based on user behavior
@Injectable()
class CustomPreloadingStrategy implements PreloadingStrategy {
  preload(route: Route, load: () => Observable<any>): Observable<any> {
    return route.data?.['preload'] ? load() : of(null);
  }
}
```

### 7. Virtual Scrolling for Large Lists

Never render thousands of DOM nodes. Use virtual scrolling.

```typescript
import { ScrollingModule } from '@angular/cdk/scrolling';

@Component({
  template: `
    <cdk-virtual-scroll-viewport itemSize="50" class="viewport">
      <div *cdkVirtualFor="let item of items" class="item">
        {{ item.name }}
      </div>
    </cdk-virtual-scroll-viewport>
  `
})
class LargeListComponent {
  items = Array.from({ length: 10000 }, (_, i) => ({ name: `Item ${i}` }));
}
```

### 8. Web Workers for Heavy Computation

Offload CPU-intensive work to avoid blocking the main thread.

```typescript
// app.worker.ts
addEventListener('message', ({ data }) => {
  const result = heavyComputation(data);
  postMessage(result);
});

// component.ts
if (typeof Worker !== 'undefined') {
  const worker = new Worker(new URL('./app.worker', import.meta.url));
  worker.onmessage = ({ data }) => {
    this.result = data;
  };
  worker.postMessage(this.inputData);
}
```

### 9. Image Optimization with NgOptimizedImage

Angular's built-in image optimization directive.

```typescript
import { NgOptimizedImage } from '@angular/common';

@Component({
  imports: [NgOptimizedImage],
  template: `
    <img ngSrc="hero.jpg" width="800" height="600" priority>
    <img ngSrc="thumbnail.jpg" width="200" height="150" loading="lazy">
  `
})
```

**Benefits:**
- Automatic lazy loading
- Prevents layout shift (requires width/height)
- Preconnect hints for CDNs
- Warning for LCP images without `priority`

### 10. Defer Blocks (Angular 17+)

Declarative lazy loading in templates.

```html
@defer (on viewport) {
  <heavy-component />
} @placeholder {
  <lightweight-skeleton />
} @loading (minimum 500ms) {
  <spinner />
}
```

**Trigger options:**
- `on viewport` - when enters viewport
- `on idle` - when browser is idle
- `on interaction` - on click/focus
- `on hover` - on mouse hover
- `on timer(500ms)` - after delay

## The Gechev Test

Before shipping, ask:

1. **Is everything lazy loaded?** Feature modules, standalone components?
2. **Is OnPush used everywhere possible?** With immutable inputs?
3. **Do all ngFor have trackBy?** No exceptions?
4. **Am I within bundle budgets?** Have I analyzed what's in the bundle?
5. **Are large lists virtualized?** Or paginated?
6. **Is heavy computation off main thread?** Web workers for CPU work?
7. **Are images optimized?** Using NgOptimizedImage?

## When Reviewing Code

Apply these checks:

- [ ] Lazy loading for all feature modules
- [ ] `ChangeDetectionStrategy.OnPush` on components
- [ ] `trackBy` on all `*ngFor`
- [ ] `async` pipe instead of manual subscriptions
- [ ] Bundle budgets configured and passing
- [ ] Virtual scrolling for lists > 100 items
- [ ] Images use `NgOptimizedImage`
- [ ] No synchronous heavy computation in components
- [ ] Preloading strategy configured

## Performance Debugging

```typescript
// Enable Angular DevTools profiler
// In browser: Angular DevTools extension

// Measure change detection
import { enableDebugTools } from '@angular/platform-browser';
enableDebugTools(appRef.components[0]);
// Then in console: ng.profiler.timeChangeDetection()

// Trace what triggers change detection
constructor(private ngZone: NgZone) {
  ngZone.onStable.subscribe(() => console.log('CD cycle complete'));
}
```

## When NOT to Use This Skill

Use a different skill when:
- **Designing component architecture** → Use `angular-core` (DI, testability)
- **Applying design patterns** → Use `design-patterns`
- **General code clarity** → Use `clarity`
- **Type system design** → Use `typescript` (TypeScript)

Minko Gechev is the **Angular performance skill**—use it for optimization, lazy loading, and runtime efficiency.

## Sources

- Gechev, "Angular Performance Checklist" (GitHub)
- Angular documentation - Performance section
- web.dev Core Web Vitals guidance
- Gechev's conference talks on Angular performance

---

*"Measure first. Optimize what matters. Ship less JavaScript."* — Minko Gechev
