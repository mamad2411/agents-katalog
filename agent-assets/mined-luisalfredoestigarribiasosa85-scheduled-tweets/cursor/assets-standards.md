---
description: Ensures that assets are managed according to Rails Sprockets conventions, with guidelines for integrating StimulusJS/Hotwire.
globs:
  - "app/assets/**/*"
  - "vendor/assets/**/*"
---

# Assets

<rule>
name: assets_standard
description: Provides guidelines for managing the asset pipeline using Sprockets, including organization of CSS, JavaScript, and images, and integration with StimulusJS/Hotwire.

filters:
  - type: path
    pattern: "^(app|vendor)/assets/.*"
    # Applies to all assets in the app/assets and vendor/assets directories

actions:
  - type: suggest
    message: |
      Asset files should:
      1. Be organized into clear subdirectories (javascripts, stylesheets, images).
      2. Follow Rails naming conventions and file structure.
      3. Use StimulusJS/Hotwire/Turbo for JavaScript interactions without relying on Webpacker.
      4. Contain comments and documentation where necessary.
      5. Strictly avoid inline JavaScript within view templates.

examples:
  - input: |
      # Bad example: Assets are unorganized and contain inline scripts
      <script>
        // Inline JavaScript in the view
      </script>
    output: "Assets should reside in the proper directories and avoid inline scripts."
  - input: |
      # Good example: Properly organized asset with StimulusJS integration
      // File: app/assets/javascripts/controllers/user_controller.js
      import { Controller } from "stimulus";

      export default class extends Controller {
        connect() {
          console.log('User controller connected');
        }
      }
    output: "Asset is organized in the asset pipeline and uses StimulusJS appropriately."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project
  responsibility: "Standardize asset organization and ensure proper integration with StimulusJS/Hotwire"
</rule>
