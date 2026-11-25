---
name: angular-signals-migration
description: Moves Angular components to signals, signal inputs and standalone APIs one component at a time, with a build and test run after each step.
---

# Angular signals migration

Migrate one component per pass. Never touch a component the user did not name, apart from its direct parents when a template call site must change.

## Steps

1. Read the component, its template, its spec and every place it is used. Note which fields the template reads.
2. Make it standalone if it is not: move imports from its NgModule into the component and remove it from the module declarations (`standalone: true` is the default from v19).
3. Convert inputs: `@Input() name` becomes `name = input<string>()` or `input.required<string>()`. Convert outputs to `output<T>()`. Two-way bindings use `model<T>()`.
4. Replace `ngOnChanges` and input setters with `computed()`. Use `effect()` only for side effects outside the template, never to set another signal.
5. Convert `@ViewChild` and `@ContentChild` to `viewChild()` and `contentChild()`.
6. Update the template: read signals with `name()`, and switch to `@if`, `@for (x of xs; track x.id)` and `@switch`.
7. Keep long-lived streams (HTTP polling, websockets) as observables and bridge them with `toSignal()` at the edge. Do not convert an RxJS pipeline that uses debounce, switchMap or retry.
8. Run `ng build` and `ng test --include <spec>`. Fix before moving on.

## Rules

- Do not add `ChangeDetectionStrategy.OnPush` unless the component already passes with it.
- Keep public names the same so parent templates need only call-site updates.

## Report

Files changed, parents that needed template edits, and anything left on observables with the reason.
