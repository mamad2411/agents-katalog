---
description: Enforces guidelines for creating and using concerns to promote code reusability and maintainability in Rails.
globs:
  - "app/models/concerns/**/*.rb"
  - "app/controllers/concerns/**/*.rb"
---

# Concerns

<rule>
name: concerns_standard
description: Ensures that concerns encapsulate shared functionality across models or controllers, keeping code DRY and modular.

filters:
  - type: path
    pattern: "app/(models|controllers)/concerns/.*\\.rb$"
    # Applies to concern files in models and controllers directories

actions:
  - type: suggest
    message: |
      Concerns should:
      1. Encapsulate reusable code applicable to multiple classes.
      2. Be clearly named to reflect their functionality.
      3. Remain decoupled from specific class implementations.
      4. Include documentation and comments for clarity.
      5. Be used only when shared functionality is needed, to avoid overcomplication.

examples:
  - input: |
      # Bad example: A concern with an unclear purpose and tight coupling
      module MiscMethods
        def do_something
          # ambiguous code
        end
      end
    output: "Concerns should be focused and clearly named to indicate their specific responsibility."
  - input: |
      # Good example
      module Trackable
        extend ActiveSupport::Concern

        included do
          has_many :activities
        end

        def track_activity(action)
          activities.create(action: action)
        end
      end
    output: "The Trackable concern cleanly encapsulates functionality for tracking activities and is well documented."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project
  responsibility: "Standardize the creation and use of concerns for code reusability"
</rule>
