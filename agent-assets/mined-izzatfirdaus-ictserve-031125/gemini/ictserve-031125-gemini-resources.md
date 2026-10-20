# resources Directory - GEMINI Instructions

This file provides instructions for the Gemini AI related to the `resources` directory of the ICTServe project.

## Directory Overview

The `resources` directory contains the application's views, raw assets (like CSS and JavaScript), and language files.

* **views:** Contains the application's Blade templates.
* **css:** Contains the application's raw CSS files. These are typically processed by Vite.
* **js:** Contains the application's raw JavaScript files. These are also typically processed by Vite.
* **lang:** Contains the application's language files for localization.

## Instructions

* **Views:** When creating or modifying Blade views, follow the existing structure and conventions. Use Blade components and layouts to promote code reuse.
* **Assets:** When adding new CSS or JavaScript, place them in the appropriate subdirectories. Remember that these files need to be processed by Vite, so you may need to update the `vite.config.js` file.
* **Language Files:** When adding or modifying language strings, ensure they are added to all relevant language files (e.g., `en` and `ms`).
