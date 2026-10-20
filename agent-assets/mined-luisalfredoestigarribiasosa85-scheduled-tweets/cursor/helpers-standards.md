---
description: Enforces best practices for writing helper methods to maintain clean, DRY, and well-organized code in Rails views and controllers.
globs:
  - "app/helpers/**/*.rb"
---

# Helpers

<rule>
name: helpers_standard
description: Provides guidelines for writing and organizing helper methods to ensure they are reusable, concise, and focused solely on presentation logic.

filters:
  - type: path
    pattern: "^app/helpers/.*\\.rb$"
    # Applies to helper files in the app/helpers directory

actions:
  - type: suggest
    message: |
      Helper methods should:
      1. Focus exclusively on presentation logic.
      2. Exclude business logic, which belongs in models or controllers.
      3. Include clear comments and documentation.
      4. Follow naming conventions that reflect their functionality.
      5. Be grouped logically based on their area of responsibility.

examples:
  - input: |
      # Bad example: Helper containing business logic
      module UsersHelper
        def formatted_user(user)
          # Complex logic mixing presentation with business rules
        end
      end
    output: "Helpers should focus solely on formatting and presentation, not on business logic."
  - input: |
      # Good example
      module UsersHelper
        def formatted_date(date)
          date.strftime("%B %d, %Y")
        end
      end
    output: "Helper method is concise, focused on presentation, and clearly documented."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project
  responsibility: "Standardize helper method development to ensure maintainable view logic"
</rule>
