---
name: author-component
description: "> Create or review Blazor components (.razor files) with correct architecture. USE FOR: writing new Blazor components that do NOT involve JavaScript interop, implementing parameters and EventCallback, RenderFragment slots, component lifecycle (OnInitializedAsy"
category: cloud
version: 1.0.0
disable-model-invocation: false
risk: low
source:
  repository: "microsoft/skills"
  commit: "8f3b1a2c"
  path: "plugins/dotnet-blazor/skills/author-component/SKILL.md"
  license: "MIT"
  imported_at: "2026-09-20"
---
# Author Blazor Component

## Core Rules

- Data flows **down** via `[Parameter]`. Events flow **up** via `EventCallback<T>` (never `Action`/`Func`).
- Never mutate `[Parameter]` properties. Copy to a private field in `OnParametersSet`.
- Use `[Parameter] public T Prop { get; set; }` — never `required` or `init` (causes BL0007).
- Use `[EditorRequired]` for required parameters.
- Handle all states: loading, empty, loaded, error — each with `@if`/`@else`.
- Use `@key` on repeated elements in loops for efficient diffing.
- Use `IReadOnlyList<T>` (not `IEnumerable<T>`) for collection parameters.

## RenderFragment & Generics

```csharp
[Parameter] public RenderFragment? ChildContent { get; set; }
[Parameter] public RenderFragment<TItem>? RowTemplate { get; set; }  // generic template
```

Use `@typeparam TItem` for generic components.

## File Patterns

- **Single-file:** `.razor` with `@code` block when logic < ~50 lines.
- **Code-behind:** `.razor` + `.razor.cs` with `partial class` when logic > ~50 lines.

## Disposal

Implement `IAsyncDisposable` (not `IDisposable`) when the component owns subscriptions, timers, or CTS.
In `DisposeAsync`: unsubscribe (`-=`), cancel CTS, dispose resources. Never call `StateHasChanged`.

## Async Patterns

- `await` every async operation. Never use `.Result`, `.Wait()`, `Task.Run`, `ContinueWith`, `Thread.Start`.
- **Debounce:** `Task.Delay` + `CancellationTokenSource`. Cancel old CTS, create new, await delay, do work. Never use `System.Threading.Timer` or `System.Timers.Timer`.
- **Polling:** Loop in `OnInitializedAsync` with `await Task.Delay(interval, token)` — stays on sync context.
- **External events** (`Action<T>`): Use `async void` handler + `await InvokeAsync(() => { state++; StateHasChanged(); })` + `catch` → `DispatchExceptionAsync`. Never `_ = InvokeAsync(...)`.
- Cancel CTS in `DisposeAsync`. Don't catch `ObjectDisposedException` — use CTS cancellation.

## Don'ts

- `required`/`init` on `[Parameter]` — runtime failure
- Mutate `[Parameter]` — copy to private field in `OnParametersSet`
- `Action`/`Func` for events — use `EventCallback<T>`
- `Task.Run`/`.Result`/`.Wait()`/Timer for debounce — deadlock or thread-pool escape
- Inline `style` attributes — use CSS classes or `data-*` attributes
- `catch { throw; }` — use `when` guard or let exceptions propagate
- Gold-plating: ARIA, wrapper divs, accessibility features not requested
- `_ = InvokeAsync(...)` — swallows exceptions; use `async void` + `DispatchExceptionAsync`
