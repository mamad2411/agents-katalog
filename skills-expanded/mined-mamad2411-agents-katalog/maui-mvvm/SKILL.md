---
name: maui-mvvm
description: Build, refactor, and review .NET MAUI features that follow the Model-View-ViewModel pattern. Use when Codex needs to create or update MAUI `ContentPage`/`ContentView` XAML, `ViewModel` classes, bindings, commands, validation state, Shell navigation, or supporting services while keeping UI logic out of code-behind and preserving testable MVVM boundaries.
---

# Maui MVVM

Implement .NET MAUI UI features with a strict MVVM split: XAML view, testable viewmodel, and non-visual model/service code. Preserve existing project conventions first, then apply the rules below to keep the code loosely coupled and easy to verify.

## Workflow

1. Inspect the app structure before editing.
   Check how the repo names `Views`, `ViewModels`, `Models`, `Services`, converters, and behaviors. Reuse the existing navigation and dependency injection style instead of introducing a second pattern.
2. Decide the smallest valid MVVM change.
   Prefer adding or adjusting a viewmodel property, command, converter, or service over pushing logic into code-behind.
3. Implement or update the viewmodel first.
   Expose state and user actions as bindable properties and commands. Keep the viewmodel free of view types and direct control references.
4. Bind the view to the viewmodel.
   Assign `BindingContext` using the project's established composition style, then wire XAML bindings, command bindings, and template bindings.
5. Keep navigation and cross-component communication testable.
   If navigation is involved, prefer a service abstraction or the repo's existing navigation wrapper instead of view-to-view coupling.
6. Verify behavior.
   Check property change notifications, empty/loading/error states, async responsiveness, and whether bindings compile or resolve correctly.

## Core Rules

### View

- Define structure, layout, and appearance in XAML whenever practical.
- Keep code-behind thin. Allow only UI-specific concerns that are difficult to express in XAML, such as visual behavior or animation hooks.
- Do not place business logic, persistence logic, or decision-heavy navigation logic in code-behind.
- Bind UI enablement, visibility, and pending-state indicators to viewmodel properties instead of toggling controls directly in code-behind.
- Use behaviors when a control exposes an event but not a usable command path, and forward the interaction to a viewmodel command.

### ViewModel

- Make the viewmodel the binding surface for the view.
- Expose state through properties and actions through commands.
- Support change notification with `INotifyPropertyChanged`, `BindableObject`, or the repo's existing MVVM base type.
- Raise property change notifications only when the value actually changes.
- Raise dependent property notifications when computed properties rely on changed state.
- Avoid raising property change notifications from constructors during initial setup.
- Prefer asynchronous commands and methods for I/O or long-running work so the UI thread stays responsive.
- Keep the viewmodel unaware of concrete view classes and controls.
- Centralize presentation-friendly data shaping in the viewmodel or in dedicated converters already used by the repo.

### Model And Services

- Keep domain data, validation rules, API access, persistence, and caching in models and services, not in the view.
- Use the viewmodel to coordinate model/service calls and expose results in a binding-friendly form.
- If the project already uses repositories or service interfaces, keep that abstraction intact.

## Binding Guidance

- Ensure every view has a clear `BindingContext` assignment path.
- Prefer compiled bindings with `x:DataType` when the codebase already uses XAML compiled bindings or when introducing new XAML pages/templates.
- Set `x:DataType` at the same scope where the binding context type is known.
- Set `x:DataType` explicitly on each `DataTemplate` to avoid inheriting the wrong outer type.
- Use `ObservableCollection<T>` for collections that change over time.
- Keep binding mode explicit when two-way interaction matters.
- Use converters sparingly for formatting or view-only transformation; do not hide business rules in converters.

## Commands, State, And Validation

- Model user actions as `ICommand` or the repo's command abstraction.
- Disable or gate commands through bindable state instead of manually guarding button clicks in the view.
- Represent loading, empty, success, and error states as explicit viewmodel properties.
- When validation exists, expose validation messages or validity flags from the viewmodel or model layer so the view can bind to them.

## Navigation

- Follow the app's existing navigation mechanism first.
- If the app uses Shell, keep route-based navigation aligned with Shell registration and parameter passing.
- Prefer invoking navigation from the viewmodel through an injected navigation service or established abstraction.
- Pass initialization data through navigation parameters or query properties instead of relying on shared mutable view state.
- Keep navigation targets loosely coupled. Avoid direct references from one viewmodel to unrelated view classes.

## Composition Choice

- Prefer view-first composition for standard MAUI apps unless the repo already has a clear viewmodel-first framework.
- Declarative `BindingContext` in XAML is acceptable for simple parameterless viewmodels.
- Programmatic `BindingContext` assignment is acceptable when dependencies are injected.
- Do not mix multiple composition strategies in the same feature unless the repo already does so consistently.

## CommunityToolkit.Mvvm

If the project already uses `CommunityToolkit.Mvvm`, prefer its existing conventions such as observable properties, relay commands, and messenger patterns. Do not introduce the toolkit into a repo that currently uses manual `INotifyPropertyChanged` or a different MVVM framework unless the user explicitly asks for that migration.

## Review Checklist

- Confirm the view contains presentation concerns, not business logic.
- Confirm the viewmodel exposes all state the view needs without referencing view types.
- Confirm property and collection changes notify the UI correctly.
- Confirm async work does not block the UI thread.
- Confirm command availability and busy-state behavior are represented in bindable state.
- Confirm `DataTemplate` bindings have the correct `x:DataType`.
- Confirm navigation stays within the repo's established abstraction.
- Confirm new code matches the existing namespace, folder, DI, and naming conventions.

## References

- Load [references/microsoft-learn.md](./references/microsoft-learn.md) when you need the distilled Microsoft guidance and source links behind this skill.
