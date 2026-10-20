---
description: "BLoC and Cubit patterns for Family-Link"
globs: lib/features/**/*.dart
alwaysApply: false
---

# State management (Bloc / Cubit)

- Presentation state under **`presentation/bloc/`** or **`presentation/cubit/`**.
- Separate **`*_event.dart`** / **`*_state.dart`** files for **`Bloc<Event, State>`** features.
- Use **`flutter_bloc`**, **`BlocBuilder`**, **`BlocListener`**, **`context.read`** / **`context.watch`**.
- **`bloc_test`** + **`mocktail`** in **`test/features/...`** mirroring **`lib/features/...`**.

See **`tech_readme_files/1_getting_started/PROJECT_ARCHITECTURE.md`**.
