### Coding Guidelines & Best Practices

#### Object Instantiation

-   Create objects explicitly with all required properties, avoid empty type casting

```typescript
// Do
const directory: Directory = { name: '', owner: [], teams: [] };
// Don't
const directory = {} as Directory;
```

#### RxJS Patterns

-   Name Observables with dollar sign suffix: `myObservable$`
-   Use correct operators (e.g., `switchMap` for dependent async operations)
-   Always unsubscribe from Observables using `takeUntil()` or `takeUntilDestroyed()`

```typescript
// Modern approach with takeUntilDestroyed
private readonly destroyRef = inject(DestroyRef);
this.form.valueChanges
    .pipe(takeUntilDestroyed(this.destroyRef))
    .subscribe(value => { /* handle */ });

// Legacy approach with takeUntil
private destroy: Subject<void> = new Subject();
this.stream$.pipe(takeUntil(this.destroy)).subscribe(/* handle */);
```

#### Angular Material Components

-   Follow Angular Material component structure to ensure version compatibility
-   Use `@if` and `@for` syntax instead of `*ngIf` and `*ngFor`
-   Maintain proper semantic HTML with `mat-button` only on `<button>` or `<a>` elements
-   Use correct child elements (e.g., `<mat-list-item>` inside `<mat-list>`)

```html
<!-- Proper Material component structure -->
<mat-card class="example-card" appearance="outlined">
    <mat-card-header>
        <div mat-card-avatar class="example-header-image"></div>
        <mat-card-title>Shiba Inu</mat-card-title>
        <mat-card-subtitle>Dog Breed</mat-card-subtitle>
    </mat-card-header>
    ...
</mat-card>

<!-- Correct list structure -->
<mat-list>
    <mat-list-item>
        <span matListItemTitle>Pepper</span>
        <span matListItemLine>Produced by a plant</span>
    </mat-list-item>
</mat-list>

<!-- Modern control flow syntax -->
<mat-error>
    @if (materialForm.get('name')?.hasError('required')) { {{ 'COMMON.VALIDATION.REQUIRED' | translate }} } @if
    (materialForm.get('name')?.hasError('maxlength')) { {{ 'COMMON.VALIDATION.LESS_THEN_100' | translate }} }
</mat-error>

@for (icon of icons; track icon) {
<mat-option [value]="icon">
    <mat-icon>{{ icon }}</mat-icon>
</mat-option>
}

<!-- Semantic HTML with mat-button -->
<button mat-button (click)="doSomething()">Click me</button>
<a mat-button routerLink="/somewhere">Navigate</a>
<!-- Don't use mat-button on div elements -->
```