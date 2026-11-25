---
name: Angular
description: Avoid common Angular mistakes — subscription leaks, change detection, dependency injection, and module organization.
metadata: {"clawdbot":{"emoji":"🅰️","requires":{"bins":["node"]},"os":["linux","darwin","win32"]}}
---

## Subscription Leaks
- Manual subscribe needs unsubscribe — in `ngOnDestroy` or use `takeUntilDestroyed()`
- `async` pipe auto-unsubscribes — prefer over manual subscribe in templates
- `takeUntilDestroyed()` in inject context — cleaner than Subject + takeUntil pattern
- HTTP observables complete automatically — but others don't, always handle cleanup

## Change Detection
- Default checks entire component tree — expensive with large apps
- `OnPush` only checks on input change or event — add `changeDetection: ChangeDetectionStrategy.OnPush`
- Mutating objects doesn't trigger OnPush — create new reference: `{...obj}` or `[...arr]`
- `markForCheck()` to manually trigger — when async changes data outside Angular

## Dependency Injection
- `providedIn: 'root'` for singleton services — tree-shakeable, no module registration needed
- Component-level `providers` creates new instance — per component, not shared
- `@Optional()` for optional dependencies — prevents error if not provided
- `@Inject(TOKEN)` for injection tokens — not just classes

## Lifecycle Hooks
- `ngOnInit` after inputs set — use for initialization, not constructor
- `ngOnChanges` before `ngOnInit` — called on every input change, receives `SimpleChanges`
- `ngAfterViewInit` for DOM access — `@ViewChild` not available until then
- `ngOnDestroy` for cleanup — subscriptions, timers, event listeners

## Templates
- `*ngFor` needs `trackBy` for performance — prevents re-rendering entire list
- `trackBy` function returns unique identifier — `trackByFn = (i, item) => item.id`
- `@if` and `@for` (Angular 17+) replace `*ngIf`/`*ngFor` — better performance, cleaner syntax
- `ng-container` for structural directives — no DOM element added

## Reactive Forms
- `FormGroup` and `FormControl` for reactive — not two-way binding
- Validators at control level — `Validators.required`, `Validators.email`
- `valueChanges` is Observable — subscribe or use async pipe
- `patchValue` for partial update — `setValue` requires all fields

## Modules vs Standalone
- Standalone components don't need module — `standalone: true` in decorator
- Import directly in other standalone components — no module declaration needed
- Mixing: standalone can import modules — modules can import standalone
- New projects prefer standalone — modules for legacy or complex DI

## Routing
- Lazy load with `loadComponent` or `loadChildren` — reduces initial bundle
- Guards return `boolean`, `UrlTree`, or Observable — `UrlTree` for redirects
- Resolvers pre-fetch data — available in `ActivatedRoute.data`
- Route params: `snapshot` once, `paramMap` Observable — for navigation without destroy

## Common Mistakes
- `ElementRef.nativeElement` direct DOM access — breaks SSR, use Renderer2
- `setTimeout` outside Angular zone — use `NgZone.run()` or change detection won't trigger
- Circular dependency in DI — use `forwardRef()` or restructure
- `HttpClient` methods return cold Observable — each subscribe makes new request
