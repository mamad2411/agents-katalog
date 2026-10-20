---
name: cmake-patterns
description: "When to activate: CMake, CMakeLists.txt, target_link_libraries, find_package, FetchContent, CMakePresets, build system, install"
origin: zakr
metadata:
  namespace: zakr/devtools-pack
  version: 1.0.0
  category: engineering
  language: cpp
  platforms: [claude-code, codex, gemini-cli, cursor, aider, windsurf]
---
# CMake Patterns

## Modern Target-Based CMake

```cmake
cmake_minimum_required(VERSION 3.25)
project(MyApp VERSION 1.0.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)  # for clangd/clang-tidy

# Library target
add_library(mylib STATIC
    src/parser.cpp
    src/network.cpp
)
target_include_directories(mylib PUBLIC include PRIVATE src)
target_compile_options(mylib PRIVATE -Wall -Wextra -Wpedantic)
target_compile_features(mylib PUBLIC cxx_std_23)

# Executable
add_executable(myapp src/main.cpp)
target_link_libraries(myapp PRIVATE mylib)
```

## find_package

```cmake
# Find system libraries
find_package(Threads REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(Boost 1.82 REQUIRED COMPONENTS filesystem program_options)

target_link_libraries(myapp PRIVATE
    Threads::Threads
    OpenSSL::SSL
    OpenSSL::Crypto
    Boost::filesystem
    Boost::program_options
)
```

## FetchContent (Dependency Management)

```cmake
include(FetchContent)

FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
    FIND_PACKAGE_ARGS NAMES GTest  # use system install if available
)
FetchContent_Declare(
    spdlog
    GIT_REPOSITORY https://github.com/gabime/spdlog.git
    GIT_TAG        v1.13.0
)
FetchContent_MakeAvailable(googletest spdlog)

target_link_libraries(mylib PRIVATE spdlog::spdlog)
target_link_libraries(tests PRIVATE GTest::gtest_main)
```

## CMakePresets.json

```json
{
  "version": 6,
  "configurePresets": [
    {
      "name": "dev",
      "displayName": "Development",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/dev",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Debug",
        "CMAKE_CXX_FLAGS": "-fsanitize=address,undefined"
      }
    },
    {
      "name": "release",
      "generator": "Ninja",
      "binaryDir": "${sourceDir}/build/release",
      "cacheVariables": {
        "CMAKE_BUILD_TYPE": "Release",
        "CMAKE_INTERPROCEDURAL_OPTIMIZATION": "ON"
      }
    }
  ],
  "buildPresets": [
    { "name": "dev",     "configurePreset": "dev" },
    { "name": "release", "configurePreset": "release" }
  ],
  "testPresets": [
    { "name": "dev", "configurePreset": "dev", "output": { "outputOnFailure": true } }
  ]
}
```

## Install & Export Rules

```cmake
include(GNUInstallDirs)
include(CMakePackageConfigHelpers)

install(TARGETS mylib myapp
    EXPORT MyLibTargets
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}
)
install(DIRECTORY include/ DESTINATION ${CMAKE_INSTALL_INCLUDEDIR})

# Allow find_package(MyLib) by consumers
write_basic_package_version_file(
    MyLibConfigVersion.cmake COMPATIBILITY SameMajorVersion
)
install(EXPORT MyLibTargets NAMESPACE MyLib:: DESTINATION lib/cmake/MyLib)
install(FILES MyLibConfig.cmake ${CMAKE_CURRENT_BINARY_DIR}/MyLibConfigVersion.cmake
    DESTINATION lib/cmake/MyLib
)
```

## Testing Setup

```cmake
enable_testing()
include(GoogleTest)

add_executable(unit_tests tests/parser_test.cpp tests/network_test.cpp)
target_link_libraries(unit_tests PRIVATE mylib GTest::gtest_main)

gtest_discover_tests(unit_tests)

# Run: cmake --build build/dev && ctest --preset dev --output-on-failure
```

## Compiler Warnings as a Target

```cmake
add_library(warnings INTERFACE)
target_compile_options(warnings INTERFACE
    $<$<CXX_COMPILER_ID:GNU,Clang>:
        -Wall -Wextra -Wpedantic -Wshadow -Wnon-virtual-dtor
        -Wold-style-cast -Woverloaded-virtual -Wconversion>
    $<$<CXX_COMPILER_ID:MSVC>:/W4 /WX>
)
target_link_libraries(mylib PRIVATE warnings)
```
