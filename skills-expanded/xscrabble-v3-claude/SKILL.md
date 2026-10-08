# XScrabble v3 Development Guide

## Build Commands
- Setup: `mkdir build && cd build && cmake ..`
- Build: `cd build && make`
- Run: `./build/xscrabble`
- Install (macOS): `./scripts/install-osx.sh`
- Clean: `cd build && make clean`
- Rebuild: `cd build && cmake .. && make`

## Debug Commands
- Debug build: `mkdir build-debug && cd build-debug && cmake -DCMAKE_BUILD_TYPE=Debug .. && make`
- Run with GDB: `gdb ./build-debug/xscrabble`

## Test Commands
- All tests: `cd build && ctest -V` or `./tests/run_tests.sh`
- Single test: `cd build && ./tests/test_board` (replace with test_game or test_dictionary)
- Build tests: `cd build && make test_board test_game test_dictionary`

## Code Style Guidelines
- C11 standard with K&R-style braces (opening brace on same line)
- 4-space indentation, no tabs
- Variables: snake_case for all identifiers
- Constants: ALL_CAPS for #define, snake_case for static const
- Module organization: Header in include/, implementation in src/
- Error handling: Return boolean success/failure when appropriate
- Memory management: Free all allocated memory; avoid memory leaks
- Include guards: Use #ifndef HEADER_H / #define HEADER_H pattern
- Comments: Function headers with descriptions, parameters, and return values
- Keep functions small and focused on single responsibility
- Separate UI logic from game mechanics

## Project Structure
- src/: Core implementation files
- include/: Header files
- tests/: Unit tests
- data/: Dictionary and game data files
- resources/: UI resources and configuration

## Dependencies
- X11 libraries (Xt, Xaw, Xmu)
- CMake 3.10+

## Dictionaries
- English: OSPD3 (Official Scrabble Players Dictionary, 3rd Edition)
- French: ODS8 (Official Dictionary of Scrabble, 8th Edition)
- Location: `data/dictionaries/` (compressed .gz) and `data/dictionaries/extracted/` (plain text)