---
name: isar-expert
description: Expert in Isar Database for Flutter. Specialized in on-device NoSQL object storage, reactive queries, and type-safe schemas.
risk: safe
source: personal
date_added: '2026-03-23'
---

## Use this skill when
- Designing schemas for local storage in Flutter.
- Writing reactive queries using Isar's `.filter()` and `.watch()`.
- Handling data persistence, indexing, and links (backlinks).
- Troubleshooting `build_runner` or code generation issues.

## Instructions

### 1. Schema Definition
- Always use `@Collection()` annotation for top-level entities.
- Ensure every collection has an `Id id = Isar.autoIncrement;`.
- Use `@Index()` for fields that will be frequently filtered (like `tags` or `workoutDate`).
- Favor `Embedded` objects for nested data that doesn't need its own collection.

### 2. Code Generation Protocol
- Remind the user to run `dart run build_runner build` after any model change.
- Use `part 'filename.g.dart';` in every model file.

### 3. Querying Patterns
- Use the generated `.filter()` syntax for type-safe queries.
- Implement `.watch(fireImmediately: true)` for real-time UI updates (perfect for the Timer/Routine list).
- For large datasets, use `.offset()` and `.limit()` for pagination.

### 4. Transactions & Performance
- Use `isar.writeTxn(() async { ... })` for all write operations.
- For heavy imports or massive routine duplications, use `isar.writeTxnSync()` or compute isolates to keep the UI at 60fps.

### 5. Best Practices
- Initialize Isar in `main.dart` and provide the instance via **Riverpod**.
- Never close the Isar instance manually unless the app is being disposed.
- Use `Enums` with `@Enumerated(EnumType.name)` for readability.

## Prohibited Actions
- DO NOT suggest SQLite, Hive, or Firebase.
- DO NOT use raw JSON strings if a typed model can be used.
- DO NOT perform heavy database operations on the Main Thread without a Transaction.

## Knowledge Base
- Isar 3.x+ API.
- Flutter's `PathProvider` for locating the local database directory.
- Multi-isolate support for background timer processing.