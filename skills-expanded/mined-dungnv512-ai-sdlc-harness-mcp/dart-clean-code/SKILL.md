---
name: dart-clean-code
description: Authoritative clean-code standard for a Dart + Flutter codebase. Covers Effective Dart, very_good_analysis lint deltas, Clean Architecture, BLoC, Result<F,T>, Freezed 3, M3 + design tokens, performance, a11y, i18n, testing, security. MANDATORY TRIGGERS - "dart", "flutter", "effective dart", "very_good_analysis", "clean architecture", "freezed", "bloc", "result", "linter", "code review", "refactor", "style guide".
allowed-tools: Read, Grep, Glob, Edit
model: sonnet
---

# Dart + Flutter Clean Code — Engineering Standard

> Sources: [Effective Dart](https://dart.dev/effective-dart) (official),
> [`very_good_analysis` 10.x](https://pub.dev/packages/very_good_analysis),
> [bloclibrary.dev/architecture](https://bloclibrary.dev/architecture),
> [`freezed` 3.x](https://pub.dev/packages/freezed),
> [`slang` 4.7](https://pub.dev/packages/slang) (or your i18n package of
> choice),
> [Flutter perf best-practices](https://docs.flutter.dev/perf/best-practices),
> [OWASP MASVS 2.x](https://mas.owasp.org/MASVS/),
> [Reso Coder Flutter Clean Architecture + TDD](https://resocoder.com/flutter-clean-architecture-tdd).
> Last refreshed 2026-06-11.
>
> **Supersedes** ad-hoc style rules scattered across older docs or
> individual skills. If anything older contradicts this file, this file
> wins; raise a PR to remove the duplicate.
>
> Treat the versions below as a baseline, not a mandate — pin to
> whatever your `pubspec.yaml` actually declares: Dart 3.10+,
> `freezed ^3.2.3`, `very_good_analysis ^7.0.0`, `slang ^4.7.0`,
> `flutter_bloc ^9.1.1`, `dio ^5.4.3`, `retrofit ^4.9`,
> `injectable ^2.4.3`. Review `pubspec.yaml` before bumping anything.

## 1. Language & style fundamentals

The official formatter output **is** the style — there is no second
opinion ([style](https://dart.dev/effective-dart/style#do-format-your-code-using-dart-format)).

Rules that bite in PRs:

- Files `snake_case`, types `UpperCamelCase`, members `lowerCamelCase`,
  constants `lowerCamelCase` (NOT `SCREAMING_CAPS`) per
  [Identifiers](https://dart.dev/effective-dart/style#prefer-using-lowercamelcase-for-constant-names).
- Acronyms ≥3 letters capitalize like words (`HttpRequest`,
  `UriParser`); two-letter acronyms stay all-caps (`UI`, `ID`).
- Imports: `dart:` block, blank line, `package:` block, blank line,
  relative block. Sort alphabetically inside each block.
  `directives_ordering` enforces it.
- Line width **80 cols** — fix by extracting a local, not by widening
  the line.
- Use the wildcard `_` for unused callback params (Dart ≥3.7 makes
  them non-binding). Multiple `_` are legal: `.onError((_, _) => …)`.

Anti-patterns: `const K_DEFAULT_TIMEOUT`, `library my_lib;` (drop the
name; bare `library;` is for `@TestOn` annotations only), relative
imports across feature boundaries (banned by `always_use_package_imports`
+ your project's import-boundary rule).

## 2. very_good_analysis — what differs from `flutter_lints`

`flutter_lints` ships ~30 rules; `very_good_analysis` ships ~210.
What you'll feel:

| Rule (VGA on, flutter_lints off) | Why it bites |
| --- | --- |
| `strict-casts: true`, `strict-inference: true`, `strict-raw-types: true` | No silent `dynamic`, no implicit downcasts. |
| `public_member_api_docs` | Forces dartdoc on public APIs. App-side `// ignore_for_file:` is acceptable; leave on in shared/core packages. |
| `always_use_package_imports` | Kills relative imports that cross feature boundaries. |
| `prefer_single_quotes` | Consistent string style. |
| `require_trailing_commas` | Lets `dart format` produce vertical, diff-friendly arg lists. |
| `unawaited_futures` | Recommend escalating this to `error` in `analysis_options.yaml`. |
| `lines_longer_than_80_chars` | Enforces the 80-col rule. |

**Suppressions.** Per-line `// ignore: <rule_name>` is acceptable
**only with a one-line justification on the same line**
(`// ignore: avoid_dynamic_calls — third-party SDK returns dynamic JSON`).
Never `// ignore_for_file:` an entire production file.

CI can grep the diff for unjustified ignores:

```bash
grep -RnE '// *ignore:[^/]*$' lib/ && exit 1
```

## 3. Project structure — Clean Architecture

Domain at the center, depends on nothing Flutter. Data implements
domain. Presentation depends on domain.

**The compile-time check**:
`grep -r "package:flutter\|package:dio" lib/features/*/domain/`
returns empty. Audit this in code review.

```
lib/
  core/         auth, cache, di, lifecycle, navigation,
                network, result, storage, utils
  config/       flavors, theme switches, routes
  design_system/ components, layout, theme, tokens
  features/<feature>/
    data/       dtos, datasources (retrofit), repositories
    domain/     entities (freezed), repositories (abstract),
                usecases, failures
    presentation/ bloc, pages, widgets
  i18n/         translation JSON files + generated translations
  shared/       cross-feature widgets, common types
```

Anti-patterns: a `BlocProvider` consuming a `RemoteDataSource`
directly; a domain entity with `Diagnosticable`/`Flutter` imports;
`data → presentation` imports.

## 4. State management — flutter_bloc canonical patterns

Per [bloclibrary.dev/architecture](https://bloclibrary.dev/architecture):
- **Bloc-to-Bloc communication is forbidden.** Route shared state
  through repository streams or coordinate in presentation with
  `BlocListener`.
- Prefer one Bloc per screen-feature; use Cubits for trivial toggles.

**Event semantics.** Events are past-tense facts
(`LoginSubmitted`, `FeedRefreshed`), never imperatives.

**State.** Freezed sealed unions:

```dart
@freezed
sealed class LoginState with _$LoginState {
  const factory LoginState.initial() = LoginInitial;
  const factory LoginState.submitting() = LoginSubmitting;
  const factory LoginState.success(UserEntity user) = LoginSuccess;
  const factory LoginState.failure(AuthFailure failure) = LoginFailure;
}
```

**Bloc body.** Exhaustive `switch` over events, `bloc_concurrency`
transformers, no hand-rolled `if (state is Loading) return;`:

```dart
class LoginBloc extends Bloc<LoginEvent, LoginState> {
  LoginBloc(this._login) : super(const LoginState.initial()) {
    on<LoginSubmitted>(_onSubmitted, transformer: droppable());
  }
  final Login _login;

  Future<void> _onSubmitted(
    LoginSubmitted event,
    Emitter<LoginState> emit,
  ) async {
    emit(const LoginState.submitting());
    final result = await _login(email: event.email, password: event.password);
    emit(switch (result) {
      Ok(:final value) => LoginState.success(value),
      Err(:final failure) => LoginState.failure(failure),
    });
  }
}
```

**Build side.** `BlocSelector` beats `BlocBuilder` when you watch one
field. `BlocListener` for navigation/snackbars. `BlocConsumer` only
when you need both.

Anti-patterns: one Bloc listening to another's `stream`; public
methods on a Bloc (`avoid_public_bloc_methods`); `setState` inside a
`BlocBuilder.builder`.

When NOT to use Bloc: pure UI toggles (chip selected,
sheet expanded/collapsed) — `ValueListenableBuilder` over a
`ValueNotifier` is shorter and clearer.

## 5. Error handling — sealed `Result<F, T>`

Exceptions are for **bugs** (null deref, range error). Domain failures
(auth expired, network timeout, validation) are **expected**, so they
appear in the return type.

The contract:
- `lib/core/result/result.dart` exposes
  `sealed class Result<F extends Failure, T>` with subclasses `Ok` /
  `Err`.
- `lib/core/result/failure.dart` defines `abstract base class Failure`
  + concrete `NetworkFailure`, `AuthFailure`, `ValidationFailure`,
  `ServerFailure`, `UnknownFailure`.
- Every domain `usecase` and `repository` returns
  `Future<Result<F, T>>`.

Use the pattern destructure in new code:

```dart
final next = switch (result) {
  Ok(:final value) => Routes.feed,
  Err(failure: AuthFailure(code: 'AUTH_LOCKED')) => Routes.support,
  Err(:final failure) => Routes.error.copyWith(extra: failure),
};
```

UI never sees raw `Failure.message` — map via
`lib/core/result/failure_messages.dart`.

Anti-patterns: `throw AuthException()` from a domain usecase;
`result.value!`; new code introducing `dartz.Either<…>` where the
project has standardized on sealed `Result`.

## 6. Data modelling — Freezed 3

**Freezed 3.0 (April 2025) changes the syntax in load-bearing ways:**

- Classes with factory constructors MUST be marked `abstract` (single
  class) or `sealed` (union).
- `map`/`when`/`maybeMap`/`maybeWhen` are removed. Use Dart's
  pattern-matching `switch`.
- `@With` / `@Implements` use generic syntax: `@With<MyMixin>()`.
- `List`/`Map`/`Set` fields are exposed as `Unmodifiable…View` — don't
  `.add()`; build a new list and `copyWith`.

Single class:

```dart
@freezed
abstract class UserEntity with _$UserEntity {
  const factory UserEntity({
    required String id,
    required String handle,
    String? displayName,
    @Default(0) int followers,
  }) = _UserEntity;

  factory UserEntity.fromJson(Map<String, Object?> json) =>
      _$UserEntityFromJson(json);
}
```

Sealed union (BLoC states, domain events):

```dart
@freezed
sealed class FeedState with _$FeedState {
  const factory FeedState.initial() = FeedInitial;
  const factory FeedState.loading() = FeedLoading;
  const factory FeedState.loaded(List<Post> posts, {bool hasMore}) = FeedLoaded;
  const factory FeedState.error(Failure failure) = FeedError;
}

Widget _build(FeedState s) => switch (s) {
  FeedInitial() || FeedLoading() => const _Skeleton(),
  FeedLoaded(:final posts, hasMore: true) => _FeedList(posts, infinite: true),
  FeedLoaded(:final posts) => _FeedList(posts, infinite: false),
  FeedError(:final failure) => _ErrorPane(failure),
};
```

**Equatable vs Freezed.** Don't `with EquatableMixin` on top of a
Freezed class — it's redundant. Equatable still earns its keep on
plain BLoC events that don't need codegen.

**Codegen rules.** Never hand-edit `*.g.dart` or `*.freezed.dart`
(block this with a pre-commit hook if you can). Re-run
`dart run build_runner build --delete-conflicting-outputs` after any
`@freezed` / `@JsonSerializable` / `@RestApi` / drift / injectable
change.

## 7. Routing — go_router

Recommended: `go_router`. Keep routes in `lib/config/routes/`.

- Use `StatefulShellRoute.indexedStack` for the bottom-nav shell.
- Route names in a `RoutePath` class; never hard-code paths.
- `redirect` is the only correct place to gate authenticated routes.
  Mutating navigation from a `BlocListener` race-conditions with deep
  links.

```dart
final routerProvider = GoRouter(
  initialLocation: RoutePath.feed,
  redirect: (ctx, state) {
    final auth = ctx.read<AuthBloc>().state;
    final isPublic = _publicPaths.contains(state.matchedLocation);
    return switch ((auth, isPublic)) {
      (AuthAuthenticated(), _) => null,
      (_, true) => null,
      _ => RoutePath.login,
    };
  },
  routes: [...],
);
```

Anti-patterns: `Navigator.of(context).push(MaterialPageRoute(...))`
for app-level navigation; passing complex objects via `state.extra`
on deep-linkable routes (use route params + repository fetch).

## 8. UI — Material 3, design tokens, ThemeExtension

Material 3 is default in Flutter 3.16+. Build from a brand seed:

```dart
ThemeData buildLightTheme() {
  final scheme = ColorScheme.fromSeed(seedColor: AppColors.brand);
  return ThemeData(
    useMaterial3: true,
    colorScheme: scheme,
    textTheme: AppTypography.textTheme,
    extensions: [SemanticColors.light, AppMotion.standard],
    visualDensity: VisualDensity.adaptivePlatformDensity,
  );
}
```

Keep design tokens in `lib/design_system/tokens/`:
`colors.dart` (palette + seed outputs), `spacing.dart`
(`AppSpacing.xs/sm/md/lg/xl`), `typography.dart` (your app's chosen
font family and line-heights), `borders.dart` (radii — pick one scale
and stick to it project-wide), `motion.dart`, `shadows.dart`.

**Layout primitives — always reach for the shared ones** (define
these once per project and reuse everywhere):
- A `SafeAreaScaffold` wrapper instead of raw `Scaffold`.
- An `AppGutter` widget for screen-edge padding.
- `AppBreakpoints` / `WindowSize` helpers for responsive forks.
- A `KeyboardDismissible` wrapper for form pages.
- An `AppHaptics` helper limited to a small, deliberate set of
  feedback events.

**Const widgets are free performance.** `const SizedBox(height: 8)`
allocates zero objects per build.

Anti-patterns: hard-coded hex colors in widget files;
`MediaQuery.of(context).size.width` to branch layout (use
`AppBreakpoints`); `Theme.of(context).colorScheme.primary` inside a
tight rebuild — extract to a local at top of `build`.

## 9. Performance — frame budgets, const, RepaintBoundary

60fps = 16.7ms/frame; 120fps = 8.3ms. Set an explicit p95 frame-time
budget for your target device tier (e.g. ≤16ms on a mid-tier Android
device) and hold to it.

- `const` constructors aggressively. One non-const ancestor kills
  const for the subtree.
- `ListView.builder` for any list >~10 items. Never
  `ListView(children: [...].map(...).toList())`.
- Sliver scrolls: `CustomScrollView` + `SliverList`/`SliverGrid` over
  `Column { Header, Expanded { ListView } }`.
- `RepaintBoundary` around subtrees that animate independently.
- Avoid `Opacity`, `Clip…` in hot paths — `Opacity` triggers an
  offscreen buffer.
- `AnimatedBuilder` over rebuilding parent for animations.
- **Impeller is the default on iOS (3.13+) and Android (3.27+).**
  Test on physical devices, not simulators.
- `MediaQuery.sizeOf(context)`, `paddingOf(context)`,
  `viewInsetsOf(context)` (3.10+) — scoped to the dependency, vs
  `MediaQuery.of(context)` which rebuilds on every keyboard/rotation.

Image cache tuning at startup:

```dart
void main() {
  WidgetsFlutterBinding.ensureInitialized();
  PaintingBinding.instance.imageCache
    ..maximumSize = 200
    ..maximumSizeBytes = 50 << 20; // 50 MB
  runApp(const MyApp());
}
```

Combine with `Image.network(url, cacheWidth: 360)` (≈ DPR × layout
width).

JSON > 50 KB or CPU work > 8 ms → `compute()` or `Isolate.run` (3.13+).

Anti-patterns: `setState` in a parent owning a `ListView.builder` with
thousands of items; `Future.delayed(Duration.zero, () => setState…)`
masking a build-cycle bug.

## 10. Accessibility — WCAG 2.1 AA

Test with your app's chosen font at `textScaler: 1.3` and with any
locale that has notably taller/wider glyphs or diacritics than English.

- Every interactive widget without visible text → `Semantics(label:…)`
  or `tooltip:`. Icons as buttons → `IconButton(tooltip:…)`.
- **Color is never the only signal.** Status/trend indicators should
  pair color with a symbol or text label, not rely on hue alone —
  roughly 5% of males have red-green color blindness.
- Hit-targets ≥48dp. Wrap small icons in
  `IconButton(iconSize: 20, constraints: BoxConstraints(minWidth: 48, minHeight: 48))`.
- Contrast vs `onSurface` / `onPrimary`: ≥4.5:1 text, ≥3:1 UI.
- Form focus order: `FocusTraversalGroup`, every focusable gets a
  `focusNode`, `autofocus: true` on first field.
- `MediaQuery.textScalerOf(context)` (3.16+) not deprecated
  `textScaleFactor`. Clamp:

```dart
MediaQuery(
  data: MediaQuery.of(context).copyWith(
    textScaler: MediaQuery.textScalerOf(context).clamp(maxScaleFactor: 1.5),
  ),
  child: child,
);
```

## 11. i18n — typed translations, ICU plurals, locale parity

Use a typed-translation generator (e.g. `slang`) so UI calls
`t.feed.empty` rather than raw string lookups. Pick one default
locale and one or more fallback locales explicit to your product.

- JSON keys `lowerCamelCase`, grouped by feature: `feed.refreshing`,
  `auth.login.cta`.
- Plurals: ICU `"posts(one) {1 post}(other) {{count} posts}"`. Some
  locales have no plural form per CLDR; ICU still works — put the same
  string in `one` and `other` for those locales.
- Currency/number formatting: keep `intl`'s `NumberFormat`/`DateFormat`
  in scope, or a locale-specific formatter if your currency needs
  custom grouping.
- Parity gate: a script (e.g. `slang analyze`) should fail CI if any
  key exists in one locale file and not another.

```dart
class FeedEmpty extends StatelessWidget {
  const FeedEmpty({super.key});
  @override
  Widget build(BuildContext context) {
    final t = Translations.of(context);
    return Center(child: Text(t.feed.empty));
  }
}
```

Anti-patterns: hard-coded user-facing strings in widget files; string
concatenation across translated fragments (word order varies across
languages). Use ICU placeholders.

## 12. Testing — unit / widget / golden / integration

Set an explicit coverage gate (a common baseline: 80% `lib/`, 90%
`domain/`). Mirror `lib/` in `test/` exactly.

- **Unit (`mocktail`)** for usecases, mappers, validators. No
  `flutter_test` import in `domain/` tests — pure Dart.
- **Bloc (`bloc_test`)** — every Bloc has a `*_test.dart` per event:

```dart
blocTest<LoginBloc, LoginState>(
  'emits [submitting, success] on Ok',
  build: () => LoginBloc(login),
  setUp: () => when(() => login(
      email: any(named: 'email'),
      password: any(named: 'password')))
    .thenAnswer((_) async => Ok(user)),
  act: (b) => b.add(const LoginSubmitted(email: 'a', password: 'b')),
  expect: () => [
    const LoginState.submitting(),
    LoginState.success(user),
  ],
);
```

- **Widget** — wrap in a helper `pumpApp(child)` that provides
  `Theme`, `Translations`, mocked `Bloc`. Find by semantic label
  (locale switches break `find.text`).
- **Golden (`alchemist`)** — for design-system components in a
  component catalogue (e.g. Widgetbook), per (light/dark) ×
  (breakpoint). Regenerate on a single, consistent CI runner OS —
  cross-OS font rendering drift is real.
- **Integration (`integration_test`)** — happy paths only; run nightly
  on a device farm (Firebase Test Lab or similar).

Anti-patterns: `await Future.delayed(...)` instead of
`pumpAndSettle()`; mocking the Bloc instead of providing one with
mocked usecases; sharing test state via top-level `late` variables.

## 13. Security — MASVS L2

Target [OWASP MASVS L2](https://mas.owasp.org/MASVS/) for any app that
handles auth tokens, PII, or financial data. Driving controls:
[MASVS-STORAGE](https://mas.owasp.org/MASVS/05-MASVS-STORAGE/) and
[MASVS-NETWORK](https://mas.owasp.org/MASVS/08-MASVS-NETWORK/).

**Storage.**
- Tokens, refresh tokens, biometric keys: `flutter_secure_storage`
  only. Android: `EncryptedSharedPreferences`. iOS: Keychain with
  `accessibility: KeychainAccessibility.first_unlock` (NOT `always`).
- Tokens **never** in `shared_preferences`, Hive plaintext box, drift
  row, logs, crash-reporter breadcrumbs, or analytics events.
- Hive boxes with user data: encrypt with a key stored in
  `secure_storage`.
- Disable screenshot/recents preview on sensitive pages: `FLAG_SECURE`
  on Android, screenshot blur on iOS (a small `ScreenGuard` helper in
  `core/security/`).

**Network.**
- All HTTP through a single shared `Dio` instance in
  `lib/core/network/` with auth + refresh interceptors. No ad-hoc
  `http` or fresh `Dio()`.
- TLS pinning to the production leaf cert SHA-256 once your API is
  stable enough to pin against.
- Reject self-signed certs in release:
  `badCertificateCallback: (_, _, _) => false`.

**Logging.** Use a structured `logger` with redaction. PII (email,
phone, financial data) never above `debug`. Stack traces sent to a
crash reporter should be sanitized via a `beforeSend`-style hook.

Anti-patterns: `print(user.email)` (`avoid_print` is on);
`dio.options.headers['Authorization'] = …` set globally (token leaks
across users on logout — use interceptor); storing JWT in
`shared_preferences` "just for a sprint".

## 14. Tooling — build_runner, lints, CI gates

Local loop:

```bash
dart pub get
dart run build_runner build --delete-conflicting-outputs
dart run slang   # or your i18n codegen command
dart format --set-exit-if-changed lib test
dart analyze --fatal-infos --fatal-warnings
flutter test --coverage
flutter test --update-goldens   # only when intentional
```

Wrap this in a `scripts/bootstrap.sh` for new contributors.

Recommended CI gates:
1. `dart format --set-exit-if-changed`
2. `flutter analyze` — zero warnings.
3. `flutter test --coverage` — enforce your coverage gate.
4. Goldens on a single, pinned OS runner.
5. i18n locale-parity check.
6. Dependency vulnerability scan (e.g. `osv-scanner`) on
   `pubspec.lock`.
7. `grep -RnE '// *ignore:[^/]*$' lib/` to catch unjustified lint
   suppressions.

`analysis_options.yaml` essentials:

```yaml
include: package:very_good_analysis/analysis_options.7.0.0.yaml
analyzer:
  language:
    strict-casts: true
    strict-inference: true
    strict-raw-types: true
  errors:
    unawaited_futures: error
    cancel_subscriptions: error
    invalid_annotation_target: ignore
  exclude:
    - "**/*.g.dart"
    - "**/*.freezed.dart"
    - "lib/i18n/i18n.g.dart"
```

Anti-patterns: editing `pubspec.lock` by hand; disabling `analyze` in
CI "temporarily"; bumping Freezed/i18n-generator major versions
without reading the migration guide.

## Quick-reference checklists

### Pre-commit
- [ ] `dart format` clean.
- [ ] `dart analyze` zero warnings.
- [ ] New strings added to every locale's translation file.
- [ ] `build_runner` re-run if `@freezed` / `@JsonSerializable` /
      `@RestApi` / `@DriftDatabase` / `@injectable` touched.
- [ ] Tests pass; coverage didn't drop.
- [ ] No `print`, no `Either`, no `dynamic`, no hard-coded hex.

### Code review
- [ ] Domain imports nothing Flutter.
- [ ] BLoC: events past-tense, state sealed, transformer chosen.
- [ ] Every async failure path returns a typed `Result` — no `throw`
      from usecases.
- [ ] UI strings via `t.…`, never inline.
- [ ] `const` propagated through static subtrees.
- [ ] `BlocSelector` used instead of `BlocBuilder` when watching one
      field.
- [ ] Public APIs documented; widget classes have plain
      `@override Widget build`.

### Performance
- [ ] `ListView.builder` for any list, `RepaintBoundary` where it earns
      its keep.
- [ ] `Image.network` has `cacheWidth`; `imageCache` tuned at startup.
- [ ] No `Opacity` / `Clip…` in hot paths.
- [ ] `MediaQuery.sizeOf` / `paddingOf` instead of `MediaQuery.of`.
- [ ] Profile build on representative low/mid-tier devices before
      declaring "feels fine."

### Security
- [ ] Tokens via `flutter_secure_storage` only.
- [ ] All HTTP through the shared `core/network/` Dio singleton.
- [ ] No PII above `debug`. Crash reporter redacts sensitive fields.
- [ ] Sensitive pages set `FLAG_SECURE` / iOS screenshot blur.
- [ ] If the diff touches auth/storage/network/deep links, run a
      dedicated security review.
