---
name: wpcom-blueprints
description: Documentation on creating and using Blueprints in WordPress Studio.
---

# WordPress Studio Blueprints

Use this skill when the user asks about Blueprints, creating custom templates, or the "Open in WordPress Studio" button.

## Overview
Blueprints are JSON files containing configurations for WordPress sites. They define plugins, themes, WordPress versions, PHP versions, and default settings. 

## How to Create Custom Blueprints
- Blueprints are based on the WordPress Playground Blueprint schema.
- Define a `blueprint.json` file.
- Example structure:
  ```json
  {
    "landingPage": "/wp-admin/",
    "preferredVersions": {
      "php": "8.2",
      "wp": "latest"
    },
    "steps": [
      {
        "step": "installPlugin",
        "pluginZipFile": {
          "resource": "wordpress.org/plugins",
          "slug": "gutenberg"
        }
      },
      {
        "step": "installTheme",
        "themeZipFile": {
          "resource": "wordpress.org/themes",
          "slug": "twentytwentyfour"
        }
      }
    ]
  }
  ```

## Open in WordPress Studio Button
- You can add a button to your website or GitHub repo that opens a Blueprint directly in WordPress Studio.
- URL structure: `studio://blueprint?url=https://example.com/blueprint.json`
- This allows users to instantiate a local WordPress environment with a single click, pre-configured with the specified Blueprint.
