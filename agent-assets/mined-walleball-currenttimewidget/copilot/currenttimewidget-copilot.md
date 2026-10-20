# Garmin Connect IQ Widget Development Guide

## Project Overview

This is a **Garmin Connect IQ widget** written in **MonkeyC**, targeting the vivoactive5 device. Widgets are glanceable home screen apps that display information at a glance.

## Architecture

### Core Components

-  **[source/CurrentTimeApp.mc](../source/CurrentTimeApp.mc)**: Application entry point extending `Application.AppBase`
   -  `initialize()`: App initialization
   -  `getInitialView()`: Returns the widget's view
   -  `onStart()/onStop()`: Lifecycle hooks for state management
-  **[source/CurrentTimeView.mc](../source/CurrentTimeView.mc)**: UI layer extending `WatchUi.View`
   -  `onLayout(dc)`: Load XML layouts via `Rez.Layouts.MainLayout(dc)`
   -  `onUpdate(dc)`: Render updates (must call `View.onUpdate(dc)` first)
   -  `onShow()/onHide()`: View lifecycle for resource management

### Resource System

Resources are defined in XML and accessed via the generated `Rez` namespace:

-  **resources/layouts/layout.xml**: UI component positioning (e.g., `<bitmap id="id_monkey" x="center" y="center"/>`)
-  **resources/strings/strings.xml**: Localized strings referenced as `@Strings.AppName`
-  **resources/drawables/drawables.xml**: Graphics assets referenced as `@Drawables.LauncherIcon`
-  Access pattern: `Rez.Layouts.MainLayout`, `Rez.Strings.AppName`, `Rez.Drawables.LauncherIcon`

## Development Workflow

### Project Configuration

**DO NOT manually edit manifest.xml** - it's auto-generated. Instead use VS Code commands:

-  `Monkey C: Edit Application` - Update app attributes
-  `Monkey C: Set Products by Product Category` - Add target devices
-  `Monkey C: Edit Products` - Manage individual device targets
-  `Monkey C: Edit Permissions` - Configure required permissions
-  `Monkey C: Edit Languages` - Set supported locales
-  `Monkey C: Configure Monkey Barrel` - Manage library dependencies

### Build System

-  **monkey.jungle**: Simple build config pointing to manifest.xml
-  Generated code lives in `bin/gen/` (device-specific resource compilation)
-  Compiled bytecode in `bin/mir/`

### Testing

Use the Garmin Connect IQ simulator or device for testing. Access via VS Code's "Run and Debug" panel with the Monkey C extension.

## Language Conventions

### MonkeyC Syntax

-  Strong typing with type annotations: `function onStart(state as Dictionary?) as Void`
-  Nullable types use `?` suffix: `Dictionary?`
-  Module imports: `import Toybox.Graphics;`
-  Class inheritance: `class MyView extends WatchUi.View`

### Common Patterns

-  Always call parent methods first in overrides: `View.onUpdate(dc)` before custom drawing
-  Use `dc` (DeviceContext) for all graphics operations
-  Resource IDs use snake_case: `id_monkey`
-  Class names use PascalCase: `CurrentTimeView`

## Key Constraints

-  **Memory limits**: Garmin devices have strict memory constraints - avoid large allocations
-  **API level**: minApiLevel="3.2.0" defines available Toybox APIs
-  **Widget refresh**: Widgets update periodically, not continuously - design for low power
-  **No background execution**: Widget code only runs when visible or during refresh

## Adding New Features

1. Update resources in `resources/` (layouts, strings, drawables)
2. Modify view logic in `CurrentTimeView.mc` (drawing, updates)
3. Add app-level logic in `CurrentTimeApp.mc` (state, lifecycle)
4. Use VS Code commands (not manual edits) for manifest changes
5. Test on simulator before deploying to device
