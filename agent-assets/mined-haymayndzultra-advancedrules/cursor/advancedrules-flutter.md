---
title: "Flutter Development — v1"
description: "Flutter development with Dart best practices and patterns"
globs: ["**/*.dart", "lib/**/*.dart", "test/**/*.dart"]
alwaysApply: false
priority: high
---

# Flutter Development Rules

## Technology Stack
- **Framework**: Flutter
- **Language**: Dart
- **Build Tool**: Flutter CLI
- **Package Manager**: pub
- **State Management**: Provider, Riverpod, Bloc

## Core Principles
- Use Flutter widgets effectively
- Implement proper state management
- Follow Material Design guidelines
- Optimize for performance and memory
- Use const constructors when possible

## Project Structure
lib/
├─ main.dart           # App entry point
├─ screens/            # Screen widgets
│   ├─ home/
│   ├─ profile/
│   └─ settings/
├─ widgets/            # Reusable widgets
│   ├─ common/
│   └─ custom/
├─ models/             # Data models
├─ services/           # Business logic
├─ providers/          # State management
├─ utils/              # Utility functions
└─ constants/          # App constants

## Coding Standards
- Use camelCase for variables and functions
- Use PascalCase for classes and widgets
- Use descriptive names for widgets and variables
- Follow Dart conventions and best practices
- Use proper indentation (2 spaces)

## Best Practices
- Use StatelessWidget when possible
- Implement proper error handling and validation
- Use const constructors for static widgets
- Optimize widget rebuilds with proper keys
- Implement proper loading states

## State Management
- Use Provider for simple state
- Use Riverpod for complex state management
- Use Bloc for advanced state patterns
- Implement proper state persistence
- Handle state changes efficiently

## Common Patterns
- Custom widgets and compositions
- Platform-specific implementations
- Responsive design with MediaQuery
- Navigation with Navigator 2.0
- Localization and internationalization

## Performance Optimization
- Use ListView.builder for long lists
- Implement proper image caching
- Use const constructors
- Minimize widget rebuilds
- Profile and optimize performance

## Testing Strategy
- Write unit tests for business logic
- Implement widget tests for UI components
- Use integration tests for user flows
- Mock external dependencies
- Maintain high test coverage
