---
description: Enforces best practices for defining RESTful routes in a Rails project.
globs:
  - "config/routes.rb"
---

# Routes

<rule>
name: routes_standard
description: Ensures that the routes file adheres to Rails RESTful conventions, including proper nesting, resource naming, and custom route constraints where necessary.

filters:
  - type: path
    pattern: "^config/routes\\.rb$"
    # Applies to the main routes file

actions:
  - type: suggest
    message: |
      Routes should:
      1. Follow RESTful conventions with resources.
      2. Use nesting judiciously to reflect resource hierarchies.
      3. Include custom routes only when necessary.
      4. Keep the routes file organized and commented.
      5. Avoid overly complex route definitions.

examples:
  - input: |
      # Bad example: Overly nested and unorganized routes.
      Rails.application.routes.draw do
        resources :users do
          resources :posts do
            resources :comments
          end
        end
      end
    output: "Avoid deep nesting; consider flattening routes or using shallow nesting."
  - input: |
      # Good example: Clear RESTful routes with shallow nesting.
      Rails.application.routes.draw do
        resources :users do
          resources :posts, shallow: true
        end
      end
    output: "Routes follow RESTful conventions and use shallow nesting effectively."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project_standard
  responsibility: "Standardize the definition of RESTful routes in a Rails application"
</rule>
