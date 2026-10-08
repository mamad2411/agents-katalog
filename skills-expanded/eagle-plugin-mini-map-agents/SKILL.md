# Eagle Plugin Map - AI Coding Instructions

## Project Overview

This is an **Eagle App Inspector Plugin** built with React + TypeScript + Vite. Eagle is a digital asset management application, and this plugin visualizes image locations on a map by reading EXIF GPS data from images.

### Key Architecture Points

- **Plugin Type**: Inspector plugin (displays in Eagle's inspector panel when images are selected)
- **Entry Point**: [index.html](../index.html) is loaded by Eagle (not a standalone web app)
- **Build Output**: The `dist/` folder becomes the plugin that Eagle imports
- **Manifest**: [public/manifest.json](../public/manifest.json) defines plugin metadata and preview configuration

## Developer Workflows

```bash
pnpm dev          # Run Vite dev server for local testing
pnpm run build    # Build for production (outputs to dist/)
pnpm run lint     # Auto-fix linting issues
```

## Project-Specific Conventions

### TypeScript Configuration

- Uses **strict type checking** with `typescript-eslint` strict config
- Split configuration: [tsconfig.app.json](../tsconfig.app.json) for app code, [tsconfig.node.json](../tsconfig.node.json) for config files
- Do not use `any` type; prefer precise types or generics, Use `satisfies` operator when necessary.
- Use kebab-case for new file and directory names.

## External Dependencies & Integration

### Eagle Plugin API

- **Documentation**: https://developer.eagle.cool/plugin-api/
- **Examples**: See [eagle-app/eagle-plugin-examples](https://github.com/eagle-app/eagle-plugin-examples/) and [tuki0918/eagle-inspector-plugin-example](https://github.com/tuki0918/eagle-inspector-plugin-example)
- Eagle injects a global `eagle` object when loading the plugin
- Type definitions are available via `src/eagle/types.ts` in this project

#### Common API Patterns

**Plugin Lifecycle & Initialization:**

```ts
// Listen to plugin creation (initialization)
eagle.onPluginCreate(async (plugin) => {
  console.log(plugin.manifest.name);
  console.log(plugin.manifest.version);
  console.log(plugin.path);

  // Get the current theme
  const theme = await eagle.app.theme;
  document.body.setAttribute("theme", theme);

  // Get the selected item
  const item = await eagle.item.getSelected();
  console.log(item);
});

// Listen to theme changes for UI adaptation
eagle.onThemeChanged((theme) => {
  document.body.setAttribute("theme", theme);
  // theme values: Auto, LIGHT, LIGHTGRAY, GRAY, DARK, BLUE, PURPLE
});
```

**Accessing Selected Items:**

```ts
// Get currently selected file(s) in Eagle
const selected = await eagle.item.getSelected();
console.log(selected);
```

**Library Change Detection:**

```ts
// React to library switching
eagle.onLibraryChanged((libraryPath) => {
  console.log(`Library switched to: ${libraryPath}`);
  // Use eagle.library.info() for complete library details
});
```

**Other Lifecycle Events:**

```ts
eagle.onPluginRun(() => {
  // Called when user clicks the plugin in panel
});

eagle.onPluginShow(() => {
  // Plugin window displayed
});

eagle.onPluginHide(() => {
  // Plugin window hidden
});

eagle.onPluginBeforeExit(() => {
  // Cleanup before window closes
});

// Prevent window from closing if needed
window.onbeforeunload = (event) => {
  return (event.returnValue = false);
};
```

### Stack

- **React 19** with StrictMode
- **Vite 7** for bundling
- **TypeScript 5.9** with strict checking
