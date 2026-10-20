---
title: "Android Jetpack Compose — v1"
description: "Android development with Jetpack Compose best practices"
globs: ["**/*.kt", "**/*.java", "app/**/*.kt", "app/**/*.java", "**/*.xml"]
alwaysApply: false
priority: high
---

# Android Development Rules

## Technology Stack
- **Framework**: Jetpack Compose
- **Language**: Kotlin (preferred), Java
- **Build Tool**: Gradle
- **Package Manager**: Maven/Gradle
- **Architecture**: MVVM, Clean Architecture

## Core Principles
- Use Compose UI components effectively
- Implement proper state management
- Follow Material Design 3 guidelines
- Optimize for performance and battery life
- Use modern Android development practices

## Project Structure
app/
├─ src/main/
│   ├─ java/           # Kotlin/Java source
│   │   └─ com/company/app/
│   │       ├─ ui/     # UI components
│   │       ├─ data/   # Data layer
│   │       ├─ domain/ # Business logic
│   │       └─ utils/  # Utilities
│   ├─ res/            # Resources
│   │   ├─ layout/     # XML layouts (if needed)
│   │   ├─ values/     # Strings, colors, themes
│   │   └─ drawable/   # Images and icons
│   └─ AndroidManifest.xml
├─ build.gradle        # Module build file
└─ proguard-rules.pro  # ProGuard rules

## Coding Standards
- Use camelCase for variables and functions
- Use PascalCase for classes and interfaces
- Use descriptive names for components
- Follow Kotlin conventions and best practices
- Use proper indentation (4 spaces)

## Best Practices
- Use Compose functions effectively
- Implement proper state hoisting
- Use remember and derivedStateOf
- Optimize recomposition
- Handle configuration changes properly

## State Management
- Use ViewModel for business logic
- Implement proper state hoisting
- Use StateFlow and LiveData
- Handle state changes efficiently
- Implement proper error handling

## Common Patterns
- State management with ViewModel
- Navigation with Compose Navigation
- Custom composables and modifiers
- Platform-specific implementations
- Dependency injection with Hilt

## Performance Optimization
- Use LazyColumn for long lists
- Implement proper image loading
- Optimize recomposition
- Use remember and derivedStateOf
- Profile and optimize performance

## Testing Strategy
- Write unit tests for ViewModels
- Implement Compose tests for UI
- Use Espresso for integration tests
- Mock external dependencies
- Maintain high test coverage
