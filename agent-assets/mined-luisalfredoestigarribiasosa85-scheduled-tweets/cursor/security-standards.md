---
description: Enforces security best practices across a Rails project, including protection against common vulnerabilities.
globs:
  - "app/controllers/**/*.rb"
  - "app/models/**/*.rb"
  - "config/**/*.rb"
---

# Security

<rule>
name: security_standard
description: Ensures that security practices such as CSRF protection, strong parameter filtering, and secure coding practices are followed throughout the Rails project.

filters:
  - type: path
    pattern: "^(app/controllers/.*\\.rb|app/models/.*\\.rb|config/.*\\.rb)$"
    # Applies to controllers, models, and configuration files

actions:
  - type: suggest
    message: |
      Security best practices should:
      1. Implement CSRF protection in controllers.
      2. Use strong parameters to filter input.
      3. Sanitize user input where applicable.
      4. Avoid storing sensitive data in plain text.
      5. Follow Rails security guidelines and regularly update dependencies.

examples:
  - input: |
      # Bad example: Controller without CSRF protection and unfiltered parameters.
      class SessionsController < ApplicationController
        def create
          user = User.find_by(email: params[:email])
          # Missing parameter sanitization
        end
      end
    output: "Ensure CSRF protection and strong parameter filtering are in place."
  - input: |
      # Good example.
      class SessionsController < ApplicationController
        protect_from_forgery with: :exception

        def create
          user = User.find_by(email: params.require(:session).permit(:email)[:email])
          # Proper filtering and security measures in place
        end
      end
    output: "Controller implements CSRF protection and uses strong parameters for input filtering."

metadata:
  priority: high
  version: 1.0
  related_rules:
    - controllers_standard
  responsibility: "Enforce security best practices across controllers, models, and configuration"
</rule>
