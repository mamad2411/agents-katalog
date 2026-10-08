# Windsurf Rules Configuration
version: 1.0.0

# Language Requirements
language:
  dart_version: ">=3.0.0"
  features:
    - interface_modifier
    - sealed_classes
    - pattern_matching

# Project Structure
structure:
  src_dir: lib
  test_dir: test
  assets_dir: assets
  core_dir:
    path: lib/core
    subfolders:
      - usecase
      - error
      - interface

# State Management
state_management:
  type: riverpod
  rules:
    - all_providers_must_be_immutable: true
    - prefer_family_providers: true
    - use_consumer_for_widgets: true
    - avoid_global_providers: true
  folder_structure:
    providers:
      path: lib/providers
      subfolders:
        - state
        - notifiers
        - services

# Navigation
routing:
  type: go_router
  rules:
    - use_path_parameters: true
    - use_route_guards: true
    - prefer_const_constructors: true
  folder_structure:
    router:
      path: lib/routes
      files:
        - routes.dart
        - router_refresh_stream.dart
        - guards

# Code Generation
codegen:
  tools:
    - auto_route_generator
    - riverpod_generator
    - freezed
    - json_serializable
  rules:
    - use_freezed_for_models: true
    - generate_immutable_classes: true

# Architecture
architecture:
  pattern: feature_first
  layers:
    - presentation
    - domain
    - data
  rules:
    - one_feature_per_folder: true
    - separate_interface_implementation: true
    - use_repository_pattern: true
    - use_interface_for_contracts: true

# Dependency Rules
dependencies:
  required:
    - flutter_riverpod: ^2.4.9
    - auto_route: ^7.8.4
    - freezed: ^2.4.6
    - json_serializable: ^6.7.1
  dev_dependencies:
    - auto_route_generator: ^7.3.2
    - riverpod_generator: ^2.3.9
    - build_runner: ^2.4.7

# Linting
linting:
  rules:
    - avoid_print: true
    - prefer_const_constructors: true
    - require_trailing_commas: true
    - use_key_in_widget_constructors: true
    - prefer_final_locals: true

# Testing
testing:
  rules:
    - unit_test_providers: true
    - widget_test_screens: true
    - integration_test_flows: true
  coverage_threshold: 80

# Localization
localization:
  type: flutter_localizations
  folder_structure:
    path: lib/core/localization
    files:
      - app_localizations.dart
      - app_localizations_en.dart
      - app_localizations_bn.dart
    subfolders:
      - translations
  rules:
    - use_arb_files: true
    - prefer_string_enums: true
    - no_hardcoded_strings: true
    - support_rtl: true
  supported_locales:
    - en
    - bn

# Patterns
patterns:
  usecase:
    location: lib/core/usecase
    template:
      - abstract interface class UseCase<Type, Params>
      - Either<Failure, Type> return type
      - NoParams for parameter-less cases
  # Error Handling
  error_handling:
    path: lib/core/error
    types:
      failures:
        - ServerFailure
        - CacheFailure
        - NetworkFailure
        - ValidationFailure
        - AuthenticationFailure
      exceptions:
        - ServerException
        - CacheException
        - NetworkException
        - ValidationException
        - AuthenticationException
    rules:
      - use_either_for_results: true
      - map_exceptions_to_failures: true
      - custom_error_messages: true
      - localize_error_messages: true
    folder_structure:
      failures:
        path: lib/core/error/failures
        base_class: Failure
      exceptions:
        path: lib/core/error/exceptions
        base_class: AppException
      messages:
        path: lib/core/error/messages
        file: error_messages.dart
# Error Handling
error_handling:
  path: lib/core/error
  types:
    failures:
      - ServerFailure
      - CacheFailure
      - NetworkFailure
      - ValidationFailure
      - AuthenticationFailure
    exceptions:
      - ServerException
      - CacheException
      - NetworkException
      - ValidationException
      - AuthenticationException
  rules:
    - use_either_for_results: true
    - map_exceptions_to_failures: true
    - custom_error_messages: true
    - localize_error_messages: true
  folder_structure:
    failures:
      path: lib/core/error/failures
      base_class: Failure
    exceptions:
      path: lib/core/error/exceptions
      base_class: AppException
    messages:
      path: lib/core/error/messages
      file: error_messages.dart