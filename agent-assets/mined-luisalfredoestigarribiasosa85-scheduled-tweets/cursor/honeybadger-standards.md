---
description: Enforces best practices for integrating Honeybadger for error monitoring in a Rails project.
globs:
  - "config/initializers/honeybadger.rb"
  - "Gemfile"
---

# Honeybadger Integration

<rule>
name: honeybadger_standard
description: Provides guidelines for integrating Honeybadger to monitor and report errors in a Rails application, ensuring secure configuration and proper usage.

filters:
  - type: path
    pattern: "^(config/initializers/honeybadger\\.rb|Gemfile)$"
    # Applies to the Honeybadger initializer and Gemfile entries related to Honeybadger

actions:
  - type: suggest
    message: |
      Honeybadger should be integrated as follows:
      1. Include the Honeybadger gem in the Gemfile.
      2. Configure Honeybadger in an initializer using environment variables for the API key.
      3. Ensure that Honeybadger is set to capture exceptions and report them in the appropriate environment.
      4. Document any custom error notifications or filters applied.
      5. Regularly review Honeybadger settings to ensure compliance with security and performance standards.

examples:
  - input: |
      # Bad example: Honeybadger gem installed without proper configuration.
      # Gemfile
      gem 'honeybadger'
      # config/initializers/honeybadger.rb with hardcoded API key:
      Honeybadger.configure do |config|
        config.api_key = "1234567890abcdef"
      end
    output: "Avoid hardcoding sensitive API keys; configure Honeybadger using environment variables."
  - input: |
      # Good example: Proper Honeybadger integration.
      # Gemfile
      gem 'honeybadger'
      # config/initializers/honeybadger.rb
      Honeybadger.configure do |config|
        config.api_key = ENV['HONEYBADGER_API_KEY']
        config.env = Rails.env
        config.exceptions.ignore += ['CustomIgnoredError']
      end
    output: "Honeybadger is properly integrated with secure API key management and custom configuration."

metadata:
  priority: high
  version: 1.0
  related_rules:
    - logging_standard
    - rails_project_standard
  responsibility: "Ensure secure and effective integration of Honeybadger for error monitoring in the Rails application"
</rule>
