---
name: icon-block-custom-libraries
description: Developer guidance on managing Icon Block libraries. Use when registering custom icon collections or disabling the raw SVG input field.
---

# Icon Block: Custom Libraries & Filters

The Icon Block can be extended by theme and plugin developers to provide curated libraries of icons to the user.

## Disabling Custom SVGs
If you are building a strict client site and want to prevent users from pasting arbitrary SVG code (forcing them to use pre-approved icons):
```js
// Use this filter in a block editor JavaScript file
wp.hooks.addFilter(
    'iconBlock.enableCustomIcons',
    'my-theme/disable-custom-icons',
    () => false
);
```

## Registering Custom Icon Libraries
Developers can register their own collections of SVGs to appear alongside the default WordPress icons in the block's Quick Inserter. This is done via JavaScript in the Block Editor context. 

*Note: For the exact JS implementation of custom library registration, refer to the plugin author's official documentation (`nickdiego.com/adding-custom-icons-to-the-icon-block/`), as the block utilizes a specific `registerIconLibrary` API.*
