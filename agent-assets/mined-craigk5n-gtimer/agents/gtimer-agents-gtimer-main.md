# AGENTS.md - Coding Guidelines for gtimer

> This file helps AI coding agents work effectively in this repository.

## Status Tracking

**STATUS.md is the source of truth for project status and progress.** Always check and update STATUS.md when:
- Starting new work (mark as "in_progress")
- Completing tasks (mark as "complete")
- Testing features (mark as "testing")
- Identifying blockers or issues

Maintain STATUS.md as work progresses through stages: not started → in_progress → testing → complete.

## Project Overview

gtimer is a GTK 4 + Libadwaita time tracking application written in C (GNU11). It uses Meson build system and follows GNOME/GTK coding conventions.

## Build Commands

### Setup and Build
```bash
# Initial setup
meson setup build

# Build
ninja -C build

# Build with verbose output
ninja -C build -v
```

### Testing
```bash
# Run all tests
meson test -C build

# Run a single test (use test name from meson.build)
meson test -C build db
meson test -C build importer
meson test -C build model
meson test -C build utils
meson test -C build service
meson test -C build idle-init

# Run with verbose output
meson test -C build --verbose
```

### Running the Application
```bash
# Run from build directory
./build/src/gtimer

# Run on Wayland
GDK_BACKEND=wayland ./build/src/gtimer

# Run on X11/XWayland
GDK_BACKEND=x11 ./build/src/gtimer

# Run with dark mode
GTK_THEME=Adwaita:dark ./build/src/gtimer
```

### Debugging
```bash
# Interactive GTK inspector
GTK_DEBUG=interactive ./build/src/gtimer

# Show layout debugging
GTK_DEBUG=layout ./build/src/gtimer

# Show events
GTK_DEBUG=events ./build/src/gtimer

# All debug messages
G_MESSAGES_DEBUG=all ./build/src/gtimer
```

## Code Style Guidelines

### Indentation and Formatting
- **Indentation**: 2 spaces (no tabs)
- **Line length**: 100 characters max
- **Brace style**: Opening brace on same line for functions, new line for control structures
- **Trailing whitespace**: Remove before committing

### Naming Conventions
- **Files**: `kebab-case.c` (e.g., `db-manager.c`, `task-list-model.c`)
- **Functions**: `gtimer_module_function_name` (e.g., `gtimer_db_manager_new`)
- **Types**: `GTimerModuleName` (e.g., `GTimerDBManager`, `GTimerTaskModel`)
- **Macros/Constants**: `GTIMER_CONSTANT_NAME` (e.g., `GTIMER_TYPE_WINDOW`)
- **Private structs**: `_GTimerModuleName` (e.g., `_GTimerDBManager`)
- **Header guards**: `GTIMER_FILE_NAME_H` (e.g., `GTIMER_DB_MANAGER_H`)

### Function Declarations
- Return type on separate line for complex types
- Function name at start of line for definitions
- Use `void` parameter list for no arguments

```c
// Good
GTimerDBManager *
gtimer_db_manager_new (const char *path, GError **error)
{
  // implementation
}

void
gtimer_db_manager_free (GTimerDBManager *self)
{
  // implementation
}
```

### Includes and Imports
- System headers first (alphabetical)
- GLib/GTK headers next
- Local headers last
- Use `#include <header.h>` for system/GLib headers
- Use `#include "local-header.h"` for local headers

```c
#include <stdio.h>
#include <sqlite3.h>
#include <adwaita.h>
#include <glib.h>

#include "db-manager.h"
#include "models.h"
```

### Error Handling
- Use `GError **` for functions that can fail
- Always check return values
- Clean up resources on error paths
- Use `g_set_error()` for setting errors

```c
GTimerDBManager *
gtimer_db_manager_new (const char *path, GError **error)
{
  int rc = sqlite3_open (path, &db);
  if (rc != SQLITE_OK) {
    g_set_error (error, G_FILE_ERROR, G_FILE_ERROR_FAILED,
                 "Failed to open database: %s", sqlite3_errmsg (db));
    sqlite3_close (db);
    return NULL;
  }
  // ...
}
```

### Memory Management
- Use GLib memory functions: `g_new0()`, `g_free()`, `g_strdup()`
- Free resources in reverse order of allocation
- Check for NULL before freeing (GLib functions handle this)
- Use `g_autofree` and `g_autoptr` when possible

### GObject Patterns
- Use `G_DECLARE_FINAL_TYPE` for final classes
- Use `G_DEFINE_TYPE` for type registration
- Follow GTK widget naming: `GTimerWindow`, `gtimer_window_*`

```c
// Header
#define GTIMER_TYPE_WINDOW (gtimer_window_get_type ())
G_DECLARE_FINAL_TYPE (GTimerWindow, gtimer_window, GTIMER, WINDOW, AdwApplicationWindow)

// Source
G_DEFINE_TYPE (GTimerWindow, gtimer_window, ADW_TYPE_APPLICATION_WINDOW)
```

### Test Writing
- Use GLib testing framework (`g_test_*`)
- Test file naming: `test-module.c`
- Test function naming: `test_module_feature`
- Use in-memory databases (`:memory:`) for DB tests

```c
static void
test_db_init (void)
{
  GError *error = NULL;
  GTimerDBManager *db = gtimer_db_manager_new (":memory:", &error);
  g_assert_no_error (error);
  g_assert_nonnull (db);
  gtimer_db_manager_free (db);
}

int
main (int argc, char **argv)
{
  g_test_init (&argc, &argv, NULL);
  g_test_add_func ("/db/init", test_db_init);
  return g_test_run ();
}
```

### Commenting
- Use `//` for single-line comments
- Use `/* */` for multi-line comments
- Add comments for complex logic or non-obvious behavior
- Document public API in headers

## Project Structure

```
gtimer/
├── meson.build          # Root build file
├── src/                 # Application source
│   ├── main.c
│   ├── gtimer-window.c
│   └── meson.build
├── core/                # Core library
│   ├── db-manager.c
│   ├── task-list-model.c
│   └── meson.build
├── tests/               # Test files
│   ├── test-db.c
│   └── meson.build
└── data/                # Resources and desktop files
    └── style.css
```

## Important Notes

- **C Standard**: GNU11 (`c_std=gnu11` in meson.build)
- **Warning Level**: 2 (treat warnings as important)
- **Dependencies**: GTK 4, Libadwaita 1, SQLite 3, GLib 2.0
- **Target**: Wayland-first, with X11 fallback support
- **Data format**: SQLite database in XDG directories
- **UI Framework**: Libadwaita for modern GNOME-style interface

## Common Tasks

### Adding a New Source File
1. Create file in appropriate directory (`src/` or `core/`)
2. Add to `meson.build` in that directory
3. Include header in dependent files
4. Build and test

### Adding a New Test
1. Create `test-feature.c` in `tests/`
2. Add to `tests/meson.build`
3. Run with `meson test -C build feature`

### Debugging Tips
- Use `g_print()` for simple debugging
- Use `g_debug()` for verbose output (shown with `G_MESSAGES_DEBUG=all`)
- GTK Inspector: `GTK_DEBUG=interactive`
- Check for memory leaks with valgrind (if needed)
