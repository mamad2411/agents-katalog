---
name: flutter-skills
description: Flutter/Dart patterns, widgets, and best practices for cross-platform mobile
category: stacks/mobile/flutter
applies_to: flutter
allowed-tools: Read, Write, Glob, Grep, Bash
user-invocable: true
context: inject
---

# Flutter Skills

Google's UI toolkit for building natively compiled applications.

## Sub-Skills

### Architecture
- [project-structure.md](architecture/project-structure.md) - Project organization
- [clean-architecture.md](architecture/clean-architecture.md) - Clean architecture
- [bloc-pattern.md](architecture/bloc-pattern.md) - BLoC pattern
- [riverpod.md](architecture/riverpod.md) - Riverpod patterns

### State Management
- [provider.md](state/provider.md) - Provider patterns
- [bloc.md](state/bloc.md) - BLoC patterns
- [riverpod.md](state/riverpod.md) - Riverpod patterns
- [getx.md](state/getx.md) - GetX patterns

### Widgets
- [stateless.md](widgets/stateless.md) - Stateless widgets
- [stateful.md](widgets/stateful.md) - Stateful widgets
- [inherited.md](widgets/inherited.md) - InheritedWidget
- [custom-paint.md](widgets/custom-paint.md) - CustomPaint

### Navigation
- [navigator.md](navigation/navigator.md) - Navigator 2.0
- [go-router.md](navigation/go-router.md) - GoRouter patterns
- [auto-route.md](navigation/auto-route.md) - AutoRoute

### Data
- [dio.md](data/dio.md) - Dio HTTP client
- [retrofit.md](data/retrofit.md) - Retrofit patterns
- [hive.md](data/hive.md) - Hive local storage
- [sqflite.md](data/sqflite.md) - SQLite patterns

### Performance
- [widget-rebuilds.md](performance/widget-rebuilds.md) - Minimize rebuilds
- [lazy-loading.md](performance/lazy-loading.md) - Lazy loading
- [images.md](performance/images.md) - Image optimization

### Testing
- [unit-testing.md](testing/unit-testing.md) - Unit tests
- [widget-testing.md](testing/widget-testing.md) - Widget tests
- [integration.md](testing/integration.md) - Integration tests
- [mocking.md](testing/mocking.md) - Mockito patterns

## Detection
Auto-detected when project contains:
- `pubspec.yaml` file
- `lib/main.dart` file
- `flutter` package
