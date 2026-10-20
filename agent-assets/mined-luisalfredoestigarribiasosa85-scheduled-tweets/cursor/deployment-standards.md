---
description: Enforces best practices for deploying a Rails application without Capistrano, covering asset precompilation, environment configuration, and CI/CD integration.
globs:
  - "config/deploy/**/*"
  - "Gemfile"
---

# Deployment

<rule>
name: deployment_standard
description: Provides guidelines for deploying a Rails application, ensuring that environment configurations, asset precompilation via the asset pipeline, and CI/CD integrations are set up properly without relying on Capistrano.

filters:
  - type: path
    pattern: "^(config/deploy/.*|Gemfile)$"
    # Applies to deployment configuration files and the Gemfile

actions:
  - type: suggest
    message: |
      Deployment configurations should:
      1. Separate environment-specific settings clearly.
      2. Precompile assets using the Rails asset pipeline (e.g., via `rake assets:precompile`).
      3. Integrate with CI/CD pipelines (like GitHub Actions, GitLab CI, etc.) to automate tests and deployment.
      4. Use environment variables to manage sensitive data.
      5. Include clear documentation for deployment procedures.

examples:
  - input: |
      # Bad example: Hardcoding environment settings and missing asset precompilation steps.
      # config/deploy/production.rb
      ENV['RAILS_ENV'] = "production"
      # Missing asset precompilation and CI/CD integration details.
    output: "Avoid hardcoding configurations; leverage environment variables and include steps for asset precompilation and CI/CD integration."
  - input: |
      # Good example: Deployment configuration snippet for CI/CD integration.
      # config/deploy/production.rb
      Rails.application.configure do
        config.cache_classes = true
        config.eager_load = true
        # Other production settings...
      end
      # CI/CD pipeline should include:
      #   - Setting ENV variables securely
      #   - Running `rake assets:precompile` before deployment
    output: "Deployment configuration clearly separates production settings and outlines CI/CD requirements without relying on Capistrano."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project_standard
  responsibility: "Standardize deployment procedures and environment configurations for Rails applications without Capistrano"
</rule>
