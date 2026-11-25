---
name: qt-cmake-project
version: 1.0.0
description: Set up and maintain a Qt6 CMake project with modern targets, QML modules, resources, and deployment scripts.
author: matrixx0070
tags: [qt6, cmake, qml, build, deployment]
capabilities: []
---
## When to use
Use this when you are creating a new Qt 6.x project, converting a legacy qmake/Qt5 build, or adding a QML module, resources, or a deployment step to an existing CMake tree. **Not for:** documenting the resulting APIs (see `qt-cpp-docs`) or reviewing the C++ that fills these targets (see `qt-cpp-review`).

## Method
1. Set the floor: `cmake_minimum_required(VERSION 3.16)` — Qt6's CMake API needs 3.16+. Decision point: if you use `qt_add_qml_module` with modern QML tooling, require 3.19+ so target-based QML linting works.
2. Declare the project and find Qt: `project(...)` then `find_package(Qt6 REQUIRED COMPONENTS Core ...)`. List only the components you link.
3. Call `qt_standard_project_setup()` immediately after the find. It enables AUTOMOC/AUTOUIC/AUTORCC and sets sane C++/install defaults. Decision point: if you must support Qt 6.2 exactly, guard with a version check — the helper landed in 6.3; otherwise set `CMAKE_AUTOMOC ON` manually.
4. Create the target: `qt_add_executable(app ...)` for GUI/console apps, or `qt_add_library(...)` for reusable code. Decision point: Widgets app → link `Qt6::Widgets`; Quick/QML app → link `Qt6::Quick` and go to step 5.
5. For QML, call `qt_add_qml_module(app URI ... VERSION 1.0 QML_FILES ... RESOURCES ...)`. This registers types, generates `qmldir`, and compiles QML into the binary. Do not also list the same `.qml` in a `.qrc`.
6. Add non-QML assets with `qt_add_resources(app "assets" PREFIX "/" FILES ...)` or a `.qrc` file passed to the target.
7. Link: `target_link_libraries(app PRIVATE Qt6::Core Qt6::Quick ...)`.
8. Configure with the Ninja generator (`cmake -G Ninja`) and set `CMAKE_EXPORT_COMPILE_COMMANDS ON` so clang-tidy/clazy and editors see the flags.
9. Add deployment: `qt_generate_deploy_app_script(...)` and `install(SCRIPT ...)`. Decision point: for ad-hoc bundling instead of installs, run `windeployqt`/`macdeployqt` on the built binary.

## Example
```cmake
cmake_minimum_required(VERSION 3.19)
project(HelloQuick VERSION 1.0 LANGUAGES CXX)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

find_package(Qt6 REQUIRED COMPONENTS Core Quick)
qt_standard_project_setup(REQUIRES 6.5)

qt_add_executable(app main.cpp)

qt_add_qml_module(app
    URI HelloQuick
    VERSION 1.0
    QML_FILES Main.qml
    RESOURCES icons/logo.png
)

target_link_libraries(app PRIVATE Qt6::Core Qt6::Quick)

qt_generate_deploy_app_script(
    TARGET app
    OUTPUT_SCRIPT deploy_script
    NO_UNSUPPORTED_PLATFORM_ERROR
)
install(SCRIPT ${deploy_script})
```

## Pitfalls
- **Missing AUTOMOC.** Any class with `Q_OBJECT` fails to link if AUTOMOC is off; `qt_standard_project_setup()` turns it on for you — never rely on old add_executable.
- **Duplicate QML registration.** Listing a `.qml` in both `qt_add_qml_module` and a `.qrc` produces resource path clashes and stale cached types.
- **URI vs directory mismatch.** The `URI` dotted path must match the module's resource prefix; a mismatch gives runtime "module not installed" errors.
- **Wrong minimum version.** Copying `qt_standard_project_setup()` into a project pinned at `cmake_minimum_required(3.16)` silently skips 3.19+ QML behaviors.
- **Deploy without install.** `qt_generate_deploy_app_script` only runs at install time; forgetting `install(SCRIPT ...)` ships nothing.

## Output format
```
project-root/
  CMakeLists.txt        # cmake_minimum_required 3.16+, find_package(Qt6 ...),
                        # qt_standard_project_setup(), qt_add_executable/qt_add_qml_module,
                        # target_link_libraries(Qt6::...), deploy script
  main.cpp
  Main.qml              # (Quick apps)
  build/                # cmake -G Ninja -DCMAKE_EXPORT_COMPILE_COMMANDS=ON
```

## Reference
- CMake minimum: `cmake_minimum_required(VERSION 3.16)`; QML target tooling needs 3.19+.
- `find_package(Qt6 REQUIRED COMPONENTS Core Gui Widgets Quick Qml Network ...)` — components map to imported targets `Qt6::Core`, `Qt6::Widgets`, `Qt6::Quick`, etc.
- `qt_standard_project_setup([REQUIRES <ver>] [SUPPORTS_UP_TO <ver>])` (added Qt 6.3) enables `CMAKE_AUTOMOC`, `CMAKE_AUTOUIC`, `CMAKE_AUTORCC` and sets `CMAKE_INCLUDE_CURRENT_DIR`.
- `qt_add_executable(<target> [WIN32] [MACOSX_BUNDLE] sources...)` — Qt's wrapper over `add_executable` that handles finalizers/plugins.
- `qt_add_qml_module(<target> URI <dotted.uri> VERSION <maj.min> QML_FILES ... RESOURCES ... [SOURCES ...] [NO_PLUGIN])` — generates `qmldir` and a type registration `.cpp`.
- `qt_add_resources(<target> <name> PREFIX <p> FILES ...)` is the target-based form; classic `.qrc` files can also be passed directly to the target's sources.
- `CMAKE_AUTOMOC` runs `moc`, `CMAKE_AUTORCC` compiles `.qrc`, `CMAKE_AUTOUIC` runs `uic` on `.ui`.
- Generator: `cmake -S . -B build -G Ninja`; build with `cmake --build build`.
- `CMAKE_EXPORT_COMPILE_COMMANDS ON` emits `build/compile_commands.json` for clang-tidy/clazy/LSP.
- Deployment: `windeployqt <app>.exe` (Windows), `macdeployqt <app>.app` (macOS), or CMake-native `qt_generate_deploy_app_script(TARGET ... OUTPUT_SCRIPT var)` + `install(SCRIPT ${var})` (cross-platform, Qt 6.3+).
