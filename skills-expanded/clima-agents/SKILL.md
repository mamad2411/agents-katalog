# Project Context: Weather APP



## Technology Stack
- **Language:** Kotlin
- **UI:** Jetpack Compose, Material 3
- **Architecture:** MVVM (Model-View-ViewModel) + Clean Architecture
- **Async:** Kotlin Coroutines
- **Local Storage:** Room
- **Navigation:** Compose Navigation
- **Dependency injection:** Hilt
- **API:** WeatherAPI

## Coding Standards
- Always use `camelCase` for variables and methods.
- Use `PascalCase` for classes.
- UI components must be composable functions, not XML.
- Use `StateFlow` or `SharedFlow` for UI state management.
- All Compose functions must be `non-skippable` where possible and annotated with `@Composable`.
- Prefer `data class` for data modeling.
- Kotlin DSL is used for configuration

## Verbs normalized

For maintain the consistency across the project with the name of methods these are the normalized
verbs:

- For request to an API use the verb *fetch*
- For response from an API use the verb *obtain*
- For response from database use the verb *obtain*
- For create a new record in database use the verb *insert*
- For update a record in database use the verb *update*
- For delete a record in database use the verb *delete*

## Project Structure
- `data/`: Repositories, local data sources.
- `data/repository`: Business logic, use cases.
- `data/local/dao`: Data access objects.
- `data/local/database`: Database configurator.
- `data/local/entity`: Entity classes.
- `ui/`: Contains Jetpack Compose screens and ViewModels.
- `ui/screens`: Activities, @Composable functions.
- `ui/viewmodel`: ViewModels.
- `ui/theme`: Theme definitions.

## External sources
- [WeatherAPI] (https://www.weatherapi.com/)

## Rules for AI Generation
1.  **Architecture:** Do not use `ViewModel` for UI navigation logic, put navigation logic inside @Composable functions. Keep business logic out of composables.
2.  **UI:** Use Material 3 components only.
3.  **Data:** Use Room DAO with suspending functions.
4.  **Testing:** Always generate unit tests for ViewModels.
5. **Documentation:** Keep documentation under `./docs/` updated if architectural changes are made,
   always use English for programming and documentation.
## Important Components
- The main activity is located at `app/src/main/java/com/example/clima_v100/MainActivity.kt`.
- The theme definitions are in `ui/theme/`.
