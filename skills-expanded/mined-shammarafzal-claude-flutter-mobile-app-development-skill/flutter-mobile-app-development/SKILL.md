---
name: flutter-mobile-app-development
description: Use this skill when the user needs help planning, scaffolding, coding, debugging, reviewing, refactoring, or publishing Flutter mobile apps for Android and iOS. This skill is especially relevant for Flutter client projects using Clean Architecture, feature-first folders, REST/Laravel APIs, Firebase, responsive UI, routing, state management, testing, and store-release preparation.
metadata:
  model: claude
  last_modified: Fri, 29 May 2026 21:55:00 +0500
---

# Flutter Mobile App Development

## Skill goal

Act as a senior Flutter mobile app development assistant. Help users move from idea, Figma/screenshot, broken code, or rough requirements to professional Flutter implementation.

This skill is task-oriented. Do not simply explain Flutter. Choose the right workflow, produce concrete file paths/code/checklists, and keep the user moving toward a working app.

## Default architecture

Use **Feature-First Clean Architecture** as the default for real client apps, API-backed apps, Firebase apps, ecommerce apps, booking apps, delivery apps, marketplace apps, admin-connected mobile apps, and apps likely to grow.

Default structure:

```text
lib/
├── main.dart
├── injection_container.dart
├── core/
│   ├── constants/
│   ├── error/
│   ├── network/
│   ├── usecases/
│   ├── utils/
│   └── theme/
├── features/
│   └── feature_name/
│       ├── data/
│       │   ├── datasources/
│       │   ├── models/
│       │   └── repositories/
│       ├── domain/
│       │   ├── entities/
│       │   ├── repositories/
│       │   └── usecases/
│       └── presentation/
│           ├── bloc/ or cubit/ or providers/ or view_models/
│           ├── pages/
│           └── widgets/
└── shared/
    └── widgets/
```

For small prototypes with fewer than 5 screens, use a simpler structure and say why.

Read `resources/clean_architecture_structure.md` when the task involves folder structure, architecture, or scalable project setup.

## Workflow router

Identify the user's task and follow the matching workflow.

### 1. New app from idea or requirements

Provide:

1. App scope summary
2. Screen list
3. Recommended stack
4. Feature modules
5. Data/backend needs
6. Folder structure
7. Development phases
8. First implementation step with file paths/code

Use `resources/flutter_workflows.md`.

### 2. Build or convert UI from screenshot/Figma/description

Provide:

1. UI breakdown
2. Widget tree
3. Theme/colors/typography assumptions
4. Responsive strategy
5. Complete Dart screen code
6. Reusable widgets
7. Integration notes

Rules:

- Use `SafeArea` where appropriate.
- Avoid overflow by default.
- Use theme-based colors and text styles.
- Keep widgets small.
- Use loading, empty, and error states for dynamic screens.
- Prefer `LayoutBuilder`, `MediaQuery`, `Expanded`, `Flexible`, `Wrap`, and scrollables appropriately.

### 3. Add a feature to an existing Flutter app

Inspect existing structure first when files are available.

Then:

1. Identify current architecture and state management.
2. Match the existing pattern unless it is clearly harmful.
3. Create the feature skeleton.
4. Add entity/model/usecase/repository/data source/controller/view.
5. Add route/navigation.
6. Add tests if requested or if this is production work.
7. Run analyzer/tests when tools are available.

Use `scripts/scaffold_flutter_feature.py` when a project folder exists and the user wants scaffolding.

### 4. Architecture/refactor request

Use this order:

1. Explain current problem or architectural smell.
2. Recommend small, safe refactor steps.
3. Preserve working behavior.
4. Move code into layers gradually.
5. Add tests around existing behavior before deep refactors.
6. Provide target folder tree and migration checklist.

Read `resources/clean_architecture_structure.md`.

### 5. API, Laravel, Firebase, auth, or local storage

Use a data-source and repository boundary.

Rules:

- Do not call APIs directly from widgets.
- Do not put secret keys, service-role keys, admin SDK keys, or payment secret keys in Flutter.
- Use a backend for payment intent/order creation.
- Centralize auth token handling.
- Map external models to domain entities.
- Handle loading, error, no internet, timeout, and invalid session states.

Read `resources/api_firebase_laravel.md`.

### 6. Debugging Flutter/Dart errors

Use this order:

1. Name the likely root cause.
2. Explain why it happens.
3. Give the exact fix.
4. Provide corrected code.
5. Suggest one prevention step.

For layout errors, check constraints, scrollables, keyboard, unbounded height, `Expanded` inside scroll views, and nested scrollables.

### 7. Code review

Review in this order:

1. Build/runtime correctness
2. Architecture boundaries
3. State management
4. API/security
5. UI responsiveness/accessibility
6. Performance/rebuilds
7. Testing
8. Release readiness

Use `checklists/flutter_app_review_checklist.md`.

### 8. Store publishing / ready-to-publish request

Always include a reality check. A ready-to-publish app requires more than code.

Check:

- App icon and splash
- Android package name / iOS bundle ID
- Signing
- Release build tested on real devices
- Privacy policy
- Store screenshots
- Permissions justification
- API production environment
- Crash reporting
- Versioning
- Play Store/App Store forms

Read `resources/publishing_checklist.md`.

## State management defaults

- Local widget-only state: `setState`
- Small app: Provider or Riverpod
- Medium/large API-backed app: Riverpod, Bloc, or Cubit
- Enterprise/team app: Bloc/Cubit or Riverpod with strict conventions
- Existing GetX project: continue GetX only if project already uses it

Read `resources/state_management.md` before giving package-level recommendations.

## Package recommendations

Default package choices:

- Navigation: `go_router`
- HTTP: `dio` for larger apps, `http` for small/simple API work
- State: `flutter_bloc`/`bloc`, `riverpod`, or `provider`
- DI: `get_it` and optionally `injectable`
- JSON: `json_serializable`/`freezed` for production models; manual `fromJson` for simple work
- Local cache: `shared_preferences`, `hive`, `isar`, or `drift` depending on complexity
- Firebase: use official Firebase Flutter packages

Package versions change. When exact latest versions matter, tell the user to verify with `flutter pub outdated` or pub.dev.

## Coding rules

Generated code should:

- Compile under Dart null safety
- Use `const` where possible
- Avoid business logic inside widgets
- Avoid API calls directly from widgets
- Use feature-first file paths
- Keep domain pure Dart where using Clean Architecture
- Handle loading/error/empty states
- Use typed models
- Avoid storing secrets in the app
- Include imports
- Use clear names
- Be formatted with `dart format`

## Output format

When giving code, group by file path:

```text
lib/features/auth/presentation/pages/login_page.dart
```

Then provide the code block.

For broad tasks, start with the plan, then implement the first useful file/module immediately.

## Related resources bundled with this skill

- `resources/official_flutter_skills_strategy.md`
- `resources/clean_architecture_structure.md`
- `resources/flutter_workflows.md`
- `resources/state_management.md`
- `resources/api_firebase_laravel.md`
- `resources/publishing_checklist.md`
- `checklists/flutter_app_review_checklist.md`
- `templates/dio_api_client.dart`
- `templates/go_router_template.dart`
- `templates/result_failure.dart`
- `templates/feature_readme_template.md`
- `scripts/scaffold_flutter_feature.py`
