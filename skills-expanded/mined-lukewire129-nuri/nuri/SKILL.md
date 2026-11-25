---
name: nuri
description: Build C# desktop UI applications with Nuri, a React-style MVU framework that renders platform-neutral virtual elements into native WPF and Avalonia controls. Use when creating or editing Nuri components, hooks (useState, useEffect, useStore, useMemo), keyed lists, routing, or animations, when scaffolding a XAML-free pure-C# desktop app, or when debugging Nuri rendering, lifecycle, or diagnostics output.
---

# Nuri Application Skill

Nuri components are plain C# classes. `Render()` returns platform-neutral `IElement` descriptions, and the renderer adapter materializes them into native WPF or Avalonia controls. No XAML, no ViewModels, no data binding.

## Step 1: Choose a Renderer

| Situation | Renderer | Package | Read next |
|---|---|---|---|
| Windows-only app, or modernizing an existing WPF application | WPF | `Nuri.WPF` | [references/wpf.md](references/wpf.md) |
| Cross-platform app, or an existing Avalonia host application | Avalonia | `Nuri.Avalonia` | [references/avalonia.md](references/avalonia.md) |

Read only the reference file for the chosen renderer, then follow its startup pattern. Never mix renderer-specific APIs in one application, and never reference WPF or Avalonia types inside a component.

## Step 2: Scaffold

Inside a Nuri repository clone, do not use NuGet: follow [apps/README.md](https://github.com/lukewire129/Nuri/blob/main/apps/README.md), create the project under `apps/`, and reference the `src/` renderer projects with `ProjectReference`. The seed app is `apps/HelloNuri`.

Otherwise, with the `Nuri.Templates` NuGet package installed (`dotnet new install Nuri.Templates`):

```powershell
dotnet new nuri.wpf -n MyApp
dotnet new nuri.avalonia -n MyApp
dotnet new nuri-component -n Todo    # single component item template
```

## Non-Negotiable Rules

- `Render()` returns platform-neutral `IElement` descriptions. Do not create WPF, Avalonia, or Duxel controls in Core components.
- Call ordered hooks consistently on every render. Do not put state, reducer, ref, latest, store, memo, effect, or navigation hooks behind conditional control flow.
- Use `.Key(...)` for stateful dynamic-list and route children.
- Put fast-changing state in the smallest component that displays it. Preserve parent ownership when siblings coordinate on the same state.
- Treat `useService<T>()` as an `IServiceProvider` lookup. Nuri does not own service registration, lifetime, or disposal; use `Store<T>` or `useEffect` for observable service state.
- Keep renderer-specific APIs in the application host, not in components.

## Component Structure Template

Every component follows this layout. Keep the order exactly as shown.

```csharp
using Nuri.UI.Controls;
using Nuri.UI.Dsl;
using Nuri.UI.Values;

namespace Sample.Components;

public sealed class MyComponent : Component
{
    private static readonly Item[] InitialItems = { ... };

    public override IElement Render()
    {
        // 1. Hooks (always in the same order)
        var (state, setState) = useState(new MyState(...));
        var stateRef = useLatest(state);
        var derived = useMemo(() => Compute(state), state);

        // 2. Blank line

        // 3. Local functions (state mutators)
        void Update(Func<MyState, MyState> change)
        {
            var next = change(stateRef.Current);
            stateRef.Current = next;
            setState(_ => next);
        }

        void DoSomething() { ... }

        // 4. Blank line

        // 5. Return the UI tree
        return
            Div(
                Text("Title")
                    .FontSize(22)
                    .FontWeight(FontWeightValue.Bold),
                Button("Action", DoSomething)
            )
            .Padding(24)
            .Background("#0f172a");
    }

    // 6. Static helper methods for UI decomposition
    private static IElement SubView(Item item) { ... }

    // 7. Static pure functions
    private static string[] Validate(MyState state) { ... }
}

// 8. Record types at the bottom of the file
internal sealed record MyState(string Draft, Item[] Items);
internal sealed record Item(string Id, string Text);
```

## Hook Quick Reference

| Hook | Use |
|---|---|
| `useState<T>(initial)` | component-local state; the setter receives `Func<T, T>` |
| `useReducer<TState, TAction>(reducer, initial)` | complex state transitions |
| `useRef<T>(initial)` | mutable box that never triggers a render (drag, pan) |
| `useLatest<T>(value)` | stale-closure-safe latest value inside callbacks |
| `useMemo<T>(factory, deps...)` | derived data cached until dependencies change |
| `useEffect(effect, deps)` | async loading, subscriptions, timers; return a cleanup function |
| `useStore(store)` / `useStore(store, selector)` | state shared across components |
| `useService<T>()` | resolve from the externally configured `IServiceProvider` |
| `useNavigation(initialRoute)` | local route state; pair with `Router(...)` and `Route(...)` |

Setter forms: `setCount(current => current + 1)` for updates based on the existing value, `setCount(_ => 42)` for replacement.

Shared state:

```csharp
internal static class UserStore
{
    public static readonly Store<UserState> State = Store.Create(new UserState("Guest"));
}

public override IElement Render()
{
    var user = useStore(UserStore.State, s => s);
    return Text(user.Name);
}
```

Effect with cleanup:

```csharp
useEffect(() =>
{
    var cts = new CancellationTokenSource();
    _ = LoadAsync(cts.Token);
    return () => cts.Cancel();
}, Array.Empty<object>());
```

## Keys

Use explicit keys for rows and components whose identity must survive reorder, filter, edit, or remove operations:

```csharp
Div(items.Select(item =>
    (IElement)new TodoItemComponent(item).Key(item.Id)
).ToArray());
```

Use a stable, sibling-unique value. `Name` is only a compatibility fallback; new code should always use `.Key(...)`.

## Layout Essentials

- `Grid(...)` with fluent `.Rows("Auto,*")` and `.Columns(240, Star)`; numeric values are pixels, `*` and `2*` are weighted.
- `Scroll(...)` is a single-content viewport; put vertical layout and spacing on its one child.
- `VStack(...)` / `HStack(...)` create vertical/horizontal stacks.
- Animate with `.Transition(ms, EasingValue.CubicInOut)` after the property setter that should animate.

## Formatting Essentials

- `return` on its own line; indent the expression by 4 spaces.
- Container children one per line; container fluent calls at closing-paren indentation.
- One blank line between hooks, local functions, and the return expression.
- Full rules and Good/Bad examples: [references/design.md](references/design.md).

## Design Conventions

Use the palettes, spacing scale, and pre-finish checklist in [references/design.md](references/design.md). Do not invent arbitrary hex colors.

## Debugging

When runtime behavior is wrong (blank UI, stale values, duplicated state, performance), follow the self-diagnosis loop in [references/troubleshooting.md](references/troubleshooting.md) before changing code.

## Verification Before Finishing

1. `dotnet build -c Release` passes with zero errors.
2. Run the app and exercise the changed behavior.
3. Check runtime diagnostics output for `DuplicateKey`, `UnsupportedProperty`, `UnsupportedEvent`, or unexpected `FullRebuild` entries.

## Full Documentation

- [Getting Started](https://github.com/lukewire129/Nuri/blob/main/docs/guides/GETTING_STARTED.md)
- [Hook Reference](https://github.com/lukewire129/Nuri/blob/main/docs/guides/HOOKS.md)
- [Formatting](https://github.com/lukewire129/Nuri/blob/main/docs/guides/FORMATTING.md)
- [YAML Styles](https://github.com/lukewire129/Nuri/blob/main/docs/guides/YAML_STYLES.md)
- Working on the Nuri repository itself: [AGENTS.md](https://github.com/lukewire129/Nuri/blob/main/AGENTS.md)
