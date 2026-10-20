---
description: Enforces standards for Rails view templates, including integration with StimulusJS/Hotwire.
globs:
  - "app/views/**/*.erb"
---

# Views

<rule>
name: views_standard
description: Ensures that Rails view templates are organized, adhere to DRY principles, and properly integrate StimulusJS/Hotwire for enhanced interactivity.

filters:
  - type: path
    pattern: "^app/views/.*\\.(erb)$"
    # Applies to all ERB view templates

actions:
  - type: suggest
    message: |
      Views should:
      1. Use partials to avoid code duplication.
      2. Maintain separation of presentation logic from business logic.
      3. Integrate StimulusJS/Hotwire cleanly for dynamic interactions.
      4. Follow standard naming and directory conventions.
      5. Include descriptive comments where necessary.

examples:
  - input: |
      # Bad example: Monolithic view with embedded logic and inline JavaScript.
      <%= if user.admin? %>
        <script>alert('Admin')</script>
      <% end %>
    output: "Avoid embedding complex logic and inline JavaScript in view templates."
  - input: |
      # Good example: View using partials and StimulusJS for interactivity.
      <%= render 'shared/header' %>
      <div data-controller="notifications">
        <!-- StimulusJS will manage dynamic behavior -->
      </div>
    output: "View template is well-structured, using partials and StimulusJS effectively."

metadata:
  priority: medium
  version: 1.0
  related_rules:
    - rails_project_standard
  responsibility: "Standardize the organization and integration of Rails view templates"
</rule>
