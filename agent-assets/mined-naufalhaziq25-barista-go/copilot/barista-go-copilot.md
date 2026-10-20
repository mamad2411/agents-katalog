# Copilot instructions — learning_structure (Barista GO)

Brief: A small Flutter app using GetX for state/routing and Firebase (Auth + Firestore) as the backend. Use these notes to make productive, low-risk changes quickly.

## Big picture
- Flutter app (mobile & desktop/web targets present). Entry: `lib/main.dart`.
- State + routing by GetX: pages & routes in `lib/utils/routes.dart`, controllers created with `Get.put(...)` (see `main.dart`).
- Backend: Firebase Auth + Firestore. Project configured via `lib/firebase_options.dart` and `android/app/google-services.json`.
- Structure: feature-first layout under `lib/features/` and plain service layer under `lib/services/` (services map to backend Firestore collections).

## Key files & conventions
- Add pages under `lib/features/<admin|customer|shared>/...` and controllers alongside them (naming: `<feature>_controller.dart`).
- Backend logic belongs in `lib/services/*` (e.g. `lib/services/customer/cart_service.dart`) — services talk to Firebase and return models from `lib/features/shared/model/`.
- Routing: add a route constant in `lib/utils/routes.dart` and a corresponding `GetPage` entry in `Routes.pages`.
- Theme & small app-wide state: `lib/utils/theme_controller.dart` uses `shared_preferences` for persistence.
- Firestore patterns: many collections are user-scoped. Example: cart items live under `cart/{userId}/coffee/{docId}` (see `CartService`).

## Developer workflows & commands
- Setup & deps: `flutter pub get`.
- Run app: `flutter run -d <device>` (Android/iOS/web/windows supported depending on platform and tooling).
- Tests: `flutter test` (there is at least `test/widget_test.dart`).
- Static analysis & formatting: `flutter analyze` and `dart format .` / `flutter format .`.
- Firebase: project config exists (`firebase.json` + `lib/firebase_options.dart`). If you add or change Firebase apps, update `android/app/google-services.json` (Android) and iOS equivalents.

## Patterns & examples (do this, not that)
- Add a route: add a constant to `Routes` and a `GetPage` entry. Example: `static const profile = '/profile';` + `GetPage(name: profile, page: () => const ProfilePage())`.
- Add a new backend operation: create a `Service` under `lib/services/<domain>/...` that uses `FirebaseFirestore.instance` and follows existing error/logging patterns (see `CartService`).
- Use `Get.put(Controller())` for controllers that should be globally available (see `main.dart`). For page-scoped controllers prefer bindings or `Get.lazyPut`.
- Persist simple prefs with `ThemeController` pattern (uses `SharedPreferences.getInstance()` and a private key).

## Integration points & gotchas
- Auth-dependent services check `FirebaseAuth.instance.currentUser` — expect `null` in unauthenticated tests; test by faking or signing in a test user.
- Firestore queries assume certain document shapes (models live under `lib/features/shared/model/`); changes to models need service + UI updates.
- SharedPreferences can fail on web; controllers in code already handle exceptions — keep the same defensive style.

## PR guidance
- Small incremental PRs with one feature or service change per PR.
- Include unit tests where logic is non-trivial (service-level conversions, price calculations). Widget tests are encouraged for page-level UI.

## What to ask the maintainers if unsure
- Where to get Firebase test credentials and whether the test environment allows writing to Firestore.
- Which devices/platforms are actively supported (if adding platform-specific code).

---
If you'd like, I can expand any section (e.g., add sample tests, or a short checklist for adding a new feature). What should I clarify or add? ✨