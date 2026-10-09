---
name: migration-migrate-component
description: "Use when a component needs migration to the target architecture or framework version."
user-invocable: true
argument-hint: "[component-file]"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

Migrate an Angular component to standalone with signals following `docs/ARCHITECTURE.md` section 5.

Component: $ARGUMENTS

## Steps

1. Read `docs/ARCHITECTURE.md` section 5.

2. Analyze the component:
   - Count lines (template, class)
   - List: @Input, @Output, constructor deps, lifecycle hooks, NgModule membership
   - Map who imports this component

3. Convert to modern Angular:
   - `@NgModule` membership -> `standalone: true`
   - `@Input() prop` -> `readonly prop = input<T>()`
   - `@Output() event = new EventEmitter()` -> `readonly event = output<T>()`
   - `constructor(private svc: Service)` -> `private readonly svc = inject(Service)`
   - `ngOnInit()` -> `constructor` or `afterNextRender()`
   - `ngOnChanges()` -> `effect()` watching input signals
   - `*ngIf` -> `@if () { }`
   - `*ngFor` -> `@for (item of items; track item.id) { }`
   - Add `ChangeDetectionStrategy.OnPush`

4. Apply composition pattern if there is prop drilling.

5. Decompose if > 200 lines.

6. Validate:
```bash
npx tsc --noEmit
ng build
ng test --watch=false
```
