---
description: Rules for Dependency Injection with GetIt
globs: lib/*/application/controllers/**/*.dart
alwaysApply: false
---

# Dependency Injection

- Use GetIt for service registration.
- Register all dependencies in the feature controller file or if the dependecy is cross feature use core controller folder.
- Registration order: datasource → repository → use case/service → viewmodel.
- Example: *lib/core/application/controllers/di.dart*