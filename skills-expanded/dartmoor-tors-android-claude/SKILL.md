# Dartmoor Tors Android

## Project Overview

An Android app for exploring and tracking visits to Dartmoor tors. The app displays 900+ tors on a map, allows users to mark visits, associate photos, and track progress.

## Tech Stack

- **Language**: Kotlin
- **UI Framework**: Jetpack Compose with Material 3
- **Maps**: Google Maps SDK for Android (Compose)
- **Database**: Room (local) + potentially Google Drive/Firebase (cloud sync)
- **Architecture**: MVVM with Repository pattern
- **DI**: Hilt (Dagger)
- **JSON Parsing**: Gson/Moshi
- **Build System**: Gradle with Kotlin DSL
- **Min SDK**: 26 (Android 8.0)
- **Target SDK**: 34 (Android 14)

## Project Structure

```
app/
├── src/main/
│   ├── java/com/dartmoortors/
│   │   ├── MainActivity.kt
│   │   ├── DartmoorTorsApplication.kt
│   │   ├── data/
│   │   │   ├── model/              # Data classes (Tor, VisitedTor, Checklist)
│   │   │   ├── local/              # Room database, DAOs
│   │   │   └── repository/         # Data repositories
│   │   ├── di/                     # Hilt modules
│   │   ├── ui/
│   │   │   ├── navigation/         # Navigation setup
│   │   │   ├── theme/              # Material 3 theming
│   │   │   ├── map/                # Map view components
│   │   │   ├── search/             # Search tab
│   │   │   ├── collection/         # Collection/filters view
│   │   │   ├── photos/             # Photos tab
│   │   │   ├── detail/             # Tor detail bottom sheet
│   │   │   └── components/         # Shared components
│   │   └── util/                   # Utilities, extensions
│   ├── assets/
│   │   └── tors.json              # Bundled tor data
│   └── res/
│       ├── drawable/              # Icons, markers
│       ├── values/                # Strings, colors, themes
│       └── mipmap/                # App icons
├── build.gradle.kts
└── proguard-rules.pro
```

## Key Features

See `/specs` directory for detailed specifications:

1. **Map View** (`specs/view-tors-map.md`)
   - Full-screen Google Maps with tor markers
   - Color-coded markers: Green (visited), Teal (accessible), Orange (not accessible)
   - My Location button, compass tracking
   - Photos layer toggle

2. **Search Tab** (`specs/navigation.md`)
   - Searchable list of tors
   - Filter chips: Accessible, Visited, Unvisited
   - Sort options: Height, Name, Distance

3. **Collection View** (`specs/view-tor-types.md`)
   - Toggle tor classifications for filtering
   - Progress tracking (visited counts)
   - About/credits sections

4. **Tor Detail** (`specs/view-tor-detail.md`)
   - Bottom sheet with tor info
   - Mark as visited with date picker
   - External links (Google Maps, Tors of Dartmoor, Wikipedia)
   - Photo association

5. **Photos** (`specs/photos.md`)
   - Associate photos with visited tors
   - Auto-scan photos by location
   - Create Dartmoor Tors album

## Data Model

```kotlin
// Tor (from bundled JSON)
data class Tor(
    val id: String,
    val name: String,
    val latitude: Double,
    val longitude: Double,
    val heightMeters: Int,
    val osGridRef: String,
    val classification: Classification,
    val access: Access,
    val parish: String?,
    val rockType: String?,
    val torsOfDartmoorURL: String?,
    val wikipediaURL: String?
)

// VisitedTor (user data, stored in Room)
@Entity
data class VisitedTor(
    @PrimaryKey val torId: String,
    val visitedDate: Long,
    val photoUri: String?,
    val checklistId: String
)
```

## Build & Run

```bash
# Build debug APK
./gradlew assembleDebug

# Install on connected device/emulator
./gradlew installDebug

# Run all tests
./gradlew test

# Run instrumented tests
./gradlew connectedAndroidTest
```

## Emulator Requirements

For VS Code Android development, you need:

1. **Android Studio** (for SDK Manager and AVD Manager)
2. **Android SDK** (API 34 recommended)
3. **Android Emulator** with a virtual device:
   - Recommended: Pixel 7 with API 34
   - Install via Android Studio → Virtual Device Manager

## VS Code Extensions

- **Android for VS Code** (`nickmillerdev.android-tools`)
- **Kotlin Language** (`mathiasfrohlich.Kotlin`)
- **Gradle for Java** (`vscjava.vscode-gradle`)

## Environment Variables

```bash
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

## API Keys

Create `local.properties` with your Google Maps API key:

```
MAPS_API_KEY=your_api_key_here
```

## Code Style

- Follow Kotlin coding conventions
- Use Compose best practices (hoisted state, remember, derivedStateOf)
- Prefer immutable data classes
- Use sealed classes for UI state
- Extract reusable composables to components/

## Testing

- Unit tests for ViewModels and Repositories
- UI tests with Compose testing framework
- Integration tests for database operations

## Specifications Reference

| Spec File                  | Description                |
| -------------------------- | -------------------------- |
| `specs/index.md`           | Overview and navigation    |
| `specs/tor-data.md`        | Tor data model and loading |
| `specs/navigation.md`      | Tab bar and navigation     |
| `specs/view-tors-map.md`   | Map view implementation    |
| `specs/view-tor-detail.md` | Tor detail sheet           |
| `specs/view-tor-types.md`  | Collection/filter view     |
| `specs/photos.md`          | Photo features             |
| `specs/user-data.md`       | User data storage          |
| `specs/user-location.md`   | Location features          |
| `specs/todo.md`            | Feature status tracking    |
| `specs/tests.md`           | Test scenarios             |
