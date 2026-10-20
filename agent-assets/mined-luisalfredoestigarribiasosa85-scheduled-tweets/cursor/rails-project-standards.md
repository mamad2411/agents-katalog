---
description: Sets overarching guidelines for Rails project structure and conventions.
globs:
  - "Gemfile"
  - "config.ru"
  - "app/**/*"
  - "config/**/*"
  - "db/**/*"
  - "lib/**/*"
---

# Rails Project

<rule>
name: rails_project_standard
description: Establishes overall project organization, file structure, and dependency management conventions in a Rails project, including multi-database support, domain-specific modules, and Hotwire/Stimulus integrations.

filters:
  - type: path
    pattern: "^(Gemfile|config\\.ru|app/|config/|db/|lib/)"
    # Applies to key project files and directories

actions:
  - type: suggest
    message: |
      This Rails project includes several advanced conventions, and each must be handled with care to maintain consistency and organization:
      
      1. Rails Versioning:
         - The Gemfile indicates an experimental or custom Rails 8.0+ usage.
         - Ensure Rails conventions remain consistent with community standards to prevent compatibility issues.
      
      2. Multi-Database Support:
         - Both PostgreSQL (pg) and MySQL (mysql2) may be used. Confirm if the app truly requires multiple databases or if certain DB adapters are legacy.
         - MySQL usage in this repository is strictly read-only for accessing legacy data from the previous app.
         - Keep DB-specific configurations (e.g., for Postgres or MySQL) well-separated or annotated.
      
      3. Hotwire/Stimulus Integration:
         - Gems and NPM packages related to turbo-rails, stimulus-rails, and hotwire_combobox govern real-time UI updates.
         - Keep JavaScript controllers in the proper app/javascript/controllers directory and follow Stimulus naming conventions.
         - Use Turbo frames and streams sensibly to improve responsiveness without bloating application logic.
      
      4. Asset Pipeline & Build Tools:
         - This project uses a Tailwind + ESBuild + PostCSS toolchain, plus importmap-rails or propshaft for asset management (rather than Webpacker).
         - Adhere to the standard Rails asset structure (app/assets, app/javascript, etc.) and keep build scripts updated to compile styles and scripts effectively.
      
      5. External Services & Deployment:
         - Kamal is used for Docker container orchestration, possibly deploying to AWS or similar. Keep Docker- and environment-related files clean and well-documented.
         - Puma, Thruster, and Bootsnap exist for performance and concurrency enhancements. Ensure these are configured correctly for each environment.
      
      6. Domain-Specific Models:
         - Tables and modules prefixed with aspire_ or safety_report_ imply specialized business logic. Keep these domains organized (e.g., within app/models or domain-specific modules).
         - Features like with_advisory_lock, ruby-limiter, and pg_search suggest concurrency handling, rate-limiting, and text search. Document usage thoroughly.
      
      7. Overall Project Structure:
         - Place related code in appropriate subdirectories (controllers, models, services, channels, etc.) to maintain a clear separation of concerns.
         - Keep environment-specific configurations in config/environments and config/credentials to avoid cross-pollution and security issues.
         - Follow naming conventions and best practices for consistency across the codebase.
      
      By following these guidelines and continuing to refine them as the project evolves, the team can maintain a coherent, consistent, and scalable Rails application.

examples:
  - input: |
      # Bad example: Placing DB adapters, controllers, and domain objects in arbitrary folders outside app, config, or db.
      # Good example: Properly organizing domain-specific code in app/models/aspire, ensuring DB adapter gems (pg, mysql2) are declared only as needed in the Gemfile.
    output: "Ensure that project directories, environment setups, and advanced tool configurations follow cohesive Rails standards for maintainability."

metadata:
  priority: high
  version: 1.2
  related_rules:
    - models_standard
    - controllers_standard
  responsibility: "Define and enforce overall Rails project organization, including multi-database conventions and advanced deployment configurations."
</rule>