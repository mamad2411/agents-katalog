---
name: widgets-and-screens
description: Playbook for building Flutter screens and widgets in this project. Use whenever writing or editing any widget, setting up a route, theming, or wiring a bloc to the UI. Covers Material 3, page/view split, recomposition discipline, typed go_router, accessibility, and testing hooks.
---

# Widgets & screens

## The page/view split

Every routable screen has two files:

- `<Feature>Page` — **the route target.** Instantiates the bloc (via `GetIt` or by `BlocProvider` wiring), installs `BlocListener`s for one-shot effects, and hands off to the stateless view.
- `<Feature>View` — **pure, stateless.** Takes state in, emits callbacks out. This is what you `pumpWidget` in tests.

```dart
// presentation/pages/search_page.dart
class SearchPage extends StatelessWidget {
  const SearchPage({super.key});

  @override
  Widget build(BuildContext context) => BlocProvider<SearchBloc>(
        create: (_) => sl<SearchBloc>(),
        child: BlocListener<SearchBloc, SearchState>(
          listenWhen: (prev, curr) => prev.snack != curr.snack && curr.snack != null,
          listener: (context, state) {
            ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text(state.snack!)));
          },
          child: const _SearchPageBody(),
        ),
      );
}

class _SearchPageBody extends StatelessWidget {
  const _SearchPageBody();

  @override
  Widget build(BuildContext context) {
    final bloc = context.read<SearchBloc>();
    return BlocBuilder<SearchBloc, SearchState>(
      builder: (_, state) => SearchView(
        state: state,
        onQueryChanged: (q) => bloc.add(SearchEvent.queryChanged(q)),
        onItemTap: (id) => ItemRoute(id: id).go(context),
      ),
    );
  }
}
```

```dart
// presentation/widgets/search_view.dart
class SearchView extends StatelessWidget {
  const SearchView({
    required this.state,
    required this.onQueryChanged,
    required this.onItemTap,
    super.key,
  });
  final SearchState state;
  final ValueChanged<String> onQueryChanged;
  final ValueChanged<String> onItemTap;

  @override
  Widget build(BuildContext context) { /* ... */ }
}
```

## Why this split

- The view is trivially testable — no `GetIt`, no real bloc, no provider wiring.
- Navigation and snackbars happen in one place and don't pollute the view.
- You can preview the view under a fake state without running a bloc.

## Recomposition discipline

- Use `const` on every constructor you can. This is the #1 way to avoid redundant rebuilds.
- Pull children out into their own widgets. A 200-line `build` is a smell.
- Prefer `BlocSelector<B, S, T>` when the widget only cares about a slice.
- Use `buildWhen` on `BlocBuilder` when you know most state changes shouldn't redraw.
- Don't rebuild lists without stable keys — `ListView.builder` with `itemCount` is fine, but if items reorder, add `key: ValueKey(item.id)`.

## State from a bloc — three tools

- `BlocBuilder` — rebuild on every (filtered) state.
- `BlocSelector` — rebuild on a derived slice.
- `BlocListener` — side effects only. Never returns a widget.

`BlocConsumer` combines builder + listener. Use it only when both genuinely belong together (e.g., show a form error inline **and** trigger a snackbar).

## Theming

- One `ThemeData` instance per brightness, in `shared/theme/`. Don't scatter colors.
- Use `Theme.of(context).colorScheme` and `Theme.of(context).textTheme` rather than raw `Color` values in widgets.
- Material 3 (`useMaterial3: true`). `ColorScheme.fromSeed(seedColor: …)` unless design gives you full tokens.
- Spacing constants live next to the theme: `AppSpacing.lg = 24.0`. Don't inline `SizedBox(height: 16)` across the app; use `AppSpacing.md`.

## Typed routing

Routes live in `routing/`. Use `go_router_builder`:

```dart
@TypedGoRoute<SearchRoute>(path: '/search')
class SearchRoute extends GoRouteData {
  const SearchRoute();
  @override
  Widget build(BuildContext context, GoRouterState state) => const SearchPage();
}

@TypedGoRoute<ItemRoute>(path: '/items/:id')
class ItemRoute extends GoRouteData {
  const ItemRoute({required this.id});
  final String id;
  @override
  Widget build(BuildContext context, GoRouterState state) => ItemPage(id: id);
}

// call site
const SearchRoute().go(context);
const ItemRoute(id: 'abc123').go(context);
```

Redirect logic (auth guard, onboarding gate) lives on the `GoRouter.redirect` in `routing/app_router.dart` — **not** inside widgets.

## Accessibility

- Every tappable without a visible label gets a `Semantics(label: ...)` or a `Tooltip`.
- Test at default text scale and at `TextScaler.linear(1.3)`. Reserve room for reflow, not clipping.
- Color contrast AA at minimum. Use `ColorScheme.onSurface` / `onPrimary` — don't eyeball it.
- `ExcludeSemantics` around decorative images.

## Forms

- Use `formz` for field validation. A `FormzInput<String, FormErrorCode>` per field.
- The bloc state carries a `status: FormzSubmissionStatus` and a `pure: bool`.
- Disable the submit button until `status.isValidated`. Show inline errors after first blur.

## Lists

- `ListView.builder(itemCount:, itemBuilder:)` with stable `ValueKey`s when items can reorder.
- `SliverList` inside a `CustomScrollView` when the screen has headers / footers that should scroll with content.
- Pagination: bloc exposes `hasMore` and `loadingMore`. View calls `onLoadMore` when the trailing sentinel is visible.

## Images

- `Image.network` with `cacheManager: DefaultCacheManager()` via `flutter_cache_manager`.
- SVGs via `flutter_svg`. Strip them at build time when they have filters that don't render correctly.
- Never a synchronous `File(...)` load in build.

## Don'ts

- `Navigator.of(context).push(MaterialPageRoute(...))` in a codebase that uses `go_router`. Hard no.
- Business logic in a widget. If you're `await`-ing a repo call in `onPressed`, you're doing it wrong — dispatch a bloc event.
- `setState` for anything non-trivial. Cubit it.
- `GetIt.I.get<T>()` inside `build`. Use `context.read<T>()` from a provider, or inject via constructor.
- Passing a `Bloc` down through many widgets. `BlocProvider` it and read from context.
