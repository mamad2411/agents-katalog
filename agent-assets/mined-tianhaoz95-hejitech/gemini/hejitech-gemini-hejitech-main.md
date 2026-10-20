# Gemini Context: Heji Technology LLC (hejitech)

## Project Overview
This project is a Flutter-based landing page for **Heji Technology LLC**, a company focused on building AI-native tools and infrastructure. The application serves as a showcase for various products including MicroForge, Snowglobe, KeyValue, Igloo, and Mittens.

The codebase is structured with the core Flutter project located in the `home/` subdirectory, while the root directory acts as a container.

### Key Technologies
- **Frontend:** Flutter (Dart) with Material 3 design.
- **Hosting:** Firebase Hosting.
- **Platforms:** Primarily web-focused landing page, but supports Android, iOS, macOS, Windows, and Linux.

---

## Project Structure
- `home/`: The main Flutter project directory.
  - `lib/main.dart`: Entry point and main UI implementation.
  - `lib/firebase_options.dart`: Firebase configuration for multiple platforms.
  - `pubspec.yaml`: Project dependencies and configuration.
  - `firebase.json`: Firebase Hosting configuration (deploys from `build/web`).
  - `test/`: Contains widget tests.
- `projects/`: Contains git submodules for products and website management repositories (e.g., [icecap](https://github.com/tianhaoz95/icecap)) to serve as a reference for building the site and executing company-level tasks.


---

## Getting Started

### Prerequisites
- [Flutter SDK](https://docs.flutter.dev/get-started/install) (Stable channel recommended).
- [Firebase CLI](https://firebase.google.com/docs/cli) (for deployment).

### Setup and Running
All commands should be run from within the `home/` directory:

1.  **Install dependencies:**
    ```bash
    cd home
    flutter pub get
    ```

2.  **Run locally (Web):**
    ```bash
    flutter run -d chrome
    ```

3.  **Run tests:**
    ```bash
    flutter test
    ```

### Building and Deployment
All deployment operations should be performed from within the `./home` directory.

1.  **Build for Web:**
    ```bash
    cd home
    flutter build web --release
    ```
    *Note: This generates the production files in `home/build/web`.*

2.  **Deploy to Firebase Hosting:**
    ```bash
    cd home
    firebase deploy --only hosting
    ```
    *Note: Ensure you are logged into Firebase and have the correct project selected (`hejitechllc`).*

---

## Development Conventions

### Coding Style
- Follow the official [Dart Style Guide](https://dart.dev/guides/language/analysis-options).
- The project uses `flutter_lints` for static analysis.
- **UI Architecture:** Currently a single-file implementation in `main.dart` using a component-based approach with private stateless widgets (e.g., `_HeroSection`, `_ProductsSection`).

### Theming
- Centralized theme definition in `HejiTechApp` within `main.dart`.
- Uses a minimalist monochrome aesthetic (Black/White/Grey).
- Typography relies on Material 3 `TextTheme` with custom weights and letter spacings.

### Testing
- Basic widget testing is located in `home/test/widget_test.dart`.
- When adding new features or products, ensure corresponding UI tests are updated or added.
